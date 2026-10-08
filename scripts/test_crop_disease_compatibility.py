"""
Automated Test Suite for Crop-Disease Compatibility & Inference Layer Protection
================================================================================
Validates the required compatibility invariants:
1. tomato + tomato__early_blight -> VALID (True)
2. tomato + tomato__septoria_leaf_spot -> VALID (True)
3. tomato + apple__scab -> INVALID (False)
4. apple + apple__scab -> VALID (True)
5. soybean + soybean__rust -> VALID (True)
6. soybean + apple__scab -> INVALID (False)
7. healthy + any crop -> VALID (True)
8. Incompatible disease must NEVER appear as final disease in end-to-end inference.
"""

import sys
import json
from pathlib import Path
from PIL import Image
import torch
import numpy as np

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.model2_classifier_v3.predict import Model2DiseaseClassifierV3
from app.backend.services import process_image_inference, get_model1, get_model2


def run_tests():
    print("=" * 80)
    print("RUNNING CROP-DISEASE COMPATIBILITY & INFERENCE LAYER TEST SUITE")
    print("=" * 80)

    classifier = Model2DiseaseClassifierV3()
    passed = 0
    total = 8

    # TEST 1: tomato + tomato__early_blight -> True
    print("\n[TEST 1/8] Verifying is_compatible('tomato', 'tomato__early_blight')...")
    c1 = classifier.is_compatible("tomato", "tomato__early_blight")
    assert c1 is True, "Expected True for tomato + tomato__early_blight"
    print("  PASS: tomato + tomato__early_blight is VALID.")
    passed += 1

    # TEST 2: tomato + tomato__septoria_leaf_spot -> True
    print("\n[TEST 2/8] Verifying is_compatible('tomato', 'tomato__septoria_leaf_spot')...")
    c2 = classifier.is_compatible("tomato", "tomato__septoria_leaf_spot")
    assert c2 is True, "Expected True for tomato + tomato__septoria_leaf_spot"
    print("  PASS: tomato + tomato__septoria_leaf_spot is VALID.")
    passed += 1

    # TEST 3: tomato + apple__scab -> False
    print("\n[TEST 3/8] Verifying is_compatible('tomato', 'apple__scab')...")
    c3 = classifier.is_compatible("tomato", "apple__scab")
    assert c3 is False, "Expected False for tomato + apple__scab"
    print("  PASS: tomato + apple__scab is strictly INVALID (rejected).")
    passed += 1

    # TEST 4: apple + apple__scab -> True
    print("\n[TEST 4/8] Verifying is_compatible('apple', 'apple__scab')...")
    c4 = classifier.is_compatible("apple", "apple__scab")
    assert c4 is True, "Expected True for apple + apple__scab"
    print("  PASS: apple + apple__scab is VALID.")
    passed += 1

    # TEST 5: soybean + soybean__rust -> True
    print("\n[TEST 5/8] Verifying is_compatible('soybean', 'soybean__rust')...")
    c5 = classifier.is_compatible("soybean", "soybean__rust")
    assert c5 is True, "Expected True for soybean + soybean__rust"
    print("  PASS: soybean + soybean__rust is VALID.")
    passed += 1

    # TEST 6: soybean + apple__scab -> False
    print("\n[TEST 6/8] Verifying is_compatible('soybean', 'apple__scab')...")
    c6 = classifier.is_compatible("soybean", "apple__scab")
    assert c6 is False, "Expected False for soybean + apple__scab"
    print("  PASS: soybean + apple__scab is strictly INVALID (rejected).")
    passed += 1

    # TEST 7: healthy + any crop -> True
    print("\n[TEST 7/8] Verifying healthy compatibility across all crops...")
    for crop in ["tomato", "cucumber", "apple", "soybean", "wheat", "corn", "banana"]:
        assert classifier.is_compatible(crop, "healthy") is True, f"Failed for {crop} + healthy"
        assert classifier.is_compatible(crop, None) is True, f"Failed for {crop} + None"
    print("  PASS: healthy is universally compatible across all crops.")
    passed += 1

    # TEST 8: Incompatible disease must never appear as final disease in real inference
    print("\n[TEST 8/8] Testing End-to-End Image Inference on Tomato sample...")
    # Find a tomato sample
    tomato_img_candidates = list((PROJECT_ROOT / "data" / "processed" / "model2_organized" / "test" / "tomato").rglob("*.jpg"))
    if not tomato_img_candidates:
        tomato_img_candidates = list((PROJECT_ROOT / "data" / "external" / "end_to_end_test" / "tomato").glob("*.jpg"))
    assert len(tomato_img_candidates) > 0, "No tomato test images found"

    test_img_path = tomato_img_candidates[0]
    img_bytes = test_img_path.read_bytes()

    res = process_image_inference(img_bytes)
    diag = res["standardized_diagnosis"]
    print(f"  Input Sample: {test_img_path.name}")
    print(f"  Predicted Crop: {diag['crop']} (Conf: {diag['crop_confidence']})")
    print(f"  Final Status: {diag['status']}")
    print(f"  Final Disease: {diag['disease']}")
    print(f"  Model 2 Primary Disease: {res['model2']['primary_disease']}")

    assert diag["disease"] != "apple__scab", "FATAL VIOLATION: apple__scab was returned as final disease for tomato!"
    if diag["status"] == "healthy":
        assert diag["disease"] is None, "Healthy status must have disease=None"
    elif diag["status"] == "diseased":
        assert diag["disease"].startswith("tomato__"), f"Expected tomato disease, got {diag['disease']}"
    print("  PASS: Apple Scab was successfully prevented on tomato leaf; output contract perfectly satisfied.")
    passed += 1

    print("\n" + "=" * 80)
    print(f"TEST SUITE COMPLETE: {passed}/{total} TESTS PASSED (100%)")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
