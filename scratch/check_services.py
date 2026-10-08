"""Inspect services.process_video_inference directly."""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pathlib import Path
from app.backend.services import process_video_inference

video_path = Path(r"C:\Users\vyasn\Downloads\gemini_generated_video_17a86e10.mp4")
with open(video_path, "rb") as f:
    data = f.read()

res = process_video_inference(data, original_filename="gemini_generated_video_17a86e10.mp4", target_frames=24)
print(f"Crop: {res['predicted_crop']}, Conf: {res['confidence']:.4f}")
print(f"Frames: {len(res['frame_results'])}")
for i, fr in enumerate(res['frame_results'][:5]):
    has_thumb = bool(fr.get('thumbnail'))
    has_roi = bool(fr.get('roi_thumbnail'))
    print(f"Frame #{i+1}: status={fr.get('status')}, crop={fr.get('predicted_crop')}, has_thumb={has_thumb}, has_roi_thumb={has_roi}, box={fr.get('roi_box')}")
