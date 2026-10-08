"""
Model 2 Disease Classifier Inference Module (Backward Compatibility Wrapper)
=============================================================================
Routes inference through Model 2 V2 with standardized healthy status contract.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.model2_classifier_v2.predict import (
    Model2DiseaseClassifierV2,
    Model2DiseaseClassifier,
    format_disease_name_clean,
    format_human_readable,
    main,
)

__all__ = [
    "Model2DiseaseClassifierV2",
    "Model2DiseaseClassifier",
    "format_disease_name_clean",
    "format_human_readable",
    "main",
]

if __name__ == "__main__":
    main()
