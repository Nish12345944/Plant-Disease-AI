# MODEL 2 V3 RETRAINING & BENCHMARK REPORT

**Date:** 2026-10-08  
**Model Directory:** `models/model2_classifier_v3/`  
**Dataset Location:** `data/processed/model2_organized/`  
**Architecture:** EfficientNet-B2 (117 Classes)  
**Best Epoch:** Epoch 9  

## 1. Executive Comparison: Model 2 V2 vs Model 2 V3 (Immutable 2,304 Test Set)

| Metric | Model 2 V2 Baseline | Model 2 V3 (Clean Organized Data) | Delta (V3 - V2) |
|:---|:---:|:---:|:---:|
| **Test Top-1 Accuracy** | 85.98% | **87.63%** | +1.65% |
| **Test Top-3 Accuracy** | 95.62% | **96.27%** | +0.65% |
| **Test Macro F1** | 65.29% | **68.61%** | +3.32% |
| **Test Disease-only Macro F1** | 64.43% | **67.75%** | +3.32% |
| **Test Healthy F1** | 99.47% | **99.52%** | +0.05% |

## 2. High-Confidence Diagnostic Classes Benchmark

| Crop | Disease Class | Support | Precision | Recall | F1 Score |
|:---|:---|:---:|:---:|:---:|:---:|
| `shared` | `healthy` | 1041 | 99.8% | 99.2% | **99.5%** |
| `bean` | `bean__rust` | 77 | 89.7% | 90.9% | **90.3%** |
| `bean` | `bean__angular_leaf_spot` | 65 | 96.9% | 96.9% | **96.9%** |
| `soybean` | `soybean__rust` | 9 | 83.3% | 55.6% | **66.7%** |
| `soybean` | `soybean__frog_eye_leaf_spot` | 21 | 73.1% | 90.5% | **80.9%** |
| `citrus` | `citrus__canker` | 48 | 93.6% | 91.7% | **92.6%** |
| `wheat` | `wheat__stripe_rust` | 32 | 79.4% | 84.4% | **81.8%** |
| `wheat` | `wheat__head_scab` | 30 | 88.2% | 100.0% | **93.8%** |
| `wheat` | `wheat__powdery_mildew` | 27 | 82.8% | 88.9% | **85.7%** |
| `wheat` | `wheat__septoria_blotch` | 19 | 88.2% | 78.9% | **83.3%** |
| `wheat` | `wheat__loose_smut` | 19 | 100.0% | 89.5% | **94.4%** |
| `grape` | `grape__downy_mildew` | 32 | 87.1% | 84.4% | **85.7%** |
| `apple` | `apple__scab` | 25 | 72.7% | 64.0% | **68.1%** |
| `corn` | `corn__smut` | 19 | 94.7% | 94.7% | **94.7%** |
| `corn` | `corn__rust` | 18 | 100.0% | 72.2% | **83.9%** |
| `corn` | `corn__northern_leaf_blight` | 14 | 81.2% | 92.9% | **86.7%** |
| `zucchini` | `zucchini__powdery_mildew` | 18 | 60.0% | 50.0% | **54.5%** |
| `cucumber` | `cucumber__powdery_mildew` | 22 | 63.6% | 63.6% | **63.6%** |
| `cucumber` | `cucumber__angular_leaf_spot` | 22 | 87.0% | 90.9% | **88.9%** |
| `cucumber` | `cucumber__bacterial_wilt` | 13 | 64.7% | 84.6% | **73.3%** |
| `tomato` | `tomato__early_blight` | 22 | 77.3% | 77.3% | **77.3%** |
| `tomato` | `tomato__late_blight` | 17 | 92.9% | 76.5% | **83.9%** |
| `tomato` | `tomato__leaf_mold` | 16 | 86.7% | 81.2% | **83.9%** |
| `tomato` | `tomato__septoria_leaf_spot` | 14 | 37.5% | 42.9% | **40.0%** |
| `peach` | `peach__leaf_curl` | 18 | 94.7% | 100.0% | **97.3%** |
| `peach` | `peach__brown_rot` | 14 | 77.8% | 100.0% | **87.5%** |
| `coffee` | `coffee__leaf_rust` | 16 | 93.3% | 87.5% | **90.3%** |
| `banana` | `banana__black_leaf_streak` | 17 | 85.0% | 100.0% | **91.9%** |
| `banana` | `banana__bunchy_top` | 11 | 100.0% | 81.8% | **90.0%** |

## 3. Dataset & Training Overview
- **Train Samples:** 15,252
- **Validation Samples:** 1,697
- **Test Samples (Immutable):** 2,304
- **Total Classes:** 117
- **Best Validation Macro F1:** 69.13% (Epoch 9)
- **Hardware Used:** NVIDIA GeForce RTX 3050 Laptop GPU (CUDA 12.8)
