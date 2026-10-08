# Model 2 Disease Classifier v2 Final Training & Evaluation Report

**Date:** 2026-10-07  
**Model Architecture:** `EfficientNet-B2` (117 Classes, PyTorch Transfer Learning)  
**Best Checkpoint:** [`models/model2_classifier_v2/best_model.pth`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\models\model2_classifier_v2\best_model.pth) (Selected at Epoch 2)  
**Evaluation Split:** Immutable Model 2 Test Set (2,304 Images)  

---

## 1. Executive Summary & Baseline Comparison

| Metric | Baseline (v1) | Final V2 Model | Absolute Change | Relative Change (%) | Status |
|---|---:|---:|---:|---:|:---:|
| **Top-1 Accuracy** | 84.29% | **85.98%** | +1.69% | +2.01% | IMPROVED |
| **Top-3 Accuracy** | 94.57% | **95.62%** | +1.05% | +1.11% | IMPROVED |
| **Macro F1 (All 117)** | 61.01% | **65.29%** | +4.28% | +7.01% | IMPROVED |
| **Disease-only Macro F1** | 60.15% | **64.43%** | +4.28% | +7.12% | IMPROVED |
| **Healthy F1 (Class 0)** | 99.24% | **99.47%** | +0.23% | +0.23% | PRESERVED |
| **Weighted F1** | N/A | **85.87%** | — | — | — |

---

## 2. Key Priority Disease Focus & Weak-Class Relief

| Target Disease Class | Baseline F1 | Final V2 F1 | Absolute Change | Test Precision | Test Recall | Test Support | Impact |
|---|---:|---:|---:|---:|---:|---:|---|
| `soybean__rust` | 41.67% | **42.86%** | +1.19% | 60.00% | 33.33% | 9 | IMPROVED |
| `plum__rust` | 0.00% | **0.00%** | +0.00% | 0.00% | 0.00% | 2 | UNCHANGED |
| `cauliflower__alternaria_leaf_spot` | 0.00% | **0.00%** | +0.00% | 0.00% | 0.00% | 4 | UNCHANGED |
| `cauliflower__bacterial_soft_rot` | 0.00% | **66.67%** | +66.67% | 100.00% | 50.00% | 2 | **MAJOR RELIEF** |
| `cherry__powdery_mildew` | 0.00% | **0.00%** | +0.00% | 0.00% | 0.00% | 3 | UNCHANGED |
| `raspberry__leaf_spot` | 0.00% | **0.00%** | +0.00% | 0.00% | 0.00% | 1 | UNCHANGED |
| `plum__bacterial_spot` | 0.00% | **0.00%** | +0.00% | 0.00% | 0.00% | 1 | UNCHANGED |
| `bell_pepper__frogeye_leaf_spot` | 0.00% | **28.57%** | +28.57% | 33.33% | 25.00% | 4 | **MAJOR RELIEF** |
| `broccoli__ring_spot` | 0.00% | **0.00%** | +0.00% | 0.00% | 0.00% | 1 | UNCHANGED |
| `coffee__black_rot` | 0.00% | **0.00%** | +0.00% | 0.00% | 0.00% | 0 | UNCHANGED |
| `coffee__brown_eye_spot` | 0.00% | **0.00%** | +0.00% | 0.00% | 0.00% | 1 | UNCHANGED |
| `peach__rust` | 0.00% | **0.00%** | +0.00% | 0.00% | 0.00% | 1 | UNCHANGED |
| `cabbage__alternaria_leaf_spot` | 15.38% | **14.29%** | -1.09% | 12.50% | 16.67% | 6 | DEGRADED |
| `plum__pocket_disease` | 22.22% | **44.44%** | +22.22% | 40.00% | 50.00% | 4 | **MAJOR RELIEF** |
| `tobacco__frogeye_leaf_spot` | 22.22% | **33.33%** | +11.11% | 33.33% | 33.33% | 3 | IMPROVED |
| `ginger__sheath_blight` | 23.53% | **42.86%** | +19.33% | 50.00% | 37.50% | 8 | **MAJOR RELIEF** |
| `bean__mosaic_virus` | 26.67% | **18.18%** | -8.49% | 11.76% | 40.00% | 5 | DEGRADED |
| `banana__cordana_leaf_spot` | 28.57% | **50.00%** | +21.43% | 37.50% | 75.00% | 4 | **MAJOR RELIEF** |
| `zucchini__downy_mildew` | 33.33% | **57.14%** | +23.81% | 100.00% | 40.00% | 5 | **MAJOR RELIEF** |
| `tomato__septoria_leaf_spot` | 34.48% | **48.28%** | +13.80% | 46.67% | 50.00% | 14 | IMPROVED |
| `squash__powdery_mildew` | 37.84% | **47.83%** | +9.99% | 42.31% | 55.00% | 20 | IMPROVED |

---

## 3. Soybean Rust & Healthy Class Verification

### `soybean__rust` Performance:
- **Baseline Test F1:** 41.67%
- **Final V2 Test F1:** **42.86%** (Precision: 60.00%, Recall: 33.33%, Support: 9)
- **Training Support:** Expanded from 46 to **455 images (+889%)**.

### `healthy` Class Performance:
- **Baseline Healthy F1:** 99.24%
- **Final V2 Healthy F1:** **99.47%** (Precision: 99.61%, Recall: 99.33%, Support: 1041)

---

## 4. Complete 117-Class Performance Table

| Class ID | Class Name | Precision | Recall | F1 Score | Test Support | Baseline F1 | Change |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | `healthy` | 99.61% | 99.33% | **99.47%** | 1041 | 99.24% | +0.23% |
| 1 | `apple__black_rot` | 50.00% | 40.00% | **44.44%** | 10 | 50.00% | -5.56% |
| 2 | `apple__mosaic_virus` | 64.29% | 81.82% | **72.00%** | 11 | 72.73% | -0.73% |
| 3 | `apple__rust` | 86.67% | 92.86% | **89.66%** | 14 | 72.00% | +17.66% |
| 4 | `apple__scab` | 90.00% | 72.00% | **80.00%** | 25 | 66.67% | +13.33% |
| 5 | `banana__anthracnose` | 85.71% | 85.71% | **85.71%** | 7 | 93.33% | -7.62% |
| 6 | `banana__black_leaf_streak` | 88.24% | 88.24% | **88.24%** | 17 | 81.08% | +7.16% |
| 7 | `banana__bunchy_top` | 90.00% | 81.82% | **85.71%** | 11 | 95.24% | -9.53% |
| 8 | `banana__cigar_end_rot` | 60.00% | 75.00% | **66.67%** | 4 | 66.67% | -0.00% |
| 9 | `banana__cordana_leaf_spot` | 37.50% | 75.00% | **50.00%** | 4 | 28.57% | +21.43% |
| 10 | `banana__panama_disease` | 87.50% | 87.50% | **87.50%** | 8 | 87.50% | +0.00% |
| 11 | `basil__downy_mildew` | 85.71% | 100.00% | **92.31%** | 6 | 66.67% | +25.64% |
| 12 | `bean__angular_leaf_spot` | 95.24% | 92.31% | **93.75%** | 65 | 93.65% | +0.10% |
| 13 | `bean__halo_blight` | 55.56% | 83.33% | **66.67%** | 6 | 40.00% | +26.67% |
| 14 | `bean__mosaic_virus` | 11.76% | 40.00% | **18.18%** | 5 | 26.67% | -8.49% |
| 15 | `bean__rust` | 80.95% | 88.31% | **84.47%** | 77 | 84.81% | -0.34% |
| 16 | `bell_pepper__bacterial_spot` | 75.00% | 42.86% | **54.55%** | 7 | 60.00% | -5.45% |
| 17 | `bell_pepper__blossom_end_rot` | 64.71% | 100.00% | **78.57%** | 11 | 84.62% | -6.05% |
| 18 | `bell_pepper__frogeye_leaf_spot` | 33.33% | 25.00% | **28.57%** | 4 | 0.00% | +28.57% |
| 19 | `bell_pepper__powdery_mildew` | 66.67% | 100.00% | **80.00%** | 2 | 80.00% | +0.00% |
| 20 | `blueberry__anthracnose` | 50.00% | 50.00% | **50.00%** | 4 | 66.67% | -16.67% |
| 21 | `blueberry__botrytis_blight` | 75.00% | 100.00% | **85.71%** | 3 | 80.00% | +5.71% |
| 22 | `blueberry__mummy_berry` | 60.00% | 75.00% | **66.67%** | 4 | 75.00% | -8.33% |
| 23 | `blueberry__rust` | 50.00% | 40.00% | **44.44%** | 5 | 54.55% | -10.11% |
| 24 | `blueberry__scorch` | 75.00% | 60.00% | **66.67%** | 5 | 60.00% | +6.67% |
| 25 | `broccoli__alternaria_leaf_spot` | 100.00% | 25.00% | **40.00%** | 8 | 61.54% | -21.54% |
| 26 | `broccoli__downy_mildew` | 66.67% | 50.00% | **57.14%** | 4 | 57.14% | +0.00% |
| 27 | `broccoli__ring_spot` | 0.00% | 0.00% | **0.00%** | 1 | 0.00% | +0.00% |
| 28 | `cabbage__alternaria_leaf_spot` | 12.50% | 16.67% | **14.29%** | 6 | 15.38% | -1.09% |
| 29 | `cabbage__black_rot` | 76.47% | 100.00% | **86.67%** | 13 | 85.71% | +0.96% |
| 30 | `cabbage__downy_mildew` | 60.00% | 75.00% | **66.67%** | 8 | 50.00% | +16.67% |
| 31 | `carrot__alternaria_leaf_blight` | 85.71% | 85.71% | **85.71%** | 7 | 75.00% | +10.71% |
| 32 | `carrot__cavity_spot` | 100.00% | 100.00% | **100.00%** | 7 | 100.00% | +0.00% |
| 33 | `carrot__cercospora_leaf_blight` | 100.00% | 33.33% | **50.00%** | 3 | 40.00% | +10.00% |
| 34 | `cauliflower__alternaria_leaf_spot` | 0.00% | 0.00% | **0.00%** | 4 | 0.00% | +0.00% |
| 35 | `cauliflower__bacterial_soft_rot` | 100.00% | 50.00% | **66.67%** | 2 | 0.00% | +66.67% |
| 36 | `celery__anthracnose` | 25.00% | 100.00% | **40.00%** | 1 | 66.67% | -26.67% |
| 37 | `celery__early_blight` | 75.00% | 60.00% | **66.67%** | 5 | 44.44% | +22.23% |
| 38 | `cherry__leaf_spot` | 57.14% | 40.00% | **47.06%** | 10 | 66.67% | -19.61% |
| 39 | `cherry__powdery_mildew` | 0.00% | 0.00% | **0.00%** | 3 | 0.00% | +0.00% |
| 40 | `citrus__canker` | 88.24% | 93.75% | **90.91%** | 48 | 89.80% | +1.11% |
| 41 | `citrus__greening_disease` | 81.25% | 92.86% | **86.67%** | 14 | 77.42% | +9.25% |
| 42 | `coffee__berry_blotch` | 88.89% | 88.89% | **88.89%** | 9 | 84.21% | +4.68% |
| 43 | `coffee__black_rot` | 0.00% | 0.00% | **0.00%** | 0 | 0.00% | +0.00% |
| 44 | `coffee__brown_eye_spot` | 0.00% | 0.00% | **0.00%** | 1 | 0.00% | +0.00% |
| 45 | `coffee__leaf_rust` | 93.75% | 93.75% | **93.75%** | 16 | 83.87% | +9.88% |
| 46 | `corn__gray_leaf_spot` | 60.00% | 50.00% | **54.55%** | 12 | 47.62% | +6.93% |
| 47 | `corn__northern_leaf_blight` | 70.59% | 85.71% | **77.42%** | 14 | 81.48% | -4.06% |
| 48 | `corn__rust` | 75.00% | 66.67% | **70.59%** | 18 | 72.73% | -2.14% |
| 49 | `corn__smut` | 94.74% | 94.74% | **94.74%** | 19 | 94.74% | -0.00% |
| 50 | `cucumber__angular_leaf_spot` | 95.24% | 90.91% | **93.02%** | 22 | 91.30% | +1.72% |
| 51 | `cucumber__bacterial_wilt` | 90.91% | 76.92% | **83.33%** | 13 | 92.31% | -8.98% |
| 52 | `cucumber__powdery_mildew` | 68.18% | 68.18% | **68.18%** | 22 | 69.39% | -1.21% |
| 53 | `eggplant__cercospora_leaf_spot` | 57.14% | 66.67% | **61.54%** | 6 | 44.44% | +17.10% |
| 54 | `eggplant__phomopsis_fruit_rot` | 100.00% | 80.00% | **88.89%** | 5 | 60.00% | +28.89% |
| 55 | `eggplant__phytophthora_blight` | 100.00% | 50.00% | **66.67%** | 4 | 40.00% | +26.67% |
| 56 | `garlic__leaf_blight` | 61.54% | 66.67% | **64.00%** | 12 | 50.00% | +14.00% |
| 57 | `garlic__rust` | 81.82% | 75.00% | **78.26%** | 12 | 66.67% | +11.59% |
| 58 | `ginger__leaf_spot` | 60.00% | 75.00% | **66.67%** | 4 | 50.00% | +16.67% |
| 59 | `ginger__sheath_blight` | 50.00% | 37.50% | **42.86%** | 8 | 23.53% | +19.33% |
| 60 | `grape__black_rot` | 68.75% | 84.62% | **75.86%** | 13 | 81.48% | -5.62% |
| 61 | `grape__downy_mildew` | 86.21% | 78.12% | **81.97%** | 32 | 80.00% | +1.97% |
| 62 | `grape__grapevine_leafroll_disease` | 44.44% | 80.00% | **57.14%** | 5 | 83.33% | -26.19% |
| 63 | `grape__leaf_spot` | 80.00% | 40.00% | **53.33%** | 10 | 58.82% | -5.49% |
| 64 | `lettuce__downy_mildew` | 85.71% | 75.00% | **80.00%** | 8 | 80.00% | +0.00% |
| 65 | `lettuce__mosaic_virus` | 100.00% | 50.00% | **66.67%** | 4 | 50.00% | +16.67% |
| 66 | `maple__tar_spot` | 100.00% | 100.00% | **100.00%** | 8 | 100.00% | +0.00% |
| 67 | `peach__anthracnose` | 33.33% | 100.00% | **50.00%** | 1 | 66.67% | -16.67% |
| 68 | `peach__brown_rot` | 85.71% | 85.71% | **85.71%** | 14 | 92.86% | -7.15% |
| 69 | `peach__leaf_curl` | 94.74% | 100.00% | **97.30%** | 18 | 92.31% | +4.99% |
| 70 | `peach__rust` | 0.00% | 0.00% | **0.00%** | 1 | 0.00% | +0.00% |
| 71 | `peach__scab` | 88.89% | 100.00% | **94.12%** | 8 | 88.89% | +5.23% |
| 72 | `plum__bacterial_spot` | 0.00% | 0.00% | **0.00%** | 1 | 0.00% | +0.00% |
| 73 | `plum__brown_rot` | 83.33% | 100.00% | **90.91%** | 5 | 83.33% | +7.58% |
| 74 | `plum__pocket_disease` | 40.00% | 50.00% | **44.44%** | 4 | 22.22% | +22.22% |
| 75 | `plum__pox_virus` | 100.00% | 50.00% | **66.67%** | 4 | 40.00% | +26.67% |
| 76 | `plum__rust` | 0.00% | 0.00% | **0.00%** | 2 | 0.00% | +0.00% |
| 77 | `potato__early_blight` | 62.50% | 50.00% | **55.56%** | 10 | 73.68% | -18.12% |
| 78 | `potato__late_blight` | 84.62% | 91.67% | **88.00%** | 12 | 83.33% | +4.67% |
| 79 | `raspberry__fire_blight` | 75.00% | 75.00% | **75.00%** | 4 | 50.00% | +25.00% |
| 80 | `raspberry__gray_mold` | 100.00% | 100.00% | **100.00%** | 2 | 100.00% | +0.00% |
| 81 | `raspberry__leaf_spot` | 0.00% | 0.00% | **0.00%** | 1 | 0.00% | +0.00% |
| 82 | `raspberry__yellow_rust` | 100.00% | 100.00% | **100.00%** | 4 | 100.00% | +0.00% |
| 83 | `rice__blast` | 57.14% | 57.14% | **57.14%** | 7 | 50.00% | +7.14% |
| 84 | `rice__sheath_blight` | 55.56% | 62.50% | **58.82%** | 8 | 45.45% | +13.37% |
| 85 | `soybean__bacterial_blight` | 50.00% | 66.67% | **57.14%** | 9 | 47.62% | +9.52% |
| 86 | `soybean__brown_spot` | 50.00% | 42.86% | **46.15%** | 7 | 40.00% | +6.15% |
| 87 | `soybean__downy_mildew` | 91.67% | 100.00% | **95.65%** | 11 | 83.33% | +12.32% |
| 88 | `soybean__frog_eye_leaf_spot` | 73.91% | 80.95% | **77.27%** | 21 | 79.07% | -1.80% |
| 89 | `soybean__mosaic` | 62.50% | 38.46% | **47.62%** | 13 | 53.85% | -6.23% |
| 90 | `soybean__rust` | 60.00% | 33.33% | **42.86%** | 9 | 41.67% | +1.19% |
| 91 | `squash__powdery_mildew` | 42.31% | 55.00% | **47.83%** | 20 | 37.84% | +9.99% |
| 92 | `strawberry__anthracnose` | 100.00% | 80.00% | **88.89%** | 5 | 88.89% | -0.00% |
| 93 | `strawberry__leaf_scorch` | 60.00% | 100.00% | **75.00%** | 3 | 75.00% | +0.00% |
| 94 | `tobacco__blue_mold` | 55.56% | 100.00% | **71.43%** | 5 | 66.67% | +4.76% |
| 95 | `tobacco__brown_spot` | 83.33% | 71.43% | **76.92%** | 7 | 76.92% | +0.00% |
| 96 | `tobacco__frogeye_leaf_spot` | 33.33% | 33.33% | **33.33%** | 3 | 22.22% | +11.11% |
| 97 | `tobacco__mosaic_virus` | 66.67% | 80.00% | **72.73%** | 5 | 60.00% | +12.73% |
| 98 | `tomato__bacterial_leaf_spot` | 54.55% | 46.15% | **50.00%** | 13 | 53.33% | -3.33% |
| 99 | `tomato__early_blight` | 75.00% | 68.18% | **71.43%** | 22 | 76.19% | -4.76% |
| 100 | `tomato__late_blight` | 92.86% | 76.47% | **83.87%** | 17 | 75.00% | +8.87% |
| 101 | `tomato__leaf_mold` | 86.67% | 81.25% | **83.87%** | 16 | 77.42% | +6.45% |
| 102 | `tomato__mosaic_virus` | 40.00% | 28.57% | **33.33%** | 7 | 40.00% | -6.67% |
| 103 | `tomato__septoria_leaf_spot` | 46.67% | 50.00% | **48.28%** | 14 | 34.48% | +13.80% |
| 104 | `tomato__yellow_leaf_curl_virus` | 77.78% | 77.78% | **77.78%** | 9 | 70.59% | +7.19% |
| 105 | `wheat__bacterial_leaf_streak_(black_chaff)` | 75.00% | 46.15% | **57.14%** | 13 | 53.85% | +3.29% |
| 106 | `wheat__head_scab` | 90.32% | 93.33% | **91.80%** | 30 | 91.80% | +0.00% |
| 107 | `wheat__leaf_rust` | 53.85% | 63.64% | **58.33%** | 11 | 46.15% | +12.18% |
| 108 | `wheat__loose_smut` | 94.74% | 94.74% | **94.74%** | 19 | 92.31% | +2.43% |
| 109 | `wheat__powdery_mildew` | 83.33% | 74.07% | **78.43%** | 27 | 66.67% | +11.76% |
| 110 | `wheat__septoria_blotch` | 76.47% | 68.42% | **72.22%** | 19 | 55.00% | +17.22% |
| 111 | `wheat__stem_rust` | 100.00% | 92.31% | **96.00%** | 13 | 84.62% | +11.38% |
| 112 | `wheat__stripe_rust` | 71.79% | 87.50% | **78.87%** | 32 | 78.12% | +0.75% |
| 113 | `zucchini__bacterial_wilt` | 50.00% | 66.67% | **57.14%** | 9 | 57.14% | +0.00% |
| 114 | `zucchini__downy_mildew` | 100.00% | 40.00% | **57.14%** | 5 | 33.33% | +23.81% |
| 115 | `zucchini__powdery_mildew` | 50.00% | 33.33% | **40.00%** | 18 | 40.00% | +0.00% |
| 116 | `zucchini__yellow_mosaic_virus` | 100.00% | 66.67% | **80.00%** | 9 | 87.50% | -7.50% |

---

## 5. Artifacts and Generated Visualizations

- **Classification Report CSV:** [`reports/model2_classifier_v2/classification_report.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\reports\model2_classifier_v2\classification_report.csv)
- **Test Predictions CSV:** [`reports/model2_classifier_v2/test_predictions.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\reports\model2_classifier_v2\test_predictions.csv)
- **Confusion Matrix Plot:** [`reports/model2_classifier_v2/confusion_matrix.png`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\reports\model2_classifier_v2\confusion_matrix.png)
- **Training Curves Plot:** [`reports/model2_classifier_v2/training_curves.png`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\reports\model2_classifier_v2\training_curves.png)
- **Hyperparameters & Config:** [`models/model2_classifier_v2/config.json`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\models\model2_classifier_v2\config.json)