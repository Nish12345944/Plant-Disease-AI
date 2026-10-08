import hashlib
import json
import os
import sys
from pathlib import Path
from collections import defaultdict
import pandas as pd

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()

# 1. Load Model 2 hashes
m2_manifest_path = PROJECT_ROOT / "data" / "processed" / "model2_organized_manifest.csv"
m2_df = pd.read_csv(m2_manifest_path)
m2_train_hashes = set(m2_df[m2_df["split"] == "train"]["sha256"].dropna())
m2_val_hashes = set(m2_df[m2_df["split"] == "val"]["sha256"].dropna())
m2_test_hashes = set(m2_df[m2_df["split"] == "test"]["sha256"].dropna())

print(f"Loaded Model 2 hashes: train={len(m2_train_hashes)}, val={len(m2_val_hashes)}, test={len(m2_test_hashes)}")

# 2. Compute/load Model 1 hashes
m1_manifest_path = PROJECT_ROOT / "data" / "processed" / "model1_balanced_manifest.csv"
m1_df = pd.read_csv(m1_manifest_path)

m1_train_hashes = set()
m1_val_hashes = set()
m1_test_hashes = set()

for idx, row in m1_df.iterrows():
    p = PROJECT_ROOT / row["image_path"]
    if p.exists():
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        sp = row.get("split", "train")
        if sp == "train":
            m1_train_hashes.add(h)
        elif sp == "val":
            m1_val_hashes.add(h)
        elif sp == "test":
            m1_test_hashes.add(h)

print(f"Computed Model 1 hashes: train={len(m1_train_hashes)}, val={len(m1_val_hashes)}, test={len(m1_test_hashes)}")

all_train_hashes = m1_train_hashes | m2_train_hashes
all_val_hashes = m1_val_hashes | m2_val_hashes
all_test_hashes = m1_test_hashes | m2_test_hashes

# 3. Check PlantSeg candidates
ps_root = PROJECT_ROOT / "data" / "external" / "model2_supplementary" / "plantsegv3" / "plantsegv3"
ps_meta_path = ps_root / "Metadatav2.csv"
if ps_meta_path.exists():
    ps_meta = pd.read_csv(ps_meta_path)
    print(f"PlantSeg metadata rows: {len(ps_meta)}")
    
    # Index files
    img_files = {}
    for s in ["train", "val", "test"]:
        s_dir = ps_root / "images" / s
        if s_dir.exists():
            for f in s_dir.iterdir():
                if f.is_file():
                    img_files[f.name] = f
    print(f"PlantSeg indexed physical images: {len(img_files)}")

    target_map = {
        # Diseases
        "bean rust": ("bean", "bean__rust", "diseased"),
        "bean angular leaf spot": ("bean", "bean__angular_leaf_spot", "diseased"),
        "soybean rust": ("soybean", "soybean__rust", "diseased"),
        "soybean frog eye leaf spot": ("soybean", "soybean__frog_eye_leaf_spot", "diseased"),
        "citrus canker": ("citrus", "citrus__canker", "diseased"),
        "wheat stripe rust": ("wheat", "wheat__stripe_rust", "diseased"),
        "wheat head scab": ("wheat", "wheat__head_scab", "diseased"),
        "wheat powdery mildew": ("wheat", "wheat__powdery_mildew", "diseased"),
        "wheat septoria blotch": ("wheat", "wheat__septoria_blotch", "diseased"),
        "wheat loose smut": ("wheat", "wheat__loose_smut", "diseased"),
        "grape downy mildew": ("grape", "grape__downy_mildew", "diseased"),
        "apple scab": ("apple", "apple__scab", "diseased"),
        "corn smut": ("corn", "corn__smut", "diseased"),
        "corn rust": ("corn", "corn__rust", "diseased"),
        "corn northern leaf blight": ("corn", "corn__northern_leaf_blight", "diseased"),
        "zucchini powdery mildew": ("zucchini", "zucchini__powdery_mildew", "diseased"),
        "cucumber powdery mildew": ("cucumber", "cucumber__powdery_mildew", "diseased"),
        "cucumber angular leaf spot": ("cucumber", "cucumber__angular_leaf_spot", "diseased"),
        "cucumber bacterial wilt": ("cucumber", "cucumber__bacterial_wilt", "diseased"),
        "tomato early blight": ("tomato", "tomato__early_blight", "diseased"),
        "tomato late blight": ("tomato", "tomato__late_blight", "diseased"),
        "tomato leaf mold": ("tomato", "tomato__leaf_mold", "diseased"),
        "tomato septoria leaf spot": ("tomato", "tomato__septoria_leaf_spot", "diseased"),
        "peach leaf curl": ("peach", "peach__leaf_curl", "diseased"),
        "peach brown rot": ("peach", "peach__brown_rot", "diseased"),
        "coffee leaf rust": ("coffee", "coffee__leaf_rust", "diseased"),
        "banana black leaf streak": ("banana", "banana__black_leaf_streak", "diseased"),
        "banana bunchy top": ("banana", "banana__bunchy_top", "diseased"),
        # Healthy
        "tomato healthy": ("tomato", None, "healthy"),
        "cucumber healthy": ("cucumber", None, "healthy"),
        "bean healthy": ("bean", None, "healthy"),
        "soybean healthy": ("soybean", None, "healthy"),
        "wheat healthy": ("wheat", None, "healthy"),
        "corn healthy": ("corn", None, "healthy"),
    }

    counts = defaultdict(lambda: {"total": 0, "clean": 0, "train_dup": 0, "val_dup": 0, "test_dup": 0})
    for _, row in ps_meta.iterrows():
        dis = str(row.get("Disease", "")).strip().lower()
        plant = str(row.get("Plant", "")).strip().lower()
        key1 = f"{plant} {dis}".strip()
        key2 = dis
        
        target = target_map.get(key1) or target_map.get(key2)
        if target:
            fname = str(row["Name"]).strip()
            if fname in img_files:
                fpath = img_files[fname]
                h = hashlib.sha256(fpath.read_bytes()).hexdigest()
                label = target[1] if target[2] == "diseased" else f"{target[0]}__healthy"
                counts[label]["total"] += 1
                if h in all_train_hashes:
                    counts[label]["train_dup"] += 1
                elif h in all_val_hashes:
                    counts[label]["val_dup"] += 1
                elif h in all_test_hashes:
                    counts[label]["test_dup"] += 1
                else:
                    counts[label]["clean"] += 1

    print("\n--- Summary of Candidate Availability from PlantSeg ---")
    for k, v in sorted(counts.items()):
        print(f"  {k:<32} | Total: {v['total']:<4} | Clean: {v['clean']:<4} | Dups: Train={v['train_dup']} Val={v['val_dup']} Test={v['test_dup']}")
