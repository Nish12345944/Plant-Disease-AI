# PlantSeg v3 Bell Pepper Frogeye Leaf Spot Extraction Report

**Date:** 2026-10-07  
**Module:** Model 2 Supplementary Dataset Curation  
**PlantSeg Root Used:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3)  
**Metadata File Used:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv)  
**Output Directory:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected\bell_pepper_frogeye_leaf_spot`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected\bell_pepper_frogeye_leaf_spot)  

---

## 1. Extraction Summary

| Metric | Count | Details |
|---|---:|---|
| **Target Disease Label** | - | `bell pepper frogeye leaf spot` |
| **Metadata Matches** | **31** | Verified via `Metadatav2.csv` |
| **Images Copied** | **31** | 100% original uncompressed images |
| **Missing Images** | **0** | Zero missing records |
| **Filename Collisions** | **0** | Safe unique naming |
| **Final Output File Count** | **31** | Staged in target directory |

---

## 2. Split Breakdown

| Split | Metadata Count | Copied Count | Missing |
|---|---:|---:|---:|
| **Training** | 21 | 21 | 0 |
| **Validation** | 4 | 4 | 0 |
| **Test** | 6 | 6 | 0 |
| **Total** | **31** | **31** | **0** |

---

## 3. Strict Compliance Audit

- **Metadata Verification:** `Metadatav2.csv` was the sole ground truth for disease identity.
- **Strict Class Isolation:** Excluded `bell pepper bacterial spot`, `bell pepper blossom end rot`, `bell pepper powdery mildew`, and healthy images.
- **Image Integrity:** Images copied with zero resizing, zero crop, zero color alteration, and zero recompression.
- **Original Dataset Safety:** PlantSeg v3 source directory remained read-only with zero modifications.
- **Model 2 Dataset Merge Status:** Staged in `data/external/model2_supplementary/plantseg_selected/` only (Not merged into `data/processed/model2_classifier/`).