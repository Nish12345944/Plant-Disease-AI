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
    green_mask = (H >= 24) & (H <= 95) & (S >= 22) & (V >= 18)
    chroma_green = (G > (R + 6)) & (G > (B + 6)) & (S >= 18)
    yellow_mask = (H >= 15) & (H < 24) & (S >= 28) & (V >= 25)
    brown_mask = (H >= 8) & (H < 18) & (S >= 25) & (V >= 18) & (V <= 170)
    warm_mask = ((H <= 15) | (H >= 165)) & (S >= 35) & (V >= 30)
    berry_mask = (H >= 95) & (H <= 135) & (S >= 15) & (S <= 95) & (V >= 15) & (V <= 135)
    cool_mask = (H >= 135) & (H <= 165) & (S >= 20) & (V >= 15)

    raw_plant_mask = (green_mask | chroma_green | yellow_mask | brown_mask | warm_mask | berry_mask | cool_mask).astype(np.uint8) * 255

    # 2. Non-plant suppression (human skin, white lab coats, cyan nitrile gloves)
    skin_mask = (Cr >= 133) & (Cr <= 173) & (Cb >= 77) & (Cb <= 127)
    white_coat_mask = (V >= 160) & (S <= 35) & (np.abs(R - G) < 20) & (np.abs(G - B) < 20)
    nitrile_mask = (B > (R + 45)) & (B > 115) & (H >= 95) & (H <= 130) & (S > 75)

    non_plant = (skin_mask | white_coat_mask | nitrile_mask).astype(np.uint8) * 255
    kernel_dil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    non_plant_dil = cv2.dilate(non_plant, kernel_dil)

    clean_plant_mask = raw_plant_mask.copy()
    clean_plant_mask[non_plant_dil > 0] = 0

    plant_pixel_count = int(np.sum(clean_plant_mask > 0))
    plant_coverage = plant_pixel_count / total_pixels

    if plant_coverage < DEFAULT_MIN_PLANT_COVERAGE:
        return []

    # 3. Assess if frame is a Macro Close-up (high plant coverage, minimal/no lab coat or skin)
    coat_coverage = float(np.sum(white_coat_mask)) / total_pixels
    skin_coverage = float(np.sum(skin_mask)) / total_pixels
    is_macro_close_up = (plant_coverage > 0.40) and (coat_coverage < 0.10) and (skin_coverage < 0.05)

    candidates: list[dict[str, Any]] = []

    if is_macro_close_up:
        # Macro close-up: the entire camera frame is focused on the plant/fruit specimen
        cx, cy = w // 2, h // 2
        side = min(w, h)
        x1 = max(0, cx - side // 2)
        y1 = max(0, cy - side // 2)
        x2 = min(w, x1 + side)
        y2 = min(h, y1 + side)

        crop_bgr = img_bgr[y1:y2, x1:x2]
        crop_gray = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY)
        sharp = float(cv2.Laplacian(crop_gray, cv2.CV_64F).var())

        candidates.append({
            "box": [x1, y1, x2, y2],
            "raw_box": [0, 0, w, h],
            "score": 1.0,
            "plant_density": plant_coverage,
            "sharpness": sharp,
            "is_macro": True,
            "roi_pil": Image.fromarray(cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)),
            "roi_bgr": crop_bgr,
        })

        # Also search for localized fruit/leaf cluster inside macro view
        kernel_m = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        closed_m = cv2.morphologyEx(clean_plant_mask, cv2.MORPH_CLOSE, kernel_m)
        contours, _ = cv2.findContours(closed_m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            if bw * bh > total_pixels * 0.15 and bw > 120 and bh > 120:
                mcx, mcy = x + bw // 2, y + bh // 2
                mside = int(max(bw, bh) * 1.05)
                mx1 = max(0, mcx - mside // 2)
                my1 = max(0, mcy - mside // 2)
                mx2 = min(w, mx1 + mside)
                my2 = min(h, my1 + mside)
                if mx2 - mx1 > 64 and my2 - my1 > 64:
                    sub_bgr = img_bgr[my1:my2, mx1:mx2]
                    sub_gray = cv2.cvtColor(sub_bgr, cv2.COLOR_BGR2GRAY)
                    sub_sharp = float(cv2.Laplacian(sub_gray, cv2.CV_64F).var())
                    candidates.append({
                        "box": [mx1, my1, mx2, my2],
                        "raw_box": [x, y, x + bw, y + bh],
                        "score": 0.9,
                        "plant_density": float(np.sum(clean_plant_mask[my1:my2, mx1:mx2] > 0)) / max(1, (mx2 - mx1) * (my2 - my1)),
                        "sharpness": sub_sharp,
                        "is_macro": True,
                        "roi_pil": Image.fromarray(cv2.cvtColor(sub_bgr, cv2.COLOR_BGR2RGB)),
                        "roi_bgr": sub_bgr,
                    })
    else:
        # Wide / medium shots (e.g. greenhouse with person in center, plants on shelves)
        kernel_c = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
        closed = cv2.morphologyEx(clean_plant_mask, cv2.MORPH_CLOSE, kernel_c)
        kernel_o = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cleaned = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_o)

        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            box_area = bw * bh

            if bw < 80 or bh < 80 or box_area < (total_pixels * min_area_ratio):
                continue

            roi_mask = clean_plant_mask[y:y + bh, x:x + bw]
            plant_density = float(np.sum(roi_mask > 0)) / max(1, box_area)
            if plant_density < 0.25:
                continue

            roi_coat = white_coat_mask[y:y + bh, x:x + bw]
            coat_ratio = float(np.sum(roi_coat)) / max(1, box_area)
            if coat_ratio > 0.25:
                continue

            roi_bgr = img_bgr[y:y + bh, x:x + bw]
            roi_gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
            sharpness = float(cv2.Laplacian(roi_gray, cv2.CV_64F).var())

            # Tight square bounding box around foliage cluster (1.08x padding, capped to 85% frame height)
            cx, cy = x + bw // 2, y + bh // 2
            side = int(max(bw, bh) * 1.08)
            side = min(side, int(h * 0.85))

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
            crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
            crop_pil = Image.fromarray(crop_rgb)

            score = plant_density * 0.5 + min(1.0, sharpness / 150.0) * 0.3 + min(1.0, box_area / (total_pixels * 0.15)) * 0.2

            candidates.append({
                "box": [x1, y1, x2, y2],
                "raw_box": [x, y, x + bw, y + bh],
                "score": score,
                "plant_density": plant_density,
                "sharpness": sharpness,
                "is_macro": False,
                "roi_pil": crop_pil,
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
    """Non-destructive quality and plant ROI evaluation order:
    
    1. Basic corruption & extreme exposure check.
    2. Plant ROI detection.
    3. ROI-level quality evaluation (ensures macro close-ups are preserved).
    """
    img_bgr = ensure_bgr_array(image_input)
    h, w = img_bgr.shape[:2]
    total_pixels = h * w

    if total_pixels == 0:
        return {
            "status": "unknown",
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
            "status": "unknown",
            "reason": f"Severely underexposed / dark frame (brightness {mean_brightness:.1f})",
            "blur_score": round(blur_score, 2),
            "brightness": round(mean_brightness, 2),
            "plant_coverage": 0.0,
            "rois": [],
        }

    if mean_brightness > max_brightness:
        return {
            "status": "unknown",
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
                "status": "blurry",
                "reason": f"Severely blurred camera motion (sharpness {blur_score:.1f} < {min_blur_score})",
                "blur_score": round(blur_score, 2),
                "brightness": round(mean_brightness, 2),
                "plant_coverage": 0.0,
                "rois": [],
            }

        return {
            "status": "unknown",
            "reason": "No identifiable plant foliage or crop specimen found in frame",
            "blur_score": round(blur_score, 2),
            "brightness": round(mean_brightness, 2),
            "plant_coverage": 0.0,
            "rois": [],
        }

    # 3. Check best ROI sharpness (evaluate sharpness on the actual plant region)
    best_roi_sharpness = max(r["sharpness"] for r in rois)
    if best_roi_sharpness < min_blur_score:
        return {
            "status": "blurry",
            "reason": f"Plant region is severely out of focus (ROI sharpness {best_roi_sharpness:.1f} < {min_blur_score})",
            "blur_score": round(best_roi_sharpness, 2),
            "brightness": round(mean_brightness, 2),
            "plant_coverage": round(rois[0]["plant_density"], 3),
            "rois": rois,
        }

    return {
        "status": "valid_plant",
        "reason": f"Found {len(rois)} tight plant region(s)",
        "blur_score": round(best_roi_sharpness, 2),
        "brightness": round(mean_brightness, 2),
        "plant_coverage": round(rois[0]["plant_density"], 3),
        "rois": rois,
    }
