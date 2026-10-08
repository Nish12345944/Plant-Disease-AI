"""Test the complete updated video Model 1 inference pipeline on gemini_generated_video_17a86e10.mp4."""
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model1_test_app.inference import load_model
from model1_test_app.video_inference import predict_video

video_path = Path(r"C:\Users\vyasn\Downloads\gemini_generated_video_17a86e10.mp4")
print(f"Testing video: {video_path}")
print(f"File exists: {video_path.exists()}, Size: {video_path.stat().st_size} bytes")

model, idx_to_class, class_to_idx, device, dev_name = load_model()

result = predict_video(
    video_path=video_path,
    model=model,
    idx_to_class=idx_to_class,
    device=device,
    target_frames=24,
    min_target=16,
    quality_filter=True,
    top_k=3,
)

final_pred = result["final_prediction"]
print("\n" + "="*60)
print(" VIDEO INFERENCE PIPELINE RESULTS")
print("="*60)
print(f"Video: {result['video']['filename']}")
print(f"Duration: {result['video']['duration_seconds']}s | Total Frames: {result['video']['frame_count']} | FPS: {result['video']['fps']}")
print(f"Frames Evaluated: {result['total_evaluated']}")
print(f"Frames Used: {result['frames_used']}")
print(f"Valid Plant Frames (ROIs identified): {result['valid_plant_frames']}")
print(f"Rejected Candidates: {result['frames_rejected']}")
print("\n--- FINAL PREDICTION ---")
print(f"Predicted Crop: {final_pred.get('label', 'Unknown')}")
print(f"Class Name: {final_pred.get('class_name', 'unknown')}")
print(f"Confidence: {final_pred.get('confidence', 0.0):.4f} ({final_pred.get('percentage', 'N/A')})")
print(f"Status: {final_pred.get('status')}")
print(f"Reason: {final_pred.get('reason')}")

print("\n--- TOP-3 AGGREGATED CROPS ---")
for t in result["top_k"]:
    print(f"Rank {t.get('rank')}: {t.get('label')} - {t.get('percentage')} ({t.get('confidence', 0.0):.4f})")

print("\n--- PER-FRAME BREAKDOWN ---")
print(f"{'#':<3} | {'Idx':<5} | {'Time(s)':<7} | {'Status':<7} | {'Crop Prediction':<18} | {'Conf':<8} | {'ROIs':<4} | {'ROI Box':<20}")
print("-" * 85)
for f in result["frame_records"]:
    num = f["frame_number"]
    idx = f["frame_index"]
    ts = f["timestamp_seconds"]
    st = f["status"]
    lbl = f["predicted_label"]
    conf = f["percentage"]
    rois = f["rois_found"]
    box_str = str(f["roi_box"]) if f["roi_box"] else "None"
    print(f"{num:<3} | {idx:<5} | {ts:<7.2f} | {st:<7} | {lbl:<18} | {conf:<8} | {rois:<4} | {box_str:<20}")
