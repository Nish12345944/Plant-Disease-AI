"""
Evaluate Model 2 v2 on Immutable 2,304 Test Set
================================================
Evaluates the trained Model 2 v2 EfficientNet-B2 best_model.pth checkpoint
against the immutable Model 2 test set.

Outputs:
- reports/model2_classifier_v2/classification_report.csv
- reports/model2_classifier_v2/test_predictions.csv
- reports/model2_classifier_v2/confusion_matrix.png
- reports/model2_classifier_v2/training_curves.png
- reports/model2_classifier_v2/model2_v2_training_report.md
- models/model2_classifier_v2/config.json
"""

import os
import sys
import csv
import json
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torchvision.models import efficientnet_b2, EfficientNet_B2_Weights
from sklearn.metrics import (
    accuracy_score,
    top_k_accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix
)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
DATA_DIR = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2"
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_manifest.csv"
CLASS_MAPPING_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_class_mapping.json"
CROP_DISEASE_MAP_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_crop_disease_mapping.json"
PROGRESS_CSV = PROJECT_ROOT / "reports" / "model2_classifier" / "model2_v2_training_progress.csv"

MODEL_DIR = PROJECT_ROOT / "models" / "model2_classifier_v2"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_classifier_v2"

BATCH_SIZE = 32
IMAGE_SIZE = (260, 260)
NUM_WORKERS = 2

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

def build_model(num_classes=117):
    model = efficientnet_b2(weights=EfficientNet_B2_Weights.DEFAULT)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes)
    )
    return model

def run_evaluation():
    print("=" * 80, flush=True)
    print("EVALUATING MODEL 2 V2 BEST MODEL ON IMMUTABLE TEST SET (2,304 Images)", flush=True)
    print("=" * 80, flush=True)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})", flush=True)

    # 1. Load Taxonomy
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        class_map_data = json.load(f)
    class_to_id = class_map_data.get("class_to_id", class_map_data)
    id_to_class = {int(v): k for k, v in class_to_id.items()}
    num_classes = len(class_to_id)
    class_names = [id_to_class[i] for i in range(num_classes)]

    # 2. Load Test Records
    manifest_df = pd.read_csv(MANIFEST_PATH)
    test_df = manifest_df[manifest_df["split"] == "test"].copy()
    test_recs = test_df.to_dict("records")
    for r in test_recs:
        r["class_id"] = int(r["class_id"])
    print(f"Test Records: {len(test_recs):,} images (100% immutable).", flush=True)

    test_transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    test_dataset = PlantDiseaseDataset(test_recs, transform=test_transform)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True)

    # 3. Load Best Checkpoint
    best_ckpt_path = MODEL_DIR / "best_model.pth"
    print(f"Loading checkpoint from: {best_ckpt_path}...", flush=True)
    best_ckpt = torch.load(best_ckpt_path, map_location=device, weights_only=False)
    
    model = build_model(num_classes).to(device)
    model.load_state_dict(best_ckpt["model_state_dict"])
    model.eval()
    print(f"Model loaded from Best Epoch {best_ckpt['epoch']} (Val Macro F1: {best_ckpt['val_macro_f1']*100:.2f}%)", flush=True)

    # 4. Evaluate on Test Set
    all_preds = []
    all_targets = []
    all_probs = []

    print("Running inference on 2,304 test images...", flush=True)
    with torch.no_grad():
        for images, labels, _ in test_loader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            with torch.amp.autocast('cuda'):
                outputs = model(images)

            probs = torch.softmax(outputs, dim=1)
            preds = torch.argmax(probs, dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    all_probs = np.array(all_probs)

    # Metrics
    acc = accuracy_score(all_targets, all_preds)
    top3_acc = top_k_accuracy_score(all_targets, all_probs, k=3, labels=list(range(num_classes)))
    prec_m, rec_m, f1_m, _ = precision_recall_fscore_support(all_targets, all_preds, average='macro', zero_division=0)
    prec_w, rec_w, f1_w, _ = precision_recall_fscore_support(all_targets, all_preds, average='weighted', zero_division=0)
    prec_c, rec_c, f1_c, sup_c = precision_recall_fscore_support(all_targets, all_preds, average=None, labels=list(range(num_classes)), zero_division=0)

    healthy_f1 = f1_c[0]
    disease_f1s = [f1_c[i] for i in range(1, num_classes)]
    disease_macro_f1 = np.mean(disease_f1s)

    test_metrics = {
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

    print("\n" + "=" * 80, flush=True)
    print("TEST EVALUATION RESULTS SUMMARY", flush=True)
    print("=" * 80, flush=True)
    print(f"Top-1 Accuracy        : {acc*100:.2f}% (Baseline: 84.29%)", flush=True)
    print(f"Top-3 Accuracy        : {top3_acc*100:.2f}% (Baseline: 94.57%)", flush=True)
    print(f"Macro F1              : {f1_m*100:.2f}% (Baseline: 61.01%)", flush=True)
    print(f"Disease-only Macro F1 : {disease_macro_f1*100:.2f}% (Baseline: 60.15%)", flush=True)
    print(f"Healthy F1            : {healthy_f1*100:.2f}% (Baseline: 99.24%)", flush=True)
    print(f"Weighted F1           : {f1_w*100:.2f}%", flush=True)
    print("=" * 80, flush=True)

    # 5. Save Test Predictions CSV
    test_pred_records = []
    for idx, (rec, pred, prob) in enumerate(zip(test_recs, all_preds, all_probs)):
        top3_idx = np.argsort(prob)[-3:][::-1]
        top3_classes = [id_to_class[i] for i in top3_idx]
        test_pred_records.append({
            "image_id": rec["image_id"],
            "filename": rec["filename"],
            "rel_path": rec["rel_path"],
            "ground_truth_class": rec["classification_class"],
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
    print(f"Saved Test Predictions to: {test_pred_path}", flush=True)

    # 6. Save Classification Report CSV
    class_report_rows = []
    for cid in range(num_classes):
        cname = id_to_class[cid]
        class_report_rows.append({
            "class_id": cid,
            "class_name": cname,
            "precision": prec_c[cid],
            "recall": rec_c[cid],
            "f1_score": f1_c[cid],
            "support": int(sup_c[cid]),
            "is_healthy": int(cid == 0)
        })

    class_report_df = pd.DataFrame(class_report_rows)
    class_report_path = REPORTS_DIR / "classification_report.csv"
    class_report_df.to_csv(class_report_path, index=False)
    print(f"Saved Classification Report to: {class_report_path}", flush=True)

    # 7. Plot Confusion Matrix
    plot_confusion_matrix(all_targets, all_preds, class_names, REPORTS_DIR / "confusion_matrix.png")

    # 8. Plot Training Curves from Progress CSV
    plot_curves_from_csv(PROGRESS_CSV, REPORTS_DIR / "training_curves.png")

    # 9. Save Config JSON
    train_count = len(manifest_df[manifest_df["split"] == "train"])
    val_count = len(manifest_df[manifest_df["split"] == "val"])
    test_count = len(test_df)
    config_dict = {
        "model_architecture": "efficientnet_b2",
        "num_classes": num_classes,
        "image_size": IMAGE_SIZE,
        "batch_size": BATCH_SIZE,
        "effective_batch_size": BATCH_SIZE * 2,
        "learning_rate": 1e-4,
        "weight_decay": 1e-4,
        "optimizer": "AdamW",
        "scheduler": "CosineAnnealingLR",
        "random_seed": 42,
        "best_epoch": int(best_ckpt["epoch"]),
        "best_val_macro_f1": float(best_ckpt["val_macro_f1"]),
        "test_top1_accuracy": float(acc),
        "test_top3_accuracy": float(top3_acc),
        "test_macro_f1": float(f1_m),
        "test_disease_macro_f1": float(disease_macro_f1),
        "test_healthy_f1": float(healthy_f1),
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else "N/A",
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
        "train_samples": train_count,
        "val_samples": val_count,
        "test_samples": test_count
    }
    with open(MODEL_DIR / "config.json", "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)
    print(f"Saved Config to: {MODEL_DIR / 'config.json'}", flush=True)

    # 10. Generate Final Training Report
    generate_final_training_report(test_metrics, class_report_df, config_dict, best_ckpt)

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
    print(f"Saved Confusion Matrix Plot to: {out_path}", flush=True)

def plot_curves_from_csv(csv_path, out_path):
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    epochs = df["epoch"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Loss
    axes[0].plot(epochs, df["train_loss"], 'b-o', label='Train Loss')
    axes[0].plot(epochs, df["val_loss"], 'r-s', label='Val Loss')
    axes[0].set_title('Cross-Entropy Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True, linestyle='--', alpha=0.6)

    # Accuracy
    axes[1].plot(epochs, df["train_accuracy"] * 100, 'b-o', label='Train Acc')
    axes[1].plot(epochs, df["val_accuracy"] * 100, 'g-s', label='Val Acc')
    axes[1].set_title('Classification Accuracy (%)')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy (%)')
    axes[1].legend()
    axes[1].grid(True, linestyle='--', alpha=0.6)

    # Macro F1
    axes[2].plot(epochs, df["train_macro_f1"] * 100, 'b-o', label='Train Macro F1')
    axes[2].plot(epochs, df["val_macro_f1"] * 100, 'm-s', label='Val Macro F1 (Selection Metric)')
    axes[2].plot(epochs, df["val_disease_macro_f1"] * 100, 'c--', label='Val Disease Macro F1')
    axes[2].set_title('Validation Macro F1 Scores (%)')
    axes[2].set_xlabel('Epoch')
    axes[2].set_ylabel('Macro F1 (%)')
    axes[2].legend()
    axes[2].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved Training Curves Plot to: {out_path}", flush=True)

def generate_final_training_report(test_metrics, class_report_df, config, best_ckpt):
    report_path = REPORTS_DIR / "model2_v2_training_report.md"

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

    print(f"\nSaved Final Training Markdown Report to: {report_path}", flush=True)

if __name__ == "__main__":
    run_evaluation()
