"""Phases 1-4 Diagnostic Script: Evaluator, Ground-Truth, Dataset Conversion, and Class Mapping Verification."""
import os
import sys
import json
import glob
import cv2
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("="*75)
print(" PHASE 4: CLASS MAPPING VERIFICATION")
print("="*75)

source_map_path = "data/processed/model2_dataset/class_mapping.json"
model_map_path = "models/model2/class_mapping.json"

with open(source_map_path, "r", encoding="utf-8") as f:
    source_map = json.load(f)

with open(model_map_path, "r", encoding="utf-8") as f:
    model_map = json.load(f)

# Inspect structures
print(f"Source Map Keys: {list(source_map.keys())}")
print(f"Model Map Keys: {list(model_map.keys())}")

source_classes = source_map.get("classes", [])
model_classes = model_map.get("classes", [])
print(f"Source Classes Count: {len(source_classes)}")
print(f"Model Classes Count: {len(model_classes)}")

source_c2i = source_map.get("class_to_idx", {})
model_c2i = model_map.get("class_to_idx", {})

print(f"Source class_to_idx length: {len(source_c2i)}")
print(f"Model class_to_idx length: {len(model_c2i)}")

# Check contiguity & equality
is_contiguous = sorted(source_c2i.values()) == list(range(115))
is_identical = source_c2i == model_c2i
print(f"Source IDs are contiguous 0-114: {is_contiguous}")
print(f"Source and Model mappings identical: {is_identical}")

print("\n" + "="*75)
print(" PHASE 1 & 3: COCO JSON ANNOTATIONS VS SOURCE YOLO LABELS")
print("="*75)

coco_val_path = "data/processed/model2_yolox/annotations/instances_val.json"
with open(coco_val_path, "r", encoding="utf-8") as f:
    coco_val = json.load(f)

print(f"COCO Val categories count: {len(coco_val['categories'])}")
print(f"COCO Val images count: {len(coco_val['images'])}")
print(f"COCO Val annotations count: {len(coco_val['annotations'])}")

# Check category IDs in COCO JSON
cat_ids = [c["id"] for c in coco_val["categories"]]
print(f"COCO Category IDs min={min(cat_ids)}, max={max(cat_ids)}, contiguous 0-114: {cat_ids == list(range(115))}")

# Check sample annotations
sample_ann = coco_val["annotations"][0]
print(f"Sample annotation: {sample_ann}")

# Verify 20 validation images: YOLO file vs COCO JSON vs Image dimensions
print("\n" + "="*75)
print(" PHASE 2: GROUND-TRUTH BOXES VERIFICATION (20 VAL SAMPLES)")
print("="*75)

# Map image filename to COCO image info & annotations
img_name_to_info = {img["file_name"]: img for img in coco_val["images"]}
img_id_to_anns = {}
for ann in coco_val["annotations"]:
    img_id_to_anns.setdefault(ann["image_id"], []).append(ann)

val_yolo_dir = "data/processed/model2_dataset/labels/val"
val_img_dir = "data/processed/model2_dataset/images/val"
val_yolo_files = sorted(glob.glob(os.path.join(val_yolo_dir, "*.txt")))[:20]

os.makedirs("reports/model2_diagnostics/gt_visual_checks", exist_ok=True)

diff_errors = []

for idx, yolo_file in enumerate(val_yolo_files, 1):
    base_name = os.path.splitext(os.path.basename(yolo_file))[0]
    img_name = base_name + ".jpg"
    img_path = os.path.join(val_img_dir, img_name)
    
    if not os.path.exists(img_path):
        print(f"Warning: image {img_path} not found")
        continue
        
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    
    # Read YOLO lines
    with open(yolo_file, "r") as f:
        yolo_lines = [l.strip().split() for l in f if l.strip()]
        
    # Get COCO annotations
    coco_img_info = img_name_to_info.get(img_name)
    if not coco_img_info:
        print(f"Error: {img_name} not in COCO JSON!")
        continue
        
    coco_anns = img_id_to_anns.get(coco_img_info["id"], [])
    
    # Check dimensions
    if coco_img_info["width"] != w or coco_img_info["height"] != h:
        print(f"Dimension mismatch for {img_name}: img={w}x{h}, coco={coco_img_info['width']}x{coco_img_info['height']}")
        
    # Draw GT on image for visual inspection
    vis_img = img.copy()
    
    # Verify each YOLO box against COCO box
    if len(yolo_lines) != len(coco_anns):
        print(f"Count mismatch in {img_name}: YOLO={len(yolo_lines)}, COCO={len(coco_anns)}")
        
    for y_idx, y_tokens in enumerate(yolo_lines):
        cls_id = int(y_tokens[0])
        cx, cy, bw, bh = map(float, y_tokens[1:5])
        
        # Correct conversion:
        # x_min = (cx - bw / 2) * w
        # y_min = (cy - bh / 2) * h
        # box_w = bw * w
        # box_h = bh * h
        calc_x = (cx - bw / 2.0) * w
        calc_y = (cy - bh / 2.0) * h
        calc_w = bw * w
        calc_h = bh * h
        
        # Check against COCO annotation
        if y_idx < len(coco_anns):
            c_ann = coco_anns[y_idx]
            c_box = c_ann["bbox"] # [x, y, w, h]
            c_cls = c_ann["category_id"]
            
            # Check cls
            if cls_id != c_cls:
                diff_errors.append(f"{img_name}: Class ID mismatch: YOLO={cls_id}, COCO={c_cls}")
                
            # Check coordinate differences
            dx = abs(calc_x - c_box[0])
            dy = abs(calc_y - c_box[1])
            dw = abs(calc_w - c_box[2])
            dh = abs(calc_h - c_box[3])
            
            if dx > 0.5 or dy > 0.5 or dw > 0.5 or dh > 0.5:
                diff_errors.append(f"{img_name} box {y_idx}: Coord diff dx={dx:.2f}, dy={dy:.2f}, dw={dw:.2f}, dh={dh:.2f}")
                
        # Draw on image
        x1, y1 = int(round(calc_x)), int(round(calc_y))
        x2, y2 = int(round(calc_x + calc_w)), int(round(calc_y + calc_h))
        
        cls_name = source_classes[cls_id] if cls_id < len(source_classes) else f"ID_{cls_id}"
        cv2.rectangle(vis_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(vis_img, f"{cls_id}: {cls_name}", (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
    out_vis_path = f"reports/model2_diagnostics/gt_visual_checks/gt_{idx:02d}_{base_name}.jpg"
    cv2.imwrite(out_vis_path, vis_img)

print(f"\nCompleted checking 20 validation images.")
print(f"Total discrepancies found: {len(diff_errors)}")
if diff_errors:
    for e in diff_errors[:10]:
        print(f"  - {e}")
else:
    print("  -> ALL 20 GT annotations match COCO pixel coordinates and class IDs PERFECTLY!")

print("Visual ground-truth verification images saved to reports/model2_diagnostics/gt_visual_checks/")
