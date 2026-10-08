# PlantSeg v3 Coffee Black Rot Extraction Report

**Date:** 2026-10-07  
**Module:** Model 2 Supplementary Dataset Curation  
**PlantSeg Root Used:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3)  
**Metadata File Used:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv)  
**Output Directory:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected\coffee_black_rot`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected\coffee_black_rot)  

---

## 1. Extraction Summary

| Metric | Count | Details |
|---|---:|---|
| **Target Disease Label** | - | `coffee black rot` |
| **Metadata Matches** | **7** | Verified via `Metadatav2.csv` |
| **Images Copied** | **7** | 100% original uncompressed images |
| **Missing Images** | **0** | Zero missing records |
| **Filename Collisions** | **0** | Safe unique naming |
| **Final Output File Count** | **7** | Staged in target directory |

---

## 2. Split Breakdown

| Split | Metadata Count | Copied Count | Missing |
|---|---:|---:|---:|
| **Training** | 5 | 5 | 0 |
| **Validation** | 1 | 1 | 0 |
| **Test** | 1 | 1 | 0 |
| **Total** | **7** | **7** | **0** |

---

## 3. Strict Compliance Audit

- **Metadata Ground Truth:** `Metadatav2.csv` was the sole ground truth for disease identification.
- **Strict Class Isolation:** Excluded `coffee leaf rust`, `coffee brown eye spot`, and healthy images.
- **Image Integrity:** Images copied with zero resizing, zero crop, zero color alteration, and zero recompression.
- **Original Dataset Safety:** PlantSeg v3 source directory remained read-only with zero modifications.
- **Model 2 Dataset Merge Status:** Staged in `data/external/model2_supplementary/plantseg_selected/` only (Not merged into `data/processed/model2_classifier/`).