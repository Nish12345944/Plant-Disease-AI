"""Train and Evaluate Model 1 Domain-Shift Experiment E1 (Isolated Head-Only Fine-Tuning).

Strict Preflight & Safety Rules:
- Original Model 1 checkpoint (models/model1_expanded/best_model.pth) is NEVER overwritten.
- Model 2 V4 (models/model2_classifier_v4/best_model.pth) is strictly UNTOUCHED.
- Frozen benchmark (2,304 images) is evaluated strictly out-of-sample; NEVER trained on.
- Output checkpoints saved strictly to models/model1_domain_shift_e1/.
- Reports and metrics saved strictly to reports/model1_expansion/exp_domain_shift_e1/.
"""

import csv
import json
import logging
import os
import random
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
from torch.utils.data import DataLoader, Dataset
from torchvision import models as tvm, transforms

# ---------------------------------------------------------------------------
# Directories and Paths
# ---------------------------------------------------------------------------
ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
SRC_CHECKPOINT_DIR = ROOT / "models" / "model1_expanded"
EXP_CHECKPOINT_DIR = ROOT / "models" / "model1_domain_shift_e1"
REPORTS_DIR = ROOT / "reports" / "model1_expansion" / "exp_domain_shift_e1"
DATASET_DIR = ROOT / "data" / "processed" / "model1_expanded"
FROZEN_BENCHMARK_CSV = ROOT / "reports" / "manual_prediction_failures" / "_e0_expandedM1_V4_benchmark.csv"

EXP_CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

BEST_MODEL_PATH = EXP_CHECKPOINT_DIR / "best_model.pth"
CONFIG_PATH = EXP_CHECKPOINT_DIR / "config.json"
CLASS_MAPPING_PATH = EXP_CHECKPOINT_DIR / "class_mapping.json"
FEATURE_CACHE_PATH = EXP_CHECKPOINT_DIR / "train_val_features_cache.pt"

# Copy class_mapping.json to experiment directory
shutil.copy2(SRC_CHECKPOINT_DIR / "class_mapping.json", CLASS_MAPPING_PATH)

# Logger setup
logger = logging.getLogger("Model1_E1_Trainer")
logger.setLevel(logging.INFO)
handlers = [
    logging.FileHandler(REPORTS_DIR / "training_and_eval.log", mode="w", encoding="utf-8"),
    logging.StreamHandler(sys.stdout),
]
for h in handlers:
    h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(h)

# Original 22 classes from production Model 1
ORIGINAL_22_CLASSES = sorted([
    "anthurium", "blueberry", "broccoli", "capsicum", "carnation", "cherry_tomato",
    "chrysanthemum", "cucumber", "french_bean", "geranium", "gerbera", "gypsophila",
    "lettuce", "lilium", "marigold", "melon", "orchid", "rose", "spinach",
    "strawberry", "tomato", "zucchini"
])

# Hyperparameters
SEED = 42
IMAGE_SIZE = 224
EPOCHS = 3
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 1e-4
BATCH_SIZE = 64
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class ImageListDataset(Dataset):
    def __init__(self, samples, transform=None):
        self.samples = samples  # list of (path, label_idx)
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        with open(path, "rb") as f:
            img = Image.open(f).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, label


class TensorFeatureDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


def get_eval_transform():
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def build_samples_list(split_dir, sorted_classes, class_to_idx):
    samples = []
    for c in sorted_classes:
        c_dir = split_dir / c
        if c_dir.exists():
            idx = class_to_idx[c]
            for p in sorted(c_dir.glob("*.jpg")):
                samples.append((str(p), idx))
    return samples


def extract_features(model, loader, device, desc=""):
    logger.info(f"Extracting features for {desc} ({len(loader.dataset)} samples)...")
    feats_list = []
    labels_list = []
    t0 = time.perf_counter()
    with torch.no_grad():
        for i, (imgs, lbls) in enumerate(loader):
            imgs = imgs.to(device)
            # EfficientNet backbone feature extraction + avgpool + flatten
            f = model.features(imgs)
            f = model.avgpool(f)
            f = torch.flatten(f, 1)
            feats_list.append(f.cpu())
            labels_list.append(lbls)
            if (i + 1) % 50 == 0 or (i + 1) == len(loader):
                elapsed = time.perf_counter() - t0
                done = (i + 1) * loader.batch_size
                logger.info(f"  [{desc}] Processed {min(done, len(loader.dataset))}/{len(loader.dataset)} in {elapsed:.1f}s")
    all_feats = torch.cat(feats_list, dim=0)
    all_labels = torch.cat(labels_list, dim=0)
    logger.info(f"  Finished {desc} feature extraction: shape={all_feats.shape} in {time.perf_counter() - t0:.1f}s")
    return all_feats, all_labels


def main():
    set_seed(SEED)
    device = torch.device("cpu")
    torch.set_num_threads(8)

    logger.info("=" * 80)
    logger.info("MODEL 1 EXPERIMENT E1: CONTROLLED DOMAIN-SHIFT HEAD FINE-TUNING")
    logger.info("=" * 80)
    logger.info(f"PyTorch Device: {device} | Threads: {torch.get_num_threads()}")
    logger.info(f"Seed: {SEED} | Epochs: {EPOCHS} | LR: {LEARNING_RATE} | WD: {WEIGHT_DECAY}")
    logger.info(f"Base checkpoint: {SRC_CHECKPOINT_DIR / 'best_model.pth'}")
    logger.info(f"Experiment dir: {EXP_CHECKPOINT_DIR}")

    # 1. Load mapping
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)
    class_to_idx = mapping_data["class_to_idx"]
    idx_to_class = {int(k): v for k, v in mapping_data["idx_to_class"].items()}
    aliases = mapping_data.get("aliases", {})
    sorted_classes = [idx_to_class[i] for i in range(len(class_to_idx))]
    num_classes = len(sorted_classes)
    assert num_classes == 46, f"Expected 46 classes, got {num_classes}"

    # 2. Build datasets
    eval_tf = get_eval_transform()
    train_samples = build_samples_list(DATASET_DIR / "train", sorted_classes, class_to_idx)
    val_samples = build_samples_list(DATASET_DIR / "val", sorted_classes, class_to_idx)
    logger.info(f"Dataset Partitions:")
    logger.info(f"  Train: {len(train_samples):,} samples (from data/processed/model1_expanded/train)")
    logger.info(f"  Val  : {len(val_samples):,} samples (from data/processed/model1_expanded/val)")
    logger.info(f"  Test & Frozen Benchmark: STRICTLY EXCLUDED from training")

    # 3. Class Imbalance Strategy (Smoothed Inverse-Frequency, without double-sampling)
    train_labels_counts = Counter([s[1] for s in train_samples])
    active_counts = [cnt for cnt in train_labels_counts.values() if cnt > 0]
    median_cnt = float(np.median(active_counts))

    raw_weights = []
    for c_idx in range(num_classes):
        cnt = train_labels_counts.get(c_idx, 0)
        if cnt > 0:
            w = float(np.clip((median_cnt / max(cnt, 2)) ** 0.35, 0.5, 2.0))
        else:
            w = 0.0
        raw_weights.append(w)
    active_mean = sum(raw_weights) / sum(1 for w in raw_weights if w > 0)
    norm_weights = [w / active_mean if w > 0 else 0.0 for w in raw_weights]
    class_weights_tensor = torch.tensor(norm_weights, dtype=torch.float32, device=device)
    logger.info(f"Class Weights validated: active={sum(1 for w in norm_weights if w > 0)}/46, min={min(w for w in norm_weights if w > 0):.3f}, max={max(norm_weights):.3f}")
    logger.info(f"  Potato weight: {norm_weights[class_to_idx['potato']]:.3f} (N={train_labels_counts[class_to_idx['potato']]})")
    logger.info(f"  Tomato weight: {norm_weights[class_to_idx['tomato']]:.3f} (N={train_labels_counts[class_to_idx['tomato']]})")
    logger.info(f"  Zucchini weight: {norm_weights[class_to_idx['zucchini']]:.3f} (N={train_labels_counts[class_to_idx['zucchini']]})")
    logger.info(f"  Cucumber weight: {norm_weights[class_to_idx['cucumber']]:.3f} (N={train_labels_counts[class_to_idx['cucumber']]})")

    # 4. Load model
    ckpt = torch.load(SRC_CHECKPOINT_DIR / "best_model.pth", map_location="cpu", weights_only=False)
    sd = ckpt["model_state_dict"] if isinstance(ckpt, dict) and "model_state_dict" in ckpt else ckpt

    model = tvm.efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    model.load_state_dict(sd, strict=True)
    model.eval()

    # Freeze feature extractor
    for p in model.features.parameters():
        p.requires_grad = False
    for p in model.classifier.parameters():
        p.requires_grad = True

    # 5. Feature extraction (or load cache if exists)
    if FEATURE_CACHE_PATH.exists():
        logger.info(f"Loading cached feature vectors from {FEATURE_CACHE_PATH}...")
        cache_data = torch.load(FEATURE_CACHE_PATH, map_location="cpu", weights_only=False)
        train_features, train_targets = cache_data["train_features"], cache_data["train_targets"]
        val_features, val_targets = cache_data["val_features"], cache_data["val_targets"]
    else:
        raw_train_loader = DataLoader(ImageListDataset(train_samples, transform=eval_tf), batch_size=BATCH_SIZE, shuffle=False, num_workers=4)
        raw_val_loader = DataLoader(ImageListDataset(val_samples, transform=eval_tf), batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

        train_features, train_targets = extract_features(model, raw_train_loader, device, desc="Train Split")
        val_features, val_targets = extract_features(model, raw_val_loader, device, desc="Val Split")

        torch.save({
            "train_features": train_features,
            "train_targets": train_targets,
            "val_features": val_features,
            "val_targets": val_targets,
        }, FEATURE_CACHE_PATH)
        logger.info(f"Saved feature cache to {FEATURE_CACHE_PATH}")

    # 6. Train Classifier Head
    head = model.classifier
    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)
    optimizer = torch.optim.AdamW(head.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

    train_feature_loader = DataLoader(TensorFeatureDataset(train_features, train_targets), batch_size=BATCH_SIZE, shuffle=True)
    val_feature_loader = DataLoader(TensorFeatureDataset(val_features, val_targets), batch_size=BATCH_SIZE, shuffle=False)

    best_val_f1 = 0.0
    history = []
    t_train_start = time.perf_counter()

    for epoch in range(1, EPOCHS + 1):
        head.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for feats, targets in train_feature_loader:
            feats, targets = feats.to(device), targets.to(device)
            optimizer.zero_grad()
            logits = head(feats)
            loss = criterion(logits, targets)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * len(targets)
            preds = logits.argmax(dim=1)
            correct += (preds == targets).sum().item()
            total += len(targets)

        train_loss = total_loss / total
        train_acc = correct / total

        # Validation
        head.eval()
        val_loss = 0.0
        val_preds_list = []
        val_targets_list = []
        with torch.no_grad():
            for feats, targets in val_feature_loader:
                feats, targets = feats.to(device), targets.to(device)
                logits = head(feats)
                loss = criterion(logits, targets)
                val_loss += loss.item() * len(targets)
                val_preds_list.append(logits.argmax(dim=1).cpu())
                val_targets_list.append(targets.cpu())

        val_preds_all = torch.cat(val_preds_list).numpy()
        val_targets_all = torch.cat(val_targets_list).numpy()
        val_loss = val_loss / len(val_targets_all)
        val_acc = (val_preds_all == val_targets_all).mean()
        val_macro_f1 = f1_score(val_targets_all, val_preds_all, average="macro", zero_division=0)

        logger.info(
            f"Epoch {epoch}/{EPOCHS} - "
            f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc*100:.2f}% | "
            f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc*100:.2f}%, Val Macro F1: {val_macro_f1*100:.2f}%"
        )
        history.append({
            "epoch": epoch,
            "train_loss": round(train_loss, 4),
            "train_acc": round(train_acc, 4),
            "val_loss": round(val_loss, 4),
            "val_acc": round(val_acc, 4),
            "val_macro_f1": round(val_macro_f1, 4),
        })

        if val_macro_f1 > best_val_f1:
            best_val_f1 = val_macro_f1
            logger.info(f"  -> New best validation Macro F1: {best_val_f1*100:.2f}%! Saving checkpoint...")
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "val_macro_f1": val_macro_f1,
                "val_accuracy": val_acc,
                "val_loss": val_loss,
                "class_to_idx": class_to_idx,
                "sorted_classes": sorted_classes,
                "architecture": "efficientnet_b2",
                "image_size": IMAGE_SIZE,
                "mean": IMAGENET_MEAN,
                "std": IMAGENET_STD,
                "experiment": "model1_domain_shift_e1",
            }, BEST_MODEL_PATH)

    train_duration = time.perf_counter() - t_train_start
    logger.info(f"Head training finished in {train_duration:.1f}s. Best checkpoint at {BEST_MODEL_PATH}")

    # Save experiment config
    exp_config = {
        "model_architecture": "efficientnet_b2",
        "num_classes": 46,
        "image_size": IMAGE_SIZE,
        "epochs": EPOCHS,
        "learning_rate": LEARNING_RATE,
        "weight_decay": WEIGHT_DECAY,
        "seed": SEED,
        "imbalance_strategy": "Smoothed Inverse Frequency Loss Weights [0.5, 2.0] + Standard Shuffle",
        "best_val_macro_f1": round(best_val_f1, 4),
        "train_duration_sec": round(train_duration, 2),
        "checkpoint": str(BEST_MODEL_PATH),
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(exp_config, f, indent=2)

    # -----------------------------------------------------------------------
    # Step C: Evaluate on Frozen Benchmark (2,304 images)
    # -----------------------------------------------------------------------
    logger.info("\n" + "=" * 80)
    logger.info("STEP C: EVALUATING E1 CHECKPOINT ON FROZEN 2,304-IMAGE BENCHMARK")
    logger.info("=" * 80)

    # Load the best saved model state
    best_ckpt = torch.load(BEST_MODEL_PATH, map_location="cpu", weights_only=False)
    model.load_state_dict(best_ckpt["model_state_dict"])
    model.eval()

    benchmark_rows = list(csv.DictReader(open(FROZEN_BENCHMARK_CSV, encoding="utf-8")))
    logger.info(f"Loaded {len(benchmark_rows)} benchmark rows from {FROZEN_BENCHMARK_CSV}")

    # Aliases mapping for canonical crop names
    canonical_class_lookup = {i: aliases.get(c, c) for i, c in idx_to_class.items()}

    evaluated_rows = []
    y_true = []
    y_pred = []

    t_eval_start = time.perf_counter()
    with torch.no_grad():
        for i, row in enumerate(benchmark_rows):
            img_rel = row["image"]
            img_full = ROOT / img_rel
            with open(img_full, "rb") as f:
                img_pil = Image.open(f).convert("RGB")
            t_img = eval_tf(img_pil).unsqueeze(0).to(device)

            logits = model(t_img)
            pred_idx = int(logits.argmax(dim=1).item())
            pred_class = canonical_class_lookup[pred_idx]
            conf = float(torch.softmax(logits, dim=1)[0, pred_idx].item())

            actual_label = row["actual"]
            gt_crop = aliases.get(actual_label.split("__")[0], actual_label.split("__")[0])
            is_ok = int(pred_class == gt_crop)

            y_true.append(gt_crop)
            y_pred.append(pred_class)

            evaluated_rows.append({
                "image": img_rel,
                "actual": actual_label,
                "gt_crop": gt_crop,
                "e0_m1_crop": row.get("m1_crop", ""),
                "e0_m1_ok": row.get("m1_ok", ""),
                "e1_m1_crop": pred_class,
                "e1_m1_conf": round(conf, 4),
                "e1_m1_ok": is_ok,
                "status": row.get("status", ""),
            })

            if (i + 1) % 500 == 0 or (i + 1) == len(benchmark_rows):
                logger.info(f"  Evaluated {i + 1}/{len(benchmark_rows)} benchmark images...")

    eval_duration = time.perf_counter() - t_eval_start
    logger.info(f"Evaluation complete in {eval_duration:.1f}s")

    # Save benchmark prediction CSV
    benchmark_pred_csv = REPORTS_DIR / "benchmark_predictions.csv"
    with open(benchmark_pred_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(evaluated_rows[0].keys()))
        writer.writeheader()
        writer.writerows(evaluated_rows)
    logger.info(f"Saved benchmark predictions to {benchmark_pred_csv}")

    # Metrics calculation
    all_classes_in_benchmark = sorted(list(set(y_true) | set(y_pred)))
    overall_acc = sum(r["e1_m1_ok"] for r in evaluated_rows) / len(evaluated_rows)
    e0_acc = sum(int(r["e0_m1_ok"]) for r in evaluated_rows if r["e0_m1_ok"] != "") / len(evaluated_rows)

    prec_per_class = precision_score(y_true, y_pred, labels=all_classes_in_benchmark, average=None, zero_division=0)
    rec_per_class = recall_score(y_true, y_pred, labels=all_classes_in_benchmark, average=None, zero_division=0)
    f1_per_class = f1_score(y_true, y_pred, labels=all_classes_in_benchmark, average=None, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=all_classes_in_benchmark)

    # Export per_class_metrics.csv
    per_class_csv = REPORTS_DIR / "per_class_metrics.csv"
    with open(per_class_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["crop", "precision", "recall", "f1_score", "support"])
        for idx, cls_name in enumerate(all_classes_in_benchmark):
            supp = sum(1 for y in y_true if y == cls_name)
            w.writerow([cls_name, round(prec_per_class[idx], 4), round(rec_per_class[idx], 4), round(f1_per_class[idx], 4), supp])
    logger.info(f"Saved per-class metrics to {per_class_csv}")

    # Export confusion_matrix.csv
    cm_csv = REPORTS_DIR / "confusion_matrix.csv"
    with open(cm_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["actual_crop"] + all_classes_in_benchmark)
        for i, row in enumerate(cm):
            w.writerow([all_classes_in_benchmark[i]] + list(row))
    logger.info(f"Saved confusion matrix to {cm_csv}")

    # Specific Target Confound Metrics:
    # 1. Tomato metrics
    tomato_rows = [r for r in evaluated_rows if r["gt_crop"] == "tomato"]
    tomato_n = len(tomato_rows)
    tomato_correct = sum(r["e1_m1_ok"] for r in tomato_rows)
    tomato_rec = tomato_correct / tomato_n if tomato_n else 0.0
    tomato_to_potato = sum(1 for r in tomato_rows if r["e1_m1_crop"] == "potato")
    tomato_confusions = Counter([r["e1_m1_crop"] for r in tomato_rows if not r["e1_m1_ok"]])

    # 2. Cucumber metrics
    cucumber_rows = [r for r in evaluated_rows if r["gt_crop"] == "cucumber"]
    cucumber_n = len(cucumber_rows)
    cucumber_correct = sum(r["e1_m1_ok"] for r in cucumber_rows)
    cucumber_rec = cucumber_correct / cucumber_n if cucumber_n else 0.0
    cucumber_to_zucchini = sum(1 for r in cucumber_rows if r["e1_m1_crop"] == "zucchini")
    cucumber_confusions = Counter([r["e1_m1_crop"] for r in cucumber_rows if not r["e1_m1_ok"]])

    # Cucumber powdery mildew
    cuc_pm_rows = [r for r in cucumber_rows if "powdery_mildew" in r["actual"]]
    cuc_pm_n = len(cuc_pm_rows)
    cuc_pm_to_zucchini = sum(1 for r in cuc_pm_rows if r["e1_m1_crop"] == "zucchini")

    # 3. Original 22 classes regression check
    orig_22_canon = {aliases.get(c, c) for c in ORIGINAL_22_CLASSES}
    orig_rows = [r for r in evaluated_rows if r["gt_crop"] in orig_22_canon]
    orig_e0_acc = sum(int(r["e0_m1_ok"]) for r in orig_rows if r["e0_m1_ok"] != "") / len(orig_rows)
    orig_e1_acc = sum(r["e1_m1_ok"] for r in orig_rows) / len(orig_rows)

    # 4. Other 44 crops regression check
    other_rows = [r for r in evaluated_rows if r["gt_crop"] not in ("tomato", "cucumber")]
    other_e0_acc = sum(int(r["e0_m1_ok"]) for r in other_rows if r["e0_m1_ok"] != "") / len(other_rows)
    other_e1_acc = sum(r["e1_m1_ok"] for r in other_rows) / len(other_rows)

    logger.info("=" * 80)
    logger.info("EVALUATION RESULTS COMPARISON: BASELINE (E0) VS EXPERIMENT (E1)")
    logger.info("=" * 80)
    logger.info(f"Overall Top-1 Benchmark Accuracy: E0={e0_acc*100:.2f}% -> E1={overall_acc*100:.2f}% (delta: {(overall_acc - e0_acc)*100:+.2f}%)")
    logger.info(f"Original 22 Classes Accuracy    : E0={orig_e0_acc*100:.2f}% -> E1={orig_e1_acc*100:.2f}% (delta: {(orig_e1_acc - orig_e0_acc)*100:+.2f}%)")
    logger.info(f"Other 44 Crops Accuracy         : E0={other_e0_acc*100:.2f}% -> E1={other_e1_acc*100:.2f}% (delta: {(other_e1_acc - other_e0_acc)*100:+.2f}%)")
    logger.info("-" * 80)
    logger.info(f"Tomato Recall (n={tomato_n})      : E0=21.4% (21/98) -> E1={tomato_rec*100:.1f}% ({tomato_correct}/{tomato_n})")
    logger.info(f"Tomato -> Potato Errors         : E0=21 -> E1={tomato_to_potato}")
    logger.info(f"Tomato Confusions Breakdown     : {dict(tomato_confusions.most_common(5))}")
    logger.info("-" * 80)
    logger.info(f"Cucumber Recall (n={cucumber_n})    : E0=24.6% (14/57) -> E1={cucumber_rec*100:.1f}% ({cucumber_correct}/{cucumber_n})")
    logger.info(f"Cucumber -> Zucchini Errors     : E0=29/57 -> E1={cucumber_to_zucchini}/{cucumber_n}")
    logger.info(f"Cucumber PM -> Zucchini         : E0=20/22 (90.9%) -> E1={cuc_pm_to_zucchini}/{cuc_pm_n} ({cuc_pm_to_zucchini/max(1, cuc_pm_n)*100:.1f}%)")
    logger.info(f"Cucumber Confusions Breakdown   : {dict(cucumber_confusions.most_common(5))}")
    logger.info("=" * 80)

    # Decision Criteria Check
    criteria_met = (tomato_rec >= 0.70) and (tomato_to_potato <= 5) and (cucumber_rec >= 0.65) and (cuc_pm_to_zucchini / max(1, cuc_pm_n) < 0.40)
    logger.info(f"PRE-AGREED SUCCESS CRITERIA MET: {criteria_met}")
    if not criteria_met:
        logger.info("-> E1 criteria NOT met. Backbone fine-tuning (Stage 2) or targeted data acquisition is required.")
        logger.info("-> As instructed, stopping before Stage 2 backbone unfreezing to report findings.")

    # Export summary JSON
    summary = {
        "experiment": "model1_domain_shift_e1",
        "description": "Isolated classifier-head-only fine-tuning on existing training split with balanced loss weights",
        "checkpoint": str(BEST_MODEL_PATH),
        "train_duration_sec": round(train_duration, 2),
        "eval_duration_sec": round(eval_duration, 2),
        "overall_accuracy": {
            "baseline_e0": round(e0_acc, 4),
            "experiment_e1": round(overall_acc, 4),
            "delta": round(overall_acc - e0_acc, 4),
        },
        "original_22_accuracy": {
            "baseline_e0": round(orig_e0_acc, 4),
            "experiment_e1": round(orig_e1_acc, 4),
            "delta": round(orig_e1_acc - orig_e0_acc, 4),
        },
        "other_44_crops_accuracy": {
            "baseline_e0": round(other_e0_acc, 4),
            "experiment_e1": round(other_e1_acc, 4),
            "delta": round(other_e1_acc - other_e0_acc, 4),
        },
        "tomato": {
            "support": tomato_n,
            "baseline_recall": 0.2143,
            "e1_recall": round(tomato_rec, 4),
            "baseline_to_potato": 21,
            "e1_to_potato": tomato_to_potato,
            "confusions": dict(tomato_confusions.most_common(5)),
        },
        "cucumber": {
            "support": cucumber_n,
            "baseline_recall": 0.2456,
            "e1_recall": round(cucumber_rec, 4),
            "baseline_to_zucchini": 29,
            "e1_to_zucchini": cucumber_to_zucchini,
            "powdery_mildew_n": cuc_pm_n,
            "baseline_pm_to_zucchini": 20,
            "e1_pm_to_zucchini": cuc_pm_to_zucchini,
            "confusions": dict(cucumber_confusions.most_common(5)),
        },
        "criteria_met": criteria_met,
    }

    summary_json_path = REPORTS_DIR / "e1_evaluation_summary.json"
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    logger.info(f"Saved evaluation summary to {summary_json_path}")


if __name__ == "__main__":
    main()
