"""Test Model 1 direct image inference on white background leaf specimens."""
import os
import sys
import glob
import torch
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model1_test_app.inference import load_model, get_eval_transform, format_class_name

model, idx_to_class, class_to_idx, device, dev_name = load_model()
transform = get_eval_transform()

test_images = [
    "data/processed/model2_dataset/images/test/test_apple_black_rot_143.jpg",
    "data/processed/model2_dataset/images/test/test_apple_scab_66.jpg",
    "data/processed/model2_dataset/images/test/test_cucumber_angular_leaf_spot_217.jpg",
    "data/processed/model2_dataset/images/test/test_bean_rust_16.jpg",
    "data/processed/model2_dataset/images/test/test_tomato_early_blight_173.jpg",
]

print("="*70)
print(" DIRECT MODEL 1 INFERENCE ON LEAF SPECIMENS (WITHOUT PLANT_DETECTOR)")
print("="*70)

for img_path in test_images:
    if not os.path.exists(img_path):
        continue
    img = Image.open(img_path).convert("RGB")
    tensor = transform(img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
        
    top5_indices = np.argsort(probs)[::-1][:5]
    
    print(f"\nImage: {os.path.basename(img_path)} ({img.size[0]}x{img.size[1]})")
    for rank, idx in enumerate(top5_indices, 1):
        raw_name = idx_to_class[int(idx)]
        conf = float(probs[idx])
        print(f"  Rank {rank}: {format_class_name(raw_name):<20} {conf*100:6.2f}%")

print("\n" + "="*70)
