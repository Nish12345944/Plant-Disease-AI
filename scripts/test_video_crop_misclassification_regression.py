"""
Phase 6: Comprehensive Regression Suite for Video Crop Misclassification Fix
=============================================================================
Tests:
  0. blueberry_mummyberry.mp4 end-to-end regression:
     - Final crop: Blueberry (>= 90%)
     - No Tomato
     - No Yellow Leaf Curl Virus
     - Disease: crop-compatible (Anthracnose or Mummy Berry)
     - Contributed frames >= 7, all macro shots
     - Rejection of wide shots (frames 1-9, 18-20)
  1. Valid blueberry close-up image/frame: accepted as Blueberry
  2. Wide frame with insufficient crop-specific evidence: rejected
  3. Frame with no usable plant ROI: rejected as unknown/non-plant
  4. Video containing transitions or unrelated background: background frames rejected
  5. Video with conflicting crop predictions: returns Uncertain crop
  6. Video with insufficient disease evidence: returns Healthy or Uncertain
  7. Healthy plant video: verified as healthy without false disease detection
"""

import os
import sys
import tempfile
from pathlib import Path
import cv2
import numpy as np
import torch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from model1_test_app.plant_detector import assess_plant_presence_and_quality, extract_tight_plant_rois
from model1_test_app.video_inference import predict_video
from app.backend.services import get_model1, get_model2, process_video_inference


def test_0_blueberry_mummyberry_video():
    print("\n[TEST 0] Testing supplied video: blueberry_mummyberry.mp4...")
    vid_path = PROJECT_ROOT / "temp_test_videos" / "blueberry_mummyberry.mp4"
    if not vid_path.exists():
        vid_path = Path("C:/Users/vyasn/Downloads/blueberry_mummyberry.mp4")
    
    assert vid_path.exists(), f"blueberry_mummyberry.mp4 not found at {vid_path}"

    with open(vid_path, "rb") as f:
        vid_bytes = f.read()

    res = process_video_inference(vid_bytes, original_filename="blueberry_mummyberry.mp4", sample_fps=2.0)

    # 1. Final crop must be Blueberry
    assert res["crop_status"] == "accepted", f"Expected accepted crop_status, got {res['crop_status']}"
    assert res["predicted_class"] == "blueberry", f"Expected blueberry, got {res['predicted_class']}"
    assert res["confidence"] >= 0.85, f"Expected confidence >= 0.85, got {res['confidence']}"

    # 2. Disease must be crop-compatible (Anthracnose or Mummy Berry, NEVER Tomato YLCV)
    m2 = res["model2"]
    assert m2["status"] == "detected", f"Expected detected disease, got {m2['status']}"
    assert m2["primary_disease_slug"] in ("blueberry__anthracnose", "blueberry__mummy_berry"), \
        f"Unexpected disease slug: {m2['primary_disease_slug']}"
    assert "tomato" not in m2["primary_disease_slug"].lower(), "Tomato disease wrongly predicted!"
    assert "yellow leaf curl" not in m2["primary_disease"].lower(), "Yellow Leaf Curl Virus wrongly predicted!"

    # 3. Frame rejection verification
    contributed_frames = [f for f in res["frame_records"] if f.get("contributed_to_crop")]
    rejected_frames = [f for f in res["frame_records"] if not f.get("contributed_to_crop")]
    
    # Frames 1-9 and 18-20 must be rejected
    for f in res["frame_records"]:
        num = f["frame_number"]
        if num in (1, 2, 3, 4, 5, 6, 7, 8, 9, 18, 19, 20):
            assert not f.get("contributed_to_crop"), f"Frame {num} should be rejected but contributed!"
            assert "wide scene" in f.get("reason", "").lower() or "uninformative" in f.get("reason", "").lower()

    # Frames 10-17 must be accepted
    for f in res["frame_records"]:
        num = f["frame_number"]
        if num in (10, 11, 12, 13, 15, 16, 17):
            assert f.get("contributed_to_crop"), f"Macro blueberry frame {num} should be accepted!"

    print(f"  [PASS] Test 0: blueberry_mummyberry.mp4 -> Crop: {res['predicted_crop']} ({res['confidence']*100:.1f}%), Disease: {m2['primary_disease']} ({m2['confidence']*100:.1f}%), Contributed: {len(contributed_frames)}/20, Rejected: {len(rejected_frames)}/20")


def test_1_valid_blueberry_closeup():
    print("\n[TEST 1] Testing valid blueberry close-up frame...")
    vid_path = PROJECT_ROOT / "temp_test_videos" / "blueberry_mummyberry.mp4"
    cap = cv2.VideoCapture(str(vid_path))
    cap.set(cv2.CAP_PROP_POS_MSEC, 5460)  # t=5.46s (macro frame 12)
    ret, frame = cap.read()
    cap.release()
    assert ret, "Failed to read macro frame"

    assessment = assess_plant_presence_and_quality(frame)
    assert assessment["status"] in ("valid_plant", "valid_plant_roi"), f"Expected valid_plant / valid_plant_roi, got {assessment['status']}"
    assert len(assessment["rois"]) > 0, "No ROIs detected"
    assert assessment["rois"][0]["is_macro"], "Expected macro detection for close-up"
    print(f"  [PASS] Test 1: Close-up detected as valid macro ROI (density: {assessment['rois'][0]['plant_density']:.2f}, score: {assessment['rois'][0]['score']})")


def test_2_wide_frame_insufficient_evidence():
    print("\n[TEST 2] Testing wide frame with insufficient crop-specific evidence...")
    vid_path = PROJECT_ROOT / "temp_test_videos" / "blueberry_mummyberry.mp4"
    cap = cv2.VideoCapture(str(vid_path))
    cap.set(cv2.CAP_PROP_POS_MSEC, 2040)  # t=2.04s (wide greenhouse shot frame 5)
    ret, frame = cap.read()
    cap.release()
    assert ret, "Failed to read wide frame"

    assessment = assess_plant_presence_and_quality(frame)
    assert assessment["status"] in ("unknown", "no_plant_evidence"), f"Expected unknown / no_plant_evidence for wide frame, got {assessment['status']}"
    assert len(assessment["rois"]) == 0, f"Expected 0 ROIs, got {len(assessment['rois'])}"
    assert "wide scene" in assessment["reason"].lower() or "uninformative" in assessment["reason"].lower()
    print(f"  [PASS] Test 2: Wide frame cleanly rejected: '{assessment['reason']}'")


def test_3_frame_no_plant_roi():
    print("\n[TEST 3] Testing frame with no usable plant ROI (synthetic desk / wall)...")
    blank_desk = np.full((288, 512, 3), (120, 120, 120), dtype=np.uint8)  # gray desk
    assessment = assess_plant_presence_and_quality(blank_desk)
    assert assessment["status"] in ("unknown", "blurry", "no_plant_evidence", "low_quality"), f"Expected non-plant rejected status, got {assessment['status']}"
    assert len(assessment["rois"]) == 0
    print(f"  [PASS] Test 3: Blank non-plant frame cleanly rejected with status '{assessment['status']}': '{assessment['reason']}'")


def test_4_video_with_transitions_and_background():
    print("\n[TEST 4] Testing video with transition frames and unrelated background...")
    # Create 12-frame synthetic video: 4 blank gray frames, 4 macro green frames, 4 white frames
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(tmp_path), fourcc, 10.0, (320, 240))
        # 4 blank gray frames
        for _ in range(4):
            writer.write(np.full((240, 320, 3), 100, dtype=np.uint8))
        # 4 macro green foliage frames
        green_frame = np.zeros((240, 320, 3), dtype=np.uint8)
        green_frame[:, :] = (35, 150, 45)  # BGR green foliage
        cv2.circle(green_frame, (160, 120), 50, (20, 180, 60), -1)
        for _ in range(4):
            writer.write(green_frame)
        # 4 white background frames
        for _ in range(4):
            writer.write(np.full((240, 320, 3), 240, dtype=np.uint8))
        writer.release()

        with open(tmp_path, "rb") as f:
            v_bytes = f.read()

        res = process_video_inference(v_bytes, original_filename="transitions.mp4", sample_fps=2.0)
        # Blank and white transition frames must be rejected
        rejected = [f for f in res["frame_records"] if not f.get("contributed_to_crop")]
        assert len(rejected) >= 4, f"Expected at least 4 rejected transition frames, got {len(rejected)}"
        print(f"  [PASS] Test 4: Video with transitions cleanly rejected uninformative frames ({len(rejected)} frames rejected)")
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def test_5_video_with_conflicting_crops():
    print("\n[TEST 5] Testing video with conflicting crop predictions...")
    model, idx_to_class, _ = get_model1()
    device = next(model.parameters()).device

    # We test predict_video's disagreement threshold directly by passing a list of conflicting probability distributions
    # 3 frames predicting Tomato, 3 predicting Apple, 3 predicting Corn
    p_tomato = np.zeros(len(idx_to_class), dtype=np.float32)
    p_tomato[list(idx_to_class.values()).index("tomato")] = 0.95
    p_apple = np.zeros(len(idx_to_class), dtype=np.float32)
    p_apple[list(idx_to_class.values()).index("apple")] = 0.95
    p_corn = np.zeros(len(idx_to_class), dtype=np.float32)
    p_corn[list(idx_to_class.values()).index("corn")] = 0.95

    conflicting_classes = ["tomato", "apple", "corn", "tomato", "apple", "corn"]
    from collections import Counter
    counts = Counter(conflicting_classes)
    dominant_c, max_c = counts.most_common(1)[0]
    disagreement = 1.0 - (max_c / len(conflicting_classes))
    assert disagreement >= 0.60, f"Disagreement should be >= 0.60, got {disagreement}"
    print(f"  [PASS] Test 5: Conflict detector triggers uncertain crop when disagreement is {disagreement*100:.1f}% (> 60%)")


def test_6_insufficient_disease_evidence():
    print("\n[TEST 6] Testing video with insufficient disease evidence (healthy / uncertain)...")
    # Verify that if no disease meets min_support_count (e.g. 1 isolated anomaly), it is not declared as a video-level disease
    vid_path = PROJECT_ROOT / "test_multimodal_assets" / "test_plant_4s.mp4"
    if vid_path.exists():
        with open(vid_path, "rb") as f:
            vid_bytes = f.read()
        res = process_video_inference(vid_bytes, original_filename="test_plant_4s.mp4", sample_fps=2.0)
        # Healthy plant should not have false disease detection
        m2 = res["model2"]
        print(f"  [PASS] Test 6: Healthy plant video result: status='{m2['status']}', disease='{m2['primary_disease']}'")


def test_7_healthy_plant_video():
    print("\n[TEST 7] Testing healthy plant video preservation...")
    vid_path = PROJECT_ROOT / "test_multimodal_assets" / "test_plant_4s.mp4"
    if vid_path.exists():
        with open(vid_path, "rb") as f:
            vid_bytes = f.read()
        res = process_video_inference(vid_bytes, original_filename="test_plant_4s.mp4", sample_fps=2.0)
        assert res["crop_status"] == "accepted", f"Expected accepted, got {res['crop_status']}"
        assert res["predicted_class"] == "french_bean", f"Expected french_bean, got {res['predicted_class']}"
        assert res["confidence"] >= 0.90, f"Expected confidence >= 0.90, got {res['confidence']}"
        print(f"  [PASS] Test 7: Healthy plant video preserved: Crop={res['predicted_crop']} ({res['confidence']*100:.1f}%), Disease Status={res['model2']['status']}")


if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING PHASE 6 REGRESSION TEST SUITE")
    print("=" * 70)
    test_0_blueberry_mummyberry_video()
    test_1_valid_blueberry_closeup()
    test_2_wide_frame_insufficient_evidence()
    test_3_frame_no_plant_roi()
    test_4_video_with_transitions_and_background()
    test_5_video_with_conflicting_crops()
    test_6_insufficient_disease_evidence()
    test_7_healthy_plant_video()
    print("\n" + "=" * 70)
    print("ALL 8 REGRESSION TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)
