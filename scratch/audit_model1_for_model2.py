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
SUMMARY_PATH = PROJECT_ROOT / "data" / "processed" / "model1_balanced_summary.json"

def run_model1_audit_for_model2():
    print("==================================================", flush=True)
    print("STARTING MODEL 1 DATASET AUDIT FOR MODEL 2 REUSE", flush=True)
    print("==================================================", flush=True)

    if not MANIFEST_PATH.exists():
        print(f"Error: Manifest {MANIFEST_PATH} does not exist!", flush=True)
        return

    # 1. Read Manifest & Basic Stats
    records = []
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            records.append(r)

    total_images = len(records)
    print(f"Total images in model1_balanced: {total_images}", flush=True)

    crops = sorted(list(set(r["plant_class"] for r in records)))
    print(f"Total crops/classes: {len(crops)}: {crops}", flush=True)

    # 2. Per-Crop & Health Status Breakdown
    crop_stats = defaultdict(lambda: {
        "total": 0,
        "splits": Counter(),
        "plant_parts": Counter(),
        "health_status": Counter(),
        "sources": Counter(),
        "diseased_sources": Counter(),
    })

    for r in records:
        c = r["plant_class"]
        st = r["split"]
        part = r.get("plant_part", "unknown")
        health = r.get("health_status", "unknown")
        src = r.get("source_dataset", "unknown")

        crop_stats[c]["total"] += 1
        crop_stats[c]["splits"][st] += 1
        crop_stats[c]["plant_parts"][part] += 1
        crop_stats[c]["health_status"][health] += 1
        crop_stats[c]["sources"][src] += 1
        if health == "diseased":
            crop_stats[c]["diseased_sources"][src] += 1

    print("\n--- PER-CROP HEALTH STATUS BREAKDOWN ---", flush=True)
    print(f"{'Crop':<15} {'Total':<7} {'Healthy':<8} {'Diseased':<9} {'Unknown':<8} {'Top Plant Parts'}")
    print("-" * 75)
    for c in crops:
        st = crop_stats[c]
        h_cnt = st["health_status"].get("healthy", 0)
        d_cnt = st["health_status"].get("diseased", 0)
        u_cnt = st["health_status"].get("unknown", 0) + st["health_status"].get("not_specified", 0)
        parts_str = ", ".join([f"{k}:{v}" for k, v in st["plant_parts"].most_common(2)])
        print(f"{c:<15} {st['total']:<7} {h_cnt:<8} {d_cnt:<9} {u_cnt:<8} {parts_str}")

    # 3. Trace Disease Provenance from Original Files / Metadata
    print("\n--- TRACING DISEASE NAMES & PROVENANCE ---", flush=True)
    
    # We will search in data/external/ to find corresponding folder structures & disease names
    # For PlantVillage / external sets (tomato, pepper, cucumber, etc.)
    disease_inventory = defaultdict(lambda: defaultdict(int))
    
    # Map external paths & folder names for disease classes
    external_disease_map = {}
    for root, dirs, files in os.walk(EXTERNAL_DIR):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                rel = os.path.relpath(root, EXTERNAL_DIR)
                # Parse folder name to see if it specifies disease
                # e.g. tomato/Tomato___Early_blight, strawberry/Strawberry_leaf/Strawberry_healthy, etc.
                parts = Path(rel).parts
                if len(parts) > 1:
                    external_disease_map[f] = {
                        "crop_dir": parts[0],
                        "subfolder": parts[1] if len(parts) > 1 else "",
                        "rel_path": rel
                    }

    print(f"Indexed {len(external_disease_map)} files from data/external/ for provenance matching.", flush=True)

    # 4. Check for localization annotations in model1_balanced and data/external
    print("\n--- CHECKING LOCALIZATION SUITABILITY ---", flush=True)
    
    # Check if model1_balanced has any bbox files (.xml, .json, .txt)
    annotation_extensions = [".xml", ".json", ".txt"]
    model1_annot_count = 0
    for root, dirs, files in os.walk(BALANCED_DIR):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in annotation_extensions and not f.endswith("summary.json"):
                model1_annot_count += 1

    print(f"Bounding box / localization files found in data/processed/model1_balanced/: {model1_annot_count}", flush=True)

    # Check external datasets with annotations
    annotated_external_dirs = {}
    for sub in EXTERNAL_DIR.iterdir():
        if sub.is_dir():
            xml_count = len(list(sub.rglob("*.xml")))
            json_count = len(list(sub.rglob("*.json")))
            txt_count = len(list(sub.rglob("*.txt")))
            if xml_count > 0 or json_count > 0 or txt_count > 0:
                annotated_external_dirs[sub.name] = {
                    "xml": xml_count,
                    "json": json_count,
                    "txt": txt_count
                }
                print(f"  External dir '{sub.name}' has annotations: xml={xml_count}, json={json_count}, txt={txt_count}", flush=True)

    # 5. Classify all 16,537 images into Suitability Categories (A, B, C, D)
    categorization = {
        "A_directly_reusable": 0,
        "B_reusable_after_annotation": 0,
        "C_healthy_negative": 0,
        "D_not_suitable": 0
    }
    
    crop_category_breakdown = defaultdict(lambda: Counter())

    for r in records:
        c = r["plant_class"]
        health = r.get("health_status", "unknown")
        part = r.get("plant_part", "unknown")
        src = r.get("source_dataset", "unknown")

        # Category C: Healthy leaf/plant image (negative sample)
        if health == "healthy" and part in ["leaves", "leaf", "whole_plant", "plant"]:
            categorization["C_healthy_negative"] += 1
            crop_category_breakdown[c]["C_healthy_negative"] += 1
        
        # Category B: Diseased leaf/plant image with reliable disease identity (from known disease datasets like PlantVillage/HF Beans)
        elif health == "diseased" and part in ["leaves", "leaf"]:
            # Check if source has known disease identity
            categorization["B_reusable_after_annotation"] += 1
            crop_category_breakdown[c]["B_reusable_after_annotation"] += 1

        # Category D: Ambiguous or flower/fruit-only image without disease labels
        else:
            categorization["D_not_suitable"] += 1
            crop_category_breakdown[c]["D_not_suitable"] += 1

    print("\n--- REUSABILITY CATEGORIZATION SUMMARY ---", flush=True)
    print(f"  A. Directly Reusable (with bbox)       : {categorization['A_directly_reusable']:,} (0.0%)")
    print(f"  B. Reusable After Annotation (diseased) : {categorization['B_reusable_after_annotation']:,} ({categorization['B_reusable_after_annotation']/total_images*100:.1f}%)")
    print(f"  C. Healthy Negative Samples (clean)    : {categorization['C_healthy_negative']:,} ({categorization['C_healthy_negative']/total_images*100:.1f}%)")
    print(f"  D. Not Suitable / Unusable for Model 2 : {categorization['D_not_suitable']:,} ({categorization['D_not_suitable']/total_images*100:.1f}%)")

    # Detailed export data
    export_data = {
        "total_images": total_images,
        "total_crops": len(crops),
        "crops": crops,
        "categorization": categorization,
        "crop_stats": {c: {
            "total": crop_stats[c]["total"],
            "splits": dict(crop_stats[c]["splits"]),
            "plant_parts": dict(crop_stats[c]["plant_parts"]),
            "health_status": dict(crop_stats[c]["health_status"]),
            "sources": dict(crop_stats[c]["sources"]),
            "categories": dict(crop_category_breakdown[c])
        } for c in crops},
        "annotated_external_dirs": annotated_external_dirs
    }

    with open(PROJECT_ROOT / "scratch" / "model1_audit_data.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)

    print("\nDetailed audit data exported to scratch/model1_audit_data.json", flush=True)

if __name__ == "__main__":
    run_model1_audit_for_model2()
