# MODEL 1 VS MODEL 2 CROP TAXONOMY GAP AUDIT

**Date:** 2026-10-08  
**Audit Purpose:** Comprehensive taxonomy gap audit between the production Model 1 crop classifier (22 classes) and Model 2 V4 disease classifier (117 classes: 1 shared healthy + 116 disease classes) to establish end-to-end reachability requirements.  
**Baseline Status:**  
- **Model 1 Production Baseline:** LOCKED (Top-1: 97.84%, Top-3: 99.46%, Macro F1: 92.91%, Weighted F1: 97.82%, 22 classes)  
- **Model 2 V4 Production Baseline:** LOCKED (117 classes, 24/24 regression PASS, 32/32 E2E PASS)  
- **Knowledge Engine:** 116/116 disease records verified and active in production  
- **Execution Mode:** Analytical taxonomy audit only (zero weight edits, zero downloads, zero code changes)  

---

## 1. Executive Summary & Audit Metrics

| Metric | Current Status | Expanded Target | Net Delta |
| :--- | :--- | :--- | :--- |
| **Model 1 Crop Classes** | **22** | **46** | **+24 new classes** |
| **Model 2 Crops with Diseases** | **34** | **34** | **0 (Full Coverage)** |
| **Model 2 Disease Classes Reachable (Direct Name)** | **26** (22.4%) | **26** | **-** |
| **Model 2 Disease Classes Reachable (with Aliases)** | **34** (29.3%) | **35** (+1 squash) | **+1** |
| **Model 2 Disease Classes Unreachable from M1** | **81** (69.8%) | **0** (0.0%) | **-81 (Eliminated)** |
| **Total Reachable Model 2 V4 Diseases** | **34 / 116** (29.3%) | **116 / 116** (100.0%) | **+82 diseases** |
| **Knowledge Base Coverage for Reachable Diseases** | 34 / 34 (100%) | 116 / 116 (100%) | **116 / 116 (100%)** |

### Key Diagnostic Finding:
Currently, **81 disease classes across 24 crop families** in Model 2 V4 are **completely unreachable** through the end-to-end vision pipeline because Model 1 lacks the ability to identify those crops. When an image of an unrepresented crop (e.g., wheat, apple, banana, corn, soybean) is processed, Model 1 forces a prediction into one of its 22 greenhouse/floriculture classes (e.g., predicting `lettuce`, `tomato`, or `orchid`), causing an incompatibility rejection or misrouting in the reasoning engine.

---

## 2. Complete Model 2 Crop Taxonomy Audit Table

The following authoritative table details all **39 crop entities** registered in `data/processed/model2_organized_crop_disease_mapping.json`:

| Model 2 Crop | Diseases | Disease Classes in Model 2 V4 | Healthy Available? | Currently Reachable from Model 1? | Recommended Model 1 Action |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **`apple`** | **4** | `apple__black_rot;apple__mosaic_virus;apple__rust;apple__scab` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`banana`** | **6** | `banana__anthracnose;banana__black_leaf_streak;banana__bunchy_top;banana__cigar_end_rot;banana__cordana_leaf_spot;banana__panama_disease` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`basil`** | **1** | `basil__downy_mildew` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`bean`** | **4** | `bean__angular_leaf_spot;bean__halo_blight;bean__mosaic_virus;bean__rust` | True | YES (Aliased from french_bean) | B. MAP TO EXISTING MODEL 1 CLASS (french_bean <-> bean) |
| **`bell_pepper`** | **4** | `bell_pepper__bacterial_spot;bell_pepper__blossom_end_rot;bell_pepper__frogeye_leaf_spot;bell_pepper__powdery_mildew` | True | YES (Aliased from capsicum) | B. MAP TO EXISTING MODEL 1 CLASS (capsicum <-> bell_pepper) |
| **`blueberry`** | **5** | `blueberry__anthracnose;blueberry__botrytis_blight;blueberry__mummy_berry;blueberry__rust;blueberry__scorch` | False (Shared Class 0 only) | YES (Direct M1 Class) | RETAIN (Current Model 1 Class) |
| **`broccoli`** | **3** | `broccoli__alternaria_leaf_spot;broccoli__downy_mildew;broccoli__ring_spot` | True | YES (Direct M1 Class) | RETAIN (Current Model 1 Class) |
| **`cabbage`** | **3** | `cabbage__alternaria_leaf_spot;cabbage__black_rot;cabbage__downy_mildew` | True | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`capsicum`** | **0** | `none` | True | YES (Healthy only, M1 recognized) | RETAIN (Current Model 1 Class) |
| **`carrot`** | **3** | `carrot__alternaria_leaf_blight;carrot__cavity_spot;carrot__cercospora_leaf_blight` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`cauliflower`** | **2** | `cauliflower__alternaria_leaf_spot;cauliflower__bacterial_soft_rot` | True | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`celery`** | **2** | `celery__anthracnose;celery__early_blight` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`cherry`** | **2** | `cherry__leaf_spot;cherry__powdery_mildew` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`citrus`** | **2** | `citrus__canker;citrus__greening_disease` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`coffee`** | **4** | `coffee__berry_blotch;coffee__black_rot;coffee__brown_eye_spot;coffee__leaf_rust` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`corn`** | **4** | `corn__gray_leaf_spot;corn__northern_leaf_blight;corn__rust;corn__smut` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`cucumber`** | **3** | `cucumber__angular_leaf_spot;cucumber__bacterial_wilt;cucumber__powdery_mildew` | True | YES (Direct M1 Class) | RETAIN (Current Model 1 Class) |
| **`eggplant`** | **3** | `eggplant__cercospora_leaf_spot;eggplant__phomopsis_fruit_rot;eggplant__phytophthora_blight` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`garlic`** | **2** | `garlic__leaf_blight;garlic__rust` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`ginger`** | **2** | `ginger__leaf_spot;ginger__sheath_blight` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`grape`** | **4** | `grape__black_rot;grape__downy_mildew;grape__grapevine_leafroll_disease;grape__leaf_spot` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`lettuce`** | **2** | `lettuce__downy_mildew;lettuce__mosaic_virus` | True | YES (Direct M1 Class) | RETAIN (Current Model 1 Class) |
| **`maple`** | **1** | `maple__tar_spot` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`marigold`** | **0** | `none` | True | YES (Healthy only, M1 recognized) | RETAIN (Current Model 1 Class) |
| **`peach`** | **5** | `peach__anthracnose;peach__brown_rot;peach__leaf_curl;peach__rust;peach__scab` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`plum`** | **5** | `plum__bacterial_spot;plum__brown_rot;plum__pocket_disease;plum__pox_virus;plum__rust` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`potato`** | **2** | `potato__early_blight;potato__late_blight` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`raspberry`** | **4** | `raspberry__fire_blight;raspberry__gray_mold;raspberry__leaf_spot;raspberry__yellow_rust` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`rice`** | **2** | `rice__blast;rice__sheath_blight` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`rose`** | **0** | `none` | True | YES (Healthy only, M1 recognized) | RETAIN (Current Model 1 Class) |
| **`soybean`** | **6** | `soybean__bacterial_blight;soybean__brown_spot;soybean__downy_mildew;soybean__frog_eye_leaf_spot;soybean__mosaic;soybean__rust` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`spinach`** | **0** | `none` | True | YES (Healthy only, M1 recognized) | RETAIN (Current Model 1 Class) |
| **`squash`** | **1** | `squash__powdery_mildew` | False (Shared Class 0 only) | NO (Unmapped to zucchini) | B. MAP TO EXISTING MODEL 1 CLASS (squash -> zucchini) |
| **`strawberry`** | **2** | `strawberry__anthracnose;strawberry__leaf_scorch` | True | YES (Direct M1 Class) | RETAIN (Current Model 1 Class) |
| **`tobacco`** | **4** | `tobacco__blue_mold;tobacco__brown_spot;tobacco__frogeye_leaf_spot;tobacco__mosaic_virus` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`tomato`** | **7** | `tomato__bacterial_leaf_spot;tomato__early_blight;tomato__late_blight;tomato__leaf_mold;tomato__mosaic_virus;tomato__septoria_leaf_spot;tomato__yellow_leaf_curl_virus` | True | YES (Direct M1 Class) | RETAIN (Current Model 1 Class) |
| **`turnip`** | **0** | `none` | True | NO (0 disease classes in M2) | C. DO NOT ADD (0 diseases in V4; healthy only; review for V5) |
| **`wheat`** | **8** | `wheat__bacterial_leaf_streak_(black_chaff);wheat__head_scab;wheat__leaf_rust;wheat__loose_smut;wheat__powdery_mildew;wheat__septoria_blotch;wheat__stem_rust;wheat__stripe_rust` | False (Shared Class 0 only) | NO (Absent from Model 1) | A. ADD AS NEW MODEL 1 CLASS |
| **`zucchini`** | **4** | `zucchini__bacterial_wilt;zucchini__downy_mildew;zucchini__powdery_mildew;zucchini__yellow_mosaic_virus` | False (Shared Class 0 only) | YES (Direct M1 Class) | RETAIN (Current Model 1 Class) |

---

## 3. Mathematical Reachability Accounting

```
Total Model 2 V4 Classes: 117
├── Shared Healthy Class: 1 (Index 0, covers all crops)
└── Disease Classes: 116 (Indices 1 to 116)
    ├── Directly Reachable via identical M1 class (7 crops): 26 classes
    │   ├── blueberry (5)
    │   ├── broccoli (3)
    │   ├── cucumber (3)
    │   ├── lettuce (2)
    │   ├── strawberry (2)
    │   ├── tomato (7)
    │   └── zucchini (4)
    ├── Reachable via existing Model 1 aliases (2 crops): 8 classes
    │   ├── bean (4) [aliased from french_bean]
    │   └── bell_pepper (4) [aliased from capsicum]
    ├── Newly Reachable via proposed squash alias (1 crop): 1 class
    │   └── squash__powdery_mildew (1) [aliased to zucchini]
    └── Currently Unreachable belonging to 24 absent crops: 81 classes
        ├── apple (4), banana (6), basil (1), cabbage (3), carrot (3), cauliflower (2),
        ├── celery (2), cherry (2), citrus (2), coffee (4), corn (4), eggplant (3),
        ├── garlic (2), ginger (2), grape (4), maple (1), peach (5), plum (5),
        ├── potato (2), raspberry (4), rice (2), soybean (6), tobacco (4), wheat (8).
        └── Subtotal: 81 classes

Total Reachable after M1 Expansion: 26 + 8 + 1 + 81 = 116 / 116 (100.0%)
```

---

## 4. Analysis of the 25 Absent Crops Identified

The 25 crops identified in the audit prompt are classified as follows:

### Category A: ADD AS NEW MODEL 1 CLASS (24 Crops)
1. **`apple`** (4 diseases): High-impact temperate fruit tree. Unrepresented in M1. Distinct woody pome morphology.
2. **`banana`** (6 diseases): High-value tropical monocot. Unrepresented in M1. Huge paddle leaves with parallel venation.
3. **`basil`** (1 disease): Culinary aromatic herb. Unrepresented in M1. Distinct glossy opposite ovate leaves.
4. **`cabbage`** (3 diseases): Essential brassica vegetable. Unrepresented in M1. Distinct compact head and waxy glaucous leaves.
5. **`carrot`** (3 diseases): Root vegetable. Unrepresented in M1. Distinctive feathery pinnate foliage.
6. **`cauliflower`** (2 diseases): Brassica vegetable. Unrepresented in M1. Distinct upright leaves and white curd.
7. **`celery`** (2 diseases): Apiaceae vegetable. Unrepresented in M1. Thick succulent grooved petioles with serrated leaflets.
8. **`cherry`** (2 diseases): Stone fruit tree. Unrepresented in M1. Distinct alternate serrated leaves with petiole glands. (Crucially distinct from cherry_tomato).
9. **`citrus`** (2 diseases): Major subtropical fruit genus. Unrepresented in M1. Leathery dark evergreen leaves with winged petioles.
10. **`coffee`** (4 diseases): Global tropical plantation crop. Unrepresented in M1. Glossy undulating opposite leaves.
11. **`corn`** (4 diseases): Primary staple cereal. Unrepresented in M1. Huge arching linear leaves with prominent midribs.
12. **`eggplant`** (3 diseases): Solanaceous vegetable. Unrepresented in M1. Large coarse lobed leaves with stellate hairs.
13. **`garlic`** (2 diseases): Allium bulb crop. Unrepresented in M1. Flat linear keeled V-shaped strap leaves.
14. **`ginger`** (2 diseases): Zingiberaceae rhizome spice. Unrepresented in M1. Reed-like pseudostems with distichous lanceolate blades.
15. **`grape`** (4 diseases): Viticulture woody vine. Unrepresented in M1. Distinct palmate cordate leaves and tendrils.
16. **`maple`** (1 disease): Landscape/shade deciduous tree. Unrepresented in M1. Distinct palmate 3-5 pointed lobes.
17. **`peach`** (5 diseases): Stone fruit tree. Unrepresented in M1. Long lanceolate serrated leaves with pointed tips.
18. **`plum`** (5 diseases): Stone fruit tree. Unrepresented in M1. Ovate finely serrated leaves broader than peach.
19. **`potato`** (2 diseases): Staple food tuber. Unrepresented in M1. Solanaceous pinnate compound leaves with rounded leaflets.
20. **`raspberry`** (4 diseases): Cane fruit shrub. Unrepresented in M1. Prickly canes with 3-5 tomentose serrated leaflets.
21. **`rice`** (2 diseases): Primary global staple cereal. Unrepresented in M1. Slender upright semi-aquatic blades with ligules.
22. **`soybean`** (6 diseases): Major oilseed legume. Unrepresented in M1. Densely pubescent trifoliate leaves with ovate leaflets.
23. **`tobacco`** (4 diseases): Solanaceous industrial crop. Unrepresented in M1. Massive ovate sticky glandular leaves.
24. **`wheat`** (8 diseases): Major staple cereal (highest disease count in M2). Unrepresented in M1. Linear upright blades with auricles.

### Category C: DO NOT ADD (1 Crop)
25. **`turnip`** (0 diseases):
   - **Reason:** Model 2 V4 has **zero** disease classes for turnip (only 181 healthy samples in the dataset manifest). Turnip has 0 KB records. Adding turnip to Model 1 would increase classifier parameters and risk confusion with brassicas without enabling any disease diagnostics in V4. Action: **Exclude until Model 2 V5 introduces turnip pathology**.

---

## 5. Reachability Gap Conclusion

Adding the **24 validated agricultural crops** to Model 1 and formalizing the **4 alias mappings** (`bean` <-> `french_bean`, `bell_pepper` <-> `capsicum`, `squash` -> `zucchini`, `cherry_tomato` -> `tomato`) will elevate end-to-end disease reachability from **34 classes (29.3%) to 116 classes (100.0%)**, unlocking the full potential of Model 2 V4.
