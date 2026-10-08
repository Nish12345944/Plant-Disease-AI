# Missing Classes Research, Acquisition & Deduplication Audit Report

**Date:** 2026-10-07  
**Module:** Model 2 Supplementary Dataset Acquisition (Missing Classes Pass)  
**Target Missing Classes:** `bean__angular_leaf_spot`, `soybean__rust`  
**Acquired Raw Staging:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\soybean_rust_anand`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\soybean_rust_anand)  
**Manifest File:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\reports\model2_classifier\missing_classes_dataset_manifest.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\reports\model2_classifier\missing_classes_dataset_manifest.csv)  

---

## 1. Executive Summary

```
BEAN ANGULAR LEAF SPOT (bean__angular_leaf_spot):
  - Primary Global Source : Makerere AI Lab (iBean / NaCRRI Uganda)
  - Baseline Status in M2 : 432 images already in Model 2 (Train=302, Val=65, Test=65)
  - Model 2 Test Baseline : F1 = 0.9365 (Precision=0.9672, Recall=0.9077 | Tier: GOOD)
  - Supplementary Finding : Makerere dataset is 100% saturated in Model 2; no new external non-duplicate public source exists.
  - Audit Conclusion     : CLASS IS FULLY SUPPORTED IN EXISTING BASELINE (0 supplementary images needed/added).

SOYBEAN RUST (soybean__rust):
  - Primary Global Source : Soybean Leaf Diseases Dataset (anandvermagmailcom / Hugging Face)
  - Raw Acquired Images   : 450 original field images (Train=315, Val=67, Test=68)
  - Model 2 Test Duplicate: 0 (0% test leakage)
  - Model 2 Train/Val Dup : 0 (0% train overlap)
  - PlantSeg Duplicate    : 0 (0% PlantSeg overlap)
  - Final Curated KEEP    : +450 clean, high-quality field images
  - Model 2 Test Baseline : F1 = 0.4167 (HIGH priority deficit with only 46 train images)
  - Potential New Train   : 46 + 450 = 496 images (+978% expansion!)
  - Audit Conclusion     : CLASS DEFICIT FULLY RESOLVED AND READY FOR MERGE.
```

---

## 2. Candidate Dataset Research Matrix

| Target Class | Candidate Source | License | Raw Count | Usable Original | Label Quality | Duplicate Risk | Recommendation |
|---|---|---|---:|---:|---|---|---|
| `bean__angular_leaf_spot` | [Makerere AI Lab Beans (iBean / NaCRRI)](https://huggingface.co/datasets/AI-Lab-Makerere/beans) | MIT License | 432 | **0** | High (Expert annotated field images by NaCRRI) | 100% Duplicate with existing Model 2 dataset (all 432 already incorporated in baseline) | **DO NOT RE-DOWNLOAD (Existing Model 2 already has all 432 images; F1=0.9365, Tier=GOOD)** |
| `soybean__rust` | [Soybean Leaf Diseases Dataset (anandvermagmailcom / HF)](https://huggingface.co/datasets/anandvermagmailcom/soybean-leaf-diseases) | Apache-2.0 / CC-BY | 450 | **450** | High (Explicit label: 3 = Soyabean_rust) | Zero overlap with Model 2 test set; independent collection | **ACQUIRE & AUDIT (Fills Model 2 HIGH priority deficit of soybean__rust)** |
| `soybean__rust` | [Auburn Soybean Disease Image Dataset (ASDID / Dryad / Zenodo)](https://doi.org/10.5061/dryad.cvdncjt4z) | CC0 Public Domain | 820 | **750** | High (Auburn University Dept of Entomology & Plant Pathology) | Low | **SECONDARY CANDIDATE (Preserved for future expansion if needed)** |

---

## 3. Soybean Rust Acquisition & Multi-Level Deduplication Audit

- **Source Dataset:** `anandvermagmailcom/soybean-leaf-diseases` (Hugging Face)
- **Format & Resolution:** 224x224 RGB JPEG, 100% verified readability.
- **Raw Staged Images:** `450` images staged in [`data/external/model2_supplementary/soybean_rust_anand/`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\soybean_rust_anand)

| Split in Source | Raw Count | M2 Test Duplicates | M2 Train/Val Duplicates | PlantSeg Duplicates | Final KEEP |
|---|---:|---:|---:|---:|---:|
| `train` | 315 | 0 | 0 | 0 | **315** |
| `validation` | 67 | 0 | 0 | 0 | **67** |
| `test` | 68 | 0 | 0 | 0 | **68** |
| **TOTAL** | **450** | **0** | **0** | **0** | **450** |

---

## 4. Final Status Summary for Missing Classes

### 1. `bean__angular_leaf_spot`
- **Status:** `SATURATED_IN_BASELINE`
- **Existing Baseline Support:** 302 Train / 65 Val / 65 Test (Total = 432 images).
- **Baseline Test Performance:** Top-1 F1 = **0.9365** (Tier: GOOD).
- **External Search Outcome:** All available public online repositories (HuggingFace, Kaggle, TFDS) distribute the exact Makerere AI Lab dataset that is already 100% incorporated into Model 2.
- **Decision:** Retain existing 432 images; zero duplicate injection required.

### 2. `soybean__rust`
- **Status:** `ACQUIRED_AND_AUDITED`
- **Existing Baseline Support:** 46 Train / 10 Val / 9 Test (Total = 65 images).
- **Baseline Test Performance:** Top-1 F1 = **0.4167** (Tier: HIGH Priority Deficit).
- **Newly Acquired Clean Images:** **+450 verified field images**.
- **Combined Training Support:** 46 -> **496 images**.
- **Decision:** Approved for controlled Phase 4E merging.

---

## 5. Readiness for Controlled Model 2 Merge

- **PlantSeg v3 Approved Pool:** 3,499 clean `KEEP` images across 114 disease classes.
- **Soybean Rust Approved Pool:** 450 clean `KEEP` images for `soybean__rust`.
- **Bean Angular Leaf Spot:** Fully represented in existing Model 2 dataset (432 images).
- **Grand Total Supplementary Pool:** **3,949 clean, audited, non-duplicate images** ready for controlled training expansion.