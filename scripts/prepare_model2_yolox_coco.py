"""Convert YOLO-format Model 2 dataset into standard COCO JSON format for YOLOX.

DOES NOT modify data/processed/model2_dataset/.
Generates data/processed/model2_yolox/annotations/ for train, val, and test splits.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from PIL import Image
from tqdm import tqdm

SOURCE_DIR = Path("data/processed/model2_dataset")
TARGET_DIR = Path("data/processed/model2_yolox")
ANNOTATIONS_DIR = TARGET_DIR / "annotations"

ANNOTATIONS_DIR.mkdir(parents=True, exist_ok=True)


def convert_split(split_name: str, class_list: list[str], class_to_idx: dict[str, int]) -> dict:
    img_dir = SOURCE_DIR / "images" / split_name
    lbl_dir = SOURCE_DIR / "labels" / split_name

    img_files = sorted([p for p in img_dir.iterdir() if p.is_file()])
    print(f"\nProcessing '{split_name}' split: {len(img_files)} images...")

    categories = [
        {"id": idx, "name": name, "supercategory": "plant_disease"}
        for idx, name in enumerate(class_list)
    ]

    images_coco = []
    annotations_coco = []
    annotation_id = 1

    total_boxes = 0

    for img_idx, img_path in enumerate(tqdm(img_files, desc=f"Converting {split_name}"), start=1):
        # Read image size
        with Image.open(img_path) as im:
            width, height = im.size

        images_coco.append({
            "id": img_idx,
            "file_name": img_path.name,
            "width": width,
            "height": height,
            "file_path": str(img_path.resolve()),
        })

        lbl_path = lbl_dir / f"{img_path.stem}.txt"
        if not lbl_path.exists():
            continue

        with open(lbl_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]

        for line in lines:
            parts = line.split()
            if len(parts) != 5:
                continue

            cls_id = int(parts[0])
            norm_xc = float(parts[1])
            norm_yc = float(parts[2])
            norm_w = float(parts[3])
            norm_h = float(parts[4])

            # Convert normalized center-format to COCO absolute [xmin, ymin, width, height]
            abs_w = norm_w * width
            abs_h = norm_h * height
            abs_xmin = (norm_xc * width) - (abs_w / 2.0)
            abs_ymin = (norm_yc * height) - (abs_h / 2.0)

            # Clamp coordinates to image boundaries
            abs_xmin = max(0.0, min(float(width), abs_xmin))
            abs_ymin = max(0.0, min(float(height), abs_ymin))
            abs_w = max(1.0, min(float(width) - abs_xmin, abs_w))
            abs_h = max(1.0, min(float(height) - abs_ymin, abs_h))
            area = abs_w * abs_h

            annotations_coco.append({
                "id": annotation_id,
                "image_id": img_idx,
                "category_id": cls_id,
                "bbox": [round(abs_xmin, 2), round(abs_ymin, 2), round(abs_w, 2), round(abs_h, 2)],
                "area": round(area, 2),
                "iscrowd": 0,
                "segmentation": [],
            })
            annotation_id += 1
            total_boxes += 1

    coco_dict = {
        "info": {
            "description": f"Alexa Farms Model 2 Disease Dataset - {split_name}",
            "version": "1.0",
            "year": 2026,
            "contributor": "Alexa Farms",
        },
        "licenses": [],
        "categories": categories,
        "images": images_coco,
        "annotations": annotations_coco,
    }

    out_file = ANNOTATIONS_DIR / f"instances_{split_name}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(coco_dict, f)

    print(f"  -> Saved {out_file.name}: {len(images_coco)} images, {len(annotations_coco)} bounding boxes across {len(categories)} classes.")
    return {"images": len(images_coco), "boxes": total_boxes}


def main():
    print("=" * 60)
    print("MODEL 2 DATASET TO YOLOX COCO FORMAT ADAPTER")
    print("=" * 60)

    # 1. Load class mapping
    class_map_file = SOURCE_DIR / "class_mapping.json"
    if not class_map_file.exists():
        print(f"Error: {class_map_file} not found.")
        sys.exit(1)

    with open(class_map_file, "r", encoding="utf-8") as f:
        cm = json.load(f)

    class_list = cm["classes"]
    class_to_idx = cm["class_to_idx"]
    num_classes = len(class_list)

    print(f"Loaded {num_classes} classes from class_mapping.json")
    assert num_classes == 115, f"Expected 115 classes, got {num_classes}"

    # Verify contiguous IDs 0..114
    for idx, name in enumerate(class_list):
        assert class_to_idx[name] == idx, f"Mismatch at index {idx}: {name} vs {class_to_idx[name]}"

    print("Class IDs verified contiguous: 0 to 114.")

    # 2. Convert train, val, test
    stats = {}
    for split in ["train", "val", "test"]:
        stats[split] = convert_split(split, class_list, class_to_idx)

    # Copy class mapping into target dir for convenience
    with open(TARGET_DIR / "class_mapping.json", "w", encoding="utf-8") as f:
        json.dump(cm, f, indent=2)

    summary_file = TARGET_DIR / "coco_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump({
            "num_classes": num_classes,
            "classes": class_list,
            "splits": stats,
        }, f, indent=2)

    print("\n" + "=" * 60)
    print("CONVERSION COMPLETE & VALIDATED")
    print(f"Train: {stats['train']['images']} images / {stats['train']['boxes']} boxes")
    print(f"Val:   {stats['val']['images']} images / {stats['val']['boxes']} boxes")
    print(f"Test:  {stats['test']['images']} images / {stats['test']['boxes']} boxes")
    print("=" * 60)


if __name__ == "__main__":
    main()
