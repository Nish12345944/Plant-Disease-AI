"""
Evaluate Model 2 Retraining V1 Classifier on Immutable Test Benchmark (143 Classes)
===================================================================================
Evaluates the best checkpoint (models/model2_retraining_v1/best_model.pth)
against the authoritative 2,304-image test set from:
  data/processed/model2_retraining_v1_manifest.csv (split == 'test')

Reuses dataset loading, preprocessing, model architecture, and evaluation logic
from scripts/train_model2_retraining_v1.py.

Outputs saved in:
  reports/model2_retraining/test_evaluation/
  ├── evaluation_summary.json
  ├── test_classification_report.csv
  ├── test_predictions.csv
  ├── confusion_matrix.png
  └── confusion_matrix.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.models import efficientnet_b2
from tqdm import tqdm

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Reuse validated modules from train script
from scripts.train_model2_retraining_v1 import (
    IMAGE_SIZE,
    Model2RetrainingDataset,
    evaluate,
    get_transforms,
)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Default Paths and Constants
# ---------------------------------------------------------------------------
DEFAULT_CHECKPOINT = PROJECT_ROOT / "models" / "model2_retraining_v1" / "best_model.pth"
DEFAULT_MANIFEST = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v1_manifest.csv"
DEFAULT_DATASET_DIR = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v1"
DEFAULT_CLASS_MAPPING = DEFAULT_DATASET_DIR / "class_mapping.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "reports" / "model2_retraining" / "test_evaluation"

EXPECTED_TEST_COUNT = 2304
EXPECTED_NUM_CLASSES = 143


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for test evaluation."""
    parser = argparse.ArgumentParser(
        description="Evaluate Model 2 Retraining V1 (143 Classes) on Immutable Test Set"
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=DEFAULT_CHECKPOINT,
        help=f"Path to model checkpoint (.pth). Default: {DEFAULT_CHECKPOINT}",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=f"Path to dataset manifest (.csv). Default: {DEFAULT_MANIFEST}",
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=DEFAULT_DATASET_DIR,
        help=f"Root directory of processed dataset images. Default: {DEFAULT_DATASET_DIR}",
    )
    parser.add_argument(
        "--class-mapping",
        type=Path,
        default=DEFAULT_CLASS_MAPPING,
        help=f"Path to class_mapping.json. Default: {DEFAULT_CLASS_MAPPING}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save evaluation reports. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=8,
        help="Evaluation batch size. Default: 8",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=0,
        help="DataLoader worker processes. Default: 0 (safe for Windows)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Target device ('cuda', 'cpu'). Auto-detected if not specified.",
    )
    return parser.parse_args()


def load_and_verify_class_mapping(mapping_path: Path) -> Tuple[Dict[str, int], Dict[int, str]]:
    """Load and verify 143-class mapping integrity."""
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

    expected_indices = set(range(EXPECTED_NUM_CLASSES))
    actual_indices = set(id_to_class.keys())
    if actual_indices != expected_indices:
        missing = expected_indices - actual_indices
        raise ValueError(f"Class mapping missing continuous indices: {missing}")

    return class_to_id, id_to_class


def load_and_verify_test_manifest(
    manifest_path: Path,
    dataset_dir: Path,
    class_to_id: Dict[str, int],
) -> List[Dict[str, Any]]:
    """Load and verify the immutable 2,304-image test set from manifest."""
    if not manifest_path.exists():
        raise FileNotFoundError(f"Dataset manifest not found at: {manifest_path}")

    test_records: List[Dict[str, Any]] = []
    with open(manifest_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("split") == "test":
                test_records.append(row)

    if len(test_records) != EXPECTED_TEST_COUNT:
        raise ValueError(
            f"Test set count mismatch! Expected exactly {EXPECTED_TEST_COUNT} test images, "
            f"but found {len(test_records)} in {manifest_path}"
        )

    # Validate image files exist and class IDs align with mapping
    missing_files = []
    invalid_classes = []
    for row in test_records:
        img_rel = row["image_path"]
        class_id = int(row["class_id"])
        canonical_class = row["canonical_class"]

        full_img_path = dataset_dir / img_rel
        if not full_img_path.exists():
            missing_files.append(img_rel)

        if class_to_id.get(canonical_class) != class_id:
            invalid_classes.append((canonical_class, class_id, class_to_id.get(canonical_class)))

    if missing_files:
        sample_missing = missing_files[:5]
        raise FileNotFoundError(
            f"{len(missing_files)} test images not found on disk under {dataset_dir}. "
            f"First missing samples: {sample_missing}"
        )

    if invalid_classes:
        sample_invalid = invalid_classes[:5]
        raise ValueError(
            f"{len(invalid_classes)} test records have class_id inconsistent with class_mapping.json. "
            f"First invalid samples: {sample_invalid}"
        )

    return test_records


def build_and_load_model(
    checkpoint_path: Path,
    num_classes: int,
    device: torch.device,
) -> Tuple[nn.Module, Dict[str, Any]]:
    """Build EfficientNet-B2 and load checkpoint weights strictly."""
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Model checkpoint not found at: {checkpoint_path}")

    # Build model architecture matching train script
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes),
    )

    print(f"Loading checkpoint from: {checkpoint_path}...")
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)

    if "model_state_dict" not in checkpoint:
        raise KeyError(
            f"Checkpoint at {checkpoint_path} does not contain 'model_state_dict'. "
            f"Keys found: {list(checkpoint.keys())}"
        )

    state_dict = checkpoint["model_state_dict"]

    # Verify head dimensions in state dict
    head_weight_key = "classifier.1.weight"
    if head_weight_key in state_dict:
        head_out_features = state_dict[head_weight_key].shape[0]
        if head_out_features != num_classes:
            raise ValueError(
                f"Checkpoint output classes ({head_out_features}) != expected classes ({num_classes})"
            )

    # Load weights strictly into model
    load_res = model.load_state_dict(state_dict, strict=True)
    print(f"Model state restored cleanly (All {len(state_dict)} tensors matched).")

    model = model.to(device)
    model.eval()

    return model, checkpoint


def save_confusion_matrix_plot(
    cm: np.ndarray,
    output_png: Path,
    num_classes: int,
):
    """Save clean, readable confusion matrix heatmap."""
    fig, ax = plt.subplots(figsize=(16, 14), dpi=150)
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax.set(
        xticks=np.arange(0, num_classes, 10),
        yticks=np.arange(0, num_classes, 10),
        xlabel="Predicted Class Index",
        ylabel="True Class Index",
        title=f"Confusion Matrix — Model 2 Retraining V1 ({num_classes} Classes, {cm.sum():,} Test Images)",
    )
    plt.tight_layout()
    fig.savefig(output_png, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved confusion matrix plot to: {output_png}")


def run_evaluation():
    """Main evaluation execution pipeline."""
    args = parse_arguments()
    start_time = time.time()

    # Determine execution device
    if args.device:
        device = torch.device(args.device)
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    device_name = torch.cuda.get_device_name(0) if device.type == "cuda" else "CPU"

    print("=" * 80)
    print("MODEL 2 RETRAINING V1 — INDEPENDENT TEST BENCHMARK EVALUATION")
    print("=" * 80)
    print(f"Execution Device : {device} ({device_name})")
    print(f"Checkpoint       : {args.checkpoint}")
    print(f"Manifest Path    : {args.manifest}")
    print(f"Batch Size       : {args.batch_size}")
    print(f"Num Workers      : {args.num_workers}")
    print("=" * 80)

    # 1. Load & verify class mapping
    class_to_id, id_to_class = load_and_verify_class_mapping(args.class_mapping)
    num_classes = len(class_to_id)
    print(f"✓ Verified Class Mapping: {num_classes} canonical classes (indices 0 to {num_classes - 1}).")

    # 2. Load & verify test manifest
    test_records = load_and_verify_test_manifest(args.manifest, args.dataset_dir, class_to_id)
    print(f"✓ Verified Test Benchmark: exactly {len(test_records):,} immutable test images present on disk.")

    # 3. Build & load model weights
    model, checkpoint_meta = build_and_load_model(args.checkpoint, num_classes, device)
    checkpoint_epoch = checkpoint_meta.get("epoch", "unknown")
    val_macro_f1 = checkpoint_meta.get("val_macro_f1", None)
    print(f"✓ Checkpoint Metadata: Epoch {checkpoint_epoch} (Validation Macro F1: {val_macro_f1:.4f})" if val_macro_f1 else f"✓ Checkpoint Metadata: Epoch {checkpoint_epoch}")

    # 4. Prepare Dataset & DataLoader
    _, test_transform = get_transforms()
    test_samples = [(row["image_path"], int(row["class_id"])) for row in test_records]
    test_dataset = Model2RetrainingDataset(test_samples, args.dataset_dir, transform=test_transform)

    test_loader = DataLoader(
        test_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=(device.type == "cuda"),
    )

    criterion = nn.CrossEntropyLoss()

    # Wrap DataLoader with tqdm progress bar and attach dataset attribute
    progress_bar = tqdm(
        test_loader,
        desc="Evaluating Test Benchmark",
        total=len(test_loader),
        unit="batch",
        ncols=90,
    )
    progress_bar.dataset = test_dataset  # Required by evaluate() for len(loader.dataset)

    # 5. Execute Evaluation
    eval_results = evaluate(
        model=model,
        loader=progress_bar,
        criterion=criterion,
        device=device,
        num_classes=num_classes,
    )

    elapsed_time = time.time() - start_time
    print(f"\nEvaluation completed in {elapsed_time:.2f} seconds ({len(test_samples) / elapsed_time:.1f} img/s).")

    # 6. Extract Metrics
    loss = eval_results["loss"]
    accuracy = eval_results["accuracy"]
    top3_accuracy = eval_results["top3_accuracy"]
    macro_f1 = eval_results["macro_f1"]
    macro_precision = eval_results["macro_precision"]
    macro_recall = eval_results["macro_recall"]
    weighted_f1 = eval_results["weighted_f1"]
    healthy_f1 = eval_results["healthy_f1"]
    disease_macro_f1 = eval_results["disease_macro_f1"]

    per_class_precision = eval_results["per_class_precision"]
    per_class_recall = eval_results["per_class_recall"]
    per_class_f1 = eval_results["per_class_f1"]
    per_class_support = eval_results["per_class_support"]
    preds = eval_results["preds"]
    targets = eval_results["targets"]
    probs = eval_results["probs"]

    # 7. Print Formatted Results
    print("\n" + "=" * 80)
    print("TEST BENCHMARK EVALUATION SUMMARY")
    print("=" * 80)
    print(f"Test Loss            : {loss:.4f}")
    print(f"Top-1 Accuracy       : {accuracy * 100:.2f}% ({np.sum(preds == targets)} / {len(targets)})")
    print(f"Top-3 Accuracy       : {top3_accuracy * 100:.2f}%")
    print(f"Macro F1             : {macro_f1 * 100:.2f}%")
    print(f"Macro Precision      : {macro_precision * 100:.2f}%")
    print(f"Macro Recall         : {macro_recall * 100:.2f}%")
    print(f"Weighted F1          : {weighted_f1 * 100:.2f}%")
    print(f"Healthy F1 (Class 0) : {healthy_f1 * 100:.2f}%")
    print(f"Disease-Only Macro F1: {disease_macro_f1 * 100:.2f}% (Classes 1..142)")
    print("=" * 80)

    # 8. Create Output Directory (Isolated)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # 9. Save Per-Class Classification Report CSV
    report_csv = output_dir / "test_classification_report.csv"
    with open(report_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "class_id",
            "canonical_class",
            "crop",
            "disease",
            "precision",
            "recall",
            "f1_score",
            "support",
        ])
        for c in range(num_classes):
            c_name = id_to_class[c]
            if "__" in c_name:
                crop_part, disease_part = c_name.split("__", 1)
            else:
                crop_part, disease_part = "all_crops", c_name

            writer.writerow([
                c,
                c_name,
                crop_part,
                disease_part,
                f"{per_class_precision[c]:.4f}",
                f"{per_class_recall[c]:.4f}",
                f"{per_class_f1[c]:.4f}",
                int(per_class_support[c]),
            ])
    print(f"Saved per-class classification report to: {report_csv}")

    # 10. Save Individual Predictions CSV
    preds_csv = output_dir / "test_predictions.csv"
    with open(preds_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "image_path",
            "true_class_id",
            "true_canonical_class",
            "predicted_class_id",
            "predicted_canonical_class",
            "confidence",
            "is_correct",
            "top3_predicted_ids",
            "top3_predicted_classes",
            "top3_confidences",
        ])
        for i, row in enumerate(test_records):
            img_rel = row["image_path"]
            true_id = int(row["class_id"])
            true_name = row["canonical_class"]

            pred_id = int(preds[i])
            pred_name = id_to_class[pred_id]
            prob_dist = probs[i]
            conf = float(prob_dist[pred_id])
            is_correct = bool(true_id == pred_id)

            top3_idx = np.argsort(prob_dist)[::-1][:3]
            top3_names = [id_to_class[idx] for idx in top3_idx]
            top3_confs = [f"{prob_dist[idx]:.4f}" for idx in top3_idx]

            writer.writerow([
                img_rel,
                true_id,
                true_name,
                pred_id,
                pred_name,
                f"{conf:.4f}",
                is_correct,
                ";".join(str(x) for x in top3_idx),
                ";".join(top3_names),
                ";".join(top3_confs),
            ])
    print(f"Saved individual test predictions to: {preds_csv}")

    # 11. Compute & Save Confusion Matrix
    cm = confusion_matrix(targets, preds, labels=list(range(num_classes)))

    # Save Confusion Matrix CSV
    cm_csv = output_dir / "confusion_matrix.csv"
    with open(cm_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["true_class_id", "true_class_name"] + [f"pred_{c}" for c in range(num_classes)])
        for c in range(num_classes):
            writer.writerow([c, id_to_class[c]] + list(cm[c]))
    print(f"Saved confusion matrix CSV to: {cm_csv}")

    # Save Confusion Matrix Heatmap PNG
    cm_png = output_dir / "confusion_matrix.png"
    save_confusion_matrix_plot(cm, cm_png, num_classes)

    # 12. Save JSON Summary
    summary_json = output_dir / "evaluation_summary.json"
    summary_data = {
        "model_architecture": "EfficientNet-B2",
        "checkpoint_evaluated": str(args.checkpoint.resolve()),
        "checkpoint_epoch": checkpoint_epoch,
        "validation_macro_f1_at_checkpoint": float(val_macro_f1) if val_macro_f1 else None,
        "dataset_manifest": str(args.manifest.resolve()),
        "test_images_count": len(test_samples),
        "num_classes": num_classes,
        "execution_device": str(device),
        "gpu_device_name": device_name,
        "evaluation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "evaluation_duration_seconds": round(elapsed_time, 2),
        "metrics": {
            "test_loss": round(float(loss), 4),
            "top1_accuracy": round(float(accuracy), 4),
            "top3_accuracy": round(float(top3_accuracy), 4),
            "macro_f1": round(float(macro_f1), 4),
            "macro_precision": round(float(macro_precision), 4),
            "macro_recall": round(float(macro_recall), 4),
            "weighted_f1": round(float(weighted_f1), 4),
            "healthy_f1": round(float(healthy_f1), 4),
            "disease_macro_f1": round(float(disease_macro_f1), 4),
        },
        "artifacts_generated": {
            "summary_json": str(summary_json.resolve()),
            "classification_report_csv": str(report_csv.resolve()),
            "predictions_csv": str(preds_csv.resolve()),
            "confusion_matrix_csv": str(cm_csv.resolve()),
            "confusion_matrix_png": str(cm_png.resolve()),
        },
    }

    with open(summary_json, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Saved evaluation JSON summary to: {summary_json}")

    print("\n" + "=" * 80)
    print("EVALUATION PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"All reports saved in: {output_dir.resolve()}")
    print("=" * 80)


if __name__ == "__main__":
    run_evaluation()
