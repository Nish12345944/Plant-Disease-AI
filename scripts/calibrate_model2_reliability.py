"""
Model 2 Prediction Reliability & Calibration Engine
===================================================
1. Evaluates raw logits, softmax probabilities, top-1/top-2 margins, and confusion patterns
   on the dedicated validation split (data/processed/model2_retraining_v2/val/).
2. Computes baseline metrics:
   - Negative Log-Likelihood (NLL)
   - Brier Score
   - Expected Calibration Error (ECE)
3. Fits optimal global temperature scaling parameter T on validation split using L-BFGS / Brent optimization.
4. Computes calibrated NLL, Brier score, and ECE.
5. Evaluates optimal decision threshold and margin threshold for reliable uncertainty detection.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from PIL import Image
from scipy.optimize import minimize_scalar
from torchvision import transforms

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.model2_classifier_v4.predict import Model2DiseaseClassifierV4

def compute_ece(probs: np.ndarray, labels: np.ndarray, n_bins: int = 15) -> float:
    """
    Compute Expected Calibration Error (ECE).
    probs: (N, C) probability distribution
    labels: (N,) true class indices
    """
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = (predictions == labels)

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    n_samples = len(labels)

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)
        
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin

    return float(ece)

def compute_brier_score(probs: np.ndarray, labels: np.ndarray) -> float:
    """Compute multi-class Brier score."""
    n_samples, n_classes = probs.shape
    one_hot = np.zeros((n_samples, n_classes))
    one_hot[np.arange(n_samples), labels] = 1.0
    brier = np.mean(np.sum((probs - one_hot) ** 2, axis=1))
    return float(brier)

def compute_nll(probs: np.ndarray, labels: np.ndarray, eps: float = 1e-12) -> float:
    """Compute Negative Log-Likelihood (cross-entropy)."""
    n_samples = len(labels)
    clipped_probs = np.clip(probs, eps, 1.0)
    correct_probs = clipped_probs[np.arange(n_samples), labels]
    return float(-np.mean(np.log(correct_probs)))


def collect_val_predictions(model_engine: Model2DiseaseClassifierV4, val_dir: Path):
    """
    Collect all logits, true class indices, and paths from the validation split.
    """
    class_to_id = model_engine.class_to_id
    crop_disease_map = model_engine.crop_disease_map

    all_logits = []
    all_labels = []
    all_crops = []
    all_paths = []
    skipped_samples = 0

    print(f"Collecting validation predictions from: {val_dir}")
    
    crops = sorted([d for d in val_dir.iterdir() if d.is_dir()])
    
    for c_dir in crops:
        crop_name = c_dir.name.lower()
        for d_dir in c_dir.iterdir():
            if not d_dir.is_dir():
                continue
            dis_name = d_dir.name.lower()
            if dis_name == "healthy":
                full_class = "healthy"
            else:
                full_class = f"{crop_name}__{dis_name}"

            if full_class not in class_to_id:
                # Check aliases
                alt_class = None
                if crop_name in ("bell_pepper", "bellpepper", "capsicum"):
                    alt_class = f"bell_pepper__{dis_name}"
                elif crop_name in ("bean", "french_bean"):
                    alt_class = f"french_bean__{dis_name}" if f"french_bean__{dis_name}" in class_to_id else f"bean__{dis_name}"
                
                if alt_class and alt_class in class_to_id:
                    full_class = alt_class
                else:
                    skipped_samples += len(list(d_dir.glob("*.*")))
                    continue

            class_id = class_to_id[full_class]
            
            for img_path in d_dir.glob("*.*"):
                if img_path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                    continue
                try:
                    pil_img = Image.open(img_path).convert("RGB")
                    tensor = model_engine.transform(pil_img).unsqueeze(0).to(model_engine.device)
                    with torch.inference_mode():
                        logit = model_engine.model(tensor).squeeze(0).cpu().numpy()
                    all_logits.append(logit)
                    all_labels.append(class_id)
                    all_crops.append(crop_name)
                    all_paths.append(str(img_path))
                except Exception as e:
                    print(f"Error reading {img_path}: {e}")

    print(f"Collected {len(all_logits)} validation samples (skipped {skipped_samples} unmapped).")
    return np.array(all_logits), np.array(all_labels), all_crops, all_paths


def fit_temperature(logits: np.ndarray, labels: np.ndarray) -> float:
    """
    Find optimal scalar temperature T > 0 that minimizes NLL on calibration set.
    """
    tensor_logits = torch.tensor(logits, dtype=torch.float32)
    tensor_labels = torch.tensor(labels, dtype=torch.long)
    nll_criterion = nn.CrossEntropyLoss()

    def loss_func(t_val):
        t = max(t_val, 0.01)
        scaled_logits = tensor_logits / t
        return float(nll_criterion(scaled_logits, tensor_labels).item())

    res = minimize_scalar(loss_func, bounds=(0.1, 5.0), method="bounded")
    optimal_t = float(res.x)
    return optimal_t


def main():
    print("Loading Model 2 V4...")
    m2 = Model2DiseaseClassifierV4()
    
    val_dir = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v2" / "val"
    logits, labels, crops, paths = collect_val_predictions(m2, val_dir)

    # 1. Uncalibrated (T = 1.0)
    uncal_probs = torch.softmax(torch.tensor(logits), dim=1).numpy()
    uncal_nll = compute_nll(uncal_probs, labels)
    uncal_brier = compute_brier_score(uncal_probs, labels)
    uncal_ece = compute_ece(uncal_probs, labels)
    uncal_top1 = float(np.mean(np.argmax(uncal_probs, axis=1) == labels))

    print("\n=== BASELINE UNCALIBRATED METRICS (T = 1.0) on Validation Split ===")
    print(f"  Top-1 Accuracy: {uncal_top1 * 100:.2f}%")
    print(f"  Negative Log-Likelihood (NLL): {uncal_nll:.4f}")
    print(f"  Brier Score: {uncal_brier:.4f}")
    print(f"  Expected Calibration Error (ECE): {uncal_ece:.4f} ({uncal_ece * 100:.2f}%)")

    # 2. Fit Temperature
    opt_t = fit_temperature(logits, labels)
    print(f"\nOptimal Temperature Fitted: T = {opt_t:.4f}")

    # 3. Calibrated (T = opt_t)
    cal_logits = logits / opt_t
    cal_probs = torch.softmax(torch.tensor(cal_logits), dim=1).numpy()
    cal_nll = compute_nll(cal_probs, labels)
    cal_brier = compute_brier_score(cal_probs, labels)
    cal_ece = compute_ece(cal_probs, labels)
    cal_top1 = float(np.mean(np.argmax(cal_probs, axis=1) == labels))

    print("\n=== CALIBRATED METRICS (T = {:.4f}) on Validation Split ===".format(opt_t))
    print(f"  Top-1 Accuracy: {cal_top1 * 100:.2f}% (temperature scaling preserves monotonic argmax)")
    print(f"  Negative Log-Likelihood (NLL): {cal_nll:.4f} (improvement: {uncal_nll - cal_nll:+.4f})")
    print(f"  Brier Score: {cal_brier:.4f} (improvement: {uncal_brier - cal_brier:+.4f})")
    print(f"  Expected Calibration Error (ECE): {cal_ece:.4f} ({cal_ece * 100:.2f}%, improvement: {(uncal_ece - cal_ece)*100:+.2f}%)")

    # 4. Analyze Margins and Decision Thresholds on Crop-Aware Space
    # In crop-aware inference, we only consider candidate diseases compatible with the crop
    print("\nAnalyzing crop-conditioned probability margins and thresholds...")
    
    # Evaluate across a grid of confidence thresholds (0.40 to 0.75) and margin thresholds (0.00 to 0.25)
    best_config = None
    best_score = -1.0
    
    id_to_class = m2.id_to_class
    
    # Precompute compatible predictions for each sample
    compat_data = []
    for i in range(len(labels)):
        crop_key = m2.normalize_crop_key(crops[i])
        probs_i = cal_probs[i]
        
        # Filter by compatibility
        compat_indices = [idx for idx in range(len(probs_i)) if m2.is_compatible(crop_key, id_to_class[idx])]
        if not compat_indices:
            continue
        
        compat_probs = probs_i[compat_indices]
        compat_mass = float(np.sum(compat_probs))
        
        if compat_mass > 1e-6:
            norm_compat_probs = compat_probs / compat_mass
        else:
            norm_compat_probs = compat_probs
            
        sort_order = np.argsort(norm_compat_probs)[::-1]
        top1_idx = compat_indices[sort_order[0]]
        top1_prob = float(norm_compat_probs[sort_order[0]])
        
        top2_prob = float(norm_compat_probs[sort_order[1]]) if len(sort_order) > 1 else 0.0
        margin = top1_prob - top2_prob
        
        is_correct = (top1_idx == labels[i])
        compat_data.append({
            "is_correct": is_correct,
            "top1_prob": top1_prob,
            "margin": margin,
            "compat_mass": compat_mass,
            "top1_class": id_to_class[top1_idx],
            "gt_class": id_to_class[labels[i]],
        })

    print(f"Total crop-compatible validation samples evaluated: {len(compat_data)}")

    grid_results = []
    for min_conf in [0.40, 0.45, 0.50, 0.55, 0.60, 0.65]:
        for min_margin in [0.00, 0.05, 0.10, 0.15, 0.20]:
            # Apply policy:
            # accepted if top1_prob >= min_conf and margin >= min_margin and compat_mass >= 0.20
            # else uncertain
            n_accepted = 0
            n_correct_accepted = 0
            n_error_accepted = 0
            n_high_conf_error = 0
            
            for item in compat_data:
                if item["compat_mass"] >= 0.20 and item["top1_prob"] >= min_conf and item["margin"] >= min_margin:
                    n_accepted += 1
                    if item["is_correct"]:
                        n_correct_accepted += 1
                    else:
                        n_error_accepted += 1
                        if item["top1_prob"] >= 0.80:
                            n_high_conf_error += 1
            
            coverage = n_accepted / len(compat_data)
            precision_accepted = n_correct_accepted / n_accepted if n_accepted > 0 else 0.0
            
            # Harmonic mean of coverage and precision on accepted decisions
            f_score = 2 * (coverage * precision_accepted) / (coverage + precision_accepted) if (coverage + precision_accepted) > 0 else 0.0
            
            grid_results.append({
                "min_conf": min_conf,
                "min_margin": min_margin,
                "coverage": round(coverage, 4),
                "accuracy_on_accepted": round(precision_accepted, 4),
                "error_rate_on_accepted": round(1.0 - precision_accepted, 4),
                "high_conf_errors": n_high_conf_error,
                "f_score": round(f_score, 4),
            })

    # Sort grid results by accuracy and f_score
    grid_results_sorted = sorted(grid_results, key=lambda x: -x["f_score"])
    print("\nTop 5 Global Uncertainty Policy Configurations (Validation Grid Search):")
    for gr in grid_results_sorted[:5]:
        print(f"  conf>={gr['min_conf']}, margin>={gr['min_margin']} -> Coverage: {gr['coverage']*100:.1f}%, Acc on Accepted: {gr['accuracy_on_accepted']*100:.2f}%, High-Conf Errors: {gr['high_conf_errors']}, F-score: {gr['f_score']:.4f}")

    # Output calibration summary
    summary = {
        "calibration_dataset": "data/processed/model2_retraining_v2/val",
        "total_val_samples": len(labels),
        "total_crops": len(set(crops)),
        "uncalibrated_metrics": {
            "temperature": 1.0,
            "nll": round(uncal_nll, 4),
            "brier_score": round(uncal_brier, 4),
            "ece": round(uncal_ece, 4),
            "top1_accuracy": round(uncal_top1, 4),
        },
        "fitted_calibration": {
            "optimal_temperature": round(opt_t, 4),
            "calibrated_nll": round(cal_nll, 4),
            "calibrated_brier_score": round(cal_brier, 4),
            "calibrated_ece": round(cal_ece, 4),
            "ece_reduction_pct": round((uncal_ece - cal_ece) / uncal_ece * 100, 2),
        },
        "optimal_uncertainty_policy": grid_results_sorted[0],
        "grid_search_summary": grid_results_sorted[:10],
    }

    out_path = PROJECT_ROOT / "reports" / "model2_calibration_audit.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nCalibration audit saved to: {out_path}")

if __name__ == "__main__":
    main()
