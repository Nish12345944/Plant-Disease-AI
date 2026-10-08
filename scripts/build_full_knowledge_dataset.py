"""Builds the complete knowledge/data/v4_disease_knowledge.py dataset for all 116 V4 diseases."""

import json
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
V4_MAPPING_PATH = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"
OUT_FILE = PROJECT_ROOT / "knowledge" / "data" / "v4_disease_knowledge.py"

print("Building complete V4 disease knowledge base...")
