"""Complete Diagnostic Script covering Phases 4, 5, 6, 7, 8, and 9."""
import os
import sys
import json
import glob
import cv2
import numpy as np
import torch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model2.config import Model2Config
from model2.test_model2 import load_model2, predict_disease, get_class_mapping
from model2.dataset import DiseaseCOCODataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, idx_to_class = load_model2("models/model2/best_model.pth", device=device)

# --- PHASE 4 CONTINUATION: Class mapping key verification ---
with open("data/processed/model2_dataset/class_mapping.json", "r") as f:
    source_map = json.load(f)
with open("models/model2/class_mapping.json", "r") as f:
    model_map = json.load(f)

source_classes = source_map["classes"]
mapping_mismatches = []
for idx in range(115):
    s_name = source_classes[idx]
    m_name = model_map.get(str(idx))
    if s_name != m_name:
        mapping_mismatches.append(f"Idx {idx}: source='{s_name}' vs model='{m_name}'")

print("="*75)
print(" PHASE 4: EXACT INDEX-TO-NAME MAPPING MATCH")
print("="*75)
print(f"Total 115 classes index alignment mismatches: {len(mapping_mismatches)}")
if mapping_mismatches:
    for m in mapping_mismatches[:5]:
        print(f"  - {m}")
else:
    print("  -> ALL 115 classes match index-for-index (0 to 114) with 100% precision!")

# --- PHASE 7: TRAINING BEHAVIOR INSPECTION ---
print("\n" + "="*75)
print(" PHASE 7: TRAINING BEHAVIOR & LOSS TRAJECTORY")
print("="*75)
summary_path = "models/model2/training_summary.json"
if os.path.exists(summary_path):
    with open(summary_path, "r") as f:
        summary = json.load(f)
    print(f"Total Epochs Completed: {summary.get('epochs_completed')}")
    print(f"Total Time: {summary.get('elapsed_time_minutes'):.2f} minutes")
    print(f"Best Validation mAP@50:95: {summary.get('best_val_map_50_95')}")
    history = summary.get("history", {})
    epochs = history.get("epoch", [])
    tot_loss = history.get("train_total_loss", [])
    iou_loss = history.get("train_iou_loss", [])
    conf_loss = history.get("train_conf_loss", [])
    cls_loss = history.get("train_cls_loss", [])
    val_map50 = history.get("val_map_50", [])
    val_map50_95 = history.get("val_map_50_95", [])
    
    print("\nEpoch | Total Loss | IoU Loss | Obj Loss | Cls Loss | Val mAP@50 | Val mAP@50:95")
    print("-" * 75)
    for i in range(len(epochs)):
        ep = epochs[i]
        tl = tot_loss[i] if i < len(tot_loss) else 0.0
        il = iou_loss[i] if i < len(iou_loss) else 0.0
        ol = conf_loss[i] if i < len(conf_loss) else 0.0
        cl = cls_loss[i] if i < len(cls_loss) else 0.0
        vm50 = val_map50[i] if i < len(val_map50) else 0.0
        vm95 = val_map50_95[i] if i < len(val_map50_95) else 0.0
        print(f"{ep:5d} | {tl:10.4f} | {il:8.4f} | {ol:8.4f} | {cl:8.4f} | {vm50:10.4f} | {vm95:13.4f}")

# --- PHASE 8: PRETRAINED WEIGHT TRANSFER INSPECTION ---
print("\n" + "="*75)
print(" PHASE 8: PRETRAINED WEIGHT TRANSFER AUDIT")
print("="*75)
pretrained_path = "models/pretrained/yolox_s.pth"
if os.path.exists(pretrained_path):
    pretrained_ckpt = torch.load(pretrained_path, map_location="cpu", weights_only=False)
    p_state = pretrained_ckpt.get("model", pretrained_ckpt)
    m_state = model.state_dict()
    
    matched_keys = []
    shape_mismatch_keys = []
    missing_in_pretrained = []
    
    for k, v in m_state.items():
        if k in p_state:
            if p_state[k].shape == v.shape:
                matched_keys.append(k)
            else:
                shape_mismatch_keys.append((k, p_state[k].shape, v.shape))
        else:
            missing_in_pretrained.append(k)
            
    print(f"Total model parameters keys: {len(m_state)}")
    print(f"Transferred from COCO pretrained: {len(matched_keys)} layers")
    print(f"Class-dependent head layers newly initialized for 115 classes: {len(shape_mismatch_keys)}")
    for k, p_sh, m_sh in shape_mismatch_keys:
        print(f"  - {k}: COCO 80 classes {p_sh} -> Model 2 115 classes {m_sh}")

# --- PHASE 9: DATASET CHARACTERISTICS & LESION SIZE DISTRIBUTION ---
print("\n" + "="*75)
print(" PHASE 9: DATASET CHARACTERISTICS & LESION SIZE ANALYSIS")
print("="*75)
with open("data/processed/model2_yolox/annotations/instances_train.json", "r") as f:
    train_coco = json.load(f)

boxes = [ann["bbox"] for ann in train_coco["annotations"]]
areas = [b[2] * b[3] for b in boxes]
widths = [b[2] for b in boxes]
heights = [b[3] for b in boxes]

# COCO scale definitions: small (< 32x32 = 1024), medium (1024 to 96x96 = 9216), large (> 9216)
small_boxes = sum(1 for a in areas if a < 1024)
med_boxes = sum(1 for a in areas if 1024 <= a < 9216)
large_boxes = sum(1 for a in areas if a >= 9216)
total_boxes = len(boxes)

print(f"Total Train Annotations: {total_boxes} boxes across {len(train_coco['images'])} images")
print(f"Average Boxes per Image: {total_boxes / len(train_coco['images']):.2f}")
print(f"Small Lesions (< 32x32 px): {small_boxes} ({small_boxes / total_boxes * 100:.2f}%)")
print(f"Medium Lesions (32x32 to 96x96 px): {med_boxes} ({med_boxes / total_boxes * 100:.2f}%)")
print(f"Large Lesions (> 96x96 px): {large_boxes} ({large_boxes / total_boxes * 100:.2f}%)")

# Class support distribution
cat_counts = {}
for ann in train_coco["annotations"]:
    c_id = ann["category_id"]
    cat_counts[c_id] = cat_counts.get(c_id, 0) + 1

support_values = list(cat_counts.values())
print(f"Min class support: {min(support_values)} boxes")
print(f"Max class support: {max(support_values)} boxes")
print(f"Median class support: {np.median(support_values):.1f} boxes")
print(f"Classes with < 50 boxes: {sum(1 for v in support_values if v < 50)} / 115")
print(f"Classes with < 20 boxes: {sum(1 for v in support_values if v < 20)} / 115")

# --- PHASE 5 & 6: PREDICTION VISUAL INSPECTION ON 30 VALIDATION IMAGES ---
print("\n" + "="*75)
print(" PHASE 5 & 6: PREDICTION VISUAL INSPECTION (30 VAL SAMPLES & CONFIDENCE DISTRIBUTION)")
print("="*75)
with open("data/processed/model2_yolox/annotations/instances_val.json", "r") as f:
    val_coco = json.load(f)

img_id_to_anns = {}
for ann in val_coco["annotations"]:
    img_id_to_anns.setdefault(ann["image_id"], []).append(ann)

os.makedirs("reports/model2_diagnostics/predictions", exist_ok=True)

val_sample_images = val_coco["images"][:30]
categories_summary = {
    "correct_detections": 0,
    "wrong_class": 0,
    "wrong_location": 0,
    "missed_disease": 0,
    "false_positive": 0,
    "no_prediction": 0
}

conf_thresholds = [0.10, 0.20, 0.25, 0.40, 0.50]
conf_counts = {t: 0 for t in conf_thresholds}

for s_idx, img_info in enumerate(val_sample_images, 1):
    file_name = img_info["file_name"]
    img_path = os.path.join("data/processed/model2_dataset/images/val", file_name)
    if not os.path.exists(img_path):
        continue
    img_bgr = cv2.imread(img_path)
    gt_anns = img_id_to_anns.get(img_info["id"], [])
    
    # Run prediction at conf=0.05 to see all candidates
    preds_all = predict_disease(img_path, conf_threshold=0.05, nms_threshold=0.65, model_path="models/model2/best_model.pth")
    detections = preds_all.get("detections", [])
    
    for t in conf_thresholds:
        conf_counts[t] += sum(1 for d in detections if d["confidence"] >= t)
        
    # Categorization against GT
    preds_020 = [d for d in detections if d["confidence"] >= 0.15]
    
    # Draw comparison
    vis_img = img_bgr.copy()
    
    # Draw GT in GREEN
    for g in gt_anns:
        gx, gy, gw, gh = g["bbox"]
        g_cls = g["category_id"]
        g_name = source_classes[g_cls]
        cv2.rectangle(vis_img, (int(gx), int(gy)), (int(gx + gw), int(gy + gh)), (0, 255, 0), 2)
        cv2.putText(vis_img, f"GT: {g_name}", (int(gx), max(15, int(gy) - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
        
    # Draw Preds in RED / ORANGE
    if not preds_020:
        categories_summary["no_prediction"] += 1
    else:
        for p in preds_020:
            px1, py1, px2, py2 = map(int, p["bbox"])
            p_cls_name = p["disease"]
            p_conf = p["confidence"]
            
            # Check overlap with any GT
            best_iou = 0.0
            matched_gt = None
            for g in gt_anns:
                gx1, gy1, gw, gh = g["bbox"]
                gx2, gy2 = gx1 + gw, gy1 + gh
                
                # Compute IoU
                ix1 = max(px1, gx1)
                iy1 = max(py1, gy1)
                ix2 = min(px2, gx2)
                iy2 = min(py2, gy2)
                iw = max(0, ix2 - ix1)
                ih = max(0, iy2 - iy1)
                inter = iw * ih
                a_pred = (px2 - px1) * (py2 - py1)
                a_gt = gw * gh
                union = a_pred + a_gt - inter
                iou = inter / union if union > 0 else 0.0
                if iou > best_iou:
                    best_iou = iou
                    matched_gt = g
                    
            if best_iou >= 0.5:
                gt_name = source_classes[matched_gt["category_id"]]
                if p_cls_name == gt_name:
                    categories_summary["correct_detections"] += 1
                else:
                    categories_summary["wrong_class"] += 1
            elif best_iou >= 0.1:
                categories_summary["wrong_location"] += 1
            else:
                categories_summary["false_positive"] += 1
                
            cv2.rectangle(vis_img, (px1, py1), (px2, py2), (0, 0, 255), 2)
            cv2.putText(vis_img, f"P: {p_cls_name} {p_conf:.2f} (IoU:{best_iou:.2f})", (px1, max(30, py1 + 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            
    out_vis_path = f"reports/model2_diagnostics/predictions/val_pred_{s_idx:02d}_{file_name}"
    cv2.imwrite(out_vis_path, vis_img)

print(f"\nConfidence Distribution across 30 sample images (total {len(val_sample_images)} images):")
for t, count in conf_counts.items():
    print(f"  - Confidence >= {t:.2f}: {count} candidate detections ({count/30:.1f} per image)")

print("\nCategorization Breakdown across 30 sample images:")
for cat, count in categories_summary.items():
    print(f"  - {cat}: {count}")

print("Saved 30 annotated diagnostic prediction images to reports/model2_diagnostics/predictions/")
