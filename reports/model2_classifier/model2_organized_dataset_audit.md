# MODEL 2 ORGANIZED DATASET INTEGRITY AUDIT REPORT

**Date:** 2026-10-07  
**Status:** READY FOR RETRAINING (PASS)  
**Location:** `data/processed/model2_organized/`  
**Manifest:** `data/processed/model2_organized_manifest.csv`  

## 1. Dataset Overview & Split Breakdown
- **Total Images:** 19,253
- **Train Split (80%):** 15,252 (79.2%)
- **Validation Split (10%):** 1,697 (8.8%)
- **Test Split (Immutable):** 2,304 (12.0%)
- **Total Classes:** 117 (1 shared healthy + 116 disease classes)
- **Total Crop Families:** 39
- **Total Healthy Images:** 6,939
- **Unresolved / Quarantined:** 0

## 2. 15-Point Integrity Verification Summary

| # | Integrity Audit Check | Result | Details |
|:---:|:---|:---:|:---|
| 1 | Total image count exact match | **PASS** | Orig: 19253, Org: 19253 |
| 2 | Train/Val/Test split counts match exactly | **PASS** | Orig: {'train': 15252, 'test': 2304, 'val': 1697}, Org: {'train': 15252, 'test': 2304, 'val': 1697} |
| 3 | Physical existence of all organized files on disk | **PASS** | Missing: 0 |
| 4 | Zero duplicate destination image paths | **PASS** | Duplicates: 0 |
| 5 | All records have valid, non-null split, crop, disease, and class | **PASS** | Null fields: 0 |
| 6 | Test set immutability (Exactly 2,304 images with 100% matching SHA-256 hashes) | **PASS** | Test count: 2304, Hash diff: 0 |
| 7 | Zero cross-split SHA-256 hash leakage | **PASS** | Train-Val: 0, Train-Test: 0, Val-Test: 0 |
| 8 | All 117 Model 2 classes preserved with 100% taxonomy match | **PASS** | Org classes: 117 |
| 9 | Physical folder path perfectly matches split/crop/disease/ hierarchy | **PASS** | Mismatches: 0 |
| 10 | Healthy images correctly resolved to host crops with disease='healthy' | **PASS** | Healthy count: 6939 |
| 11 | Per-class image counts match original V2 dataset across all 117 classes | **PASS** |  |
| 12 | Disease classes strictly mapped to their corresponding host crops | **PASS** | Mismatches: 0 |
| 13 | Total distinct crop families represented (39 crops) | **PASS** | Crops: 39 |
| 14 | Zero unresolved or quarantined images in clean dataset | **PASS** |  |
| 15 | Original source datasets and manifests remain completely preserved | **PASS** |  |

## 3. Crop-Level Summary (Images & Classes per Crop)

| Crop | Total Images | Disease Classes | Healthy Images | Total Classes Represented |
|:---|:---:|:---:|:---:|:---:|
| `apple` | 566 | 4 | 0 | 4 |
| `banana` | 536 | 6 | 0 | 6 |
| `basil` | 63 | 1 | 0 | 1 |
| `bean` | 1,572 | 4 | 427 | 5 |
| `bell_pepper` | 938 | 4 | 708 | 5 |
| `blueberry` | 206 | 5 | 0 | 5 |
| `broccoli` | 211 | 3 | 110 | 4 |
| `cabbage` | 274 | 3 | 12 | 4 |
| `capsicum` | 804 | 0 | 804 | 1 |
| `carrot` | 148 | 3 | 0 | 3 |
| `cauliflower` | 104 | 2 | 29 | 3 |
| `celery` | 65 | 2 | 0 | 2 |
| `cherry` | 139 | 2 | 0 | 2 |
| `citrus` | 521 | 2 | 0 | 2 |
| `coffee` | 284 | 4 | 0 | 4 |
| `corn` | 616 | 4 | 0 | 4 |
| `cucumber` | 644 | 3 | 168 | 4 |
| `eggplant` | 136 | 3 | 0 | 3 |
| `garlic` | 198 | 2 | 0 | 2 |
| `ginger` | 91 | 2 | 0 | 2 |
| `grape` | 558 | 4 | 0 | 4 |
| `lettuce` | 568 | 2 | 447 | 3 |
| `maple` | 113 | 1 | 0 | 1 |
| `marigold` | 270 | 0 | 270 | 1 |
| `peach` | 444 | 5 | 0 | 5 |
| `plum` | 215 | 5 | 0 | 5 |
| `potato` | 239 | 2 | 0 | 2 |
| `raspberry` | 123 | 4 | 0 | 4 |
| `rice` | 155 | 2 | 0 | 2 |
| `rose` | 432 | 0 | 432 | 1 |
| `soybean` | 1,122 | 6 | 0 | 6 |
| `spinach` | 1,399 | 0 | 1,399 | 1 |
| `squash` | 174 | 1 | 0 | 1 |
| `strawberry` | 464 | 2 | 367 | 3 |
| `tobacco` | 178 | 4 | 0 | 4 |
| `tomato` | 2,464 | 7 | 1,585 | 8 |
| `turnip` | 181 | 0 | 181 | 1 |
| `wheat` | 1,632 | 8 | 0 | 8 |
| `zucchini` | 406 | 4 | 0 | 4 |

## 4. Retraining Readiness Conclusion

**Verdict: READY FOR RETRAINING**
The dataset is 100% structurally validated, test set immutability is mathematically guaranteed by SHA-256 hashes, zero leakage exists, and all hierarchical folder paths strictly reflect crop/disease taxonomic truth.
