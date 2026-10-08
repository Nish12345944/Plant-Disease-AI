# EXPANDED MODEL 1 CROP TAXONOMY ARCHITECTURE

**Date:** 2026-10-08  
**Status:** Approved for Taxonomy Architecture (Pre-Training Phase)  
**Baseline Model 1:** 22 Classes (Top-1: 97.84%, Macro F1: 92.91%)  
**Target Model 1:** 46 Classes (+24 New Classes, 4 Aliases Formalized)  
**Reachable Disease Coverage:** 116 / 116 Model 2 V4 Disease Classes (100.0%)  

---

## 1. Executive Summary

This document specifies the complete **46-class target taxonomy** for the future expanded Model 1 crop classifier. Expanding Model 1 from 22 classes to 46 classes eliminates the architectural bottleneck preventing Model 2 V4's full 116-disease pathology from being diagnosed through the visual inference pipeline.

### Taxonomy Summary Statistics:
- **Current Model 1 Classes:** **22**
- **Proposed New Classes:** **24**
- **Proposed Semantic / Cultivar Aliases:** **4**
- **Excluded Crops:** **1** (`turnip` - 0 diseases in V4)
- **Proposed Final Model 1 Class Count:** **46**
- **Disease Classes Newly Reachable:** **82** (81 from 24 new crops + 1 from squash alias)
- **Total End-to-End Reachable Diseases:** **116 / 116** (100.0%)
- **Verified Knowledge Base Coverage:** **116 / 116** (100.0% HIGH-quality records)

---

## 2. In-Depth Alias & Botanical vs Visual Taxonomy Analysis

The relationship between crops, botanical classifications, and computer vision classification was rigorously audited across seven core cases:

### Case 1: `french_bean` vs `bean`
- **Biological Taxon:** *Phaseolus vulgaris* (common bean / French bean / green bean).
- **Botanical vs Visual Reality:** Both terms describe the exact same plant species. Model 1's dataset was constructed from the Hugging Face `beans` dataset, and Model 2's dataset was constructed from Makerere University's bean dataset—which are the exact same images. Foliage features identical trifoliate, cordate-deltoid leaflets.
- **Decision:** **SAME CROP / SEMANTIC ALIAS**.
- **Architectural Action:** Retain `french_bean` in Model 1; map `french_bean` <-> `bean` in the compatibility router. All 4 Model 2 bean disease classes (`bean__angular_leaf_spot`, `bean__halo_blight`, `bean__mosaic_virus`, `bean__rust`) are fully inherited.

### Case 2: `capsicum` vs `bell_pepper`
- **Biological Taxon:** *Capsicum annuum* (sweet pepper / bell pepper / capsicum).
- **Botanical vs Visual Reality:** "Capsicum" is British/Commonwealth English; "bell pepper" is North American English. The plants are genetically and morphologically identical, featuring glabrous, ovate leaves and solitary pendant white flowers.
- **Decision:** **SAME CROP / SEMANTIC ALIAS**.
- **Architectural Action:** Retain `capsicum` in Model 1; map `capsicum` <-> `bell_pepper` in the compatibility router. All 4 Model 2 bell pepper disease classes (`bell_pepper__bacterial_spot`, `bell_pepper__blossom_end_rot`, `bell_pepper__frogeye_leaf_spot`, `bell_pepper__powdery_mildew`) are fully inherited.

### Case 3: `zucchini` vs `squash`
- **Biological Taxon:** Zucchini is *Cucurbita pepo* var. *cylindrica* (a summer squash morphotype); dataset "squash" refers to *Cucurbita pepo* / *Cucurbita moschata*.
- **Botanical vs Visual Reality:** Zucchini foliage possesses deep palmate lobing, stiff epidermal prickles, and characteristic silver-gray mottling. Generic summer squash foliage exhibits near-identical lobing, pubescence, and vein patterning. Distinguishing zucchini foliage from other summer squashes without mature fruit is unreliable for computer vision. Furthermore, Model 1's baseline already exhibits its lowest precision on `zucchini` (82.98% precision due to confusion with cucumber/melon). Creating a separate `squash` class would introduce massive mutual confusion.
- **Decision:** **CULTIVAR / VARIETY — SHOULD NOT BE SEPARATE VISUAL CLASSES**.
- **Architectural Action:** **MAP TO EXISTING MODEL 1 CLASS**. Model 1's `zucchini` class canonically covers zucchini and summer squashes. In the compatibility router, `zucchini` maps to both `zucchini` and `squash` diseases. This immediately activates `squash__powdery_mildew` without destabilizing Model 1.

### Case 4: `cherry_tomato` vs `tomato`
- **Biological Taxon:** *Solanum lycopersicum* var. *cerasiforme* (cherry tomato) vs *Solanum lycopersicum* (standard tomato).
- **Botanical vs Visual Reality:** Foliage structure (irregular pinnatifid/pinnatisect leaflets, glandular hairs, pungent aroma) is identical. Without miniature fruit in frame, foliage cannot be reliably separated. In Model 1's test evaluation, `cherry_tomato` had **0 test samples** (F1 0.00%). In Model 2, all 7 tomato diseases are cataloged strictly under `tomato__*`.
- **Decision:** **CULTIVAR / VARIETY — ALIASED TO CANONICAL TOMATO**.
- **Architectural Action:** Maintain `cherry_tomato` in Model 1 for backward compatibility or alias directly to `tomato`. The compatibility router aliases `cherry_tomato` -> `tomato`, granting access to all 7 tomato disease classes.

### Case 5: `cherry` vs Cherry Fruit/Tree Terminology
- **Biological Taxon:** *Prunus avium* (sweet cherry) / *Prunus cerasus* (sour cherry), Family Rosaceae.
- **Botanical vs Visual Reality:** `cherry` is a woody deciduous stone fruit tree, completely unrelated to `cherry_tomato` (a solanaceous herbaceous vine). Leaves are simple, alternate, elliptic-ovate, with serrate margins and conspicuous red nectariferous petiole glands.
- **Decision:** **DISTINCT WOODY TREE FRUIT CROP — NOT AN ALIAS**.
- **Architectural Action:** **ADD AS NEW MODEL 1 CLASS** (`cherry`). Activates `cherry__leaf_spot` and `cherry__powdery_mildew`.

### Case 6: `citrus` as a Crop Family
- **Biological Taxon:** Genus *Citrus* (Family Rutaceae), including sweet orange (*C. sinensis*), lemon (*C. limon*), lime (*C. aurantiifolia*), grapefruit (*C. paradisi*), and mandarin (*C. reticulata*).
- **Botanical vs Visual Reality:** Across citrus species, foliage shares distinctive morphological signatures: thick, leathery, dark glossy green leaves, pellucid oil glands, and winged or articulated petioles. Furthermore, key citrus pathogens (*Xanthomonas citri* causing canker, *Candidatus Liberibacter* causing greening/HLB) systematically infect multiple citrus species.
- **Decision:** **GENUS-LEVEL CROP CLASS (UNIFIED CITRUS FAMILY)**.
- **Architectural Action:** **ADD AS NEW MODEL 1 CLASS** (`citrus`). Activates `citrus__canker` and `citrus__greening_disease`.

### Case 7: `melon` vs Related Cucurbits
- **Biological Taxon:** `melon` (*Cucumis melo*) vs `cucumber` (*Cucumis sativus*) vs `zucchini` (*Cucurbita pepo*).
- **Botanical vs Visual Reality:**
  - `melon`: Leaves are rounded, suborbicular to reniform with shallow, rounded lobes and wavy margins.
  - `cucumber`: Leaves are sharply triangular-ovate with acute, angular lobes.
  - `zucchini`: Leaves are deeply palmate-dissected with harsh prickles and silvery mottling.
  - Despite belonging to Cucurbitaceae, their foliage morphologies are easily distinguishable by convolutional neural networks. In Model 1 baseline, `melon` achieved **100.00% precision and 100.00% recall**. Merging them would degrade proven discrimination.
- **Decision:** **BOTANICAL RELATIONSHIP BUT MUST REMAIN SEPARATE VISUAL CLASSES**.
- **Architectural Action:** Maintain `melon`, `cucumber`, and `zucchini` as separate classes in Model 1. Do not merge.

---

## 3. The Complete 46-Class Model 1 Target Taxonomy

| # | Canonical Name | Display Name | Model 2 Compatibility Mapping | Disease Count | Knowledge Base Coverage | Reason for Inclusion |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **`anthurium`** | Anthurium | `None (Healthy only in M2)` | **0** | No V4 diseases (Floriculture) | Retain baseline greenhouse ornamental class |
| 2 | **`blueberry`** | Blueberry | `blueberry` | **5** | 5/5 V4 records active | Retain baseline berry crop; 5 high-impact diseases |
| 3 | **`broccoli`** | Broccoli | `broccoli` | **3** | 3/3 V4 records active | Retain baseline brassica crop; 3 diseases |
| 4 | **`capsicum`** | Capsicum (Bell Pepper) | `bell_pepper, capsicum` | **4** | 4/4 V4 records active | Retain baseline solanaceous crop; aliased to bell_pepper |
| 5 | **`carnation`** | Carnation | `None (Healthy only in M2)` | **0** | No V4 diseases (Floriculture) | Retain baseline greenhouse ornamental class |
| 6 | **`cherry_tomato`** | Cherry Tomato | `tomato` | **7** | 7/7 V4 records active (via tomato) | Retain baseline cultivar class; aliased to tomato |
| 7 | **`chrysanthemum`** | Chrysanthemum | `None (Healthy only in M2)` | **0** | No V4 diseases (Floriculture) | Retain baseline greenhouse ornamental class |
| 8 | **`cucumber`** | Cucumber | `cucumber` | **3** | 3/3 V4 records active | Retain baseline cucurbit crop; 3 diseases |
| 9 | **`french_bean`** | French Bean (Common Bean) | `bean` | **4** | 4/4 V4 records active | Retain baseline legume crop; aliased to bean |
| 10 | **`geranium`** | Geranium | `None (Healthy only in M2)` | **0** | No V4 diseases (Floriculture) | Retain baseline greenhouse ornamental class |
| 11 | **`gerbera`** | Gerbera Daisy | `None (Healthy only in M2)` | **0** | No V4 diseases (Floriculture) | Retain baseline greenhouse ornamental class |
| 12 | **`gypsophila`** | Baby's Breath (Gypsophila) | `None (Healthy only in M2)` | **0** | No V4 diseases (Floriculture) | Retain baseline greenhouse ornamental class |
| 13 | **`lettuce`** | Lettuce | `lettuce` | **2** | 2/2 V4 records active | Retain baseline leafy salad crop; 2 diseases |
| 14 | **`lilium`** | Lily (Lilium) | `None (Healthy only in M2)` | **0** | No V4 diseases (Floriculture) | Retain baseline greenhouse ornamental class |
| 15 | **`marigold`** | Marigold | `marigold` | **0** | No V4 diseases (Healthy only) | Retain baseline floriculture/companion crop |
| 16 | **`melon`** | Melon | `None (Healthy only in M2)` | **0** | No V4 diseases (Cucurbit) | Retain baseline cucurbit crop (distinct from cucumber/zucchini) |
| 17 | **`orchid`** | Orchid | `None (Healthy only in M2)` | **0** | No V4 diseases (Floriculture) | Retain baseline greenhouse ornamental class |
| 18 | **`rose`** | Rose | `rose` | **0** | No V4 diseases (Healthy only) | Retain baseline ornamental woody shrub |
| 19 | **`spinach`** | Spinach | `spinach` | **0** | No V4 diseases (Healthy only) | Retain baseline leafy green crop |
| 20 | **`strawberry`** | Strawberry | `strawberry` | **2** | 2/2 V4 records active | Retain baseline berry crop; 2 diseases |
| 21 | **`tomato`** | Tomato | `tomato` | **7** | 7/7 V4 records active | Retain baseline solanaceous staple; 7 diseases |
| 22 | **`zucchini`** | Zucchini & Summer Squash | `zucchini, squash` | **5** | 5/5 V4 records active (4 zucchini + 1 squash) | Retain baseline cucurbit; encompasses squash powdery mildew |
| 23 | **`apple`** | Apple | `apple` | **4** | 4/4 V4 records active | New class: High-value pome fruit tree; activates 4 M2 diseases |
| 24 | **`banana`** | Banana | `banana` | **6** | 6/6 V4 records active | New class: Critical tropical fruit staple; activates 6 M2 diseases |
| 25 | **`basil`** | Basil | `basil` | **1** | 1/1 V4 records active | New class: High-value culinary herb; activates downy mildew |
| 26 | **`cabbage`** | Cabbage | `cabbage` | **3** | 3/3 V4 records active | New class: Major brassica head vegetable; activates 3 M2 diseases |
| 27 | **`carrot`** | Carrot | `carrot` | **3** | 3/3 V4 records active | New class: Major root vegetable; activates 3 M2 diseases |
| 28 | **`cauliflower`** | Cauliflower | `cauliflower` | **2** | 2/2 V4 records active | New class: Major brassica curd vegetable; activates 2 M2 diseases |
| 29 | **`celery`** | Celery | `celery` | **2** | 2/2 V4 records active | New class: Major petiole vegetable; activates 2 M2 diseases |
| 30 | **`cherry`** | Cherry | `cherry` | **2** | 2/2 V4 records active | New class: Stone fruit tree; activates 2 M2 diseases |
| 31 | **`citrus`** | Citrus (Orange, Lemon, Lime) | `citrus` | **2** | 2/2 V4 records active | New class: Subtropical fruit family; activates canker & greening |
| 32 | **`coffee`** | Coffee | `coffee` | **4** | 4/4 V4 records active | New class: Global commercial beverage crop; activates 4 M2 diseases |
| 33 | **`corn`** | Corn (Maize) | `corn` | **4** | 4/4 V4 records active | New class: Major global staple cereal; activates 4 M2 diseases |
| 34 | **`eggplant`** | Eggplant (Aubergine) | `eggplant` | **3** | 3/3 V4 records active | New class: Solanaceous fruit vegetable; activates 3 M2 diseases |
| 35 | **`garlic`** | Garlic | `garlic` | **2** | 2/2 V4 records active | New class: Allium bulb crop; activates leaf blight & rust |
| 36 | **`ginger`** | Ginger | `ginger` | **2** | 2/2 V4 records active | New class: Rhizome spice crop; activates leaf spot & sheath blight |
| 37 | **`grape`** | Grape (Grapevine) | `grape` | **4** | 4/4 V4 records active | New class: Viticulture woody vine; activates 4 M2 diseases |
| 38 | **`maple`** | Maple | `maple` | **1** | 1/1 V4 records active | New class: Landscape/shade tree; activates tar spot |
| 39 | **`peach`** | Peach | `peach` | **5** | 5/5 V4 records active | New class: Stone fruit tree; activates 5 M2 diseases |
| 40 | **`plum`** | Plum | `plum` | **5** | 5/5 V4 records active | New class: Stone fruit tree; activates 5 M2 diseases |
| 41 | **`potato`** | Potato | `potato` | **2** | 2/2 V4 records active | New class: Major staple food tuber; activates early & late blight |
| 42 | **`raspberry`** | Raspberry | `raspberry` | **4** | 4/4 V4 records active | New class: Cane fruit crop; activates 4 M2 diseases |
| 43 | **`rice`** | Rice | `rice` | **2** | 2/2 V4 records active | New class: Primary staple cereal; activates blast & sheath blight |
| 44 | **`soybean`** | Soybean | `soybean` | **6** | 6/6 V4 records active | New class: Major global oilseed legume; activates 6 M2 diseases |
| 45 | **`tobacco`** | Tobacco | `tobacco` | **4** | 4/4 V4 records active | New class: Solanaceous industrial crop; activates 4 M2 diseases |
| 46 | **`wheat`** | Wheat | `wheat` | **8** | 8/8 V4 records active | New class: Primary staple cereal (highest M2 disease count); activates 8 diseases |

---

## 4. End-to-End Pathology Reachability Master Table

The following table demonstrates that all **116 Model 2 V4 disease classes** become 100% reachable through the expanded 46-class Model 1 architecture:

| Model 1 Crop | Model 2 Compatible Disease Classes | KB Records Active | E2E Reachable? |
| :--- | :--- | :---: | :---: |
| **`apple`** | `apple__black_rot`, `apple__mosaic_virus`, `apple__rust`, `apple__scab` | 4 / 4 | **YES (Newly Enabled)** |
| **`banana`** | `banana__anthracnose`, `banana__black_leaf_streak`, `banana__bunchy_top`, `banana__cigar_end_rot`, `banana__cordana_leaf_spot`, `banana__panama_disease` | 6 / 6 | **YES (Newly Enabled)** |
| **`basil`** | `basil__downy_mildew` | 1 / 1 | **YES (Newly Enabled)** |
| **`blueberry`** | `blueberry__anthracnose`, `blueberry__botrytis_blight`, `blueberry__mummy_berry`, `blueberry__rust`, `blueberry__scorch` | 5 / 5 | **YES (Production Active)** |
| **`broccoli`** | `broccoli__alternaria_leaf_spot`, `broccoli__downy_mildew`, `broccoli__ring_spot` | 3 / 3 | **YES (Production Active)** |
| **`cabbage`** | `cabbage__alternaria_leaf_spot`, `cabbage__black_rot`, `cabbage__downy_mildew` | 3 / 3 | **YES (Newly Enabled)** |
| **`capsicum`** | `bell_pepper__bacterial_spot`, `bell_pepper__blossom_end_rot`, `bell_pepper__frogeye_leaf_spot`, `bell_pepper__powdery_mildew` | 4 / 4 | **YES (Production Active via Alias)** |
| **`carrot`** | `carrot__alternaria_leaf_blight`, `carrot__cavity_spot`, `carrot__cercospora_leaf_blight` | 3 / 3 | **YES (Newly Enabled)** |
| **`cauliflower`** | `cauliflower__alternaria_leaf_spot`, `cauliflower__bacterial_soft_rot` | 2 / 2 | **YES (Newly Enabled)** |
| **`celery`** | `celery__anthracnose`, `celery__early_blight` | 2 / 2 | **YES (Newly Enabled)** |
| **`cherry`** | `cherry__leaf_spot`, `cherry__powdery_mildew` | 2 / 2 | **YES (Newly Enabled)** |
| **`cherry_tomato`**| `tomato__*` (Inherits all 7 tomato classes via alias) | 7 / 7 | **YES (Production Active via Alias)** |
| **`citrus`** | `citrus__canker`, `citrus__greening_disease` | 2 / 2 | **YES (Newly Enabled)** |
| **`coffee`** | `coffee__berry_blotch`, `coffee__black_rot`, `coffee__brown_eye_spot`, `coffee__leaf_rust` | 4 / 4 | **YES (Newly Enabled)** |
| **`corn`** | `corn__gray_leaf_spot`, `corn__northern_leaf_blight`, `corn__rust`, `corn__smut` | 4 / 4 | **YES (Newly Enabled)** |
| **`cucumber`** | `cucumber__angular_leaf_spot`, `cucumber__bacterial_wilt`, `cucumber__powdery_mildew` | 3 / 3 | **YES (Production Active)** |
| **`eggplant`** | `eggplant__cercospora_leaf_spot`, `eggplant__phomopsis_fruit_rot`, `eggplant__phytophthora_blight` | 3 / 3 | **YES (Newly Enabled)** |
| **`french_bean`** | `bean__angular_leaf_spot`, `bean__halo_blight`, `bean__mosaic_virus`, `bean__rust` | 4 / 4 | **YES (Production Active via Alias)** |
| **`garlic`** | `garlic__leaf_blight`, `garlic__rust` | 2 / 2 | **YES (Newly Enabled)** |
| **`ginger`** | `ginger__leaf_spot`, `ginger__sheath_blight` | 2 / 2 | **YES (Newly Enabled)** |
| **`grape`** | `grape__black_rot`, `grape__downy_mildew`, `grape__grapevine_leafroll_disease`, `grape__leaf_spot` | 4 / 4 | **YES (Newly Enabled)** |
| **`lettuce`** | `lettuce__downy_mildew`, `lettuce__mosaic_virus` | 2 / 2 | **YES (Production Active)** |
| **`maple`** | `maple__tar_spot` | 1 / 1 | **YES (Newly Enabled)** |
| **`peach`** | `peach__anthracnose`, `peach__brown_rot`, `peach__leaf_curl`, `peach__rust`, `peach__scab` | 5 / 5 | **YES (Newly Enabled)** |
| **`plum`** | `plum__bacterial_spot`, `plum__brown_rot`, `plum__pocket_disease`, `plum__pox_virus`, `plum__rust` | 5 / 5 | **YES (Newly Enabled)** |
| **`potato`** | `potato__early_blight`, `potato__late_blight` | 2 / 2 | **YES (Newly Enabled)** |
| **`raspberry`** | `raspberry__fire_blight`, `raspberry__gray_mold`, `raspberry__leaf_spot`, `raspberry__yellow_rust` | 4 / 4 | **YES (Newly Enabled)** |
| **`rice`** | `rice__blast`, `rice__sheath_blight` | 2 / 2 | **YES (Newly Enabled)** |
| **`soybean`** | `soybean__bacterial_blight`, `soybean__brown_spot`, `soybean__downy_mildew`, `soybean__frog_eye_leaf_spot`, `soybean__mosaic`, `soybean__rust` | 6 / 6 | **YES (Newly Enabled)** |
| **`strawberry`** | `strawberry__anthracnose`, `strawberry__leaf_scorch` | 2 / 2 | **YES (Production Active)** |
| **`tobacco`** | `tobacco__blue_mold`, `tobacco__brown_spot`, `tobacco__frogeye_leaf_spot`, `tobacco__mosaic_virus` | 4 / 4 | **YES (Newly Enabled)** |
| **`tomato`** | `tomato__bacterial_leaf_spot`, `tomato__early_blight`, `tomato__late_blight`, `tomato__leaf_mold`, `tomato__mosaic_virus`, `tomato__septoria_leaf_spot`, `tomato__yellow_leaf_curl_virus` | 7 / 7 | **YES (Production Active)** |
| **`wheat`** | `wheat__bacterial_leaf_streak_(black_chaff)`, `wheat__head_scab`, `wheat__leaf_rust`, `wheat__loose_smut`, `wheat__powdery_mildew`, `wheat__septoria_blotch`, `wheat__stem_rust`, `wheat__stripe_rust` | 8 / 8 | **YES (Newly Enabled)** |
| **`zucchini`** | `zucchini__bacterial_wilt`, `zucchini__downy_mildew`, `zucchini__powdery_mildew`, `zucchini__yellow_mosaic_virus`, `squash__powdery_mildew` | 5 / 5 | **YES (Production Active + Squash Enabled)** |
| **Floriculture (10)** | *None (Healthy foliage identification only in V4)* | N/A | **YES (Healthy Classification)** |
| **TOTAL** | **116 Disease Classes + 1 Shared Healthy Class** | **116 / 116** | **100.0% FULL REACHABILITY** |

---

## 5. Architectural Implementation Directives

1. **Compatibility Router Alias Layer:** Formalize bidirectional aliasing in `knowledge/reasoning.py` and `app/backend/main.py`:
   ```python
   CROP_ALIASES = {
       "french_bean": "bean",
       "bean": "french_bean",
       "capsicum": "bell_pepper",
       "bell_pepper": "capsicum",
       "cherry_tomato": "tomato",
       "squash": "zucchini",
   }
   ```
2. **Model 1 Expansion Readiness:** The taxonomy is formally defined at 46 classes. Proceeding to dataset acquisition will enable training an EfficientNet-B2 classifier capable of routing to 100% of Model 2 V4 diseases.
