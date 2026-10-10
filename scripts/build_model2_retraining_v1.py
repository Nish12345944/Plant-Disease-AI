"""
Model 2 Retraining Phase 2: High-Performance Taxonomy Reconciliation and Dataset Builder
========================================================================================
Builds the canonicalized Model 2 Retraining V1 dataset under:
  data/processed/model2_retraining_v1/

Strict Safety Invariants:
- Preserves 100% of historical V4 Test Set (2,304 images) and Validation Set (1,764 images).
- Resolves all train-test and train-val duplicate leaks by excluding duplicate copies from train.
- Reconciles 175 raw class folders into a clean canonical taxonomy.
- Allocates validation splits (15%) for newly added classes using global SHA-256 two-pass partitioning.
- Quarantines ambiguous / abiotic labels (cauliflower purple tinges, pepper nutrition deficiency).
"""

import os
import sys
import io
import json
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
MODEL2_V4_DIR = PROJECT_ROOT / "data" / "processed" / "model2_v4"
V4_MANIFEST_PATH = MODEL2_V4_DIR / "model2_v4_manifest.csv"
V4_CLASS_MAPPING_PATH = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"

OUTPUT_DATASET_DIR = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v1"
OUTPUT_MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model2_retraining_v1_manifest.csv"
REPORTS_DIR = PROJECT_ROOT / "reports" / "model2_retraining"

QUARANTINED_CLASSES = {
    'cauliflower__cauliflower_fruit_Purple Tinges': 'Physiological/abiotic sun exposure anthocyanin response, non-pathological',
    'bell_pepper__PepperBell_Nutrition Deficiency': 'Abiotic nutritional deficiency, non-pathological'
}

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_canonical_class_name(crop, disease, raw_full_class):
    # 1. Healthy mappings
    if disease == 'healthy' or 'healthy' in disease.lower() or 'healthy' in raw_full_class.lower():
        return 'healthy', crop, 'healthy', 'Mapped to unified shared healthy class'

    # 2. Cauliflower mappings
    if crop == 'cauliflower':
        if 'black_rot' in disease.lower() or 'black rot' in disease.lower():
            return 'cauliflower__black_rot', 'cauliflower', 'black_rot', 'Merged organ leaf black rot into canonical black rot'
        if 'downy_mildew' in disease.lower() or 'downy mildew' in disease.lower():
            return 'cauliflower__downy_mildew', 'cauliflower', 'downy_mildew', 'Merged leaf downy mildew into canonical downy mildew'
        if 'alternaria' in disease.lower() or 'black spot' in disease.lower():
            return 'cauliflower__alternaria_leaf_spot', 'cauliflower', 'alternaria_leaf_spot', 'Merged alternaria leaf/head spot into canonical alternaria leaf spot'
        if 'bacterial' in disease.lower() or 'soft rot' in disease.lower():
            return 'cauliflower__bacterial_soft_rot', 'cauliflower', 'bacterial_soft_rot', 'Merged bacterial soft/spot rot into canonical bacterial soft rot'
        if 'insect hole' in disease.lower() or 'insect_hole' in disease.lower():
            return 'cauliflower__pest_damage', 'cauliflower', 'pest_damage', 'Standardized insect damage to pest_damage'

    # 3. Strawberry mappings
    if crop == 'strawberry':
        if 'strawberry_fruit_anthracnose' in disease.lower() or disease == 'anthracnose':
            return 'strawberry__anthracnose', 'strawberry', 'anthracnose', 'Merged fruit anthracnose into canonical anthracnose'
        if 'leaf spot' in disease.lower() or disease == 'leaf_spot':
            return 'strawberry__leaf_spot', 'strawberry', 'leaf_spot', 'Canonicalized leaf spot spacing'
        if 'gray_mold' in disease.lower() or 'gray mold' in disease.lower():
            return 'strawberry__gray_mold', 'strawberry', 'gray_mold', 'Canonicalized gray mold'
        if 'angular_leaf_spot' in disease.lower():
            return 'strawberry__angular_leaf_spot', 'strawberry', 'angular_leaf_spot', 'Canonicalized angular leaf spot'
        if 'powdery_mildew' in disease.lower():
            return 'strawberry__powdery_mildew', 'strawberry', 'powdery_mildew', 'Canonicalized powdery mildew'

    # 4. Plum mappings
    if crop == 'plum':
        if 'shot hole' in disease.lower() or disease == 'shot_hole':
            return 'plum__shot_hole', 'plum', 'shot_hole', 'Canonicalized shot hole spacing'

    # 5. Rose mappings
    if crop == 'rose':
        if 'black spot' in disease.lower() or disease == 'black_spot':
            return 'rose__black_spot', 'rose', 'black_spot', 'Canonicalized black spot spacing'
        if 'powdery_mildew' in disease.lower():
            return 'rose__powdery_mildew', 'rose', 'powdery_mildew', 'Canonicalized powdery mildew'
        if 'downy_mildew' in disease.lower():
            return 'rose__downy_mildew', 'rose', 'downy_mildew', 'Canonicalized downy mildew'
        if 'rust' in disease.lower():
            return 'rose__rust', 'rose', 'rust', 'Canonicalized rust'
        if 'mosiac' in disease.lower() or 'mosaic' in disease.lower():
            return 'rose__mosaic_virus', 'rose', 'mosaic_virus', 'Fixed mosaic spelling'
        if 'insect_hole' in disease.lower() or 'insect hole' in disease.lower():
            return 'rose__pest_damage', 'rose', 'pest_damage', 'Standardized insect damage to pest_damage'

    # 6. Spinach mappings
    if crop == 'spinach':
        if 'anthracnose' in disease.lower():
            return 'spinach__anthracnose', 'spinach', 'anthracnose', 'Removed redundant crop prefix'
        if 'mildew' in disease.lower() or 'mildrew' in disease.lower():
            return 'spinach__downy_mildew', 'spinach', 'downy_mildew', 'Standardized spinach mildew to downy_mildew'
        if 'bacterial' in disease.lower():
            return 'spinach__bacterial_spot', 'spinach', 'bacterial_spot', 'Removed redundant crop prefix'
        if 'pest' in disease.lower():
            return 'spinach__pest_damage', 'spinach', 'pest_damage', 'Standardized pest damage'

    # 7. Eggplant mappings
    if crop == 'eggplant':
        if disease == 'leaf_spot':
            return 'eggplant__cercospora_leaf_spot', 'eggplant', 'cercospora_leaf_spot', 'Merged generic leaf spot into cercospora leaf spot'
        if 'mosiac' in disease.lower() or 'mosaic' in disease.lower():
            return 'eggplant__mosaic_virus', 'eggplant', 'mosaic_virus', 'Fixed mosaic spelling'
        if 'wilt' in disease.lower():
            return 'eggplant__wilt_disease', 'eggplant', 'wilt_disease', 'Canonicalized wilt disease'
        if 'insect' in disease.lower() or 'pest' in disease.lower():
            return 'eggplant__pest_damage', 'eggplant', 'pest_damage', 'Standardized insect pest damage'

    # 8. Bell Pepper mappings
    if crop == 'bell_pepper':
        if 'cerespora' in disease.lower() or 'cercospora' in disease.lower():
            return 'bell_pepper__frogeye_leaf_spot', 'bell_pepper', 'frogeye_leaf_spot', 'Merged Cerespora typo into frogeye leaf spot'
        if 'leaf_curl' in disease.lower():
            return 'bell_pepper__leaf_curl', 'bell_pepper', 'leaf_curl', 'Canonicalized leaf curl'

    # 9. Blueberry mappings
    if crop == 'blueberry':
        if 'septoria' in disease.lower():
            return 'blueberry__septoria_leaf_spot', 'blueberry', 'septoria_leaf_spot', 'Canonicalized septoria leaf spot'
        if 'exobasidium' in disease.lower():
            return 'blueberry__exobasidium', 'blueberry', 'exobasidium', 'Canonicalized exobasidium'

    # 10. Ginger mappings
    if crop == 'ginger':
        if 'leaf_blight' in disease.lower():
            return 'ginger__leaf_blight', 'ginger', 'leaf_blight', 'Canonicalized leaf blight'
        if 'damage' in disease.lower() or 'pest' in disease.lower():
            return 'ginger__pest_damage', 'ginger', 'pest_damage', 'Standardized pest damage'

    # Standard existing classes
    clean_crop = crop.lower().strip()
    clean_disease = disease.lower().strip().replace(' ', '_').replace('-', '_')
    canonical = f"{clean_crop}__{clean_disease}"
    return canonical, clean_crop, clean_disease, 'Direct standard canonical mapping'

def main():
    print("=" * 80, flush=True)
    print("MODEL 2 RETRAINING V1: DATASET PREPARATION & TAXONOMY RECONCILIATION", flush=True)
    print("=" * 80, flush=True)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if OUTPUT_DATASET_DIR.exists():
        shutil.rmtree(OUTPUT_DATASET_DIR, ignore_errors=True)
    OUTPUT_DATASET_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load V4 Manifest
    print("\n[1/6] Loading V4 Authoritative Manifest...", flush=True)
    df_v4_manifest = pd.read_csv(V4_MANIFEST_PATH)
    v4_test_shas = set(df_v4_manifest[df_v4_manifest['split'] == 'test']['sha256'].dropna().astype(str).str.lower().str.strip())
    v4_val_shas = set(df_v4_manifest[df_v4_manifest['split'] == 'val']['sha256'].dropna().astype(str).str.lower().str.strip())
    v4_train_shas = set(df_v4_manifest[df_v4_manifest['split'] == 'train']['sha256'].dropna().astype(str).str.lower().str.strip())
    print(f"  V4 Protected Test SHAs: {len(v4_test_shas):,}", flush=True)
    print(f"  V4 Historical Val SHAs: {len(v4_val_shas):,}", flush=True)

    # 2. Scan All Images on Disk
    print("\n[2/6] Scanning Disk Dataset and Applying Taxonomy Rules...", flush=True)
    raw_records = []
    quarantined_records = []

    for s in ['train', 'val', 'test']:
        split_dir = MODEL2_V4_DIR / s
        for img_path in split_dir.glob('*/*/*.*'):
            if img_path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.webp']:
                continue
            crop = img_path.parent.parent.name
            disease = img_path.parent.name
            raw_full_class = f"{crop}__{disease}"
            sha = compute_sha256(img_path).lower().strip()

            # Check quarantined classes
            if raw_full_class in QUARANTINED_CLASSES:
                quarantined_records.append({
                    'image_path': str(img_path.relative_to(MODEL2_V4_DIR)).replace('\\', '/'),
                    'split': s,
                    'raw_class': raw_full_class,
                    'sha256': sha,
                    'reason': QUARANTINED_CLASSES[raw_full_class]
                })
                continue

            canonical_cls, c_crop, c_dis, map_reason = get_canonical_class_name(crop, disease, raw_full_class)

            raw_records.append({
                'source_abs_path': str(img_path),
                'source_rel_path': str(img_path.relative_to(MODEL2_V4_DIR)).replace('\\', '/'),
                'original_split': s,
                'raw_crop': crop,
                'raw_disease': disease,
                'raw_full_class': raw_full_class,
                'canonical_class': canonical_cls,
                'canonical_crop': c_crop,
                'canonical_disease': c_dis,
                'mapping_reason': map_reason,
                'sha256': sha,
                'filename': img_path.name
            })

    print(f"  Valid Candidates Processed: {len(raw_records):,}", flush=True)
    print(f"  Quarantined Images Excluded: {len(quarantined_records):,}", flush=True)

    # 3. Export Taxonomy Mapping CSV
    df_clean = pd.DataFrame(raw_records)
    taxonomy_mappings = df_clean[['raw_full_class', 'canonical_class', 'mapping_reason']].drop_duplicates().sort_values('raw_full_class')
    taxonomy_csv = REPORTS_DIR / "model2_taxonomy_mapping.csv"
    taxonomy_mappings.to_csv(taxonomy_csv, index=False)
    print(f"\n[3/6] Exported Taxonomy Mapping to {taxonomy_csv} ({len(taxonomy_mappings)} unique mappings).", flush=True)

    # 4. In-Memory Two-Pass Global Hash-Aware Split Allocation
    print("\n[4/6] Two-Pass Global Hash-Aware Split Balancing...", flush=True)
    
    final_assigned_records = []
    excluded_duplicate_records = []
    class_groups = defaultdict(lambda: {'train': [], 'val': [], 'test': []})
    
    for r in raw_records:
        c_cls = r['canonical_class']
        s = r['original_split']
        class_groups[c_cls][s].append(r)

    all_canonical_classes = sorted(class_groups.keys())
    print(f"  Total Unique Canonical Classes: {len(all_canonical_classes)}", flush=True)

    # PASS 1: Establish immutable Test and Validation splits and collect global hash sets
    global_test_shas = set()
    global_val_shas = set()
    np.random.seed(42)

    for c_cls in all_canonical_classes:
        grp = class_groups[c_cls]
        
        # 1. Historical test images
        for r in grp['test']:
            rec = dict(r)
            rec['final_split'] = 'test'
            rec['split_provenance'] = 'v4_historical_test'
            final_assigned_records.append(rec)
            global_test_shas.add(r['sha256'])

        # 2. Historical val images
        for r in grp['val']:
            rec = dict(r)
            rec['final_split'] = 'val'
            rec['split_provenance'] = 'v4_historical_val'
            final_assigned_records.append(rec)
            global_val_shas.add(r['sha256'])

        # 3. If class has 0 validation, allocate new validation hashes
        if len(grp['val']) == 0 and len(grp['train']) >= 10:
            # Group candidate train items by sha256
            sha_to_items = defaultdict(list)
            for r in grp['train']:
                # Skip if already in test or val
                if r['sha256'] in global_test_shas or r['sha256'] in global_val_shas:
                    continue
                sha_to_items[r['sha256']].append(r)

            unique_shas = list(sha_to_items.keys())
            np.random.shuffle(unique_shas)

            n_val_shas = max(5, min(40, int(len(unique_shas) * 0.15)))
            for sha in unique_shas[:n_val_shas]:
                global_val_shas.add(sha)
                for r in sha_to_items[sha]:
                    rec = dict(r)
                    rec['final_split'] = 'val'
                    rec['split_provenance'] = 'new_retraining_val'
                    final_assigned_records.append(rec)

    # PASS 2: Assign Training split with strict global deduplication against test and val
    val_and_test_shas = global_test_shas.union(global_val_shas)

    # Keep track of assigned items in final_assigned_records to avoid re-adding
    already_assigned_sources = set(r['source_rel_path'] for r in final_assigned_records)

    for c_cls in all_canonical_classes:
        grp = class_groups[c_cls]
        for r in grp['train']:
            if r['source_rel_path'] in already_assigned_sources:
                continue

            sha = r['sha256']
            if sha in global_test_shas:
                excluded_duplicate_records.append({
                    'image_path': r['source_rel_path'],
                    'split': 'train',
                    'raw_class': r['raw_full_class'],
                    'sha256': sha,
                    'reason': "Train copy of protected test image (excluded to prevent test leakage)"
                })
                continue

            if sha in global_val_shas:
                excluded_duplicate_records.append({
                    'image_path': r['source_rel_path'],
                    'split': 'train',
                    'raw_class': r['raw_full_class'],
                    'sha256': sha,
                    'reason': "Train copy of validation image (excluded to prevent val leakage)"
                })
                continue

            rec = dict(r)
            rec['final_split'] = 'train'
            rec['split_provenance'] = 'v4_historical_train' if sha in v4_train_shas else 'new_retraining_train'
            final_assigned_records.append(rec)

    # Export excluded / quarantined manifest
    all_excluded = quarantined_records + excluded_duplicate_records
    df_excl = pd.DataFrame(all_excluded)
    excl_csv = REPORTS_DIR / "model2_excluded_images.csv"
    df_excl.to_csv(excl_csv, index=False)
    print(f"  Exported {len(df_excl)} excluded/quarantined records to {excl_csv} ({len(quarantined_records)} quarantined + {len(excluded_duplicate_records)} duplicate leaks).", flush=True)

    df_final = pd.DataFrame(final_assigned_records)
    print(f"  Final Split Summary: {df_final['final_split'].value_counts().to_dict()}", flush=True)
    print(f"  Split Provenance Summary:\n{df_final['split_provenance'].value_counts()}", flush=True)

    # 5. Build Class Mapping & Output Filesystem
    print("\n[5/6] Generating Canonical Class Mappings and Building Dataset Filesystem...", flush=True)
    
    unique_disease_classes = sorted([c for c in all_canonical_classes if c != 'healthy'])
    class_to_id = {'healthy': 0}
    for idx, c in enumerate(unique_disease_classes, start=1):
        class_to_id[c] = idx

    print(f"  Canonical Class Mapping: {len(class_to_id)} classes (Healthy = 0, {len(unique_disease_classes)} Disease Classes)", flush=True)

    crop_disease_map = defaultdict(list)
    for c_cls in all_canonical_classes:
        if c_cls == 'healthy':
            continue
        crop, disease = c_cls.split('__')
        crop_disease_map[crop].append(disease)

    with open(OUTPUT_DATASET_DIR / "class_mapping.json", 'w') as f:
        json.dump(class_to_id, f, indent=2)
    with open(OUTPUT_DATASET_DIR / "crop_disease_mapping.json", 'w') as f:
        json.dump(dict(crop_disease_map), f, indent=2)

    # Multi-threaded file copying
    print("  Copying images to canonical directory structure in parallel...", flush=True)
    manifest_rows = []

    def copy_file_task(row):
        s = row['final_split']
        crop = row['canonical_crop']
        disease = row['canonical_disease']
        fname = row['filename']
        sha = row['sha256']
        c_cls = row['canonical_class']
        c_id = class_to_id[c_cls]

        dest_dir = OUTPUT_DATASET_DIR / s / crop / disease
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / fname

        src_file = Path(row['source_abs_path'])
        if not dest_file.exists():
            shutil.copy2(src_file, dest_file)

        dest_relpath = f"{s}/{crop}/{disease}/{fname}"
        return {
            'image_path': dest_relpath,
            'split': s,
            'split_provenance': row['split_provenance'],
            'canonical_class': c_cls,
            'class_id': c_id,
            'crop': crop,
            'disease': disease,
            'raw_class': row['raw_full_class'],
            'sha256': sha,
            'filename': fname,
            'quality_status': 'verified_valid'
        }

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(copy_file_task, r) for r in final_assigned_records]
        for idx, fut in enumerate(as_completed(futures), start=1):
            manifest_rows.append(fut.result())
            if idx % 5000 == 0 or idx == len(final_assigned_records):
                print(f"    Copied {idx:,}/{len(final_assigned_records):,} files...", flush=True)

    # 6. Save Manifests and Class Counts
    print("\n[6/6] Writing Manifests and Class Count Reports...", flush=True)
    df_out_manifest = pd.DataFrame(manifest_rows)
    df_out_manifest.to_csv(OUTPUT_MANIFEST_PATH, index=False)
    print(f"  Saved master manifest to {OUTPUT_MANIFEST_PATH} ({len(df_out_manifest):,} rows).", flush=True)

    class_stats = []
    for c_cls in sorted(class_to_id.keys(), key=lambda x: class_to_id[x]):
        c_id = class_to_id[c_cls]
        c_sub = df_out_manifest[df_out_manifest['canonical_class'] == c_cls]
        tr = len(c_sub[c_sub['split'] == 'train'])
        va = len(c_sub[c_sub['split'] == 'val'])
        te = len(c_sub[c_sub['split'] == 'test'])
        tot = len(c_sub)
        class_stats.append({
            'class_id': c_id,
            'canonical_class': c_cls,
            'train_count': tr,
            'val_count': va,
            'test_count': te,
            'total_count': tot,
            'has_validation': va > 0,
            'has_test': te > 0
        })

    df_class_stats = pd.DataFrame(class_stats)
    class_counts_csv = REPORTS_DIR / "model2_dataset_class_counts.csv"
    df_class_stats.to_csv(class_counts_csv, index=False)
    print(f"  Saved class counts table to {class_counts_csv}", flush=True)

    # Final Verification
    new_test_shas = set(df_out_manifest[df_out_manifest['split'] == 'test']['sha256'])
    test_match = (new_test_shas == v4_test_shas)
    print(f"\nFinal Test Set Integrity Check (Exact Match with V4 Test): {test_match} (Count: {len(new_test_shas)})", flush=True)
    assert test_match, "CRITICAL ERROR: Test set changed!"

    train_shas = set(df_out_manifest[df_out_manifest['split'] == 'train']['sha256'])
    val_shas = set(df_out_manifest[df_out_manifest['split'] == 'val']['sha256'])
    
    leak_train_test = train_shas.intersection(new_test_shas)
    leak_train_val = train_shas.intersection(val_shas)
    leak_val_test = val_shas.intersection(new_test_shas)

    print(f"\nCross-Split Leakage Results:")
    print(f"  Train <-> Test Overlap: {len(leak_train_test)} (Zero Expected)")
    print(f"  Train <-> Val Overlap:  {len(leak_train_val)} (Zero Expected)")
    print(f"  Val <-> Test Overlap:   {len(leak_val_test)} (Zero Expected)", flush=True)

    assert len(leak_train_test) == 0, f"Train-Test leakage: {len(leak_train_test)}"
    assert len(leak_train_val) == 0, f"Train-Val leakage: {len(leak_train_val)}"
    assert len(leak_val_test) == 0, f"Val-Test leakage: {len(leak_val_test)}"

    print("\nDataset preparation completed successfully and all invariants verified 100% clean!", flush=True)

if __name__ == "__main__":
    main()
