# EXP-1 Test Set Evaluation & Performance Audit

> **Report Date**: 2026-10-10 14:38:44  
> **Project Root**: [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction)  
> **Evaluated Checkpoint**: [`models/model1_expanded/exp1/best_model_exp1.pth`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1_expanded/exp1/best_model_exp1.pth) (Global Epoch 14, Stage S2)  
> **Test Set**: Immutable 46-Class Test Split (**1,586 images**) across 44 active classes  

---

## 1. Executive Summary & Benchmark vs EXP-0 Baseline

| Evaluation Subset | Metric | EXP-0 Baseline | EXP-1 Two-Stage | Delta | Verification Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Overall (46 Classes)** | Top-1 Accuracy | 90.38% | **89.72%** | -0.66% | Regressed |
| | Top-3 Accuracy | 97.34% | **96.97%** | -0.37% | Regressed |
| | Macro F1 (Active 44) | 83.81% | **84.71%** | +0.90% | Improved |
| | Weighted F1 | 90.29% | **89.70%** | -0.59% | Regressed |
| **Original 22 Crops** | Top-1 Accuracy | 95.53% | **95.11%** | -0.42% | Regressed |
| | Active Macro F1 (20) | 92.51% | **96.13%** | +3.62% | Maintained |
| | Weighted F1 | 97.03% | **96.73%** | -0.30% | Regressed |
| **New 24 Crops** | Top-1 Accuracy | 84.02% | **83.03%** | -0.99% | Regressed |
| | Macro F1 (24) | 81.43% | **78.96%** | -2.47% | Regressed |
| | Weighted F1 | 84.27% | **84.55%** | +0.28% | Improved |

---

## 2. Evaluation Methodology & Integrity Notes

1. **Label-Constrained Scikit-Learn Metric Calculation**:
   - Active Macro F1 is computed by specifying `labels=active_test_indices` (`zero_division=0`).
   - Subset Macro F1 for Original-22 and New-24 is evaluated strictly over the exact label indices belonging to that subset.
2. **Zero-Support Gap Classes**:
   - **2 gap classes** have zero samples in test split: `['cherry_tomato', 'gypsophila']`.
   - Both classes have 0 samples across train, val, and test splits (known data gaps handled gracefully with loss weight 0.0).
3. **Inference Performance**:
   - Evaluated **1,586 images** in **24.11s** (65.8 images/sec) with PyTorch AMP FP16 and batch size 32.

---

## 3. Complete Per-Class Classification Report

| Index | Canonical Class | Subset | Test Support | Precision | Recall | F1 Score | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 0 | **anthurium** | ORIGINAL_22 | 10 | 100.00% | 100.00% | **100.00%** | ✅ Active |
| 1 | **apple** | NEW_24 | 57 | 81.67% | 85.96% | **83.76%** | ⚠️ Active |
| 2 | **banana** | NEW_24 | 54 | 92.98% | 98.15% | **95.50%** | ✅ Active |
| 3 | **basil** | NEW_24 | 6 | 35.71% | 83.33% | **50.00%** | ❌ Active |
| 4 | **blueberry** | ORIGINAL_22 | 31 | 88.89% | 77.42% | **82.76%** | ⚠️ Active |
| 5 | **broccoli** | ORIGINAL_22 | 41 | 83.72% | 87.80% | **85.71%** | ✅ Active |
| 6 | **cabbage** | NEW_24 | 27 | 83.33% | 74.07% | **78.43%** | ⚠️ Active |
| 7 | **bellpepper** | ORIGINAL_22 | 65 | 94.03% | 96.92% | **95.45%** | ✅ Active |
| 8 | **carnation** | ORIGINAL_22 | 5 | 100.00% | 100.00% | **100.00%** | ✅ Active |
| 9 | **carrot** | NEW_24 | 15 | 83.33% | 100.00% | **90.91%** | ✅ Active |
| 10 | **cauliflower** | NEW_24 | 10 | 55.56% | 50.00% | **52.63%** | ❌ Active |
| 11 | **celery** | NEW_24 | 6 | 62.50% | 83.33% | **71.43%** | ⚠️ Active |
| 12 | **cherry** | NEW_24 | 14 | 55.56% | 35.71% | **43.48%** | ❌ Active |
| 13 | **cherry_tomato** | ORIGINAL_22 | 0 | - | - | **-** | ⚪ Zero Support Zero Support Gap |
| 14 | **chrysanthemum** | ORIGINAL_22 | 42 | 100.00% | 92.86% | **96.30%** | ✅ Active |
| 15 | **citrus** | NEW_24 | 52 | 88.89% | 92.31% | **90.57%** | ✅ Active |
| 16 | **coffee** | NEW_24 | 28 | 89.29% | 89.29% | **89.29%** | ✅ Active |
| 17 | **corn** | NEW_24 | 62 | 90.62% | 93.55% | **92.06%** | ✅ Active |
| 18 | **cucumber** | ORIGINAL_22 | 65 | 94.03% | 96.92% | **95.45%** | ✅ Active |
| 19 | **eggplant** | NEW_24 | 14 | 71.43% | 71.43% | **71.43%** | ⚠️ Active |
| 20 | **french_bean** | ORIGINAL_22 | 65 | 92.19% | 90.77% | **91.47%** | ✅ Active |
| 21 | **garlic** | NEW_24 | 20 | 63.64% | 70.00% | **66.67%** | ⚠️ Active |
| 22 | **geranium** | ORIGINAL_22 | 25 | 100.00% | 100.00% | **100.00%** | ✅ Active |
| 23 | **gerbera** | ORIGINAL_22 | 7 | 70.00% | 100.00% | **82.35%** | ⚠️ Active |
| 24 | **ginger** | NEW_24 | 9 | 40.00% | 44.44% | **42.11%** | ❌ Active |
| 25 | **grape** | NEW_24 | 56 | 85.45% | 83.93% | **84.68%** | ⚠️ Active |
| 26 | **gypsophila** | ORIGINAL_22 | 0 | - | - | **-** | ⚪ Zero Support Zero Support Gap |
| 27 | **lettuce** | ORIGINAL_22 | 65 | 98.31% | 89.23% | **93.55%** | ✅ Active |
| 28 | **lilium** | ORIGINAL_22 | 4 | 100.00% | 100.00% | **100.00%** | ✅ Active |
| 29 | **maple** | NEW_24 | 11 | 90.00% | 81.82% | **85.71%** | ✅ Active |
| 30 | **marigold** | ORIGINAL_22 | 65 | 95.59% | 100.00% | **97.74%** | ✅ Active |
| 31 | **melon** | ORIGINAL_22 | 25 | 96.15% | 100.00% | **98.04%** | ✅ Active |
| 32 | **orchid** | ORIGINAL_22 | 65 | 98.48% | 100.00% | **99.24%** | ✅ Active |
| 33 | **peach** | NEW_24 | 44 | 84.09% | 84.09% | **84.09%** | ⚠️ Active |
| 34 | **plum** | NEW_24 | 22 | 77.78% | 63.64% | **70.00%** | ⚠️ Active |
| 35 | **potato** | NEW_24 | 24 | 85.71% | 75.00% | **80.00%** | ⚠️ Active |
| 36 | **raspberry** | NEW_24 | 12 | 71.43% | 83.33% | **76.92%** | ⚠️ Active |
| 37 | **rice** | NEW_24 | 16 | 73.33% | 68.75% | **70.97%** | ⚠️ Active |
| 38 | **rose** | ORIGINAL_22 | 65 | 96.97% | 98.46% | **97.71%** | ✅ Active |
| 39 | **soybean** | NEW_24 | 65 | 88.89% | 86.15% | **87.50%** | ✅ Active |
| 40 | **spinach** | ORIGINAL_22 | 65 | 100.00% | 100.00% | **100.00%** | ✅ Active |
| 41 | **strawberry** | ORIGINAL_22 | 65 | 98.46% | 98.46% | **98.46%** | ✅ Active |
| 42 | **tobacco** | NEW_24 | 18 | 85.00% | 94.44% | **89.47%** | ✅ Active |
| 43 | **tomato** | ORIGINAL_22 | 65 | 98.48% | 100.00% | **99.24%** | ✅ Active |
| 44 | **wheat** | NEW_24 | 65 | 88.14% | 80.00% | **83.87%** | ⚠️ Active |
| 45 | **zucchini** | ORIGINAL_22 | 39 | 88.24% | 76.92% | **82.19%** | ⚠️ Active |

---

## 4. Top Confusing Class Pairs

Total test misclassifications: **163 / 1586** (10.28% error rate).

| True Class | Predicted Class | Error Count | True Class Support | Subset Transition |
| :--- | :--- | :---: | :---: | :---: |
| **peach** | **apple** | **5** | 44 | New -> New |
| **cabbage** | **broccoli** | **4** | 27 | New -> Orig |
| **french_bean** | **soybean** | **4** | 65 | Orig -> New |
| **wheat** | **corn** | **4** | 65 | New -> New |
| **wheat** | **garlic** | **4** | 65 | New -> New |
| **zucchini** | **basil** | **4** | 39 | Orig -> New |
| **apple** | **citrus** | **3** | 57 | New -> New |
| **blueberry** | **grape** | **3** | 31 | Orig -> New |
| **cauliflower** | **broccoli** | **3** | 10 | New -> Orig |
| **chrysanthemum** | **gerbera** | **3** | 42 | Orig -> Orig |
| **garlic** | **wheat** | **3** | 20 | New -> New |
| **plum** | **cherry** | **3** | 22 | New -> New |
| **broccoli** | **cabbage** | **2** | 41 | Orig -> New |
| **cherry** | **rose** | **2** | 14 | New -> Orig |
| **citrus** | **banana** | **2** | 52 | New -> New |

---

## 5. Machine-Readable Artifact Index

- **Summary Metrics CSV**: [`reports/model1_expansion/exp1/exp1_test_metrics.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_test_metrics.csv)
- **Per-Class Metrics CSV**: [`reports/model1_expansion/exp1/exp1_per_class_metrics.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_per_class_metrics.csv)
- **Misclassifications CSV**: [`reports/model1_expansion/exp1/exp1_misclassifications.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_misclassifications.csv)
- **Confusion Matrix JSON**: [`reports/model1_expansion/exp1/exp1_confusion_matrix.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_confusion_matrix.json)
- **Complete Evaluation JSON**: [`reports/model1_expansion/exp1/exp1_test_evaluation.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_test_evaluation.json)