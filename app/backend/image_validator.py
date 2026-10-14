"""Plant Image Validation Gate.

Safeguard A: Enforces image file integrity, minimum dimensions, exposure,
blur/sharpness, and multi-spectral vegetation presence before passing the image
to Model 1 (crop classification) or Model 2 (disease classification).

Return structured reason codes:
- invalid_file: Corrupt, unreadable, zero-size, or sub-minimum dimension image.
- low_visibility: Severely underexposed (pitch-black) or overexposed (whiteout glare).
- blurry_image: Severely blurred motion/focus ruining foliage details.
- non_plant_image: No recognizable plant foliage, leaf, or crop tissue detected.
- uncertain_plant_content: Marginal or ambiguous plant tissue.
"""

from __future__ import annotations

import io
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional, Union

import cv2
import numpy as np
from PIL import Image

from model1_test_app.plant_detector import (
    DEFAULT_MAX_BRIGHTNESS,
    DEFAULT_MIN_BLUR_SCORE,
    DEFAULT_MIN_BRIGHTNESS,
    DEFAULT_MIN_PLANT_COVERAGE,
    ensure_bgr_array,
    extract_tight_plant_rois,
)

logger = logging.getLogger(__name__)

# Minimum spatial dimensions for reliable neural plant feature extraction
MIN_IMAGE_DIMENSION = 64

# Blur & exposure thresholds (non-destructive: preserves macro close-ups & healthy foliage)
MIN_BLUR_SCORE = 8.0
MIN_BRIGHTNESS = DEFAULT_MIN_BRIGHTNESS   # 15.0
MAX_BRIGHTNESS = DEFAULT_MAX_BRIGHTNESS   # 248.0
MIN_PLANT_COVERAGE = DEFAULT_MIN_PLANT_COVERAGE  # 0.005 (0.5% minimum vegetation coverage)
UNCERTAIN_PLANT_COVERAGE = 0.015          # 1.5% coverage threshold for uncertain content


@dataclass
class ValidationResult:
    """Structured response contract for Plant Image Validation Gate."""
    valid: bool
    status: str            # "valid", "rejected", "uncertain"
    reason_code: Optional[str]  # "invalid_file", "low_visibility", "blurry_image", "non_plant_image", "uncertain_plant_content", or None
    message: str           # Actionable, farmer-friendly guidance
    metrics: dict[str, Any]
    image_size: tuple[int, int]  # (width, height)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Lazy-loaded OpenCV cascades for human portrait rejection
_FACE_CASCADE: Optional[cv2.CascadeClassifier] = None
_EYE_CASCADE: Optional[cv2.CascadeClassifier] = None


def get_face_cascades() -> tuple[Optional[cv2.CascadeClassifier], Optional[cv2.CascadeClassifier]]:
    """Lazily load OpenCV Haar face and eye cascades."""
    global _FACE_CASCADE, _EYE_CASCADE
    if _FACE_CASCADE is None:
        try:
            cas_path = Path(cv2.data.haarcascades)
            alt2 = cas_path / "haarcascade_frontalface_alt2.xml"
            default_cas = cas_path / "haarcascade_frontalface_default.xml"
            eye_cas = cas_path / "haarcascade_eye.xml"

            if alt2.exists():
                _FACE_CASCADE = cv2.CascadeClassifier(str(alt2))
            elif default_cas.exists():
                _FACE_CASCADE = cv2.CascadeClassifier(str(default_cas))

            if eye_cas.exists():
                _EYE_CASCADE = cv2.CascadeClassifier(str(eye_cas))
        except Exception as exc:
            logger.warning(f"Could not initialize face cascades: {exc}")
    return _FACE_CASCADE, _EYE_CASCADE


def detect_human_face_presence(img_bgr: np.ndarray, gray: np.ndarray) -> bool:
    """Detect whether the image contains a human portrait or person.

    Uses frontal face cascade paired with eye feature verification to prevent
    false rejections on circular plant lesions or vein bifurcations.
    """
    face_cas, eye_cas = get_face_cascades()
    if face_cas is None or face_cas.empty():
        return False

    h, w = gray.shape[:2]
    min_dim = min(h, w)
    # Face in a portrait is prominent (at least 60x60 or 8% of frame)
    min_face_size = (max(60, int(min_dim * 0.08)), max(60, int(min_dim * 0.08)))

    try:
        faces = face_cas.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=min_face_size,
        )
        for (x, y, fw, fh) in faces:
            crop_gray = gray[y : y + fh, x : x + fw]
            # Verify facial geometry: eyes in the upper 65% of the candidate face box
            if eye_cas is not None and not eye_cas.empty():
                eyes = eye_cas.detectMultiScale(
                    crop_gray[: int(fh * 0.65), :],
                    scaleFactor=1.1,
                    minNeighbors=3,
                )
                if len(eyes) >= 1:
                    return True
            else:
                # Fallback if eye cascade unavailable: verify skin ratio in face ROI
                crop_bgr = img_bgr[y : y + fh, x : x + fw]
                ycrcb_crop = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2YCrCb)
                Cr, Cb = ycrcb_crop[:, :, 1], ycrcb_crop[:, :, 2]
                B = crop_bgr[:, :, 0].astype(np.float32)
                G = crop_bgr[:, :, 1].astype(np.float32)
                R = crop_bgr[:, :, 2].astype(np.float32)
                skin = (Cr >= 133) & (Cr <= 173) & (Cb >= 77) & (Cb <= 127) & (R > G) & (G > B)
                if np.mean(skin) > 0.40:
                    return True
    except Exception as exc:
        logger.debug(f"Face cascade detection note: {exc}")
    return False


def validate_plant_image(
    image_input: Union[bytes, str, Path, Image.Image, np.ndarray],
    min_dimension: int = MIN_IMAGE_DIMENSION,
    min_blur: float = MIN_BLUR_SCORE,
    min_brightness: float = MIN_BRIGHTNESS,
    max_brightness: float = MAX_BRIGHTNESS,
    min_coverage: float = MIN_PLANT_COVERAGE,
) -> ValidationResult:
    """Validate image decodability, dimensions, exposure, blur, and plant presence.

    Args:
        image_input: Raw image bytes, file path, PIL Image, or numpy array.
        min_dimension: Minimum required width and height in pixels.
        min_blur: Minimum Laplacian variance for blur check.
        min_brightness: Minimum mean luminance (below = pitch black).
        max_brightness: Maximum mean luminance (above = washed out whiteout).
        min_coverage: Minimum vegetation pixel coverage ratio.

    Returns:
        ValidationResult with status, reason_code, message, and metrics.
    """
    # -------------------------------------------------------------------------
    # 1. Image Decoding and Format Verification
    # -------------------------------------------------------------------------
    pil_img: Optional[Image.Image] = None
    try:
        if isinstance(image_input, bytes):
            if len(image_input) == 0:
                return ValidationResult(
                    valid=False,
                    status="rejected",
                    reason_code="invalid_file",
                    message="The uploaded image file is empty (0 bytes). Please upload a valid image photo.",
                    metrics={"byte_size": 0},
                    image_size=(0, 0),
                )
            pil_img = Image.open(io.BytesIO(image_input))
            # Verify image integrity
            pil_img.verify()
            # Reopen after verify() because verify() clears file pointers
            pil_img = Image.open(io.BytesIO(image_input))
        elif isinstance(image_input, (str, Path)):
            p = Path(image_input)
            if not p.exists() or p.stat().st_size == 0:
                return ValidationResult(
                    valid=False,
                    status="rejected",
                    reason_code="invalid_file",
                    message=f"Image file not found or empty at '{p}'.",
                    metrics={"file_path": str(p)},
                    image_size=(0, 0),
                )
            pil_img = Image.open(p)
            pil_img.verify()
            pil_img = Image.open(p)
        elif isinstance(image_input, Image.Image):
            pil_img = image_input
        elif isinstance(image_input, np.ndarray):
            if image_input.size == 0:
                return ValidationResult(
                    valid=False,
                    status="rejected",
                    reason_code="invalid_file",
                    message="Image array contains 0 elements.",
                    metrics={},
                    image_size=(0, 0),
                )
            if image_input.ndim == 2:
                pil_img = Image.fromarray(image_input).convert("RGB")
            elif image_input.ndim == 3 and image_input.shape[2] in (3, 4):
                pil_img = Image.fromarray(image_input[:, :, :3])
            else:
                return ValidationResult(
                    valid=False,
                    status="rejected",
                    reason_code="invalid_file",
                    message=f"Unsupported image array shape {image_input.shape}.",
                    metrics={"shape": list(image_input.shape)},
                    image_size=(0, 0),
                )
        else:
            return ValidationResult(
                valid=False,
                status="rejected",
                reason_code="invalid_file",
                message=f"Unsupported image input type '{type(image_input).__name__}'.",
                metrics={},
                image_size=(0, 0),
            )
    except Exception as exc:
        logger.warning(f"Image decoding failed: {exc}")
        return ValidationResult(
            valid=False,
            status="rejected",
            reason_code="invalid_file",
            message="The uploaded file could not be decoded as a valid image. Please provide a standard JPG, PNG, or WebP photo.",
            metrics={"decode_error": str(exc)},
            image_size=(0, 0),
        )

    # Convert to RGB (handling palette / alpha transparency)
    if getattr(pil_img, "is_animated", False):
        try:
            pil_img.seek(0)
        except Exception:
            pass

    try:
        rgb_img = pil_img.convert("RGB")
    except Exception as exc:
        return ValidationResult(
            valid=False,
            status="rejected",
            reason_code="invalid_file",
            message="Could not convert image to RGB color space. Please upload a standard photo.",
            metrics={"conversion_error": str(exc)},
            image_size=(pil_img.width, pil_img.height),
        )

    w, h = rgb_img.size

    # Check minimum dimensions
    if w < min_dimension or h < min_dimension:
        return ValidationResult(
            valid=False,
            status="rejected",
            reason_code="invalid_file",
            message=(
                f"Image resolution ({w}x{h} px) is too small to inspect plant details. "
                f"Please upload a photo of at least {min_dimension}x{min_dimension} pixels."
            ),
            metrics={"width": w, "height": h, "min_dimension": min_dimension},
            image_size=(w, h),
        )

    # -------------------------------------------------------------------------
    # 2. Exposure & Luminance Verification
    # -------------------------------------------------------------------------
    # Scale down large image for fast OpenCV Laplacian & exposure computation
    if w > 1024 or h > 1024:
        scale = 1024.0 / max(w, h)
        eval_img = rgb_img.resize((int(w * scale), int(h * scale)), Image.Resampling.BILINEAR)
    else:
        eval_img = rgb_img

    np_rgb = np.array(eval_img)
    img_bgr = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2GRAY)

    mean_brightness = float(np.mean(gray))

    if mean_brightness < min_brightness:
        return ValidationResult(
            valid=False,
            status="rejected",
            reason_code="low_visibility",
            message=(
                f"The photo is too dark or underexposed (brightness {mean_brightness:.1f}/{min_brightness:.0f}). "
                "Please take a photo in brighter daylight or illuminate the crop leaf."
            ),
            metrics={"brightness": round(mean_brightness, 2), "min_brightness": min_brightness},
            image_size=(w, h),
        )

    if mean_brightness > max_brightness:
        return ValidationResult(
            valid=False,
            status="rejected",
            reason_code="low_visibility",
            message=(
                f"The photo is overexposed or washed out by harsh glare (brightness {mean_brightness:.1f}/{max_brightness:.0f}). "
                "Please shield the leaf from direct flash or excessive sunlight reflection."
            ),
            metrics={"brightness": round(mean_brightness, 2), "max_brightness": max_brightness},
            image_size=(w, h),
        )

    # -------------------------------------------------------------------------
    # 3. Blur & Sharpness Verification
    # -------------------------------------------------------------------------
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    # -------------------------------------------------------------------------
    # 4. Human Portrait & Person Detection Guard
    # -------------------------------------------------------------------------
    if detect_human_face_presence(img_bgr, gray):
        return ValidationResult(
            valid=False,
            status="rejected",
            reason_code="non_plant_image",
            message="This image does not appear to contain a plant. Please upload a clear plant image.",
            metrics={
                "detected_human_face": True,
                "plant_coverage": 0.0,
                "blur_score": round(blur_score, 2),
                "brightness": round(mean_brightness, 2),
                "rois_found": 0,
            },
            image_size=(w, h),
        )

    # -------------------------------------------------------------------------
    # 5. Multi-Spectral Plant Presence & Candidate ROI Extraction
    # -------------------------------------------------------------------------
    try:
        rois = extract_tight_plant_rois(img_bgr, max_rois=3, min_area_ratio=0.01)
    except Exception as exc:
        logger.warning(f"Plant ROI extraction note: {exc}")
        rois = []

    # Calculate overall plant pixel coverage
    h_bgr, w_bgr = img_bgr.shape[:2]
    total_px = h_bgr * w_bgr

    # Multi-spectral color masks
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    Cr, Cb = ycrcb[:, :, 1], ycrcb[:, :, 2]
    B = img_bgr[:, :, 0].astype(np.float32)
    G = img_bgr[:, :, 1].astype(np.float32)
    R = img_bgr[:, :, 2].astype(np.float32)

    # 1. True Chlorophyll Foliage & Vegetation (Excess Green ExG = 2G - R - B)
    green_foliage = (H >= 24) & (H <= 95) & (S >= 20) & (V >= 18) & (G > R) & (G > B)
    exg = 2 * G - R - B
    chlorophyll_mask = green_foliage & (exg > 3)

    # 2. Chlorotic (Yellowing / Mosaic) & Necrotic (Brown / Rust / Blight) Tissues
    yellow_chlorosis = (H >= 15) & (H < 24) & (S >= 25) & (V >= 25) & (G > B)
    brown_necrotic = (H >= 8) & (H < 18) & (S >= 22) & (V >= 18) & (V <= 170)

    # Core vegetative foliage coverage
    vegetative_mask = chlorophyll_mask | yellow_chlorosis | brown_necrotic
    veg_coverage = float(np.sum(vegetative_mask) / total_px) if total_px > 0 else 0.0

    # 3. Fruits, Berries, and Flowers (only valid if vegetative tissue is also present)
    warm_fruit = ((H <= 15) | (H >= 165)) & (S >= 35) & (V >= 30)
    berry_fruit = (H >= 95) & (H <= 135) & (S >= 25) & (V >= 20) & (V <= 135)
    cool_flower = (H >= 135) & (H <= 165) & (S >= 25) & (V >= 20)

    # Non-foliage tissue requires at least minimal vegetative support (leaves/stems)
    if veg_coverage > 0.002:
        raw_plant_mask = vegetative_mask | warm_fruit | berry_fruit | cool_flower
    else:
        raw_plant_mask = vegetative_mask

    # Suppress skin, lab coats, nitrile gloves
    skin_mask = (Cr >= 133) & (Cr <= 173) & (Cb >= 77) & (Cb <= 127) & (R > G) & (G > B) & ((R - G) >= 6)
    white_coat_mask = (V >= 160) & (S <= 35) & (np.abs(R - G) < 20) & (np.abs(G - B) < 20)
    nitrile_mask = (B > (R + 45)) & (B > 115) & (H >= 95) & (H <= 130) & (S > 75)
    non_plant = skin_mask | white_coat_mask | nitrile_mask

    clean_plant_mask = raw_plant_mask & (~non_plant)
    plant_px_count = int(np.sum(clean_plant_mask))
    plant_coverage = float(plant_px_count / total_px) if total_px > 0 else 0.0

    # Best ROI sharpness if plant ROIs exist
    best_roi_sharpness = max([r.get("sharpness", blur_score) for r in rois], default=blur_score)

    # Case A: Complete absence or sub-minimal plant content
    if plant_coverage < min_coverage:
        return ValidationResult(
            valid=False,
            status="rejected",
            reason_code="non_plant_image",
            message="This image does not appear to contain a plant. Please upload a clear plant image.",
            metrics={
                "plant_coverage": round(plant_coverage, 4),
                "min_coverage": min_coverage,
                "blur_score": round(blur_score, 2),
                "brightness": round(mean_brightness, 2),
                "rois_found": len(rois),
            },
            image_size=(w, h),
        )

    # Case B: Severe blur check
    # We evaluate sharpness on both the whole frame and the plant ROI
    effective_sharpness = max(blur_score, best_roi_sharpness)
    if effective_sharpness < min_blur:
        return ValidationResult(
            valid=False,
            status="rejected",
            reason_code="blurry_image",
            message=(
                f"The image is severely blurry or out of focus (sharpness {effective_sharpness:.1f}/{min_blur:.0f}). "
                "Please hold the camera steady and retake a sharp, well-focused photo of the crop leaf."
            ),
            metrics={
                "blur_score": round(effective_sharpness, 2),
                "frame_blur": round(blur_score, 2),
                "min_blur": min_blur,
                "brightness": round(mean_brightness, 2),
                "plant_coverage": round(plant_coverage, 4),
                "rois_found": len(rois),
            },
            image_size=(w, h),
        )

    # Case C: Uncertain / borderline plant content
    if plant_coverage < UNCERTAIN_PLANT_COVERAGE and len(rois) <= 1 and best_roi_sharpness < (min_blur * 1.5):
        return ValidationResult(
            valid=False,
            status="uncertain",
            reason_code="uncertain_plant_content",
            message=(
                "Plant content was partially visible but could not be clearly verified. "
                "Please bring the camera closer so the crop leaf fills more of the frame."
            ),
            metrics={
                "plant_coverage": round(plant_coverage, 4),
                "blur_score": round(effective_sharpness, 2),
                "brightness": round(mean_brightness, 2),
                "rois_found": len(rois),
            },
            image_size=(w, h),
        )

    # -------------------------------------------------------------------------
    # 5. Passed All Validation Checks
    # -------------------------------------------------------------------------
    return ValidationResult(
        valid=True,
        status="valid",
        reason_code=None,
        message="Plant image verified successfully.",
        metrics={
            "plant_coverage": round(plant_coverage, 4),
            "blur_score": round(effective_sharpness, 2),
            "brightness": round(mean_brightness, 2),
            "rois_found": len(rois),
        },
        image_size=(w, h),
    )
