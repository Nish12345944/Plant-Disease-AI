"""Full Model 1 Training & Test Evaluation Pipeline.

Architecture: EfficientNet-B2
Target: 19 Populated Plant/Crop Classes (22 Target Taxonomy)
Hardware: NVIDIA GeForce RTX 3050 (4GB VRAM) via CUDA & AMP FP16
"""

import csv
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models import EfficientNet_B2_Weights, efficientnet_b2

# Configuration
ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DATASET_DIR = ROOT / "data" / "processed" / "model1_dataset"
MODELS_DIR = ROOT / "models" / "model1"
RESULTS_DIR = ROOT / "results" / "model1"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

BEST_MODEL_PATH = MODELS_DIR / "best_model.pth"
LAST_MODEL_PATH = MODELS_DIR / "last_model.pth"
CLASS_NAMES_PATH = MODELS_DIR / "class_names.json"
CONFIG_PATH = MODELS_DIR / "config.json"
HISTORY_CSV_PATH = RESULTS_DIR / "training_history.csv"
TEST_METRICS_PATH = RESULTS_DIR / "test_evaluation_report.json"
CONFUSION_MATRIX_PATH = RESULTS_DIR / "confusion_matrix.json"

IMAGE_SIZE = 224
BATCH_SIZE = 16
NUM_WORKERS = 2
EPOCHS = 12
LEARNING_RATE = 3e-4
WEIGHT_DECAY = 1e-4
PATIENCE = 4
SEED = 42

def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

class RobustImageFolder(datasets.ImageFolder):
    """ImageFolder that reuses existing class mappings even if a class is unpopulated in split."""
    def __init__(self, root, fixed_classes, fixed_class_to_idx, transform=None):
        self.fixed_classes = fixed_classes
        self.fixed_class_to_idx = fixed_class_to_idx
        super().__init__(root, transform=transform, allow_empty=True)

    def find_classes(self, directory):
        return self.fixed_classes, self.fixed_class_to_idx

def build_loaders():
    imagenet_mean = [0.485, 0.456, 0.406]
    imagenet_std = [0.229, 0.224, 0.225]

    train_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15, hue=0.03),
        transforms.ToTensor(),
        transforms.Normalize(mean=imagenet_mean, std=imagenet_std),
    ])

    eval_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=imagenet_mean, std=imagenet_std),
    ])

    train_dir = DATASET_DIR / "train"
    val_dir = DATASET_DIR / "val"
    test_dir = DATASET_DIR / "test"

    base_train = datasets.ImageFolder(train_dir)
    classes = base_train.classes
    class_to_idx = base_train.class_to_idx

    train_dataset = datasets.ImageFolder(train_dir, transform=train_transform)
    val_dataset = RobustImageFolder(val_dir, classes, class_to_idx, transform=eval_transform)
    test_dataset = RobustImageFolder(test_dir, classes, class_to_idx, transform=eval_transform)

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=True,
        persistent_workers=True,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True,
        persistent_workers=True,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True,
        persistent_workers=True,
    )

    return train_loader, val_loader, test_loader, classes, class_to_idx

def evaluate_model(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    all_preds = []
    all_targets = []
    all_probs = []

    with torch.no_grad():
        for images, targets in loader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            with torch.autocast("cuda", dtype=torch.float16):
                outputs = model(images)
                loss = criterion(outputs, targets)

            total_loss += loss.item() * targets.size(0)
            probs = torch.softmax(outputs, dim=1)
            preds = outputs.argmax(dim=1)

            all_probs.append(probs.cpu().numpy())
            all_preds.append(preds.cpu().numpy())
            all_targets.append(targets.cpu().numpy())

    all_preds = np.concatenate(all_preds)
    all_targets = np.concatenate(all_targets)
    all_probs = np.concatenate(all_probs)

    avg_loss = total_loss / len(all_targets)
    acc = (all_preds == all_targets).mean()
    macro_f1 = f1_score(all_targets, all_preds, average="macro", zero_division=0)

    return avg_loss, acc, macro_f1, all_targets, all_preds, all_probs

def train_and_eval():
    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 80)
    print("MODEL 1 FULL TRAINING PIPELINE")
    print(f"Device        : {device} ({torch.cuda.get_device_name(0)})")
    print(f"Architecture  : EfficientNet-B2 (ImageNet Pretrained)")
    print(f"Dataset Root  : {DATASET_DIR}")
    print(f"Batch Size    : {BATCH_SIZE} | Workers: {NUM_WORKERS} | Image Size: {IMAGE_SIZE}x{IMAGE_SIZE}")
    print(f"AMP FP16      : ENABLED | Optimizer: AdamW | Scheduler: CosineAnnealingLR")
    print("=" * 80)
    sys.stdout.flush()

    train_loader, val_loader, test_loader, classes, class_to_idx = build_loaders()
    num_classes = len(classes)
    print(f"\nPopulated Classes ({num_classes}): {classes}")
    print(f"Train samples: {len(train_loader.dataset):,} | Val samples: {len(val_loader.dataset):,} | Test samples: {len(test_loader.dataset):,}")

    # Save class names mapping
    with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as f:
        json.dump({"classes": classes, "class_to_idx": class_to_idx}, f, indent=2)

    # Save training config
    config = {
        "architecture": "efficientnet_b2",
        "num_classes": num_classes,
        "classes": classes,
        "image_size": IMAGE_SIZE,
        "batch_size": BATCH_SIZE,
        "num_workers": NUM_WORKERS,
        "epochs": EPOCHS,
        "initial_lr": LEARNING_RATE,
        "weight_decay": WEIGHT_DECAY,
        "patience": PATIENCE,
        "amp": True,
        "device": str(device),
        "device_name": torch.cuda.get_device_name(0),
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    # Model definition
    weights = EfficientNet_B2_Weights.DEFAULT
    model = efficientnet_b2(weights=weights)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=1e-6)
    scaler = torch.amp.GradScaler("cuda")

    # CSV History initialization
    with open(HISTORY_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "epoch", "train_loss", "train_accuracy",
            "val_loss", "val_accuracy", "val_macro_f1",
            "lr", "epoch_time_sec", "peak_vram_mb"
        ])

    best_val_macro_f1 = 0.0
    patience_counter = 0

    print("\n" + "-" * 110)
    print(f"{'Epoch':^7} | {'Train Loss':^10} | {'Train Acc':^10} | {'Val Loss':^10} | {'Val Acc':^10} | {'Val F1':^10} | {'LR':^9} | {'Time':^7} | {'Peak VRAM':^10}")
    print("-" * 110)
    sys.stdout.flush()

    for epoch in range(1, EPOCHS + 1):
        epoch_start = time.time()
        torch.cuda.reset_peak_memory_stats(device=device)

        # Training phase
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0

        current_lr = optimizer.param_groups[0]["lr"]

        for images, targets in train_loader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)

            with torch.autocast("cuda", dtype=torch.float16):
                outputs = model(images)
                loss = criterion(outputs, targets)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            bs = targets.size(0)
            train_loss += loss.item() * bs
            train_correct += (outputs.argmax(dim=1) == targets).sum().item()
            train_total += bs

        scheduler.step()

        epoch_train_loss = train_loss / train_total
        epoch_train_acc = train_correct / train_total

        # Validation phase
        val_loss, val_acc, val_f1, _, _, _ = evaluate_model(model, val_loader, criterion, device)

        epoch_time = time.time() - epoch_start
        peak_vram = torch.cuda.max_memory_allocated(device) / (1024 ** 2)

        # Log to CSV
        with open(HISTORY_CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                epoch,
                round(epoch_train_loss, 4),
                round(epoch_train_acc, 4),
                round(val_loss, 4),
                round(val_acc, 4),
                round(val_f1, 4),
                f"{current_lr:.6f}",
                round(epoch_time, 1),
                round(peak_vram, 1),
            ])

        # Save last checkpoint
        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "val_macro_f1": val_f1,
            "classes": classes,
        }, LAST_MODEL_PATH)

        # Save best checkpoint
        is_best = val_f1 > best_val_macro_f1
        marker = ""
        if is_best:
            best_val_macro_f1 = val_f1
            patience_counter = 0
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "val_loss": val_loss,
                "val_accuracy": val_acc,
                "val_macro_f1": val_f1,
                "classes": classes,
            }, BEST_MODEL_PATH)
            marker = " *"
        else:
            patience_counter += 1

        print(f"{epoch:^7d} | {epoch_train_loss:^10.4f} | {epoch_train_acc:^10.4f} | {val_loss:^10.4f} | {val_acc:^10.4f} | {val_f1:^10.4f}{marker} | {current_lr:^9.2e} | {epoch_time:^6.1f}s | {peak_vram:^8.1f}MB")
        sys.stdout.flush()

        if patience_counter >= PATIENCE:
            print(f"\n[Early Stopping] No improvement in validation macro F1 for {PATIENCE} consecutive epochs. Stopping training.")
            break

    print("-" * 110)
    print(f"Training completed. Best Val Macro F1: {best_val_macro_f1:.4f} (Saved to {BEST_MODEL_PATH})")
    sys.stdout.flush()

    # ============================================================
    # TEST SET EVALUATION ON BEST CHECKPOINT
    # ============================================================
    print("\n" + "=" * 80)
    print("EVALUATING BEST MODEL ON UNSEEN TEST SET")
    print("=" * 80)
    sys.stdout.flush()

    checkpoint = torch.load(BEST_MODEL_PATH, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    test_loss, test_acc, test_macro_f1, test_targets, test_preds, test_probs = evaluate_model(
        model, test_loader, criterion, device
    )

    macro_prec = precision_score(test_targets, test_preds, average="macro", zero_division=0)
    macro_rec = recall_score(test_targets, test_preds, average="macro", zero_division=0)
    weighted_f1 = f1_score(test_targets, test_preds, average="weighted", zero_division=0)

    # Top-3 Accuracy
    top3_correct = 0
    for i, target in enumerate(test_targets):
        top3_indices = np.argsort(test_probs[i])[-3:]
        if target in top3_indices:
            top3_correct += 1
    top3_acc = top3_correct / len(test_targets)

    # Classification report
    unique_labels_present = sorted(list(set(test_targets) | set(test_preds)))
    target_names = [classes[idx] for idx in unique_labels_present]
    report_dict = classification_report(
        test_targets,
        test_preds,
        labels=unique_labels_present,
        target_names=target_names,
        output_dict=True,
        zero_division=0,
    )
    report_text = classification_report(
        test_targets,
        test_preds,
        labels=unique_labels_present,
        target_names=target_names,
        digits=4,
        zero_division=0,
    )

    # Confusion matrix
    cm = confusion_matrix(test_targets, test_preds, labels=list(range(num_classes)))
    cm_list = cm.tolist()

    # Save outputs
    test_results = {
        "test_loss": float(round(test_loss, 4)),
        "test_accuracy": float(round(test_acc, 4)),
        "macro_precision": float(round(macro_prec, 4)),
        "macro_recall": float(round(macro_rec, 4)),
        "macro_f1": float(round(test_macro_f1, 4)),
        "weighted_f1": float(round(weighted_f1, 4)),
        "top3_accuracy": float(round(top3_acc, 4)),
        "per_class_report": report_dict,
        "best_epoch": int(checkpoint.get("epoch", 0)),
    }

    with open(TEST_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2)

    with open(CONFUSION_MATRIX_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "classes": classes,
            "confusion_matrix": cm_list,
        }, f, indent=2)

    print(f"\n[Test Set Summary Metrics]")
    print(f"  Test Accuracy   : {test_acc * 100:.2f}%")
    print(f"  Macro Precision : {macro_prec:.4f}")
    print(f"  Macro Recall    : {macro_rec:.4f}")
    print(f"  Macro F1        : {test_macro_f1:.4f}")
    print(f"  Weighted F1     : {weighted_f1:.4f}")
    print(f"  Top-3 Accuracy  : {top3_acc * 100:.2f}%")

    print(f"\n[Per-Class Classification Report]")
    print(report_text)

    print("=" * 80)
    print("ALL ARTIFACTS AND EVALUATION SAVED SUCCESSFULLY!")
    print(f"Best Model Checkpoint : {BEST_MODEL_PATH}")
    print(f"Last Model Checkpoint : {LAST_MODEL_PATH}")
    print(f"Class Names Mapping   : {CLASS_NAMES_PATH}")
    print(f"Training Config       : {CONFIG_PATH}")
    print(f"Training History CSV  : {HISTORY_CSV_PATH}")
    print(f"Test Evaluation JSON  : {TEST_METRICS_PATH}")
    print(f"Confusion Matrix JSON : {CONFUSION_MATRIX_PATH}")
    print("=" * 80)
    sys.stdout.flush()

if __name__ == "__main__":
    train_and_eval()
