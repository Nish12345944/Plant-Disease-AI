# EXPANDED MODEL 1 (46 CLASSES) TRAINING AND EVALUATION REPORT

**Date:** 2026-10-09 10:42:31  
**Architecture:** EfficientNet-B2 (ImageNet Pretrained)  
**Model Directory:** `models/model1_expanded/` (Isolated)  
**Production Baseline Model:** `models/model1/` (Untouched, Locked)  

---

## 1. Executive Summary & Final Recommendation

### Final Recommendation: **NEEDS TRAINING TUNING**

> **Rationale:** Imbalance or hyperparameter tuning required to improve minority class F1 scores.


### Baseline vs Expanded Model 1 Comparison


| Metric | Original Locked Baseline (22 Classes) | Expanded Model 1 (Overall 46 Classes) | Expanded Model 1 (Original 22 Subset) | Expanded Model 1 (New 24 Subset) |
| :--- | :---: | :---: | :---: | :---: |
| **Top-1 Accuracy** | **97.84%** | **90.38%** | **95.53%** | **84.02%** |
| **Top-3 Accuracy** | **99.46%** | **97.34%** | **98.28%** | **96.18%** |
| **Macro F1 Score** | **92.91%** | **83.81%** | **54.42%** | **63.77%** |
| **Weighted F1 Score** | **97.82%** | **90.29%** | **97.03%** | **84.95%** |

---

## 2. Training Dynamics & Epoch Progression


- **Best Epoch:** Epoch 10

- **Best Validation Macro F1:** 86.63%

- **Best Validation Accuracy:** 90.94%


| Epoch | Train Loss | Train Acc | Train Macro F1 | Val Loss | Val Acc | Val Macro F1 | LR | Time (s) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 1.2622 | 69.13% | 61.57% | 0.5979 | 82.14% | 75.04% | 3.00e-04 | 192.3s |
| 2 | 0.5387 | 84.95% | 81.64% | 0.5182 | 85.12% | 79.35% | 2.93e-04 | 118.8s |
| 3 | 0.3827 | 89.34% | 86.44% | 0.4531 | 87.97% | 82.94% | 2.71e-04 | 115.8s |
| 4 | 0.2775 | 92.01% | 90.74% | 0.4586 | 88.16% | 82.81% | 2.38e-04 | 110.0s |
| 5 | 0.1884 | 94.55% | 93.79% | 0.4213 | 88.22% | 83.56% | 1.97e-04 | 108.5s |
| 6 | 0.1402 | 95.97% | 95.69% | 0.4104 | 89.04% | 84.59% | 1.50e-04 | 102.8s |
| 7 | 0.0983 | 97.28% | 96.96% | 0.3880 | 90.44% | 84.84% | 1.04e-04 | 117.7s |
| 8 | 0.0695 | 98.03% | 97.51% | 0.3906 | 90.56% | 86.12% | 6.26e-05 | 92.9s |
| 9 | 0.0553 | 98.43% | 98.30% | 0.3892 | 90.44% | 86.34% | 2.96e-05 | 93.0s |
| 10 | 0.0485 | 98.61% | 98.49% | 0.3791 | 90.94% | 86.63% | 8.30e-06 | 95.4s |

---

## 3. Class Imbalance Strategy


The 46-class dataset exhibits natural agricultural volume divergence (e.g. `gerbera` has 2 train images while `capsicum`/`lettuce` have 500 images).

To avoid gradient explosion while preventing minority starvation:

1. **Smoothed Class-Weighted CrossEntropyLoss:** Loss weights calculated as $w_c = (N_{median} / N_c)^{0.35}$, normalized to unit mean across active classes and clamped to $[0.3, 3.5]$. This dampens extreme loss spikes.

2. **Mild WeightedRandomSampler:** Sampling probabilities smoothed with exponent $0.20$ and clamped, providing gentle minority oversampling without collapsing diversity.

3. **Documented Gaps:** Empty classes `cherry_tomato` and `gypsophila` assigned weight $0.0$.


---

## 4. Per-Class Performance Breakdown


| Class | Taxonomy Group | Support (Test) | Precision | Recall | F1-Score |
|:---|:---:|:---:|:---:|:---:|:---:|
| **`anthurium`** | ORIGINAL_22 | 10.0 | 100.00% | 100.00% | 100.00% |
| **`apple`** | NEW_24 | 57.0 | 84.44% | 66.67% | 74.51% |
| **`banana`** | NEW_24 | 54.0 | 96.30% | 96.30% | 96.30% |
| **`basil`** | NEW_24 | 6.0 | 57.14% | 66.67% | 61.54% |
| **`blueberry`** | ORIGINAL_22 | 31.0 | 93.10% | 87.10% | 90.00% |
| **`broccoli`** | ORIGINAL_22 | 41.0 | 81.40% | 85.37% | 83.33% |
| **`cabbage`** | NEW_24 | 27.0 | 76.00% | 70.37% | 73.08% |
| **`capsicum`** | ORIGINAL_22 | 65.0 | 98.41% | 95.38% | 96.88% |
| **`carnation`** | ORIGINAL_22 | 5.0 | 100.00% | 100.00% | 100.00% |
| **`carrot`** | NEW_24 | 15.0 | 75.00% | 100.00% | 85.71% |
| **`cauliflower`** | NEW_24 | 10.0 | 55.56% | 50.00% | 52.63% |
| **`celery`** | NEW_24 | 6.0 | 80.00% | 66.67% | 72.73% |
| **`cherry`** | NEW_24 | 14.0 | 45.45% | 35.71% | 40.00% |
| **`cherry_tomato`** | ORIGINAL_22 | 0.0 | 0.00% | 0.00% | 0.00% |
| **`chrysanthemum`** | ORIGINAL_22 | 42.0 | 100.00% | 97.62% | 98.80% |
| **`citrus`** | NEW_24 | 52.0 | 87.50% | 94.23% | 90.74% |
| **`coffee`** | NEW_24 | 28.0 | 89.29% | 89.29% | 89.29% |
| **`corn`** | NEW_24 | 62.0 | 93.75% | 96.77% | 95.24% |
| **`cucumber`** | ORIGINAL_22 | 65.0 | 96.97% | 98.46% | 97.71% |
| **`eggplant`** | NEW_24 | 14.0 | 63.16% | 85.71% | 72.73% |
| **`french_bean`** | ORIGINAL_22 | 65.0 | 93.44% | 87.69% | 90.48% |
| **`garlic`** | NEW_24 | 20.0 | 71.43% | 75.00% | 73.17% |
| **`geranium`** | ORIGINAL_22 | 25.0 | 96.15% | 100.00% | 98.04% |
| **`gerbera`** | ORIGINAL_22 | 1.0 | 0.00% | 0.00% | 0.00% |
| **`ginger`** | NEW_24 | 9.0 | 83.33% | 55.56% | 66.67% |
| **`grape`** | NEW_24 | 56.0 | 89.09% | 87.50% | 88.29% |
| **`gypsophila`** | ORIGINAL_22 | 0.0 | 0.00% | 0.00% | 0.00% |
| **`lettuce`** | ORIGINAL_22 | 65.0 | 98.31% | 89.23% | 93.55% |
| **`lilium`** | ORIGINAL_22 | 4.0 | 100.00% | 100.00% | 100.00% |
| **`maple`** | NEW_24 | 11.0 | 76.92% | 90.91% | 83.33% |
| **`marigold`** | ORIGINAL_22 | 65.0 | 97.01% | 100.00% | 98.48% |
| **`melon`** | ORIGINAL_22 | 25.0 | 100.00% | 100.00% | 100.00% |
| **`orchid`** | ORIGINAL_22 | 65.0 | 100.00% | 100.00% | 100.00% |
| **`peach`** | NEW_24 | 44.0 | 80.39% | 93.18% | 86.32% |
| **`plum`** | NEW_24 | 22.0 | 78.95% | 68.18% | 73.17% |
| **`potato`** | NEW_24 | 24.0 | 90.00% | 75.00% | 81.82% |
| **`raspberry`** | NEW_24 | 12.0 | 58.82% | 83.33% | 68.97% |
| **`rice`** | NEW_24 | 16.0 | 66.67% | 75.00% | 70.59% |
| **`rose`** | ORIGINAL_22 | 65.0 | 96.97% | 98.46% | 97.71% |
| **`soybean`** | NEW_24 | 65.0 | 85.71% | 92.31% | 88.89% |
| **`spinach`** | ORIGINAL_22 | 65.0 | 98.48% | 100.00% | 99.24% |
| **`strawberry`** | ORIGINAL_22 | 65.0 | 100.00% | 95.38% | 97.64% |
| **`tobacco`** | NEW_24 | 18.0 | 80.95% | 94.44% | 87.18% |
| **`tomato`** | ORIGINAL_22 | 65.0 | 100.00% | 98.46% | 99.22% |
| **`wheat`** | NEW_24 | 65.0 | 88.52% | 83.08% | 85.71% |
| **`zucchini`** | ORIGINAL_22 | 39.0 | 83.72% | 92.31% | 87.80% |

### Weakest 5 Classes (Lowest F1)


| Class | Category | Test Support | F1-Score | Notes / Diagnosis |
|:---|:---:|:---:|:---:|:---|
| **`gerbera`** | ORIGINAL_22 | 1.0 | **0.00%** | P=0.0%, R=0.0% |
| **`cherry`** | NEW_24 | 14.0 | **40.00%** | P=45.5%, R=35.7% |
| **`cauliflower`** | NEW_24 | 10.0 | **52.63%** | P=55.6%, R=50.0% |
| **`basil`** | NEW_24 | 6.0 | **61.54%** | P=57.1%, R=66.7% |
| **`ginger`** | NEW_24 | 9.0 | **66.67%** | P=83.3%, R=55.6% |

---

## 5. Confusion Analysis & Top Error Pairs


### Top 20 Confusion Pairs


| Rank | Actual Class | Predicted Class | Misclassified Count | Actual Support | Error Share |
|:---:|:---|:---|:---:|:---:|:---:|
| 1 | `wheat` | `garlic` | 6 | 65 | 9.2% |
| 2 | `french_bean` | `soybean` | 5 | 65 | 7.7% |
| 3 | `apple` | `citrus` | 4 | 57 | 7.0% |
| 4 | `apple` | `peach` | 4 | 57 | 7.0% |
| 5 | `cabbage` | `broccoli` | 4 | 27 | 14.8% |
| 6 | `broccoli` | `cabbage` | 3 | 41 | 7.3% |
| 7 | `cauliflower` | `broccoli` | 3 | 10 | 30.0% |
| 8 | `garlic` | `wheat` | 3 | 20 | 15.0% |
| 9 | `ginger` | `rice` | 3 | 9 | 33.3% |
| 10 | `plum` | `peach` | 3 | 22 | 13.6% |
| 11 | `apple` | `cherry` | 2 | 57 | 3.5% |
| 12 | `apple` | `maple` | 2 | 57 | 3.5% |
| 13 | `apple` | `plum` | 2 | 57 | 3.5% |
| 14 | `apple` | `soybean` | 2 | 57 | 3.5% |
| 15 | `celery` | `zucchini` | 2 | 6 | 33.3% |
| 16 | `cherry` | `apple` | 2 | 14 | 14.3% |
| 17 | `cherry` | `grape` | 2 | 14 | 14.3% |
| 18 | `grape` | `raspberry` | 2 | 56 | 3.6% |
| 19 | `peach` | `apple` | 2 | 44 | 4.5% |
| 20 | `plum` | `cherry` | 2 | 22 | 9.1% |

### Biological & Morphological Confounders Analysis


| Confounder Pair | A -> B Count | B -> A Count | Total Cross-Confusions | Status / Impact |
|:---|:---:|:---:|:---:|:---|
| **tomato <-> potato** | 0 | 0 | **0** | Negligible |
| **tomato <-> eggplant** | 0 | 0 | **0** | Negligible |
| **tomato <-> tobacco** | 0 | 0 | **0** | Negligible |
| **capsicum <-> eggplant** | 0 | 1 | **1** | Negligible |
| **wheat <-> rice** | 2 | 2 | **4** | Moderate |
| **wheat <-> corn** | 2 | 1 | **3** | Moderate |
| **broccoli <-> cabbage** | 3 | 4 | **7** | Elevated Confound |
| **broccoli <-> cauliflower** | 1 | 3 | **4** | Moderate |
| **cabbage <-> cauliflower** | 1 | 1 | **2** | Negligible |
| **peach <-> plum** | 0 | 3 | **3** | Moderate |
| **peach <-> cherry** | 1 | 0 | **1** | Negligible |
| **plum <-> cherry** | 2 | 0 | **2** | Negligible |
| **cucumber <-> zucchini** | 1 | 1 | **2** | Negligible |
| **cucumber <-> melon** | 0 | 0 | **0** | Negligible |
| **blueberry <-> raspberry** | 1 | 0 | **1** | Negligible |
| **banana <-> tobacco** | 0 | 0 | **0** | Negligible |

---

## 6. Audit & Isolation Verification


- [x] `models/model1/` production model weights SHA-256 unchanged.

- [x] `models/model2_classifier_v4/` production model weights unchanged.

- [x] `data/processed/model1_expanded/test/` 1,580 images completely untouched during training.

- [x] Model artifacts completely isolated in `models/model1_expanded/`.
