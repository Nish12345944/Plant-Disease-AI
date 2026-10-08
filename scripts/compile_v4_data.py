"""Builder script that defines all 116 Model 2 V4 disease profiles and writes v4_disease_knowledge.py."""

import json
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
OUT_PATH = PROJECT_ROOT / "knowledge" / "data" / "v4_disease_knowledge.py"
M2_MAP_PATH = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"

with open(M2_MAP_PATH, "r", encoding="utf-8") as f:
    class_map = json.load(f)

disease_slugs = sorted([k for k in class_map.keys() if k != "healthy"])
print(f"Targeting {len(disease_slugs)} disease profiles.")
