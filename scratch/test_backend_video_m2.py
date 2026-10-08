import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000"
video_path = "gemini_generated_video_17a86e10.mp4"

if not os.path.exists(video_path):
    # Search for mp4 in directory
    mp4s = [f for f in os.listdir(".") if f.endswith(".mp4")]
    if mp4s:
        video_path = mp4s[0]

print(f"Testing video inference with: {video_path}")
with open(video_path, "rb") as f:
    resp = requests.post(
        f"{BASE_URL}/api/chat",
        data={"text": "Identify crop and any diseases in this video", "target_frames": "16"},
        files={"video_file": (os.path.basename(video_path), f, "video/mp4")},
    )

print("Status:", resp.status_code)
data = resp.json()
print("Assistant Message:", data.get("message"))
print("Model 2 Data:", json.dumps(data.get("model2"), indent=2))
print("Frames count in video_inference:", len(data.get("video_inference", {}).get("frame_results", [])))
