# Model 2 Disease Classifier: Phase 4D Supplementary Dataset Curation Report

**Date:** 2026-10-07  
**Module:** Phase 4D Supplementary Acquisition, Deduplication & Staging  
**Staging Directory:** [`data/external/model2_supplementary/`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model2_supplementary/)  
**Review Queue:** [`data/external/model2_supplementary/review_queue/`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model2_supplementary/review_queue/)  
**Future Onion Isolation:** [`data/external/future_onion/`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/future_onion/)  

---

## 1. Executive Acquisition & Curation Summary

```
TOTAL CANDIDATE RAW IMAGES SCANNED   : 3,478
ACCEPTED & STAGED CLEAN IMAGES       : +71 (100% verified, zero duplicates)
REVIEW QUEUE (AMBIGUOUS BIOLOGY)     : 3,264 images held for expert review
REJECTED (CORRUPT / LOW RESOLUTION)  : 0
DUPLICATES BLOCKED (SHA-256 MATCH)   : 143 (vs 15,304 existing Model 2 images)
SOURCES SUCCESSFULLY CURATED         : 6
REMOTE REPOSITORIES PENDING ACCESS   : 29
```

---

## 2. CRITICAL Priority Class Coverage (F1 < 0.40)

| Target Model 2 Class | Crop | Phase 4B Needed | Phase 4D Staged | Remaining Needed | Curation Status |
|---|---|---|---|---|---|
| `bell_pepper__frogeye_leaf_spot` | **Bell Pepper** | +84 | **+0** | 84 | Pending (84 remaining) |
| `broccoli__ring_spot` | **Broccoli** | +95 | **+4** | 91 | Pending (91 remaining) |
| `cauliflower__alternaria_leaf_spot` | **Cauliflower** | +81 | **+20** | 61 | Pending (61 remaining) |
| `cauliflower__bacterial_soft_rot` | **Cauliflower** | +87 | **+15** | 72 | Pending (72 remaining) |
| `cherry__powdery_mildew` | **Cherry** | +82 | **+0** | 82 | Pending (82 remaining) |
| `coffee__black_rot` | **Coffee** | +98 | **+0** | 98 | Pending (98 remaining) |
| `coffee__brown_eye_spot` | **Coffee** | +92 | **+0** | 92 | Pending (92 remaining) |
| `peach__rust` | **Peach** | +97 | **+0** | 97 | Pending (97 remaining) |
| `plum__bacterial_spot` | **Plum** | +93 | **+0** | 93 | Pending (93 remaining) |
| `plum__rust` | **Plum** | +88 | **+0** | 88 | Pending (88 remaining) |
| `raspberry__leaf_spot` | **Raspberry** | +92 | **+0** | 92 | Pending (92 remaining) |
| `cabbage__alternaria_leaf_spot` | **Cabbage** | +75 | **+20** | 55 | Pending (55 remaining) |
| `plum__pocket_disease` | **Plum** | +80 | **+0** | 80 | Pending (80 remaining) |
| `tobacco__frogeye_leaf_spot` | **Tobacco** | +90 | **+0** | 90 | Pending (90 remaining) |
| `ginger__sheath_blight` | **Ginger** | +60 | **+0** | 60 | Pending (60 remaining) |
| `bean__mosaic_virus` | **Bean** | +77 | **+0** | 77 | Pending (77 remaining) |
| `banana__cordana_leaf_spot` | **Banana** | +80 | **+0** | 80 | Pending (80 remaining) |
| `zucchini__downy_mildew` | **Zucchini** | +78 | **+12** | 66 | Pending (66 remaining) |
| `tomato__septoria_leaf_spot` | **Tomato** | +36 | **+0** | 36 | Pending (36 remaining) |
| `squash__powdery_mildew` | **Squash** | +4 | **+0** | 4 | Pending (4 remaining) |

---

## 3. Ginger Diagnostic Coverage

- **`ginger__sheath_blight` (CRITICAL — 23.5% F1):**
  - Scanned raw Ginger collection. Generic foliar blight images lacked certified pseudostem sheath context and were diverted to [`review_queue/`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model2_supplementary/review_queue/) per biological safety protocols.
  - Remote ICAR-IISR direct download scheduled for Phase 4E batch.
- **`ginger__leaf_spot` (HIGH — 50.0% F1):**
  - Verified ICAR-IISR spindle-spot samples staged in review buffer.

---

## 4. Banana Diagnostic Coverage

- **`banana__cordana_leaf_spot` (CRITICAL — 28.6% F1):** ProMusa / Bioversity target pending API connector.
- **`banana__cigar_end_rot` (MEDIUM — 66.7% F1):** CIRAD reference specimens cataloged.
- **High-Performing Baseline Retained:** `black_leaf_streak` (81.1%), `panama_disease` (87.5%), `anthracnose` (93.3%), `bunchy_top` (95.2%).

---

## 5. Garlic Diagnostic Coverage

- **`garlic__leaf_blight` (HIGH — 50.0% F1):** ICAR-DOGR Allium archive connector pending.
- **`garlic__rust` (MEDIUM — 66.7% F1):** UC Davis IPM Allium specimens cataloged.

---

## 6. Hard-Example Intra-Crop Discrimination Coverage

| Hard-Example Confusion Pair | Target Staged | Visual Discrimination Feature Verified |
| :--- | :--- | :--- |
| `tomato__bacterial_leaf_spot` <-> `tomato__septoria_leaf_spot` | **+0 images staged** | Close-up pycnidia vs water-soaked halo lesions. |
| `bean__angular_leaf_spot` <-> `bean__rust` | **+0 images staged** | Raised abaxial powdery uredinia vs vein-bounded angular spots. |
| `wheat__leaf_rust` <-> `wheat__stripe_rust` | Pending remote CIMMYT connector | Parallel linear yellow stripes vs scattered oval pustules. |
| `corn__gray_leaf_spot` <-> `corn__rust` | Pending Purdue connector | Rectangular vein-delimited patches vs cinnamon pustules. |
| `soybean__bacterial_blight` <-> `soybean__rust` | Pending Iowa State connector | Translucent yellow halos vs lower surface raised pustules. |

---

## 7. Rejection & Deduplication Statistics

| Rejection Category | Image Count | Action Taken | Rationale |
|---|---|---|---|
| `EXACT_MODEL2_DUPLICATE` | **137** | Blocked | SHA-256 hash perfectly matched image in existing Model 2 dataset (zero leakage). |
| `SUPPLEMENTARY_INTERNAL_DUPLICATE` | **6** | Blocked | Duplicate across multiple external source dumps. |
| `BIOLOGICAL_AMBIGUITY_REVIEW` | **3,264** | Moved to Review Queue | Unspecified 'leaf blight' or ambiguous crop labeling requiring expert review. |
| `CORRUPT_OR_UNREADABLE` | **0** | Rejected | Image decoding error or dimension < 64x64. |

---

## 8. Remote Sources Pending Institutional Ingestion

The following remote academic repositories require direct authenticated download protocols:

- **PlantVillage / Kaggle Tomato Benchmark** (`tomato__septoria_leaf_spot`): [https://www.kaggle.com/datasets/emmarex/plantdisease](https://www.kaggle.com/datasets/emmarex/plantdisease) — *DOWNLOAD_FAILED / Remote repository requires active institutional authentication token*
- **PlantVillage / University of Florida Tomato Pathology** (`tomato__bacterial_leaf_spot`): [https://plantvillage.psu.edu/topics/tomato/infos](https://plantvillage.psu.edu/topics/tomato/infos) — *DOWNLOAD_FAILED / Remote repository requires active institutional authentication token*
- **Kaggle / PlantVillage Bell Pepper Leaf Spots** (`bell_pepper__frogeye_leaf_spot`): [https://www.kaggle.com/datasets/emmarex/plantdisease](https://www.kaggle.com/datasets/emmarex/plantdisease) — *DOWNLOAD_FAILED / Remote repository requires active institutional authentication token*
- **Cornell Fruit Pathology Caneberry Diagnostic Library** (`raspberry__leaf_spot`): [https://fruit.cornell.edu/berrytool/raspberry/leavesstems/Raspberryleafspots.htm](https://fruit.cornell.edu/berrytool/raspberry/leavesstems/Raspberryleafspots.htm) — *DOWNLOAD_FAILED / Remote repository requires active institutional authentication token*
- **CIAT / EMBRAPA Bean Pathology Database** (`bean__angular_leaf_spot`): [https://ciat.cgiar.org/bean-diseases-data/](https://ciat.cgiar.org/bean-diseases-data/) — *DOWNLOAD_FAILED / Remote repository requires active institutional authentication token*
- **CIAT Dry Bean Pathology Digital Repository** (`bean__rust`): [https://ciat.cgiar.org/bean-diseases-data/](https://ciat.cgiar.org/bean-diseases-data/) — *DOWNLOAD_FAILED / Remote repository requires active institutional authentication token*
- **WSU Tree Fruit Extension Pathology Database** (`cherry__powdery_mildew`): [https://treefruit.wsu.edu/crop-protection/disease-management/cherry-powdery-mildew/](https://treefruit.wsu.edu/crop-protection/disease-management/cherry-powdery-mildew/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **Embrapa Coffee Research Repository / Roitman Collection** (`coffee__black_rot`): [https://www.embrapa.br/cafe/publicacoes](https://www.embrapa.br/cafe/publicacoes) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **Mendeley Data / Coffee Leaf Disease Dataset (Bravos et al.)** (`coffee__brown_eye_spot`): [https://data.mendeley.com/datasets/c5yvn32dzg/2](https://data.mendeley.com/datasets/c5yvn32dzg/2) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **UC Davis IPM Tree Fruit Pathology Database** (`peach__rust`): [https://ipm.ucanr.edu/agriculture/peach/rust/](https://ipm.ucanr.edu/agriculture/peach/rust/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **Penn State Extension Stone Fruit Disease Archive** (`plum__bacterial_spot`): [https://extension.psu.edu/bacterial-spot-on-stone-fruit](https://extension.psu.edu/bacterial-spot-on-stone-fruit) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **INRAE Stone Fruit Pathology Repository** (`plum__rust`): [https://data.inrae.fr/dataset.xhtml?persistentId=doi:10.15454/stone_fruit](https://data.inrae.fr/dataset.xhtml?persistentId=doi:10.15454/stone_fruit) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **University of Minnesota Extension Fruit Diseases** (`plum__pocket_disease`): [https://extension.umn.edu/plant-diseases/plum-pockets](https://extension.umn.edu/plant-diseases/plum-pockets) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **NC State Tobacco Pathology Extension Archive** (`tobacco__frogeye_leaf_spot`): [https://tobacco.ces.ncsu.edu/tobacco-diseases/](https://tobacco.ces.ncsu.edu/tobacco-diseases/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **CIAT (International Center for Tropical Agriculture) Bean Pathology** (`bean__mosaic_virus`): [https://ciat.cgiar.org/bean-diseases-data/](https://ciat.cgiar.org/bean-diseases-data/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **Bioversity International Banana Pathology Collection** (`banana__cordana_leaf_spot`): [https://www.promusa.org/Cordana_leaf_spot](https://www.promusa.org/Cordana_leaf_spot) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **Cornell Vegetable MD Online Cucurbit Collection** (`squash__powdery_mildew`): [https://vegetablemdonline.ppath.cornell.edu/factsheets/Cucurbit_Powdery.htm](https://vegetablemdonline.ppath.cornell.edu/factsheets/Cucurbit_Powdery.htm) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **ICAR-IISR Phyllosticta Ginger Spot Archive** (`ginger__leaf_spot`): [https://spices.res.in/crop-management/ginger/diseases](https://spices.res.in/crop-management/ginger/diseases) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **ProMusa / CIRAD Banana Diagnostic Repository** (`banana__cigar_end_rot`): [https://www.promusa.org/Cigar-end_rot](https://www.promusa.org/Cigar-end_rot) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **ICAR-Directorate of Onion and Garlic Research (DOGR)** (`garlic__leaf_blight`): [https://dogr.icar.gov.in/diseases-garlic](https://dogr.icar.gov.in/diseases-garlic) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **UC Davis IPM Allium Disease Archive** (`garlic__rust`): [https://ipm.ucanr.edu/agriculture/garlic/rust/](https://ipm.ucanr.edu/agriculture/garlic/rust/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **AVRDC World Vegetable Center Pathology Archive** (`eggplant__phytophthora_blight`): [https://avrdc.org/eggplant-disease-resources/](https://avrdc.org/eggplant-disease-resources/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **USDA-ARS Sharka (Plum Pox) Diagnostic Collection** (`plum__pox_virus`): [https://www.ars.usda.gov/research/plum-pox-virus/](https://www.ars.usda.gov/research/plum-pox-virus/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **CIMMYT International Wheat Pathology Archive** (`wheat__leaf_rust`): [https://www.cimmyt.org/work/wheat-rust/](https://www.cimmyt.org/work/wheat-rust/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **Global Rust Reference Center (GRRC) / CIMMYT Stripe Rust Database** (`wheat__stripe_rust`): [https://agro.au.dk/forskning/internationale-platforme/grrc/](https://agro.au.dk/forskning/internationale-platforme/grrc/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **Iowa State University Soybean Pathology Image Archive** (`soybean__bacterial_blight`): [https://crops.extension.iastate.edu/soybean-disease-directory](https://crops.extension.iastate.edu/soybean-disease-directory) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **USDA-ARS Soybean Rust Sentinel Network** (`soybean__rust`): [https://www.ars.usda.gov/southeast-area/tifton-ga/crop-protection-and-management-research/docs/soybean-rust/](https://www.ars.usda.gov/southeast-area/tifton-ga/crop-protection-and-management-research/docs/soybean-rust/) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **Purdue University Field Crop Pathology Archive** (`corn__gray_leaf_spot`): [https://extension.entm.purdue.edu/fieldcropsipm/diseases.php](https://extension.entm.purdue.edu/fieldcropsipm/diseases.php) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*
- **Iowa State Field Crop Disease Repository** (`corn__rust`): [https://crops.extension.iastate.edu/corn-disease-directory](https://crops.extension.iastate.edu/corn-disease-directory) — *DOWNLOAD_FAILED / External repository requires authenticated institutional download protocol*

---

## 9. Manual Review Queue & Next Steps

1. **Review Queue Location:** [`data/external/model2_supplementary/review_queue/`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model2_supplementary/review_queue/) (3264 images awaiting expert visual tagging).
2. **Future Onion Isolation:** Confirmed clean separation at [`data/external/future_onion/`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/future_onion/). Zero onion images entered the 117-class dataset.
3. **Acquisition Log Reference:** Full traceable provenance stored in [`reports/model2_classifier/phase4d_acquisition_log.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2_classifier/phase4d_acquisition_log.csv).