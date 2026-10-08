# Model 2 Disease Classifier: Targeted Supplementary Dataset Collection Manifest

**Date:** 2026-10-07  
**Module:** Model 2 EfficientNet-B2 Supplementary Collection Strategy  
**Baseline Performance:** Top-1 Accuracy: **84.29%**, Top-3: **94.57%**, Macro F1: **61.01%**, Healthy F1: **99.24%**  
**Data Policy:** Strictly genuine, real-world, unblemished/diseased plant photography (No synthetic data, no artificial duplication).  

---

## 1. Executive Summary & Collection Quotas

```
TOTAL DISEASE CLASSES IN TAXONOMY   : 116 disease classes
CRITICAL PRIORITY CLASSES (F1 < 0.40): 20 classes (+1,569 images)
HIGH PRIORITY CLASSES (0.40 <= F1 < 0.60): 29 classes (+1,807 images)
MEDIUM PRIORITY CLASSES (0.60 <= F1 < 0.75): 21 classes (+1,225 images)
LOW PRIORITY CLASSES (F1 >= 0.75)   : 46 classes (Fully sufficient; 0 images required)
TOTAL ADDITIONAL IMAGES RECOMMENDED : +4,601 genuine field/leaf images
```

---

## 2. CRITICAL Priority Tier (Test F1 < 0.40) — Target: 100 Train Images

These 20 classes suffer from severe data scarcity (<25 training images) or high confusion, leading to low test recall. Expanding these classes to 100 images will yield the largest gain in macro F1.

| # | Class Name | Crop | Train | Val | Test | Precision | Recall | Test F1 | Target Train | Additional Needed |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `bell_pepper__frogeye_leaf_spot` | **Bell Pepper** | 16 | 3 | 4 | 0.0% | 0.0% | **0.0%** | 100 | **+84** |
| 2 | `broccoli__ring_spot` | **Broccoli** | 5 | 1 | 1 | 0.0% | 0.0% | **0.0%** | 100 | **+95** |
| 3 | `cauliflower__alternaria_leaf_spot` | **Cauliflower** | 19 | 4 | 4 | 0.0% | 0.0% | **0.0%** | 100 | **+81** |
| 4 | `cauliflower__bacterial_soft_rot` | **Cauliflower** | 13 | 3 | 2 | 0.0% | 0.0% | **0.0%** | 100 | **+87** |
| 5 | `cherry__powdery_mildew` | **Cherry** | 18 | 4 | 3 | 0.0% | 0.0% | **0.0%** | 100 | **+82** |
| 6 | `coffee__black_rot` | **Coffee** | 2 | 1 | 0 | 0.0% | 0.0% | **0.0%** | 100 | **+98** |
| 7 | `coffee__brown_eye_spot` | **Coffee** | 8 | 2 | 1 | 0.0% | 0.0% | **0.0%** | 100 | **+92** |
| 8 | `peach__rust` | **Peach** | 3 | 1 | 1 | 0.0% | 0.0% | **0.0%** | 100 | **+97** |
| 9 | `plum__bacterial_spot` | **Plum** | 7 | 2 | 1 | 0.0% | 0.0% | **0.0%** | 100 | **+93** |
| 10 | `plum__rust` | **Plum** | 12 | 3 | 2 | 0.0% | 0.0% | **0.0%** | 100 | **+88** |
| 11 | `raspberry__leaf_spot` | **Raspberry** | 8 | 2 | 1 | 0.0% | 0.0% | **0.0%** | 100 | **+92** |
| 12 | `cabbage__alternaria_leaf_spot` | **Cabbage** | 25 | 5 | 6 | 14.3% | 16.7% | **15.4%** | 100 | **+75** |
| 13 | `plum__pocket_disease` | **Plum** | 20 | 4 | 4 | 20.0% | 25.0% | **22.2%** | 100 | **+80** |
| 14 | `tobacco__frogeye_leaf_spot` | **Tobacco** | 10 | 2 | 3 | 16.7% | 33.3% | **22.2%** | 100 | **+90** |
| 15 | `ginger__sheath_blight` | **Ginger** | 40 | 9 | 8 | 22.2% | 25.0% | **23.5%** | 100 | **+60** |
| 16 | `bean__mosaic_virus` | **Bean** | 23 | 5 | 5 | 20.0% | 40.0% | **26.7%** | 100 | **+77** |
| 17 | `banana__cordana_leaf_spot` | **Banana** | 20 | 4 | 4 | 33.3% | 25.0% | **28.6%** | 100 | **+80** |
| 18 | `zucchini__downy_mildew` | **Zucchini** | 22 | 5 | 5 | 100.0% | 20.0% | **33.3%** | 100 | **+78** |
| 19 | `tomato__septoria_leaf_spot` | **Tomato** | 64 | 14 | 14 | 33.3% | 35.7% | **34.5%** | 100 | **+36** |
| 20 | `squash__powdery_mildew` | **Squash** | 96 | 21 | 20 | 41.2% | 35.0% | **37.8%** | 100 | **+4** |

---

## 3. HIGH Priority Tier (0.40 ≤ Test F1 < 0.60) — Target: 100 Train Images

These 29 classes exhibit moderate baseline signal (40–59% F1). Expanding to 100 authentic images will stabilize intra-class variation and eliminate borderline misclassifications.

| # | Class Name | Crop | Train | Val | Test | Precision | Recall | Test F1 | Target Train | Additional Needed |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `eggplant__phytophthora_blight` | **Eggplant** | 15 | 3 | 4 | 100.0% | 25.0% | **40.0%** | 100 | **+85** |
| 2 | `plum__pox_virus` | **Plum** | 15 | 3 | 4 | 100.0% | 25.0% | **40.0%** | 100 | **+85** |
| 3 | `soybean__brown_spot` | **Soybean** | 33 | 7 | 7 | 66.7% | 28.6% | **40.0%** | 100 | **+67** |
| 4 | `tomato__mosaic_virus` | **Tomato** | 30 | 6 | 7 | 66.7% | 28.6% | **40.0%** | 100 | **+70** |
| 5 | `bean__halo_blight` | **Bean** | 24 | 5 | 6 | 50.0% | 33.3% | **40.0%** | 100 | **+76** |
| 6 | `carrot__cercospora_leaf_blight` | **Carrot** | 11 | 2 | 3 | 50.0% | 33.3% | **40.0%** | 100 | **+89** |
| 7 | `zucchini__powdery_mildew` | **Zucchini** | 87 | 19 | 18 | 41.2% | 38.9% | **40.0%** | 100 | **+13** |
| 8 | `soybean__rust` | **Soybean** | 46 | 10 | 9 | 33.3% | 55.6% | **41.7%** | 100 | **+54** |
| 9 | `eggplant__cercospora_leaf_spot` | **Eggplant** | 25 | 5 | 6 | 66.7% | 33.3% | **44.4%** | 100 | **+75** |
| 10 | `celery__early_blight` | **Celery** | 20 | 4 | 5 | 50.0% | 40.0% | **44.4%** | 100 | **+80** |
| 11 | `rice__sheath_blight` | **Rice** | 36 | 8 | 8 | 35.7% | 62.5% | **45.5%** | 100 | **+64** |
| 12 | `wheat__leaf_rust` | **Wheat** | 51 | 11 | 11 | 40.0% | 54.5% | **46.2%** | 100 | **+49** |
| 13 | `corn__gray_leaf_spot` | **Corn** | 53 | 11 | 12 | 55.6% | 41.7% | **47.6%** | 100 | **+47** |
| 14 | `soybean__bacterial_blight` | **Soybean** | 42 | 9 | 9 | 41.7% | 55.6% | **47.6%** | 100 | **+58** |
| 15 | `apple__black_rot` | **Apple** | 44 | 9 | 10 | 66.7% | 40.0% | **50.0%** | 100 | **+56** |
| 16 | `rice__blast` | **Rice** | 35 | 8 | 7 | 60.0% | 42.9% | **50.0%** | 100 | **+65** |
| 17 | `cabbage__downy_mildew` | **Cabbage** | 34 | 7 | 8 | 50.0% | 50.0% | **50.0%** | 100 | **+66** |
| 18 | `ginger__leaf_spot` | **Ginger** | 15 | 3 | 4 | 50.0% | 50.0% | **50.0%** | 100 | **+85** |
| 19 | `lettuce__mosaic_virus` | **Lettuce** | 15 | 3 | 4 | 50.0% | 50.0% | **50.0%** | 100 | **+85** |
| 20 | `raspberry__fire_blight` | **Raspberry** | 16 | 3 | 4 | 50.0% | 50.0% | **50.0%** | 100 | **+84** |
| 21 | `garlic__leaf_blight` | **Garlic** | 55 | 12 | 12 | 43.8% | 58.3% | **50.0%** | 100 | **+45** |
| 22 | `tomato__bacterial_leaf_spot` | **Tomato** | 62 | 13 | 13 | 47.1% | 61.5% | **53.3%** | 100 | **+38** |
| 23 | `soybean__mosaic` | **Soybean** | 62 | 13 | 13 | 53.8% | 53.8% | **53.8%** | 100 | **+38** |
| 24 | `wheat__bacterial_leaf_streak_(black_chaff)` | **Wheat** | 57 | 12 | 13 | 53.8% | 53.8% | **53.8%** | 100 | **+43** |
| 25 | `blueberry__rust` | **Blueberry** | 23 | 5 | 5 | 50.0% | 60.0% | **54.5%** | 100 | **+77** |
| 26 | `wheat__septoria_blotch` | **Wheat** | 86 | 18 | 19 | 52.4% | 57.9% | **55.0%** | 100 | **+14** |
| 27 | `broccoli__downy_mildew` | **Broccoli** | 16 | 3 | 4 | 66.7% | 50.0% | **57.1%** | 100 | **+84** |
| 28 | `zucchini__bacterial_wilt` | **Zucchini** | 39 | 8 | 9 | 50.0% | 66.7% | **57.1%** | 100 | **+61** |
| 29 | `grape__leaf_spot` | **Grape** | 46 | 10 | 10 | 71.4% | 50.0% | **58.8%** | 100 | **+54** |

---

## 4. MEDIUM Priority Tier (0.60 ≤ Test F1 < 0.75) — Target: 100 Train Images

These 21 classes perform solidly (60–74% F1). Supplementary collection brings them to the benchmark tier (≥75% F1).

| # | Class Name | Crop | Train | Val | Test | Precision | Recall | Test F1 | Target Train | Additional Needed |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `bell_pepper__bacterial_spot` | **Bell Pepper** | 33 | 7 | 7 | 100.0% | 42.9% | **60.0%** | 100 | **+67** |
| 2 | `blueberry__scorch` | **Blueberry** | 22 | 5 | 5 | 60.0% | 60.0% | **60.0%** | 100 | **+78** |
| 3 | `eggplant__phomopsis_fruit_rot` | **Eggplant** | 22 | 5 | 5 | 60.0% | 60.0% | **60.0%** | 100 | **+78** |
| 4 | `tobacco__mosaic_virus` | **Tobacco** | 20 | 4 | 5 | 60.0% | 60.0% | **60.0%** | 100 | **+80** |
| 5 | `broccoli__alternaria_leaf_spot` | **Broccoli** | 37 | 8 | 8 | 80.0% | 50.0% | **61.5%** | 100 | **+63** |
| 6 | `cherry__leaf_spot` | **Cherry** | 46 | 10 | 10 | 100.0% | 50.0% | **66.7%** | 100 | **+54** |
| 7 | `wheat__powdery_mildew` | **Wheat** | 122 | 26 | 27 | 83.3% | 55.6% | **66.7%** | 142 | **+20** |
| 8 | `apple__scab` | **Apple** | 116 | 25 | 25 | 75.0% | 60.0% | **66.7%** | 136 | **+20** |
| 9 | `basil__downy_mildew` | **Basil** | 29 | 6 | 6 | 66.7% | 66.7% | **66.7%** | 100 | **+71** |
| 10 | `banana__cigar_end_rot` | **Banana** | 22 | 5 | 4 | 60.0% | 75.0% | **66.7%** | 100 | **+78** |
| 11 | `blueberry__anthracnose` | **Blueberry** | 18 | 4 | 4 | 60.0% | 75.0% | **66.7%** | 100 | **+82** |
| 12 | `garlic__rust` | **Garlic** | 56 | 12 | 12 | 60.0% | 75.0% | **66.7%** | 100 | **+44** |
| 13 | `tobacco__blue_mold` | **Tobacco** | 24 | 5 | 5 | 57.1% | 80.0% | **66.7%** | 100 | **+76** |
| 14 | `celery__anthracnose` | **Celery** | 8 | 2 | 1 | 50.0% | 100.0% | **66.7%** | 100 | **+92** |
| 15 | `peach__anthracnose` | **Peach** | 7 | 2 | 1 | 50.0% | 100.0% | **66.7%** | 100 | **+93** |
| 16 | `cucumber__powdery_mildew` | **Cucumber** | 106 | 23 | 22 | 63.0% | 77.3% | **69.4%** | 126 | **+20** |
| 17 | `tomato__yellow_leaf_curl_virus` | **Tomato** | 41 | 9 | 9 | 75.0% | 66.7% | **70.6%** | 100 | **+59** |
| 18 | `apple__rust` | **Apple** | 69 | 15 | 14 | 81.8% | 64.3% | **72.0%** | 100 | **+31** |
| 19 | `corn__rust` | **Corn** | 84 | 18 | 18 | 80.0% | 66.7% | **72.7%** | 100 | **+16** |
| 20 | `apple__mosaic_virus` | **Apple** | 51 | 11 | 11 | 72.7% | 72.7% | **72.7%** | 100 | **+49** |
| 21 | `potato__early_blight` | **Potato** | 46 | 10 | 10 | 77.8% | 70.0% | **73.7%** | 100 | **+54** |

---

## 5. Crop-Specific Analysis & Targeted Directives

### A. GINGER Diagnostic Requirements

| Class Name | Train | Test | Precision | Recall | Test F1 | Priority | Actionable Directive |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ginger__sheath_blight` | 40 | 8 | 22.2% | 25.0% | **23.5%** | `CRITICAL` | **CRITICAL (23.5% F1):** Severe confusion with rice sheath blight. Collect +60 genuine ginger pseudostem/sheath lesion images. |
| `ginger__leaf_spot` | 15 | 4 | 50.0% | 50.0% | **50.0%** | `HIGH` | **HIGH (50.0% F1):** Moderate foliar spot identification. Collect +85 genuine ginger leaf spot images to reach 100. |

### B. BANANA Diagnostic Requirements

| Class Name | Train | Test | Precision | Recall | Test F1 | Priority | Actionable Directive |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `banana__cordana_leaf_spot` | 20 | 4 | 33.3% | 25.0% | **28.6%** | `CRITICAL` | **CRITICAL (28.6% F1):** Confused with Black Leaf Streak. Collect +80 oval zonate leaf spot images with bright yellow halos. |
| `banana__cigar_end_rot` | 22 | 4 | 60.0% | 75.0% | **66.7%** | `MEDIUM` | **MEDIUM (66.7% F1):** Tip rot symptom. Collect +78 genuine banana fruit/tip rot images. |
| `banana__black_leaf_streak` | 76 | 17 | 75.0% | 88.2% | **81.1%** | `LOW` | **LOW (81.1% F1):** Black Sigatoka / Black Leaf Streak is well represented. No mandatory collection. |
| `banana__panama_disease` | 34 | 8 | 87.5% | 87.5% | **87.5%** | `LOW` | **LOW (87.5% F1):** Vascular wilt foliar yellowing is well distinguished. No mandatory collection. |
| `banana__anthracnose` | 34 | 7 | 87.5% | 100.0% | **93.3%** | `LOW` | **LOW (93.3% F1):** Diamond-shaped necrotic lesions are well identified. No mandatory collection. |
| `banana__bunchy_top` | 50 | 11 | 100.0% | 90.9% | **95.2%** | `LOW` | **LOW (95.2% F1):** Stunted rosette growth habit is well identified. No mandatory collection. |

### C. GARLIC Diagnostic Requirements

| Class Name | Train | Test | Precision | Recall | Test F1 | Priority | Actionable Directive |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `garlic__leaf_blight` | 55 | 12 | 43.8% | 58.3% | **50.0%** | `HIGH` | **HIGH (50.0% F1):** Garlic leaf blight has moderate recall (58.3%). Collect +45 images to reach 100. |
| `garlic__rust` | 56 | 12 | 60.0% | 75.0% | **66.7%** | `MEDIUM` | **MEDIUM (66.7% F1):** Garlic rust pustules perform moderately. Collect +44 images to reach 100. |

### D. ONION Future Taxonomy Expansion (DO NOT ADD TO CURRENT 117-CLASS DATASET)

Onion is not part of the active 117-class Model 2 deployment. When ready to expand the model taxonomy, collect the following classes:

| Proposed Class Name | Pathogen / Condition | Target Image Volume | Expansion Priority |
| :--- | :--- | :--- | :--- |
| `onion__purple_blotch` | Purple Blotch (Alternaria porri) | 100 images | `HIGH_FUTURE` |
| `onion__downy_mildew` | Downy Mildew (Peronospora destructor) | 100 images | `HIGH_FUTURE` |
| `onion__black_mold` | Black Mold (Aspergillus niger) | 100 images | `MEDIUM_FUTURE` |
| `onion__stemphylium_leaf_blight` | Stemphylium Leaf Blight (Stemphylium vesicarium) | 100 images | `HIGH_FUTURE` |
| `onion__bacterial_soft_rot` | Bacterial Soft Rot (Pectobacterium carotovorum) | 80 images | `MEDIUM_FUTURE` |
| `healthy` | Onion Clean Foliage / Bulbs | 150 images | `MANDATORY_FUTURE` |

---

## 6. Hard-Example Intra-Crop Confusion Collection Directives

Rather than gathering random images, collection for these 5 high-confusion intra-crop pairs must prioritize **diagnostic discriminating features**:

### 1. Tomato Bacterial Leaf Spot ↔ Tomato Septoria Leaf Spot (Tomato)
- **Observed Mutual Errors:** 8 test instances
- **Diagnostic Ambiguity:** Both produce small, pinpoint circular dark necrotic lesions with yellow halos on tomato foliage.
- **Targeted Collection Directive:** Collect high-resolution macro-photography capturing mature lesions with pycnidia (black dots in center for Septoria) vs water-soaked angular borders (Bacterial Spot).

### 2. Bean Angular Leaf Spot ↔ Bean Rust (Bean)
- **Observed Mutual Errors:** 8 test instances
- **Diagnostic Ambiguity:** Both present as angular or circular reddish-brown necrotic spots across Phaseolus foliage.
- **Targeted Collection Directive:** Collect distinct underside foliar imagery emphasizing raised powdery rust urediniospores vs vein-delimited angular necrotic patches.

### 3. Wheat Leaf Rust ↔ Wheat Stripe Rust (Wheat)
- **Observed Mutual Errors:** 6 test instances
- **Diagnostic Ambiguity:** Early stage uredinial pustules exhibit overlapping orange-brown discoloration before distinct striping occurs.
- **Targeted Collection Directive:** Collect field images showing elongated linear stripe patterns along leaf veins (Stripe Rust) vs randomly scattered oval pustules (Leaf Rust).

### 4. Corn Gray Leaf Spot ↔ Corn Rust (Corn)
- **Observed Mutual Errors:** 4 test instances
- **Diagnostic Ambiguity:** Lesions on maize foliage can appear similar in early stages under bright outdoor lighting.
- **Targeted Collection Directive:** Collect mature rectangular vein-bounded gray-brown lesions (Gray Leaf Spot) vs raised cinnamon-brown pustules that rupture epidermal tissue (Rust).

### 5. Soybean Bacterial Blight ↔ Soybean Rust (Soybean)
- **Observed Mutual Errors:** 4 test instances
- **Diagnostic Ambiguity:** Small angular brown lesions on Glycine max leaves overlap visually in low contrast frames.
- **Targeted Collection Directive:** Collect backlit leaves highlighting translucent yellow water-soaked halos (Bacterial Blight) vs abaxial surface raised pustules (Soybean Rust).

---

## 7. Artifact References

- CSV Manifest: [`reports/model2_classifier/supplementary_collection_manifest.csv`](file:///reports/model2_classifier/supplementary_collection_manifest.csv)
- Summary JSON: [`reports/model2_classifier/supplementary_collection_summary.json`](file:///reports/model2_classifier/supplementary_collection_summary.json)
- Markdown Manifest Report: [`reports/model2_classifier/supplementary_collection_manifest.md`](file:///reports/model2_classifier/supplementary_collection_manifest.md)