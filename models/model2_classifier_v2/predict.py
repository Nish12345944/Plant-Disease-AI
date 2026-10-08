"""
Model 2 Disease Classifier V2 Inference Engine
===============================================
Provides raw classification inference, crop-disease compatibility filtering,
and the standardized inference contract for the Alexa Farms two-stage pipeline.

Output Contract:
----------------
{
    "crop": "tomato",
    "crop_confidence": 0.98,
    "status": "healthy" | "diseased" | "uncertain",
    "disease": "tomato__early_blight" | null,
    "disease_confidence": 0.95
}

Rules:
1. Model 2 class == healthy:
   -> status = "healthy"
   -> disease = null
   -> Human-readable:
        Crop: Tomato
        Status: Healthy
   (DO NOT output Disease: Healthy)

2. Model 2 class == disease:
   -> status = "diseased"
   -> disease = <predicted disease class slug>
   -> Human-readable:
        Crop: Tomato
        Disease: Early Blight
        Status: Diseased

3. Existing uncertainty logic triggers:
   -> status = "uncertain"
   -> disease = null
   -> Human-readable:
        Crop: Tomato
        Status: Uncertain

4. Incompatible Crop-Disease Prediction:
   -> status = "uncertain"
   -> disease = null
"""

from __future__ import annotations

import argparse
import io
import json
import logging
from pathlib import Path
from typing import Any, Optional, Union

import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import efficientnet_b2

logger = logging.getLogger(__name__)

# Base paths
PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
MODEL_DIR_V2 = PROJECT_ROOT / "models" / "model2_classifier_v2"
DEFAULT_CHECKPOINT_PATH = MODEL_DIR_V2 / "best_model.pth"
DEFAULT_MAPPING_PATH = MODEL_DIR_V2 / "class_mapping.json"
DEFAULT_CONFIG_PATH = MODEL_DIR_V2 / "config.json"
CROP_DISEASE_MAP_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_crop_disease_mapping.json"

# Fallbacks if v2 specific files are in v1 directory
if not DEFAULT_MAPPING_PATH.exists():
    DEFAULT_MAPPING_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_class_mapping.json"
if not CROP_DISEASE_MAP_PATH.exists():
    CROP_DISEASE_MAP_PATH = PROJECT_ROOT / "data" / "processed" / "model2_classifier_crop_disease_mapping.json"

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
DEFAULT_IMAGE_SIZE = (260, 260)


def format_disease_name_clean(slug: Optional[str]) -> Optional[str]:
    """Format machine disease slug (e.g. 'tomato__early_blight') into clean disease title ('Early Blight')."""
    if not slug or slug.lower() == "healthy":
        return None
    if "__" in slug:
        _, disease_part = slug.split("__", 1)
        return disease_part.replace("_", " ").title()
    return slug.replace("_", " ").title()


def format_human_readable(result: dict[str, Any]) -> str:
    """Format standardized prediction result dictionary into human-readable text."""
    crop_str = result.get("crop")
    crop_display = crop_str.replace("_", " ").title() if crop_str else "Unknown Crop"
    status = str(result.get("status", "uncertain")).lower()

    if status == "healthy":
        return f"Crop: {crop_display}\nStatus: Healthy"
    elif status == "diseased":
        disease_slug = result.get("disease")
        disease_display = format_disease_name_clean(disease_slug) or "Disease Detected"
        return f"Crop: {crop_display}\nDisease: {disease_display}\nStatus: Diseased"
    else:
        return f"Crop: {crop_display}\nStatus: Uncertain"


class Model2DiseaseClassifierV2:
    """EfficientNet-B2 117-class disease classifier with crop-aware compatibility masking."""

    def __init__(
        self,
        checkpoint_path: Union[str, Path] = DEFAULT_CHECKPOINT_PATH,
        mapping_path: Union[str, Path] = DEFAULT_MAPPING_PATH,
        crop_disease_map_path: Union[str, Path] = CROP_DISEASE_MAP_PATH,
        config_path: Optional[Union[str, Path]] = DEFAULT_CONFIG_PATH,
        device: Optional[torch.device] = None,
    ):
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device_name = f"CUDA — {torch.cuda.get_device_name(0)}" if self.device.type == "cuda" else "CPU"

        # Load class mappings
        mapping_path = Path(mapping_path).resolve()
        if not mapping_path.exists():
            raise FileNotFoundError(f"Class mapping file not found at: {mapping_path}")

        with open(mapping_path, "r", encoding="utf-8") as f:
            mapping_data = json.load(f)

        self.classes = mapping_data["classes"] if "classes" in mapping_data else list(mapping_data["class_to_id"].keys())
        self.num_classes = len(self.classes)
        self.class_to_id: dict[str, int] = mapping_data["class_to_id"]
        self.id_to_class: dict[int, str] = {int(k): v for k, v in mapping_data["id_to_class"].items()}

        # Verify class 0 is healthy
        if self.id_to_class.get(0) != "healthy":
            raise ValueError(f"Expected class 0 to be 'healthy', got: {self.id_to_class.get(0)}")

        # Load crop-disease compatibility map
        crop_disease_map_path = Path(crop_disease_map_path).resolve()
        if crop_disease_map_path.exists():
            with open(crop_disease_map_path, "r", encoding="utf-8") as f:
                self.crop_disease_map: dict[str, list[str]] = json.load(f)
        else:
            self.crop_disease_map = {}

        # Default decision thresholds
        self.healthy_threshold = 0.50
        self.disease_threshold = 0.35
        self.uncertain_threshold = 0.20
        self.incompatibility_threshold = 0.35
        self.min_compatible_prob_mass = 0.25

        # Load config if available
        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                dt = cfg.get("decision_thresholds", {})
                self.healthy_threshold = dt.get("healthy_threshold", self.healthy_threshold)
                self.disease_threshold = dt.get("disease_threshold", self.disease_threshold)
                self.uncertain_threshold = dt.get("uncertain_threshold", self.uncertain_threshold)

        # Build Model Architecture
        self.model = efficientnet_b2(weights=None)
        in_features = self.model.classifier[1].in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(in_features, self.num_classes),
        )

        # Load Checkpoint weights
        checkpoint_path = Path(checkpoint_path).resolve()
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Model 2 checkpoint not found at: {checkpoint_path}")

        chk = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
        state_dict = chk.get("model_state_dict", chk)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()

        # Standard Preprocessing Transform
        self.transform = transforms.Compose([
            transforms.Resize(DEFAULT_IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])

        logger.info(f"Model 2 V2 loaded on {self.device_name} with {self.num_classes} classes.")

    def _prepare_image(self, image_input: Union[str, Path, Image.Image, np.ndarray, bytes]) -> Image.Image:
        """Convert various input types to RGB PIL Image."""
        if isinstance(image_input, (str, Path)):
            return Image.open(str(image_input)).convert("RGB")
        elif isinstance(image_input, bytes):
            return Image.open(io.BytesIO(image_input)).convert("RGB")
        elif isinstance(image_input, np.ndarray):
            if image_input.ndim == 3 and image_input.shape[2] == 3:
                return Image.fromarray(image_input).convert("RGB")
            elif image_input.ndim == 2:
                return Image.fromarray(image_input).convert("RGB")
            else:
                raise ValueError(f"Unsupported array shape: {image_input.shape}")
        elif isinstance(image_input, Image.Image):
            return image_input.convert("RGB")
        else:
            raise TypeError(f"Unsupported image input type: {type(image_input)}")

    def predict_raw(self, image_input: Union[str, Path, Image.Image, np.ndarray, bytes]) -> dict[str, Any]:
        """Runs unconstrained Model 2 classification over all 117 classes."""
        img = self._prepare_image(image_input)
        tensor = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()

        top5_indices = probs.argsort()[-5:][::-1]
        top5_results = [
            {
                "class_id": int(i),
                "class_name": self.id_to_class[i],
                "disease_name": format_disease_name_clean(self.id_to_class[i]),
                "probability": float(probs[i]),
                "is_healthy": (i == 0),
            }
            for i in top5_indices
        ]

        top1_idx = int(top5_indices[0])
        top1_class = self.id_to_class[top1_idx]
        is_healthy = (top1_idx == 0)

        return {
            "top1_class_id": top1_idx,
            "top1_class": top1_class,
            "top1_confidence": float(probs[top1_idx]),
            "is_healthy": is_healthy,
            "all_probabilities": probs,
            "top5": top5_results,
        }

    def _get_compatible_classes_for_crop(self, crop_name: str) -> list[str]:
        """Resolve compatible classes for a given crop name from the compatibility map."""
        crop_clean = crop_name.strip()
        crop_title = crop_clean.title()
        crop_lower = crop_clean.lower()

        # Direct map lookup (case-insensitive key)
        for key, val in self.crop_disease_map.items():
            if key.lower() == crop_lower or key.lower() == crop_title.lower():
                compatible = list(val)
                if "healthy" not in compatible:
                    compatible.append("healthy")
                return compatible

        # Substring / slug lookup
        crop_prefix = crop_lower.replace(" ", "_") + "__"
        matched = [c for c in self.classes if c == "healthy" or c.startswith(crop_prefix)]
        if len(matched) > 1:
            return matched

        # Fallback to shared healthy class only
        return ["healthy"]

    def predict_crop_aware(
        self,
        image_input: Union[str, Path, Image.Image, np.ndarray, bytes],
        crop_name: Optional[str] = None,
        crop_confidence: Optional[float] = None,
    ) -> dict[str, Any]:
        """
        Runs Model 2 inference conditioned on Model 1 crop prediction.
        Applies crop-disease compatibility mask, incompatible prediction protection,
        and standardizes the output contract.
        """
        raw_res = self.predict_raw(image_input)
        probs = raw_res["all_probabilities"].copy()
        raw_top1_idx = raw_res["top1_class_id"]
        raw_top1_class = raw_res["top1_class"]
        raw_top1_conf = raw_res["top1_confidence"]

        if not crop_name:
            # Standalone Model 2 inference without Model 1 crop conditioning
            if raw_res["is_healthy"]:
                status = "healthy"
                disease = None
                disease_conf = raw_top1_conf
                inferred_crop = None
            elif raw_top1_conf >= self.disease_threshold:
                status = "diseased"
                disease = raw_top1_class
                disease_conf = raw_top1_conf
                inferred_crop = raw_top1_class.split("__")[0] if "__" in raw_top1_class else None
            else:
                status = "uncertain"
                disease = None
                disease_conf = raw_top1_conf
                inferred_crop = None

            result = {
                "crop": inferred_crop,
                "crop_confidence": 1.0 if inferred_crop else None,
                "status": status,
                "disease": disease,
                "disease_confidence": round(float(disease_conf), 4),
            }
            result["human_readable"] = format_human_readable(result)
            result["raw_prediction"] = raw_res
            return result

        crop_clean = crop_name.strip()
        crop_normalized = crop_clean.lower()
        compatible_classes = self._get_compatible_classes_for_crop(crop_clean)

        # Create compatibility boolean mask
        mask = np.zeros(self.num_classes, dtype=bool)
        for c_name in compatible_classes:
            if c_name in self.class_to_id:
                mask[self.class_to_id[c_name]] = True

        # Class 0 (healthy) is ALWAYS compatible with every supported crop
        mask[0] = True

        # Incompatible prediction protection:
        # If raw top-1 prediction is a disease of a DIFFERENT crop with strong confidence,
        # or the sum of probabilities for compatible classes is negligible, reject as uncertain.
        raw_top1_is_disease = (raw_top1_idx != 0)
        raw_top1_is_incompatible = raw_top1_is_disease and not mask[raw_top1_idx]
        total_compatible_prob = float(probs[mask].sum())

        if raw_top1_is_incompatible and (raw_top1_conf >= self.incompatibility_threshold or total_compatible_prob < self.min_compatible_prob_mass):
            result = {
                "crop": crop_normalized,
                "crop_confidence": float(crop_confidence) if crop_confidence is not None else 1.0,
                "status": "uncertain",
                "disease": None,
                "disease_confidence": round(float(raw_top1_conf), 4),
                "incompatibility_flag": True,
                "incompatible_raw_prediction": raw_top1_class,
            }
            result["human_readable"] = format_human_readable(result)
            result["raw_prediction"] = raw_res
            return result

        # Compute masked and renormalized probabilities
        masked_probs = probs * mask
        total_masked_prob = masked_probs.sum()

        if total_masked_prob > 1e-6:
            renorm_probs = masked_probs / total_masked_prob
        else:
            renorm_probs = np.zeros(self.num_classes, dtype=float)
            renorm_probs[0] = 1.0

        healthy_prob = float(renorm_probs[0])

        # Find best disease candidate among compatible disease classes (indices 1..116)
        disease_indices = [i for i in range(1, self.num_classes) if mask[i]]
        if disease_indices:
            best_disease_idx = max(disease_indices, key=lambda i: renorm_probs[i])
            best_disease_prob = float(renorm_probs[best_disease_idx])
            best_disease_name = self.id_to_class[best_disease_idx]
        else:
            best_disease_idx = None
            best_disease_prob = 0.0
            best_disease_name = None

        # Standard Decision Logic
        # 1. Healthy: If healthy probability exceeds healthy threshold or exceeds disease candidate
        if healthy_prob >= self.healthy_threshold or (healthy_prob > best_disease_prob and healthy_prob >= self.uncertain_threshold):
            status = "healthy"
            disease = None
            disease_conf = healthy_prob
        # 2. Diseased: If confirmed disease candidate probability exceeds disease threshold
        elif best_disease_prob >= self.disease_threshold:
            status = "diseased"
            disease = best_disease_name
            disease_conf = best_disease_prob
        # 3. Uncertain: Low confidence on both healthy and disease
        else:
            status = "uncertain"
            disease = None
            disease_conf = max(healthy_prob, best_disease_prob)

        final_result = {
            "crop": crop_normalized,
            "crop_confidence": float(crop_confidence) if crop_confidence is not None else 1.0,
            "status": status,
            "disease": disease,
            "disease_confidence": round(float(disease_conf), 4),
        }
        final_result["human_readable"] = format_human_readable(final_result)
        final_result["healthy_probability"] = round(healthy_prob, 4)
        final_result["best_disease_probability"] = round(best_disease_prob, 4)
        final_result["best_disease_name"] = best_disease_name
        final_result["raw_prediction"] = raw_res

        return final_result

    def predict_pipeline(
        self,
        image_input: Union[str, Path, Image.Image, np.ndarray, bytes],
        crop_name: str,
        crop_confidence: float = 1.0,
    ) -> dict[str, Any]:
        """Alias for two-stage Model 1 -> Model 2 pipeline inference."""
        return self.predict_crop_aware(
            image_input=image_input,
            crop_name=crop_name,
            crop_confidence=crop_confidence,
        )


# Backward-compatible alias
Model2DiseaseClassifier = Model2DiseaseClassifierV2


def main():
    parser = argparse.ArgumentParser(description="Model 2 V2 Disease Classifier Inference")
    parser.add_argument("--image", type=str, required=True, help="Path to input image file")
    parser.add_argument("--crop", type=str, default=None, help="Optional Model 1 identified crop (e.g. Tomato, Cucumber)")
    parser.add_argument("--crop-conf", type=float, default=1.0, help="Confidence of Model 1 crop prediction")
    args = parser.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        print(f"Error: Image not found at {img_path}")
        return

    classifier = Model2DiseaseClassifierV2()
    result = classifier.predict_crop_aware(img_path, crop_name=args.crop, crop_confidence=args.crop_conf)

    print("\n==================================================")
    print("MODEL 2 V2 PREDICTION RESULT")
    print("==================================================")
    print(f"Standardized Result JSON:")
    print(json.dumps({
        "crop": result["crop"],
        "crop_confidence": result["crop_confidence"],
        "status": result["status"],
        "disease": result["disease"],
        "disease_confidence": result["disease_confidence"],
    }, indent=2))
    print("\nHuman-Readable Output:")
    print(result["human_readable"])
    print("==================================================")


if __name__ == "__main__":
    main()
