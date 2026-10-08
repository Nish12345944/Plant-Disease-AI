"""
Model 2 Disease Classifier V4 Inference Engine
===============================================
Provides raw classification inference, crop-disease compatibility filtering,
crop-aware probability masking, and the standardized inference contract for the Alexa Farms two-stage pipeline.

Output Contract:
----------------
{
    "crop": "tomato",
    "crop_confidence": 0.98,
    "status": "healthy" | "diseased" | "uncertain",
    "disease": "tomato__early_blight" | null,
    "disease_confidence": 0.95
}
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
MODEL_DIR_V4 = PROJECT_ROOT / "models" / "model2_classifier_v4"
DEFAULT_CHECKPOINT_PATH = MODEL_DIR_V4 / "best_model.pth"
DEFAULT_MAPPING_PATH = MODEL_DIR_V4 / "class_mapping.json"
DEFAULT_CONFIG_PATH = MODEL_DIR_V4 / "config.json"
CROP_DISEASE_MAP_PATH = PROJECT_ROOT / "data" / "processed" / "model2_organized_crop_disease_mapping.json"

if not DEFAULT_MAPPING_PATH.exists():
    DEFAULT_MAPPING_PATH = PROJECT_ROOT / "data" / "processed" / "model2_organized_class_mapping.json"
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

    if status == "diseased":
        disease_slug = result.get("disease")
        disease_display = format_disease_name_clean(disease_slug) or "Unspecified Disease"
        return f"Crop: {crop_display}\nDisease: {disease_display}\nStatus: Diseased"

    return f"Crop: {crop_display}\nStatus: Uncertain"


class Model2DiseaseClassifierV4:
    """Inference engine for Model 2 V4 Disease Classifier (EfficientNet-B2)."""

    def __init__(
        self,
        checkpoint_path: Optional[Union[str, Path]] = None,
        class_mapping_path: Optional[Union[str, Path]] = None,
        crop_disease_map_path: Optional[Union[str, Path]] = None,
        device: Optional[str] = None,
        uncertainty_threshold: float = 0.40,
        margin_threshold: float = 0.05,
    ):
        self.checkpoint_path = Path(checkpoint_path or DEFAULT_CHECKPOINT_PATH)
        self.class_mapping_path = Path(class_mapping_path or DEFAULT_MAPPING_PATH)
        self.crop_disease_map_path = Path(crop_disease_map_path or CROP_DISEASE_MAP_PATH)
        self.uncertainty_threshold = uncertainty_threshold
        self.margin_threshold = margin_threshold

        if device:
            self.device = torch.device(device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.class_to_id: dict[str, int] = {}
        self.id_to_class: dict[int, str] = {}
        self.num_classes: int = 117
        self.crop_disease_map: dict[str, list[str]] = {}

        self._load_taxonomy()
        self.model = self._load_model()
        self.transform = self._get_transform()
        logger.info(f"Initialized Model 2 V4 ({self.num_classes} classes) from {self.checkpoint_path}")

    def _load_taxonomy(self):
        if not self.class_mapping_path.exists():
            raise FileNotFoundError(f"Class mapping file not found at: {self.class_mapping_path}")

        with open(self.class_mapping_path, "r", encoding="utf-8") as f:
            raw_map = json.load(f)

        if "class_to_id" in raw_map:
            self.class_to_id = {k: int(v) for k, v in raw_map["class_to_id"].items()}
        else:
            self.class_to_id = {k: int(v) for k, v in raw_map.items()}

        self.id_to_class = {v: k for k, v in self.class_to_id.items()}
        self.num_classes = len(self.class_to_id)

        if self.crop_disease_map_path.exists():
            with open(self.crop_disease_map_path, "r", encoding="utf-8") as f:
                self.crop_disease_map = json.load(f)

    def _get_transform(self):
        return transforms.Compose([
            transforms.Resize(DEFAULT_IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])

    def _load_model(self) -> nn.Module:
        model = efficientnet_b2(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(in_features, self.num_classes),
        )

        if not self.checkpoint_path.exists():
            raise FileNotFoundError(f"Model checkpoint not found at: {self.checkpoint_path}")

        ckpt = torch.load(self.checkpoint_path, map_location="cpu", weights_only=False)
        state_dict = ckpt.get("model_state_dict", ckpt)
        model.load_state_dict(state_dict)
        model.to(self.device)
        model.eval()
        return model

    def is_compatible(self, crop: Optional[str], disease_slug: Optional[str]) -> bool:
        """Verify biological compatibility between crop and disease."""
        if not disease_slug or disease_slug.lower() == "healthy":
            return True
        if not crop:
            return True

        crop_clean = crop.lower().strip()
        disease_clean = disease_slug.lower().strip()

        # Direct crop prefix match
        if disease_clean.startswith(f"{crop_clean}__"):
            return True

        # Normalized aliases
        aliases = {
            "french_bean": "bean",
            "bean": "french_bean",
            "capsicum": "bell_pepper",
            "cherry_tomato": "tomato",
        }
        alt_crop = aliases.get(crop_clean)
        if alt_crop and disease_clean.startswith(f"{alt_crop}__"):
            return True

        # Check registered mapping
        if crop_clean in self.crop_disease_map and disease_clean in self.crop_disease_map[crop_clean]:
            return True
        if alt_crop and alt_crop in self.crop_disease_map and disease_clean in self.crop_disease_map[alt_crop]:
            return True

        return False

    def predict_raw(self, pil_img: Image.Image) -> tuple[np.ndarray, list[dict[str, Any]]]:
        """Compute unconstrained 117-class probability distribution."""
        tensor = self.transform(pil_img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()

        sorted_indices = np.argsort(probs)[::-1]
        top_classes = [
            {
                "class_id": int(i),
                "class_name": self.id_to_class[int(i)],
                "probability": float(probs[i]),
                "percentage": f"{probs[i] * 100:.2f}%",
            }
            for i in sorted_indices
        ]
        return probs, top_classes

    def predict_crop_aware(
        self,
        image_input: Union[str, Path, Image.Image, bytes],
        crop_name: Optional[str] = None,
        crop_confidence: Optional[float] = None,
    ) -> dict[str, Any]:
        """Run crop-conditioned inference with probability masking and compatibility enforcement."""
        if isinstance(image_input, (str, Path)):
            img = Image.open(image_input).convert("RGB")
        elif isinstance(image_input, bytes):
            img = Image.open(io.BytesIO(image_input)).convert("RGB")
        elif isinstance(image_input, Image.Image):
            img = image_input.convert("RGB")
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")

        probs, all_ranked = self.predict_raw(img)

        norm_crop = crop_name.lower().strip() if crop_name else None

        # Filter candidates by compatibility
        compatible_ranked = [
            c for c in all_ranked
            if self.is_compatible(norm_crop, c["class_name"])
        ]

        raw_top1 = all_ranked[0]
        is_raw_compatible = self.is_compatible(norm_crop, raw_top1["class_name"])

        # Default fallback
        final_status = "uncertain"
        final_disease = None
        final_disease_conf = 0.0

        if compatible_ranked:
            best_compat = compatible_ranked[0]
            cand_name = best_compat["class_name"]
            cand_conf = best_compat["probability"]
            final_disease_conf = cand_conf

            # Healthy case
            if cand_name == "healthy":
                if cand_conf >= self.uncertainty_threshold:
                    final_status = "healthy"
                    final_disease = None
                else:
                    final_status = "uncertain"
                    final_disease = None
            else:
                # Disease case
                if cand_conf >= self.uncertainty_threshold:
                    final_status = "diseased"
                    final_disease = cand_name
                else:
                    final_status = "uncertain"
                    final_disease = None
        else:
            final_status = "uncertain"
            final_disease = None

        result = {
            "crop": norm_crop,
            "crop_confidence": round(float(crop_confidence), 4) if crop_confidence is not None else None,
            "status": final_status,
            "disease": final_disease,
            "disease_confidence": round(float(final_disease_conf), 4),
            "raw_top1": {
                "class_name": raw_top1["class_name"],
                "confidence": round(raw_top1["probability"], 4),
                "is_compatible": is_raw_compatible,
            },
            "top_compatible": compatible_ranked[:5],
            "raw_top10": all_ranked[:10],
        }
        result["human_readable"] = format_human_readable(result)
        return result

    def predict_image(
        self,
        image_input: Union[str, Path, Image.Image, bytes],
        crop_context: Optional[str] = None,
        crop_confidence: Optional[float] = None,
    ) -> dict[str, Any]:
        """Convenience alias conforming to standard pipeline interface."""
        return self.predict_crop_aware(
            image_input=image_input,
            crop_name=crop_context,
            crop_confidence=crop_confidence,
        )


def main():
    parser = argparse.ArgumentParser(description="Model 2 V4 Disease Classifier CLI")
    parser.add_argument("image_path", type=str, help="Path to leaf image")
    parser.add_argument("--crop", type=str, default=None, help="Conditioning crop name from Model 1")
    parser.add_argument("--crop-conf", type=float, default=0.95, help="Confidence of Model 1 crop prediction")
    args = parser.parse_args()

    classifier = Model2DiseaseClassifierV4()
    res = classifier.predict_crop_aware(args.image_path, crop_name=args.crop, crop_confidence=args.crop_conf)
    print(json.dumps(res, indent=2))
    print("\nHuman-Readable Output:")
    print(res["human_readable"])


if __name__ == "__main__":
    main()
