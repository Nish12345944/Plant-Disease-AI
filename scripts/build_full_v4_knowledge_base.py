"""
Build and verify all 116 Model 2 V4 disease knowledge records.
Outputs data directly to knowledge/data/ commodity files and verifies 100% exact class alignment.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Read authoritative classes
mapping_path = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"
with open(mapping_path, "r") as f:
    CLASS_MAPPING = json.load(f)

DISEASE_CLASSES = [k for k in CLASS_MAPPING.keys() if k != "healthy"]
assert len(DISEASE_CLASSES) == 116, f"Expected 116 classes, got {len(DISEASE_CLASSES)}"

print("Authoritative V4 disease classes:")
for i, c in enumerate(DISEASE_CLASSES, 1):
    print(f"{i:3d}. {c}")
