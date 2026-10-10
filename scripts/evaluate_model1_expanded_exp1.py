"""EXP-1 Test Evaluation Script for Expanded Model 1 (46-Class EfficientNet-B2).

Evaluates the best EXP-1 checkpoint:
  models/model1_expanded/exp1/best_model_exp1.pth
on the immutable test split:
  data/processed/model1_expanded/test/ (1,586 images)

Outputs generated under reports/model1_expansion/exp1/:
  - exp1_test_evaluation_report.md
  - exp1_test_metrics.csv
  - exp1_per_class_metrics.csv
  - exp1_misclassifications.csv
  - exp1_confusion_matrix.json
  - exp1_test_evaluation.json
"""

from __future__ import annotations

import csv
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import EfficientNet_B2_Weights, efficientnet_b2

# ---------------------------------------------------------------------------
# Root and Paths
# ---------------------------------------------------------------------------
ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DATASET_DIR = ROOT / "data" / "processed" / "model1_expanded"
TEST_DIR = DATASET_DIR / "test"
MAPPING_PATH = ROOT / "data" / "processed" / "model1_expanded_class_mapping.json"
MANIFEST_PATH = ROOT / "data" / "processed" / "model1_expanded_manifest.csv"

EXP1_DIR = ROOT / "models" / "model1_expanded" / "exp1"
BEST_MODEL_PATH = EXP1_DIR / "best_model_exp1.pth"
SUMMARY_PATH = EXP1_DIR / "training_summary_exp1.json"

REPORTS_EXP1_DIR = ROOT / "reports" / "model1_expansion" / "exp1"
TEST_REPORT_MD = REPORTS_EXP1_DIR / "exp1_test_evaluation_report.md"
TEST_REPORT_JSON = REPORTS_EXP1_DIR / "exp1_test_evaluation.json"
TEST_METRICS_CSV = REPORTS_EXP1_DIR / "exp1_test_metrics.csv"
PER_CLASS_CSV = REPORTS_EXP1_DIR / "exp1_per_class_metrics.csv"
MISCLASS_CSV = REPORTS_EXP1_DIR / "exp1_misclassifications.csv"
CONFUSION_JSON = REPORTS_EXP1_DIR / "exp1_confusion_matrix.json"

IMAGE_SIZE = 224
BATCH_SIZE = 32
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

ORIGINAL_22_CLASSES = sorted([
    "anthurium", "blueberry", "broccoli", "bellpepper", "carnation", "cherry_tomato",
    "chrysanthemum", "cucumber", "french_bean", "geranium", "gerbera", "gypsophila",
    "lettuce", "lilium", "marigold", "melon", "orchid", "rose", "spinach",
    "strawberry", "tomato", "zucchini",
])

# EXP-0 Baseline audited metrics for direct comparison
EXP0_BASELINE = {
    "overall": {"top1": 0.9038, "top3": 0.9734, "macro_f1": 0.8381, "weighted_f1": 0.9029},
    "orig22": {"top1": 0.9553, "top3": 0.9828, "macro_f1_active": 0.9251, "weighted_f1": 0.9703},
    "new24": {"top1": 0.8402, "top3": 0.9618, "macro_f1": 0.8143, "weighted_f1": 0.8427},
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("EXP1Eval")


class BoundedExpandedPlantDataset(Dataset):
    VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    def __init__(self, split_dir: Path, sorted_classes: list[str], class_to_idx: dict[str, int], transform=None):
        self.split_dir = Path(split_dir)
        self.transform = transform
        self.samples: list[tuple[str, int]] = []
        for c in sorted_classes:
            c_dir = self.split_dir / c
            if c_dir.exists() and c_dir.is_dir():
                idx = class_to_idx[c]
                class_files = []
                for p in c_dir.iterdir():
                    if p.is_file() and p.suffix.lower() in self.VALID_EXTENSIONS:
                        class_files.append(p)
                for p in sorted(class_files, key=lambda x: x.name):
                    self.samples.append((str(p), idx))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int):
        path, target = self.samples[idx]
        with Image.open(path) as raw:
            try:
                raw.draft("RGB", (448, 448))
            except Exception:
                pass
            img = raw.convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, target, path


def evaluate():
    logger.info("=" * 80)
    logger.info("EXP-1 TEST EVALUATION — Two-Stage Transfer Learning Model")
    logger.info("=" * 80)

    # 1. Load taxonomy & mappings
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping = json.load(f)
    class_to_idx = mapping["class_to_idx"]
    idx_to_class = {int(k): v for k, v in mapping["idx_to_class"].items()}
    num_classes = len(class_to_idx)
    sorted_classes = [idx_to_class[i] for i in range(num_classes)]

    # 2. Check checkpoint existence
    if not BEST_MODEL_PATH.exists():
        raise FileNotFoundError(f"Best EXP-1 checkpoint missing: {BEST_MODEL_PATH}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Loading checkpoint: {BEST_MODEL_PATH} (device: {device})")
    checkpoint = torch.load(BEST_MODEL_PATH, map_location=device, weights_only=False)

    ckpt_epoch = checkpoint.get("epoch", "Unknown")
    ckpt_stage = checkpoint.get("stage", "Unknown")
    ckpt_val_macro = checkpoint.get("val_macro_f1_active", "Unknown")
    ckpt_val_acc = checkpoint.get("val_accuracy", "Unknown")
    logger.info(f"Checkpoint info: Global Epoch={ckpt_epoch}, Stage={ckpt_stage}, Val Macro F1={ckpt_val_macro}, Val Acc={ckpt_val_acc}")

    # Build and load model
    model = efficientnet_b2(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    # 3. Setup test dataset
    eval_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    test_dataset = BoundedExpandedPlantDataset(TEST_DIR, sorted_classes, class_to_idx, transform=eval_tf)
    logger.info(f"Test dataset loaded: {len(test_dataset)} images across {num_classes} classes")
    assert len(test_dataset) == 1586, f"Expected 1,586 test images, found {len(test_dataset)}"

    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    # 4. Inference
    t0 = time.time()
    targets_all = []
    preds_all = []
    probs_all = []
    paths_all = []

    logger.info("Running test inference...")
    with torch.no_grad():
        for images, targets, paths in test_loader:
            images = images.to(device, non_blocking=True)
            with torch.amp.autocast("cuda", enabled=(device.type == "cuda")):
                outputs = model(images)
                probs = torch.softmax(outputs, dim=1)

            _, preds = probs.max(1)
            targets_all.extend(targets.cpu().numpy())
            preds_all.extend(preds.cpu().numpy())
            probs_all.extend(probs.cpu().numpy())
            paths_all.extend(paths)

    eval_time = time.time() - t0
    logger.info(f"Inference complete in {eval_time:.2f}s ({len(test_dataset)/eval_time:.1f} img/s)")

    targets_np = np.array(targets_all)
    preds_np = np.array(preds_all)
    probs_np = np.array(probs_all)

    # Top-1 and Top-3 predictions
    top1_correct = (preds_np == targets_np)
    top3_indices = np.argsort(probs_np, axis=1)[:, -3:]
    top3_correct = np.array([targets_np[i] in top3_indices[i] for i in range(len(targets_np))])

    # Class subsets
    orig_indices = sorted(class_to_idx[c] for c in ORIGINAL_22_CLASSES if c in class_to_idx)
    new_indices = sorted(set(range(num_classes)) - set(orig_indices))

    orig_mask = np.isin(targets_np, orig_indices)
    new_mask = np.isin(targets_np, new_indices)

    # Active test classes
    test_class_counts = {i: int((targets_np == i).sum()) for i in range(num_classes)}
    active_test_indices = sorted(i for i, cnt in test_class_counts.items() if cnt > 0)
    gap_test_classes = [sorted_classes[i] for i in range(num_classes) if i not in active_test_indices]

    orig_active_indices = [i for i in orig_indices if test_class_counts[i] > 0]
    orig_zero_classes = [sorted_classes[i] for i in orig_indices if test_class_counts[i] == 0]

    # Compute metrics
    # A. Overall 46 classes
    overall_top1 = float(top1_correct.mean())
    overall_top3 = float(top3_correct.mean())
    overall_macro_f1_active = float(f1_score(targets_np, preds_np, labels=active_test_indices, average="macro", zero_division=0))
    overall_macro_f1_full = float(f1_score(targets_np, preds_np, labels=list(range(num_classes)), average="macro", zero_division=0))
    overall_weighted_f1 = float(f1_score(targets_np, preds_np, average="weighted", zero_division=0))

    # B. Original 22 classes
    orig_top1 = float(top1_correct[orig_mask].mean())
    orig_top3 = float(top3_correct[orig_mask].mean())
    orig_macro_f1_active = float(f1_score(targets_np[orig_mask], preds_np[orig_mask], labels=orig_active_indices, average="macro", zero_division=0))
    orig_macro_f1_full = float(f1_score(targets_np[orig_mask], preds_np[orig_mask], labels=orig_indices, average="macro", zero_division=0))
    orig_weighted_f1 = float(f1_score(targets_np[orig_mask], preds_np[orig_mask], labels=orig_indices, average="weighted", zero_division=0))

    # C. New 24 classes
    new_top1 = float(top1_correct[new_mask].mean())
    new_top3 = float(top3_correct[new_mask].mean())
    new_macro_f1 = float(f1_score(targets_np[new_mask], preds_np[new_mask], labels=new_indices, average="macro", zero_division=0))
    new_weighted_f1 = float(f1_score(targets_np[new_mask], preds_np[new_mask], labels=new_indices, average="weighted", zero_division=0))

    logger.info(f"Overall Top-1: {overall_top1*100:.2f}% | Top-3: {overall_top3*100:.2f}% | Macro F1 (active): {overall_macro_f1_active*100:.2f}%")
    logger.info(f"Orig-22 Top-1: {orig_top1*100:.2f}% | Top-3: {orig_top3*100:.2f}% | Macro F1 (active): {orig_macro_f1_active*100:.2f}%")
    logger.info(f"New-24  Top-1: {new_top1*100:.2f}% | Top-3: {new_top3*100:.2f}% | Macro F1: {new_macro_f1*100:.2f}%")

    # 5. Per-class metrics
    per_class_prec = precision_score(targets_np, preds_np, labels=list(range(num_classes)), average=None, zero_division=0)
    per_class_rec = recall_score(targets_np, preds_np, labels=list(range(num_classes)), average=None, zero_division=0)
    per_class_f1 = f1_score(targets_np, preds_np, labels=list(range(num_classes)), average=None, zero_division=0)

    per_class_records = []
    for i, c_name in enumerate(sorted_classes):
        sup = test_class_counts[i]
        subset = "ORIGINAL_22" if i in orig_indices else "NEW_24"
        per_class_records.append({
            "class_index": i,
            "class_name": c_name,
            "subset": subset,
            "test_support": sup,
            "precision": round(float(per_class_prec[i]), 4),
            "recall": round(float(per_class_rec[i]), 4),
            "f1_score": round(float(per_class_f1[i]), 4),
            "status": "Active" if sup > 0 else "Zero Support Gap",
        })

    # 6. Misclassification analysis
    misclass_records = []
    for idx, (is_correct, true_idx, pred_idx, path, probs) in enumerate(zip(top1_correct, targets_np, preds_np, paths_all, probs_np)):
        if not is_correct:
            rel_path = Path(path).relative_to(ROOT).as_posix()
            top3_idx = np.argsort(probs)[-3:][::-1]
            top3_str = ", ".join([f"{sorted_classes[k]}: {probs[k]*100:.1f}%" for k in top3_idx])
            misclass_records.append({
                "index": idx,
                "image_path": rel_path,
                "true_class": sorted_classes[true_idx],
                "predicted_class": sorted_classes[pred_idx],
                "confidence": round(float(probs[pred_idx]), 4),
                "top3_predictions": top3_str,
                "subset": "ORIGINAL_22" if true_idx in orig_indices else "NEW_24",
            })

    # 7. Confusion matrix
    cm = confusion_matrix(targets_np, preds_np, labels=list(range(num_classes)))
    cm_dict = {
        "classes": sorted_classes,
        "matrix": cm.tolist(),
    }

    # Top confusing pairs
    confusing_pairs = []
    for i in range(num_classes):
        for j in range(num_classes):
            if i != j and cm[i, j] > 0:
                confusing_pairs.append({
                    "true_class": sorted_classes[i],
                    "predicted_class": sorted_classes[j],
                    "count": int(cm[i, j]),
                    "true_support": int(test_class_counts[i]),
                    "subset_pair": f"{'Orig' if i in orig_indices else 'New'} -> {'Orig' if j in orig_indices else 'New'}",
                })
    confusing_pairs = sorted(confusing_pairs, key=lambda x: x["count"], reverse=True)

    # 8. Save CSV files
    # A. Test summary metrics CSV
    summary_rows = [
        {
            "subset": "OVERALL_46",
            "top1_accuracy": round(overall_top1, 4),
            "top3_accuracy": round(overall_top3, 4),
            "macro_f1_active": round(overall_macro_f1_active, 4),
            "macro_f1_full": round(overall_macro_f1_full, 4),
            "weighted_f1": round(overall_weighted_f1, 4),
            "test_images": len(test_dataset),
            "active_classes": len(active_test_indices),
            "zero_support_classes": len(gap_test_classes),
        },
        {
            "subset": "ORIGINAL_22",
            "top1_accuracy": round(orig_top1, 4),
            "top3_accuracy": round(orig_top3, 4),
            "macro_f1_active": round(orig_macro_f1_active, 4),
            "macro_f1_full": round(orig_macro_f1_full, 4),
            "weighted_f1": round(orig_weighted_f1, 4),
            "test_images": int(orig_mask.sum()),
            "active_classes": len(orig_active_indices),
            "zero_support_classes": len(orig_zero_classes),
        },
        {
            "subset": "NEW_24",
            "top1_accuracy": round(new_top1, 4),
            "top3_accuracy": round(new_top3, 4),
            "macro_f1_active": round(new_macro_f1, 4),
            "macro_f1_full": round(new_macro_f1, 4),
            "weighted_f1": round(new_weighted_f1, 4),
            "test_images": int(new_mask.sum()),
            "active_classes": len(new_indices),
            "zero_support_classes": 0,
        },
    ]

    with open(TEST_METRICS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    # B. Per class CSV
    with open(PER_CLASS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(per_class_records[0].keys()))
        writer.writeheader()
        writer.writerows(per_class_records)

    # C. Misclassifications CSV
    with open(MISCLASS_CSV, "w", newline="", encoding="utf-8") as f:
        if misclass_records:
            writer = csv.DictWriter(f, fieldnames=list(misclass_records[0].keys()))
            writer.writeheader()
            writer.writerows(misclass_records)

    # D. Confusion Matrix JSON
    with open(CONFUSION_JSON, "w", encoding="utf-8") as f:
        json.dump(cm_dict, f, indent=2)

    # E. Full evaluation JSON
    eval_json_data = {
        "experiment": "EXP-1",
        "evaluated_checkpoint": str(BEST_MODEL_PATH),
        "best_epoch_global": ckpt_epoch,
        "best_stage": ckpt_stage,
        "evaluation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_image_count": len(test_dataset),
        "active_classes_evaluated": len(active_test_indices),
        "zero_support_classes": gap_test_classes,
        "metrics": {
            "overall_46": {
                "top1_accuracy": round(overall_top1, 4),
                "top3_accuracy": round(overall_top3, 4),
                "macro_f1_active": round(overall_macro_f1_active, 4),
                "macro_f1_full": round(overall_macro_f1_full, 4),
                "weighted_f1": round(overall_weighted_f1, 4),
            },
            "original_22": {
                "top1_accuracy": round(orig_top1, 4),
                "top3_accuracy": round(orig_top3, 4),
                "macro_f1_active": round(orig_macro_f1_active, 4),
                "macro_f1_full": round(orig_macro_f1_full, 4),
                "weighted_f1": round(orig_weighted_f1, 4),
            },
            "new_24": {
                "top1_accuracy": round(new_top1, 4),
                "top3_accuracy": round(new_top3, 4),
                "macro_f1_active": round(new_macro_f1, 4),
                "weighted_f1": round(new_weighted_f1, 4),
            },
        },
        "comparison_vs_exp0": {
            "overall_top1_delta": round(overall_top1 - EXP0_BASELINE["overall"]["top1"], 4),
            "overall_macro_f1_delta": round(overall_macro_f1_active - EXP0_BASELINE["overall"]["macro_f1"], 4),
            "orig_top1_delta": round(orig_top1 - EXP0_BASELINE["orig22"]["top1"], 4),
            "orig_macro_f1_active_delta": round(orig_macro_f1_active - EXP0_BASELINE["orig22"]["macro_f1_active"], 4),
            "new_top1_delta": round(new_top1 - EXP0_BASELINE["new24"]["top1"], 4),
            "new_macro_f1_delta": round(new_macro_f1 - EXP0_BASELINE["new24"]["macro_f1"], 4),
        },
        "total_misclassifications": len(misclass_records),
    }

    with open(TEST_REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(eval_json_data, f, indent=2)

    # Update training_summary_exp1.json with test results
    if SUMMARY_PATH.exists():
        with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
            t_summary = json.load(f)
        t_summary["test_results"] = eval_json_data["metrics"]
        with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
            json.dump(t_summary, f, indent=2)

    # 9. Generate Markdown Report
    _write_markdown_report(
        overall_top1, overall_top3, overall_macro_f1_active, overall_macro_f1_full, overall_weighted_f1,
        orig_top1, orig_top3, orig_macro_f1_active, orig_macro_f1_full, orig_weighted_f1,
        new_top1, new_top3, new_macro_f1, new_weighted_f1,
        per_class_records, misclass_records, confusing_pairs, gap_test_classes,
        ckpt_epoch, ckpt_stage, eval_time, len(test_dataset)
    )

    logger.info(f"Test evaluation artifacts successfully saved to {REPORTS_EXP1_DIR}")
    return eval_json_data


def _write_markdown_report(
    overall_top1, overall_top3, overall_macro_f1_active, overall_macro_f1_full, overall_weighted_f1,
    orig_top1, orig_top3, orig_macro_f1_active, orig_macro_f1_full, orig_weighted_f1,
    new_top1, new_top3, new_macro_f1, new_weighted_f1,
    per_class_records, misclass_records, confusing_pairs, gap_test_classes,
    ckpt_epoch, ckpt_stage, eval_time, total_test_images
):
    def fmt_pct(val):
        return f"{val * 100:.2f}%"

    def fmt_delta(val):
        sign = "+" if val >= 0 else ""
        return f"{sign}{val * 100:.2f}%"

    md_lines = []
    md_lines.append("# EXP-1 Test Set Evaluation & Performance Audit")
    md_lines.append("")
    md_lines.append(f"> **Report Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}  ")
    md_lines.append(f"> **Project Root**: [`{ROOT}`](file:///{str(ROOT).replace(chr(92), '/')})  ")
    md_lines.append(f"> **Evaluated Checkpoint**: [`models/model1_expanded/exp1/best_model_exp1.pth`](file:///{str(BEST_MODEL_PATH).replace(chr(92), '/')}) (Global Epoch {ckpt_epoch}, Stage {ckpt_stage})  ")
    md_lines.append(f"> **Test Set**: Immutable 46-Class Test Split (**{total_test_images:,} images**) across 44 active classes  ")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 1. Executive Summary & Benchmark vs EXP-0 Baseline")
    md_lines.append("")
    md_lines.append("| Evaluation Subset | Metric | EXP-0 Baseline | EXP-1 Two-Stage | Delta | Verification Status |")
    md_lines.append("| :--- | :--- | :---: | :---: | :---: | :---: |")
    
    # Overall
    d_top1 = overall_top1 - EXP0_BASELINE["overall"]["top1"]
    d_top3 = overall_top3 - EXP0_BASELINE["overall"]["top3"]
    d_f1 = overall_macro_f1_active - EXP0_BASELINE["overall"]["macro_f1"]
    d_wf1 = overall_weighted_f1 - EXP0_BASELINE["overall"]["weighted_f1"]
    md_lines.append(f"| **Overall (46 Classes)** | Top-1 Accuracy | {fmt_pct(EXP0_BASELINE['overall']['top1'])} | **{fmt_pct(overall_top1)}** | {fmt_delta(d_top1)} | {'Improved' if d_top1 >= 0 else 'Regressed'} |")
    md_lines.append(f"| | Top-3 Accuracy | {fmt_pct(EXP0_BASELINE['overall']['top3'])} | **{fmt_pct(overall_top3)}** | {fmt_delta(d_top3)} | {'Improved' if d_top3 >= 0 else 'Regressed'} |")
    md_lines.append(f"| | Macro F1 (Active 44) | {fmt_pct(EXP0_BASELINE['overall']['macro_f1'])} | **{fmt_pct(overall_macro_f1_active)}** | {fmt_delta(d_f1)} | {'Improved' if d_f1 >= 0 else 'Regressed'} |")
    md_lines.append(f"| | Weighted F1 | {fmt_pct(EXP0_BASELINE['overall']['weighted_f1'])} | **{fmt_pct(overall_weighted_f1)}** | {fmt_delta(d_wf1)} | {'Improved' if d_wf1 >= 0 else 'Regressed'} |")
    
    # Original 22
    d_o_top1 = orig_top1 - EXP0_BASELINE["orig22"]["top1"]
    d_o_f1 = orig_macro_f1_active - EXP0_BASELINE["orig22"]["macro_f1_active"]
    d_o_wf1 = orig_weighted_f1 - EXP0_BASELINE["orig22"]["weighted_f1"]
    md_lines.append(f"| **Original 22 Crops** | Top-1 Accuracy | {fmt_pct(EXP0_BASELINE['orig22']['top1'])} | **{fmt_pct(orig_top1)}** | {fmt_delta(d_o_top1)} | {'Maintained' if d_o_top1 >= 0 else 'Regressed'} |")
    md_lines.append(f"| | Active Macro F1 (20) | {fmt_pct(EXP0_BASELINE['orig22']['macro_f1_active'])} | **{fmt_pct(orig_macro_f1_active)}** | {fmt_delta(d_o_f1)} | {'Maintained' if d_o_f1 >= 0 else 'Regressed'} |")
    md_lines.append(f"| | Weighted F1 | {fmt_pct(EXP0_BASELINE['orig22']['weighted_f1'])} | **{fmt_pct(orig_weighted_f1)}** | {fmt_delta(d_o_wf1)} | {'Maintained' if d_o_wf1 >= 0 else 'Regressed'} |")
    
    # New 24
    d_n_top1 = new_top1 - EXP0_BASELINE["new24"]["top1"]
    d_n_f1 = new_macro_f1 - EXP0_BASELINE["new24"]["macro_f1"]
    d_n_wf1 = new_weighted_f1 - EXP0_BASELINE["new24"]["weighted_f1"]
    md_lines.append(f"| **New 24 Crops** | Top-1 Accuracy | {fmt_pct(EXP0_BASELINE['new24']['top1'])} | **{fmt_pct(new_top1)}** | {fmt_delta(d_n_top1)} | {'Improved' if d_n_top1 >= 0 else 'Regressed'} |")
    md_lines.append(f"| | Macro F1 (24) | {fmt_pct(EXP0_BASELINE['new24']['macro_f1'])} | **{fmt_pct(new_macro_f1)}** | {fmt_delta(d_n_f1)} | {'Improved' if d_n_f1 >= 0 else 'Regressed'} |")
    md_lines.append(f"| | Weighted F1 | {fmt_pct(EXP0_BASELINE['new24']['weighted_f1'])} | **{fmt_pct(new_weighted_f1)}** | {fmt_delta(d_n_wf1)} | {'Improved' if d_n_wf1 >= 0 else 'Regressed'} |")
    
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 2. Evaluation Methodology & Integrity Notes")
    md_lines.append("")
    md_lines.append("1. **Label-Constrained Scikit-Learn Metric Calculation**:")
    md_lines.append("   - Active Macro F1 is computed by specifying `labels=active_test_indices` (`zero_division=0`).")
    md_lines.append("   - Subset Macro F1 for Original-22 and New-24 is evaluated strictly over the exact label indices belonging to that subset.")
    md_lines.append("2. **Zero-Support Gap Classes**:")
    md_lines.append(f"   - **{len(gap_test_classes)} gap classes** have zero samples in test split: `{gap_test_classes}`.")
    md_lines.append("   - Both classes have 0 samples across train, val, and test splits (known data gaps handled gracefully with loss weight 0.0).")
    md_lines.append("3. **Inference Performance**:")
    md_lines.append(f"   - Evaluated **{total_test_images:,} images** in **{eval_time:.2f}s** ({total_test_images/eval_time:.1f} images/sec) with PyTorch AMP FP16 and batch size 32.")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 3. Complete Per-Class Classification Report")
    md_lines.append("")
    md_lines.append("| Index | Canonical Class | Subset | Test Support | Precision | Recall | F1 Score | Status |")
    md_lines.append("| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    for r in per_class_records:
        p_str = fmt_pct(r["precision"]) if r["test_support"] > 0 else "-"
        r_str = fmt_pct(r["recall"]) if r["test_support"] > 0 else "-"
        f_str = fmt_pct(r["f1_score"]) if r["test_support"] > 0 else "-"
        status_badge = "✅" if r["f1_score"] >= 0.85 else ("⚠️" if r["f1_score"] >= 0.60 else ("❌" if r["test_support"] > 0 else "⚪ Zero Support"))
        md_lines.append(f"| {r['class_index']} | **{r['class_name']}** | {r['subset']} | {r['test_support']} | {p_str} | {r_str} | **{f_str}** | {status_badge} {r['status']} |")
    
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 4. Top Confusing Class Pairs")
    md_lines.append("")
    md_lines.append(f"Total test misclassifications: **{len(misclass_records)} / {total_test_images}** ({len(misclass_records)/total_test_images*100:.2f}% error rate).")
    md_lines.append("")
    md_lines.append("| True Class | Predicted Class | Error Count | True Class Support | Subset Transition |")
    md_lines.append("| :--- | :--- | :---: | :---: | :---: |")
    for p in confusing_pairs[:15]:
        md_lines.append(f"| **{p['true_class']}** | **{p['predicted_class']}** | **{p['count']}** | {p['true_support']} | {p['subset_pair']} |")
    
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 5. Machine-Readable Artifact Index")
    md_lines.append("")
    md_lines.append(f"- **Summary Metrics CSV**: [`reports/model1_expansion/exp1/exp1_test_metrics.csv`](file:///{str(TEST_METRICS_CSV).replace(chr(92), '/')})")
    md_lines.append(f"- **Per-Class Metrics CSV**: [`reports/model1_expansion/exp1/exp1_per_class_metrics.csv`](file:///{str(PER_CLASS_CSV).replace(chr(92), '/')})")
    md_lines.append(f"- **Misclassifications CSV**: [`reports/model1_expansion/exp1/exp1_misclassifications.csv`](file:///{str(MISCLASS_CSV).replace(chr(92), '/')})")
    md_lines.append(f"- **Confusion Matrix JSON**: [`reports/model1_expansion/exp1/exp1_confusion_matrix.json`](file:///{str(CONFUSION_JSON).replace(chr(92), '/')})")
    md_lines.append(f"- **Complete Evaluation JSON**: [`reports/model1_expansion/exp1/exp1_test_evaluation.json`](file:///{str(TEST_REPORT_JSON).replace(chr(92), '/')})")

    with open(TEST_REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))


if __name__ == "__main__":
    evaluate()
