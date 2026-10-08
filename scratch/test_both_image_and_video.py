"""Comprehensive test script verifying both standalone image inference and video inference."""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.backend.services import process_image_inference, process_video_inference

print("="*75)
print(" 1. TESTING STANDALONE IMAGE INFERENCE (LEAF ON WHITE/PLAIN BACKGROUND)")
print("="*75)

test_images = [
    ("Single Leaf Specimen (Apple)", "data/processed/model2_dataset/images/test/test_apple_scab_66.jpg"),
    ("Multiple Leaves Specimen (Bean Rust)", "data/processed/model2_dataset/images/test/test_bean_rust_16.jpg"),
    ("Detached Leaf Specimen (Tomato Early Blight)", "data/processed/model2_dataset/images/test/test_tomato_early_blight_173.jpg"),
    ("Isolated Leaf Specimen (Cucumber)", "data/processed/model2_dataset/images/test/test_cucumber_angular_leaf_spot_217.jpg"),
]

for label, img_path in test_images:
    if not os.path.exists(img_path):
        continue
    with open(img_path, "rb") as f:
        img_bytes = f.read()
    res = process_image_inference(img_bytes)
    print(f"\n[{label}] File: {os.path.basename(img_path)}")
    print(f"  Status: {res.get('status')}")
    print(f"  Predicted Crop: {res.get('predicted_crop')} ({res.get('percentage')})")
    print(f"  Confidence: {res.get('confidence', 0.0):.4f}")
    print(f"  Top-3:")
    for t in res.get("top_k", [])[:3]:
        print(f"    - Rank {t['rank']}: {t['label']} ({t['percentage']})")

print("\n" + "="*75)
print(" 2. TESTING VIDEO INFERENCE (gemini_generated_video_17a86e10.mp4)")
print("="*75)

video_path = Path(r"C:\Users\vyasn\Downloads\gemini_generated_video_17a86e10.mp4")
if video_path.exists():
    with open(video_path, "rb") as f:
        vid_bytes = f.read()
    v_res = process_video_inference(vid_bytes, original_filename=video_path.name, target_frames=24)
    print(f"Video: {v_res.get('video_name')}")
    print(f"Status: {v_res.get('status')}")
    print(f"Predicted Crop: {v_res.get('predicted_crop')} ({v_res.get('percentage')})")
    print(f"Confidence: {v_res.get('confidence', 0.0):.4f}")
    print(f"Frames Used: {v_res.get('frames_used')} | Valid Plant Frames: {v_res.get('valid_plant_frames')}")
    print(f"Top-3:")
    for t in v_res.get("top_k", []):
        print(f"  - Rank {t['rank']}: {t['label']} ({t['percentage']})")
else:
    print(f"Video file not found at {video_path}")

print("="*75)
