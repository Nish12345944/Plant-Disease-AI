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
import os
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
PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", str(Path(__file__).resolve().parent.parent.parent))).resolve()
MODEL_DIR_V4 = Path(__file__).resolve().parent
MODEL2_RETRAINED_V3_DIR = PROJECT_ROOT / "models" / "model2_retrained_v3"
MODEL2_RETRAINING_V2_DIR = PROJECT_ROOT / "models" / "model2_retraining_v2"

DEFAULT_CHECKPOINT_PATH = Path(
    os.environ.get(
        "MODEL2_CHECKPOINT",
        str(MODEL2_RETRAINED_V3_DIR / "best_model.pth" if (MODEL2_RETRAINED_V3_DIR / "best_model.pth").exists() else (MODEL2_RETRAINING_V2_DIR / "best_model.pth" if (MODEL2_RETRAINING_V2_DIR / "best_model.pth").exists() else MODEL_DIR_V4 / "best_model.pth")),
    )
)
DEFAULT_MAPPING_PATH = Path(
    os.environ.get(
        "MODEL2_CLASS_MAPPING",
        str(MODEL2_RETRAINED_V3_DIR / "class_mapping.json" if (MODEL2_RETRAINED_V3_DIR / "class_mapping.json").exists() else (MODEL2_RETRAINING_V2_DIR / "class_mapping.json" if (MODEL2_RETRAINING_V2_DIR / "class_mapping.json").exists() else MODEL_DIR_V4 / "class_mapping.json")),
    )
)
DEFAULT_CONFIG_PATH = Path(
    os.environ.get(
        "MODEL2_CONFIG",
        str(MODEL2_RETRAINED_V3_DIR / "config.json" if (MODEL2_RETRAINED_V3_DIR / "config.json").exists() else (MODEL2_RETRAINING_V2_DIR / "config.json" if (MODEL2_RETRAINING_V2_DIR / "config.json").exists() else MODEL_DIR_V4 / "config.json")),
    )
)
CROP_DISEASE_MAP_PATH = Path(
    os.environ.get(
        "CROP_DISEASE_MAPPING",
        str(MODEL2_RETRAINED_V3_DIR / "crop_disease_mapping.json" if (MODEL2_RETRAINED_V3_DIR / "crop_disease_mapping.json").exists() else (MODEL2_RETRAINING_V2_DIR / "crop_disease_mapping.json" if (MODEL2_RETRAINING_V2_DIR / "crop_disease_mapping.json").exists() else PROJECT_ROOT / "data" / "processed" / "model2_organized_crop_disease_mapping.json")),
    )
)

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
DEFAULT_IMAGE_SIZE = (260, 260)

# 36 disease classes with zero test support in the immutable evaluation benchmark
# (28 legacy classes from V2 plus 8 newly added V3 classes).
# Safeguards ensure these classes cannot falsely override healthy foliage predictions,
# cannot trigger on incompatible crops, and require high calibrated confidence (>= 0.70)
# for provisional detection.
ZERO_TEST_SUPPORT_CLASSES: set[str] = {
    # 28 legacy zero-test-support classes
    "bell_pepper__leaf_curl",
    "blueberry__exobasidium",
    "blueberry__septoria_leaf_spot",
    "cauliflower__black_rot",
    "cauliflower__downy_mildew",
    "cauliflower__pest_damage",
    "coffee__black_rot",
    "eggplant__mosaic_virus",
    "eggplant__pest_damage",
    "eggplant__wilt_disease",
    "ginger__leaf_blight",
    "ginger__pest_damage",
    "plum__shot_hole",
    "rose__black_spot",
    "rose__downy_mildew",
    "rose__mosaic_virus",
    "rose__pest_damage",
    "rose__powdery_mildew",
    "rose__rust",
    "spinach__anthracnose",
    "spinach__bacterial_spot",
    "spinach__downy_mildew",
    "spinach__pest_damage",
    "strawberry__angular_leaf_spot",
    "strawberry__gray_mold",
    "strawberry__leaf_spot",
    "strawberry__powdery_mildew",
    "tomato__anthracnose",
    # 8 newly added V3 zero-test-support classes
    "cauliflower__alternaria_brassicae",
    "cauliflower__black_spot",
    "cucumber__anthracnose",
    "cucumber__belly_rot",
    "cucumber__downy_mildew",
    "cucumber__gummy_stem_blight",
    "cucumber__pythium_fruit_rot",
    "tomato__fruit_fusarium",
}


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
    crop_display = result.get("crop_display")
    if not crop_display:
        crop_str = result.get("crop")
        if not crop_str or str(crop_str).lower() in ("unknown", "none"):
            crop_display = "Unknown Crop"
        elif str(crop_str).lower() in ("bellpepper", "capsicum", "bell_pepper"):
            crop_display = "Bell Pepper"
        else:
            crop_display = str(crop_str).replace("_", " ").title()

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
        temperature: Optional[float] = None,
    ):
        self.checkpoint_path = Path(checkpoint_path or DEFAULT_CHECKPOINT_PATH)
        self.class_mapping_path = Path(class_mapping_path or DEFAULT_MAPPING_PATH)
        self.crop_disease_map_path = Path(crop_disease_map_path or CROP_DISEASE_MAP_PATH)
        self.uncertainty_threshold = float(os.environ.get("MODEL2_UNCERTAINTY_THRESHOLD", str(uncertainty_threshold)))
        self.margin_threshold = float(os.environ.get("MODEL2_MARGIN_THRESHOLD", str(margin_threshold)))
        self.temperature = float(os.environ.get("MODEL2_TEMPERATURE", str(temperature if temperature is not None else 0.9188)))
        self.zero_support_threshold = float(os.environ.get("ZERO_SUPPORT_THRESHOLD", "0.70"))

        if device:
            self.device = torch.device(device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.class_to_id: dict[str, int] = {}
        self.id_to_class: dict[int, str] = {}
        self.num_classes: int = 144
        self.crop_disease_map: dict[str, list[str]] = {}
        self.zero_support_classes: set[str] = set(ZERO_TEST_SUPPORT_CLASSES)

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
        else:
            logger.warning(f"Crop-disease map file not found at: {self.crop_disease_map_path}")
            self.crop_disease_map = {}

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

    @staticmethod
    def normalize_crop_key(crop: Optional[str]) -> Optional[str]:
        """Normalize crop identifier to taxonomy crop key (matching crop_disease_mapping.json).

        Maps canonical and legacy aliases:
          'bellpepper', 'capsicum', 'bell_pepper' -> 'bell_pepper'
          'french_bean', 'bean' -> 'bean'
          'cherry_tomato', 'tomato' -> 'tomato'
        Leaves others in lowercase format. Note that 'zucchini', 'cucumber', and 'squash'
        are distinct taxonomy crops and are NEVER cross-aliased.
        """
        if not crop:
            return None
        c = str(crop).strip().lower().replace(" ", "_")
        if c in ("unknown", "none", "no_plant", "unidentified", "blurry"):
            return None
        aliases = {
            "bellpepper": "bell_pepper",
            "capsicum": "bell_pepper",
            "french_bean": "bean",
            "cherry_tomato": "tomato",
        }
        return aliases.get(c, c)

    @staticmethod
    def get_canonical_crop_id(crop: Optional[str]) -> str:
        """Return canonical internal crop ID ('bellpepper' for bell pepper)."""
        if not crop:
            return "unknown"
        c = str(crop).strip().lower().replace(" ", "_")
        if c in ("capsicum", "bell_pepper", "bellpepper"):
            return "bellpepper"
        if c in ("bean", "french_bean"):
            return "french_bean"
        if c in ("tomato", "cherry_tomato"):
            return "tomato" if c == "tomato" else "cherry_tomato"
        return c

    @staticmethod
    def get_crop_display_label(crop: Optional[str]) -> str:
        """Return user-facing crop label ('Bell Pepper' for bell pepper, never 'Capsicum')."""
        if not crop:
            return "Unknown Crop"
        canonical = Model2DiseaseClassifierV4.get_canonical_crop_id(crop)
        display_map = {
            "bellpepper": "Bell Pepper",
            "french_bean": "French Bean",
            "cherry_tomato": "Cherry Tomato",
        }
        return display_map.get(canonical, canonical.replace("_", " ").title())

    def is_compatible(self, crop: Optional[str], disease_slug: Optional[str]) -> bool:
        """Verify biological compatibility between crop and candidate disease class.

        Strict rules:
        - If crop is None, unknown, or blurry: no disease/healthy is compatible (returns False).
        - If crop is not registered in self.crop_disease_map:
            no class (including 'healthy') is compatible (returns False).
        - If disease_slug is None or 'healthy':
            compatible ONLY if crop is registered in self.crop_disease_map.
        - For specific diseases:
            must belong strictly to the normalized crop's registered diseases in self.crop_disease_map.
            Cross-crop contamination (e.g. cucumber <-> zucchini) is strictly prohibited.
        """
        if not crop:
            return False

        norm_crop = self.normalize_crop_key(crop)
        if not norm_crop or norm_crop not in self.crop_disease_map:
            return False

        if not disease_slug or disease_slug.lower().strip() == "healthy":
            # Crop is registered in taxonomy, so healthy foliage / absence of disease is compatible
            return True

        slug_clean = disease_slug.lower().strip()

        # Candidate disease must belong strictly to this crop
        expected_prefix = f"{norm_crop}__"
        if not slug_clean.startswith(expected_prefix):
            return False

        disease_short = slug_clean[len(expected_prefix):]
        permitted = self.crop_disease_map.get(norm_crop, [])
        return (slug_clean in permitted) or (disease_short in permitted)

    def predict_raw(self, pil_img: Image.Image) -> tuple[np.ndarray, list[dict[str, Any]]]:
        """Compute unconstrained probability distribution with calibrated temperature."""
        tensor = self.transform(pil_img).unsqueeze(0).to(self.device)
        with torch.inference_mode():
            logits = self.model(tensor)
            if hasattr(self, "temperature") and self.temperature and self.temperature > 0:
                scaled_logits = logits / self.temperature
            else:
                scaled_logits = logits
            probs = torch.softmax(scaled_logits, dim=1).squeeze(0).cpu().numpy()

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
        raw_top1 = all_ranked[0] if all_ranked else None

        norm_crop = self.normalize_crop_key(crop_name)
        canonical_crop_id = self.get_canonical_crop_id(crop_name) if norm_crop else None
        crop_display = self.get_crop_display_label(crop_name) if norm_crop else "Unknown Crop"

        is_unknown_crop = norm_crop is None
        is_low_conf = crop_confidence is not None and crop_confidence < 0.25
        is_crop_in_taxonomy = bool(norm_crop and norm_crop in self.crop_disease_map)

        # Guard: Unknown crop or low-confidence crop -> no disease inference based on guessed crop
        if is_unknown_crop or is_low_conf:
            result = {
                "crop": canonical_crop_id,
                "crop_display": crop_display if not is_unknown_crop else "Unknown Crop",
                "crop_confidence": round(float(crop_confidence), 4) if crop_confidence is not None else None,
                "status": "uncertain",
                "disease": None,
                "disease_confidence": 0.0,
                "raw_top1": {
                    "class_name": raw_top1["class_name"] if raw_top1 else "none",
                    "confidence": round(raw_top1["probability"], 4) if raw_top1 else 0.0,
                    "is_compatible": False,
                } if raw_top1 else None,
                "top_compatible": [],
                "raw_top10": all_ranked[:10] if all_ranked else [],
                "message": (
                    "Crop identity uncertain or below confidence threshold; disease inference skipped."
                    if is_low_conf
                    else "Crop unidentified; cannot infer disease."
                ),
            }
            result["human_readable"] = format_human_readable(result)
            return result

        # Guard: Crop not registered in taxonomy (missing crop mapping) -> fail safely as uncertain
        if not is_crop_in_taxonomy:
            result = {
                "crop": canonical_crop_id,
                "crop_display": crop_display,
                "crop_confidence": round(float(crop_confidence), 4) if crop_confidence is not None else None,
                "status": "uncertain",
                "disease": None,
                "disease_confidence": 0.0,
                "raw_top1": {
                    "class_name": raw_top1["class_name"] if raw_top1 else "none",
                    "confidence": round(raw_top1["probability"], 4) if raw_top1 else 0.0,
                    "is_compatible": False,
                } if raw_top1 else None,
                "top_compatible": [],
                "raw_top10": all_ranked[:10] if all_ranked else [],
                "message": f"Crop '{crop_display}' is not registered in the disease taxonomy.",
            }
            result["human_readable"] = format_human_readable(result)
            return result

        # Filter candidates strictly by compatibility BEFORE ranking/selecting predictions
        compatible_ranked = [
            c.copy() for c in all_ranked
            if self.is_compatible(norm_crop, c["class_name"])
        ]

        is_raw_compatible = self.is_compatible(norm_crop, raw_top1["class_name"]) if raw_top1 else False

        # Compute crop-conditioned normalized probabilities over the compatible space
        compat_mass = sum(c["probability"] for c in compatible_ranked)

        # When compatible candidates carry meaningful probability mass (compat_mass >= 0.20),
        # compute normalized crop-aware probabilities so cross-crop logits do not dilute valid predictions.
        if compat_mass >= 0.20 and compatible_ranked:
            for c in compatible_ranked:
                c["crop_aware_probability"] = c["probability"] / compat_mass
                c["crop_aware_percentage"] = f"{c['crop_aware_probability'] * 100:.2f}%"
        else:
            for c in compatible_ranked:
                c["crop_aware_probability"] = c["probability"]
                c["crop_aware_percentage"] = c["percentage"]

        # Evaluation of compatible candidates with general prediction-reliability policy
        if compatible_ranked and compat_mass >= 0.20:
            best_compat = compatible_ranked[0]
            cand_name = best_compat["class_name"]
            cand_conf = float(best_compat.get("crop_aware_probability", best_compat["probability"]))

            second_compat = compatible_ranked[1] if len(compatible_ranked) > 1 else None
            second_cand_name = second_compat["class_name"] if second_compat else None
            second_cand_conf = float(second_compat.get("crop_aware_probability", second_compat["probability"])) if second_compat else 0.0
            margin = cand_conf - second_cand_conf

            # Retrieve compatible healthy candidate probability if available
            healthy_cands = [c for c in compatible_ranked if c["class_name"] == "healthy"]
            healthy_prob = float(healthy_cands[0].get("crop_aware_probability", healthy_cands[0]["probability"])) if healthy_cands else 0.0

            # General Reliability Policy:
            # 1. Competing prediction ambiguity: if margin between top-2 candidates < margin_threshold
            is_narrow_margin = (second_compat is not None) and (margin < self.margin_threshold)

            # 2. Decision confidence threshold
            is_sub_threshold = (cand_conf < self.uncertainty_threshold)

            if cand_name in self.zero_support_classes:
                # Safeguard against unverified zero-test-support disease classes:
                # 1. Healthy foliage protection: if healthy probability is >= 0.10, healthy takes precedence or forces uncertain.
                # 2. Documented explicit policy: if healthy probability is < 0.10 and cand_conf >= zero_support_threshold (0.70),
                #    and prediction is decisive (not narrow margin), the disease is provisionally diagnosed.
                # 3. Otherwise, safely hold as uncertain.
                if healthy_prob >= 0.10:
                    if healthy_prob >= self.uncertainty_threshold and not is_narrow_margin:
                        final_status = "healthy"
                        final_disease = None
                        final_disease_conf = healthy_prob
                    else:
                        final_status = "uncertain"
                        final_disease = None
                        final_disease_conf = healthy_prob
                elif cand_conf >= self.zero_support_threshold and not is_narrow_margin:
                    final_status = "diseased"
                    final_disease = cand_name
                    final_disease_conf = cand_conf
                else:
                    final_status = "uncertain"
                    final_disease = None
                    final_disease_conf = cand_conf
            elif cand_name == "healthy":
                if not is_sub_threshold and not is_narrow_margin:
                    final_status = "healthy"
                    final_disease = None
                    final_disease_conf = cand_conf
                else:
                    final_status = "uncertain"
                    final_disease = None
                    final_disease_conf = cand_conf
                    if raw_top1 and raw_top1["probability"] > cand_conf:
                        final_disease_conf = float(raw_top1["probability"])
            else:
                # Standard disease candidate with test support:
                # Universal healthy shielding: if healthy probability closely competes with disease
                # candidate (healthy_prob >= 0.35 and cand_conf - healthy_prob < self.margin_threshold),
                # do not trigger a false disease alarm; hold as uncertain.
                is_healthy_competing = (healthy_prob >= 0.35) and ((cand_conf - healthy_prob) < self.margin_threshold)

                if is_sub_threshold or is_narrow_margin or is_healthy_competing:
                    final_status = "uncertain"
                    final_disease = None
                    final_disease_conf = cand_conf
                    if raw_top1 and raw_top1["probability"] > cand_conf:
                        final_disease_conf = float(raw_top1["probability"])
                else:
                    final_status = "diseased"
                    final_disease = cand_name
                    final_disease_conf = cand_conf
        else:
            final_status = "uncertain"
            final_disease = None
            final_disease_conf = float(raw_top1["probability"]) if raw_top1 else 0.0

        result = {
            "crop": canonical_crop_id,
            "crop_display": crop_display,
            "crop_confidence": round(float(crop_confidence), 4) if crop_confidence is not None else None,
            "status": final_status,
            "disease": final_disease,
            "disease_confidence": round(float(final_disease_conf), 4),
            "raw_top1": {
                "class_name": raw_top1["class_name"] if raw_top1 else "none",
                "confidence": round(raw_top1["probability"], 4) if raw_top1 else 0.0,
                "is_compatible": is_raw_compatible,
            } if raw_top1 else None,
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
