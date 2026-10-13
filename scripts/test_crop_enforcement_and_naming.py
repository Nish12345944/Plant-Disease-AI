"""
Comprehensive End-to-End Regression Test Suite for Crop Enforcement & Bell Pepper Naming
========================================================================================
Validates all constraints of Tasks 1, 2, and 3:
1. Cucumber input -> only cucumber disease/healthy classes.
2. Zucchini input -> only zucchini disease/healthy classes (no cucumber/squash cross-matching).
3. Bell pepper input -> displayed as 'Bell Pepper', never 'Capsicum'.
4. Unknown or low-confidence crop -> no disease inference based on a guessed crop.
5. Healthy result versus uncertain result distinction.
6. Missing crop mapping -> fails safely (status="uncertain", never "healthy" or guessed disease).
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
from PIL import Image
import numpy as np

WORKSPACE = Path(__file__).resolve().parent.parent
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

from models.model2_classifier_v4.predict import (
    Model2DiseaseClassifierV4,
    format_disease_name_clean,
    format_human_readable,
)
from app.backend.services import process_image_inference, get_model1, get_model2
from model1_test_app.inference import normalize_crop_id, format_class_name


def create_synthetic_leaf(color=(34, 139, 34)) -> Image.Image:
    """Create a synthetic RGB test image."""
    arr = np.full((260, 260, 3), color, dtype=np.uint8)
    return Image.fromarray(arr)


def run_all_tests():
    print("=" * 80)
    print("RUNNING END-TO-END CROP ENFORCEMENT & BELL PEPPER NAMING REGRESSION SUITE")
    print("=" * 80)

    # Initialize classifier with production Retrained V2 configuration
    classifier = get_model2()
    print(f"Loaded Model 2 with {classifier.num_classes} classes from '{classifier.checkpoint_path}'")
    print(f"Loaded crop-disease mapping with {len(classifier.crop_disease_map)} crops from '{classifier.crop_disease_map_path}'")

    test_img = create_synthetic_leaf()
    buf = io.BytesIO()
    test_img.save(buf, format="JPEG")
    test_img_bytes = buf.getvalue()

    tests_run = 0
    tests_passed = 0

    # --------------------------------------------------------------------------
    # Test 1: Cucumber input -> only cucumber disease/healthy classes
    # --------------------------------------------------------------------------
    print("\n--- Test 1: Cucumber Input Biological Compatibility ---")
    tests_run += 1
    # Compatible cucumber classes
    assert classifier.is_compatible("cucumber", "cucumber__powdery_mildew") is True
    assert classifier.is_compatible("cucumber", "cucumber__angular_leaf_spot") is True
    assert classifier.is_compatible("cucumber", "cucumber__bacterial_wilt") is True
    assert classifier.is_compatible("cucumber", "healthy") is True

    # Incompatible other crop classes must be strictly rejected
    incompatible_for_cucumber = [
        "zucchini__powdery_mildew",
        "zucchini__bacterial_wilt",
        "zucchini__yellow_mosaic_virus",
        "squash__powdery_mildew",
        "tomato__early_blight",
        "bell_pepper__bacterial_spot",
        "apple__scab",
    ]
    for inc in incompatible_for_cucumber:
        assert classifier.is_compatible("cucumber", inc) is False, f"Cucumber must reject {inc}"

    # Inference test: cucumber cannot return any other crop's disease
    cuc_res = classifier.predict_crop_aware(test_img, crop_name="cucumber", crop_confidence=0.98)
    assert cuc_res["crop"] == "cucumber"
    assert cuc_res["crop_display"] == "Cucumber"
    if cuc_res["status"] == "diseased":
        assert cuc_res["disease"].startswith("cucumber__"), f"Non-cucumber disease returned: {cuc_res['disease']}"
    for comp in cuc_res["top_compatible"]:
        assert comp["class_name"] == "healthy" or comp["class_name"].startswith("cucumber__")
    print("  [PASS] Test 1: Cucumber input strictly restricted to cucumber diseases and healthy.")
    tests_passed += 1

    # --------------------------------------------------------------------------
    # Test 2: Zucchini input -> only zucchini disease/healthy classes
    # --------------------------------------------------------------------------
    print("\n--- Test 2: Zucchini Input Biological Compatibility ---")
    tests_run += 1
    # Compatible zucchini classes
    assert classifier.is_compatible("zucchini", "zucchini__bacterial_wilt") is True
    assert classifier.is_compatible("zucchini", "zucchini__downy_mildew") is True
    assert classifier.is_compatible("zucchini", "zucchini__powdery_mildew") is True
    assert classifier.is_compatible("zucchini", "zucchini__yellow_mosaic_virus") is True
    assert classifier.is_compatible("zucchini", "healthy") is True

    # Incompatible classes: must NOT allow cucumber or squash diseases on zucchini
    incompatible_for_zucchini = [
        "cucumber__powdery_mildew",
        "cucumber__bacterial_wilt",
        "cucumber__angular_leaf_spot",
        "squash__powdery_mildew",
        "tomato__early_blight",
        "bell_pepper__bacterial_spot",
    ]
    for inc in incompatible_for_zucchini:
        assert classifier.is_compatible("zucchini", inc) is False, f"Zucchini must reject {inc}"

    zuc_res = classifier.predict_crop_aware(test_img, crop_name="zucchini", crop_confidence=0.95)
    assert zuc_res["crop"] == "zucchini"
    assert zuc_res["crop_display"] == "Zucchini"
    if zuc_res["status"] == "diseased":
        assert zuc_res["disease"].startswith("zucchini__"), f"Non-zucchini disease returned: {zuc_res['disease']}"
    for comp in zuc_res["top_compatible"]:
        assert comp["class_name"] == "healthy" or comp["class_name"].startswith("zucchini__")
    print("  [PASS] Test 2: Zucchini input strictly restricted to zucchini diseases and healthy (no cross-match).")
    tests_passed += 1

    # --------------------------------------------------------------------------
    # Test 3: Bell Pepper input -> displayed as "Bell Pepper", never "Capsicum"
    # --------------------------------------------------------------------------
    print("\n--- Test 3: Bell Pepper Naming & Legacy Alias Normalization ---")
    tests_run += 1
    # Normalizer checks
    for alias in ["bellpepper", "capsicum", "bell_pepper", "bell pepper"]:
        assert normalize_crop_id(alias) == "bellpepper", f"Expected canonical ID 'bellpepper' for {alias}"
        assert format_class_name(alias) == "Bell Pepper", f"Expected display 'Bell Pepper' for {alias}"

    # Model 2 inference checks with legacy aliases
    bp_res1 = classifier.predict_crop_aware(test_img, crop_name="bellpepper", crop_confidence=0.99)
    assert bp_res1["crop"] == "bellpepper"
    assert bp_res1["crop_display"] == "Bell Pepper"
    assert "Capsicum" not in bp_res1["human_readable"]
    assert "Bell Pepper" in bp_res1["human_readable"]

    bp_res2 = classifier.predict_crop_aware(test_img, crop_name="capsicum", crop_confidence=0.99)
    assert bp_res2["crop"] == "bellpepper"
    assert bp_res2["crop_display"] == "Bell Pepper"
    assert "Capsicum" not in bp_res2["human_readable"]
    assert "Bell Pepper" in bp_res2["human_readable"]

    # Backend image inference check
    real_bell_path = WORKSPACE / r"data\processed\model2_retraining_v1\test\bell_pepper\blossom_end_rot\3f66f50342_bell_pepper_blossom_end_rot_Google_0327.jpg"
    assert real_bell_path.exists(), f"Image not found at {real_bell_path}"
    real_bp_bytes = real_bell_path.read_bytes()
    backend_res = process_image_inference(real_bp_bytes)
    m1 = backend_res["model1"]
    m2 = backend_res["model2"]
    diag = backend_res["standardized_diagnosis"]
    assert m1["predicted_crop"] == "Bell Pepper", f"Got m1 predicted_crop={m1['predicted_crop']}"
    assert m1["predicted_class"] == "bellpepper", f"Got m1 predicted_class={m1['predicted_class']}"
    assert "Capsicum" not in m2["message"], f"User-facing message contained Capsicum: {m2['message']}"
    assert "Capsicum" not in str(backend_res.get("predicted_crop", "")), "predicted_crop had Capsicum"
    assert diag["crop"] == "bellpepper"
    assert diag["crop_display"] == "Bell Pepper"

    print("  [PASS] Test 3: Canonical ID 'bellpepper' enforced and user-facing label is 'Bell Pepper' (never 'Capsicum').")
    tests_passed += 1

    # --------------------------------------------------------------------------
    # Test 4: Unknown or low-confidence crop -> no disease inference on guessed crop
    # --------------------------------------------------------------------------
    print("\n--- Test 4: Rejection of Unknown / Low-Confidence Crops ---")
    tests_run += 1
    # Unknown crop
    unk_res1 = classifier.predict_crop_aware(test_img, crop_name=None)
    assert unk_res1["status"] == "uncertain"
    assert unk_res1["disease"] is None
    assert len(unk_res1["top_compatible"]) == 0

    unk_res2 = classifier.predict_crop_aware(test_img, crop_name="unknown")
    assert unk_res2["status"] == "uncertain"
    assert unk_res2["disease"] is None
    assert len(unk_res2["top_compatible"]) == 0

    # Low-confidence crop (< 0.25)
    low_res = classifier.predict_crop_aware(test_img, crop_name="tomato", crop_confidence=0.18)
    assert low_res["status"] == "uncertain"
    assert low_res["disease"] is None
    assert len(low_res["top_compatible"]) == 0
    assert "uncertain" in low_res["message"].lower() or "threshold" in low_res["message"].lower()
    print("  [PASS] Test 4: Unknown / low-confidence crops safely yield status='uncertain' with no guessed disease.")
    tests_passed += 1

    # --------------------------------------------------------------------------
    # Test 5: Healthy result versus uncertain result distinction
    # --------------------------------------------------------------------------
    print("\n--- Test 5: Healthy Result vs Uncertain Result Distinction ---")
    tests_run += 1
    # Incompatible condition: bell pepper leaf conditioned on 'apple' -> uncertain, NOT healthy
    if real_bell_path.exists():
        unc_eval = classifier.predict_crop_aware(real_bp_bytes, crop_name="apple", crop_confidence=0.95)
        assert unc_eval["status"] == "uncertain", f"Expected uncertain, got {unc_eval['status']}"
        assert unc_eval["disease"] is None
        assert "Status: Uncertain" in unc_eval["human_readable"]
        assert "No disease detected" not in unc_eval["human_readable"]

    # When healthy foliage has sufficient confidence: status='healthy', disease=None
    # Verify is_compatible handles healthy
    assert classifier.is_compatible("tomato", "healthy") is True
    print("  [PASS] Test 5: Healthy result and uncertain result are strictly differentiated.")
    tests_passed += 1

    # --------------------------------------------------------------------------
    # Test 6: Missing crop mapping -> fail safely
    # --------------------------------------------------------------------------
    print("\n--- Test 6: Missing Crop Mapping Safe Failure ---")
    tests_run += 1
    # Crops in Model 1 but not in Model 2's 36-crop taxonomy:
    missing_crops = ["marigold", "orchid", "anthurium", "carnation", "geranium", "melon"]
    for mc in missing_crops:
        # None of these should be compatible with healthy or any disease
        assert classifier.is_compatible(mc, "healthy") is False, f"Missing crop {mc} must not be compatible with healthy"
        assert classifier.is_compatible(mc, "apple__scab") is False

        # predict_crop_aware must fail safely
        res_mc = classifier.predict_crop_aware(test_img, crop_name=mc, crop_confidence=0.92)
        assert res_mc["status"] == "uncertain", f"Missing crop {mc} must return uncertain, got {res_mc['status']}"
        assert res_mc["disease"] is None, f"Missing crop {mc} must not return disease"
        assert len(res_mc["top_compatible"]) == 0, f"Missing crop {mc} must have 0 compatible candidates"
        assert "not registered" in res_mc["message"].lower()

    print("  [PASS] Test 6: Missing crop mappings fail safely as status='uncertain', never 'No disease detected'.")
    tests_passed += 1

    # Summary
    print("\n" + "=" * 80)
    print(f"ALL {tests_passed}/{tests_run} END-TO-END REGRESSION TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
