# Model 2 Disease Classifier: Comprehensive Training & Evaluation Report

**Date:** 2026-10-07  
**Architecture:** EfficientNet-B2 (`torchvision.models.efficientnet_b2` with ImageNet Pretraining)  
**Target Task:** Whole-Leaf Crop Disease Image Classification (117 Classes)  
**Hardware Platform:** NVIDIA GeForce RTX 3050 Laptop GPU (PyTorch 2.11.0+cu128, Torchvision 0.26.0+cu128)  

---

## 1. Executive Summary & Core Results

```
TRAINING STATUS                    : COMPLETED
BEST EPOCH                         : Epoch 14
BEST VALIDATION MACRO F1           : 65.40%
TEST TOP-1 ACCURACY                : 84.29%
TEST TOP-3 ACCURACY                : 94.57%
TEST MACRO F1                      : 61.01%
TEST WEIGHTED F1                   : 83.98%
HEALTHY CLASS F1 (Class 0)         : 99.24%
DISEASE-ONLY MACRO F1 (116 Diseases): 60.15%
```

---

## 2. Training Hyperparameters & Strategy

| Hyperparameter | Value | Rationale |
| :--- | :--- | :--- |
| **Backbone Architecture** | EfficientNet-B2 | Optimal accuracy-efficiency trade-off for 4GB RTX 3050 |
| **Input Resolution** | 260 x 260 px | Standard native resolution for EfficientNet-B2 |
| **Batch Size / Accumulation** | 32 (x2 grad accum = 64 eff.) | Fits within 4GB VRAM while preserving stable BN gradients |
| **Mixed Precision** | Native PyTorch AMP (FP16) | Accelerated computation and low VRAM footprint |
| **Transfer Learning Protocol** | 2-Stage Warmup & Fine-Tune | Stage 1 (3 ep head warmup) -> Stage 2 (12 ep full unfreeze) |
| **Optimizer & Weight Decay** | AdamW (1e-2 decay) | Robust convergence and regularization |
| **Loss Function** | Smoothed Class-Weighted CrossEntropy | (N / (K * N_c))^0.5 from training set counts |

---

## 3. Tail-Class Tier Performance Analysis

| Sample Count Tier (Train Set) | Number of Classes | Test Set Image Support | Test Macro F1 (%) |
| :--- | :--- | :--- | :--- |
| **<20 samples** | 27 classes | 70 images | **36.46%** |
| **20-49 samples** | 45 classes | 309 images | **60.67%** |
| **50-99 samples** | 33 classes | 482 images | **71.95%** |
| **>=100 samples** | 12 classes | 1443 images | **82.30%** |

---

## 4. Per-Crop Evaluation Summary (Top Crops)

| Crop | Test Support | Overall Accuracy (%) | Healthy Accuracy (%) | Disease Accuracy (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Tomato** | 354 images | **89.5%** | 100.0% | 62.2% |
| **Bean** | 216 images | **89.4%** | 100.0% | 85.0% |
| **Spinach** | 207 images | **100.0%** | 100.0% | 0.0% |
| **Wheat** | 164 images | **73.8%** | 0.0% | 73.8% |
| **Capsicum** | 120 images | **99.2%** | 99.2% | 0.0% |
| **Bell Pepper** | 115 images | **93.0%** | 100.0% | 66.7% |
| **Lettuce** | 86 images | **95.3%** | 100.0% | 66.7% |
| **Cucumber** | 81 images | **91.4%** | 100.0% | 87.7% |
| **Soybean** | 70 images | **65.7%** | 0.0% | 65.7% |
| **Rose** | 69 images | **100.0%** | 100.0% | 0.0% |
| **Corn** | 63 images | **73.0%** | 0.0% | 73.0% |
| **Citrus** | 62 images | **90.3%** | 0.0% | 90.3% |
| **Apple** | 60 images | **60.0%** | 0.0% | 60.0% |
| **Grape** | 60 images | **75.0%** | 0.0% | 75.0% |
| **Strawberry** | 54 images | **94.4%** | 95.7% | 87.5% |

---

## 5. Artifact Paths

- Best Checkpoint: [`models/model2_classifier/best_model.pth`](file:///models/model2_classifier/best_model.pth)
- Class Mapping: [`models/model2_classifier/class_mapping.json`](file:///models/model2_classifier/class_mapping.json)
- Configuration: [`models/model2_classifier/config.json`](file:///models/model2_classifier/config.json)
- Training Report JSON: [`models/model2_classifier/training_report.json`](file:///models/model2_classifier/training_report.json)
- Classification Report CSV: [`reports/model2_classifier/classification_report.csv`](file:///reports/model2_classifier/classification_report.csv)
- Test Predictions CSV: [`reports/model2_classifier/test_predictions.csv`](file:///reports/model2_classifier/test_predictions.csv)
- Training Curves: [`reports/model2_classifier/training_curves.png`](file:///reports/model2_classifier/training_curves.png)
- Confusion Matrix: [`reports/model2_classifier/confusion_matrix.png`](file:///reports/model2_classifier/confusion_matrix.png)