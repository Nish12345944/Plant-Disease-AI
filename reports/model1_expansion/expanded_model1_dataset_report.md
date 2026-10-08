# EXPANDED MODEL 1 CURATED DATASET REPORT

**Date:** 2026-10-08 17:40:22  
**Target Taxonomy:** 46 Canonical Model 1 Crop Classes  
**Dataset Location:** `data/processed/model1_expanded/`  
**Manifest Path:** `data/processed/model1_expanded_manifest.csv`  
**Class Mapping Path:** `data/processed/model1_expanded_class_mapping.json`  
**Summary Path:** `data/processed/model1_expanded_summary.json`  

---

## 1. Executive Summary

This report establishes the audited dataset baseline for the expanded **46-class Model 1 crop classifier**. The dataset combines verified local greenhouse/floriculture images from the baseline Model 1 dataset with verified field crop images from the locked Model 2 V4 archive. Oversized classes have been intelligently capped at 500–600 training images to prevent dominant classes from overpowering the visual feature space.

### Key Metrics:
- **Total Curated Images:** **15,566**
- **Training Split (Train):** **12,407** (79.7%)
- **Validation Split (Val):** **1,579** (10.1%)
- **Test Split (Test):** **1,580** (10.2%)
- **Total Classes:** **46** (44 with verified real data, 2 documented gap / aliased)
- **Exact Duplicate Leakage:** **0 images (0.0%)**
- **Benchmark Contamination:** **0 images (0.0%)**
- **Model 2 V4 Test Contamination:** **0 images (0.0%)**
- **Corrupt / Invalid Images:** **0**

---

## 2. Per-Class Distribution & Split Breakdown

| # | Canonical Class | Total Images | Train | Val | Test | Dataset % | Category / Status |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | **`anthurium`** | **104** | 84 | 10 | 10 | 0.67% | BASELINE (Greenhouse/Flora) |
| 2 | **`apple`** | **566** | 452 | 57 | 57 | 3.64% | NEW (Agricultural) |
| 3 | **`banana`** | **536** | 428 | 54 | 54 | 3.44% | NEW (Agricultural) |
| 4 | **`basil`** | **63** | 51 | 6 | 6 | 0.40% | NEW (Agricultural) | LOW DATA |
| 5 | **`blueberry`** | **314** | 252 | 31 | 31 | 2.02% | BASELINE (Greenhouse/Flora) |
| 6 | **`broccoli`** | **414** | 332 | 41 | 41 | 2.66% | BASELINE (Greenhouse/Flora) |
| 7 | **`cabbage`** | **274** | 220 | 27 | 27 | 1.76% | NEW (Agricultural) |
| 8 | **`capsicum`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 9 | **`carnation`** | **51** | 41 | 5 | 5 | 0.33% | BASELINE (Greenhouse/Flora) | LOW DATA |
| 10 | **`carrot`** | **148** | 118 | 15 | 15 | 0.95% | NEW (Agricultural) |
| 11 | **`cauliflower`** | **104** | 84 | 10 | 10 | 0.67% | NEW (Agricultural) |
| 12 | **`celery`** | **65** | 53 | 6 | 6 | 0.42% | NEW (Agricultural) | LOW DATA |
| 13 | **`cherry`** | **139** | 111 | 14 | 14 | 0.89% | NEW (Agricultural) |
| 14 | **`cherry_tomato`** | **0** | 0 | 0 | 0 | 0.00% | BASELINE (Greenhouse/Flora) | DOCUMENTED GAP |
| 15 | **`chrysanthemum`** | **418** | 334 | 42 | 42 | 2.69% | BASELINE (Greenhouse/Flora) |
| 16 | **`citrus`** | **521** | 417 | 52 | 52 | 3.35% | NEW (Agricultural) |
| 17 | **`coffee`** | **284** | 228 | 28 | 28 | 1.82% | NEW (Agricultural) |
| 18 | **`corn`** | **616** | 492 | 62 | 62 | 3.96% | NEW (Agricultural) |
| 19 | **`cucumber`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 20 | **`eggplant`** | **136** | 108 | 14 | 14 | 0.87% | NEW (Agricultural) |
| 21 | **`french_bean`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 22 | **`garlic`** | **198** | 158 | 20 | 20 | 1.27% | NEW (Agricultural) |
| 23 | **`geranium`** | **251** | 201 | 25 | 25 | 1.61% | BASELINE (Greenhouse/Flora) |
| 24 | **`gerbera`** | **3** | 2 | 0 | 1 | 0.02% | BASELINE (Greenhouse/Flora) | LOW DATA |
| 25 | **`ginger`** | **91** | 73 | 9 | 9 | 0.58% | NEW (Agricultural) | LOW DATA |
| 26 | **`grape`** | **558** | 446 | 56 | 56 | 3.58% | NEW (Agricultural) |
| 27 | **`gypsophila`** | **0** | 0 | 0 | 0 | 0.00% | BASELINE (Greenhouse/Flora) | DOCUMENTED GAP |
| 28 | **`lettuce`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 29 | **`lilium`** | **45** | 37 | 4 | 4 | 0.29% | BASELINE (Greenhouse/Flora) | LOW DATA |
| 30 | **`maple`** | **113** | 91 | 11 | 11 | 0.73% | NEW (Agricultural) |
| 31 | **`marigold`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 32 | **`melon`** | **247** | 197 | 25 | 25 | 1.59% | BASELINE (Greenhouse/Flora) |
| 33 | **`orchid`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 34 | **`peach`** | **444** | 356 | 44 | 44 | 2.85% | NEW (Agricultural) |
| 35 | **`plum`** | **215** | 171 | 22 | 22 | 1.38% | NEW (Agricultural) |
| 36 | **`potato`** | **239** | 191 | 24 | 24 | 1.54% | NEW (Agricultural) |
| 37 | **`raspberry`** | **123** | 99 | 12 | 12 | 0.79% | NEW (Agricultural) |
| 38 | **`rice`** | **155** | 123 | 16 | 16 | 1.00% | NEW (Agricultural) |
| 39 | **`rose`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 40 | **`soybean`** | **630** | 500 | 65 | 65 | 4.05% | NEW (Agricultural) |
| 41 | **`spinach`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 42 | **`strawberry`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 43 | **`tobacco`** | **178** | 142 | 18 | 18 | 1.14% | NEW (Agricultural) |
| 44 | **`tomato`** | **630** | 500 | 65 | 65 | 4.05% | BASELINE (Greenhouse/Flora) |
| 45 | **`wheat`** | **630** | 500 | 65 | 65 | 4.05% | NEW (Agricultural) |
| 46 | **`zucchini`** | **393** | 315 | 39 | 39 | 2.52% | BASELINE (Greenhouse/Flora) |

---

## 3. Strict Production Safety & Contamination Audits

| Audit Requirement | Verification Method | Result | Status |
| :--- | :--- | :---: | :---: |
| **No 178-Benchmark Images in Test Split** | SHA-256 hash match against `data/external/end_to_end_test/` | **0 matches** | **PASS (100% Clean)** |
| **No Model 2 V4 Test Images in Test Split** | SHA-256 hash match against Model 2 V4 test split | **0 matches** | **PASS (100% Clean)** |
| **Zero Cross-Split Hash Leakage** | SHA-256 intersection: `(Train ∩ Val) ∪ (Train ∩ Test) ∪ (Val ∩ Test)` | **0 leaks** | **PASS (100% Clean)** |
| **Corrupted Image Elimination** | PIL `verify()` + dimension check ($\ge 32\times 32$) | **0 corrupt** | **PASS** |
| **Exact Duplicate Elimination** | Intra-class and inter-class SHA-256 uniqueness | **0 duplicates** | **PASS** |

---

## 4. Class Balancing & Capping Rationale

In accordance with Phase instructions:
1. **Oversized Classes Capped:** High-volume crops (`wheat`, `soybean`, `tomato`, `cucumber`, `capsicum`, `lettuce`, `rose`, `spinach`, `strawberry`, `french_bean`, `orchid`, `marigold`) were capped at **500 training images** (plus 65 validation and 65 test images). This prevents large classes from skewing gradients while maintaining sufficient intra-class phenotypic diversity.
2. **Moderate Classes Preserved:** Crops with 100–400 images (`broccoli`, `chrysanthemum`, `zucchini`, `coffee`, `cabbage`, `blueberry`, `potato`, `plum`, `garlic`, `tobacco`, `rice`, `carrot`, `cherry`, `eggplant`, `cauliflower`, `raspberry`, `melon`, `geranium`, `maple`) were preserved at their full verified volume with 80/10/10 stratification.
3. **Low-Data Minority Classes Preserved:** Specialized floriculture and spice crops (`anthurium`, `carnation`, `lilium`, `ginger`, `celery`, `basil`, `gerbera`) were preserved with zero synthetic duplication.
4. **Documented Gaps:** `cherry_tomato` is structurally aliased to `tomato`, and `gypsophila` remains documented as 0 images pending dedicated flower acquisition.

---

## 5. Source Breakdown

| Source Dataset | Images | Share | Primary Crops |
| :--- | :---: | :---: | :--- |
| `model2_v4_plantseg` | **4,550** | 29.23% | apple, banana, basil, cabbage |
| `model2_v4_plantseg_v3_supplementary` | **2,181** | 14.01% | apple, banana, basil, cabbage |
| `Herbal_Dataset.v11i.yolov11` | **921** | 5.92% | chrysanthemum, cucumber, marigold, melon |
| `pepper_bell` | **630** | 4.05% | capsicum |
| `lettuce-disease.v6i.folder` | **630** | 4.05% | lettuce |
| `Orchid_source` | **630** | 4.05% | orchid |
| `spinach_disease` | **630** | 4.05% | spinach |
| `cucumber` | **625** | 4.02% | cucumber |
| `rose_new` | **611** | 3.93% | rose |
| `tomato` | **597** | 3.84% | tomato |
| `hf_makerere_beans` | **572** | 3.67% | french_bean |
| `strawberry_clean` | **562** | 3.61% | strawberry |
| `broccoli_new` | **414** | 2.66% | broccoli |
| `Marigold_new` | **372** | 2.39% | marigold |
| `plantseg` | **337** | 2.16% | french_bean, tomato, zucchini |
| `model2_v4_anand_soybean_rust_hf` | **254** | 1.63% | soybean |
| `blueberry_leaves` | **201** | 1.29% | blueberry |
| `zuchhini` | **141** | 0.91% | zucchini |
| `medicinal_plants` | **135** | 0.87% | geranium |
| `geranium` | **116** | 0.75% | geranium |
| `blueberry` | **112** | 0.72% | blueberry |
| `anthurium` | **104** | 0.67% | anthurium |
| `carnation` | **51** | 0.33% | carnation |
| `strawberry_leaves` | **47** | 0.30% | strawberry |
| `oxford_flowers_102` | **45** | 0.29% | lilium |
| `Fruits Model.v1i.yolov11` | **32** | 0.21% | melon |
| `model2_v4_external_healthy_cauliflower` | **29** | 0.19% | cauliflower |
| `strawberry` | **21** | 0.13% | strawberry |
| `model2_v4_external_healthy_cabbage` | **12** | 0.08% | cabbage |
| `gerbera_commons` | **3** | 0.02% | gerbera |
| `blueberry_leaves_external` | **1** | 0.01% | blueberry |

---

## 6. Final Certification

The dataset located at `data/processed/model1_expanded/` has been compiled, deduplicated, verified, and audited. It is certified **READY FOR EXPANDED MODEL 1 TRAINING**.
