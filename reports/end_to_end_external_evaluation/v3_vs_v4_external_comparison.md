# Model 2 V3 vs Model 2 V4 External Field Benchmark Comparison Report

**Date:** 2026-10-08 12:49:15  
**Evaluation Scope:** Locked 178-image external natural field benchmark across 13 target crops.  
**Strict Isolation Check:** Verified zero benchmark leakage; test sets and models unmodified.  
**Primary Verdict:** **V4 is BETTER**

---

## 1. Executive Summary & Overall Benchmark Metrics

| Metric | Model 2 V3 | Model 2 V4 | Absolute Delta | Relative Change |
| :--- | :--- | :--- | :--- | :--- |
| **Total Benchmark Images** | **178** | **178** | 0 | 100% evaluated |
| **Model 1 Crop Top-1 Accuracy** | **65.17%** | **65.17%** | 0.00% | Preserved identical |
| **End-to-End Complete Diagnosis Accuracy** | **21.91%** | **43.26%** | **+21.35%** | Improved |
| **Disease Accuracy (Post-Gating)** | **21.91%** | **43.26%** | **+21.35%** | Improved |
| **Raw Model 2 Top-1 Disease Accuracy** | **43.82%** | **64.61%** | **+20.79%** | Improved |
| **Disease Macro F1** | **16.31%** | **23.75%** | **+7.44%** | Improved |
| **Disease Weighted F1** | **29.52%** | **46.23%** | **+16.71%** | Improved |
| **Healthy Precision** | **0.00%** | **0.00%** | **+0.00%** | Unchanged |
| **Healthy Recall** | **0.00%** | **0.00%** | **+0.00%** | Unchanged |
| **Healthy F1-Score** | **0.00%** | **0.00%** | **+0.00%** | Unchanged |
| **Uncertain Prediction Rate** | **58.99%** | **39.89%** | **-19.10%** | Reduced uncertainty |
| **Mean Model 2 Prediction Confidence** | **0.6375** | **0.8718** | **+0.2343** | Calibration |
| **Correct Sample Mean Confidence** | **0.6679** | **0.9434** | **+0.2756** | Separation |
| **Incorrect Sample Mean Confidence** | **0.6290** | **0.8172** | **+0.1882** | Separation |

---

## 2. Priority Disease Classes Performance Analysis

Performance comparison on the key targeted field disease classes augmented in Model 2 V4:

| Priority Disease Class | External Support | V3 Acc (Post-Gating) | V4 Acc (Post-Gating) | Delta (Post-Gating) | V3 Raw Top-1 Acc | V4 Raw Top-1 Acc | Delta (Raw Top-1) | V3 Avg Conf | V4 Avg Conf |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `cucumber__powdery_mildew` | 20 | 15.0% | 20.0% | **+5.0%** | 20.0% | 25.0% | **+5.0%** | 0.6154 | 0.7841 |
| `tomato__early_blight` | 20 | 20.0% | 90.0% | **+70.0%** | 40.0% | 90.0% | **+50.0%** | 0.4997 | 0.9420 |
| `tomato__late_blight` | 20 | 20.0% | 55.0% | **+35.0%** | 20.0% | 65.0% | **+45.0%** | 0.5178 | 0.9136 |
| `tomato__leaf_mold` | 20 | 75.0% | 100.0% | **+25.0%** | 75.0% | 100.0% | **+25.0%** | 0.7474 | 0.9653 |
| `tomato__septoria_leaf_spot` | 20 | 40.0% | 95.0% | **+55.0%** | 40.0% | 95.0% | **+55.0%** | 0.6387 | 0.9580 |
| `zucchini__powdery_mildew` | 18 | 22.2% | 22.2% | **+0.0%** | 22.2% | 22.2% | **+0.0%** | 0.6484 | 0.8630 |

---

## 3. Key Disease Confusion Pairs Analysis

Analysis of specific critical confusion pairs identified during field testing:

| Ground Truth Class | Misclassified As | Priority Pair? | V3 Error Count | V4 Error Count | Delta | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `tomato__early_blight` | `tomato__septoria_leaf_spot` | Yes | 6 | 1 | -5 | **IMPROVED (fewer errors)** |
| `cucumber__powdery_mildew` | `zucchini__powdery_mildew` | Yes | 1 | 1 | +0 | **UNCHANGED** |
| `tomato__early_blight` | `tomato__late_blight` | Yes | 1 | 1 | +0 | **UNCHANGED** |
| `zucchini__powdery_mildew` | `cucumber__powdery_mildew` | Yes | 1 | 1 | +0 | **UNCHANGED** |
| `tomato__late_blight` | `tomato__early_blight` | Yes | 0 | 2 | +2 | **REGRESSED (more errors)** |
| `healthy` | `banana__bunchy_top` | No | 11 | 11 | +0 | **UNCHANGED** |
| `cucumber__powdery_mildew` | `cucumber__angular_leaf_spot` | No | 8 | 11 | +3 | **REGRESSED (more errors)** |
| `tomato__septoria_leaf_spot` | `healthy` | No | 7 | 0 | -7 | **IMPROVED (fewer errors)** |
| `tomato__late_blight` | `healthy` | No | 6 | 0 | -6 | **IMPROVED (fewer errors)** |
| `healthy` | `banana__black_leaf_streak` | No | 5 | 3 | -2 | **IMPROVED (fewer errors)** |
| `zucchini__powdery_mildew` | `cucumber__bacterial_wilt` | No | 5 | 3 | -2 | **IMPROVED (fewer errors)** |
| `zucchini__powdery_mildew` | `zucchini__bacterial_wilt` | No | 5 | 7 | +2 | **REGRESSED (more errors)** |
| `tomato__leaf_mold` | `healthy` | No | 4 | 0 | -4 | **IMPROVED (fewer errors)** |
| `banana__cordana_leaf_spot` | `banana__black_leaf_streak` | No | 3 | 3 | +0 | **UNCHANGED** |
| `cucumber__powdery_mildew` | `lettuce__downy_mildew` | No | 3 | 3 | +0 | **UNCHANGED** |

---

## 4. Per-Crop Accuracy Breakdown

| Crop | External Samples | Model 1 Top-1 Acc | V3 Disease Acc | V4 Disease Acc | V3 Complete Acc | V4 Complete Acc | Complete Delta |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `banana` | 44 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **+0.0%** |
| `bean` | 2 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | **+0.0%** |
| `cucumber` | 20 | 95.0% | 15.0% | 20.0% | 15.0% | 20.0% | **+5.0%** |
| `peach` | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **+0.0%** |
| `soybean` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **+0.0%** |
| `tomato` | 80 | 97.5% | 38.8% | 85.0% | 38.8% | 85.0% | **+46.2%** |
| `wheat` | 8 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **+0.0%** |
| `zucchini` | 18 | 100.0% | 22.2% | 22.2% | 22.2% | 22.2% | **+0.0%** |

---

## 5. Verification & Integrity Checklist

- [x] **Benchmark Image Count:** Exactly 178 unseen natural field images.
- [x] **V3 Evaluated on All 178:** Yes (178/178 complete).
- [x] **V4 Evaluated on All 178:** Yes (178/178 complete).
- [x] **Benchmark SHA-256 Manifest Unchanged:** Yes, verified against `data/external/end_to_end_test/manifest.csv`.
- [x] **Zero Benchmark Leakage:** No benchmark images were copied into training or validation directories.
- [x] **Model 1 Untouched:** Weights and inference configuration unchanged.
- [x] **Model 2 V3 Checkpoint Untouched:** `models/model2_classifier_v3/best_model.pth` verified.
- [x] **Model 2 V4 Checkpoint Untouched:** `models/model2_classifier_v4/best_model.pth` verified.
- [x] **Immutable Test Set Integrity:** 2,304-image test set remains strictly held-out and unchanged.

---

## 6. Conclusion & Recommendation

### Verdict: **BETTER**

### Detailed Analysis:
1. **Targeted Field Generalization:** 
   - Model 2 V4 was trained with targeted real-field images for priority classes (`tomato__early_blight`, `tomato__late_blight`, `tomato__septoria_leaf_spot`, `cucumber__powdery_mildew`, `tomato__leaf_mold`).
   - Comparing Macro F1 on the 178 external field images: **V3 = 16.31%** vs **V4 = 23.75%** (+7.44%).
   - Complete end-to-end diagnosis accuracy: **V3 = 21.91%** vs **V4 = 43.26%** (+21.35%).

2. **Priority Class Highlights:**
   - Review of priority classes shows tangible improvements in real-world discrimination between closely resembling foliar pathogens (e.g. early blight vs septoria).

3. **Production Recommendation:**
   - In accordance with instructions, **Model 2 V4 has NOT been automatically promoted to production**, and `app/backend` configuration has remained untouched.
   - The team can review these comparative metrics before deciding on production deployment.
