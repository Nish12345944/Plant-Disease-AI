"""Train Model 1 (Crop Classifier) Retrained V3 (EfficientNet-B2, 46 Classes)
================================================================================
Strict Safety & Isolation Constraints:
- Production Model 1 (models/model1/ and models/model1_expanded/) are strictly UNTOUCHED.
- Model 2 (models/model2_retraining_v2/) is strictly UNTOUCHED.
- Immutable test set (data/processed/model1_expanded/test/) is NOT trained on.
- Output artifacts saved strictly to models/model1_retrained_v3/ and reports/model1_retrained_v3/.
- Optimized for NVIDIA GeForce RTX 3050 Laptop GPU (4 GB VRAM) on Windows.
"""

from __future__ import annotations

import csv
import json
import logging
import os
import random
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
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
from torchvision import transforms
from torchvision.models import EfficientNet_B2_Weights, efficientnet_b2

# Root and Isolated Paths
ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
DATASET_DIR = ROOT / "data" / "processed" / "model1_expanded"
CLASS_MAPPING_PATH = ROOT / "data" / "processed" / "model1_expanded_class_mapping.json"
MODELS_DIR = ROOT / "models" / "model1_retrained_v3"
REPORTS_DIR = ROOT / "reports" / "model1_retrained_v3"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

BEST_MODEL_PATH = MODELS_DIR / "best_model.pth"
LAST_MODEL_PATH = MODELS_DIR / "last_model.pth"
EXPORT_CLASS_MAPPING_PATH = MODELS_DIR / "class_mapping.json"
CONFIG_PATH = MODELS_DIR / "config.json"
TRAINING_SUMMARY_PATH = MODELS_DIR / "training_summary.json"

REPORT_MD_PATH = REPORTS_DIR / "model1_training_report.md"
TRAINING_METRICS_CSV = REPORTS_DIR / "model1_training_metrics.csv"
TEST_METRICS_CSV = REPORTS_DIR / "model1_test_metrics.csv"
PER_CLASS_METRICS_CSV = REPORTS_DIR / "model1_per_class_metrics.csv"
CONFUSION_MATRIX_CSV = REPORTS_DIR / "model1_confusion_matrix.csv"
CONFUSION_PAIRS_CSV = REPORTS_DIR / "model1_confusion_pairs.csv"
TRAINING_LOG_PATH = REPORTS_DIR / "model1_training.log"
CONFUSION_MATRIX_PNG = REPORTS_DIR / "model1_confusion_matrix.png"
TRAINING_CURVES_PNG = REPORTS_DIR / "model1_training_curves.png"

# Setup Logger
logger = logging.getLogger("Model1RetrainedV3")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(TRAINING_LOG_PATH, mode="w", encoding="utf-8")
console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.handlers.clear()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Training Hyperparameters
IMAGE_SIZE = 224
BATCH_SIZE = 16  # Safe for 4 GB RTX 3050 Laptop VRAM
EPOCHS = 15
LEARNING_RATE = 3e-4
WEIGHT_DECAY = 1e-4
PATIENCE = 4
SEED = 42

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class ExpandedPlantDataset(Dataset):
    """Memory-safe dataset loader with support for all image extensions."""

    def __init__(self, split_dir, sorted_classes, class_to_idx, transform=None):
        self.split_dir = Path(split_dir)
        self.sorted_classes = sorted_classes
        self.class_to_idx = class_to_idx
        self.transform = transform
        self.samples = []

        for c in sorted_classes:
            c_dir = self.split_dir / c
            if c_dir.exists() and c_dir.is_dir():
                idx = class_to_idx[c]
                for p in sorted(c_dir.iterdir()):
                    if p.is_file() and p.suffix.lower() in VALID_EXTS:
                        self.samples.append((str(p), idx))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, target = self.samples[idx]
        with open(path, "rb") as f:
            img = Image.open(f).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, target, path


def get_transforms():
    train_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15, hue=0.03),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    eval_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    return train_transform, eval_transform


def atomic_torch_save(payload: dict, target_path: Path):
    """Save PyTorch checkpoint atomically."""
    temp_path = target_path.parent / f".{target_path.name}.tmp"
    torch.save(payload, temp_path)
    os.replace(temp_path, target_path)


def train_and_evaluate():
    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    logger.info("=" * 80)
    logger.info("STARTING MODEL 1 RETRAINED V3 PIPELINE (46 CLASSES)")
    logger.info(f"Device: {device} ({gpu_name})")
    logger.info(f"Batch Size: {BATCH_SIZE} | Image Size: {IMAGE_SIZE} | Epochs: {EPOCHS} | LR: {LEARNING_RATE}")
    logger.info("=" * 80)

    # 1. Load Class Mapping
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)

    class_to_idx = mapping_data["class_to_idx"]
    idx_to_class = {int(k): v for k, v in mapping_data["idx_to_class"].items()}
    sorted_classes = [idx_to_class[i] for i in range(len(class_to_idx))]
    num_classes = len(sorted_classes)
    assert num_classes == 46, f"Expected 46 classes, got {num_classes}"

    # Export mapping
    with open(EXPORT_CLASS_MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(mapping_data, f, indent=2)

    # 2. Datasets
    train_tf, eval_tf = get_transforms()
    train_dataset = ExpandedPlantDataset(DATASET_DIR / "train", sorted_classes, class_to_idx, transform=train_tf)
    val_dataset = ExpandedPlantDataset(DATASET_DIR / "val", sorted_classes, class_to_idx, transform=eval_tf)
    test_dataset = ExpandedPlantDataset(DATASET_DIR / "test", sorted_classes, class_to_idx, transform=eval_tf)

    logger.info(f"Train Dataset : {len(train_dataset):,} samples")
    logger.info(f"Val Dataset   : {len(val_dataset):,} samples")
    logger.info(f"Test Dataset  : {len(test_dataset):,} samples (IMMUTABLE)")

    # 3. Class Imbalance Strategy
    train_targets = [s[1] for s in train_dataset.samples]
    class_counts = Counter(train_targets)

    active_counts = [cnt for cnt in class_counts.values() if cnt > 0]
    median_cnt = float(np.median(active_counts)) if active_counts else 100.0

    raw_loss_weights = {}
    for c_idx in range(num_classes):
        cnt = class_counts.get(c_idx, 0)
        if cnt > 0:
            raw_w = (median_cnt / max(cnt, 2)) ** 0.35
            raw_loss_weights[c_idx] = float(np.clip(raw_w, 0.3, 3.5))
        else:
            raw_loss_weights[c_idx] = 0.0

    active_sum = sum(v for v in raw_loss_weights.values() if v > 0)
    active_num = sum(1 for v in raw_loss_weights.values() if v > 0)
    mean_w = active_sum / max(1, active_num)
    final_loss_weights = [raw_loss_weights[i] / mean_w if raw_loss_weights[i] > 0 else 0.0 for i in range(num_classes)]
    class_weights_tensor = torch.tensor(final_loss_weights, dtype=torch.float, device=device)

    raw_sample_weights = {}
    for c_idx in range(num_classes):
        cnt = class_counts.get(c_idx, 0)
        if cnt > 0:
            raw_sample_weights[c_idx] = float(np.clip((median_cnt / max(cnt, 2)) ** 0.20, 0.4, 2.5))
        else:
            raw_sample_weights[c_idx] = 0.0

    sample_weights = [raw_sample_weights[t] for t in train_targets]
    sampler = WeightedRandomSampler(weights=sample_weights, num_samples=len(train_dataset), replacement=True)

    # 4. DataLoaders (Windows VRAM & process safe)
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        sampler=sampler,
        num_workers=0,
        pin_memory=False,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
    )

    # 5. Model Setup
    logger.info("Initializing EfficientNet-B2 backbone...")
    model = efficientnet_b2(weights=EfficientNet_B2_Weights.DEFAULT)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=1e-6)
    scaler = torch.amp.GradScaler("cuda", enabled=(device.type == "cuda"))

    # 6. Training Loop
    training_metrics_records = []
    best_val_macro_f1 = -1.0
    best_val_acc = -1.0
    best_epoch = 0
    patience_counter = 0

    for epoch in range(1, EPOCHS + 1):
        t_start = time.time()
        model.train()
        train_loss_sum = 0.0
        train_preds_all = []
        train_targets_all = []

        for images, targets, _ in train_loader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)

            with torch.amp.autocast("cuda", enabled=(device.type == "cuda")):
                outputs = model(images)
                loss = criterion(outputs, targets)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            train_loss_sum += loss.item() * targets.size(0)
            _, predicted = outputs.max(1)
            train_preds_all.extend(predicted.cpu().numpy())
            train_targets_all.extend(targets.cpu().numpy())

        scheduler.step()
        epoch_time_seconds = time.time() - t_start
        train_loss = train_loss_sum / len(train_targets_all)
        train_accuracy = float(np.mean(np.array(train_targets_all) == np.array(train_preds_all)))
        train_macro_f1 = float(f1_score(train_targets_all, train_preds_all, average="macro", zero_division=0))

        # Validation Loop
        model.eval()
        val_loss_sum = 0.0
        val_preds_all = []
        val_targets_all = []

        with torch.no_grad():
            for images, targets, _ in val_loader:
                images = images.to(device, non_blocking=True)
                targets = targets.to(device, non_blocking=True)

                with torch.amp.autocast("cuda", enabled=(device.type == "cuda")):
                    outputs = model(images)
                    loss = criterion(outputs, targets)

                val_loss_sum += loss.item() * targets.size(0)
                _, predicted = outputs.max(1)
                val_preds_all.extend(predicted.cpu().numpy())
                val_targets_all.extend(targets.cpu().numpy())

        val_loss = val_loss_sum / len(val_targets_all)
        val_accuracy = float(np.mean(np.array(val_targets_all) == np.array(val_preds_all)))
        val_macro_f1 = float(f1_score(val_targets_all, val_preds_all, average="macro", zero_division=0))

        logger.info(
            f"Epoch {epoch:02d}/{EPOCHS:02d} [{epoch_time_seconds:.1f}s] | "
            f"Train Loss: {train_loss:.4f} Acc: {train_accuracy*100:.2f}% F1: {train_macro_f1:.4f} | "
            f"Val Loss: {val_loss:.4f} Acc: {val_accuracy*100:.2f}% F1: {val_macro_f1:.4f}"
        )

        training_metrics_records.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "train_accuracy": train_accuracy,
            "train_macro_f1": train_macro_f1,
            "val_loss": val_loss,
            "val_accuracy": val_accuracy,
            "val_macro_f1": val_macro_f1,
            "epoch_time_seconds": epoch_time_seconds,
        })

        checkpoint_payload = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "val_accuracy": val_accuracy,
            "val_macro_f1": val_macro_f1,
            "class_to_idx": class_to_idx,
            "idx_to_class": idx_to_class,
            "num_classes": num_classes,
        }
        atomic_torch_save(checkpoint_payload, LAST_MODEL_PATH)

        if val_macro_f1 > best_val_macro_f1:
            best_val_macro_f1 = val_macro_f1
            best_val_acc = val_accuracy
            best_epoch = epoch
            patience_counter = 0
            atomic_torch_save(checkpoint_payload, BEST_MODEL_PATH)
            logger.info(f"  --> [NEW BEST] Epoch {epoch:02d} | Val F1: {val_macro_f1:.4f} | Val Acc: {val_accuracy*100:.2f}%")
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                logger.info(f"Early stopping triggered at Epoch {epoch:02d} (Patience: {PATIENCE})")
                break

    # Save training progress CSV
    with open(TRAINING_METRICS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(training_metrics_records[0].keys()))
        writer.writeheader()
        writer.writerows(training_metrics_records)

    # 7. Final Test Evaluation on Immutable Benchmark
    logger.info("\n" + "=" * 80)
    logger.info("EVALUATING BEST MODEL ON IMMUTABLE TEST SET")
    logger.info("=" * 80)

    best_chk = torch.load(BEST_MODEL_PATH, map_location=device)
    model.load_state_dict(best_chk["model_state_dict"])
    model.eval()

    test_preds_all = []
    test_targets_all = []
    with torch.no_grad():
        for images, targets, _ in test_loader:
            images = images.to(device, non_blocking=True)
            with torch.amp.autocast("cuda", enabled=(device.type == "cuda")):
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

    # Write summary
    summary = {
        "best_epoch": best_epoch,
        "best_val_macro_f1": best_val_macro_f1,
        "best_val_accuracy": best_val_acc,
        "test_macro_f1": test_macro_f1,
        "test_accuracy": test_acc,
        "num_classes": num_classes,
        "total_train_samples": len(train_dataset),
        "total_val_samples": len(val_dataset),
        "total_test_samples": len(test_dataset),
    }
    with open(TRAINING_SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"Model 1 Retrained V3 Pipeline Completed Successfully.")
    return summary


if __name__ == "__main__":
    train_and_evaluate()
