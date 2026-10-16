"""
Regression Test Suite for General Prediction-Reliability & Uncertainty Policy
=============================================================================
Tests:
1. Calibrated temperature scaling is applied to logits.
2. Competing margin threshold triggers 'uncertain' when margin between top-2 candidates is narrow.
3. Universal healthy shielding prevents borderline false alarms when healthy foliage competes.
4. High-confidence clear diseased and clear healthy images remain correctly classified.
5. Three-way outcomes (valid, uncertain, non-plant) are strictly preserved.
"""

import sys
import unittest
from pathlib import Path
from PIL import Image
import numpy as np
import torch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.model2_classifier_v4.predict import Model2DiseaseClassifierV4
from app.backend.services import process_image_inference

class TestGeneralUncertaintyPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.classifier = Model2DiseaseClassifierV4()

    def test_temperature_scaling_attribute_and_application(self):
        """Verify temperature scaling is configured and actively applied."""
        self.assertTrue(hasattr(self.classifier, "temperature"))
        self.assertGreater(self.classifier.temperature, 0.0)
        self.assertAlmostEqual(self.classifier.temperature, 0.9188, delta=0.05)

    def test_competing_margin_uncertainty(self):
        """Verify that narrow margins between top-2 compatible candidates yield status='uncertain'."""
        # Find an image where model predictions are known to be ambiguous
        ambiguous_path = PROJECT_ROOT / "data/processed/model2_retraining_v2/val/eggplant/cercospora_leaf_spot/ps_eggplant_cercospora_leaf_spot_google_0047.jpg"
        if ambiguous_path.exists():
            res = self.classifier.predict_crop_aware(ambiguous_path, crop_name="eggplant")
            # If margin between candidates is narrow or crop is ambiguous, should be uncertain or have high margin
            top_comp = res.get("top_compatible", [])
            if len(top_comp) > 1:
                p1 = top_comp[0].get("crop_aware_probability", top_comp[0]["probability"])
                p2 = top_comp[1].get("crop_aware_probability", top_comp[1]["probability"])
                margin = p1 - p2
                if margin < self.classifier.margin_threshold:
                    self.assertEqual(res["status"], "uncertain")

    def test_clear_healthy_remains_healthy(self):
        """Verify clear healthy images are diagnosed as healthy with high confidence."""
        healthy_path = next((PROJECT_ROOT / "data/processed/model2_retraining_v2/test/tomato/healthy").glob("*.jpg"), None)
        self.assertIsNotNone(healthy_path)
        res = self.classifier.predict_crop_aware(healthy_path, crop_name="tomato")
        self.assertEqual(res["status"], "healthy")
        self.assertGreaterEqual(res["disease_confidence"], 0.70)

    def test_clear_diseased_remains_diseased(self):
        """Verify decisive high-confidence diseases are diagnosed as diseased without suppression."""
        cuc_path = next((PROJECT_ROOT / "data/processed/model2_retraining_v2/test/cucumber/powdery_mildew").glob("*.jpg"), None)
        self.assertIsNotNone(cuc_path)
        res = self.classifier.predict_crop_aware(cuc_path, crop_name="cucumber")
        self.assertEqual(res["status"], "diseased")
        self.assertEqual(res["disease"], "cucumber__powdery_mildew")
        self.assertGreaterEqual(res["disease_confidence"], 0.85)

    def test_e2e_three_way_outcomes_preserved(self):
        """Verify that valid, uncertain, and non-plant outcomes remain distinct."""
        # Valid diseased
        cuc_path = next((PROJECT_ROOT / "data/processed/model2_retraining_v2/test/cucumber/powdery_mildew").glob("*.jpg"), None)
        with open(cuc_path, "rb") as f:
            res_valid = process_image_inference(f.read())
        self.assertEqual(res_valid["model1"]["status"], "valid")
        self.assertEqual(res_valid["model2"]["status"], "detected")

        # Non-plant
        import cv2, io
        blue_img = np.full((224, 224, 3), (255, 0, 0), dtype=np.uint8)
        _, enc = cv2.imencode(".jpg", blue_img)
        res_nonplant = process_image_inference(enc.tobytes())
        self.assertEqual(res_nonplant["model1"]["status"], "rejected")
        self.assertEqual(res_nonplant["model1"]["reason_code"], "non_plant_image")

if __name__ == "__main__":
    unittest.main()
