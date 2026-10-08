"""Read-only validation of the cleaned plant-part dataset and its split.

Checks, without writing anything:

  * the cleaned dataset uses the exact <plant>/<plant>_<part> layout
  * no empty plant / part folders were created
  * train + val + test counts add up to the cleaned dataset
  * every split file exists in the cleaned dataset
  * no sha256 or near-duplicate group spans more than one split
    (i.e. no train/val/test leakage)

Usage
-----
    python scripts/13_validate_plant_part_dataset.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
SOURCE = ROOT / "data" / "processed" / "plant_part_dataset"
SPLIT = ROOT / "data" / "processed" / "plant_part_dataset_split"
REPORTS = ROOT / "reports"
MANIFEST = REPORTS / "plant_part_dataset_manifest.json"
SUMMARY = REPORTS / "plant_part_dataset_summary.json"

SPLITS = ("train", "val", "test")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif",
                    ".tif", ".tiff"}


def scan_source(source):
    """Return (per-class counts, problems)."""
    counts = Counter()
    problems = []
    for plant_dir in sorted(p for p in source.iterdir() if p.is_dir()):
        plant = plant_dir.name
        part_dirs = [d for d in plant_dir.iterdir() if d.is_dir()]
        for stray in (f for f in plant_dir.iterdir() if f.is_file()):
            problems.append(f"loose file at plant level: {stray.name}")
        if not part_dirs:
            problems.append(f"empty plant folder: {plant}")
        for part_dir in part_dirs:
            if not part_dir.name.startswith(f"{plant}_"):
                problems.append(
                    f"bad part folder name: {plant}/{part_dir.name}")
            n = sum(1 for f in part_dir.iterdir()
                    if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS)
            if n == 0:
                problems.append(f"empty part folder: {plant}/{part_dir.name}")
            counts[f"{plant}/{part_dir.name}"] += n
    return counts, problems


def scan_split(split_root):
    """Return (class -> split -> count, file -> split, problems)."""
    per_class = defaultdict(Counter)
    file_split = {}
    problems = []
    for split in SPLITS:
        split_dir = split_root / split
        if not split_dir.is_dir():
            problems.append(f"missing split folder: {split}")
            continue
        for plant_dir in sorted(p for p in split_dir.iterdir() if p.is_dir()):
            for part_dir in sorted(
                p for p in plant_dir.iterdir() if p.is_dir()
            ):
                for image in part_dir.iterdir():
                    if not image.is_file():
                        problems.append(
                            f"unexpected entry: {split}/{plant_dir.name}/"
                            f"{part_dir.name}/{image.name}")
                        continue
                    key = f"{plant_dir.name}/{part_dir.name}"
                    per_class[key][split] += 1
                    rel = f"{plant_dir.name}/{part_dir.name}/{image.name}" \
                          .replace("\\", "/")
                    file_split[rel] = split
            for stray in (f for f in plant_dir.iterdir() if f.is_file()):
                problems.append(
                    f"loose file in split: {plant_dir.name}/{stray.name}")
    return per_class, file_split, problems


def main():
    print("=" * 78)
    print("PLANT-PART DATASET VALIDATION")
    print("=" * 78)

    failures = []

    # ---------------------------------------------------------- dataset
    print("\n[1] cleaned dataset layout")
    if not SOURCE.exists():
        print(f"  MISSING: {SOURCE}")
        return 1
    source_counts, source_problems = scan_source(SOURCE)
    total_source = sum(source_counts.values())
    plants = {key.split("/")[0] for key in source_counts}
    print(f"  plant folders : {len(plants)}")
    print(f"  part classes  : {len(source_counts)}")
    print(f"  images        : {total_source:,}")
    for problem in source_problems[:10]:
        print(f"  PROBLEM: {problem}")
    failures.extend(source_problems)

    # ------------------------------------------------------------ split
    print("\n[2] train/val/test layout")
    if not SPLIT.exists():
        print(f"  MISSING: {SPLIT}")
        return 1
    per_class, file_split, split_problems = scan_split(SPLIT)
    split_totals = Counter()
    for counts in per_class.values():
        split_totals.update(counts)
    total_split = sum(split_totals.values())
    for split in SPLITS:
        share = split_totals[split] / max(total_split, 1)
        print(f"  {split:<6} {split_totals[split]:>8,}  ({share:.1%})")
    print(f"  total    {total_split:>8,}")
    for problem in split_problems[:10]:
        print(f"  PROBLEM: {problem}")
    failures.extend(split_problems)

    # --------------------------------------------------------- integrity
    print("\n[3] counts agree")
    if total_split != total_source:
        message = (f"split total {total_split} != "
                   f"dataset total {total_source}")
        print(f"  PROBLEM: {message}")
        failures.append(message)
    else:
        print("  OK - split total matches the cleaned dataset")

    drift = []
    for key in source_counts:
        measured = sum(per_class.get(key, {}).values())
        if measured != source_counts[key]:
            drift.append((key, source_counts[key], measured))
    if drift:
        for key, expected, measured in drift[:10]:
            print(f"  PROBLEM: {key} dataset={expected} split={measured}")
        failures.append(f"{len(drift)} classes drifted")
    else:
        print("  OK - every class count matches per split")

    # ---------------------------------------------------------- leakage
    print("\n[4] leakage check (sha256 + near-dup group)")
    if not MANIFEST.exists():
        print(f"  MISSING manifest: {MANIFEST}")
        failures.append("manifest missing")
    else:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        sha_splits = defaultdict(set)
        group_splits = defaultdict(set)
        missing = 0
        for row in manifest:
            rel = row["output_path"].replace("\\", "/")
            split = file_split.get(rel)
            if split is None:
                missing += 1
                continue
            sha_splits[row["sha256"]].add(split)
            group_splits[row["group_id"]].add(split)

        leak_sha = [k for k, v in sha_splits.items() if len(v) > 1]
        leak_group = [k for k, v in group_splits.items() if len(v) > 1]
        print(f"  manifest entries        : {len(manifest):,}")
        print(f"  missing from split      : {missing}")
        print(f"  sha256 spanning splits  : {len(leak_sha)}")
        print(f"  groups spanning splits  : {len(leak_group)}")
        if missing:
            failures.append(f"{missing} manifest entries missing from split")
        if leak_sha:
            failures.append(
                f"{len(leak_sha)} duplicate hashes leak across splits")
        if leak_group:
            failures.append(
                f"{len(leak_group)} near-dup groups leak across splits")

    # ---------------------------------------------------------- summary
    print("\n[5] summary json")
    if not SUMMARY.exists():
        failures.append("summary json missing")
    else:
        summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
        final = summary["totals"]["final_images"]
        print(f"  reported final images : {final:,}")
        print(f"  measured images       : {total_source:,}")
        if final != total_source:
            failures.append("summary final_images does not match dataset")
        else:
            print("  OK")

    # ----------------------------------------------------------- verdict
    print()
    print("=" * 78)
    if failures:
        print(f"FAIL - {len(failures)} problem(s):")
        for item in failures[:20]:
            print(f"  - {item}")
        print("=" * 78)
        return 1

    print("PASS - dataset, split and leakage checks are all clean.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())


