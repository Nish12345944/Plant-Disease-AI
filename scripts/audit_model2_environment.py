"""Comprehensive Audit for Model 2 Environment, Dataset, and Dependencies."""

import os
import sys
import json
from pathlib import Path

import torch
import torchvision
import cv2

print("=" * 60)
print("MODEL 2 ENVIRONMENT & HARDWARE AUDIT")
print("=" * 60)
print(f"Python Version: {sys.version.split()[0]}")
print(f"Executable: {sys.executable}")
print(f"PyTorch Version: {torch.__version__}")
print(f"Torchvision Version: {torchvision.__version__}")
print(f"OpenCV Version: {cv2.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA Version: {torch.version.cuda}")
    print(f"GPU Device 0: {torch.cuda.get_device_name(0)}")
    print(f"Compute Capability: {torch.cuda.get_device_capability(0)}")
    vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    print(f"Total VRAM: {vram_gb:.2f} GB")

# Check YOLOX
try:
    import yolox
    yolox_ver = getattr(yolox, "__version__", "custom")
    print(f"YOLOX Installed: YES (version: {yolox_ver})")
except ImportError:
    print("YOLOX Installed: NO")

# Check pycocotools / loguru / tabulate / thop
for pkg in ["pycocotools", "loguru", "tabulate", "thop"]:
    try:
        __import__(pkg)
        print(f"Package '{pkg}': Available")
    except ImportError:
        print(f"Package '{pkg}': NOT Available")

print("\n" + "=" * 60)
print("MODEL 2 DATASET AUDIT")
print("=" * 60)

ds_dir = Path("data/processed/model2_dataset")
print(f"Dataset Path: {ds_dir} (Exists: {ds_dir.exists()})")

if ds_dir.exists():
    for child in sorted(ds_dir.iterdir()):
        if child.is_dir():
            subdirs = [s.name for s in child.iterdir() if s.is_dir()]
            files = [f.name for f in child.iterdir() if f.is_file()]
            print(f"  Directory '{child.name}': {len(subdirs)} subdirs, {len(files)} files")
            for sub in sorted(child.iterdir()):
                if sub.is_dir():
                    count = len(list(sub.glob("*")))
                    print(f"    - {sub.name}: {count} files")
        else:
            print(f"  File: {child.name} ({child.stat().st_size:,} bytes)")

    # Audit Class Mapping
    map_file = ds_dir / "class_mapping.json"
    if map_file.exists():
        with open(map_file, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        
        print("\nClass Mapping Structure:")
        print(f"  Keys in mapping: {list(mapping.keys())}")
        
        # Handle dict format
        if "classes" in mapping:
            cls_list = mapping["classes"]
        elif "class_to_idx" in mapping:
            cls_list = mapping["class_to_idx"]
        elif "idx_to_class" in mapping:
            cls_list = mapping["idx_to_class"]
        else:
            cls_list = mapping
            
        print(f"  Total Classes Count: {len(cls_list)}")
        
        # Print sample
        if isinstance(cls_list, list):
            print(f"  Sample classes (first 5): {cls_list[:5]}")
            print(f"  Sample classes (last 5): {cls_list[-5:]}")
        elif isinstance(cls_list, dict):
            sample_keys = list(cls_list.keys())[:5]
            print(f"  Sample mapping: { {k: cls_list[k] for k in sample_keys} }")

print("=" * 60)
