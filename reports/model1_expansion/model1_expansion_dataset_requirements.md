# MODEL 1 EXPANSION: DATASET SPECIFICATIONS & RISK AUDIT

**Date:** 2026-10-08  
**Scope:** Dataset Acquisition Specifications for 24 Proposed New Crop Classes & Impact Risk Analysis  
**Policy Reminder:** No dataset acquisition has been performed during this taxonomy-audit phase. All guidelines here govern the subsequent dataset build phase.  

---

## 1. Dataset Specifications for Proposed New Classes

The following specifications define the sample sizes, visual attributes, confounding species, and reuse feasibility for every proposed new Model 1 class:

| Proposed Crop | Min Train | Min Val | Min Test | Total Target | Visual Characteristics | Major Confounders | Classification Difficulty | Existing V4 Images Reusable? |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :--- |
| **`apple`** | 400 | 50 | 50 | **500** | Orchard field & controlled lighting; simple serrated leaves, shoot tips, fruit clusters; both healthy foliage and scab/rot lesions. | peach, plum, cherry, rose | **Medium** | Yes - 566 images in model2_v4 (456 train, 50 val, 60 test from plantseg) |
| **`banana`** | 400 | 50 | 50 | **500** | Tropical plantation field photos; large paddle leaves with prominent parallel veins, tearing, and bunching symptoms. | ginger (young stages), canna, heliconia | **Low** | Yes - 536 images in model2_v4 (436 train, 49 val, 51 test from plantseg) |
| **`basil`** | 250 | 35 | 35 | **320** | Potted herbs & greenhouse beds; smooth glossy opposite ovate leaves, square stems, downy mildew sporulation on undersides. | mint, oregano, young spinach | **Medium** | Yes - 63 images in model2_v4 (supplementary acquisition needed: +187 train images) |
| **`cabbage`** | 350 | 45 | 45 | **440** | Field truck crops; tightly cupped waxy glaucous leaves with prominent white veins, head formation stages. | broccoli, cauliflower, turnip, collards | **High** | Yes - 274 images in model2_v4 (220 train, 25 val, 29 test; +130 train images recommended) |
| **`carrot`** | 300 | 40 | 40 | **380** | Field raised beds; tripinnate feathery umbelliferous foliage, close-ups of crown and leaf margins with blight lesions. | celery, parsley, fennel | **Medium** | Yes - 148 images in model2_v4 (119 train, 12 val, 17 test; +181 train images recommended) |
| **`cauliflower`** | 300 | 40 | 40 | **380** | Open field; oblong glaucous upright leaves surrounding white curd; field soil background. | cabbage, broccoli | **High** | Yes - 104 images in model2_v4 (83 train, 8 val, 13 test; +217 train images recommended) |
| **`celery`** | 250 | 35 | 35 | **320** | Muck soil field crops; succulent grooved petioles, pinnate toched leaflets, blight spots. | carrot, parsley, cilantro | **Medium** | Yes - 65 images in model2_v4 (53 train, 6 val, 6 test; +197 train images recommended) |
| **`cherry`** | 350 | 45 | 45 | **440** | Orchard canopy; simple serrate leaves with prominent reddish petiole glands, shot-hole and powdery mildew symptoms. | plum, peach, apple | **High** | Yes - 139 images in model2_v4 (113 train, 13 val, 13 test; +237 train images recommended) |
| **`citrus`** | 400 | 50 | 50 | **500** | Grove orchard conditions; dark glossy leathery evergreen leaves with winged petioles; canker pustules and HLB mottling. | coffee, gardenia, camellia | **Medium** | Yes - 521 images in model2_v4 (413 train, 46 val, 62 test; sufficient for direct reuse) |
| **`coffee`** | 350 | 45 | 45 | **440** | Tropical agroforestry & sun plantations; opposite glossy dark green elliptic leaves with wavy margins and sunken veins. | citrus, gardenia | **Medium** | Yes - 284 images in model2_v4 (232 train, 26 val, 26 test; +118 train images recommended) |
| **`corn`** | 500 | 60 | 60 | **620** | Commercial field conditions; long linear arching blades with parallel venation, sheath clasp, leaf blight lesions and rust pustules. | sorghum, sugarcane, young wheat/rice | **Medium** | Yes - 616 images in model2_v4 (497 train, 56 val, 63 test; sufficient for direct reuse) |
| **`eggplant`** | 300 | 40 | 40 | **380** | Field & greenhouse vegetable; broad ovate leaves with lobed/sinuate margins, dense stellate pubescence, purple veins. | tobacco, tomato, potato | **Medium** | Yes - 136 images in model2_v4 (109 train, 12 val, 15 test; +191 train images recommended) |
| **`garlic`** | 300 | 40 | 40 | **380** | Field raised beds; flat linear strap leaves with solid V-shape cross-section and keeled spine, leaf blight lesions. | onion, leek, chives | **Medium** | Yes - 198 images in model2_v4 (157 train, 17 val, 24 test; +143 train images recommended) |
| **`ginger`** | 250 | 35 | 35 | **320** | Tropical shade & field beds; slender distichous lanceolate leaves along reed-like pseudostems; sheath blight lesions. | turmeric, cardamom, bamboo | **Medium** | Yes - 91 images in model2_v4 (71 train, 8 val, 12 test; +179 train images recommended) |
| **`grape`** | 450 | 55 | 55 | **560** | Vineyard trellis; cordate palmate-lobed leaves with coarse teeth, tendrils, black rot spots, downy mildew oilspots. | melon, squash, cucumber | **Medium** | Yes - 558 images in model2_v4 (447 train, 51 val, 60 test; sufficient for direct reuse) |
| **`maple`** | 200 | 30 | 30 | **260** | Deciduous canopy/lawn trees; palmate 3-5 pointed lobed leaves with sharply serrated teeth and tar spot stroma. | sycamore, sweetgum, grape | **Low** | Yes - 113 images in model2_v4 (95 train, 10 val, 8 test; +105 train images recommended) |
| **`peach`** | 400 | 50 | 50 | **500** | Orchard trees; narrow lanceolate leaves with pointed tips and fine glandular serrations; prominent leaf curl distortion. | plum, cherry, almond, willow | **High** | Yes - 444 images in model2_v4 (362 train, 40 val, 42 test; sufficient for direct reuse) |
| **`plum`** | 350 | 45 | 45 | **440** | Orchard canopy; ovate to elliptic leaves, darker green and broader than peach, with bacterial spot shot-holes. | peach, cherry, apple | **High** | Yes - 215 images in model2_v4 (179 train, 20 val, 16 test; +171 train images recommended) |
| **`potato`** | 350 | 45 | 45 | **440** | Hilled field crops; imparipinnate compound leaves with large oval terminal leaflet and smaller interjected leaflets; concentric blight rings. | tomato, eggplant | **High** | Yes - 239 images in model2_v4 (196 train, 21 val, 22 test; +154 train images recommended) |
| **`raspberry`** | 300 | 40 | 40 | **380** | Cane berry trellis; compound 3-5 ovate leaflets with white-felted tomentose undersides and prickly stems; leaf spot lesions. | blackberry, rose, strawberry | **Medium** | Yes - 123 images in model2_v4 (100 train, 12 val, 11 test; +200 train images recommended) |
| **`rice`** | 400 | 50 | 50 | **500** | Paddy field / wetland conditions; slender upright linear blades with distinct long ligule, spindle-shaped blast lesions. | wheat, barley, grasses | **High** | Yes - 155 images in model2_v4 (126 train, 14 val, 15 test; +274 train images recommended) |
| **`soybean`** | 500 | 60 | 60 | **620** | Broadacre row crops; trifoliate leaves with broadly ovate leaflets densely clad in fine tawny puberulence; rust pustules and frogeye spots. | french_bean, cowpea, alfalfa | **High** | Yes - 1122 images in model2_v4 (947 train, 105 val, 70 test; fully sufficient for direct reuse) |
| **`tobacco`** | 350 | 45 | 45 | **440** | Field crops; massive sessile ovate-elliptic leaves with viscous glandular trichomes, prominent white veins, and blue mold spots. | eggplant, comfrey | **Low** | Yes - 178 images in model2_v4 (141 train, 17 val, 20 test; +209 train images recommended) |
| **`wheat`** | 600 | 75 | 75 | **750** | Temperate grain field conditions; narrow linear upright blades with clamping auricles, tiller canopies, leaf rust and stripe rust pustules. | barley, rye, rice, oats | **High** | Yes - 1632 images in model2_v4 (1322 train, 146 val, 164 test; fully sufficient for direct reuse) |

---

## 2. In-Depth Project Data Reuse Assessment

An immediate advantage discovered during this audit is that **all 24 proposed new classes are already present in `data/processed/model2_v4/model2_v4_manifest.csv`**!

### Reuse Tiers:
1. **Tier 1 — Full Direct Sufficiency (>=400 Train Images Already in Project):**
   - `wheat` (1,322 train / 146 val / 164 test)
   - `soybean` (947 train / 105 val / 70 test)
   - `corn` (497 train / 56 val / 63 test)
   - `apple` (456 train / 50 val / 60 test)
   - `grape` (447 train / 51 val / 60 test)
   - `banana` (436 train / 49 val / 51 test)
   - `citrus` (413 train / 46 val / 62 test)
   - `peach` (362 train / 40 val / 42 test)
   *These 8 classes require zero external dataset downloads and can be immediately sampled from verified project data.*

2. **Tier 2 — Substantial Core Available (100–350 Train Images):**
   - `coffee` (232 train), `cabbage` (220 train), `potato` (196 train), `plum` (179 train), `garlic` (157 train), `tobacco` (141 train), `rice` (126 train), `carrot` (119 train), `cherry` (113 train), `eggplant` (109 train), `cauliflower` (83 train), `raspberry` (100 train), `maple` (95 train).
   *These 13 classes have verified, clean real images in Model 2 V4. Moderate supplemental sampling (+100 to +250 images) will bring them to optimal sample density.*

3. **Tier 3 — Supplementary Acquisition Required (<100 Train Images):**
   - `ginger` (71 train), `celery` (53 train), `basil` (51 train).
   *These 3 classes will require targeted external acquisition (e.g. from Kaggle/PlantSeg archives) to reach the 250+ image threshold.*

---

## 3. Comprehensive Risk Analysis on Current Model 1 Baseline

Expanding Model 1 from 22 classes to 46 classes carries distinct classification and operational risks that must be proactively mitigated:

### Baseline Performance Reference:
- **Top-1 Accuracy:** **97.84%**
- **Top-3 Accuracy:** **99.46%**
- **Macro F1-Score:** **92.91%**
- **Weighted F1-Score:** **97.82%**

Any future expanded model must meet or exceed these operational baselines.

### Major Visual Confusion Clusters & Mitigation:

#### 1. Solanaceae Cluster (`tomato`, `cherry_tomato`, `capsicum`, `eggplant`, `potato`, `tobacco`)
- **Risk:** High visual similarity in leaf venation, trichomes, and solanaceous morphology. In particular, `potato` vs `tomato` foliage can exhibit high confusion when symptoms are absent.
- **Mitigation:**
  - Enforce diverse scale augmentation (full canopy vs close-up leaflet).
  - Include fruit/flower morphology where present.
  - Maintain `cherry_tomato` -> `tomato` aliasing to prevent intra-species split confusion.

#### 2. Cucurbitaceae Cluster (`cucumber`, `melon`, `zucchini`, `squash`)
- **Risk:** Palmate lobing, harsh trichomes, and trailing vine habit cause high feature overlap. Baseline Model 1 already showed lower precision on `zucchini` (82.98%) due to confusion with cucumber.
- **Mitigation:**
  - Strictly maintain `squash` as an alias of `zucchini` rather than creating a separate class.
  - Exploit silver leaf variegation cues specific to *Cucurbita pepo*.

#### 3. Cereals & Poaceae Cluster (`wheat`, `rice`, `corn`)
- **Risk:** Linear strap leaves and monocot venation are easily confused at early vegetative stages.
- **Mitigation:**
  - `corn` has broad blades (5–10 cm wide) easily separated by leaf-width-to-length ratio.
  - `wheat` vs `rice`: Ensure training images include ligule/auricle close-ups and agricultural background context (flooded paddy vs dry field drills).

#### 4. Rosaceae Stone & Pome Fruits Cluster (`apple`, `peach`, `plum`, `cherry`)
- **Risk:** Simple alternate serrated tree leaves on woody twigs. Close leaf close-ups can lead to mutual misclassification.
- **Mitigation:**
  - `peach` leaves are uniquely long-lanceolate (length-to-width ratio > 4:1).
  - `cherry` leaves feature prominent red glands on petioles.
  - `apple` leaves feature rounder bases and tomentose undersides.
  - Add hard-negative mining across fruit trees during training.

#### 5. Brassica Cluster (`broccoli`, `cabbage`, `cauliflower`)
- **Risk:** *Brassica oleracea* varieties share glaucous waxy blooms and undulating margins.
- **Mitigation:**
  - `cabbage`: Dense spherical head structure.
  - `cauliflower`: Upright long oblong leaves cradling white curd.
  - `broccoli`: Branching open rosette leaves with blue-green floret heads.

#### 6. Leafy Greens & Herbs (`lettuce`, `spinach`, `basil`, `celery`)
- **Risk:** Broad green foliage without distinct floral features.
- **Mitigation:**
  - `spinach`: Arrowhead/hastate basal leaves.
  - `basil`: Square stem morphology and small glossy opposite pairs.
  - `celery`: Compound pinnate leaflets on thick fluted stalks.

### Class Imbalance & Weak Baseline Classes:
- Current baseline has weak/low-data classes: `gerbera` (1 test sample, F1 0.00%), `gypsophila` (0 test samples), `cherry_tomato` (0 test samples), `carnation` (5 test samples), `lilium` (5 test samples).
- **Mitigation for Expansion Training:**
  - Employ **Effective Number of Samples Class-Balanced Loss** or **Focal Loss** (gamma=2.0).
  - Apply weighted random sampling to guarantee minimum batch representation for low-data floriculture classes.
  - Cap maximum training images per class at 600 to prevent dominant classes (`wheat`, `tomato`, `soybean`) from overpowering minor classes.
