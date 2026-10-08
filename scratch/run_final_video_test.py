"""Run complete updated video inference pipeline on gemini_generated_video_17a86e10.mp4 and verify debug images."""
import os
import sys
import glob
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model1_test_app.inference import load_model
from model1_test_app.video_inference import predict_video

video_path = Path(r"C:\Users\vyasn\Downloads\gemini_generated_video_17a86e10.mp4")
model, idx_to_class, class_to_idx, device, dev_name = load_model()

print("="*75)
print(" RUNNING TIGHT PLANT ROI VIDEO INFERENCE ON gemini_generated_video_17a86e10.mp4")
print("="*75)

result = predict_video(
    video_path=video_path,
    model=model,
    idx_to_class=idx_to_class,
    device=device,
    target_frames=24,
    min_target=16,
    quality_filter=True,
    blur_threshold=10.0,
    save_debug_rois=True,
    debug_dir="reports/video_debug",
)

final_pred = result["final_prediction"]
top_k = result["top_k"]

print(f"\n[VIDEO METADATA]")
print(f"File: {result['video']['filename']} | Duration: {result['video']['duration_seconds']}s | Total Frames: {result['video']['frame_count']}")
print(f"Total Sampled Frames: {result['frames_used']}")
print(f"Usable Plant Frames (Inferences performed): {result['valid_plant_frames']}")
print(f"Rejected Candidate Frames: {result['frames_rejected']}")

print(f"\n[FINAL AGGREGATED RESULT]")
print(f"Final Crop: {final_pred.get('label')}")
print(f"Final Confidence: {final_pred.get('confidence', 0.0):.4f} ({final_pred.get('percentage')})")
print(f"Status: {final_pred.get('status')}")
print(f"Reason: {final_pred.get('reason')}")

print(f"\n[TOP-3 AGGREGATED CROPS]")
for t in top_k:
    print(f"  Rank {t['rank']}: {t['label']:<20} {t['percentage']} (conf: {t['confidence']:.4f})")

print(f"\n[PER-FRAME INFERENCE BREAKDOWN]")
print(f"{'#':<3} | {'Idx':<5} | {'Time':<6} | {'Status':<7} | {'Crop Prediction':<16} | {'Conf':<10} | {'ROIs':<4} | {'ROI Box':<22} | {'Reason'}")
print("-" * 110)
for f in result["frame_records"]:
    num = f["frame_number"]
    idx = f["frame_index"]
    ts = f["timestamp_seconds"]
    st = f["status"]
    lbl = f["predicted_label"]
    conf = f["percentage"]
    rois = f["rois_found"]
    box_str = str(f["roi_box"]) if f["roi_box"] else "None"
    reason = f["reason"]
    print(f"{num:<3} | {idx:<5} | {ts:<5.2f}s | {st:<7} | {lbl:<16} | {conf:<10} | {rois:<4} | {box_str:<22} | {reason}")

debug_files = glob.glob("reports/video_debug/*.jpg")
print(f"\nDebug ROI images generated: {len(debug_files)} images in reports/video_debug/")
