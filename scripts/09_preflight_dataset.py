"""Read-only preflight check for the updated Model 1 dataset.

Run this BEFORE training. It reports anything that would quietly
ruin a training run:

  - missing / empty class folders
  - classes that leak across train / val / test (content hashing)
  - unreadable or corrupt images
  - suspiciously tiny images
  - per-split and per-class counts, plus imbalance warnings

This script NEVER writes to the dataset. It only reads.

Usage
-----
    python scripts/09_preflight_dataset.py
    python scripts/09_preflight_dataset.py --dataset data\\final\\model1_updated
    python scripts/09_preflight_dataset.py --skip-hash
"""

import argparse
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image


# ============================================================
# DEFAULTS
# ============================================================

ROOT = Path(
    r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction"
)

DEFAULT_DATASET = (
    ROOT / "data" / "final" / "model1_updated"
)

SPLITS = ["train", "val", "test"]

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp"
}

# A class with fewer than this many TRAIN images will
# destabilise the WeightedRandomSampler.
MIN_TRAIN_PER_CLASS = 30

# Ratio of largest to smallest class. Above this the sampler
# is doing all the work and the big classes dominate the loss.
IMBALANCE_RATIO_WARN = 5.0

# Images whose shorter side is below this are almost always
# thumbnails, crops or broken downloads.
MIN_EDGE_WARN = 32


# ============================================================
# ARGS
# ============================================================

def parse_args():

    parser = argparse.ArgumentParser(
        description=(
            "Read-only preflight validation of the "
            "updated Model 1 dataset."
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
        "--skip-hash",
        action="store_true",
        help=(
            "Skip content hashing. Much faster, but "
            "cannot detect cross-split duplicates."
        )
    )

    parser.add_argument(
        "--sample-pixels",
        action="store_true",
        help=(
            "Also open every image to check dimensions "
            "and readability. Slower."
        )
    )

    return parser.parse_args()


# ============================================================
# HELPERS
# ============================================================

def iter_images(folder):

    if not folder or not folder.exists():

        return

    for path in sorted(folder.rglob("*")):

        if not path.is_file():

            continue

        if path.suffix.lower() in IMAGE_EXTENSIONS:

            yield path


def content_hash(path):

    digest = hashlib.sha256()

    with open(path, "rb") as handle:

        for chunk in iter(
            lambda: handle.read(1024 * 1024), b""
        ):

            digest.update(chunk)

    return digest.hexdigest()


def relative(path, root):

    try:

        return str(
            path.relative_to(root)
        ).replace("\\", "/")

    except ValueError:

        return str(path)


def main():

    args = parse_args()

    dataset = args.dataset

    print()
    print("=" * 78)
    print("MODEL 1 DATASET PREFLIGHT (read-only)")
    print("=" * 78)

    print(f"  dataset : {dataset}")

    if not dataset.exists():

        print()
        print("  DATASET NOT FOUND.")
        print()
        print("  Build it first:")
        print()
        print("      python scripts/02_build_model1_39.py")
        print()

        return 1

    # --------------------------------------------------------
    # Collect
    # --------------------------------------------------------

    counts = defaultdict(int)

    hashes = defaultdict(set)

    bad_images = []

    small_images = []

    class_dirs = defaultdict(dict)

    for split in SPLITS:

        split_dir = dataset / split

        if not split_dir.exists():

            print()
            print(f"  MISSING SPLIT: {split_dir}")

            continue

        for class_dir in sorted(
            split_dir.iterdir()
        ):

            if not class_dir.is_dir():

                continue

            class_name = class_dir.name

            class_dirs[class_name][split] = class_dir

            for image_path in iter_images(class_dir):

                counts[(split, class_name)] += 1

                if not args.skip_hash:

                    try:

                        digest = content_hash(
                            image_path
                        )

                    except OSError as exc:

                        bad_images.append(
                            (image_path, str(exc))
                        )

                        continue

                else:

                    # Cheap stand-in so the duplicate check
                    # still runs on name+size rather than
                    # nothing at all.
                    digest = (
                        f"{image_path.name}:"
                        f"{image_path.stat().st_size}"
                    )

                hashes[split].add((digest, class_name))

                if args.sample_pixels:

                    try:

                        with Image.open(
                            image_path
                        ) as im:

                            width, height = im.size

                        if min(width, height) < MIN_EDGE_WARN:

                            small_images.append(
                                (image_path, width, height)
                            )

                    except Exception as exc:

                        bad_images.append(
                            (image_path, str(exc))
                        )

    if not class_dirs:

        print()
        print("  No class folders found. Is the path right?")

        return 1

    # --------------------------------------------------------
    # Class table
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("PER-CLASS COUNTS")
    print("=" * 78)

    print(
        f"  {'class':<16}"
        f"{'train':>8}"
        f"{'val':>7}"
        f"{'test':>7}"
        f"{'total':>8}"
    )

    print("  " + "-" * 46)

    train_counts = {}

    for class_name in sorted(class_dirs):

        train_n = counts.get(("train", class_name), 0)
        val_n = counts.get(("val", class_name), 0)
        test_n = counts.get(("test", class_name), 0)

        train_counts[class_name] = train_n

        flag = ""

        if train_n == 0:

            flag = "  <-- NO TRAIN IMAGES"

        elif train_n < MIN_TRAIN_PER_CLASS:

            flag = "  <-- very low"

        print(
            f"  {class_name:<16}"
            f"{train_n:>8}"
            f"{val_n:>7}"
            f"{test_n:>7}"
            f"{train_n + val_n + test_n:>8}"
            f"{flag}"
        )

    totals = {
        split: sum(
            n for (s, _), n in counts.items()
            if s == split
        )
        for split in SPLITS
    }

    print()
    print(
        f"  {'TOTAL':<16}"
        f"{totals['train']:>8}"
        f"{totals['val']:>7}"
        f"{totals['test']:>7}"
        f"{sum(totals.values()):>8}"
    )

    print()
    print(f"  classes: {len(class_dirs)}")

    # --------------------------------------------------------
    # Leakage
    # --------------------------------------------------------

    warnings = []

    print()
    print("=" * 78)
    print("CROSS-SPLIT DUPLICATE CHECK")
    print("=" * 78)

    method = (
        "content hash (sha256)"
        if not args.skip_hash
        else "name+size (FAST, approximate)"
    )

    print(f"  method: {method}")

    overlap = 0

    for first, second in [
        ("train", "val"),
        ("train", "test"),
        ("val", "test"),
    ]:

        shared = {
            digest
            for digest, _ in hashes.get(first, set())
        } & {
            digest
            for digest, _ in hashes.get(second, set())
        }

        if shared:

            overlap += len(shared)

            print()
            print(
                f"  LEAK: {len(shared):,} identical image(s) "
                f"in both {first} and {second}"
            )

            warnings.append(
                f"{first}/{second} share {len(shared)} images"
            )

    if not overlap:

        print()
        print("  OK - no cross-split duplicates found.")

    # --------------------------------------------------------
    # Within-split duplicates
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("WITHIN-SPLIT DUPLICATES")
    print("=" * 78)

    dup_total = 0

    for split in SPLITS:

        seen = defaultdict(int)

        for digest, _class_name in hashes.get(split, set()):

            seen[digest] += 1

        duplicates = sum(
            count - 1
            for count in seen.values()
            if count > 1
        )

        dup_total += duplicates

        print(
            f"  {split:<6} {duplicates:,} repeated image(s)"
        )

        if duplicates:

            warnings.append(
                f"{split} has {duplicates} duplicates"
            )

    # --------------------------------------------------------
    # Imbalance
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("CLASS IMBALANCE (train)")
    print("=" * 78)

    nonzero = {
        k: v for k, v in train_counts.items()
        if v > 0
    }

    if nonzero:

        smallest = min(nonzero.values())
        largest = max(nonzero.values())

        ratio = largest / max(smallest, 1)

        small_name = min(nonzero, key=nonzero.get)
        big_name = max(nonzero, key=nonzero.get)

        print(f"  smallest : {smallest:,} ({small_name})")
        print(f"  largest  : {largest:,} ({big_name})")
        print(f"  ratio    : {ratio:.1f}x")

        if ratio > IMBALANCE_RATIO_WARN:

            print()
            print(
                f"  WARN: ratio above {IMBALANCE_RATIO_WARN}x. "
                f"The weighted sampler will dominate training."
            )

            warnings.append(
                f"imbalance ratio {ratio:.1f}x"
            )

    # --------------------------------------------------------
    # Image problems
    # --------------------------------------------------------

    if bad_images or small_images:

        print()
        print("=" * 78)
        print("IMAGE PROBLEMS")
        print("=" * 78)

        if bad_images:

            print(f"  unreadable: {len(bad_images)}")

            for path, reason in bad_images[:10]:

                print(
                    f"     {relative(path, dataset)}  {reason}"
                )

            warnings.append(
                f"{len(bad_images)} unreadable images"
            )

        if small_images:

            print(f"  tiny      : {len(small_images)}")

            for path, w, h in small_images[:10]:

                print(
                    f"     {relative(path, dataset)}  {w}x{h}"
                )

            warnings.append(
                f"{len(small_images)} tiny images"
            )

    # --------------------------------------------------------
    # Verdict
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)

    if not warnings:

        print()
        print("  PASS - dataset looks safe to train on.")
        print()
        print("  Train with:")
        print()
        print("      python scripts/10_train_model1_updated.py")

    else:

        print()
        print(f"  {len(warnings)} warning(s):")

        for item in warnings:

            print(f"     - {item}")

        print()
        print(
            "  Training is still possible, but review the "
            "items above first."
        )

    print()

    return 0


if __name__ == "__main__":

    sys.exit(main())