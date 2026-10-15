# Model 2 V2 Supplementary Benchmark - Dataset Audit and Exclusions Report

**Generated:** 2026-10-13 15:35:42  
**Target Candidates Evaluated:** 123 raw external images from `data/external/model2_new_data/eggplant/`  
**Benchmark Directory:** `data/processed/model2_v2_supplementary_benchmark/`  

## 1. Candidate Source Inventory & Search Results

Across all subdirectories in `data/external/`, image candidates for the 10 target classes were audited:

| Target Class | Candidates Found in `data/external/` | Eligible Images | Excluded Images | Audit Status / Shortfall Reason |
|---|---|---|---|---|
| `carrot__cavity_spot` | 0 | **0** | 0 | Shortfall: No additional external carrot cavity spot images present in data/external/. Historical V4 split exhausted. |
| `coffee__berry_blotch` | 0 | **0** | 0 | Shortfall: No additional external coffee berry blotch images present in data/external/. Historical V4 split exhausted. |
| `maple__tar_spot` | 0 | **0** | 0 | Shortfall: No additional external maple tar spot images present in data/external/. Historical V4 split exhausted. |
| `eggplant__phomopsis_fruit_rot` | 123 | **24** | 99 | Verified & Screened |
| `zucchini__yellow_mosaic_virus` | 0 | **0** | 0 | Shortfall: data/external/end_to_end_test/zucchini contains 18 images, but all are confirmed powdery mildew, not yellow mosaic virus. |
| `plum__brown_rot` | 0 | **0** | 0 | Shortfall: data/external/end_to_end_test/ contains 4 peach brown rot images, but 0 plum brown rot images. |
| `grape__grapevine_leafroll_disease` | 0 | **0** | 0 | Shortfall: No additional external grape leafroll disease images present in data/external/. |
| `bean__halo_blight` | 0 | **0** | 0 | Shortfall: data/external/end_to_end_test/bean contains 2 bean rust images; 0 halo blight images present. |
| `tobacco__mosaic_virus` | 0 | **0** | 0 | Shortfall: data/external/model2_new_data/ contains lettuce mosaic virus (113 images); 0 tobacco mosaic virus images present. |
| `banana__panama_disease` | 0 | **0** | 0 | Shortfall: data/external/ contains banana cigar end rot (204) and cordana/bunchy top/black leaf streak; 0 panama disease images present. |

## 2. Exclusion Breakdown for `eggplant__phomopsis_fruit_rot` ($n=123$)

Of the 123 candidate images in `data/external/model2_new_data/eggplant/`:
- **52 images**: Excluded as **Exact Training Duplicates** (matching `model2_retraining_v2` train split).
- **9 images**: Excluded as **Exact Validation Duplicates** (matching `model2_retraining_v2` val split).
- **11 images**: Excluded due to **Cross-Folder Label Collisions** (identical image present in `eggplant phytophthora spot`).
- **25 images**: Excluded as **Intra-Candidate Duplicates** (duplicate copies across candidate folders).
- **2 images**: Excluded as **Perceptual Near-Duplicates of Test Set** (pHash distance = 0 to `b0ad010c3b_eggplant_phomopsis_fruit_rot_Google_0031.jpg`).
- **24 images**: **VERIFIED ELIGIBLE** (Zero overlap with train, val, or test splits; unambiguous phomopsis fruit rot labels).

## 3. Data Shortfall Declaration (9 Classes)

Per requirement 7, data was neither fabricated nor artificially relabeled. The following 9 classes have **0 verified additional images in `data/external/`**:
1. `carrot__cavity_spot`: 0 additional external images.
2. `coffee__berry_blotch`: 0 additional external images.
3. `maple__tar_spot`: 0 additional external images.
4. `zucchini__yellow_mosaic_virus`: 0 additional external images (18 images in `end_to_end_test/zucchini` are powdery mildew).
5. `plum__brown_rot`: 0 additional external images (peach brown rot cannot be relabeled as plum).
6. `grape__grapevine_leafroll_disease`: 0 additional external images.
7. `bean__halo_blight`: 0 additional external images (`end_to_end_test` contains only bean rust).
8. `tobacco__mosaic_virus`: 0 additional external images (`model2_new_data` contains only lettuce mosaic virus).
9. `banana__panama_disease`: 0 additional external images (`end_to_end_test` contains cordana, bunchy top, and black leaf streak).