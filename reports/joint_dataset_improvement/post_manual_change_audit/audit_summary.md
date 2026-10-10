# Post-Manual Changes Dataset Audit Summary

**Audit Timestamp:** 2026-10-09  
**Target Project:** `Disease_prediction`  
**Audit Scope:** Deep, read-only audit of all processed datasets, manifests, class mappings, test splits, and manual additions for Model 1 and Model 2.  
**Safety Protocol Executed:** Strict read-only audit. 56 baseline manifests and metadata files were backed up to `backups/pre_audit_snapshot/`. No image was moved, renamed, relabeled, deleted, or altered.

---

## 1. Overall Dataset Status

| Dataset Directory | Associated Model | Baseline Count | Current Disk Count | Net Discrepancy | Modification Status | Safety Verdict |
|---|---|:---:|:---:|:---:|:---:|:---:|
| `data/processed/model1_balanced/` | Model 1 Production (22 classes) | 16,537 | 16,537 | 0 | **Unchanged (Clean)** | **SAFE** |
| `data/processed/model1_expanded/` | Model 1 Expansion (46 classes) | 15,566 | 17,048 | +1,482 | **Modified (+1,483 new, -1 missing)** | **NOT SAFE (BLOCKED)** |
| `data/processed/model2_v4/` | Model 2 Classifier v4 (117 classes) | 19,920 | 29,230 | +9,310 | **Severely Modified (+9,393 new, -83 displaced)** | **NOT SAFE (BLOCKED)** |

---

## 2. Exact Directories Affected

1. **`data/processed/model1_expanded/train/`**  
   - **`basil/`**: +517 images
   - **`cauliflower/`**: +341 images
   - **`tobacco/`**: +190 images
   - **`coffee/`**: +176 images (and 1 original image missing)
   - **`capsicum/`**: +131 images
   - **`plum/`**: +128 images
2. **`data/processed/model2_v4/train/`**  
   - **`cauliflower/`**: Completely replaced. The 3 canonical folders (`alternaria_leaf_spot`, `bacterial_soft_rot`, `healthy`) were removed; **12 raw source folders** with **6,042 images** were added.
   - **`bell_pepper/`**: +1,728 images added across 6 folders including unmapped disorder classes (`Leaf_Curl`, `PepperBell_Nutrition Deficiency`, `Cerespora`).
   - **`plum/`**: +1,269 images added across 4 folders including unmapped names and formatting errors (`healthy_leaf`, `healthy_fruit`, `shot hole`).
   - **`basil/`**: +354 images added to `downy_mildew`.

---

## 3. Main Discrepancies & Audit Findings

### A. Test Set & Split Integrity
- **Immutable Test Sets Unchanged on Disk:** The existing test sets in `model1_balanced/test/` (1,663 files), `model1_expanded/test/` (1,580 files), and `model2_v4/test/` (2,304 files) have **zero files deleted or modified**, and no images were placed directly into test folders.
- **Split Leakage via Added Training Images:**
  - In `model1_expanded`, **7 newly added training images** are exact SHA-256 duplicates of existing `test/` images, and **6 images** duplicate existing `val/` images (primarily in `capsicum`).
  - In `model2_v4`, **2 newly added training images** duplicate existing `test/` images.
  - In `model1_expanded`, **18 near-duplicate pairs** (pHash Hamming distance $\le 4$) were detected across splits.

### B. Class Mapping & Taxonomy Violations
- **Model 1 (Expanded):** Current directory names match the 46 target classes in `models/model1_expanded/class_mapping.json`. However, manifest `model1_expanded_manifest.csv` is out of sync by 1,483 files.
- **Model 2 (Classifier v4):** 
  - Standard training will **fail** because `models/model2_classifier_v4/class_mapping.json` (117 classes) does not match the modified folder structure in `train/cauliflower/`, `train/bell_pepper/`, and `train/plum/`.
  - In `train/cauliflower/`, classes like `cauliflower__alternaria_leaf_spot` and `cauliflower__bacterial_soft_rot` are completely missing from the training split.
  - Folders with spaces (`plum/shot hole`), misspellings (`bell_pepper/Cerespora`), and unmapped disorders (`Purple Tinges`, `Nutrition Deficiency`, `Leaf_Curl`, `Insect Hole`) have been injected.

### C. Duplication & Contamination
- **1,066 total duplicate instances** identified across the processed datasets.
- `data/processed/model2_v4/` contains **954 intra-split duplicates**, including 153 redundant copies in `cauliflower_leaf_Downy Mildew` alone.
- `cauliflower_fruit_Bacterial Spot` and `cauliflower_fruit_Bacterial spot rot` share 14 exact duplicates.

---

## 4. Training Safety Verdict

| Model | Status | Action Required |
|---|:---:|---|
| **Model 1 Production** | **SAFE** | Can be evaluated or retained with existing checkpoint (`models/model1/best_model.pth`). |
| **Model 1 Expanded** | **UNSAFE (BLOCKED)** | Must remove 7 test-leaking and 6 val-leaking training images and reconcile manifest before retraining. |
| **Model 2 Classifier v4** | **UNSAFE (BLOCKED)** | Must restore canonical cauliflower structure, remove unmapped folders, deduplicate, and reconcile manifest before retraining. |

Detailed breakdowns and ordered recovery steps are available in:
- `model1_changes.csv`
- `model2_changes.csv`
- `duplicate_and_leakage_report.csv`
- `cauliflower_label_review.md`
- `training_readiness.md`
