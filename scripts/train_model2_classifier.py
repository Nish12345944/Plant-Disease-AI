"""
Train Model 2 Disease Classifier (EfficientNet-B2)
==================================================
Trains a 117-class image classification model using PyTorch + torchvision EfficientNet-B2
with ImageNet transfer learning, class-weighted loss, AMP FP16, and stratified evaluation.

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
DATA_DIR = PROJECT_ROOT / "data" / "processed" / "model2_classifier"
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_manifest.csv"
CLASS_MAPPING_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_class_mapping.json"
CROP_DISEASE_MAP_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_crop_disease_mapping.json"

MODEL_DIR = PROJECT_ROOT / "models" / "model2_classifier"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_classifier"

# Hyperparameters optimized for RTX 3050 4GB
BATCH_SIZE = 32
GRAD_ACCUM_STEPS = 2  # Effective batch size = 64
NUM_WORKERS = 2
IMAGE_SIZE = (260, 260)
STAGE1_EPOCHS = 3
STAGE2_EPOCHS = 12
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
        # Smoothed inverse frequency: (Total / (K * cnt)) ^ alpha
        raw_w = (total_train / (num_classes * cnt)) ** alpha
        clamped_w = max(min_weight, min(max_weight, raw_w))
        weights.append(clamped_w)

    weights_tensor = torch.tensor(weights, dtype=torch.float32)
    # Re-normalize weights to mean = 1.0
    weights_tensor = weights_tensor / weights_tensor.mean()
    return weights_tensor, train_counts

def evaluate_model(model, dataloader, criterion, device, num_classes):
    model.eval()
    total_loss = 0.0
    all_preds = []
    all_targets = []
    all_probs = []

    with torch.no_grad():
        for images, targets, _ in dataloader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            with torch.amp.autocast('cuda'):
                outputs = model(images)
                loss = criterion(outputs, targets)

            probs = torch.softmax(outputs, dim=1)
            preds = torch.argmax(probs, dim=1)

            total_loss += loss.item() * images.size(0)
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())
            all_probs.append(probs.cpu().numpy())

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    all_probs = np.vstack(all_probs)
    avg_loss = total_loss / len(dataloader.dataset)

    acc = accuracy_score(all_targets, all_preds)
    
    # Top-3 accuracy
    top3_acc = top_k_accuracy_score(all_targets, all_probs, k=min(3, num_classes), labels=list(range(num_classes)))

    # Macro & Weighted metrics
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(all_targets, all_preds, average='macro', zero_division=0)
    p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(all_targets, all_preds, average='weighted', zero_division=0)

    # Healthy class metrics (class 0)
    p_per_class, r_per_class, f1_per_class, support_per_class = precision_recall_fscore_support(
        all_targets, all_preds, labels=list(range(num_classes)), zero_division=0
    )

    healthy_p = p_per_class[0]
    healthy_r = r_per_class[0]
    healthy_f1 = f1_per_class[0]

    # Disease-only Macro F1 (classes 1 to N-1)
    disease_f1_macro = float(np.mean(f1_per_class[1:]))

    return {
        "loss": avg_loss,
        "accuracy": float(acc),
        "top3_accuracy": float(top3_acc),
        "precision_macro": float(p_macro),
        "recall_macro": float(r_macro),
        "f1_macro": float(f1_macro),
        "precision_weighted": float(p_weighted),
        "recall_weighted": float(r_weighted),
        "f1_weighted": float(f1_weighted),
        "healthy_precision": float(healthy_p),
        "healthy_recall": float(healthy_r),
        "healthy_f1": float(healthy_f1),
        "disease_macro_f1": float(disease_f1_macro),
        "preds": all_preds,
        "targets": all_targets,
        "probs": all_probs,
        "per_class_precision": p_per_class,
        "per_class_recall": r_per_class,
        "per_class_f1": f1_per_class,
        "per_class_support": support_per_class
    }

def train_classifier():
    print("==================================================", flush=True)
    print("STARTING MODEL 2 EFFICIENTNET-B2 CLASSIFIER TRAINING", flush=True)
    print("==================================================", flush=True)

    torch.manual_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})", flush=True)

    # Load class mapping
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_mapping_data = json.load(f)
    classes = class_mapping_data["classes"]
    num_classes = len(classes)
    class_to_id = class_mapping_data["class_to_id"]
    id_to_class = {int(k): v for k, v in class_mapping_data["id_to_class"].items()}

    print(f"Total Target Classes: {num_classes}", flush=True)

    # Load records
    train_recs, val_recs, test_recs, all_recs = load_dataset_records()
    print(f"Dataset Splits: Train={len(train_recs):,}, Val={len(val_recs):,}, Test={len(test_recs):,}", flush=True)

    # Compute class weights
    class_weights, train_counts = compute_class_weights(train_recs, num_classes)
    class_weights = class_weights.to(device)
    print(f"Computed training-set class weights (Min: {class_weights.min():.2f}, Max: {class_weights.max():.2f}, Mean: {class_weights.mean():.2f})", flush=True)

    # Data loaders
    train_tf, val_tf = get_transforms()
    train_ds = PlantDiseaseDataset(train_recs, transform=train_tf)
    val_ds = PlantDiseaseDataset(val_recs, transform=val_tf)
    test_ds = PlantDiseaseDataset(test_recs, transform=val_tf)

    train_loader = DataLoader(
        train_ds, batch_size=BATCH_SIZE, shuffle=True,
        num_workers=NUM_WORKERS, pin_memory=True, drop_last=True
    )
    val_loader = DataLoader(
        val_ds, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=NUM_WORKERS, pin_memory=True
    )
    test_loader = DataLoader(
        test_ds, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=NUM_WORKERS, pin_memory=True
    )

    # Initialize EfficientNet-B2
    print("\n--- INITIALIZING EFFICIENTNET-B2 PRETRAINED BACKBONE ---", flush=True)
    model = efficientnet_b2(weights=EfficientNet_B2_Weights.IMAGENET1K_V1)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes)
    )
    model = model.to(device)

    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Model Architecture: EfficientNet-B2 (Total Params: {total_params:,}, Trainable Head: {trainable_params:,})", flush=True)

    criterion = nn.CrossEntropyLoss(weight=class_weights)
    scaler = torch.amp.GradScaler('cuda')

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    history = {
        "epoch": [],
        "stage": [],
        "train_loss": [],
        "val_loss": [],
        "val_accuracy": [],
        "val_top3_acc": [],
        "val_macro_f1": [],
        "val_weighted_f1": [],
        "val_healthy_f1": [],
        "val_disease_macro_f1": [],
        "lr": []
    }

    best_val_macro_f1 = -1.0
    best_epoch = 0
    best_model_path = MODEL_DIR / "best_model.pth"

    # STAGE 1: WARMUP CLASSIFICATION HEAD (BACKBONE FROZEN)
    print(f"\n==================================================", flush=True)
    print(f"STAGE 1: WARMUP HEAD ({STAGE1_EPOCHS} EPOCHS, BACKBONE FROZEN)", flush=True)
    print(f"==================================================", flush=True)

    for param in model.features.parameters():
        param.requires_grad = False

    stage1_optimizer = optim.AdamW(model.classifier.parameters(), lr=1e-3, weight_decay=1e-2)

    for epoch in range(1, STAGE1_EPOCHS + 1):
        t0 = time.time()
        model.train()
        train_loss = 0.0
        stage1_optimizer.zero_grad()

        for step, (images, targets, _) in enumerate(train_loader):
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            with torch.amp.autocast('cuda'):
                outputs = model(images)
                loss = criterion(outputs, targets) / GRAD_ACCUM_STEPS

            scaler.scale(loss).backward()

            if (step + 1) % GRAD_ACCUM_STEPS == 0 or (step + 1) == len(train_loader):
                scaler.step(stage1_optimizer)
                scaler.update()
                stage1_optimizer.zero_grad()

            train_loss += loss.item() * GRAD_ACCUM_STEPS * images.size(0)

        avg_train_loss = train_loss / len(train_ds)
        val_metrics = evaluate_model(model, val_loader, criterion, device, num_classes)
        elapsed = time.time() - t0

        print(
            f"Epoch {epoch:02d}/{STAGE1_EPOCHS:02d} [Stage 1] ({elapsed:.1f}s) | "
            f"Train Loss: {avg_train_loss:.4f} | "
            f"Val Loss: {val_metrics['loss']:.4f} | "
            f"Val Acc: {val_metrics['accuracy']*100:.2f}% | "
            f"Val Macro F1: {val_metrics['f1_macro']*100:.2f}% | "
            f"Val Disease F1: {val_metrics['disease_macro_f1']*100:.2f}% | "
            f"Val Healthy F1: {val_metrics['healthy_f1']*100:.2f}%",
            flush=True
        )

        history["epoch"].append(epoch)
        history["stage"].append(1)
        history["train_loss"].append(avg_train_loss)
        history["val_loss"].append(val_metrics["loss"])
        history["val_accuracy"].append(val_metrics["accuracy"])
        history["val_top3_acc"].append(val_metrics["top3_accuracy"])
        history["val_macro_f1"].append(val_metrics["f1_macro"])
        history["val_weighted_f1"].append(val_metrics["f1_weighted"])
        history["val_healthy_f1"].append(val_metrics["healthy_f1"])
        history["val_disease_macro_f1"].append(val_metrics["disease_macro_f1"])
        history["lr"].append(1e-3)

        if val_metrics["f1_macro"] > best_val_macro_f1:
            best_val_macro_f1 = val_metrics["f1_macro"]
            best_epoch = epoch
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "val_macro_f1": best_val_macro_f1,
                "val_accuracy": val_metrics["accuracy"],
                "num_classes": num_classes,
                "classes": classes
            }, best_model_path)
            print(f"  --> Saved new best checkpoint (Val Macro F1: {best_val_macro_f1*100:.2f}%)", flush=True)

    # STAGE 2: FULL NETWORK FINE-TUNING
    print(f"\n==================================================", flush=True)
    print(f"STAGE 2: FULL NETWORK FINE-TUNING ({STAGE2_EPOCHS} EPOCHS)", flush=True)
    print(f"==================================================", flush=True)

    for param in model.features.parameters():
        param.requires_grad = True

    stage2_optimizer = optim.AdamW([
        {"params": model.features.parameters(), "lr": 1e-4},
        {"params": model.classifier.parameters(), "lr": 3e-4}
    ], weight_decay=1e-2)

    scheduler = optim.lr_scheduler.CosineAnnealingLR(stage2_optimizer, T_max=STAGE2_EPOCHS, eta_min=1e-6)

    for s2_epoch in range(1, STAGE2_EPOCHS + 1):
        global_epoch = STAGE1_EPOCHS + s2_epoch
        t0 = time.time()
        model.train()
        train_loss = 0.0
        stage2_optimizer.zero_grad()

        for step, (images, targets, _) in enumerate(train_loader):
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            with torch.amp.autocast('cuda'):
                outputs = model(images)
                loss = criterion(outputs, targets) / GRAD_ACCUM_STEPS

            scaler.scale(loss).backward()

            if (step + 1) % GRAD_ACCUM_STEPS == 0 or (step + 1) == len(train_loader):
                scaler.step(stage2_optimizer)
                scaler.update()
                stage2_optimizer.zero_grad()

            train_loss += loss.item() * GRAD_ACCUM_STEPS * images.size(0)

        scheduler.step()
        current_lr = scheduler.get_last_lr()[-1]
        avg_train_loss = train_loss / len(train_ds)
        val_metrics = evaluate_model(model, val_loader, criterion, device, num_classes)
        elapsed = time.time() - t0

        print(
            f"Epoch {global_epoch:02d}/{STAGE1_EPOCHS+STAGE2_EPOCHS:02d} [Stage 2] ({elapsed:.1f}s, lr={current_lr:.1e}) | "
            f"Train Loss: {avg_train_loss:.4f} | "
            f"Val Loss: {val_metrics['loss']:.4f} | "
            f"Val Acc: {val_metrics['accuracy']*100:.2f}% | "
            f"Val Macro F1: {val_metrics['f1_macro']*100:.2f}% | "
            f"Val Disease F1: {val_metrics['disease_macro_f1']*100:.2f}% | "
            f"Val Healthy F1: {val_metrics['healthy_f1']*100:.2f}%",
            flush=True
        )

        history["epoch"].append(global_epoch)
        history["stage"].append(2)
        history["train_loss"].append(avg_train_loss)
        history["val_loss"].append(val_metrics["loss"])
        history["val_accuracy"].append(val_metrics["accuracy"])
        history["val_top3_acc"].append(val_metrics["top3_accuracy"])
        history["val_macro_f1"].append(val_metrics["f1_macro"])
        history["val_weighted_f1"].append(val_metrics["f1_weighted"])
        history["val_healthy_f1"].append(val_metrics["healthy_f1"])
        history["val_disease_macro_f1"].append(val_metrics["disease_macro_f1"])
        history["lr"].append(current_lr)

        if val_metrics["f1_macro"] > best_val_macro_f1:
            best_val_macro_f1 = val_metrics["f1_macro"]
            best_epoch = global_epoch
            torch.save({
                "epoch": global_epoch,
                "model_state_dict": model.state_dict(),
                "val_macro_f1": best_val_macro_f1,
                "val_accuracy": val_metrics["accuracy"],
                "num_classes": num_classes,
                "classes": classes
            }, best_model_path)
            print(f"  --> Saved new best checkpoint (Val Macro F1: {best_val_macro_f1*100:.2f}%)", flush=True)

    print(f"\nTraining Complete! Best Epoch: {best_epoch} with Validation Macro F1: {best_val_macro_f1*100:.2f}%", flush=True)

    # FINAL EVALUATION ON UNTOUCHED TEST SET
    print("\n==================================================", flush=True)
    print("EVALUATING BEST MODEL CHECKPOINT ON UNTOUCHED TEST SET", flush=True)
    print("==================================================", flush=True)

    checkpoint = torch.load(best_model_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    test_metrics = evaluate_model(model, test_loader, criterion, device, num_classes)

    print(f"Test Set Overall Accuracy     : {test_metrics['accuracy']*100:.2f}%", flush=True)
    print(f"Test Set Top-3 Accuracy       : {test_metrics['top3_accuracy']*100:.2f}%", flush=True)
    print(f"Test Set Macro Precision      : {test_metrics['precision_macro']*100:.2f}%", flush=True)
    print(f"Test Set Macro Recall         : {test_metrics['recall_macro']*100:.2f}%", flush=True)
    print(f"Test Set Macro F1             : {test_metrics['f1_macro']*100:.2f}%", flush=True)
    print(f"Test Set Weighted F1          : {test_metrics['f1_weighted']*100:.2f}%", flush=True)
    print(f"Healthy Class F1 (Class 0)    : {test_metrics['healthy_f1']*100:.2f}%", flush=True)
    print(f"Disease-Only Macro F1         : {test_metrics['disease_macro_f1']*100:.2f}%", flush=True)

    # Save classification report CSV
    cls_report_csv_path = REPORTS_DIR / "classification_report.csv"
    with open(cls_report_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["class_id", "class_name", "precision", "recall", "f1_score", "support", "train_samples", "imbalance_tier"])
        for c_id in range(num_classes):
            c_name = id_to_class[c_id]
            prec = test_metrics["per_class_precision"][c_id]
            rec = test_metrics["per_class_recall"][c_id]
            f1 = test_metrics["per_class_f1"][c_id]
            sup = int(test_metrics["per_class_support"][c_id])
            tr_cnt = train_counts.get(c_id, 0)
            tier = "<20" if tr_cnt < 20 else ("20-49" if tr_cnt < 50 else ("50-99" if tr_cnt < 100 else ">=100"))
            writer.writerow([c_id, c_name, f"{prec:.4f}", f"{rec:.4f}", f"{f1:.4f}", sup, tr_cnt, tier])

    # Save test predictions CSV
    test_preds_csv_path = REPORTS_DIR / "test_predictions.csv"
    with open(test_preds_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image_id", "filename", "crop", "true_class", "pred_class", "is_correct", "confidence", "true_is_healthy", "pred_is_healthy"])
        for idx, rec in enumerate(test_recs):
            true_cid = rec["class_id"]
            pred_cid = int(test_metrics["preds"][idx])
            conf = float(test_metrics["probs"][idx, pred_cid])
            true_name = id_to_class[true_cid]
            pred_name = id_to_class[pred_cid]
            is_correct = 1 if true_cid == pred_cid else 0
            true_healthy = 1 if true_cid == 0 else 0
            pred_healthy = 1 if pred_cid == 0 else 0
            writer.writerow([rec["image_id"], rec["filename"], rec["crop"], true_name, pred_name, is_correct, f"{conf:.4f}", true_healthy, pred_healthy])

    # Tail-class analysis by training sample tiers
    tier_stats = defaultdict(lambda: {"f1s": [], "supports": 0, "correct": 0, "classes": 0})
    for c_id in range(num_classes):
        tr_cnt = train_counts.get(c_id, 0)
        tier = "<20" if tr_cnt < 20 else ("20-49" if tr_cnt < 50 else ("50-99" if tr_cnt < 100 else ">=100"))
        tier_stats[tier]["f1s"].append(test_metrics["per_class_f1"][c_id])
        tier_stats[tier]["supports"] += int(test_metrics["per_class_support"][c_id])
        tier_stats[tier]["classes"] += 1

    print("\n--- TAIL-CLASS TIER PERFORMANCE ON TEST SET ---", flush=True)
    tier_summary = {}
    for tier in ["<20", "20-49", "50-99", ">=100"]:
        st = tier_stats[tier]
        avg_f1 = float(np.mean(st["f1s"])) if st["f1s"] else 0.0
        tier_summary[tier] = {
            "num_classes": st["classes"],
            "test_samples": st["supports"],
            "macro_f1": avg_f1
        }
        print(f"  Tier {tier:<6} : {st['classes']:>3} classes | {st['supports']:>5} test images | Macro F1: {avg_f1*100:.2f}%", flush=True)

    # Per-Crop performance analysis
    crop_stats = defaultdict(lambda: {"total": 0, "correct": 0, "healthy_correct": 0, "healthy_total": 0, "disease_correct": 0, "disease_total": 0})
    for idx, rec in enumerate(test_recs):
        crop = rec["crop"].strip().title()
        true_cid = rec["class_id"]
        pred_cid = int(test_metrics["preds"][idx])
        is_corr = (true_cid == pred_cid)
        crop_stats[crop]["total"] += 1
        if is_corr:
            crop_stats[crop]["correct"] += 1

        if true_cid == 0:
            crop_stats[crop]["healthy_total"] += 1
            if is_corr:
                crop_stats[crop]["healthy_correct"] += 1
        else:
            crop_stats[crop]["disease_total"] += 1
            if is_corr:
                crop_stats[crop]["disease_correct"] += 1

    per_crop_summary = {}
    print("\n--- PER-CROP PERFORMANCE ON TEST SET (SAMPLE) ---", flush=True)
    for crop, st in sorted(crop_stats.items(), key=lambda x: -x[1]["total"])[:15]:
        acc = st["correct"] / st["total"] if st["total"] > 0 else 0.0
        h_acc = st["healthy_correct"] / st["healthy_total"] if st["healthy_total"] > 0 else 0.0
        d_acc = st["disease_correct"] / st["disease_total"] if st["disease_total"] > 0 else 0.0
        per_crop_summary[crop] = {
            "total_test_images": st["total"],
            "accuracy": float(acc),
            "healthy_accuracy": float(h_acc),
            "disease_accuracy": float(d_acc)
        }
        print(f"  {crop:<15} : {st['total']:>4} test images | Accuracy: {acc*100:.1f}% (Healthy: {h_acc*100:.1f}%, Disease: {d_acc*100:.1f}%)", flush=True)

    # Generate training curves plot
    plot_path = REPORTS_DIR / "training_curves.png"
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history["epoch"], history["train_loss"], label="Train Loss", color="crimson")
    plt.plot(history["epoch"], history["val_loss"], label="Val Loss", color="royalblue")
    plt.axvline(x=STAGE1_EPOCHS + 0.5, color="gray", linestyle="--", label="Unfreeze Backbone")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(history["epoch"], [x * 100 for x in history["val_accuracy"]], label="Val Accuracy", color="forestgreen")
    plt.plot(history["epoch"], [x * 100 for x in history["val_macro_f1"]], label="Val Macro F1", color="purple")
    plt.plot(history["epoch"], [x * 100 for x in history["val_disease_macro_f1"]], label="Val Disease F1", color="darkorange", linestyle=":")
    plt.axvline(x=STAGE1_EPOCHS + 0.5, color="gray", linestyle="--", label="Unfreeze Backbone")
    plt.title("Validation Performance Metrics (%)")
    plt.xlabel("Epoch")
    plt.ylabel("Score (%)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"\nSaved training curves to {plot_path}", flush=True)

    # Generate Confusion Matrix plot
    cm_path = REPORTS_DIR / "confusion_matrix.png"
    cm = confusion_matrix(test_metrics["targets"], test_metrics["preds"], labels=list(range(num_classes)))
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(f"Model 2 Classifier Confusion Matrix ({num_classes} Classes)")
    plt.colorbar()
    plt.xlabel("Predicted Class ID")
    plt.ylabel("True Class ID")
    plt.tight_layout()
    plt.savefig(cm_path, dpi=150)
    plt.close()
    print(f"Saved confusion matrix plot to {cm_path}", flush=True)

    # Save training report JSON & config JSON
    training_report_data = {
        "model_architecture": "EfficientNet-B2 (Pretrained ImageNet-1K)",
        "hardware": {
            "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
            "pytorch_version": torch.__version__,
            "torchvision_version": torchvision.__version__
        },
        "hyperparameters": {
            "batch_size": BATCH_SIZE,
            "gradient_accumulation_steps": GRAD_ACCUM_STEPS,
            "effective_batch_size": BATCH_SIZE * GRAD_ACCUM_STEPS,
            "stage1_epochs": STAGE1_EPOCHS,
            "stage2_epochs": STAGE2_EPOCHS,
            "total_epochs": STAGE1_EPOCHS + STAGE2_EPOCHS,
            "stage1_lr": 1e-3,
            "stage2_classifier_lr": 3e-4,
            "stage2_backbone_lr": 1e-4,
            "optimizer": "AdamW",
            "scheduler": "CosineAnnealingLR",
            "image_size": IMAGE_SIZE
        },
        "dataset_split_counts": {
            "train": len(train_recs),
            "val": len(val_recs),
            "test": len(test_recs),
            "total": len(all_recs),
            "num_classes": num_classes
        },
        "training_outcome": {
            "status": "COMPLETED",
            "best_epoch": best_epoch,
            "best_val_macro_f1": float(best_val_macro_f1)
        },
        "test_evaluation": {
            "accuracy": test_metrics["accuracy"],
            "top3_accuracy": test_metrics["top3_accuracy"],
            "macro_precision": test_metrics["precision_macro"],
            "macro_recall": test_metrics["recall_macro"],
            "macro_f1": test_metrics["f1_macro"],
            "weighted_precision": test_metrics["precision_weighted"],
            "weighted_recall": test_metrics["recall_weighted"],
            "weighted_f1": test_metrics["f1_weighted"],
            "healthy_precision": test_metrics["healthy_precision"],
            "healthy_recall": test_metrics["healthy_recall"],
            "healthy_f1": test_metrics["healthy_f1"],
            "disease_macro_f1": test_metrics["disease_macro_f1"]
        },
        "tail_class_performance": tier_summary,
        "per_crop_performance": per_crop_summary,
        "history": history
    }

    report_json_path = MODEL_DIR / "training_report.json"
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(training_report_data, f, indent=2)

    config_json_path = MODEL_DIR / "config.json"
    with open(config_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "model_type": "efficientnet_b2",
            "num_classes": num_classes,
            "image_size": IMAGE_SIZE,
            "mean": [0.485, 0.456, 0.406],
            "std": [0.229, 0.224, 0.225],
            "decision_thresholds": {
                "healthy_threshold": 0.50,
                "disease_threshold": 0.35,
                "uncertain_threshold": 0.20
            }
        }, f, indent=2)

    shutil.copy2(CLASS_MAPPING_PATH, MODEL_DIR / "class_mapping.json")

    # Generate Markdown Training Report
    md_report_path = REPORTS_DIR / "model2_classifier_training_report.md"
    generate_markdown_report(md_report_path, training_report_data, tier_summary, per_crop_summary)
    print(f"Markdown training report saved to {md_report_path}", flush=True)

def generate_markdown_report(report_path: Path, report_data: dict, tier_summary: dict, per_crop_summary: dict):
    test_eval = report_data["test_evaluation"]
    hp = report_data["hyperparameters"]
    hw = report_data["hardware"]

    lines = [
        "# Model 2 Disease Classifier: Comprehensive Training & Evaluation Report",
        "",
        "**Date:** 2026-10-07  ",
        "**Architecture:** EfficientNet-B2 (`torchvision.models.efficientnet_b2` with ImageNet Pretraining)  ",
        "**Target Task:** Whole-Leaf Crop Disease Image Classification (117 Classes)  ",
        f"**Hardware Platform:** {hw['device']} (PyTorch {hw['pytorch_version']}, Torchvision {hw['torchvision_version']})  ",
        "",
        "---",
        "",
        "## 1. Executive Summary & Core Results",
        "",
        "```",
        f"TRAINING STATUS                    : {report_data['training_outcome']['status']}",
        f"BEST EPOCH                         : Epoch {report_data['training_outcome']['best_epoch']}",
        f"BEST VALIDATION MACRO F1           : {report_data['training_outcome']['best_val_macro_f1']*100:.2f}%",
        f"TEST TOP-1 ACCURACY                : {test_eval['accuracy']*100:.2f}%",
        f"TEST TOP-3 ACCURACY                : {test_eval['top3_accuracy']*100:.2f}%",
        f"TEST MACRO F1                      : {test_eval['macro_f1']*100:.2f}%",
        f"TEST WEIGHTED F1                   : {test_eval['weighted_f1']*100:.2f}%",
        f"HEALTHY CLASS F1 (Class 0)         : {test_eval['healthy_f1']*100:.2f}%",
        f"DISEASE-ONLY MACRO F1 (116 Diseases): {test_eval['disease_macro_f1']*100:.2f}%",
        "```",
        "",
        "---",
        "",
        "## 2. Training Hyperparameters & Strategy",
        "",
        "| Hyperparameter | Value | Rationale |",
        "| :--- | :--- | :--- |",
        f"| **Backbone Architecture** | EfficientNet-B2 | Optimal accuracy-efficiency trade-off for 4GB RTX 3050 |",
        f"| **Input Resolution** | 260 x 260 px | Standard native resolution for EfficientNet-B2 |",
        f"| **Batch Size / Accumulation** | 32 (x2 grad accum = 64 eff.) | Fits within 4GB VRAM while preserving stable BN gradients |",
        f"| **Mixed Precision** | Native PyTorch AMP (FP16) | Accelerated computation and low VRAM footprint |",
        f"| **Transfer Learning Protocol** | 2-Stage Warmup & Fine-Tune | Stage 1 (3 ep head warmup) -> Stage 2 (12 ep full unfreeze) |",
        f"| **Optimizer & Weight Decay** | AdamW (1e-2 decay) | Robust convergence and regularization |",
        "| **Loss Function** | Smoothed Class-Weighted CrossEntropy | (N / (K * N_c))^0.5 from training set counts |",
        "",
        "---",
        "",
        "## 3. Tail-Class Tier Performance Analysis",
        "",
        "| Sample Count Tier (Train Set) | Number of Classes | Test Set Image Support | Test Macro F1 (%) |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for tier, info in tier_summary.items():
        lines.append(f"| **{tier} samples** | {info['num_classes']} classes | {info['test_samples']} images | **{info['macro_f1']*100:.2f}%** |")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Per-Crop Evaluation Summary (Top Crops)",
        "",
        "| Crop | Test Support | Overall Accuracy (%) | Healthy Accuracy (%) | Disease Accuracy (%) |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])

    for crop, info in list(per_crop_summary.items())[:20]:
        lines.append(f"| **{crop}** | {info['total_test_images']} images | **{info['accuracy']*100:.1f}%** | {info['healthy_accuracy']*100:.1f}% | {info['disease_accuracy']*100:.1f}% |")

    lines.extend([
        "",
        "---",
        "",
        "## 5. Artifact Paths",
        "",
        "- Best Checkpoint: [`models/model2_classifier/best_model.pth`](file:///models/model2_classifier/best_model.pth)",
        "- Class Mapping: [`models/model2_classifier/class_mapping.json`](file:///models/model2_classifier/class_mapping.json)",
        "- Configuration: [`models/model2_classifier/config.json`](file:///models/model2_classifier/config.json)",
        "- Training Report JSON: [`models/model2_classifier/training_report.json`](file:///models/model2_classifier/training_report.json)",
        "- Classification Report CSV: [`reports/model2_classifier/classification_report.csv`](file:///reports/model2_classifier/classification_report.csv)",
        "- Test Predictions CSV: [`reports/model2_classifier/test_predictions.csv`](file:///reports/model2_classifier/test_predictions.csv)",
        "- Training Curves: [`reports/model2_classifier/training_curves.png`](file:///reports/model2_classifier/training_curves.png)",
        "- Confusion Matrix: [`reports/model2_classifier/confusion_matrix.png`](file:///reports/model2_classifier/confusion_matrix.png)"
    ])

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    train_classifier()
