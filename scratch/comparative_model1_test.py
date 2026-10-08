"""Model 1 Comparative Debug Test across A) Full frame, B) Large ROI, C) Tight ROI, D) Blueberry close-up ROI."""
import os
import sys
import cv2
import numpy as np
import torch
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model1_test_app.inference import load_model, get_eval_transform, format_class_name
from scratch.test_tight_rois import detect_tight_plant_rois

model, idx_to_class, class_to_idx, device, dev_name = load_model()
transform = get_eval_transform()

def eval_pil(pil_img):
    tensor = transform(pil_img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
    top_indices = np.argsort(probs)[::-1][:3]
    return [
        (idx_to_class[int(i)], format_class_name(idx_to_class[int(i)]), float(probs[i]))
        for i in top_indices
    ]

# Frame 08 (idx 072 - Wide Greenhouse shot with person in center and plants on both sides)
f8_bgr = cv2.imread("scratch/all_video_frames/frame_08_idx_072.jpg")
f8_rgb = cv2.cvtColor(f8_bgr, cv2.COLOR_BGR2RGB)

# A. Full frame (Frame 8)
pil_full = Image.fromarray(f8_rgb)
top3_full = eval_pil(pil_full)

# B. Large old ROI [511, 0, 1280, 720]
pil_large = Image.fromarray(f8_rgb[0:720, 511:1280])
top3_large = eval_pil(pil_large)

# C. New tight plant ROI on Frame 8 [649, 108, 1261, 720]
tight_rois_f8 = detect_tight_plant_rois(f8_bgr)
pil_tight = tight_rois_f8[0]["roi_pil"]
box_tight = tight_rois_f8[0]["box"]
top3_tight = eval_pil(pil_tight)

# D. Actual Blueberry close-up ROI (Frame 14 - idx 135)
f14_bgr = cv2.imread("scratch/all_video_frames/frame_14_idx_135.jpg")
f14_rgb = cv2.cvtColor(f14_bgr, cv2.COLOR_BGR2RGB)
tight_rois_f14 = detect_tight_plant_rois(f14_bgr)
pil_macro = tight_rois_f14[0]["roi_pil"]
box_macro = tight_rois_f14[0]["box"]
top3_macro = eval_pil(pil_macro)

print("="*70)
print(" COMPARATIVE MODEL 1 INFERENCE TEST")
print("="*70)

print("\n[A] FULL FRAME (Frame #08 - 1280x720):")
for r, (c, l, p) in enumerate(top3_full, 1):
    print(f"  Rank {r}: {l:<20} {p*100:6.2f}%")

print(f"\n[B] OLD LARGE ROI (Frame #08 - [511, 0, 1280, 720]):")
for r, (c, l, p) in enumerate(top3_large, 1):
    print(f"  Rank {r}: {l:<20} {p*100:6.2f}%")

print(f"\n[C] NEW TIGHT PLANT ROI (Frame #08 - {box_tight}):")
for r, (c, l, p) in enumerate(top3_tight, 1):
    print(f"  Rank {r}: {l:<20} {p*100:6.2f}%")

print(f"\n[D] ACTUAL BLUEBERRY CLOSE-UP ROI (Frame #14 - {box_macro}):")
for r, (c, l, p) in enumerate(top3_macro, 1):
    print(f"  Rank {r}: {l:<20} {p*100:6.2f}%")

print("="*70)
