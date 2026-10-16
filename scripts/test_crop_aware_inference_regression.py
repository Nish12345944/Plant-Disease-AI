"""
Regression Test Suite for Crop-Aware Inference Improvements
===========================================================
Verifies:
1. Cucumber vs. Zucchini cross-crop confusion elimination.
2. Tomato disease within-taxonomy prediction and cross-crop barring.
3. Bean disease within-taxonomy prediction and soybean barring.
4. Healthy false positive protection (zero-support classes cannot declare diseased).
5. User-facing 'Bell Pepper' naming (never 'Capsicum').
6. Strict separation of healthy, diseased, and uncertain outcomes.
"""

import sys
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.model2_classifier_v4.predict import Model2DiseaseClassifierV4, ZERO_TEST_SUPPORT_CLASSES

def run_regression_tests():
    print("=" * 80)
    print("RUNNING CROP-AWARE INFERENCE & TAXONOMY REGRESSION TEST SUITE")
    print("=" * 80)

    classifier = Model2DiseaseClassifierV4()

    # Locate test images from dataset
    cuc_img_path = next((PROJECT_ROOT / "data/processed/model2_retraining_v2/test/cucumber/powdery_mildew").glob("*.jpg"), None)
    zuc_img_path = next((PROJECT_ROOT / "data/processed/model2_retraining_v2/test/zucchini/yellow_mosaic_virus").glob("*.jpg"), None)
    tom_img_path = next((PROJECT_ROOT / "data/processed/model2_retraining_v2/test/tomato/early_blight").glob("*.jpg"), None)
    bean_img_path = next((PROJECT_ROOT / "data/processed/model2_retraining_v2/test/bean/rust").glob("*.jpg"), None)
    bp_healthy_path = next((PROJECT_ROOT / "data/processed/model2_retraining_v2/test/bell_pepper/healthy").glob("*.jpg"), None)
    spin_healthy_path = next((PROJECT_ROOT / "data/processed/model2_retraining_v2/test/spinach/healthy").glob("*.jpg"), None)

    assert cuc_img_path and cuc_img_path.exists(), "Cucumber test image not found"
    assert zuc_img_path and zuc_img_path.exists(), "Zucchini test image not found"
    assert tom_img_path and tom_img_path.exists(), "Tomato test image not found"
    assert bean_img_path and bean_img_path.exists(), "Bean test image not found"
    assert bp_healthy_path and bp_healthy_path.exists(), "Bell pepper healthy test image not found"
    assert spin_healthy_path and spin_healthy_path.exists(), "Spinach healthy test image not found"

    # --- Test 1: Cucumber vs Zucchini Confusion Elimination ---
    print("\n--- Test 1: Cucumber vs. Zucchini Cross-Crop Protection ---")
    cuc_res = classifier.predict_crop_aware(cuc_img_path, crop_name="cucumber", crop_confidence=0.99)
    assert cuc_res["status"] == "diseased", f"Expected diseased, got {cuc_res['status']}"
    assert cuc_res["disease"] == "cucumber__powdery_mildew", f"Expected cucumber powdery mildew, got {cuc_res['disease']}"
    assert not cuc_res["disease"].startswith("zucchini__"), "Zucchini disease leaked to cucumber!"
    assert not cuc_res["disease"].startswith("squash__"), "Squash disease leaked to cucumber!"

    # Cross-crop condition test: When given cucumber leaf conditioned on zucchini
    cuc_under_zuc = classifier.predict_crop_aware(cuc_img_path, crop_name="zucchini", crop_confidence=0.99)
    if cuc_under_zuc["status"] == "diseased":
        assert cuc_under_zuc["disease"].startswith("zucchini__"), "Crop-specific filtering violated!"
    print("  [PASS] Test 1: Cucumber and Zucchini cannot cross-contaminate diseases.")

    # --- Test 2: Zucchini yellow mosaic virus within-crop isolation ---
    print("\n--- Test 2: Zucchini Disease Isolation ---")
    zuc_res = classifier.predict_crop_aware(zuc_img_path, crop_name="zucchini", crop_confidence=0.98)
    assert zuc_res["status"] == "diseased", f"Expected diseased, got {zuc_res['status']}"
    assert zuc_res["disease"] == "zucchini__yellow_mosaic_virus", f"Expected zucchini yellow mosaic virus, got {zuc_res['disease']}"
    assert not zuc_res["disease"].startswith("cucumber__"), "Cucumber disease leaked into zucchini!"
    print("  [PASS] Test 2: Zucchini strictly isolated from cucumber and other cucurbits.")

    # --- Test 3: Tomato Disease Taxonomy Isolation ---
    print("\n--- Test 3: Tomato Disease Isolation ---")
    tom_res = classifier.predict_crop_aware(tom_img_path, crop_name="tomato", crop_confidence=0.99)
    assert tom_res["status"] == "diseased", f"Expected diseased, got {tom_res['status']}"
    assert tom_res["disease"] == "tomato__early_blight", f"Expected tomato early blight, got {tom_res['disease']}"
    assert tom_res["disease"].startswith("tomato__"), "Non-tomato disease predicted for tomato leaf!"
    print("  [PASS] Test 3: Tomato early blight correctly diagnosed within tomato taxonomy.")

    # --- Test 4: Bean Rust vs Soybean Confusion Elimination ---
    print("\n--- Test 4: Bean vs. Soybean Disease Isolation ---")
    bean_res = classifier.predict_crop_aware(bean_img_path, crop_name="french_bean", crop_confidence=0.99)
    assert bean_res["status"] == "diseased", f"Expected diseased, got {bean_res['status']}"
    assert bean_res["disease"].startswith("bean__"), f"Expected bean disease, got {bean_res['disease']}"
    assert not bean_res["disease"].startswith("soybean__"), "Soybean disease leaked into bean prediction!"
    print("  [PASS] Test 4: Bean rust strictly isolated from soybean diseases.")

    # --- Test 5: Healthy False Positive Protection & Zero-Support Classes ---
    print("\n--- Test 5: Healthy False Positive Protection ---")
    # Bell pepper healthy
    bp_res = classifier.predict_crop_aware(bp_healthy_path, crop_name="bellpepper", crop_confidence=0.99)
    assert bp_res["status"] == "healthy", f"Expected healthy, got {bp_res['status']}"
    assert bp_res["disease"] is None, f"Expected None disease, got {bp_res['disease']}"

    # Spinach healthy (was historically mispredicted as spinach__pest_damage)
    spin_res = classifier.predict_crop_aware(spin_healthy_path, crop_name="spinach", crop_confidence=0.99)
    assert spin_res["status"] == "healthy", f"Expected healthy, got {spin_res['status']}"
    assert spin_res["disease"] != "spinach__pest_damage", "Zero-support spinach__pest_damage falsely declared on healthy foliage!"
    print("  [PASS] Test 5: Healthy foliage preserved; zero-support classes barred from false disease declaration.")

    # --- Test 6: Zero-Support Disease Non-Certification & 8 V3 Classes ---
    print("\n--- Test 6: Zero-Support Class Rejection & V3 Registration ---")
    assert "spinach__pest_damage" in ZERO_TEST_SUPPORT_CLASSES
    assert "bell_pepper__leaf_curl" in ZERO_TEST_SUPPORT_CLASSES
    assert "tomato__anthracnose" in ZERO_TEST_SUPPORT_CLASSES

    # 8 newly added V3 zero-test-support classes
    v3_new_classes = [
        "cauliflower__alternaria_brassicae",
        "cauliflower__black_spot",
        "cucumber__anthracnose",
        "cucumber__belly_rot",
        "cucumber__downy_mildew",
        "cucumber__gummy_stem_blight",
        "cucumber__pythium_fruit_rot",
        "tomato__fruit_fusarium",
    ]
    for c in v3_new_classes:
        assert c in ZERO_TEST_SUPPORT_CLASSES, f"Missing {c} in ZERO_TEST_SUPPORT_CLASSES"
    assert len(ZERO_TEST_SUPPORT_CLASSES) == 36, f"Expected 36 zero-support classes, found {len(ZERO_TEST_SUPPORT_CLASSES)}"
    print("  [PASS] Test 6: Exactly 36 zero-test-support classes registered and guarded.")

    # --- Test 7: User-Facing Bell Pepper Naming ---
    print("\n--- Test 7: User-Facing Bell Pepper Naming ---")
    for alias in ["bellpepper", "capsicum", "bell_pepper", "Bell Pepper"]:
        res_alias = classifier.predict_crop_aware(bp_healthy_path, crop_name=alias, crop_confidence=0.99)
        assert res_alias["crop_display"] == "Bell Pepper", f"Expected 'Bell Pepper', got '{res_alias['crop_display']}'"
        assert "Capsicum" not in res_alias["human_readable"], f"'Capsicum' leaked into human readable output: {res_alias['human_readable']}"
    print("  [PASS] Test 7: 'Bell Pepper' naming enforced across all aliases (never 'Capsicum').")

    # --- Test 8: Separation of Outcomes ---
    print("\n--- Test 8: Separation of Healthy, Diseased, and Uncertain Outcomes ---")
    assert bp_res["status"] == "healthy" and bp_res["disease"] is None
    assert tom_res["status"] == "diseased" and tom_res["disease"] is not None

    # Inconclusive/uncertain test
    unc_res = classifier.predict_crop_aware(tom_img_path, crop_name="apple", crop_confidence=0.99)
    assert unc_res["status"] == "uncertain", f"Expected uncertain, got {unc_res['status']}"
    assert unc_res["disease"] is None, f"Expected None disease, got {unc_res['disease']}"
    print("  [PASS] Test 8: Outcomes strictly separated (healthy, diseased, uncertain).")

    # --- Test 9: Model 2 V3 Output Dimension & Crop Compatibility ---
    print("\n--- Test 9: Model 2 V3 Output Dimension & Compatibility Mapping ---")
    assert classifier.num_classes == 152, f"Expected 152 classes in Model 2 V3, found {classifier.num_classes}"
    for c in v3_new_classes:
        crop_part = c.split("__")[0]
        assert classifier.is_compatible(crop_part, c) is True, f"Expected {c} to be compatible with {crop_part}"
        assert classifier.is_compatible("apple", c) is False, f"Expected {c} to be incompatible with apple"
    print("  [PASS] Test 9: Model 2 V3 152-class dimension and 8-new-class compatibility verified.")

    # --- Test 10: Rollback Preservation to Model 2 V2 ---
    print("\n--- Test 10: Model 2 V2 Rollback Preservation ---")
    v2_classifier = Model2DiseaseClassifierV4(
        checkpoint_path=PROJECT_ROOT / "models" / "model2_retraining_v2" / "best_model.pth",
        class_mapping_path=PROJECT_ROOT / "models" / "model2_retraining_v2" / "class_mapping.json",
        crop_disease_map_path=PROJECT_ROOT / "models" / "model2_retraining_v2" / "crop_disease_mapping.json",
    )
    assert v2_classifier.num_classes == 144, f"Expected 144 classes in rollback V2, found {v2_classifier.num_classes}"
    v2_res = v2_classifier.predict_crop_aware(bp_healthy_path, crop_name="bell_pepper", crop_confidence=0.99)
    assert v2_res["status"] == "healthy"
    print("  [PASS] Test 10: Model 2 V2 rollback operational with 144 classes and intact behavior.")

    print("\n" + "=" * 80)
    print("ALL 10/10 CROP-AWARE INFERENCE REGRESSION TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_regression_tests()
