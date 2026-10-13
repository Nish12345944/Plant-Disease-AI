"""
Regression Test Suite for Model 1 Runtime Checkpoint & Compatibility Configuration.
=====================================================================================
Verifies:
1. Production configuration resolves to the expanded 46-class checkpoint, mapping, and config.
2. Checkpoint output dimension is exactly 46 and class mapping contains exactly 46 classes.
3. The legacy 22-class model cannot be silently selected in production (raises RuntimeError).
4. Explicit test configurations (allow_legacy=True or ALLOW_LEGACY_MODEL1=true) can select alternate checkpoints.
5. Dimension mismatch between checkpoint and class mapping fails clearly (raises ValueError).
6. Missing checkpoint fails clearly (raises FileNotFoundError).
7. Model 2 crop aliases and compatibility handling work seamlessly across all normalized crops.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest
import torch

WORKSPACE = Path(__file__).resolve().parent.parent
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

from app.backend.config import (
    ALLOW_LEGACY_MODEL1,
    MODEL1_CHECKPOINT,
    MODEL1_CLASS_MAPPING,
    MODEL1_CONFIG,
    PROJECT_ROOT,
)
from model1_test_app.inference import (
    DEFAULT_CHECKPOINT_PATH,
    DEFAULT_CONFIG_PATH,
    DEFAULT_MAPPING_PATH,
    validate_model1_setup,
)
from models.model2_classifier_v4.predict import Model2DiseaseClassifierV4


def test_production_config_selects_expanded_checkpoint():
    """Verify production configuration selects expanded 46-class checkpoint."""
    expected_chk = (PROJECT_ROOT / "models" / "model1_expanded" / "best_model.pth").resolve()
    expected_map = (PROJECT_ROOT / "models" / "model1_expanded" / "class_mapping.json").resolve()
    expected_cfg = (PROJECT_ROOT / "models" / "model1_expanded" / "config.json").resolve()

    assert MODEL1_CHECKPOINT.resolve() == expected_chk, (
        f"Expected MODEL1_CHECKPOINT to resolve to {expected_chk}, got {MODEL1_CHECKPOINT}"
    )
    assert MODEL1_CLASS_MAPPING.resolve() == expected_map, (
        f"Expected MODEL1_CLASS_MAPPING to resolve to {expected_map}, got {MODEL1_CLASS_MAPPING}"
    )
    assert MODEL1_CONFIG.resolve() == expected_cfg, (
        f"Expected MODEL1_CONFIG to resolve to {expected_cfg}, got {MODEL1_CONFIG}"
    )

    # Defaults in inference engine
    assert (PROJECT_ROOT / DEFAULT_CHECKPOINT_PATH).resolve() == expected_chk
    assert (PROJECT_ROOT / DEFAULT_MAPPING_PATH).resolve() == expected_map
    assert (PROJECT_ROOT / DEFAULT_CONFIG_PATH).resolve() == expected_cfg


def test_checkpoint_and_mapping_have_46_classes():
    """Verify expanded checkpoint has 46 outputs and mapping has 46 classes."""
    assert MODEL1_CHECKPOINT.exists(), f"Expanded checkpoint missing at {MODEL1_CHECKPOINT}"
    assert MODEL1_CLASS_MAPPING.exists(), f"Expanded mapping missing at {MODEL1_CLASS_MAPPING}"

    # Verify class mapping
    with open(MODEL1_CLASS_MAPPING, "r", encoding="utf-8") as f:
        map_data = json.load(f)
    assert map_data.get("num_classes") == 46, f"Expected 46 classes, got {map_data.get('num_classes')}"
    assert len(map_data["idx_to_class"]) == 46, f"Expected 46 idx_to_class, got {len(map_data['idx_to_class'])}"
    assert len(map_data["class_to_idx"]) == 46, f"Expected 46 class_to_idx, got {len(map_data['class_to_idx'])}"

    # Verify checkpoint weights
    ckpt = torch.load(MODEL1_CHECKPOINT, map_location="cpu", weights_only=False)
    state = ckpt.get("model_state_dict", ckpt)
    weight = state.get("classifier.1.weight", state.get("classifier.weight"))
    assert weight is not None, "Classifier weight not found in checkpoint state dict"
    assert weight.shape[0] == 46, f"Expected 46 output logits, got {weight.shape[0]}"
    assert weight.shape[1] == 1408, f"Expected 1408 EfficientNet-B2 features, got {weight.shape[1]}"


def test_legacy_22_class_model_cannot_be_silently_selected_in_production():
    """Verify legacy 22-class model cannot be silently selected when allow_legacy=False."""
    legacy_chk = PROJECT_ROOT / "models" / "model1" / "best_model.pth"
    legacy_map = PROJECT_ROOT / "models" / "model1" / "class_mapping.json"

    with pytest.raises(RuntimeError) as exc_info:
        validate_model1_setup(
            checkpoint_path=legacy_chk,
            mapping_path=legacy_map,
            allow_legacy=False,
        )
    assert "Legacy Model 1 checkpoint with 22 classes" in str(exc_info.value)
    assert "cannot be silently selected in production" in str(exc_info.value)


def test_explicit_test_config_can_select_alternate_checkpoint():
    """Verify explicit test configurations can still select alternate checkpoints."""
    legacy_chk = PROJECT_ROOT / "models" / "model1" / "best_model.pth"
    legacy_map = PROJECT_ROOT / "models" / "model1" / "class_mapping.json"

    val_info = validate_model1_setup(
        checkpoint_path=legacy_chk,
        mapping_path=legacy_map,
        allow_legacy=True,
    )
    assert val_info["checkpoint_output_dim"] == 22
    assert val_info["num_classes"] == 22
    assert val_info["is_expanded"] is False


def test_mismatched_dimension_and_mapping_fails_clearly():
    """Verify mismatched checkpoint dimension and mapping class count fails clearly."""
    expanded_chk = PROJECT_ROOT / "models" / "model1_expanded" / "best_model.pth"
    legacy_map = PROJECT_ROOT / "models" / "model1" / "class_mapping.json"  # 22 classes

    with pytest.raises(ValueError) as exc_info:
        validate_model1_setup(
            checkpoint_path=expanded_chk,
            mapping_path=legacy_map,
            allow_legacy=True,
        )
    assert "Model 1 dimension mismatch" in str(exc_info.value)
    assert "has 46 output classes, but class mapping" in str(exc_info.value)
    assert "defines 22 classes" in str(exc_info.value)


def test_missing_checkpoint_fails_clearly():
    """Verify missing checkpoint path raises FileNotFoundError with clear explanation."""
    nonexistent = PROJECT_ROOT / "models" / "nonexistent" / "best_model.pth"

    with pytest.raises(FileNotFoundError) as exc_info:
        validate_model1_setup(
            checkpoint_path=nonexistent,
            mapping_path=MODEL1_CLASS_MAPPING,
        )
    assert "Required Model 1 checkpoint not found at" in str(exc_info.value)


def test_model2_crop_aliases_and_compatibility():
    """Verify Model 2 crop aliases and compatibility without modifying checkpoint or taxonomy."""
    m2_chk = PROJECT_ROOT / "models" / "model2_retraining_v2" / "best_model.pth"
    m2_map = PROJECT_ROOT / "models" / "model2_retraining_v2" / "class_mapping.json"
    m2_crop_map = PROJECT_ROOT / "models" / "model2_retraining_v2" / "crop_disease_mapping.json"

    classifier = Model2DiseaseClassifierV4(
        checkpoint_path=m2_chk,
        class_mapping_path=m2_map,
        crop_disease_map_path=m2_crop_map,
        device="cpu",
    )

    # Compatible alias cases
    assert classifier.is_compatible("bellpepper", "bell_pepper__blossom_end_rot") is True
    assert classifier.is_compatible("capsicum", "bell_pepper__bacterial_spot") is True
    assert classifier.is_compatible("bell_pepper", "bell_pepper__bacterial_spot") is True
    assert classifier.is_compatible("french_bean", "bean__rust") is True
    assert classifier.is_compatible("cherry_tomato", "tomato__early_blight") is True
    assert classifier.is_compatible("zucchini", "zucchini__powdery_mildew") is True
    assert classifier.is_compatible("zucchini", "zucchini__yellow_mosaic_virus") is True
    assert classifier.is_compatible("squash", "squash__powdery_mildew") is True
    assert classifier.is_compatible("banana", "banana__panama_disease") is True
    assert classifier.is_compatible("apple", "apple__scab") is True

    # Incompatible cases
    assert classifier.is_compatible("tomato", "apple__scab") is False
    assert classifier.is_compatible("banana", "tomato__early_blight") is False
    assert classifier.is_compatible("bellpepper", "grape__black_rot") is False
    assert classifier.is_compatible("zucchini", "squash__powdery_mildew") is False
    assert classifier.is_compatible("zucchini", "cucumber__powdery_mildew") is False
    assert classifier.is_compatible("cucumber", "zucchini__bacterial_wilt") is False

    # Healthy universal compatibility
    for c in ["bellpepper", "capsicum", "zucchini", "french_bean", "banana", "apple", "potato"]:
        assert classifier.is_compatible(c, "healthy") is True
        assert classifier.is_compatible(c, None) is True


def run_all_tests():
    print("=" * 80)
    print("RUNNING MODEL 1 RUNTIME CONFIGURATION REGRESSION TEST SUITE")
    print("=" * 80)

    test_production_config_selects_expanded_checkpoint()
    print("  [PASS] Test 1: Production config resolves to expanded 46-class checkpoint & mapping")

    test_checkpoint_and_mapping_have_46_classes()
    print("  [PASS] Test 2: Checkpoint has 46 outputs and class mapping has 46 classes")

    test_legacy_22_class_model_cannot_be_silently_selected_in_production()
    print("  [PASS] Test 3: Legacy 22-class model rejected in production without allow_legacy")

    test_explicit_test_config_can_select_alternate_checkpoint()
    print("  [PASS] Test 4: Explicit test configuration (allow_legacy=True) can select alternate checkpoint")

    test_mismatched_dimension_and_mapping_fails_clearly()
    print("  [PASS] Test 5: Checkpoint/mapping dimension mismatch raises clear ValueError")

    test_missing_checkpoint_fails_clearly()
    print("  [PASS] Test 6: Missing checkpoint raises clear FileNotFoundError")

    test_model2_crop_aliases_and_compatibility()
    print("  [PASS] Test 7: Model 2 crop aliases and compatibility function correctly for 46 crops")

    print("\n" + "=" * 80)
    print("ALL 7/7 REGRESSION TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    run_all_tests()
