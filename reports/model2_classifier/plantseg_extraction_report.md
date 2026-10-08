# PlantSeg v3 Targeted Disease Extraction Report

**Date:** 2026-10-07  
**Module:** Model 2 Supplementary Dataset Curation  
**PlantSeg Root Used:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3)  
**Metadata File Used:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv)  
**Output Directory:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected)  

---

## 1. Metadata Schema Discovery

- **Metadata Filename:** `Metadatav2.csv`
- **Metadata Columns Discovered (9):** `Name, Index, Plant, Disease, Resolution, Label file, Mask ratio, URL, Split`
- **Disease Identification Column:** `Disease`
- **Image Filename Column:** `Name`
- **Plant / Crop Column:** `Plant`
- **Split Representation:** `Training`, `Validation`, `Test`

---

## 2. Extraction & Verification Summary

| Target disease | Metadata matches | Images copied | Missing | Output folder |
|---|---:|---:|---:|---|
| `banana cigar end rot` | 60 | **60** | 0 | `banana_cigar_end_rot` |
| `banana cordana leaf spot` | 55 | **55** | 0 | `banana_cordana_leaf_spot` |
| `zucchini downy mildew` | 44 | **44** | 0 | `zucchini_downy_mildew` |
| `broccoli ring spot` | 16 | **16** | 0 | `broccoli_ring_spot` |
| `cauliflower alternaria leaf spot` | 54 | **54** | 0 | `cauliflower_alternaria_leaf_spot` |
| `cauliflower bacterial soft rot` | 36 | **36** | 0 | `cauliflower_bacterial_soft_rot` |
| `cabbage alternaria leaf spot` | 61 | **61** | 0 | `cabbage_alternaria_leaf_spot` |
| **TOTAL** | **326** | **326** | **0** | [`data/external/model2_supplementary/plantseg_selected/`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected) |

---

## 3. Detailed Split Breakdown per Target Class

| Output Folder | PlantSeg Label | Training | Validation | Test | Total Extracted |
|---|---|---:|---:|---:|---:|
| `banana_cigar_end_rot` | `banana cigar end rot` | 41 | 7 | 12 | **60** |
| `banana_cordana_leaf_spot` | `banana cordana leaf spot` | 38 | 6 | 11 | **55** |
| `zucchini_downy_mildew` | `zucchini downy mildew` | 30 | 5 | 9 | **44** |
| `broccoli_ring_spot` | `broccoli ring spot` | 11 | 2 | 3 | **16** |
| `cauliflower_alternaria_leaf_spot` | `cauliflower alternaria leaf spot` | 37 | 6 | 11 | **54** |
| `cauliflower_bacterial_soft_rot` | `cauliflower bacterial soft rot` | 25 | 4 | 7 | **36** |
| `cabbage_alternaria_leaf_spot` | `cabbage alternaria leaf spot` | 41 | 7 | 13 | **61** |

---

## 4. Integrity & Quality Audit

- **Total Candidate Images Copied:** **326**
- **Total Missing Images:** **0** (100% metadata records located on disk)
- **Filename Collisions:** **0** (Zero overwrites)
- **Modifications to Original PlantSeg Dataset:** None (Read-only operations enforced)
- **Image Processing / Augmentation:** Zero transformations applied (Original image files copied at native resolution/quality)
- **Model 2 Dataset Merge Status:** Staged in `plantseg_selected/` only (Not merged into `data/processed/model2_classifier/`)