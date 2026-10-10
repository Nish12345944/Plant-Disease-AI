# Training Readiness Assessment (Post-Manual Changes Audit)

**Date:** 2026-10-09  
**Audit Status:** Complete  
**Scope:** Model 1 (Plant Identification) & Model 2 (Crop Disease Classification) datasets

---

## 1. Executive Training Verdicts

| Target Model | Dataset Directory | Readiness Verdict | Primary Reason |
|---|---|:---:|---|
| **Model 1 Production (Balanced)** | `data/processed/model1_balanced/` | **READY (Clean)** | Unmodified since original training; 0 missing, 0 added, 0 test leakage. |
| **Model 1 Expansion (46 Classes)** | `data/processed/model1_expanded/` | **NOT SAFE (BLOCKED)** | **Test-Train Data Leakage**: 7 exact duplicate images in test+train, 6 in val+train, 18 near duplicates, and manifest is out of sync (+1,483 unmanifested images, -1 missing file). |
| **Model 2 Classifier v4 (117 Classes)** | `data/processed/model2_v4/` | **NOT SAFE (BLOCKED)** | **Critical Taxonomy & Split Breakage**: Broken folder hierarchy in `train/cauliflower`, unmapped classes added (`bell_pepper`, `plum`), 83 original baseline training images displaced, 2 exact test-train duplicate leakages, 954 intra-split duplicate files, and non-disease disorder (`Purple Tinges`) injected. |

---

## 2. Blocking Problems (Must Fix Before Any Retraining)

### Model 1 Expanded (Plant Identifier)
1. **Critical Split Leakage (Train vs. Test & Val):**
   - **7 exact duplicate images** (identical SHA-256) exist across `train` and `test` splits (e.g. in `capsicum`).
   - **6 exact duplicate images** exist across `train` and `val` splits.
   - **18 near-duplicate image pairs** (perceptual hash Hamming distance $\le 4$) exist across splits (e.g., `download-13-_jpeg.rf...` in `train/basil` vs `basil_07e6b14a6e...` in `val/basil`).
   - Training on these leaked images will artificially inflate test accuracy and invalidate generalization benchmarks.
2. **Manifest Desynchronization:**
   - Manifest `model1_expanded_manifest.csv` records 15,566 images; disk contains 17,048 files (**1,483 unrecorded images** across `basil`, `cauliflower`, `tobacco`, `coffee`, `capsicum`, and `plum`).
   - **1 image missing** from disk: `train/coffee/coffee_11ed103b8a_11ed103b8a_coffee_leaf_rust_google_0173.jpg`.

### Model 2 Classifier v4 (Disease Classifier)
1. **Directory Structure & Class Mapping Incompatibility:**
   - In `train/cauliflower/`, the 3 canonical Model 2 class folders were replaced by 12 raw source folders. Standard training scripts loading `<crop>__<disease>` will fail with KeyErrors or assign incorrect class indices.
   - In `train/bell_pepper/`, three unmapped disorder classes were added: `Leaf_Curl` (485 images), `PepperBell_Nutrition Deficiency` (444 images), and `Cerespora` (281 images). None exist in `models/model2_classifier_v4/class_mapping.json`.
   - In `train/plum/`, `shot hole` contains a space in the directory name, and `healthy_leaf` vs `healthy_fruit` are unmapped split folders.
2. **Missing/Displaced Baseline Training Images:**
   - All **83 original cauliflower training images** are missing from their canonical directories (`train/cauliflower/alternaria_leaf_spot`, `bacterial_soft_rot`, `healthy`). 34 images were removed completely.
3. **Exact Test-Train Leakage in Model 2:**
   - **2 exact duplicate images** exist across `train` and `test` in Model 2.
4. **Intra-Split Duplication & Data Contamination:**
   - **954 duplicate files** within training splits (e.g., `cauliflower_leaf_Downy Mildew` contains 153 redundant duplicates of the same images).
   - Physiological condition (`Purple Tinges`, 153 images) and pest damage (`Insect Hole`, 639 images) were introduced as disease categories.
   - Severe plant part mixing (1,461 curd images mixed into foliar disease models).

---

## 3. Non-Blocking Concerns

1. **Severe Class Imbalance in Training Split:**
   - `cauliflower_leaf_Healthy` contains 1,859 images, whereas `cauliflower_fruit_Alternaria Brassicae` has only 45 images (41:1 imbalance ratio).
2. **Unused External Data:**
   - The candidate folders in `data/external/` contain valid candidate images that have not yet been curated or formally vetted.

---

## 4. Exact Recommended Corrective Actions (In Order)

To safely prepare both datasets for retraining without compromising benchmarks or model integrity, execute these steps sequentially:

### Step 1: Quarantine and Freeze Current Data
- Do **not** trigger training runs for Model 1 Expanded or Model 2 Classifier v4.
- Model 1 Balanced (`data/processed/model1_balanced/`) and all production test sets (`data/processed/*/test/`) remain clean and protected.

### Step 2: Clean Model 1 Expanded Dataset
1. **Remove Leaked Training Images:**
   - Delete the 7 exact test-duplicate images and 6 val-duplicate images from `data/processed/model1_expanded/train/` (detailed paths in `duplicate_and_leakage_report.csv`).
2. **Reconcile Manifest:**
   - Audit the remaining 1,470 new training images for quality.
   - Update `model1_expanded_manifest.csv` with the verified images and remove the missing coffee image entry.

### Step 3: Restructure Model 2 Cauliflower & Special Classes
1. **Restore Canonical Cauliflower Folders:**
   - Recreate canonical directories in `data/processed/model2_v4/train/cauliflower/`:
     - `alternaria_leaf_spot/`
     - `bacterial_soft_rot/`
     - `healthy/`
2. **Filter & Clean Cauliflower Candidates:**
   - **Discard:** `cauliflower_fruit_Purple Tinges` (physiological) and `cauliflower_leaf_Insect Hole` (pest damage).
   - **Deduplicate:** Purge the 153 duplicate files in `cauliflower_leaf_Downy Mildew`.
   - **Map Foliar Images:** Route verified foliar images from `cauliflower_leaf_Alternaria Leaf Spot` into `cauliflower/alternaria_leaf_spot/`, and `cauliflower_leaf_Healthy` into `cauliflower/healthy/`.
   - **Curd Decision:** If curd symptoms are excluded from foliar Model 2, quarantine the 7 `cauliflower_fruit_*` folders into a separate produce dataset.
3. **Clean Bell Pepper & Plum Folders:**
   - Rename `train/plum/shot hole` to `train/plum/shot_hole`.
   - Reconcile `train/bell_pepper/Cerespora` to `cercospora_leaf_spot` or remove if unmapped.
   - Move unmapped `Leaf_Curl` and `Nutrition Deficiency` out of the disease training directory.
4. **Purge Test Leakage in Model 2:**
   - Delete the 2 training images that duplicate test-set items.

### Step 4: Validate and Regenerate Manifests
1. Run automated split-integrity verification script to ensure 0 exact duplicates and 0 near duplicates across `train`, `val`, and `test`.
2. Regenerate `data/processed/model2_v4/model2_v4_manifest.csv` and `data/processed/model1_expanded_manifest.csv`.
3. Verify that all directory names strictly match `models/model2_classifier_v4/class_mapping.json`.

### Step 5: Proceed to Supervised Retraining
- Only once Steps 1–4 are validated with 0 errors and verified manifests, proceed with model retraining.
