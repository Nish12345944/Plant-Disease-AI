"""Train Model 1 on the UPDATED dataset (EfficientNet-B2).

Ready to run, but NOT run for you. Start it yourself tomorrow:

    python scripts/10_train_model1_updated.py

Everything is configurable, so you rarely need to edit the file:

    python scripts/10_train_model1_updated.py --epochs 30
    python scripts/10_train_model1_updated.py --batch-size 32
    python scripts/10_train_model1_updated.py --dry-run

Design notes
------------
* Uses AMP (mixed precision) - roughly 2x faster on the
  RTX 3050 with almost no accuracy cost.
* Cosine annealing instead of a flat LR, so the run settles.
* Saves the best checkpoint by validation accuracy, and
  also keeps a resume point each epoch so a crash does not
  lose the whole run.
* Writes a history.csv and a training_report.json so you
  can see per-class behaviour after it finishes.
* Refuses to train if the dataset is missing.
"""

import argparse
import csv
import json
import time
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import (
    DataLoader,
    WeightedRandomSampler
)
from torchvision import datasets, transforms
from torchvision.models import (
    EfficientNet_B2_Weights,
    efficientnet_b2
)


# ============================================================
# PATHS
# ============================================================

ROOT = Path(
    r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction"
)

DEFAULT_DATASET = (
    ROOT / "data" / "final" / "model1_updated"
)

MODEL_DIR = ROOT / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DEFAULT_MODEL_PATH = (
    MODEL_DIR / "model1_updated_efficientnet_b2.pth"
)

RUNS_DIR = MODEL_DIR / "runs"

RUNS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# ARGS
# ============================================================

def parse_args():

    parser = argparse.ArgumentParser(
        description=(
            "Train Model 1 (EfficientNet-B2) on the "
            "updated dataset."
        )
    )

    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET,
        help=(
            "Dataset root containing train/ val/ test/. "
            f"Default: {DEFAULT_DATASET}"
        )
    )

    parser.add_argument(
        "--model-out",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help=(
            "Where to save the final checkpoint. "
            f"Default: {DEFAULT_MODEL_PATH}"
        )
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=30
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=32
    )

    parser.add_argument(
        "--lr",
        type=float,
        default=3e-4,
        help="Initial learning rate."
    )

    parser.add_argument(
        "--weight-decay",
        type=float,
        default=1e-4
    )

    parser.add_argument(
        "--patience",
        type=int,
        default=7,
        help=(
            "Early stopping. Stop after this many "
            "epochs with no val improvement."
        )
    )

    parser.add_argument(
        "--image-size",
        type=int,
        default=224
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42
    )

    parser.add_argument(
        "--num-workers",
        type=int,
        default=4,
        help=(
            "0 is safest on Windows. Raise only if "
            "training stalls on data loading."
        )
    )

    parser.add_argument(
        "--no-amp",
        action="store_true",
        help="Disable mixed precision."
    )

    parser.add_argument(
        "--resume",
        type=Path,
        default=None,
        help=(
            "Resume from a checkpoint saved by a "
            "previous interrupted run."
        )
    )

    parser.add_argument(
        "--run-name",
        type=str,
        default=None,
        help=(
            "Name for this run's artefacts. "
            "Default: timestamped."
        )
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Load everything, build the model and the "
            "loaders, run ONE forward pass, then exit. "
            "Use this to validate the setup without "
            "committing to a full run."
        )
    )

    return parser.parse_args()


# ============================================================
# SEEDING
# ============================================================

def seed_everything(seed):

    import random

    random.seed(seed)

    torch.manual_seed(seed)

    torch.cuda.manual_seed_all(seed)

    # Deterministic cuDNN. Slower, but comparable runs.
    torch.backends.cudnn.deterministic = True

    torch.backends.cudnn.benchmark = False


# ============================================================
# TRANSFORMS
# ============================================================

def build_transforms(image_size):

    imagenet_mean = [
        0.485, 0.456, 0.406
    ]

    imagenet_std = [
        0.229, 0.224, 0.225
    ]

    train_transform = transforms.Compose([

        transforms.Resize(
            (image_size, image_size)
        ),

        transforms.RandomHorizontalFlip(),

        transforms.RandomVerticalFlip(),

        # Leaves and flowers benefit from mild rotation.
        transforms.RandomRotation(
            degrees=15
        ),

        transforms.ColorJitter(
            brightness=0.2,
            contrast=0.2,
            saturation=0.2,
            hue=0.05
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=imagenet_mean,
            std=imagenet_std
        ),

        transforms.RandomErasing(
            p=0.1,
            scale=(0.02, 0.1)
        ),
    ])

    eval_transform = transforms.Compose([

        transforms.Resize(
            (image_size, image_size)
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=imagenet_mean,
            std=imagenet_std
        ),
    ])

    return train_transform, eval_transform


# ============================================================
# MODEL
# ============================================================

def build_model(num_classes, use_pretrained):

    # Pretrained ImageNet weights transfer well to leaf and
    # flower photos, and cut training time significantly.
    weights = (
        EfficientNet_B2_Weights.DEFAULT
        if use_pretrained
        else None
    )

    model = efficientnet_b2(
        weights=weights
    )

    in_features = model.classifier[1].in_features

    model.classifier[1] = nn.Linear(
        in_features,
        num_classes
    )

    return model


# ============================================================
# TRAIN / EVAL
# ============================================================

def run_epoch(
    model,
    loader,
    criterion,
    device,
    scaler,
    optimizer=None,
):

    is_training = optimizer is not None

    model.train() if is_training else model.eval()

    total_loss = 0.0
    correct = 0
    total = 0

    # epoch-level TP/FP/FN per class
    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)

    for images, labels in loader:

        images = images.to(
            device,
            non_blocking=True
        )

        labels = labels.to(
            device,
            non_blocking=True
        )

        with torch.set_grad_enabled(
            is_training
        ):

            if is_training:

                optimizer.zero_grad(
                    set_to_none=True
                )

            with torch.autocast(
                device_type=device.type,
                enabled=scaler is not None,
            ):

                outputs = model(images)

                loss = criterion(
                    outputs, labels
                )

            if is_training:

                scaler.step(optimizer)

                scaler.update()

        batch_size = labels.size(0)

        total_loss += loss.item() * batch_size

        predictions = outputs.argmax(dim=1)

        correct += (
            predictions == labels
        ).sum().item()

        total += batch_size

        for p, t in zip(
            predictions.cpu().numpy(),
            labels.cpu().numpy()
        ):

            if p == t:

                tp[int(t)] += 1

            else:

                fp[int(p)] += 1
                fn[int(t)] += 1

    stats = {
        "loss": total_loss / max(total, 1),
        "accuracy": correct / max(total, 1),
        "tp": dict(tp),
        "fp": dict(fp),
        "fn": dict(fn),
    }

    return stats


def per_class_report(stats, class_names):

    rows = []

    for index, name in enumerate(class_names):

        t_p = stats["tp"].get(index, 0)
        f_p = stats["fp"].get(index, 0)
        f_n = stats["fn"].get(index, 0)

        support = t_p + f_n

        predicted = t_p + f_p

        precision = (
            t_p / (t_p + f_p)
            if (t_p + f_p) else 0.0
        )

        recall = (
            t_p / (t_p + f_n)
            if (t_p + f_n) else 0.0
        )

        f1 = (
            2 * precision * recall
            / (precision + recall)
            if (precision + recall) else 0.0
        )

        rows.append({
            "class": name,
            "support": support,
            "predicted": predicted,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        })

    return rows


def print_per_class(rows, title):

    print()
    print("-" * 78)
    print(title)
    print("-" * 78)

    print(
        f"  {'class':<16}"
        f"{'supp':>6}"
        f"{'prec':>7}"
        f"{'rec':>7}"
        f"{'f1':>7}"
    )

    for row in sorted(
        rows, key=lambda r: r["f1"]
    ):

        flag = ""

        if row["support"] == 0:

            flag = "  <-- never in test"

        elif row["recall"] == 0:

            flag = "  <-- never predicted"

        print(
            f"  {row['class']:<16}"
            f"{row['support']:>6}"
            f"{row['precision'] * 100:>6.1f}%"
            f"{row['recall'] * 100:>6.1f}%"
            f"{row['f1'] * 100:>6.1f}%"
            f"{flag}"
        )

    macro_f1 = (
        sum(r["f1"] for r in rows)
        / len(rows)
        if rows else 0.0
    )

    print()
    print(f"  macro F1 : {macro_f1 * 100:.2f}%")

    return macro_f1


# ============================================================
# MAIN
# ============================================================

def main():

    args = parse_args()

    seed_everything(args.seed)

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print()
    print("=" * 78)
    print("MODEL 1 - EFFICIENTNET-B2 (UPDATED DATASET)")
    print("=" * 78)

    print(f"  device       : {device}")

    if device.type == "cuda":

        print(f"  GPU          : {torch.cuda.get_device_name(0)}")
        print(f"  CUDA         : {torch.version.cuda}")

    print(f"  dataset      : {args.dataset}")
    print(f"  model out    : {args.model_out}")
    print(f"  epochs       : {args.epochs}")
    print(f"  batch size   : {args.batch_size}")
    print(f"  learning rate: {args.lr}")
    print(f"  patience     : {args.patience}")
    print(f"  amp          : {not args.no_amp}")

    # --------------------------------------------------------
    # Dataset check
    # --------------------------------------------------------

    splits = {}

    for split in ["train", "val", "test"]:

        path = args.dataset / split

        if not path.exists():

            print()
            print(f"  MISSING SPLIT: {path}")
            print()
            print(
                "  Build the updated dataset first, or point "
                "--dataset at an existing split layout:"
            )
            print()
            print(
                "      python scripts/10_train_model1_updated.py"
                " --dataset data\\final\\model1_39"
            )
            print()

            return 1

        splits[split] = path

    # --------------------------------------------------------
    # Datasets and transforms
    # --------------------------------------------------------

    train_transform, eval_transform = (
        build_transforms(args.image_size)
    )

    train_dataset = datasets.ImageFolder(
        root=str(splits["train"]),
        transform=train_transform
    )

    val_dataset = datasets.ImageFolder(
        root=str(splits["val"]),
        transform=eval_transform
    )

    test_dataset = datasets.ImageFolder(
        root=str(splits["test"]),
        transform=eval_transform
    )

    class_names = train_dataset.classes

    num_classes = len(class_names)

    print(f"  classes      : {num_classes}")
    print(f"  train images : {len(train_dataset):,}")
    print(f"  val images   : {len(val_dataset):,}")
    print(f"  test images  : {len(test_dataset):,}")

    if not class_names:

        print()
        print("  No classes found in the training split.")

        return 1

    # --------------------------------------------------------
    # Class balance table
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("CLASS BALANCE (train)")
    print("=" * 78)

    counts = defaultdict(int)

    for _path, label in train_dataset.samples:

        counts[label] += 1

    for index, name in enumerate(class_names):

        n = counts.get(index, 0)

        bar = "#" * min(40, int(n / 10))

        print(f"  {name:<16}{n:>6}  {bar}")

    smallest = min(counts.values())
    largest = max(counts.values())

    print()
    print(
        f"  imbalance ratio : "
        f"{largest / max(smallest, 1):.1f}x"
    )

    if smallest < 30:

        print()
        print(
            f"  WARN: smallest class has only {smallest} "
            f"image(s). Consider dropping it or sourcing "
            f"more data before training."
        )

    # --------------------------------------------------------
    # Loaders, model, optimiser
    # --------------------------------------------------------

    # Balance classes by sampling frequency.
    weights = [
        1.0 / counts.get(label, 1)
        for _path, label in train_dataset.samples
    ]

    sampler = WeightedRandomSampler(
        weights=weights,
        num_samples=len(weights),
        replacement=True
    )

    common = {
        "num_workers": args.num_workers,
        "pin_memory": device.type == "cuda",
    }

    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        sampler=sampler,
        drop_last=True,
        **common
    )

    eval_batch = max(
        args.batch_size // 2, 4
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=eval_batch,
        shuffle=False,
        **common
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=eval_batch,
        shuffle=False,
        **common
    )

    model = build_model(
        num_classes,
        use_pretrained=True
    )

    model = model.to(device)

    total_params = sum(
        p.numel() for p in model.parameters()
    )

    print()
    print(f"  parameters    : {total_params:,}")

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay
    )

    scheduler = (
        torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=args.epochs
        )
    )

    use_amp = (
        device.type == "cuda"
        and not args.no_amp
    )

    scaler = torch.amp.GradScaler(
        "cuda",
        enabled=use_amp
    )

    # --------------------------------------------------------
    # Dry run
    # --------------------------------------------------------

    if args.dry_run:

        print()
        print("=" * 78)
        print("DRY RUN - one forward pass only")
        print("=" * 78)

        images, labels = next(
            iter(train_loader)
        )

        images = images.to(device)
        labels = labels.to(device)

        with torch.no_grad():

            with torch.autocast(
                device_type=device.type,
                enabled=scaler.is_enabled(),
            ):

                output = model(images)
                loss = criterion(output, labels)

        print(f"  batch shape  : {tuple(images.shape)}")
        print(f"  output shape : {tuple(output.shape)}")
        print(f"  loss         : {loss.item():.4f}")
        print(f"  amp enabled  : {scaler.is_enabled()}")
        print(f"  classes      : {num_classes}")
        print()
        print("  Setup is valid. Nothing was trained or saved.")
        print()

        return 0

    # --------------------------------------------------------
    # Run artefacts
    # --------------------------------------------------------

    run_name = args.run_name or (
        time.strftime("run_%Y%m%d_%H%M%S")
    )

    run_dir = RUNS_DIR / run_name

    run_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    history_path = run_dir / "history.csv"
    resume_path = run_dir / "last_epoch.pth"
    best_path = run_dir / "best.pth"
    report_path = run_dir / "training_report.json"

    print()
    print(f"  run dir       : {run_dir}")

    start_epoch = 1
    best_val_accuracy = 0.0
    best_epoch = 0

    # Resume support
    if args.resume:

        if not args.resume.exists():

            print()
            print(f"  RESUME FILE NOT FOUND: {args.resume}")

            return 1

        state = torch.load(
            args.resume,
            map_location=device,
            weights_only=False
        )

        model.load_state_dict(state["model_state_dict"])
        optimizer.load_state_dict(state["optimizer_state_dict"])
        scheduler.load_state_dict(state["scheduler_state_dict"])

        start_epoch = state["epoch"] + 1
        best_val_accuracy = state.get(
            "best_val_accuracy", 0.0
        )
        best_epoch = state.get("best_epoch", 0)

        print(f"  resumed from  : {args.resume}")
        print(f"  start epoch   : {start_epoch}")

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("TRAINING")
    print("=" * 78)

    epochs_without_improvement = 0

    for epoch in range(
        start_epoch,
        args.epochs + 1
    ):

        epoch_start = time.time()

        lr_now = optimizer.param_groups[0]["lr"]

        print()
        print("-" * 78)
        print(
            f"EPOCH {epoch}/{args.epochs}"
            f"   lr={lr_now:.2e}"
        )
        print("-" * 78)

        train_stats = run_epoch(
            model,
            train_loader,
            criterion,
            device,
            scaler,
            optimizer=optimizer
        )

        val_stats = run_epoch(
            model,
            val_loader,
            criterion,
            device,
            scaler
        )

        elapsed = time.time() - epoch_start

        print(
            f"  train loss {train_stats['loss']:.4f}"
            f"   acc {train_stats['accuracy'] * 100:.2f}%"
        )
        print(
            f"  val   loss {val_stats['loss']:.4f}"
            f"   acc {val_stats['accuracy'] * 100:.2f}%"
        )
        print(f"  time {elapsed:.0f}s")

        scheduler.step()

        # Append to history
        write_header = (
            not history_path.exists()
        )

        with open(
            history_path,
            "a",
            newline="",
            encoding="utf-8"
        ) as handle:

            writer = csv.writer(handle)

            if write_header:

                writer.writerow([
                    "epoch", "lr", "train_loss",
                    "train_acc", "val_loss",
                    "val_acc", "seconds"
                ])

            writer.writerow([
                epoch,
                f"{lr_now:.8f}",
                f"{train_stats['loss']:.6f}",
                f"{train_stats['accuracy']:.6f}",
                f"{val_stats['loss']:.6f}",
                f"{val_stats['accuracy']:.6f}",
                f"{elapsed:.1f}",
            ])

        # Resume point every epoch
        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "best_val_accuracy": best_val_accuracy,
            "best_epoch": best_epoch,
        }, resume_path)

        # Track best
        if val_stats["accuracy"] > best_val_accuracy:

            best_val_accuracy = val_stats["accuracy"]
            best_epoch = epoch

            torch.save(model.state_dict(), best_path)

            print(
                f"  >>> new best val accuracy "
                f"{best_val_accuracy * 100:.2f}% (saved)"
            )

            epochs_without_improvement = 0

        else:

            epochs_without_improvement += 1

            print(
                f"  >>> no improvement "
                f"({epochs_without_improvement}/"
                f"{args.patience})"
            )

        if epochs_without_improvement >= args.patience:

            print()
            print("  Early stopping.")

            break

    # --------------------------------------------------------
    # Restore best, final test
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("FINAL TEST (best checkpoint)")
    print("=" * 78)

    if best_path.exists():

        model.load_state_dict(
            torch.load(
                best_path,
                map_location=device,
                weights_only=True
            )
        )

    test_stats = run_epoch(
        model,
        test_loader,
        criterion,
        device,
        scaler
    )

    print()
    print(f"  test loss     : {test_stats['loss']:.4f}")
    print(
        f"  test accuracy : "
        f"{test_stats['accuracy'] * 100:.2f}%"
    )
    print(
        f"  best val acc  : "
        f"{best_val_accuracy * 100:.2f}%"
    )
    print(f"  best epoch    : {best_epoch}")

    test_rows = per_class_report(
        test_stats, class_names
    )

    macro_f1 = print_per_class(
        test_rows,
        "PER-CLASS TEST RESULTS"
    )

    # --------------------------------------------------------
    # Save final model
    # --------------------------------------------------------

    args.model_out.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    torch.save({
        "model_state_dict": model.state_dict(),
        "class_names": class_names,
        "class_to_idx": train_dataset.class_to_idx,
        "num_classes": num_classes,
        "architecture": "efficientnet_b2",
        "image_size": args.image_size,
        "test_accuracy": test_stats["accuracy"],
        "best_val_accuracy": best_val_accuracy,
        "best_epoch": best_epoch,
        "macro_f1": macro_f1,
        "dataset": str(args.dataset),
        "trained_at": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }, args.model_out)

    report_path.write_text(
        json.dumps({
            "dataset": str(args.dataset),
            "num_classes": num_classes,
            "class_names": class_names,
            "train_images": len(train_dataset),
            "val_images": len(val_dataset),
            "test_images": len(test_dataset),
            "epochs_requested": args.epochs,
            "best_epoch": best_epoch,
            "best_val_accuracy": best_val_accuracy,
            "test_accuracy": test_stats["accuracy"],
            "macro_f1": macro_f1,
            "hyperparameters": {
                "batch_size": args.batch_size,
                "lr": args.lr,
                "weight_decay": args.weight_decay,
                "patience": args.patience,
                "image_size": args.image_size,
                "seed": args.seed,
                "amp": not args.no_amp,
            },
            "per_class_test": test_rows,
        }, indent=2),
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Done
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("TRAINING COMPLETE")
    print("=" * 78)

    print()
    print(f"  model   : {args.model_out}")
    print(f"  history : {history_path}")
    print(f"  report  : {report_path}")
    print()
    print(
        "  To use this model, point the upload app at "
        "it with --model, or update MODEL_PATH in "
        "05_model1_upload_test.py."
    )
    print()

    return 0


if __name__ == "__main__":

    raise SystemExit(main())