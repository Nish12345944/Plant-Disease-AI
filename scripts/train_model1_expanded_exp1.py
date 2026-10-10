"""EXP-1 — Two-Stage Transfer Learning Experiment for Expanded Model 1 (PREPARED, NOT EXECUTED).

Experiment Hypothesis (from reports/model1_expansion/expanded_model1_tuning_experiment_plan.md):
Full-backbone gradient updates from a randomly initialized linear head distort pretrained
ImageNet features. A two-stage schedule isolates head adaptation from backbone fine-tuning.

  STAGE 1 (Head Warmup)   : backbone FROZEN, train 46-class classifier head only.
                            4 epochs, AdamW lr=1e-3, weight_decay=1e-4, constant LR.
                            Backbone BatchNorm layers held in eval mode (running stats
                            and affine parameters stay at ImageNet values).
  STAGE 2 (Fine-Tune)     : ALL parameters unfrozen. Up to 10 epochs, AdamW lr=7e-5,
                            CosineAnnealingLR(T_max=10, eta_min=1e-6), early-stopping
                            patience 4 on validation Macro F1 (active classes).

Controlled-variable discipline (single-variable isolation vs Run 1 / EXP-0):
  HELD CONSTANT: dataset + splits, seed=42, ImageNet normalization, augmentations,
                 BATCH_SIZE=16 (4 GB RTX 3050 safe), WeightedRandomSampler (exp 0.20),
                 smoothed class-weighted CrossEntropyLoss (exp 0.35, 0.0 for gap
                 classes), AMP FP16, checkpoint metadata schema, AdamW weight decay.
  CHANGED (the single experimental factor): the optimization SCHEDULE (freeze policy
                 + staged learning rates + cosine decay in stage 2).

Checkpoint reuse decision (see expanded_model1_exp1_preflight.md):
  This experiment starts from `EfficientNet_B2_Weights.DEFAULT` with a FRESH random
  46-class head. It does NOT resume from models/model1_expanded/best_model.pth —
  that checkpoint stores only model weights (no optimizer/scheduler/scaler/RNG state),
  and its backbone is already co-adapted by single-stage training, which would
  confound the stage-1 hypothesis under test. The run-1 checkpoint remains the
  EXP-0 baseline for comparison.

Strict Safety Constraints:
- Training executes ONLY with the explicit `--run` flag. A bare invocation prints
  the EXP-1 preflight plan and exits without touching anything.
- Production models/model1/ and models/model2_classifier_v4/ are UNTOUCHED.
- Immutable test set is evaluated ONLY with the explicit `--evaluate-test` flag.
- All artifacts are isolated in models/model1_expanded/exp1/ and
  reports/model1_expansion/exp1/ — run-1 artifacts are never overwritten.
- 46-crop taxonomy unchanged. No dataset is downloaded, created, or modified.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import f1_score, precision_score, recall_score
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
from torchvision import transforms
from torchvision.models import EfficientNet_B2_Weights, efficientnet_b2

# ---------------------------------------------------------------------------
# Root and Paths (all outputs isolated to the exp1/ subdirectories)
# ---------------------------------------------------------------------------
ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DATASET_DIR = ROOT / "data" / "processed" / "model1_expanded"
MAPPING_PATH = ROOT / "data" / "processed" / "model1_expanded_class_mapping.json"

MODELS_EXP1_DIR = ROOT / "models" / "model1_expanded" / "exp1"
REPORTS_EXP1_DIR = ROOT / "reports" / "model1_expansion" / "exp1"

BEST_MODEL_PATH = MODELS_EXP1_DIR / "best_model_exp1.pth"
LAST_MODEL_PATH = MODELS_EXP1_DIR / "last_model_exp1.pth"
CONFIG_PATH = MODELS_EXP1_DIR / "config_exp1.json"
SUMMARY_PATH = MODELS_EXP1_DIR / "training_summary_exp1.json"

TRAINING_LOG_PATH = REPORTS_EXP1_DIR / "exp1_training.log"
TRAINING_METRICS_CSV = REPORTS_EXP1_DIR / "exp1_training_metrics.csv"
TEST_METRICS_CSV = REPORTS_EXP1_DIR / "exp1_test_metrics.csv"
PER_CLASS_METRICS_CSV = REPORTS_EXP1_DIR / "exp1_per_class_metrics.csv"

# ---------------------------------------------------------------------------
# EXP-1 Hyperparameters
# ---------------------------------------------------------------------------
IMAGE_SIZE = 224
BATCH_SIZE = 16                 # GPU-safe for 4 GB RTX 3050 laptop (unchanged from Run 1)
SEED = 42                       # Reproducibility (unchanged from Run 1)
WEIGHT_DECAY = 1e-4             # AdamW (unchanged from Run 1)

STAGE1_EPOCHS = 4               # Head warmup
STAGE1_LR = 1e-3                # ~1e-3 per experiment plan
STAGE2_EPOCHS = 10              # Fine-tune, up to 10 epochs
STAGE2_LR = 7e-5                # ~7e-5 per experiment plan
STAGE2_ETA_MIN = 1e-6           # Cosine decay floor
STAGE2_PATIENCE = 4             # Early stopping on val Macro F1 (active classes)

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Original 22 classes (identical definition across all scripts)
ORIGINAL_22_CLASSES = sorted([
    "anthurium", "blueberry", "broccoli", "bellpepper", "carnation", "cherry_tomato",
    "chrysanthemum", "cucumber", "french_bean", "geranium", "gerbera", "gypsophila",
    "lettuce", "lilium", "marigold", "melon", "orchid", "rose", "spinach",
    "strawberry", "tomato", "zucchini",
])

# Setup logger (file + console)
logger = logging.getLogger("EXP1Trainer")
logger.setLevel(logging.INFO)
_file_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_console_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")


def _ensure_dirs() -> None:
    MODELS_EXP1_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_EXP1_DIR.mkdir(parents=True, exist_ok=True)
    if not logger.handlers:
        fh = logging.FileHandler(TRAINING_LOG_PATH, mode="w", encoding="utf-8")
        ch = logging.StreamHandler(sys.stdout)
        fh.setFormatter(_file_fmt)
        ch.setFormatter(_console_fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)


def set_seed(seed: int = SEED) -> None:
    """Identical reproducibility discipline as Run 1."""
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class ExpandedPlantDataset(Dataset):
    """Dataset class for Expanded Model 1 (loads .jpg, .jpeg, .png case-insensitively with deduplication)."""

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
                # Bounded memory decoding: downscale multi-megapixel JPEGs directly during C libjpeg decode
                raw.draft("RGB", (448, 448))
            except Exception:
                pass
            img = raw.convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, target, path


# ---------------------------------------------------------------------------
# Two-stage helpers
# ---------------------------------------------------------------------------
def set_stage1(model: nn.Module) -> list[nn.Parameter]:
    """Freeze everything except the classifier head; return trainable params.

    EfficiencyNet-B2 components: model.features (blocks), model.conv_head,
    model.avgpool, model.classifier [Dropout, Linear]. Only `classifier.*`
    remains trainable — conv_head is part of the pretrained feature extractor
    and must stay frozen during head warmup (the run-1 plan's `model.features`
    snippet alone would leave conv_head unfrozen; this is the corrected form).
    """
    trainable = []
    for name, param in model.named_parameters():
        param.requires_grad = name.startswith("classifier.")
        if param.requires_grad:
            trainable.append(param)
    return trainable


def set_stage2(model: nn.Module) -> list[nn.Parameter]:
    """Unfreeze ALL parameters for full backbone fine-tuning."""
    for param in model.parameters():
        param.requires_grad = True
    return [p for p in model.parameters() if p.requires_grad]


def freeze_backbone_bn(model: nn.Module) -> None:
    """Put backbone BatchNorm layers in eval mode while the model trains.

    Called after model.train() during STAGE 1 so pretrained BN running stats
    and affine parameters are never perturbed by head-only updates.
    """
    for module in model.modules():
        if isinstance(module, (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d)):
            # classifier.* contains no BN; all EfficientNet BN lives in the backbone
            module.eval()


def build_model(num_classes: int) -> nn.Module:
    """Fresh ImageNet-pretrained EfficientNet-B2 with a NEW random 46-class head.

    Deliberately does NOT load Run 1's checkpoint (see module docstring).
    """
    model = efficientnet_b2(weights=EfficientNet_B2_Weights.DEFAULT)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    return model


def train_one_epoch(model, train_loader, criterion, optimizer, scaler, device, stage: str,
                    freeze_bn: bool) -> tuple[float, float, float, float]:
    """One training epoch with AMP (identical to Run 1, plus optional BN freeze)."""
    model.train()
    if freeze_bn:
        freeze_backbone_bn(model)  # keep backbone BN at ImageNet stats during stage 1

    loss_sum = 0.0
    preds_all: list[int] = []
    targets_all: list[int] = []

    for images, targets, _ in train_loader:
        images = images.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)
        with torch.amp.autocast("cuda", enabled=(device.type == "cuda")):
            outputs = model(images)
            loss = criterion(outputs, targets)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        loss_sum += loss.item() * targets.size(0)
        _, predicted = outputs.max(1)
        preds_all.extend(predicted.cpu().numpy())
        targets_all.extend(targets.cpu().numpy())

    train_loss = loss_sum / len(targets_all)
    train_acc = float(np.mean(np.array(targets_all) == np.array(preds_all)))
    train_macro = float(f1_score(targets_all, preds_all, average="macro", zero_division=0))
    train_weighted = float(f1_score(targets_all, preds_all, average="weighted", zero_division=0))
    return train_loss, train_acc, train_macro, train_weighted


def validate(model, val_loader, criterion, device, active_indices: list[int]) -> tuple[float, float, float, float]:
    """Validation. Primary selection metric = label-constrained Macro F1 over the
    ACTIVE classes (train support > 0, 44 classes) — zero_division=0, per the
    experiment plan ('label-constrained scikit-learn')."""
    model.eval()
    loss_sum = 0.0
    preds_all: list[int] = []
    targets_all: list[int] = []

    with torch.no_grad():
        for images, targets, _ in val_loader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)
            with torch.amp.autocast("cuda", enabled=(device.type == "cuda")):
                outputs = model(images)
                loss = criterion(outputs, targets)
            loss_sum += loss.item() * targets.size(0)
            _, predicted = outputs.max(1)
            preds_all.extend(predicted.cpu().numpy())
            targets_all.extend(targets.cpu().numpy())

    val_loss = loss_sum / len(targets_all)
    val_acc = float(np.mean(np.array(targets_all) == np.array(preds_all)))
    val_macro = float(f1_score(targets_all, preds_all, labels=active_indices, average="macro", zero_division=0))
    val_weighted = float(f1_score(targets_all, preds_all, labels=active_indices, average="weighted", zero_division=0))
    return val_loss, val_acc, val_macro, val_weighted


def run_exp1(evaluate_test: bool = False) -> dict:
    _ensure_dirs()
    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    logger.info("=" * 80)
    logger.info("EXP-1 — TWO-STAGE TRANSFER LEARNING (EfficientNet-B2, 46 classes)")
    logger.info(f"Device: {device} | Seed: {SEED} | Batch size: {BATCH_SIZE} (GPU-safe)")
    logger.info("Safety: production model1/ and model2_classifier_v4/ untouched; outputs isolated to exp1/.")
    logger.info("=" * 80)

    # 1. Taxonomy (read-only)
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)
    class_to_idx = mapping_data["class_to_idx"]
    idx_to_class = {int(k): v for k, v in mapping_data["idx_to_class"].items()}
    num_classes = len(class_to_idx)
    sorted_classes = [idx_to_class[i] for i in range(num_classes)]
    assert num_classes == 46, f"Expected 46 classes, got {num_classes}"
    assert (DATASET_DIR / "test").exists(), "Immutable test split directory missing"

    # 2. Transforms (IDENTICAL to Run 1 — augmentation is a held-constant variable)
    train_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15, hue=0.03),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])
    eval_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    train_dataset = ExpandedPlantDataset(DATASET_DIR / "train", sorted_classes, class_to_idx, transform=train_tf)
    val_dataset = ExpandedPlantDataset(DATASET_DIR / "val", sorted_classes, class_to_idx, transform=eval_tf)
    test_dataset = ExpandedPlantDataset(DATASET_DIR / "test", sorted_classes, class_to_idx, transform=eval_tf)
    
    # Validate against authoritative manifest if available
    manifest_csv = ROOT / "data" / "processed" / "model1_expanded_manifest.csv"
    if manifest_csv.exists():
        import pandas as pd
        df_man = pd.read_csv(manifest_csv)
        exp_train = len(df_man[df_man["split"] == "train"])
        exp_val = len(df_man[df_man["split"] == "val"])
        exp_test = len(df_man[df_man["split"] == "test"])
        assert len(train_dataset) == exp_train, f"Train set count mismatch: {len(train_dataset)} vs manifest {exp_train}"
        assert len(val_dataset) == exp_val, f"Val set count mismatch: {len(val_dataset)} vs manifest {exp_val}"
        assert len(test_dataset) == exp_test, f"Test set count mismatch: {len(test_dataset)} vs manifest {exp_test}"
    else:
        assert len(train_dataset) > 0, "Train set cannot be empty"
        assert len(val_dataset) > 0, "Val set cannot be empty"
        assert len(test_dataset) > 0, "Test set cannot be empty"
        
    logger.info(f"Dataset: train={len(train_dataset):,} val={len(val_dataset):,} test={len(test_dataset):,} "
                f"(test NOT touched unless --evaluate-test after training)")

    # 3. Class counts, ACTIVE indices, imbalance strategy (IDENTICAL to Run 1)
    from collections import Counter
    class_counts = Counter(t for _, t in train_dataset.samples)
    active_counts = [c for c in class_counts.values() if c > 0]
    median_cnt = float(np.median(active_counts))
    active_indices = sorted(i for i in range(num_classes) if class_counts.get(i, 0) > 0)
    gap_classes = [sorted_classes[i] for i in range(num_classes) if i not in active_indices]
    logger.info(f"Active train classes: {len(active_indices)}/{num_classes} "
                f"(zero-data gap classes: {gap_classes})")

    raw_loss_weights: dict[int, float] = {}
    for c_idx in range(num_classes):
        cnt = class_counts.get(c_idx, 0)
        if cnt > 0:
            raw_loss_weights[c_idx] = float(np.clip((median_cnt / max(cnt, 2)) ** 0.35, 0.3, 3.5))
        else:
            raw_loss_weights[c_idx] = 0.0  # gap classes (cherry_tomato, gypsophila) -> 0.0 loss weight
    active_mean = sum(v for v in raw_loss_weights.values() if v > 0) / max(1, sum(1 for v in raw_loss_weights.values() if v > 0))
    final_loss_weights = [raw_loss_weights[i] / active_mean if raw_loss_weights[i] > 0 else 0.0 for i in range(num_classes)]
    class_weights_tensor = torch.tensor(final_loss_weights, dtype=torch.float, device=device)

    raw_sample_weights = {
        c_idx: (float(np.clip((median_cnt / max(class_counts.get(c_idx, 0), 2)) ** 0.20, 0.4, 2.5))
                if class_counts.get(c_idx, 0) > 0 else 0.0)
        for c_idx in range(num_classes)
    }
    sample_weights = [raw_sample_weights[t] for _, t in train_dataset.samples]
    sampler = WeightedRandomSampler(sample_weights, num_samples=len(train_dataset), replacement=True)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, sampler=sampler, num_workers=0,
                              pin_memory=(device.type == "cuda"))
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0,
                            pin_memory=(device.type == "cuda"))
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0,
                             pin_memory=(device.type == "cuda"))

    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)
    model = build_model(num_classes).to(device)
    scaler = torch.amp.GradScaler("cuda", enabled=(device.type == "cuda"))

    # -------------------------------------------------------------------------
    # 4. STAGE 1 — Head warmup (backbone frozen), 4 epochs @ lr=1e-3
    # -------------------------------------------------------------------------
    trainable = set_stage1(model)
    optimizer = torch.optim.AdamW(trainable, lr=STAGE1_LR, weight_decay=WEIGHT_DECAY)
    scheduler = None  # constant LR during stage 1 (per experiment plan)

    logger.info("\n" + "=" * 80)
    logger.info(f"STAGE 1 — HEAD WARMUP: frozen backbone, {len(trainable)} trainable tensors "
                f"(classifier only), lr={STAGE1_LR:.0e}, epochs={STAGE1_EPOCHS}")
    logger.info("=" * 80)

    training_metrics_records: list[dict] = []
    best_val_macro = -1.0
    best_val_acc = -1.0
    best_epoch = 0
    best_stage = ""
    global_epoch = 0

    def run_stage(stage_tag: str, epochs: int, optimizer_, scheduler_, freeze_bn: bool,
                  patience: int | None, start_global: int) -> None:
        """Shared stage loop (best-checkpoint selection is global across stages)."""
        nonlocal best_val_macro, best_val_acc, best_epoch, best_stage, global_epoch
        patience_counter = 0
        for local_epoch in range(1, epochs + 1):
            t0 = time.time()
            global_epoch = start_global + local_epoch
            current_lr = optimizer_.param_groups[0]["lr"]

            train_loss, train_acc, train_macro, train_weighted = train_one_epoch(
                model, train_loader, criterion, optimizer_, scaler, device, stage_tag, freeze_bn)
            val_loss, val_acc, val_macro, val_weighted = validate(
                model, val_loader, criterion, device, active_indices)
            epoch_time = time.time() - t0
            gpu_mb = float(torch.cuda.max_memory_allocated() / (1024 ** 2)) if device.type == "cuda" else 0.0

            is_best = (val_macro > best_val_macro or
                       (np.isclose(val_macro, best_val_macro, atol=1e-4) and val_acc > best_val_acc))
            if is_best:
                best_val_macro, best_val_acc, best_epoch, best_stage = val_macro, val_acc, global_epoch, stage_tag
                patience_counter = 0
                torch.save({
                    "epoch": global_epoch, "stage": stage_tag, "experiment": "EXP-1",
                    "model_state_dict": model.state_dict(),
                    "val_macro_f1_active": val_macro, "val_accuracy": val_acc,
                    "val_weighted_f1_active": val_weighted, "val_loss": val_loss,
                    "class_to_idx": class_to_idx, "sorted_classes": sorted_classes,
                    "architecture": "efficientnet_b2", "image_size": IMAGE_SIZE,
                    "mean": IMAGENET_MEAN, "std": IMAGENET_STD,
                    "stage_config": {"stage1_lr": STAGE1_LR, "stage1_epochs": STAGE1_EPOCHS,
                                     "stage2_lr": STAGE2_LR, "stage2_epochs": STAGE2_EPOCHS,
                                     "stage2_eta_min": STAGE2_ETA_MIN, "weight_decay": WEIGHT_DECAY,
                                     "seed": SEED, "batch_size": BATCH_SIZE},
                }, BEST_MODEL_PATH)
            else:
                patience_counter += 1

            torch.save({
                "epoch": global_epoch, "stage": stage_tag, "experiment": "EXP-1",
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer_.state_dict(),
                "scheduler_state_dict": scheduler_.state_dict() if scheduler_ else None,
                "scaler_state_dict": scaler.state_dict(),
                "val_macro_f1_active": val_macro, "val_accuracy": val_acc, "val_loss": val_loss,
                "class_to_idx": class_to_idx, "sorted_classes": sorted_classes,
            }, LAST_MODEL_PATH)

            if scheduler_ is not None:
                scheduler_.step()

            training_metrics_records.append({
                "epoch": global_epoch, "stage": stage_tag, "learning_rate": round(current_lr, 7),
                "train_loss": round(train_loss, 4), "train_accuracy": round(train_acc, 4),
                "train_macro_f1": round(train_macro, 4), "train_weighted_f1": round(train_weighted, 4),
                "val_loss": round(val_loss, 4), "val_accuracy": round(val_acc, 4),
                "val_macro_f1_active": round(val_macro, 4), "val_weighted_f1_active": round(val_weighted, 4),
                "best_val_macro_f1_active": round(best_val_macro, 4), "best_epoch": best_epoch,
                "epoch_time_seconds": round(epoch_time, 1), "gpu_memory_mb": round(gpu_mb, 1),
            })

            star = " *** BEST CHECKPOINT ***" if is_best else ""
            logger.info(f"[{stage_tag} {local_epoch:02d}/{epochs:02d}] (global {global_epoch:02d}) | "
                        f"Train Loss {train_loss:.4f} Acc {train_acc*100:.2f}% | "
                        f"Val Loss {val_loss:.4f} Acc {val_acc*100:.2f}% F1a {val_macro*100:.2f}% | "
                        f"LR {current_lr:.2e} | {epoch_time:.1f}s | VRAM {gpu_mb:.0f}MB{star}")

            if patience is not None and patience_counter >= patience:
                logger.info(f"[Early Stopping] {stage_tag}: no val Macro F1 (active) improvement "
                            f"for {patience} epochs at global epoch {global_epoch}.")
                break

    # --- Stage 1 execution (fixed 4 epochs, no early stop) ---
    run_stage("S1", STAGE1_EPOCHS, optimizer, scheduler, freeze_bn=True, patience=None, start_global=0)

    # -------------------------------------------------------------------------
    # 5. STAGE 2 — Full fine-tune, up to 10 epochs @ lr=7e-5 cosine -> 1e-6
    # -------------------------------------------------------------------------
    trainable = set_stage2(model)
    optimizer = torch.optim.AdamW(trainable, lr=STAGE2_LR, weight_decay=WEIGHT_DECAY)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=STAGE2_EPOCHS,
                                                           eta_min=STAGE2_ETA_MIN)
    logger.info("\n" + "=" * 80)
    logger.info(f"STAGE 2 — FULL FINE-TUNE: all parameters trainable, lr={STAGE2_LR:.0e} cosine -> "
                f"{STAGE2_ETA_MIN:.0e}, epochs<={STAGE2_EPOCHS}, patience={STAGE2_PATIENCE}")
    logger.info("=" * 80)
    run_stage("S2", STAGE2_EPOCHS, optimizer, scheduler, freeze_bn=False,
              patience=STAGE2_PATIENCE, start_global=STAGE1_EPOCHS)

    # -------------------------------------------------------------------------
    # 6. Persist run artifacts (isolated in exp1/ — Run 1 artifacts untouched)
    # -------------------------------------------------------------------------
    logger.info(f"\nSaving training metrics to {TRAINING_METRICS_CSV}...")
    with open(TRAINING_METRICS_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["epoch", "stage", "learning_rate", "train_loss", "train_accuracy",
                      "train_macro_f1", "train_weighted_f1", "val_loss", "val_accuracy",
                      "val_macro_f1_active", "val_weighted_f1_active",
                      "best_val_macro_f1_active", "best_epoch", "epoch_time_seconds", "gpu_memory_mb"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(training_metrics_records)

    config_dict = {
        "experiment": "EXP-1 (Two-Stage Transfer Learning)",
        "model_architecture": "efficientnet_b2",
        "init_weights": "EfficientNet_B2_Weights.DEFAULT + fresh random 46-class head",
        "resume_from_run1_checkpoint": False,
        "num_classes": 46,
        "image_size": IMAGE_SIZE,
        "batch_size": BATCH_SIZE,
        "seed": SEED,
        "weight_decay": WEIGHT_DECAY,
        "stage1": {"epochs": STAGE1_EPOCHS, "lr": STAGE1_LR, "frozen": "all except classifier.*",
                   "bn_policy": "backbone BatchNorm kept in eval mode", "scheduler": "constant"},
        "stage2": {"epochs_max": STAGE2_EPOCHS, "lr": STAGE2_LR, "scheduler": "CosineAnnealingLR",
                   "eta_min": STAGE2_ETA_MIN, "patience": STAGE2_PATIENCE},
        "imbalance_strategy": "Held constant vs Run 1: WeightedRandomSampler(exp 0.20) + "
                              "Class-weighted CrossEntropyLoss(exp 0.35, 0.0 for gap classes)",
        "amp": True,
        "mean": IMAGENET_MEAN, "std": IMAGENET_STD,
        "train_samples": len(train_dataset), "val_samples": len(val_dataset),
        "test_samples": len(test_dataset),
        "test_evaluated": bool(evaluate_test),
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)

    summary = {
        "status": "COMPLETED",
        "experiment": "EXP-1",
        "best_epoch_global": best_epoch,
        "best_stage": best_stage,
        "best_val_macro_f1_active": round(best_val_macro, 4),
        "best_val_accuracy": round(best_val_acc, 4),
        "epochs_run": len(training_metrics_records),
        "acceptance_target_val_macro_f1": 0.8800,
        "test_results": None,
    }

    # -------------------------------------------------------------------------
    # 7. OPTIONAL test evaluation (gated: only with --evaluate-test)
    # -------------------------------------------------------------------------
    if evaluate_test:
        logger.info("\n[EXP-1] EVALUATING BEST CHECKPOINT ON IMMUTABLE TEST SET "
                    "(1,580 IMAGES, explicit --evaluate-test)")
        best_ckpt = torch.load(BEST_MODEL_PATH, map_location=device, weights_only=False)
        model.load_state_dict(best_ckpt["model_state_dict"])
        model.eval()

        t_targets, t_preds, t_probs = [], [], []
        with torch.no_grad():
            for images, targets, _ in test_loader:
                images = images.to(device, non_blocking=True)
                with torch.amp.autocast("cuda", enabled=(device.type == "cuda")):
                    probs = torch.softmax(model(images), dim=1)
                _, predicted = probs.max(1)
                t_targets.extend(targets.cpu().numpy())
                t_preds.extend(predicted.cpu().numpy())
                t_probs.extend(probs.cpu().numpy())
        t_targets = np.array(t_targets)
        t_preds = np.array(t_preds)
        top3 = np.argsort(np.array(t_probs), axis=1)[:, -3:]

        # CORRECTED label-constrained subset metrics (Task A methodology)
        orig_idx = sorted(class_to_idx[c] for c in ORIGINAL_22_CLASSES if c in class_to_idx)
        new_idx = sorted(set(range(num_classes)) - set(orig_idx))
        o_mask = np.isin(t_targets, orig_idx)
        n_mask = np.isin(t_targets, new_idx)
        o_sup = {i: int((t_targets[o_mask] == i).sum()) for i in orig_idx}
        o_act = [i for i in orig_idx if o_sup[i] > 0]
        o_zero = [sorted_classes[i] for i in orig_idx if o_sup[i] == 0]

        results = {
            "overall_46": {
                "top1": round(float((t_preds == t_targets).mean()), 4),
                "top3": round(float(np.mean([t_targets[i] in top3[i] for i in range(len(t_targets))])), 4),
                "macro_f1": round(float(f1_score(t_targets, t_preds, average="macro", zero_division=0)), 4),
                "weighted_f1": round(float(f1_score(t_targets, t_preds, average="weighted", zero_division=0)), 4),
            },
            "original_22": {
                "top1": round(float((t_preds[o_mask] == t_targets[o_mask]).mean()), 4),
                "top3": round(float(np.mean([t_targets[o_mask][i] in top3[o_mask][i] for i in range(int(o_mask.sum()))])), 4),
                "macro_f1_active": round(float(f1_score(t_targets[o_mask], t_preds[o_mask],
                                                        labels=o_act, average="macro", zero_division=0)), 4),
                "macro_f1_full": round(float(f1_score(t_targets[o_mask], t_preds[o_mask],
                                                      labels=orig_idx, average="macro", zero_division=0)), 4),
                "weighted_f1": round(float(f1_score(t_targets[o_mask], t_preds[o_mask],
                                                    labels=orig_idx, average="weighted", zero_division=0)), 4),
                "zero_support_classes": o_zero,
            },
            "new_24": {
                "top1": round(float((t_preds[n_mask] == t_targets[n_mask]).mean()), 4),
                "top3": round(float(np.mean([t_targets[n_mask][i] in top3[n_mask][i] for i in range(int(n_mask.sum()))])), 4),
                "macro_f1": round(float(f1_score(t_targets[n_mask], t_preds[n_mask],
                                                 labels=new_idx, average="macro", zero_division=0)), 4),
                "weighted_f1": round(float(f1_score(t_targets[n_mask], t_preds[n_mask],
                                                    labels=new_idx, average="weighted", zero_division=0)), 4),
            },
        }
        summary["test_results"] = results
        with open(TEST_METRICS_CSV, "w", newline="", encoding="utf-8") as f:
            rows = [{"subset": "OVERALL_46", **results["overall_46"]},
                    {"subset": "ORIGINAL_22", **results["original_22"]},
                    {"subset": "NEW_24", **results["new_24"]}]
            fieldnames = ["subset"] + [k for r in rows for k in r if k != "subset"]
            fieldnames = list(dict.fromkeys(fieldnames))  # ordered union
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"[EXP-1 TEST] overall={results['overall_46']}")
        logger.info(f"[EXP-1 TEST] orig22={results['original_22']}")
        logger.info(f"[EXP-1 TEST] new24={results['new_24']}")
    else:
        logger.info("[EXP-1] Test set NOT evaluated (default). Re-run with --evaluate-test only after "
                    "the candidate checkpoint has been selected on validation.")

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info("=" * 80)
    logger.info(f"EXP-1 FINISHED. Best: global epoch {best_epoch} ({best_stage}) | "
                f"Val Macro F1 (active) {best_val_macro*100:.2f}% | Val Acc {best_val_acc*100:.2f}%")
    logger.info(f"Acceptance target (Val Macro F1 >= 88.00%): "
                f"{'MET' if best_val_macro >= 0.88 else 'NOT MET'}")
    logger.info(f"Artifacts: {MODELS_EXP1_DIR} | {REPORTS_EXP1_DIR}")
    logger.info("=" * 80)
    return summary


# ---------------------------------------------------------------------------
# Preflight (default mode): prints the plan, runs safety checks, exits cleanly
# ---------------------------------------------------------------------------
def preflight() -> int:
    """Print the EXP-1 plan and run non-mutating readiness checks. Never trains."""
    print("=" * 80)
    print("EXP-1 PREFLIGHT — Two-Stage Transfer Learning (PREPARED, NOT EXECUTED)")
    print("=" * 80)
    print("""
Configuration
  Architecture : EfficientNet-B2 (ImageNet-1K pretrained) + fresh random 46-class head
  STAGE 1      : backbone FROZEN (all except classifier.*), BN held in eval,
                 AdamW lr=1e-3, weight_decay=1e-4, 4 epochs, constant LR
  STAGE 2      : full backbone unfrozen, AdamW lr=7e-5,
                 CosineAnnealingLR(T_max=10, eta_min=1e-6), up to 10 epochs,
                 early-stopping patience=4 on val Macro F1 (active classes)
  Held fixed   : seed=42, batch=16 (4 GB RTX 3050 safe), AMP FP16, ImageNet
                 normalization, Run-1 augmentations, WeightedRandomSampler(0.20)
                 + class-weighted CE(0.35, gap classes=0.0) — single-variable design
  Init policy  : ALWAYS fresh ImageNet weights; NEVER resumes run-1 checkpoint
                 (no optimizer/scheduler/scaler/RNG state in it; backbone already
                 co-adapted — would confound the stage-1 hypothesis)
  Outputs      : models/model1_expanded/exp1/ + reports/model1_expansion/exp1/
                 (run-1 artifacts and production models are never written)
  Test set     : evaluated ONLY with --evaluate-test (after checkpoint selection)
  Acceptance   : val Macro F1 (active) >= 88.00% vs EXP-0 baseline 86.63%
""")
    checks = {
        "dataset root exists": DATASET_DIR.exists(),
        "train split exists": (DATASET_DIR / "train").exists(),
        "val split exists": (DATASET_DIR / "val").exists(),
        "immutable test split exists": (DATASET_DIR / "test").exists(),
        "class mapping exists": MAPPING_PATH.exists(),
        "run-1 baseline checkpoint present (comparison only, NOT resumed)"
            : (ROOT / "models" / "model1_expanded" / "best_model.pth").exists(),
        "production Model 1 present (locked, must not be written)"
            : (ROOT / "models" / "model1" / "best_model.pth").exists(),
        "production Model 2 V4 present (locked, must not be written)"
            : (ROOT / "models" / "model2_classifier_v4" / "best_model.pth").exists(),
        "ImageNet-B2 weights cached locally (no download needed)"
            : (Path.home() / ".cache" / "torch" / "hub" / "checkpoints"
               / "efficientnet_b2_rwightman-c35c1473.pth").exists(),
        "torch importable": True,
    }
    try:
        import torch as _t  # noqa: F401
        checks["torch importable"] = True
    except Exception:
        checks["torch importable"] = False

    all_ok = True
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        all_ok = all_ok and ok

    # Non-training dataset-loading verification
    print("\nDataset Loading & Split Verification (Non-Training):")
    try:
        with open(MAPPING_PATH, "r", encoding="utf-8") as f:
            mapping_data = json.load(f)
        class_to_idx = mapping_data["class_to_idx"]
        idx_to_class = {int(k): v for k, v in mapping_data["idx_to_class"].items()}
        num_classes = len(class_to_idx)
        sorted_classes = [idx_to_class[i] for i in range(num_classes)]

        ds_train = ExpandedPlantDataset(DATASET_DIR / "train", sorted_classes, class_to_idx)
        ds_val = ExpandedPlantDataset(DATASET_DIR / "val", sorted_classes, class_to_idx)
        ds_test = ExpandedPlantDataset(DATASET_DIR / "test", sorted_classes, class_to_idx)
        
        from collections import Counter
        class_counts = Counter(t for _, t in ds_train.samples)
        active_indices = sorted(i for i in range(num_classes) if class_counts.get(i, 0) > 0)
        gap_classes = [sorted_classes[i] for i in range(num_classes) if i not in active_indices]

        print(f"  [PASS] Train dataset loaded: {len(ds_train):,} images")
        print(f"  [PASS] Val dataset loaded:   {len(ds_val):,} images")
        print(f"  [PASS] Test dataset loaded:  {len(ds_test):,} images")
        print(f"  [PASS] Total real images:    {len(ds_train) + len(ds_val) + len(ds_test):,} images")
        print(f"  [PASS] Active train classes: {len(active_indices)}/46 (Gap classes: {gap_classes})")
        print(f"  [PASS] Index 7: {idx_to_class[7]} | Index 20: {idx_to_class[20]}")

        manifest_csv = ROOT / "data" / "processed" / "model1_expanded_manifest.csv"
        if manifest_csv.exists():
            import pandas as pd
            df_man = pd.read_csv(manifest_csv)
            assert len(ds_train) == len(df_man[df_man["split"] == "train"]), "Train mismatch with manifest"
            assert len(ds_val) == len(df_man[df_man["split"] == "val"]), "Val mismatch with manifest"
            assert len(ds_test) == len(df_man[df_man["split"] == "test"]), "Test mismatch with manifest"
            print(f"  [PASS] Manifest alignment: 100% verified against {len(df_man):,} manifest records")
    except Exception as e:
        print(f"  [FAIL] Dataset loading test failed: {e}")
        all_ok = False

    print("\nTo EXECUTE (requires explicit consent):")
    print("  python scripts/train_model1_expanded_exp1.py --run")
    print("  python scripts/train_model1_expanded_exp1.py --run --evaluate-test")
    print("\nNo training, download, or data change has occurred in preflight mode.")
    print("=" * 80)
    return 0 if all_ok else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EXP-1 Two-Stage Transfer Learning (Expanded Model 1)")
    parser.add_argument("--run", action="store_true",
                        help="Execute EXP-1 training. Without this flag only the preflight plan is printed.")
    parser.add_argument("--evaluate-test", action="store_true",
                        help="After training, evaluate the selected checkpoint on the immutable test set.")
    args = parser.parse_args()

    if not args.run:
        sys.exit(preflight())
    sys.exit(0 if run_exp1(evaluate_test=args.evaluate_test)["status"] == "COMPLETED" else 1)








