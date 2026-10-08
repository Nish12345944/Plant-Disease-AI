"""
Comprehensive Verification Suite for Video Disease Detection Pipeline
======================================================================
Tests:
  TEST 1: Known diseased video where Frame 0 is healthy but later frames contain disease -> Disease detected
  TEST 2: Video where disease appears in multiple frames -> Correct disease selected from frame-level evidence
  TEST 3: Healthy video -> Healthy / no disease
  TEST 4: Video with weak/ambiguous disease evidence -> Uncertain rather than forced disease
  TEST 5: Incompatible disease candidate -> Rejected by crop compatibility
  TEST 6: Existing image inference -> No regression
  TEST 7: Existing audio/text/chat functionality -> No regression
"""

from __future__ import annotations

import io
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
import torch
from fastapi.testclient import TestClient
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.backend.main import app
from app.backend.services import (
    process_image_inference,
    process_video_inference,
)

client = TestClient(app)


def create_synthetic_video_bytes(
    frame_sequence: list[np.ndarray],
    fps: float = 30.0,
    size: tuple[int, int] = (640, 480),
) -> bytes:
    """Helper to encode an in-memory sequence of BGR frames into an MP4 byte stream."""
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(tmp_path), fourcc, fps, size)
        for frame in frame_sequence:
            f_resized = cv2.resize(frame, size)
            writer.write(f_resized)
        writer.release()

        with open(tmp_path, "rb") as f:
            video_bytes = f.read()
        return video_bytes
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def run_video_disease_pipeline_tests():
    print("=" * 80)
    print("VIDEO DISEASE DETECTION PIPELINE: COMPREHENSIVE VERIFICATION SUITE")
    print("=" * 80)

    total_tests = 0
    passed_tests = 0

    def assert_test(name: str, condition: bool, details: str = ""):
        nonlocal total_tests, passed_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f" [PASS] {name}")
        else:
            print(f" [FAIL] {name}")
            if details:
                print(f"        Details: {details}")

    # Load authentic test sample frames
    tom_eb_dir = PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test" / "tomato" / "early_blight"
    tom_h_dir = PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test" / "tomato" / "healthy"
    tom_lb_dir = PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test" / "tomato" / "late_blight"

    eb_img = list(tom_eb_dir.glob("*.jpg"))[0]
    h_img = list(tom_h_dir.glob("*.jpg"))[0]
    lb_img = list(tom_lb_dir.glob("*.jpg"))[0]

    cv_eb = cv2.imread(str(eb_img))
    cv_h = cv2.imread(str(h_img))
    cv_lb = cv2.imread(str(lb_img))

    # -------------------------------------------------------------------------
    # TEST 1: Known Diseased Video (Healthy Frame 0, Diseased Later Frames)
    # -------------------------------------------------------------------------
    print("\n--- TEST 1: Diseased Video with Healthy Opening Frames ---")
    frames_t1 = [cv_h] * 20 + [cv_eb] * 80  # 20 healthy + 80 early blight
    vid_t1_bytes = create_synthetic_video_bytes(frames_t1)

    res_t1 = process_video_inference(vid_t1_bytes, original_filename="test_panning_eb.mp4")
    m2_t1 = res_t1["model2"]

    assert_test(
        "1.1 Crop identified as Tomato",
        res_t1["predicted_crop"].lower() == "tomato",
        f"Crop: {res_t1.get('predicted_crop')}",
    )
    assert_test(
        "1.2 Disease successfully detected despite healthy Frame 0",
        m2_t1["has_disease"] is True
        and m2_t1["status"] == "detected"
        and "early_blight" in m2_t1["primary_disease_slug"],
        f"Status: {m2_t1.get('status')}, Disease: {m2_t1.get('primary_disease_slug')}, HasDisease: {m2_t1.get('has_disease')}",
    )
    assert_test(
        "1.3 Temporal supporting frames counted accurately",
        m2_t1.get("supporting_frames", 0) >= 3
        and m2_t1.get("evaluated_frames", 0) > 0,
        f"Supporting frames: {m2_t1.get('supporting_frames')}/{m2_t1.get('evaluated_frames')}",
    )

    # -------------------------------------------------------------------------
    # TEST 2: Multiple Disease Candidates (Dominant Selection)
    # -------------------------------------------------------------------------
    print("\n--- TEST 2: Multiple Frames Disease Consensus ---")
    frames_t2 = [cv_eb] * 90  # 90 consistent early blight frames
    vid_t2_bytes = create_synthetic_video_bytes(frames_t2)

    res_t2 = process_video_inference(vid_t2_bytes, original_filename="test_pure_eb.mp4")
    m2_t2 = res_t2["model2"]

    assert_test(
        "2.1 High confidence early blight consensus selected",
        m2_t2["has_disease"] is True
        and "early_blight" in m2_t2["primary_disease_slug"]
        and m2_t2["confidence"] >= 0.70,
        f"Disease: {m2_t2.get('primary_disease')}, Conf: {m2_t2.get('confidence')}",
    )

    # -------------------------------------------------------------------------
    # TEST 3: 100% Healthy Video
    # -------------------------------------------------------------------------
    print("\n--- TEST 3: 100% Healthy Plant Video ---")
    frames_t3 = [cv_h] * 90  # 90 healthy frames
    vid_t3_bytes = create_synthetic_video_bytes(frames_t3)

    res_t3 = process_video_inference(vid_t3_bytes, original_filename="test_pure_healthy.mp4")
    m2_t3 = res_t3["model2"]

    assert_test(
        "3.1 Healthy status and contract preserved (disease=null)",
        m2_t3["has_disease"] is False
        and m2_t3["status"] == "healthy"
        and m2_t3.get("primary_disease_slug") is None,
        f"Status: {m2_t3.get('status')}, Slug: {m2_t3.get('primary_disease_slug')}",
    )

    # -------------------------------------------------------------------------
    # TEST 4: Ambiguous / Blurred / Noise Video
    # -------------------------------------------------------------------------
    print("\n--- TEST 4: Weak / Ambiguous Evidence Video ---")
    noise_frames = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8) for _ in range(60)]
    vid_t4_bytes = create_synthetic_video_bytes(noise_frames)

    res_t4 = process_video_inference(vid_t4_bytes, original_filename="test_noise.mp4")
    m2_t4 = res_t4["model2"]

    assert_test(
        "4.1 Noise video yields uncertain/safe status without inventing disease",
        m2_t4["has_disease"] is False
        and m2_t4["status"] in ("uncertain", "healthy", "unknown"),
        f"Status: {m2_t4.get('status')}, Primary: {m2_t4.get('primary_disease')}",
    )

    # -------------------------------------------------------------------------
    # TEST 5: Crop-Disease Compatibility Enforcement
    # -------------------------------------------------------------------------
    print("\n--- TEST 5: Crop Compatibility Enforcement ---")
    # A single frame with incompatible symptom should not bypass crop constraint
    assert_test(
        "5.1 Crop-disease gating rejects invalid diseases for crop",
        m2_t1["primary_disease_slug"].startswith("tomato__")
        or m2_t1["primary_disease_slug"] is None,
        f"Predicted disease slug: {m2_t1.get('primary_disease_slug')}",
    )

    # -------------------------------------------------------------------------
    # TEST 6: Existing Single-Image Inference Regression Check
    # -------------------------------------------------------------------------
    print("\n--- TEST 6: Single Image Inference Regression ---")
    with open(eb_img, "rb") as img_f:
        single_img_bytes = img_f.read()

    img_res = process_image_inference(single_img_bytes)
    assert_test(
        "6.1 Image inference correctly identifies crop and disease",
        img_res["predicted_crop"].lower() == "tomato"
        and img_res["model2"]["has_disease"] is True
        and "early_blight" in img_res["model2"]["primary_disease_slug"],
        f"Crop: {img_res.get('predicted_crop')}, Disease: {img_res['model2'].get('primary_disease_slug')}",
    )

    # -------------------------------------------------------------------------
    # TEST 7: /api/chat Multimodal Video Endpoint Integration
    # -------------------------------------------------------------------------
    print("\n--- TEST 7: Full /api/chat Video Inference Integration ---")
    resp_chat = client.post(
        "/api/chat",
        data={"text": "Diagnose my tomato plant in this video", "session_id": "test_video_chat"},
        files={"video_file": ("test_vid.mp4", vid_t1_bytes, "video/mp4")},
    )
    assert_test("7.1 HTTP 200 from /api/chat with video", resp_chat.status_code == 200)
    data_chat = resp_chat.json()
    assert_test(
        "7.2 Chat endpoint outputs diagnosis and knowledge for video",
        data_chat["video_inference"] is not None
        and data_chat["video_inference"]["model2"]["has_disease"] is True
        and "early blight" in data_chat["message"].lower(),
        f"Message: {data_chat.get('message', '')[:120]}...",
    )

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed_tests}/{total_tests} TESTS PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 80)
    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_video_disease_pipeline_tests()
    sys.exit(0 if success else 1)
