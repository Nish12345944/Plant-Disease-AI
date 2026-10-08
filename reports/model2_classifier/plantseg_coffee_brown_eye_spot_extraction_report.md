# PlantSeg v3 Coffee Brown Eye Spot Extraction Report

**Date:** 2026-10-07  
**Module:** Model 2 Supplementary Dataset Curation  
**PlantSeg Root Used:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3)  
**Metadata File Used:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv)  
**Output Directory:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected\coffee_brown_eye_spot`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected\coffee_brown_eye_spot)  

---

## 1. Extraction Summary

| Metric | Count | Details |
|---|---:|---|
| **Target Disease Label** | - | `coffee brown eye spot` |
| **Metadata Matches** | **20** | Verified via `Metadatav2.csv` |
| **Images Copied** | **20** | 100% original uncompressed images |
| **Missing Images** | **0** | Zero missing records |
| **Filename Collisions** | **0** | Safe unique naming |
| **Final Output File Count** | **20** | Staged in target directory |

---

## 2. Split Breakdown

| Split | Metadata Count | Copied Count | Missing |
|---|---:|---:|---:|
| **Training** | 13 | 13 | 0 |
| **Validation** | 3 | 3 | 0 |
| **Test** | 4 | 4 | 0 |
| **Total** | **20** | **20** | **0** |

---

## 3. Strict Compliance Audit

- **Metadata Ground Truth:** `Metadatav2.csv` was the sole ground truth for disease identification.
- **Strict Class Isolation:** Excluded `coffee black rot`, `coffee leaf rust`, and healthy images.
- **Image Integrity:** Images copied with zero resizing, zero crop, zero color alteration, and zero recompression.
- **Original Dataset Safety:** PlantSeg v3 source directory remained read-only with zero modifications.
- **Model 2 Dataset Merge Status:** Staged in `data/external/model2_supplementary/plantseg_selected/` only (Not merged into `data/processed/model2_classifier/`).