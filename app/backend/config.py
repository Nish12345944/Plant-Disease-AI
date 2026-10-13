"""Backend Configuration for Alexa Farms Multimodal Testing App."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import torch

# Base project root
BACKEND_DIR = Path(__file__).resolve().parent
APP_DIR = BACKEND_DIR.parent
PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", str(APP_DIR.parent))).resolve()

# Ensure project root is in sys.path so modules (audio, video, router, pipeline, model1_test_app) import cleanly
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def _resolve_model_path(env_var: str, default_subpath: Path) -> Path:
    val = os.environ.get(env_var)
    if val:
        p = Path(val)
        return (PROJECT_ROOT / p).resolve() if not p.is_absolute() else p.resolve()
    return default_subpath.resolve()

# Flag to permit legacy / test checkpoints (disabled by default in production)
ALLOW_LEGACY_MODEL1 = os.environ.get("ALLOW_LEGACY_MODEL1", "false").lower() in ("true", "1", "yes")

# Model 1 Paths (Expanded EfficientNet-B2 46-Crop Classifier for Production)
MODEL1_CHECKPOINT = _resolve_model_path(
    "MODEL1_CHECKPOINT", PROJECT_ROOT / "models" / "model1_expanded" / "best_model.pth"
)
MODEL1_CLASS_MAPPING = _resolve_model_path(
    "MODEL1_CLASS_MAPPING", PROJECT_ROOT / "models" / "model1_expanded" / "class_mapping.json"
)
MODEL1_CONFIG = _resolve_model_path(
    "MODEL1_CONFIG", PROJECT_ROOT / "models" / "model1_expanded" / "config.json"
)

# Model 2 Paths (Retrained V2 144-Class Disease Classifier for Production)
MODEL2_CHECKPOINT = _resolve_model_path(
    "MODEL2_CHECKPOINT", PROJECT_ROOT / "models" / "model2_retraining_v2" / "best_model.pth"
)
MODEL2_CLASS_MAPPING = _resolve_model_path(
    "MODEL2_CLASS_MAPPING", PROJECT_ROOT / "models" / "model2_retraining_v2" / "class_mapping.json"
)
MODEL2_CONFIG = _resolve_model_path(
    "MODEL2_CONFIG", PROJECT_ROOT / "models" / "model2_retraining_v2" / "config.json"
)

_env_crop_disease_map = os.environ.get("CROP_DISEASE_MAPPING")
if _env_crop_disease_map:
    _cdm_p = Path(_env_crop_disease_map)
    CROP_DISEASE_MAPPING = (PROJECT_ROOT / _cdm_p).resolve() if not _cdm_p.is_absolute() else _cdm_p.resolve()
else:
    CROP_DISEASE_MAPPING = (PROJECT_ROOT / "models" / "model2_retraining_v2" / "crop_disease_mapping.json").resolve()

# Deployment & Memory Tuning Flags
EAGER_LOAD_MODELS = os.environ.get("EAGER_LOAD_MODELS", "false").lower() in ("true", "1", "yes")
WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "tiny")

# Media Extensions
SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
SUPPORTED_VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v"}
SUPPORTED_AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".opus", ".wma", ".aac", ".webm"}

# Temp storage for uploaded audio, images, and videos during session
TEMP_MEDIA_DIR = Path(os.environ.get("TEMP_MEDIA_DIR", str(PROJECT_ROOT / "temp_multimodal_uploads")))
try:
    TEMP_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

# Hardware execution device
_cuda_available = torch.cuda.is_available() and torch.cuda.device_count() > 0
DEVICE = torch.device("cuda" if _cuda_available else "cpu")
DEVICE_NAME = f"CUDA — {torch.cuda.get_device_name(0)}" if _cuda_available else "CPU"

if not _cuda_available:
    # Optimize CPU inference thread count to prevent thread thrashing on limited-core / container environments
    _optimal_threads = min(4, max(1, os.cpu_count() or 1))
    torch.set_num_threads(_optimal_threads)
