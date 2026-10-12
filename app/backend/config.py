"""Backend Configuration for Alexa Farms Multimodal Testing App."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import torch

# Base project root
BACKEND_DIR = Path(__file__).resolve().parent
APP_DIR = BACKEND_DIR.parent
PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", str(APP_DIR.parent))).resolve()

# Ensure project root is in sys.path so modules (audio, video, router, pipeline, model1_test_app) import cleanly
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Model 1 Paths (Plant Identification Classifier)
MODEL1_CHECKPOINT = Path(os.environ.get("MODEL1_CHECKPOINT", str(PROJECT_ROOT / "models" / "model1" / "best_model.pth")))
MODEL1_CLASS_MAPPING = Path(os.environ.get("MODEL1_CLASS_MAPPING", str(PROJECT_ROOT / "models" / "model1" / "class_mapping.json")))
MODEL1_CONFIG = Path(os.environ.get("MODEL1_CONFIG", str(PROJECT_ROOT / "models" / "model1" / "config.json")))

# Model 2 Paths (EfficientNet-B2 V4 Disease/Healthy Classifier)
MODEL2_CHECKPOINT = Path(os.environ.get("MODEL2_CHECKPOINT", str(PROJECT_ROOT / "models" / "model2_classifier_v4" / "best_model.pth")))
MODEL2_CLASS_MAPPING = Path(os.environ.get("MODEL2_CLASS_MAPPING", str(PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json")))
MODEL2_CONFIG = Path(os.environ.get("MODEL2_CONFIG", str(PROJECT_ROOT / "models" / "model2_classifier_v4" / "config.json")))

_env_crop_disease_map = os.environ.get("CROP_DISEASE_MAPPING")
if _env_crop_disease_map:
    CROP_DISEASE_MAPPING = Path(_env_crop_disease_map)
else:
    CROP_DISEASE_MAPPING = PROJECT_ROOT / "models" / "model2_classifier_v4" / "crop_disease_mapping.json"
    if not CROP_DISEASE_MAPPING.exists():
        CROP_DISEASE_MAPPING = PROJECT_ROOT / "data" / "processed" / "model2_organized_crop_disease_mapping.json"
    if not CROP_DISEASE_MAPPING.exists():
        CROP_DISEASE_MAPPING = PROJECT_ROOT / "data" / "processed" / "model2_classifier_crop_disease_mapping.json"

# Deployment & Memory Tuning Flags
EAGER_LOAD_MODELS = os.environ.get("EAGER_LOAD_MODELS", "false").lower() in ("true", "1", "yes")
WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "tiny")

# Media Extensions
SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
SUPPORTED_VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v"}
SUPPORTED_AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".opus", ".wma", ".aac", ".webm"}

# Temp storage for uploaded audio, images, and videos during session
TEMP_MEDIA_DIR = Path(os.environ.get("TEMP_MEDIA_DIR", str(PROJECT_ROOT / "temp_multimodal_uploads")))
try:
    TEMP_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

# Hardware execution device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEVICE_NAME = f"CUDA — {torch.cuda.get_device_name(0)}" if torch.cuda.is_available() else "CPU"
