"""Train Model 1 (EfficientNet-B2) on Final Balanced Dataset (22 Target Classes).

Pipeline:
- Architecture: EfficientNet-B2 with ImageNet transfer learning.
- Dataset: data/processed/model1_balanced/ (train/val/test untouched).
- Class-aware handling: Smooth class-weighted CrossEntropyLoss and WeightedRandomSampler.
- Training augmentation: HorizontalFlip, RandomRotation, ColorJitter, ImageNet Normalization.
- Evaluation on untouched test split: Top-1, Top-3, per-class P/R/F1, confusion matrix, confidence table.
- Output artifacts saved to models/model1/ and reports/model1/.
"""

import csv
import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
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

# Paths
ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
BALANCED_DIR = ROOT / "data" / "processed" / "model1_balanced"
MODELS_DIR = ROOT / "models" / "model1"
REPORTS_DIR = ROOT / "reports" / "model1"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

BEST_MODEL_PATH = MODELS_DIR / "best_model.pth"
CLASS_MAPPING_PATH = MODELS_DIR / "class_mapping.json"
CONFIG_PATH = MODELS_DIR / "config.json"
TRAINING_REPORT_JSON = MODELS_DIR / "training_report.json"

REPORT_MD_PATH = REPORTS_DIR / "model1_training_report.md"
REPORT_CSV_PATH = REPORTS_DIR / "classification_report.csv"
CONFUSION_MATRIX_PNG = REPORTS_DIR / "confusion_matrix.png"
TRAINING_CURVES_PNG = REPORTS_DIR / "training_curves.png"
TEST_PREDICTIONS_CSV = REPORTS_DIR / "test_predictions.csv"

# Configuration
TARGET_CLASSES = [
    "tomato", "cucumber", "rose", "spinach", "capsicum", "orchid", "lettuce",
    "strawberry", "marigold", "broccoli", "chrysanthemum", "zucchini",
    "blueberry", "geranium", "melon", "french_bean", "anthurium", "carnation",
    "gerbera", "cherry_tomato", "lilium", "gypsophila"
]
SORTED_CLASSES = sorted(TARGET_CLASSES)
CLASS_TO_IDX = {c: i for i, c in enumerate(SORTED_CLASSES)}
IDX_TO_CLASS = {i: c for c, i in CLASS_TO_IDX.items()}
NUM_CLASSES = len(SORTED_CLASSES)

IMAGE_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 10
LEARNING_RATE = 3e-4
WEIGHT_DECAY = 1e-4
PATIENCE = 3
SEED = 42

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

class BalancedPlantDataset(Dataset):
    def __init__(self, split_dir, classes, class_to_idx, transform=None):
        self.split_dir = Path(split_dir)
        self.classes = classes
        self.class_to_idx = class_to_idx
        self.transform = transform
        self.samples = []
        for c in classes:
            c_dir = self.split_dir / c
            if c_dir.exists():
                idx = class_to_idx[c]
                for p in sorted(c_dir.glob("*.jpg")):
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

def train_and_evaluate():
    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 80)
    print("STARTING MODEL 1 TRAINING PIPELINE (EFFICIENTNET-B2)")
    print(f"Device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
    print(f"Random Seed: {SEED}")
    print(f"Target Classes ({NUM_CLASSES}): {SORTED_CLASSES}")
    print("=" * 80)

    train_tf, eval_tf = get_transforms()

    train_dataset = BalancedPlantDataset(BALANCED_DIR / "train", SORTED_CLASSES, CLASS_TO_IDX, transform=train_tf)
    val_dataset = BalancedPlantDataset(BALANCED_DIR / "val", SORTED_CLASSES, CLASS_TO_IDX, transform=eval_tf)
    test_dataset = BalancedPlantDataset(BALANCED_DIR / "test", SORTED_CLASSES, CLASS_TO_IDX, transform=eval_tf)

    print(f"\n[Dataset Partitions]")
    print(f"  Train : {len(train_dataset):,} samples")
    print(f"  Val   : {len(val_dataset):,} samples")
    print(f"  Test  : {len(test_dataset):,} samples")

    # Class distribution and class-aware weighting
    train_targets = [s[1] for s in train_dataset.samples]
    class_counts = Counter(train_targets)
    print("\n[Train Set Per-Class Counts]")
    for c_idx in range(NUM_CLASSES):
        c_name = IDX_TO_CLASS[c_idx]
        cnt = class_counts.get(c_idx, 0)
        print(f"  [{c_idx:2d}] {c_name:<15}: {cnt:,} samples")

    # Compute smoothed class weights for CrossEntropyLoss
    active_weights = {}
    for c_idx in range(NUM_CLASSES):
        cnt = class_counts.get(c_idx, 0)
        if cnt > 0:
            active_weights[c_idx] = 1.0 / (cnt ** 0.5)
        else:
            active_weights[c_idx] = 0.0

    mean_weight = sum(active_weights.values()) / max(1, sum(1 for v in active_weights.values() if v > 0))
    class_weights_list = [active_weights[i] / mean_weight if active_weights[i] > 0 else 0.0 for i in range(NUM_CLASSES)]
    class_weights_tensor = torch.tensor(class_weights_list, dtype=torch.float, device=device)

    # WeightedRandomSampler for class-aware training
    sample_weights = [active_weights[target] for _, target in train_dataset.samples]
    sampler = WeightedRandomSampler(sample_weights, num_samples=len(train_dataset), replacement=True)

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        sampler=sampler,
        num_workers=2,
        pin_memory=True if device.type == "cuda" else False,
        persistent_workers=True,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=2,
        pin_memory=True if device.type == "cuda" else False,
        persistent_workers=True,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=2,
        pin_memory=True if device.type == "cuda" else False,
        persistent_workers=True,
    )

    # Initialize EfficientNet-B2
    print("\n[Model Initialization]")
    print("Loading pretrained EfficientNet-B2 weights...")
    weights = EfficientNet_B2_Weights.DEFAULT
    model = efficientnet_b2(weights=weights)

    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, NUM_CLASSES)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=1e-6)
    scaler = torch.cuda.amp.GradScaler(enabled=(device.type == "cuda"))

    # Training Loop
    history = {
        "train_loss": [], "train_acc": [],
        "val_loss": [], "val_acc": [], "val_macro_f1": [],
        "lr": [], "epoch_time": [],
    }

    best_val_f1 = -1.0
    best_epoch = 0
    patience_counter = 0

    print("\n" + "=" * 80)
    print("STARTING TRAINING LOOP")
    print("=" * 80)

    for epoch in range(1, EPOCHS + 1):
        t_start = time.time()
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, targets, _ in train_loader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)

            with torch.cuda.amp.autocast(enabled=(device.type == "cuda")):
                outputs = model(images)
                loss = criterion(outputs, targets)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            running_loss += loss.item() * targets.size(0)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

        epoch_time = time.time() - t_start
        train_loss = running_loss / total
        train_acc = correct / total

        # Validation
        model.eval()
        val_loss_sum = 0.0
        val_targets_all = []
        val_preds_all = []

        with torch.no_grad():
            for images, targets, _ in val_loader:
                images = images.to(device, non_blocking=True)
                targets = targets.to(device, non_blocking=True)

                with torch.cuda.amp.autocast(enabled=(device.type == "cuda")):
                    outputs = model(images)
                    loss = criterion(outputs, targets)

                val_loss_sum += loss.item() * targets.size(0)
                _, predicted = outputs.max(1)
                val_targets_all.extend(targets.cpu().numpy())
                val_preds_all.extend(predicted.cpu().numpy())

        val_loss = val_loss_sum / len(val_targets_all)
        val_acc = np.mean(np.array(val_targets_all) == np.array(val_preds_all))
        val_macro_f1 = f1_score(val_targets_all, val_preds_all, average="macro", zero_division=0)

        current_lr = optimizer.param_groups[0]["lr"]
        scheduler.step()

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        history["val_macro_f1"].append(val_macro_f1)
        history["lr"].append(current_lr)
        history["epoch_time"].append(epoch_time)

        vram_mb = torch.cuda.max_memory_allocated() / (1024 ** 2) if device.type == "cuda" else 0.0
        print(f"Epoch [{epoch:02d}/{EPOCHS:02d}] | Train Loss: {train_loss:.4f} Acc: {train_acc*100:.2f}% | "
              f"Val Loss: {val_loss:.4f} Acc: {val_acc*100:.2f}% F1: {val_macro_f1*100:.2f}% | "
              f"LR: {current_lr:.2e} | Time: {epoch_time:.1f}s | VRAM: {vram_mb:.0f}MB")

        # Save Best Checkpoint
        if val_macro_f1 > best_val_f1:
            best_val_f1 = val_macro_f1
            best_epoch = epoch
            patience_counter = 0
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "val_macro_f1": val_macro_f1,
                "val_acc": val_acc,
                "class_to_idx": CLASS_TO_IDX,
                "sorted_classes": SORTED_CLASSES,
                "architecture": "efficientnet_b2",
                "image_size": IMAGE_SIZE,
                "mean": IMAGENET_MEAN,
                "std": IMAGENET_STD,
            }, BEST_MODEL_PATH)
            print(f"  >>> Best model saved at epoch {epoch:02d} (Val Macro F1: {val_macro_f1*100:.2f}%)")
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                print(f"\n[Early Stopping Triggered] No improvement in validation macro F1 for {PATIENCE} epochs.")
                break

    print("\n" + "=" * 80)
    print(f"TRAINING COMPLETE. Best Epoch: {best_epoch:02d} with Val Macro F1: {best_val_f1*100:.2f}%")
    print("=" * 80)

    # Load Best Model for Evaluation on Untouched Test Split
    print("\n[Evaluating Best Model on Untouched Test Set]")
    checkpoint = torch.load(BEST_MODEL_PATH, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    test_targets_all = []
    test_preds_all = []
    test_probs_all = []
    test_paths_all = []

    with torch.no_grad():
        for images, targets, paths in test_loader:
            images = images.to(device, non_blocking=True)
            with torch.cuda.amp.autocast(enabled=(device.type == "cuda")):
                outputs = model(images)
                probs = torch.softmax(outputs, dim=1)

            _, predicted = outputs.max(1)
            test_targets_all.extend(targets.cpu().numpy())
            test_preds_all.extend(predicted.cpu().numpy())
            test_probs_all.extend(probs.cpu().numpy())
            test_paths_all.extend(paths)

    test_targets = np.array(test_targets_all)
    test_preds = np.array(test_preds_all)
    test_probs = np.array(test_probs_all)

    # Top-1 and Top-3 Accuracy
    top1_correct = (test_preds == test_targets).sum()
    top1_acc = top1_correct / len(test_targets)

    # Top-3 Accuracy
    top3_preds = np.argsort(test_probs, axis=1)[:, -3:]
    top3_correct = sum(test_targets[i] in top3_preds[i] for i in range(len(test_targets)))
    top3_acc = top3_correct / len(test_targets)

    overall_acc = top1_acc
    macro_f1 = f1_score(test_targets, test_preds, average="macro", zero_division=0)
    weighted_f1 = f1_score(test_targets, test_preds, average="weighted", zero_division=0)
    macro_prec = precision_score(test_targets, test_preds, average="macro", zero_division=0)
    macro_rec = recall_score(test_targets, test_preds, average="macro", zero_division=0)

    print(f"\n[Test Set Results]")
    print(f"  Total Test Images : {len(test_targets):,}")
    print(f"  Top-1 Accuracy    : {top1_acc*100:.2f}% ({top1_correct}/{len(test_targets)})")
    print(f"  Top-3 Accuracy    : {top3_acc*100:.2f}% ({top3_correct}/{len(test_targets)})")
    print(f"  Macro F1 Score    : {macro_f1*100:.2f}%")
    print(f"  Weighted F1 Score : {weighted_f1*100:.2f}%")
    print(f"  Macro Precision   : {macro_prec*100:.2f}%")
    print(f"  Macro Recall      : {macro_rec*100:.2f}%")

    # Per-Class Metrics Table
    present_indices = sorted(list(set(test_targets)))
    clf_dict = classification_report(
        test_targets,
        test_preds,
        labels=list(range(NUM_CLASSES)),
        target_names=SORTED_CLASSES,
        output_dict=True,
        zero_division=0,
    )

    # Save classification_report.csv
    print(f"\nSaving {REPORT_CSV_PATH}...")
    with open(REPORT_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["class_name", "class_idx", "precision", "recall", "f1_score", "support"])
        for c_idx, c_name in enumerate(SORTED_CLASSES):
            metrics = clf_dict.get(c_name, {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 0})
            writer.writerow([
                c_name, c_idx,
                round(metrics["precision"], 4),
                round(metrics["recall"], 4),
                round(metrics["f1-score"], 4),
                metrics["support"]
            ])

    # Save test_predictions.csv
    print(f"Saving {TEST_PREDICTIONS_CSV}...")
    with open(TEST_PREDICTIONS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image_path", "true_class", "pred_class", "confidence", "correct", "top3_classes"])
        for i in range(len(test_targets)):
            true_c = IDX_TO_CLASS[test_targets[i]]
            pred_c = IDX_TO_CLASS[test_preds[i]]
            conf = float(test_probs[i][test_preds[i]])
            is_corr = int(true_c == pred_c)
            top3 = [IDX_TO_CLASS[idx] for idx in reversed(top3_preds[i])]
            rel_path = os.path.relpath(test_paths_all[i], ROOT)
            writer.writerow([rel_path, true_c, pred_c, round(conf, 4), is_corr, ";".join(top3)])

    # Confusion Matrix
    cm = confusion_matrix(test_targets, test_preds, labels=list(range(NUM_CLASSES)))

    # Save confusion_matrix.png
    plt.figure(figsize=(14, 12))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Model 1 Confusion Matrix (22 Target Classes)", fontsize=14, pad=15)
    plt.colorbar()
    tick_marks = np.arange(NUM_CLASSES)
    plt.xticks(tick_marks, SORTED_CLASSES, rotation=45, ha="right", fontsize=9)
    plt.yticks(tick_marks, SORTED_CLASSES, fontsize=9)
    plt.xlabel("Predicted Label", fontsize=11, labelpad=10)
    plt.ylabel("True Label", fontsize=11, labelpad=10)

    # Text annotations
    thresh = cm.max() / 2.0
    for i in range(NUM_CLASSES):
        for j in range(NUM_CLASSES):
            val = cm[i, j]
            if val > 0:
                plt.text(j, i, format(val, "d"),
                         ha="center", va="center",
                         color="white" if val > thresh else "black", fontsize=8)

    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_PNG, dpi=300)
    plt.close()
    print(f"Saved {CONFUSION_MATRIX_PNG}")

    # Training Curves PNG
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(history["train_loss"]) + 1), history["train_loss"], "b-o", label="Train Loss")
    plt.plot(range(1, len(history["val_loss"]) + 1), history["val_loss"], "r-s", label="Val Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Cross-Entropy Loss")
    plt.title("Training & Validation Loss")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(history["train_acc"]) + 1), [a * 100 for a in history["train_acc"]], "b-o", label="Train Acc (%)")
    plt.plot(range(1, len(history["val_acc"]) + 1), [a * 100 for a in history["val_acc"]], "r-s", label="Val Acc (%)")
    plt.plot(range(1, len(history["val_macro_f1"]) + 1), [f * 100 for f in history["val_macro_f1"]], "g-^", label="Val Macro F1 (%)")
    plt.xlabel("Epoch")
    plt.ylabel("Percentage (%)")
    plt.title("Training & Validation Performance")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(TRAINING_CURVES_PNG, dpi=300)
    plt.close()
    print(f"Saved {TRAINING_CURVES_PNG}")

    # Save class_mapping.json
    with open(CLASS_MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "class_to_idx": CLASS_TO_IDX,
            "idx_to_class": {str(k): v for k, v in IDX_TO_CLASS.items()},
            "target_classes": SORTED_CLASSES,
        }, f, indent=2)

    # Save config.json
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "model_architecture": "efficientnet_b2",
            "weights_pretrained": "ImageNet1K",
            "num_classes": NUM_CLASSES,
            "image_size": [IMAGE_SIZE, IMAGE_SIZE],
            "normalization": {
                "mean": IMAGENET_MEAN,
                "std": IMAGENET_STD,
            },
            "training_hyperparameters": {
                "batch_size": BATCH_SIZE,
                "learning_rate": LEARNING_RATE,
                "weight_decay": WEIGHT_DECAY,
                "optimizer": "AdamW",
                "scheduler": "CosineAnnealingLR",
                "epochs_trained": len(history["train_loss"]),
                "best_epoch": best_epoch,
                "seed": SEED,
            }
        }, f, indent=2)

    # Save training_report.json
    training_report_data = {
        "best_epoch": best_epoch,
        "best_val_macro_f1": best_val_f1,
        "test_overall_accuracy": top1_acc,
        "test_top1_accuracy": top1_acc,
        "test_top3_accuracy": top3_acc,
        "test_macro_f1": macro_f1,
        "test_weighted_f1": weighted_f1,
        "test_macro_precision": macro_prec,
        "test_macro_recall": macro_rec,
        "history": history,
        "per_class_metrics": {c: clf_dict[c] for c in SORTED_CLASSES if c in clf_dict},
    }
    with open(TRAINING_REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(training_report_data, f, indent=2)

    # Generate model1_training_report.md
    low_data_classes = ["gerbera", "lilium", "carnation", "anthurium", "melon", "geranium", "blueberry", "zucchini", "broccoli", "chrysanthemum"]

    md = []
    md.append("# MODEL 1 (EFFICIENTNET-B2) TRAINING & TEST EVALUATION REPORT\n")
    md.append(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}  ")
    md.append(f"**Target Architecture:** EfficientNet-B2 (PyTorch Transfer Learning)  ")
    md.append(f"**Dataset Location:** `data/processed/model1_balanced/`  ")
    md.append(f"**Best Checkpoint:** `models/model1/best_model.pth` (Saved at Epoch {best_epoch})  \n")
    md.append("---")
    md.append("## 1. Executive Summary")
    md.append(f"- **Top-1 Test Accuracy:** **{top1_acc*100:.2f}%** ({top1_correct:,} / {len(test_targets):,} images)")
    md.append(f"- **Top-3 Test Accuracy:** **{top3_acc*100:.2f}%** ({top3_correct:,} / {len(test_targets):,} images)")
    md.append(f"- **Test Macro F1:** **{macro_f1*100:.2f}%**")
    md.append(f"- **Test Weighted F1:** **{weighted_f1*100:.2f}%**")
    md.append(f"- **Best Validation Macro F1:** **{best_val_f1*100:.2f}%** (Achieved at Epoch {best_epoch})")
    md.append(f"- **Epochs Trained:** {len(history['train_loss'])} / {EPOCHS} (Patience: {PATIENCE})\n")

    md.append("## 2. Complete Per-Class Test Performance (22 Target Taxonomy)")
    md.append("| # | Class Name | Support (Test) | Precision | Recall | F1-Score | Status |")
    md.append("|:---:|:---|:---:|:---:|:---:|:---:|:---|")

    for idx, c_name in enumerate(SORTED_CLASSES, 1):
        m = clf_dict.get(c_name, {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 0})
        sup = m["support"]
        p = m["precision"] * 100
        r = m["recall"] * 100
        f1 = m["f1-score"] * 100
        if sup == 0:
            status = "NO TEST DATA (DOCUMENTED GAP)"
        elif f1 >= 95.0:
            status = "EXCELLENT"
        elif f1 >= 85.0:
            status = "GOOD"
        else:
            status = "NEEDS ATTENTION"
        md.append(f"| {idx} | `{c_name}` | {sup} | {p:.2f}% | {r:.2f}% | **{f1:.2f}%** | {status} |")

    md.append(f"\n| - | **Macro Average** | **{len(test_targets)}** | **{macro_prec*100:.2f}%** | **{macro_rec*100:.2f}%** | **{macro_f1*100:.2f}%** | - |")
    md.append(f"| - | **Weighted Average** | **{len(test_targets)}** | **{precision_score(test_targets, test_preds, average='weighted', zero_division=0)*100:.2f}%** | **{recall_score(test_targets, test_preds, average='weighted', zero_division=0)*100:.2f}%** | **{weighted_f1*100:.2f}%** | - |\n")

    md.append("## 3. Dedicated Performance Summary for Low-Data Classes")
    md.append("Classes with restricted sample sizes were managed via smooth class-weighting and balanced sampling without synthetic duplicates:")
    md.append("| Class Name | Train Samples | Test Support | Precision | Recall | F1-Score | Remarks |")
    md.append("|:---|:---:|:---:|:---:|:---:|:---:|:---|")

    for c_name in low_data_classes:
        tr_cnt = class_counts.get(CLASS_TO_IDX[c_name], 0)
        m = clf_dict.get(c_name, {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 0})
        md.append(f"| `{c_name}` | {tr_cnt} | {m['support']} | {m['precision']*100:.2f}% | {m['recall']*100:.2f}% | **{m['f1-score']*100:.2f}%** | Underrepresented class preserved without synthetic copies |")

    md.append("\n## 4. Training History by Epoch")
    md.append("| Epoch | Train Loss | Train Acc | Val Loss | Val Acc | Val Macro F1 | Learning Rate | Epoch Time |")
    md.append("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
    for ep in range(len(history["train_loss"])):
        md.append(f"| {ep+1:02d} | {history['train_loss'][ep]:.4f} | {history['train_acc'][ep]*100:.2f}% | "
                  f"{history['val_loss'][ep]:.4f} | {history['val_acc'][ep]*100:.2f}% | "
                  f"{history['val_macro_f1'][ep]*100:.2f}% | {history['lr'][ep]:.2e} | {history['epoch_time'][ep]:.1f}s |")

    md.append("\n## 5. Artifact Directory & Verification")
    md.append("- **Best Checkpoint:** [`models/model1/best_model.pth`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/best_model.pth)")
    md.append("- **Class Mapping JSON:** [`models/model1/class_mapping.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/class_mapping.json)")
    md.append("- **Preprocessing Config:** [`models/model1/config.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/config.json)")
    md.append("- **Classification CSV:** [`reports/model1/classification_report.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/classification_report.csv)")
    md.append("- **Test Predictions:** [`reports/model1/test_predictions.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/test_predictions.csv)")
    md.append("- **Confusion Matrix Plot:** [`reports/model1/confusion_matrix.png`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/confusion_matrix.png)")
    md.append("- **Training Curves Plot:** [`reports/model1/training_curves.png`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/training_curves.png)")

    with open(REPORT_MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print(f"\nSaved complete markdown training report: {REPORT_MD_PATH}")
    print("=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    train_and_evaluate()
