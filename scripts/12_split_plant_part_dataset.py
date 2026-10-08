"""Build a second-level ML-ready split from the cleaned plant-part dataset.

Reads ``data/processed/plant_part_dataset`` and copies it into::

    data/processed/plant_part_dataset_split/
        train/<plant>/<plant>_<part>/
        val/<plant>/<plant>_<part>/
        test/<plant>/<plant>_<part>/

The split is stratified per (plant, part) class with an 80 / 10 / 10
ratio.  Near-duplicate groups (recorded by
``11_clean_organize_plant_parts.py``) are kept entirely inside a single
split so visually identical images cannot leak across splits.

Files are hard-linked when possible (fast, no extra disk use) and copied
otherwise.

Usage
-----
    python scripts/12_split_plant_part_dataset.py
    python scripts/12_split_plant_part_dataset.py --force --seed 42
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DEFAULT_SOURCE = ROOT / "data" / "processed" / "plant_part_dataset"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "plant_part_dataset_split"
DEFAULT_REPORTS = ROOT / "reports"

SPLITS = ("train", "val", "test")
RATIOS = {"train": 0.8, "val": 0.1, "test": 0.1}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif",
                    ".tif", ".tiff"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Stratified train/val/test split of the plant-part dataset."
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--reports", type=Path, default=DEFAULT_REPORTS)
    parser.add_argument("--manifest", type=Path, default=None,
                        help="Manifest JSON from script 11 (near-dup groups).")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def load_manifest(path):
    """Return ``{output_path: group_id}`` or an empty dict."""
    if path is None or not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {row["output_path"]: row.get("group_id") for row in data}


def collect_classes(source):
    """``(plant, part) -> [relative paths]`` discovered on disk."""
    classes = defaultdict(list)
    for plant_dir in sorted(p for p in source.iterdir() if p.is_dir()):
        plant = plant_dir.name
        for part_dir in sorted(p for p in plant_dir.iterdir() if p.is_dir()):
            for image in sorted(part_dir.iterdir()):
                if (image.is_file()
                        and image.suffix.lower() in IMAGE_EXTENSIONS):
                    classes[(plant, part_dir.name)].append(
                        image.relative_to(source)
                    )
    return classes


def split_class(rel_paths, group_of, rng):
    """Return ``{split: [rel_paths]}`` for one class.

    Near-duplicate groups are kept intact and assigned to whichever split
    is furthest below its target size.
    """
    groups = defaultdict(list)
    for index, rel in enumerate(rel_paths):
        key = str(rel).replace("\\", "/")
        groups[group_of.get(key, f"__{index}")].append(rel)

    group_list = [groups[key] for key in sorted(groups)]
    rng.shuffle(group_list)

    total = len(rel_paths)
    counts = {split: 0 for split in SPLITS}
    buckets = {split: [] for split in SPLITS}

    for members in group_list:
        size = len(members)
        best = max(
            SPLITS,
            key=lambda s: (RATIOS[s] * total - counts[s], -SPLITS.index(s)),
        )
        counts[best] += size
        buckets[best].extend(members)
    return buckets


def link_or_copy(src, dst):
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def main():
    args = parse_args()
    started = time.time()

    source = args.source
    output = args.output
    reports = args.reports
    reports.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        print(f"ERROR: source dataset not found: {source}")
        return 1
    if output.exists():
        if not args.force:
            print(f"ERROR: {output} already exists. Re-run with --force.")
            return 1
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    manifest_path = args.manifest or (
        reports / "plant_part_dataset_manifest.json"
    )
    group_of = load_manifest(manifest_path)

    print("=" * 78)
    print("PLANT-PART TRAIN/VAL/TEST SPLIT")
    print("=" * 78)
    print(f"source   : {source}")
    print(f"output   : {output}")
    print(f"manifest : {manifest_path} "
          f"({'loaded' if group_of else 'MISSING - groups ignored'})")
    print(f"seed     : {args.seed}")
    print()

    classes = collect_classes(source)
    split_counts = Counter()
    per_split_class = {split: Counter() for split in SPLITS}
    total_files = 0

    for (plant, part), rel_paths in sorted(classes.items()):
        class_rng = random.Random(f"{args.seed}-{plant}-{part}")
        buckets = split_class(rel_paths, group_of, class_rng)
        for split in SPLITS:
            for rel in buckets[split]:
                src = source / rel
                dst = output / split / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not dst.exists():
                    link_or_copy(src, dst)
                split_counts[split] += 1
                per_split_class[split][f"{plant}/{part}"] += 1
                total_files += 1

    elapsed = round(time.time() - started, 1)
    print(f"total files processed: {total_files:,}")
    print()
    for split in SPLITS:
        print(f"{split:<6}: {split_counts[split]:>8,}  "
              f"({split_counts[split] / max(total_files, 1):.1%})")

    print()
    print("PER-CLASS COUNTS (train / val / test)")
    header = f"{'class':<40}{'train':>8}{'val':>8}{'test':>8}"
    print(header)
    print("-" * len(header))
    for (plant, part) in sorted(classes):
        key = f"{plant}/{part}"
        print(f"{key:<40}"
              f"{per_split_class['train'][key]:>8}"
              f"{per_split_class['val'][key]:>8}"
              f"{per_split_class['test'][key]:>8}")

    summary = {
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": str(source),
        "output": str(output),
        "seed": args.seed,
        "ratios": RATIOS,
        "totals": dict(split_counts),
        "per_split_class": {
            split: dict(sorted(counts.items()))
            for split, counts in per_split_class.items()
        },
        "elapsed_seconds": elapsed,
    }
    out_json = reports / "plant_part_dataset_split_summary.json"
    out_json.write_text(json.dumps(summary, indent=1), encoding="utf-8")

    print()
    print(f"summary json : {out_json}")
    print(f"elapsed      : {elapsed}s")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())

