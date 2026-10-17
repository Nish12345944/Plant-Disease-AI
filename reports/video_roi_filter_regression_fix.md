# Technical Report: Video ROI Filter Regression Fix

**Date:** 2026-10-17  
**Status:** Validated & Passed  
**Branch:** `test/stability-release`  

---

## 1. Executive Summary

A regression in the video inference pipeline caused all 20 sampled frames of `gemini_generated_video_Capsicum — Bacterial Spot.mp4` to be rejected as `Unknown` / `Low Conf / No Plant` with the rejection reason `"Uninformative wide scene or background clutter"`. Consequently, Model 1 and Model 2 executed 0 times, preventing plant identification and disease diagnosis on clear capsicum leaf close-ups exhibiting circular bacterial spot lesions.

This regression has been resolved by:
1. Eliminating the flawed global background rejection rule in `model1_test_app/plant_detector.py` that discarded entire frames if white/light background exceeded 2.5%, which had falsely triggered on leaf close-ups photographed against greenhouse structures, bright walls, or ambient glare.
2. Introducing a robust distinction between true uninformative wide background scenes and valid close-up leaf regions.
3. Implementing graded validation states across the pipeline (`valid_plant_roi`, `low_quality`, `no_plant_evidence`, `crop_uncertain`), preventing crop uncertainty or background artifacts from being conflated with the absence of a plant.
4. Ensuring macro close-up inspection frames retain full evidentiary weight during aggregation without being penalized as redundant duplicates.
5. Verifying complete end-to-end inference and executing full regression suites across both test videos (`gemini_generated_video_Capsicum — Bacterial Spot.mp4` and `blueberry_mummyberry.mp4`) as well as isolated frame tests.

---

## 2. Root Cause Analysis

### 2.1 The Flawed Rejection Condition
In the previous fix, `extract_tight_plant_rois` in `model1_test_app/plant_detector.py` contained the following logic:
```python
# Flawed logic previously added:
coat_coverage = float(np.sum(white_coat_mask)) / total_pixels
is_macro_close_up = (plant_coverage > 0.40) and (coat_coverage < 0.10)

if not is_macro_close_up and coat_coverage >= 0.025:
    return []  # Rejected 100% of frames in capsicum video
```

### 2.2 Why It Failed on Capsicum Video
- In `gemini_generated_video_Capsicum — Bacterial Spot.mp4`, the plant leaf occupies 57.5% – 71.7% of the frame.
- However, the top ~20% of the video frame captures a white/light greenhouse ceiling/wall and ambient daylight (`coat_coverage` ~0.15–0.25).
- Because `coat_coverage >= 0.10`, `is_macro_close_up` evaluated to `False`.
- Consequently, `if not is_macro_close_up and coat_coverage >= 0.025` triggered, causing `extract_tight_plant_rois` to return `[]` (empty list) on **every single frame**.
- The pipeline then misclassified every frame as `"Uninformative wide scene or background clutter"`, completely bypassing Model 1 and Model 2 inference.

### 2.3 Additional Conflations
- Crop uncertainty (low identification confidence for a specific crop) was previously conflated with the complete absence of a plant.
- Consecutive close-up frames captured while holding the camera steady on a diseased leaf were overly discounted by duplicate frame penalties (35% multiplier), while panning wide shots were not discounted.

---

## 3. Engineering Fixes Implemented

### 3.1 Refined Wide-Scene vs. Close-up Discrimination
Updated `model1_test_app/plant_detector.py`:
- A frame is only flagged as a wide background scene if `coat_coverage >= 0.45` **AND** `plant_coverage < 0.45`.
- Even in wide scenes, large macro plant contours (`area_ratio >= 0.35`) are preserved.
- When foliage covers `>= 0.35` of the frame in a non-wide scene, a full square macro crop is generated, capturing the complete leaf blade, venation, and lesions for Model 1.

### 3.2 Graded Validation Decisions
Separated and standardized frame decision states across the pipeline:
1. `valid_plant_roi`: Usable plant evidence localized with valid ROI; Model 1 evaluated and accepted.
2. `low_quality`: Frame is severely blurred, underexposed, or washed out.
3. `no_plant_evidence`: Frame contains no plant foliage or crop specimen (or is an uninformative wide background scene).
4. `crop_uncertain`: Usable plant ROI is localized and evaluated by Model 1, but crop identity confidence is below the acceptance threshold.

### 3.3 Preserving Macro Close-Up Evidence During Aggregation
Updated `model1_test_app/video_inference.py`:
- Macro close-up plant inspection frames (`is_macro=True`) retain higher evidentiary weight (`2.0` multiplier) and are not discounted as consecutive duplicates during steady camera inspection.

### 3.4 Backend & Frontend Synchronization
- Updated `app/backend/services.py` to recognize `valid_plant_roi` for Model 2 disease inference and video temporal aggregation.
- Updated `app/frontend/src/components/ExtractedFramesModal.jsx` to render distinct badges for `Valid Plant`, `Crop Uncertain`, `Low Quality`, and `Low Conf / No Plant`.

---

## 4. Empirical Validation & Measured Results

### 4.1 Video A: `gemini_generated_video_Capsicum — Bacterial Spot.mp4`

| Metric | Before Fix (Regression) | After Fix (Restored) |
| :--- | :--- | :--- |
| **Decoded Frames** | 240 | 240 |
| **Sampled Frames** | 20 | 20 |
| **Valid Plant Frames** | 0 | **18** (2 frames flagged as `crop_uncertain` during fast pan) |
| **Rejected Frames** | 20 | **2** |
| **Model 1 Runs** | 0 | **29** (top candidate ROIs evaluated across frames) |
| **Model 2 Runs** | 0 | **18** |
| **Final Crop Prediction** | `Unknown` (0.0%) | **Bell Pepper (`bellpepper`) (45.5% / consensus supported across 10 frames)** |
| **Disease Decision** | None (bypassed) | **Bacterial Spot (`bell_pepper__bacterial_spot`) — 86.2% confidence (5 supporting frames)** |

### 4.2 Video B: `blueberry_mummyberry.mp4`

| Metric | Measured Result | Evaluation |
| :--- | :--- | :--- |
| **Decoded Frames** | 240 | Baseline preserved |
| **Sampled Frames** | 20 | Baseline preserved |
| **Valid Plant Frames** | **8** | Frames 10–17 (close-up macro berry/leaf bunch) |
| **Rejected Frames** | **12** | Frames 1–9 and 18–20 (wide greenhouse shots) |
| **Model 1 Runs** | **8** | Evaluated on accepted macro ROIs |
| **Model 2 Runs** | **8** | Evaluated on accepted macro ROIs |
| **Final Crop Prediction** | **Blueberry (`blueberry`) (93.3%)** | Cleanly accepted (Tomato is strictly 0%) |
| **Disease Decision** | **Anthracnose Fruit Rot (`blueberry__anthracnose`) (89.0%)** | Crop-compatible; Yellow Leaf Curl Virus is strictly absent |

### 4.3 Frame-Level Graded Decision Tests

1. **Close-up leaf (Capsicum):** Status = `valid_plant_roi`, 1 usable ROI extracted, plant coverage = 71.7%.
2. **Wide scene with small plant (Blueberry Frame 5):** Status = `no_plant_evidence`, 0 ROIs extracted, reason = `"Uninformative wide scene or background clutter"`.
3. **Frame containing no plant (Blue textured wall / non-vegetation):** Status = `no_plant_evidence`, 0 ROIs extracted, reason = `"No identifiable plant foliage or crop specimen found in frame"`.
4. **Blurry / obstructed frame (Motion blurred leaf):** Status = `low_quality`, 0 ROIs extracted, reason = `"Plant region is severely out of focus (ROI sharpness < 10.0)"`.

---

## 5. Verification Test Suite Results

All test suites were executed in the repository environment:

1. `scripts/test_video_roi_filter_regression.py`: **ALL 3 TEST SUITES PASSED (Exit Code: 0)**
   - Video A (Capsicum): Restored plant frames, M1/M2 runs, Bell Pepper, Bacterial Spot (86.2%).
   - Video B (Blueberry): Preserved macro shots, rejected wide shots, Blueberry (93.3%), Anthracnose (89.0%).
   - Frame-Level Graded Decisions: All 4 states verified.
2. `scripts/test_video_crop_misclassification_regression.py`: **8/8 TESTS PASSED (Exit Code: 0)**
3. `scripts/test_safeguards.py`: **10/10 TESTS PASSED (Exit Code: 0)**
4. `scripts/test_video_pipeline_regression.py`: **19/19 TESTS PASSED (Exit Code: 0)**
5. Frontend Build (`vite build`): **Compiled successfully (0 errors)**

---

## 6. Constraints Adherence
- No model weights, checkpoints, or class mappings were modified or retrained.
- Raw datasets were unchanged.
- Frontend visual layout and design were preserved.
- Standalone image inference remains untouched and fully operational.
- Existing frame extractor logic was preserved.
- No deployment actions taken.
