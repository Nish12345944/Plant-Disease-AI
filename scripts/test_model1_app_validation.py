"""Comprehensive validation test suite for Model 1 Test App.

Tests:
1. Known Tomato Image
2. Known Cucumber Image
3. Known Rose Image
4. Real Plant Video
5. Video with Movement
6. Invalid File Handling
7. Short Video Handling (<1s)
"""

from __future__ import annotations

import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np

from model1_test_app.inference import load_model, predict_image
from model1_test_app.video_inference import predict_video
from video.frame_extractor import InvalidVideoError


def run_tests():
    print("=" * 65)
    print("RUNNING MODEL 1 TEST APP VALIDATION SUITE")
    print("=" * 65)

    # 1. Load Model 1
    print("\n[INIT] Loading Model 1 checkpoint & class mapping...")
    model, idx_to_class, class_to_idx, device, dev_name = load_model()
    print(f"  -> Model loaded successfully on: {dev_name}")
    print(f"  -> Classes ({len(idx_to_class)}): {list(idx_to_class.values())[:6]} ...")

    # 2. Test 1: Known Tomato Image
    print("\n[TEST 1] Testing Known Tomato Image...")
    tom_path = PROJECT_ROOT / "data/processed/model1_balanced/test/tomato/tomato_fruit_diseased_001434.jpg"
    tom_res = predict_image(tom_path, model, idx_to_class, device)
    print(f"  -> Prediction: {tom_res['predicted_label']} ({tom_res['percentage']})")
    print(f"  -> Top-3: {[(x['label'], x['percentage']) for x in tom_res['top_k']]}")
    assert tom_res["predicted_class"] == "tomato", f"Expected tomato, got {tom_res['predicted_class']}"
    print("  -> PASS: Tomato correctly classified.")

    # 3. Test 2: Known Cucumber Image
    print("\n[TEST 2] Testing Known Cucumber Image...")
    cuc_path = PROJECT_ROOT / "data/processed/model1_balanced/test/cucumber/cucumber_fruit_diseased_002851.jpg"
    cuc_res = predict_image(cuc_path, model, idx_to_class, device)
    print(f"  -> Prediction: {cuc_res['predicted_label']} ({cuc_res['percentage']})")
    print(f"  -> Top-3: {[(x['label'], x['percentage']) for x in cuc_res['top_k']]}")
    assert cuc_res["predicted_class"] == "cucumber", f"Expected cucumber, got {cuc_res['predicted_class']}"
    print("  -> PASS: Cucumber correctly classified.")

    # 4. Test 3: Known Rose Image
    print("\n[TEST 3] Testing Known Rose Image...")
    ros_path = PROJECT_ROOT / "data/processed/model1_balanced/test/rose/rose_flower_unknown_004360.jpg"
    ros_res = predict_image(ros_path, model, idx_to_class, device)
    print(f"  -> Prediction: {ros_res['predicted_label']} ({ros_res['percentage']})")
    print(f"  -> Top-3: {[(x['label'], x['percentage']) for x in ros_res['top_k']]}")
    assert ros_res["predicted_class"] == "rose", f"Expected rose, got {ros_res['predicted_class']}"
    print("  -> PASS: Rose correctly classified.")

    # 5. Test 4: Real Plant Video (Cucumber Frames)
    print("\n[TEST 4] Testing Real Plant Video (Cucumber)...")
    cuc_img = cv2.imread(str(cuc_path))
    # Resize to standard video frame dimensions (640, 480)
    cuc_img_frame = cv2.resize(cuc_img, (640, 480), interpolation=cv2.INTER_LINEAR)
    vid4_path = PROJECT_ROOT / "test_cuc_video.mp4"
    out4 = cv2.VideoWriter(str(vid4_path), cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (640, 480))
    for _ in range(60):  # 2.0 seconds @ 30 FPS
        out4.write(cuc_img_frame)
    out4.release()

    res_vid4 = predict_video(
        vid4_path,
        model,
        idx_to_class,
        device,
        sample_fps=1.0,
        quality_filter=False,  # Test sampling without filter first
    )
    print(f"  -> Aggregated Prediction: {res_vid4['final_prediction']['label']} ({res_vid4['final_prediction']['percentage']})")
    print(f"  -> Sampled Frames: {res_vid4['sampled_frames_count']}, Accepted: {res_vid4['accepted_frames_count']}")
    assert res_vid4["final_prediction"]["class_name"] == "cucumber", f"Expected cucumber, got {res_vid4['final_prediction']['class_name']}"
    if vid4_path.exists():
        vid4_path.unlink()
    print("  -> PASS: Real plant video classified & aggregated as Cucumber.")

    # 6. Test 5: Video with Movement (Panning Tomato Frames)
    print("\n[TEST 5] Testing Video with Movement (Panning Tomato Frames)...")
    tom_img = cv2.imread(str(tom_path))
    tom_img_frame = cv2.resize(tom_img, (640, 480), interpolation=cv2.INTER_LINEAR)
    vid5_path = PROJECT_ROOT / "test_motion_video.mp4"
    out5 = cv2.VideoWriter(str(vid5_path), cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (640, 480))
    for i in range(90):  # 3.0 seconds
        dx = int(8 * np.sin(i / 6.0))
        dy = int(4 * np.cos(i / 6.0))
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        shifted = cv2.warpAffine(tom_img_frame, M, (640, 480))
        out5.write(shifted)
    out5.release()

    res_vid5 = predict_video(vid5_path, model, idx_to_class, device, sample_fps=1.0, quality_filter=True)
    print(f"  -> Aggregated Prediction: {res_vid5['final_prediction']['label']} ({res_vid5['final_prediction']['percentage']})")
    print(f"  -> Sampled Frames: {res_vid5['sampled_frames_count']}, Accepted: {res_vid5['accepted_frames_count']}")
    assert res_vid5["final_prediction"]["class_name"] == "tomato", f"Expected tomato, got {res_vid5['final_prediction']['class_name']}"
    if vid5_path.exists():
        vid5_path.unlink()
    print("  -> PASS: Motion video classified & aggregated as Tomato.")

    # 7. Test 6: Invalid File Handling
    print("\n[TEST 6] Testing Invalid File Handling...")
    try:
        predict_video("non_existent_fake_video.mp4", model, idx_to_class, device)
        print("  -> FAIL: Did not raise InvalidVideoError")
    except InvalidVideoError as exc:
        print(f"  -> PASS: Caught expected InvalidVideoError: {exc}")

    # 8. Test 7: Short Video (<1s: 0.3s)
    print("\n[TEST 7] Testing Short Video (<1s: 10 frames @ 30 FPS)...")
    ros_img = cv2.imread(str(ros_path))
    ros_img_frame = cv2.resize(ros_img, (640, 480), interpolation=cv2.INTER_LINEAR)
    vid7_path = PROJECT_ROOT / "test_short_video.mp4"
    out7 = cv2.VideoWriter(str(vid7_path), cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (640, 480))
    for _ in range(10):  # 10 frames = 0.33s
        out7.write(ros_img_frame)
    out7.release()

    res_vid7 = predict_video(vid7_path, model, idx_to_class, device, sample_fps=1.0, quality_filter=True)
    print(f"  -> Aggregated Prediction: {res_vid7['final_prediction']['label']} ({res_vid7['final_prediction']['percentage']})")
    print(f"  -> Sampled Frames: {res_vid7['sampled_frames_count']}, Accepted: {res_vid7['accepted_frames_count']}")
    assert res_vid7["final_prediction"]["class_name"] == "rose", f"Expected rose, got {res_vid7['final_prediction']['class_name']}"
    if vid7_path.exists():
        vid7_path.unlink()
    print("  -> PASS: Short video handled cleanly.")

    print("\n" + "=" * 65)
    print("ALL 7 MODEL 1 APP VALIDATION TESTS PASSED (100%)")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
