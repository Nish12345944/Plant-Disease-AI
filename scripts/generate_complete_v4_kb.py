"""Master builder to assemble and write knowledge/data/v4_disease_knowledge.py for all 116 V4 disease classes."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
OUT_FILE = PROJECT_ROOT / "knowledge" / "data" / "v4_disease_knowledge.py"
M2_MAPPING_PATH = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"

with open(M2_MAPPING_PATH, "r", encoding="utf-8") as f:
    class_map = json.load(f)

v4_slugs = sorted([k for k in class_map.keys() if k != "healthy"])
print(f"Targeting {len(v4_slugs)} disease profiles across {len(set(s.split('__')[0] for s in v4_slugs))} crops.")
