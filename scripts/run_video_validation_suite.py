"""Comprehensive validation test suite for the video processing module.

Tests all required edge cases:
1. Valid MP4
2. Valid video with different FPS (15 FPS, 30 FPS, 60 FPS)
3. Invalid/missing file
4. Unsupported extension
5. Very short video (<1s)
6. Empty/corrupt video files
7. Dark, overexposed, and blurry frame rejection
8. Temporary frame cleanup
9. Metadata extraction accuracy
10. 1 FPS sampling
11. 2 FPS sampling
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np

from video.frame_extractor import (
    EmptyVideoError,
    InvalidVideoError,
    VideoProcessingError,
    get_video_metadata,
    validate_video,
)
from video.processor import (
    FrameQualityFilter,
    QualityFilterConfig,
    cleanup_frames,
    compute_sample_indices,
    process_video,
)

SYNTHETIC_DIR = PROJECT_ROOT / "temp_test_videos"


def create_synthetic_leaf_frame(width: int = 640, height: int = 480, frame_num: int = 0) -> np.ndarray:
    """Generate a realistic high-contrast synthetic plant leaf image."""
    img = np.full((height, width, 3), (230, 240, 235), dtype=np.uint8)  # soft background

    # Draw stem
    cv2.line(img, (width // 2, height), (width // 2, height // 3), (35, 75, 25), 8)

    # Draw leaf contours
    center = (width // 2 + int(10 * np.sin(frame_num / 5.0)), height // 2)
    axes = (160, 90)
    angle = 35 + int(5 * np.cos(frame_num / 6.0))
    cv2.ellipse(img, center, axes, angle, 0, 360, (45, 140, 35), -1)
    cv2.ellipse(img, center, axes, angle, 0, 360, (20, 90, 15), 3)

    # Veins
    for offset in range(-60, 70, 25):
        pt1 = (center[0] + offset, center[1] - offset // 2)
        pt2 = (center[0] + offset + 30, center[1] + offset // 2)
        cv2.line(img, pt1, pt2, (60, 175, 45), 2)

    # Texture and text label
    cv2.putText(
        img,
        f"Frame {frame_num:03d} - Plant Specimen",
        (25, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (20, 60, 20),
        2,
        cv2.LINE_AA,
    )
    return img


def generate_test_videos() -> dict[str, Path]:
    """Generate synthetic videos covering diverse FPS, durations, and artifact types."""
    SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    fourcc_mp4 = cv2.VideoWriter_fourcc(*"mp4v")
    fourcc_avi = cv2.VideoWriter_fourcc(*"XVID")

    # 1. Standard 30 FPS MP4 (5 seconds = 150 frames) with artifact frames
    p1 = SYNTHETIC_DIR / "sample_plant_30fps.mp4"
    out1 = cv2.VideoWriter(str(p1), fourcc_mp4, 30.0, (640, 480))
    for i in range(150):
        # Normal plant frame
        frame = create_synthetic_leaf_frame(640, 480, i)

        # Frame 60 (at 2.0s): Extremely dark frame
        if i == 60:
            frame = np.full((480, 640, 3), 10, dtype=np.uint8)
        # Frame 90 (at 3.0s): Extremely bright/overexposed frame
        elif i == 90:
            frame = np.full((480, 640, 3), 250, dtype=np.uint8)
        # Frame 120 (at 4.0s): Extremely blurry frame (Gaussian blur)
        elif i == 120:
            frame = cv2.GaussianBlur(frame, (51, 51), 30)

        out1.write(frame)
    out1.release()
    paths["standard_30fps"] = p1

    # 2. 15 FPS AVI Video (3 seconds = 45 frames)
    p2 = SYNTHETIC_DIR / "sample_plant_15fps.avi"
    out2 = cv2.VideoWriter(str(p2), fourcc_avi, 15.0, (640, 480))
    for i in range(45):
        frame = create_synthetic_leaf_frame(640, 480, i)
        out2.write(frame)
    out2.release()
    paths["low_fps_15"] = p2

    # 3. 60 FPS MP4 Video (2 seconds = 120 frames)
    p3 = SYNTHETIC_DIR / "sample_plant_60fps.mp4"
    out3 = cv2.VideoWriter(str(p3), fourcc_mp4, 60.0, (640, 480))
    for i in range(120):
        frame = create_synthetic_leaf_frame(640, 480, i)
        out3.write(frame)
    out3.release()
    paths["high_fps_60"] = p3

    # 4. Very Short Video (<1 second: 0.33s = 10 frames at 30 FPS)
    p4 = SYNTHETIC_DIR / "sample_short_03s.mp4"
    out4 = cv2.VideoWriter(str(p4), fourcc_mp4, 30.0, (640, 480))
    for i in range(10):
        frame = create_synthetic_leaf_frame(640, 480, i)
        out4.write(frame)
    out4.release()
    paths["short_video"] = p4

    # 5. Empty Video File (0 bytes)
    p5 = SYNTHETIC_DIR / "empty_video.mp4"
    p5.write_bytes(b"")
    paths["empty_video"] = p5

    # 6. Corrupt Video File (Random garbage bytes)
    p6 = SYNTHETIC_DIR / "corrupt_video.mp4"
    p6.write_bytes(b"GARBAGE_HEADER_CORRUPT_BYTES_NOT_A_REAL_VIDEO_STREAM" * 20)
    paths["corrupt_video"] = p6

    # 7. Unsupported Extension (.txt)
    p7 = SYNTHETIC_DIR / "unsupported_format.txt"
    p7.write_text("This is a plain text file, not a video.")
    paths["unsupported_ext"] = p7

    return paths


def run_all_tests() -> dict[str, Any]:
    print("=" * 60)
    print("RUNNING COMPREHENSIVE VIDEO INPUT MODULE VALIDATION SUITE")
    print("=" * 60)

    test_paths = generate_test_videos()
    results: dict[str, bool] = {}

    # Test 1: Valid MP4 Processing & Metadata
    print("\n[TEST 1] Valid MP4 Metadata Extraction & Processing...")
    try:
        meta = get_video_metadata(test_paths["standard_30fps"])
        assert meta["width"] == 640, f"Expected 640, got {meta['width']}"
        assert meta["height"] == 480, f"Expected 480, got {meta['height']}"
        assert abs(meta["fps"] - 30.0) < 0.5, f"Expected ~30 FPS, got {meta['fps']}"
        assert meta["frame_count"] == 150, f"Expected 150 frames, got {meta['frame_count']}"
        assert abs(meta["duration_seconds"] - 5.0) < 0.2, f"Expected ~5.0s, got {meta['duration_seconds']}"
        print(f"  -> PASS: Valid MP4 detected ({meta['width']}x{meta['height']}, {meta['fps']} FPS, {meta['duration_seconds']}s)")
        results["test_1_valid_mp4_metadata"] = True
    except Exception as e:
        print(f"  -> FAIL: {e}")
        results["test_1_valid_mp4_metadata"] = False

    # Test 2: Valid Video with Different FPS (15 FPS and 60 FPS)
    print("\n[TEST 2] Multi-FPS Video Handling (15 FPS & 60 FPS)...")
    try:
        meta_15 = get_video_metadata(test_paths["low_fps_15"])
        meta_60 = get_video_metadata(test_paths["high_fps_60"])
        assert abs(meta_15["fps"] - 15.0) < 0.5, f"Expected 15 FPS, got {meta_15['fps']}"
        assert abs(meta_60["fps"] - 60.0) < 0.5, f"Expected 60 FPS, got {meta_60['fps']}"
        print(f"  -> PASS: 15 FPS ({meta_15['fps']}) and 60 FPS ({meta_60['fps']}) validated.")
        results["test_2_multi_fps"] = True
    except Exception as e:
        print(f"  -> FAIL: {e}")
        results["test_2_multi_fps"] = False

    # Test 3: Invalid / Non-existent File
    print("\n[TEST 3] Invalid / Non-existent File Error Handling...")
    try:
        validate_video("non_existent_video_path_12345.mp4")
        print("  -> FAIL: Did not raise InvalidVideoError")
        results["test_3_non_existent"] = False
    except InvalidVideoError as e:
        print(f"  -> PASS: Caught expected InvalidVideoError: {e}")
        results["test_3_non_existent"] = True
    except Exception as e:
        print(f"  -> FAIL: Caught unexpected exception: {e}")
        results["test_3_non_existent"] = False

    # Test 4: Unsupported Extension (.txt)
    print("\n[TEST 4] Unsupported Video Extension (.txt)...")
    try:
        validate_video(test_paths["unsupported_ext"])
        print("  -> FAIL: Did not raise InvalidVideoError")
        results["test_4_unsupported_ext"] = False
    except InvalidVideoError as e:
        print(f"  -> PASS: Caught expected InvalidVideoError: {e}")
        results["test_4_unsupported_ext"] = True
    except Exception as e:
        print(f"  -> FAIL: Caught unexpected exception: {e}")
        results["test_4_unsupported_ext"] = False

    # Test 5: Very Short Video (<1s: 0.33s)
    print("\n[TEST 5] Very Short Video (<1s)...")
    try:
        proc_short = process_video(test_paths["short_video"], sample_fps=1.0)
        assert proc_short["sampled_frames"] >= 1, "Should sample at least 1 frame"
        assert proc_short["accepted_frames"] >= 1, "Should accept valid short video frame"
        print(f"  -> PASS: Short video handled cleanly (Sampled: {proc_short['sampled_frames']}, Accepted: {proc_short['accepted_frames']})")
        cleanup_frames(proc_short)
        results["test_5_short_video"] = True
    except Exception as e:
        print(f"  -> FAIL: {e}")
        results["test_5_short_video"] = False

    # Test 6: Empty Video (0 bytes) and Corrupt Video
    print("\n[TEST 6] Empty Video (0 bytes) and Corrupt Video Handling...")
    empty_ok = False
    corrupt_ok = False
    try:
        validate_video(test_paths["empty_video"])
    except EmptyVideoError as e:
        print(f"  -> PASS: Empty video caught EmptyVideoError: {e}")
        empty_ok = True
    except Exception as e:
        print(f"  -> FAIL empty: {e}")

    try:
        validate_video(test_paths["corrupt_video"])
    except (InvalidVideoError, EmptyVideoError) as e:
        print(f"  -> PASS: Corrupt video caught: {e}")
        corrupt_ok = True
    except Exception as e:
        print(f"  -> FAIL corrupt: {e}")

    results["test_6_empty_and_corrupt"] = empty_ok and corrupt_ok

    # Test 7: Dark, Overexposed, and Blurry Frame Rejection
    print("\n[TEST 7] Quality Filter: Dark, Bright, and Blurry Frame Rejection...")
    try:
        # Sample at 1 FPS from standard_30fps (indices: 0, 30, 60, 90, 120)
        # 60 is dark, 90 is bright, 120 is blurry!
        res_q = process_video(test_paths["standard_30fps"], sample_fps=1.0)
        frames_dict = {f["frame_index"]: f for f in res_q["frames"]}

        dark_f = frames_dict.get(60)
        bright_f = frames_dict.get(90)
        blurry_f = frames_dict.get(120)
        normal_f = frames_dict.get(0)

        assert normal_f and normal_f["accepted"] is True, "Frame 0 should be accepted"
        assert dark_f and dark_f["accepted"] is False and dark_f["reason"] == "too_dark", f"Frame 60 expected too_dark, got {dark_f}"
        assert bright_f and bright_f["accepted"] is False and bright_f["reason"] == "too_bright", f"Frame 90 expected too_bright, got {bright_f}"
        assert blurry_f and blurry_f["accepted"] is False and blurry_f["reason"] == "blurry", f"Frame 120 expected blurry, got {blurry_f}"

        print(f"  -> PASS: Normal frame 0 accepted (quality: {normal_f['quality_score']})")
        print(f"  -> PASS: Dark frame 60 rejected (reason: '{dark_f['reason']}', brightness: {dark_f['brightness']})")
        print(f"  -> PASS: Bright frame 90 rejected (reason: '{bright_f['reason']}', brightness: {bright_f['brightness']})")
        print(f"  -> PASS: Blurry frame 120 rejected (reason: '{blurry_f['reason']}', blur_score: {blurry_f['blur_score']})")
        cleanup_frames(res_q)
        results["test_7_quality_rejection"] = True
    except Exception as e:
        print(f"  -> FAIL: {e}")
        results["test_7_quality_rejection"] = False

    # Test 8: Temporary Frame Storage and Cleanup
    print("\n[TEST 8] Temporary Frame Storage and Cleanup...")
    try:
        proc_clean = process_video(test_paths["standard_30fps"], sample_fps=1.0)
        temp_dir = Path(proc_clean["temp_dir"])
        assert temp_dir.exists(), "Temporary directory should exist"
        saved_files = list(temp_dir.glob("*.jpg"))
        assert len(saved_files) == proc_clean["sampled_frames"], f"Saved {len(saved_files)} files, expected {proc_clean['sampled_frames']}"

        # Test cleanup
        cleanup_frames(proc_clean)
        assert not temp_dir.exists(), "Temporary directory should be deleted after cleanup"
        print(f"  -> PASS: Created {len(saved_files)} frames and verified complete directory cleanup.")
        results["test_8_cleanup"] = True
    except Exception as e:
        print(f"  -> FAIL: {e}")
        results["test_8_cleanup"] = False

    # Test 9: Frame Sampling at 1.0 FPS
    print("\n[TEST 9] Frame Sampling at 1.0 FPS...")
    try:
        # 5 seconds at 1 FPS should yield exactly 5 sampled frames (0, 30, 60, 90, 120)
        indices_1fps = compute_sample_indices(150, 30.0, 1.0)
        assert indices_1fps == [0, 30, 60, 90, 120], f"Expected [0, 30, 60, 90, 120], got {indices_1fps}"
        proc_1fps = process_video(test_paths["standard_30fps"], sample_fps=1.0)
        assert proc_1fps["sampled_frames"] == 5, f"Expected 5 sampled frames, got {proc_1fps['sampled_frames']}"
        print(f"  -> PASS: 1.0 FPS sampled exactly 5 frames: {indices_1fps}")
        cleanup_frames(proc_1fps)
        results["test_9_sampling_1fps"] = True
    except Exception as e:
        print(f"  -> FAIL: {e}")
        results["test_9_sampling_1fps"] = False

    # Test 10: Frame Sampling at 2.0 FPS
    print("\n[TEST 10] Frame Sampling at 2.0 FPS...")
    try:
        # 5 seconds at 2 FPS should yield exactly 10 sampled frames (every 15 frames)
        indices_2fps = compute_sample_indices(150, 30.0, 2.0)
        assert len(indices_2fps) == 10, f"Expected 10 indices, got {len(indices_2fps)}: {indices_2fps}"
        assert indices_2fps == [0, 15, 30, 45, 60, 75, 90, 105, 120, 135]
        proc_2fps = process_video(test_paths["standard_30fps"], sample_fps=2.0)
        assert proc_2fps["sampled_frames"] == 10, f"Expected 10 sampled frames, got {proc_2fps['sampled_frames']}"
        print(f"  -> PASS: 2.0 FPS sampled exactly 10 frames: {indices_2fps}")
        cleanup_frames(proc_2fps)
        results["test_10_sampling_2fps"] = True
    except Exception as e:
        print(f"  -> FAIL: {e}")
        results["test_10_sampling_2fps"] = False

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUITE RESULTS SUMMARY")
    print("=" * 60)
    total_passed = sum(1 for v in results.values() if v)
    total_tests = len(results)
    for test_name, passed in results.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {test_name}")
    print(f"\nTOTAL: {total_passed}/{total_tests} passed ({total_passed / total_tests * 100:.1f}%)")

    return results


if __name__ == "__main__":
    res = run_all_tests()
    all_ok = all(res.values())
    sys.exit(0 if all_ok else 1)
