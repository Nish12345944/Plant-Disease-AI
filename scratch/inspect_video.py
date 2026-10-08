"""Scratch test script to inspect gemini_generated_video_17a86e10.mp4 frames."""
import os
import cv2
import numpy as np
from pathlib import Path

video_path = Path(r"C:\Users\vyasn\Downloads\gemini_generated_video_17a86e10.mp4")
print(f"Video exists: {video_path.exists()}, Size: {video_path.stat().st_size if video_path.exists() else 0} bytes")

cap = cv2.VideoCapture(str(video_path))
fps = cap.get(cv2.CAP_PROP_FPS)
count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Video metadata: {w}x{h}, {fps} FPS, {count} total frames, duration: {count/fps:.2f}s")

# Extract sample frames to inspect
os.makedirs("scratch/video_test_frames", exist_ok=True)
indices = np.linspace(0, count - 1, num=6, dtype=int)
for i, idx in enumerate(indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f"scratch/video_test_frames/frame_{i:02d}_idx_{idx}.jpg", frame)
        print(f"Saved frame {i} (index {idx})")

cap.release()
