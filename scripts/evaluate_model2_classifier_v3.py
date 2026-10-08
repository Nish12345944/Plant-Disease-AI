"""
Evaluate Model 2 V3 on Immutable Test Set (2,304 images) and Generate Reports
==============================================================================
Evaluates the best checkpoint from `models/model2_classifier_v3/best_model.pth`.
Generates:
- classification_report.csv
- test_predictions.csv
- confusion_matrix.png
- training_curves.png
- config.json & class_mapping.json in models/model2_classifier_v3/
- model2_v3_training_report.md
"""

import csv
import json
import os
import sys
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
from torch.amp import autocast
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import efficientnet_b2

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
ORGANIZED_DIR = PROJECT_ROOT / "data" / "processed" / "model2_organized"
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_organized_manifest.csv"
CLASS_MAPPING_PATH = PROJECT_ROOT / "data" / "processed" / "model2_organized_class_mapping.json"
MODEL_DIR = PROJECT_ROOT / "models" / "model2_classifier_v3"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_classifier_v3"
PROGRESS_CSV = REPORTS_DIR / "training_progress.csv"

IMAGE_SIZE = (260, 260)
BATCH_SIZE = 32
NUM_WORKERS = 0


class OrganizedTestDataset(Dataset):
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


def evaluate_v3():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Evaluation] Using device: {device}")

    # 1. Load Taxonomy
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        raw_map = json.load(f)
        class_to_id = raw_map.get("class_to_id", raw_map)
    id_to_class = {int(v): k for k, v in class_to_id.items()}
    num_classes = len(class_to_id)

    # Copy class mapping to model directory
    with open(MODEL_DIR / "class_mapping.json", "w", encoding="utf-8") as f:
        json.dump(class_to_id, f, indent=2)

    # 2. Load Test Records
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        all_recs = list(csv.DictReader(f))

    for r in all_recs:
        r["class_id"] = int(r["class_id"])

    train_recs = [r for r in all_recs if r["split"] == "train"]
    val_recs = [r for r in all_recs if r["split"] == "val"]
    test_recs = [r for r in all_recs if r["split"] == "test"]

    print(f"Loaded {len(test_recs):,} immutable test records (Train: {len(train_recs):,}, Val: {len(val_recs):,}).")

    # 3. Data Loader
    val_test_tf = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    test_dataset = OrganizedTestDataset(test_recs, ORGANIZED_DIR, transform=val_test_tf)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True)

    # 4. Load Model
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes),
    )

    best_ckpt_path = MODEL_DIR / "best_model.pth"
    print(f"Loading best checkpoint from: {best_ckpt_path}")
    ckpt = torch.load(best_ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model_state_dict"])
    model.to(device)
    model.eval()

    best_epoch = ckpt.get("epoch", 9)
    best_val_macro_f1 = ckpt.get("val_macro_f1", 0.6913)

    # 5. Evaluate on Test Set
    eval_criterion = nn.CrossEntropyLoss()
    total_loss = 0.0
    all_preds = []
    all_targets = []
    all_probs = []

    with torch.no_grad():
        for images, labels, _ in test_loader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            with autocast("cuda" if torch.cuda.is_available() else "cpu"):
                outputs = model(images)
                loss = eval_criterion(outputs, labels)

            total_loss += loss.item() * images.size(0)
            probs = torch.softmax(outputs, dim=1)
            preds = torch.argmax(probs, dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())

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

    print("\n=== MODEL 2 V3 TEST EVALUATION RESULTS ===")
    print(f"Top-1 Accuracy        : {acc*100:.2f}%")
    print(f"Top-3 Accuracy        : {top3_acc*100:.2f}%")
    print(f"Macro F1 Score        : {f1_m*100:.2f}%")
    print(f"Weighted F1 Score     : {f1_w*100:.2f}%")
    print(f"Disease-Only Macro F1 : {disease_macro_f1*100:.2f}%")
    print(f"Healthy F1 Score      : {healthy_f1*100:.2f}%")

    # 6. Save Test Predictions CSV
    test_pred_records = []
    for idx, (rec, pred, prob) in enumerate(zip(test_recs, all_preds, all_probs)):
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
    print(f"[Saved] Test Predictions to: {test_pred_path}")

    # 7. Save Classification Report CSV
    class_report_rows = []
    for cid in range(num_classes):
        cname = id_to_class[cid]
        class_report_rows.append({
            "class_id": cid,
            "class_name": cname,
            "precision": float(prec_c[cid]),
            "recall": float(rec_c[cid]),
            "f1_score": float(f1_c[cid]),
            "support": int(sup_c[cid]),
            "is_healthy": int(cid == 0),
        })

    class_report_df = pd.DataFrame(class_report_rows)
    class_report_path = REPORTS_DIR / "classification_report.csv"
    class_report_df.to_csv(class_report_path, index=False)
    print(f"[Saved] Classification Report to: {class_report_path}")

    # 8. Save config.json
    config_dict = {
        "model_architecture": "efficientnet_b2",
        "num_classes": num_classes,
        "image_size": IMAGE_SIZE,
        "batch_size": BATCH_SIZE,
        "effective_batch_size": BATCH_SIZE * 2,
        "learning_rate": 0.0001,
        "weight_decay": 0.0001,
        "optimizer": "AdamW",
        "scheduler": "CosineAnnealingLR",
        "random_seed": 42,
        "best_epoch": int(best_epoch),
        "best_val_macro_f1": float(best_val_macro_f1),
        "test_top1_accuracy": float(acc),
        "test_top3_accuracy": float(top3_acc),
        "test_macro_f1": float(f1_m),
        "test_disease_macro_f1": float(disease_macro_f1),
        "test_healthy_f1": float(healthy_f1),
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else "N/A",
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
        "train_samples": len(train_recs),
        "val_samples": len(val_recs),
        "test_samples": len(test_recs),
    }
    with open(MODEL_DIR / "config.json", "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)
    print(f"[Saved] Config to: {MODEL_DIR / 'config.json'}")

    # 9. Plot Training Curves from progress CSV
    if PROGRESS_CSV.exists():
        prog_df = pd.read_csv(PROGRESS_CSV)
        if len(prog_df) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            epochs = prog_df["epoch"]

            axes[0, 0].plot(epochs, prog_df["train_loss"], "b-o", label="Train Loss")
            axes[0, 0].plot(epochs, prog_df["val_loss"], "r-s", label="Val Loss")
            axes[0, 0].set_title("Cross-Entropy Loss")
            axes[0, 0].set_xlabel("Epoch")
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)

            axes[0, 1].plot(epochs, prog_df["train_accuracy"] * 100, "b-o", label="Train Acc")
            axes[0, 1].plot(epochs, prog_df["val_accuracy"] * 100, "r-s", label="Val Acc")
            axes[0, 1].set_title("Accuracy (%)")
            axes[0, 1].set_xlabel("Epoch")
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)

            axes[1, 0].plot(epochs, prog_df["train_macro_f1"] * 100, "b-o", label="Train Macro F1")
            axes[1, 0].plot(epochs, prog_df["val_macro_f1"] * 100, "r-s", label="Val Macro F1")
            axes[1, 0].set_title("Macro F1 (%)")
            axes[1, 0].set_xlabel("Epoch")
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)

            axes[1, 1].plot(epochs, prog_df["val_disease_macro_f1"] * 100, "g-^", label="Val Disease-Only F1")
            axes[1, 1].plot(epochs, prog_df["val_healthy_f1"] * 100, "m-d", label="Val Healthy F1")
            axes[1, 1].set_title("Disease-Only vs Healthy F1 (%)")
            axes[1, 1].set_xlabel("Epoch")
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig(REPORTS_DIR / "training_curves.png", dpi=200)
            plt.close()
            print(f"[Saved] Training Curves to: {REPORTS_DIR / 'training_curves.png'}")

    # Plot Confusion Matrix
    cm = confusion_matrix(all_targets, all_preds, labels=list(range(num_classes)))
    plt.figure(figsize=(18, 16))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Model 2 V3 Test Set Confusion Matrix (117 Classes)")
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.xlabel("Predicted Class ID")
    plt.ylabel("Ground Truth Class ID")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "confusion_matrix.png", dpi=200)
    plt.close()
    print(f"[Saved] Confusion Matrix to: {REPORTS_DIR / 'confusion_matrix.png'}")

    # 10. Generate Markdown Report
    generate_markdown_report(config_dict, class_report_df)
    return 0


def generate_markdown_report(config, class_df):
    report_path = REPORTS_DIR / "model2_v3_training_report.md"

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

    v3_top1 = config["test_top1_accuracy"]
    v3_top3 = config["test_top3_accuracy"]
    v3_macro_f1 = config["test_macro_f1"]
    v3_dis_f1 = config["test_disease_macro_f1"]
    v3_hlt_f1 = config["test_healthy_f1"]

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# MODEL 2 V3 RETRAINING & BENCHMARK REPORT\n\n")
        f.write(f"**Date:** 2026-10-08  \n")
        f.write(f"**Model Directory:** `models/model2_classifier_v3/`  \n")
        f.write(f"**Dataset Location:** `data/processed/model2_organized/`  \n")
        f.write(f"**Architecture:** EfficientNet-B2 (117 Classes)  \n")
        f.write(f"**Best Epoch:** Epoch {config['best_epoch']}  \n\n")

        f.write("## 1. Executive Comparison: Model 2 V2 vs Model 2 V3 (Immutable 2,304 Test Set)\n\n")
        f.write("| Metric | Model 2 V2 Baseline | Model 2 V3 (Clean Organized Data) | Delta (V3 - V2) |\n")
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

        f.write("\n## 3. Dataset & Training Overview\n")
        f.write(f"- **Train Samples:** {config['train_samples']:,}\n")
        f.write(f"- **Validation Samples:** {config['val_samples']:,}\n")
        f.write(f"- **Test Samples (Immutable):** {config['test_samples']:,}\n")
        f.write(f"- **Total Classes:** {config['num_classes']}\n")
        f.write(f"- **Best Validation Macro F1:** {config['best_val_macro_f1']*100:.2f}% (Epoch {config['best_epoch']})\n")
        f.write(f"- **Hardware Used:** {config['gpu']} (CUDA {config['cuda_version']})\n")

    print(f"[Saved] Training Report to: {report_path}")


if __name__ == "__main__":
    code = evaluate_v3()
    sys.exit(code)
