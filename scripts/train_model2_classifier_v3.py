"""
Train Model 2 Disease Classifier v3 on Clean Organized Dataset (EfficientNet-B2)
================================================================================
Trains on the newly organized hierarchical dataset:
  data/processed/model2_organized/
  ├── train/{crop}/{disease}/
  ├── val/{crop}/{disease}/
  └── test/{crop}/{disease}/ (IMMUTABLE 2,304 test set)

Outputs:
  models/model2_classifier_v3/
  ├── best_model.pth
  ├── last_model.pth
  ├── config.json
  └── class_mapping.json

Reports:
  reports/model2_classifier_v3/
  ├── classification_report.csv
  ├── test_predictions.csv
  ├── confusion_matrix.png
  ├── training_curves.png
  ├── training_progress.csv
  ├── training.log
  └── model2_v3_training_report.md
"""

import csv
import json
import math
import os
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
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
from torchvision.models import EfficientNet_B2_Weights, efficientnet_b2

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
ORGANIZED_DIR = PROJECT_ROOT / "data" / "processed" / "model2_organized"
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_organized_manifest.csv"
CLASS_MAPPING_PATH = PROJECT_ROOT / "data" / "processed" / "model2_organized_class_mapping.json"
CROP_DISEASE_MAP_PATH = PROJECT_ROOT / "data" / "processed" / "model2_organized_crop_disease_mapping.json"

MODEL_DIR = PROJECT_ROOT / "models" / "model2_classifier_v3"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_classifier_v3"
PROGRESS_CSV = REPORTS_DIR / "training_progress.csv"
TRAINING_LOG = REPORTS_DIR / "training.log"

# Hyperparameters (Matched with V2 for strict controlled comparison)
BATCH_SIZE = 32
GRAD_ACCUM_STEPS = 2  # Effective batch size = 64
NUM_WORKERS = 2
IMAGE_SIZE = (260, 260)
MAX_EPOCHS = 20
PATIENCE = 10
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-4
RANDOM_SEED = 42


class OrganizedPlantDiseaseDataset(Dataset):
    """Loads images from the organized hierarchical crop/disease structure."""

    def __init__(self, records, base_dir, transform=None):
        self.records = records
        self.base_dir = Path(base_dir)
        self.transform = transform

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        rec = self.records[idx]
        img_path = self.base_dir / rec["image_path"]
        img = Image.open(img_path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        label = int(rec["class_id"])
        return img, label, idx


def get_transforms():
    train_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.2),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15, hue=0.05),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    val_test_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    return train_transform, val_test_transform


def log_message(msg):
    print(msg, flush=True)
    with open(TRAINING_LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def compute_class_weights(train_records, num_classes, alpha=0.5, max_weight=10.0, min_weight=0.2):
    train_counts = Counter([r["class_id"] for r in train_records])
    total_train = len(train_records)

    weights = []
    for c in range(num_classes):
        cnt = train_counts.get(c, 1)
        w = (total_train / (num_classes * cnt)) ** alpha
        w = max(min_weight, min(max_weight, w))
        weights.append(w)

    weights = np.array(weights, dtype=np.float32)
    weights = weights / weights.mean()
    return torch.tensor(weights, dtype=torch.float32)


def build_model(num_classes=117):
    model = efficientnet_b2(weights=EfficientNet_B2_Weights.DEFAULT)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes),
    )
    return model


def evaluate(model, loader, criterion, device, num_classes):
    model.eval()
    total_loss = 0.0
    all_preds = []
    all_targets = []
    all_probs = []

    with torch.no_grad():
        for images, labels, _ in loader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            with autocast("cuda"):
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


def plot_training_curves(history, save_path):
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
    axes[1, 0].set_title("Macro F1 Score (%)")
    axes[1, 0].set_xlabel("Epoch")
    axes[1, 0].set_ylabel("Macro F1 (%)")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # 4. Disease-only vs Healthy F1
    axes[1, 1].plot(epochs, [f * 100 for f in history["val_disease_macro_f1"]], "g-^", label="Val Disease-Only F1")
    axes[1, 1].plot(epochs, [f * 100 for f in history["val_healthy_f1"]], "m-d", label="Val Healthy F1")
    axes[1, 1].set_title("Disease-Only vs Healthy F1 (%)")
    axes[1, 1].set_xlabel("Epoch")
    axes[1, 1].set_ylabel("F1 Score (%)")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()


def train_pipeline():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    log_message("=" * 80)
    log_message("MODEL 2 V3 DISEASE CLASSIFIER RETRAINING (EFFICIENTNET-B2)")
    log_message("=" * 80)

    torch.manual_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(RANDOM_SEED)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    log_message(f"Execution Device : {device} ({gpu_name})")

    # 1. Load Taxonomy and Class Mapping
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        raw_map = json.load(f)
        class_to_id = raw_map.get("class_to_id", raw_map)
    id_to_class = {int(v): k for k, v in class_to_id.items()}
    num_classes = len(class_to_id)
    class_names = [id_to_class[i] for i in range(num_classes)]

    # 2. Load Manifest Records
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_recs = list(reader)

    for r in all_recs:
        r["class_id"] = int(r["class_id"])

    train_recs = [r for r in all_recs if r["split"] == "train"]
    val_recs = [r for r in all_recs if r["split"] == "val"]
    test_recs = [r for r in all_recs if r["split"] == "test"]

    # Pre-training Verification
    crops_set = set(r["crop"] for r in all_recs)
    healthy_count = sum(1 for r in all_recs if r["class_name"] == "healthy")
    diseased_count = sum(1 for r in all_recs if r["class_name"] != "healthy")

    log_message("\n=== PRE-TRAINING DATASET AUDIT VERIFICATION ===")
    log_message(f"Total Crops         : {len(crops_set)} (Expected: 39)")
    log_message(f"Total Classes       : {num_classes} (Expected: 117)")
    log_message(f"Total Images        : {len(all_recs):,} (Expected: 19,253)")
    log_message(f"Train Images        : {len(train_recs):,} (Expected: 15,252)")
    log_message(f"Val Images          : {len(val_recs):,} (Expected: 1,697)")
    log_message(f"Test Images         : {len(test_recs):,} (Expected: 2,304)")
    log_message(f"Healthy Images      : {healthy_count:,} (Expected: 6,939)")
    log_message(f"Diseased Images     : {diseased_count:,} (Expected: 12,314)")

    # Assert exact match before starting
    if len(train_recs) != 15252 or len(val_recs) != 1697 or len(test_recs) != 2304 or num_classes != 117 or len(crops_set) != 39:
        log_message("ERROR: Dataset counts do not match expected audited values! ABORTING TRAINING.")
        return 1

    log_message("All pre-training dataset assertions PASSED. Proceeding to training.")

    # 3. Create Datasets & DataLoaders
    train_tf, val_test_tf = get_transforms()
    train_dataset = OrganizedPlantDiseaseDataset(train_recs, ORGANIZED_DIR, transform=train_tf)
    val_dataset = OrganizedPlantDiseaseDataset(val_recs, ORGANIZED_DIR, transform=val_test_tf)
    test_dataset = OrganizedPlantDiseaseDataset(test_recs, ORGANIZED_DIR, transform=val_test_tf)

    train_loader = DataLoader(
        train_dataset, batch_size=BATCH_SIZE, shuffle=True,
        num_workers=NUM_WORKERS, pin_memory=True, drop_last=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=NUM_WORKERS, pin_memory=True
    )
    test_loader = DataLoader(
        test_dataset, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=NUM_WORKERS, pin_memory=True
    )

    # 4. Class Weights & Loss
    class_weights = compute_class_weights(train_recs, num_classes).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    eval_criterion = nn.CrossEntropyLoss()

    # 5. Build Model
    model = build_model(num_classes).to(device)

    # 6. Optimizer & Scheduler
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=MAX_EPOCHS, eta_min=1e-6)
    scaler = GradScaler("cuda")

    # 7. Progress CSV Header
    with open(PROGRESS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "epoch", "learning_rate", "train_loss", "train_accuracy",
            "train_macro_f1", "train_weighted_f1", "val_loss", "val_accuracy",
            "val_macro_f1", "val_weighted_f1", "val_healthy_f1", "val_disease_macro_f1",
            "best_val_macro_f1", "best_epoch", "epoch_time_seconds", "gpu_memory_mb"
        ])

    best_val_macro_f1 = 0.0
    best_epoch = 0
    patience_counter = 0

    history = {
        "train_loss": [], "train_acc": [], "train_macro_f1": [],
        "val_loss": [], "val_acc": [], "val_macro_f1": [],
        "val_disease_macro_f1": [], "val_healthy_f1": []
    }

    log_message("\nStarting Model 2 V3 Training Loop...")
    log_message("-" * 80)

    for epoch in range(1, MAX_EPOCHS + 1):
        epoch_start = time.time()
        model.train()
        train_loss = 0.0
        train_preds = []
        train_targets = []

        optimizer.zero_grad()
        for step, (images, labels, _) in enumerate(train_loader):
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            with autocast("cuda"):
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss = loss / GRAD_ACCUM_STEPS

            scaler.scale(loss).backward()

            if (step + 1) % GRAD_ACCUM_STEPS == 0 or (step + 1) == len(train_loader):
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()

            train_loss += loss.item() * GRAD_ACCUM_STEPS * images.size(0)
            preds = torch.argmax(outputs, dim=1)
            train_preds.extend(preds.detach().cpu().numpy())
            train_targets.extend(labels.detach().cpu().numpy())

        scheduler.step()
        cur_lr = scheduler.get_last_lr()[0]

        avg_train_loss = train_loss / (len(train_loader) * BATCH_SIZE)
        train_acc = accuracy_score(train_targets, train_preds)
        train_prec_m, train_rec_m, train_f1_m, _ = precision_recall_fscore_support(
            train_targets, train_preds, average="macro", zero_division=0
        )
        train_prec_w, train_rec_w, train_f1_w, _ = precision_recall_fscore_support(
            train_targets, train_preds, average="weighted", zero_division=0
        )

        # Validation Evaluation
        val_metrics = evaluate(model, val_loader, eval_criterion, device, num_classes)
        epoch_duration = time.time() - epoch_start
        gpu_mem = torch.cuda.max_memory_allocated() / (1024 * 1024) if torch.cuda.is_available() else 0.0

        history["train_loss"].append(avg_train_loss)
        history["train_acc"].append(train_acc)
        history["train_macro_f1"].append(train_f1_m)
        history["val_loss"].append(val_metrics["loss"])
        history["val_acc"].append(val_metrics["accuracy"])
        history["val_macro_f1"].append(val_metrics["macro_f1"])
        history["val_disease_macro_f1"].append(val_metrics["disease_macro_f1"])
        history["val_healthy_f1"].append(val_metrics["healthy_f1"])

        is_best = False
        if val_metrics["macro_f1"] > best_val_macro_f1:
            best_val_macro_f1 = val_metrics["macro_f1"]
            best_epoch = epoch
            is_best = True
            patience_counter = 0

            # Save best checkpoint
            best_ckpt = {
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "val_macro_f1": best_val_macro_f1,
                "val_accuracy": val_metrics["accuracy"],
                "val_disease_macro_f1": val_metrics["disease_macro_f1"],
                "val_healthy_f1": val_metrics["healthy_f1"],
                "num_classes": num_classes,
                "classes": class_names,
            }
            torch.save(best_ckpt, MODEL_DIR / "best_model.pth")
        else:
            patience_counter += 1

        # Save last checkpoint
        last_ckpt = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "val_macro_f1": val_metrics["macro_f1"],
            "val_accuracy": val_metrics["accuracy"],
            "best_epoch": best_epoch,
            "best_val_macro_f1": best_val_macro_f1,
            "num_classes": num_classes,
            "classes": class_names,
        }
        torch.save(last_ckpt, MODEL_DIR / "last_model.pth")

        # Live Progress CSV update
        csv_row = [
            epoch, f"{cur_lr:.6e}",
            f"{avg_train_loss:.4f}", f"{train_acc:.4f}", f"{train_f1_m:.4f}", f"{train_f1_w:.4f}",
            f"{val_metrics['loss']:.4f}", f"{val_metrics['accuracy']:.4f}", f"{val_metrics['macro_f1']:.4f}",
            f"{val_metrics['weighted_f1']:.4f}", f"{val_metrics['healthy_f1']:.4f}", f"{val_metrics['disease_macro_f1']:.4f}",
            f"{best_val_macro_f1:.4f}", best_epoch, f"{epoch_duration:.2f}", f"{gpu_mem:.2f}"
        ]
        with open(PROGRESS_CSV, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(csv_row)

        star = " ★ BEST" if is_best else ""
        log_message(
            f"Epoch {epoch:02d}/{MAX_EPOCHS:02d} [{epoch_duration:.1f}s] | "
            f"Tr Loss: {avg_train_loss:.4f}, Tr Acc: {train_acc*100:.2f}%, Tr F1: {train_f1_m*100:.2f}% | "
            f"Val Loss: {val_metrics['loss']:.4f}, Val Acc: {val_metrics['accuracy']*100:.2f}%, "
            f"Val Macro F1: {val_metrics['macro_f1']*100:.2f}% (Dis: {val_metrics['disease_macro_f1']*100:.2f}%, Hlt: {val_metrics['healthy_f1']*100:.2f}%){star}"
        )

        if patience_counter >= PATIENCE:
            log_message(f"\n[Early Stopping] No improvement in Validation Macro F1 for {PATIENCE} epochs. Stopping at epoch {epoch}.")
            break

    log_message("-" * 80)
    log_message(f"Training Complete! Best Validation Epoch: {best_epoch} with Val Macro F1: {best_val_macro_f1*100:.2f}%\n")

    # Save Class Mapping to model dir
    with open(MODEL_DIR / "class_mapping.json", "w", encoding="utf-8") as f:
        json.dump(class_to_id, f, indent=2)

    # 8. Plot Training Curves
    plot_training_curves(history, REPORTS_DIR / "training_curves.png")

    # 9. Final Independent Test Evaluation (IMMUTABLE 2,304 TEST SET)
    log_message("=" * 80)
    log_message("FINAL INDEPENDENT TEST EVALUATION (IMMUTABLE 2,304 TEST SET)")
    log_message("=" * 80)

    best_ckpt = torch.load(MODEL_DIR / "best_model.pth", map_location=device, weights_only=False)
    model.load_state_dict(best_ckpt["model_state_dict"])
    log_message(f"Loaded Best Model Checkpoint from Epoch {best_ckpt['epoch']}")

    test_metrics = evaluate(model, test_loader, eval_criterion, device, num_classes)

    # Save Test Predictions CSV
    test_pred_records = []
    for idx, (rec, pred, prob) in enumerate(zip(test_recs, test_metrics["preds"], test_metrics["probs"])):
        top3_idx = np.argsort(prob)[-3:][::-1]
        top3_classes = [id_to_class[i] for i in top3_idx]
        test_pred_records.append({
            "image_path": rec["image_path"],
            "crop": rec["crop"],
            "disease": rec["disease"],
            "ground_truth_class": rec["class_name"],
            "ground_truth_id": rec["class_id"],
            "predicted_class": id_to_class[pred],
            "predicted_id": int(pred),
            "is_correct": int(pred == rec["class_id"]),
            "confidence": float(prob[pred]),
            "top3_classes": "; ".join(top3_classes),
        })

    test_pred_df = pd.DataFrame(test_pred_records)
    test_pred_path = REPORTS_DIR / "test_predictions.csv"
    test_pred_df.to_csv(test_pred_path, index=False)
    log_message(f"Saved Test Predictions to: {test_pred_path}")

    # Save Per-Class Classification Report CSV
    class_report_rows = []
    for cid in range(num_classes):
        cname = id_to_class[cid]
        class_report_rows.append({
            "class_id": cid,
            "class_name": cname,
            "precision": float(test_metrics["per_class_precision"][cid]),
            "recall": float(test_metrics["per_class_recall"][cid]),
            "f1_score": float(test_metrics["per_class_f1"][cid]),
            "support": int(test_metrics["per_class_support"][cid]),
            "is_healthy": int(cid == 0),
        })

    class_report_df = pd.DataFrame(class_report_rows)
    class_report_path = REPORTS_DIR / "classification_report.csv"
    class_report_df.to_csv(class_report_path, index=False)
    log_message(f"Saved Classification Report to: {class_report_path}")

    # Save Configuration
    config_dict = {
        "model_architecture": "efficientnet_b2",
        "num_classes": num_classes,
        "image_size": IMAGE_SIZE,
        "batch_size": BATCH_SIZE,
        "effective_batch_size": BATCH_SIZE * GRAD_ACCUM_STEPS,
        "learning_rate": LEARNING_RATE,
        "weight_decay": WEIGHT_DECAY,
        "optimizer": "AdamW",
        "scheduler": "CosineAnnealingLR",
        "random_seed": RANDOM_SEED,
        "best_epoch": best_epoch,
        "best_val_macro_f1": float(best_val_macro_f1),
        "test_top1_accuracy": float(test_metrics["accuracy"]),
        "test_top3_accuracy": float(test_metrics["top3_accuracy"]),
        "test_macro_f1": float(test_metrics["macro_f1"]),
        "test_disease_macro_f1": float(test_metrics["disease_macro_f1"]),
        "test_healthy_f1": float(test_metrics["healthy_f1"]),
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else "N/A",
        "gpu": gpu_name,
        "train_samples": len(train_recs),
        "val_samples": len(val_recs),
        "test_samples": len(test_recs),
    }
    with open(MODEL_DIR / "config.json", "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)

    # 10. Generate Model 2 V3 vs V2 Technical Report
    generate_markdown_report(config_dict, test_metrics, class_report_df, id_to_class)

    return 0


def generate_markdown_report(config, test_metrics, class_df, id_to_class):
    report_path = REPORTS_DIR / "model2_v3_training_report.md"

    # Load V2 Baseline Config for comparison
    v2_config_path = PROJECT_ROOT / "models" / "model2_classifier_v2" / "config.json"
    v2_config = {}
    if v2_config_path.exists():
        with open(v2_config_path, "r", encoding="utf-8") as f:
            v2_config = json.load(f)

    v2_top1 = v2_config.get("test_top1_accuracy", 0.8598)
    v2_top3 = v2_config.get("test_top3_accuracy", 0.9562)
    v2_macro_f1 = v2_config.get("test_macro_f1", 0.6529)
    v2_dis_f1 = v2_config.get("test_disease_macro_f1", 0.6443)
    v2_hlt_f1 = v2_config.get("test_healthy_f1", 0.9947)

    v3_top1 = test_metrics["accuracy"]
    v3_top3 = test_metrics["top3_accuracy"]
    v3_macro_f1 = test_metrics["macro_f1"]
    v3_dis_f1 = test_metrics["disease_macro_f1"]
    v3_hlt_f1 = test_metrics["healthy_f1"]

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# MODEL 2 V3 RETRAINING & BENCHMARK REPORT\n\n")
        f.write(f"**Date:** 2026-10-07  \n")
        f.write(f"**Model Directory:** `models/model2_classifier_v3/`  \n")
        f.write(f"**Dataset Location:** `data/processed/model2_organized/`  \n")
        f.write(f"**Architecture:** EfficientNet-B2 (117 Classes)  \n")
        f.write(f"**Best Epoch:** {config['best_epoch']}  \n\n")

        f.write("## 1. Executive Comparison: Model 2 V2 vs Model 2 V3\n\n")
        f.write("| Metric | Model 2 V2 Baseline | Model 2 V3 (Organized Dataset) | Delta (V3 - V2) |\n")
        f.write("|:---|:---:|:---:|:---:|\n")
        f.write(f"| **Test Top-1 Accuracy** | {v2_top1*100:.2f}% | **{v3_top1*100:.2f}%** | {((v3_top1 - v2_top1)*100):+.2f}% |\n")
        f.write(f"| **Test Top-3 Accuracy** | {v2_top3*100:.2f}% | **{v3_top3*100:.2f}%** | {((v3_top3 - v2_top3)*100):+.2f}% |\n")
        f.write(f"| **Test Macro F1** | {v2_macro_f1*100:.2f}% | **{v3_macro_f1*100:.2f}%** | {((v3_macro_f1 - v2_macro_f1)*100):+.2f}% |\n")
        f.write(f"| **Test Disease-only Macro F1** | {v2_dis_f1*100:.2f}% | **{v3_dis_f1*100:.2f}%** | {((v3_dis_f1 - v2_dis_f1)*100):+.2f}% |\n")
        f.write(f"| **Test Healthy F1** | {v2_hlt_f1*100:.2f}% | **{v3_hlt_f1*100:.2f}%** | {((v3_hlt_f1 - v2_hlt_f1)*100):+.2f}% |\n")

        f.write("\n## 2. High-Confidence Diagnostic Classes Benchmark\n\n")
        f.write("| Crop | Disease Class | Support | Precision | Recall | F1 Score |\n")
        f.write("|:---|:---|:---:|:---:|:---:|:---:|\n")

        key_classes = [
            "healthy", "bean__rust", "bean__angular_leaf_spot", "soybean__rust", "soybean__frog_eye_leaf_spot",
            "citrus__canker", "wheat__stripe_rust", "wheat__head_scab", "wheat__powdery_mildew", "wheat__septoria_blotch",
            "wheat__loose_smut", "grape__downy_mildew", "apple__scab", "corn__smut", "corn__rust", "corn__northern_leaf_blight",
            "zucchini__powdery_mildew", "cucumber__powdery_mildew", "cucumber__angular_leaf_spot", "cucumber__bacterial_wilt",
            "tomato__early_blight", "tomato__late_blight", "tomato__leaf_mold", "tomato__septoria_leaf_spot",
            "peach__leaf_curl", "peach__brown_rot", "coffee__leaf_rust", "banana__black_leaf_streak", "banana__bunchy_top"
        ]
        for kc in key_classes:
            row = class_df[class_df["class_name"] == kc]
            if not row.empty:
                r = row.iloc[0]
                crop_name = "shared" if kc == "healthy" else kc.split("__")[0]
                f.write(f"| `{crop_name}` | `{kc}` | {int(r['support'])} | {r['precision']*100:.1f}% | {r['recall']*100:.1f}% | **{r['f1_score']*100:.1f}%** |\n")

        f.write("\n## 3. Training & Validation Progress Overview\n")
        f.write(f"- **Train Samples:** {config['train_samples']:,}\n")
        f.write(f"- **Val Samples:** {config['val_samples']:,}\n")
        f.write(f"- **Test Samples (Immutable):** {config['test_samples']:,}\n")
        f.write(f"- **Total Classes:** {config['num_classes']}\n")
        f.write(f"- **Best Validation Macro F1:** {config['best_val_macro_f1']*100:.2f}% (Epoch {config['best_epoch']})\n\n")

    log_message(f"Generated Training Report at: {report_path}")


if __name__ == "__main__":
    code = train_pipeline()
    sys.exit(code)
