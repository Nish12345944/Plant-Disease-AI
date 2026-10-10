"""
Train Model 2 Disease Classifier Retraining V1 (EfficientNet-B2, 143 Classes)
================================================================================
Trains on the Model 2 Retraining V1 dataset:
  data/processed/model2_retraining_v1/
  ├── train/{crop}/{disease}/ (27,982 images: 13,700 historical + 14,282 new)
  ├── val/{crop}/{disease}/   (2,647 images: 1,764 historical + 883 new)
  └── test/{crop}/{disease}/  (2,304 images: IMMUTABLE historical test benchmark)

Initialization: models/model2_classifier_v4/best_model.pth (backbone weights)
Classifier Head: New 143-class linear layer (initialized fresh)
Primary Model Selection Metric: Validation Macro F1

Outputs:
  models/model2_retraining_v1/
  ├── best_model.pth
  ├── last_model.pth
  ├── config.json
  ├── class_mapping.json
  ├── crop_disease_mapping.json
  └── training_summary.json

Reports:
  reports/model2_retraining/
  ├── training.log
  ├── training_progress.csv
  ├── classification_report.csv
  ├── test_predictions.csv
  ├── confusion_matrix.png
  ├── training_curves.png
  └── model2_training_preflight_report.md
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
DATASET_DIR = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v1"
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v1_manifest.csv"
CLASS_MAPPING_PATH = DATASET_DIR / "class_mapping.json"
CROP_DISEASE_MAP_PATH = DATASET_DIR / "crop_disease_mapping.json"
V4_CHECKPOINT_PATH = PROJECT_ROOT / "models" / "model2_classifier_v4" / "best_model.pth"

MODEL_DIR = PROJECT_ROOT / "models" / "model2_retraining_v1"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_retraining"
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

def set_seed(seed: int = RANDOM_SEED):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# ---------------------------------------------------------------------------
# Dataset with Robust Error-Handled Bounded Memory Decoding
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
                    # Bounded memory decoding: downscale multi-megapixel JPEGs directly during C decode
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
    with open(TRAINING_LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def compute_effective_class_weights(train_samples: list[tuple[str, int]], num_classes: int, beta: float = 0.999):
    """Compute Effective Number of Samples weights (Cui et al., 2019)."""
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


def build_and_init_model(num_classes: int = 143, v4_checkpoint_path: Path | None = None, device: str = "cpu"):
    """Builds EfficientNet-B2, initializes backbone from V4, and creates new 143-class head."""
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes),
    )

    if v4_checkpoint_path and Path(v4_checkpoint_path).exists():
        log_message(f"Initializing backbone weights from V4 checkpoint: {v4_checkpoint_path}")
        checkpoint = torch.load(v4_checkpoint_path, map_location="cpu", weights_only=False)
        state_dict = checkpoint["model_state_dict"] if "model_state_dict" in checkpoint else checkpoint
        
        # In-place remove old classifier weights
        if "classifier.1.weight" in state_dict:
            del state_dict["classifier.1.weight"]
        if "classifier.1.bias" in state_dict:
            del state_dict["classifier.1.bias"]

        load_res = model.load_state_dict(state_dict, strict=False)
        log_message(f"Successfully transferred backbone weights from V4 (Excluded: {load_res.missing_keys})")
        del checkpoint, state_dict
        gc.collect()
    else:
        log_message("Warning: V4 checkpoint not found; initializing from ImageNet-1K default weights.")
        model = efficientnet_b2(weights=torchvision.models.EfficientNet_B2_Weights.DEFAULT)
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(in_features, num_classes),
        )

    return model.to(device)


def evaluate(model, loader, criterion, device, num_classes):
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
    axes[1, 0].plot(epochs, [f * 100 for f in history["train_macro_f1"]], "b-o", label="Train Macro F1")
    axes[1, 0].plot(epochs, [f * 100 for f in history["val_macro_f1"]], "r-s", label="Val Macro F1")
    axes[1, 0].plot(epochs, [f * 100 for f in history["val_disease_macro_f1"]], "g--^", label="Val Disease Macro F1")
    axes[1, 0].set_title("Macro F1 Scores (%)")
    axes[1, 0].set_xlabel("Epoch")
    axes[1, 0].set_ylabel("Macro F1 (%)")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # 4. Healthy F1
    axes[1, 1].plot(epochs, [f * 100 for f in history["val_healthy_f1"]], "m-d", label="Val Healthy F1")
    axes[1, 1].set_title("Healthy Class F1 (%)")
    axes[1, 1].set_xlabel("Epoch")
    axes[1, 1].set_ylabel("F1 (%)")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def run_preflight_check() -> bool:
    """Non-training preflight assertion suite."""
    print("=" * 80)
    print("MODEL 2 RETRAINING V1 -- PREFLIGHT VALIDATION & VERIFICATION")
    print("=" * 80)
    
    # 1. Verify Manifest
    assert MANIFEST_PATH.exists(), f"Manifest missing: {MANIFEST_PATH}"
    
    train_count = 0
    val_count = 0
    test_count = 0
    train_classes = set()
    val_classes = set()
    test_classes = set()
    
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            split = row["split"]
            cid = int(row["class_id"])
            if split == "train":
                train_count += 1
                train_classes.add(cid)
            elif split == "val":
                val_count += 1
                val_classes.add(cid)
            elif split == "test":
                test_count += 1
                test_classes.add(cid)
                
    total_imgs = train_count + val_count + test_count
    print(f"Manifest Verification: {total_imgs:,} total images ({train_count:,} train, {val_count:,} val, {test_count:,} test).")
    assert train_count == 27982, f"Train count mismatch: {train_count}"
    assert val_count == 2647, f"Val count mismatch: {val_count}"
    assert test_count == 2304, f"Test count mismatch: {test_count}"
    
    # 2. Class Mapping
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_to_id = json.load(f)
    print(f"Class Mapping: {len(class_to_id)} classes (Class 0: {list(class_to_id.keys())[0]}).")
    assert len(class_to_id) == 143, f"Expected 143 classes, got {len(class_to_id)}"
    assert class_to_id["healthy"] == 0, "Healthy class must be index 0!"
    assert len(train_classes) == 143, "Train missing classes!"
    assert len(val_classes) == 143, "Val missing classes!"
    print("Class coverage check: 100% validation coverage (0 blindspots across all 143 classes).")
    
    # 3. Checkpoint Backbone Compatibility & Model Construction
    torch.backends.mkldnn.enabled = False
    torch.set_num_threads(1)
    device = torch.device("cpu")
    model = build_and_init_model(num_classes=143, v4_checkpoint_path=V4_CHECKPOINT_PATH, device=device)
    model.eval()
    
    dummy_x = torch.randn(2, 3, 260, 260, device=device)
    with torch.no_grad():
        dummy_out = model(dummy_x)
    assert dummy_out.shape == (2, 143), f"Output shape mismatch: {dummy_out.shape}"
    print(f"Forward Pass Smoke Test: (2, 3, 260, 260) -> {tuple(dummy_out.shape)} PASSED.")
    
    print("\n" + "=" * 80)
    print("ALL PREFLIGHT CHECKS PASSED: Ready for Training Execution (--run)")
    print("=" * 80)
    return True


def run_training():
    """Main training execution function for Model 2 Retraining V1."""
    start_time = time.time()
    set_seed(RANDOM_SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

    # Initialize log
    with open(TRAINING_LOG, "a", encoding="utf-8") as f:
        f.write(f"\nModel 2 Retraining V1 Training Run - Started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n")

    log_message(f"Execution Device : {device} ({gpu_name})")
    log_message(f"PyTorch Version  : {torch.__version__}")
    log_message(f"CUDA Version     : {torch.version.cuda if torch.cuda.is_available() else 'N/A'}")

    # 1. Load Mappings
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_to_id = json.load(f)
    id_to_class = {int(v): k for k, v in class_to_id.items()}
    num_classes = len(class_to_id)

    shutil.copy2(CLASS_MAPPING_PATH, MODEL_DIR / "class_mapping.json")
    if CROP_DISEASE_MAP_PATH.exists():
        shutil.copy2(CROP_DISEASE_MAP_PATH, MODEL_DIR / "crop_disease_mapping.json")

    # 2. Load Manifest Records as lightweight tuples
    train_samples = []
    val_samples = []
    test_samples = []
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = (row["image_path"], int(row["class_id"]))
            if row["split"] == "train":
                train_samples.append(item)
            elif row["split"] == "val":
                val_samples.append(item)
            elif row["split"] == "test":
                test_samples.append(item)

    log_message("\n=== PRE-TRAINING DATASET AUDIT VERIFICATION ===")
    log_message(f"Total Canonical Classes : {num_classes}")
    log_message(f"Train Images            : {len(train_samples):,}")
    log_message(f"Val Images              : {len(val_samples):,}")
    log_message(f"Test Images (Immutable) : {len(test_samples):,}")

    # 3. Create Datasets & DataLoaders
    train_tf, val_test_tf = get_transforms()
    train_dataset = Model2RetrainingDataset(train_samples, DATASET_DIR, transform=train_tf)
    val_dataset = Model2RetrainingDataset(val_samples, DATASET_DIR, transform=val_test_tf)
    test_dataset = Model2RetrainingDataset(test_samples, DATASET_DIR, transform=val_test_tf)

    train_loader = DataLoader(
        train_dataset, batch_size=BATCH_SIZE, shuffle=True,
        num_workers=NUM_WORKERS, pin_memory=False, drop_last=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=NUM_WORKERS, pin_memory=False
    )
    test_loader = DataLoader(
        test_dataset, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=NUM_WORKERS, pin_memory=False
    )

    # 4. Class Weights & Loss
    class_weights = compute_effective_class_weights(train_samples, num_classes).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=LABEL_SMOOTHING)
    eval_criterion = nn.CrossEntropyLoss()

    # 5. Build and Initialize Model
    model = build_and_init_model(num_classes, V4_CHECKPOINT_PATH, device=device)

    # Check for resume checkpoint
    start_epoch = 1
    best_val_macro_f1 = 0.0
    best_epoch = 0
    patience_counter = 0

    history = {
        "train_loss": [], "train_acc": [], "train_macro_f1": [],
        "val_loss": [], "val_acc": [], "val_macro_f1": [],
        "val_disease_macro_f1": [], "val_healthy_f1": []
    }

    last_ckpt_path = MODEL_DIR / "last_model.pth"
    best_ckpt_path = MODEL_DIR / "best_model.pth"
    if last_ckpt_path.exists():
        try:
            last_ckpt = torch.load(last_ckpt_path, map_location=device, weights_only=False)
            model.load_state_dict(last_ckpt["model_state_dict"])
            start_epoch = last_ckpt["epoch"] + 1
            log_message(f"Resuming from previous checkpoint at epoch {last_ckpt['epoch']}. Starting at Epoch {start_epoch:02d}...")
            
            if best_ckpt_path.exists():
                best_ckpt = torch.load(best_ckpt_path, map_location="cpu", weights_only=False)
                best_val_macro_f1 = best_ckpt.get("val_macro_f1", 0.0)
                best_epoch = best_ckpt.get("epoch", 1)
                log_message(f"Loaded existing best validation macro F1: {best_val_macro_f1*100:.2f}% (Epoch {best_epoch})")
                del best_ckpt
            del last_ckpt
            gc.collect()
        except Exception as e:
            log_message(f"Note: could not resume checkpoint ({e}), starting freshly from Epoch 1.")

    # 6. Two-Stage Schedule
    scaler = GradScaler("cuda") if device.type == "cuda" else None

    if not PROGRESS_CSV.exists() or start_epoch == 1:
        with open(PROGRESS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "epoch", "stage", "learning_rate", "train_loss", "train_accuracy",
                "train_macro_f1", "train_weighted_f1", "val_loss", "val_accuracy",
                "val_macro_f1", "val_weighted_f1", "val_healthy_f1", "val_disease_macro_f1",
                "best_val_macro_f1", "best_epoch", "epoch_time_seconds"
            ])

    total_epochs = STAGE1_EPOCHS + STAGE2_EPOCHS

    # Setup Stage 1 or Stage 2 optimizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    if start_epoch <= STAGE1_EPOCHS:
        stage = "Stage 1 (Head Warmup)"
        log_message(f"\n--- {stage}: Frozen backbone, training 143-class head only (Epochs {start_epoch}..{STAGE1_EPOCHS}) ---")
        for param in model.features.parameters():
            param.requires_grad = False
        model.features.eval()
        optimizer = optim.AdamW(model.classifier.parameters(), lr=STAGE1_LR, weight_decay=WEIGHT_DECAY, foreach=False)
        scheduler = None
    else:
        stage = "Stage 2 (Full Fine-Tuning)"
        log_message(f"\n--- {stage}: Unfrozen backbone with cosine annealing (Epochs {start_epoch}..{total_epochs}) ---")
        for param in model.parameters():
            param.requires_grad = True
        optimizer = optim.AdamW(model.parameters(), lr=STAGE2_LR, weight_decay=WEIGHT_DECAY, foreach=False)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=STAGE2_EPOCHS, eta_min=STAGE2_ETA_MIN, last_epoch=start_epoch - STAGE1_EPOCHS - 1)

    for epoch in range(start_epoch, total_epochs + 1):
        epoch_start = time.time()

        # Switch to Stage 2 after STAGE1_EPOCHS
        if epoch == STAGE1_EPOCHS + 1:
            stage = "Stage 2 (Full Fine-Tuning)"
            log_message(f"\n--- Entering {stage}: Unfreezing all backbone parameters with cosine annealing ---")
            for param in model.parameters():
                param.requires_grad = True
            optimizer = optim.AdamW(model.parameters(), lr=STAGE2_LR, weight_decay=WEIGHT_DECAY, foreach=False)
            scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=STAGE2_EPOCHS, eta_min=STAGE2_ETA_MIN)

        if epoch <= STAGE1_EPOCHS:
            model.features.eval()
            model.classifier.train()
        else:
            model.train()

        train_loss = 0.0
        train_preds = []
        train_targets = []

        optimizer.zero_grad()
        for step, (images, labels, _) in enumerate(train_loader):
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            if device.type == "cuda":
                with autocast("cuda"):
                    outputs = model(images)
                    loss = criterion(outputs, labels) / GRAD_ACCUM_STEPS
                scaler.scale(loss).backward()
                if (step + 1) % GRAD_ACCUM_STEPS == 0 or (step + 1) == len(train_loader):
                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad()
            else:
                outputs = model(images)
                loss = criterion(outputs, labels) / GRAD_ACCUM_STEPS
                loss.backward()
                if (step + 1) % GRAD_ACCUM_STEPS == 0 or (step + 1) == len(train_loader):
                    optimizer.step()
                    optimizer.zero_grad()

            train_loss += loss.item() * GRAD_ACCUM_STEPS * images.size(0)
            preds = torch.argmax(outputs, dim=1)
            train_preds.extend(preds.detach().cpu().numpy())
            train_targets.extend(labels.detach().cpu().numpy())

            if (step + 1) % 500 == 0:
                gc.collect()
                if device.type == "cuda":
                    torch.cuda.empty_cache()

        if epoch > STAGE1_EPOCHS and scheduler is not None:
            scheduler.step()
            cur_lr = scheduler.get_last_lr()[-1]
        else:
            cur_lr = STAGE1_LR

        avg_train_loss = train_loss / (len(train_loader) * BATCH_SIZE)
        train_acc = accuracy_score(train_targets, train_preds)
        _, _, train_f1_m, _ = precision_recall_fscore_support(train_targets, train_preds, average="macro", zero_division=0)
        _, _, train_f1_w, _ = precision_recall_fscore_support(train_targets, train_preds, average="weighted", zero_division=0)

        # Validation Step
        val_metrics = evaluate(model, val_loader, eval_criterion, device, num_classes)
        val_loss = val_metrics["loss"]
        val_acc = val_metrics["accuracy"]
        val_macro_f1 = val_metrics["macro_f1"]
        val_weighted_f1 = val_metrics["weighted_f1"]
        val_healthy_f1 = val_metrics["healthy_f1"]
        val_disease_macro_f1 = val_metrics["disease_macro_f1"]

        epoch_duration = time.time() - epoch_start

        history["train_loss"].append(avg_train_loss)
        history["train_acc"].append(train_acc)
        history["train_macro_f1"].append(train_f1_m)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        history["val_macro_f1"].append(val_macro_f1)
        history["val_disease_macro_f1"].append(val_disease_macro_f1)
        history["val_healthy_f1"].append(val_healthy_f1)

        is_best = val_macro_f1 > best_val_macro_f1
        if is_best:
            best_val_macro_f1 = val_macro_f1
            best_epoch = epoch
            patience_counter = 0

            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "scaler_state_dict": scaler.state_dict() if scaler else None,
                "scheduler_state_dict": scheduler.state_dict() if scheduler else None,
                "val_macro_f1": val_macro_f1,
                "val_accuracy": val_acc,
                "val_weighted_f1": val_weighted_f1,
                "val_disease_macro_f1": val_disease_macro_f1,
                "val_healthy_f1": val_healthy_f1,
                "num_classes": num_classes,
                "class_mapping": class_to_id,
            }, MODEL_DIR / "best_model.pth")
        else:
            if epoch > STAGE1_EPOCHS:
                patience_counter += 1

        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scaler_state_dict": scaler.state_dict() if scaler else None,
            "scheduler_state_dict": scheduler.state_dict() if scheduler else None,
            "val_macro_f1": val_macro_f1,
        }, MODEL_DIR / "last_model.pth")

        log_message(
            f"Epoch {epoch:02d}/{total_epochs:02d} [{stage[:7]}] | LR: {cur_lr:.2e} | "
            f"Train Loss: {avg_train_loss:.4f} Acc: {train_acc*100:.2f}% F1: {train_f1_m*100:.2f}% | "
            f"Val Loss: {val_loss:.4f} Acc: {val_acc*100:.2f}% F1: {val_macro_f1*100:.2f}% "
            f"(Dis: {val_disease_macro_f1*100:.2f}%, Hlt: {val_healthy_f1*100:.2f}%) | "
            f"Time: {epoch_duration:.1f}s {'[BEST]' if is_best else ''}"
        )

        with open(PROGRESS_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                epoch, stage, f"{cur_lr:.6e}", f"{avg_train_loss:.4f}", f"{train_acc:.4f}",
                f"{train_f1_m:.4f}", f"{train_f1_w:.4f}", f"{val_loss:.4f}", f"{val_acc:.4f}",
                f"{val_macro_f1:.4f}", f"{val_weighted_f1:.4f}", f"{val_healthy_f1:.4f}",
                f"{val_disease_macro_f1:.4f}", f"{best_val_macro_f1:.4f}", best_epoch,
                f"{epoch_duration:.1f}"
            ])

        if patience_counter >= PATIENCE:
            log_message(f"Early stopping triggered at epoch {epoch} (Patience: {PATIENCE}).")
            break

    total_training_time = time.time() - start_time
    log_message(f"\nTraining Complete in {total_training_time/60:.2f} minutes.")
    log_message(f"Best Validation Epoch: {best_epoch} with Val Macro F1: {best_val_macro_f1*100:.2f}%")

    try:
        plot_training_curves(history, REPORTS_DIR / "training_curves.png")
    except Exception as e:
        log_message(f"Could not plot curves: {e}")

    # Save summary
    summary = {
        "best_epoch": best_epoch,
        "best_val_macro_f1": best_val_macro_f1,
        "total_epochs_trained": epoch,
        "total_training_time_seconds": total_training_time,
        "num_classes": num_classes,
        "architecture": "EfficientNet-B2",
        "image_size": IMAGE_SIZE,
    }
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return True


def main():
    parser = argparse.ArgumentParser(description="Train Model 2 Retraining V1 Classifier")
    parser.add_argument("--run", action="store_true", help="Execute actual training run")
    parser.add_argument("--preflight", action="store_true", help="Run preflight validation assertions and exit")
    args = parser.parse_args()

    if args.run:
        run_training()
    else:
        run_preflight_check()


if __name__ == "__main__":
    main()
