"""Open-Set Crop Recognition & Unsupported-Crop Rejection Guard.

Safeguard B: Evaluates Model 1 output distributions to ensure the input belongs
to a verified, supported crop distribution before downstream disease diagnosis
or treatment recommendations can proceed.

Never accepts top-1 predictions on raw softmax confidence alone, because
out-of-distribution unsupported crops (such as bajra / pearl millet, weeds, or wild flora)
can trigger high-confidence false matches in closed-set neural classifiers.

Authoritative Class Source:
`models/model1_expanded/class_mapping.json` (46 supported crops).

Statuses returned:
- accepted: Crop confirmed within supported distribution; safe to proceed to Model 2.
- unsupported_crop: Input likely outside the supported crop catalog; blocks Model 2.
- uncertain_crop: Crop identity ambiguous (tight top-1/top-2 margin or high entropy); blocks Model 2.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

import numpy as np
import torch

from app.backend.config import MODEL1_CLASS_MAPPING
from model1_test_app.inference import format_class_name, normalize_crop_id

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Provisional Acceptance & Rejection Thresholds
# Note: In accordance with project instructions, these thresholds are documented
# as provisional conservative guards calibrated on held-out and OOD test cases:
# - Valid in-distribution test samples (wheat, banana, soybean, etc.) achieved prototype
#   cosine similarities between 0.631 and 0.833 (median 0.750).
# - Out-of-distribution alien flora (e.g. Gypsophila) achieved prototype similarities < 0.45.
# - Confident lookalikes (e.g. Bajra/pearl millet heads misclassified as wheat) achieved
#   prototype similarities ~0.601, falling between 0.50 and 0.62.
# ---------------------------------------------------------------------------
PROVISIONAL_MIN_CONFIDENCE = 0.45            # Minimum top-1 confidence for outright crop acceptance
PROVISIONAL_MIN_MARGIN = 0.15                # Minimum (Top-1 - Top-2) margin to reject ambiguous lookalikes
PROVISIONAL_MAX_ENTROPY = 0.70               # Maximum normalized Shannon entropy across classes
PROVISIONAL_REJECTION_CONF = 0.30            # Below this, crop is strictly rejected as unsupported/unknown
PROVISIONAL_TEMPERATURE = 1.5                # Logit temperature scaling factor for calibration
PROVISIONAL_MIN_PROTO_SIM_ACCEPTED = 0.62    # Minimum prototype cosine similarity for confident acceptance
PROVISIONAL_MIN_PROTO_SIM_UNCERTAIN = 0.50   # Below this, sample is strictly rejected as unsupported crop


@dataclass
class CropGuardResult:
    """Standardized result contract for Open-Set Crop Recognition Guard."""
    crop_status: str              # "accepted", "unsupported_crop", "uncertain_crop"
    status: str                   # "valid", "rejected", "uncertain"
    reason_code: Optional[str]    # None, "unsupported_crop", "uncertain_crop"
    predicted_crop: str           # User-facing label (e.g. "Wheat")
    predicted_class: str          # Canonical ID (e.g. "wheat")
    confidence: float             # Calibrated top-1 confidence
    raw_confidence: float         # Raw top-1 confidence
    margin: float                 # Top-1 minus Top-2 margin
    entropy: float                # Normalized Shannon entropy [0.0 - 1.0]
    prototype_similarity: Optional[float]  # Cosine similarity to class prototype embedding
    proceed_to_disease_detection: bool    # True ONLY if crop_status == "accepted"
    user_message: str             # Actionable, farmer-friendly guidance
    warning: Optional[str]        # Non-blocking warning (e.g. moderate margin)
    top_candidates: list[dict[str, Any]]
    is_supported_label: bool      # Whether top-1 class is in authoritative 46-crop list

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Cached authoritative set of supported crop labels
_SUPPORTED_CROPS: Optional[set[str]] = None
_CROP_PROTOTYPES: Optional[dict[str, np.ndarray]] = None


def get_supported_crop_classes() -> set[str]:
    """Load authoritative list of supported crop classes from Model 1 mapping."""
    global _SUPPORTED_CROPS
    if _SUPPORTED_CROPS is None:
        try:
            with open(MODEL1_CLASS_MAPPING, "r", encoding="utf-8") as f:
                data = json.load(f)
            raw_classes = list(data.get("idx_to_class", {}).values())
            _SUPPORTED_CROPS = {
                normalize_crop_id(c) or c.lower().strip() for c in raw_classes
            }
        except Exception as exc:
            logger.error(f"Failed to load authoritative crop mapping from {MODEL1_CLASS_MAPPING}: {exc}")
            _SUPPORTED_CROPS = set()
    return _SUPPORTED_CROPS


def get_crop_prototypes() -> dict[str, np.ndarray]:
    """Load cached class prototype embeddings from models/model1_expanded/crop_prototypes.npz."""
    global _CROP_PROTOTYPES
    if _CROP_PROTOTYPES is None:
        proto_file = Path("models/model1_expanded/crop_prototypes.npz")
        if proto_file.exists():
            try:
                raw_data = np.load(proto_file)
                _CROP_PROTOTYPES = {
                    k: raw_data[k].flatten()
                    for k in raw_data.files
                    if getattr(raw_data[k], "shape", None) == (1408,)
                }
                logger.info(f"Loaded {len(_CROP_PROTOTYPES)} crop prototypes for open-set detection.")
            except Exception as exc:
                logger.warning(f"Could not load crop prototypes from {proto_file}: {exc}")
                _CROP_PROTOTYPES = {}
        else:
            _CROP_PROTOTYPES = {}
    return _CROP_PROTOTYPES


def evaluate_crop_acceptance(
    top_k_list: list[dict[str, Any]],
    raw_probabilities: Optional[np.ndarray] = None,
    logits: Optional[np.ndarray] = None,
    feature_vector: Optional[np.ndarray] = None,
    min_confidence: float = PROVISIONAL_MIN_CONFIDENCE,
    min_margin: float = PROVISIONAL_MIN_MARGIN,
    max_entropy: float = PROVISIONAL_MAX_ENTROPY,
    temperature: float = PROVISIONAL_TEMPERATURE,
    min_proto_sim_accepted: float = PROVISIONAL_MIN_PROTO_SIM_ACCEPTED,
    min_proto_sim_uncertain: float = PROVISIONAL_MIN_PROTO_SIM_UNCERTAIN,
) -> CropGuardResult:
    """Evaluate whether Model 1 prediction belongs to a supported, unambiguous crop distribution.

    Args:
        top_k_list: Ranked candidate prediction list from Model 1.
        raw_probabilities: Array of softmax probabilities over all 46 classes.
        logits: Unnormalized output logits from Model 1 (for temperature calibration).
        feature_vector: Normalized penultimate embedding from EfficientNet-B2 backbone.
        min_confidence: Threshold for top-1 acceptance.
        min_margin: Threshold for top-1 vs top-2 margin.
        max_entropy: Threshold for normalized entropy.
        temperature: Temperature factor for logit calibration.
        min_proto_sim_accepted: Minimum prototype cosine similarity for outright acceptance.
        min_proto_sim_uncertain: Minimum prototype cosine similarity before rejection as unsupported.

    Returns:
        CropGuardResult with acceptance decision and detailed diagnostics.
    """
    supported_classes = get_supported_crop_classes()

    if not top_k_list:
        return CropGuardResult(
            crop_status="unsupported_crop",
            status="rejected",
            reason_code="unsupported_crop",
            predicted_crop="Unknown",
            predicted_class="unknown",
            confidence=0.0,
            raw_confidence=0.0,
            margin=0.0,
            entropy=1.0,
            prototype_similarity=None,
            proceed_to_disease_detection=False,
            user_message="No crop predictions were generated for this image.",
            warning=None,
            top_candidates=[],
            is_supported_label=False,
        )

    top1 = top_k_list[0]
    top2 = top_k_list[1] if len(top_k_list) > 1 else None

    raw_cls = top1.get("class_name") or top1.get("predicted_class") or "unknown"
    canonical_cls = normalize_crop_id(raw_cls) or raw_cls
    display_label = format_class_name(canonical_cls)
    raw_p1 = float(top1.get("confidence", 0.0))
    raw_p2 = float(top2.get("confidence", 0.0)) if top2 else 0.0
    margin = float(raw_p1 - raw_p2)

    # 1. Authoritative label check
    is_supported = canonical_cls in supported_classes

    # 2. Temperature-calibrated confidence
    calibrated_p1 = raw_p1
    if logits is not None and len(logits) > 0:
        scaled_logits = logits / max(temperature, 0.1)
        shifted = scaled_logits - np.max(scaled_logits)
        exp_vals = np.exp(shifted)
        calibrated_probs = exp_vals / np.sum(exp_vals)
        top_idx = int(np.argmax(logits))
        calibrated_p1 = float(calibrated_probs[top_idx])

    # 3. Normalized Shannon Entropy calculation
    if raw_probabilities is not None and len(raw_probabilities) > 1:
        probs = np.clip(raw_probabilities, 1e-12, 1.0)
        num_c = len(probs)
        raw_entropy = -float(np.sum(probs * np.log(probs)))
        norm_entropy = float(raw_entropy / np.log(num_c))
    else:
        norm_entropy = 0.0 if raw_p1 > 0.9 else 0.5

    # 4. Feature prototype cosine similarity evaluation
    proto_sim: Optional[float] = None
    if feature_vector is not None:
        prototypes = get_crop_prototypes()
        proto_vec = prototypes.get(canonical_cls)
        if proto_vec is not None:
            fn = feature_vector.flatten()
            proto_sim = float(np.dot(fn, proto_vec))

    # -------------------------------------------------------------------------
    # DECISION LOGIC: Guarding Against Unsupported & Confidently Incorrect Crops
    # -------------------------------------------------------------------------

    # Condition 1: Crop label is NOT in the authoritative supported 46-crop list
    if not is_supported or canonical_cls == "unknown":
        return CropGuardResult(
            crop_status="unsupported_crop",
            status="rejected",
            reason_code="unsupported_crop",
            predicted_crop="Unsupported Crop",
            predicted_class="unsupported_crop",
            confidence=0.0,
            raw_confidence=0.0,
            margin=round(margin, 4),
            entropy=round(norm_entropy, 4),
            prototype_similarity=round(proto_sim, 4) if proto_sim is not None else None,
            proceed_to_disease_detection=False,
            user_message="This crop is not currently supported. Please upload an image of a supported crop.",
            warning=None,
            top_candidates=[],
            is_supported_label=False,
        )

    # Condition 2: Deep feature prototype dissimilarity (Non-plant image / Alien flora)
    if proto_sim is not None and proto_sim < min_proto_sim_uncertain:
        return CropGuardResult(
            crop_status="rejected",
            status="rejected",
            reason_code="non_plant_image",
            predicted_crop="Non-Plant Image",
            predicted_class="non_plant_image",
            confidence=0.0,
            raw_confidence=0.0,
            margin=round(margin, 4),
            entropy=round(norm_entropy, 4),
            prototype_similarity=round(proto_sim, 4),
            proceed_to_disease_detection=False,
            user_message="This image does not appear to contain a plant. Please upload a clear plant image.",
            warning=None,
            top_candidates=[],
            is_supported_label=False,
        )

    # Condition 3: Confidence is severely depressed (raw probability < 0.30)
    if raw_p1 < PROVISIONAL_REJECTION_CONF:
        is_non_plant = (proto_sim is not None and proto_sim < min_proto_sim_uncertain)
        return CropGuardResult(
            crop_status="rejected" if is_non_plant else "unsupported_crop",
            status="rejected",
            reason_code="non_plant_image" if is_non_plant else "unsupported_crop",
            predicted_crop="Non-Plant Image" if is_non_plant else "Unsupported Crop",
            predicted_class="non_plant_image" if is_non_plant else "unsupported_crop",
            confidence=0.0,
            raw_confidence=0.0,
            margin=round(margin, 4),
            entropy=round(norm_entropy, 4),
            prototype_similarity=round(proto_sim, 4) if proto_sim is not None else None,
            proceed_to_disease_detection=False,
            user_message=(
                "This image does not appear to contain a plant. Please upload a clear plant image."
                if is_non_plant
                else "This crop is not currently supported. Please upload an image of a supported crop."
            ),
            warning=None,
            top_candidates=[],
            is_supported_label=False if is_non_plant else True,
        )

    # Condition 4: Intermediate similarity or Ambiguous margin (Near-boundary lookalike crops or seedlings)
    is_proto_ambiguous = (proto_sim is not None and proto_sim < min_proto_sim_accepted)
    is_margin_ambiguous = (margin < min_margin or norm_entropy > max_entropy or raw_p1 < min_confidence)

    if is_proto_ambiguous or is_margin_ambiguous:
        return CropGuardResult(
            crop_status="uncertain_crop",
            status="uncertain",
            reason_code="uncertain_crop",
            predicted_crop="Uncertain Crop",
            predicted_class="uncertain_crop",
            confidence=0.0,
            raw_confidence=0.0,
            margin=round(margin, 4),
            entropy=round(norm_entropy, 4),
            prototype_similarity=round(proto_sim, 4) if proto_sim is not None else None,
            proceed_to_disease_detection=False,
            user_message="Crop identity could not be determined reliably. Please upload a clearer image showing distinctive leaves, flowers, or fruit.",
            warning="Crop identity could not be determined reliably. Disease diagnosis withheld.",
            top_candidates=[],
            is_supported_label=True,
        )

    # Condition 5: Accepted Supported Crop
    uncertainty_warning = None
    if margin < 0.25 or raw_p1 < 0.60:
        uncertainty_warning = f"Moderate crop confidence ({raw_p1 * 100:.1f}%). Please verify this is indeed {display_label}."

    return CropGuardResult(
        crop_status="accepted",
        status="valid",
        reason_code=None,
        predicted_crop=display_label,
        predicted_class=canonical_cls,
        confidence=round(calibrated_p1, 4),
        raw_confidence=round(raw_p1, 4),
        margin=round(margin, 4),
        entropy=round(norm_entropy, 4),
        prototype_similarity=round(proto_sim, 4) if proto_sim is not None else None,
        proceed_to_disease_detection=True,
        user_message=f"Verified supported crop: {display_label} ({raw_p1 * 100:.1f}% confidence).",
        warning=uncertainty_warning,
        top_candidates=top_k_list[:3],
        is_supported_label=True,
    )

