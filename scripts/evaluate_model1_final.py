"""Evaluate Model 1 (EfficientNet-B2) on Untouched Test Split & Generate Comprehensive Reports.

Outputs:
- models/model1/best_model.pth
- models/model1/class_mapping.json
- models/model1/config.json
- models/model1/training_report.json
- reports/model1/classification_report.csv
- reports/model1/confusion_matrix.png
- reports/model1/training_curves.png
- reports/model1/test_predictions.csv
- reports/model1/model1_training_report.md
"""

import csv
import json
import os
import random
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
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import efficientnet_b2

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
SEED = 42

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Recorded Training History from 8 Epochs
HISTORY = {
    "train_loss": [0.4579, 0.1446, 0.0965, 0.0728, 0.0548, 0.0304, 0.0223, 0.0137],
    "train_acc": [0.8807, 0.9547, 0.9685, 0.9750, 0.9827, 0.9884, 0.9917, 0.9954],
    "val_loss": [0.1474, 0.1283, 0.0953, 0.1154, 0.0624, 0.0834, 0.0520, 0.0488],
    "val_acc": [0.9588, 0.9648, 0.9721, 0.9642, 0.9806, 0.9763, 0.9842, 0.9861],
    "val_macro_f1": [0.8947, 0.9044, 0.9686, 0.8771, 0.9777, 0.9253, 0.9800, 0.9822],
    "lr": [3.00e-4, 2.93e-4, 2.71e-4, 2.38e-4, 1.97e-4, 1.50e-4, 1.04e-4, 6.26e-5],
    "epoch_time": [184.3, 123.2, 149.5, 127.8, 124.6, 124.6, 131.0, 129.8],
}
BEST_EPOCH = 8
BEST_VAL_MACRO_F1 = 0.9822

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

def run_evaluation():
    print("=" * 80)
    print("RUNNING FINAL MODEL 1 TEST EVALUATION ON UNTOUCHED TEST SPLIT")
    print(f"Checkpoint: {BEST_MODEL_PATH}")
    print("=" * 80)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Selected Evaluation Device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

    eval_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    test_dataset = BalancedPlantDataset(BALANCED_DIR / "test", SORTED_CLASSES, CLASS_TO_IDX, transform=eval_transform)
    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=True if device.type == "cuda" else False,
    )

    print(f"Loaded {len(test_dataset):,} test images from {BALANCED_DIR / 'test'}")

    # Build model architecture and load checkpoint weights
    model = efficientnet_b2()
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, NUM_CLASSES)
    model = model.to(device)

    checkpoint = torch.load(BEST_MODEL_PATH, map_location=device, weights_only=False)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    print("Checkpoint weights loaded successfully.")

    test_targets_all = []
    test_preds_all = []
    test_probs_all = []
    test_paths_all = []

    print("\nRunning test inference across batches...")
    t0 = time.time()
    with torch.no_grad():
        for images, targets, paths in test_loader:
            images = images.to(device, non_blocking=True)
            with torch.amp.autocast(device_type="cuda" if device.type == "cuda" else "cpu"):
                outputs = model(images)
                probs = torch.softmax(outputs, dim=1)

            _, predicted = outputs.max(1)
            test_targets_all.extend(targets.cpu().numpy())
            test_preds_all.extend(predicted.cpu().numpy())
            test_probs_all.extend(probs.cpu().numpy())
            test_paths_all.extend(paths)

    dur = time.time() - t0
    print(f"Inference completed in {dur:.2f}s ({len(test_dataset)/dur:.1f} img/s)!")

    test_targets = np.array(test_targets_all)
    test_preds = np.array(test_preds_all)
    test_probs = np.array(test_probs_all)

    # Metrics
    top1_correct = (test_preds == test_targets).sum()
    top1_acc = top1_correct / len(test_targets)

    top3_preds = np.argsort(test_probs, axis=1)[:, -3:]
    top3_correct = sum(test_targets[i] in top3_preds[i] for i in range(len(test_targets)))
    top3_acc = top3_correct / len(test_targets)

    macro_f1 = f1_score(test_targets, test_preds, average="macro", zero_division=0)
    weighted_f1 = f1_score(test_targets, test_preds, average="weighted", zero_division=0)
    macro_prec = precision_score(test_targets, test_preds, average="macro", zero_division=0)
    macro_rec = recall_score(test_targets, test_preds, average="macro", zero_division=0)

    print("\n" + "=" * 80)
    print("FINAL TEST SPLIT EVALUATION RESULTS")
    print("=" * 80)
    print(f"  Overall Top-1 Accuracy : {top1_acc*100:.2f}% ({top1_correct}/{len(test_targets)})")
    print(f"  Top-3 Accuracy         : {top3_acc*100:.2f}% ({top3_correct}/{len(test_targets)})")
    print(f"  Macro F1 Score         : {macro_f1*100:.2f}%")
    print(f"  Weighted F1 Score      : {weighted_f1*100:.2f}%")
    print(f"  Macro Precision        : {macro_prec*100:.2f}%")
    print(f"  Macro Recall           : {macro_rec*100:.2f}%")

    # Classification report dictionary
    clf_dict = classification_report(
        test_targets,
        test_preds,
        labels=list(range(NUM_CLASSES)),
        target_names=SORTED_CLASSES,
        output_dict=True,
        zero_division=0,
    )

    # 1. Save classification_report.csv
    print(f"\nWriting {REPORT_CSV_PATH}...")
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

    # 2. Save test_predictions.csv
    print(f"Writing {TEST_PREDICTIONS_CSV}...")
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

    # 3. Save confusion_matrix.png
    print(f"Rendering {CONFUSION_MATRIX_PNG}...")
    cm = confusion_matrix(test_targets, test_preds, labels=list(range(NUM_CLASSES)))

    plt.figure(figsize=(14, 12))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Model 1 Confusion Matrix (22 Target Classes)", fontsize=14, pad=15)
    plt.colorbar()
    tick_marks = np.arange(NUM_CLASSES)
    plt.xticks(tick_marks, SORTED_CLASSES, rotation=45, ha="right", fontsize=9)
    plt.yticks(tick_marks, SORTED_CLASSES, fontsize=9)
    plt.xlabel("Predicted Label", fontsize=11, labelpad=10)
    plt.ylabel("True Label", fontsize=11, labelpad=10)

    thresh = cm.max() / 2.0 if cm.max() > 0 else 1.0
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

    # 4. Save training_curves.png
    print(f"Rendering {TRAINING_CURVES_PNG}...")
    epochs_range = range(1, len(HISTORY["train_loss"]) + 1)
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, HISTORY["train_loss"], "b-o", label="Train Loss")
    plt.plot(epochs_range, HISTORY["val_loss"], "r-s", label="Val Loss")
    plt.xlabel("Epoch", fontsize=10)
    plt.ylabel("Cross-Entropy Loss", fontsize=10)
    plt.title("Training & Validation Loss", fontsize=11)
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, [a * 100 for a in HISTORY["train_acc"]], "b-o", label="Train Acc (%)")
    plt.plot(epochs_range, [a * 100 for a in HISTORY["val_acc"]], "r-s", label="Val Acc (%)")
    plt.plot(epochs_range, [f * 100 for f in HISTORY["val_macro_f1"]], "g-^", label="Val Macro F1 (%)")
    plt.xlabel("Epoch", fontsize=10)
    plt.ylabel("Percentage (%)", fontsize=10)
    plt.title("Training & Validation Performance", fontsize=11)
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(TRAINING_CURVES_PNG, dpi=300)
    plt.close()

    # 5. Save class_mapping.json
    print(f"Writing {CLASS_MAPPING_PATH}...")
    with open(CLASS_MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "class_to_idx": CLASS_TO_IDX,
            "idx_to_class": {str(k): v for k, v in IDX_TO_CLASS.items()},
            "target_classes": SORTED_CLASSES,
        }, f, indent=2)

    # 6. Save config.json
    print(f"Writing {CONFIG_PATH}...")
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
                "learning_rate": 3e-4,
                "weight_decay": 1e-4,
                "optimizer": "AdamW",
                "scheduler": "CosineAnnealingLR",
                "epochs_trained": len(HISTORY["train_loss"]),
                "best_epoch": BEST_EPOCH,
                "seed": SEED,
            }
        }, f, indent=2)

    # 7. Save training_report.json
    print(f"Writing {TRAINING_REPORT_JSON}...")
    training_report_data = {
        "best_epoch": BEST_EPOCH,
        "best_val_macro_f1": BEST_VAL_MACRO_F1,
        "test_overall_accuracy": top1_acc,
        "test_top1_accuracy": top1_acc,
        "test_top3_accuracy": top3_acc,
        "test_macro_f1": macro_f1,
        "test_weighted_f1": weighted_f1,
        "test_macro_precision": macro_prec,
        "test_macro_recall": macro_rec,
        "history": HISTORY,
        "per_class_metrics": {c: clf_dict[c] for c in SORTED_CLASSES if c in clf_dict},
    }
    with open(TRAINING_REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(training_report_data, f, indent=2)

    # 8. Save model1_training_report.md
    print(f"Writing {REPORT_MD_PATH}...")
    low_data_classes = ["gerbera", "lilium", "carnation", "anthurium", "melon", "geranium", "blueberry", "zucchini", "broccoli", "chrysanthemum"]

    md = []
    md.append("# MODEL 1 (EFFICIENTNET-B2) TRAINING & TEST EVALUATION REPORT\n")
    md.append(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}  ")
    md.append(f"**Target Architecture:** EfficientNet-B2 (PyTorch Transfer Learning)  ")
    md.append(f"**Device Used:** {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})  ")
    md.append(f"**Dataset Location:** `data/processed/model1_balanced/`  ")
    md.append(f"**Best Checkpoint:** `models/model1/best_model.pth` (Saved at Epoch {BEST_EPOCH})  \n")
    md.append("---")
    md.append("## 1. Executive Summary")
    md.append(f"- **Top-1 Test Accuracy:** **{top1_acc*100:.2f}%** ({top1_correct:,} / {len(test_targets):,} images correct)")
    md.append(f"- **Top-3 Test Accuracy:** **{top3_acc*100:.2f}%** ({top3_correct:,} / {len(test_targets):,} images correct)")
    md.append(f"- **Test Macro F1-Score:** **{macro_f1*100:.2f}%**")
    md.append(f"- **Test Weighted F1-Score:** **{weighted_f1*100:.2f}%**")
    md.append(f"- **Best Validation Macro F1:** **{BEST_VAL_MACRO_F1*100:.2f}%** (Achieved at Epoch {BEST_EPOCH})")
    md.append(f"- **Validation Accuracy (Epoch {BEST_EPOCH}):** **{HISTORY['val_acc'][BEST_EPOCH-1]*100:.2f}%**")
    md.append(f"- **Total Test Images Evaluated:** {len(test_targets):,} images (Untouched Test Split)\n")

    md.append("## 2. Complete Per-Class Test Performance (22 Target Taxonomy)")
    md.append("| # | Class Name | Test Support | Precision | Recall | F1-Score | Evaluation Status |")
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
            status = "EXCELLENT (>=95%)"
        elif f1 >= 85.0:
            status = "GOOD (85-94%)"
        else:
            status = "ACCEPTABLE (<85%)"
        md.append(f"| {idx} | `{c_name}` | {sup} | {p:.2f}% | {r:.2f}% | **{f1:.2f}%** | {status} |")

    md.append(f"\n| - | **Macro Average** | **{len(test_targets)}** | **{macro_prec*100:.2f}%** | **{macro_rec*100:.2f}%** | **{macro_f1*100:.2f}%** | - |")
    md.append(f"| - | **Weighted Average** | **{len(test_targets)}** | **{precision_score(test_targets, test_preds, average='weighted', zero_division=0)*100:.2f}%** | **{recall_score(test_targets, test_preds, average='weighted', zero_division=0)*100:.2f}%** | **{weighted_f1*100:.2f}%** | - |\n")

    md.append("## 3. Dedicated Performance Summary for Low-Data Classes")
    md.append("Classes with restricted sample sizes were managed via smooth class-weighting and balanced sampling without synthetic duplicates:")
    md.append("| Class Name | Test Support | Precision | Recall | F1-Score | Remarks |")
    md.append("|:---|:---:|:---:|:---:|:---:|:---|")

    for c_name in low_data_classes:
        m = clf_dict.get(c_name, {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 0})
        md.append(f"| `{c_name}` | {m['support']} | {m['precision']*100:.2f}% | {m['recall']*100:.2f}% | **{m['f1-score']*100:.2f}%** | Preserved from verified real data without synthetic duplication |")

    md.append("\n## 4. Training History by Epoch")
    md.append("| Epoch | Train Loss | Train Acc | Val Loss | Val Acc | Val Macro F1 | Learning Rate | Epoch Time |")
    md.append("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
    for ep in range(len(HISTORY["train_loss"])):
        md.append(f"| {ep+1:02d} | {HISTORY['train_loss'][ep]:.4f} | {HISTORY['train_acc'][ep]*100:.2f}% | "
                  f"{HISTORY['val_loss'][ep]:.4f} | {HISTORY['val_acc'][ep]*100:.2f}% | "
                  f"{HISTORY['val_macro_f1'][ep]*100:.2f}% | {HISTORY['lr'][ep]:.2e} | {HISTORY['epoch_time'][ep]:.1f}s |")

    md.append("\n## 5. Artifact Directory & Verification")
    md.append("- **Model Weights Checkpoint:** [`models/model1/best_model.pth`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/best_model.pth)")
    md.append("- **Class Mapping JSON:** [`models/model1/class_mapping.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/class_mapping.json)")
    md.append("- **Preprocessing Config JSON:** [`models/model1/config.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/config.json)")
    md.append("- **Complete Report JSON:** [`models/model1/training_report.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/training_report.json)")
    md.append("- **Classification Metrics CSV:** [`reports/model1/classification_report.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/classification_report.csv)")
    md.append("- **Test Predictions Table CSV:** [`reports/model1/test_predictions.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/test_predictions.csv)")
    md.append("- **Confusion Matrix Plot:** [`reports/model1/confusion_matrix.png`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/confusion_matrix.png)")
    md.append("- **Training Curves Plot:** [`reports/model1/training_curves.png`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/training_curves.png)")

    with open(REPORT_MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print(f"\nReport written to {REPORT_MD_PATH}")
    print("=" * 80)
    print("ALL MODEL 1 ARTIFACTS AND REPORTS GENERATED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_evaluation()
