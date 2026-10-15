"""
Model 2 Retraining V2: Isolated Dataset Builder & Taxonomy Integration
======================================================================
Builds the canonicalized Model 2 Retraining V2 dataset under:
  data/processed/model2_retraining_v2/
  ├── train/{crop}/{disease}/
  ├── val/{crop}/{disease}/
  └── test/{crop}/{disease}/ (100% IMMUTABLE historical 2,304-image test benchmark)

Outputs:
  data/processed/model2_retraining_v2_manifest.csv
  data/processed/model2_retraining_v2/class_mapping.json (144 classes)
  data/processed/model2_retraining_v2/crop_disease_mapping.json

Strict Safety & Integrity Invariants:
1. Preserves 100% of historical V1/V4 test images (2,304) and existing train/val allocations.
2. Incorporates Tomato Anthracnose (Colletotrichum coccodes) as Class ID 143 (144 classes total).
3. Quarantines and excludes Tomato Fruit Fusarium Wilt due to pathological inconsistency.
4. Excludes 48 near-duplicate images matching protected test set (pHash <= 4).
5. Excludes 323 historical train duplicates from Blueberry healthy.
6. Excludes 213 cross-folder label collision images and 2 filename-conflicting early blight images.
7. Excludes 157 intra-folder duplicate copies.
8. Deterministic 85% train / 15% val partition for newly accepted clean images.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
RAW_ROOT = PROJECT_ROOT / "data" / "external" / "model2_new_data"
V1_DATASET_DIR = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v1"
V1_MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v1_manifest.csv"
V1_CLASS_MAPPING_PATH = V1_DATASET_DIR / "class_mapping.json"
V1_CROP_DISEASE_MAP_PATH = V1_DATASET_DIR / "crop_disease_mapping.json"

V2_DATASET_DIR = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v2"
V2_MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v2_manifest.csv"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_retraining_v2"

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def execute_v2_build():
    start_time = time.time()
    print("=" * 80)
    print("MODEL 2 RETRAINING V2: ISOLATED DATASET BUILD EXECUTION")
    print("=" * 80)
    print(f"Target Output Directory : {V2_DATASET_DIR}")
    print(f"Target Manifest         : {V2_MANIFEST_PATH}")
    print("=" * 80)

    # 1. Load V1 Base Mappings
    with open(V1_CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        v1_class_to_id = json.load(f)
    with open(V1_CROP_DISEASE_MAP_PATH, "r", encoding="utf-8") as f:
        crop_disease_map = json.load(f)

    # Construct 144-class mapping
    v2_class_to_id = dict(v1_class_to_id)
    if "tomato__anthracnose" not in v2_class_to_id:
        v2_class_to_id["tomato__anthracnose"] = len(v2_class_to_id)
        if "tomato" in crop_disease_map:
            if "anthracnose" not in crop_disease_map["tomato"]:
                crop_disease_map["tomato"].append("anthracnose")

    num_classes = len(v2_class_to_id)
    assert num_classes == 144, f"Expected 144 classes, got {num_classes}"
    print(f"[1/6] Configured V2 Taxonomy: exactly {num_classes} classes (Class 0: healthy, Class 143: tomato__anthracnose).")

    # 2. Read Duplicate Exclusion List from Audit
    dup_audit_csv = REPORTS_DIR / "duplicate_audit.csv"
    excluded_shas = set()
    if dup_audit_csv.exists():
        with open(dup_audit_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                excluded_shas.add(row["sha256"].lower().strip())
    print(f"[2/6] Loaded {len(excluded_shas):,} excluded/colliding SHA-256 hashes from audit.")

    # 3. Load V1 Historical Records
    print("[3/6] Ingesting V1 historical manifest records...")
    v1_records = []
    v1_shas = set()
    v1_split_counts = Counter()

    with open(V1_MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s = row["split"]
            v1_split_counts[s] += 1
            sha = row["sha256"].lower().strip()
            v1_shas.add(sha)

            # Assign class_id according to v2_class_to_id
            row["class_id"] = v2_class_to_id[row["canonical_class"]]
            row["source_abs_path"] = str(V1_DATASET_DIR / row["image_path"])
            v1_records.append(row)

    print(f"  V1 Historical Baseline: {len(v1_records):,} images (Train: {v1_split_counts['train']:,}, Val: {v1_split_counts['val']:,}, Test: {v1_split_counts['test']:,})")
    assert v1_split_counts["test"] == 2304, f"Test count must be 2304, got {v1_split_counts['test']}"

    # 4. Filter and Process New Accepted Images
    print("[4/6] Filtering and partitioning accepted clean images from data/external/model2_new_data...")

    folder_target_mapping = {
        "banana cigar end rot": ("banana__cigar_end_rot", "banana", "cigar_end_rot"),
        "Blueberry Fruit healthy": ("healthy", "blueberry", "healthy"),
        "broccoli alternaria leaf spot": ("broccoli__alternaria_leaf_spot", "broccoli", "alternaria_leaf_spot"),
        "broccoli downy mildew": ("broccoli__downy_mildew", "broccoli", "downy_mildew"),
        "broccoli healthy": ("healthy", "broccoli", "healthy"),
        "broccoli ring spot": ("broccoli__ring_spot", "broccoli", "ring_spot"),
        "celery anthracnose": ("celery__anthracnose", "celery", "anthracnose"),
        "eggplant phomopsis blight": ("eggplant__phomopsis_fruit_rot", "eggplant", "phomopsis_fruit_rot"),
        "eggplant_phomopsis": ("eggplant__phomopsis_fruit_rot", "eggplant", "phomopsis_fruit_rot"),
        "eggplant phytophthora spot": ("eggplant__phytophthora_blight", "eggplant", "phytophthora_blight"),
        "lettuce downy mildew": ("lettuce__downy_mildew", "lettuce", "downy_mildew"),
        "lettuce mosaic virus": ("lettuce__mosaic_virus", "lettuce", "mosaic_virus"),
        "early blight of tomato fruit": ("tomato__early_blight", "tomato", "early_blight"),
        "Late blight of tomato fruit": ("tomato__late_blight", "tomato", "late_blight"),
        "tomato fruit Anthracnose": ("tomato__anthracnose", "tomato", "anthracnose"),
        "tomato yellow curl virus": ("tomato__yellow_leaf_curl_virus", "tomato", "yellow_leaf_curl_virus"),
        # "tomato fruit fusarium wilt" is quarantined and omitted
    }

    # Files with explicit keyword conflicts in filename
    explicit_conflict_filenames = {
        "imgi_722_earlyblight2_600px.jpg",
        "imgi_750_7-17-Photo2_Early-blight-MARY.jpg",
        "imgi_759_earlyblight1_600px.jpg",
    }

    leaf_dirs = []
    for p in sorted(RAW_ROOT.rglob('*')):
        if p.is_dir() and not [x for x in p.iterdir() if x.is_dir()]:
            leaf_dirs.append(p)

    new_accepted_records = []
    seen_shas = set(v1_shas)

    for ld in leaf_dirs:
        folder_name = ld.name
        if "fusarium" in folder_name.lower():
            # Quarantined as approved
            continue

        matched_target = None
        for k, v in folder_target_mapping.items():
            if k in folder_name:
                matched_target = v
                break
        if not matched_target:
            continue

        c_class, c_crop, c_dis = matched_target
        c_id = v2_class_to_id[c_class]

        for f in sorted(ld.iterdir()):
            if not f.is_file():
                continue
            if f.name in explicit_conflict_filenames:
                continue

            sha = compute_sha256(f).lower().strip()
            if sha in excluded_shas or sha in seen_shas:
                continue
            seen_shas.add(sha)

            # Deterministic split allocation (85% train, 15% val based on sha hash)
            split_bucket = int(sha[:6], 16) % 100
            split = "val" if split_bucket < 15 else "train"

            # Create clean standardized filename: {sha[:10]}_{crop}_{disease}_{original_fname}
            clean_fname = f"{sha[:10]}_{f.name}"
            dest_relpath = f"{split}/{c_crop}/{c_dis}/{clean_fname}" if c_class != "healthy" else f"{split}/{c_crop}/healthy/{clean_fname}"

            new_accepted_records.append({
                "image_path": dest_relpath,
                "split": split,
                "split_provenance": f"v2_new_{split}",
                "canonical_class": c_class,
                "class_id": c_id,
                "crop": c_crop,
                "disease": c_dis if c_class != "healthy" else "healthy",
                "raw_class": f"{c_crop}__{folder_name}",
                "sha256": sha,
                "filename": clean_fname,
                "quality_status": "verified_valid",
                "source_abs_path": str(f),
            })

    print(f"  New Accepted Clean Images: {len(new_accepted_records):,}")
    new_train = sum(1 for r in new_accepted_records if r["split"] == "train")
    new_val = sum(1 for r in new_accepted_records if r["split"] == "val")
    print(f"    Train Additions (85%): {new_train:,}")
    print(f"    Val Additions (15%)  : {new_val:,}")
    print(f"    Test Additions       : 0 (Strictly Immutable)")

    # 5. Populate Dataset Directory in Parallel
    print("\n[5/6] Writing files to data/processed/model2_retraining_v2/...")
    if V2_DATASET_DIR.exists():
        shutil.rmtree(V2_DATASET_DIR)
    V2_DATASET_DIR.mkdir(parents=True, exist_ok=True)

    # Save Mappings
    with open(V2_DATASET_DIR / "class_mapping.json", "w", encoding="utf-8") as f:
        json.dump(v2_class_to_id, f, indent=2)
    with open(V2_DATASET_DIR / "crop_disease_mapping.json", "w", encoding="utf-8") as f:
        json.dump(crop_disease_map, f, indent=2)

    all_dataset_records = v1_records + new_accepted_records
    print(f"  Total Dataset Records to write: {len(all_dataset_records):,}")

    def copy_image_worker(rec):
        dest_file = V2_DATASET_DIR / rec["image_path"]
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        src_file = Path(rec["source_abs_path"])
        shutil.copy2(src_file, dest_file)
        return True

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(copy_image_worker, r) for r in all_dataset_records]
        for idx, fut in enumerate(as_completed(futures), start=1):
            fut.result()
            if idx % 5000 == 0 or idx == len(all_dataset_records):
                print(f"    Copied {idx:,} / {len(all_dataset_records):,} files...", flush=True)

    # 6. Write Final Manifest
    print("\n[6/6] Writing Manifest: data/processed/model2_retraining_v2_manifest.csv...")
    fieldnames = [
        "image_path",
        "split",
        "split_provenance",
        "canonical_class",
        "class_id",
        "crop",
        "disease",
        "raw_class",
        "sha256",
        "filename",
        "quality_status",
    ]

    with open(V2_MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in all_dataset_records:
            row_dict = {k: r[k] for k in fieldnames}
            writer.writerow(row_dict)

    elapsed_time = time.time() - start_time
    print(f"Dataset build completed in {elapsed_time:.2f} seconds.")

    # 7. Post-Build Integrity Validation
    print("\n" + "=" * 80)
    print("RUNNING POST-BUILD VALIDATION CHECKS...")
    print("=" * 80)

    # Check manifest exists and row count
    with open(V2_MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_rows = list(csv.DictReader(f))

    assert len(manifest_rows) == len(all_dataset_records), "Manifest row count mismatch!"
    splits_final = Counter(r["split"] for r in manifest_rows)
    classes_final = set(r["canonical_class"] for r in manifest_rows)

    print(f"✓ Manifest Total Records : {len(manifest_rows):,}")
    print(f"✓ Final Train Set Count   : {splits_final['train']:,}")
    print(f"✓ Final Validation Count : {splits_final['val']:,}")
    print(f"✓ Final Test Set Count   : {splits_final['test']:,} (EXACT 2,304 MATCH)")
    print(f"✓ Total Unique Classes   : {len(classes_final)} (EXACT 144 MATCH)")

    assert splits_final["test"] == 2304, f"FAIL: Test count {splits_final['test']} != 2304"
    assert len(classes_final) == 144, f"FAIL: Class count {len(classes_final)} != 144"

    # Verify all files exist on disk
    missing_files = []
    for r in manifest_rows:
        img_p = V2_DATASET_DIR / r["image_path"]
        if not img_p.exists():
            missing_files.append(r["image_path"])

    assert len(missing_files) == 0, f"FAIL: {len(missing_files)} missing files on disk!"
    print(f"✓ Disk File Resolution   : All {len(manifest_rows):,} manifest paths resolve to readable files.")

    # Verify no split leakage
    split_shas = defaultdict(set)
    for r in manifest_rows:
        split_shas[r["split"]].add(r["sha256"])

    leak_train_test = split_shas["train"] & split_shas["test"]
    leak_val_test = split_shas["val"] & split_shas["test"]
    leak_train_val = split_shas["train"] & split_shas["val"]

    assert len(leak_train_test) == 0, f"FAIL: Train-Test leak of {len(leak_train_test)} images!"
    assert len(leak_val_test) == 0, f"FAIL: Val-Test leak of {len(leak_val_test)} images!"
    assert len(leak_train_val) == 0, f"FAIL: Train-Val leak of {len(leak_train_val)} images!"
    print("✓ Split Leakage Check    : ZERO cross-split duplicate leakage detected across Train, Val, and Test.")

    print("\n" + "=" * 80)
    print("ALL VALIDATION CHECKS PASSED: MODEL 2 RETRAINING V2 READY FOR PREFLIGHT!")
    print("=" * 80)

if __name__ == "__main__":
    execute_v2_build()
