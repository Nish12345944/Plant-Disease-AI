"""Plant presence, tight candidate region extraction, and non-destructive quality evaluation engine.

Detects:
1. Candidate plant/crop regions of interest (ROIs) across the frame using multi-spectral
   vegetation cues (green leaves, yellow chlorosis, brown stems/lesions, dark blueberries, warm/cool fruits/flowers).
2. Suppresses non-plant subjects (human skin, white lab coats, blue nitrile gloves).
3. Distinguishes between wide/medium greenhouse views (generating tight foliage cluster ROIs)
   and macro close-ups (preserving high-detail fruit/leaf regions).
4. Evaluates visual quality directly on the localized plant ROI rather than rejecting entire frames prematurely.
"""

from __future__ import annotations

import logging
from typing import Any, Optional, Union

import cv2
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# Non-destructive Quality & Detection Thresholds
DEFAULT_MIN_BLUR_SCORE = 10.0          # Non-destructive threshold to preserve macro/bokeh close-ups
DEFAULT_MIN_BRIGHTNESS = 15.0          # Only reject genuinely pitch-black frames
DEFAULT_MAX_BRIGHTNESS = 248.0         # Only reject genuinely washed-out/blown-out whiteout frames
DEFAULT_MIN_PLANT_COVERAGE = 0.005     # Minimal plant presence threshold
DEFAULT_CONFIDENCE_THRESHOLD = 0.40    # Model 1 confidence threshold for crop identification


def ensure_bgr_array(image_input: Union[str, np.ndarray, Image.Image, bytes]) -> np.ndarray:
    """Convert various image representations into an 8-bit BGR numpy array."""
    if isinstance(image_input, np.ndarray):
        if image_input.ndim == 2:
            return cv2.cvtColor(image_input, cv2.COLOR_GRAY2BGR)
        if image_input.ndim == 3:
            if image_input.shape[2] == 4:
                return cv2.cvtColor(image_input, cv2.COLOR_BGRA2BGR)
            return image_input
        raise ValueError(f"Invalid image array shape: {image_input.shape}")

    if isinstance(image_input, Image.Image):
        rgb_arr = np.array(image_input.convert("RGB"))
        return cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2BGR)

    if isinstance(image_input, (str, bytes)):
        from pathlib import Path
        if isinstance(image_input, str) and Path(image_input).exists():
            img = cv2.imread(image_input)
            if img is not None:
                return img
        if isinstance(image_input, str):
            image_bytes = image_input.encode("latin1")
        else:
            image_bytes = image_input
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is not None:
            return img

    raise ValueError("Could not convert input into a valid BGR image array.")


def extract_tight_plant_rois(
    image_input: Union[str, np.ndarray, Image.Image, bytes],
    max_rois: int = 3,
    min_area_ratio: float = 0.015,
) -> list[dict[str, Any]]:
    """Extract tight, focused candidate plant ROIs that isolate foliage without grabbing half the frame.

    Args:
        image_input: BGR array, RGB PIL image, or path.
        max_rois: Maximum number of top distinct candidate ROIs to return.
        min_area_ratio: Minimum area of a foliage cluster relative to total frame area.

    Returns:
        List of candidate ROI dictionaries sorted by quality score descending.
    """
    img_bgr = ensure_bgr_array(image_input)
    h, w = img_bgr.shape[:2]
    total_pixels = h * w

    if total_pixels == 0:
        return []

    # Color space conversions
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    Cr, Cb = ycrcb[:, :, 1], ycrcb[:, :, 2]

    B = img_bgr[:, :, 0].astype(np.float32)
    G = img_bgr[:, :, 1].astype(np.float32)
    R = img_bgr[:, :, 2].astype(np.float32)

    # 1. Multi-spectral vegetation detection
    green_foliage = (H >= 24) & (H <= 95) & (S >= 20) & (V >= 18) & (G > R) & (G > B)
    exg = 2 * G - R - B
    chlorophyll_mask = green_foliage & (exg > 3)
    yellow_chlorosis = (H >= 15) & (H < 25) & (S >= 20) & (V >= 20) & (G > B)
    brown_necrotic = (H >= 6) & (H < 22) & (S >= 18) & (V >= 15) & (R > B)

    warm_fruit = ((H <= 18) | (H >= 162)) & (S >= 25) & (V >= 25)
    berry_fruit = (H >= 95) & (H <= 135) & (S >= 20) & (V >= 15) & (V <= 140)
    cool_flower = (H >= 135) & (H <= 165) & (S >= 25) & (V >= 20)
    purple_fruit = (H >= 125) & (H <= 165) & (S >= 20) & (V >= 12)

    raw_mask_bool = (
        chlorophyll_mask
        | yellow_chlorosis
        | brown_necrotic
        | warm_fruit
        | berry_fruit
        | cool_flower
        | purple_fruit
    )

    raw_plant_mask = raw_mask_bool.astype(np.uint8) * 255

    # 2. Non-plant suppression (white lab coats, structural white glass, cyan nitrile gloves, human skin)
    white_coat_mask = (V >= 150) & (S <= 40) & (np.abs(R - G) < 25) & (np.abs(G - B) < 25)
    nitrile_mask = (B > (R + 45)) & (B > 115) & (H >= 95) & (H <= 130) & (S > 75)
    skin_mask = (Cr >= 133) & (Cr <= 173) & (Cb >= 77) & (Cb <= 127) & (R > G) & (G > B)

    non_plant = (white_coat_mask | nitrile_mask | skin_mask).astype(np.uint8) * 255
    kernel_dil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    non_plant_dil = cv2.dilate(non_plant, kernel_dil)

    clean_plant_mask = raw_plant_mask.copy()
    clean_plant_mask[non_plant_dil > 0] = 0

    plant_pixel_count = int(np.sum(clean_plant_mask > 0))
    plant_coverage = plant_pixel_count / total_pixels

    if plant_coverage < DEFAULT_MIN_PLANT_COVERAGE:
        return []

    # Wide scene check: frame dominated by white structural glass/ceiling/walls with only distant foliage
    white_coverage = float(np.sum(white_coat_mask)) / total_pixels
    is_wide_scene = (white_coverage >= 0.45) and (plant_coverage < 0.45)

    candidates: list[dict[str, Any]] = []

    # Check contours of clean plant mask
    kernel_c = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    closed = cv2.morphologyEx(clean_plant_mask, cv2.MORPH_CLOSE, kernel_c)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, bw, bh = cv2.boundingRect(cnt)
        box_area = bw * bh
        area_ratio = box_area / total_pixels

        if bw < 64 or bh < 64 or area_ratio < 0.04:
            continue

        roi_mask = clean_plant_mask[y:y + bh, x:x + bw]
        plant_density = float(np.sum(roi_mask > 0)) / max(1, box_area)
        roi_coat = white_coat_mask[y:y + bh, x:x + bw]
        coat_ratio = float(np.sum(roi_coat)) / max(1, box_area)

        if is_wide_scene:
            # In a wide background scene, skip distant benches / tables
            if area_ratio < 0.35 or plant_density < 0.60:
                continue

        if plant_density < 0.35 or coat_ratio > 0.25:
            continue

        # Tight square bounding box around foliage cluster (1.08x padding, capped to frame dimensions)
        cx, cy = x + bw // 2, y + bh // 2
        side = int(max(bw, bh) * 1.08)
        side = min(side, max(w, h))

        x1 = max(0, cx - side // 2)
        y1 = max(0, cy - side // 2)
        x2 = min(w, x1 + side)
        y2 = min(h, y1 + side)

        if x2 - x1 < side and x1 > 0:
            x1 = max(0, x2 - side)
        if y2 - y1 < side and y1 > 0:
            y1 = max(0, y2 - side)

        if (x2 - x1) < 64 or (y2 - y1) < 64:
            continue

        crop_bgr = img_bgr[y1:y2, x1:x2]
        crop_gray = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY)
        sharpness = float(cv2.Laplacian(crop_gray, cv2.CV_64F).var())

        score = plant_density * 0.4 + min(1.0, sharpness / 150.0) * 0.3 + min(1.0, area_ratio / 0.25) * 0.3
        is_macro = (plant_density >= 0.65) and (area_ratio >= 0.30)

        candidates.append({
            "box": [x1, y1, x2, y2],
            "raw_box": [x, y, x + bw, y + bh],
            "score": score,
            "plant_density": plant_density,
            "sharpness": sharpness,
            "coat_ratio": coat_ratio,
            "is_macro": is_macro,
            "roi_pil": Image.fromarray(cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)),
            "roi_bgr": crop_bgr,
        })

    # Macro center candidate if frame is dominated by plant foliage
    if plant_coverage >= 0.35 and not is_wide_scene:
        cx, cy = w // 2, h // 2
        side = min(w, h)
        x1 = max(0, cx - side // 2)
        y1 = max(0, cy - side // 2)
        x2 = min(w, x1 + side)
        y2 = min(h, y1 + side)
        crop_bgr = img_bgr[y1:y2, x1:x2]
        crop_gray = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY)
        sharpness = float(cv2.Laplacian(crop_gray, cv2.CV_64F).var())
        candidates.append({
            "box": [x1, y1, x2, y2],
            "raw_box": [0, 0, w, h],
            "score": 0.85 + 0.15 * min(1.0, sharpness / 150.0),
            "plant_density": plant_coverage,
            "sharpness": sharpness,
            "coat_ratio": white_coverage,
            "is_macro": True,
            "roi_pil": Image.fromarray(cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)),
            "roi_bgr": crop_bgr,
        })

    candidates.sort(key=lambda c: c["score"], reverse=True)

    # NMS across candidates (IoU 0.35)
    selected: list[dict[str, Any]] = []
    for cand in candidates:
        b1 = cand["box"]
        overlap = False
        for s in selected:
            b2 = s["box"]
            ix1 = max(b1[0], b2[0])
            iy1 = max(b1[1], b2[1])
            ix2 = min(b1[2], b2[2])
            iy2 = min(b1[3], b2[3])
            iw = max(0, ix2 - ix1)
            ih = max(0, iy2 - iy1)
            inter = iw * ih
            a1 = (b1[2] - b1[0]) * (b1[3] - b1[1])
            a2 = (b2[2] - b2[0]) * (b2[3] - b2[1])
            union = a1 + a2 - inter
            iou = inter / union if union > 0 else 0.0
            if iou > 0.35:
                overlap = True
                break
        if not overlap:
            selected.append(cand)
            if len(selected) >= max_rois:
                break

    return selected


def assess_plant_presence_and_quality(
    image_input: Union[str, np.ndarray, Image.Image, bytes],
    min_blur_score: float = DEFAULT_MIN_BLUR_SCORE,
    min_brightness: float = DEFAULT_MIN_BRIGHTNESS,
    max_brightness: float = DEFAULT_MAX_BRIGHTNESS,
) -> dict[str, Any]:
    """Graded quality and plant ROI evaluation order:
    
    1. Basic corruption & extreme exposure check -> 'low_quality'
    2. Plant ROI detection -> 'valid_plant_roi' or 'no_plant_evidence'
    3. ROI-level quality evaluation (ensures macro close-ups are preserved)
    """
    img_bgr = ensure_bgr_array(image_input)
    h, w = img_bgr.shape[:2]
    total_pixels = h * w

    if total_pixels == 0:
        return {
            "status": "no_plant_evidence",
            "reason": "Empty or zero-size image frame",
            "blur_score": 0.0,
            "brightness": 0.0,
            "plant_coverage": 0.0,
            "rois": [],
        }

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    mean_brightness = float(np.mean(gray))

    # 1. Extreme underexposure / overexposure
    if mean_brightness < min_brightness:
        return {
            "status": "low_quality",
            "reason": f"Severely underexposed / dark frame (brightness {mean_brightness:.1f})",
            "blur_score": round(blur_score, 2),
            "brightness": round(mean_brightness, 2),
            "plant_coverage": 0.0,
            "rois": [],
        }

    if mean_brightness > max_brightness:
        return {
            "status": "low_quality",
            "reason": f"Severely overexposed / washed out frame (brightness {mean_brightness:.1f})",
            "blur_score": round(blur_score, 2),
            "brightness": round(mean_brightness, 2),
            "plant_coverage": 0.0,
            "rois": [],
        }

    # 2. Extract tight plant candidate ROIs
    rois = extract_tight_plant_rois(img_bgr)

    if not rois:
        # Check if frame had severe motion blur across entire scene
        if blur_score < min_blur_score:
            return {
                "status": "low_quality",
                "reason": f"Severely blurred camera motion (sharpness {blur_score:.1f} < {min_blur_score})",
                "blur_score": round(blur_score, 2),
                "brightness": round(mean_brightness, 2),
                "plant_coverage": 0.0,
                "rois": [],
            }

        # Check if frame is an uninformative wide scene with background clutter
        hsv_t = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        S_t, V_t = hsv_t[:, :, 1], hsv_t[:, :, 2]
        R_t = img_bgr[:, :, 2].astype(np.float32)
        G_t = img_bgr[:, :, 1].astype(np.float32)
        B_t = img_bgr[:, :, 0].astype(np.float32)
        w_mask_t = (V_t >= 150) & (S_t <= 40) & (np.abs(R_t - G_t) < 25) & (np.abs(G_t - B_t) < 25)
        w_cov_t = float(np.sum(w_mask_t)) / max(1, total_pixels)

        if w_cov_t >= 0.45:
            reason_str = "Uninformative wide scene or background clutter"
        else:
            reason_str = "No identifiable plant foliage or crop specimen found in frame"

        return {
            "status": "no_plant_evidence",
            "reason": reason_str,
            "blur_score": round(blur_score, 2),
            "brightness": round(mean_brightness, 2),
            "plant_coverage": 0.0,
            "rois": [],
        }

    # 3. Check best ROI sharpness (evaluate sharpness on the actual plant region)
    best_roi_sharpness = max(r["sharpness"] for r in rois)
    if best_roi_sharpness < min_blur_score:
        return {
            "status": "low_quality",
            "reason": f"Plant region is severely out of focus (ROI sharpness {best_roi_sharpness:.1f} < {min_blur_score})",
            "blur_score": round(best_roi_sharpness, 2),
            "brightness": round(mean_brightness, 2),
            "plant_coverage": round(rois[0]["plant_density"], 3),
            "rois": rois,
        }

    return {
        "status": "valid_plant_roi",
        "reason": f"Found {len(rois)} usable plant region(s)",
        "blur_score": round(best_roi_sharpness, 2),
        "brightness": round(mean_brightness, 2),
        "plant_coverage": round(rois[0]["plant_density"], 3),
        "rois": rois,
    }
