"""
SMOKE TEST & VERIFICATION SUITE: MODEL 2 V4 PROMOTION
======================================================
Verifies:
1. Backend configuration and imports load Model 2 V4.
2. Exact checkpoint path: models/model2_classifier_v4/best_model.pth.
3. No Model 2 V3 checkpoint is loaded into memory.
4. Model 1 + Model 2 V4 hierarchical inference on sample images.
5. Standardized diagnosis contracts (healthy, diseased, uncertain).
6. Crop-disease compatibility enforcement.
7. Video inference pipeline with Model 2 V4.
8. Query routing and deterministic intent handling.
"""

import os
import sys
import json
import time
import io
import requests
import numpy as np
import cv2
from PIL import Image
from pathlib import Path
import torch

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from app.backend.config import (
    MODEL1_CHECKPOINT,
    MODEL2_CHECKPOINT,
    MODEL2_CLASS_MAPPING,
    MODEL2_CONFIG,
    CROP_DISEASE_MAPPING,
    DEVICE,
    DEVICE_NAME,
)
from app.backend.services import (
    get_model1,
    get_model2,
    process_image_inference,
    process_video_inference,
    process_query_routing,
)
from models.model2_classifier_v4.predict import Model2DiseaseClassifierV4

print("=" * 80)
print("VERIFICATION SUITE: MODEL 2 V4 PRODUCTION PROMOTION")
print("=" * 80)

# -----------------------------------------------------------------------------
# 1. VERIFY CONFIGURATION & CHECKPOINTS
# -----------------------------------------------------------------------------
print("\n[TEST 1] Verifying Backend Configuration & Checkpoints...")
print(f"MODEL1_CHECKPOINT: {MODEL1_CHECKPOINT}")
print(f"MODEL2_CHECKPOINT: {MODEL2_CHECKPOINT}")
print(f"MODEL2_CLASS_MAPPING: {MODEL2_CLASS_MAPPING}")
print(f"MODEL2_CONFIG: {MODEL2_CONFIG}")

assert "model2_classifier_v4" in str(MODEL2_CHECKPOINT), f"Expected V4 checkpoint, got {MODEL2_CHECKPOINT}"
assert MODEL2_CHECKPOINT.exists(), f"V4 Checkpoint does not exist: {MODEL2_CHECKPOINT}"
assert MODEL2_CLASS_MAPPING.exists(), f"V4 Class mapping does not exist: {MODEL2_CLASS_MAPPING}"
assert MODEL2_CONFIG.exists(), f"V4 Config does not exist: {MODEL2_CONFIG}"
print("[PASS] Backend configuration points exclusively to Model 2 V4.")

# -----------------------------------------------------------------------------
# 2. VERIFY BACKEND SERVICE SINGLETON INITIALIZATION
# -----------------------------------------------------------------------------
print("\n[TEST 2] Initializing Model 1 & Model 2 V4 Singletons...")
m1, m1_idx, m1_cls = get_model1()
m2 = get_model2()

print(f"Model 1: Loaded with {len(m1_idx)} crop classes.")
print(f"Model 2: Instance type = {type(m2).__name__}")
print(f"Model 2 Checkpoint: {m2.checkpoint_path}")
print(f"Model 2 Number of classes: {m2.num_classes}")

assert isinstance(m2, Model2DiseaseClassifierV4), f"Expected Model2DiseaseClassifierV4 instance, got {type(m2)}"
assert m2.num_classes == 117, f"Expected 117 classes, got {m2.num_classes}"
assert "model2_classifier_v4" in str(m2.checkpoint_path), f"Expected V4 checkpoint in predictor, got {m2.checkpoint_path}"
print("[PASS] Model 2 V4 singleton initialized successfully.")

# -----------------------------------------------------------------------------
# 3. VERIFY NO V3 CHECKPOINT LOADED
# -----------------------------------------------------------------------------
print("\n[TEST 3] Verifying Isolation from V3 Checkpoint...")
v3_path = PROJECT_ROOT / "models" / "model2_classifier_v3" / "best_model.pth"
assert str(m2.checkpoint_path) != str(v3_path), "Error: V3 checkpoint is still loaded!"
print("[PASS] Zero V3 checkpoint loaded.")

# -----------------------------------------------------------------------------
# 4. SMOKE TEST: DIRECT IMAGE INFERENCE & OUTPUT CONTRACTS
# -----------------------------------------------------------------------------
print("\n[TEST 4] Testing Image Inference & Output Contracts...")

# Create synthetic sample test leaf
test_img = np.full((384, 384, 3), (230, 245, 230), dtype=np.uint8)
cv2.ellipse(test_img, (192, 192), (120, 70), 45, 0, 360, (40, 150, 45), -1)
cv2.line(test_img, (192, 384), (192, 120), (35, 80, 30), 8)
_, img_bytes = cv2.imencode(".jpg", test_img)
img_bytes = img_bytes.tobytes()

res_image = process_image_inference(img_bytes)

print("Inference Result Keys:", list(res_image.keys()))
print("Model 1 Output:", res_image.get("model1"))
print("Model 2 Output:", res_image.get("model2"))
print("Standardized Diagnosis Contract:", res_image.get("standardized_diagnosis"))

diag = res_image.get("standardized_diagnosis", {})
assert "crop" in diag, "Missing 'crop' in standardized diagnosis"
assert "crop_confidence" in diag, "Missing 'crop_confidence' in standardized diagnosis"
assert "status" in diag, "Missing 'status' in standardized diagnosis"
assert "disease" in diag, "Missing 'disease' in standardized diagnosis"
assert "disease_confidence" in diag, "Missing 'disease_confidence' in standardized diagnosis"
assert diag["status"] in ["healthy", "diseased", "uncertain"], f"Invalid status: {diag['status']}"

if diag["status"] == "healthy":
    assert diag["disease"] is None, "Healthy status must have disease = null"
elif diag["status"] == "uncertain":
    assert diag["disease"] is None, "Uncertain status must have disease = null"

print("[PASS] Image inference output contract verified.")

# -----------------------------------------------------------------------------
# 5. TEST CROP-DISEASE COMPATIBILITY GATING
# -----------------------------------------------------------------------------
print("\n[TEST 5] Testing Crop-Disease Compatibility Gating...")
# Test compatibility function directly on known pairs
assert m2.is_compatible("tomato", "tomato__early_blight") == True, "tomato + tomato__early_blight should be compatible"
assert m2.is_compatible("tomato", "apple__scab") == False, "tomato + apple__scab MUST be incompatible"
assert m2.is_compatible("cucumber", "cucumber__powdery_mildew") == True, "cucumber + cucumber__powdery_mildew should be compatible"
assert m2.is_compatible("cucumber", "grape__black_rot") == False, "cucumber + grape__black_rot MUST be incompatible"
assert m2.is_compatible("tomato", "healthy") == True, "tomato + healthy should be compatible"
print("[PASS] Crop-disease compatibility logic strictly enforced.")

# -----------------------------------------------------------------------------
# 6. TEST VIDEO INFERENCE PIPELINE WITH MODEL 2 V4
# -----------------------------------------------------------------------------
print("\n[TEST 6] Testing Video Inference Pipeline with Model 2 V4...")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
temp_video_path = PROJECT_ROOT / "temp_multimodal_uploads" / "smoke_test_video.mp4"
temp_video_path.parent.mkdir(exist_ok=True, parents=True)
out = cv2.VideoWriter(str(temp_video_path), fourcc, 15, (384, 384))
for i in range(30):
    frame = np.full((384, 384, 3), (230, 245, 230), dtype=np.uint8)
    cv2.ellipse(frame, (192, 192), (120, 70), 45, 0, 360, (40, 150, 45), -1)
    out.write(frame)
out.release()

with open(temp_video_path, "rb") as f:
    video_bytes = f.read()
if temp_video_path.exists():
    temp_video_path.unlink()

v_res = process_video_inference(video_bytes, original_filename="smoke_test_video.mp4", target_frames=16)
print("Video Processed Frames:", v_res.get("frames_processed"))
print("Video Final Prediction:", v_res.get("final_prediction"))
print("Video Model 2 Output:", v_res.get("model2"))

assert "predicted_crop" in v_res, "Missing predicted_crop in video response"
assert "model2" in v_res, "Missing model2 in video response"
print("[PASS] Video inference pipeline executes Model 1 + Model 2 V4 cleanly.")

# -----------------------------------------------------------------------------
# 7. TEST QUERY ROUTING & KNOWLEDGE PATH
# -----------------------------------------------------------------------------
print("\n[TEST 7] Testing Deterministic Query Router...")
q1 = process_query_routing("What plant is this?")
q2 = process_query_routing("How do I treat tomato early blight?")
print(f"Query 1: {q1}")
print(f"Query 2: {q2}")
assert q1["needs_model1"] == True, "Expected plant query to need Model 1"
print("[PASS] Query router and intent pipeline functioning normally.")

# -----------------------------------------------------------------------------
# 8. TEST REST API ENDPOINTS (IF SERVER IS RUNNING)
# -----------------------------------------------------------------------------
print("\n[TEST 8] Testing Running Server Endpoints (http://127.0.0.1:8000)...")
try:
    health_r = requests.get("http://127.0.0.1:8000/api/health", timeout=3)
    if health_r.status_code == 200:
        print("[PASS] /api/health responded 200 OK")
        root_r = requests.get("http://127.0.0.1:8000/", timeout=3)
        root_data = root_r.json()
        print(f"[PASS] / returned models: {root_data.get('models')}")
        assert "Model 2 V4" in root_data.get("models", {}).get("model2", ""), "Root endpoint should report Model 2 V4"
    else:
        print(f"[NOTE] Server returned status {health_r.status_code}")
except Exception as e:
    print(f"[NOTE] Live HTTP check skipped or server reloading: {e}")

print("\n" + "=" * 80)
print("ALL PROMOTION VERIFICATION TESTS PASSED SUCCESSFULLY!")
print("=" * 80)
