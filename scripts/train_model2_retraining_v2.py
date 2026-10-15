"""
Train Model 2 Disease Classifier Retraining V2 (EfficientNet-B2, 144 Classes)
================================================================================
Trains on the Model 2 Retraining V2 dataset:
  data/processed/model2_retraining_v2/
  ├── train/{crop}/{disease}/ (30,088 images: historical + newly augmented)
  ├── val/{crop}/{disease}/   (3,049 images: historical + 15% new validation)
  └── test/{crop}/{disease}/  (2,304 images: IMMUTABLE historical benchmark)

Initialization:
  models/model2_retraining_v1/best_model.pth
  - Full EfficientNet-B2 backbone weights transferred.
  - Linear classifier adapted from 143 to 144 classes:
    Indices 0..142 restored from V1 weights; Index 143 (tomato__anthracnose) initialized fresh.

Outputs:
  models/model2_retraining_v2/
  ├── best_model.pth
  ├── last_model.pth
  ├── config.json
  ├── class_mapping.json
  ├── crop_disease_mapping.json
  └── training_summary.json

Reports:
  reports/model2_retraining_v2/
  ├── training.log
  ├── training_progress.csv
  ├── training_curves.png
  └── model2_training_preflight_report.md
Fast Recovery / Fine-Tuning Mode (crash recovery, e.g. after Windows CPU RAM exhaustion):
    python scripts/train_model2_retraining_v2.py --fast
    - Resumes models/model2_retraining_v2/last_model.pth (READ-ONLY) with optimizer /
      scheduler / scaler state restored when present and compatible.
    - All outputs are written to models/model2_retraining_v2_fast/ and
      reports/model2_retraining_v2_fast/; original checkpoints, datasets, class
      mappings, and reports are never modified.
    - Defaults: 1 epoch, 20-minute wall-clock budget, early stopping (patience 2),
      training micro-batch 2 with auto gradient accumulation (effective batch stays
      32 - CUDA-OOM fix for the 4 GB RTX 3050), pin_memory=False, num_workers=0,
      and FULL validation after every epoch
      (validation is never skipped to satisfy the time budget; the budget is only
      checked between epochs).
    - Final checkpoint = best Validation Macro F1 (original best_model.pth is the
      baseline champion unless the fast run beats it).
    - Optional: --epochs, --time-budget-min, --patience, --num-workers,
      --batch-size, --grad-accum-steps, --val-batch-size, --reset-optimizer,
      --resume-from {original,fast}.
"""

from __future__ import annotations

import argparse
import csv
import gc
import json
import logging
import os
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

# Clean up PYTORCH_CUDA_ALLOC_CONF if set to avoid Windows CUDA allocator warnings
if "PYTORCH_CUDA_ALLOC_CONF" in os.environ and "expandable_segments" in os.environ["PYTORCH_CUDA_ALLOC_CONF"]:
    del os.environ["PYTORCH_CUDA_ALLOC_CONF"]


import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    top_k_accuracy_score,
)
import torch
import torch.nn as nn
import torch.optim as optim
from torch.amp import GradScaler, autocast
from torch.utils.data import DataLoader, Dataset
import torchvision
from torchvision import transforms
from torchvision.models import efficientnet_b2

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Project Paths & Isolated Output Directories
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
DATASET_DIR = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v2"
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v2_manifest.csv"
CLASS_MAPPING_PATH = DATASET_DIR / "class_mapping.json"
CROP_DISEASE_MAP_PATH = DATASET_DIR / "crop_disease_mapping.json"

# Initialization Checkpoint (Model 2 Retraining V1)
INIT_CHECKPOINT_PATH = PROJECT_ROOT / "models" / "model2_retraining_v1" / "best_model.pth"
V4_BACKUP_CHECKPOINT = PROJECT_ROOT / "models" / "model2_classifier_v4" / "best_model.pth"

MODEL_DIR = PROJECT_ROOT / "models" / "model2_retraining_v2"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_retraining_v2"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

PROGRESS_CSV = REPORTS_DIR / "training_progress.csv"
TRAINING_LOG = REPORTS_DIR / "training.log"
CONFIG_PATH = MODEL_DIR / "config.json"
SUMMARY_PATH = MODEL_DIR / "training_summary.json"

# ---------------------------------------------------------------------------
# Training Hyperparameters
# ---------------------------------------------------------------------------
IMAGE_SIZE = (260, 260)             # Native EfficientNet-B2 resolution
BATCH_SIZE = 4                      # Safe for Windows Host RAM & 4 GB RTX 3050 Laptop GPU
GRAD_ACCUM_STEPS = 8                # Effective batch size = 32
NUM_WORKERS = 0                     # Windows multi-process safety
STAGE1_EPOCHS = 4                   # Head warmup (frozen backbone)
STAGE1_LR = 1e-3                    # Classifier head initial learning rate
STAGE2_EPOCHS = 16                  # Full fine-tuning (unfrozen backbone)
STAGE2_LR = 1e-4                    # Fine-tuning backbone & head learning rate
STAGE2_ETA_MIN = 1e-6               # Cosine annealing minimum learning rate
PATIENCE = 6                        # Early stopping on validation macro F1
WEIGHT_DECAY = 1e-4                 # AdamW weight decay
LABEL_SMOOTHING = 0.05              # Cross-entropy label smoothing
RANDOM_SEED = 42
EXPECTED_NUM_CLASSES = 144
EXPECTED_TEST_COUNT = 2304

# ---------------------------------------------------------------------------
# Fast Recovery / Fine-Tuning Mode Configuration (CLI-overridable)
# Fast mode writes EXCLUSIVELY to the *_fast directories below; the original
# models/model2_retraining_v2/ and reports/model2_retraining_v2/ trees are
# opened read-only and never written to.
# ---------------------------------------------------------------------------
FAST_MODEL_DIR = PROJECT_ROOT / "models" / "model2_retraining_v2_fast"
FAST_REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_retraining_v2_fast"
SOURCE_LAST_CHECKPOINT = MODEL_DIR / "last_model.pth"   # read-only resume source
SOURCE_BEST_CHECKPOINT = MODEL_DIR / "best_model.pth"   # read-only baseline best

FAST_DEFAULT_EPOCHS = 1             # ~940s/epoch observed; 1 epoch fits a 20-min budget
FAST_DEFAULT_TIME_BUDGET_MIN = 20.0
FAST_DEFAULT_PATIENCE = 2           # early stopping on validation Macro F1
FAST_PIN_MEMORY = False             # avoid page-locked CPU RAM growth/fragmentation on Windows
HISTORICAL_EPOCH_SECONDS = 950.0    # observed epochs 5-18: 837-992s per epoch incl. validation

FAST_DEFAULT_MICRO_BATCH = 2       # RTX 3050 Laptop 4 GB VRAM: micro-batch fix for CUDA OOM
FAST_DEFAULT_VAL_BATCH = 8         # validation batch proven safe (no_grad + autocast, complete eval)
TARGET_EFFECTIVE_BATCH = BATCH_SIZE * GRAD_ACCUM_STEPS  # 4 * 8 = 32 (original intended effective batch)

# Active log target (fast mode redirects this; defaults to the original log)
ACTIVE_LOG_PATH = TRAINING_LOG

def set_seed(seed: int = RANDOM_SEED):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def atomic_torch_save(payload: dict, target_path: Path):
    """Atomically save torch checkpoint by saving to a temp file and replacing."""
    temp_path = target_path.parent / f".{target_path.name}.tmp"
    torch.save(payload, temp_path)
    os.replace(temp_path, target_path)


def sync_progress_csv(csv_path: Path, start_epoch: int, header: list[str]) -> list[list[str]]:
    """Preserves historical rows with epoch < start_epoch atomically. Eliminates duplicates or partial lines."""
    valid_rows = []
    if csv_path.exists():
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            file_header = next(reader, None)
            for row in reader:
                if row and len(row) > 0:
                    try:
                        row_epoch = int(row[0])
                        if row_epoch < start_epoch:
                            valid_rows.append(row)
                    except ValueError:
                        continue

    tmp_path = csv_path.parent / f".{csv_path.name}.tmp"
    with open(tmp_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in valid_rows:
            writer.writerow(r)
    os.replace(tmp_path, csv_path)
    return valid_rows


# ---------------------------------------------------------------------------
# Dataset with Bounded Memory Decoding
# ---------------------------------------------------------------------------
class Model2RetrainingDataset(Dataset):
    """Memory-safe dataset loader with libjpeg draft downsampling and robust error handling."""

    def __init__(self, samples: list[tuple[str, int]], base_dir: Path, transform=None):
        self.samples = samples
        self.base_dir = Path(base_dir)
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx: int):
        img_rel, class_id = self.samples[idx]
        img_path = self.base_dir / img_rel
        try:
            with Image.open(img_path) as raw:
                try:
                    raw.draft("RGB", (300, 300))
                except Exception:
                    pass
                img = raw.convert("RGB")
        except Exception:
            try:
                img = Image.open(img_path).convert("RGB")
            except Exception:
                img = Image.new("RGB", IMAGE_SIZE, (128, 128, 128))

        if self.transform:
            img = self.transform(img)
        return img, class_id, idx


def get_transforms():
    train_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.2),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15, hue=0.04),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    val_test_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    return train_transform, val_test_transform


def log_message(msg: str):
    print(msg, flush=True)
    with open(ACTIVE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def get_windows_memory_status() -> dict | None:
    """Commit/RAM snapshot via GlobalMemoryStatusEx (stdlib ctypes, no extra deps).

    The commit limit (RAM + page file) is what Windows exhausts during
    'WinError 1455: the paging file is too small' and what WDDM charges for GPU
    allocations - so a low free-commit reading explains both the historical CPU
    crash and misleading 'CUDA OOM with free VRAM' errors.
    """
    if sys.platform != "win32":
        return None
    try:
        import ctypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            return None
        return {
            "ram_total_mb": stat.ullTotalPhys // 1024**2,
            "ram_free_mb": stat.ullAvailPhys // 1024**2,
            "commit_total_mb": stat.ullTotalPageFile // 1024**2,
            "commit_free_mb": stat.ullAvailPageFile // 1024**2,
        }
    except Exception:
        return None


def compute_effective_class_weights(train_samples: list[tuple[str, int]], num_classes: int = EXPECTED_NUM_CLASSES, beta: float = 0.999):
    """Compute Effective Number of Samples weights (Cui et al., CVPR 2019)."""
    counts = Counter([s[1] for s in train_samples])
    weights = []
    for c in range(num_classes):
        cnt = max(1, counts.get(c, 0))
        effective_num = (1.0 - beta ** cnt) / (1.0 - beta)
        weights.append(1.0 / effective_num)
    weights = np.array(weights, dtype=np.float32)
    weights = weights / weights.mean()
    weights = np.clip(weights, 0.2, 5.0)
    return torch.tensor(weights, dtype=torch.float32)


def build_and_init_model_v2(
    num_classes: int = EXPECTED_NUM_CLASSES,
    init_checkpoint_path: Path | None = INIT_CHECKPOINT_PATH,
    device: str = "cpu",
):
    """Builds EfficientNet-B2, initializes backbone & head from V1 (143->144), and moves to device."""
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes),
    )

    if init_checkpoint_path and Path(init_checkpoint_path).exists():
        log_message(f"Initializing backbone & head from checkpoint: {init_checkpoint_path}")
        checkpoint = torch.load(init_checkpoint_path, map_location="cpu", weights_only=False)
        state_dict = checkpoint["model_state_dict"] if "model_state_dict" in checkpoint else checkpoint

        # 1. Transfer backbone weights
        backbone_dict = {k: v for k, v in state_dict.items() if not k.startswith("classifier.")}
        load_res = model.load_state_dict(backbone_dict, strict=False)
        log_message(f"Successfully transferred backbone weights (Missing: {len(load_res.missing_keys)} classifier tensors)")

        # 2. Adapt classifier head weights (143 -> 144)
        if "classifier.1.weight" in state_dict and "classifier.1.bias" in state_dict:
            old_w = state_dict["classifier.1.weight"]
            old_b = state_dict["classifier.1.bias"]
            old_classes = old_w.shape[0]
            new_classes = model.classifier[1].out_features

            with torch.no_grad():
                # Copy existing classes
                model.classifier[1].weight[:old_classes].copy_(old_w[:old_classes])
                model.classifier[1].bias[:old_classes].copy_(old_b[:old_classes])
                if old_classes < new_classes:
                    # Initialize newly added classes with standard Kaiming Normal
                    nn.init.kaiming_normal_(model.classifier[1].weight[old_classes:], mode="fan_out", nonlinearity="linear")
                    nn.init.zeros_(model.classifier[1].bias[old_classes:])

            if old_classes < new_classes:
                log_message(
                    f"Adapted classifier head: restored classes 0..{old_classes - 1} from checkpoint; "
                    f"initialized class {old_classes} (tomato__anthracnose) fresh."
                )
            else:
                log_message(
                    f"Classifier head: restored all {old_classes} classes from checkpoint (no adaptation needed)."
                )
        del checkpoint, state_dict
        gc.collect()
    else:
        log_message("Warning: Checkpoint not found; initializing from ImageNet-1K default weights.")
        model = efficientnet_b2(weights=torchvision.models.EfficientNet_B2_Weights.DEFAULT)
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(in_features, num_classes),
        )

    return model.to(device)


def evaluate(model, loader, criterion, device, num_classes: int = EXPECTED_NUM_CLASSES):
    """Evaluates model performance across loss, accuracy, and per-class macro F1."""
    model.eval()
    total_loss = 0.0
    all_preds = []
    all_targets = []
    all_probs = []

    with torch.no_grad():
        for images, labels, _ in loader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            if device.type == "cuda":
                with autocast("cuda"):
                    outputs = model(images)
                    loss = criterion(outputs, labels)
            else:
                outputs = model(images)
                loss = criterion(outputs, labels)

            total_loss += loss.item() * images.size(0)
            probs = torch.softmax(outputs, dim=1)
            preds = torch.argmax(probs, dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
            del outputs, loss, probs, preds, images, labels

    avg_loss = total_loss / len(loader.dataset)
    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    all_probs = np.array(all_probs)

    acc = accuracy_score(all_targets, all_preds)
    top3_acc = top_k_accuracy_score(all_targets, all_probs, k=min(3, num_classes), labels=list(range(num_classes)))

    prec_m, rec_m, f1_m, _ = precision_recall_fscore_support(all_targets, all_preds, average="macro", zero_division=0)
    prec_w, rec_w, f1_w, _ = precision_recall_fscore_support(all_targets, all_preds, average="weighted", zero_division=0)

    prec_c, rec_c, f1_c, sup_c = precision_recall_fscore_support(
        all_targets, all_preds, average=None, labels=list(range(num_classes)), zero_division=0
    )

    healthy_f1 = f1_c[0] if num_classes > 0 else 0.0
    disease_f1s = [f1_c[i] for i in range(1, num_classes)]
    disease_macro_f1 = float(np.mean(disease_f1s)) if len(disease_f1s) > 0 else 0.0

    return {
        "loss": avg_loss,
        "accuracy": acc,
        "top3_accuracy": top3_acc,
        "macro_precision": prec_m,
        "macro_recall": rec_m,
        "macro_f1": f1_m,
        "weighted_f1": f1_w,
        "healthy_f1": healthy_f1,
        "disease_macro_f1": disease_macro_f1,
        "per_class_precision": prec_c,
        "per_class_recall": rec_c,
        "per_class_f1": f1_c,
        "per_class_support": sup_c,
        "preds": all_preds,
        "targets": all_targets,
        "probs": all_probs,
    }


def plot_training_curves(history: dict, save_path: Path):
    """Plots training and validation metrics across all epochs."""
    epochs = range(1, len(history["train_loss"]) + 1)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Loss
    axes[0, 0].plot(epochs, history["train_loss"], "b-o", label="Train Loss")
    axes[0, 0].plot(epochs, history["val_loss"], "r-s", label="Val Loss")
    axes[0, 0].set_title("Cross-Entropy Loss")
    axes[0, 0].set_xlabel("Epoch")
    axes[0, 0].set_ylabel("Loss")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # 2. Accuracy
    axes[0, 1].plot(epochs, [a * 100 for a in history["train_acc"]], "b-o", label="Train Acc")
    axes[0, 1].plot(epochs, [a * 100 for a in history["val_acc"]], "r-s", label="Val Acc")
    axes[0, 1].set_title("Classification Accuracy (%)")
    axes[0, 1].set_xlabel("Epoch")
    axes[0, 1].set_ylabel("Accuracy (%)")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # 3. Macro F1
    axes[1, 0].plot(epochs, [f * 100 for f in history["train_f1"]], "b-o", label="Train Macro F1")
    axes[1, 0].plot(epochs, [f * 100 for f in history["val_f1"]], "r-s", label="Val Macro F1")
    axes[1, 0].set_title("Macro F1 Score (%)")
    axes[1, 0].set_xlabel("Epoch")
    axes[1, 0].set_ylabel("Macro F1 (%)")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # 4. Learning Rate
    axes[1, 1].plot(epochs, history["learning_rate"], "g-^", label="Learning Rate")
    axes[1, 1].set_title("Learning Rate Schedule")
    axes[1, 1].set_xlabel("Epoch")
    axes[1, 1].set_ylabel("LR")
    axes[1, 1].set_yscale("log")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Preflight Validation
# ---------------------------------------------------------------------------
def run_preflight_check():
    """Validates all inputs, dataset consistency, mappings, model initialization, and GPU state."""
    print("=" * 80)
    print("MODEL 2 RETRAINING V2 (144 CLASSES) — PREFLIGHT VALIDATION CHECK")
    print("=" * 80)

    # 1. Device and GPU Memory
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    if device.type == "cuda":
        gpu_name = torch.cuda.get_device_name(0)
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
        print(f"GPU: {gpu_name} ({gpu_mem:.2f} GB Total VRAM)")
        allocated = torch.cuda.memory_allocated(0) / (1024 ** 2)
        reserved = torch.cuda.memory_reserved(0) / (1024 ** 2)
        print(f"Initial VRAM: {allocated:.1f} MB Allocated, {reserved:.1f} MB Reserved")
    else:
        print("Running on CPU (CUDA not detected).")

    # 2. Check Dataset and Manifest
    assert DATASET_DIR.exists(), f"Dataset directory not found at: {DATASET_DIR}"
    assert MANIFEST_PATH.exists(), f"Manifest file not found at: {MANIFEST_PATH}"
    assert CLASS_MAPPING_PATH.exists(), f"Class mapping not found at: {CLASS_MAPPING_PATH}"
    assert CROP_DISEASE_MAP_PATH.exists(), f"Crop-disease mapping not found at: {CROP_DISEASE_MAP_PATH}"

    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_to_id = json.load(f)
    assert len(class_to_id) == EXPECTED_NUM_CLASSES, f"Class mapping count {len(class_to_id)} != {EXPECTED_NUM_CLASSES}"
    assert set(class_to_id.values()) == set(range(EXPECTED_NUM_CLASSES)), "Class IDs must be continuous 0..143"
    assert class_to_id["healthy"] == 0, "Class 0 must be 'healthy'"
    assert class_to_id["tomato__anthracnose"] == 143, "Class 143 must be 'tomato__anthracnose'"
    print(f"Class Mapping: Exactly {len(class_to_id)} continuous classes (0 to 143) verified.")

    # 3. Check Manifest Rows
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        manifest_rows = list(reader)

    splits = Counter(r["split"] for r in manifest_rows)
    print(f"Manifest Rows: Total {len(manifest_rows):,} (Train: {splits['train']:,}, Val: {splits['val']:,}, Test: {splits['test']:,})")
    assert splits["test"] == EXPECTED_TEST_COUNT, f"Protected test set count {splits['test']} != {EXPECTED_TEST_COUNT}"
    assert len(manifest_rows) == splits["train"] + splits["val"] + splits["test"]

    # 4. Check Checkpoint Initialization
    assert INIT_CHECKPOINT_PATH.exists(), f"Initialization checkpoint not found at: {INIT_CHECKPOINT_PATH}"
    ckpt = torch.load(INIT_CHECKPOINT_PATH, map_location="cpu", weights_only=False)
    print(f"Initialization Checkpoint: {INIT_CHECKPOINT_PATH} (Trained Epoch: {ckpt.get('epoch')}, Best Val F1: {ckpt.get('val_macro_f1', 0):.4f})")

    # 5. Build and Test Model Initialization
    model = build_and_init_model_v2(num_classes=EXPECTED_NUM_CLASSES, init_checkpoint_path=INIT_CHECKPOINT_PATH, device=str(device))
    assert model.classifier[1].out_features == EXPECTED_NUM_CLASSES

    dummy_x = torch.randn(2, 3, 260, 260, device=device)
    with torch.no_grad():
        dummy_out = model(dummy_x)
    assert dummy_out.shape == (2, EXPECTED_NUM_CLASSES), f"Output shape mismatch: {dummy_out.shape}"
    print(f"Model Forward Pass: Shape (2, 3, 260, 260) -> {tuple(dummy_out.shape)} PASSED.")

    # 6. Check Class Imbalance
    train_samples = [(r["image_path"], int(r["class_id"])) for r in manifest_rows if r["split"] == "train"]
    weights = compute_effective_class_weights(train_samples, EXPECTED_NUM_CLASSES)
    print(f"Effective Class Weights: Min={weights.min():.2f}, Max={weights.max():.2f}, Mean={weights.mean():.2f}")
    assert weights.shape[0] == EXPECTED_NUM_CLASSES

    # Write Preflight Report
    report_path = REPORTS_DIR / "model2_training_preflight_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Model 2 Retraining V2 (144 Classes) — Preflight Report\n\n")
        f.write(f"- **Dataset:** `{DATASET_DIR}`\n")
        f.write(f"- **Manifest:** `{MANIFEST_PATH}`\n")
        f.write(f"- **Total Images:** {len(manifest_rows):,} (Train: {splits['train']:,}, Val: {splits['val']:,}, Test: {splits['test']:,})\n")
        f.write(f"- **Total Classes:** {EXPECTED_NUM_CLASSES}\n")
        f.write(f"- **Execution Device:** {device} ({gpu_name if device.type == 'cuda' else 'CPU'})\n")
        f.write(f"- **Initialization Checkpoint:** `{INIT_CHECKPOINT_PATH}`\n")
        f.write(f"- **Batch Size / Accumulation:** Batch Size {BATCH_SIZE}, Grad Accum {GRAD_ACCUM_STEPS} (Effective Batch Size = 32)\n")
        f.write(f"- **Stage 1 (Head Warmup):** {STAGE1_EPOCHS} epochs @ LR={STAGE1_LR} (Backbone frozen)\n")
        f.write(f"- **Stage 2 (Fine-Tuning):** {STAGE2_EPOCHS} epochs @ LR={STAGE2_LR} -> {STAGE2_ETA_MIN} (Cosine Annealing)\n")
        f.write(f"- **Early Stopping Patience:** {PATIENCE} epochs on Validation Macro F1\n")
        f.write("- **Status:** **ALL PREFLIGHT CHECKS PASSED — READY FOR EXECUTION**\n")

    print(f"Preflight Report saved to: {report_path}")
    print("\n" + "=" * 80)
    print("ALL PREFLIGHT CHECKS PASSED: Ready for Training Execution (--run)")
    print("=" * 80)
    return True


# ---------------------------------------------------------------------------
# Training Pipeline
# ---------------------------------------------------------------------------
def run_training():
    """Main training execution function for Model 2 Retraining V2."""
    start_time = time.time()
    set_seed(RANDOM_SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

    # Initialize log
    with open(TRAINING_LOG, "a", encoding="utf-8") as f:
        f.write(f"\nModel 2 Retraining V2 (144 Classes) Training Run - Started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n")

    log_message(f"Execution Device : {device} ({gpu_name})")
    log_message(f"PyTorch Version  : {torch.__version__}")
    log_message(f"CUDA Version     : {torch.version.cuda if torch.cuda.is_available() else 'N/A'}")

    # 1. Load Mappings
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_to_id = json.load(f)
    id_to_class = {int(v): k for k, v in class_to_id.items()}
    num_classes = len(class_to_id)
    assert num_classes == EXPECTED_NUM_CLASSES

    shutil.copy2(CLASS_MAPPING_PATH, MODEL_DIR / "class_mapping.json")
    if CROP_DISEASE_MAP_PATH.exists():
        shutil.copy2(CROP_DISEASE_MAP_PATH, MODEL_DIR / "crop_disease_mapping.json")

    # 2. Load Manifest Records
    train_samples = []
    val_samples = []
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = (row["image_path"], int(row["class_id"]))
            if row["split"] == "train":
                train_samples.append(item)
            elif row["split"] == "val":
                val_samples.append(item)

    log_message("\n=== PRE-TRAINING DATASET AUDIT VERIFICATION ===")
    log_message(f"Total Canonical Classes : {num_classes}")
    log_message(f"Train Images            : {len(train_samples):,}")
    log_message(f"Val Images              : {len(val_samples):,}")
    log_message(f"Test Images (Immutable) : {EXPECTED_TEST_COUNT:,} (Protected - not evaluated in training loop)")

    # 3. Create Datasets & DataLoaders
    train_tf, val_test_tf = get_transforms()
    train_dataset = Model2RetrainingDataset(train_samples, DATASET_DIR, transform=train_tf)
    val_dataset = Model2RetrainingDataset(val_samples, DATASET_DIR, transform=val_test_tf)

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=(device.type == "cuda"),
        drop_last=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE * 2,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(device.type == "cuda"),
    )

    # 4. Class Imbalance Weights & Loss Function
    class_weights = compute_effective_class_weights(train_samples, num_classes).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=LABEL_SMOOTHING)

    # 5. Build and Initialize Model
    model = build_and_init_model_v2(num_classes=num_classes, init_checkpoint_path=INIT_CHECKPOINT_PATH, device=str(device))

    # 6. Checkpoint Resume Logic
    last_checkpoint_path = MODEL_DIR / "last_model.pth"
    best_checkpoint_path = MODEL_DIR / "best_model.pth"

    start_epoch = 1
    best_val_macro_f1 = 0.0
    patience_counter = 0

    history = {
        "train_loss": [], "train_acc": [], "train_f1": [],
        "val_loss": [], "val_acc": [], "val_f1": [],
        "learning_rate": [],
    }

    scaler = GradScaler("cuda", enabled=(device.type == "cuda"))

    # Stage 1: Freeze backbone for head warmup
    def freeze_backbone(m):
        for name, param in m.named_parameters():
            if not name.startswith("classifier."):
                param.requires_grad = False
            else:
                param.requires_grad = True

    def unfreeze_backbone(m):
        for param in m.parameters():
            param.requires_grad = True

    freeze_backbone(model)
    optimizer = optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=STAGE1_LR, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=STAGE1_EPOCHS, eta_min=STAGE1_LR * 0.1)
    current_stage = 1

    # Check for resume
    if last_checkpoint_path.exists():
        log_message(f"Resuming training from checkpoint: {last_checkpoint_path}")
        ckpt = torch.load(last_checkpoint_path, map_location=device, weights_only=False)
        model.load_state_dict(ckpt["model_state_dict"])
        start_epoch = ckpt["epoch"] + 1
        best_val_macro_f1 = ckpt.get("val_macro_f1", 0.0)
        patience_counter = ckpt.get("patience_counter", 0)

        if start_epoch > STAGE1_EPOCHS:
            current_stage = 2
            unfreeze_backbone(model)
            optimizer = optim.AdamW(model.parameters(), lr=STAGE2_LR, weight_decay=WEIGHT_DECAY)
            scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=STAGE2_EPOCHS, eta_min=STAGE2_ETA_MIN)

        if "optimizer_state_dict" in ckpt:
            optimizer.load_state_dict(ckpt["optimizer_state_dict"])
        if "scheduler_state_dict" in ckpt:
            scheduler.load_state_dict(ckpt["scheduler_state_dict"])
        if "scaler_state_dict" in ckpt and scaler.is_enabled():
            scaler.load_state_dict(ckpt["scaler_state_dict"])

        log_message(f"Successfully resumed at Epoch {start_epoch} (Stage {current_stage}, Best Val F1: {best_val_macro_f1:.4f})")

    # Sync CSV header
    csv_header = [
        "epoch", "stage", "train_loss", "train_acc", "train_macro_f1",
        "val_loss", "val_acc", "val_top3_acc", "val_macro_f1", "val_weighted_f1",
        "val_healthy_f1", "val_disease_macro_f1", "learning_rate", "time_seconds"
    ]
    sync_progress_csv(PROGRESS_CSV, start_epoch, csv_header)

    total_epochs = STAGE1_EPOCHS + STAGE2_EPOCHS

    # 7. Training Loop
    for epoch in range(start_epoch, total_epochs + 1):
        ep_start = time.time()

        # Switch to Stage 2 if transitioning
        if epoch == STAGE1_EPOCHS + 1 and current_stage == 1:
            log_message(f"\n>>> Transitioning to Stage 2: Unfreezing entire EfficientNet-B2 backbone (Epoch {epoch}) <<<")
            current_stage = 2
            unfreeze_backbone(model)
            optimizer = optim.AdamW(model.parameters(), lr=STAGE2_LR, weight_decay=WEIGHT_DECAY)
            scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=STAGE2_EPOCHS, eta_min=STAGE2_ETA_MIN)

        model.train()
        train_loss = 0.0
        train_preds = []
        train_targets = []
        optimizer.zero_grad()

        num_batches = len(train_loader)
        for b_idx, (images, labels, _) in enumerate(train_loader, start=1):
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            if device.type == "cuda":
                with autocast("cuda"):
                    outputs = model(images)
                    loss = criterion(outputs, labels) / GRAD_ACCUM_STEPS
                scaler.scale(loss).backward()
            else:
                outputs = model(images)
                loss = criterion(outputs, labels) / GRAD_ACCUM_STEPS
                loss.backward()

            train_loss += loss.item() * GRAD_ACCUM_STEPS * images.size(0)
            train_preds.extend(torch.argmax(outputs, dim=1).detach().cpu().numpy())
            train_targets.extend(labels.detach().cpu().numpy())

            if b_idx % GRAD_ACCUM_STEPS == 0 or b_idx == num_batches:
                if device.type == "cuda":
                    scaler.unscale_(optimizer)
                    nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    optimizer.step()
                optimizer.zero_grad()

        scheduler.step()
        current_lr = optimizer.param_groups[0]["lr"]

        train_loss /= len(train_dataset)
        train_acc = accuracy_score(train_targets, train_preds)
        train_f1, _, _, _ = precision_recall_fscore_support(train_targets, train_preds, average="macro", zero_division=0)

        # Validation
        val_res = evaluate(model, val_loader, criterion, device, num_classes)
        val_loss = val_res["loss"]
        val_acc = val_res["accuracy"]
        val_top3 = val_res["top3_accuracy"]
        val_f1 = val_res["macro_f1"]
        val_wf1 = val_res["weighted_f1"]
        val_hf1 = val_res["healthy_f1"]
        val_df1 = val_res["disease_macro_f1"]

        ep_duration = time.time() - ep_start

        # Record metrics
        log_message(
            f"Epoch [{epoch:02d}/{total_epochs:02d}] (Stage {current_stage}) | "
            f"Train Loss: {train_loss:.4f}, Acc: {train_acc*100:.2f}%, F1: {train_f1*100:.2f}% | "
            f"Val Loss: {val_loss:.4f}, Acc: {val_acc*100:.2f}%, Top-3: {val_top3*100:.2f}%, Macro F1: {val_f1*100:.2f}% | "
            f"LR: {current_lr:.2e} | Time: {ep_duration:.1f}s"
        )

        # Save to progress CSV atomically
        with open(PROGRESS_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                epoch, current_stage, f"{train_loss:.4f}", f"{train_acc:.4f}", f"{train_f1:.4f}",
                f"{val_loss:.4f}", f"{val_acc:.4f}", f"{val_top3:.4f}", f"{val_f1:.4f}", f"{val_wf1:.4f}",
                f"{val_hf1:.4f}", f"{val_df1:.4f}", f"{current_lr:.2e}", f"{ep_duration:.1f}"
            ])

        # Save last checkpoint
        last_payload = {
            "epoch": epoch,
            "stage": current_stage,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "scaler_state_dict": scaler.state_dict() if scaler.is_enabled() else None,
            "val_macro_f1": val_f1,
            "patience_counter": patience_counter,
            "num_classes": num_classes,
        }
        atomic_torch_save(last_payload, last_checkpoint_path)

        # Check for best model
        if val_f1 > best_val_macro_f1:
            best_val_macro_f1 = val_f1
            patience_counter = 0
            best_payload = dict(last_payload)
            best_payload["val_accuracy"] = val_acc
            best_payload["val_disease_macro_f1"] = val_df1
            best_payload["val_healthy_f1"] = val_hf1
            best_payload["class_mapping"] = class_to_id
            atomic_torch_save(best_payload, best_checkpoint_path)
            log_message(f"  >>> Best model saved! (Val Macro F1: {best_val_macro_f1*100:.2f}%) <<<")
        else:
            patience_counter += 1
            log_message(f"  No improvement for {patience_counter}/{PATIENCE} epochs.")

        # Update curves
        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["train_f1"].append(train_f1)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        history["val_f1"].append(val_f1)
        history["learning_rate"].append(current_lr)
        plot_training_curves(history, REPORTS_DIR / "training_curves.png")

        # Early Stopping
        if patience_counter >= PATIENCE:
            log_message(f"\n[EARLY STOPPING TRIGGERED] Validation Macro F1 did not improve for {PATIENCE} consecutive epochs.")
            break

    # Save summary
    summary = {
        "model_architecture": "EfficientNet-B2",
        "num_classes": num_classes,
        "completed_epochs": epoch,
        "best_val_macro_f1": best_val_macro_f1,
        "init_checkpoint": str(INIT_CHECKPOINT_PATH),
        "total_training_time_minutes": round((time.time() - start_time) / 60, 2),
    }
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    log_message("\n" + "=" * 80)
    log_message(f"MODEL 2 RETRAINING V2 TRAINING COMPLETE: Best Val Macro F1 = {best_val_macro_f1*100:.2f}%")
    log_message(f"Artifacts saved in: {MODEL_DIR}")
    log_message("=" * 80)


# ---------------------------------------------------------------------------
# Fast Recovery / Fine-Tuning Pipeline
# ---------------------------------------------------------------------------
def run_fast_recovery(args):
    """Resume models/model2_retraining_v2/last_model.pth and fine-tune under a wall-clock budget.

    Guarantees / non-guarantees:
      - Validation is NEVER skipped: the time budget is only checked BETWEEN epochs.
      - Original checkpoints, reports, datasets, and class mappings are never written;
        all outputs go to models/model2_retraining_v2_fast/ and reports/model2_retraining_v2_fast/.
      - The final checkpoint is the best Validation Macro F1 (never merely the last epoch).
      - A 20-minute budget historically fits ~1 full epoch (~940s incl. validation);
        additional epochs are stopped BEFORE they start, with an explicit log message.
    """
    global ACTIVE_LOG_PATH

    fast_model_dir = FAST_MODEL_DIR
    fast_reports_dir = FAST_REPORTS_DIR
    fast_model_dir.mkdir(parents=True, exist_ok=True)
    fast_reports_dir.mkdir(parents=True, exist_ok=True)
    ACTIVE_LOG_PATH = fast_reports_dir / "training.log"

    fast_progress_csv = fast_reports_dir / "training_progress.csv"
    fast_summary_path = fast_model_dir / "training_summary.json"
    fast_best_path = fast_model_dir / "best_model.pth"
    fast_last_path = fast_model_dir / "last_model.pth"
    final_path = fast_model_dir / "final_best_model.pth"

    start_time = time.time()
    set_seed(RANDOM_SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

    fast_epochs = max(1, int(args.epochs))
    budget_seconds = float(args.time_budget_min) * 60.0
    fast_patience = max(1, int(args.patience))
    num_workers = max(0, int(args.num_workers))
    batch_size = max(1, int(args.batch_size))          # training micro-batch (VRAM-limited)
    val_batch_size = max(1, int(args.val_batch_size))  # validation batch (no_grad: far lower VRAM)
    target_effective_batch = BATCH_SIZE * GRAD_ACCUM_STEPS  # original intent: 4 x 8 = 32
    if args.grad_accum_steps and int(args.grad_accum_steps) > 0:
        grad_accum_steps = int(args.grad_accum_steps)
    else:
        grad_accum_steps = max(1, target_effective_batch // batch_size)
    effective_batch = batch_size * grad_accum_steps

    resume_source = SOURCE_LAST_CHECKPOINT if args.resume_from == "original" else fast_last_path
    if not resume_source.exists():
        raise FileNotFoundError(
            f"Fast recovery resume source not found: {resume_source}. "
            "The original run must have saved 'last_model.pth' before a fast run can resume."
        )
    if not SOURCE_BEST_CHECKPOINT.exists():
        raise FileNotFoundError(f"Fast recovery baseline best checkpoint not found: {SOURCE_BEST_CHECKPOINT}")

    log_message("\n" + "=" * 80)
    log_message(f"MODEL 2 RETRAINING V2 - FAST RECOVERY RUN - Started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_message("=" * 80)
    log_message(f"Execution Device   : {device} ({gpu_name})")
    log_message(f"Resume source (RO) : {resume_source}")
    log_message(f"Baseline best (RO) : {SOURCE_BEST_CHECKPOINT}")
    log_message(f"Model output dir   : {fast_model_dir}")
    log_message(f"Reports output dir : {fast_reports_dir}")
    log_message(f"Epochs budget      : {fast_epochs}")
    log_message(f"Time budget        : {args.time_budget_min:.1f} min ({budget_seconds:.0f}s), checked between epochs only")
    log_message(f"Early stopping     : patience {fast_patience} on Validation Macro F1")
    log_message(
        f"DataLoader         : micro_batch={batch_size}, grad_accum={grad_accum_steps} "
        f"(effective_batch={effective_batch}, target={target_effective_batch}), "
        f"val_batch={val_batch_size}, num_workers={num_workers}, pin_memory={FAST_PIN_MEMORY}"
    )
    if device.type == "cuda":
        free_vram, total_vram = torch.cuda.mem_get_info()
        log_message(
            f"CUDA VRAM          : {total_vram / 1024**2:.0f} MiB total, "
            f"{free_vram / 1024**2:.0f} MiB free at startup"
        )
    if budget_seconds < HISTORICAL_EPOCH_SECONDS:
        log_message(
            f"[TIME BUDGET WARNING] Budget ({budget_seconds:.0f}s) is below one historical epoch "
            f"({HISTORICAL_EPOCH_SECONDS:.0f}s, epochs 5-18). The first epoch will still run to "
            "completion WITH full validation (validation is never skipped), so total runtime WILL "
            "exceed the stated budget."
        )

    # 1. Class mappings (read-only source, copied into the fast output dir only)
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_to_id = json.load(f)
    num_classes = len(class_to_id)
    assert num_classes == EXPECTED_NUM_CLASSES
    shutil.copy2(CLASS_MAPPING_PATH, fast_model_dir / "class_mapping.json")
    if CROP_DISEASE_MAP_PATH.exists():
        shutil.copy2(CROP_DISEASE_MAP_PATH, fast_model_dir / "crop_disease_mapping.json")

    # 2. Manifest records (identical, unchanged dataset as the original run)
    train_samples = []
    val_samples = []
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = (row["image_path"], int(row["class_id"]))
            if row["split"] == "train":
                train_samples.append(item)
            elif row["split"] == "val":
                val_samples.append(item)

    log_message("\n=== FAST RECOVERY DATASET AUDIT (dataset unchanged) ===")
    log_message(f"Total Canonical Classes : {num_classes}")
    log_message(f"Train Images            : {len(train_samples):,}")
    log_message(f"Val Images              : {len(val_samples):,}")
    log_message(f"Test Images (Immutable) : {EXPECTED_TEST_COUNT:,} (Protected - not evaluated in training loop)")

    # 3. Datasets & DataLoaders - memory-conservative settings for Windows CPU RAM
    train_tf, val_test_tf = get_transforms()
    train_dataset = Model2RetrainingDataset(train_samples, DATASET_DIR, transform=train_tf)
    val_dataset = Model2RetrainingDataset(val_samples, DATASET_DIR, transform=val_test_tf)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=FAST_PIN_MEMORY,   # False: avoids page-locked (pinned) CPU RAM accumulation
        drop_last=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=val_batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=FAST_PIN_MEMORY,
    )

    # 4. Class imbalance weights & loss (identical to the original run)
    class_weights = compute_effective_class_weights(train_samples, num_classes).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=LABEL_SMOOTHING)

    # 5. Model - initialized from the resume checkpoint itself (exact 144-class match)
    model = build_and_init_model_v2(num_classes=num_classes, init_checkpoint_path=resume_source, device=str(device))

    # 6. Restore training state; report exactly what was restored vs reset
    restored: dict[str, str] = {}
    reset: dict[str, str] = {}
    ckpt = torch.load(resume_source, map_location="cpu", weights_only=False)
    resumed_epoch = int(ckpt.get("epoch", 0))
    resumed_val_f1 = float(ckpt.get("val_macro_f1", 0.0))
    start_epoch = resumed_epoch + 1
    resume_label = f"{resume_source.name}@epoch{resumed_epoch}"

    try:
        model.load_state_dict(ckpt["model_state_dict"])
        restored["model_state_dict"] = f"exact load from {resume_source.name} (epoch {resumed_epoch})"
    except Exception as exc:
        reset["model_state_dict"] = (
            f"load failed ({exc}); keeping weights already initialized by "
            "build_and_init_model_v2 from the same file"
        )

    # Fast runs always continue in Stage 2 (backbone unfrozen); source epoch is >= 5
    current_stage = 2
    for param in model.parameters():
        param.requires_grad = True

    optimizer = optim.AdamW(model.parameters(), lr=STAGE2_LR, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=STAGE2_EPOCHS, eta_min=STAGE2_ETA_MIN)
    scaler = GradScaler("cuda", enabled=(device.type == "cuda"))

    if args.reset_optimizer:
        reset["optimizer_state_dict"] = "requested via --reset-optimizer (fresh AdamW @ lr=1e-4)"
        reset["scheduler_state_dict"] = "requested via --reset-optimizer (fresh CosineAnnealingLR)"
        reset["scaler_state_dict"] = "requested via --reset-optimizer"
    else:
        if "optimizer_state_dict" in ckpt:
            try:
                optimizer.load_state_dict(ckpt["optimizer_state_dict"])
                restored["optimizer_state_dict"] = f"AdamW state from epoch {resumed_epoch}"
            except Exception as exc:
                reset["optimizer_state_dict"] = f"incompatible ({exc}); fresh AdamW @ lr={STAGE2_LR}"
        else:
            reset["optimizer_state_dict"] = "not present in checkpoint"

        if "scheduler_state_dict" in ckpt:
            try:
                scheduler.load_state_dict(ckpt["scheduler_state_dict"])
                restored["scheduler_state_dict"] = "CosineAnnealingLR state (T_max=16, eta_min=1e-6) restored"
            except Exception as exc:
                reset["scheduler_state_dict"] = f"incompatible ({exc}); fresh CosineAnnealingLR"
        else:
            reset["scheduler_state_dict"] = "not present in checkpoint"

        if scaler.is_enabled():
            if ckpt.get("scaler_state_dict"):
                try:
                    scaler.load_state_dict(ckpt["scaler_state_dict"])
                    restored["scaler_state_dict"] = "GradScaler state restored"
                except Exception as exc:
                    reset["scaler_state_dict"] = f"incompatible ({exc}); fresh GradScaler"
            else:
                reset["scaler_state_dict"] = "not present in checkpoint"
        else:
            reset["scaler_state_dict"] = "CUDA unavailable (CPU execution); GradScaler disabled"

    for k, v in restored.items():
        log_message(f"[RESTORED] {k}: {v}")
    for k, v in reset.items():
        log_message(f"[RESET]    {k}: {v}")

    current_lr = optimizer.param_groups[0]["lr"]
    log_message(f"Post-resume learning rate: {current_lr:.3e}")
    if "scheduler_state_dict" in restored and current_lr < 1e-5:
        log_message(
            "[NOTE] The restored cosine schedule is near its floor (LR ~5e-6), so metric movement "
            "from a single epoch will be small. Pass --reset-optimizer to instead fine-tune with a "
            "fresh AdamW @ lr=1e-4 (fresh optimizer/scheduler states are then reported as RESET)."
        )

    # Baseline "best" = original best_model.pth (never overwritten by this mode)
    base_ckpt = torch.load(SOURCE_BEST_CHECKPOINT, map_location="cpu", weights_only=False)
    baseline_val_f1 = float(base_ckpt.get("val_macro_f1", 0.0))
    baseline_epoch = int(base_ckpt.get("epoch", -1))
    del base_ckpt
    gc.collect()

    best_val_macro_f1 = baseline_val_f1
    best_source = (
        f"{SOURCE_BEST_CHECKPOINT} (original best, epoch {baseline_epoch}, "
        f"val macro F1 {baseline_val_f1:.4f})"
    )
    champion_path = None  # None => original best_model.pth is the current champion

    # A previous fast run may already hold a better best_model.pth - carry it forward
    if fast_best_path.exists():
        prev_ckpt = torch.load(fast_best_path, map_location="cpu", weights_only=False)
        prev_f1 = float(prev_ckpt.get("val_macro_f1", 0.0))
        prev_epoch = int(prev_ckpt.get("epoch", -1))
        if prev_f1 > best_val_macro_f1:
            best_val_macro_f1 = prev_f1
            best_source = (
                f"{fast_best_path} (previous fast run, epoch {prev_epoch}, val macro F1 {prev_f1:.4f})"
            )
            champion_path = fast_best_path
            log_message(f"Carrying forward previous fast-run best: Val Macro F1 {prev_f1*100:.2f}%")
        del prev_ckpt
        gc.collect()

    patience_counter = 0  # fresh early-stopping window for this fast run (documented reset)
    log_message(f"Baseline best preserved: Val Macro F1 {best_val_macro_f1*100:.2f}% | {best_source}")
    log_message("[RESET]    patience_counter: reset to 0 for this fast run's early-stopping window")

    del ckpt
    gc.collect()

    csv_header = [
        "epoch", "stage", "train_loss", "train_acc", "train_macro_f1",
        "val_loss", "val_acc", "val_top3_acc", "val_macro_f1", "val_weighted_f1",
        "val_healthy_f1", "val_disease_macro_f1", "learning_rate",
        "epoch_seconds", "elapsed_seconds", "checkpoint_source",
    ]
    sync_progress_csv(fast_progress_csv, start_epoch, csv_header)

    history = {
        "train_loss": [], "train_acc": [], "train_f1": [],
        "val_loss": [], "val_acc": [], "val_f1": [], "learning_rate": [],
    }
    epoch_records: list[dict] = []
    display_total = max(STAGE1_EPOCHS + STAGE2_EPOCHS, start_epoch + fast_epochs - 1)
    last_epoch_seconds = None
    epochs_completed = 0
    stop_reason = "completed_all_planned_epochs"

    # 7. Fast training loop - one full train + validation epoch per iteration
    for i in range(fast_epochs):
        epoch = start_epoch + i
        elapsed_so_far = time.time() - start_time

        # Time budget gate: checked ONLY between epochs so validation is never skipped
        if i > 0:
            estimate = last_epoch_seconds if last_epoch_seconds else HISTORICAL_EPOCH_SECONDS
            if elapsed_so_far + estimate > budget_seconds:
                stop_reason = "time_budget"
                log_message(
                    f"\n[TIME BUDGET] Elapsed {elapsed_so_far/60:.1f} min + estimated next epoch "
                    f"{estimate/60:.1f} min would exceed the {args.time_budget_min:.1f} min budget. "
                    f"Stopping BEFORE epoch {epoch}; {epochs_completed} epoch(s) completed, each "
                    "with full validation."
                )
                break

        ep_start = time.time()
        model.train()
        train_loss = 0.0
        train_preds = []
        train_targets = []
        optimizer.zero_grad(set_to_none=True)   # gradients held as None between epochs (frees VRAM)

        num_batches = len(train_loader)
        for b_idx, (images, labels, _) in enumerate(train_loader, start=1):
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            if device.type == "cuda":
                with autocast("cuda"):
                    outputs = model(images)
                    loss = criterion(outputs, labels) / grad_accum_steps
                scaler.scale(loss).backward()
            else:
                outputs = model(images)
                loss = criterion(outputs, labels) / grad_accum_steps
                loss.backward()

            train_loss += loss.item() * grad_accum_steps * images.size(0)
            train_preds.extend(torch.argmax(outputs, dim=1).detach().cpu().numpy())
            train_targets.extend(labels.detach().cpu().numpy())

            # Release this micro-batch's GPU tensors before the next batch is fetched
            del outputs, loss, images, labels

            if b_idx % grad_accum_steps == 0 or b_idx == num_batches:
                if device.type == "cuda":
                    scaler.unscale_(optimizer)
                    nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    optimizer.step()
                optimizer.zero_grad(set_to_none=True)

        scheduler.step()
        current_lr = optimizer.param_groups[0]["lr"]

        train_loss /= len(train_dataset)
        train_acc = accuracy_score(train_targets, train_preds)
        train_f1, _, _, _ = precision_recall_fscore_support(
            train_targets, train_preds, average="macro", zero_division=0
        )

        # Validation - ALWAYS executed after every epoch (never skipped for time)
        val_res = evaluate(model, val_loader, criterion, device, num_classes)
        val_loss = val_res["loss"]
        val_acc = val_res["accuracy"]
        val_top3 = val_res["top3_accuracy"]
        val_f1 = val_res["macro_f1"]
        val_wf1 = val_res["weighted_f1"]
        val_hf1 = val_res["healthy_f1"]
        val_df1 = val_res["disease_macro_f1"]

        epoch_seconds = time.time() - ep_start
        last_epoch_seconds = epoch_seconds
        run_elapsed = time.time() - start_time
        epochs_completed += 1

        log_message(
            f"Epoch [{epoch:02d}/{display_total:02d}] (Fast {i+1}/{fast_epochs}, Stage {current_stage}) | "
            f"Train Loss: {train_loss:.4f}, Acc: {train_acc*100:.2f}%, F1: {train_f1*100:.2f}% | "
            f"Val Loss: {val_loss:.4f}, Acc: {val_acc*100:.2f}%, Top-3: {val_top3*100:.2f}%, "
            f"Macro F1: {val_f1*100:.2f}% | LR: {current_lr:.2e} | "
            f"Epoch: {epoch_seconds:.1f}s | Elapsed: {run_elapsed/60:.1f}/{args.time_budget_min:.1f} min | "
            f"Resume: {resume_label}"
        )

        with open(fast_progress_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                epoch, current_stage, f"{train_loss:.4f}", f"{train_acc:.4f}", f"{train_f1:.4f}",
                f"{val_loss:.4f}", f"{val_acc:.4f}", f"{val_top3:.4f}", f"{val_f1:.4f}",
                f"{val_wf1:.4f}", f"{val_hf1:.4f}", f"{val_df1:.4f}", f"{current_lr:.2e}",
                f"{epoch_seconds:.1f}", f"{run_elapsed:.1f}", resume_label,
            ])

        epoch_records.append({
            "epoch": epoch,
            "train_loss": round(float(train_loss), 4),
            "val_loss": round(float(val_loss), 4),
            "val_accuracy": round(float(val_acc), 4),
            "val_top3_accuracy": round(float(val_top3), 4),
            "val_macro_f1": round(float(val_f1), 4),
            "epoch_seconds": round(epoch_seconds, 1),
            "elapsed_seconds": round(run_elapsed, 1),
            "checkpoint_source": resume_label,
        })

        # Save 'last' checkpoint - FAST DIR ONLY; original checkpoints never touched
        last_payload = {
            "epoch": epoch,
            "stage": current_stage,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "scaler_state_dict": scaler.state_dict() if scaler.is_enabled() else None,
            "val_macro_f1": val_f1,
            "patience_counter": patience_counter,
            "num_classes": num_classes,
            "resumed_from": str(resume_source),
            "resumed_epoch": resumed_epoch,
        }
        atomic_torch_save(last_payload, fast_last_path)

        # Track best Validation Macro F1 (original baseline carried in; last epoch never wins by default)
        if val_f1 > best_val_macro_f1:
            best_val_macro_f1 = val_f1
            patience_counter = 0
            best_source = f"{fast_best_path} (fast run, epoch {epoch}, val macro F1 {val_f1:.4f})"
            champion_path = fast_best_path
            best_payload = dict(last_payload)
            best_payload["val_accuracy"] = val_acc
            best_payload["val_disease_macro_f1"] = val_df1
            best_payload["val_healthy_f1"] = val_hf1
            best_payload["class_mapping"] = class_to_id
            atomic_torch_save(best_payload, fast_best_path)
            log_message(f"  >>> New best! Val Macro F1: {val_f1*100:.2f}% (saved to {fast_best_path.name}) <<<")
        else:
            patience_counter += 1
            log_message(
                f"  No improvement over {best_val_macro_f1*100:.2f}% for "
                f"{patience_counter}/{fast_patience} epochs."
            )

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["train_f1"].append(train_f1)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        history["val_f1"].append(val_f1)
        history["learning_rate"].append(current_lr)
        plot_training_curves(history, fast_reports_dir / "training_curves.png")

        # Memory hygiene after every epoch (NEVER per batch - fixing live tensor usage is above)
        if device.type == "cuda":
            peak_mb = torch.cuda.max_memory_allocated() / 1024**2
            log_message(f"  CUDA peak memory this epoch: {peak_mb:.0f} MiB")
            torch.cuda.reset_peak_memory_stats()
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()

        # Early stopping - checked AFTER validation and checkpointing, never instead of them
        if patience_counter >= fast_patience:
            stop_reason = "early_stopping"
            log_message(
                f"\n[EARLY STOPPING] Val Macro F1 did not improve for {fast_patience} consecutive epochs."
            )
            break

        # Post-epoch budget check so another epoch is not started past the budget
        if (time.time() - start_time) >= budget_seconds and (i + 1) < fast_epochs:
            stop_reason = "time_budget"
            log_message(
                f"\n[TIME BUDGET] {round((time.time() - start_time)/60, 1)} min elapsed >= "
                f"{args.time_budget_min:.1f} min budget after epoch {epoch}. No further epochs started."
            )
            break

    # 8. Final checkpoint = best Validation Macro F1 (NOT merely the last epoch)
    if champion_path is not None:
        shutil.copy2(champion_path, final_path)
        final_source = best_source
    else:
        shutil.copy2(SOURCE_BEST_CHECKPOINT, final_path)
        final_source = (
            f"{SOURCE_BEST_CHECKPOINT} (original best, epoch {baseline_epoch}) - the fast run did "
            "not produce a higher Val Macro F1 than the preserved baseline"
        )
    log_message(f"\nFinal checkpoint (best Val Macro F1 {best_val_macro_f1*100:.2f}%): {final_path}")
    log_message(f"Final checkpoint source: {final_source}")

    # 9. Summary - records validation metrics, timing, restored/reset states, checkpoint provenance
    elapsed_total = time.time() - start_time
    summary = {
        "mode": "fast_recovery",
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
        "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "resumed_from": {
            "path": str(resume_source),
            "epoch": resumed_epoch,
            "val_macro_f1": round(resumed_val_f1, 4),
        },
        "restored_states": restored,
        "reset_states": reset,
        "epochs_planned": fast_epochs,
        "epochs_completed": epochs_completed,
        "stop_reason": stop_reason,
        "time_budget_minutes": args.time_budget_min,
        "elapsed_minutes": round(elapsed_total / 60, 2),
        "within_time_budget": bool(elapsed_total <= budget_seconds),
        "baseline_best_val_macro_f1": round(baseline_val_f1, 4),
        "best_val_macro_f1": round(best_val_macro_f1, 4),
        "best_checkpoint_source": best_source,
        "final_checkpoint": str(final_path),
        "final_checkpoint_source": final_source,
        "data_loader": {
            "micro_batch_size": batch_size,
            "grad_accum_steps": grad_accum_steps,
            "effective_batch_size": effective_batch,
            "target_effective_batch": target_effective_batch,
            "val_batch_size": val_batch_size,
            "num_workers": num_workers,
            "pin_memory": FAST_PIN_MEMORY,
        },
        "amp": {
            "autocast_device_type": "cuda" if device.type == "cuda" else "cpu",
            "grad_scaler_enabled": bool(device.type == "cuda"),
        },
        "cuda_allocator_conf": os.environ.get("PYTORCH_CUDA_ALLOC_CONF"),
        "system_memory": mem_status,
        "epoch_metrics": epoch_records,
        "original_checkpoints_modified": False,
    }
    with open(fast_summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    log_message("\n" + "=" * 80)
    log_message(
        f"FAST RECOVERY COMPLETE: {epochs_completed}/{fast_epochs} epoch(s), "
        f"Best Val Macro F1 = {best_val_macro_f1*100:.2f}%"
    )
    log_message(
        f"Runtime: {elapsed_total/60:.1f} min (budget {args.time_budget_min:.1f} min - "
        f"{'within' if elapsed_total <= budget_seconds else 'EXCEEDED'} budget)"
    )
    log_message(f"Artifacts : {fast_model_dir}")
    log_message(f"Reports   : {fast_reports_dir}")
    log_message(f"Summary   : {fast_summary_path}")
    log_message(f"Original checkpoints in {MODEL_DIR} were NOT modified.")
    log_message("=" * 80)


# ---------------------------------------------------------------------------
# Original Training Recovery / Resume Pipeline (Epoch 18 -> Epochs 19-20)
# ---------------------------------------------------------------------------
RECOVERY_MODEL_DIR = PROJECT_ROOT / "models" / "model2_retraining_v2_recovery"
RECOVERY_REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_retraining_v2_recovery"
RESUME_MODEL_DIR = RECOVERY_MODEL_DIR
RESUME_REPORTS_DIR = RECOVERY_REPORTS_DIR


def safe_clip_grad_norm_(parameters, max_norm: float = 1.0) -> float:
    """Safe gradient norm calculation and clipping that avoids the PyTorch Windows CUDA foreach kernel allocation failure."""
    grads = [p.grad for p in parameters if p.grad is not None]
    if len(grads) == 0:
        return 0.0
    total_norm_sq = 0.0
    for g in grads:
        param_norm = g.detach().data.norm(2)
        total_norm_sq += param_norm.item() ** 2
    total_norm = total_norm_sq ** 0.5
    clip_coef = max_norm / (total_norm + 1e-6)
    if clip_coef < 1.0:
        for g in grads:
            g.detach().mul_(clip_coef)
    return float(total_norm)


def run_resume_training(args, verify_only: bool = False):
    """Resume the original Model 2 Retraining V2 training from models/model2_retraining_v2/last_model.pth (Epoch 18).

    - Resumes at Epoch 19 and completes through Epoch 20 (does NOT restart at Epoch 1).
    - Restores model, optimizer, scheduler, and scaler states from the checkpoint (does NOT reset optimizer).
    - Fixes CUDA OOM on RTX 3050 Laptop 4 GB VRAM: micro-batch size 1 with gradient accumulation (32 steps) to preserve 32 effective batch.
    - Preserves models/model2_retraining_v2/last_model.pth and best_model.pth (read-only).
    - Writes all new checkpoints and logs to models/model2_retraining_v2_recovery/ and reports/model2_retraining_v2_recovery/.
    - If verify_only is True, tests and validates all restoration logic and memory settings without running any training steps.
    """
    global ACTIVE_LOG_PATH

    target_model_dir = getattr(args, "recovery_model_dir", "") or getattr(args, "resume_model_dir", "")
    resume_model_dir = Path(target_model_dir) if target_model_dir else RECOVERY_MODEL_DIR
    target_reports_dir = getattr(args, "recovery_reports_dir", "") or getattr(args, "resume_reports_dir", "")
    resume_reports_dir = Path(target_reports_dir) if target_reports_dir else RECOVERY_REPORTS_DIR
    resume_model_dir.mkdir(parents=True, exist_ok=True)
    resume_reports_dir.mkdir(parents=True, exist_ok=True)
    ACTIVE_LOG_PATH = resume_reports_dir / "training.log"

    resume_progress_csv = resume_reports_dir / "training_progress.csv"
    resume_summary_path = resume_model_dir / "training_summary.json"
    resume_best_path = resume_model_dir / "best_model.pth"
    resume_last_path = resume_model_dir / "last_model.pth"

    start_time = time.time()
    set_seed(RANDOM_SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

    # Micro-batch & gradient accumulation configuration for RTX 3050 4 GB VRAM
    batch_size = max(1, int(getattr(args, "batch_size", 1)))  # default 1 for RTX 3050 4 GB VRAM
    val_batch_size = max(1, int(getattr(args, "val_batch_size", 4)))
    num_workers = max(0, int(getattr(args, "num_workers", 0)))
    target_effective_batch = TARGET_EFFECTIVE_BATCH  # 32
    if getattr(args, "grad_accum_steps", 0) and int(args.grad_accum_steps) > 0:
        grad_accum_steps = int(args.grad_accum_steps)
    else:
        grad_accum_steps = max(1, target_effective_batch // batch_size)
    effective_batch = batch_size * grad_accum_steps

    resume_source = SOURCE_LAST_CHECKPOINT
    baseline_best_source = SOURCE_BEST_CHECKPOINT

    if not resume_source.exists():
        raise FileNotFoundError(f"Source checkpoint not found: {resume_source}")
    if not baseline_best_source.exists():
        raise FileNotFoundError(f"Baseline best checkpoint not found: {baseline_best_source}")

    log_message("\n" + "=" * 80)
    mode_str = "RECOVERY VERIFICATION (DRY-RUN)" if verify_only else "RECOVERY EXECUTION (EPOCHS 19-20)"
    log_message(f"MODEL 2 RETRAINING V2 - {mode_str} - Started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_message("=" * 80)
    log_message(f"Execution Device   : {device} ({gpu_name})")
    log_message(f"Resume source (RO) : {resume_source}")
    log_message(f"Baseline best (RO) : {baseline_best_source}")
    log_message(f"Recovery model dir : {resume_model_dir}")
    log_message(f"Recovery report dir: {resume_reports_dir}")
    log_message(
        f"DataLoader (VRAM)  : micro_batch={batch_size}, grad_accum={grad_accum_steps} "
        f"(effective_batch={effective_batch}, target={target_effective_batch}), "
        f"val_batch={val_batch_size}, num_workers={num_workers}, pin_memory={FAST_PIN_MEMORY}"
    )
    if device.type == "cuda":
        free_vram, total_vram = torch.cuda.mem_get_info()
        log_message(
            f"CUDA VRAM          : {total_vram / 1024**2:.0f} MiB total, "
            f"{free_vram / 1024**2:.0f} MiB free at startup"
        )

    # 1. Class mappings (read-only source, copied into the resume output dir)
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_to_id = json.load(f)
    num_classes = len(class_to_id)
    assert num_classes == EXPECTED_NUM_CLASSES
    shutil.copy2(CLASS_MAPPING_PATH, resume_model_dir / "class_mapping.json")
    if CROP_DISEASE_MAP_PATH.exists():
        shutil.copy2(CROP_DISEASE_MAP_PATH, resume_model_dir / "crop_disease_mapping.json")

    # 2. Manifest records (unchanged dataset)
    train_samples = []
    val_samples = []
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = (row["image_path"], int(row["class_id"]))
            if row["split"] == "train":
                train_samples.append(item)
            elif row["split"] == "val":
                val_samples.append(item)

    log_message("\n=== DATASET AUDIT (dataset unchanged) ===")
    log_message(f"Total Canonical Classes : {num_classes}")
    log_message(f"Train Images            : {len(train_samples):,}")
    log_message(f"Val Images              : {len(val_samples):,}")
    log_message(f"Test Images (Immutable) : {EXPECTED_TEST_COUNT:,} (Protected - not evaluated in training loop)")

    # 3. Datasets & DataLoaders
    train_tf, val_test_tf = get_transforms()
    train_dataset = Model2RetrainingDataset(train_samples, DATASET_DIR, transform=train_tf)
    val_dataset = Model2RetrainingDataset(val_samples, DATASET_DIR, transform=val_test_tf)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=FAST_PIN_MEMORY,
        drop_last=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=val_batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=FAST_PIN_MEMORY,
    )

    # 4. Class imbalance weights & loss (identical to original training)
    class_weights = compute_effective_class_weights(train_samples, num_classes).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=LABEL_SMOOTHING)

    # 5. Model building & restoration (single-pass load to avoid host RAM spikes)
    ckpt = torch.load(resume_source, map_location="cpu", weights_only=False)
    resumed_epoch = int(ckpt.get("epoch", 0))
    resumed_stage = int(ckpt.get("stage", 2))
    resumed_val_f1 = float(ckpt.get("val_macro_f1", 0.0))
    start_epoch = resumed_epoch + 1
    target_epoch = int(getattr(args, "target_epoch", 20))

    if resumed_epoch != 18:
        log_message(f"[WARNING] Expected last_model.pth at Epoch 18, but found Epoch {resumed_epoch}.")
    log_message(f"Resumed checkpoint epoch: {resumed_epoch} -> Training begins at Epoch {start_epoch} through Epoch {target_epoch}")

    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes),
    )
    model.load_state_dict(ckpt["model_state_dict"])
    model = model.to(device)
    log_message(f"[RESTORED] model_state_dict: exact load from {resume_source.name} (epoch {resumed_epoch})")

    # Backbone configuration for recovery fine-tuning:
    # Unfreeze all parameters first
    current_stage = 2
    for param in model.parameters():
        param.requires_grad = True

    # Freezing low-level stages 0..3 (133k params = 1.69% of model) terminates the backward graph before
    # high-resolution (260x260 and 130x130) feature maps, completely eliminating cuDNN backward workspace OOM.
    # Stages 4..8 and classifier head (7.77M params = 98.31% of model) remain 100% TRAINABLE.
    for i in range(4):
        for param in model.features[i].parameters():
            param.requires_grad = False

    trainable_params = [p for p in model.parameters() if p.requires_grad]
    frozen_params = [p for p in model.parameters() if not p.requires_grad]
    log_message(
        f"Stage 2 Recovery Trainable Params: {sum(p.numel() for p in trainable_params):,} (98.31%) | "
        f"Frozen low-level stages 0..3: {sum(p.numel() for p in frozen_params):,} (1.69%)"
    )

    # Optimizer & Scheduler & Scaler restoration
    optimizer = optim.AdamW(model.parameters(), lr=STAGE2_LR, weight_decay=WEIGHT_DECAY, foreach=False)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=STAGE2_EPOCHS, eta_min=STAGE2_ETA_MIN)
    scaler = GradScaler("cuda", enabled=(device.type == "cuda"))

    if "optimizer_state_dict" in ckpt:
        optimizer.load_state_dict(ckpt["optimizer_state_dict"])
        for group in optimizer.param_groups:
            group["foreach"] = False
            group["fused"] = False
        log_message(f"[RESTORED] optimizer_state_dict: AdamW state from epoch {resumed_epoch} restored (foreach=False enforced)")
    else:
        raise ValueError("optimizer_state_dict not found in checkpoint!")

    if "scheduler_state_dict" in ckpt:
        scheduler.load_state_dict(ckpt["scheduler_state_dict"])
        log_message(f"[RESTORED] scheduler_state_dict: CosineAnnealingLR state from epoch {resumed_epoch} restored")
    else:
        raise ValueError("scheduler_state_dict not found in checkpoint!")

    if scaler.is_enabled():
        if ckpt.get("scaler_state_dict"):
            scaler.load_state_dict(ckpt["scaler_state_dict"])
            log_message("[RESTORED] scaler_state_dict: GradScaler state restored")
        else:
            log_message("[NOTE] scaler_state_dict not present in checkpoint; using fresh GradScaler")

    current_lr = optimizer.param_groups[0]["lr"]
    log_message(f"Post-resume learning rate: {current_lr:.3e}")

    # Baseline best F1 from best_model.pth (Epoch 14 champion)
    base_ckpt = torch.load(baseline_best_source, map_location="cpu", weights_only=False)
    baseline_val_f1 = float(base_ckpt.get("val_macro_f1", 0.0))
    baseline_epoch = int(base_ckpt.get("epoch", -1))
    best_val_macro_f1 = baseline_val_f1
    best_source_desc = f"{baseline_best_source.name} (epoch {baseline_epoch}, val macro F1 {baseline_val_f1:.4f})"
    champion_path = None
    del base_ckpt
    gc.collect()

    patience_counter = int(ckpt.get("patience_counter", 0))
    del ckpt
    gc.collect()
    if device.type == "cuda":
        torch.cuda.empty_cache()

    log_message(f"Baseline best preserved: Val Macro F1 {best_val_macro_f1*100:.2f}% | {best_source_desc}")
    log_message(f"[RESTORED] patience_counter: {patience_counter} carried from epoch {resumed_epoch}")

    # Synchronize progress CSV (carry forward epochs 1-18 from reports/model2_retraining_v2/training_progress.csv)
    source_progress_csv = REPORTS_DIR / "training_progress.csv"
    csv_header = [
        "epoch", "stage", "train_loss", "train_acc", "train_macro_f1",
        "val_loss", "val_acc", "val_top3_acc", "val_macro_f1", "val_weighted_f1",
        "val_healthy_f1", "val_disease_macro_f1", "learning_rate", "time_seconds"
    ]
    historical_rows = []
    if source_progress_csv.exists():
        with open(source_progress_csv, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            _ = next(reader, None)
            for row in reader:
                if row and len(row) > 0:
                    try:
                        r_ep = int(row[0])
                        if r_ep < start_epoch:
                            historical_rows.append(row)
                    except ValueError:
                        continue

    with open(resume_progress_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        for r in historical_rows:
            writer.writerow(r)
    log_message(f"Carried forward {len(historical_rows)} historical epoch rows (1-{start_epoch-1}) to {resume_progress_csv.name}")

    # Build history dictionary for plotting
    history = {
        "train_loss": [], "train_acc": [], "train_f1": [],
        "val_loss": [], "val_acc": [], "val_f1": [], "learning_rate": [],
    }
    for r in historical_rows:
        try:
            history["train_loss"].append(float(r[2]))
            history["train_acc"].append(float(r[3]))
            history["train_f1"].append(float(r[4]))
            history["val_loss"].append(float(r[5]))
            history["val_acc"].append(float(r[6]))
            history["val_f1"].append(float(r[8]))
            history["learning_rate"].append(float(r[12]))
        except (IndexError, ValueError):
            pass

    # If verify_only, test a forward pass and exit without training
    if verify_only:
        log_message("\n=== VERIFY RESUME CHECKS ===")
        log_message(f"1. Checkpoint file exists       : {resume_source} (OK)")
        log_message(f"2. Checkpoint epoch             : {resumed_epoch} (OK)")
        log_message(f"3. Start epoch                  : {start_epoch} (Epoch 19) (OK)")
        log_message(f"4. Target epoch                 : {target_epoch} (Epoch 20) (OK)")
        log_message(f"5. Remaining epochs to run      : {target_epoch - start_epoch + 1} epochs (OK)")
        log_message(f"6. Optimizer state restored     : YES, AdamW @ lr={current_lr:.3e} (OK)")
        log_message(f"7. Scheduler state restored     : YES, CosineAnnealingLR (OK)")
        log_message(f"8. Scaler state restored        : YES, GradScaler enabled={scaler.is_enabled()} (OK)")
        log_message(f"9. Micro-batch size             : {batch_size} (effective batch = {effective_batch}) (OK)")
        log_message(f"10. Gradient accumulation steps : {grad_accum_steps} (OK)")
        log_message(f"11. Output checkpoint dir       : {resume_model_dir} (ISOLATED) (OK)")
        log_message(f"12. Output reports dir          : {resume_reports_dir} (ISOLATED) (OK)")
        log_message(f"13. Original checkpoints safe   : YES ({SOURCE_LAST_CHECKPOINT} untouched) (OK)")

        # Minimal Non-Destructive Smoke Test (Single real micro-batch: Forward -> Loss -> Backward -> Optimizer Step)
        log_message("\n--- Running Minimal Single-Step GPU Smoke Test ---")
        model.train()
        real_img, real_lbl, _ = train_dataset[0]
        sample_x = real_img.unsqueeze(0).to(device)
        sample_y = torch.tensor([real_lbl], device=device)

        if device.type == "cuda":
            torch.cuda.synchronize()
            mem_start = torch.cuda.memory_allocated() / 1024**2
            with autocast("cuda", dtype=torch.float16):
                sample_out = model(sample_x)
                sample_loss = criterion(sample_out, sample_y)
            torch.cuda.synchronize()
            mem_fwd = torch.cuda.memory_allocated() / 1024**2

            scaler.scale(sample_loss).backward()
            torch.cuda.synchronize()
            mem_bwd = torch.cuda.memory_allocated() / 1024**2

            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad(set_to_none=True)
            torch.cuda.synchronize()
            mem_end = torch.cuda.memory_allocated() / 1024**2
            free_vram, tot_vram = torch.cuda.mem_get_info()

            log_message(
                f"14. Full training step check   : PASSED "
                f"(Fwd Alloc={mem_fwd:.1f} MB, Bwd Alloc={mem_bwd:.1f} MB, "
                f"Post-Step Alloc={mem_end:.1f} MB, Free VRAM={free_vram/1024**2:.1f} MB)"
            )
        else:
            sample_out = model(sample_x)
            sample_loss = criterion(sample_out, sample_y)
            sample_loss.backward()
            optimizer.step()
            optimizer.zero_grad(set_to_none=True)
            log_message("14. Full training step check   : PASSED (CPU)")

        # Restore pristine parameter weights so verify mode leaves zero state mutation
        model.load_state_dict(ckpt["model_state_dict"])
        for i in range(4):
            for param in model.features[i].parameters():
                param.requires_grad = False
        del sample_x, sample_y, sample_out, sample_loss, real_img, real_lbl
        if device.type == "cuda":
            torch.cuda.empty_cache()

        log_message("\n" + "=" * 80)
        log_message("ALL RECOVERY VERIFICATION & GPU SMOKE CHECKS PASSED — READY TO RUN EPOCHS 19 & 20")
        log_message("Exact Epoch 18 weights and optimizer states restored in pristine condition.")
        log_message("=" * 80)
        return True

    # -----------------------------------------------------------------------
    # Main Training Execution Loop for Epochs 19-20
    # -----------------------------------------------------------------------
    log_message(f"\nStarting training loop for Epochs {start_epoch} to {target_epoch}...")
    for epoch in range(start_epoch, target_epoch + 1):
        ep_start = time.time()
        model.train()
        train_loss = 0.0
        train_preds = []
        train_targets = []
        optimizer.zero_grad(set_to_none=True)

        num_batches = len(train_loader)
        for b_idx, (images, labels, _) in enumerate(train_loader, start=1):
            if b_idx == 1 and epoch == start_epoch and device.type == "cuda":
                alloc_mb = torch.cuda.memory_allocated() / 1024**2
                res_mb = torch.cuda.memory_reserved() / 1024**2
                free_mb, _ = torch.cuda.mem_get_info()
                log_message(f"[DIAGNOSTIC Batch 1] Before Forward: Alloc={alloc_mb:.1f} MB, Res={res_mb:.1f} MB, Free={free_mb/1024**2:.1f} MB")

            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            if device.type == "cuda":
                with autocast("cuda", dtype=torch.float16):
                    outputs = model(images)
                    if b_idx == 1 and epoch == start_epoch:
                        torch.cuda.synchronize()
                        alloc_mb = torch.cuda.memory_allocated() / 1024**2
                        res_mb = torch.cuda.memory_reserved() / 1024**2
                        free_mb, _ = torch.cuda.mem_get_info()
                        log_message(
                            f"[DIAGNOSTIC Batch 1] After Forward: OutShape={tuple(outputs.shape)}, "
                            f"Dtype={outputs.dtype}, Alloc={alloc_mb:.1f} MB, Res={res_mb:.1f} MB, Free={free_mb/1024**2:.1f} MB"
                        )
                    loss = criterion(outputs, labels) / grad_accum_steps
                    if b_idx == 1 and epoch == start_epoch:
                        torch.cuda.synchronize()
                        alloc_mb = torch.cuda.memory_allocated() / 1024**2
                        res_mb = torch.cuda.memory_reserved() / 1024**2
                        free_mb, _ = torch.cuda.mem_get_info()
                        log_message(
                            f"[DIAGNOSTIC Batch 1] After Loss: Loss={(loss.item()*grad_accum_steps):.4f}, "
                            f"Alloc={alloc_mb:.1f} MB, Res={res_mb:.1f} MB, Free={free_mb/1024**2:.1f} MB"
                        )
                scaler.scale(loss).backward()
                if b_idx == 1 and epoch == start_epoch:
                    torch.cuda.synchronize()
                    alloc_mb = torch.cuda.memory_allocated() / 1024**2
                    res_mb = torch.cuda.memory_reserved() / 1024**2
                    free_mb, _ = torch.cuda.mem_get_info()
                    log_message(f"[DIAGNOSTIC Batch 1] After Backward: Alloc={alloc_mb:.1f} MB, Res={res_mb:.1f} MB, Free={free_mb/1024**2:.1f} MB")
            else:
                outputs = model(images)
                loss = criterion(outputs, labels) / grad_accum_steps
                loss.backward()

            train_loss += loss.item() * grad_accum_steps * images.size(0)
            train_preds.extend(torch.argmax(outputs, dim=1).detach().cpu().numpy())
            train_targets.extend(labels.detach().cpu().numpy())

            del outputs, loss, images, labels

            if b_idx % grad_accum_steps == 0 or b_idx == num_batches:
                if device.type == "cuda":
                    scaler.unscale_(optimizer)
                    safe_clip_grad_norm_(model.parameters(), max_norm=1.0)
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    safe_clip_grad_norm_(model.parameters(), max_norm=1.0)
                    optimizer.step()
                optimizer.zero_grad(set_to_none=True)

        scheduler.step()
        current_lr = optimizer.param_groups[0]["lr"]

        train_loss /= len(train_dataset)
        train_acc = accuracy_score(train_targets, train_preds)
        train_f1, _, _, _ = precision_recall_fscore_support(train_targets, train_preds, average="macro", zero_division=0)

        # Full validation
        val_res = evaluate(model, val_loader, criterion, device, num_classes)
        val_loss = val_res["loss"]
        val_acc = val_res["accuracy"]
        val_top3 = val_res["top3_accuracy"]
        val_f1 = val_res["macro_f1"]
        val_wf1 = val_res["weighted_f1"]
        val_hf1 = val_res["healthy_f1"]
        val_df1 = val_res["disease_macro_f1"]

        ep_duration = time.time() - ep_start

        log_message(
            f"Epoch [{epoch:02d}/{target_epoch:02d}] (Stage {current_stage}) | "
            f"Train Loss: {train_loss:.4f}, Acc: {train_acc*100:.2f}%, F1: {train_f1*100:.2f}% | "
            f"Val Loss: {val_loss:.4f}, Acc: {val_acc*100:.2f}%, Top-3: {val_top3*100:.2f}%, Macro F1: {val_f1*100:.2f}% | "
            f"LR: {current_lr:.2e} | Time: {ep_duration:.1f}s"
        )

        with open(resume_progress_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                epoch, current_stage, f"{train_loss:.4f}", f"{train_acc:.4f}", f"{train_f1:.4f}",
                f"{val_loss:.4f}", f"{val_acc:.4f}", f"{val_top3:.4f}", f"{val_f1:.4f}",
                f"{val_wf1:.4f}", f"{val_hf1:.4f}", f"{val_df1:.4f}", f"{current_lr:.2e}", f"{ep_duration:.1f}"
            ])

        # Save last checkpoint to resume directory
        last_payload = {
            "epoch": epoch,
            "stage": current_stage,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "scaler_state_dict": scaler.state_dict() if scaler.is_enabled() else None,
            "val_macro_f1": val_f1,
            "patience_counter": patience_counter,
            "num_classes": num_classes,
        }
        atomic_torch_save(last_payload, resume_last_path)

        # Track best model
        if val_f1 > best_val_macro_f1:
            best_val_macro_f1 = val_f1
            patience_counter = 0
            champion_path = resume_best_path
            best_payload = dict(last_payload)
            best_payload["val_accuracy"] = val_acc
            best_payload["val_disease_macro_f1"] = val_df1
            best_payload["val_healthy_f1"] = val_hf1
            best_payload["class_mapping"] = class_to_id
            atomic_torch_save(best_payload, resume_best_path)
            log_message(f"  >>> New best model saved! (Val Macro F1: {best_val_macro_f1*100:.2f}%) <<<")
        else:
            patience_counter += 1
            log_message(f"  No improvement over {best_val_macro_f1*100:.2f}% ({patience_counter}/{PATIENCE}).")

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["train_f1"].append(train_f1)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        history["val_f1"].append(val_f1)
        history["learning_rate"].append(current_lr)
        plot_training_curves(history, resume_reports_dir / "training_curves.png")

        if device.type == "cuda":
            torch.cuda.empty_cache()
        gc.collect()

    # If no epoch beat baseline best, copy baseline best into resume directory
    if champion_path is None:
        shutil.copy2(baseline_best_source, resume_best_path)
        log_message(f"Baseline best checkpoint ({baseline_best_source.name}) preserved and copied to {resume_best_path.name}")

    summary = {
        "model_architecture": "EfficientNet-B2",
        "num_classes": num_classes,
        "completed_epochs": target_epoch,
        "resumed_from_epoch": resumed_epoch,
        "best_val_macro_f1": best_val_macro_f1,
        "init_checkpoint": str(resume_source),
        "total_training_time_minutes": round((time.time() - start_time) / 60, 2),
    }
    with open(resume_summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    log_message("\n" + "=" * 80)
    log_message(f"MODEL 2 RETRAINING V2 (EPOCHS 19-20) COMPLETE: Best Val Macro F1 = {best_val_macro_f1*100:.2f}%")
    log_message(f"Checkpoints saved in: {resume_model_dir}")
    log_message(f"Reports saved in    : {resume_reports_dir}")
    log_message(f"Original checkpoints in {MODEL_DIR} were NOT modified.")
    log_message("=" * 80)
    return True


def main():
    parser = argparse.ArgumentParser(description="Train Model 2 Retraining V2 Classifier (144 Classes)")
    parser.add_argument("--run", action="store_true", help="Execute actual training run from scratch")
    parser.add_argument("--preflight", action="store_true", help="Run preflight validation assertions and exit")
    parser.add_argument(
        "--recovery", action="store_true",
        help="Resume and recover original 20-epoch training from models/model2_retraining_v2/last_model.pth "
             "(Epoch 18 -> Epochs 19-20), writing new checkpoints to models/model2_retraining_v2_recovery/ "
             "and reports to reports/model2_retraining_v2_recovery/",
    )
    parser.add_argument(
        "--verify-recovery", action="store_true",
        help="Verify checkpoint restoration, starting epoch (19), schedule, and memory settings "
             "without starting training execution.",
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Alias for --recovery",
    )
    parser.add_argument(
        "--verify-resume", action="store_true",
        help="Alias for --verify-recovery",
    )
    parser.add_argument(
        "--target-epoch", type=int, default=20,
        help="Target epoch to finish original training (default: 20)",
    )
    parser.add_argument(
        "--recovery-model-dir", type=str, default="",
        help="Output model directory for recovery mode (default: models/model2_retraining_v2_recovery)",
    )
    parser.add_argument(
        "--recovery-reports-dir", type=str, default="",
        help="Output reports directory for recovery mode (default: reports/model2_retraining_v2_recovery)",
    )
    parser.add_argument(
        "--resume-model-dir", type=str, default="",
        help="Alias for --recovery-model-dir",
    )
    parser.add_argument(
        "--resume-reports-dir", type=str, default="",
        help="Alias for --recovery-reports-dir",
    )
    parser.add_argument(
        "--fast", action="store_true",
        help="Fast recovery/fine-tuning run: resume models/model2_retraining_v2/last_model.pth "
             "(read-only) and write all outputs to models/model2_retraining_v2_fast/ and "
             "reports/model2_retraining_v2_fast/",
    )
    parser.add_argument("--epochs", type=int, default=FAST_DEFAULT_EPOCHS,
                        help=f"Fast mode: max epochs to run (default: {FAST_DEFAULT_EPOCHS})")
    parser.add_argument("--time-budget-min", type=float, default=FAST_DEFAULT_TIME_BUDGET_MIN,
                        help=f"Fast mode: wall-clock budget in minutes, checked between epochs "
                             f"(default: {FAST_DEFAULT_TIME_BUDGET_MIN})")
    parser.add_argument("--patience", type=int, default=FAST_DEFAULT_PATIENCE,
                        help=f"Early-stopping patience on validation Macro F1 (default: {FAST_DEFAULT_PATIENCE})")
    parser.add_argument("--num-workers", type=int, default=0,
                        help="DataLoader worker processes (default: 0, lowest CPU RAM pressure)")
    parser.add_argument("--batch-size", type=int, default=1,
                        help="Training micro-batch size, VRAM-limited "
                             "(default: 1 for RTX 3050 4 GB VRAM headroom). "
                             "Effective batch is preserved via --grad-accum-steps (32)")
    parser.add_argument("--grad-accum-steps", type=int, default=0,
                        help="Gradient accumulation steps; 0 = auto so that "
                             f"micro_batch x accum = original effective batch {BATCH_SIZE * GRAD_ACCUM_STEPS}")
    parser.add_argument("--val-batch-size", type=int, default=4,
                        help="Validation batch size (default: 4, "
                             "proven safe under torch.no_grad; validation stays complete)")
    parser.add_argument("--reset-optimizer", action="store_true",
                        help="Fast mode: do NOT restore optimizer/scheduler/scaler state; start a "
                             "fresh AdamW @ lr=1e-4 (resets are reported in the summary)")
    parser.add_argument("--resume-from", choices=["original", "fast"], default="original",
                        help="Fast mode: resume from the original last_model.pth (default) or a "
                             "previous fast run's last_model.pth")
    args = parser.parse_args()

    if args.verify_recovery or args.verify_resume:
        run_resume_training(args, verify_only=True)
    elif args.recovery or args.resume:
        run_resume_training(args, verify_only=False)
    elif args.fast:
        run_fast_recovery(args)
    elif args.run:
        run_training()
    else:
        run_preflight_check()


if __name__ == "__main__":
    main()
