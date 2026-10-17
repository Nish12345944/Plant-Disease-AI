# Technical Investigation: Video Crop Misclassification Caused by Invalid Frames

**File Under Investigation:** `blueberry_mummyberry.mp4`  
**Observed Bug:** Video clearly showing diseased blueberries was misclassified as:
- **Crop:** Tomato (49.3% confidence)
- **Disease:** Yellow Leaf Curl Virus (78.1% confidence across 3 supporting frames)
- **Frame Summary:** 20 sampled frames, 20 reported valid plant frames, 0 rejected frames.

---

## 1. Executive Summary & Root Cause Overview

The video `blueberry_mummyberry.mp4` contains three distinct temporal segments:
1. **Segment 1 (t = 0.0s – 4.0s, Frames 1–9):** Wide-angle establishing shot of a greenhouse aisle showing an agronomist in a white lab coat and blue gloves walking by nursery tables holding distant brassica/nursery plants against greenhouse glass panels.
2. **Segment 2 (t = 4.5s – 8.2s, Frames 10–17):** High-detail macro close-up of blueberry foliage and blueberry fruits visibly infected with Mummy Berry (`blueberry__mummy_berry`).
3. **Segment 3 (t = 8.5s – 10.0s, Frames 18–20):** Wide-angle cut back to the agronomist in the greenhouse.

The misclassification occurs due to a cascading failure across four key stages:
1. **Loose Plant ROI Extraction on Wide Shots:** Wide greenhouse scenes with distant background nursery benches were extracted into a large 244×244 bounding box (`[265, 44, 509, 288]` on a 512×288 frame). Over 40% of this bounding box is non-plant background (white greenhouse glass, structural metal framing, and a lab coat).
2. **Model 1 Softmax Overconfidence on Out-of-Domain Clutter:** When Model 1 (trained on close-up crop specimens) is evaluated on this wide background clutter, softmax normalization arbitrarily collapses onto `tomato` with 92.3%–99.8% probability. Neural-network confidence was erroneously treated as proof of plant presence.
3. **Duplicate Background Frame Weighting:** Repeated, near-identical background frames (7 frames in Segment 1, 3 frames in Segment 3) were each given full weight in the probability accumulation vector.
4. **Unweighted Arithmetic Mean Aggregation:** Simple `np.mean(prob_vectors)` aggregated 10 background frames (predicting Tomato ~99%) against 7 macro blueberry frames (predicting Blueberry ~100%), allowing background noise to win by sheer frame count (49.3% Tomato vs 34.9% Blueberry).
5. **Coupled Misdiagnosis Cascade in Model 2:** Because the video consensus crop was set to `tomato`, Model 2 evaluated all frames under `crop_name="tomato"`. This masked out the true blueberry diseases on the macro frames and falsely matched background foliage in frames 18–20 to `tomato__yellow_leaf_curl_virus` (78.1% confidence, 3 supporting frames).

---

## 2. Frame-by-Frame Diagnostic Trace

| Frame # | Timestamp | Frame Type | Extracted ROI Box | Plant Density | Background / White % | Model 1 Top Prediction (Raw Conf) | Model 2 Prediction (Conditioned on Tomato) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **01** | 0.00s | Wide greenhouse | `[134, 44, 378, 288]` | 44.3% | 26.5% | Broccoli (73.7%) | None (withheld) |
| **02** | 0.33s | Wide greenhouse | `[134, 44, 378, 288]` | 44.5% | 26.5% | Broccoli (73.3%) | None (withheld) |
| **03** | 1.00s | Wide greenhouse | `[265, 44, 509, 288]` | 56.0% | 40.0% | Tomato (92.3%) | None (withheld) |
| **04** | 1.33s | Wide greenhouse | `[260, 44, 504, 288]` | 55.3% | 40.3% | Tomato (99.4%) | None (withheld) |
| **05** | 2.04s | Wide greenhouse | `[265, 44, 509, 288]` | 56.2% | 38.0% | Tomato (99.8%) | None (withheld) |
| **06** | 2.38s | Wide greenhouse | `[268, 44, 512, 288]` | 55.5% | 30.2% | Tomato (99.7%) | None (withheld) |
| **07** | 3.08s | Wide greenhouse | `[259, 44, 503, 288]` | 50.8% | 38.1% | Tomato (99.5%) | None (withheld) |
| **08** | 3.42s | Wide greenhouse | `[265, 44, 509, 288]` | 50.7% | 37.3% | Tomato (95.3%) | None (withheld) |
| **09** | 4.08s | Wide greenhouse | `[262, 44, 506, 288]` | 52.4% | 36.0% | Tomato (97.1%) | None (withheld) |
| **10** | 4.46s | **Macro Specimen** | `[112, 0, 400, 288]` | **87.1%** | **2.5%** | **Blueberry (100.0%)** | Masked out by Tomato |
| **11** | 5.12s | **Macro Specimen** | `[112, 0, 400, 288]` | **86.2%** | **2.6%** | **Blueberry (99.9%)** | Masked out by Tomato |
| **12** | 5.46s | **Macro Specimen** | `[112, 0, 400, 288]` | **86.5%** | **2.5%** | **Blueberry (100.0%)** | Masked out by Tomato |
| **13** | 6.17s | **Macro Specimen** | `[112, 0, 400, 288]` | **81.6%** | **1.8%** | **Blueberry (100.0%)** | Masked out by Tomato |
| **14** | 6.50s | **Macro Specimen** | `[112, 0, 400, 288]` | **65.8%** | **0.0%** | Corn (98.4%) | Masked out by Tomato |
| **15** | 7.21s | **Macro Specimen** | `[112, 0, 400, 288]` | **75.6%** | **0.0%** | **Blueberry (99.5%)** | Masked out by Tomato |
| **16** | 7.54s | **Macro Specimen** | `[112, 0, 400, 288]` | **74.2%** | **0.4%** | **Blueberry (99.3%)** | Masked out by Tomato |
| **17** | 8.21s | **Macro Specimen** | `[112, 0, 400, 288]` | **74.2%** | **0.3%** | **Blueberry (97.7%)** | Masked out by Tomato |
| **18** | 8.58s | Wide greenhouse | `[257, 44, 501, 288]` | 47.1% | 52.3% | Tomato (99.8%) | `tomato__yellow_leaf_curl_virus` (64.7%) |
| **19** | 9.25s | Wide greenhouse | `[256, 44, 500, 288]` | 46.8% | 52.3% | Tomato (99.9%) | `tomato__yellow_leaf_curl_virus` (77.1%) |
| **20** | 9.96s | Wide greenhouse | `[257, 44, 501, 288]` | 52.5% | 52.3% | Tomato (99.9%) | `tomato__yellow_leaf_curl_virus` (78.1%) |

---

## 3. Detailed Root Causes

### 3.1 Initial Frame Sampling & Filter Deficiencies
In `video/processor.py`, `FrameQualityFilter.evaluate()` only validates mean grayscale brightness (25 to 235) and Laplacian variance (>10.0). The wide greenhouse shot has high contrast metal mullions and glass boundaries, giving high blur scores (180–240), easily passing quality checks. The sampling engine extracted 20 frames across the video, drawing 12 wide-angle frames and 8 macro close-up frames.

### 3.2 Loose ROI Bounding Boxes & Background Contamination
In `model1_test_app/plant_detector.py`, `extract_tight_plant_rois()` handled wide/medium shots by:
- Taking external contours of any vegetation mask where `plant_density >= 0.25`.
- A 25% plant density threshold permits up to 75% of the bounding box to be completely non-plant background (glass panes, walls, white lab coats).
- When expanded to a square box with 1.08x padding, the bounding box spanned 244×244 pixels (85% of the frame height and 48% of the frame width), containing distant, out-of-focus background nursery tables.

### 3.3 Softmax Overconfidence on Cluttered Scenes
Because convolutional neural networks with softmax activation must normalize class probabilities to sum to 1.0, out-of-distribution inputs (such as distant greenhouse glass and tables) force one class to absorb residual probability mass. Model 1 arbitrarily assigned 92%–99.8% confidence to `tomato`. The pipeline accepted these frames as valid because `top_conf >= 0.40`.

### 3.4 Duplicate Frame Weighting and Simple Mean Aggregation
In `model1_test_app/video_inference.py`:
- Consecutive near-identical wide greenhouse frames (frames 3–9 and 18–20) were each appended to `valid_plant_prob_vectors`.
- `np.mean(valid_plant_prob_vectors, axis=0)` was used for final prediction.
- Out of 20 frames, 10 background frames predicted Tomato, 7 macro frames predicted Blueberry, 2 predicted Broccoli, and 1 predicted Corn.
- Simple averaging gave `Tomato: 49.3%`, `Blueberry: 35.0%`.

### 3.5 Misdiagnosis Cascade in Model 2
Because the consensus crop was erroneously determined as `tomato`:
- In `app/backend/services.py`, Model 2 was invoked with `crop_name="tomato"` across all frames.
- On the genuine blueberry close-ups (frames 10–17), genuine blueberry diseases (Mummy Berry and Anthracnose) were filtered out as incompatible with Tomato.
- On frames 18–20, Model 2 evaluated the background greenhouse nursery foliage under Tomato rules, detecting `tomato__yellow_leaf_curl_virus` at 64.7%, 77.1%, and 78.1%.
- Because exactly 3 supporting frames matched the `min_support_count = 3` threshold, Yellow Leaf Curl Virus was declared as the final diagnosed disease.
