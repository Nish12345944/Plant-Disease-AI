"""Test the live backend video endpoint with gemini_generated_video_17a86e10.mp4."""
import requests
from pathlib import Path

video_path = Path(r"C:\Users\vyasn\Downloads\gemini_generated_video_17a86e10.mp4")

url = "http://127.0.0.1:8000/api/inference/video"

with open(video_path, "rb") as f:
    files = {"file": (video_path.name, f, "video/mp4")}
    data = {"target_frames": 24}
    print(f"Sending {video_path.name} to {url}...")
    resp = requests.post(url, files=files, data=data, timeout=60)

print(f"Status Code: {resp.status_code}")
if resp.status_code == 200:
    res = resp.json()
    print("SUCCESS!")
    print(f"Predicted Crop: {res.get('predicted_crop')} ({res.get('confidence', 0)*100:.2f}%)")
    print(f"Frames Used: {res.get('frames_used')} | Valid Plant Frames: {res.get('valid_plant_frames')}")
    print(f"Top-3: {res.get('top_k')}")
    frames = res.get("frame_results", [])
    print(f"Returned {len(frames)} frame records with thumbnails & ROI thumbnails.")
    if frames:
        sample = frames[0]
        print(f"Sample frame #1: pred={sample.get('predicted_crop')}, conf={sample.get('percentage')}, has_roi_thumb={bool(sample.get('roi_thumbnail'))}")
else:
    print(f"Error: {resp.text}")
