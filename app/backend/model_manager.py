"""Shared Model Manager for Alexa Farms Multimodal Plant Assistant.

Provides:
- Thread-safe singleton model lifecycle management (Model 1 & Model 2 V4).
- Guaranteed single-instance initialization (no duplicate models or reloading).
- Memory-safe checkpoint loading (immediate deletion of training/optimizer states).
- PyTorch CPU thread capping (1 thread) to protect Render 512MB / 0.5 vCPU containers.
- Sequential execution support (Model 2 is never loaded when crop is rejected/uncertain).
- Explicit heap reclamation (gc.collect + glibc malloc_trim).
- Detailed process memory telemetry before and after model operations.
"""

from __future__ import annotations

import gc
import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Optional, Tuple

import torch
import torch.nn as nn

logger = logging.getLogger(__name__)

# Configure PyTorch CPU execution for low-memory container environments
# Prevents multi-threaded OpenMP pool memory explosion on shared cloud host vCPUs
torch.set_num_threads(1)
if hasattr(torch, "set_num_interop_threads"):
    try:
        torch.set_num_interop_threads(1)
    except Exception:
        pass


def get_process_rss_mb() -> float:
    """Return the current resident set size (RSS) of the process in megabytes."""
    try:
        import psutil
        p = psutil.Process(os.getpid())
        return p.memory_info().rss / (1024 * 1024)
    except Exception:
        try:
            # Fallback for Linux /proc/self/statm
            with open("/proc/self/statm", "r") as f:
                fields = f.read().split()
                # 2nd field is resident pages
                return (int(fields[1]) * 4096) / (1024 * 1024)
        except Exception:
            return 0.0


def release_memory():
    """Trigger Python garbage collection and release freed C-heap memory back to the kernel."""
    gc.collect()
    try:
        import ctypes
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
    except Exception:
        pass


class SharedModelManager:
    """Centralized thread-safe singleton manager for Model 1 and Model 2 V4."""

    _instance: Optional["SharedModelManager"] = None
    _init_lock = threading.Lock()

    def __new__(cls) -> "SharedModelManager":
        if cls._instance is None:
            with cls._init_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self._lock = threading.Lock()
        self._model1: Optional[nn.Module] = None
        self._idx_to_class: Optional[dict[int, str]] = None
        self._class_to_idx: Optional[dict[str, int]] = None
        self._model2_v4: Optional[Any] = None
        self._sequential_swapping: bool = os.environ.get(
            "SEQUENTIAL_MODEL_SWAPPING", "true"
        ).lower() in ("true", "1", "yes")
        self._initialized = True
        logger.info(
            f"[MODEL_MANAGER] SharedModelManager initialized. Initial RSS: {get_process_rss_mb():.1f} MB, "
            f"Sequential Swapping: {self._sequential_swapping}"
        )

    @property
    def is_sequential_swapping_enabled(self) -> bool:
        return self._sequential_swapping

    @is_sequential_swapping_enabled.setter
    def is_sequential_swapping_enabled(self, val: bool) -> None:
        self._sequential_swapping = bool(val)

    @property
    def is_model1_loaded(self) -> bool:
        return self._model1 is not None

    @property
    def is_model2_loaded(self) -> bool:
        return self._model2_v4 is not None

    @property
    def model1(self) -> Optional[nn.Module]:
        return self._model1

    @property
    def idx_to_class(self) -> Optional[dict[int, str]]:
        return self._idx_to_class

    @property
    def class_to_idx(self) -> Optional[dict[str, int]]:
        return self._class_to_idx

    @property
    def model2(self) -> Optional[Any]:
        return self._model2_v4

    def get_model1(self) -> Tuple[nn.Module, dict[int, str], dict[str, int]]:
        """Retrieve or initialize the cached Model 1 neural network (guaranteed singleton)."""
        if self._model1 is None:
            with self._lock:
                if self._model1 is None:
                    from app.backend.config import (
                        DEVICE,
                        DEVICE_NAME,
                        MODEL1_CHECKPOINT,
                        MODEL1_CLASS_MAPPING,
                        MODEL1_CONFIG,
                    )
                    from model1_test_app.inference import load_model

                    if not MODEL1_CHECKPOINT.exists():
                        raise FileNotFoundError(
                            f"Model 1 checkpoint not found at: '{MODEL1_CHECKPOINT}'."
                        )

                    rss_before = get_process_rss_mb()
                    logger.info(
                        f"[MODEL_MANAGER] Loading Model 1 from {MODEL1_CHECKPOINT} onto {DEVICE_NAME}... "
                        f"(RSS before: {rss_before:.1f} MB)"
                    )
                    t0 = time.time()

                    m1, i2c, c2i, _, _ = load_model(
                        checkpoint_path=MODEL1_CHECKPOINT,
                        mapping_path=MODEL1_CLASS_MAPPING,
                        config_path=MODEL1_CONFIG,
                        device=DEVICE,
                    )
                    m1.eval()

                    self._model1 = m1
                    self._idx_to_class = i2c
                    self._class_to_idx = c2i

                    release_memory()
                    rss_after = get_process_rss_mb()
                    logger.info(
                        f"[MODEL_MANAGER] Model 1 (52 crops) loaded in {time.time()-t0:.2f}s. "
                        f"RSS after: {rss_after:.1f} MB (Delta: +{rss_after - rss_before:.1f} MB)"
                    )
        return self._model1, self._idx_to_class, self._class_to_idx

    def get_model2(self) -> Any:
        """Retrieve or initialize the cached Model 2 V4 classifier (guaranteed singleton)."""
        if self._model2_v4 is None:
            with self._lock:
                if self._model2_v4 is None:
                    from app.backend.config import (
                        CROP_DISEASE_MAPPING,
                        DEVICE,
                        DEVICE_NAME,
                        MODEL2_CHECKPOINT,
                        MODEL2_CLASS_MAPPING,
                    )
                    from models.model2_classifier_v4.predict import Model2DiseaseClassifierV4

                    if not MODEL2_CHECKPOINT.exists():
                        raise FileNotFoundError(
                            f"Model 2 V4 checkpoint not found at: '{MODEL2_CHECKPOINT}'."
                        )

                    rss_before = get_process_rss_mb()
                    logger.info(
                        f"[MODEL_MANAGER] Loading Model 2 V4 from {MODEL2_CHECKPOINT} onto {DEVICE_NAME}... "
                        f"(RSS before: {rss_before:.1f} MB)"
                    )
                    t0 = time.time()

                    m2 = Model2DiseaseClassifierV4(
                        checkpoint_path=MODEL2_CHECKPOINT,
                        class_mapping_path=MODEL2_CLASS_MAPPING,
                        crop_disease_map_path=CROP_DISEASE_MAPPING,
                        device=str(DEVICE),
                        uncertainty_threshold=0.40,
                        margin_threshold=0.05,
                    )
                    m2.model.eval()

                    self._model2_v4 = m2

                    release_memory()
                    rss_after = get_process_rss_mb()
                    logger.info(
                        f"[MODEL_MANAGER] Model 2 V4 ({m2.num_classes} classes) loaded in {time.time()-t0:.2f}s. "
                        f"RSS after: {rss_after:.1f} MB (Delta: +{rss_after - rss_before:.1f} MB)"
                    )
        return self._model2_v4

    def unload_model1(self) -> None:
        """Completely release Model 1 neural network and free resident memory."""
        with self._lock:
            if self._model1 is not None:
                rss_before = get_process_rss_mb()
                self._model1 = None
                release_memory()
                rss_after = get_process_rss_mb()
                logger.info(
                    f"[MODEL_MANAGER] Model 1 unloaded. RSS: {rss_before:.1f} MB -> {rss_after:.1f} MB "
                    f"(Reclaimed: {rss_before - rss_after:.1f} MB)"
                )

    def unload_model2(self) -> None:
        """Completely release Model 2 V4 classifier and free resident memory."""
        with self._lock:
            if self._model2_v4 is not None:
                rss_before = get_process_rss_mb()
                if hasattr(self._model2_v4, "model"):
                    self._model2_v4.model = None
                self._model2_v4 = None
                release_memory()
                rss_after = get_process_rss_mb()
                logger.info(
                    f"[MODEL_MANAGER] Model 2 V4 unloaded. RSS: {rss_before:.1f} MB -> {rss_after:.1f} MB "
                    f"(Reclaimed: {rss_before - rss_after:.1f} MB)"
                )

    def unload_whisper(self) -> None:
        """Release any cached Whisper speech model instances and free C-heap memory."""
        try:
            from audio.test_audio import unload_whisper
            unload_whisper()
        except Exception:
            pass

    def unload_all(self) -> None:
        """Release all neural models (Model 1, Model 2, Whisper) to minimize memory footprint."""
        self.unload_model1()
        self.unload_model2()
        self.unload_whisper()

    def get_memory_telemetry(self) -> dict[str, Any]:
        """Return memory diagnostics for logging and operational health status."""
        rss = get_process_rss_mb()
        return {
            "rss_mb": round(rss, 2),
            "model1_loaded": self.is_model1_loaded,
            "model2_loaded": self.is_model2_loaded,
            "sequential_swapping": self.is_sequential_swapping_enabled,
            "render_limit_mb": 512.0,
            "headroom_mb": round(512.0 - rss, 2),
        }


# Global singleton instance
model_manager = SharedModelManager()
