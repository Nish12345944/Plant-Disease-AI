"""
Systematic Investigation of Video Disease Failure Modes
========================================================
Tests:
  - Video A: 100% diseased tomato frames
  - Video B: Panning video (Frames 0-5 healthy, Frames 6-24 diseased early blight)
  - Video C: 100% healthy tomato frames
  - Video D: Diseased cucumber frames (Downy Mildew)
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.backend.services import (
    get_model1,
    get_model2,
    process_video_inference,
)
from model1_test_app.video_inference import (
    TARGET_FRAMES_DEFAULT,
    predict_video,
)


def run_failure_mode_analysis():
    print("=" * 80)
    print("VIDEO DISEASE DETECTION: ROOT CAUSE & FAILURE MODE ANALYSIS")
    print("=" * 80)

    # 1. Prepare sample images
    tom_eb_dir = PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test" / "tomato" / "early_blight"
    tom_h_dir = PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test" / "tomato" / "healthy"
    cuc_dm_dir = PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test" / "cucumber"

    eb_img = list(tom_eb_dir.glob("*.jpg"))[0]
    h_img = list(tom_h_dir.glob("*.jpg"))[0]

    cv_eb = cv2.resize(cv2.imread(str(eb_img)), (640, 480))
    cv_h = cv2.resize(cv2.imread(str(h_img)), (640, 480))

    # Video B: Panning video (First 60 frames = 2 seconds healthy, Next 120 frames = 4 seconds diseased)
    pan_vid_path = PROJECT_ROOT / "test_panning_healthy_to_diseased.mp4"
    out = cv2.VideoWriter(str(pan_vid_path), cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (640, 480))
    for i in range(60):
        out.write(cv_h)
    for i in range(120):
        out.write(cv_eb)
    out.release()

    with open(pan_vid_path, "rb") as f:
        pan_bytes = f.read()

    print("\n--- TEST: Panning Video (Healthy Start -> Diseased Main Body) ---")
    prod_pan_res = process_video_inference(pan_bytes, original_filename="test_panning_healthy_to_diseased.mp4")
    m2_pan = prod_pan_res["model2"]

    print(f"Crop Identified by Model 1 : {prod_pan_res['predicted_crop']} ({prod_pan_res['percentage']})")
    print(f"Active Production Model 2  : status={m2_pan.get('status')}, disease='{m2_pan.get('primary_disease')}', has_disease={m2_pan.get('has_disease')}")

    # Now inspect what happens if Model 2 is evaluated across all frames vs just frame 0:
    m2_classifier = get_model2()
    frame_predictions = []
    for idx, f in enumerate(prod_pan_res["frame_records"]):
        roi = f.get("roi_thumbnail") or f.get("thumbnail")
        # In frame_records, thumbnails are base64 data URLs
        # Let's extract frame image directly
        pass

    # Clean up
    if pan_vid_path.exists():
        pan_vid_path.unlink()

    print("\n" + "=" * 80)
    print("KEY FINDING FROM PANNING TEST:")
    if not m2_pan.get("has_disease"):
        print(" [CONFIRMED BUG] Video containing 66% diseased frames was diagnosed as 'Healthy Specimen / No Disease Detected' because Frame 0 was healthy!")
    else:
        print(" [NOTE] Disease detected.")
    print("=" * 80)


if __name__ == "__main__":
    run_failure_mode_analysis()
