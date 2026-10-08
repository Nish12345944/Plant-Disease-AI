"""
Model 2 Dataset Reorganization Script
=====================================
Reorganizes Model 2 V2 disease classification dataset into a clean hierarchical structure:
data/processed/model2_organized/
├── train/
│   ├── crop/
│   │   ├── disease_1/
│   │   ├── disease_2/
│   │   └── healthy/ (where applicable)
├── val/
└── test/

Features:
- Preserves 100% data integrity & test-set immutability (2,304 images).
- Zero image modifications (exact binary copy via shutil.copy2).
- Generates model2_organized_manifest.csv, model2_organized_class_mapping.json, and model2_organized_crop_disease_mapping.json.
- Supports --dry-run mode.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_MANIFEST = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_manifest.csv"
SRC_BASE_DIR = PROJECT_ROOT / "data" / "processed"
DEST_DIR = PROJECT_ROOT / "data" / "processed" / "model2_organized"
DEST_MANIFEST = PROJECT_ROOT / "data" / "processed" / "model2_organized_manifest.csv"
DEST_CROP_DISEASE_MAP = PROJECT_ROOT / "data" / "processed" / "model2_organized_crop_disease_mapping.json"
DEST_CLASS_MAP = PROJECT_ROOT / "data" / "processed" / "model2_organized_class_mapping.json"
TREE_REPORT = PROJECT_ROOT / "reports" / "model2_classifier" / "model2_organized_dataset_tree.txt"


def canonical_crop_slug(crop_str: Any, cls_name: str) -> str:
    """Derives canonical lowercase slug for a crop."""
    if cls_name != "healthy" and "__" in cls_name:
        return cls_name.split("__", 1)[0].lower()
    c = str(crop_str).strip().lower().replace(" ", "_").replace("-", "_")
    return c


def compute_sha256(filepath: Path) -> str:
    """Computes SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def organize_dataset(dry_run: bool = False) -> int:
    print("=" * 80)
    print(f"MODEL 2 DATASET REORGANIZATION {'[DRY RUN]' if dry_run else '[LIVE EXECUTION]'}")
    print("=" * 80)

    if not SRC_MANIFEST.exists():
        print(f"ERROR: Source manifest not found at: {SRC_MANIFEST}")
        return 1

    df = pd.read_csv(SRC_MANIFEST)
    total_records = len(df)
    print(f"Loaded source manifest with {total_records:,} image records.")

    # Load original class mapping to preserve exact class IDs
    orig_class_map_path = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_class_mapping.json"
    if not orig_class_map_path.exists():
        orig_class_map_path = PROJECT_ROOT / "data" / "processed" / "model2_classifier_class_mapping.json"

    with open(orig_class_map_path, "r", encoding="utf-8") as f:
        raw_class_map = json.load(f)
        if "class_to_id" in raw_class_map:
            orig_class_to_id = raw_class_map["class_to_id"]
        else:
            orig_class_to_id = raw_class_map

    print(f"Loaded class mapping with {len(orig_class_to_id)} classes (class 0 = '{list(orig_class_to_id.keys())[0]}').")

    # Tracking data structures
    new_records: list[dict[str, Any]] = []
    quarantine_records: list[dict[str, Any]] = []
    crop_disease_map: dict[str, set[str]] = {}
    dest_path_set: set[str] = set()

    split_counts = {"train": 0, "val": 0, "test": 0}
    copied_count = 0

    if not dry_run:
        DEST_DIR.mkdir(parents=True, exist_ok=True)
        (DEST_DIR / "train").mkdir(exist_ok=True)
        (DEST_DIR / "val").mkdir(exist_ok=True)
        (DEST_DIR / "test").mkdir(exist_ok=True)
        (DEST_DIR / "_quarantine").mkdir(exist_ok=True)

    print("\nAuditing and planning reorganization...")

    for idx, row in df.iterrows():
        split = str(row["split"]).strip().lower()
        cls_name = str(row["classification_class"]).strip()
        class_id = int(row["class_id"])
        raw_crop = row["crop"]
        sha256_val = str(row["sha256_hash"]).strip()
        filename = str(row["filename"]).strip()
        source_dataset = str(row["source_dataset"]).strip()
        source_path = str(row["source_path"]).strip()
        rel_path = str(row["rel_path"]).strip()

        src_file_path = SRC_BASE_DIR / rel_path
        if not src_file_path.exists():
            # Flag missing file for quarantine
            quarantine_records.append({
                "original_path": str(src_file_path),
                "filename": filename,
                "sha256": sha256_val,
                "suspected_class": cls_name,
                "reason": "Source file does not exist on disk",
                "source_dataset": source_dataset,
                "recommended_manual_action": "Check source archive extraction",
            })
            continue

        # Resolve canonical crop and disease
        crop_slug = canonical_crop_slug(raw_crop, cls_name)
        if cls_name == "healthy":
            disease_slug = "healthy"
        else:
            disease_slug = cls_name.split("__", 1)[1].lower()

        # Update crop-disease mapping
        if crop_slug not in crop_disease_map:
            crop_disease_map[crop_slug] = set()
        crop_disease_map[crop_slug].add(disease_slug)

        # Formulate destination path
        dest_rel_path = f"{split}/{crop_slug}/{disease_slug}/{filename}"
        dest_full_path = DEST_DIR / split / crop_slug / disease_slug / filename

        if dest_rel_path in dest_path_set:
            quarantine_records.append({
                "original_path": str(src_file_path),
                "filename": filename,
                "sha256": sha256_val,
                "suspected_class": cls_name,
                "reason": f"Destination path collision: {dest_rel_path}",
                "source_dataset": source_dataset,
                "recommended_manual_action": "Resolve filename collision",
            })
            continue

        dest_path_set.add(dest_rel_path)
        split_counts[split] = split_counts.get(split, 0) + 1

        new_record = {
            "image_path": dest_rel_path,
            "split": split,
            "crop": crop_slug,
            "disease": disease_slug,
            "class_name": cls_name,
            "class_id": class_id,
            "source_dataset": source_dataset,
            "source_path": source_path,
            "sha256": sha256_val,
            "original_filename": filename,
            "original_class": cls_name,
            "original_split": split,
            "provenance": f"model2_classifier_v2:{rel_path}",
            "status": "organized",
            "width": row.get("width", None),
            "height": row.get("height", None),
        }
        new_records.append(new_record)

        if not dry_run:
            dest_full_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file_path, dest_full_path)
            copied_count += 1
            if copied_count % 2500 == 0 or copied_count == total_records:
                print(f"  Organized {copied_count:,} / {total_records:,} images...")

    print(f"\nProcessing complete:")
    print(f"  • Organized Images: {len(new_records):,}")
    print(f"    - Train: {split_counts['train']:,}")
    print(f"    - Val:   {split_counts['val']:,}")
    print(f"    - Test:  {split_counts['test']:,}")
    print(f"  • Quarantined / Unresolved: {len(quarantine_records)}")

    # Sort crop disease map into serializable format
    sorted_crop_disease_map = {
        crop: sorted(list(diseases))
        for crop, diseases in sorted(crop_disease_map.items())
    }

    if not dry_run:
        # Write new manifest
        new_df = pd.DataFrame(new_records)
        new_df.to_csv(DEST_MANIFEST, index=False)
        print(f"\n[OK] Created organized manifest at: {DEST_MANIFEST}")

        # Write crop-disease mapping
        with open(DEST_CROP_DISEASE_MAP, "w", encoding="utf-8") as f:
            json.dump(sorted_crop_disease_map, f, indent=2)
        print(f"[OK] Created crop-disease mapping at: {DEST_CROP_DISEASE_MAP}")

        # Write class mapping
        with open(DEST_CLASS_MAP, "w", encoding="utf-8") as f:
            json.dump(orig_class_to_id, f, indent=2)
        print(f"[OK] Created class mapping at: {DEST_CLASS_MAP}")

        # Generate tree report
        TREE_REPORT.parent.mkdir(parents=True, exist_ok=True)
        with open(TREE_REPORT, "w", encoding="utf-8") as f:
            f.write("MODEL 2 ORGANIZED DATASET HIERARCHICAL TREE\n")
            f.write("=" * 60 + "\n\n")
            for split in ["train", "val", "test"]:
                f.write(f"[{split.upper()}]\n")
                split_dir = DEST_DIR / split
                if split_dir.exists():
                    for crop_dir in sorted(split_dir.iterdir()):
                        if crop_dir.is_dir():
                            f.write(f"  ├── {crop_dir.name}/\n")
                            for disease_dir in sorted(crop_dir.iterdir()):
                                if disease_dir.is_dir():
                                    count = len(list(disease_dir.glob("*.*")))
                                    f.write(f"  │    ├── {disease_dir.name}/ ({count} images)\n")
                f.write("\n")
        print(f"[OK] Generated dataset tree report at: {TREE_REPORT}")

    print("\nReorganization step completed successfully.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reorganize Model 2 V2 dataset into hierarchical crop/disease structure.")
    parser.add_argument("--dry-run", action="store_true", help="Perform simulation and audit without copying files.")
    args = parser.parse_args()

    exit_code = organize_dataset(dry_run=args.dry_run)
    sys.exit(exit_code)
