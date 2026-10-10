import os
import sys
import json
import hashlib
from pathlib import Path
from collections import defaultdict
import pandas as pd

PROJECT_ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
MODEL2_V4_DIR = PROJECT_ROOT / "data" / "processed" / "model2_v4"
V4_MANIFEST_PATH = MODEL2_V4_DIR / "model2_v4_manifest.csv"

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    print("=" * 80)
    print("RECONCILING CURRENT MODEL 2 V4 DATASET VS AUTHORITATIVE V4 MANIFEST")
    print("=" * 80)

    # 1. Load Authoritative V4 Manifest
    df_manifest = pd.read_csv(V4_MANIFEST_PATH)
    print(f"Authoritative Manifest ({V4_MANIFEST_PATH.name}): {len(df_manifest):,} rows")
    print(f"  Manifest splits: {df_manifest['split'].value_counts().to_dict()}")
    print(f"  Manifest unique class_names: {df_manifest['class_name'].nunique()}")

    manifest_sha_map = {}
    manifest_path_map = {}
    for idx, r in df_manifest.iterrows():
        sha = str(r['sha256']).lower().strip()
        manifest_sha_map[sha] = r.to_dict()
        manifest_path_map[r['image_path']] = r.to_dict()

    # 2. Scan Current Disk Files
    records = []
    disk_sha_map = {}
    for s in ['train', 'val', 'test']:
        split_dir = MODEL2_V4_DIR / s
        for img_path in split_dir.glob('*/*/*.*'):
            if img_path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.webp']:
                continue
            crop = img_path.parent.parent.name
            disease = img_path.parent.name
            full_class = f"{crop}__{disease}"
            relpath = str(img_path.relative_to(MODEL2_V4_DIR)).replace('\\', '/')
            sha = compute_sha256(img_path).lower().strip()
            
            rec = {
                'image_path': relpath,
                'split': s,
                'crop': crop,
                'disease': disease,
                'class_name': full_class,
                'filename': img_path.name,
                'sha256': sha
            }
            records.append(rec)
            disk_sha_map[sha] = rec

    df_disk = pd.DataFrame(records)
    print(f"\nCurrent Disk Files: {len(df_disk):,} files")
    print(f"  Disk splits: {df_disk['split'].value_counts().to_dict()}")
    print(f"  Disk unique class_names: {df_disk['class_name'].nunique()}")

    # 3. Identify Added / Removed / Moved / Relabeled
    manifest_shas = set(manifest_sha_map.keys())
    disk_shas = set(disk_sha_map.keys())

    common_shas = manifest_shas.intersection(disk_shas)
    added_shas = disk_shas - manifest_shas
    removed_shas = manifest_shas - disk_shas

    print(f"\nHash Comparison:")
    print(f"  Common unchanged SHA-256: {len(common_shas):,}")
    print(f"  Newly added SHA-256 on disk: {len(added_shas):,}")
    print(f"  Removed SHA-256 (in manifest but not disk): {len(removed_shas):,}")

    # Inspect added images by class
    added_records = [disk_sha_map[s] for s in added_shas]
    df_added = pd.DataFrame(added_records)
    print(f"\nAdded images split breakdown:")
    print(df_added['split'].value_counts().to_dict())
    print(f"\nTop added classes on disk (total {df_added['class_name'].nunique()} added classes):")
    print(df_added['class_name'].value_counts().head(15))

    # Inspect moved splits
    moved_splits = []
    relabeled = []
    for s in common_shas:
        m_rec = manifest_sha_map[s]
        d_rec = disk_sha_map[s]
        if m_rec['split'] != d_rec['split']:
            moved_splits.append((s, m_rec['split'], d_rec['split'], m_rec['image_path'], d_rec['image_path']))
        if m_rec['class_name'] != d_rec['class_name']:
            relabeled.append((s, m_rec['class_name'], d_rec['class_name'], m_rec['image_path'], d_rec['image_path']))

    print(f"\nSplit Movements (same SHA, different split): {len(moved_splits)}")
    for item in moved_splits[:5]:
        print(f"  {item[0][:10]}: {item[1]} -> {item[2]} ({item[3]} -> {item[4]})")

    print(f"\nRelabeled Images (same SHA, different class_name): {len(relabeled)}")
    print(f"Sample relabeled:")
    for item in relabeled[:10]:
        print(f"  {item[0][:10]}: {item[1]} -> {item[2]}")

    # Check test set specifically
    m_test_shas = set(r['sha256'] for r in df_manifest[df_manifest['split'] == 'test'].to_dict(orient='records'))
    d_test_shas = set(r['sha256'] for r in df_disk[df_disk['split'] == 'test'].to_dict(orient='records'))

    test_exact_match = (m_test_shas == d_test_shas)
    print(f"\nTest Set Exact SHA Match between V4 manifest and Disk: {test_exact_match}")
    print(f"  Manifest test SHAs: {len(m_test_shas)}")
    print(f"  Disk test SHAs: {len(d_test_shas)}")
    print(f"  Difference: {len(m_test_shas.symmetric_difference(d_test_shas))}")

    # Check validation set specifically
    m_val_shas = set(r['sha256'] for r in df_manifest[df_manifest['split'] == 'val'].to_dict(orient='records'))
    d_val_shas = set(r['sha256'] for r in df_disk[df_disk['split'] == 'val'].to_dict(orient='records'))
    print(f"Val Set Exact SHA Match: {m_val_shas == d_val_shas}")

if __name__ == "__main__":
    main()
