"""Module to construct all 116 V4 Disease Records and write knowledge/data/v4_disease_knowledge.py."""

import json
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
OUT_FILE = PROJECT_ROOT / "knowledge" / "data" / "v4_disease_knowledge.py"
M2_MAPPING_PATH = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"

# Load the 116 V4 disease classes
with open(M2_MAPPING_PATH, "r", encoding="utf-8") as f:
    class_map = json.load(f)

disease_classes = sorted([k for k in class_map.keys() if k != "healthy"])
print(f"Loaded {len(disease_classes)} disease classes.")
