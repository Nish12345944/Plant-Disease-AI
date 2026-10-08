"""Backend Configuration for Alexa Farms Multimodal Testing App."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import torch

# Base project root
BACKEND_DIR = Path(__file__).resolve().parent
APP_DIR = BACKEND_DIR.parent
PROJECT_ROOT = APP_DIR.parent

# Ensure project root is in sys.path so modules (audio, video, router, pipeline, model1_test_app) import cleanly
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Model 1 Paths
MODEL1_CHECKPOINT = PROJECT_ROOT / "models" / "model1" / "best_model.pth"
MODEL1_CLASS_MAPPING = PROJECT_ROOT / "models" / "model1" / "class_mapping.json"
MODEL1_CONFIG = PROJECT_ROOT / "models" / "model1" / "config.json"

# Model 2 Paths (EfficientNet-B2 V4 Disease/Healthy Classifier)
MODEL2_CHECKPOINT = PROJECT_ROOT / "models" / "model2_classifier_v4" / "best_model.pth"
MODEL2_CLASS_MAPPING = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"
MODEL2_CONFIG = PROJECT_ROOT / "models" / "model2_classifier_v4" / "config.json"
CROP_DISEASE_MAPPING = PROJECT_ROOT / "data" / "processed" / "model2_organized_crop_disease_mapping.json"
if not CROP_DISEASE_MAPPING.exists():
    CROP_DISEASE_MAPPING = PROJECT_ROOT / "data" / "processed" / "model2_classifier_crop_disease_mapping.json"

# Media Extensions
SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
SUPPORTED_VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v"}
SUPPORTED_AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".opus", ".wma", ".aac", ".webm"}

# Temp storage for uploaded audio, images, and videos during session
TEMP_MEDIA_DIR = PROJECT_ROOT / "temp_multimodal_uploads"
TEMP_MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Hardware execution device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEVICE_NAME = f"CUDA — {torch.cuda.get_device_name(0)}" if torch.cuda.is_available() else "CPU"
