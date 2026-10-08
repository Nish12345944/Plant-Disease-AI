import os
import sys
import csv
import json
import hashlib
from pathlib import Path
from collections import Counter, defaultdict

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
EXTERNAL_DIR = PROJECT_ROOT / "data" / "external"
BALANCED_DIR = PROJECT_ROOT / "data" / "processed" / "model1_balanced"
MANIFEST_PATH = PROJECT_ROOT / "data" / "processed" / "model1_balanced_manifest.csv"
PLANT_PARTS_AUDIT = PROJECT_ROOT / "reports" / "plant_part_dataset_audit.csv"

def run_disease_provenance_audit():
    print("--- 1. INDEXING ORIGINAL SOURCE METADATA & EXTERNAL PATHS ---", flush=True)
    
    # Load plant part dataset audit if available to get original source paths
    orig_path_by_hash = {}
    orig_disease_by_hash = {}
    
    if PLANT_PARTS_AUDIT.exists():
        print(f"Loading {PLANT_PARTS_AUDIT.name}...", flush=True)
        with open(PLANT_PARTS_AUDIT, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for r in reader:
                h = r.get("sha256") or r.get("hash")
                orig_p = r.get("original_path") or r.get("source_path") or r.get("image_path")
                if h and orig_p:
                    orig_path_by_hash[h] = orig_p
                    
    print(f"Indexed {len(orig_path_by_hash)} entries from plant parts audit.", flush=True)

    # Load model1_balanced manifest
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    print(f"Analyzing {len(records)} records in model1_balanced_manifest.csv...", flush=True)

    # Let's inspect external directories to map folder names to clean disease labels
    # e.g., tomato/Tomato___Early_blight -> "Tomato Early Blight"
    disease_patterns = {
        "early_blight": "Early Blight",
        "late_blight": "Late Blight",
        "bacterial_spot": "Bacterial Spot",
        "leaf_mold": "Leaf Mold",
        "septoria": "Septoria Leaf Spot",
        "yellow_leaf_curl": "Yellow Leaf Curl Virus",
        "mosaic_virus": "Mosaic Virus",
        "target_spot": "Target Spot",
        "spider_mites": "Two-spotted Spider Mite",
        "powdery_mildew": "Powdery Mildew",
        "downy_mildew": "Downy Mildew",
        "black_rot": "Black Rot",
        "anthracnose": "Anthracnose",
        "rust": "Rust",
        "scorch": "Leaf Scorch",
        "cercospora": "Cercospora Leaf Spot",
        "leaf_spot": "Leaf Spot",
        "angular_leaf_spot": "Angular Leaf Spot",
        "healthy": "Healthy"
    }

    # Trace each crop in model1_balanced
    crop_disease_counts = defaultdict(lambda: Counter())
    crop_provenance_evidence = defaultdict(lambda: Counter())
    crop_health_table = []

    # Check each image file in model1_balanced
    for r in records:
        c = r["plant_class"]
        st = r["split"]
        part = r.get("plant_part", "unknown")
        health = r.get("health_status", "unknown")
        src = r.get("source_dataset", "unknown")
        p = r["image_path"]
        
        # Analyze filename and source
        fname = Path(p).name.lower()
        
        # Determine disease label
        detected_disease = "Unknown / General Diseased"
        if health == "healthy":
            detected_disease = "Healthy"
        elif health == "diseased":
            # Check source dataset and keywords
            matched = False
            for pat_k, pat_name in disease_patterns.items():
                if pat_k in fname or pat_k in src.lower():
                    detected_disease = pat_name
                    matched = True
                    break
            if not matched:
                if src == "hf_makerere_beans":
                    detected_disease = "Bean Angular Leaf Spot / Bean Rust"
                elif src == "lettuce-disease.v6i.folder":
                    detected_disease = "Lettuce Bacterial Rot / Septoria"
                elif src == "spinach_disease":
                    detected_disease = "Spinach Downy Mildew / Anthracnose"
                elif src == "zuchhini" or c == "zucchini":
                    detected_disease = "Zucchini Powdery Mildew"
                elif src == "blueberry_leaves" or src == "blueberry_leaves_external":
                    detected_disease = "Blueberry Rust / Leaf Spot"
                elif src == "strawberry_leaves" or src == "strawberry_leaves_external":
                    detected_disease = "Strawberry Leaf Scorch"
                else:
                    detected_disease = f"{c.title()} Foliar Disease (Unspecified in M1)"

        crop_disease_counts[c][detected_disease] += 1
        crop_provenance_evidence[c][f"source:{src}"] += 1

    print("\n==================================================")
    print("CROP x DISEASE INVENTORY MATRIX (FROM MODEL 1)")
    print("==================================================")
    print(f"{'Crop':<14} {'Condition / Disease':<38} {'Images':<8} {'Localization':<15}")
    print("-" * 75)
    
    matrix_rows = []
    for c in sorted(crop_disease_counts.keys()):
        for d, count in crop_disease_counts[c].most_common():
            loc_status = "NO (Image-level only)"
            print(f"{c:<14} {d:<38} {count:<8} {loc_status:<15}")
            matrix_rows.append({
                "crop": c,
                "disease": d,
                "images": count,
                "localization": "NO",
                "annotation_type": "None (Classification only)"
            })

    # Save detailed disease analysis
    out_dict = {
        "matrix": matrix_rows,
        "crop_disease_counts": {c: dict(cnt) for c, cnt in crop_disease_counts.items()},
        "crop_provenance_evidence": {c: dict(cnt) for c, cnt in crop_provenance_evidence.items()}
    }
    with open(PROJECT_ROOT / "scratch" / "disease_provenance_audit.json", "w", encoding="utf-8") as f:
        json.dump(out_dict, f, indent=2)

    print("\nDisease provenance audit exported to scratch/disease_provenance_audit.json", flush=True)

if __name__ == "__main__":
    run_disease_provenance_audit()
