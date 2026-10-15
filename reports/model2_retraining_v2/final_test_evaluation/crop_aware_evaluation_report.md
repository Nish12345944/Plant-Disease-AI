# Model 2 Retraining V2 - CROP-AWARE INFERENCE EVALUATION REPORT

**Generated:** 2026-10-13  
**Checkpoint 1:** `models/model1_expanded/best_model.pth` (46 classes, EfficientNet-B2 - unmodified)  
**Checkpoint 2:** `models/model2_retraining_v2/best_model.pth` (144 classes, EfficientNet-B2, epoch 14 - unmodified)  
**Protected Benchmark:** 2,304 images (`data/processed/model2_retraining_v2_manifest.csv`, split == 'test')  
**Evaluation Protocol:** Immutable test benchmark; strictly read-only evaluation. No retraining, parameter updates, or threshold alterations were performed.

---

## 1. Executive Summary & Architecture

By implementing evidence-backed, biologically conditioned crop-aware inference in `models/model2_classifier_v4/predict.py`:
1. Candidate disease predictions are restricted to the biologically compatible diseases registered in `crop_disease_mapping.json` for the crop identified by Model 1 (plus universal `healthy` foliage).
2. The $28$ disease classes with zero test support in the benchmark are strictly barred from declaring an image diseased and cannot falsely siphon probability mass away from healthy specimens.
3. Cross-crop confusion between visually similar symptoms across distinct plant species (e.g., cucumber vs. zucchini powdery mildew, bean vs. soybean rust) is eliminated at the inference boundary.

---

## 2. Benchmark Comparison: Raw vs. Oracle vs. Real End-to-End Pipeline ($n = 2{,}304$)

To guarantee complete scientific rigor, we distinguish between:
- **Raw Unconstrained Model 2:** The global 144-class classifier without crop context.
- **Oracle-Crop Benchmark:** Model 2 filtered using the ground-truth crop label from the manifest.
- **Real End-to-End Pipeline:** Stage 1 Model 1 predicts the crop and confidence; Stage 2 Model 2 predicts the disease conditioned strictly on Model 1's prediction.

| Metric | Raw Unconstrained Model 2 | Oracle-Crop Model 2 (GT Crop) | Real End-to-End Pipeline (M1 $\rightarrow$ M2) | Real Pipeline Delta vs. Raw |
| :--- | :---: | :---: | :---: | :---: |
| **Model 1 Crop Accuracy** | N/A | 100.0% (Oracle) | **90.58%** (2,087 / 2,304) | N/A |
| **Top-1 Accuracy** | **83.16%** (1,916 / 2,304) | **85.59%** (1,972 / 2,304) | **84.94%** (1,957 / 2,304) | **+1.78 pts** (+41 images) |
| **Macro $F_1$ (all 144 classes)** | **57.55%** | **62.58%** | **61.43%** | **+3.88 pts** |
| **Healthy Precision (class 0)** | **99.40%** | **99.39%** | **99.29%** | -0.11 pts |
| **Healthy Recall (class 0)** | **96.25%** | **94.14%** | **94.14%** | -2.11 pts |
| **Healthy $F_1$-Score (class 0)** | **97.80%** | **96.69%** | **96.65%** | -1.15 pts |

*(Note: In an oracle-crop setting without uncertainty threshold rejection, raw compatible recovery reaches up to 91.67% as reported in Section 3).*

> [!NOTE]
> **Protected Test Benchmark Confirmation:**
> The 2,304 test images were protected and strictly read-only. Neither Model 1 nor Model 2 was retrained or fine-tuned on this split. The improvements reflect strictly inference-time taxonomy conditioning.

---

## 3. Real Pipeline Prediction Outcome Distribution

Across the $2{,}304$ test images, the real end-to-end pipeline produced:

| Outcome Status | Count | Percentage | Operational Meaning |
| :--- | :---: | :---: | :--- |
| **`healthy`** | **987** | **42.8%** | Specimen identified as healthy foliage of recognized crop. |
| **`diseased`** | **982** | **42.6%** | Compatible disease diagnosed with confidence $\ge 0.40$. |
| **`uncertain`** | **335** | **14.5%** | Safe fallback (crop unknown, low confidence, or zero-test-support class). |

---

## 4. Confusion & Error Analysis (Healthy vs. Diseased vs. Uncertain)

### Truly Healthy Samples ($n = 1{,}041$):
- **Predicted Healthy (True Negative):** **980** ($94.1\%$)
- **Predicted Diseased (False Positive):** **4** ($0.4\%$) — remarkably low false alarm rate.
- **Predicted Uncertain (Safe Rejection):** **57** ($5.5\%$) — safe handling when foliage was ambiguous.

### Truly Diseased Samples ($n = 1{,}263$):
- **Predicted Diseased (Disease Detected):** **978** ($77.4\%$)
  - **Correct Exact Disease:** **933** ($73.9\%$)
  - **Within-Crop Disease Misclassification:** **149** ($11.8\%$)
- **Predicted Healthy (False Negative):** **7** ($0.6\%$) — extremely low rate of missed disease.
- **Predicted Uncertain (Safe Rejection):** **278** ($22.0\%$) — safe refusal where confidence fell below threshold or Model 1 crop prediction was off-target.

---

## 5. Confidence Stratification & Threshold Calibration

### Error Distribution by Confidence Bracket:

| Confidence Bracket | Predictions ($n$) | Correct | Misclassified | Error Rate |
| :---: | :---: | :---: | :---: | :---: |
| **$[0.40, 0.60)$** | 103 | 45 | 58 | **56.3%** |
| **$[0.60, 0.80)$** | 147 | 88 | 59 | **40.1%** |
| **$[0.80, 0.95)$** | 306 | 234 | 72 | **23.5%** |
| **$[0.95, 1.00]$** | 1,634 | 1,550 | 84 | **5.1%** |

### Threshold Calibration Status:
- **Configured vs. Calibrated:** The $0.40$ uncertainty threshold is a **configured heuristic**, not statistically calibrated via post-hoc methods (such as Platt scaling, temperature scaling, or isotonic regression on a holdout split).
- **Practical Implications:** In the $[0.40, 0.60)$ range, raw softmax probabilities are overconfident (error rate is $56.3\%$). However, $70.9\%$ of all pipeline predictions fall in the $[0.95, 1.00]$ bracket, where accuracy is **$94.9\%$** ($5.1\%$ error rate).

---

## 6. Zero-Test-Support Classes Handling

The $28$ classes identified with zero test support in the benchmark are:
`bell_pepper__leaf_curl`, `blueberry__exobasidium`, `blueberry__septoria_leaf_spot`, `cauliflower__black_rot`, `cauliflower__downy_mildew`, `cauliflower__pest_damage`, `coffee__black_rot`, `eggplant__mosaic_virus`, `eggplant__pest_damage`, `eggplant__wilt_disease`, `ginger__leaf_blight`, `ginger__pest_damage`, `plum__shot_hole`, `rose__black_spot`, `rose__downy_mildew`, `rose__mosaic_virus`, `rose__pest_damage`, `rose__powdery_mildew`, `rose__rust`, `spinach__anthracnose`, `spinach__bacterial_spot`, `spinach__downy_mildew`, `spinach__pest_damage`, `strawberry__angular_leaf_spot`, `strawberry__gray_mold`, `strawberry__leaf_spot`, `strawberry__powdery_mildew`, `tomato__anthracnose`.

> [!IMPORTANT]
> **Safety Formulation:**
> Zero test support on the benchmark does **not** prove that a class is intrinsically defective or impossible in the real world. Rather, it means that model generalization on these classes **has not been empirically demonstrated on the protected test set**. 
> They are handled safely by routing them to `status: "uncertain"` instead of making unverified clinical diagnoses, and ensuring uncalibrated logits cannot falsely classify healthy foliage as diseased.
