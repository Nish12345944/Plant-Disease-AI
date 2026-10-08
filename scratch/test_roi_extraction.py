"""Test script to develop and verify candidate plant ROI extraction on gemini_generated_video_17a86e10.mp4."""
import os
import sys
import glob
import cv2
import numpy as np
import torch
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model1_test_app.inference import load_model, get_eval_transform, format_class_name

# Load Model 1
model, idx_to_class, class_to_idx, device, dev_name = load_model(
    checkpoint_path="models/model1/best_model.pth",
    mapping_path="models/model1/class_mapping.json",
    config_path="models/model1/config.json",
)
transform = get_eval_transform()

def extract_plant_rois(img_bgr, max_rois=3, min_area_ratio=0.015):
    """Extract 1-3 high-quality plant-focused candidate ROIs from a wide frame."""
    h, w = img_bgr.shape[:2]
    total_pixels = h * w
    
    # Color spaces
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    Cr, Cb = ycrcb[:, :, 1], ycrcb[:, :, 2]
    
    B, G, R = img_bgr[:, :, 0].astype(np.float32), img_bgr[:, :, 1].astype(np.float32), img_bgr[:, :, 2].astype(np.float32)
    
    # Vegetation detection
    # 1. Green foliage
    green_mask = (H >= 25) & (H <= 95) & (S >= 28) & (V >= 20)
    # 2. Chromatic green
    chroma_green = (G > (R + 8)) & (G > (B + 8)) & (S >= 20)
    # 3. Yellow/chlorotic/blight leaves
    yellow_mask = (H >= 15) & (H < 25) & (S >= 35) & (V >= 30)
    # 4. Brown lesions / stems
    brown_mask = (H >= 8) & (H < 18) & (S >= 30) & (V >= 20) & (V <= 170)
    # 5. Warm fruit / flower
    warm_mask = ((H <= 15) | (H >= 165)) & (S >= 38) & (V >= 35)
    
    plant_mask = (green_mask | chroma_green | yellow_mask | brown_mask | warm_mask).astype(np.uint8) * 255
    
    # Suppress non-plant regions (human skin, lab coats, blue nitrile gloves)
    skin_mask = (Cr >= 133) & (Cr <= 173) & (Cb >= 77) & (Cb <= 127)
    white_coat_mask = (V >= 175) & (S <= 35) & (np.abs(R - G) < 15) & (np.abs(G - B) < 15)
    nitrile_mask = (B > (R + 45)) & (B > 115) & (H >= 95) & (H <= 130)
    
    non_plant_mask = skin_mask | white_coat_mask | nitrile_mask
    plant_mask[non_plant_mask] = 0
    
    total_plant_pixels = int(np.sum(plant_mask > 0))
    plant_coverage = total_plant_pixels / total_pixels
    
    if plant_coverage < 0.008:
        # Genuinely no plant matter
        return []
    
    # Morphological closing to group leaves on the same plant together
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed = cv2.morphologyEx(plant_mask, cv2.MORPH_CLOSE, kernel_close)
    
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    cleaned = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_open)
    
    # Find contours of candidate plant clusters
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    candidates = []
    min_box_area = total_pixels * min_area_ratio
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, bw, bh = cv2.boundingRect(cnt)
        box_area = bw * bh
        
        if box_area < min_box_area or bw < 60 or bh < 60:
            continue
            
        # Crop region from plant mask to check density
        roi_plant_mask = plant_mask[y:y+bh, x:x+bw]
        plant_density = float(np.sum(roi_plant_mask > 0)) / box_area
        
        if plant_density < 0.15:
            continue
            
        # Calculate sharpness of the cropped BGR region
        roi_bgr = img_bgr[y:y+bh, x:x+bw]
        roi_gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
        sharpness = float(cv2.Laplacian(roi_gray, cv2.CV_64F).var())
        
        # Penalize if it contains high skin/coat ratio
        roi_non_plant = non_plant_mask[y:y+bh, x:x+bw]
        non_plant_ratio = float(np.sum(roi_non_plant)) / box_area
        
        # Score calculation
        size_score = min(1.0, box_area / (total_pixels * 0.40))
        sharp_score = min(1.0, sharpness / 200.0)
        density_score = plant_density
        penalty = 1.0 - (non_plant_ratio * 0.8)
        
        score = (0.35 * size_score + 0.35 * density_score + 0.30 * sharp_score) * max(0.1, penalty)
        
        # Expand bounding box to square-like crop with padding for Model 1
        cx, cy = x + bw // 2, y + bh // 2
        side = max(bw, bh)
        side = int(side * 1.15)  # 15% padding
        
        x1 = max(0, cx - side // 2)
        y1 = max(0, cy - side // 2)
        x2 = min(w, x1 + side)
        y2 = min(h, y1 + side)
        # Re-adjust x1/y1 if hitting edges
        if x2 - x1 < side and x1 > 0:
            x1 = max(0, x2 - side)
        if y2 - y1 < side and y1 > 0:
            y1 = max(0, y2 - side)
            
        candidates.append({
            "box": [x1, y1, x2, y2],
            "raw_box": [x, y, x + bw, y + bh],
            "score": score,
            "plant_density": plant_density,
            "sharpness": sharpness,
            "area": (x2 - x1) * (y2 - y1)
        })
        
    if not candidates and plant_coverage >= 0.02:
        # Fallback: create ROI around bounding box of all plant pixels
        pts = cv2.findNonZero(plant_mask)
        if pts is not None:
            x, y, bw, bh = cv2.boundingRect(pts)
            cx, cy = x + bw // 2, y + bh // 2
            side = int(max(bw, bh) * 1.1)
            x1 = max(0, cx - side // 2)
            y1 = max(0, cy - side // 2)
            x2 = min(w, x1 + side)
            y2 = min(h, y1 + side)
            candidates.append({
                "box": [x1, y1, x2, y2],
                "raw_box": [x, y, x + bw, y + bh],
                "score": 0.5,
                "plant_density": plant_coverage,
                "sharpness": 50.0,
                "area": (x2 - x1) * (y2 - y1)
            })
            
    # Sort by score descending
    candidates.sort(key=lambda c: c["score"], reverse=True)
    
    # NMS across candidate boxes
    selected = []
    for cand in candidates:
        b1 = cand["box"]
        overlap = False
        for s in selected:
            b2 = s["box"]
            # Compute IoU
            ix1 = max(b1[0], b2[0])
            iy1 = max(b1[1], b2[1])
            ix2 = min(b1[2], b2[2])
            iy2 = min(b1[3], b2[3])
            iw = max(0, ix2 - ix1)
            ih = max(0, iy2 - iy1)
            inter = iw * ih
            union = cand["area"] + s["area"] - inter
            iou = inter / union if union > 0 else 0
            if iou > 0.40:
                overlap = True
                break
        if not overlap:
            selected.append(cand)
            if len(selected) >= max_rois:
                break
                
    return selected

# Test on the 6 extracted frames
frame_files = sorted(glob.glob("scratch/video_test_frames/*.jpg"))
print(f"\nEvaluating {len(frame_files)} test frames with candidate plant ROI extractor:\n")

os.makedirs("scratch/roi_visualizations", exist_ok=True)

for f_path in frame_files:
    fname = os.path.basename(f_path)
    img_bgr = cv2.imread(f_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    rois = extract_plant_rois(img_bgr)
    print(f"[{fname}] Found {len(rois)} candidate plant ROIs")
    
    vis_img = img_bgr.copy()
    for idx, r in enumerate(rois, 1):
        x1, y1, x2, y2 = r["box"]
        # Crop ROI for Model 1
        roi_rgb = img_rgb[y1:y2, x1:x2]
        pil_roi = Image.fromarray(roi_rgb)
        
        # Model 1 inference
        tensor = transform(pil_roi).unsqueeze(0).to(device)
        with torch.no_grad():
            logits = model(tensor)
            probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
            
        top_idx = int(np.argmax(probs))
        top_cls = idx_to_class[top_idx]
        top_conf = float(probs[top_idx])
        
        print(f"  -> ROI #{idx} [{x1},{y1},{x2},{y2}] Score: {r['score']:.3f} | Pred: {format_class_name(top_cls)} ({top_conf*100:.1f}%)")
        
        cv2.rectangle(vis_img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        label_text = f"ROI {idx}: {format_class_name(top_cls)} {top_conf*100:.1f}%"
        cv2.putText(vis_img, label_text, (x1 + 5, max(25, y1 + 25)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
    cv2.imwrite(f"scratch/roi_visualizations/annotated_{fname}", vis_img)

print("\nDone! Visualizations saved to scratch/roi_visualizations/")
