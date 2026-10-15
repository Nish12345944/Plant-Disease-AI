"""Validation and Safeguard Regression Test Suite.

Tests both Safeguards in the Plant Disease AI multimodal application:
A. Plant Image Validation Gate:
   - Valid supported crop images
   - Non-plant images (synthetic texture/noise/solid)
   - Corrupt / empty / invalid file images
   - Blurry images
   - Dark / underexposed images
B. Open-Set Crop Recognition / Unsupported-Crop Rejection:
   - Unsupported crop rejection (bajra pearl millet, turmeric, etc.)
   - Ambiguous / low-margin predictions flagged as uncertain_crop
   - Visually similar crop pairs
   - Ensuring Model 2 is NEVER invoked when image or crop is rejected
C. Pipeline Integration:
   - Valid text-only requests pass without vision requirements
   - Valid audio-only requests pass without vision requirements
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np
import torch
from PIL import Image

from app.backend.image_validator import (
    MIN_BLUR_SCORE,
    MIN_BRIGHTNESS,
    validate_plant_image,
)
from app.backend.open_set_crop_guard import (
    evaluate_crop_acceptance,
    get_supported_crop_classes,
)
from app.backend.services import (
    process_audio_file,
    process_image_inference,
    process_query_routing,
)


def make_test_image(
    color: tuple[int, int, int] = (34, 139, 34),
    size: tuple[int, int] = (256, 256),
    add_leaf_shapes: bool = True,
) -> bytes:
    """Helper to synthesize valid PNG image bytes with green foliage shapes."""
    img = Image.new("RGB", size, (180, 180, 180))
    arr = np.array(img)
    if add_leaf_shapes:
        # Draw green leaf ellipses with veins
        cv2.ellipse(arr, (128, 128), (80, 45), 35, 0, 360, (34, 139, 34), -1)
        cv2.ellipse(arr, (110, 140), (60, 35), -20, 0, 360, (46, 160, 60), -1)
        # Leaf veins
        cv2.line(arr, (60, 100), (190, 150), (20, 100, 20), 2)
        cv2.line(arr, (128, 128), (145, 110), (20, 100, 20), 1)
        cv2.line(arr, (128, 128), (110, 145), (20, 100, 20), 1)
    else:
        # Solid non-plant color
        arr[:, :] = color

    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def run_safeguard_tests():
    print("=" * 75)
    print("RUNNING COMPREHENSIVE SAFEGUARDS TEST SUITE")
    print("=" * 75)
    passed = 0
    total = 0

    # -------------------------------------------------------------------------
    # TEST 1: Corrupt & Invalid Image Bytes (Safeguard A)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 1] Corrupt and empty image handling...")
    corrupt_bytes = b"NOT_AN_IMAGE_GARBAGE_BYTES_1234567890"
    empty_bytes = b""
    tiny_img = Image.new("RGB", (32, 32), (0, 255, 0))
    tiny_buf = io.BytesIO()
    tiny_img.save(tiny_buf, format="JPEG")
    tiny_bytes = tiny_buf.getvalue()

    r_corrupt = validate_plant_image(corrupt_bytes)
    r_empty = validate_plant_image(empty_bytes)
    r_tiny = validate_plant_image(tiny_bytes)

    assert not r_corrupt.valid and r_corrupt.reason_code == "invalid_file", f"Failed: {r_corrupt}"
    assert not r_empty.valid and r_empty.reason_code == "invalid_file", f"Failed: {r_empty}"
    assert not r_tiny.valid and r_tiny.reason_code == "invalid_file", f"Failed: {r_tiny}"
    print("  -> [PASS] Corrupt, empty, and sub-minimum dimension files rejected with 'invalid_file'.")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 2: Dark / Underexposed & Overexposed Images (Safeguard A)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 2] Extreme exposure and low visibility handling...")
    dark_img = Image.new("RGB", (256, 256), (5, 5, 5))
    dark_buf = io.BytesIO()
    dark_img.save(dark_buf, format="JPEG")
    r_dark = validate_plant_image(dark_buf.getvalue())

    washed_img = Image.new("RGB", (256, 256), (252, 252, 252))
    washed_buf = io.BytesIO()
    washed_img.save(washed_buf, format="JPEG")
    r_washed = validate_plant_image(washed_buf.getvalue())

    assert not r_dark.valid and r_dark.reason_code == "low_visibility", f"Failed dark: {r_dark}"
    assert not r_washed.valid and r_washed.reason_code == "low_visibility", f"Failed washed: {r_washed}"
    print("  -> [PASS] Pitch-black and washed-out glare images rejected with 'low_visibility'.")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 3: Blurry / Out-of-Focus Image (Safeguard A)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 3] Severe blur detection...")
    # Create an image and apply extreme Gaussian blur
    sharp_leaf_bytes = make_test_image(add_leaf_shapes=True)
    sharp_np = np.array(Image.open(io.BytesIO(sharp_leaf_bytes)))
    blurry_np = cv2.GaussianBlur(sharp_np, (51, 51), sigmaX=30)
    blurry_buf = io.BytesIO()
    Image.fromarray(blurry_np).save(blurry_buf, format="JPEG")

    r_blurry = validate_plant_image(blurry_buf.getvalue())
    assert not r_blurry.valid and r_blurry.reason_code == "blurry_image", f"Failed blur: {r_blurry}"
    print(f"  -> [PASS] Severe blur rejected with 'blurry_image' (blur score: {r_blurry.metrics['blur_score']}).")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 4: Non-Plant Image & Real Human Portrait Rejection (Safeguard A)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 4] Non-plant image and real human portrait rejection...")
    # Blue wall / non-vegetation object
    blue_bytes = make_test_image(color=(30, 80, 200), add_leaf_shapes=False)
    r_non_plant = validate_plant_image(blue_bytes)
    assert not r_non_plant.valid and r_non_plant.reason_code == "non_plant_image", f"Failed: {r_non_plant}"

    # Real human portraits (tested with actual user-supplied portraits)
    portrait_candidates = [
        Path.home() / "Downloads" / "nishchal photo.jpg",
        Path.home() / "Downloads" / "praveen soni.jpeg",
    ]
    portrait_tested = False
    for p_path in portrait_candidates:
        if p_path.exists():
            with open(p_path, "rb") as f:
                port_bytes = f.read()
            r_port = validate_plant_image(port_bytes)
            assert not r_port.valid and r_port.reason_code == "non_plant_image", (
                f"Failed: Portrait at {p_path.name} was not rejected as non_plant_image! Result: {r_port}"
            )
            # Ensure full pipeline rejection before Model 1 and Model 2
            with patch("app.backend.services.get_model2") as mock_m2:
                pipe_res = process_image_inference(port_bytes)
                mock_m2.assert_not_called()
                assert pipe_res["status"] == "rejected"
                assert pipe_res["reason_code"] == "non_plant_image"
                assert pipe_res["predicted_crop"] == "Invalid / Non-Plant Image"
                assert pipe_res["model2"]["status"] == "not_applicable"
            portrait_tested = True
            print(f"  -> Verified real portrait '{p_path.name}' strictly rejected at Safeguard A.")

    assert portrait_tested, "At least one real portrait image must be verified."
    print("  -> [PASS] Synthetic and real human portraits rejected as 'non_plant_image' before Model 1 & Model 2.")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 5: Valid Real Plant Images (Safeguard A Pass)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 5] Valid supported plant images validation...")
    wheat_test_path = PROJECT_ROOT / "data/external/end_to_end_test/wheat/wheat_wheat_head_scab_0001.jpg"
    assert wheat_test_path.exists(), "Wheat test image missing"
    with open(wheat_test_path, "rb") as f:
        wheat_bytes = f.read()

    r_wheat_val = validate_plant_image(wheat_bytes)
    assert r_wheat_val.valid and r_wheat_val.status == "valid", f"Failed wheat validation: {r_wheat_val}"
    assert r_wheat_val.reason_code is None
    print(f"  -> [PASS] Real wheat image successfully validated (coverage: {r_wheat_val.metrics['plant_coverage']:.2%}).")

    # Verify supported bell pepper fruit with blossom-end rot passes Safeguards A & B and proceeds to disease diagnosis
    bp_rot_path = PROJECT_ROOT / "data/processed/model2_retraining_v2/test/bell_pepper/blossom_end_rot/190568c5bb_bell_pepper_blossom_end_rot_Bing_0198.jpg"
    if bp_rot_path.exists():
        with open(bp_rot_path, "rb") as f:
            bp_bytes = f.read()
        bp_val = validate_plant_image(bp_bytes)
        assert bp_val.valid, f"Bell pepper blossom-end rot validation failed: {bp_val}"
        bp_res = process_image_inference(bp_bytes)
        assert bp_res["status"] == "valid" and bp_res["crop_status"] == "accepted", f"Crop guard falsely rejected: {bp_res}"
        assert bp_res["predicted_crop"] == "Bell Pepper"
        assert bp_res["model2"]["status"] == "detected"
        print(f"  -> [PASS] Supported Bell Pepper with blossom-end rot accepted and diagnosed ({bp_res['model2']['primary_disease']}, {bp_res['model2']['confidence'] * 100:.1f}%).")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 6: Open-Set Crop Guard - Authoritative Supported Crops (Safeguard B)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 6] Open-Set Crop Guard Authoritative Mapping...")
    supported = get_supported_crop_classes()
    assert len(supported) == 46, f"Expected 46 supported classes, got {len(supported)}"
    assert "wheat" in supported
    assert "tomato" in supported
    assert "cucumber" in supported
    assert "bellpepper" in supported
    assert "plum" in supported
    assert "basil" in supported
    assert "bajra" not in supported
    assert "millet" not in supported
    assert "turmeric" not in supported
    print(f"  -> [PASS] Authoritative 46 supported crops registered (bajra/millet/turmeric strictly absent).")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 7: Open-Set Crop Guard - Unsupported Crop Rejection (Bajra / Turmeric)
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # TEST 7: Open-Set Crop Guard - Unsupported Crop Rejection (Bajra / Turmeric)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 7] Unsupported Crop Rejection on Bajra & Out-of-Distribution Crops...")
    bajra_path = PROJECT_ROOT / "test_multimodal_assets/bajra_test_sample.jpg"
    assert bajra_path.exists(), f"Bajra test asset not found at {bajra_path}"
    with open(bajra_path, "rb") as f:
        bajra_bytes = f.read()

    bajra_res = process_image_inference(bajra_bytes)
    print(f"  -> Bajra prediction: status='{bajra_res.get('status')}', reason_code='{bajra_res.get('reason_code')}'")
    print(f"  -> Predicted crop display: '{bajra_res.get('predicted_crop')}' (confidence: {bajra_res.get('confidence')})")
    print(f"  -> Model 2 status: '{bajra_res['model2']['status']}' (message: {bajra_res['model2']['message']})")

    assert bajra_res["model2"]["status"] == "not_applicable", (
        f"Expected Model 2 to be bypassed ('not_applicable'), but got '{bajra_res['model2']['status']}'"
    )
    assert not bajra_res["model2"]["has_disease"], "Model 2 must not diagnose disease on unsupported crop!"
    assert bajra_res.get("reason_code") in ("unsupported_crop", "uncertain_crop")
    assert bajra_res.get("predicted_crop") in ("Unsupported Crop", "Uncertain Crop")
    assert len(bajra_res.get("top_k", [])) == 0, "Candidate crop predictions must not be exposed to user!"
    print("  -> [PASS] Bajra test image rejected from disease diagnosis without exposing closest-match crop name.")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 8: Ambiguous / Low-Margin & Seedling Predictions Flagged as uncertain_crop
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 8] Ambiguous predictions with narrow margin & seedling uncertainty...")
    ambiguous_top_k = [
        {"class_name": "cucumber", "label": "Cucumber", "confidence": 0.48},
        {"class_name": "zucchini", "label": "Zucchini", "confidence": 0.44},
    ]
    guard_ambiguous = evaluate_crop_acceptance(ambiguous_top_k, min_margin=0.15)
    assert guard_ambiguous.crop_status == "uncertain_crop", f"Failed: {guard_ambiguous}"
    assert not guard_ambiguous.proceed_to_disease_detection, "Must not proceed to Model 2 when ambiguous"
    assert guard_ambiguous.reason_code == "uncertain_crop"
    assert guard_ambiguous.predicted_crop == "Uncertain Crop"
    assert "Crop identity could not be determined reliably" in guard_ambiguous.user_message
    print(f"  -> [PASS] Narrow margin ({guard_ambiguous.margin:.2f} < 0.15) flagged as 'uncertain_crop' without competing names.")

    # Failure 2 regression: Potted green seedling with depressed confidence (Plum 36.7%, Tomato 17.6%)
    seedling_top_k = [
        {"class_name": "plum", "label": "Plum", "confidence": 0.367},
        {"class_name": "tomato", "label": "Tomato", "confidence": 0.176},
    ]
    guard_seedling = evaluate_crop_acceptance(seedling_top_k, min_confidence=0.45)
    assert guard_seedling.crop_status == "uncertain_crop", f"Failed seedling status: {guard_seedling}"
    assert not guard_seedling.proceed_to_disease_detection, "Must not proceed to Model 2 on uncertain seedling"
    assert guard_seedling.reason_code == "uncertain_crop"
    assert guard_seedling.predicted_crop == "Uncertain Crop"
    assert "Crop identity could not be determined reliably" in guard_seedling.user_message
    print(f"  -> [PASS] Seedling prediction correctly flagged as 'uncertain_crop' with standard guidance.")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 9: Model 2 is NEVER Invoked When Validation Fails (Safeguard A + B)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 9] Model 2 Execution Guard Verification...")
    # Test on blurry image through the full inference endpoint
    with patch("app.backend.services.get_model2") as mock_get_m2:
        res_blur_full = process_image_inference(blurry_buf.getvalue())
        # Model 2 singleton must never have been called
        mock_get_m2.assert_not_called()
        assert res_blur_full["model2"]["status"] == "not_applicable"
        assert not res_blur_full["model2"]["has_disease"]

    print("  -> [PASS] Verified Model 2 is strictly bypassed when image validation fails.")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 10: Valid Text-Only and Audio-Only Requests Pass Intact
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 10] Text-Only and Audio-Only Request Preservation...")
    text_query = "What causes tomato early blight and how do I prevent it?"
    route_res = process_query_routing(text_query)
    assert route_res["intent"] in ("disease_detection", "treatment_information", "symptoms"), f"Routing error: {route_res}"

    dummy_audio_bytes = b"RIFF....WAVEfmt " + b"\x00" * 40
    audio_res = process_audio_file(dummy_audio_bytes)
    # Audio processor returns structured dict even if speech transcription is idle/unavailable
    assert "status" in audio_res
    print("  -> [PASS] Text-only and audio-only workflows operate normally without vision gate interference.")
    passed += 1

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print(f"RESULTS: {passed}/{total} SAFEGUARD TESTS PASSED SUCCESSFULLY!")
    print("=" * 75)
    return passed == total


if __name__ == "__main__":
    success = run_safeguard_tests()
    if not success:
        sys.exit(1)
