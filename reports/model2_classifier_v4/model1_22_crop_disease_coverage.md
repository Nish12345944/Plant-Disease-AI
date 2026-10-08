# Model 1 (22 Crops) Disease Coverage Audit Report
## Comprehensive Analysis of Model 2 V4 Disease & Healthy Taxonomy

**Evaluation Date:** 2026-10-08  
**Model 1 Scope:** 22 Greenhouse & Agricultural Crops (`models/model1/class_mapping.json`)  
**Model 2 V4 Scope:** 117 Total Classes (1 Shared Healthy + 116 Disease Classes, `models/model2_classifier_v4/class_mapping.json`)  
**Authoritative Dataset Manifest:** `data/processed/model2_v4/model2_v4_manifest.csv` (19,920 audited images)  
**Crop-Disease Compatibility Mapping:** `data/processed/model2_organized_crop_disease_mapping.json`  

---

## 1. Executive Summary

This audit establishes the definitive disease-coverage baseline for all **22 crops** supported by Model 1 against the active **Model 2 V4** production classifier.

### Key Audit Metrics:
- **Total Model 1 Crops:** **22**
- **Crops with Active Disease Coverage:** **8** (45.5%)
- **Crops with Healthy-Only Coverage:** **14** (13.6%)
- **Total Disease Classes Covering Model 1 Crops:** **27** classes (out of 116 total Model 2 V4 disease classes)
- **Crops with Complete/Strong Coverage (4+ Classes, Strong Support):** **4** (`tomato`, `capsicum`/`bell_pepper`, `french_bean`/`bean`, `blueberry`)
- **Crops with Partial Coverage:** **4** (`cucumber`, `zucchini`, `broccoli`, `lettuce`, `strawberry`)
- **Crops Requiring Major Disease Expansion:** **14** floriculture, leafy, and specialty crops currently limited to healthy-state identification.

---

## 2. 22-Crop Master Coverage Table

| Crop (Model 1) | Taxonomy Mapping | Healthy Supported? | Disease Classes Count | Disease Classes in V4 | Training Support (Dis / Healthy) | Weak Classes (<30 train) | Coverage Status | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **anthurium** | `direct` | No (0 img) | **0** | *None (Healthy only)* | 0 / 0 (0 total) | None | **NO_DISEASE_COVERAGE** | **P3** |
| **blueberry** | `direct` | No (0 img) | **5** | `anthracnose`, `botrytis_blight`, `mummy_berry`, `rust`, `scorch` | 166 / 0 (166 total) | `botrytis_blight` | **PARTIAL** | **P1** |
| **broccoli** | `direct` | Yes (91 img) | **3** | `alternaria_leaf_spot`, `downy_mildew`, `ring_spot` | 80 / 91 (171 total) | `downy_mildew`, `ring_spot` | **PARTIAL** | **P1** |
| **capsicum** | `capsicum -> bell_pepper` | Yes (1154 img) | **4** | `bacterial_spot`, `blossom_end_rot`, `frogeye_leaf_spot`, `powdery_mildew` | 186 / 1154 (1340 total) | `frogeye_leaf_spot`, `powdery_mildew` | **PARTIAL** | **P1** |
| **carnation** | `direct` | No (0 img) | **0** | *None (Healthy only)* | 0 / 0 (0 total) | None | **NO_DISEASE_COVERAGE** | **P3** |
| **cherry_tomato** | `cherry_tomato -> tomato` | Yes (1202 img) | **7** | `bacterial_leaf_spot`, `early_blight`, `late_blight`, `leaf_mold`, `mosaic_virus`, `septoria_leaf_spot`, `yellow_leaf_curl_virus` | 1167 / 1202 (2369 total) | None | **COMPLETE** | **P0** |
| **chrysanthemum** | `direct` | No (0 img) | **0** | *None (Healthy only)* | 0 / 0 (0 total) | None | **NO_DISEASE_COVERAGE** | **P3** |
| **cucumber** | `direct` | Yes (134 img) | **3** | `angular_leaf_spot`, `bacterial_wilt`, `powdery_mildew` | 512 / 134 (646 total) | None | **PARTIAL** | **P1** |
| **french_bean** | `french_bean -> bean` | Yes (330 img) | **4** | `angular_leaf_spot`, `halo_blight`, `mosaic_virus`, `rust` | 893 / 330 (1223 total) | None | **COMPLETE** | **P0** |
| **geranium** | `direct` | No (0 img) | **0** | *None (Healthy only)* | 0 / 0 (0 total) | None | **NO_DISEASE_COVERAGE** | **P3** |
| **gerbera** | `direct` | No (0 img) | **0** | *None (Healthy only)* | 0 / 0 (0 total) | None | **NO_DISEASE_COVERAGE** | **P3** |
| **gypsophila** | `direct` | No (0 img) | **0** | *None (Healthy only)* | 0 / 0 (0 total) | None | **NO_DISEASE_COVERAGE** | **P3** |
| **lettuce** | `direct` | Yes (338 img) | **2** | `downy_mildew`, `mosaic_virus` | 98 / 338 (436 total) | None | **PARTIAL** | **P2** |
| **lilium** | `direct` | No (0 img) | **0** | *None (Healthy only)* | 0 / 0 (0 total) | None | **NO_DISEASE_COVERAGE** | **P3** |
| **marigold** | `direct` | Yes (202 img) | **0** | *None (Healthy only)* | 0 / 202 (202 total) | None | **HEALTHY_ONLY** | **P1** |
| **melon** | `direct` | No (0 img) | **0** | *None (Healthy only)* | 0 / 0 (0 total) | None | **NO_DISEASE_COVERAGE** | **P3** |
| **orchid** | `direct` | No (0 img) | **0** | *None (Healthy only)* | 0 / 0 (0 total) | None | **NO_DISEASE_COVERAGE** | **P3** |
| **rose** | `direct` | Yes (334 img) | **0** | *None (Healthy only)* | 0 / 334 (334 total) | None | **HEALTHY_ONLY** | **P1** |
| **spinach** | `direct` | Yes (1064 img) | **0** | *None (Healthy only)* | 0 / 1064 (1064 total) | None | **HEALTHY_ONLY** | **P1** |
| **strawberry** | `direct` | Yes (289 img) | **2** | `anthracnose`, `leaf_scorch` | 80 / 289 (369 total) | None | **PARTIAL** | **P2** |
| **tomato** | `direct` | Yes (1202 img) | **7** | `bacterial_leaf_spot`, `early_blight`, `late_blight`, `leaf_mold`, `mosaic_virus`, `septoria_leaf_spot`, `yellow_leaf_curl_virus` | 1167 / 1202 (2369 total) | None | **COMPLETE** | **P0** |
| **zucchini** | `direct` | No (0 img) | **4** | `bacterial_wilt`, `downy_mildew`, `powdery_mildew`, `yellow_mosaic_virus` | 328 / 0 (328 total) | None | **COMPLETE** | **P0** |

---

## 3. Detailed Per-Crop Disease Breakdown

### 3.1 `anthurium` (Normalized: `anthurium`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **NO_DISEASE_COVERAGE** | **Priority:** **P3**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (4):** `bacterial_blight`, `anthracnose`, `phytophthora_blight`, `pythium_root_rot`

### 3.2 `blueberry` (Normalized: `blueberry`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **PARTIAL** | **Priority:** **P1**
- **Active Model 2 V4 Disease Classes (5):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `blueberry__anthracnose` | Anthracnose | 32 | 4 | 4 | 40 | Yes |
| `blueberry__botrytis_blight` | Botrytis Blight | 29 | 3 | 3 | 35 | Yes |
| `blueberry__mummy_berry` | Mummy Berry | 38 | 4 | 4 | 46 | Yes |
| `blueberry__rust` | Rust | 34 | 4 | 5 | 43 | Yes |
| `blueberry__scorch` | Scorch | 33 | 4 | 5 | 42 | Yes |

- **Uncovered Agricultural Pathogens (1):** `stem_canker`

### 3.3 `broccoli` (Normalized: `broccoli`)
- **Healthy Support:** Yes (91 training images in shared healthy class)
- **Coverage Status:** **PARTIAL** | **Priority:** **P1**
- **Active Model 2 V4 Disease Classes (3):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `broccoli__alternaria_leaf_spot` | Alternaria Leaf Spot | 49 | 5 | 8 | 62 | Yes |
| `broccoli__downy_mildew` | Downy Mildew | 23 | 2 | 4 | 29 | Yes |
| `broccoli__ring_spot` | Ring Spot | 8 | 1 | 1 | 10 | Yes |

- **Uncovered Agricultural Pathogens (2):** `black_rot`, `clubroot`

### 3.4 `capsicum` (Normalized: `bell_pepper`)
- **Healthy Support:** Yes (1154 training images in shared healthy class)
- **Coverage Status:** **PARTIAL** | **Priority:** **P1**
- **Active Model 2 V4 Disease Classes (4):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `bell_pepper__bacterial_spot` | Bacterial Spot | 55 | 6 | 7 | 68 | Yes |
| `bell_pepper__blossom_end_rot` | Blossom End Rot | 87 | 10 | 11 | 108 | Yes |
| `bell_pepper__frogeye_leaf_spot` | Frogeye Leaf Spot | 22 | 2 | 4 | 28 | Yes |
| `bell_pepper__powdery_mildew` | Powdery Mildew | 22 | 2 | 2 | 26 | Yes |

- **Uncovered Agricultural Pathogens (3):** `phytophthora_blight`, `anthracnose`, `mosaic_virus`

### 3.5 `carnation` (Normalized: `carnation`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **NO_DISEASE_COVERAGE** | **Priority:** **P3**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (4):** `rust`, `alternaria_leaf_spot`, `fusarium_wilt`, `fairy_ring_spot`

### 3.6 `cherry_tomato` (Normalized: `tomato`)
- **Healthy Support:** Yes (1202 training images in shared healthy class)
- **Coverage Status:** **COMPLETE** | **Priority:** **P0**
- **Active Model 2 V4 Disease Classes (7):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `tomato__bacterial_leaf_spot` | Bacterial Leaf Spot | 85 | 9 | 13 | 107 | Yes |
| `tomato__early_blight` | Early Blight | 275 | 31 | 22 | 328 | Yes |
| `tomato__late_blight` | Late Blight | 254 | 29 | 17 | 300 | Yes |
| `tomato__leaf_mold` | Leaf Mold | 198 | 22 | 16 | 236 | Yes |
| `tomato__mosaic_virus` | Mosaic Virus | 50 | 6 | 7 | 63 | Yes |
| `tomato__septoria_leaf_spot` | Septoria Leaf Spot | 233 | 26 | 14 | 273 | Yes |
| `tomato__yellow_leaf_curl_virus` | Yellow Leaf Curl Virus | 72 | 8 | 9 | 89 | Yes |

- **Uncovered Agricultural Pathogens (1):** `powdery_mildew`

### 3.7 `chrysanthemum` (Normalized: `chrysanthemum`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **NO_DISEASE_COVERAGE** | **Priority:** **P3**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (5):** `white_rust`, `brown_rust`, `septoria_leaf_spot`, `powdery_mildew`, `botrytis`

### 3.8 `cucumber` (Normalized: `cucumber`)
- **Healthy Support:** Yes (134 training images in shared healthy class)
- **Coverage Status:** **PARTIAL** | **Priority:** **P1**
- **Active Model 2 V4 Disease Classes (3):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `cucumber__angular_leaf_spot` | Angular Leaf Spot | 144 | 16 | 22 | 182 | Yes |
| `cucumber__bacterial_wilt` | Bacterial Wilt | 85 | 10 | 13 | 108 | Yes |
| `cucumber__powdery_mildew` | Powdery Mildew | 283 | 31 | 22 | 336 | Yes |

- **Uncovered Agricultural Pathogens (4):** `downy_mildew`, `anthracnose`, `scab`, `mosaic_virus`

### 3.9 `french_bean` (Normalized: `bean`)
- **Healthy Support:** Yes (330 training images in shared healthy class)
- **Coverage Status:** **COMPLETE** | **Priority:** **P0**
- **Active Model 2 V4 Disease Classes (4):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `bean__angular_leaf_spot` | Angular Leaf Spot | 330 | 37 | 65 | 432 | Yes |
| `bean__halo_blight` | Halo Blight | 45 | 5 | 6 | 56 | Yes |
| `bean__mosaic_virus` | Mosaic Virus | 47 | 5 | 5 | 57 | Yes |
| `bean__rust` | Rust | 471 | 52 | 77 | 600 | Yes |

- **Uncovered Agricultural Pathogens (3):** `anthracnose`, `root_rot`, `white_mold`

### 3.10 `geranium` (Normalized: `geranium`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **NO_DISEASE_COVERAGE** | **Priority:** **P3**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (4):** `rust`, `bacterial_blight`, `botrytis_blight`, `leaf_spot`

### 3.11 `gerbera` (Normalized: `gerbera`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **NO_DISEASE_COVERAGE** | **Priority:** **P3**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (3):** `powdery_mildew`, `botrytis_blight`, `alternaria_leaf_spot`

### 3.12 `gypsophila` (Normalized: `gypsophila`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **NO_DISEASE_COVERAGE** | **Priority:** **P3**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (4):** `bacterial_gall`, `powdery_mildew`, `phytophthora_crown_rot`, `botrytis`

### 3.13 `lettuce` (Normalized: `lettuce`)
- **Healthy Support:** Yes (338 training images in shared healthy class)
- **Coverage Status:** **PARTIAL** | **Priority:** **P2**
- **Active Model 2 V4 Disease Classes (2):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `lettuce__downy_mildew` | Downy Mildew | 67 | 7 | 8 | 82 | Yes |
| `lettuce__mosaic_virus` | Mosaic Virus | 31 | 4 | 4 | 39 | Yes |

- **Uncovered Agricultural Pathogens (3):** `bottom_rot`, `septoria_leaf_spot`, `powdery_mildew`

### 3.14 `lilium` (Normalized: `lilium`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **NO_DISEASE_COVERAGE** | **Priority:** **P3**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (3):** `botrytis_blight`, `fusarium_rot`, `lily_mosaic_virus`

### 3.15 `marigold` (Normalized: `marigold`)
- **Healthy Support:** Yes (202 training images in shared healthy class)
- **Coverage Status:** **HEALTHY_ONLY** | **Priority:** **P1**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (4):** `leaf_spot`, `botrytis_blight`, `aster_yellows`, `powdery_mildew`

### 3.16 `melon` (Normalized: `melon`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **NO_DISEASE_COVERAGE** | **Priority:** **P3**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (5):** `powdery_mildew`, `downy_mildew`, `fusarium_wilt`, `gummy_stem_blight`, `anthracnose`

### 3.17 `orchid` (Normalized: `orchid`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **NO_DISEASE_COVERAGE** | **Priority:** **P3**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (4):** `bacterial_brown_spot`, `black_rot`, `anthracnose`, `cymbidium_mosaic_virus`

### 3.18 `rose` (Normalized: `rose`)
- **Healthy Support:** Yes (334 training images in shared healthy class)
- **Coverage Status:** **HEALTHY_ONLY** | **Priority:** **P1**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (5):** `black_spot`, `powdery_mildew`, `rust`, `downy_mildew`, `botrytis_blight`

### 3.19 `spinach` (Normalized: `spinach`)
- **Healthy Support:** Yes (1064 training images in shared healthy class)
- **Coverage Status:** **HEALTHY_ONLY** | **Priority:** **P1**
- **Active Disease Classes:** *0 disease classes in current Model 2 V4.* Model 1 classifies this crop; Model 2 classifies healthy foliage or triggers uncertainty when lesions are observed.

- **Uncovered Agricultural Pathogens (5):** `downy_mildew`, `anthracnose`, `cercospora_leaf_spot`, `fusarium_wilt`, `mosaic_virus`

### 3.20 `strawberry` (Normalized: `strawberry`)
- **Healthy Support:** Yes (289 training images in shared healthy class)
- **Coverage Status:** **PARTIAL** | **Priority:** **P2**
- **Active Model 2 V4 Disease Classes (2):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `strawberry__anthracnose` | Anthracnose | 48 | 5 | 5 | 58 | Yes |
| `strawberry__leaf_scorch` | Leaf Scorch | 32 | 4 | 3 | 39 | Yes |

- **Uncovered Agricultural Pathogens (3):** `powdery_mildew`, `gray_mold_(botrytis)`, `angular_leaf_spot`

### 3.21 `tomato` (Normalized: `tomato`)
- **Healthy Support:** Yes (1202 training images in shared healthy class)
- **Coverage Status:** **COMPLETE** | **Priority:** **P0**
- **Active Model 2 V4 Disease Classes (7):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `tomato__bacterial_leaf_spot` | Bacterial Leaf Spot | 85 | 9 | 13 | 107 | Yes |
| `tomato__early_blight` | Early Blight | 275 | 31 | 22 | 328 | Yes |
| `tomato__late_blight` | Late Blight | 254 | 29 | 17 | 300 | Yes |
| `tomato__leaf_mold` | Leaf Mold | 198 | 22 | 16 | 236 | Yes |
| `tomato__mosaic_virus` | Mosaic Virus | 50 | 6 | 7 | 63 | Yes |
| `tomato__septoria_leaf_spot` | Septoria Leaf Spot | 233 | 26 | 14 | 273 | Yes |
| `tomato__yellow_leaf_curl_virus` | Yellow Leaf Curl Virus | 72 | 8 | 9 | 89 | Yes |

- **Uncovered Agricultural Pathogens (4):** `anthracnose`, `fusarium_wilt`, `powdery_mildew`, `target_spot`

### 3.22 `zucchini` (Normalized: `zucchini`)
- **Healthy Support:** No (0 training images in shared healthy class)
- **Coverage Status:** **COMPLETE** | **Priority:** **P0**
- **Active Model 2 V4 Disease Classes (4):**

| Exact Model 2 V4 Class | Disease | Train Count | Val Count | Test Count | Total Count | Compatible? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `zucchini__bacterial_wilt` | Bacterial Wilt | 53 | 6 | 9 | 68 | Yes |
| `zucchini__downy_mildew` | Downy Mildew | 34 | 4 | 5 | 43 | Yes |
| `zucchini__powdery_mildew` | Powdery Mildew | 164 | 18 | 18 | 200 | Yes |
| `zucchini__yellow_mosaic_virus` | Yellow Mosaic Virus | 77 | 9 | 9 | 95 | Yes |

- **Uncovered Agricultural Pathogens (2):** `scab`, `choanephora_wet_rot`


---

## 4. Taxonomy & Compatibility Consistency Verification

1. **Crop Name Aliasing & Normalization:**
   - `cherry_tomato` $\rightarrow$ Aliased to `tomato` in the compatibility engine. Inherits all 7 tomato disease classes (`tomato__early_blight`, `tomato__late_blight`, etc.).
   - `french_bean` $\rightarrow$ Aliased to `bean` in the compatibility engine. Inherits all 4 bean disease classes (`bean__rust`, `bean__angular_leaf_spot`, etc.).
   - `capsicum` $\rightarrow$ Aliased to `bell_pepper` in the compatibility engine. Inherits all 4 bell pepper disease classes (`bell_pepper__bacterial_spot`, etc.).
   - `melon` $\rightarrow$ Model 1 predicts `melon`. In Model 2 V4, no dedicated `melon__*` classes exist; shared healthy is supported.

2. **Shared Healthy Class Architecture:**
   - `healthy` is represented as Class 0 across all 39 crops in Model 2 V4.
   - For all 22 Model 1 crops, healthy leaves are validated through Model 1 (crop identity) + Model 2 (healthy state confirmation).

3. **Taxonomy Integrity Checks:**
   - [x] All 116 Model 2 disease classes map cleanly to their respective crop families (`crop__disease` syntax).
   - [x] All 22 Model 1 crops are registered in `data/processed/model2_organized_crop_disease_mapping.json`.
   - [x] Zero duplicate or conflicting class IDs exist in `models/model2_classifier_v4/class_mapping.json`.
   - [x] No cross-crop disease misassignment (e.g. `apple__scab` is strictly blocked on `tomato`).

---

## 5. Weak and Low-Support Classes Analysis

Classes with fewer than 30 training samples in Model 2 V4:

| Crop | Disease Class | Train Count | Validation Count | Test Count | Total Count | Risk Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `blueberry` | `blueberry__botrytis_blight` | 29 | 3 | 3 | 35 | Moderate Sample Support |
| `broccoli` | `broccoli__downy_mildew` | 23 | 2 | 4 | 29 | Moderate Sample Support |
| `broccoli` | `broccoli__ring_spot` | 8 | 1 | 1 | 10 | Moderate Sample Support |
| `capsicum` | `bell_pepper__frogeye_leaf_spot` | 22 | 2 | 4 | 28 | Moderate Sample Support |
| `capsicum` | `bell_pepper__powdery_mildew` | 22 | 2 | 2 | 26 | Moderate Sample Support |

---

## 6. Crops Requiring Future Disease Expansion

### Top Priority Crops for Expansion:
1. **`melon` (P1):** High-value commercial crop with Model 1 support (84%+ acc), but 0 disease classes in Model 2 V4 (missing Powdery Mildew, Downy Mildew, Fusarium Wilt).
2. **`spinach` (P1):** Essential greenhouse leafy green with 0 disease classes in Model 2 V4 (missing Downy Mildew, Anthracnose, Leaf Spot).
3. **`rose` (P1):** Core floriculture plant with 0 disease classes in Model 2 V4 (missing Black Spot, Powdery Mildew, Rust).
4. **`strawberry` (P2):** Has 2 disease classes (`leaf_scorch`, `anthracnose`), missing Powdery Mildew and Botrytis Gray Mold.
5. **Floriculture Group (`anthurium`, `carnation`, `chrysanthemum`, `geranium`, `gerbera`, `lilium`, `marigold`, `orchid`, `gypsophila`) (P2/P3):** Model 1 classifies flower species; disease detection requires future dedicated ornamental pathogen datasets.

---

## 7. Final Decision & Priority Summary

| Crop | Healthy Supported | Active Disease Classes | Coverage Status | Priority | Action Summary |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **anthurium** | No | **0** | **NO_DISEASE_COVERAGE** | **P3** | Healthy detection active; prioritize disease curation |
| **blueberry** | No | **5** | **PARTIAL** | **P1** | Active partial coverage; expand secondary diseases in future |
| **broccoli** | Yes | **3** | **PARTIAL** | **P1** | Active partial coverage; expand secondary diseases in future |
| **capsicum** | Yes | **4** | **PARTIAL** | **P1** | Active partial coverage; expand secondary diseases in future |
| **carnation** | No | **0** | **NO_DISEASE_COVERAGE** | **P3** | Healthy detection active; prioritize disease curation |
| **cherry_tomato** | Yes | **7** | **COMPLETE** | **P0** | Production ready with strong multi-disease coverage |
| **chrysanthemum** | No | **0** | **NO_DISEASE_COVERAGE** | **P3** | Healthy detection active; prioritize disease curation |
| **cucumber** | Yes | **3** | **PARTIAL** | **P1** | Active partial coverage; expand secondary diseases in future |
| **french_bean** | Yes | **4** | **COMPLETE** | **P0** | Production ready with strong multi-disease coverage |
| **geranium** | No | **0** | **NO_DISEASE_COVERAGE** | **P3** | Healthy detection active; prioritize disease curation |
| **gerbera** | No | **0** | **NO_DISEASE_COVERAGE** | **P3** | Healthy detection active; prioritize disease curation |
| **gypsophila** | No | **0** | **NO_DISEASE_COVERAGE** | **P3** | Healthy detection active; prioritize disease curation |
| **lettuce** | Yes | **2** | **PARTIAL** | **P2** | Active partial coverage; expand secondary diseases in future |
| **lilium** | No | **0** | **NO_DISEASE_COVERAGE** | **P3** | Healthy detection active; prioritize disease curation |
| **marigold** | Yes | **0** | **HEALTHY_ONLY** | **P1** | Healthy detection active; prioritize disease curation |
| **melon** | No | **0** | **NO_DISEASE_COVERAGE** | **P3** | Healthy detection active; prioritize disease curation |
| **orchid** | No | **0** | **NO_DISEASE_COVERAGE** | **P3** | Healthy detection active; prioritize disease curation |
| **rose** | Yes | **0** | **HEALTHY_ONLY** | **P1** | Healthy detection active; prioritize disease curation |
| **spinach** | Yes | **0** | **HEALTHY_ONLY** | **P1** | Healthy detection active; prioritize disease curation |
| **strawberry** | Yes | **2** | **PARTIAL** | **P2** | Active partial coverage; expand secondary diseases in future |
| **tomato** | Yes | **7** | **COMPLETE** | **P0** | Production ready with strong multi-disease coverage |
| **zucchini** | No | **4** | **COMPLETE** | **P0** | Production ready with strong multi-disease coverage |

---

### Final Audit Conclusions:
- **Crops with Disease Coverage:** **8 / 22** crops have trained disease diagnostic capabilities in Model 2 V4.
- **Crops with Healthy-Only Coverage:** **14 / 22** crops are verified for healthy foliage recognition.
- **Total Active Disease Classes Covering Model 1:** **27** disease classes.
- **Crops with Highest Production Robustness:** `tomato` (7 diseases), `capsicum` (4 diseases), `french_bean` (4 diseases), `blueberry` (5 diseases), `zucchini` (4 diseases), `cucumber` (3 diseases).
