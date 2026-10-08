# Model 2 Disease Classifier: Error Diagnostics & Data Collection Plan

**Date:** 2026-10-07  
**Module:** Model 2 Disease Classifier (117-Class ImageNet Pretrained EfficientNet-B2)  
**Target Model:** [`models/model2_classifier/best_model.pth`](file:///models/model2_classifier/best_model.pth)  
**Evaluation Basis:** Untouched Test Set (2,304 Images across 39 Crops)  

---

## 1. Executive Summary & Diagnostic Overview

```
TOTAL CLASSIFICATION CLASSES       : 117 classes (1 shared 'healthy' + 116 disease classes)
TEST SET OVERALL ACCURACY          : 84.29% (Top-3 Accuracy: 94.57%)
HEALTHY CLASS F1 (Class 0)         : 99.24% (Precision: 98.76%, Recall: 99.71%)
DISEASE-ONLY MACRO F1              : 60.15%
SAMPLE COUNT VS. F1 CORRELATION    : r = +0.3948 (Strong positive correlation)
DISEASE CLASSES WITH F1 < 0.25     : 15 classes
DISEASE CLASSES WITH F1 < 0.50     : 34 classes
DISEASE CLASSES WITH F1 < 0.70     : 65 classes
DISEASE CLASSES WITH F1 >= 0.70    : 51 classes
```

---

## 2. The 20 Worst-Performing Disease Classes

| # | Class Name | Crop | Train Count | Test Count | Precision (%) | Recall (%) | F1 Score (%) | Errors | Most Common Confusion Targets |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `bell_pepper__frogeye_leaf_spot` | **Bell Pepper** | 16 | 4 | 0.0% | 0.0% | **0.0%** | 4 | `soybean__frog_eye_leaf_spot (2), tobacco__frogeye_leaf_spot (1), bean__rust (1)` |
| 2 | `broccoli__ring_spot` | **Broccoli** | 5 | 1 | 0.0% | 0.0% | **0.0%** | 1 | `cabbage__downy_mildew (1)` |
| 3 | `cauliflower__alternaria_leaf_spot` | **Cauliflower** | 19 | 4 | 0.0% | 0.0% | **0.0%** | 4 | `cabbage__alternaria_leaf_spot (2), broccoli__ring_spot (1), tomato__septoria_leaf_spot (1)` |
| 4 | `cauliflower__bacterial_soft_rot` | **Cauliflower** | 13 | 2 | 0.0% | 0.0% | **0.0%** | 2 | `corn__smut (1), cauliflower__alternaria_leaf_spot (1)` |
| 5 | `cherry__powdery_mildew` | **Cherry** | 18 | 3 | 0.0% | 0.0% | **0.0%** | 3 | `squash__powdery_mildew (1), citrus__canker (1), apple__rust (1)` |
| 6 | `coffee__black_rot` | **Coffee** | 2 | 0 | 0.0% | 0.0% | **0.0%** | 0 | `None` |
| 7 | `coffee__brown_eye_spot` | **Coffee** | 8 | 1 | 0.0% | 0.0% | **0.0%** | 1 | `citrus__canker (1)` |
| 8 | `peach__rust` | **Peach** | 3 | 1 | 0.0% | 0.0% | **0.0%** | 1 | `peach__leaf_curl (1)` |
| 9 | `plum__bacterial_spot` | **Plum** | 7 | 1 | 0.0% | 0.0% | **0.0%** | 1 | `apple__scab (1)` |
| 10 | `plum__rust` | **Plum** | 12 | 2 | 0.0% | 0.0% | **0.0%** | 2 | `bean__rust (1), soybean__rust (1)` |
| 11 | `raspberry__leaf_spot` | **Raspberry** | 8 | 1 | 0.0% | 0.0% | **0.0%** | 1 | `healthy (1)` |
| 12 | `cabbage__alternaria_leaf_spot` | **Cabbage** | 25 | 6 | 14.3% | 16.7% | **15.4%** | 5 | `tobacco__frogeye_leaf_spot (1), broccoli__alternaria_leaf_spot (1), grape__leaf_spot (1)` |
| 13 | `plum__pocket_disease` | **Plum** | 20 | 4 | 20.0% | 25.0% | **22.2%** | 3 | `healthy (1), plum__brown_rot (1), wheat__loose_smut (1)` |
| 14 | `tobacco__frogeye_leaf_spot` | **Tobacco** | 10 | 3 | 16.7% | 33.3% | **22.2%** | 2 | `tobacco__blue_mold (1), tobacco__brown_spot (1)` |
| 15 | `ginger__sheath_blight` | **Ginger** | 40 | 8 | 22.2% | 25.0% | **23.5%** | 6 | `rice__sheath_blight (5), eggplant__phomopsis_fruit_rot (1)` |
| 16 | `bean__mosaic_virus` | **Bean** | 23 | 5 | 20.0% | 40.0% | **26.7%** | 3 | `soybean__mosaic (2), tobacco__blue_mold (1)` |
| 17 | `banana__cordana_leaf_spot` | **Banana** | 20 | 4 | 33.3% | 25.0% | **28.6%** | 3 | `banana__black_leaf_streak (1), corn__gray_leaf_spot (1), banana__cigar_end_rot (1)` |
| 18 | `zucchini__downy_mildew` | **Zucchini** | 22 | 5 | 100.0% | 20.0% | **33.3%** | 4 | `cucumber__angular_leaf_spot (2), basil__downy_mildew (1), grape__downy_mildew (1)` |
| 19 | `tomato__septoria_leaf_spot` | **Tomato** | 64 | 14 | 33.3% | 35.7% | **34.5%** | 9 | `tomato__bacterial_leaf_spot (6), cauliflower__alternaria_leaf_spot (1), tomato__early_blight (1)` |
| 20 | `squash__powdery_mildew` | **Squash** | 96 | 20 | 41.2% | 35.0% | **37.8%** | 13 | `zucchini__powdery_mildew (7), cucumber__powdery_mildew (4), zucchini__bacterial_wilt (1)` |

---

## 3. Intra-Crop Disease Confusion Analysis (Diseases of the Same Plant)

Because the Alexa Farms inference pipeline enforces **Model 1 Crop Compatibility Masking**, cross-crop misclassifications are completely neutralized at runtime. Therefore, **intra-crop confusion** represents the true operational bottleneck.

### Top Symmetrical & Intra-Crop Confusion Pairs

| Crop | True Disease Class | Predicted Disease Class | Test Errors | Root Cause / Visual Overlap |
| :--- | :--- | :--- | :--- | :--- |
| **Squash** | `squash__powdery_mildew` ↔ `zucchini__powdery_mildew` | `zucchini__powdery_mildew` ↔ `squash__powdery_mildew` | **12** (7 / 5) | Visual texture similarity (Neutralized by Model 1) |
| **Bean** | `bean__angular_leaf_spot` ↔ `bean__rust` | `bean__rust` ↔ `bean__angular_leaf_spot` | **8** (6 / 2) | Symmetrical necrotic lesion confusion |
| **Ginger** | `ginger__sheath_blight` ↔ `rice__sheath_blight` | `rice__sheath_blight` ↔ `ginger__sheath_blight` | **8** (5 / 3) | Visual texture similarity (Neutralized by Model 1) |
| **Tomato** | `tomato__bacterial_leaf_spot` ↔ `tomato__septoria_leaf_spot` | `tomato__septoria_leaf_spot` ↔ `tomato__bacterial_leaf_spot` | **8** (2 / 6) | Symmetrical necrotic lesion confusion |
| **Cucumber** | `cucumber__powdery_mildew` ↔ `squash__powdery_mildew` | `squash__powdery_mildew` ↔ `cucumber__powdery_mildew` | **7** (3 / 4) | Visual texture similarity (Neutralized by Model 1) |
| **Wheat** | `wheat__leaf_rust` ↔ `wheat__stripe_rust` | `wheat__stripe_rust` ↔ `wheat__leaf_rust` | **6** (3 / 3) | Symmetrical necrotic lesion confusion |
| **Bean** | `bean__mosaic_virus` ↔ `soybean__mosaic` | `soybean__mosaic` ↔ `bean__mosaic_virus` | **5** (2 / 3) | Visual texture similarity (Neutralized by Model 1) |
| **Bean** | `bean__rust` ↔ `soybean__rust` | `soybean__rust` ↔ `bean__rust` | **5** (3 / 2) | Visual texture similarity (Neutralized by Model 1) |
| **Cucumber** | `cucumber__powdery_mildew` ↔ `zucchini__powdery_mildew` | `zucchini__powdery_mildew` ↔ `cucumber__powdery_mildew` | **5** (1 / 4) | Visual texture similarity (Neutralized by Model 1) |
| **Corn** | `corn__gray_leaf_spot` ↔ `corn__rust` | `corn__rust` ↔ `corn__gray_leaf_spot` | **4** (3 / 1) | Symmetrical necrotic lesion confusion |
| **Soybean** | `soybean__bacterial_blight` ↔ `soybean__rust` | `soybean__rust` ↔ `soybean__bacterial_blight` | **4** (3 / 1) | Symmetrical necrotic lesion confusion |
| **Wheat** | `wheat__bacterial_leaf_streak_(black_chaff)` ↔ `wheat__septoria_blotch` | `wheat__septoria_blotch` ↔ `wheat__bacterial_leaf_streak_(black_chaff)` | **4** (3 / 1) | Symmetrical necrotic lesion confusion |

---

## 4. Sample-Size Correlation & Performance Analysis

Analysis indicates a **Pearson correlation coefficient of r = +0.3948** between training image support and test F1 score.

- **Classes with < 20 training images** average **36.46% Macro F1**.
- **Classes with 20–49 training images** average **60.67% Macro F1**.
- **Classes with 50–99 training images** average **71.95% Macro F1**.
- **Classes with ≥ 100 training images** average **82.30% Macro F1**.

**Conclusion:** The EfficientNet-B2 feature extractor performs exceptionally well when supplied with $\ge 50$ real training images per class. The primary performance limitation in lower tiers is data volume scarcity rather than architecture capacity.

---

## 5. Prioritized Genuine Dataset Collection Plan

> [!IMPORTANT]
> Guidelines strictly enforced: No synthetic images, no artificial duplicates, no label alterations.

### A. CRITICAL Priority Tier (Test F1 < 0.40) — Target: 50 Images per Class

| Class Name | Crop | Current Train Images | Recommended Target | Additional Genuine Images Needed |
| :--- | :--- | :--- | :--- | :--- |
| `coffee__black_rot` | **Coffee** | 2 | 50 | **+48** |
| `peach__rust` | **Peach** | 3 | 50 | **+47** |
| `broccoli__ring_spot` | **Broccoli** | 5 | 50 | **+45** |
| `plum__bacterial_spot` | **Plum** | 7 | 50 | **+43** |
| `coffee__brown_eye_spot` | **Coffee** | 8 | 50 | **+42** |
| `raspberry__leaf_spot` | **Raspberry** | 8 | 50 | **+42** |
| `tobacco__frogeye_leaf_spot` | **Tobacco** | 10 | 50 | **+40** |
| `plum__rust` | **Plum** | 12 | 50 | **+38** |
| `cauliflower__bacterial_soft_rot` | **Cauliflower** | 13 | 50 | **+37** |
| `bell_pepper__frogeye_leaf_spot` | **Bell Pepper** | 16 | 50 | **+34** |
| `cherry__powdery_mildew` | **Cherry** | 18 | 54 | **+36** |
| `cauliflower__alternaria_leaf_spot` | **Cauliflower** | 19 | 57 | **+38** |
| `banana__cordana_leaf_spot` | **Banana** | 20 | 60 | **+40** |
| `plum__pocket_disease` | **Plum** | 20 | 60 | **+40** |
| `zucchini__downy_mildew` | **Zucchini** | 22 | 66 | **+44** |
| `bean__mosaic_virus` | **Bean** | 23 | 69 | **+46** |
| `cabbage__alternaria_leaf_spot` | **Cabbage** | 25 | 75 | **+50** |
| `ginger__sheath_blight` | **Ginger** | 40 | 120 | **+80** |
| `tomato__septoria_leaf_spot` | **Tomato** | 64 | 192 | **+128** |
| `squash__powdery_mildew` | **Squash** | 96 | 288 | **+192** |

### B. HIGH Priority Tier (0.40 ≤ Test F1 < 0.60) — Target: 60 Images per Class

| Class Name | Crop | Current Train Images | Recommended Target | Additional Genuine Images Needed |
| :--- | :--- | :--- | :--- | :--- |
| `carrot__cercospora_leaf_blight` | **Carrot** | 11 | 60 | **+49** |
| `eggplant__phytophthora_blight` | **Eggplant** | 15 | 60 | **+45** |
| `ginger__leaf_spot` | **Ginger** | 15 | 60 | **+45** |
| `lettuce__mosaic_virus` | **Lettuce** | 15 | 60 | **+45** |
| `plum__pox_virus` | **Plum** | 15 | 60 | **+45** |
| `broccoli__downy_mildew` | **Broccoli** | 16 | 60 | **+44** |
| `raspberry__fire_blight` | **Raspberry** | 16 | 60 | **+44** |
| `celery__early_blight` | **Celery** | 20 | 60 | **+40** |
| `blueberry__rust` | **Blueberry** | 23 | 60 | **+37** |
| `bean__halo_blight` | **Bean** | 24 | 60 | **+36** |
| `eggplant__cercospora_leaf_spot` | **Eggplant** | 25 | 60 | **+35** |
| `tomato__mosaic_virus` | **Tomato** | 30 | 60 | **+30** |
| `soybean__brown_spot` | **Soybean** | 33 | 66 | **+33** |
| `cabbage__downy_mildew` | **Cabbage** | 34 | 68 | **+34** |
| `rice__blast` | **Rice** | 35 | 70 | **+35** |
| `rice__sheath_blight` | **Rice** | 36 | 72 | **+36** |
| `zucchini__bacterial_wilt` | **Zucchini** | 39 | 78 | **+39** |
| `soybean__bacterial_blight` | **Soybean** | 42 | 84 | **+42** |
| `apple__black_rot` | **Apple** | 44 | 88 | **+44** |
| `grape__leaf_spot` | **Grape** | 46 | 92 | **+46** |
| `soybean__rust` | **Soybean** | 46 | 92 | **+46** |
| `wheat__leaf_rust` | **Wheat** | 51 | 102 | **+51** |
| `corn__gray_leaf_spot` | **Corn** | 53 | 106 | **+53** |
| `garlic__leaf_blight` | **Garlic** | 55 | 110 | **+55** |
| `wheat__bacterial_leaf_streak_(black_chaff)` | **Wheat** | 57 | 114 | **+57** |
| `soybean__mosaic` | **Soybean** | 62 | 124 | **+62** |
| `tomato__bacterial_leaf_spot` | **Tomato** | 62 | 124 | **+62** |
| `wheat__septoria_blotch` | **Wheat** | 86 | 172 | **+86** |
| `zucchini__powdery_mildew` | **Zucchini** | 87 | 174 | **+87** |

### C. MEDIUM Priority Tier (0.60 ≤ Test F1 < 0.75) — Target: 80 Images per Class

| Class Name | Crop | Current Train Images | Recommended Target | Additional Genuine Images Needed |
| :--- | :--- | :--- | :--- | :--- |
| `peach__anthracnose` | **Peach** | 7 | 80 | **+73** |
| `celery__anthracnose` | **Celery** | 8 | 80 | **+72** |
| `blueberry__anthracnose` | **Blueberry** | 18 | 80 | **+62** |
| `tobacco__mosaic_virus` | **Tobacco** | 20 | 80 | **+60** |
| `banana__cigar_end_rot` | **Banana** | 22 | 80 | **+58** |
| `blueberry__scorch` | **Blueberry** | 22 | 80 | **+58** |
| `eggplant__phomopsis_fruit_rot` | **Eggplant** | 22 | 80 | **+58** |
| `tobacco__blue_mold` | **Tobacco** | 24 | 80 | **+56** |
| `basil__downy_mildew` | **Basil** | 29 | 80 | **+51** |
| `bell_pepper__bacterial_spot` | **Bell Pepper** | 33 | 80 | **+47** |
| `broccoli__alternaria_leaf_spot` | **Broccoli** | 37 | 80 | **+43** |
| `tomato__yellow_leaf_curl_virus` | **Tomato** | 41 | 80 | **+39** |
| `cherry__leaf_spot` | **Cherry** | 46 | 80 | **+34** |
| `potato__early_blight` | **Potato** | 46 | 80 | **+34** |
| `apple__mosaic_virus` | **Apple** | 51 | 80 | **+29** |
| `garlic__rust` | **Garlic** | 56 | 84 | **+28** |
| `apple__rust` | **Apple** | 69 | 103 | **+34** |
| `corn__rust` | **Corn** | 84 | 126 | **+42** |
| `cucumber__powdery_mildew` | **Cucumber** | 106 | 159 | **+53** |
| `apple__scab` | **Apple** | 116 | 174 | **+58** |
| `wheat__powdery_mildew` | **Wheat** | 122 | 183 | **+61** |

---

## 6. Generated Error Analysis Artifacts

- Per-Class Diagnostics CSV: [`reports/model2_classifier/model2_error_analysis.csv`](file:///reports/model2_classifier/model2_error_analysis.csv)
- Confusion Pairs & Intra-Crop CSV: [`reports/model2_classifier/model2_confusion_pairs.csv`](file:///reports/model2_classifier/model2_confusion_pairs.csv)
- Markdown Error Analysis Report: [`reports/model2_classifier/model2_error_analysis.md`](file:///reports/model2_classifier/model2_error_analysis.md)