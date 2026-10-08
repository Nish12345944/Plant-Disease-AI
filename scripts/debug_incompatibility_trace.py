"""
DEBUG SCRIPT: MODEL 1 -> MODEL 2 V3 CROP/DISEASE INCOMPATIBILITY TRACE
======================================================================
1. Loads Model 1 (EfficientNet-B2, models/model1/best_model.pth).
2. Loads Model 2 V3 (EfficientNet-B2, models/model2_classifier_v3/best_model.pth).
3. Loads crop-disease compatibility mapping.
4. Evaluates representative tomato leaf images.
5. Logs:
   - Model 1 top-5 crop predictions & probabilities.
   - Model 2 V3 top-10 raw disease predictions & probabilities.
   - Compatibility validation (VALID vs INVALID).
   - Crop-aware masked predictions & final diagnosis.
6. Saves reports/debug/tomato_apple_scab_case.json.
"""

import json
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import efficientnet_b2

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
DEBUG_DIR = PROJECT_ROOT / "reports" / "debug"
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[DEBUG TRACE] Device: {device}")

# 1. Verify and Load Model 1
m1_ckpt = PROJECT_ROOT / "models" / "model1" / "best_model.pth"
m1_map = PROJECT_ROOT / "models" / "model1" / "class_mapping.json"
assert m1_ckpt.exists(), f"Model 1 checkpoint missing: {m1_ckpt}"
print(f"[DEBUG TRACE] Loading Model 1 from: {m1_ckpt}")

with open(m1_map, "r") as f:
    m1_map_data = json.load(f)
m1_class_to_idx = m1_map_data["class_to_idx"]
m1_idx_to_class = {int(k): v for k, v in m1_map_data["idx_to_class"].items()}
m1_num_classes = len(m1_class_to_idx)

model1 = efficientnet_b2(weights=None)
model1.classifier[1] = nn.Linear(model1.classifier[1].in_features, m1_num_classes)
m1_sd = torch.load(m1_ckpt, map_location=device, weights_only=False)
if "model_state_dict" in m1_sd:
    m1_sd = m1_sd["model_state_dict"]
elif "state_dict" in m1_sd:
    m1_sd = m1_sd["state_dict"]
model1.load_state_dict(m1_sd)
model1.to(device)
model1.eval()
print(f"[DEBUG TRACE] Model 1 successfully loaded with {m1_num_classes} classes.")

# 2. Verify and Load Model 2 V3
m2_ckpt = PROJECT_ROOT / "models" / "model2_classifier_v3" / "best_model.pth"
m2_map = PROJECT_ROOT / "models" / "model2_classifier_v3" / "class_mapping.json"
assert m2_ckpt.exists(), f"Model 2 V3 checkpoint missing: {m2_ckpt}"
print(f"[DEBUG TRACE] Loading Model 2 V3 from: {m2_ckpt}")

with open(m2_map, "r") as f:
    m2_map_data = json.load(f)
if "class_to_idx" in m2_map_data:
    m2_class_to_idx = m2_map_data["class_to_idx"]
    m2_idx_to_class = {int(k): v for k, v in m2_map_data["idx_to_class"].items()}
else:
    m2_class_to_idx = m2_map_data
    m2_idx_to_class = {int(v): k for k, v in m2_map_data.items()}
m2_num_classes = len(m2_class_to_idx)

model2_v3 = efficientnet_b2(weights=None)
model2_v3.classifier[1] = nn.Linear(model2_v3.classifier[1].in_features, m2_num_classes)
m2_sd = torch.load(m2_ckpt, map_location=device, weights_only=False)
if "model_state_dict" in m2_sd:
    m2_sd = m2_sd["model_state_dict"]
elif "state_dict" in m2_sd:
    m2_sd = m2_sd["state_dict"]
model2_v3.load_state_dict(m2_sd)
model2_v3.to(device)
model2_v3.eval()
print(f"[DEBUG TRACE] Model 2 V3 successfully loaded with {m2_num_classes} classes.")

# 3. Load Crop-Disease Compatibility Mapping
compat_map_path = PROJECT_ROOT / "data" / "processed" / "model2_organized_crop_disease_mapping.json"
if not compat_map_path.exists():
    compat_map_path = PROJECT_ROOT / "data" / "processed" / "model2_classifier_crop_disease_mapping.json"
with open(compat_map_path, "r") as f:
    crop_disease_mapping = json.load(f)
print(f"[DEBUG TRACE] Loaded crop-disease compatibility mapping for {len(crop_disease_mapping)} crops.")

def is_compatible(crop: str, disease: str) -> bool:
    """Check if crop and disease are biologically valid."""
    if not disease or disease.lower() == "healthy":
        return True
    if not crop:
        return False
    crop_clean = crop.lower().strip()
    disease_clean = disease.lower().strip()
    
    # Check direct prefix
    if disease_clean.startswith(f"{crop_clean}__"):
        return True
    
    # Check alias mapping
    crop_aliases = {"french_bean": "bean", "bean": "french_bean", "capsicum": "bell_pepper", "cherry_tomato": "tomato"}
    alt_crop = crop_aliases.get(crop_clean)
    if alt_crop and disease_clean.startswith(f"{alt_crop}__"):
        return True
    
    # Check registered diseases in map
    valid_diseases = crop_disease_mapping.get(crop_clean, [])
    if disease_clean in valid_diseases:
        return True
    if alt_crop and disease_clean in crop_disease_mapping.get(alt_crop, []):
        return True
    
    return False

# Transforms
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
m1_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])
m2_tf = transforms.Compose([
    transforms.Resize((260, 260)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])

# Find a test tomato image
tomato_candidates = list((PROJECT_ROOT / "data" / "external" / "end_to_end_test" / "tomato").glob("*.jpg"))
if not tomato_candidates:
    tomato_candidates = list((PROJECT_ROOT / "data" / "processed" / "model2_organized" / "test" / "tomato").rglob("*.jpg"))

test_image_path = tomato_candidates[0]
print(f"\n[DEBUG TRACE] Evaluating Test Image: {test_image_path}")

pil_img = Image.open(test_image_path).convert("RGB")

# Stage 1: Model 1
t1 = m1_tf(pil_img).unsqueeze(0).to(device)
with torch.no_grad():
    m1_probs = torch.softmax(model1(t1), dim=1).squeeze(0).cpu().numpy()

m1_top5_idx = np.argsort(m1_probs)[-5:][::-1]
model1_top5 = [
    {"crop": m1_idx_to_class[int(i)], "probability": float(m1_probs[i]), "percentage": f"{m1_probs[i]*100:.2f}%"}
    for i in m1_top5_idx
]
pred_crop = model1_top5[0]["crop"]
crop_conf = model1_top5[0]["probability"]

print(f"\nMODEL 1 OUTPUT:")
print(f"  Predicted Crop: {pred_crop} (Confidence: {crop_conf:.4f})")
print(f"  Top-5 Crop Predictions:")
for r in model1_top5:
    print(f"    - {r['crop']:<15}: {r['percentage']}")

# Stage 2: Model 2 V3
t2 = m2_tf(pil_img).unsqueeze(0).to(device)
with torch.no_grad():
    m2_probs = torch.softmax(model2_v3(t2), dim=1).squeeze(0).cpu().numpy()

m2_top10_idx = np.argsort(m2_probs)[-10:][::-1]
model2_top10 = [
    {
        "class_id": int(i),
        "class_name": m2_idx_to_class[int(i)],
        "probability": float(m2_probs[i]),
        "percentage": f"{m2_probs[i]*100:.2f}%",
        "is_compatible_with_m1_crop": is_compatible(pred_crop, m2_idx_to_class[int(i)])
    }
    for i in m2_top10_idx
]

raw_top_m2_class = model2_top10[0]["class_name"]
raw_top_m2_conf = model2_top10[0]["probability"]
raw_compat = is_compatible(pred_crop, raw_top_m2_class)

print(f"\nMODEL 2 V3 OUTPUT (RAW 117 CLASSES):")
print(f"  Raw Top-1 Prediction: {raw_top_m2_class} (Confidence: {raw_top_m2_conf:.4f})")
print(f"  Compatibility with '{pred_crop}': {'VALID' if raw_compat else 'INVALID'}")
print(f"  Top-10 Raw Class Predictions:")
for r in model2_top10:
    status_str = "VALID" if r["is_compatible_with_m1_crop"] else "INVALID (MASKED)"
    print(f"    [{r['class_id']:3d}] {r['class_name']:<35} : {r['percentage']:<8} | {status_str}")

# Stage 3: Crop-Aware Compatibility Filtering & Probability Masking
compatible_candidates = [r for r in model2_top10 if r["is_compatible_with_m1_crop"]]

final_status = "uncertain"
final_disease = None
final_disease_conf = 0.0

if compatible_candidates:
    best_compat = compatible_candidates[0]
    final_disease_conf = best_compat["probability"]
    if best_compat["class_name"] == "healthy":
        if final_disease_conf >= 0.50:
            final_status = "healthy"
            final_disease = None
    else:
        if final_disease_conf >= 0.20:
            final_status = "diseased"
            final_disease = best_compat["class_name"]

print(f"\n==================================================")
print(f"FINAL STRUCTURED DIAGNOSIS (AFTER COMPATIBILITY):")
print(f"  Crop: {pred_crop}")
print(f"  Crop Confidence: {crop_conf:.4f}")
print(f"  Status: {final_status}")
print(f"  Disease: {final_disease}")
print(f"  Disease Confidence: {final_disease_conf:.4f}")
print(f"==================================================")

# Save failure case report
debug_report = {
    "image": str(test_image_path),
    "model1_predicted_crop": pred_crop,
    "model1_crop_confidence": crop_conf,
    "model1_top5": model1_top5,
    "model2_raw_predicted_class": raw_top_m2_class,
    "model2_raw_confidence": raw_top_m2_conf,
    "raw_compatibility_result": "VALID" if raw_compat else "INVALID",
    "model2_top10": model2_top10,
    "compatible_candidates_found": len(compatible_candidates),
    "best_compatible_candidate": compatible_candidates[0] if compatible_candidates else None,
    "final_prediction": {
        "crop": pred_crop,
        "crop_confidence": crop_conf,
        "status": final_status,
        "disease": final_disease,
        "disease_confidence": final_disease_conf,
    },
    "diagnosis_contract": {
        "apple_scab_prevented_on_tomato": not (pred_crop == "tomato" and final_disease == "apple__scab"),
        "healthy_invariant_satisfied": not (final_status == "healthy" and final_disease is not None),
    }
}

out_path = DEBUG_DIR / "tomato_apple_scab_case.json"
with open(out_path, "w") as f:
    json.dump(debug_report, f, indent=2)

print(f"\nSaved debug report to: {out_path}")
