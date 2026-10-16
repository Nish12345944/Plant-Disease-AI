"""Regression Test Suite for Non-Plant False Rejection Fix.

Verifies:
1. Valid fruit-bearing plants (Eggplant Phomopsis fruit rot, Bell Pepper blossom-end rot,
   Eggplant Cercospora leaf spot) are verified as plants and NOT rejected as 'non_plant_image'.
2. Ambiguous / multi-crop lookalike plant images are safely categorized as 'uncertain_crop'
   (holding disease diagnosis without falsely claiming the image contains no plant).
3. Genuine non-plant images (human portraits, solid color walls, non-vegetation objects)
   continue to be strictly rejected as 'non_plant_image' before Model 2.
4. Severely blurred images continue to be rejected as 'blurry_image'.
5. Unsupported crops (e.g. Bajra) continue to be safely withheld from disease diagnosis.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np
from PIL import Image

from app.backend.image_validator import validate_plant_image
from app.backend.open_set_crop_guard import evaluate_crop_acceptance
from app.backend.services import process_image_inference


def make_test_image(
    color: tuple[int, int, int] = (30, 80, 200),
    size: tuple[int, int] = (256, 256),
    add_leaf_shapes: bool = False,
) -> bytes:
    img = Image.new("RGB", size, (180, 180, 180))
    arr = np.array(img)
    if add_leaf_shapes:
        cv2.ellipse(arr, (size[0] // 2, size[1] // 2), (size[0] // 3, size[1] // 5), 35, 0, 360, color, -1)
        cv2.line(arr, (size[0] // 4, size[1] // 4), (3 * size[0] // 4, 3 * size[1] // 4), (10, 80, 10), 2)
    else:
        arr[:] = color
        cv2.putText(arr, "NON-PLANT TEST OBJECT", (15, size[1] // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    is_success, buf = cv2.imencode(".png", cv2.cvtColor(arr, cv2.COLOR_RGB2BGR))
    return buf.tobytes()


def run_tests():
    print("=" * 80)
    print("RUNNING NON-PLANT FALSE REJECTION REGRESSION TEST SUITE")
    print("=" * 80)

    passed = 0
    total = 0

    # -------------------------------------------------------------------------
    # TEST 1: Eggplant Phomopsis Fruit Rot (Previously falsely rejected at Safeguard A)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 1] Eggplant Phomopsis Fruit Rot (Fruit lesion validation & diagnosis)...")
    egg_phom_path = PROJECT_ROOT / "data/processed/model2_v2_supplementary_benchmark/images/eggplant/phomopsis_fruit_rot/imgi_121_2.phomopsis1.jpg"
    assert egg_phom_path.exists(), f"Sample not found: {egg_phom_path}"
    with open(egg_phom_path, "rb") as f:
        egg_phom_bytes = f.read()

    val_phom = validate_plant_image(egg_phom_bytes)
    assert val_phom.valid, f"Eggplant fruit rot falsely rejected by Safeguard A: {val_phom}"
    assert val_phom.reason_code is None, f"Expected None reason, got: {val_phom.reason_code}"

    res_phom = process_image_inference(egg_phom_bytes)
    assert res_phom["status"] == "valid", f"Expected valid status, got: {res_phom['status']}"
    assert res_phom["crop_status"] == "accepted", f"Expected accepted, got: {res_phom['crop_status']}"
    assert res_phom["predicted_crop"] == "Eggplant", f"Expected Eggplant, got: {res_phom['predicted_crop']}"
    assert res_phom["model2"]["status"] in ("detected", "healthy", "uncertain"), f"Model 2 status unexpected: {res_phom['model2']['status']}"
    print(f"  -> [PASS] Eggplant Phomopsis fruit rot accepted as Eggplant (coverage: {val_phom.metrics['plant_coverage']:.1%}) and diagnosed by Model 2.")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 2: Eggplant Cercospora Leaf Spot (Previously falsely rejected at Safeguard B)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 2] Eggplant Cercospora Leaf Spot (Foliage lesion acceptance)...")
    egg_leaf_path = PROJECT_ROOT / "data/processed/model2_retraining_v2/val/eggplant/cercospora_leaf_spot/ps_eggplant_cercospora_leaf_spot_google_0050.jpg"
    assert egg_leaf_path.exists(), f"Sample not found: {egg_leaf_path}"
    with open(egg_leaf_path, "rb") as f:
        egg_leaf_bytes = f.read()

    val_leaf = validate_plant_image(egg_leaf_bytes)
    assert val_leaf.valid, f"Eggplant leaf falsely rejected by Safeguard A: {val_leaf}"

    res_leaf = process_image_inference(egg_leaf_bytes)
    assert res_leaf["status"] == "valid", f"Expected valid, got: {res_leaf['status']}"
    assert res_leaf["crop_status"] == "accepted", f"Expected accepted, got: {res_leaf['crop_status']}"
    assert res_leaf["predicted_crop"] == "Eggplant", f"Expected Eggplant, got: {res_leaf['predicted_crop']}"
    assert res_leaf["model2"]["status"] in ("detected", "healthy", "uncertain")
    print(f"  -> [PASS] Eggplant leaf accepted as Eggplant and diagnosed ({res_leaf['model2'].get('primary_disease')}).")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 3: Ambiguous / Low-Margin Plant Images categorized as 'uncertain_crop', NOT 'non_plant_image'
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 3] Ambiguous plant images categorized as 'uncertain_crop' (never 'non_plant_image')...")
    ambig_samples = [
        PROJECT_ROOT / "data/processed/model2_retraining_v2/val/eggplant/cercospora_leaf_spot/ps_eggplant_cercospora_leaf_spot_google_0047.jpg",
        PROJECT_ROOT / "data/processed/model2_retraining_v2/val/eggplant/phomopsis_fruit_rot/1c5b6363e0_imgi_24_images.jpg",
    ]
    for p in ambig_samples:
        if p.exists():
            with open(p, "rb") as f:
                b = f.read()
            val = validate_plant_image(b)
            assert val.valid, f"Plant image should pass Safeguard A: {val}"
            res = process_image_inference(b)
            assert res["status"] == "uncertain", f"Expected uncertain, got: {res['status']}"
            assert res["crop_status"] == "uncertain_crop", f"Expected uncertain_crop, got: {res['crop_status']}"
            assert res["reason_code"] == "uncertain_crop", f"Expected reason_code='uncertain_crop', got: {res['reason_code']}"
            assert res["predicted_crop"] == "Uncertain Crop", f"Expected 'Uncertain Crop', got: {res['predicted_crop']}"
            assert res["model2"]["status"] == "not_applicable", "Model 2 must be bypassed on uncertain crop"
            print(f"  -> [PASS] Ambiguous specimen '{p.name[:30]}' held as 'Uncertain Crop' without falsely claiming non-plant.")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 4: Genuine Non-Plant Images Strictly Rejected
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 4] Genuine non-plant images rejected as 'non_plant_image'...")
    blue_bytes = make_test_image(color=(30, 80, 200), add_leaf_shapes=False)
    r_blue = validate_plant_image(blue_bytes)
    assert not r_blue.valid and r_blue.reason_code == "non_plant_image", f"Blue wall not rejected: {r_blue}"

    gray_bytes = make_test_image(color=(128, 128, 128), add_leaf_shapes=False)
    r_gray = validate_plant_image(gray_bytes)
    assert not r_gray.valid and r_gray.reason_code == "non_plant_image", f"Solid gray not rejected: {r_gray}"

    portraits = [
        Path.home() / "Downloads" / "nishchal photo.jpg",
        Path.home() / "Downloads" / "praveen soni.jpeg",
    ]
    for port in portraits:
        if port.exists():
            with open(port, "rb") as f:
                port_b = f.read()
            r_port = validate_plant_image(port_b)
            assert not r_port.valid and r_port.reason_code == "non_plant_image", f"Portrait not rejected: {r_port}"
            res_port = process_image_inference(port_b)
            assert res_port["status"] == "rejected"
            assert res_port["reason_code"] == "non_plant_image"
            assert res_port["predicted_crop"] == "Invalid / Non-Plant Image"
            print(f"  -> [PASS] Verified real portrait '{port.name}' strictly rejected at Safeguard A.")

    print("  -> [PASS] Genuine non-plant objects and human portraits strictly rejected as 'non_plant_image'.")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 5: Blurry Image Rejection
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 5] Severe blur detection...")
    leaf_img = cv2.imread(str(egg_leaf_path))
    blurred = cv2.GaussianBlur(leaf_img, (65, 65), 30.0)
    _, blur_buf = cv2.imencode(".jpg", blurred)
    r_blur = validate_plant_image(blur_buf.tobytes())
    assert not r_blur.valid and r_blur.reason_code == "blurry_image", f"Blur check failed: {r_blur}"
    print(f"  -> [PASS] Severe blur rejected as 'blurry_image' (blur score: {r_blur.metrics['blur_score']:.1f}).")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 6: Unsupported Crop Rejection (Bajra / Pearl Millet)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 6] Unsupported crop rejection (Bajra)...")
    bajra_path = PROJECT_ROOT / "test_multimodal_assets/bajra_test_sample.jpg"
    assert bajra_path.exists(), f"Bajra sample missing: {bajra_path}"
    with open(bajra_path, "rb") as f:
        bajra_b = f.read()
    bajra_res = process_image_inference(bajra_b)
    assert bajra_res["model2"]["status"] == "not_applicable", "Model 2 must not run on unsupported crop"
    assert bajra_res.get("reason_code") in ("unsupported_crop", "uncertain_crop")
    assert bajra_res.get("predicted_crop") in ("Unsupported Crop", "Uncertain Crop")
    print(f"  -> [PASS] Bajra safely rejected from disease diagnosis (reason: {bajra_res.get('reason_code')}).")
    passed += 1

    # -------------------------------------------------------------------------
    # TEST 7: Fruit-Bearing Organ Variance (Bell Pepper Blossom-End Rot Fruit)
    # -------------------------------------------------------------------------
    total += 1
    print("\n[TEST 7] Bell Pepper Blossom-End Rot Fruit...")
    bp_path = PROJECT_ROOT / "data/processed/model2_retraining_v2/test/bell_pepper/blossom_end_rot/190568c5bb_bell_pepper_blossom_end_rot_Bing_0198.jpg"
    assert bp_path.exists(), f"Bell pepper sample missing: {bp_path}"
    with open(bp_path, "rb") as f:
        bp_b = f.read()
    bp_res = process_image_inference(bp_b)
    assert bp_res["status"] == "valid" and bp_res["crop_status"] == "accepted"
    assert bp_res["predicted_crop"] == "Bell Pepper"
    assert bp_res["model2"]["status"] == "detected"
    print(f"  -> [PASS] Bell Pepper fruit accepted and diagnosed (Disease: {bp_res['model2']['primary_disease']}).")
    passed += 1

    print("=" * 80)
    print(f"RESULTS: {passed}/{total} NON-PLANT REGRESSION TESTS PASSED (100.0%)")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
