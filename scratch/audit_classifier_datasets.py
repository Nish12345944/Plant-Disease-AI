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
M1_BALANCED_DIR = PROJECT_ROOT / "data" / "processed" / "model1_balanced"
M1_MANIFEST = PROJECT_ROOT / "data" / "processed" / "model1_balanced_manifest.csv"
M2_MANIFEST = PROJECT_ROOT / "data" / "processed" / "model2_dataset" / "manifest.csv"
M2_IMAGES_DIR = PROJECT_ROOT / "data" / "processed" / "model2_dataset" / "images"
M2_CLASS_MAP = PROJECT_ROOT / "data" / "processed" / "model2_dataset" / "class_mapping.json"
BEANS_DIR = PROJECT_ROOT / "data" / "downloads" / "beans"

def run_classifier_dataset_audit():
    print("==================================================", flush=True)
    print("AUDITING ALL DISEASE & HEALTHY DATASETS FOR MODEL 2 CLASSIFIER", flush=True)
    print("==================================================", flush=True)

    # 1. Audit Model 2 existing dataset (115 disease classes)
    print("\n--- 1. AUDITING MODEL 2 EXISTING DISEASE DATASET ---", flush=True)
    with open(M2_CLASS_MAP, "r", encoding="utf-8") as f:
        m2_class_info = json.load(f)
    
    m2_classes = m2_class_info.get("classes", [])
    m2_crops = m2_class_info.get("crops", [])
    print(f"Model 2 class taxonomy: {len(m2_classes)} disease classes across {len(m2_crops)} crops.", flush=True)

    m2_img_to_crop = {}
    m2_img_to_disease = {}
    m2_disease_image_counts = Counter()
    m2_crop_disease_map = defaultdict(set)

    with open(M2_MANIFEST, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            img = r["image"]
            crop = r["crop"].strip().title()
            disease = r["disease"].strip().lower()
            if img not in m2_img_to_disease:
                m2_img_to_disease[img] = disease
                m2_img_to_crop[img] = crop
                m2_disease_image_counts[disease] += 1
                m2_crop_disease_map[crop].add(disease)

    print(f"Found {len(m2_img_to_disease)} unique disease images in Model 2 manifest across {len(m2_disease_image_counts)} disease classes.", flush=True)

    # 2. Audit Model 1 Healthy Foliage Images
    print("\n--- 2. AUDITING MODEL 1 HEALTHY FOLIAGE IMAGES ---", flush=True)
    m1_healthy_images = []
    m1_healthy_by_crop = Counter()
    with open(M1_MANIFEST, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            health = r.get("health_status")
            part = r.get("plant_part")
            crop = r.get("plant_class", "").strip().title()
            p = r["image_path"]
            if health == "healthy" and part in ["leaves", "leaf", "whole_plant"]:
                full_p = PROJECT_ROOT / "data" / "processed" / p
                if full_p.exists():
                    m1_healthy_images.append({
                        "path": str(full_p),
                        "crop": crop,
                        "rel_path": p
                    })
                    m1_healthy_by_crop[crop] += 1

    print(f"Total confirmed healthy leaf images from Model 1: {len(m1_healthy_images)} across {len(m1_healthy_by_crop)} crops.", flush=True)
    for c, cnt in m1_healthy_by_crop.most_common():
        print(f"  - {c:<15} : {cnt:>5} healthy images", flush=True)

    # 3. Audit Makerere HF Beans Dataset
    print("\n--- 3. AUDITING BEANS DATASET ---", flush=True)
    beans_stats = Counter()
    beans_images = []
    if BEANS_DIR.exists():
        for sub in ["train", "validation", "test"]:
            sub_dir = BEANS_DIR / sub
            if sub_dir.exists():
                for cls_dir in sub_dir.iterdir():
                    if cls_dir.is_dir():
                        cls_name = cls_dir.name.lower()
                        for img_p in cls_dir.glob("*.jpg"):
                            beans_images.append({
                                "path": str(img_p),
                                "crop": "Bean",
                                "condition": cls_name,
                                "split": sub
                            })
                            beans_stats[cls_name] += 1
    print(f"Beans dataset counts: {dict(beans_stats)} (Total: {len(beans_images)})", flush=True)

    # 4. Check External Sources (PlantVillage healthy & disease classes)
    print("\n--- 4. AUDITING EXTERNAL PLANTVILLAGE / KAGGLE SOURCES ---", flush=True)
    external_healthy_by_crop = Counter()
    external_disease_counts = Counter()

    for sub in EXTERNAL_DIR.iterdir():
        if sub.is_dir():
            for folder in sub.glob("**/*"):
                if folder.is_dir():
                    f_name = folder.name.lower()
                    if "healthy" in f_name:
                        img_cnt = len(list(folder.glob("*.jpg")) + list(folder.glob("*.png")))
                        if img_cnt > 0:
                            external_healthy_by_crop[sub.name] += img_cnt
                    elif "___" in folder.name or "_" in folder.name:
                        img_cnt = len(list(folder.glob("*.jpg")) + list(folder.glob("*.png")))
                        if img_cnt > 0:
                            external_disease_counts[f"{sub.name}__{folder.name}"] += img_cnt

    print(f"External healthy image pools found: {dict(external_healthy_by_crop)}", flush=True)

    # 5. Compile Comprehensive Crop x Disease & Healthy Availability
    print("\n==================================================")
    print("UNIFIED CROP-DISEASE TAXONOMY & IMAGE INVENTORY")
    print("==================================================")

    all_active_crops = sorted(list(set(list(m2_crop_disease_map.keys()) + list(m1_healthy_by_crop.keys()) + ["Bean"])))
    
    crop_inventory = {}
    total_healthy_count = 0
    total_diseased_count = 0
    classes_under_50 = []
    classes_under_20 = []
    missing_healthy_crops = []

    for crop in all_active_crops:
        h_count = m1_healthy_by_crop.get(crop, 0) + external_healthy_by_crop.get(crop.lower(), 0)
        if crop == "Bean":
            h_count += beans_stats.get("healthy", 0)

        diseases = sorted(list(m2_crop_disease_map.get(crop, set())))
        if crop == "Bean":
            diseases = sorted(list(set(diseases + ["bean angular leaf spot", "bean rust"])))

        total_healthy_count += h_count
        if h_count == 0:
            missing_healthy_crops.append(crop)

        disease_details = {}
        for d in diseases:
            cnt = m2_disease_image_counts.get(d, 0)
            if crop == "Bean":
                if "angular" in d:
                    cnt += beans_stats.get("angular_leaf_spot", 0)
                elif "rust" in d:
                    cnt += beans_stats.get("bean_rust", 0)
            
            disease_details[d] = cnt
            total_diseased_count += cnt
            if cnt < 20:
                classes_under_20.append(f"{crop}: {d} ({cnt})")
            if cnt < 50:
                classes_under_50.append(f"{crop}: {d} ({cnt})")

        crop_inventory[crop] = {
            "healthy_images": h_count,
            "diseases_count": len(diseases),
            "disease_classes": disease_details,
            "total_crop_images": h_count + sum(disease_details.values())
        }

    print(f"\nTOTAL CROPS CATALOGED : {len(all_active_crops)}")
    print(f"TOTAL DISEASE CLASSES : {len(m2_disease_image_counts)}")
    print(f"TOTAL HEALTHY IMAGES  : {total_healthy_count:,}")
    print(f"TOTAL DISEASED IMAGES : {total_diseased_count:,}")
    print(f"TOTAL USABLE IMAGES   : {total_healthy_count + total_diseased_count:,}")
    print(f"MISSING HEALTHY CROPS ({len(missing_healthy_crops)}): {missing_healthy_crops}")
    print(f"DISEASE CLASSES < 50 IMAGES: {len(classes_under_50)}")
    print(f"DISEASE CLASSES < 20 IMAGES: {len(classes_under_20)}")

    # 6. Check duplicates via hash indexing
    print("\n--- 6. CHECKING DUPLICATES ---", flush=True)
    seen_hashes = {}
    duplicate_groups = 0
    duplicate_images = 0

    # Index M2 images
    if M2_IMAGES_DIR.exists():
        for img_p in M2_IMAGES_DIR.glob("*.jpg"):
            try:
                with open(img_p, "rb") as f:
                    h = hashlib.md5(f.read(65536)).hexdigest()
                if h in seen_hashes:
                    duplicate_images += 1
                else:
                    seen_hashes[h] = str(img_p)
            except Exception:
                pass

    print(f"Duplicate check in M2 images: {duplicate_images} duplicate frames detected.", flush=True)

    # Export audit summary to JSON
    audit_summary = {
        "total_crops": len(all_active_crops),
        "total_disease_classes": len(m2_disease_image_counts),
        "total_healthy_images": total_healthy_count,
        "total_diseased_images": total_diseased_count,
        "total_usable_images": total_healthy_count + total_diseased_count,
        "missing_healthy_crops": missing_healthy_crops,
        "classes_under_50_images": classes_under_50,
        "classes_under_20_images": classes_under_20,
        "crop_inventory": crop_inventory,
        "recommended_architecture": "EfficientNet-B2 with ImageNet pretrained transfer learning",
        "recommended_splits": {"train": "70%", "val": "15%", "test": "15%"}
    }

    with open(PROJECT_ROOT / "scratch" / "model2_classifier_audit_summary.json", "w", encoding="utf-8") as f:
        json.dump(audit_summary, f, indent=2)

    print("\nAudit summary saved to scratch/model2_classifier_audit_summary.json", flush=True)

if __name__ == "__main__":
    run_classifier_dataset_audit()
