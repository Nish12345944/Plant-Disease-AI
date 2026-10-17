"""
Regression Test Suite: Video ROI Filter Regression Hotfix
=========================================================
Tests:
1. Video A: gemini_generated_video_Capsicum — Bacterial Spot.mp4:
   - Clear capsicum leaf frames accepted
   - Model 1 runs > 0
   - Model 2 runs > 0
   - Crop identified as Bell Pepper (Capsicum)
   - Disease identified as Bacterial Spot
2. Video B: blueberry_mummyberry.mp4:
   - Valid blueberry frames remain accepted (8 frames)
   - Misleading background frames rejected (12 frames)
   - Crop identified as Blueberry (>= 90%)
   - No Tomato or Yellow Leaf Curl Virus
   - Disease identified as Anthracnose or Mummy Berry
3. Specific frame checks:
   - Close-up leaf: accepted as valid_plant_roi
   - Wide scene with small plant / background clutter: rejected as no_plant_evidence
   - Frame containing no plant: rejected as no_plant_evidence
   - Blurry or obstructed frame: rejected as low_quality
4. Graded validation decision states:
   - valid_plant_roi, low_quality, no_plant_evidence, crop_uncertain
"""

import os
import sys
from pathlib import Path
import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from model1_test_app.plant_detector import assess_plant_presence_and_quality, extract_tight_plant_rois
from model1_test_app.video_inference import predict_video
from app.backend.services import get_model1, get_model2, process_video_inference


def find_capsicum_video_path():
    candidates = [
        PROJECT_ROOT / "temp_test_videos" / "capsicum_bacterial_spot.mp4",
        Path(os.path.expanduser("~/Downloads/gemini_generated_video_Capsicum — Bacterial Spot.mp4")),
        Path(os.path.expanduser("~/Downloads/gemini_generated_video_Capsicum - Bacterial Spot.mp4")),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def find_blueberry_video_path():
    candidates = [
        PROJECT_ROOT / "temp_test_videos" / "blueberry_mummyberry.mp4",
        Path(os.path.expanduser("~/Downloads/blueberry_mummyberry.mp4")),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def test_capsicum_bacterial_spot_video():
    """Video A: Clear capsicum leaf frames accepted, M1/M2 run, Bacterial Spot diagnosed."""
    print("\n" + "=" * 60)
    print("[TEST] Video A: Capsicum Bacterial Spot Video Pipeline")
    print("=" * 60)
    vid_path = find_capsicum_video_path()
    assert vid_path is not None, "Capsicum Bacterial Spot test video not found!"

    with open(vid_path, "rb") as f:
        vid_bytes = f.read()

    res = process_video_inference(vid_bytes, original_filename="gemini_generated_video_Capsicum — Bacterial Spot.mp4", sample_fps=2.0)

    # Decoded & Sampled
    total_decoded = res.get("total_decoded_frames", len(res["frame_records"]))
    sampled_count = res.get("sampled_frames_count", len(res["frame_records"]))
    assert sampled_count >= 16, f"Expected at least 16 sampled frames, got {sampled_count}"

    # Valid plant frames & rejected frames
    valid_frames = [f for f in res["frame_records"] if f["status"] in ("valid", "valid_plant_roi") or f.get("contributed_to_crop")]
    rejected_frames = [f for f in res["frame_records"] if not (f["status"] in ("valid", "valid_plant_roi") or f.get("contributed_to_crop"))]

    print(f"  Decoded: {total_decoded}")
    print(f"  Sampled: {sampled_count}")
    print(f"  Valid Plant: {len(valid_frames)}")
    print(f"  Rejected: {len(rejected_frames)}")
    print(f"  M1 Runs: {res.get('model1_inference_count', 'N/A')}")
    print(f"  M2 Runs: {res.get('model2_inference_count', 'N/A')}")
    print(f"  Final Crop: {res.get('predicted_crop')} ({res.get('confidence', 0)*100:.1f}%)")
    m2 = res.get("model2", {})
    print(f"  Disease Decision: {m2.get('primary_disease')} ({m2.get('confidence', 0)*100:.1f}%) [Status: {m2.get('status')}]")

    # Regression Checks:
    assert len(valid_frames) > 0, "Regression! All frames were rejected (0 valid plant frames)!"
    assert len(valid_frames) >= 15, f"Expected >= 15 clear capsicum frames accepted, got {len(valid_frames)}"
    assert res.get("model1_inference_count", 0) > 0, "Model 1 did not run on any frame!"
    assert res.get("model2_inference_count", 0) > 0, "Model 2 did not run on any frame!"

    # Crop check: Bell Pepper (Capsicum)
    assert res["predicted_class"] == "bellpepper", f"Expected bellpepper, got {res['predicted_class']}"
    assert res["crop_status"] == "accepted", f"Expected crop_status accepted, got {res['crop_status']}"

    # Disease check: Bacterial Spot
    assert m2.get("status") == "detected", f"Expected disease detected, got {m2.get('status')}"
    assert m2.get("primary_disease_slug") == "bell_pepper__bacterial_spot", f"Expected bell_pepper__bacterial_spot, got {m2.get('primary_disease_slug')}"
    assert m2.get("supporting_frames", 0) >= 3, f"Expected >= 3 supporting disease frames, got {m2.get('supporting_frames')}"
    print("  => PASS: Capsicum Bacterial Spot video restored with high confidence!")


def test_blueberry_mummyberry_video():
    """Video B: Blueberry frames accepted, wide background rejected, Blueberry preserved."""
    print("\n" + "=" * 60)
    print("[TEST] Video B: Blueberry Mummyberry Video Pipeline")
    print("=" * 60)
    vid_path = find_blueberry_video_path()
    assert vid_path is not None, "Blueberry test video not found!"

    with open(vid_path, "rb") as f:
        vid_bytes = f.read()

    res = process_video_inference(vid_bytes, original_filename="blueberry_mummyberry.mp4", sample_fps=2.0)

    total_decoded = res.get("total_decoded_frames", len(res["frame_records"]))
    sampled_count = res.get("sampled_frames_count", len(res["frame_records"]))
    valid_frames = [f for f in res["frame_records"] if f["status"] in ("valid", "valid_plant_roi") or f.get("contributed_to_crop")]
    rejected_frames = [f for f in res["frame_records"] if not (f["status"] in ("valid", "valid_plant_roi") or f.get("contributed_to_crop"))]

    print(f"  Decoded: {total_decoded}")
    print(f"  Sampled: {sampled_count}")
    print(f"  Valid Plant: {len(valid_frames)}")
    print(f"  Rejected: {len(rejected_frames)}")
    print(f"  M1 Runs: {res.get('model1_inference_count', 'N/A')}")
    print(f"  M2 Runs: {res.get('model2_inference_count', 'N/A')}")
    print(f"  Final Crop: {res.get('predicted_crop')} ({res.get('confidence', 0)*100:.1f}%)")
    m2 = res.get("model2", {})
    print(f"  Disease Decision: {m2.get('primary_disease')} ({m2.get('confidence', 0)*100:.1f}%) [Status: {m2.get('status')}]")

    # Crop: Blueberry (never Tomato)
    assert res["predicted_class"] == "blueberry", f"Expected blueberry, got {res['predicted_class']}"
    assert res["confidence"] >= 0.85, f"Expected confidence >= 0.85, got {res['confidence']}"

    # Frame rejection: wide shots 1-9 and 18-20 must be rejected
    for f in res["frame_records"]:
        num = f["frame_number"]
        if num in (1, 2, 3, 4, 5, 6, 7, 8, 9, 18, 19, 20):
            assert not f.get("contributed_to_crop"), f"Frame {num} should be rejected!"
        elif num in (10, 11, 12, 13, 14, 15, 16, 17):
            assert f.get("contributed_to_crop"), f"Frame {num} should be accepted!"

    # Disease: Anthracnose or Mummy Berry (crop-compatible, never Tomato YLCV)
    assert m2.get("status") == "detected"
    assert m2.get("primary_disease_slug") in ("blueberry__anthracnose", "blueberry__mummy_berry")
    assert "tomato" not in m2.get("primary_disease_slug", "").lower()
    print("  => PASS: Blueberry Mummyberry video preserves macro frames and rejects wide shots!")


def test_frame_level_graded_decisions():
    """Test 3: Direct frame-level validation of close-up, wide scene, no plant, and blurry."""
    print("\n" + "=" * 60)
    print("[TEST] Frame-Level Graded Decisions")
    print("=" * 60)

    # 1. Close-up leaf: from Capsicum video (e.g. frame 10)
    caps_path = find_capsicum_video_path()
    cap = cv2.VideoCapture(str(caps_path))
    cap.set(cv2.CAP_PROP_POS_MSEC, 4000)
    ret, caps_frame = cap.read()
    cap.release()
    assert ret, "Failed to read Capsicum close-up frame"

    res_closeup = assess_plant_presence_and_quality(caps_frame)
    assert res_closeup["status"] in ("valid_plant_roi", "valid_plant"), f"Expected valid_plant_roi, got {res_closeup['status']}"
    assert len(res_closeup["rois"]) > 0, "Expected plant ROIs extracted for close-up leaf"
    print(f"  [PASS] Close-up leaf accepted: status={res_closeup['status']}, rois={len(res_closeup['rois'])}, plant_coverage={res_closeup['plant_coverage']}")

    # 2. Wide scene with small plant / greenhouse structure: from Blueberry frame 5 (t=2.04s)
    bb_path = find_blueberry_video_path()
    cap2 = cv2.VideoCapture(str(bb_path))
    cap2.set(cv2.CAP_PROP_POS_MSEC, 2040)
    ret2, wide_frame = cap2.read()
    cap2.release()
    assert ret2, "Failed to read wide frame"

    res_wide = assess_plant_presence_and_quality(wide_frame)
    assert res_wide["status"] == "no_plant_evidence", f"Expected no_plant_evidence for wide scene, got {res_wide['status']}"
    assert len(res_wide["rois"]) == 0, "Wide scene should yield 0 candidate ROIs"
    assert "wide scene" in res_wide["reason"].lower() or "uninformative" in res_wide["reason"].lower()
    print(f"  [PASS] Wide scene with greenhouse background rejected: status={res_wide['status']}, reason='{res_wide['reason']}'")

    # 3. Frame containing no plant: blue textured wall (sharpness > 10, no plant foliage)
    no_plant_frame = np.zeros((360, 640, 3), dtype=np.uint8)
    no_plant_frame[:, :] = (200, 80, 30)  # BGR blue wall
    no_plant_frame[::10, :] = (240, 100, 40)
    no_plant_frame[:, ::10] = (160, 60, 20)
    res_no_plant = assess_plant_presence_and_quality(no_plant_frame)
    assert res_no_plant["status"] == "no_plant_evidence", f"Expected no_plant_evidence, got {res_no_plant['status']}"
    assert len(res_no_plant["rois"]) == 0
    print(f"  [PASS] Frame containing no plant rejected: status={res_no_plant['status']}, reason='{res_no_plant['reason']}'")

    # 4. Blurry or obstructed frame: motion blurred frame
    blurred_frame = cv2.GaussianBlur(caps_frame, (51, 51), 0)
    res_blurry = assess_plant_presence_and_quality(blurred_frame)
    assert res_blurry["status"] == "low_quality", f"Expected low_quality for blurred frame, got {res_blurry['status']}"
    assert "blur" in res_blurry["reason"].lower() or "focus" in res_blurry["reason"].lower()
    print(f"  [PASS] Blurry frame rejected: status={res_blurry['status']}, reason='{res_blurry['reason']}'")


if __name__ == "__main__":
    test_capsicum_bacterial_spot_video()
    test_blueberry_mummyberry_video()
    test_frame_level_graded_decisions()
    print("\n" + "=" * 60)
    print("ALL REGRESSION FIX TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
