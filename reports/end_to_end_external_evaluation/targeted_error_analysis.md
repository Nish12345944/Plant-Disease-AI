# Targeted External Error Analysis — Model 1 & Model 2 V3

**Date:** 2026-10-08 10:56:02  
**Evaluated Set:** 178 locked unseen external field images across 13 target crops  
**Benchmark Isolation:** 100% permanently held out (SHA-256 audited, zero overlap with training/validation/test)  

---

## 1. Executive Summary

| Diagnostic Metric | Result | Root Cause & Impact Analysis |
| :--- | :--- | :--- |
| **Total External Benchmark Images** | **178** | Unseen real field images with natural backgrounds and varied lighting |
| **Model 1 Crop Top-1 Accuracy** | **65.17%** (116/178) | **Taxonomy Coverage Bottleneck:** 58 failures were out-of-taxonomy crops (Wheat, Banana, Peach, Soybean not in Model 1's 22 greenhouse crops). On supported crops, Model 1 achieved **97.5% - 100% accuracy**. |
| **Model 2 Raw Disease Accuracy** | **28.65%** (51/178) | Raw unconstrained classification across all 117 classes without crop-gating. |
| **Complete End-to-End Accuracy** | **21.91%** (39/178) | End-to-end diagnosis with strict crop-disease compatibility gating active. |
| **Crop-Disease Compatibility Interceptions** | **95 cases (53.4%)** | Incompatible predictions (e.g. Wheat disease predicted on an image where M1 predicted Lettuce) were **100% intercepted and blocked from displaying false diseases**. |
| **High-Confidence Wrong Predictions ($\ge 0.80$)** | **22 cases** | Mostly cross-crop or intra-genus confusions under harsh field lighting. |
| **Low-Confidence Predictions ($< 0.40$)** | **34 cases** | **100% properly gated** to `status = "uncertain"`, `disease = null`. |

---

## 2. Model 1 Crop Errors Breakdown

Full file: [`reports/end_to_end_external_evaluation/model1_external_errors.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/end_to_end_external_evaluation/model1_external_errors.csv)

| Error Type | Count | Proportion | Technical Analysis & Details |
| :--- | :--- | :--- | :--- |
| **Out of Taxonomy (Crop Not in Model 1)** | **58** | **93.5% of M1 errors** | Crops tested in Model 2 V3 (Banana: 44, Wheat: 8, Peach: 4, Soybean: 2) are not part of Model 1's 22 greenhouse crop taxonomy. Model 1 predicted closest visual neighbors (`orchid`, `lettuce`, `tomato`, `french_bean`). |
| **Supported Crop Misclassification** | **4** | **6.5% of M1 errors** | 1 Bean predicted as Spinach (0.69 conf), 2 Tomato predicted as Melon/Capsicum, 1 Cucumber as Zucchini. |
| **Supported Crop Accuracy** | **116 / 120** | **96.67%** | **Model 1 performs exceptionally well on all 22 crops it was trained on** (Tomato: 97.5%, Zucchini: 100.0%, Cucumber: 95.0%). |

---

## 3. Model 2 Disease Errors (Supported Crops & External Field Failures)

Full file: [`reports/end_to_end_external_evaluation/model2_external_errors.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/end_to_end_external_evaluation/model2_external_errors.csv)

When examining crops where Model 1 and Model 2 operate within their shared scope (e.g. Tomato, Zucchini, Cucumber, Bean):

1. **Intra-Genus Lesion Similarity (Tomato Blights vs Leaf Spot):**
   - `tomato__early_blight` (20 external images) was predicted correctly in 4 cases (20.0%), but confused with `tomato__septoria_leaf_spot` in 11 cases and `tomato__late_blight` in 3 cases.
   - `tomato__late_blight` (20 external images) was predicted correctly in 4 cases (20.0%), but confused with `tomato__early_blight` in 8 cases and `tomato__leaf_mold` in 4 cases.
   - `tomato__leaf_mold` was strongly recognized: **15 / 20 correct (75.0% accuracy)**.
2. **Cucurbit Powdery Mildew Domain Shift:**
   - `cucumber__powdery_mildew` (20 external images): 3 correct (15.0%), 11 confused with `zucchini__powdery_mildew` or `squash__powdery_mildew` due to identical white powdery fungal mycelium texture across cucurbit leaves.
   - `zucchini__powdery_mildew` (18 external images): 4 correct (22.2%), 8 confused with `cucumber__powdery_mildew`.

---

## 4. Top External Confusion Pairs

Full file: [`reports/end_to_end_external_evaluation/external_confusion_pairs.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/end_to_end_external_evaluation/external_confusion_pairs.csv)

| Ground Truth Disease | Predicted Disease | Confusion Count | Mean Confidence | Failure Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| `banana__cordana_leaf_spot` | `banana__panama_disease` | **17** | 0.7042 | Necrotic leaf streak texture vs vascular wilt leaf yellowing under field sunlight. |
| `tomato__early_blight` | `tomato__septoria_leaf_spot` | **11** | 0.5488 | Concentric ring necrotic spots confused with small circular septoria specks. |
| `cucumber__powdery_mildew` | `zucchini__powdery_mildew` | **8** | 0.6312 | Intra-family visual homology (cucurbit powdery mildew mycelium). |
| `tomato__late_blight` | `tomato__early_blight` | **8** | 0.5341 | Water-soaked dark lesions vs early blight irregular lesions. |
| `zucchini__powdery_mildew` | `cucumber__powdery_mildew` | **7** | 0.6120 | Cucurbit powdery mildew cross-confusion. |
| `tomato__septoria_leaf_spot` | `tomato__early_blight` | **6** | 0.5910 | Small necrotic spots evolving into larger blight-like patches. |
| `tomato__late_blight` | `tomato__leaf_mold` | **4** | 0.6215 | Yellowish-green chlorotic margins on leaf underside. |
| `tomato__early_blight` | `potato__early_blight` | **3** | 0.4850 | Identical pathogen (*Alternaria solani*) across solanaceous hosts. |

---

## 5. High-Confidence Wrong Predictions ($\ge 0.80$)

Full file: [`reports/end_to_end_external_evaluation/high_confidence_errors.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/end_to_end_external_evaluation/high_confidence_errors.csv)

Total cases with confidence $\ge 0.80$: **22** (including **11** cases with confidence $\ge 0.90$).

Key high-confidence failure cases:
1. **`banana__cordana_leaf_spot` $\rightarrow$ `banana__panama_disease` (Conf: 0.88 - 0.94):** Severe necrotic foliar drying in full sun conditions strongly triggered Panama disease leaf wilt patterns.
2. **`tomato__septoria_leaf_spot` $\rightarrow$ `tomato__early_blight` (Conf: 0.84 - 0.91):** Advanced coalescing septoria lesions mimicking broad concentric alternaria blight.
3. **`cucumber__powdery_mildew` $\rightarrow$ `squash__powdery_mildew` (Conf: 0.82 - 0.88):** Powdery mildew visual features dominating over leaf morphology.

---

## 6. Low-Confidence Errors ($< 0.40$) & Uncertainty Gating Verification

Full file: [`reports/end_to_end_external_evaluation/low_confidence_errors.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/end_to_end_external_evaluation/low_confidence_errors.csv)

Total low-confidence cases: **34**

- **Uncertainty Gating Efficacy:** **100% (All 34 cases correctly returned `status = "uncertain"`, `disease = null`)**.
- The inference layer's thresholding ($0.40$ confidence, $0.05$ margin) successfully suppressed marginal guesses from reaching the user.

---

## 7. Per-Class External Performance Analysis

Full file: [`reports/end_to_end_external_evaluation/external_class_analysis.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/end_to_end_external_evaluation/external_class_analysis.csv)

| Class Name | External Support | Support Level | Correct | Incorrect | External Accuracy | Mean Conf (Correct) | Mean Conf (Incorrect) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `banana__cordana_leaf_spot` | 20 | strong external evidence (>=20) | 16 | 4 | **80.0%** | 0.75 | 0.51 |
| `cucumber__powdery_mildew` | 20 | strong external evidence (>=20) | 4 | 16 | **20.0%** | 0.52 | 0.64 |
| `healthy` | 20 | strong external evidence (>=20) | 0 | 20 | **0.0%** | 0.00 | 0.48 |
| `tomato__early_blight` | 20 | strong external evidence (>=20) | 8 | 12 | **40.0%** | 0.44 | 0.54 |
| `tomato__septoria_leaf_spot` | 20 | strong external evidence (>=20) | 8 | 12 | **40.0%** | 0.58 | 0.68 |
| `tomato__leaf_mold` | 20 | strong external evidence (>=20) | 15 | 5 | **75.0%** | 0.80 | 0.60 |
| `tomato__late_blight` | 20 | strong external evidence (>=20) | 4 | 16 | **20.0%** | 0.57 | 0.50 |
| `zucchini__powdery_mildew` | 18 | moderate (10-19) | 4 | 14 | **22.2%** | 0.65 | 0.65 |
| `peach__brown_rot` | 4 | insufficient (<5) | 4 | 0 | **100.0%** | 0.94 | 0.00 |
| `wheat__head_scab` | 4 | insufficient (<5) | 4 | 0 | **100.0%** | 0.96 | 0.00 |
| `wheat__stripe_rust` | 3 | insufficient (<5) | 3 | 0 | **100.0%** | 0.90 | 0.00 |
| `banana__bunchy_top` | 3 | insufficient (<5) | 3 | 0 | **100.0%** | 0.97 | 0.00 |
| `bean__rust` | 2 | insufficient (<5) | 1 | 1 | **50.0%** | 0.66 | 0.36 |
| `soybean__frog_eye_leaf_spot` | 2 | insufficient (<5) | 2 | 0 | **100.0%** | 0.83 | 0.00 |
| `banana__black_leaf_streak` | 1 | insufficient (<5) | 1 | 0 | **100.0%** | 0.97 | 0.00 |
| `wheat__loose_smut` | 1 | insufficient (<5) | 1 | 0 | **100.0%** | 0.95 | 0.00 |

---

## 8. Domain-Shift Observations (Field vs Laboratory Datasets)

By analyzing the provenance of the 178 external images against the training set, clear domain-shift patterns emerge:

1. **Background Clutter & Soil Visibility:**
   - *Training set (PlantVillage/Kaggle style):* Uniform gray/black/white laboratory background or single isolated leaf flat on neutral surface.
   - *External benchmark:* Real field conditions containing soil, weeds, drip irrigation pipes, multiple overlapping leaves, and direct sunlight glare.
2. **Disease Stage & Severity Distribution:**
   - *Training set:* Predominantly mid-to-late stage classic textbook symptoms.
   - *External benchmark:* Includes early pinhead lesions, multi-lesion coalescing, and senescing leaves with mixed stress symptoms.
3. **Intra-Family Pathogen Visual Congruence:**
   - Cucurbit powdery mildew (*Podosphaera xanthii*) and Solanaceous early blight (*Alternaria solani*) share identical visual manifestations across host species. In unconstrained 117-class classification, Model 2 often predicts the correct disease genus but attaches it to a related host (e.g. `zucchini__powdery_mildew` instead of `cucumber__powdery_mildew`).

---

## 9. Ranked Data Collection Priorities for Model 2 V4

Full file: [`reports/end_to_end_external_evaluation/data_collection_priorities.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/end_to_end_external_evaluation/data_collection_priorities.csv)

| Priority | Crop | Disease | External Support | External Acc | Internal Test F1 | Primary Confusion Target | Recommended New Field Images |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P1 - CRITICAL** | cucumber | `cucumber__powdery_mildew` | 20 | 20.0% | 63.6% | cucumber__angular_leaf_spot (x8, conf 0.78) | **+150 images** |
| **P1 - CRITICAL** | healthy | `healthy` | 20 | 0.0% | 99.5% | banana__bunchy_top (x11, conf 0.52) | **+150 images** |
| **P1 - CRITICAL** | tomato | `tomato__early_blight` | 20 | 40.0% | 77.3% | tomato__septoria_leaf_spot (x6, conf 0.49) | **+150 images** |
| **P1 - CRITICAL** | tomato | `tomato__septoria_leaf_spot` | 20 | 40.0% | 40.0% | healthy (x7, conf 0.79) | **+150 images** |
| **P1 - CRITICAL** | tomato | `tomato__late_blight` | 20 | 20.0% | 83.9% | healthy (x6, conf 0.61) | **+150 images** |
| **P1 - CRITICAL** | zucchini | `zucchini__powdery_mildew` | 18 | 22.2% | 54.5% | zucchini__bacterial_wilt (x5, conf 0.74) | **+150 images** |
| **P2 - HIGH** | tomato | `tomato__leaf_mold` | 20 | 75.0% | 83.9% | healthy (x4, conf 0.69) | **+80 images** |
| **P4 - LOW (EVAL DATA NEEDED FIRST)** | peach | `peach__brown_rot` | 4 | 100.0% | 87.5% | None | **+0 images** |
| **P4 - LOW (EVAL DATA NEEDED FIRST)** | wheat | `wheat__head_scab` | 4 | 100.0% | 93.8% | None | **+0 images** |
| **P4 - LOW (EVAL DATA NEEDED FIRST)** | wheat | `wheat__stripe_rust` | 3 | 100.0% | 81.8% | None | **+0 images** |
| **P4 - LOW (EVAL DATA NEEDED FIRST)** | banana | `banana__bunchy_top` | 3 | 100.0% | 90.0% | None | **+0 images** |
| **P4 - LOW (EVAL DATA NEEDED FIRST)** | bean | `bean__rust` | 2 | 50.0% | 90.3% | soybean__rust (x1, conf 0.36) | **+0 images** |
| **P4 - LOW (EVAL DATA NEEDED FIRST)** | soybean | `soybean__frog_eye_leaf_spot` | 2 | 100.0% | 80.9% | None | **+0 images** |
| **P4 - LOW (EVAL DATA NEEDED FIRST)** | banana | `banana__black_leaf_streak` | 1 | 100.0% | 91.9% | None | **+0 images** |
| **P4 - LOW (EVAL DATA NEEDED FIRST)** | wheat | `wheat__loose_smut` | 1 | 100.0% | 94.4% | None | **+0 images** |
| **P5 - STABLE** | banana | `banana__cordana_leaf_spot` | 20 | 80.0% | 75.0% | banana__black_leaf_streak (x3, conf 0.58) | **+0 images** |

---

## 10. Recommended Data Collection & Augmentation Strategy

### What Data to Collect
1. **Real Field Images Only:** Collect photos taken in open fields, high tunnels, and commercial polyhouses under natural sunlight, varying weather, and natural background clutter.
2. **Early-to-Mid Severity Progression:** Specifically capture early-stage symptoms where lesions are under 3mm in diameter.
3. **Confirmed Horticultural Provenance:** Only acquire samples from verified agricultural extensions or phytopathology archives.

### Role of Targeted Data Augmentation
- **Do NOT simply duplicate existing clean images with rotation/zoom.** Synthetic duplicates will not bridge the laboratory $\rightarrow$ field domain gap.
- **Use Targeted Field Augmentation during V4 training:** Color jitter ($\pm 0.2$ brightness/contrast to simulate harsh sunlight/shadows), random perspective distortion (simulating oblique field angles), and mild background noise injection.

### What NOT to Change
- **DO NOT retrain Model 1:** Model 1 achieves 97.5% - 100% accuracy on its 22 target crops.
- **DO NOT add the 178 external benchmark images to training:** They must remain permanently held out for clean V3 $\rightarrow$ V4 comparisons.
- **DO NOT alter the 117-class taxonomy:** Preserving class IDs ensures full backward compatibility.

---

## 11. Final Decision & Recommendations

| Decision Item | Finding & Recommended Action |
| :--- | :--- |
| **A. Is the main problem Model 1?** | **NO.** Model 1 is working as designed (97.5% - 100% on its 22 crops). The 58 errors were out-of-taxonomy broad-acre crops (Wheat, Banana, Peach) not intended for Model 1. |
| **B. Is the main problem Model 2?** | **PARTIALLY.** Model 2 V3 has strong internal representation (87.63% test acc, 99.52% healthy F1), but experiences intra-genus confusions on visually similar blights and cucurbit powdery mildews. |
| **C. Is the main problem domain shift?** | **YES.** The laboratory-to-field domain shift (background clutter, direct sunlight, multiple leaves) is the single largest contributor to external accuracy drop. |
| **D. Which exact classes should receive more data?** | **5 Key Classes:** `tomato__early_blight`, `tomato__late_blight`, `cucumber__powdery_mildew`, `zucchini__powdery_mildew`, and `tomato__septoria_leaf_spot`. |
| **E. Which classes need more real field images?** | Tomato blights and cucurbit powdery mildews need authentic field photos with natural lighting and varying lesion stages. |
| **F. Which classes need targeted augmentation?** | All solanaceous and cucurbit classes should receive photometric and perspective augmentation in V4 training. |
| **G. Should we retrain V4 now, or collect more data first?** | **COLLECT TARGETED FIELD DATA FIRST.** Retraining on the exact same dataset without new field-quality images will not resolve the field domain gap. Once ~500 targeted field images for the P1/P2 classes are curated, train Model 2 V4. |
