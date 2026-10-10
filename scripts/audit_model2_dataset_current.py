import os
import sys
import json
import hashlib
from pathlib import Path
from collections import defaultdict
import pandas as pd
from PIL import Image

PROJECT_ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
MODEL2_V4_DIR = PROJECT_ROOT / "data" / "processed" / "model2_v4"
V4_MODEL_DIR = PROJECT_ROOT / "models" / "model2_classifier_v4"

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    print("=" * 80)
    print("MODEL 2 CURRENT DATASET AUDIT & RECONCILIATION")
    print("=" * 80)

    # 1. Load V4 Checkpoint Mapping & Config
    with open(V4_MODEL_DIR / "class_mapping.json") as f:
        v4_class_mapping = json.load(f)
    with open(V4_MODEL_DIR / "config.json") as f:
        v4_config = json.load(f)

    print(f"\n[1] V4 Historic Configuration:")
    print(f"  Architecture: {v4_config.get('architecture')}")
    print(f"  Trained num_classes: {v4_config.get('num_classes')}")
    print(f"  Historic splits: Train={v4_config.get('train_images')}, Val={v4_config.get('val_images')}, Test={v4_config.get('test_images')} (Total={v4_config.get('train_images',0)+v4_config.get('val_images',0)+v4_config.get('test_images',0)})")

    # 2. Check Existing Model 2 Manifests
    print(f"\n[2] Existing Manifests:")
    for mf in [
        PROJECT_ROOT / "data" / "processed" / "model2_classifier_manifest.csv",
        PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_manifest.csv",
        PROJECT_ROOT / "data" / "processed" / "model2_organized_manifest.csv"
    ]:
        if mf.exists():
            df = pd.read_csv(mf)
            print(f"  {mf.name}: {len(df):,} rows, splits: {df['split'].value_counts().to_dict()}")

    # 3. Scan Current Dataset on Disk
    print(f"\n[3] Scanning Current Disk Files in {MODEL2_V4_DIR}...")
    records = []
    sha_to_records = defaultdict(list)
    split_counts = defaultdict(int)
    class_split_counts = defaultdict(lambda: defaultdict(int))
    corrupted_images = []

    for s in ['train', 'val', 'test']:
        split_dir = MODEL2_V4_DIR / s
        if not split_dir.exists():
            continue
        for img_path in split_dir.glob('*/*/*.*'):
            if img_path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.webp']:
                continue
            crop = img_path.parent.parent.name
            disease = img_path.parent.name
            full_class = f"{crop}__{disease}"
            
            try:
                sha = compute_sha256(img_path)
            except Exception as e:
                corrupted_images.append((str(img_path), str(e)))
                continue

            rec = {
                'path': str(img_path),
                'relpath': str(img_path.relative_to(MODEL2_V4_DIR)),
                'split': s,
                'crop': crop,
                'disease': disease,
                'full_class': full_class,
                'filename': img_path.name,
                'sha256': sha
            }
            records.append(rec)
            sha_to_records[sha].append(rec)
            split_counts[s] += 1
            class_split_counts[full_class][s] += 1

    df_disk = pd.DataFrame(records)
    print(f"  Total Valid Images on Disk: {len(df_disk):,}")
    print(f"  Splits on Disk: {dict(split_counts)}")
    print(f"  Unique Classes on Disk: {df_disk['full_class'].nunique()}")
    print(f"  Corrupted files: {len(corrupted_images)}")

    # 4. Duplicate & Cross-Split Analysis
    print(f"\n[4] Duplicate & Cross-Split Leakage Audit:")
    exact_duplicate_hashes = {k: v for k, v in sha_to_records.items() if len(v) > 1}
    cross_split_leakage = []
    intra_split_duplicates = []
    
    for sha, instances in exact_duplicate_hashes.items():
        splits_involved = set(inst['split'] for inst in instances)
        if len(splits_involved) > 1:
            cross_split_leakage.append((sha, instances))
        else:
            intra_split_duplicates.append((sha, instances))

    print(f"  Total Duplicate Hash Groups: {len(exact_duplicate_hashes):,}")
    print(f"  Cross-Split Leakage Groups: {len(cross_split_leakage):,}")
    print(f"  Intra-Split Duplicate Groups: {len(intra_split_duplicates):,}")

    if cross_split_leakage:
        print("  Sample Cross-Split Leakage:")
        for sha, insts in cross_split_leakage[:5]:
            print(f"    Hash {sha[:10]}: {[i['relpath'] for i in insts]}")

    # 5. Taxonomy Comparison: V4 vs Disk
    print(f"\n[5] Taxonomy Reconcilation:")
    v4_classes = set(v4_class_mapping.keys())
    disk_classes = set(df_disk['full_class'].unique())

    matched_classes = v4_classes.intersection(disk_classes)
    only_in_v4 = v4_classes - disk_classes
    only_on_disk = disk_classes - v4_classes

    print(f"  Classes in both V4 and Disk: {len(matched_classes)}")
    print(f"  Classes in V4 but NOT on Disk ({len(only_in_v4)}): {only_in_v4}")
    print(f"  Classes on Disk but NOT in V4 ({len(only_on_disk)}): {sorted(list(only_on_disk))}")

    # 6. Check Split Imbalance & Zero-Support Classes
    print(f"\n[6] Class Split Support Summary:")
    train_only_classes = []
    test_missing_classes = []
    val_missing_classes = []
    for cls in sorted(disk_classes):
        cnts = class_split_counts[cls]
        tr = cnts.get('train', 0)
        va = cnts.get('val', 0)
        te = cnts.get('test', 0)
        if va == 0 and te == 0:
            train_only_classes.append((cls, tr))
        if te == 0:
            test_missing_classes.append((cls, tr, va))
        if va == 0:
            val_missing_classes.append((cls, tr, te))

    print(f"  Classes with TRAIN ONLY (0 Val, 0 Test) ({len(train_only_classes)}):")
    for cls, tr in train_only_classes[:10]:
        print(f"    {cls}: {tr} train")
    if len(train_only_classes) > 10:
        print(f"    ... and {len(train_only_classes)-10} more")

    print(f"  Total classes missing Test split: {len(test_missing_classes)}")
    print(f"  Total classes missing Val split: {len(val_missing_classes)}")

    # 7. Check Test Set Integrity vs V4 Historical Test Set
    print(f"\n[7] Historical Test Set Audit:")
    v4_test_count = v4_config.get('test_images', 2304)
    disk_test_count = split_counts.get('test', 0)
    print(f"  V4 config test images: {v4_test_count}")
    print(f"  Current disk test images: {disk_test_count}")

    # Save detailed class table to CSV in scratch
    class_rows = []
    for cls in sorted(disk_classes):
        cnts = class_split_counts[cls]
        class_rows.append({
            'full_class': cls,
            'in_v4_mapping': cls in v4_classes,
            'train_count': cnts.get('train', 0),
            'val_count': cnts.get('val', 0),
            'test_count': cnts.get('test', 0),
            'total_count': cnts.get('train', 0) + cnts.get('val', 0) + cnts.get('test', 0)
        })
    pd.DataFrame(class_rows).to_csv(PROJECT_ROOT / "reports" / "model2_retraining" / "model2_current_class_breakdown.csv", index=False)
    print(f"\nSaved detailed class breakdown to reports/model2_retraining/model2_current_class_breakdown.csv")

if __name__ == "__main__":
    main()
