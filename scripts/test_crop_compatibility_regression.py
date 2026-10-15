"""
Regression Test Suite for Crop-Disease Compatibility & Status Contract
=======================================================================
Verifies:
1. `bellpepper` matches `bell_pepper__blossom_end_rot` (True).
2. `bellpepper` matches `bell_pepper__bacterial_spot` (True).
3. `capsicum` matches `bell_pepper__bacterial_spot` (True).
4. Incompatible disease remains filtered out (`bellpepper` + `apple__scab` -> False).
5. Healthy compatibility retains universal True across all crops.
6. Backend status contract distinguishes `healthy`, `detected`, and `uncertain`.
7. Uncertain status does not fabricate 0.0% confidence and sets explicit inconclusive indicator.
8. Real diseased bell-pepper leaf is diagnosed properly with high confidence.
"""

import sys
import json
from pathlib import Path
from PIL import Image
import torch
import numpy as np

WORKSPACE = Path(__file__).resolve().parent.parent
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

from models.model2_classifier_v4.predict import Model2DiseaseClassifierV4
from app.backend.services import process_image_inference, get_model1, get_model2


def run_tests():
    print("=" * 80)
    print("RUNNING CROP COMPATIBILITY & STATUS CONTRACT REGRESSION TEST SUITE")
    print("=" * 80)

    # 1. Compatibility unit tests
    m2_chk = WORKSPACE / "models" / "model2_retraining_v2" / "best_model.pth"
    m2_map = WORKSPACE / "models" / "model2_retraining_v2" / "class_mapping.json"
    m2_crop_map = WORKSPACE / "models" / "model2_retraining_v2" / "crop_disease_mapping.json"

    classifier = Model2DiseaseClassifierV4(
        checkpoint_path=m2_chk,
        class_mapping_path=m2_map,
        crop_disease_map_path=m2_crop_map,
        device="cpu",
    )

    tests_run = 0
    tests_passed = 0

    # Test 1: bellpepper + bell_pepper__blossom_end_rot -> True
    tests_run += 1
    t1 = classifier.is_compatible("bellpepper", "bell_pepper__blossom_end_rot")
    assert t1 is True, "Expected True for bellpepper + bell_pepper__blossom_end_rot"
    print("  [PASS] Test 1: 'bellpepper' matches 'bell_pepper__blossom_end_rot' -> True")
    tests_passed += 1

    # Test 2: bellpepper + bell_pepper__bacterial_spot -> True
    tests_run += 1
    t2 = classifier.is_compatible("bellpepper", "bell_pepper__bacterial_spot")
    assert t2 is True, "Expected True for bellpepper + bell_pepper__bacterial_spot"
    print("  [PASS] Test 2: 'bellpepper' matches 'bell_pepper__bacterial_spot' -> True")
    tests_passed += 1

    # Test 3: capsicum + bell_pepper__bacterial_spot -> True (existing alias)
    tests_run += 1
    t3 = classifier.is_compatible("capsicum", "bell_pepper__bacterial_spot")
    assert t3 is True, "Expected True for capsicum + bell_pepper__bacterial_spot"
    print("  [PASS] Test 3: 'capsicum' matches 'bell_pepper__bacterial_spot' -> True")
    tests_passed += 1

    # Test 4: bell_pepper + bell_pepper__bacterial_spot -> True
    tests_run += 1
    t4 = classifier.is_compatible("bell_pepper", "bell_pepper__bacterial_spot")
    assert t4 is True, "Expected True for bell_pepper + bell_pepper__bacterial_spot"
    print("  [PASS] Test 4: 'bell_pepper' matches 'bell_pepper__bacterial_spot' -> True")
    tests_passed += 1

    # Test 5: Incompatible disease filtered out: bellpepper + apple__scab -> False
    tests_run += 1
    t5 = classifier.is_compatible("bellpepper", "apple__scab")
    assert t5 is False, "Expected False for bellpepper + apple__scab"
    print("  [PASS] Test 5: 'bellpepper' + 'apple__scab' -> False (incompatible correctly filtered)")
    tests_passed += 1

    # Test 6: Incompatible disease filtered out: tomato + apple__scab -> False
    tests_run += 1
    t6 = classifier.is_compatible("tomato", "apple__scab")
    assert t6 is False, "Expected False for tomato + apple__scab"
    print("  [PASS] Test 6: 'tomato' + 'apple__scab' -> False (incompatible correctly filtered)")
    tests_passed += 1

    # Test 7: healthy + any crop -> True
    tests_run += 1
    for crop in ["bellpepper", "capsicum", "bell_pepper", "tomato", "apple", "banana"]:
        assert classifier.is_compatible(crop, "healthy") is True, f"Failed healthy for {crop}"
        assert classifier.is_compatible(crop, None) is True, f"Failed None for {crop}"
    print("  [PASS] Test 7: 'healthy' universally compatible across all crops -> True")
    tests_passed += 1

    # Test 8: End-to-end predict_crop_aware on real diseased bell-pepper leaf
    tests_run += 1
    test_img_path = WORKSPACE / r"data\processed\model2_retraining_v2\test\bell_pepper\blossom_end_rot\3f66f50342_bell_pepper_blossom_end_rot_Google_0327.jpg"
    if not test_img_path.is_file():
        test_img_path = WORKSPACE / r"data\processed\model2_retraining_v1\test\bell_pepper\blossom_end_rot\3f66f50342_bell_pepper_blossom_end_rot_Google_0327.jpg"
    assert test_img_path.is_file(), f"Test image not found at {test_img_path}"
    real_img = Image.open(test_img_path).convert("RGB")

    res = classifier.predict_crop_aware(real_img, crop_name="bellpepper", crop_confidence=0.99)
    assert res["status"] == "diseased", f"Expected status 'diseased', got {res['status']}"
    assert res["disease"] in ("bell_pepper__blossom_end_rot", "bell_pepper__bacterial_spot"), f"Unexpected disease: {res['disease']}"
    assert res["disease_confidence"] > 0.90, f"Expected confidence > 0.90, got {res['disease_confidence']}"
    print(f"  [PASS] Test 8: predict_crop_aware('bellpepper') correctly diagnoses disease: '{res['disease']}' ({res['disease_confidence']*100:.1f}%)")
    tests_passed += 1

    # Test 9: End-to-end backend services image inference contract on bell pepper leaf
    tests_run += 1
    img_bytes = test_img_path.read_bytes()
    backend_res = process_image_inference(img_bytes)
    m2 = backend_res.get("model2", {})

    # The backend should detect disease now that bellpepper is compatible!
    assert m2.get("status") == "detected", f"Expected backend status 'detected', got {m2.get('status')}"
    assert m2.get("has_disease") is True, f"Expected has_disease=True, got {m2.get('has_disease')}"
    assert m2.get("primary_disease") is not None, "Expected primary_disease to not be None"
    assert m2.get("confidence") > 0.90, f"Expected confidence > 0.90, got {m2.get('confidence')}"
    print(f"  [PASS] Test 9: process_image_inference contract returns: status='{m2.get('status')}', disease='{m2.get('primary_disease')}', confidence={m2.get('confidence')*100:.1f}%")
    tests_passed += 1

    # Test 10: Uncertain status preservation test (synthesize uncertain condition with incompatible crop)
    tests_run += 1
    # Condition the bell pepper image on 'apple' where bell pepper diseases are incompatible
    unc_res = classifier.predict_crop_aware(real_img, crop_name="apple", crop_confidence=0.95)
    assert unc_res["status"] == "uncertain", f"Expected 'uncertain', got {unc_res['status']}"
    assert unc_res["disease"] is None, f"Expected disease=None, got {unc_res['disease']}"
    # Verify confidence is NOT fabricated 0.0
    assert unc_res["disease_confidence"] > 0.0, f"Expected actual disease_confidence > 0, got {unc_res['disease_confidence']}"
    print(f"  [PASS] Test 10: Incompatible crop produces status='uncertain' with preserved raw confidence: {unc_res['disease_confidence']:.4f}")
    tests_passed += 1

    # Test 11: Healthy specimen contract retention test
    tests_run += 1
    healthy_img_candidates = list((WORKSPACE / "data" / "processed" / "model2_retraining_v1" / "test" / "bell_pepper" / "healthy").glob("*.jpg"))
    if not healthy_img_candidates:
        healthy_img_candidates = list((WORKSPACE / "data" / "downloads" / "beans" / "test" / "test" / "healthy").glob("*.jpg"))
    assert len(healthy_img_candidates) > 0, "No healthy test images found"
    healthy_img_path = healthy_img_candidates[0]
    healthy_bytes = healthy_img_path.read_bytes()
    healthy_backend_res = process_image_inference(healthy_bytes)
    h_m2 = healthy_backend_res.get("model2", {})

    assert h_m2.get("status") in ("healthy", "uncertain"), f"Unexpected healthy status: {h_m2.get('status')}"
    assert h_m2.get("has_disease") is False, f"Expected has_disease=False, got {h_m2.get('has_disease')}"
    if h_m2.get("status") == "healthy":
        assert "Healthy" in h_m2.get("primary_disease", ""), f"Expected Healthy in primary_disease: {h_m2.get('primary_disease')}"
        print(f"  [PASS] Test 11: Healthy specimen correctly identified: status='{h_m2.get('status')}', message='{h_m2.get('message')}', conf={h_m2.get('confidence')*100:.1f}%")
    else:
        print(f"  [PASS] Test 11: Healthy specimen processed without false disease detection: status='{h_m2.get('status')}', has_disease=False")
    tests_passed += 1

    print("\n" + "=" * 80)
    print(f"ALL {tests_passed}/{tests_run} REGRESSION TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)
    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
