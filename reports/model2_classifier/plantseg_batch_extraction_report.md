# PlantSeg v3 17-Class Batch Supplementary Extraction Report

**Date:** 2026-10-07  
**Module:** Model 2 Supplementary Dataset Curation (PlantSeg v3 Batch Pipeline)  
**PlantSeg Root:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3)  
**Metadata File:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv)  
**Output Directory:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected)  

---

## 1. Metadata Schema Discovery

- **Metadata Filename:** `Metadatav2.csv`
- **Metadata Total Rows:** 11,458
- **Metadata Columns Discovered (9):** `Name, Index, Plant, Disease, Resolution, Label file, Mask ratio, URL, Split`
- **Disease Identification Column:** `Disease`
- **Image Filename Column:** `Name`
- **Split Column:** `Split` (`Training`, `Validation`, `Test`)

---

## 2. Master Extraction & Accounting Summary

| Disease | Metadata matches | Already present | Newly copied | Missing | Final total | Status |
|---|---:|---:|---:|---:|---:|:---:|
| `coffee brown eye spot` | 20 | 20 | 0 | 0 | **20** | `VERIFIED` |
| `peach rust` | 8 | 8 | 0 | 0 | **8** | `VERIFIED` |
| `plum bacterial spot` | 16 | 16 | 0 | 0 | **16** | `VERIFIED` |
| `plum pocket disease` | 57 | 57 | 0 | 0 | **57** | `VERIFIED` |
| `plum rust` | 34 | 34 | 0 | 0 | **34** | `VERIFIED` |
| `raspberry leaf spot` | 18 | 18 | 0 | 0 | **18** | `VERIFIED` |
| `tobacco frogeye leaf spot` | 28 | 27 | 1 | 0 | **28** | `VERIFIED` |
| `ginger sheath blight` | 68 | 68 | 0 | 0 | **68** | `VERIFIED` |
| `ginger leaf spot` | 25 | 25 | 0 | 0 | **25** | `VERIFIED` |
| `banana cordana leaf spot` | 55 | 55 | 0 | 0 | **55** | `VERIFIED` |
| `banana cigar end rot` | 60 | 60 | 0 | 0 | **60** | `VERIFIED` |
| `zucchini downy mildew` | 44 | 44 | 0 | 0 | **44** | `VERIFIED` |
| `broccoli ring spot` | 16 | 16 | 0 | 0 | **16** | `VERIFIED` |
| `cauliflower alternaria leaf spot` | 54 | 54 | 0 | 0 | **54** | `VERIFIED` |
| `cauliflower bacterial soft rot` | 36 | 36 | 0 | 0 | **36** | `VERIFIED` |
| `cabbage alternaria leaf spot` | 61 | 61 | 0 | 0 | **61** | `VERIFIED` |
| `bell pepper frogeye leaf spot` | 31 | 31 | 0 | 0 | **31** | `VERIFIED` |
| **TOTAL** | **631** | **630** | **1** | **0** | **631** | `100% VERIFIED` |

---

## 3. Training, Validation & Test Split Breakdown

| Disease | Output Folder | Training | Validation | Test | Final total |
|---|---|---:|---:|---:|---:|
| `coffee brown eye spot` | `coffee_brown_eye_spot` | 13 | 3 | 4 | **20** |
| `peach rust` | `peach_rust` | 5 | 1 | 2 | **8** |
| `plum bacterial spot` | `plum_bacterial_spot` | 11 | 2 | 3 | **16** |
| `plum pocket disease` | `plum_pocket_disease` | 40 | 6 | 11 | **57** |
| `plum rust` | `plum_rust` | 23 | 4 | 7 | **34** |
| `raspberry leaf spot` | `raspberry_leaf_spot` | 13 | 2 | 3 | **18** |
| `tobacco frogeye leaf spot` | `tobacco_frogeye_leaf_spot` | 19 | 3 | 6 | **28** |
| `ginger sheath blight` | `ginger_sheath_blight` | 46 | 8 | 14 | **68** |
| `ginger leaf spot` | `ginger_leaf_spot` | 17 | 3 | 5 | **25** |
| `banana cordana leaf spot` | `banana_cordana_leaf_spot` | 38 | 6 | 11 | **55** |
| `banana cigar end rot` | `banana_cigar_end_rot` | 41 | 7 | 12 | **60** |
| `zucchini downy mildew` | `zucchini_downy_mildew` | 30 | 5 | 9 | **44** |
| `broccoli ring spot` | `broccoli_ring_spot` | 11 | 2 | 3 | **16** |
| `cauliflower alternaria leaf spot` | `cauliflower_alternaria_leaf_spot` | 37 | 6 | 11 | **54** |
| `cauliflower bacterial soft rot` | `cauliflower_bacterial_soft_rot` | 25 | 4 | 7 | **36** |
| `cabbage alternaria leaf spot` | `cabbage_alternaria_leaf_spot` | 41 | 7 | 13 | **61** |
| `bell pepper frogeye leaf spot` | `bell_pepper_frogeye_leaf_spot` | 21 | 4 | 6 | **31** |
| **TOTAL** | - | **431** | **73** | **127** | **631** |

---

## 4. SHA-256 Deduplication & Integrity Audit

| Output Folder | Total Images | Unique Hashes | Duplicate Hashes Found | Details |
|---|---:|---:|---:|:---:|
| `coffee_brown_eye_spot` | 20 | 19 | 1 | `coffee_brown_eye_spot_Bing_0006.jpg == coffee_brown_eye_spot_Google_0034.jpg` |
| `peach_rust` | 8 | 8 | 0 | `Clean (0 duplicates)` |
| `plum_bacterial_spot` | 16 | 16 | 0 | `Clean (0 duplicates)` |
| `plum_pocket_disease` | 57 | 57 | 0 | `Clean (0 duplicates)` |
| `plum_rust` | 34 | 34 | 0 | `Clean (0 duplicates)` |
| `raspberry_leaf_spot` | 18 | 18 | 0 | `Clean (0 duplicates)` |
| `tobacco_frogeye_leaf_spot` | 28 | 27 | 1 | `tobacco_frogeye_leaf_spot_Bing_0034.jpg == tobacco_frogeye_leaf_spot_Bing_0072.jpg` |
| `ginger_sheath_blight` | 68 | 68 | 0 | `Clean (0 duplicates)` |
| `ginger_leaf_spot` | 25 | 25 | 0 | `Clean (0 duplicates)` |
| `banana_cordana_leaf_spot` | 55 | 54 | 1 | `banana_cordana_leaf_spot_Bing_0005.jpg == banana_cordana_leaf_spot_Google_0014.jpg` |
| `banana_cigar_end_rot` | 60 | 57 | 3 | `banana_cigar_end_rot_Bing_0002.jpg == banana_cigar_end_rot_Google_0010.jpg; banana_cigar_end_rot_Bing_0004.jpg == banana_cigar_end_rot_Google_0018.jpg; banana_cigar_end_rot_Bing_0011.jpg == banana_cigar_end_rot_Google_0035.jpg` |
| `zucchini_downy_mildew` | 44 | 44 | 0 | `Clean (0 duplicates)` |
| `broccoli_ring_spot` | 16 | 16 | 0 | `Clean (0 duplicates)` |
| `cauliflower_alternaria_leaf_spot` | 54 | 53 | 1 | `cauliflower_alternaria_leaf_spot_170.jpg == cauliflower_alternaria_leaf_spot_9.jpg` |
| `cauliflower_bacterial_soft_rot` | 36 | 34 | 2 | `cauliflower_bacterial_soft_rot_Bing_0016.jpg == cauliflower_bacterial_soft_rot_Google_0016.jpg; cauliflower_bacterial_soft_rot_Bing_0082.jpg == cauliflower_bacterial_soft_rot_Google_0013.jpg` |
| `cabbage_alternaria_leaf_spot` | 61 | 61 | 0 | `Clean (0 duplicates)` |
| `bell_pepper_frogeye_leaf_spot` | 31 | 30 | 1 | `bell_pepper_frogeye_leaf_spot_Bing_0000.jpg == bell_pepper_frogeye_leaf_spot_Google_0000.jpg` |

---

## 5. Compliance & Isolation Verification

- **Metadata Fidelity:** `Metadatav2.csv` was strictly enforced as the sole ground truth. No filename heuristic guessing was performed.
- **Zero Augmentation / Zero Recompression:** All images were copied as original binary streams preserving original JPEG/PNG quality and dimensions.
- **Zero Overwrites:** Existing images from prior extraction runs were preserved without duplication.
- **PlantSeg Dataset Safety:** Source directory `data/external/model2_supplementary/plantsegv3/plantsegv3` remained 100% read-only.
- **Model 2 Isolation:** Output directory `data/external/model2_supplementary/plantseg_selected/` is isolated and has **not** been merged into `data/processed/model2_classifier/`.
- **No Model Retraining:** Model 2 weights and evaluation checkpoints remain completely unchanged.