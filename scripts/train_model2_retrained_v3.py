"""Train Model 2 (Disease Classifier) Retrained V3 (EfficientNet-B2, 152 Classes)
================================================================================
Strict Safety & Isolation Constraints:
- Production Model 2 (models/model2_retraining_v2/ and models/model2_classifier_v4/) are strictly UNTOUCHED.
- Warm-starts from models/model2_retraining_v2/best_model.pth:
    - Backbone weights preserved 100%.
    - Classifier head extended from 144 to 152 classes (weights 0..143 copied; weights 144..151 initialized with He normal).
- Immutable test set (data/processed/model2_retraining_v2/test/) is NOT trained on.
- Output artifacts saved strictly to models/model2_retrained_v3/ and reports/model2_retrained_v3/.
- Optimized for NVIDIA GeForce RTX 3050 Laptop GPU (4 GB VRAM) on Windows.
"""

from __future__ import annotations

import argparse
import csv
import gc
import json
import logging
import os
import random
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from torch.amp import GradScaler, autocast
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import efficientnet_b2

# Clean up PYTORCH_CUDA_ALLOC_CONF if set to avoid Windows CUDA allocator warnings
if "PYTORCH_CUDA_ALLOC_CONF" in os.environ and "expandable_segments" in os.environ["PYTORCH_CUDA_ALLOC_CONF"]:
    del os.environ["PYTORCH_CUDA_ALLOC_CONF"]

# Paths
PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
DATASET_DIR = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v2"
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v3_manifest.csv"
INIT_CHECKPOINT_PATH = PROJECT_ROOT / "models" / "model2_retraining_v2" / "best_model.pth"

MODEL_DIR = PROJECT_ROOT / "models" / "model2_retrained_v3"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_retrained_v3"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

CLASS_MAPPING_PATH = MODEL_DIR / "class_mapping.json"
CROP_DISEASE_MAP_PATH = MODEL_DIR / "crop_disease_mapping.json"
PROGRESS_CSV = REPORTS_DIR / "training_progress.csv"
TRAINING_LOG = REPORTS_DIR / "training.log"
CONFIG_PATH = MODEL_DIR / "config.json"
SUMMARY_PATH = MODEL_DIR / "training_summary.json"
BEST_MODEL_PATH = MODEL_DIR / "best_model.pth"
LAST_MODEL_PATH = MODEL_DIR / "last_model.pth"

# Hyperparameters
IMAGE_SIZE = (260, 260)  # Native EfficientNet-B2
MICRO_BATCH_SIZE = 8     # 4 GB VRAM safe
GRAD_ACCUM_STEPS = 4     # Effective batch size = 32
EPOCHS = 15
PATIENCE = 4
LEARNING_RATE_BACKBONE = 1e-4
LEARNING_RATE_HEAD_OLD = 2e-4
LEARNING_RATE_HEAD_NEW = 1e-3
WEIGHT_DECAY = 1e-2
RANDOM_SEED = 42

logger = logging.getLogger("Model2RetrainedV3")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(TRAINING_LOG, mode="w", encoding="utf-8")
console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.handlers.clear()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def set_seed(seed=RANDOM_SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class Model2Dataset(Dataset):
    """Memory-safe dataset loader with libjpeg draft downsampling."""

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
                    raw.draft("RGB", (320, 320))
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


def atomic_torch_save(payload: dict, target_path: Path):
    temp_path = target_path.parent / f".{target_path.name}.tmp"
    torch.save(payload, temp_path)
    os.replace(temp_path, target_path)


def build_warm_start_model(num_classes: int, init_checkpoint_path: Path, device: torch.device):
    """Build EfficientNet-B2 and transfer weights from checkpoint, adapting classifier from 144 to num_classes."""
    logger.info(f"Building EfficientNet-B2 with {num_classes} output classes...")
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)

    if init_checkpoint_path.exists():
        logger.info(f"Loading warm-start checkpoint from: {init_checkpoint_path}")
        chk = torch.load(init_checkpoint_path, map_location="cpu", weights_only=False)
        state_dict = chk.get("model_state_dict", chk)

        old_weight = state_dict.get("classifier.1.weight")
        old_bias = state_dict.get("classifier.1.bias")

        if old_weight is not None and old_weight.shape[0] != num_classes:
            old_num = old_weight.shape[0]
            logger.info(f"Adapting classifier head from {old_num} classes to {num_classes} classes...")
            new_weight = torch.empty(num_classes, in_features)
            new_bias = torch.zeros(num_classes)
            nn.init.kaiming_normal_(new_weight, nonlinearity="linear")

            copy_len = min(old_num, num_classes)
            new_weight[:copy_len] = old_weight[:copy_len]
            if old_bias is not None:
                new_bias[:copy_len] = old_bias[:copy_len]

            state_dict["classifier.1.weight"] = new_weight
            state_dict["classifier.1.bias"] = new_bias

        model.load_state_dict(state_dict, strict=True)
        logger.info("Successfully loaded backbone and transferred pre-trained classifier weights.")
    else:
        logger.warning(f"Initial checkpoint not found at {init_checkpoint_path}. Training from scratch.")

    return model.to(device)


def run_training():
    set_seed(RANDOM_SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

    logger.info("=" * 80)
    logger.info("STARTING MODEL 2 RETRAINED V3 PIPELINE (152 CLASSES)")
    logger.info(f"Execution Device : {device} ({gpu_name})")
    logger.info(f"Micro-batch      : {MICRO_BATCH_SIZE} | Accumulation Steps: {GRAD_ACCUM_STEPS} (Effective batch: {MICRO_BATCH_SIZE*GRAD_ACCUM_STEPS})")
    logger.info(f"Resolution       : {IMAGE_SIZE} | Epochs: {EPOCHS} | Patience: {PATIENCE}")
    logger.info("=" * 80)

    # 1. Load Mappings
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_to_id = json.load(f)
    num_classes = len(class_to_id)
    id_to_class = {int(v): k for k, v in class_to_id.items()}

    # 2. Load Manifest Records
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

    logger.info(f"Total Canonical Classes : {num_classes}")
    logger.info(f"Train Images            : {len(train_samples):,}")
    logger.info(f"Val Images              : {len(val_samples):,}")
    logger.info(f"Test Images (Immutable) : {len(test_samples):,}")

    train_tf, val_test_tf = get_transforms()
    train_dataset = Model2Dataset(train_samples, DATASET_DIR, transform=train_tf)
    val_dataset = Model2Dataset(val_samples, DATASET_DIR, transform=val_test_tf)
    test_dataset = Model2Dataset(test_samples, DATASET_DIR, transform=val_test_tf)

    train_loader = DataLoader(
        train_dataset,
        batch_size=MICRO_BATCH_SIZE,
        shuffle=True,
        num_workers=0,
        pin_memory=False,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=MICRO_BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=MICRO_BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
    )

    # 3. Model & Differential Optimizer
    model = build_warm_start_model(num_classes, INIT_CHECKPOINT_PATH, device)

    # Parameter groups for differential learning rates
    backbone_params = []
    head_params = []
    for name, param in model.named_parameters():
        if "classifier" in name:
            head_params.append(param)
        else:
            backbone_params.append(param)

    optimizer = torch.optim.AdamW([
        {"params": backbone_params, "lr": LEARNING_RATE_BACKBONE},
        {"params": head_params, "lr": LEARNING_RATE_HEAD_OLD},
    ], weight_decay=WEIGHT_DECAY)

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=1e-6)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    scaler = GradScaler("cuda", enabled=(device.type == "cuda"))

    # 4. Training Loop
    best_val_macro_f1 = -1.0
    best_val_acc = -1.0
    best_epoch = 0
    patience_counter = 0
    progress_records = []

    for epoch in range(1, EPOCHS + 1):
        t_start = time.time()
        model.train()
        train_loss_sum = 0.0
        train_preds_all = []
        train_targets_all = []

        optimizer.zero_grad(set_to_none=True)

        for step, (images, targets, _) in enumerate(train_loader):
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            with autocast("cuda", enabled=(device.type == "cuda")):
                outputs = model(images)
                loss = criterion(outputs, targets)
                scaled_loss = loss / GRAD_ACCUM_STEPS

            scaler.scale(scaled_loss).backward()

            if (step + 1) % GRAD_ACCUM_STEPS == 0 or (step + 1) == len(train_loader):
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)

            train_loss_sum += loss.item() * targets.size(0)
            _, predicted = outputs.max(1)
            train_preds_all.extend(predicted.cpu().numpy())
            train_targets_all.extend(targets.cpu().numpy())

        scheduler.step()
        epoch_time = time.time() - t_start
        train_loss = train_loss_sum / len(train_targets_all)
        train_acc = float(np.mean(np.array(train_targets_all) == np.array(train_preds_all)))
        train_macro_f1 = float(f1_score(train_targets_all, train_preds_all, average="macro", zero_division=0))

        # Validation
        model.eval()
        val_loss_sum = 0.0
        val_preds_all = []
        val_targets_all = []

        with torch.no_grad():
            for images, targets, _ in val_loader:
                images = images.to(device, non_blocking=True)
                targets = targets.to(device, non_blocking=True)

                with autocast("cuda", enabled=(device.type == "cuda")):
                    outputs = model(images)
                    loss = criterion(outputs, targets)

                val_loss_sum += loss.item() * targets.size(0)
                _, predicted = outputs.max(1)
                val_preds_all.extend(predicted.cpu().numpy())
                val_targets_all.extend(targets.cpu().numpy())

        val_loss = val_loss_sum / len(val_targets_all)
        val_acc = float(np.mean(np.array(val_targets_all) == np.array(val_preds_all)))
        val_macro_f1 = float(f1_score(val_targets_all, val_preds_all, average="macro", zero_division=0))

        logger.info(
            f"Epoch {epoch:02d}/{EPOCHS:02d} [{epoch_time:.1f}s] | "
            f"Train Loss: {train_loss:.4f} Acc: {train_acc*100:.2f}% F1: {train_macro_f1:.4f} | "
            f"Val Loss: {val_loss:.4f} Acc: {val_acc*100:.2f}% F1: {val_macro_f1:.4f}"
        )

        progress_records.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "train_acc": train_acc,
            "train_macro_f1": train_macro_f1,
            "val_loss": val_loss,
            "val_acc": val_acc,
            "val_macro_f1": val_macro_f1,
            "epoch_time_seconds": epoch_time,
        })

        checkpoint_payload = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "val_accuracy": val_acc,
            "val_macro_f1": val_macro_f1,
            "class_mapping": class_to_id,
            "num_classes": num_classes,
        }
        atomic_torch_save(checkpoint_payload, LAST_MODEL_PATH)

        if val_macro_f1 > best_val_macro_f1:
            best_val_macro_f1 = val_macro_f1
            best_val_acc = val_acc
            best_epoch = epoch
            patience_counter = 0
            atomic_torch_save(checkpoint_payload, BEST_MODEL_PATH)
            logger.info(f"  --> [NEW BEST] Epoch {epoch:02d} | Val Macro F1: {val_macro_f1:.4f} | Val Acc: {val_acc*100:.2f}%")
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                logger.info(f"Early stopping triggered at Epoch {epoch:02d} (Patience: {PATIENCE})")
                break

    # Save training progress CSV
    with open(PROGRESS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(progress_records[0].keys()))
        writer.writeheader()
        writer.writerows(progress_records)

    # 5. Final Evaluation on Immutable Test Set
    logger.info("\n" + "=" * 80)
    logger.info("FINAL TEST EVALUATION ON IMMUTABLE BENCHMARK")
    logger.info("=" * 80)

    best_chk = torch.load(BEST_MODEL_PATH, map_location=device, weights_only=False)
    model.load_state_dict(best_chk["model_state_dict"])
    model.eval()

    test_preds_all = []
    test_targets_all = []
    with torch.no_grad():
        for images, targets, _ in test_loader:
            images = images.to(device, non_blocking=True)
            with autocast("cuda", enabled=(device.type == "cuda")):
                outputs = model(images)
            _, predicted = outputs.max(1)
            test_preds_all.extend(predicted.cpu().numpy())
            test_targets_all.extend(targets.numpy())

    test_acc = float(np.mean(np.array(test_targets_all) == np.array(test_preds_all)))
    test_macro_f1 = float(f1_score(test_targets_all, test_preds_all, average="macro", zero_division=0))
    test_weighted_f1 = float(f1_score(test_targets_all, test_preds_all, average="weighted", zero_division=0))

    logger.info(f"Test Accuracy    : {test_acc*100:.2f}%")
    logger.info(f"Test Macro F1    : {test_macro_f1:.4f}")
    logger.info(f"Test Weighted F1 : {test_weighted_f1:.4f}")

    present_classes = sorted(list(set(test_targets_all) | set(test_preds_all)))
    present_class_names = [id_to_class.get(c, f"class_{c}") for c in present_classes]
    cls_report = classification_report(
        test_targets_all,
        test_preds_all,
        labels=present_classes,
        target_names=present_class_names,
        output_dict=True,
        zero_division=0,
    )
    with open(REPORTS_DIR / "test_classification_report.json", "w", encoding="utf-8") as f:
        json.dump(cls_report, f, indent=2)

    cm = confusion_matrix(test_targets_all, test_preds_all, labels=present_classes).tolist()
    with open(REPORTS_DIR / "test_confusion_matrix.json", "w", encoding="utf-8") as f:
        json.dump({"labels": present_class_names, "matrix": cm}, f, indent=2)

    summary = {
        "best_epoch": best_epoch,
        "best_val_macro_f1": best_val_macro_f1,
        "best_val_accuracy": best_val_acc,
        "test_macro_f1": test_macro_f1,
        "test_weighted_f1": test_weighted_f1,
        "test_accuracy": test_acc,
        "num_classes": num_classes,
        "total_train_samples": len(train_dataset),
        "total_val_samples": len(val_dataset),
        "total_test_samples": len(test_dataset),
    }
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info("Model 2 Retrained V3 Pipeline Completed Successfully.")
    return summary


if __name__ == "__main__":
    run_training()
