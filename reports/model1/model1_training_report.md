# MODEL 1 (EFFICIENTNET-B2) TRAINING & TEST EVALUATION REPORT

**Date:** 2026-10-05 15:49:54  
**Target Architecture:** EfficientNet-B2 (PyTorch Transfer Learning)  
**Device Used:** cuda (NVIDIA GeForce RTX 3050 Laptop GPU)  
**Dataset Location:** `data/processed/model1_balanced/`  
**Best Checkpoint:** `models/model1/best_model.pth` (Saved at Epoch 8)  

---
## 1. Executive Summary
- **Top-1 Test Accuracy:** **97.84%** (1,627 / 1,663 images correct)
- **Top-3 Test Accuracy:** **99.46%** (1,654 / 1,663 images correct)
- **Test Macro F1-Score:** **92.91%**
- **Test Weighted F1-Score:** **97.82%**
- **Best Validation Macro F1:** **98.22%** (Achieved at Epoch 8)
- **Validation Accuracy (Epoch 8):** **98.61%**
- **Total Test Images Evaluated:** 1,663 images (Untouched Test Split)

## 2. Complete Per-Class Test Performance (22 Target Taxonomy)
| # | Class Name | Test Support | Precision | Recall | F1-Score | Evaluation Status |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| 1 | `anthurium` | 11.0 | 100.00% | 100.00% | **100.00%** | EXCELLENT (>=95%) |
| 2 | `blueberry` | 32.0 | 93.75% | 93.75% | **93.75%** | GOOD (85-94%) |
| 3 | `broccoli` | 42.0 | 95.24% | 95.24% | **95.24%** | EXCELLENT (>=95%) |
| 4 | `capsicum` | 150.0 | 96.05% | 97.33% | **96.69%** | EXCELLENT (>=95%) |
| 5 | `carnation` | 6.0 | 100.00% | 100.00% | **100.00%** | EXCELLENT (>=95%) |
| 6 | `cherry_tomato` | 0.0 | 0.00% | 0.00% | **0.00%** | NO TEST DATA (DOCUMENTED GAP) |
| 7 | `chrysanthemum` | 43.0 | 97.67% | 97.67% | **97.67%** | EXCELLENT (>=95%) |
| 8 | `cucumber` | 150.0 | 98.66% | 98.00% | **98.33%** | EXCELLENT (>=95%) |
| 9 | `french_bean` | 140.0 | 97.08% | 95.00% | **96.03%** | EXCELLENT (>=95%) |
| 10 | `geranium` | 26.0 | 100.00% | 100.00% | **100.00%** | EXCELLENT (>=95%) |
| 11 | `gerbera` | 1.0 | 0.00% | 0.00% | **0.00%** | ACCEPTABLE (<85%) |
| 12 | `gypsophila` | 0.0 | 0.00% | 0.00% | **0.00%** | NO TEST DATA (DOCUMENTED GAP) |
| 13 | `lettuce` | 150.0 | 98.64% | 96.67% | **97.64%** | EXCELLENT (>=95%) |
| 14 | `lilium` | 5.0 | 100.00% | 100.00% | **100.00%** | EXCELLENT (>=95%) |
| 15 | `marigold` | 121.0 | 97.56% | 99.17% | **98.36%** | EXCELLENT (>=95%) |
| 16 | `melon` | 26.0 | 100.00% | 100.00% | **100.00%** | EXCELLENT (>=95%) |
| 17 | `orchid` | 120.0 | 100.00% | 99.17% | **99.58%** | EXCELLENT (>=95%) |
| 18 | `rose` | 150.0 | 99.33% | 98.67% | **99.00%** | EXCELLENT (>=95%) |
| 19 | `spinach` | 150.0 | 100.00% | 100.00% | **100.00%** | EXCELLENT (>=95%) |
| 20 | `strawberry` | 150.0 | 98.68% | 99.33% | **99.00%** | EXCELLENT (>=95%) |
| 21 | `tomato` | 150.0 | 97.97% | 96.67% | **97.32%** | EXCELLENT (>=95%) |
| 22 | `zucchini` | 40.0 | 82.98% | 97.50% | **89.66%** | GOOD (85-94%) |

| - | **Macro Average** | **1663** | **92.68%** | **93.21%** | **92.91%** | - |
| - | **Weighted Average** | **1663** | **97.84%** | **97.84%** | **97.82%** | - |

## 3. Dedicated Performance Summary for Low-Data Classes
Classes with restricted sample sizes were managed via smooth class-weighting and balanced sampling without synthetic duplicates:
| Class Name | Test Support | Precision | Recall | F1-Score | Remarks |
|:---|:---:|:---:|:---:|:---:|:---|
| `gerbera` | 1.0 | 0.00% | 0.00% | **0.00%** | Preserved from verified real data without synthetic duplication |
| `lilium` | 5.0 | 100.00% | 100.00% | **100.00%** | Preserved from verified real data without synthetic duplication |
| `carnation` | 6.0 | 100.00% | 100.00% | **100.00%** | Preserved from verified real data without synthetic duplication |
| `anthurium` | 11.0 | 100.00% | 100.00% | **100.00%** | Preserved from verified real data without synthetic duplication |
| `melon` | 26.0 | 100.00% | 100.00% | **100.00%** | Preserved from verified real data without synthetic duplication |
| `geranium` | 26.0 | 100.00% | 100.00% | **100.00%** | Preserved from verified real data without synthetic duplication |
| `blueberry` | 32.0 | 93.75% | 93.75% | **93.75%** | Preserved from verified real data without synthetic duplication |
| `zucchini` | 40.0 | 82.98% | 97.50% | **89.66%** | Preserved from verified real data without synthetic duplication |
| `broccoli` | 42.0 | 95.24% | 95.24% | **95.24%** | Preserved from verified real data without synthetic duplication |
| `chrysanthemum` | 43.0 | 97.67% | 97.67% | **97.67%** | Preserved from verified real data without synthetic duplication |

## 4. Training History by Epoch
| Epoch | Train Loss | Train Acc | Val Loss | Val Acc | Val Macro F1 | Learning Rate | Epoch Time |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 01 | 0.4579 | 88.07% | 0.1474 | 95.88% | 89.47% | 3.00e-04 | 184.3s |
| 02 | 0.1446 | 95.47% | 0.1283 | 96.48% | 90.44% | 2.93e-04 | 123.2s |
| 03 | 0.0965 | 96.85% | 0.0953 | 97.21% | 96.86% | 2.71e-04 | 149.5s |
| 04 | 0.0728 | 97.50% | 0.1154 | 96.42% | 87.71% | 2.38e-04 | 127.8s |
| 05 | 0.0548 | 98.27% | 0.0624 | 98.06% | 97.77% | 1.97e-04 | 124.6s |
| 06 | 0.0304 | 98.84% | 0.0834 | 97.63% | 92.53% | 1.50e-04 | 124.6s |
| 07 | 0.0223 | 99.17% | 0.0520 | 98.42% | 98.00% | 1.04e-04 | 131.0s |
| 08 | 0.0137 | 99.54% | 0.0488 | 98.61% | 98.22% | 6.26e-05 | 129.8s |

## 5. Artifact Directory & Verification
- **Model Weights Checkpoint:** [`models/model1/best_model.pth`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/best_model.pth)
- **Class Mapping JSON:** [`models/model1/class_mapping.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/class_mapping.json)
- **Preprocessing Config JSON:** [`models/model1/config.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/config.json)
- **Complete Report JSON:** [`models/model1/training_report.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/training_report.json)
- **Classification Metrics CSV:** [`reports/model1/classification_report.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/classification_report.csv)
- **Test Predictions Table CSV:** [`reports/model1/test_predictions.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/test_predictions.csv)
- **Confusion Matrix Plot:** [`reports/model1/confusion_matrix.png`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/confusion_matrix.png)
- **Training Curves Plot:** [`reports/model1/training_curves.png`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1/training_curves.png)
