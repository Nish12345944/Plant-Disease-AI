"""Train and Evaluate Model 1 Domain-Shift Experiment E2 (Controlled Top-Backbone Fine-Tuning).

Safety & Workflow Rules:
1. Architecture: EfficientNet-B2, 46 classes.
2. Fresh training initializes ONLY from models/model1_expanded/best_model.pth with strict compatibility check.
3. Lower backbone model.features[:6] FROZEN (requires_grad = False).
4. Upper backbone model.features[6:] UNFROZEN @ lr=2e-5.
5. Classifier head model.classifier[1] UNFROZEN @ lr=3e-4.
6. best_model.pth is kept EXCLUSIVELY for the best validation macro-F1 checkpoint.
7. recovery_checkpoint.pth is saved atomically after EVERY completed epoch, containing model state,
   optimizer state, completed epoch, best metrics, and RNG states.
8. Resume from recovery_checkpoint.pth is supported ONLY when explicitly requested (--resume).
   best_model.pth is NEVER loaded as a fallback resume checkpoint.
9. Logs and metrics write to a run-specific log and CSV file, preserving all previous logs.
"""

import argparse
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
SRC_MODEL_PATH = SRC_CHECKPOINT_DIR / "best_model.pth"
EXP_CHECKPOINT_DIR = ROOT / "models" / "model1_domain_shift_e2"
REPORTS_DIR = ROOT / "reports" / "model1_expansion" / "exp_domain_shift_e2"
DATASET_DIR = ROOT / "data" / "processed" / "model1_expanded"
FROZEN_BENCHMARK_CSV = ROOT / "reports" / "manual_prediction_failures" / "_e0_expandedM1_V4_benchmark.csv"

EXP_CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

BEST_MODEL_PATH = EXP_CHECKPOINT_DIR / "best_model.pth"
RECOVERY_CHECKPOINT_PATH = EXP_CHECKPOINT_DIR / "recovery_checkpoint.pth"
CONFIG_PATH = EXP_CHECKPOINT_DIR / "config.json"
CLASS_MAPPING_PATH = EXP_CHECKPOINT_DIR / "class_mapping.json"

# Copy verified class mapping to experiment directory if not present
if not CLASS_MAPPING_PATH.exists():
    shutil.copy2(SRC_CHECKPOINT_DIR / "class_mapping.json", CLASS_MAPPING_PATH)

# Canonical crop aliases
CANONICAL_ALIASES = {
    "capsicum": "bellpepper",
    "bell_pepper": "bellpepper",
    "bean": "french_bean",
    "squash": "zucchini",
    "cherry_tomato": "tomato",
}

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
LR_BACKBONE = 2e-5
LR_HEAD = 3e-4
WEIGHT_DECAY = 1e-4
BATCH_SIZE = 32
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def determine_run_id(explicit_id=None):
    """Determine run identifier while preserving existing logs and progress CSVs."""
    if explicit_id:
        return explicit_id
    if not (REPORTS_DIR / "training.log").exists():
        return "run1"
    # Find next available run id
    idx = 2
    while (REPORTS_DIR / f"training_run{idx}.log").exists():
        idx += 1
    return f"run{idx}"


def setup_logger(log_file_path):
    """Configure logger with regular flush to file and stdout."""
    logger = logging.getLogger(f"Model1_E2_Trainer_{log_file_path.stem}")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    stream_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def save_atomic_checkpoint(state, target_path):
    """Atomically save checkpoint using a temporary file and os.replace."""
    target_path = Path(target_path)
    temp_path = target_path.with_name(f".{target_path.name}.tmp")
    torch.save(state, temp_path)
    os.replace(temp_path, target_path)


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


def get_transforms():
    train_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])
    eval_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])
    return train_tf, eval_tf


def build_samples_list(split_dir, sorted_classes, class_to_idx):
    samples = []
    for c in sorted_classes:
        c_dir = split_dir / c
        if c_dir.exists():
            idx = class_to_idx[c]
            for p in sorted(c_dir.glob("*.jpg")):
                samples.append((str(p), idx))
    return samples


def parse_args():
    parser = argparse.ArgumentParser(description="Model 1 Experiment E2: Controlled Top-Backbone Fine-Tuning")
    parser.add_argument("--run-id", type=str, default=None, help="Identifier for training run (e.g. 'run2'). Default auto-increments to preserve existing logs.")
    parser.add_argument("--resume", action="store_true", help="Explicitly resume from recovery_checkpoint.pth. Error if recovery checkpoint does not exist.")
    return parser.parse_args()


def main():
    args = parse_args()
    set_seed(SEED)
    device = torch.device("cpu")
    torch.set_num_threads(8)

    # Determine run-specific paths
    run_id = determine_run_id(args.run_id)
    if run_id == "run1" and not (REPORTS_DIR / "training.log").exists():
        training_log_path = REPORTS_DIR / "training.log"
        progress_csv_path = REPORTS_DIR / "training_progress.csv"
    else:
        training_log_path = REPORTS_DIR / f"training_{run_id}.log"
        progress_csv_path = REPORTS_DIR / f"training_progress_{run_id}.csv"

    logger = setup_logger(training_log_path)

    def log_flush(msg, level=logging.INFO):
        logger.log(level, msg)
        for h in logger.handlers:
            h.flush()
        sys.stdout.flush()

    log_flush("=" * 80)
    log_flush(f"MODEL 1 EXPERIMENT E2: CONTROLLED TOP-BACKBONE FINE-TUNING (RUN: {run_id})")
    log_flush("=" * 80)
    log_flush(f"PyTorch Device: {device} | Active Threads: {torch.get_num_threads()}")
    log_flush(f"Seed: {SEED} | Epochs: {EPOCHS} | Batch Size: {BATCH_SIZE}")
    log_flush(f"LR Backbone (features[6:]): {LR_BACKBONE} | LR Classifier: {LR_HEAD} | WD: {WEIGHT_DECAY}")
    log_flush(f"Base Checkpoint: {SRC_MODEL_PATH}")
    log_flush(f"Best Model Path: {BEST_MODEL_PATH}")
    log_flush(f"Recovery Checkpoint Path: {RECOVERY_CHECKPOINT_PATH}")
    log_flush(f"Run-Specific Log: {training_log_path}")
    log_flush(f"Run-Specific Progress CSV: {progress_csv_path}")

    # 1. Load class mapping
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)
    class_to_idx = mapping_data["class_to_idx"]
    idx_to_class = {int(k): v for k, v in mapping_data["idx_to_class"].items()}
    mapping_aliases = mapping_data.get("aliases", {})
    all_aliases = {**mapping_aliases, **CANONICAL_ALIASES}
    sorted_classes = [idx_to_class[i] for i in range(len(class_to_idx))]
    num_classes = len(sorted_classes)
    assert num_classes == 46, f"Expected 46 classes, got {num_classes}"
    log_flush(f"Verified 46 classes from {CLASS_MAPPING_PATH}")

    # 2. Build datasets
    train_tf, eval_tf = get_transforms()
    train_samples = build_samples_list(DATASET_DIR / "train", sorted_classes, class_to_idx)
    val_samples = build_samples_list(DATASET_DIR / "val", sorted_classes, class_to_idx)
    log_flush(f"Dataset Partitions:")
    log_flush(f"  Train: {len(train_samples):,} samples (from data/processed/model1_expanded/train)")
    log_flush(f"  Val  : {len(val_samples):,} samples (from data/processed/model1_expanded/val)")
    log_flush(f"  Test & Frozen Benchmark: STRICTLY EXCLUDED from training split")

    train_loader = DataLoader(
        ImageListDataset(train_samples, transform=train_tf),
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0,
        pin_memory=False,
    )
    val_loader = DataLoader(
        ImageListDataset(val_samples, transform=eval_tf),
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
    )

    # 3. Class Imbalance Strategy (Smoothed Inverse-Frequency Loss Weights)
    train_labels_counts = Counter([s[1] for s in train_samples])
    active_counts = [cnt for cnt in train_labels_counts.values() if cnt > 0]
    median_cnt = float(np.median(active_counts))

    raw_weights = []
    for c_idx in range(num_classes):
        cnt = train_labels_counts.get(c_idx, 0)
        if cnt == 0:
            w = 1.0
        else:
            w = float(np.sqrt(median_cnt / cnt))
            w = max(0.5, min(2.0, w))
        raw_weights.append(w)

    raw_weights = np.array(raw_weights, dtype=np.float32)
    norm_weights = raw_weights / raw_weights.mean()
    loss_weights_tensor = torch.tensor(norm_weights, dtype=torch.float32).to(device)

    log_flush(f"Conservative loss weighting configured:")
    log_flush(f"  Range: [{norm_weights.min():.3f}, {norm_weights.max():.3f}], Mean: {norm_weights.mean():.3f}")
    criterion = nn.CrossEntropyLoss(weight=loss_weights_tensor)

    # 4. Model Architecture & Base Model Setup
    model = tvm.efficientnet_b2(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

    # 5. Parameter Freezing Scheme
    # Freeze lower backbone: features[:6]
    for p in model.features[:6].parameters():
        p.requires_grad = False

    # Unfreeze upper backbone: features[6:]
    for p in model.features[6:].parameters():
        p.requires_grad = True

    # Unfreeze classifier head
    for p in model.classifier.parameters():
        p.requires_grad = True

    model.to(device)

    # 6. Optimizer Setup
    param_groups = [
        {"params": [p for p in model.features[6:].parameters() if p.requires_grad], "lr": LR_BACKBONE, "weight_decay": WEIGHT_DECAY},
        {"params": [p for p in model.classifier.parameters() if p.requires_grad], "lr": LR_HEAD, "weight_decay": WEIGHT_DECAY},
    ]
    optimizer = torch.optim.AdamW(param_groups)

    def evaluate_validation(eval_model, loader):
        eval_model.eval()
        val_loss = 0.0
        y_true = []
        y_pred = []
        t0 = time.perf_counter()
        with torch.no_grad():
            for imgs, lbls in loader:
                imgs = imgs.to(device)
                lbls = lbls.to(device)
                logits = eval_model(imgs)
                loss = criterion(logits, lbls)
                val_loss += loss.item() * imgs.size(0)
                preds = logits.argmax(dim=1).cpu().numpy()
                y_true.extend(lbls.cpu().numpy())
                y_pred.extend(preds)
        val_loss /= len(loader.dataset)
        val_acc = np.mean(np.array(y_true) == np.array(y_pred))
        val_macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
        duration = time.perf_counter() - t0
        return val_loss, val_acc, val_macro_f1, duration

    # 7. Checkpoint Loading: Fresh vs. Explicit Resume
    start_epoch = 1
    best_val_f1 = 0.0
    best_epoch = 0

    if args.resume:
        # Strict requirement: resume ONLY from recovery_checkpoint.pth when explicitly requested
        log_flush("-" * 80)
        log_flush(f"EXPLICIT RESUME REQUESTED (--resume)")
        if not RECOVERY_CHECKPOINT_PATH.exists():
            err_msg = (
                f"Resume failed: recovery checkpoint does not exist at '{RECOVERY_CHECKPOINT_PATH}'.\n"
                f"Safety Rule: 'best_model.pth' stores the best validation model and is NEVER used as a resume checkpoint."
            )
            log_flush(f"ERROR: {err_msg}", level=logging.ERROR)
            raise FileNotFoundError(err_msg)

        log_flush(f"Loading recovery checkpoint: {RECOVERY_CHECKPOINT_PATH}")
        recovery_ckpt = torch.load(RECOVERY_CHECKPOINT_PATH, map_location="cpu", weights_only=False)

        model.load_state_dict(recovery_ckpt["model_state_dict"], strict=True)
        optimizer.load_state_dict(recovery_ckpt["optimizer_state_dict"])

        completed_epoch = recovery_ckpt["epoch"]
        start_epoch = completed_epoch + 1
        best_val_f1 = recovery_ckpt.get("best_val_f1", recovery_ckpt.get("val_macro_f1", 0.0))
        best_epoch = recovery_ckpt.get("best_epoch", completed_epoch)

        # Restore RNG states if available
        if "rng_state" in recovery_ckpt:
            rng = recovery_ckpt["rng_state"]
            if "torch" in rng and rng["torch"] is not None:
                torch.set_rng_state(rng["torch"])
            if "numpy" in rng and rng["numpy"] is not None:
                np.random.set_state(rng["numpy"])
            if "random" in rng and rng["random"] is not None:
                random.setstate(rng["random"])
            log_flush("Restored PyTorch, NumPy, and Python RNG states from recovery checkpoint.")

        log_flush(f"Resume Successful: Completed Epoch: {completed_epoch} | Next Epoch: {start_epoch} | Best Val Macro F1: {best_val_f1*100:.2f}% (Epoch {best_epoch})")
    else:
        # Fresh Initialization: STRICTLY load from models/model1_expanded/best_model.pth
        log_flush("-" * 80)
        log_flush(f"FRESH TRAINING INITIALIZATION (Source: {SRC_MODEL_PATH})")
        ckpt = torch.load(SRC_MODEL_PATH, map_location="cpu", weights_only=False)
        state_dict = ckpt["model_state_dict"] if isinstance(ckpt, dict) and "model_state_dict" in ckpt else ckpt

        model.load_state_dict(state_dict, strict=True)
        log_flush(f"Strict Checkpoint Compatibility Check PASSED: 0 missing keys, 0 unexpected keys")

        total_params = sum(p.numel() for p in model.parameters())
        frozen_params = sum(p.numel() for p in model.parameters() if not p.requires_grad)
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        backbone_trainable = sum(p.numel() for p in model.features[6:].parameters() if p.requires_grad)
        head_trainable = sum(p.numel() for p in model.classifier.parameters() if p.requires_grad)

        log_flush(f"Model Parameter Breakdown:")
        log_flush(f"  Total Parameters     : {total_params:,}")
        log_flush(f"  Frozen Parameters    : {frozen_params:,} ({frozen_params/total_params*100:.1f}%) [features[:6]]")
        log_flush(f"  Trainable Parameters : {trainable_params:,} ({trainable_params/total_params*100:.1f}%)")
        log_flush(f"    - Upper Backbone (features[6:]): {backbone_trainable:,} @ lr={LR_BACKBONE}")
        log_flush(f"    - Classifier Head (classifier) : {head_trainable:,} @ lr={LR_HEAD}")

        # Initialize progress CSV with header
        if not progress_csv_path.exists():
            with open(progress_csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "epoch", "total_epochs", "train_loss", "train_acc",
                    "val_loss", "val_acc", "val_macro_f1",
                    "lr_backbone", "lr_head", "duration_sec", "best_score", "is_best"
                ])

        # Step A: Evaluate Initial Model on Validation (Pre-training Baseline)
        log_flush("\n" + "=" * 80)
        log_flush("STEP A: PRE-TRAINING VALIDATION EVALUATION")
        log_flush("=" * 80)

        init_val_loss, init_val_acc, init_val_f1, init_val_time = evaluate_validation(model, val_loader)
        log_flush(f"Pre-training Val Loss: {init_val_loss:.4f} | Val Acc: {init_val_acc*100:.2f}% | Val Macro F1: {init_val_f1*100:.2f}% ({init_val_time:.1f}s)")

        best_val_f1 = init_val_f1
        best_epoch = 0

        # Save initial model as default best baseline if best_model.pth does not exist
        if not BEST_MODEL_PATH.exists():
            save_atomic_checkpoint({
                "epoch": 0,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_macro_f1": best_val_f1,
                "val_accuracy": init_val_acc,
            }, BEST_MODEL_PATH)
            log_flush(f"Initialized best checkpoint at {BEST_MODEL_PATH}")
        else:
            log_flush(f"Preserving existing best checkpoint at {BEST_MODEL_PATH}")

    # -----------------------------------------------------------------------
    # Step B: Controlled Fine-Tuning Loop
    # -----------------------------------------------------------------------
    log_flush("\n" + "=" * 80)
    log_flush(f"STEP B: TRAINING LOOP (EPOCHS {start_epoch} TO {EPOCHS})")
    log_flush("=" * 80)

    total_train_start = time.perf_counter()

    for epoch in range(start_epoch, EPOCHS + 1):
        epoch_start = time.perf_counter()
        model.train()
        # Keep frozen backbone in eval mode to prevent running stats drift in BatchNorm
        model.features[:6].eval()

        running_train_loss = 0.0
        train_correct = 0
        train_total = 0

        total_batches = len(train_loader)
        for batch_idx, (imgs, lbls) in enumerate(train_loader):
            imgs = imgs.to(device)
            lbls = lbls.to(device)

            optimizer.zero_grad()
            logits = model(imgs)
            loss = criterion(logits, lbls)
            loss.backward()
            optimizer.step()

            running_train_loss += loss.item() * imgs.size(0)
            preds = logits.argmax(dim=1)
            train_correct += (preds == lbls).sum().item()
            train_total += imgs.size(0)

            if (batch_idx + 1) % 50 == 0 or (batch_idx + 1) == total_batches:
                elapsed = time.perf_counter() - epoch_start
                cur_loss = running_train_loss / train_total
                cur_acc = train_correct / train_total
                log_flush(f"  [Epoch {epoch}/{EPOCHS}] Batch {batch_idx + 1:3d}/{total_batches} | Train Loss: {cur_loss:.4f} | Train Acc: {cur_acc*100:.2f}% | Elapsed: {elapsed:.1f}s")

        train_loss = running_train_loss / train_total
        train_acc = train_correct / train_total

        # Validation evaluation
        val_loss, val_acc, val_macro_f1, val_eval_time = evaluate_validation(model, val_loader)
        epoch_duration = time.perf_counter() - epoch_start

        is_best = False
        if val_macro_f1 > best_val_f1:
            best_val_f1 = val_macro_f1
            best_epoch = epoch
            is_best = True
            save_atomic_checkpoint({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_macro_f1": best_val_f1,
                "val_accuracy": val_acc,
            }, BEST_MODEL_PATH)
            status_str = f"*** NEW BEST CHECKPOINT SAVED (Val Macro F1: {best_val_f1*100:.2f}%) ***"
        else:
            status_str = f"No improvement (Best: {best_val_f1*100:.2f}% at epoch {best_epoch})"

        # Unconditionally save atomic recovery checkpoint after every completed epoch
        rng_state = {
            "torch": torch.get_rng_state(),
            "torch_cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
            "numpy": np.random.get_state(),
            "random": random.getstate(),
        }
        recovery_state = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "val_macro_f1": val_macro_f1,
            "val_accuracy": val_acc,
            "best_val_f1": best_val_f1,
            "best_epoch": best_epoch,
            "rng_state": rng_state,
        }
        save_atomic_checkpoint(recovery_state, RECOVERY_CHECKPOINT_PATH)
        log_flush(f"Saved atomic recovery checkpoint for Epoch {epoch} to {RECOVERY_CHECKPOINT_PATH}")

        log_flush(f"Epoch {epoch}/{EPOCHS} Finished in {epoch_duration:.1f}s:")
        log_flush(f"  Train Loss: {train_loss:.4f} | Train Acc: {train_acc*100:.2f}%")
        log_flush(f"  Val Loss  : {val_loss:.4f} | Val Acc  : {val_acc*100:.2f}% | Val Macro F1: {val_macro_f1*100:.2f}%")
        log_flush(f"  Status    : {status_str}")

        # Append to run-specific training_progress CSV
        with open(progress_csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                epoch, EPOCHS,
                round(train_loss, 4), round(train_acc, 4),
                round(val_loss, 4), round(val_acc, 4), round(val_macro_f1, 4),
                LR_BACKBONE, LR_HEAD,
                round(epoch_duration, 1), round(best_val_f1, 4), int(is_best)
            ])

    total_train_duration = time.perf_counter() - total_train_start
    log_flush(f"\nTraining Loop Complete in {total_train_duration:.1f}s. Best Epoch: {best_epoch} with Val Macro F1: {best_val_f1*100:.2f}%")

    # Save experiment config
    exp_config = {
        "experiment": "model1_domain_shift_e2",
        "run_id": run_id,
        "description": "Controlled top-backbone fine-tuning (features[6:] @ 2e-5, classifier @ 3e-4)",
        "base_checkpoint": str(SRC_MODEL_PATH),
        "best_epoch": best_epoch,
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "lr_backbone": LR_BACKBONE,
        "lr_head": LR_HEAD,
        "weight_decay": WEIGHT_DECAY,
        "seed": SEED,
        "best_val_macro_f1": round(best_val_f1, 4),
        "total_train_duration_sec": round(total_train_duration, 2),
        "checkpoint": str(BEST_MODEL_PATH),
        "recovery_checkpoint": str(RECOVERY_CHECKPOINT_PATH),
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(exp_config, f, indent=2)

    # -----------------------------------------------------------------------
    # Step C: Evaluate Best Checkpoint on Frozen Benchmark (2,304 images)
    # -----------------------------------------------------------------------
    log_flush("\n" + "=" * 80)
    log_flush("STEP C: EVALUATING BEST E2 CHECKPOINT ON FROZEN 2,304-IMAGE BENCHMARK")
    log_flush("=" * 80)

    # Load best checkpoint strictly for evaluation
    best_ckpt = torch.load(BEST_MODEL_PATH, map_location="cpu", weights_only=False)
    model.load_state_dict(best_ckpt["model_state_dict"])
    model.eval()

    benchmark_rows = list(csv.DictReader(open(FROZEN_BENCHMARK_CSV, encoding="utf-8")))
    log_flush(f"Loaded {len(benchmark_rows)} benchmark rows from {FROZEN_BENCHMARK_CSV}")

    # Canonical class lookup for Model 1 predictions
    canonical_class_lookup = {i: all_aliases.get(c, c) for i, c in idx_to_class.items()}

    evaluated_rows = []
    y_true_canonical = []
    y_pred_canonical = []

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

            # Canonical Ground Truth extracted strictly from folder path
            parts = Path(img_rel).parts
            test_idx = parts.index("test")
            folder_crop = parts[test_idx + 1]
            gt_crop = all_aliases.get(folder_crop, folder_crop)

            is_ok = int(pred_class == gt_crop)

            y_true_canonical.append(gt_crop)
            y_pred_canonical.append(pred_class)

            evaluated_rows.append({
                "image": img_rel,
                "folder_crop": folder_crop,
                "gt_crop": gt_crop,
                "actual_label": row.get("actual", ""),
                "e0_m1_crop": all_aliases.get(row.get("m1_crop", ""), row.get("m1_crop", "")),
                "e0_m1_ok": int(all_aliases.get(row.get("m1_crop", ""), row.get("m1_crop", "")) == gt_crop),
                "e2_m1_crop": pred_class,
                "e2_m1_conf": round(conf, 4),
                "e2_m1_ok": is_ok,
                "status": row.get("status", ""),
            })

            if (i + 1) % 500 == 0 or (i + 1) == len(benchmark_rows):
                log_flush(f"  Evaluated {i + 1}/{len(benchmark_rows)} benchmark images...")

    eval_duration = time.perf_counter() - t_eval_start
    log_flush(f"Benchmark evaluation complete in {eval_duration:.1f}s")

    # Save benchmark prediction CSV (both run-specific and canonical)
    for p in [REPORTS_DIR / f"benchmark_predictions_{run_id}.csv", REPORTS_DIR / "benchmark_predictions.csv"]:
        with open(p, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(evaluated_rows[0].keys()))
            writer.writeheader()
            writer.writerows(evaluated_rows)
    log_flush(f"Saved benchmark predictions to {REPORTS_DIR / 'benchmark_predictions.csv'}")

    # Overall Metrics Calculation
    all_classes_in_benchmark = sorted(list(set(y_true_canonical) | set(y_pred_canonical)))
    e2_overall_acc = sum(r["e2_m1_ok"] for r in evaluated_rows) / len(evaluated_rows)
    e0_overall_acc = sum(r["e0_m1_ok"] for r in evaluated_rows) / len(evaluated_rows)

    prec_per_class = precision_score(y_true_canonical, y_pred_canonical, labels=all_classes_in_benchmark, average=None, zero_division=0)
    rec_per_class = recall_score(y_true_canonical, y_pred_canonical, labels=all_classes_in_benchmark, average=None, zero_division=0)
    f1_per_class = f1_score(y_true_canonical, y_pred_canonical, labels=all_classes_in_benchmark, average=None, zero_division=0)
    cm = confusion_matrix(y_true_canonical, y_pred_canonical, labels=all_classes_in_benchmark)

    # Export per_class_metrics.csv
    for p in [REPORTS_DIR / f"per_class_metrics_{run_id}.csv", REPORTS_DIR / "per_class_metrics.csv"]:
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["crop", "precision", "recall", "f1_score", "support"])
            for idx, cls_name in enumerate(all_classes_in_benchmark):
                supp = sum(1 for y in y_true_canonical if y == cls_name)
                w.writerow([cls_name, round(prec_per_class[idx], 4), round(rec_per_class[idx], 4), round(f1_per_class[idx], 4), supp])
    log_flush(f"Saved per-class metrics to {REPORTS_DIR / 'per_class_metrics.csv'}")

    # Export confusion_matrix.csv
    for p in [REPORTS_DIR / f"confusion_matrix_{run_id}.csv", REPORTS_DIR / "confusion_matrix.csv"]:
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["actual_crop"] + all_classes_in_benchmark)
            for i, row in enumerate(cm):
                w.writerow([all_classes_in_benchmark[i]] + list(row))
    log_flush(f"Saved confusion matrix to {REPORTS_DIR / 'confusion_matrix.csv'}")

    # Target Confound Analysis:
    # 1. Tomato metrics
    tomato_rows = [r for r in evaluated_rows if r["gt_crop"] == "tomato"]
    tomato_n = len(tomato_rows)
    tomato_e0_corr = sum(r["e0_m1_ok"] for r in tomato_rows)
    tomato_e2_corr = sum(r["e2_m1_ok"] for r in tomato_rows)
    tomato_e0_rec = tomato_e0_corr / tomato_n if tomato_n else 0.0
    tomato_e2_rec = tomato_e2_corr / tomato_n if tomato_n else 0.0
    tomato_e0_to_potato = sum(1 for r in tomato_rows if r["e0_m1_crop"] == "potato")
    tomato_e2_to_potato = sum(1 for r in tomato_rows if r["e2_m1_crop"] == "potato")
    tomato_confusions = Counter([r["e2_m1_crop"] for r in tomato_rows if not r["e2_m1_ok"]])

    # 2. Cucumber metrics
    cucumber_rows = [r for r in evaluated_rows if r["gt_crop"] == "cucumber"]
    cucumber_n = len(cucumber_rows)
    cucumber_e0_corr = sum(r["e0_m1_ok"] for r in cucumber_rows)
    cucumber_e2_corr = sum(r["e2_m1_ok"] for r in cucumber_rows)
    cucumber_e0_rec = cucumber_e0_corr / cucumber_n if cucumber_n else 0.0
    cucumber_e2_rec = cucumber_e2_corr / cucumber_n if cucumber_n else 0.0
    cucumber_e0_to_zucchini = sum(1 for r in cucumber_rows if r["e0_m1_crop"] == "zucchini")
    cucumber_e2_to_zucchini = sum(1 for r in cucumber_rows if r["e2_m1_crop"] == "zucchini")
    cucumber_confusions = Counter([r["e2_m1_crop"] for r in cucumber_rows if not r["e2_m1_ok"]])

    # Cucumber powdery mildew
    cuc_pm_rows = [r for r in cucumber_rows if "powdery_mildew" in r["actual_label"]]
    cuc_pm_n = len(cuc_pm_rows)
    cuc_pm_e0_to_zucchini = sum(1 for r in cuc_pm_rows if r["e0_m1_crop"] == "zucchini")
    cuc_pm_e2_to_zucchini = sum(1 for r in cuc_pm_rows if r["e2_m1_crop"] == "zucchini")

    # 3. Original 22 classes regression check
    orig_22_canon = {all_aliases.get(c, c) for c in ORIGINAL_22_CLASSES}
    orig_rows = [r for r in evaluated_rows if r["gt_crop"] in orig_22_canon]
    orig_e0_acc = sum(r["e0_m1_ok"] for r in orig_rows) / len(orig_rows)
    orig_e2_acc = sum(r["e2_m1_ok"] for r in orig_rows) / len(orig_rows)

    # 4. Remaining classes non-regression check
    other_rows = [r for r in evaluated_rows if r["gt_crop"] not in ("tomato", "cucumber")]
    other_e0_acc = sum(r["e0_m1_ok"] for r in other_rows) / len(other_rows)
    other_e2_acc = sum(r["e2_m1_ok"] for r in other_rows) / len(other_rows)

    log_flush("\n" + "=" * 80)
    log_flush("FINAL EVALUATION COMPARISON: BASELINE (E0) VS EXPERIMENT (E2)")
    log_flush("=" * 80)
    log_flush(f"Overall Canonical Benchmark Accuracy: E0={e0_overall_acc*100:.2f}% (2088/2304) -> E2={e2_overall_acc*100:.2f}% ({sum(r['e2_m1_ok'] for r in evaluated_rows)}/2304) [delta: {(e2_overall_acc - e0_overall_acc)*100:+.2f}%]")
    log_flush(f"Original 22 Classes Accuracy         : E0={orig_e0_acc*100:.2f}% -> E2={orig_e2_acc*100:.2f}% [delta: {(orig_e2_acc - orig_e0_acc)*100:+.2f}%]")
    log_flush(f"Remaining Crops Accuracy (excl tom/cuc): E0={other_e0_acc*100:.2f}% -> E2={other_e2_acc*100:.2f}% [delta: {(other_e2_acc - other_e0_acc)*100:+.2f}%]")
    log_flush("-" * 80)
    log_flush(f"Tomato Recall (n={tomato_n})           : E0={tomato_e0_rec*100:.1f}% ({tomato_e0_corr}/{tomato_n}) -> E2={tomato_e2_rec*100:.1f}% ({tomato_e2_corr}/{tomato_n})")
    log_flush(f"Tomato -> Potato Errors              : E0={tomato_e0_to_potato} -> E2={tomato_e2_to_potato}")
    log_flush(f"Tomato Confusions Breakdown          : {dict(tomato_confusions.most_common(5))}")
    log_flush("-" * 80)
    log_flush(f"Cucumber Recall (n={cucumber_n})         : E0={cucumber_e0_rec*100:.1f}% ({cucumber_e0_corr}/{cucumber_n}) -> E2={cucumber_e2_rec*100:.1f}% ({cucumber_e2_corr}/{cucumber_n})")
    log_flush(f"Cucumber -> Zucchini Errors          : E0={cucumber_e0_to_zucchini}/{cucumber_n} -> E2={cucumber_e2_to_zucchini}/{cucumber_n}")
    log_flush(f"Cucumber PM -> Zucchini (n={cuc_pm_n})   : E0={cuc_pm_e0_to_zucchini}/{cuc_pm_n} ({cuc_pm_e0_to_zucchini/max(1, cuc_pm_n)*100:.1f}%) -> E2={cuc_pm_e2_to_zucchini}/{cuc_pm_n} ({cuc_pm_e2_to_zucchini/max(1, cuc_pm_n)*100:.1f}%)")
    log_flush(f"Cucumber Confusions Breakdown        : {dict(cucumber_confusions.most_common(5))}")
    log_flush("=" * 80)

    # Acceptance Criteria Check
    criteria_met = (
        (tomato_e2_rec >= 0.70) and
        (tomato_e2_to_potato <= 5) and
        (cucumber_e2_rec >= 0.65) and
        (cuc_pm_e2_to_zucchini / max(1, cuc_pm_n) < 0.40) and
        (e2_overall_acc >= e0_overall_acc - 0.01)
    )
    log_flush(f"PRE-AGREED SUCCESS CRITERIA MET: {criteria_met}")

    # Export summary JSON
    summary = {
        "experiment": "model1_domain_shift_e2",
        "run_id": run_id,
        "description": "Controlled top-backbone fine-tuning (features[6:] @ 2e-5, classifier @ 3e-4)",
        "checkpoint": str(BEST_MODEL_PATH),
        "recovery_checkpoint": str(RECOVERY_CHECKPOINT_PATH),
        "train_duration_sec": round(total_train_duration, 2),
        "eval_duration_sec": round(eval_duration, 2),
        "overall_canonical_accuracy": {
            "baseline_e0": round(e0_overall_acc, 4),
            "experiment_e2": round(e2_overall_acc, 4),
            "delta": round(e2_overall_acc - e0_overall_acc, 4),
        },
        "original_22_accuracy": {
            "baseline_e0": round(orig_e0_acc, 4),
            "experiment_e2": round(orig_e2_acc, 4),
            "delta": round(orig_e2_acc - orig_e0_acc, 4),
        },
        "remaining_crops_accuracy": {
            "baseline_e0": round(other_e0_acc, 4),
            "experiment_e2": round(other_e2_acc, 4),
            "delta": round(other_e2_acc - other_e0_acc, 4),
        },
        "tomato": {
            "support": tomato_n,
            "baseline_recall": round(tomato_e0_rec, 4),
            "e2_recall": round(tomato_e2_rec, 4),
            "baseline_to_potato": tomato_e0_to_potato,
            "e2_to_potato": tomato_e2_to_potato,
            "confusions": dict(tomato_confusions.most_common(5)),
        },
        "cucumber": {
            "support": cucumber_n,
            "baseline_recall": round(cucumber_e0_rec, 4),
            "e2_recall": round(cucumber_e2_rec, 4),
            "baseline_to_zucchini": cucumber_e0_to_zucchini,
            "e2_to_zucchini": cucumber_e2_to_zucchini,
            "powdery_mildew_n": cuc_pm_n,
            "baseline_pm_to_zucchini": cuc_pm_e0_to_zucchini,
            "e2_pm_to_zucchini": cuc_pm_e2_to_zucchini,
            "confusions": dict(cucumber_confusions.most_common(5)),
        },
        "criteria_met": criteria_met,
    }

    for p in [REPORTS_DIR / f"e2_evaluation_summary_{run_id}.json", REPORTS_DIR / "e2_evaluation_summary.json"]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
    log_flush(f"Saved summary to {REPORTS_DIR / 'e2_evaluation_summary.json'}")


if __name__ == "__main__":
    main()
