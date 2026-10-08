"""Master Generator for 116 Model 2 V4 Diseases."""

import json
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
OUT_FILE = PROJECT_ROOT / "knowledge" / "data" / "v4_disease_knowledge.py"
M2_MAPPING_PATH = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"

with open(M2_MAPPING_PATH, "r", encoding="utf-8") as f:
    class_map = json.load(f)

v4_slugs = sorted([k for k in class_map.keys() if k != "healthy"])
print(f"Total V4 disease slugs: {len(v4_slugs)}")
