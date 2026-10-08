"""
Train Model 2 Disease Classifier v2 (EfficientNet-B2)
=====================================================
Fine-tunes the 117-class EfficientNet-B2 on the final Model 2 V2 dataset
(15,252 train, 1,697 val, 2,304 immutable test).

Hardware Target: RTX 3050 Laptop GPU (4 GB VRAM)
"""

import os
import sys
import csv
import json
import time
import math
import shutil
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.amp import autocast, GradScaler
import torchvision
from torchvision import transforms
from torchvision.models import efficientnet_b2, EfficientNet_B2_Weights
from sklearn.metrics import (
    accuracy_score,
    top_k_accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
DATA_DIR = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2"
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_manifest.csv"
CLASS_MAPPING_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_class_mapping.json"
CROP_DISEASE_MAP_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_crop_disease_mapping.json"

PREV_BEST_CHECKPOINT = PROJECT_ROOT / "models" / "model2_classifier" / "best_model.pth"

MODEL_DIR = PROJECT_ROOT / "models" / "model2_classifier_v2"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_classifier_v2"
PROGRESS_CSV = PROJECT_ROOT / "reports" / "model2_classifier" / "model2_v2_training_progress.csv"
TRAINING_LOG = PROJECT_ROOT / "reports" / "model2_classifier" / "model2_v2_training.log"

# Hyperparameters optimized for RTX 3050 4GB
BATCH_SIZE = 32
GRAD_ACCUM_STEPS = 2  # Effective batch size = 64
NUM_WORKERS = 2
IMAGE_SIZE = (260, 260)
MAX_EPOCHS = 20
PATIENCE = 10
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-4
RANDOM_SEED = 42

class PlantDiseaseDataset(Dataset):
    def __init__(self, records, transform=None):
        self.records = records
        self.transform = transform

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        rec = self.records[idx]
        img_path = PROJECT_ROOT / "data" / "processed" / rec["rel_path"]
        img = Image.open(img_path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        label = rec["class_id"]
        return img, label, idx

def get_transforms():
    train_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.2),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15, hue=0.05),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_test_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    return train_transform, val_test_transform

def load_dataset_records():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_records = list(reader)

    for r in all_records:
        r["class_id"] = int(r["class_id"])
        r["is_healthy"] = int(r["is_healthy"])

    train_recs = [r for r in all_records if r["split"] == "train"]
    val_recs = [r for r in all_records if r["split"] == "val"]
    test_recs = [r for r in all_records if r["split"] == "test"]

    return train_recs, val_recs, test_recs, all_records

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
        nn.Linear(in_features, num_classes)
    )
    return model

def load_previous_checkpoint(model, ckpt_path):
    if not ckpt_path.exists():
        print(f"[Warning] Previous checkpoint {ckpt_path} not found. Starting from ImageNet weights.", flush=True)
        return model, 0.0

    print(f"[Model 2 v2] Loading weights from previous best checkpoint: {ckpt_path}...", flush=True)
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    state_dict = ckpt.get("model_state_dict", ckpt)
    
    model_dict = model.state_dict()
    matched = {}
    mismatched = []
    for k, v in state_dict.items():
        if k in model_dict and model_dict[k].shape == v.shape:
            matched[k] = v
        else:
            mismatched.append(k)

    model_dict.update(matched)
    model.load_state_dict(model_dict)
    print(f"Loaded {len(matched)} layers successfully ({len(mismatched)} mismatched/new).", flush=True)
    prev_best_f1 = ckpt.get("val_macro_f1", 0.0) if isinstance(ckpt, dict) else 0.0
    return model, prev_best_f1

def init_progress_csv(csv_path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    headers = [
        "epoch", "stage", "learning_rate", "train_loss", "train_accuracy",
        "train_macro_f1", "train_weighted_f1", "val_loss", "val_accuracy",
        "val_macro_f1", "val_weighted_f1", "val_healthy_f1", "val_disease_macro_f1",
        "best_val_macro_f1", "best_epoch", "epoch_time_seconds", "gpu_memory_mb"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

def append_progress_csv(csv_path, row_data):
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row_data)

def log_message(msg):
    print(msg, flush=True)
    with open(TRAINING_LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

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

            with autocast('cuda'):
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
    
    # Top-3 Accuracy
    top3_acc = top_k_accuracy_score(all_targets, all_probs, k=min(3, num_classes), labels=list(range(num_classes)))

    # Metrics
    prec_m, rec_m, f1_m, _ = precision_recall_fscore_support(all_targets, all_preds, average='macro', zero_division=0)
    prec_w, rec_w, f1_w, _ = precision_recall_fscore_support(all_targets, all_preds, average='weighted', zero_division=0)

    # Per-class metrics
    prec_c, rec_c, f1_c, sup_c = precision_recall_fscore_support(all_targets, all_preds, average=None, labels=list(range(num_classes)), zero_division=0)

    healthy_f1 = f1_c[0] if num_classes > 0 else 0.0
    disease_f1s = [f1_c[i] for i in range(1, num_classes)]
    disease_macro_f1 = np.mean(disease_f1s) if len(disease_f1s) > 0 else 0.0

    metrics = {
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
        "probs": all_probs
    }
    return metrics

def train_pipeline():
    log_message("=" * 80)
    log_message("MODEL 2 V2 DISEASE CLASSIFIER TRAINING PIPELINE (EfficientNet-B2)")
    log_message("=" * 80)

    torch.manual_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(RANDOM_SEED)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    log_message(f"Execution Device : {device} ({gpu_name})")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load Taxonomy
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_map_data = json.load(f)
    class_to_id = class_map_data.get("class_to_id", class_map_data)
    id_to_class = {int(v): k for k, v in class_to_id.items()}
    num_classes = len(class_to_id)
    class_names = [id_to_class[i] for i in range(num_classes)]
    log_message(f"Taxonomy Loaded  : {num_classes} classes (Class 0 = {class_names[0]})")

    # 2. Load Dataset Records
    train_recs, val_recs, test_recs, all_recs = load_dataset_records()
    log_message(f"Dataset Records  : Train={len(train_recs):,}, Val={len(val_recs):,}, Test={len(test_recs):,} (Total={len(all_recs):,})")

    # 3. Create Datasets & DataLoaders
    train_tf, val_test_tf = get_transforms()
    train_dataset = PlantDiseaseDataset(train_recs, transform=train_tf)
    val_dataset = PlantDiseaseDataset(val_recs, transform=val_test_tf)
    test_dataset = PlantDiseaseDataset(test_recs, transform=val_test_tf)

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

    # 5. Build Model & Load Checkpoint
    model = build_model(num_classes).to(device)
    model, prev_best_f1 = load_previous_checkpoint(model, PREV_BEST_CHECKPOINT)

    # 6. Optimizer & Scheduler
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=MAX_EPOCHS, eta_min=1e-6)
    scaler = GradScaler('cuda')

    # 7. Initialize Progress CSV
    init_progress_csv(PROGRESS_CSV)
    log_message(f"Initialized Progress CSV at: {PROGRESS_CSV}")

    best_val_macro_f1 = 0.0
    best_epoch = 0
    patience_counter = 0

    history = {
        "train_loss": [], "train_acc": [], "train_macro_f1": [],
        "val_loss": [], "val_acc": [], "val_macro_f1": [], "val_disease_macro_f1": [], "val_healthy_f1": []
    }

    log_message("\nStarting Model 2 v2 Training Loop...")
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

            with autocast('cuda'):
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
        train_prec_m, train_rec_m, train_f1_m, _ = precision_recall_fscore_support(train_targets, train_preds, average='macro', zero_division=0)
        train_prec_w, train_rec_w, train_f1_w, _ = precision_recall_fscore_support(train_targets, train_preds, average='weighted', zero_division=0)

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

        # Check for Best Val Macro F1
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
                "classes": class_names
            }
            torch.save(best_ckpt, MODEL_DIR / "best_model.pth")
        else:
            patience_counter += 1

        # Always save last checkpoint
        last_ckpt = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "val_macro_f1": val_metrics["macro_f1"],
            "val_accuracy": val_metrics["accuracy"],
            "best_epoch": best_epoch,
            "best_val_macro_f1": best_val_macro_f1,
            "num_classes": num_classes,
            "classes": class_names
        }
        torch.save(last_ckpt, MODEL_DIR / "last_model.pth")

        # Live Progress CSV update
        csv_row = [
            epoch, "finetune_v2", f"{cur_lr:.6e}",
            f"{avg_train_loss:.4f}", f"{train_acc:.4f}", f"{train_f1_m:.4f}", f"{train_f1_w:.4f}",
            f"{val_metrics['loss']:.4f}", f"{val_metrics['accuracy']:.4f}", f"{val_metrics['macro_f1']:.4f}",
            f"{val_metrics['weighted_f1']:.4f}", f"{val_metrics['healthy_f1']:.4f}", f"{val_metrics['disease_macro_f1']:.4f}",
            f"{best_val_macro_f1:.4f}", best_epoch, f"{epoch_duration:.2f}", f"{gpu_mem:.2f}"
        ]
        append_progress_csv(PROGRESS_CSV, csv_row)

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

    # 8. Save Configuration
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
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else "N/A",
        "gpu": gpu_name,
        "train_samples": len(train_recs),
        "val_samples": len(val_recs),
        "test_samples": len(test_recs)
    }
    with open(MODEL_DIR / "config.json", "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)

    # 9. Plot Training Curves
    plot_training_curves(history, REPORTS_DIR / "training_curves.png")

    # 10. Final Independent Test Evaluation (IMMUTABLE 2,304 TEST SET)
    log_message("=" * 80)
    log_message("FINAL INDEPENDENT TEST EVALUATION (IMMUTABLE 2,304 TEST SET)")
    log_message("=" * 80)

    # Load Best Model Checkpoint
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
            "image_id": rec["image_id"],
            "filename": rec["filename"],
            "rel_path": rec["rel_path"],
            "ground_truth_class": rec["class_name"],
            "ground_truth_id": rec["class_id"],
            "predicted_class": id_to_class[pred],
            "predicted_id": int(pred),
            "is_correct": int(pred == rec["class_id"]),
            "confidence": float(prob[pred]),
            "top3_classes": "; ".join(top3_classes)
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
            "precision": test_metrics["per_class_precision"][cid],
            "recall": test_metrics["per_class_recall"][cid],
            "f1_score": test_metrics["per_class_f1"][cid],
            "support": int(test_metrics["per_class_support"][cid]),
            "is_healthy": int(cid == 0)
        })

    class_report_df = pd.DataFrame(class_report_rows)
    class_report_path = REPORTS_DIR / "classification_report.csv"
    class_report_df.to_csv(class_report_path, index=False)
    log_message(f"Saved Classification Report CSV to: {class_report_path}")

    # Plot Confusion Matrix
    plot_confusion_matrix(test_metrics["targets"], test_metrics["preds"], class_names, REPORTS_DIR / "confusion_matrix.png")

    # Generate Comprehensive Markdown Report
    generate_final_training_report(
        test_metrics, class_report_df, config_dict, best_ckpt
    )

def plot_training_curves(history, out_path):
    epochs = range(1, len(history["train_loss"]) + 1)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Loss
    axes[0].plot(epochs, history["train_loss"], 'b-o', label='Train Loss')
    axes[0].plot(epochs, history["val_loss"], 'r-s', label='Val Loss')
    axes[0].set_title('Cross-Entropy Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True, linestyle='--', alpha=0.6)

    # Accuracy
    axes[1].plot(epochs, [a * 100 for a in history["train_acc"]], 'b-o', label='Train Acc')
    axes[1].plot(epochs, [a * 100 for a in history["val_acc"]], 'g-s', label='Val Acc')
    axes[1].set_title('Classification Accuracy (%)')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy (%)')
    axes[1].legend()
    axes[1].grid(True, linestyle='--', alpha=0.6)

    # Macro F1
    axes[2].plot(epochs, [f * 100 for f in history["train_macro_f1"]], 'b-o', label='Train Macro F1')
    axes[2].plot(epochs, [f * 100 for f in history["val_macro_f1"]], 'm-s', label='Val Macro F1 (Selection Metric)')
    axes[2].plot(epochs, [f * 100 for f in history["val_disease_macro_f1"]], 'c--', label='Val Disease Macro F1')
    axes[2].set_title('Validation Macro F1 Scores (%)')
    axes[2].set_xlabel('Epoch')
    axes[2].set_ylabel('Macro F1 (%)')
    axes[2].legend()
    axes[2].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    log_message(f"Saved Training Curves to: {out_path}")

def plot_confusion_matrix(targets, preds, class_names, out_path):
    cm = confusion_matrix(targets, preds, labels=list(range(len(class_names))))
    plt.figure(figsize=(24, 20))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Model 2 v2 Test Confusion Matrix (117 Classes)', fontsize=16)
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=90, fontsize=6)
    plt.yticks(tick_marks, class_names, fontsize=6)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    log_message(f"Saved Confusion Matrix to: {out_path}")

def generate_final_training_report(test_metrics, class_report_df, config, best_ckpt):
    report_path = REPORTS_DIR / "model2_v2_training_report.md"

    # Baseline comparison metrics
    b_top1 = 84.29
    b_top3 = 94.57
    b_macro_f1 = 61.01
    b_dis_macro_f1 = 60.15
    b_healthy_f1 = 99.24

    v2_top1 = test_metrics["accuracy"] * 100
    v2_top3 = test_metrics["top3_accuracy"] * 100
    v2_macro_f1 = test_metrics["macro_f1"] * 100
    v2_dis_macro_f1 = test_metrics["disease_macro_f1"] * 100
    v2_healthy_f1 = test_metrics["healthy_f1"] * 100
    v2_weighted_f1 = test_metrics["weighted_f1"] * 100

    # Load Baseline Error Analysis
    baseline_err_file = PROJECT_ROOT / "reports" / "model2_classifier" / "model2_error_analysis.csv"
    b_f1_map = {}
    if baseline_err_file.exists():
        b_df = pd.read_csv(baseline_err_file)
        b_f1_map = {row["class_name"]: row["f1_score"] * 100 for _, row in b_df.iterrows()}

    lines = []
    lines.append("# Model 2 Disease Classifier v2 Final Training & Evaluation Report")
    lines.append("")
    lines.append("**Date:** 2026-10-07  ")
    lines.append("**Model Architecture:** `EfficientNet-B2` (117 Classes, PyTorch Transfer Learning)  ")
    lines.append(f"**Best Checkpoint:** [`models/model2_classifier_v2/best_model.pth`](file:///{MODEL_DIR / 'best_model.pth'}) (Selected at Epoch {best_ckpt['epoch']})  ")
    lines.append(f"**Evaluation Split:** Immutable Model 2 Test Set (2,304 Images)  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Executive Summary & Baseline Comparison")
    lines.append("")
    lines.append("| Metric | Baseline (v1) | Final V2 Model | Absolute Change | Relative Change (%) | Status |")
    lines.append("|---|---:|---:|---:|---:|:---:|")
    lines.append(f"| **Top-1 Accuracy** | {b_top1:.2f}% | **{v2_top1:.2f}%** | {v2_top1 - b_top1:+.2f}% | {((v2_top1 - b_top1)/b_top1)*100:+.2f}% | {'IMPROVED' if v2_top1 >= b_top1 else 'DEGRADED'} |")
    lines.append(f"| **Top-3 Accuracy** | {b_top3:.2f}% | **{v2_top3:.2f}%** | {v2_top3 - b_top3:+.2f}% | {((v2_top3 - b_top3)/b_top3)*100:+.2f}% | {'IMPROVED' if v2_top3 >= b_top3 else 'DEGRADED'} |")
    lines.append(f"| **Macro F1 (All 117)** | {b_macro_f1:.2f}% | **{v2_macro_f1:.2f}%** | {v2_macro_f1 - b_macro_f1:+.2f}% | {((v2_macro_f1 - b_macro_f1)/b_macro_f1)*100:+.2f}% | {'IMPROVED' if v2_macro_f1 >= b_macro_f1 else 'DEGRADED'} |")
    lines.append(f"| **Disease-only Macro F1** | {b_dis_macro_f1:.2f}% | **{v2_dis_macro_f1:.2f}%** | {v2_dis_macro_f1 - b_dis_macro_f1:+.2f}% | {((v2_dis_macro_f1 - b_dis_macro_f1)/b_dis_macro_f1)*100:+.2f}% | {'IMPROVED' if v2_dis_macro_f1 >= b_dis_macro_f1 else 'DEGRADED'} |")
    lines.append(f"| **Healthy F1 (Class 0)** | {b_healthy_f1:.2f}% | **{v2_healthy_f1:.2f}%** | {v2_healthy_f1 - b_healthy_f1:+.2f}% | {((v2_healthy_f1 - b_healthy_f1)/b_healthy_f1)*100:+.2f}% | {'PRESERVED' if v2_healthy_f1 >= 98.5 else 'REVIEW'} |")
    lines.append(f"| **Weighted F1** | N/A | **{v2_weighted_f1:.2f}%** | — | — | — |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Key Priority Disease Focus & Weak-Class Relief")
    lines.append("")
    lines.append("| Target Disease Class | Baseline F1 | Final V2 F1 | Absolute Change | Test Precision | Test Recall | Test Support | Impact |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---|")

    focus_classes = [
        "soybean__rust", "plum__rust", "cauliflower__alternaria_leaf_spot",
        "cauliflower__bacterial_soft_rot", "cherry__powdery_mildew", "raspberry__leaf_spot",
        "plum__bacterial_spot", "bell_pepper__frogeye_leaf_spot", "broccoli__ring_spot",
        "coffee__black_rot", "coffee__brown_eye_spot", "peach__rust",
        "cabbage__alternaria_leaf_spot", "plum__pocket_disease", "tobacco__frogeye_leaf_spot",
        "ginger__sheath_blight", "bean__mosaic_virus", "banana__cordana_leaf_spot",
        "zucchini__downy_mildew", "tomato__septoria_leaf_spot", "squash__powdery_mildew"
    ]

    for cname in focus_classes:
        sub = class_report_df[class_report_df["class_name"] == cname]
        if not sub.empty:
            r = sub.iloc[0]
            v2_f1 = r["f1_score"] * 100
            b_f1 = b_f1_map.get(cname, 0.0)
            diff = v2_f1 - b_f1
            imp = "**MAJOR RELIEF**" if diff >= 15.0 else ("IMPROVED" if diff > 0 else ("UNCHANGED" if diff == 0 else "DEGRADED"))
            lines.append(f"| `{cname}` | {b_f1:.2f}% | **{v2_f1:.2f}%** | {diff:+.2f}% | {r['precision']*100:.2f}% | {r['recall']*100:.2f}% | {int(r['support'])} | {imp} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Soybean Rust & Healthy Class Verification")
    lines.append("")
    sr_sub = class_report_df[class_report_df["class_name"] == "soybean__rust"].iloc[0]
    lines.append(f"### `soybean__rust` Performance:")
    lines.append(f"- **Baseline Test F1:** 41.67%")
    lines.append(f"- **Final V2 Test F1:** **{sr_sub['f1_score']*100:.2f}%** (Precision: {sr_sub['precision']*100:.2f}%, Recall: {sr_sub['recall']*100:.2f}%, Support: {int(sr_sub['support'])})")
    lines.append(f"- **Training Support:** Expanded from 46 to **455 images (+889%)**.")
    lines.append("")
    h_sub = class_report_df[class_report_df["class_name"] == "healthy"].iloc[0]
    lines.append(f"### `healthy` Class Performance:")
    lines.append(f"- **Baseline Healthy F1:** {b_healthy_f1:.2f}%")
    lines.append(f"- **Final V2 Healthy F1:** **{h_sub['f1_score']*100:.2f}%** (Precision: {h_sub['precision']*100:.2f}%, Recall: {h_sub['recall']*100:.2f}%, Support: {int(h_sub['support'])})")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Complete 117-Class Performance Table")
    lines.append("")
    lines.append("| Class ID | Class Name | Precision | Recall | F1 Score | Test Support | Baseline F1 | Change |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|---:|")

    for _, r in class_report_df.iterrows():
        cname = r["class_name"]
        cid = int(r["class_id"])
        b_f1 = b_f1_map.get(cname, 0.0)
        v2_f1 = r["f1_score"] * 100
        diff = v2_f1 - b_f1
        lines.append(f"| {cid} | `{cname}` | {r['precision']*100:.2f}% | {r['recall']*100:.2f}% | **{v2_f1:.2f}%** | {int(r['support'])} | {b_f1:.2f}% | {diff:+.2f}% |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Artifacts and Generated Visualizations")
    lines.append("")
    lines.append(f"- **Classification Report CSV:** [`reports/model2_classifier_v2/classification_report.csv`](file:///{REPORTS_DIR / 'classification_report.csv'})")
    lines.append(f"- **Test Predictions CSV:** [`reports/model2_classifier_v2/test_predictions.csv`](file:///{REPORTS_DIR / 'test_predictions.csv'})")
    lines.append(f"- **Confusion Matrix Plot:** [`reports/model2_classifier_v2/confusion_matrix.png`](file:///{REPORTS_DIR / 'confusion_matrix.png'})")
    lines.append(f"- **Training Curves Plot:** [`reports/model2_classifier_v2/training_curves.png`](file:///{REPORTS_DIR / 'training_curves.png'})")
    lines.append(f"- **Hyperparameters & Config:** [`models/model2_classifier_v2/config.json`](file:///{MODEL_DIR / 'config.json'})")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    log_message(f"Saved Final Training Markdown Report to: {report_path}")

if __name__ == "__main__":
    train_pipeline()
