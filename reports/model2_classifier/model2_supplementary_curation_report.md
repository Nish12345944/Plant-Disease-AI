# Model 2 Supplementary Dataset Curation and Deduplication Audit Report

**Date:** 2026-10-07  
**Module:** Model 2 Classifier Curation Pipeline (Phase 4D)  
**Supplementary Source:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected)  
**Curated Manifest:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_curated_manifest.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_curated_manifest.csv)  
**Protected Model 2 Test Set:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\processed\model2_classifier\test`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\processed\model2_classifier\test)  

---

## 1. Executive Summary & Audit Dashboard

```
TOTAL PLANTSEG INSPECTED          : 11,458 images
VALID & READABLE IMAGES           : 11,458 images
INVALID / CORRUPT IMAGES          : 0
UNMAPPED TAXONOMY IMAGES          : 0
TOTAL EXACT DUPLICATES            : 7,899
  - EXCLUDE_TEST_DUPLICATE (Test) : 1179 (Protected Model 2 Test Set)
  - EXACT_DUPLICATE_EXISTING (Tr/V): 6600 (Existing Model 2 Train/Val)
  - EXACT_DUPLICATE_PLANTSEG      : 120 (Internal PlantSeg Redundancy)
NEAR_DUPLICATE_REVIEW (pHash/dHash): 60 images flagged for manual review
FINAL CURATED KEEP POOL           : 3,499 high-quality field images
CLASSES COVERED                   : 114 / 116 disease classes (98.3%)
CLASSES MISSING IN PLANTSEG       : 2 classes (bean__angular_leaf_spot, soybean__rust)
```

---

## 2. Primary Curation Status Distribution

| Curation Status | Meaning & Policy | Image Count | Percentage | Action |
|---|---|---:|---:|---|
| `KEEP` | Clean, genuine field image matching Model 2 taxonomy with no protected overlap | **3,499** | **30.54%** | Staged for controlled Model 2 augmentation |
| `EXCLUDE_TEST_DUPLICATE` | Exact SHA-256 match to immutable Model 2 test image | **1179** | **10.29%** | **Strictly excluded** from training/validation |
| `EXACT_DUPLICATE_EXISTING` | Exact SHA-256 match to existing Model 2 train/val image | **6600** | **57.60%** | Excluded to prevent train-set memorization |
| `EXACT_DUPLICATE_PLANTSEG` | Exact SHA-256 duplicate within PlantSeg supplementary batch | **120** | **1.05%** | Excluded (canonical copy preserved) |
| `NEAR_DUPLICATE_REVIEW` | Perceptual hash near-duplicate (pHash/dHash identical) | **60** | **0.52%** | Isolated for manual visual review |
| `INVALID` | Corrupted, unreadable, or unsupported image format | **0** | **0.00%** | Excluded |
| `UNMAPPED` | Cannot be mapped to 117-class Model 2 taxonomy | **0** | **0.00%** | Excluded |
| **TOTAL** | **All Analyzed PlantSeg Images** | **11,458** | **100.00%** | — |

---

## 3. Class-by-Class Curation and Deduplication Table (All 116 Disease Classes)

| Model 2 Class | PlantSeg Raw | Exact Dup (PlantSeg) | Dup (M2 Train/Val) | Dup (M2 Test) | Near-Dup Review | Invalid | Unmapped | Final KEEP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `apple__black_rot` | 83 | 0 | 53 | 10 | 0 | 0 | 0 | **20** |
| `apple__mosaic_virus` | 89 | 0 | 62 | 11 | 0 | 0 | 0 | **16** |
| `apple__rust` | 139 | 0 | 85 | 14 | 0 | 0 | 0 | **40** |
| `apple__scab` | 258 | 0 | 143 | 25 | 0 | 0 | 0 | **90** |
| `banana__anthracnose` | 71 | 0 | 42 | 8 | 0 | 0 | 0 | **21** |
| `banana__black_leaf_streak` | 167 | 3 | 97 | 17 | 1 | 0 | 0 | **49** |
| `banana__bunchy_top` | 157 | 9 | 66 | 12 | 3 | 0 | 0 | **67** |
| `banana__cigar_end_rot` | 60 | 1 | 29 | 4 | 1 | 0 | 0 | **25** |
| `banana__cordana_leaf_spot` | 55 | 2 | 26 | 4 | 0 | 0 | 0 | **23** |
| `banana__panama_disease` | 63 | 0 | 41 | 8 | 0 | 0 | 0 | **14** |
| `basil__downy_mildew` | 63 | 0 | 35 | 6 | 0 | 0 | 0 | **22** |
| `bean__angular_leaf_spot` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| `bean__halo_blight` | 56 | 0 | 29 | 6 | 0 | 0 | 0 | **21** |
| `bean__mosaic_virus` | 58 | 0 | 28 | 6 | 0 | 0 | 0 | **24** |
| `bean__rust` | 233 | 0 | 120 | 21 | 2 | 0 | 0 | **90** |
| `bell_pepper__bacterial_spot` | 76 | 0 | 46 | 7 | 2 | 0 | 0 | **21** |
| `bell_pepper__blossom_end_rot` | 112 | 0 | 70 | 11 | 1 | 0 | 0 | **30** |
| `bell_pepper__frogeye_leaf_spot` | 31 | 1 | 20 | 4 | 1 | 0 | 0 | **5** |
| `bell_pepper__powdery_mildew` | 28 | 1 | 16 | 2 | 1 | 0 | 0 | **8** |
| `blueberry__anthracnose` | 42 | 0 | 23 | 5 | 0 | 0 | 0 | **14** |
| `blueberry__botrytis_blight` | 36 | 0 | 16 | 3 | 1 | 0 | 0 | **16** |
| `blueberry__mummy_berry` | 47 | 0 | 25 | 4 | 0 | 0 | 0 | **18** |
| `blueberry__rust` | 43 | 0 | 28 | 5 | 0 | 0 | 0 | **10** |
| `blueberry__scorch` | 43 | 0 | 27 | 6 | 0 | 0 | 0 | **10** |
| `broccoli__alternaria_leaf_spot` | 65 | 0 | 47 | 9 | 0 | 0 | 0 | **9** |
| `broccoli__downy_mildew` | 29 | 0 | 19 | 4 | 0 | 0 | 0 | **6** |
| `broccoli__ring_spot` | 16 | 1 | 10 | 2 | 0 | 0 | 0 | **3** |
| `cabbage__alternaria_leaf_spot` | 61 | 0 | 32 | 7 | 0 | 0 | 0 | **22** |
| `cabbage__black_rot` | 131 | 3 | 78 | 15 | 3 | 0 | 0 | **32** |
| `cabbage__downy_mildew` | 84 | 0 | 41 | 8 | 0 | 0 | 0 | **35** |
| `carrot__alternaria_leaf_blight` | 60 | 0 | 38 | 7 | 1 | 0 | 0 | **14** |
| `carrot__cavity_spot` | 72 | 0 | 35 | 7 | 0 | 0 | 0 | **30** |
| `carrot__cercospora_leaf_blight` | 19 | 0 | 15 | 3 | 0 | 0 | 0 | **1** |
| `cauliflower__alternaria_leaf_spot` | 54 | 4 | 29 | 5 | 0 | 0 | 0 | **16** |
| `cauliflower__bacterial_soft_rot` | 36 | 2 | 17 | 2 | 1 | 0 | 0 | **14** |
| `celery__anthracnose` | 29 | 0 | 10 | 1 | 0 | 0 | 0 | **18** |
| `celery__early_blight` | 36 | 0 | 24 | 5 | 0 | 0 | 0 | **7** |
| `cherry__leaf_spot` | 106 | 0 | 56 | 10 | 0 | 0 | 0 | **40** |
| `cherry__powdery_mildew` | 33 | 0 | 22 | 3 | 0 | 0 | 0 | **8** |
| `citrus__canker` | 390 | 0 | 274 | 49 | 0 | 0 | 0 | **67** |
| `citrus__greening_disease` | 133 | 0 | 79 | 14 | 0 | 0 | 0 | **40** |
| `coffee__berry_blotch` | 118 | 2 | 59 | 10 | 7 | 0 | 0 | **40** |
| `coffee__black_rot` | 7 | 1 | 3 | 0 | 0 | 0 | 0 | **3** |
| `coffee__brown_eye_spot` | 20 | 0 | 15 | 2 | 0 | 0 | 0 | **3** |
| `coffee__leaf_rust` | 159 | 0 | 91 | 16 | 0 | 0 | 0 | **52** |
| `corn__gray_leaf_spot` | 107 | 0 | 64 | 12 | 0 | 0 | 0 | **31** |
| `corn__northern_leaf_blight` | 130 | 0 | 78 | 14 | 0 | 0 | 0 | **38** |
| `corn__rust` | 177 | 0 | 102 | 18 | 0 | 0 | 0 | **57** |
| `corn__smut` | 202 | 0 | 112 | 19 | 0 | 0 | 0 | **71** |
| `cucumber__angular_leaf_spot` | 182 | 0 | 126 | 22 | 0 | 0 | 0 | **34** |
| `cucumber__bacterial_wilt` | 108 | 0 | 69 | 13 | 0 | 0 | 0 | **26** |
| `cucumber__powdery_mildew` | 188 | 0 | 130 | 23 | 0 | 0 | 0 | **35** |
| `eggplant__cercospora_leaf_spot` | 60 | 0 | 31 | 7 | 0 | 0 | 0 | **22** |
| `eggplant__phomopsis_fruit_rot` | 46 | 0 | 27 | 5 | 1 | 0 | 0 | **13** |
| `eggplant__phytophthora_blight` | 33 | 0 | 18 | 4 | 0 | 0 | 0 | **11** |
| `garlic__leaf_blight` | 92 | 0 | 67 | 12 | 0 | 0 | 0 | **13** |
| `garlic__rust` | 106 | 0 | 68 | 12 | 0 | 0 | 0 | **26** |
| `ginger__leaf_spot` | 25 | 0 | 18 | 4 | 0 | 0 | 0 | **3** |
| `ginger__sheath_blight` | 68 | 0 | 51 | 8 | 0 | 0 | 0 | **9** |
| `grape__black_rot` | 122 | 0 | 75 | 13 | 0 | 0 | 0 | **34** |
| `grape__downy_mildew` | 280 | 0 | 179 | 32 | 0 | 0 | 0 | **69** |
| `grape__grapevine_leafroll_disease` | 71 | 0 | 27 | 5 | 0 | 0 | 0 | **39** |
| `grape__leaf_spot` | 91 | 0 | 57 | 12 | 0 | 0 | 0 | **22** |
| `lettuce__downy_mildew` | 84 | 1 | 46 | 8 | 0 | 0 | 0 | **29** |
| `lettuce__mosaic_virus` | 39 | 0 | 18 | 4 | 0 | 0 | 0 | **17** |
| `maple__tar_spot` | 114 | 0 | 50 | 8 | 0 | 0 | 0 | **56** |
| `peach__anthracnose` | 13 | 0 | 9 | 1 | 0 | 0 | 0 | **3** |
| `peach__brown_rot` | 173 | 0 | 81 | 15 | 4 | 0 | 0 | **73** |
| `peach__leaf_curl` | 182 | 0 | 103 | 18 | 0 | 0 | 0 | **61** |
| `peach__rust` | 8 | 0 | 4 | 1 | 0 | 0 | 0 | **3** |
| `peach__scab` | 78 | 1 | 47 | 8 | 0 | 0 | 0 | **22** |
| `plum__bacterial_spot` | 16 | 0 | 9 | 1 | 0 | 0 | 0 | **6** |
| `plum__brown_rot` | 81 | 1 | 36 | 6 | 0 | 0 | 0 | **38** |
| `plum__pocket_disease` | 57 | 0 | 24 | 4 | 0 | 0 | 0 | **29** |
| `plum__pox_virus` | 33 | 0 | 19 | 4 | 0 | 0 | 0 | **10** |
| `plum__rust` | 34 | 0 | 15 | 2 | 0 | 0 | 0 | **17** |
| `potato__early_blight` | 126 | 0 | 58 | 10 | 0 | 0 | 0 | **58** |
| `potato__late_blight` | 117 | 0 | 66 | 12 | 0 | 0 | 0 | **39** |
| `raspberry__fire_blight` | 34 | 1 | 21 | 4 | 0 | 0 | 0 | **8** |
| `raspberry__gray_mold` | 40 | 1 | 16 | 2 | 0 | 0 | 0 | **21** |
| `raspberry__leaf_spot` | 18 | 0 | 10 | 1 | 0 | 0 | 0 | **7** |
| `raspberry__yellow_rust` | 37 | 0 | 19 | 4 | 0 | 0 | 0 | **14** |
| `rice__blast` | 83 | 0 | 43 | 7 | 0 | 0 | 0 | **33** |
| `rice__sheath_blight` | 76 | 0 | 46 | 10 | 0 | 0 | 0 | **20** |
| `soybean__bacterial_blight` | 91 | 1 | 53 | 9 | 1 | 0 | 0 | **27** |
| `soybean__brown_spot` | 71 | 1 | 45 | 10 | 1 | 0 | 0 | **14** |
| `soybean__downy_mildew` | 153 | 8 | 65 | 11 | 7 | 0 | 0 | **62** |
| `soybean__frog_eye_leaf_spot` | 238 | 11 | 131 | 23 | 2 | 0 | 0 | **71** |
| `soybean__mosaic` | 117 | 1 | 76 | 13 | 0 | 0 | 0 | **27** |
| `soybean__rust` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| `squash__powdery_mildew` | 182 | 1 | 124 | 20 | 0 | 0 | 0 | **37** |
| `strawberry__anthracnose` | 58 | 0 | 25 | 5 | 0 | 0 | 0 | **28** |
| `strawberry__leaf_scorch` | 39 | 0 | 16 | 3 | 0 | 0 | 0 | **20** |
| `tobacco__blue_mold` | 60 | 0 | 30 | 6 | 3 | 0 | 0 | **21** |
| `tobacco__brown_spot` | 66 | 0 | 43 | 7 | 0 | 0 | 0 | **16** |
| `tobacco__frogeye_leaf_spot` | 28 | 4 | 15 | 4 | 0 | 0 | 0 | **5** |
| `tobacco__mosaic_virus` | 41 | 0 | 24 | 5 | 0 | 0 | 0 | **12** |
| `tomato__bacterial_leaf_spot` | 109 | 0 | 76 | 14 | 0 | 0 | 0 | **19** |
| `tomato__early_blight` | 187 | 2 | 130 | 23 | 0 | 0 | 0 | **32** |
| `tomato__late_blight` | 163 | 0 | 100 | 17 | 0 | 0 | 0 | **46** |
| `tomato__leaf_mold` | 156 | 0 | 86 | 16 | 0 | 0 | 0 | **54** |
| `tomato__mosaic_virus` | 63 | 0 | 36 | 7 | 0 | 0 | 0 | **20** |
| `tomato__septoria_leaf_spot` | 130 | 0 | 84 | 15 | 0 | 0 | 0 | **31** |
| `tomato__yellow_leaf_curl_virus` | 93 | 0 | 52 | 11 | 0 | 0 | 0 | **30** |
| `wheat__bacterial_leaf_streak_(black_chaff)` | 117 | 1 | 70 | 13 | 0 | 0 | 0 | **33** |
| `wheat__head_scab` | 319 | 9 | 198 | 32 | 4 | 0 | 0 | **76** |
| `wheat__leaf_rust` | 132 | 2 | 64 | 11 | 0 | 0 | 0 | **55** |
| `wheat__loose_smut` | 215 | 10 | 120 | 21 | 1 | 0 | 0 | **63** |
| `wheat__powdery_mildew` | 271 | 6 | 151 | 27 | 0 | 0 | 0 | **87** |
| `wheat__septoria_blotch` | 232 | 11 | 120 | 23 | 0 | 0 | 0 | **78** |
| `wheat__stem_rust` | 148 | 2 | 76 | 13 | 4 | 0 | 0 | **53** |
| `wheat__stripe_rust` | 358 | 14 | 194 | 34 | 3 | 0 | 0 | **113** |
| `zucchini__bacterial_wilt` | 70 | 0 | 48 | 9 | 1 | 0 | 0 | **12** |
| `zucchini__downy_mildew` | 44 | 0 | 27 | 6 | 0 | 0 | 0 | **11** |
| `zucchini__powdery_mildew` | 213 | 1 | 114 | 19 | 3 | 0 | 0 | **76** |
| `zucchini__yellow_mosaic_virus` | 95 | 0 | 47 | 9 | 0 | 0 | 0 | **39** |
| **TOTAL (116 Disease Classes)** | **11,458** | **120** | **6600** | **1179** | **60** | **0** | **0** | **3,499** |

---

## 4. Weak-Class Cross-Analysis & Impact Assessment

Cross-referenced against Model 2 Error Analysis ([`reports/model2_classifier/model2_error_analysis.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2_classifier/model2_error_analysis.csv)):

| Priority Tier | Model 2 Class | Test F1 | M2 Train Support | PlantSeg KEEP | Combined Potential Train | Target Needed | Supplementary Sufficiency |
|---|---|---:|---:|---:|---:|---:|---|
| `CRITICAL` | `plum__rust` | 0.0000 | 12 | +17 | 29 | 38 | PARTIAL (+17 of 38 needed) |
| `CRITICAL` | `cauliflower__alternaria_leaf_spot` | 0.0000 | 19 | +16 | 35 | 38 | PARTIAL (+16 of 38 needed) |
| `CRITICAL` | `cauliflower__bacterial_soft_rot` | 0.0000 | 13 | +14 | 27 | 37 | PARTIAL (+14 of 37 needed) |
| `CRITICAL` | `cherry__powdery_mildew` | 0.0000 | 18 | +8 | 26 | 36 | PARTIAL (+8 of 36 needed) |
| `CRITICAL` | `raspberry__leaf_spot` | 0.0000 | 8 | +7 | 15 | 42 | PARTIAL (+7 of 42 needed) |
| `CRITICAL` | `plum__bacterial_spot` | 0.0000 | 7 | +6 | 13 | 43 | PARTIAL (+6 of 43 needed) |
| `CRITICAL` | `bell_pepper__frogeye_leaf_spot` | 0.0000 | 16 | +5 | 21 | 34 | PARTIAL (+5 of 34 needed) |
| `CRITICAL` | `broccoli__ring_spot` | 0.0000 | 5 | +3 | 8 | 45 | PARTIAL (+3 of 45 needed) |
| `CRITICAL` | `coffee__black_rot` | 0.0000 | 2 | +3 | 5 | 48 | PARTIAL (+3 of 48 needed) |
| `CRITICAL` | `coffee__brown_eye_spot` | 0.0000 | 8 | +3 | 11 | 42 | PARTIAL (+3 of 42 needed) |
| `CRITICAL` | `peach__rust` | 0.0000 | 3 | +3 | 6 | 47 | PARTIAL (+3 of 47 needed) |
| `CRITICAL` | `cabbage__alternaria_leaf_spot` | 0.1538 | 25 | +22 | 47 | 50 | PARTIAL (+22 of 50 needed) |
| `CRITICAL` | `plum__pocket_disease` | 0.2222 | 20 | +29 | 49 | 40 | PARTIAL (+29 of 40 needed) |
| `CRITICAL` | `tobacco__frogeye_leaf_spot` | 0.2222 | 10 | +5 | 15 | 40 | PARTIAL (+5 of 40 needed) |
| `CRITICAL` | `ginger__sheath_blight` | 0.2353 | 40 | +9 | 49 | 80 | PARTIAL (+9 of 80 needed) |
| `CRITICAL` | `bean__mosaic_virus` | 0.2667 | 23 | +24 | 47 | 46 | PARTIAL (+24 of 46 needed) |
| `CRITICAL` | `banana__cordana_leaf_spot` | 0.2857 | 20 | +23 | 43 | 40 | PARTIAL (+23 of 40 needed) |
| `CRITICAL` | `zucchini__downy_mildew` | 0.3333 | 22 | +11 | 33 | 44 | PARTIAL (+11 of 44 needed) |
| `CRITICAL` | `tomato__septoria_leaf_spot` | 0.3448 | 64 | +31 | 95 | 128 | PARTIAL (+31 of 128 needed) |
| `CRITICAL` | `squash__powdery_mildew` | 0.3784 | 96 | +37 | 133 | 192 | PARTIAL (+37 of 192 needed) |
| `HIGH` | `zucchini__powdery_mildew` | 0.4000 | 87 | +76 | 163 | 87 | PARTIAL (+76 of 87 needed) |
| `HIGH` | `bean__halo_blight` | 0.4000 | 24 | +21 | 45 | 36 | PARTIAL (+21 of 36 needed) |
| `HIGH` | `tomato__mosaic_virus` | 0.4000 | 30 | +20 | 50 | 30 | PARTIAL (+20 of 30 needed) |
| `HIGH` | `soybean__brown_spot` | 0.4000 | 33 | +14 | 47 | 33 | PARTIAL (+14 of 33 needed) |
| `HIGH` | `eggplant__phytophthora_blight` | 0.4000 | 15 | +11 | 26 | 45 | PARTIAL (+11 of 45 needed) |
| `HIGH` | `plum__pox_virus` | 0.4000 | 15 | +10 | 25 | 45 | PARTIAL (+10 of 45 needed) |
| `HIGH` | `carrot__cercospora_leaf_blight` | 0.4000 | 11 | +1 | 12 | 49 | PARTIAL (+1 of 49 needed) |
| `HIGH` | `soybean__rust` | 0.4167 | 46 | +0 | 46 | 46 | **DEFICIT (0 images in PlantSeg)** |
| `HIGH` | `eggplant__cercospora_leaf_spot` | 0.4444 | 25 | +22 | 47 | 35 | PARTIAL (+22 of 35 needed) |
| `HIGH` | `celery__early_blight` | 0.4444 | 20 | +7 | 27 | 40 | PARTIAL (+7 of 40 needed) |
| `HIGH` | `rice__sheath_blight` | 0.4545 | 36 | +20 | 56 | 36 | PARTIAL (+20 of 36 needed) |
| `HIGH` | `wheat__leaf_rust` | 0.4615 | 51 | +55 | 106 | 51 | SUFFICIENT (+55 imgs) |
| `HIGH` | `corn__gray_leaf_spot` | 0.4762 | 53 | +31 | 84 | 53 | PARTIAL (+31 of 53 needed) |
| `HIGH` | `soybean__bacterial_blight` | 0.4762 | 42 | +27 | 69 | 42 | PARTIAL (+27 of 42 needed) |
| `HIGH` | `cabbage__downy_mildew` | 0.5000 | 34 | +35 | 69 | 34 | SUFFICIENT (+35 imgs) |
| `HIGH` | `rice__blast` | 0.5000 | 35 | +33 | 68 | 35 | PARTIAL (+33 of 35 needed) |
| `HIGH` | `apple__black_rot` | 0.5000 | 44 | +20 | 64 | 44 | PARTIAL (+20 of 44 needed) |
| `HIGH` | `lettuce__mosaic_virus` | 0.5000 | 15 | +17 | 32 | 45 | PARTIAL (+17 of 45 needed) |
| `HIGH` | `garlic__leaf_blight` | 0.5000 | 55 | +13 | 68 | 55 | PARTIAL (+13 of 55 needed) |
| `HIGH` | `raspberry__fire_blight` | 0.5000 | 16 | +8 | 24 | 44 | PARTIAL (+8 of 44 needed) |
| `HIGH` | `ginger__leaf_spot` | 0.5000 | 15 | +3 | 18 | 45 | PARTIAL (+3 of 45 needed) |
| `HIGH` | `tomato__bacterial_leaf_spot` | 0.5333 | 62 | +19 | 81 | 62 | PARTIAL (+19 of 62 needed) |
| `HIGH` | `wheat__bacterial_leaf_streak_(black_chaff)` | 0.5385 | 57 | +33 | 90 | 57 | PARTIAL (+33 of 57 needed) |
| `HIGH` | `soybean__mosaic` | 0.5385 | 62 | +27 | 89 | 62 | PARTIAL (+27 of 62 needed) |
| `HIGH` | `blueberry__rust` | 0.5455 | 23 | +10 | 33 | 37 | PARTIAL (+10 of 37 needed) |
| `HIGH` | `wheat__septoria_blotch` | 0.5500 | 86 | +78 | 164 | 86 | PARTIAL (+78 of 86 needed) |
| `HIGH` | `zucchini__bacterial_wilt` | 0.5714 | 39 | +12 | 51 | 39 | PARTIAL (+12 of 39 needed) |
| `HIGH` | `broccoli__downy_mildew` | 0.5714 | 16 | +6 | 22 | 44 | PARTIAL (+6 of 44 needed) |
| `HIGH` | `grape__leaf_spot` | 0.5882 | 46 | +22 | 68 | 46 | PARTIAL (+22 of 46 needed) |
| `MEDIUM` | `bell_pepper__bacterial_spot` | 0.6000 | 33 | +21 | 54 | 47 | PARTIAL (+21 of 47 needed) |
| `MEDIUM` | `eggplant__phomopsis_fruit_rot` | 0.6000 | 22 | +13 | 35 | 58 | PARTIAL (+13 of 58 needed) |
| `MEDIUM` | `tobacco__mosaic_virus` | 0.6000 | 20 | +12 | 32 | 60 | PARTIAL (+12 of 60 needed) |
| `MEDIUM` | `blueberry__scorch` | 0.6000 | 22 | +10 | 32 | 58 | PARTIAL (+10 of 58 needed) |
| `MEDIUM` | `broccoli__alternaria_leaf_spot` | 0.6154 | 37 | +9 | 46 | 43 | PARTIAL (+9 of 43 needed) |
| `MEDIUM` | `apple__scab` | 0.6667 | 116 | +90 | 206 | 58 | SUFFICIENT (+90 imgs) |
| `MEDIUM` | `wheat__powdery_mildew` | 0.6667 | 122 | +87 | 209 | 61 | SUFFICIENT (+87 imgs) |
| `MEDIUM` | `cherry__leaf_spot` | 0.6667 | 46 | +40 | 86 | 34 | SUFFICIENT (+40 imgs) |
| `MEDIUM` | `garlic__rust` | 0.6667 | 56 | +26 | 82 | 28 | PARTIAL (+26 of 28 needed) |
| `MEDIUM` | `banana__cigar_end_rot` | 0.6667 | 22 | +25 | 47 | 58 | PARTIAL (+25 of 58 needed) |
| `MEDIUM` | `basil__downy_mildew` | 0.6667 | 29 | +22 | 51 | 51 | PARTIAL (+22 of 51 needed) |
| `MEDIUM` | `tobacco__blue_mold` | 0.6667 | 24 | +21 | 45 | 56 | PARTIAL (+21 of 56 needed) |
| `MEDIUM` | `celery__anthracnose` | 0.6667 | 8 | +18 | 26 | 72 | PARTIAL (+18 of 72 needed) |
| `MEDIUM` | `blueberry__anthracnose` | 0.6667 | 18 | +14 | 32 | 62 | PARTIAL (+14 of 62 needed) |
| `MEDIUM` | `peach__anthracnose` | 0.6667 | 7 | +3 | 10 | 73 | PARTIAL (+3 of 73 needed) |
| `MEDIUM` | `cucumber__powdery_mildew` | 0.6939 | 106 | +35 | 141 | 53 | PARTIAL (+35 of 53 needed) |
| `MEDIUM` | `tomato__yellow_leaf_curl_virus` | 0.7059 | 41 | +30 | 71 | 39 | PARTIAL (+30 of 39 needed) |
| `MEDIUM` | `apple__rust` | 0.7200 | 69 | +40 | 109 | 34 | SUFFICIENT (+40 imgs) |
| `MEDIUM` | `corn__rust` | 0.7273 | 84 | +57 | 141 | 42 | SUFFICIENT (+57 imgs) |
| `MEDIUM` | `apple__mosaic_virus` | 0.7273 | 51 | +16 | 67 | 29 | PARTIAL (+16 of 29 needed) |
| `MEDIUM` | `potato__early_blight` | 0.7368 | 46 | +58 | 104 | 34 | SUFFICIENT (+58 imgs) |

---

## 5. Critical Split Concentration & Bias Warnings

> [!WARNING]
> **Do NOT preserve original PlantSeg train/val/test splits.**
> In PlantSeg v3, certain classes are 100% placed into a single partition:
> - `potato__early_blight`: 126 / 126 images (100%) were originally marked 'Training'
> - `potato__late_blight`: 117 / 117 images (100%) were originally marked 'Training'
> - When merging into Model 2, all curated `KEEP` images must be merged into the training candidate pool or partitioned via controlled stratified K-fold cross-validation, keeping the official Model 2 test set 100% intact.

---

## 6. Provenance & Licensing Metadata

- **Dataset Provenance:** All 11,458 images originate from the public PlantSeg v3 research archive, referenced via `Metadatav2.csv`.
- **URLs & Annotations:** Preserved in [`model2_supplementary_provenance.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2_classifier/model2_supplementary_provenance.csv).
- **Original Binary Integrity:** 100% unaltered (zero resizing, cropping, or re-encoding).

---

## 7. Final Recommendation & Next Steps

### Recommended Action: `B) MERGE AFTER MANUAL REVIEW`

1. **Automated Status Applied:**
   - **3,499 `KEEP` images** in [`plantseg_curated_manifest.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model2_supplementary/plantseg_curated_manifest.csv) are clean and ready for controlled Model 2 augmentation.
   - **7,899 Exact duplicates** are automatically quarantined.
   - **60 Near-duplicates** in [`model2_supplementary_near_duplicates.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2_classifier/model2_supplementary_near_duplicates.csv) are flagged for rapid spot inspection.
2. **Next Workflow Steps:**
   - **Step 1:** Review flagged near-duplicate pairs (if any borderline cases exist).
   - **Step 2:** Plan stratified Model 2 training dataset expansion using only the approved `KEEP` manifest.
   - **Step 3:** Perform controlled Model 2 retraining with strict immutable test set evaluation.