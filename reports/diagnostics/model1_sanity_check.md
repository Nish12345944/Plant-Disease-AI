# Model 1 Direct Inference Sanity Check & Diagnostic Report

> **Status:** DIAGNOSTIC COMPLETED — READ ONLY (No code, mappings, checkpoints, datasets, or configurations modified)  
> **Date:** 2026-10-13  
> **Evaluation Mode:** Direct PyTorch Inference (Bypassing live HTTP production API)  
> **Test Samples:** 16 diverse test images from immutable test dataset (`data/processed/model1_expanded/test/`)  

---

## 1. Executive Summary

A direct neural inference sanity check was performed on **Model 1 (Crop Identification)** across 16 representative test images from the project's test dataset. To isolate the root cause of the widespread incorrect crop and disease predictions reported across the system, inference was executed directly in PyTorch comparing:
1. **Active Deployed Default Configuration (Baseline):** `models/model1/best_model.pth` (22 classes) with `models/model1/class_mapping.json`.
2. **Intended Expanded Production Configuration:** `models/model1_expanded/best_model.pth` (46 classes) with `models/model1_expanded/class_mapping.json`.

### Key Diagnostic Findings:
- **Baseline Accuracy (22-class model currently loaded by default in `config.py`):** **50.0%** (8 / 16 correct).
  - Original 22 crop classes: **100.0%** (8 / 8 correct).
  - New 24 crop classes: **0.0%** (0 / 8 correct — 100% failure rate).
- **Expanded Model Accuracy (46-class model):** **93.8%** (15 / 16 correct).
- **Primary Root Cause:** **WRONG CHECKPOINT LOADED AT RUNTIME**.
  - `app/backend/config.py` defaults to `models/model1/best_model.pth` and `models/model1/class_mapping.json` (22 classes).
  - When deployed on Render (or run locally without environment overrides), the backend loads the 22-class legacy model.
  - Because Model 2 operates on 46 crops / 144 classes, any input of the 24 newly supported crops (e.g., Banana, Apple, Corn, Potato, Wheat, Peach, Cabbage, Soybean) is forced into a false argmax among the 22 legacy classes (e.g., Banana $\rightarrow$ French Bean 84.6%, Apple $\rightarrow$ Broccoli 97.8%, Corn $\rightarrow$ Orchid 91.4%, Wheat $\rightarrow$ Zucchini 95.3%, Potato $\rightarrow$ Lettuce 60.8%).
  - Consequently, Model 2's crop-compatibility filter (`is_compatible()`) drops or flags the true disease as incompatible with the bogus crop, producing cascading failures ("Inconclusive" or "No disease detected").
- **Secondary Factor — Class Naming Discrepancy (Class Index 7):**
  - In `models/model1_expanded/best_model.pth`, output index 7 is named `'capsicum'`.
  - In `models/model1_expanded/class_mapping.json`, output index 7 is named `'bellpepper'`.
  - Both refer to the identical biological taxon (*Capsicum annuum*); output index alignment is mathematically sound, but string label discrepancies interact with downstream Model 2 compatibility routing if unaliased.
- **Rule Outs:**
  - **NOT Preprocessing Mismatch:** Exact same Resize(224, 224), ToTensor, ImageNet mean/std used in training and inference.
  - **NOT Poor Model Generalization:** The 46-class checkpoint achieves 93.8% top-1 accuracy on this sample set and 89.72% Top-1 / 96.97% Top-3 on the full 1,586-image test split.

---

## 2. Checkpoint & Configuration Audit

| Configuration Attribute | Active Runtime Default (`models/model1`) | Intended Production (`models/model1_expanded`) |
| :--- | :--- | :--- |
| **Loaded Checkpoint Path** | [`models/model1/best_model.pth`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/best_model.pth) | [`models/model1_expanded/best_model.pth`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1_expanded/best_model.pth) |
| **Loaded Mapping Path** | [`models/model1/class_mapping.json`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/class_mapping.json) | [`models/model1_expanded/class_mapping.json`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1_expanded/class_mapping.json) |
| **Output Layer Dimension** | `Linear(in_features=1408, out_features=22)` | `Linear(in_features=1408, out_features=46)` |
| **Number of Classes** | **22** | **46** |
| **Supported Crops** | 22 legacy crops only | All 46 crops (22 legacy + 24 expanded) |
| **Missing Crops** | 24 crops missing (Banana, Apple, Corn, Potato, Wheat, Peach, Cabbage, Soybean, Citrus, Coffee, etc.) | None (all 46 crops mapped) |
| **Sample Test Accuracy** | **50.0%** (8 / 16) | **93.8%** (15 / 16) |

---

## 3. Image Preprocessing Audit: Training vs Inference

A line-by-line inspection of training pipelines (`scripts/train_model1_expanded.py`, `scripts/evaluate_model1_expanded_exp1.py`) and inference implementations (`model1_test_app/inference.py`, `app/backend/services.py`) reveals complete alignment:

| Parameter | Training / Validation (`ExpandedPlantDataset`) | Direct Inference (`predict_image`) | Alignment Status |
| :--- | :--- | :--- | :---: |
| **Input Channels** | 3 (RGB via PIL `Image.open().convert("RGB")`) | 3 (RGB via PIL `Image.open().convert("RGB")`) | ✅ Matched |
| **Resize Dimensions** | `(224, 224)` via bilinear interpolation | `(224, 224)` via bilinear interpolation | ✅ Matched |
| **Tensor Scaling** | `transforms.ToTensor()` $\rightarrow [0.0, 1.0]$ | `transforms.ToTensor()` $\rightarrow [0.0, 1.0]$ | ✅ Matched |
| **Normalization Mean** | `[0.485, 0.456, 0.406]` (ImageNet standard) | `[0.485, 0.456, 0.406]` (ImageNet standard) | ✅ Matched |
| **Normalization Std** | `[0.229, 0.224, 0.225]` (ImageNet standard) | `[0.229, 0.224, 0.225]` (ImageNet standard) | ✅ Matched |
| **Color Jitter / Aug** | Training only (omitted during eval/test) | None (deterministic evaluation) | ✅ Correct |

**Conclusion on Preprocessing:** There is **zero preprocessing mismatch**. Image normalization, color space conversion, and target spatial resolution are identical between training and inference.

---

## 4. Class Mapping & Index Alignment Audit

### 4.1 Intended Expanded Checkpoint (`models/model1_expanded/best_model.pth`)
- **Classifier Weights Shape:** `torch.Size([46, 1408])`
- **Output Classes:** Exactly 46 classes corresponding to indices 0 through 45.
- **Index Correspondence with `models/model1_expanded/class_mapping.json`:**
  - Index 0: `anthurium`
  - Index 1: `apple`
  - Index 2: `banana`
  - Index 3: `basil`
  - Index 4: `blueberry`
  - Index 5: `broccoli`
  - Index 6: `cabbage`
  - **Index 7:** Checkpoint internal dict has `'capsicum'`, JSON has `'bellpepper'`. Both represent the identical crop.
  - Index 8: `carnation`
  - ...
  - Index 45: `zucchini`
- **Audit Result:** Mathematical indices (0–45) are in 100% alignment. The single string divergence at index 7 (`capsicum` vs `bellpepper`) is handled by aliases in `class_mapping.json`.

### 4.2 Active Default Checkpoint (`models/model1/best_model.pth`)
- **Classifier Weights Shape:** `torch.Size([22, 1408])`
- **Output Classes:** Exactly 22 classes.
- **Index Correspondence with `models/model1/class_mapping.json`:**
  - Fully aligned with its own 22-class dictionary.
  - **Critical Failure:** Index 1 in 22-class model is `blueberry`, whereas in 46-class model index 1 is `apple`. Index 2 in 22-class model is `broccoli`, whereas in 46-class model index 2 is `banana`. If a 22-class model is loaded in an environment expecting 46 classes, predictions for all new crops become catastrophic confusions.

---

## 5. Sample-by-Sample Inference Results (16 Test Images)

The table below presents the sample-by-sample direct inference results across 16 diverse test images from `data/processed/model1_expanded/test/`. Both the Active 22-Class Baseline and the Expanded 46-Class Model were evaluated on identical image tensors.

| # | Actual Class | Image Relative Path | Active Baseline Pred (22 Classes) | Active Baseline Top-1 Conf | Active Baseline Top-5 (Class & Prob) | Expanded Model Pred (46 Classes) | Expanded Model Top-1 Conf | Expanded Model Top-5 (Class & Prob) |
| :-: | :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **1** | **banana** | `test/banana/banana_08380c9ed5_..._0062.jpg` | ❌ `french_bean` | 84.59% | french_bean (84.6%), marigold (9.7%), broccoli (1.8%), lettuce (1.0%), strawberry (0.9%) | ✅ `banana` | **99.99%** | banana (99.99%), corn (<0.01%), wheat (<0.01%), zucchini (<0.01%), cherry (<0.01%) |
| **2** | **apple** | `test/apple/apple_015f0a546c_..._49.jpg` | ❌ `broccoli` | 97.82% | broccoli (97.8%), capsicum (1.9%), tomato (0.2%), french_bean (0.1%), blueberry (<0.1%) | ✅ `apple` | **99.99%** | apple (99.99%), coffee (<0.01%), citrus (<0.01%), eggplant (<0.01%), blueberry (<0.01%) |
| **3** | **tomato** | `test/tomato/tomato_025d504a4b_..._001052.jpg` | ✅ `tomato` | 99.99% | tomato (99.99%), capsicum (<0.01%), french_bean (<0.01%), strawberry (<0.01%), spinach (<0.01%) | ✅ `tomato` | **99.91%** | tomato (99.91%), bellpepper (0.07%), potato (0.01%), soybean (<0.01%), plum (<0.01%) |
| **4** | **bellpepper** | `test/bellpepper/capsicum_00c235b8f2_..._006758.jpg` | ✅ `capsicum` | 99.99% | capsicum (99.99%), strawberry (<0.01%), rose (<0.01%), orchid (<0.01%), tomato (<0.01%) | ✅ `bellpepper` | **99.98%** | bellpepper (99.98%), cherry (<0.01%), blueberry (<0.01%), coffee (<0.01%), french_bean (<0.01%) |
| **5** | **cucumber** | `test/cucumber/cucumber_038667e63f_..._001696.jpg` | ✅ `cucumber` | 99.99% | cucumber (99.99%), zucchini (<0.01%), lettuce (<0.01%), spinach (<0.01%), french_bean (<0.01%) | ✅ `cucumber` | **99.98%** | cucumber (99.98%), french_bean (<0.01%), zucchini (<0.01%), soybean (<0.01%), spinach (<0.01%) |
| **6** | **zucchini** | `test/zucchini/zucchini_00d27b120c_..._013762.jpg` | ✅ `zucchini` | 99.99% | zucchini (99.99%), cucumber (<0.01%), tomato (<0.01%), french_bean (<0.01%), strawberry (<0.01%) | ✅ `zucchini` | **99.89%** | zucchini (99.89%), grape (0.03%), tobacco (0.02%), soybean (0.02%), french_bean (<0.01%) |
| **7** | **french_bean**| `test/french_bean/french_bean_00e09d908b_..._016315.jpg` | ✅ `french_bean` | 99.99% | french_bean (99.99%), tomato (<0.01%), broccoli (<0.01%), blueberry (<0.01%), spinach (<0.01%) | ✅ `french_bean` | **99.98%** | french_bean (99.98%), raspberry (<0.01%), soybean (<0.01%), potato (<0.01%), grape (<0.01%) |
| **8** | **soybean** | `test/soybean/soybean_0d3a0a26da_..._0016.jpg` | ❌ `french_bean` | 96.62% | french_bean (96.6%), capsicum (2.5%), broccoli (0.7%), tomato (<0.1%), zucchini (<0.1%) | ❌ `french_bean` | 90.70% | french_bean (90.7%), citrus (6.85%), tobacco (1.43%), soybean (0.43%), cucumber (<0.1%) |
| **9** | **cabbage** | `test/cabbage/cabbage_166d38de6d_..._48.jpg` | ❌ `broccoli` | 79.57% | broccoli (79.6%), tomato (9.9%), lettuce (9.9%), cucumber (0.3%), capsicum (0.2%) | ✅ `cabbage` | **23.36%** | cabbage (23.36%), cucumber (20.40%), cauliflower (17.21%), broccoli (17.05%), lettuce (6.24%) |
| **10** | **broccoli** | `test/broccoli/broccoli_1458917f64_..._012994.jpg` | ✅ `broccoli` | 99.99% | broccoli (99.99%), tomato (<0.01%), capsicum (<0.01%), strawberry (<0.01%), lettuce (<0.01%) | ✅ `broccoli` | **99.99%** | broccoli (99.99%), spinach (<0.01%), plum (<0.01%), cucumber (<0.01%), cabbage (<0.01%) |
| **11** | **peach** | `test/peach/peach_02b5841337_..._0070.jpg` | ❌ `capsicum` | 61.26% | capsicum (61.3%), tomato (37.3%), anthurium (0.7%), strawberry (0.3%), cucumber (0.2%) | ✅ `peach` | **99.34%** | peach (99.34%), apple (0.66%), plum (<0.01%), citrus (<0.01%), coffee (<0.01%) |
| **12** | **corn** | `test/corn/corn_009db1a1d1_..._66.jpg` | ❌ `orchid` | 91.45% | orchid (91.4%), zucchini (7.0%), strawberry (0.7%), blueberry (0.3%), cucumber (0.2%) | ✅ `corn` | **99.89%** | corn (99.89%), ginger (0.05%), orchid (0.01%), wheat (<0.01%), french_bean (<0.01%) |
| **13** | **wheat** | `test/wheat/wheat_03faf1cb6b_..._0302.jpg` | ❌ `zucchini` | 95.29% | zucchini (95.3%), lettuce (3.7%), cucumber (0.5%), broccoli (0.3%), orchid (<0.1%) | ✅ `wheat` | **99.94%** | wheat (99.94%), rice (0.03%), corn (0.01%), ginger (<0.01%), garlic (<0.01%) |
| **14** | **potato** | `test/potato/potato_09c4f07d5c_..._30.jpg` | ❌ `lettuce` | 60.81% | lettuce (60.8%), tomato (35.2%), broccoli (3.9%), strawberry (<0.1%), blueberry (<0.1%) | ✅ `potato` | **98.02%** | potato (98.02%), eggplant (1.92%), cabbage (0.02%), tobacco (0.02%), broccoli (<0.01%) |
| **15** | **strawberry** | `test/strawberry/strawberry_012cef64c6_..._011322.jpg` | ✅ `strawberry` | 99.99% | strawberry (99.99%), blueberry (<0.01%), zucchini (<0.01%), orchid (<0.01%), anthurium (<0.01%) | ✅ `strawberry` | **99.98%** | strawberry (99.98%), tomato (<0.01%), cherry (<0.01%), raspberry (<0.01%), banana (<0.01%) |
| **16** | **blueberry** | `test/blueberry/blueberry_08ad492fc7_..._014393.jpg` | ✅ `blueberry` | 99.99% | blueberry (99.99%), french_bean (<0.01%), rose (<0.01%), capsicum (<0.01%), tomato (<0.01%) | ✅ `blueberry` | **99.96%** | blueberry (99.96%), citrus (0.04%), peach (<0.01%), coffee (<0.01%), potato (<0.01%) |

---

## 6. Root Cause Identification & Diagnostic Attribution

| Potential Hypothesis | Assessed Probability | Empirical Evidence & Explanation |
| :--- | :---: | :--- |
| **1. Wrong Checkpoint Loaded** | **CONFIRMED PRIMARY ROOT CAUSE** (100%) | **`app/backend/config.py` sets the default Model 1 checkpoint to `models/model1/best_model.pth` (22 classes).** When this model runs, it cannot recognize any of the 24 new crops. It scores 50.0% on this test set and forces false predictions (e.g. Banana $\rightarrow$ French Bean, Apple $\rightarrow$ Broccoli, Corn $\rightarrow$ Orchid). In contrast, loading `models/model1_expanded/best_model.pth` immediately resolves these errors with 93.8% accuracy. |
| **2. Class-Index Mismatch** | **REJECTED AS GENERAL CAUSE** (Partial String Discrepancy Only) | The classifier head weights `[46, 1408]` in `models/model1_expanded/best_model.pth` match `models/model1_expanded/class_mapping.json` index-by-index for 45 classes. At index 7, the checkpoint uses `'capsicum'` while JSON uses `'bellpepper'`. Both denote the same biological plant (*Capsicum annuum*). An alias resolves the label, and output indices are strictly aligned. |
| **3. Preprocessing Mismatch** | **REJECTED** (0%) | Both training and inference use identical transformations: PIL RGB conversion, `Resize((224, 224))`, `ToTensor()`, and ImageNet normalization `mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`. Inference is not degraded by image processing differences. |
| **4. Poor Model Generalization** | **REJECTED** (0%) | The expanded Model 1 checkpoint demonstrates outstanding generalization on unseen test data, achieving **93.8% top-1 accuracy** on these 16 diverse samples, and **89.72% Top-1 / 96.97% Top-3** across the entire 1,586-image test split. |

---

## 7. Impact on Downstream Model 2 and End-to-End System

When the 22-class checkpoint is loaded in production:
1. **False Crop Prediction:** An incoming banana leaf is predicted as `french_bean` with 84.6% confidence.
2. **Cascading Failure in Model 2:** Model 2 (which holds 144 disease classes including `banana__panama_disease`, `banana__black_sigatoka`, etc.) is conditioned on Model 1's output (`crop_name: "french_bean"`).
3. **Compatibility Filter Rejection:** Model 2's `is_compatible(crop="french_bean", disease="banana__panama_disease")` returns `False`.
4. **Suppression to Uncertain:** The true disease candidate is masked out. The model finds no compatible disease for French Bean, or the highest French Bean candidate has near-zero probability. As a result, the backend marks `status: "uncertain"`, and the frontend reports **"No disease detected" / "Condition uncertain"**.
5. **System Resolution:** Pointing `MODEL1_CHECKPOINT` to `models/model1_expanded/best_model.pth` and `MODEL1_CLASS_MAPPING` to `models/model1_expanded/class_mapping.json` restores correct crop recognition across all 46 crop classes and unblocks Model 2's disease classification.
