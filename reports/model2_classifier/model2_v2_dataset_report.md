# Model 2 Classifier v2 Final Dataset Construction Report

**Date:** 2026-10-07  
**Module:** Model 2 Classifier v2 Dataset (Phase 4E Final Dataset)  
**Dataset Location:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\processed\model2_classifier_v2`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\processed\model2_classifier_v2)  
**Manifest Location:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\processed\model2_classifier_v2_manifest.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\processed\model2_classifier_v2_manifest.csv)  
**Random Seed:** `42` (Strictly Reproducible Stratified Split)  

---

## 1. Executive Summary & Verification Dashboard

```
ORIGINAL MODEL 2 DATASET          : 15,304 images (117 classes)
APPROVED SUPPLEMENTARY ADDED      : +3,949 images (3,499 PlantSeg + 450 Soybean Rust)
FINAL TRAINING SET (90% Pool)     : 15,252 images
FINAL VALIDATION SET (10% Pool)   : 1,697 images
IMMUTABLE TEST SET (Protected)    : 2,304 images (100% Bit-for-Bit Preserved)
TOTAL FINAL V2 DATASET SIZE       : 19,253 images
TOTAL CLASSES                     : 117 (116 disease classes + 1 healthy)
TRAIN / VAL / TEST LEAKAGE        : 0 (Zero exact duplicates across any split)
SOYBEAN RUST TRAIN SUPPORT        : 455 images (up from 46)
BEAN ANGULAR LEAF SPOT TRAIN      : 330 images (retained from Makerere baseline)
```

---

## 2. Weak-Class Expansion & Target Relief

| Priority Tier | Model 2 Class | Baseline Test F1 | Original Train | Supp Added | New Train | New Val | Immutable Test | Total Images |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `CRITICAL` | `plum__rust` | 0.0000 | 12 | **+17** | 29 | 3 | 2 | **34** |
| `CRITICAL` | `cauliflower__alternaria_leaf_spot` | 0.0000 | 19 | **+16** | 35 | 4 | 4 | **43** |
| `CRITICAL` | `cauliflower__bacterial_soft_rot` | 0.0000 | 13 | **+14** | 27 | 3 | 2 | **32** |
| `CRITICAL` | `cherry__powdery_mildew` | 0.0000 | 18 | **+8** | 27 | 3 | 3 | **33** |
| `CRITICAL` | `raspberry__leaf_spot` | 0.0000 | 8 | **+7** | 15 | 2 | 1 | **18** |
| `CRITICAL` | `plum__bacterial_spot` | 0.0000 | 7 | **+6** | 13 | 2 | 1 | **16** |
| `CRITICAL` | `bell_pepper__frogeye_leaf_spot` | 0.0000 | 16 | **+5** | 22 | 2 | 4 | **28** |
| `CRITICAL` | `broccoli__ring_spot` | 0.0000 | 5 | **+3** | 8 | 1 | 1 | **10** |
| `CRITICAL` | `coffee__black_rot` | 0.0000 | 2 | **+3** | 5 | 1 | 0 | **6** |
| `CRITICAL` | `coffee__brown_eye_spot` | 0.0000 | 8 | **+3** | 12 | 1 | 1 | **14** |
| `CRITICAL` | `peach__rust` | 0.0000 | 3 | **+3** | 6 | 1 | 1 | **8** |
| `CRITICAL` | `cabbage__alternaria_leaf_spot` | 0.1538 | 25 | **+22** | 47 | 5 | 6 | **58** |
| `CRITICAL` | `plum__pocket_disease` | 0.2222 | 20 | **+29** | 48 | 5 | 4 | **57** |
| `CRITICAL` | `tobacco__frogeye_leaf_spot` | 0.2222 | 10 | **+5** | 15 | 2 | 3 | **20** |
| `CRITICAL` | `ginger__sheath_blight` | 0.2353 | 40 | **+9** | 52 | 6 | 8 | **66** |
| `CRITICAL` | `bean__mosaic_virus` | 0.2667 | 23 | **+24** | 47 | 5 | 5 | **57** |
| `CRITICAL` | `banana__cordana_leaf_spot` | 0.2857 | 20 | **+23** | 42 | 5 | 4 | **51** |
| `CRITICAL` | `zucchini__downy_mildew` | 0.3333 | 22 | **+11** | 34 | 4 | 5 | **43** |
| `CRITICAL` | `tomato__septoria_leaf_spot` | 0.3448 | 64 | **+31** | 98 | 11 | 14 | **123** |
| `CRITICAL` | `squash__powdery_mildew` | 0.3784 | 96 | **+37** | 139 | 15 | 20 | **174** |
| `HIGH` | `zucchini__powdery_mildew` | 0.4000 | 87 | **+76** | 164 | 18 | 18 | **200** |
| `HIGH` | `bean__halo_blight` | 0.4000 | 24 | **+21** | 45 | 5 | 6 | **56** |
| `HIGH` | `tomato__mosaic_virus` | 0.4000 | 30 | **+20** | 50 | 6 | 7 | **63** |
| `HIGH` | `soybean__brown_spot` | 0.4000 | 33 | **+14** | 49 | 5 | 7 | **61** |
| `HIGH` | `eggplant__phytophthora_blight` | 0.4000 | 15 | **+11** | 26 | 3 | 4 | **33** |
| `HIGH` | `plum__pox_virus` | 0.4000 | 15 | **+10** | 25 | 3 | 4 | **32** |
| `HIGH` | `carrot__cercospora_leaf_blight` | 0.4000 | 11 | **+1** | 13 | 1 | 3 | **17** |
| `HIGH` | `soybean__rust` | 0.4167 | 46 | **+450** | 455 | 51 | 9 | **515** |
| `HIGH` | `eggplant__cercospora_leaf_spot` | 0.4444 | 25 | **+22** | 47 | 5 | 6 | **58** |
| `HIGH` | `celery__early_blight` | 0.4444 | 20 | **+7** | 28 | 3 | 5 | **36** |
| `HIGH` | `rice__sheath_blight` | 0.4545 | 36 | **+20** | 58 | 6 | 8 | **72** |
| `HIGH` | `wheat__leaf_rust` | 0.4615 | 51 | **+55** | 105 | 12 | 11 | **128** |
| `HIGH` | `corn__gray_leaf_spot` | 0.4762 | 53 | **+31** | 85 | 10 | 12 | **107** |
| `HIGH` | `soybean__bacterial_blight` | 0.4762 | 42 | **+27** | 70 | 8 | 9 | **87** |
| `HIGH` | `cabbage__downy_mildew` | 0.5000 | 34 | **+35** | 68 | 8 | 8 | **84** |
| `HIGH` | `rice__blast` | 0.5000 | 35 | **+33** | 68 | 8 | 7 | **83** |
| `HIGH` | `apple__black_rot` | 0.5000 | 44 | **+20** | 66 | 7 | 10 | **83** |
| `HIGH` | `lettuce__mosaic_virus` | 0.5000 | 15 | **+17** | 31 | 4 | 4 | **39** |
| `HIGH` | `garlic__leaf_blight` | 0.5000 | 55 | **+13** | 72 | 8 | 12 | **92** |
| `HIGH` | `raspberry__fire_blight` | 0.5000 | 16 | **+8** | 24 | 3 | 4 | **31** |
| `HIGH` | `ginger__leaf_spot` | 0.5000 | 15 | **+3** | 19 | 2 | 4 | **25** |
| `HIGH` | `tomato__bacterial_leaf_spot` | 0.5333 | 62 | **+19** | 85 | 9 | 13 | **107** |
| `HIGH` | `wheat__bacterial_leaf_streak_(black_chaff)` | 0.5385 | 57 | **+33** | 92 | 10 | 13 | **115** |
| `HIGH` | `soybean__mosaic` | 0.5385 | 62 | **+27** | 92 | 10 | 13 | **115** |
| `HIGH` | `blueberry__rust` | 0.5455 | 23 | **+10** | 34 | 4 | 5 | **43** |
| `HIGH` | `wheat__septoria_blotch` | 0.5500 | 86 | **+78** | 164 | 18 | 19 | **201** |
| `HIGH` | `zucchini__bacterial_wilt` | 0.5714 | 39 | **+12** | 53 | 6 | 9 | **68** |
| `HIGH` | `broccoli__downy_mildew` | 0.5714 | 16 | **+6** | 23 | 2 | 4 | **29** |
| `HIGH` | `grape__leaf_spot` | 0.5882 | 46 | **+22** | 70 | 8 | 10 | **88** |

---

## 3. Complete 117-Class Accounting & Distribution Master Table

| Class ID | Class Name | Original Train | Original Val | Supp Added | New Train | New Val | Original Test | Total |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `apple__black_rot` | 44 | 9 | +20 | 66 | 7 | 10 | **83** |
| 2 | `apple__mosaic_virus` | 51 | 11 | +16 | 70 | 8 | 11 | **89** |
| 3 | `apple__rust` | 69 | 15 | +40 | 112 | 12 | 14 | **138** |
| 4 | `apple__scab` | 116 | 25 | +90 | 208 | 23 | 25 | **256** |
| 5 | `banana__anthracnose` | 34 | 7 | +21 | 56 | 6 | 7 | **69** |
| 6 | `banana__black_leaf_streak` | 76 | 16 | +49 | 127 | 14 | 17 | **158** |
| 7 | `banana__bunchy_top` | 50 | 11 | +67 | 115 | 13 | 11 | **139** |
| 8 | `banana__cigar_end_rot` | 22 | 5 | +25 | 47 | 5 | 4 | **56** |
| 9 | `banana__cordana_leaf_spot` | 20 | 4 | +23 | 42 | 5 | 4 | **51** |
| 10 | `banana__panama_disease` | 34 | 7 | +14 | 49 | 6 | 8 | **63** |
| 11 | `basil__downy_mildew` | 29 | 6 | +22 | 51 | 6 | 6 | **63** |
| 12 | `bean__angular_leaf_spot` | 302 | 65 | +0 | 330 | 37 | 65 | **432** |
| 13 | `bean__halo_blight` | 24 | 5 | +21 | 45 | 5 | 6 | **56** |
| 14 | `bean__mosaic_virus` | 23 | 5 | +24 | 47 | 5 | 5 | **57** |
| 15 | `bean__rust` | 357 | 76 | +90 | 471 | 52 | 77 | **600** |
| 16 | `bell_pepper__bacterial_spot` | 33 | 7 | +21 | 55 | 6 | 7 | **68** |
| 17 | `bell_pepper__blossom_end_rot` | 55 | 12 | +30 | 87 | 10 | 11 | **108** |
| 18 | `bell_pepper__frogeye_leaf_spot` | 16 | 3 | +5 | 22 | 2 | 4 | **28** |
| 19 | `bell_pepper__powdery_mildew` | 13 | 3 | +8 | 22 | 2 | 2 | **26** |
| 20 | `blueberry__anthracnose` | 18 | 4 | +14 | 32 | 4 | 4 | **40** |
| 21 | `blueberry__botrytis_blight` | 13 | 3 | +16 | 29 | 3 | 3 | **35** |
| 22 | `blueberry__mummy_berry` | 20 | 4 | +18 | 38 | 4 | 4 | **46** |
| 23 | `blueberry__rust` | 23 | 5 | +10 | 34 | 4 | 5 | **43** |
| 24 | `blueberry__scorch` | 22 | 5 | +10 | 33 | 4 | 5 | **42** |
| 25 | `broccoli__alternaria_leaf_spot` | 37 | 8 | +9 | 49 | 5 | 8 | **62** |
| 26 | `broccoli__downy_mildew` | 16 | 3 | +6 | 23 | 2 | 4 | **29** |
| 27 | `broccoli__ring_spot` | 5 | 1 | +3 | 8 | 1 | 1 | **10** |
| 28 | `cabbage__alternaria_leaf_spot` | 25 | 5 | +22 | 47 | 5 | 6 | **58** |
| 29 | `cabbage__black_rot` | 62 | 13 | +32 | 96 | 11 | 13 | **120** |
| 30 | `cabbage__downy_mildew` | 34 | 7 | +35 | 68 | 8 | 8 | **84** |
| 31 | `carrot__alternaria_leaf_blight` | 31 | 7 | +14 | 47 | 5 | 7 | **59** |
| 32 | `carrot__cavity_spot` | 29 | 6 | +30 | 59 | 6 | 7 | **72** |
| 33 | `carrot__cercospora_leaf_blight` | 11 | 2 | +1 | 13 | 1 | 3 | **17** |
| 34 | `cauliflower__alternaria_leaf_spot` | 19 | 4 | +16 | 35 | 4 | 4 | **43** |
| 35 | `cauliflower__bacterial_soft_rot` | 13 | 3 | +14 | 27 | 3 | 2 | **32** |
| 36 | `celery__anthracnose` | 8 | 2 | +18 | 25 | 3 | 1 | **29** |
| 37 | `celery__early_blight` | 20 | 4 | +7 | 28 | 3 | 5 | **36** |
| 38 | `cherry__leaf_spot` | 46 | 10 | +40 | 86 | 10 | 10 | **106** |
| 39 | `cherry__powdery_mildew` | 18 | 4 | +8 | 27 | 3 | 3 | **33** |
| 40 | `citrus__canker` | 225 | 48 | +67 | 306 | 34 | 48 | **388** |
| 41 | `citrus__greening_disease` | 65 | 14 | +40 | 107 | 12 | 14 | **133** |
| 42 | `coffee__berry_blotch` | 46 | 10 | +40 | 86 | 10 | 9 | **105** |
| 43 | `coffee__black_rot` | 2 | 1 | +3 | 5 | 1 | 0 | **6** |
| 44 | `coffee__brown_eye_spot` | 8 | 2 | +3 | 12 | 1 | 1 | **14** |
| 45 | `coffee__leaf_rust` | 75 | 16 | +52 | 129 | 14 | 16 | **159** |
| 46 | `corn__gray_leaf_spot` | 53 | 11 | +31 | 85 | 10 | 12 | **107** |
| 47 | `corn__northern_leaf_blight` | 64 | 14 | +38 | 104 | 12 | 14 | **130** |
| 48 | `corn__rust` | 84 | 18 | +57 | 143 | 16 | 18 | **177** |
| 49 | `corn__smut` | 92 | 20 | +71 | 165 | 18 | 19 | **202** |
| 50 | `cucumber__angular_leaf_spot` | 104 | 22 | +34 | 144 | 16 | 22 | **182** |
| 51 | `cucumber__bacterial_wilt` | 57 | 12 | +26 | 85 | 10 | 13 | **108** |
| 52 | `cucumber__powdery_mildew` | 106 | 23 | +35 | 148 | 16 | 22 | **186** |
| 53 | `eggplant__cercospora_leaf_spot` | 25 | 5 | +22 | 47 | 5 | 6 | **58** |
| 54 | `eggplant__phomopsis_fruit_rot` | 22 | 5 | +13 | 36 | 4 | 5 | **45** |
| 55 | `eggplant__phytophthora_blight` | 15 | 3 | +11 | 26 | 3 | 4 | **33** |
| 56 | `garlic__leaf_blight` | 55 | 12 | +13 | 72 | 8 | 12 | **92** |
| 57 | `garlic__rust` | 56 | 12 | +26 | 85 | 9 | 12 | **106** |
| 58 | `ginger__leaf_spot` | 15 | 3 | +3 | 19 | 2 | 4 | **25** |
| 59 | `ginger__sheath_blight` | 40 | 9 | +9 | 52 | 6 | 8 | **66** |
| 60 | `grape__black_rot` | 61 | 13 | +34 | 97 | 11 | 13 | **121** |
| 61 | `grape__downy_mildew` | 146 | 31 | +69 | 221 | 25 | 32 | **278** |
| 62 | `grape__grapevine_leafroll_disease` | 22 | 5 | +39 | 59 | 7 | 5 | **71** |
| 63 | `grape__leaf_spot` | 46 | 10 | +22 | 70 | 8 | 10 | **88** |
| 0 | `healthy` | 4857 | 1041 | +0 | 5308 | 590 | 1041 | **6939** |
| 64 | `lettuce__downy_mildew` | 37 | 8 | +29 | 67 | 7 | 8 | **82** |
| 65 | `lettuce__mosaic_virus` | 15 | 3 | +17 | 31 | 4 | 4 | **39** |
| 66 | `maple__tar_spot` | 40 | 9 | +56 | 95 | 10 | 8 | **113** |
| 67 | `peach__anthracnose` | 7 | 2 | +3 | 11 | 1 | 1 | **13** |
| 68 | `peach__brown_rot` | 65 | 14 | +73 | 137 | 15 | 14 | **166** |
| 69 | `peach__leaf_curl` | 85 | 18 | +61 | 148 | 16 | 18 | **182** |
| 70 | `peach__rust` | 3 | 1 | +3 | 6 | 1 | 1 | **8** |
| 71 | `peach__scab` | 37 | 8 | +22 | 60 | 7 | 8 | **75** |
| 72 | `plum__bacterial_spot` | 7 | 2 | +6 | 13 | 2 | 1 | **16** |
| 73 | `plum__brown_rot` | 27 | 6 | +38 | 64 | 7 | 5 | **76** |
| 74 | `plum__pocket_disease` | 20 | 4 | +29 | 48 | 5 | 4 | **57** |
| 75 | `plum__pox_virus` | 15 | 3 | +10 | 25 | 3 | 4 | **32** |
| 76 | `plum__rust` | 12 | 3 | +17 | 29 | 3 | 2 | **34** |
| 77 | `potato__early_blight` | 46 | 10 | +58 | 103 | 11 | 10 | **124** |
| 78 | `potato__late_blight` | 53 | 11 | +39 | 93 | 10 | 12 | **115** |
| 79 | `raspberry__fire_blight` | 16 | 3 | +8 | 24 | 3 | 4 | **31** |
| 80 | `raspberry__gray_mold` | 12 | 3 | +21 | 32 | 4 | 2 | **38** |
| 81 | `raspberry__leaf_spot` | 8 | 2 | +7 | 15 | 2 | 1 | **18** |
| 82 | `raspberry__yellow_rust` | 15 | 3 | +14 | 29 | 3 | 4 | **36** |
| 83 | `rice__blast` | 35 | 8 | +33 | 68 | 8 | 7 | **83** |
| 84 | `rice__sheath_blight` | 36 | 8 | +20 | 58 | 6 | 8 | **72** |
| 85 | `soybean__bacterial_blight` | 42 | 9 | +27 | 70 | 8 | 9 | **87** |
| 86 | `soybean__brown_spot` | 33 | 7 | +14 | 49 | 5 | 7 | **61** |
| 87 | `soybean__downy_mildew` | 50 | 11 | +62 | 111 | 12 | 11 | **134** |
| 88 | `soybean__frog_eye_leaf_spot` | 97 | 21 | +71 | 170 | 19 | 21 | **210** |
| 89 | `soybean__mosaic` | 62 | 13 | +27 | 92 | 10 | 13 | **115** |
| 90 | `soybean__rust` | 46 | 10 | +450 | 455 | 51 | 9 | **515** |
| 91 | `squash__powdery_mildew` | 96 | 21 | +37 | 139 | 15 | 20 | **174** |
| 92 | `strawberry__anthracnose` | 21 | 4 | +28 | 48 | 5 | 5 | **58** |
| 93 | `strawberry__leaf_scorch` | 13 | 3 | +20 | 32 | 4 | 3 | **39** |
| 94 | `tobacco__blue_mold` | 24 | 5 | +21 | 45 | 5 | 5 | **55** |
| 95 | `tobacco__brown_spot` | 32 | 7 | +16 | 49 | 6 | 7 | **62** |
| 96 | `tobacco__frogeye_leaf_spot` | 10 | 2 | +5 | 15 | 2 | 3 | **20** |
| 97 | `tobacco__mosaic_virus` | 20 | 4 | +12 | 32 | 4 | 5 | **41** |
| 98 | `tomato__bacterial_leaf_spot` | 62 | 13 | +19 | 85 | 9 | 13 | **107** |
| 99 | `tomato__early_blight` | 102 | 22 | +32 | 140 | 16 | 22 | **178** |
| 100 | `tomato__late_blight` | 82 | 18 | +46 | 131 | 15 | 17 | **163** |
| 101 | `tomato__leaf_mold` | 71 | 15 | +54 | 126 | 14 | 16 | **156** |
| 102 | `tomato__mosaic_virus` | 30 | 6 | +20 | 50 | 6 | 7 | **63** |
| 103 | `tomato__septoria_leaf_spot` | 64 | 14 | +31 | 98 | 11 | 14 | **123** |
| 104 | `tomato__yellow_leaf_curl_virus` | 41 | 9 | +30 | 72 | 8 | 9 | **89** |
| 105 | `wheat__bacterial_leaf_streak_(black_chaff)` | 57 | 12 | +33 | 92 | 10 | 13 | **115** |
| 106 | `wheat__head_scab` | 139 | 30 | +76 | 221 | 24 | 30 | **275** |
| 107 | `wheat__leaf_rust` | 51 | 11 | +55 | 105 | 12 | 11 | **128** |
| 108 | `wheat__loose_smut` | 89 | 19 | +63 | 154 | 17 | 19 | **190** |
| 109 | `wheat__powdery_mildew` | 122 | 26 | +87 | 211 | 24 | 27 | **262** |
| 110 | `wheat__septoria_blotch` | 86 | 18 | +78 | 164 | 18 | 19 | **201** |
| 111 | `wheat__stem_rust` | 58 | 12 | +53 | 111 | 12 | 13 | **136** |
| 112 | `wheat__stripe_rust` | 148 | 32 | +113 | 264 | 29 | 32 | **325** |
| 113 | `zucchini__bacterial_wilt` | 39 | 8 | +12 | 53 | 6 | 9 | **68** |
| 114 | `zucchini__downy_mildew` | 22 | 5 | +11 | 34 | 4 | 5 | **43** |
| 115 | `zucchini__powdery_mildew` | 87 | 19 | +76 | 164 | 18 | 18 | **200** |
| 116 | `zucchini__yellow_mosaic_virus` | 39 | 8 | +39 | 77 | 9 | 9 | **95** |
| **—** | **TOTAL (117 Classes)** | **10,705** | **2,295** | **+3,949** | **15,252** | **1,697** | **2,304** | **19,253** |

---

## 4. Final Validation & Quality Checklist

- [x] **117 classes represented** (116 disease classes + 1 shared healthy class)
- [x] **0 corrupted or unreadable images**
- [x] **0 train/val duplicates** (verified by SHA-256 hash audit)
- [x] **0 train/test duplicates** (verified by SHA-256 hash audit)
- [x] **0 val/test duplicates** (verified by SHA-256 hash audit)
- [x] **Original Model 2 test set 100% unchanged and immutable** (exactly 2,304 images)
- [x] **Class IDs 100% preserved** (0 to 116 identical to baseline)
- [x] **No synthetic images or artificial duplicate copies**
- [x] **Soybean rust successfully augmented** (+450 clean images, new train support = 447)
- [x] **Bean angular leaf spot safely retained from baseline** (new train support = 330)
- [x] **Healthy class 100% preserved** (zero unverified additions)
- [x] **Reproducible stratified 90/10 split** with seed `42`
- [x] **Complete source provenance preserved** in `model2_classifier_v2_manifest.csv`

---

## 5. Readiness Declaration

```
MODEL 2 DATASET READY FOR TRAINING
```