"""Comprehensive frame inspection of gemini_generated_video_17a86e10.mp4."""
import os
import sys
import cv2
import numpy as np
from pathlib import Path

video_path = Path(r"C:\Users\vyasn\Downloads\gemini_generated_video_17a86e10.mp4")
cap = cv2.VideoCapture(str(video_path))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Total frames: {total_frames}, FPS: {fps}")

os.makedirs("scratch/all_video_frames", exist_ok=True)

# Sample every 10th frame (24 frames across video)
indices = np.linspace(0, total_frames - 1, num=24, dtype=int)
frame_data = []

for i, idx in enumerate(indices, 1):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
    ret, frame = cap.read()
    if not ret:
        continue
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    mean_bright = float(np.mean(gray))
    
    out_path = f"scratch/all_video_frames/frame_{i:02d}_idx_{idx:03d}.jpg"
    cv2.imwrite(out_path, frame)
    
    print(f"Frame #{i:02d} | Idx: {idx:03d} | Time: {idx/fps:.2f}s | Brightness: {mean_bright:.1f} | Sharpness (Laplacian): {blur_score:.2f}")

cap.release()
