"""
Configuration settings for Model 2 (Plant Disease Detection & Localization using YOLOX-S).
"""

import os
import json

class Model2Config:
    # Model architecture
    MODEL_NAME = "yolox_s"
    DEPTH = 0.33
    WIDTH = 0.50
    NUM_CLASSES = 115
    INPUT_SIZE = (640, 640)
    
    # Pretrained weights
    PRETRAINED_WEIGHTS = "models/pretrained/yolox_s.pth"
    
    # Dataset paths
    SOURCE_DATASET_DIR = "data/processed/model2_dataset"
    CLASS_MAPPING_PATH = os.path.join(SOURCE_DATASET_DIR, "class_mapping.json")
    COCO_DIR = "data/processed/model2_yolox"
    
    # Training hyperparameters
    # Conservative batch size for 4GB RTX 3050 Laptop GPU
    BATCH_SIZE = 8
    VAL_BATCH_SIZE = 8
    ACCUMULATE_GRAD_BATCHES = 2  # Effective batch size = 16
    MAX_EPOCH = 50
    WARMUP_EPOCHS = 3
    BASIC_LR_PER_IMG = 0.01 / 64.0
    LR = 0.002
    MIN_LR_RATIO = 0.05
    MOMENTUM = 0.9
    WEIGHT_DECAY = 5e-4
    EMA = True
    AMP = True
    
    # Output directories
    OUTPUT_MODEL_DIR = "models/model2"
    BEST_MODEL_PATH = os.path.join(OUTPUT_MODEL_DIR, "best_model.pth")
    LAST_MODEL_PATH = os.path.join(OUTPUT_MODEL_DIR, "last_model.pth")
    SAVED_CONFIG_PATH = os.path.join(OUTPUT_MODEL_DIR, "config.json")
    SAVED_CLASS_MAPPING_PATH = os.path.join(OUTPUT_MODEL_DIR, "class_mapping.json")
    TRAINING_SUMMARY_PATH = os.path.join(OUTPUT_MODEL_DIR, "training_summary.json")
    
    # Report directories
    REPORT_DIR = "reports/model2"
    TRAINING_CURVES_PATH = os.path.join(REPORT_DIR, "training_curves.png")
    METRICS_PATH = os.path.join(REPORT_DIR, "metrics.json")
    TRAINING_REPORT_PATH = os.path.join(REPORT_DIR, "model2_training_report.md")
    PREDICTIONS_DIR = "reports/model2_predictions"
    VISUAL_REPORT_PATH = "reports/model2_visual_report.md"

    @classmethod
    def load_class_mapping(cls):
        """Loads and verifies class mapping."""
        with open(cls.CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if "classes" in raw and isinstance(raw["classes"], list):
            mapping = {i: name for i, name in enumerate(raw["classes"])}
        elif "id_to_class" in raw:
            mapping = {int(k): v for k, v in raw["id_to_class"].items()}
        elif "class_to_idx" in raw:
            mapping = {int(v): k for k, v in raw["class_to_idx"].items()}
        else:
            mapping = {int(k): v for k, v in raw.items()}
            
        assert len(mapping) == cls.NUM_CLASSES, f"Expected {cls.NUM_CLASSES} classes, found {len(mapping)}"
        return mapping

    @classmethod
    def to_dict(cls):
        return {
            "model_name": cls.MODEL_NAME,
            "depth": cls.DEPTH,
            "width": cls.WIDTH,
            "num_classes": cls.NUM_CLASSES,
            "input_size": list(cls.INPUT_SIZE),
            "batch_size": cls.BATCH_SIZE,
            "effective_batch_size": cls.BATCH_SIZE * cls.ACCUMULATE_GRAD_BATCHES,
            "max_epoch": cls.MAX_EPOCH,
            "lr": cls.LR,
            "amp": cls.AMP,
            "pretrained_weights": cls.PRETRAINED_WEIGHTS
        }
