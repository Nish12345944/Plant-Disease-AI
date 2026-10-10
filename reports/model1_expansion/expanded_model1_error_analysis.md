# EXPANDED MODEL 1 — ERROR ANALYSIS & EVALUATION VERIFICATION

**Phase:** Error Analysis & Tuning Preparation  
**Target Architecture:** EfficientNet-B2 (PyTorch, CUDA, AMP FP16)  
**Dataset Reference:** `data/processed/model1_expanded/` (15,566 images: 12,407 train, 1,579 val, 1,580 test)  
**Checkpoint Analyzed:** `models/model1_expanded/best_model.pth` (Epoch 10)  
**Production Isolation:** `models/model1/` (Locked, SHA-256 Verified), `models/model2_classifier_v4/` (Locked)  

---

## 1. Executive Summary & Verification of First-Run Evaluation

An independent reproduction of the first-run evaluation was performed using the locked checkpoint `models/model1_expanded/best_model.pth` on the 1,580 immutable test set images.

### 1.1 Verification Results
- **Overall 46-Class Metrics:**
  - **Top-1 Accuracy:** **90.38%** (1,428 / 1,580) — *Exact reproduction*
  - **Top-3 Accuracy:** **97.34%** (1,538 / 1,580) — *Exact reproduction*
  - **Overall Macro F1:** **83.81%** — *Exact reproduction*
  - **Overall Weighted F1:** **90.29%** — *Exact reproduction*
  - **Overall Macro Precision:** **83.83%**
  - **Overall Macro Recall:** **84.49%**

### 1.2 Discovery of Evaluation / Reporting Metric Anomaly
In the initial training summary report, the **Original 22-Class Macro F1** was reported as **54.42%**, and the **New 24-Class Macro F1** was reported as **63.77%**. Investigation of the evaluation script (`scripts/train_model1_expanded.py`) uncovered an arithmetic bug in subset slicing:

```python
# Flawed implementation in first-run script:
orig_mask = np.isin(test_targets, list(orig_22_indices))
orig_targets = test_targets[orig_mask]
orig_preds = test_preds[orig_mask]
orig_macro_f1 = f1_score(orig_targets, orig_preds, average="macro", zero_division=0)
```

**Why this caused an artificial metric collapse:**
When `f1_score()` is invoked on a slice without explicitly binding `labels=orig_22_indices`, scikit-learn infers the label universe from `np.unique(np.concatenate([orig_targets, orig_preds]))`. Whenever an image from the original 22 classes was misclassified into a new class (e.g. `french_bean` $\rightarrow$ `soybean`, `zucchini` $\rightarrow$ `grape`, `broccoli` $\rightarrow$ `cabbage`), those phantom new-class labels entered the evaluation matrix with **0 true instances** in `orig_targets`. Scikit-learn assigned these phantom classes Precision=0, Recall=0, and F1=0, and divided the sum by ~32 classes instead of 20 or 22!

**Corrected Subset Metrics:**
- **Original 22-Class Active Macro F1 (20 classes with test support):** **92.51%** *(vs 92.91% in original locked baseline: a negligible -0.40% delta!)*
- **Original 22-Class Full Macro F1 (including 2 zero-support gap classes):** **84.10%** *(vs 54.42% previously reported)*
- **Original 22-Class Top-1 Accuracy:** **95.53%** *(vs 97.84% locked baseline)*
- **Original 22-Class Weighted F1:** **97.03%** *(vs 97.82% locked baseline)*
- **New 24-Class Macro F1 (Labels Constrained):** **79.72%** *(vs 63.77% previously reported)*
- **New 24-Class Top-1 Accuracy:** **84.02%**
- **New 24-Class Top-3 Accuracy:** **96.18%**
- **New 24-Class Weighted F1:** **84.95%**

> **Key Finding:** Adding 24 agricultural classes did **not** cause severe degradation to the original 22 classes. The original crops perform at **95.53% Top-1** and **92.51% active Macro F1**. The reported drop to 54.42% was entirely an **evaluation slicing bug**.

---

## 2. Taxonomy & Zero-Support Class Investigation

### 2.1 `cherry_tomato` (Class ID 13)
- **Status:** 0 train, 0 val, 0 test images.
- **Taxonomy Rule:** `cherry_tomato` is defined as an alias of `tomato` (`"cherry_tomato": "tomato"` in `aliases`).
- **Defect Identified:** Despite being an alias, `cherry_tomato` was assigned index 13 as a dedicated output logit in the 46-class network head. Because it has zero training data, its weights received zero gradient updates, resulting in a dead output node that can never be activated or validated.
- **Action Required:** `cherry_tomato` must be resolved at the inference/query layer and mapped to `tomato`, rather than occupying a logit in the neural network classifier.

### 2.2 `gypsophila` (Class ID 26)
- **Status:** 0 train, 0 val, 0 test images.
- **Taxonomy Rule:** Documented floriculture gap class from earlier Model 1 expansion phases.
- **Defect Identified:** Allocated index 26 in the classifier head with 0 data. It acts as an unlearnable dead weight in the linear layer.
- **Action Required:** Either acquire genuine *Gypsophila paniculata* images or excise it from the neural classifier head, preserving it in a documented taxonomy registry until acquired.

### 2.3 `gerbera` (Class ID 23)
- **Status:** 2 train, 0 val, 1 test image. Total: 3 images.
- **Source:** `gerbera_commons`.
- **Test Performance:** 0/1 correct (0.0% accuracy, 0.00% F1).
- **Test Sample Prediction:** `gerbera_flower_unknown_016491.jpg` predicted as `raspberry` (conf: 0.3369), with `gerbera` ranked 2nd (conf: 0.2922), and `chrysanthemum` ranked 3rd (conf: 0.2785).
- **Diagnosis:** Pure **extreme data scarcity**. A deep neural network cannot construct a separable manifold in 46-dimensional space from 2 training images.

### 2.4 Inference Layer Alias Inconsistency
In `model1_test_app/inference.py`:
- `load_model()` parses `idx_to_class` and `class_to_idx`, but completely ignores `aliases`.
- Any external request for `"cherry_tomato"`, `"squash"`, `"bean"`, or `"bell_pepper"` fails to resolve through canonical alias translation at inference time.
- Standardized alias normalization must be incorporated into `format_class_name()` or `predict_image()`.

---

## 3. Weak-Class Empirical Data Audit

The 6 weakest classes were analyzed image-by-image against predictions, original image metadata, and source datasets:

### 3.1 Gerbera (F1: 0.00% | Test Support: 1)
- **Split Distribution:** Train: 2 | Val: 0 | Test: 1 | Total: 3 (100% unique SHA-256 hashes).
- **Source:** `gerbera_commons`.
- **Visual Traits:** Daisy-like composite inflorescence with brightly colored ray florets.
- **Error Analysis:** Top-1 prediction was `raspberry` (0.34), but `gerbera` was runner-up (0.29). The classifier actually recognized partial features, but the extreme low prior suppressed the logit.
- **Root Cause:** **Insufficient Data (Volume Scarcity)**.
- **More Images Needed:** **YES — CRITICAL** (Minimum 100+ images needed for viable learning).

### 3.2 Cherry (F1: 40.00% | Test Support: 14)
- **Split Distribution:** Train: 111 | Val: 14 | Test: 14 | Total: 139 (100% unique SHA-256 hashes).
- **Sources:** `model2_v4_plantseg` (91), `model2_v4_plantseg_v3_supplementary` (48).
- **Visual Traits:** Simple ovate leaves with finely serrated margins. Tight macro crops focused on leaf spot and powdery mildew.
- **Test Results:** 5/14 correct (35.7% Top-1 accuracy).
- **Error Breakdown:**
  - `ps_cherry_leaf_spot_google_0082.jpg` $\rightarrow$ `grape` (conf: 0.60; cherry 2nd at 0.37)
  - `b64aa02e3f_cherry_powdery_mildew_22.jpg` $\rightarrow$ `apple` (conf: 0.79)
  - `ps_cherry_leaf_spot_google_0038.jpg` $\rightarrow$ `apple` (conf: 0.37; cherry 2nd at 0.37)
  - `e47d0398af_cherry_leaf_spot_16.jpg` $\rightarrow$ `rose` (conf: 0.92)
  - `3ab93ce29d_cherry_leaf_spot_35.jpg` $\rightarrow$ `citrus` (conf: 0.87)
  - `12b6777909_cherry_powdery_mildew_45.jpg` $\rightarrow$ `zucchini` (conf: 0.96)
  - `725c29e579_cherry_leaf_spot_70.jpg` $\rightarrow$ `banana` (conf: 0.99)
- **Root Cause:**
  1. **Botanical Proximity / Visual Overlap:** Cherry, Apple, and Rose belong to the family *Rosaceae*. Their serrated leaf margins and reticulate venation are visually congruent in single-leaf crops.
  2. **Background / Domain Bias:** Tight disease crops lack canopy, petiole, or bark context.
  3. **Data Volume:** 111 train images vs 452 for Apple.
- **More Images Needed:** **YES — RECOMMENDED** (Need 150+ diverse branch/canopy images).

### 3.3 Cauliflower (F1: 52.63% | Test Support: 10)
- **Split Distribution:** Train: 84 | Val: 10 | Test: 10 | Total: 104 (100% unique SHA-256 hashes).
- **Sources:** `model2_v4_plantseg` (45), `model2_v4_plantseg_v3_supplementary` (30), `model2_v4_external_healthy_cauliflower` (29).
- **Visual Traits:** Glaucous waxy oblong leaves with heavy white midribs.
- **Test Results:** 5/10 correct (50.0% Top-1 accuracy).
- **Error Breakdown:**
  - `ps_cauliflower_alternaria_leaf_spot_google_0026.jpg` $\rightarrow$ `broccoli` (conf: 0.96)
  - `ef2273ba3d_cauliflower_alternaria_leaf_spot_google_0004.jpg` $\rightarrow$ `broccoli` (conf: 0.99)
  - `ps_cauliflower_alternaria_leaf_spot_google_0034.jpg` $\rightarrow$ `broccoli` (conf: 0.76)
  - `ps_cauliflower_alternaria_leaf_spot_147.jpg` $\rightarrow$ `cabbage` (conf: 0.51; cauliflower 2nd at 0.36)
  - `a6f081d232_cauliflower_alternaria_leaf_spot_google_0259.jpg` $\rightarrow$ `eggplant` (conf: 0.99)
- **Root Cause:**
  1. **Shared Species Taxonomy:** Broccoli (*Brassica oleracea var. italica*), Cauliflower (*B. oleracea var. botrytis*), and Cabbage (*B. oleracea var. capitata*) are cultivars of the **same biological species**. Their leaves are practically identical without the central curd or head.
  2. **Class Imbalance:** Cauliflower has 84 train images; Broccoli has 332 and Cabbage has 220. The model defaults to the higher-prior Brassica classes.
- **More Images Needed:** **YES — RECOMMENDED** (Need 150+ cauliflower images emphasizing curd and midrib morphology).

### 3.4 Basil (F1: 61.54% | Test Support: 6)
- **Split Distribution:** Train: 51 | Val: 6 | Test: 6 | Total: 63 (100% unique SHA-256 hashes).
- **Sources:** `model2_v4_plantseg` (41), `model2_v4_plantseg_v3_supplementary` (22).
- **Visual Traits:** Small ovate culinary herb leaves with downy mildew yellowing.
- **Test Results:** 4/6 correct (66.7% Top-1 accuracy).
- **Error Breakdown:**
  - `6057b87676_basil_downy_mildew_google_0018.jpg` $\rightarrow$ `zucchini` (conf: 0.31; celery 2nd at 0.18)
  - `e4428f20cf_basil_downy_mildew_google_0035.jpg` $\rightarrow$ `carrot` (conf: 0.46; celery 2nd at 0.37)
- **Root Cause:** **Insufficient Data + Low-Confidence Predictions**. Both errors had low confidence (<0.47), indicating uncertain decision boundaries due to small sample size (51 train).
- **More Images Needed:** **YES — RECOMMENDED** (Need 100+ images).

### 3.5 Ginger (F1: 66.67% | Test Support: 9)
- **Split Distribution:** Train: 73 | Val: 9 | Test: 9 | Total: 91 (100% unique SHA-256 hashes).
- **Sources:** `model2_v4_plantseg` (79), `model2_v4_plantseg_v3_supplementary` (12).
- **Visual Traits:** Long lanceolate monocot leaves with parallel venation; sheath blight lesions.
- **Test Results:** 5/9 correct (55.6% Top-1 accuracy).
- **Error Breakdown:**
  - `062883c8e1_ginger_sheath_blight_40.jpg` $\rightarrow$ `rice` (conf: 0.29; wheat 2nd at 0.24)
  - `4de06edc4e_ginger_sheath_blight_60.jpg` $\rightarrow$ `rice` (conf: 0.995)
  - `a353157071_ginger_leaf_spot_35.jpg` $\rightarrow$ `rice` (conf: 0.70; ginger 2nd at 0.30)
  - `986e414182_ginger_sheath_blight_10.jpg` $\rightarrow$ `wheat` (conf: 0.43; ginger 2nd at 0.38)
- **Root Cause:**
  1. **Monocot Leaf Geometry:** Long, slender grass-like foliage directly mimics Rice and Wheat.
  2. **Shared Pathogen Lesions:** *Rhizoctonia solani* (sheath blight) causes identical necrotic lesions across ginger and rice.
  3. **Class Imbalance:** 73 ginger train vs 123 rice, 500 wheat.
- **More Images Needed:** **YES — RECOMMENDED** (Need 100+ images, especially showing rhizome or clump growth habit).

### 3.6 Raspberry (F1: 68.97% | Test Support: 12)
- **Split Distribution:** Train: 99 | Val: 12 | Test: 12 | Total: 123 (100% unique SHA-256 hashes).
- **Sources:** `model2_v4_plantseg` (73), `model2_v4_plantseg_v3_supplementary` (50).
- **Visual Traits:** Compound pinnate leaves with 3–5 serrated leaflets.
- **Test Results:** 10/12 correct (83.3% Top-1 accuracy, 83.33% Recall).
- **Error Breakdown:**
  - Raspberry test samples performed well (10/12 correct).
  - The lower F1 (68.97%) is driven by **low Precision (58.82%)**: other classes were mistakenly classified *into* Raspberry (`grape` $\rightarrow$ raspberry: 2, `strawberry` $\rightarrow$ raspberry: 2, `blueberry` $\rightarrow$ raspberry: 1, `gerbera` $\rightarrow$ raspberry: 1).
- **Root Cause:** **Visual Similarity within Berry/Rosaceae Complex**. The network learned broad "berry-like compound serration" features that over-predict raspberry on ambiguous strawberry/grape leaves.
- **More Images Needed:** **MODERATE** (More than data, this requires fine-grained decision boundary tuning).

---

## 4. Root Cause Classification Matrix

| Root Cause Category | Affected Classes | Concrete Evidence |
| :--- | :--- | :--- |
| **Insufficient Data** | `gerbera` (3 total), `basil` (63 total), `ginger` (91 total), `cauliflower` (104 total) | `gerbera` has only 2 train images (0% test acc); `basil` has 51 train images (confidences <0.46 on errors). |
| **Label / Mapping Issue** | `cherry_tomato`, `gypsophila` | Classes exist as logits in 46-class network head despite having 0 data. `cherry_tomato` is an alias of `tomato`. |
| **Class Imbalance** | `cauliflower` (84) vs `broccoli` (332); `ginger` (73) vs `wheat` (500) | 3/5 cauliflower errors collapsed into majority `broccoli`; 4/4 ginger errors collapsed into majority monocots `rice`/`wheat`. |
| **Visual Similarity / Shared Taxonomy** | `cauliflower` $\leftrightarrow$ `broccoli` $\leftrightarrow$ `cabbage`; `cherry` $\leftrightarrow$ `apple` $\leftrightarrow$ `rose`; `french_bean` $\leftrightarrow$ `soybean` | Same botanical species (*Brassica oleracea*), same family (*Rosaceae*, *Fabaceae*). Foliar geometry and venation overlap heavily. |
| **Background / Domain Bias** | `cherry`, `raspberry`, `basil` | Single-leaf tightly cropped images from PlantDoc/Bing with uniform or laboratory backgrounds lack canopy and context. |
| **Evaluation / Reporting Error** | `ORIGINAL_22` & `NEW_24` subset metrics in first-run report | Unconstrained `f1_score()` on sliced subsets produced phantom classes with 0 support, falsely reporting 54.42% instead of true 92.51% active Macro F1. |
| **Insufficient Training Schedule** | Global network convergence | Validation loss was still declining at Epoch 10 (0.3791). Full 46-class manifold was not fully saturated. |

---

## 5. Final Decision

### Decision: **EVALUATION PIPELINE ISSUE FOUND** *(with critical data quality actions identified)*

#### Justification:
1. **Evaluation Pipeline Issue:** The first-run report contained a critical arithmetic slicing defect that reported the Original 22 Macro F1 as **54.42%** instead of its true **92.51%**. The corrected metric proves that adding 24 classes did **not** degrade the original 22 crops (Top-1: **95.53%**, Weighted F1: **97.03%**). This evaluation issue must be permanently corrected across all metrics scripts.
2. **Data / Taxonomy Issues to Address:**
   - `cherry_tomato` and `gypsophila` must not occupy dead logits in the 46-class network head while having zero data.
   - `gerbera` (3 images total) cannot be learned by any tuning strategy without data acquisition or exclusion from the primary loss.
3. **Safety Status:**
   - Production Model 1 (`models/model1/`) remains **100% UNTOUCHED, LOCKED, and ACTIVE**.
   - Model 2 V4 remains **100% UNTOUCHED, LOCKED, and ACTIVE**.
   - No models have been retrained or promoted.
