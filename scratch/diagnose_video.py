import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import torch
import numpy as np
from collections import defaultdict, Counter

from model1_test_app.inference import load_model
from model1_test_app.video_inference import predict_video
from app.backend.config import (
    DEVICE, MODEL1_CHECKPOINT, MODEL1_CLASS_MAPPING, MODEL1_CONFIG,
    MODEL2_CHECKPOINT
)

video_path = os.path.expanduser('~/Downloads/gemini_generated_video_17a86e10.mp4')
print(f'Testing video: {video_path}')

# Load Model 1
model, idx_to_class, _, _, _ = load_model(
    checkpoint_path=MODEL1_CHECKPOINT,
    mapping_path=MODEL1_CLASS_MAPPING,
    config_path=MODEL1_CONFIG,
    device=DEVICE,
)

# Run video inference with current defaults (conf=0.20)
res = predict_video(
    video_path=video_path,
    model=model,
    idx_to_class=idx_to_class,
    device=DEVICE,
    target_frames=24,
    quality_filter=True,
    top_k=3,
    detect_disease=True,
    disease_conf_threshold=0.20,
)

print('=== VIDEO LEVEL RESULT ===')
print('Final Crop Prediction:', res['final_prediction'])
print('Total Frames Used:', res['frames_used'])
print('Valid Plant Frames:', res['valid_plant_frames'])

print('\n=== FRAME BY FRAME BREAKDOWN ===')
crop_counts = Counter()
disease_frame_map = defaultdict(list)

for f in res['frame_records']:
    f_idx = f['frame_index']
    f_num = f['frame_number']
    status = f['status']
    crop = f['predicted_label']
    conf = f['confidence']
    dets = f.get('disease_detections', [])
    
    crop_counts[crop] += 1
    
    det_strs = [f"{d['disease_label']} ({d['confidence']:.3f})" for d in dets]
    print(f"Frame {f_num:02d} (idx {f_idx:03d}) | Status: {status:7s} | Crop: {crop:12s} ({conf:.2f}) | Diseases: {det_strs if det_strs else 'None'}")
    
    for d in dets:
        disease_frame_map[d['disease_label']].append({
            'frame_num': f_num,
            'frame_idx': f_idx,
            'confidence': d['confidence'],
            'bbox': d['bbox']
        })

print('\n=== DISEASE AGGREGATION AUDIT ===')
print(f'Unique Diseases Predicted: {len(disease_frame_map)}')

for dis, items in sorted(disease_frame_map.items(), key=lambda x: len(x[1]), reverse=True):
    frames_present = sorted(list(set(item['frame_num'] for item in items)))
    confs = [item['confidence'] for item in items]
    mean_conf = float(np.mean(confs))
    max_conf = float(np.max(confs))
    pct_valid = (len(frames_present) / res['valid_plant_frames']) * 100 if res['valid_plant_frames'] > 0 else 0
    is_compat = 'blueberry' in dis.lower()
    compat_str = 'YES (Blueberry disease)' if is_compat else 'NO (Incompatible Crop Disease)'
    print(f"Disease: {dis}")
    print(f"  - Frames: {len(frames_present)}/{res['valid_plant_frames']} ({pct_valid:.1f}%) -> {frames_present}")
    print(f"  - Mean Conf: {mean_conf:.3f} | Max Conf: {max_conf:.3f}")
    print(f"  - Compatible with Crop Blueberry?: {compat_str}")

print('\n=== CURRENT MODEL 2 OUTPUT IN SYSTEM ===')
print(json.dumps(res.get('model2', {}), indent=2))
