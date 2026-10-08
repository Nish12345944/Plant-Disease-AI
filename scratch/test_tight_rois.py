"""Develop and test tight plant ROI extraction and comparative Model 1 inference."""
import os
import sys
import glob
import cv2
import numpy as np
import torch
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model1_test_app.inference import load_model, get_eval_transform, format_class_name

model, idx_to_class, class_to_idx, device, dev_name = load_model()
transform = get_eval_transform()

def detect_tight_plant_rois(img_bgr, max_rois=3):
    """Generate tight, focused candidate plant ROIs that isolate foliage clusters without grabbing the whole half-frame.
    
    1. Detect vegetation mask (green leaves, yellow/brown leaf spots, blueberries/fruits).
    2. Explicitly subtract person/lab coat/skin masks with morphological safety margin.
    3. Find localized connected components of foliage.
    4. For each component, crop a TIGHT bounding box enclosing the actual foliage with small (5-10%) padding.
    5. Discard components that are too small (<3000 px) or have poor plant density (<35%).
    6. For macro close-ups where the entire frame is the plant/fruit (plant coverage > 60%), use tight central crops or high-density patches.
    """
    h, w = img_bgr.shape[:2]
    total_pixels = h * w
    
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    Cr, Cb = ycrcb[:, :, 1], ycrcb[:, :, 2]
    
    B = img_bgr[:, :, 0].astype(np.float32)
    G = img_bgr[:, :, 1].astype(np.float32)
    R = img_bgr[:, :, 2].astype(np.float32)
    
    # --- Multi-spectral plant detection ---
    # Green foliage
    green_mask = (H >= 24) & (H <= 95) & (S >= 22) & (V >= 18)
    chroma_green = (G > (R + 6)) & (G > (B + 6)) & (S >= 18)
    # Yellow / chlorotic / blight
    yellow_mask = (H >= 15) & (H < 24) & (S >= 28) & (V >= 25)
    # Brown lesion / twigs
    brown_mask = (H >= 8) & (H < 18) & (S >= 25) & (V >= 18) & (V <= 170)
    # Warm fruit / flowers
    warm_mask = ((H <= 15) | (H >= 165)) & (S >= 35) & (V >= 30)
    # Blueberries / cool fruits / dark leaves
    # Dark blue berries: H in [95, 130], low to medium V, low to med S
    berry_mask = (H >= 95) & (H <= 135) & (S >= 15) & (S <= 95) & (V >= 15) & (V <= 135)
    # Purple / violet fruits
    cool_mask = (H >= 135) & (H <= 165) & (S >= 20) & (V >= 15)
    
    raw_plant_mask = (green_mask | chroma_green | yellow_mask | brown_mask | warm_mask | berry_mask | cool_mask).astype(np.uint8) * 255
    
    # --- Non-plant suppression (skin, lab coat, neutral background) ---
    skin_mask = (Cr >= 133) & (Cr <= 173) & (Cb >= 77) & (Cb <= 127)
    # White lab coat: high brightness, low saturation, near-equal RGB channels
    white_coat_mask = (V >= 160) & (S <= 35) & (np.abs(R - G) < 20) & (np.abs(G - B) < 20)
    # Nitrile gloves
    nitrile_mask = (B > (R + 45)) & (B > 115) & (H >= 95) & (H <= 130) & (S > 75)
    
    non_plant = (skin_mask | white_coat_mask | nitrile_mask).astype(np.uint8) * 255
    # Dilate non-plant slightly to avoid clipping clothing edges into plant ROIs
    kernel_dil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    non_plant_dil = cv2.dilate(non_plant, kernel_dil)
    
    clean_plant_mask = raw_plant_mask.copy()
    clean_plant_mask[non_plant_dil > 0] = 0
    
    plant_pixel_count = int(np.sum(clean_plant_mask > 0))
    plant_coverage = plant_pixel_count / total_pixels
    
    if plant_coverage < 0.005:
        # Genuinely no plant content
        return []
        
    # --- Is this a macro / close-up frame? ---
    # In close-ups (e.g. frames 12-20), plant coverage is high (>40%), and there is minimal/no lab coat in center
    coat_coverage = float(np.sum(white_coat_mask)) / total_pixels
    skin_coverage = float(np.sum(skin_mask)) / total_pixels
    
    is_macro_close_up = (plant_coverage > 0.40) and (coat_coverage < 0.10) and (skin_coverage < 0.05)
    
    candidates = []
    
    if is_macro_close_up:
        # For macro close-ups: generate high-detail square focal crops (e.g. center, high-sharpness patch, or full frame if aspect ratio is good)
        # 1. Full frame crop (scaled to square)
        cx, cy = w // 2, h // 2
        side = min(w, h)
        x1 = max(0, cx - side // 2)
        y1 = max(0, cy - side // 2)
        x2 = min(w, x1 + side)
        y2 = min(h, y1 + side)
        
        crop_bgr = img_bgr[y1:y2, x1:x2]
        crop_gray = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY)
        sharp = float(cv2.Laplacian(crop_gray, cv2.CV_64F).var())
        
        candidates.append({
            "box": [x1, y1, x2, y2],
            "raw_box": [0, 0, w, h],
            "score": 1.0,
            "plant_density": plant_coverage,
            "sharpness": sharp,
            "is_macro": True,
            "roi_pil": Image.fromarray(cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)),
            "roi_bgr": crop_bgr,
        })
        
        # 2. Tightest high-density berry/foliage cluster within close-up
        kernel_m = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        closed_m = cv2.morphologyEx(clean_plant_mask, cv2.MORPH_CLOSE, kernel_m)
        contours, _ = cv2.findContours(closed_m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            if bw * bh > total_pixels * 0.15 and bw > 120 and bh > 120:
                # Tight square around this cluster
                mcx, mcy = x + bw // 2, y + bh // 2
                mside = max(bw, bh)
                mside = int(mside * 1.05)
                mx1 = max(0, mcx - mside // 2)
                my1 = max(0, mcy - mside // 2)
                mx2 = min(w, mx1 + mside)
                my2 = min(h, my1 + mside)
                if mx2 - mx1 > 64 and my2 - my1 > 64:
                    sub_bgr = img_bgr[my1:my2, mx1:mx2]
                    sub_gray = cv2.cvtColor(sub_bgr, cv2.COLOR_BGR2GRAY)
                    sub_sharp = float(cv2.Laplacian(sub_gray, cv2.CV_64F).var())
                    candidates.append({
                        "box": [mx1, my1, mx2, my2],
                        "raw_box": [x, y, x + bw, y + bh],
                        "score": 0.9,
                        "plant_density": float(np.sum(clean_plant_mask[my1:my2, mx1:mx2] > 0)) / ((mx2 - mx1) * (my2 - my1)),
                        "sharpness": sub_sharp,
                        "is_macro": True,
                        "roi_pil": Image.fromarray(cv2.cvtColor(sub_bgr, cv2.COLOR_BGR2RGB)),
                        "roi_bgr": sub_bgr,
                    })
    else:
        # Wide / medium shots (greenhouse with person & background)
        # Use moderate closing kernel to keep distinct plant clusters separate
        kernel_c = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
        closed = cv2.morphologyEx(clean_plant_mask, cv2.MORPH_CLOSE, kernel_c)
        kernel_o = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cleaned = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_o)
        
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            box_area = bw * bh
            
            # Minimum size: at least 100x100 or 1.5% of total frame, and maximum size capped so it doesn't take the whole half-frame
            if bw < 80 or bh < 80 or box_area < (total_pixels * 0.015):
                continue
            
            # Check plant density inside the raw bounding box
            roi_mask = clean_plant_mask[y:y+bh, x:x+bw]
            plant_density = float(np.sum(roi_mask > 0)) / max(1, box_area)
            if plant_density < 0.25:
                continue
                
            # Check non-plant contamination (e.g. lab coat inside box)
            roi_coat = white_coat_mask[y:y+bh, x:x+bw]
            coat_ratio = float(np.sum(roi_coat)) / max(1, box_area)
            if coat_ratio > 0.25:
                continue
                
            roi_bgr = img_bgr[y:y+bh, x:x+bw]
            roi_gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
            sharpness = float(cv2.Laplacian(roi_gray, cv2.CV_64F).var())
            
            # Form a TIGHT square bounding box around this foliage cluster (max 10% padding)
            cx, cy = x + bw // 2, y + bh // 2
            side = int(max(bw, bh) * 1.08)
            # Cap side so it cannot exceed 60% of frame dimension
            side = min(side, int(h * 0.85))
            
            x1 = max(0, cx - side // 2)
            y1 = max(0, cy - side // 2)
            x2 = min(w, x1 + side)
            y2 = min(h, y1 + side)
            
            # Re-adjust if hitting borders
            if x2 - x1 < side and x1 > 0:
                x1 = max(0, x2 - side)
            if y2 - y1 < side and y1 > 0:
                y1 = max(0, y2 - side)
                
            if (x2 - x1) < 64 or (y2 - y1) < 64:
                continue
                
            crop_bgr = img_bgr[y1:y2, x1:x2]
            crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
            crop_pil = Image.fromarray(crop_rgb)
            
            # Score: reward high plant density, clean foliage, sharpness; penalize huge boxes with low density
            score = plant_density * 0.5 + min(1.0, sharpness / 150.0) * 0.3 + min(1.0, box_area / (total_pixels * 0.15)) * 0.2
            
            candidates.append({
                "box": [x1, y1, x2, y2],
                "raw_box": [x, y, x + bw, y + bh],
                "score": score,
                "plant_density": plant_density,
                "sharpness": sharpness,
                "is_macro": False,
                "roi_pil": crop_pil,
                "roi_bgr": crop_bgr,
            })

    # Sort candidates by score descending
    candidates.sort(key=lambda c: c["score"], reverse=True)
    
    # NMS across candidate boxes (IoU threshold 0.35)
    selected = []
    for cand in candidates:
        b1 = cand["box"]
        overlap = False
        for s in selected:
            b2 = s["box"]
            ix1 = max(b1[0], b2[0])
            iy1 = max(b1[1], b2[1])
            ix2 = min(b1[2], b2[2])
            iy2 = min(b1[3], b2[3])
            iw = max(0, ix2 - ix1)
            ih = max(0, iy2 - iy1)
            inter = iw * ih
            a1 = (b1[2] - b1[0]) * (b1[3] - b1[1])
            a2 = (b2[2] - b2[0]) * (b2[3] - b2[1])
            union = a1 + a2 - inter
            iou = inter / union if union > 0 else 0.0
            if iou > 0.35:
                overlap = True
                break
        if not overlap:
            selected.append(cand)
            if len(selected) >= max_rois:
                break
                
    return selected

# Test on all 24 frames
os.makedirs("reports/video_debug", exist_ok=True)
frame_files = sorted(glob.glob("scratch/all_video_frames/frame_*.jpg"))
print(f"Testing on {len(frame_files)} frames...\n")

for f_path in frame_files:
    fname = os.path.basename(f_path)
    base_name = os.path.splitext(fname)[0]
    img_bgr = cv2.imread(f_path)
    
    rois = detect_tight_plant_rois(img_bgr)
    
    # Save original
    cv2.imwrite(f"reports/video_debug/{base_name}_original.jpg", img_bgr)
    
    if not rois:
        print(f"[{fname}] NO ROIs FOUND")
        continue
        
    for r_idx, r in enumerate(rois, 1):
        box = r["box"]
        roi_bgr = r["roi_bgr"]
        roi_pil = r["roi_pil"]
        
        # Run Model 1 on this tight ROI
        tensor = transform(roi_pil).unsqueeze(0).to(device)
        with torch.no_grad():
            logits = model(tensor)
            probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
            
        top_idx = int(np.argmax(probs))
        top_cls = idx_to_class[top_idx]
        top_conf = float(probs[top_idx])
        
        # Save debug ROI image
        cv2.imwrite(f"reports/video_debug/{base_name}_roi_{r_idx}.jpg", roi_bgr)
        
        print(f"[{fname}] ROI #{r_idx} Box: {box} | Sharpness: {r['sharpness']:.1f} | Macro: {r.get('is_macro', False)} | Model 1: {format_class_name(top_cls)} ({top_conf*100:.2f}%)")

print("\nDebug images written to reports/video_debug/")
