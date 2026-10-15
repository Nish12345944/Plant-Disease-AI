"""
Evaluate Model 2 Retraining V2 on the Immutable 2,304-Image Protected Test Set (144 Classes)
============================================================================================
Implements the missing FINAL TEST EVALUATION for the deployed checkpoint
  models/model2_retraining_v2/best_model.pth
against the frozen benchmark declared in
  data/processed/model2_retraining_v2_manifest.csv  (split == 'test', 2,304 images)
  data/processed/model2_retraining_v2/test/...

Preprocessing and class-index mapping match production inference exactly
(models/model2_classifier_v4/predict.py served with the retraining_v2 mapping):
  PIL open -> RGB -> Resize((260, 260)) -> ToTensor -> Normalize(ImageNet mean/std)
  EfficientNet-B2(weights=None) + Dropout(0.3) + Linear(1024->144), strict state_dict load.

All 144 classes are reported (including zero/low-support classes); every test image
is evaluated and every failed prediction is recorded - nothing is excluded.

Outputs (reports/model2_retraining_v2/final_test_evaluation/):
  evaluation_summary.json, test_classification_report.csv, test_predictions.csv,
  confusion_matrix.csv, confusion_matrix.png, top_misclassifications.csv,
  final_test_evaluation_report.md

READ-ONLY over the test set, checkpoint, and mappings. No retraining, no threshold
or mapping changes, no deployment. If any prerequisite is inconsistent, the script
STOPS with an explicit error instead of substituting another dataset.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
    top_k_accuracy_score,
)
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import efficientnet_b2

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Deployed artifacts under audit (read-only)
CHECKPOINT_PATH = PROJECT_ROOT / "models" / "model2_retraining_v2" / "best_model.pth"
CLASS_MAPPING_PATH = PROJECT_ROOT / "models" / "model2_retraining_v2" / "class_mapping.json"
CROP_DISEASE_MAP_PATH = PROJECT_ROOT / "models" / "model2_retraining_v2" / "crop_disease_mapping.json"

# Immutable benchmark
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v2_manifest.csv"
DATASET_DIR = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v2"
DATASET_MAPPING_PATH = DATASET_DIR / "class_mapping.json"

# Training-time validation reference (validation split - NOT test)
VAL_PROGRESS_CSV = PROJECT_ROOT / "reports" / "model2_retraining_v2" / "training_progress.csv"

OUTPUT_DIR = PROJECT_ROOT / "reports" / "model2_retraining_v2" / "final_test_evaluation"

EXPECTED_TEST_COUNT = 2304
EXPECTED_NUM_CLASSES = 144

# Production inference constants (verbatim from models/model2_classifier_v4/predict.py)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
DEFAULT_IMAGE_SIZE = (260, 260)

LOW_SUPPORT_THRESHOLD = 10  # per-class test support below this is flagged in the report

def verify_class_mapping(mapping_path: Path) -> Tuple[Dict[str, int], Dict[int, str]]:
    """Load the deployed class mapping and verify 144-class taxonomy integrity."""
    if not mapping_path.exists():
        raise FileNotFoundError(f"Class mapping file not found at: {mapping_path}")

    with open(mapping_path, "r", encoding="utf-8") as f:
        class_to_id = json.load(f)

    if len(class_to_id) != EXPECTED_NUM_CLASSES:
        raise ValueError(
            f"Class mapping size mismatch! Expected {EXPECTED_NUM_CLASSES} classes, "
            f"but found {len(class_to_id)} in {mapping_path}"
        )

    id_to_class = {int(v): k for k, v in class_to_id.items()}
    if len(id_to_class) != EXPECTED_NUM_CLASSES:
        raise ValueError("Class mapping contains duplicate or non-invertible class indices!")

    if set(id_to_class.keys()) != set(range(EXPECTED_NUM_CLASSES)):
        raise ValueError("Class mapping indices are not continuous 0..143!")

    if class_to_id.get("healthy") != 0:
        raise ValueError(f"'healthy' must map to class 0, found {class_to_id.get('healthy')}")

    return class_to_id, id_to_class


def verify_dataset_mapping_consistency(class_to_id: Dict[str, int]) -> None:
    """The dataset-dir copy of class_mapping.json must match the deployed copy."""
    if not DATASET_MAPPING_PATH.exists():
        raise FileNotFoundError(f"Dataset class mapping not found at: {DATASET_MAPPING_PATH}")
    with open(DATASET_MAPPING_PATH, "r", encoding="utf-8") as f:
        dataset_map = json.load(f)
    if dataset_map != class_to_id:
        only_deployed = sorted(set(class_to_id) - set(dataset_map))
        only_dataset = sorted(set(dataset_map) - set(class_to_id))
        diff_ids = sorted(
            k for k in set(class_to_id) & set(dataset_map) if class_to_id[k] != dataset_map[k]
        )
        raise ValueError(
            "Deployed mapping and dataset mapping disagree! "
            f"only_in_deployed={only_deployed[:5]}, only_in_dataset={only_dataset[:5]}, "
            f"id_mismatches={diff_ids[:5]}"
        )


def verify_test_manifest(
    manifest_path: Path, dataset_dir: Path, class_to_id: Dict[str, int]
) -> List[Dict[str, str]]:
    """Load the immutable 2,304-image test split and verify taxonomy + files on disk."""
    if not manifest_path.exists():
        raise FileNotFoundError(f"Dataset manifest not found at: {manifest_path}")

    test_records: List[Dict[str, str]] = []
    with open(manifest_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("split") == "test":
                test_records.append(row)

    if len(test_records) != EXPECTED_TEST_COUNT:
        raise ValueError(
            f"Test set count mismatch! Expected exactly {EXPECTED_TEST_COUNT} test images, "
            f"but found {len(test_records)} in {manifest_path}. Refusing to substitute another dataset."
        )

    missing_files: List[str] = []
    invalid_classes: List[Tuple[str, int, Any]] = []
    for row in test_records:
        img_rel = row["image_path"]
        class_id = int(row["class_id"])
        canonical_class = row["canonical_class"]

        if not (dataset_dir / img_rel).exists():
            missing_files.append(img_rel)
        if class_to_id.get(canonical_class) != class_id:
            invalid_classes.append((canonical_class, class_id, class_to_id.get(canonical_class)))

    if missing_files:
        raise FileNotFoundError(
            f"{len(missing_files)} test images not found under {dataset_dir}. "
            f"First missing samples: {missing_files[:5]}"
        )
    if invalid_classes:
        raise ValueError(
            f"{len(invalid_classes)} test records have class_id inconsistent with the deployed "
            f"144-class mapping. First invalid samples: {invalid_classes[:5]}"
        )

    return test_records


def verify_checkpoint(checkpoint_path: Path) -> Dict[str, Any]:
    """Load the deployed checkpoint; verify it is the 144-class v2 model (read-only)."""
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found at: {checkpoint_path}")

    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    if not isinstance(ckpt, dict) or "model_state_dict" not in ckpt:
        raise ValueError(f"Unexpected checkpoint format at {checkpoint_path} (missing 'model_state_dict')")

    state = ckpt["model_state_dict"]
    head_weight = state.get("classifier.1.weight")
    if head_weight is None or tuple(head_weight.shape) != (EXPECTED_NUM_CLASSES, 1408):
        raise ValueError(
            f"Checkpoint classifier head is {None if head_weight is None else tuple(head_weight.shape)}; "
            f"expected ({EXPECTED_NUM_CLASSES}, 1408). Wrong checkpoint for the 144-class taxonomy."
        )

    if ckpt.get("num_classes") != EXPECTED_NUM_CLASSES:
        raise ValueError(
            f"Checkpoint num_classes={ckpt.get('num_classes')} != {EXPECTED_NUM_CLASSES}"
        )

    return ckpt

# ---------------------------------------------------------------------------
# Production-identical preprocessing & model
# ---------------------------------------------------------------------------
def get_production_transform() -> transforms.Compose:
    """Exactly the val/test transform of training and the transform of production
    inference (models/model2_classifier_v4/predict.py _get_transform)."""
    return transforms.Compose([
        transforms.Resize(DEFAULT_IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


class Model2TestDataset(Dataset):
    """Manifest-driven test dataset with graceful decode fallback (never drops samples)."""

    def __init__(self, records: List[Dict[str, str]], base_dir: Path, transform=None):
        self.records = records
        self.base_dir = Path(base_dir)
        self.transform = transform
        self.decode_failures: List[str] = []  # paths that fell back to gray placeholder

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, idx: int):
        rec = self.records[idx]
        img_path = self.base_dir / rec["image_path"]
        try:
            with Image.open(img_path) as raw:
                img = raw.convert("RGB")
        except Exception:
            self.decode_failures.append(rec["image_path"])
            img = Image.new("RGB", DEFAULT_IMAGE_SIZE, (128, 128, 128))
        if self.transform:
            img = self.transform(img)
        return img, int(rec["class_id"]), idx


def build_model(num_classes: int, checkpoint_state: Dict[str, torch.Tensor]) -> nn.Module:
    """EfficientNet-B2 exactly as production (predict.py _load_model), strict weights load."""
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes),
    )
    # strict=True raises on any missing/unexpected key: guarantees the checkpoint
    # matches this exact architecture (same contract as production predict.py)
    model.load_state_dict(checkpoint_state, strict=True)
    model.eval()
    return model


@torch.inference_mode()
def run_inference(
    model: nn.Module, loader: DataLoader, device: torch.device
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Forward every test image exactly once; returns preds, targets, probs, mean CE loss."""
    criterion = nn.CrossEntropyLoss(reduction="sum")
    all_preds: List[int] = []
    all_targets: List[int] = []
    all_probs: List[np.ndarray] = []
    total_loss = 0.0

    for images, labels, indices in loader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)
        outputs = model(images)
        loss = criterion(outputs, labels)
        total_loss += loss.item()
        probs = torch.softmax(outputs, dim=1)
        preds = torch.argmax(probs, dim=1)
        all_preds.extend(preds.cpu().tolist())
        all_targets.extend(labels.cpu().tolist())
        all_probs.extend(probs.cpu().numpy())
        del outputs, loss, probs, preds, images, labels

    n = len(all_targets)
    return (
        np.array(all_preds),
        np.array(all_targets),
        np.array(all_probs),
        total_loss / n,
    )


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def compute_metrics(
    preds: np.ndarray, targets: np.ndarray, probs: np.ndarray, num_classes: int
) -> Dict[str, Any]:
    """All requested metrics over the FULL label space (low-support classes included)."""
    label_space = list(range(num_classes))

    acc = accuracy_score(targets, preds)
    top3 = top_k_accuracy_score(targets, probs, k=min(3, num_classes), labels=label_space)

    prec_m, rec_m, f1_m, _ = precision_recall_fscore_support(
        targets, preds, average="macro", zero_division=0
    )
    prec_w, rec_w, f1_w, _ = precision_recall_fscore_support(
        targets, preds, average="weighted", zero_division=0
    )

    prec_c, rec_c, f1_c, sup_c = precision_recall_fscore_support(
        targets, preds, average=None, labels=label_space, zero_division=0
    )

    # Healthy class (id 0): precision/recall/F1
    healthy = {"precision": float(prec_c[0]), "recall": float(rec_c[0]), "f1": float(f1_c[0]),
               "support": int(sup_c[0])}

    # Disease-only macro F1 (classes 1..143)
    disease_f1s = f1_c[1:]
    disease_macro_f1 = float(np.mean(disease_f1s)) if len(disease_f1s) > 0 else 0.0

    cm = confusion_matrix(targets, preds, labels=label_space)

    return {
        "accuracy_top1": float(acc),
        "accuracy_top3": float(top3),
        "macro_precision": float(prec_m),
        "macro_recall": float(rec_m),
        "macro_f1": float(f1_m),
        "weighted_precision": float(prec_w),
        "weighted_recall": float(rec_w),
        "weighted_f1": float(f1_w),
        "healthy": healthy,
        "disease_macro_f1": disease_macro_f1,
        "per_class_precision": prec_c,
        "per_class_recall": rec_c,
        "per_class_f1": f1_c,
        "per_class_support": sup_c,
        "confusion_matrix": cm,
    }


def top_confusions(cm: np.ndarray, id_to_class: Dict[int, str], k: int = 25):
    """Most frequent (actual -> predicted) misclassification pairs."""
    pairs = []
    n = cm.shape[0]
    for i in range(n):
        for j in range(n):
            if i != j and cm[i][j] > 0:
                pairs.append((id_to_class[i], id_to_class[j], int(cm[i][j])))
    pairs.sort(key=lambda x: (-x[2], x[0], x[1]))
    return pairs[:k], pairs


# ---------------------------------------------------------------------------
# Artifact writers
# ---------------------------------------------------------------------------
def save_per_class_report(output_dir: Path, id_to_class: Dict[int, str], m: Dict[str, Any]):
    """Per-class P/R/F1/support for ALL 144 classes (zero/low support included, flagged)."""
    with open(output_dir / "test_classification_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["class_id", "canonical_class", "crop", "disease",
                         "precision", "recall", "f1_score", "support", "low_support"])
        for c in range(EXPECTED_NUM_CLASSES):
            name = id_to_class[c]
            crop_part, _, disease_part = name.partition("__")
            if not disease_part:
                crop_part, disease_part = "all_crops", name
            support = int(m["per_class_support"][c])
            writer.writerow([
                c, name, crop_part, disease_part,
                f"{m['per_class_precision'][c]:.4f}",
                f"{m['per_class_recall'][c]:.4f}",
                f"{m['per_class_f1'][c]:.4f}",
                support,
                "yes" if support < LOW_SUPPORT_THRESHOLD else "no",
            ])


def save_predictions(output_dir: Path, records: List[Dict[str, str]],
                     id_to_class: Dict[int, str], preds: np.ndarray, targets: np.ndarray,
                     probs: np.ndarray):
    """Every test image with its prediction - including all failed predictions."""
    with open(output_dir / "test_predictions.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image_path", "true_class", "true_id", "pred_class", "pred_id",
                         "confidence", "top3_classes", "top3_probs", "correct"])
        for idx, rec in enumerate(records):
            p = int(preds[idx])
            t = int(targets[idx])
            top3_idx = np.argsort(probs[idx])[::-1][:3]
            top3_names = "|".join(id_to_class[int(i)] for i in top3_idx)
            top3_ps = "|".join(f"{probs[idx][i]:.4f}" for i in top3_idx)
            writer.writerow([
                rec["image_path"], id_to_class[t], t, id_to_class[p], p,
                f"{probs[idx][p]:.4f}", top3_names, top3_ps, int(p == t),
            ])


def save_confusion(output_dir: Path, id_to_class: Dict[int, str], cm: np.ndarray):
    with open(output_dir / "confusion_matrix.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["actual\\predicted"] + [id_to_class[c] for c in range(EXPECTED_NUM_CLASSES)])
        for i in range(EXPECTED_NUM_CLASSES):
            writer.writerow([id_to_class[i]] + [int(v) for v in cm[i]])

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(16, 14))
        im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
        ax.set_title("Model 2 Retraining V2 - Test Confusion Matrix (144 classes, 2,304 images)")
        fig.colorbar(im, ax=ax, fraction=0.02, pad=0.02)
        fig.tight_layout()
        fig.savefig(output_dir / "confusion_matrix.png", dpi=120)
        plt.close(fig)
    except Exception as exc:
        print(f"[warn] confusion_matrix.png not written: {exc}", flush=True)


def save_top_misclassifications(output_dir: Path, top_pairs, all_pairs):
    with open(output_dir / "top_misclassifications.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "actual_class", "predicted_class", "count"])
        for rank, (a, p, c) in enumerate(top_pairs, 1):
            writer.writerow([rank, a, p, c])
    with open(output_dir / "all_misclassification_pairs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["actual_class", "predicted_class", "count"])
        for a, p, c in all_pairs:
            writer.writerow([a, p, c])

# ---------------------------------------------------------------------------
# Validation reference (validation split - clearly distinguished from test)
# ---------------------------------------------------------------------------
def load_validation_reference() -> Dict[str, Any]:
    """Best-epoch VALIDATION metrics from training_progress.csv (n=3,049 val images).
    Validation data was seen during training/model selection; the test split was not."""
    if not VAL_PROGRESS_CSV.exists():
        return {}
    with open(VAL_PROGRESS_CSV, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return {}
    best = max(rows, key=lambda r: float(r["val_macro_f1"]))
    return {
        "source": str(VAL_PROGRESS_CSV),
        "note": "VALIDATION split (3,049 images, used for model selection) - NOT the test split",
        "best_epoch": int(best["epoch"]),
        "val_loss": float(best["val_loss"]),
        "val_top1_accuracy": float(best["val_acc"]),
        "val_top3_accuracy": float(best["val_top3_acc"]),
        "val_macro_f1": float(best["val_macro_f1"]),
        "val_weighted_f1": float(best["val_weighted_f1"]),
        "val_healthy_f1": float(best["val_healthy_f1"]),
        "val_disease_macro_f1": float(best["val_disease_macro_f1"]),
    }


def save_summary_json(output_dir: Path, ckpt: Dict[str, Any], test_loss: float,
                      m: Dict[str, Any], top_pairs, decode_failures: List[str],
                      val_ref: Dict[str, Any], elapsed: float, device: torch.device):
    per_class_list = []
    for c in range(EXPECTED_NUM_CLASSES):
        per_class_list.append({
            "class_id": c,
            "precision": round(float(m["per_class_precision"][c]), 4),
            "recall": round(float(m["per_class_recall"][c]), 4),
            "f1_score": round(float(m["per_class_f1"][c]), 4),
            "support": int(m["per_class_support"][c]),
        })

    summary = {
        "evaluation_type": "FINAL TEST EVALUATION (immutable protected test split)",
        "evaluation_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "checkpoint_evaluated": str(CHECKPOINT_PATH),
        "checkpoint_saved_epoch": ckpt.get("epoch"),
        "checkpoint_num_classes": ckpt.get("num_classes"),
        "class_mapping": str(CLASS_MAPPING_PATH),
        "dataset_manifest": str(MANIFEST_PATH),
        "dataset_dir": str(DATASET_DIR),
        "test_images_count": EXPECTED_TEST_COUNT,
        "preprocessing": {
            "resize": list(DEFAULT_IMAGE_SIZE),
            "normalize_mean": IMAGENET_MEAN,
            "normalize_std": IMAGENET_STD,
            "note": "identical to production inference (models/model2_classifier_v4/predict.py)",
        },
        "execution_device": str(device),
        "evaluation_duration_seconds": round(elapsed, 2),
        "decode_failures": decode_failures,
        "metrics": {
            "test_loss": round(test_loss, 4),
            "top1_accuracy": round(m["accuracy_top1"], 4),
            "top3_accuracy": round(m["accuracy_top3"], 4),
            "macro_precision": round(m["macro_precision"], 4),
            "macro_recall": round(m["macro_recall"], 4),
            "macro_f1": round(m["macro_f1"], 4),
            "weighted_f1": round(m["weighted_f1"], 4),
            "healthy_precision": round(m["healthy"]["precision"], 4),
            "healthy_recall": round(m["healthy"]["recall"], 4),
            "healthy_f1": round(m["healthy"]["f1"], 4),
            "healthy_support": m["healthy"]["support"],
            "disease_macro_f1": round(m["disease_macro_f1"], 4),
        },
        "validation_reference": val_ref,
        "top_misclassifications": [
            {"actual": a, "predicted": p, "count": c} for a, p, c in top_pairs
        ],
        "per_class_metrics": per_class_list,
        "artifacts_generated": {
            "summary_json": str(output_dir / "evaluation_summary.json"),
            "classification_report_csv": str(output_dir / "test_classification_report.csv"),
            "predictions_csv": str(output_dir / "test_predictions.csv"),
            "confusion_matrix_csv": str(output_dir / "confusion_matrix.csv"),
            "confusion_matrix_png": str(output_dir / "confusion_matrix.png"),
            "top_misclassifications_csv": str(output_dir / "top_misclassifications.csv"),
            "all_misclassification_pairs_csv": str(output_dir / "all_misclassification_pairs.csv"),
            "markdown_report": str(output_dir / "final_test_evaluation_report.md"),
        },
    }
    with open(output_dir / "evaluation_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary

# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------
def save_markdown_report(output_dir: Path, ckpt: Dict[str, Any], test_loss: float,
                         m: Dict[str, Any], top_pairs, all_pairs, val_ref: Dict[str, Any],
                         elapsed: float, device: torch.device, id_to_class: Dict[int, str],
                         correct_count: int):
    lines: List[str] = []
    a = lines.append
    a("# Model 2 Retraining V2 - FINAL TEST EVALUATION (Immutable Protected Benchmark)")
    a("")
    a(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    a(f"**Checkpoint:** `models/model2_retraining_v2/best_model.pth` (saved at epoch {ckpt.get('epoch')})  ")
    a("**Test set:** 2,304 images (`data/processed/model2_retraining_v2_manifest.csv`, split == 'test')  ")
    a(f"**Taxonomy:** {EXPECTED_NUM_CLASSES} classes (`healthy` + 143 diseases)  ")
    a("**Preprocessing:** Resize(260x260) -> ToTensor -> Normalize(ImageNet) - identical to production `predict.py`  ")
    a(f"**Device:** {device} | **Duration:** {elapsed:.1f}s")
    a("")
    a("## 1. Prerequisite Verification (all PASSED)")
    a("")
    a(f"- Checkpoint classifier head = ({EXPECTED_NUM_CLASSES}, 1408) - matches deployed taxonomy (strict state-dict load)")
    a(f"- Checkpoint `num_classes` field = {ckpt.get('num_classes')} - matches mapping")
    a("- Deployed `models/model2_retraining_v2/class_mapping.json` byte-identical to dataset-dir copy (144 continuous ids, healthy=0)")
    a(f"- Manifest contains exactly {EXPECTED_TEST_COUNT} test rows; every image exists on disk; every `class_id` consistent with the mapping")
    a("- No dataset substitution, no retraining, no threshold or mapping changes")
    embedded = ckpt.get("class_mapping")
    if isinstance(embedded, dict):
        matches = embedded == json.loads(CLASS_MAPPING_PATH.read_text(encoding="utf-8"))
        a(f"- Checkpoint-embedded class mapping matches the deployed mapping file: **{matches}**")
    a("")
    a("## 2. Aggregate Test Metrics (n = 2,304, ALL samples included)")
    a("")
    a("| Metric | Value |")
    a("|---|---|")
    a(f"| Test loss (CE) | {test_loss:.4f} |")
    a(f"| Top-1 accuracy | {m['accuracy_top1']*100:.2f}% ({correct_count} / {EXPECTED_TEST_COUNT}) |")
    a(f"| Top-3 accuracy | {m['accuracy_top3']*100:.2f}% |")
    a(f"| Macro F1 (144 classes) | {m['macro_f1']*100:.2f}% |")
    a(f"| Weighted F1 | {m['weighted_f1']*100:.2f}% |")
    a(f"| Disease-only macro F1 (classes 1-143) | {m['disease_macro_f1']*100:.2f}% |")
    a(f"| Healthy precision (class 0, n={m['healthy']['support']}) | {m['healthy']['precision']*100:.2f}% |")
    a(f"| Healthy recall (class 0) | {m['healthy']['recall']*100:.2f}% |")
    a(f"| Healthy F1 (class 0) | {m['healthy']['f1']*100:.2f}% |")
    a("")
    a("## 3. TEST vs VALIDATION (clearly distinguished)")
    a("")
    a("| Metric | Validation (best epoch, n=3,049) | TEST (this report, n=2,304) | Delta |")
    a("|---|---|---|---|")
    if val_ref:
        pairs = [
            ("Top-1 accuracy", val_ref["val_top1_accuracy"], m["accuracy_top1"]),
            ("Top-3 accuracy", val_ref["val_top3_accuracy"], m["accuracy_top3"]),
            ("Macro F1", val_ref["val_macro_f1"], m["macro_f1"]),
            ("Weighted F1", val_ref["val_weighted_f1"], m["weighted_f1"]),
            ("Healthy F1", val_ref["val_healthy_f1"], m["healthy"]["f1"]),
            ("Disease-only macro F1", val_ref["val_disease_macro_f1"], m["disease_macro_f1"]),
        ]
        for name, v, t in pairs:
            a(f"| {name} | {v*100:.2f}% | {t*100:.2f}% | {(t-v)*100:+.2f} pts |")
        a("")
        a(f"Validation numbers come from `{val_ref['source']}` (best epoch {val_ref['best_epoch']} by val macro F1). "
          "Validation images guided model selection and are therefore optimistic; the test split was never seen "
          "during training or checkpoint selection.")
    else:
        a("| (validation reference unavailable) | - | - | - |")
    a("")
    a("## 4. Most Frequent Misclassifications (Top 25)")
    a("")
    a("| Rank | Actual | Predicted | Count |")
    a("|---|---|---|---|")
    for rank, (actual, pred, count) in enumerate(top_pairs, 1):
        a(f"| {rank} | {actual} | {pred} | {count} |")
    a("")
    a(f"Full pair list: `all_misclassification_pairs.csv` ({len(all_pairs)} distinct error pairs).")
    a("")
    a("## 5. Low-Support & Zero-Support Classes (NOT excluded)")
    a("")
    sup = m["per_class_support"]
    zero_sup = [c for c in range(EXPECTED_NUM_CLASSES) if int(sup[c]) == 0]
    low_sup = [c for c in range(EXPECTED_NUM_CLASSES) if 0 < int(sup[c]) < LOW_SUPPORT_THRESHOLD]
    a(f"- Zero-support classes in the test split: **{len(zero_sup)}**"
      + (f" - {', '.join(id_to_class[c] for c in zero_sup)}" if zero_sup else ""))
    a(f"- Low-support classes (1-{LOW_SUPPORT_THRESHOLD - 1} images): **{len(low_sup)}**"
      + (" - " + ", ".join(f"{id_to_class[c]} (n={int(sup[c])})" for c in low_sup) if low_sup else ""))
    a("- All classes remain in macro F1 and in the per-class report; low-support rows are flagged "
      "in the `low_support` column of `test_classification_report.csv`.")
    a("")
    a("## 6. Artifacts")
    a("")
    a("- `evaluation_summary.json` - machine-readable summary incl. all per-class metrics")
    a("- `test_classification_report.csv` - per-class precision/recall/F1/support for all 144 classes")
    a("- `test_predictions.csv` - every one of the 2,304 predictions incl. failures (correct flag + top-3)")
    a("- `confusion_matrix.csv` / `confusion_matrix.png` - 144x144 test confusion matrix")
    a("- `top_misclassifications.csv` / `all_misclassification_pairs.csv` - error analysis")
    a("")
    a("## 7. Follow-Up for the Reliability Audit")
    a("")
    a("This evaluation supplies the per-class disease evidence recorded as MISSING in "
      "`reports/crop_disease_reliability_audit/reliability_audit.md` (all 143 disease rows carried "
      "`NOT_EVALUATED` disease metrics). The audit was not modified by this run; re-running its "
      "generator would now be able to apply the disease gate on real test metrics.")
    a("")

    (output_dir / "final_test_evaluation_report.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="FINAL TEST EVALUATION of Model 2 Retraining V2 (144 classes) on the immutable 2,304-image benchmark"
    )
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--num-workers", type=int, default=0,
                        help="DataLoader workers (0 = safe on Windows)")
    parser.add_argument("--device", type=str, default=None,
                        help="Target device ('cuda', 'cpu'). Auto-detected if omitted.")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    start_time = time.time()

    # torch thread tuning mirrors app/backend/config.py for CPU runs
    if not torch.cuda.is_available():
        torch.set_num_threads(min(4, max(1, torch.get_num_threads())))

    print("=" * 90, flush=True)
    print("MODEL 2 RETRAINING V2 - FINAL TEST EVALUATION (immutable protected benchmark)", flush=True)
    print("=" * 90, flush=True)

    # 1. Prerequisite verification - STOP on any inconsistency (no dataset substitution)
    print("[1/5] Verifying prerequisites...", flush=True)
    class_to_id, id_to_class = verify_class_mapping(CLASS_MAPPING_PATH)
    verify_dataset_mapping_consistency(class_to_id)
    test_records = verify_test_manifest(MANIFEST_PATH, DATASET_DIR, class_to_id)
    ckpt = verify_checkpoint(CHECKPOINT_PATH)
    print(f"      OK: {len(class_to_id)}-class taxonomy; {len(test_records)} test images; "
          f"checkpoint epoch {ckpt.get('epoch')}", flush=True)

    if args.device:
        device = torch.device(args.device)
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"      Device: {device}", flush=True)

    # 2. Build production-identical model
    print("[2/5] Loading deployed checkpoint (production architecture)...", flush=True)
    model = build_model(EXPECTED_NUM_CLASSES, ckpt["model_state_dict"])
    model.to(device)

    # 3. Run inference over ALL 2,304 test images
    print(f"[3/5] Running inference on {len(test_records)} test images...", flush=True)
    dataset = Model2TestDataset(test_records, DATASET_DIR, transform=get_production_transform())
    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=(device.type == "cuda"),
    )
    preds, targets, probs, test_loss = run_inference(model, loader, device)
    decode_failures = list(dataset.decode_failures)
    if decode_failures:
        print(f"      [warn] {len(decode_failures)} images failed to decode and were evaluated as "
              f"gray placeholders (never dropped): {decode_failures[:5]}", flush=True)

    # 4. Metrics over the FULL label space
    print("[4/5] Computing metrics (full 144-class label space, low-support included)...", flush=True)
    m = compute_metrics(preds, targets, probs, EXPECTED_NUM_CLASSES)
    correct_count = int((preds == targets).sum())
    top_pairs, all_pairs = top_confusions(m["confusion_matrix"], id_to_class, k=25)
    val_ref = load_validation_reference()
    elapsed = time.time() - start_time

    print("\n" + "=" * 90, flush=True)
    print("TEST BENCHMARK RESULTS (n = 2,304)", flush=True)
    print("=" * 90, flush=True)
    print(f"Test loss (CE)                : {test_loss:.4f}", flush=True)
    print(f"Top-1 accuracy                : {m['accuracy_top1'] * 100:.2f}% ({correct_count} / {EXPECTED_TEST_COUNT})", flush=True)
    print(f"Top-3 accuracy                : {m['accuracy_top3'] * 100:.2f}%", flush=True)
    print(f"Macro F1 (144 classes)        : {m['macro_f1'] * 100:.2f}%", flush=True)
    print(f"Weighted F1                   : {m['weighted_f1'] * 100:.2f}%", flush=True)
    print(f"Disease-only macro F1 (1-143) : {m['disease_macro_f1'] * 100:.2f}%", flush=True)
    print(f"Healthy P/R/F1 (class 0)      : {m['healthy']['precision'] * 100:.2f}% / "
          f"{m['healthy']['recall'] * 100:.2f}% / {m['healthy']['f1'] * 100:.2f}% "
          f"(n={m['healthy']['support']})", flush=True)
    print("=" * 90, flush=True)
    if val_ref:
        print(f"VALIDATION reference (best epoch {val_ref['best_epoch']}, n=3,049 - NOT test): "
              f"top1={val_ref['val_top1_accuracy'] * 100:.2f}%, macroF1={val_ref['val_macro_f1'] * 100:.2f}%, "
              f"disMacroF1={val_ref['val_disease_macro_f1'] * 100:.2f}%", flush=True)

    # 5. Save artifacts
    print("[5/5] Saving artifacts...", flush=True)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    save_per_class_report(output_dir, id_to_class, m)
    save_predictions(output_dir, test_records, id_to_class, preds, targets, probs)
    save_confusion(output_dir, id_to_class, m["confusion_matrix"])
    save_top_misclassifications(output_dir, top_pairs, all_pairs)
    save_summary_json(output_dir, ckpt, test_loss, m, top_pairs, decode_failures,
                      val_ref, elapsed, device)
    save_markdown_report(output_dir, ckpt, test_loss, m, top_pairs, all_pairs, val_ref,
                         elapsed, device, id_to_class, correct_count)

    print(f"\nAll artifacts written to: {output_dir}", flush=True)
    for name in sorted(p.name for p in output_dir.iterdir()):
        print(f"  - {name}", flush=True)

    # Never modified: test set, checkpoint, mappings, thresholds - evaluation only.


if __name__ == "__main__":
    main()
