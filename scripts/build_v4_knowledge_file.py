"""Generator for knowledge/data/v4_disease_knowledge.py covering all 116 Model 2 V4 diseases."""

import json
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
OUT_PATH = PROJECT_ROOT / "knowledge" / "data" / "v4_disease_knowledge.py"

def generate_v4_knowledge():
    # Build complete python file content
    lines = []
    lines.append('"""')
    lines.append('Comprehensive Production Agricultural Knowledge Base for Model 2 V4')
    lines.append('=====================================================================')
    lines.append('Contains verified, evidence-grounded DiseaseRecord entries for all 116')
    lines.append('disease classes recognized by Model 2 V4, plus CropRecord agronomy profiles.')
    lines.append('')
    lines.append('100% Deterministic — Zero Generative AI / LLM Dependencies.')
    lines.append('"""')
    lines.append('')
    lines.append('from __future__ import annotations')
    lines.append('')
    lines.append('from knowledge.schema import (')
    lines.append('    CropRecord,')
    lines.append('    DiseaseRecord,')
    lines.append('    ManagementStrategies,')
    lines.append('    SourcedFact,')
    lines.append(')')
    lines.append('')
    lines.append('V4_DISEASE_KNOWLEDGE: dict[str, DiseaseRecord] = {')
    
    # We will write the diseases in order
    return "\n".join(lines)

print("Generator structure ready.")
