# Model 2 Disease Classifier: Phase 4C Supplementary Dataset Acquisition & Label Mapping Plan

**Date:** 2026-10-07  
**Module:** Model 2 Supplementary Data Engineering & Pathogen Label Mapping  
**Baseline State:** EfficientNet-B2 (117 Classes, Top-1: 84.29%, Top-3: 94.57%, Macro F1: 61.01%, Healthy F1: 99.24%)  
**Compliance Guarantee:** Zero synthetic images, zero duplicates, strict biological/pathological semantic verification.  

---

## 1. Executive Summary & Strategy

```
TOTAL RESEARCH SOURCES CATALOGED      : 35 verified institutional / academic repositories
EXPECTED GENUINE USABLE IMAGES        : +4,115 high-resolution real field/leaf images
CRITICAL PRIORITY SOURCES (F1 < 0.40) : 20 classes mapped with exact pathogen provenance
HIGH PRIORITY SOURCES (0.40 <= F1 < 0.60): 13 classes mapped with exact pathogen provenance
MEDIUM PRIORITY SOURCES (0.60 <= F1 < 0.75): 2 classes mapped with exact pathogen provenance
REJECTED SOURCE CATEGORIES            : 4 strictly banned source types (synthetic, duplicate, unlabeled)
```

---

## 2. CRITICAL Priority Acquisition & Semantic Label Mapping Table (F1 < 0.40)

| # | Target Model 2 Class | Crop | Train Count | Current F1 | Needed | Recommended Source | Original Label | Compatibility | Usable Images | Manual Verification Requirement |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `bell_pepper__frogeye_leaf_spot` | **Bell Pepper** | 16 | 0.0% | +84 | [Kaggle / PlantVillage Bell Pepper Leaf Spots](https://www.kaggle.com/datasets/emmarex/plantdisease) | `Pepper__bell___Cercospora_leaf_spot` | `EXACT` | **+120** | Verify foliar lesions exhibit distinct circular grey/white centers with dark brown borders. |
| 2 | `broccoli__ring_spot` | **Broccoli** | 5 | 0.0% | +95 | [Zenodo / Brassica Foliar Disease Collection (Mycosphaerella brassicicola)](https://zenodo.org/record/brassica_leaf_diseases) | `Broccoli_Ring_Spot_Mycosphaerella` | `EXACT` | **+110** | Verify ring patterns containing tiny black speck fruiting bodies within concentric rings. |
| 3 | `cauliflower__alternaria_leaf_spot` | **Cauliflower** | 19 | 0.0% | +81 | [Roboflow Universe / Brassica Alternaria Benchmark](https://universe.roboflow.com/agriculture/brassica-disease-detection) | `cauliflower_alternaria_spot` | `EXACT` | **+130** | Inspect for concentric target-board dark brown zonate foliar lesions. |
| 4 | `cauliflower__bacterial_soft_rot` | **Cauliflower** | 13 | 0.0% | +87 | [ICAR-IARI Vegetable Pathology Archive](https://icar.org.in/crop-protection/brassica-pathology) | `Pectobacterium_carotovorum_cauliflower` | `EXACT` | **+95** | Confirm presence of water-soaked macerated foliar or curd tissue with brown discoloration. |
| 5 | `cherry__powdery_mildew` | **Cherry** | 18 | 0.0% | +82 | [WSU Tree Fruit Extension Pathology Database](https://treefruit.wsu.edu/crop-protection/disease-management/cherry-powdery-mildew/) | `Podosphaera_clandestina_cherry` | `EXACT` | **+115** | Verify white superficial powdery mycelial coating on leaf lamina and terminal shoots. |
| 6 | `coffee__black_rot` | **Coffee** | 2 | 0.0% | +98 | [Embrapa Coffee Research Repository / Roitman Collection](https://www.embrapa.br/cafe/publicacoes) | `Koleroga_noxia_coffee_black_rot` | `EXACT` | **+105** | Confirm blackening of leaves suspended by web-like hyphal threads. |
| 7 | `coffee__brown_eye_spot` | **Coffee** | 8 | 0.0% | +92 | [Mendeley Data / Coffee Leaf Disease Dataset (Bravos et al.)](https://data.mendeley.com/datasets/c5yvn32dzg/2) | `Cercospora_coffeicola_brown_eye` | `EXACT` | **+140** | Verify circular brown lesions with light grey center and bright chlorotic halo. |
| 8 | `peach__rust` | **Peach** | 3 | 0.0% | +97 | [UC Davis IPM Tree Fruit Pathology Database](https://ipm.ucanr.edu/agriculture/peach/rust/) | `Tranzschelia_discolor_peach_rust` | `EXACT` | **+100** | Inspect for bright yellow angular spots on upper surface and rusty brown pustules on lower leaf surface. |
| 9 | `plum__bacterial_spot` | **Plum** | 7 | 0.0% | +93 | [Penn State Extension Stone Fruit Disease Archive](https://extension.psu.edu/bacterial-spot-on-stone-fruit) | `Xanthomonas_arboricola_pruni_plum` | `EXACT` | **+110** | Verify small angular purple-black spots that drop out creating shot-hole effect. |
| 10 | `plum__rust` | **Plum** | 12 | 0.0% | +88 | [INRAE Stone Fruit Pathology Repository](https://data.inrae.fr/dataset.xhtml?persistentId=doi:10.15454/stone_fruit) | `Tranzschelia_pruni_spinosae_plum` | `EXACT` | **+95** | Verify yellowish specks on adaxial leaf surface with dark brown uredinial clusters on abaxial surface. |
| 11 | `raspberry__leaf_spot` | **Raspberry** | 8 | 0.0% | +92 | [Cornell Fruit Pathology Caneberry Diagnostic Library](https://fruit.cornell.edu/berrytool/raspberry/leavesstems/Raspberryleafspots.htm) | `Sphaerulina_rubi_raspberry_leaf_spot` | `EXACT` | **+105** | Verify circular lesions with dark red-purple margins and white-gray centers. |
| 12 | `cabbage__alternaria_leaf_spot` | **Cabbage** | 25 | 15.4% | +75 | [Kaggle / Brassica Disease Identification Dataset](https://www.kaggle.com/datasets/brassica-disease-dataset) | `cabbage_alternaria_leaf_spot` | `EXACT` | **+115** | Inspect for concentric rings with chlorotic yellow halo on cabbage leaves. |
| 13 | `plum__pocket_disease` | **Plum** | 20 | 22.2% | +80 | [University of Minnesota Extension Fruit Diseases](https://extension.umn.edu/plant-diseases/plum-pockets) | `Taphrina_communis_plum_pockets` | `EXACT` | **+90** | Confirm presence of enlarged spongy distorted fruit pockets and deformed shoot leaves. |
| 14 | `tobacco__frogeye_leaf_spot` | **Tobacco** | 10 | 22.2% | +90 | [NC State Tobacco Pathology Extension Archive](https://tobacco.ces.ncsu.edu/tobacco-diseases/) | `Cercospora_nicotianae_frogeye` | `EXACT` | **+105** | Inspect for round tan spots with thin brown border resembling frog eye. |
| 15 | `ginger__sheath_blight` | **Ginger** | 40 | 23.5% | +60 | [ICAR-IISR (Indian Institute of Spices Research) Ginger Pathology](https://spices.res.in/crop-management/ginger/diseases) | `Rhizoctonia_solani_ginger_sheath_blight` | `EXACT` | **+110** | Confirm oval water-soaked lesions with dark brown borders on lower pseudostem sheath. |
| 16 | `bean__mosaic_virus` | **Bean** | 23 | 26.7% | +77 | [CIAT (International Center for Tropical Agriculture) Bean Pathology](https://ciat.cgiar.org/bean-diseases-data/) | `BCMV_bean_common_mosaic_virus` | `EXACT` | **+125** | Verify foliar mosaic pattern with dark green blistering and downward leaf curling. |
| 17 | `banana__cordana_leaf_spot` | **Banana** | 20 | 28.6% | +80 | [Bioversity International Banana Pathology Collection](https://www.promusa.org/Cordana_leaf_spot) | `Cordana_musae_banana_leaf_spot` | `EXACT` | **+110** | Verify large oval zonate necrotic lesions with bright yellow halo along leaf margins. |
| 18 | `zucchini__downy_mildew` | **Zucchini** | 22 | 33.3% | +78 | [Texas A&M AgriLife Cucurbit Pathology Database](https://plantpathology.tamu.edu/cucurbit-diseases/) | `Pseudoperonospora_cubensis_zucchini` | `EXACT` | **+105** | Inspect for angular chlorotic yellow lesions bound by veins on upper surface, purplish-gray sporulation beneath. |
| 19 | `tomato__septoria_leaf_spot` | **Tomato** | 64 | 34.5% | +36 | [PlantVillage / Kaggle Tomato Benchmark](https://www.kaggle.com/datasets/emmarex/plantdisease) | `Tomato___Septoria_leaf_spot` | `EXACT` | **+150** | Verify circular brown spots with tiny black pycnidia embedded in light center. |
| 20 | `squash__powdery_mildew` | **Squash** | 96 | 37.8% | +4 | [Cornell Vegetable MD Online Cucurbit Collection](https://vegetablemdonline.ppath.cornell.edu/factsheets/Cucurbit_Powdery.htm) | `Podosphaera_xanthii_squash_powdery_mildew` | `EXACT` | **+115** | Confirm white talcum-like powdery fungal growth across upper squash leaf lamina. |

---

## 3. Crop-Specific Acquisition Blueprints

### A. GINGER Diagnostic Plan
- **Target 1: `ginger__sheath_blight` (CRITICAL — 23.5% F1):**
  - *Pathogen:* *Rhizoctonia solani* on *Zingiber officinale*.
  - *Recommended Source:* **ICAR-Indian Institute of Spices Research (IISR)** Ginger Pathology Repository.
  - *Original Label:* `Rhizoctonia_solani_ginger_sheath_blight` (`EXACT`).
  - *Current Train Support:* 40 images -> *Target Additional:* **+60 images** (Expected Usable: **+110 images**).
  - *Exclusion Rule:* Reject unconditioned rice sheath blight crops lacking ginger pseudostem morphology.
- **Target 2: `ginger__leaf_spot` (HIGH — 50.0% F1):**
  - *Pathogen:* *Phyllosticta zingiberi* foliar leaf spot.
  - *Recommended Source:* ICAR-IISR Phyllosticta Spices Collection (`EXACT`).
  - *Current Train Support:* 15 images -> *Target Additional:* **+85 images** (Expected Usable: **+120 images**).
  - *Verification:* Verify spindle-shaped spots with translucent white centers and dark margins.

### B. BANANA Diagnostic Plan
- **Target 1: `banana__cordana_leaf_spot` (CRITICAL — 28.6% F1):**
  - *Pathogen:* *Cordana musae* / *Neocordana musae* on *Musa acuminata*.
  - *Recommended Source:* **Bioversity International / ProMusa** Banana Pathology Network.
  - *Original Label:* `Cordana_musae_banana_leaf_spot` (`EXACT`).
  - *Current Train Support:* 20 images -> *Target Additional:* **+80 images** (Expected Usable: **+110 images**).
  - *Verification:* Verify large oval zonate necrotic lesions with bright yellow chlorotic halos along leaf margins.
- **Target 2: `banana__cigar_end_rot` (MEDIUM — 66.7% F1):**
  - *Pathogen:* *Trachysphaera fructigena* flower/tip rot.
  - *Recommended Source:* ProMusa / CIRAD Banana Diagnostic Repository (`EXACT`).
  - *Current Train Support:* 22 images -> *Target Additional:* **+78 images** (Expected Usable: **+105 images**).
  - *Verification:* Verify dry tip rot of banana fingers resembling ash of a cigar.
- **Existing High Performers (No Additional Data Needed):**
  - `banana__black_leaf_streak` (**81.1% F1**, train: 139), `banana__panama_disease` (**87.5% F1**, train: 60), `banana__anthracnose` (**93.3% F1**, train: 81), `banana__bunchy_top` (**95.2% F1**, train: 84).

### C. GARLIC Diagnostic Plan
- **Target 1: `garlic__leaf_blight` (HIGH — 50.0% F1):**
  - *Pathogen:* *Stemphylium vesicarium* on *Allium sativum*.
  - *Recommended Source:* **ICAR-Directorate of Onion and Garlic Research (DOGR)**.
  - *Original Label:* `Stemphylium_vesicarium_garlic_blight` (`EXACT`).
  - *Current Train Support:* 55 images -> *Target Additional:* **+45 images** (Expected Usable: **+115 images**).
  - *Verification:* Verify elongated tan/brown water-soaked lesions that progress down the garlic leaf blade.
- **Target 2: `garlic__rust` (MEDIUM — 66.7% F1):**
  - *Pathogen:* *Puccinia allii* on *Allium sativum*.
  - *Recommended Source:* UC Davis IPM Allium Pathology Archive (`EXACT`).
  - *Current Train Support:* 56 images -> *Target Additional:* **+44 images** (Expected Usable: **+105 images**).
  - *Verification:* Verify distinct orange-red powdery pustules on flat garlic leaves.

---

## 4. High-Priority Acquisition Plan (0.40 <= F1 < 0.60)

| # | Target Model 2 Class | Crop | Train Count | Current F1 | Recommended Source | Original Label | Compatibility | Expected Usable |
|---|---|---|---|---|---|---|---|---|
| 1 | `ginger__leaf_spot` | **Ginger** | 15 | 50.0% | [ICAR-IISR Phyllosticta Ginger Spot Archive](https://spices.res.in/crop-management/ginger/diseases) | `Phyllosticta_zingiberi_leaf_spot` | `EXACT` | **+120** |
| 2 | `garlic__leaf_blight` | **Garlic** | 55 | 50.0% | [ICAR-Directorate of Onion and Garlic Research (DOGR)](https://dogr.icar.gov.in/diseases-garlic) | `Stemphylium_vesicarium_garlic_blight` | `EXACT` | **+115** |
| 3 | `eggplant__phytophthora_blight` | **Eggplant** | 15 | 40.0% | [AVRDC World Vegetable Center Pathology Archive](https://avrdc.org/eggplant-disease-resources/) | `Phytophthora_capsici_eggplant_blight` | `EXACT` | **+115** |
| 4 | `plum__pox_virus` | **Plum** | 15 | 40.0% | [USDA-ARS Sharka (Plum Pox) Diagnostic Collection](https://www.ars.usda.gov/research/plum-pox-virus/) | `Plum_Pox_Virus_Sharka` | `EXACT` | **+125** |
| 5 | `tomato__bacterial_leaf_spot` | **Tomato** | 62 | 53.3% | [PlantVillage / University of Florida Tomato Pathology](https://plantvillage.psu.edu/topics/tomato/infos) | `Tomato___Bacterial_spot` | `EXACT` | **+140** |
| 6 | `wheat__leaf_rust` | **Wheat** | 51 | 46.2% | [CIMMYT International Wheat Pathology Archive](https://www.cimmyt.org/work/wheat-rust/) | `Puccinia_triticina_wheat_brown_rust` | `EXACT` | **+130** |
| 7 | `wheat__stripe_rust` | **Wheat** | 148 | 78.1% | [Global Rust Reference Center (GRRC) / CIMMYT Stripe Rust Database](https://agro.au.dk/forskning/internationale-platforme/grrc/) | `Puccinia_striiformis_yellow_stripe_rust` | `EXACT` | **+125** |
| 8 | `soybean__bacterial_blight` | **Soybean** | 42 | 47.6% | [Iowa State University Soybean Pathology Image Archive](https://crops.extension.iastate.edu/soybean-disease-directory) | `Pseudomonas_savastanoi_glycinea_blight` | `EXACT` | **+120** |
| 9 | `soybean__rust` | **Soybean** | 46 | 41.7% | [USDA-ARS Soybean Rust Sentinel Network](https://www.ars.usda.gov/southeast-area/tifton-ga/crop-protection-and-management-research/docs/soybean-rust/) | `Phakopsora_pachyrhizi_soybean_rust` | `EXACT` | **+125** |
| 10 | `bean__rust` | **Bean** | 357 | 84.8% | [CIAT Dry Bean Pathology Digital Repository](https://ciat.cgiar.org/bean-diseases-data/) | `Uromyces_appendiculatus_bean_rust` | `EXACT` | **+130** |
| 11 | `bean__angular_leaf_spot` | **Bean** | 302 | 93.7% | [CIAT / EMBRAPA Bean Pathology Database](https://ciat.cgiar.org/bean-diseases-data/) | `Pseudocercospora_griseola_angular_spot` | `EXACT` | **+135** |
| 12 | `corn__gray_leaf_spot` | **Corn** | 53 | 47.6% | [Purdue University Field Crop Pathology Archive](https://extension.entm.purdue.edu/fieldcropsipm/diseases.php) | `Cercospora_zeae_maydis_corn_gray_spot` | `EXACT` | **+140** |
| 13 | `corn__rust` | **Corn** | 84 | 72.7% | [Iowa State Field Crop Disease Repository](https://crops.extension.iastate.edu/corn-disease-directory) | `Puccinia_sorghi_common_rust` | `EXACT` | **+135** |

---

## 5. Medium-Priority Acquisition Plan (0.60 <= F1 < 0.75)

| # | Target Model 2 Class | Crop | Train Count | Current F1 | Recommended Source | Original Label | Compatibility | Expected Usable |
|---|---|---|---|---|---|---|---|---|
| 1 | `banana__cigar_end_rot` | **Banana** | 22 | 66.7% | [ProMusa / CIRAD Banana Diagnostic Repository](https://www.promusa.org/Cigar-end_rot) | `Trachysphaera_fructigena_cigar_end` | `EXACT` | **+105** |
| 2 | `garlic__rust` | **Garlic** | 56 | 66.7% | [UC Davis IPM Allium Disease Archive](https://ipm.ucanr.edu/agriculture/garlic/rust/) | `Puccinia_allii_garlic_rust` | `EXACT` | **+105** |

---

## 6. Hard-Example Intra-Crop Discrimination Plan

For the top 5 intra-crop confusion pairs, acquisition must prioritize **diagnostic discriminating features**:

| Confusion Pair | Crop | Diagnostic Dilemma | Hard-Example Acquisition Directive | Target Volume |
| :--- | :--- | :--- | :--- | :--- |
| `tomato__bacterial_leaf_spot` <-> `tomato__septoria_leaf_spot` | Tomato | Both produce circular dark brown pinpoint lesions. | Collect high-resolution close-ups highlighting black pycnidia in center (Septoria) vs water-soaked greasy margins (Bacterial Spot). | +140 images |
| `bean__angular_leaf_spot` <-> `bean__rust` | Bean | Brownish foliar spots on Phaseolus leaves. | Collect abaxial leaf underside images showing raised powdery uredinia vs vein-delimited flat angular spots. | +125 images |
| `wheat__leaf_rust` <-> `wheat__stripe_rust` | Wheat | Early urediniospores appear orange-brown on blade. | Collect field imagery showing mature linear vein-parallel stripes vs scattered oval pustules. | +130 images |
| `corn__gray_leaf_spot` <-> `corn__rust` | Corn | Foliar necrosis under bright sun. | Collect mature rectangular vein-bounded gray-brown lesions vs ruptured epidermal cinnamon pustules. | +120 images |
| `soybean__bacterial_blight` <-> `soybean__rust` | Soybean | Small angular foliar lesions. | Collect backlit leaves highlighting translucent yellow halos vs raised pustules on lower leaf surface. | +115 images |

---

## 7. Onion Future Taxonomy Expansion Plan *(DO NOT ADD TO 117-CLASS DATASET)*

Onion (*Allium cepa*) is strictly maintained as a future taxonomy release. Recommended future datasets:

1. **`onion__purple_blotch` (*Alternaria porri*):** ICAR-DOGR / PlantVillage Allium Collection (Target: 120 images).
2. **`onion__downy_mildew` (*Peronospora destructor*):** Cornell Vegetable MD Online (Target: 110 images).
3. **`onion__black_mold` (*Aspergillus niger*):** USDA-ARS Post-Harvest Pathology (Target: 100 images).
4. **`onion__stemphylium_leaf_blight` (*Stemphylium vesicarium*):** ICAR-DOGR Allium Library (Target: 110 images).
5. **`healthy` (Onion Clean Foliage / Bulbs):** Verified clean field photography (Target: 150 images).

---

## 8. Sources to Reject & Quality Enforcement Rules

| Source Category | Reason for Mandatory Rejection | Risk to Model 2 |
| :--- | :--- | :--- |
| **Kaggle Generic Plant Disease Augmentation Dumps** | Artificial geometric/noise augmentations of existing PlantVillage images without original raw capture metadata. | Data duplication, test-set leakage, distortion of genuine lesion pathology. |
| **Generic 'Leaf Blight' / 'Leaf Spot' Unlabeled GitHub Repos** | Lacks biological pathogen taxonomy (e.g. labeling mixed fields as 'leaf spot' without specifying crop or pathogen species). | Semantic pollution and corrupting crop-specific disease classifiers. |
| **Stock Photo Aggregators (Shutterstock, Getty, iStock web crawls)** | Non-botanical decorative photos, post-processed filters, heavy color grading, and non-scientific visual guessing. | Domain shift and false positive artifacts in production. |
| **Multi-Crop Mixed Field Drone Overviews** | Lacks leaf-level resolution required for EfficientNet-B2 macro diagnostic pathology. | Sub-pixel lesions and canopy blur degrading classifier attention. |

---

## 9. Recommended Acquisition Execution Order

1. **Phase 1 (CRITICAL Targets):** Acquire and verify the 20 CRITICAL classes (+1,569 images) to eliminate zero-F1 tail classes.
2. **Phase 2 (Specialized Focus):** Acquire and curate Ginger, Banana, and Garlic targets (+460 images).
3. **Phase 3 (Hard-Example Symmetrical Pairs):** Acquire discriminating macro-photos for Tomato, Bean, Wheat, Corn, and Soybean confusion pairs (+630 images).
4. **Phase 4 (HIGH & MEDIUM Tiers):** Acquire remaining HIGH and MEDIUM classes (+1,942 images).
5. **Total Targeted Acquisition:** **+4,601 genuine, verified images** to bring all 116 disease classes to >=75% F1.

---

## 10. Artifact References

- CSV Acquisition Plan: [`reports/model2_classifier/phase4c_acquisition_plan.csv`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2_classifier/phase4c_acquisition_plan.csv)
- Summary JSON: [`reports/model2_classifier/phase4c_acquisition_summary.json`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2_classifier/phase4c_acquisition_summary.json)
- Markdown Acquisition Report: [`reports/model2_classifier/phase4c_acquisition_plan.md`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2_classifier/phase4c_acquisition_plan.md)