"""Test script for 16-24 uniform video frame sampling, inference, and aggregation."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np

from model1_test_app.inference import load_model
from model1_test_app.video_inference import predict_video


def run_test():
    print("=" * 65)
    print("TESTING 16-24 FRAME VIDEO INFERENCE & AGGREGATION")
    print("=" * 65)

    model, idx_to_class, class_to_idx, device, dev_name = load_model()
    print(f"Device: {dev_name}")

    # Create a 6-second video (180 frames @ 30 FPS) with tomato frames
    # and 8 artificially inserted dark/blurry frames to test replenishment!
    tom_path = PROJECT_ROOT / "data/processed/model1_balanced/test/tomato/tomato_fruit_diseased_001434.jpg"
    tom_img = cv2.imread(str(tom_path))
    tom_img = cv2.resize(tom_img, (640, 480))

    vid_path = PROJECT_ROOT / "test_24f_tomato.mp4"
    out = cv2.VideoWriter(str(vid_path), cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (640, 480))

    for i in range(180):
        frame = tom_img.copy()
        # Add smooth movement
        dx = int(12 * np.sin(i / 8.0))
        dy = int(6 * np.cos(i / 8.0))
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        frame = cv2.warpAffine(frame, M, (640, 480))

        # Intentionally inject 8 bad frames (dark/overexposed)
        if i in [15, 35, 55, 75, 95, 115, 135, 155]:
            frame = np.zeros_like(frame)

        out.write(frame)
    out.release()

    print("\nRunning predict_video(target_frames=24)...")
    res = predict_video(
        video_path=vid_path,
        model=model,
        idx_to_class=idx_to_class,
        device=device,
        target_frames=24,
        min_target=16,
        quality_filter=True,
    )

    print(f"\nFinal Prediction: {res['final_prediction']['label']} ({res['final_prediction']['percentage']})")
    print(f"Frames used for Model 1 inference : {res['frames_used']}")
    print(f"Frames rejected by quality filter  : {res['frames_rejected']}")
    print(f"Total candidate frames evaluated  : {res['total_evaluated']}")
    print(f"Number of frame records generated : {len(res['frame_records'])}")
    print(f"Top-3: {[(x['label'], x['percentage']) for x in res['top_k']]}")

    # Invariant assertions:
    assert res["frames_used"] == 24, f"Expected exactly 24 frames, got {res['frames_used']}"
    assert len(res["frame_records"]) == 24, f"Expected 24 frame records, got {len(res['frame_records'])}"
    assert res["final_prediction"]["class_name"] == "tomato", f"Expected tomato, got {res['final_prediction']['class_name']}"

    # Verify every frame record has individual predictions and thumbnails
    for f in res["frame_records"]:
        assert f["predicted_label"] == "Tomato"
        assert f["confidence"] > 0.50
        assert f["thumbnail"] is not None
        assert f["thumbnail"].size == (320, 240)

    print("\nSample of individual frame predictions:")
    for f in res["frame_records"][:6]:
        print(f"  Frame {f['frame_number']:2d} (idx {f['frame_index']:3d}, {f['timestamp_seconds']:5.2f}s): {f['predicted_label']} - {f['percentage']}")
    print("  ...")
    for f in res["frame_records"][-3:]:
        print(f"  Frame {f['frame_number']:2d} (idx {f['frame_index']:3d}, {f['timestamp_seconds']:5.2f}s): {f['predicted_label']} - {f['percentage']}")

    # Clean up test video
    if vid_path.exists():
        vid_path.unlink()

    print("\n" + "=" * 65)
    print("SUCCESS: 24 frames extracted, 24 Model 1 inferences, 24 displayed!")
    print("=" * 65)


if __name__ == "__main__":
    run_test()
