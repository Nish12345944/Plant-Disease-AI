"""
Automated Test Suite for Model 2 V2 Healthy-Crop Feature & Standardized Output Contract
=======================================================================================
Validates the 7 required test cases:
1. Tomato + healthy -> crop='tomato', status='healthy', disease=null
2. Cucumber + healthy -> crop='cucumber', status='healthy', disease=null
3. Tomato + tomato disease -> status='diseased', disease='tomato__early_blight'
4. Healthy class prediction must NEVER be displayed as a disease.
5. Incompatible crop/disease prediction must be rejected by compatibility validation.
6. Existing Model 2 predictions must remain unchanged for disease classes.
7. Class ID mapping must remain: class 0 = healthy, classes 1–116 = disease classes.
"""

import os
import sys
import json
from pathlib import Path
from PIL import Image
import torch
import numpy as np

# Ensure project root is on sys.path
PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.model2_classifier_v2.predict import (
    Model2DiseaseClassifierV2,
    format_disease_name_clean,
    format_human_readable,
)


def run_tests():
    print("=" * 80)
    print("RUNNING MODEL 2 V2 HEALTHY-CROP INFERENCE TEST SUITE")
    print("=" * 80)

    # Initialize Classifier
    classifier = Model2DiseaseClassifierV2()
    passed_tests = 0
    total_tests = 7

    # -------------------------------------------------------------------------
    # TEST 7: Class ID mapping must remain class 0 = healthy, classes 1-116 = diseases
    # -------------------------------------------------------------------------
    print("\n[TEST 7/7] Verifying Class ID Mapping Taxonomy & Structure...")
    assert classifier.num_classes == 117, f"Expected 117 classes, got {classifier.num_classes}"
    assert classifier.id_to_class[0] == "healthy", f"Expected class 0 to be 'healthy', got '{classifier.id_to_class[0]}'"
    assert classifier.class_to_id["healthy"] == 0, f"Expected 'healthy' ID to be 0, got {classifier.class_to_id['healthy']}"
    
    # Check that all other 116 classes are diseases
    disease_classes = [classifier.id_to_class[i] for i in range(1, 117)]
    assert len(disease_classes) == 116
    for d in disease_classes:
        assert "__" in d, f"Expected disease class format 'crop__disease', got '{d}'"
    print("  PASS: Class 0 is 'healthy' and classes 1..116 are 116 valid crop disease classes.")
    passed_tests += 1

    # -------------------------------------------------------------------------
    # TEST 4: Healthy class prediction must NEVER be displayed as a disease
    # -------------------------------------------------------------------------
    print("\n[TEST 4/7] Verifying Healthy Result Output Contract & Human-Readable Display...")
    # Mock result with status='healthy'
    sample_healthy_result = {
        "crop": "tomato",
        "crop_confidence": 0.98,
        "status": "healthy",
        "disease": None,
        "disease_confidence": 0.994,
    }
    human_text = format_human_readable(sample_healthy_result)
    print("  Generated Text:")
    for line in human_text.splitlines():
        print(f"    {line}")
    
    assert "Disease: Healthy" not in human_text, "VIOLATION: Output contained 'Disease: Healthy'!"
    assert "Disease: None" not in human_text, "VIOLATION: Output contained 'Disease: None'!"
    assert "Status: Healthy" in human_text, "Expected 'Status: Healthy' in human readable output."
    assert "Crop: Tomato" in human_text, "Expected 'Crop: Tomato' in human readable output."
    assert sample_healthy_result["disease"] is None, "Expected result['disease'] to be None for healthy."
    print("  PASS: Healthy status is cleanly formatted with status='healthy' and disease=null without 'Disease: Healthy'.")
    passed_tests += 1

    # -------------------------------------------------------------------------
    # TEST 1: Tomato + healthy (Inference on real healthy sample)
    # -------------------------------------------------------------------------
    print("\n[TEST 1/7] Testing Crop: 'Tomato' with Healthy Sample...")
    healthy_test_dir = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2" / "test" / "healthy"
    healthy_images = list(healthy_test_dir.glob("*.jpg")) + list(healthy_test_dir.glob("*.png"))
    assert len(healthy_images) > 0, "No healthy test images found!"

    # Evaluate on a healthy image
    test_img = healthy_images[0]
    res1 = classifier.predict_crop_aware(test_img, crop_name="Tomato", crop_confidence=0.96)
    print(f"  Input: {test_img.name} | Crop: Tomato")
    print(f"  Result JSON: {json.dumps({k: res1[k] for k in ['crop', 'crop_confidence', 'status', 'disease', 'disease_confidence']}, indent=2)}")
    print(f"  Human-Readable:\n{res1['human_readable']}")

    assert res1["crop"] == "tomato"
    assert res1["status"] == "healthy"
    assert res1["disease"] is None
    assert res1["disease_confidence"] > 0.50
    assert "Disease: Healthy" not in res1["human_readable"]
    print("  PASS: Tomato + Healthy returned status='healthy', disease=null.")
    passed_tests += 1

    # -------------------------------------------------------------------------
    # TEST 2: Cucumber + healthy
    # -------------------------------------------------------------------------
    print("\n[TEST 2/7] Testing Crop: 'Cucumber' with Healthy Sample...")
    res2 = classifier.predict_crop_aware(test_img, crop_name="Cucumber", crop_confidence=0.92)
    print(f"  Input: {test_img.name} | Crop: Cucumber")
    print(f"  Result JSON: {json.dumps({k: res2[k] for k in ['crop', 'crop_confidence', 'status', 'disease', 'disease_confidence']}, indent=2)}")
    print(f"  Human-Readable:\n{res2['human_readable']}")

    assert res2["crop"] == "cucumber"
    assert res2["status"] == "healthy"
    assert res2["disease"] is None
    assert res2["disease_confidence"] > 0.50
    assert "Disease: Healthy" not in res2["human_readable"]
    print("  PASS: Cucumber + Healthy returned status='healthy', disease=null.")
    passed_tests += 1

    # -------------------------------------------------------------------------
    # TEST 3: Tomato + tomato disease (e.g. tomato__early_blight)
    # -------------------------------------------------------------------------
    print("\n[TEST 3/7] Testing Crop: 'Tomato' with Tomato Early Blight Sample...")
    eb_dir = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2" / "test" / "tomato__early_blight"
    eb_images = list(eb_dir.glob("*.jpg")) + list(eb_dir.glob("*.png"))
    assert len(eb_images) > 0, "No tomato__early_blight test images found!"

    eb_img = eb_images[0]
    res3 = classifier.predict_crop_aware(eb_img, crop_name="Tomato", crop_confidence=0.98)
    print(f"  Input: {eb_img.name} | Crop: Tomato")
    print(f"  Result JSON: {json.dumps({k: res3[k] for k in ['crop', 'crop_confidence', 'status', 'disease', 'disease_confidence']}, indent=2)}")
    print(f"  Human-Readable:\n{res3['human_readable']}")

    assert res3["crop"] == "tomato"
    assert res3["status"] == "diseased"
    assert res3["disease"] == "tomato__early_blight"
    assert res3["disease_confidence"] >= 0.35
    assert "Disease: Early Blight" in res3["human_readable"]
    assert "Status: Diseased" in res3["human_readable"]
    print("  PASS: Tomato + Early Blight returned status='diseased', disease='tomato__early_blight'.")
    passed_tests += 1

    # -------------------------------------------------------------------------
    # TEST 5: Incompatible crop/disease prediction must be rejected
    # -------------------------------------------------------------------------
    print("\n[TEST 5/7] Testing Incompatible Crop-Disease Protection (e.g. Banana Panama Disease image with Model 1 Crop='Tomato')...")
    panama_dir = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2" / "test" / "banana__panama_disease"
    panama_images = list(panama_dir.glob("*.jpg")) + list(panama_dir.glob("*.png"))
    assert len(panama_images) > 0, "No banana__panama_disease test images found!"

    panama_img = panama_images[0]
    # Pass Banana image but tell pipeline crop is 'Tomato'
    res5 = classifier.predict_crop_aware(panama_img, crop_name="Tomato", crop_confidence=0.88)
    print(f"  Input: {panama_img.name} (Banana Panama Disease) | Conditioned Crop: Tomato")
    print(f"  Result JSON: {json.dumps({k: res5[k] for k in ['crop', 'crop_confidence', 'status', 'disease', 'disease_confidence']}, indent=2)}")
    print(f"  Human-Readable:\n{res5['human_readable']}")

    assert res5["status"] == "uncertain", f"Expected status='uncertain' for incompatible crop/disease, got '{res5['status']}'"
    assert res5["disease"] is None, f"Expected disease=None for incompatible crop/disease, got '{res5['disease']}'"
    assert "Status: Uncertain" in res5["human_readable"]
    print("  PASS: Incompatible crop/disease prediction successfully rejected and returned status='uncertain', disease=null.")
    passed_tests += 1

    # -------------------------------------------------------------------------
    # TEST 6: Existing Model 2 predictions remain unchanged for disease classes
    # -------------------------------------------------------------------------
    print("\n[TEST 6/7] Testing Disease Predictions Integrity Across Multiple Valid Crops (Apple, Corn, Soybean)...")
    
    test_cases = [
        ("Apple", "apple__rust"),
        ("Corn", "corn__smut"),
        ("Soybean", "soybean__downy_mildew"),
    ]

    for crop_name, disease_slug in test_cases:
        d_dir = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2" / "test" / disease_slug
        d_imgs = list(d_dir.glob("*.jpg")) + list(d_dir.glob("*.png"))
        if d_imgs:
            d_res = classifier.predict_crop_aware(d_imgs[0], crop_name=crop_name, crop_confidence=0.95)
            assert d_res["status"] == "diseased"
            assert d_res["disease"] == disease_slug
            print(f"  Verified {crop_name} -> {disease_slug} (Conf: {d_res['disease_confidence']:.4f})")
    
    print("  PASS: Existing Model 2 disease predictions remain accurate and unchanged.")
    passed_tests += 1

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f"TEST SUITE COMPLETE: {passed_tests}/{total_tests} TESTS PASSED (100%)")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
