# PlantSeg v3 Final Broad Taxonomy Supplementary Extraction Report

**Date:** 2026-10-07  
**Module:** Model 2 Supplementary Dataset Curation (Full PlantSeg v3 Taxonomy Pass)  
**PlantSeg Root:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3)  
**Metadata File:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantsegv3\plantsegv3\Metadatav2.csv)  
**Output Directory:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected)  

---

## 1. Executive Summary

```
MODEL 2 TAXONOMY INSPECTED        : 117 classes (116 disease classes + 1 healthy)
PLANTSEG METADATA ROWS INSPECTED  : 11,458 records
PLANTSEG EXACT DISEASE MATCHES    : 114 classes mapped with 100% biological precision
PLANTSEG LABELS REJECTED          : 0 categories (healthy classes or non-taxonomy diseases)
PREVIOUSLY EXTRACTED IMAGES       : 11,458 images preserved without duplication
NEWLY EXTRACTED IMAGES            : +0 genuine original field images
TOTAL SUPPLEMENTARY IMAGES STAGED : 11,458 images across 114 class folders
MISSING IMAGES                    : 0 (100% verified)
```

---

## 2. Complete PlantSeg Mapping & Accounting Table

| PlantSeg disease | Model 2 class | Metadata matches | Already present | Newly copied | Missing | Final total |
|---|---|---:|---:|---:|---:|---:|
| `apple black rot` | `apple__black_rot` | 83 | 83 | 0 | 0 | **83** |
| `apple mosaic virus` | `apple__mosaic_virus` | 89 | 89 | 0 | 0 | **89** |
| `apple rust` | `apple__rust` | 139 | 139 | 0 | 0 | **139** |
| `apple scab` | `apple__scab` | 258 | 258 | 0 | 0 | **258** |
| `banana anthracnose` | `banana__anthracnose` | 71 | 71 | 0 | 0 | **71** |
| `banana black leaf streak` | `banana__black_leaf_streak` | 167 | 167 | 0 | 0 | **167** |
| `banana bunchy top` | `banana__bunchy_top` | 157 | 157 | 0 | 0 | **157** |
| `banana cigar end rot` | `banana__cigar_end_rot` | 60 | 60 | 0 | 0 | **60** |
| `banana cordana leaf spot` | `banana__cordana_leaf_spot` | 55 | 55 | 0 | 0 | **55** |
| `banana panama disease` | `banana__panama_disease` | 63 | 63 | 0 | 0 | **63** |
| `basil downy mildew` | `basil__downy_mildew` | 63 | 63 | 0 | 0 | **63** |
| `bean halo blight` | `bean__halo_blight` | 56 | 56 | 0 | 0 | **56** |
| `bean mosaic virus` | `bean__mosaic_virus` | 58 | 58 | 0 | 0 | **58** |
| `bean rust` | `bean__rust` | 233 | 233 | 0 | 0 | **233** |
| `bell pepper bacterial spot` | `bell_pepper__bacterial_spot` | 76 | 76 | 0 | 0 | **76** |
| `bell pepper blossom end rot` | `bell_pepper__blossom_end_rot` | 112 | 112 | 0 | 0 | **112** |
| `bell pepper frogeye leaf spot` | `bell_pepper__frogeye_leaf_spot` | 31 | 31 | 0 | 0 | **31** |
| `bell pepper powdery mildew` | `bell_pepper__powdery_mildew` | 28 | 28 | 0 | 0 | **28** |
| `blueberry anthracnose` | `blueberry__anthracnose` | 42 | 42 | 0 | 0 | **42** |
| `blueberry botrytis blight` | `blueberry__botrytis_blight` | 36 | 36 | 0 | 0 | **36** |
| `blueberry mummy berry` | `blueberry__mummy_berry` | 47 | 47 | 0 | 0 | **47** |
| `blueberry rust` | `blueberry__rust` | 43 | 43 | 0 | 0 | **43** |
| `blueberry scorch` | `blueberry__scorch` | 43 | 43 | 0 | 0 | **43** |
| `broccoli alternaria leaf spot` | `broccoli__alternaria_leaf_spot` | 65 | 65 | 0 | 0 | **65** |
| `broccoli downy mildew` | `broccoli__downy_mildew` | 29 | 29 | 0 | 0 | **29** |
| `broccoli ring spot` | `broccoli__ring_spot` | 16 | 16 | 0 | 0 | **16** |
| `cabbage alternaria leaf spot` | `cabbage__alternaria_leaf_spot` | 61 | 61 | 0 | 0 | **61** |
| `cabbage black rot` | `cabbage__black_rot` | 131 | 131 | 0 | 0 | **131** |
| `cabbage downy mildew` | `cabbage__downy_mildew` | 84 | 84 | 0 | 0 | **84** |
| `carrot alternaria leaf blight` | `carrot__alternaria_leaf_blight` | 60 | 60 | 0 | 0 | **60** |
| `carrot cavity spot` | `carrot__cavity_spot` | 72 | 72 | 0 | 0 | **72** |
| `carrot cercospora leaf blight` | `carrot__cercospora_leaf_blight` | 19 | 19 | 0 | 0 | **19** |
| `cauliflower alternaria leaf spot` | `cauliflower__alternaria_leaf_spot` | 54 | 54 | 0 | 0 | **54** |
| `cauliflower bacterial soft rot` | `cauliflower__bacterial_soft_rot` | 36 | 36 | 0 | 0 | **36** |
| `celery anthracnose` | `celery__anthracnose` | 29 | 29 | 0 | 0 | **29** |
| `celery early blight` | `celery__early_blight` | 36 | 36 | 0 | 0 | **36** |
| `cherry leaf spot` | `cherry__leaf_spot` | 106 | 106 | 0 | 0 | **106** |
| `cherry powdery mildew` | `cherry__powdery_mildew` | 33 | 33 | 0 | 0 | **33** |
| `citrus canker` | `citrus__canker` | 390 | 390 | 0 | 0 | **390** |
| `citrus greening disease` | `citrus__greening_disease` | 133 | 133 | 0 | 0 | **133** |
| `coffee berry blotch` | `coffee__berry_blotch` | 118 | 118 | 0 | 0 | **118** |
| `coffee black rot` | `coffee__black_rot` | 7 | 7 | 0 | 0 | **7** |
| `coffee brown eye spot` | `coffee__brown_eye_spot` | 20 | 20 | 0 | 0 | **20** |
| `coffee leaf rust` | `coffee__leaf_rust` | 159 | 159 | 0 | 0 | **159** |
| `corn gray leaf spot` | `corn__gray_leaf_spot` | 107 | 107 | 0 | 0 | **107** |
| `corn northern leaf blight` | `corn__northern_leaf_blight` | 130 | 130 | 0 | 0 | **130** |
| `corn rust` | `corn__rust` | 177 | 177 | 0 | 0 | **177** |
| `corn smut` | `corn__smut` | 202 | 202 | 0 | 0 | **202** |
| `cucumber angular leaf spot` | `cucumber__angular_leaf_spot` | 182 | 182 | 0 | 0 | **182** |
| `cucumber bacterial wilt` | `cucumber__bacterial_wilt` | 108 | 108 | 0 | 0 | **108** |
| `cucumber powdery mildew` | `cucumber__powdery_mildew` | 188 | 188 | 0 | 0 | **188** |
| `eggplant cercospora leaf spot` | `eggplant__cercospora_leaf_spot` | 60 | 60 | 0 | 0 | **60** |
| `eggplant phomopsis fruit rot` | `eggplant__phomopsis_fruit_rot` | 46 | 46 | 0 | 0 | **46** |
| `eggplant phytophthora blight` | `eggplant__phytophthora_blight` | 33 | 33 | 0 | 0 | **33** |
| `garlic leaf blight` | `garlic__leaf_blight` | 92 | 92 | 0 | 0 | **92** |
| `garlic rust` | `garlic__rust` | 106 | 106 | 0 | 0 | **106** |
| `ginger leaf spot` | `ginger__leaf_spot` | 25 | 25 | 0 | 0 | **25** |
| `ginger sheath blight` | `ginger__sheath_blight` | 68 | 68 | 0 | 0 | **68** |
| `grape black rot` | `grape__black_rot` | 122 | 122 | 0 | 0 | **122** |
| `grape downy mildew` | `grape__downy_mildew` | 280 | 280 | 0 | 0 | **280** |
| `grape leaf spot` | `grape__leaf_spot` | 91 | 91 | 0 | 0 | **91** |
| `grapevine leafroll disease` | `grape__grapevine_leafroll_disease` | 71 | 71 | 0 | 0 | **71** |
| `lettuce downy mildew` | `lettuce__downy_mildew` | 84 | 84 | 0 | 0 | **84** |
| `lettuce mosaic virus` | `lettuce__mosaic_virus` | 39 | 39 | 0 | 0 | **39** |
| `maple tar spot` | `maple__tar_spot` | 114 | 114 | 0 | 0 | **114** |
| `peach anthracnose` | `peach__anthracnose` | 13 | 13 | 0 | 0 | **13** |
| `peach brown rot` | `peach__brown_rot` | 173 | 173 | 0 | 0 | **173** |
| `peach leaf curl` | `peach__leaf_curl` | 182 | 182 | 0 | 0 | **182** |
| `peach rust` | `peach__rust` | 8 | 8 | 0 | 0 | **8** |
| `peach scab` | `peach__scab` | 78 | 78 | 0 | 0 | **78** |
| `plum bacterial spot` | `plum__bacterial_spot` | 16 | 16 | 0 | 0 | **16** |
| `plum brown rot` | `plum__brown_rot` | 81 | 81 | 0 | 0 | **81** |
| `plum pocket disease` | `plum__pocket_disease` | 57 | 57 | 0 | 0 | **57** |
| `plum pox virus` | `plum__pox_virus` | 33 | 33 | 0 | 0 | **33** |
| `plum rust` | `plum__rust` | 34 | 34 | 0 | 0 | **34** |
| `potato early blight` | `potato__early_blight` | 126 | 126 | 0 | 0 | **126** |
| `potato late blight` | `potato__late_blight` | 117 | 117 | 0 | 0 | **117** |
| `raspberry fire blight` | `raspberry__fire_blight` | 34 | 34 | 0 | 0 | **34** |
| `raspberry gray mold` | `raspberry__gray_mold` | 40 | 40 | 0 | 0 | **40** |
| `raspberry leaf spot` | `raspberry__leaf_spot` | 18 | 18 | 0 | 0 | **18** |
| `raspberry yellow rust` | `raspberry__yellow_rust` | 37 | 37 | 0 | 0 | **37** |
| `rice blast` | `rice__blast` | 83 | 83 | 0 | 0 | **83** |
| `rice sheath blight` | `rice__sheath_blight` | 76 | 76 | 0 | 0 | **76** |
| `soybean bacterial blight` | `soybean__bacterial_blight` | 91 | 91 | 0 | 0 | **91** |
| `soybean brown spot` | `soybean__brown_spot` | 71 | 71 | 0 | 0 | **71** |
| `soybean downy mildew` | `soybean__downy_mildew` | 153 | 153 | 0 | 0 | **153** |
| `soybean frog eye leaf spot` | `soybean__frog_eye_leaf_spot` | 238 | 238 | 0 | 0 | **238** |
| `soybean mosaic` | `soybean__mosaic` | 117 | 117 | 0 | 0 | **117** |
| `squash powdery mildew` | `squash__powdery_mildew` | 182 | 182 | 0 | 0 | **182** |
| `strawberry anthracnose` | `strawberry__anthracnose` | 58 | 58 | 0 | 0 | **58** |
| `strawberry leaf scorch` | `strawberry__leaf_scorch` | 39 | 39 | 0 | 0 | **39** |
| `tobacco blue mold` | `tobacco__blue_mold` | 60 | 60 | 0 | 0 | **60** |
| `tobacco brown spot` | `tobacco__brown_spot` | 66 | 66 | 0 | 0 | **66** |
| `tobacco frogeye leaf spot` | `tobacco__frogeye_leaf_spot` | 28 | 28 | 0 | 0 | **28** |
| `tobacco mosaic virus` | `tobacco__mosaic_virus` | 41 | 41 | 0 | 0 | **41** |
| `tomato bacterial leaf spot` | `tomato__bacterial_leaf_spot` | 109 | 109 | 0 | 0 | **109** |
| `tomato early blight` | `tomato__early_blight` | 187 | 187 | 0 | 0 | **187** |
| `tomato late blight` | `tomato__late_blight` | 163 | 163 | 0 | 0 | **163** |
| `tomato leaf mold` | `tomato__leaf_mold` | 156 | 156 | 0 | 0 | **156** |
| `tomato mosaic virus` | `tomato__mosaic_virus` | 63 | 63 | 0 | 0 | **63** |
| `tomato septoria leaf spot` | `tomato__septoria_leaf_spot` | 130 | 130 | 0 | 0 | **130** |
| `tomato yellow leaf curl virus` | `tomato__yellow_leaf_curl_virus` | 93 | 93 | 0 | 0 | **93** |
| `wheat bacterial leaf streak (black chaff)` | `wheat__bacterial_leaf_streak_(black_chaff)` | 117 | 117 | 0 | 0 | **117** |
| `wheat head scab` | `wheat__head_scab` | 319 | 319 | 0 | 0 | **319** |
| `wheat leaf rust` | `wheat__leaf_rust` | 132 | 132 | 0 | 0 | **132** |
| `wheat loose smut` | `wheat__loose_smut` | 215 | 215 | 0 | 0 | **215** |
| `wheat powdery mildew` | `wheat__powdery_mildew` | 271 | 271 | 0 | 0 | **271** |
| `wheat septoria blotch` | `wheat__septoria_blotch` | 232 | 232 | 0 | 0 | **232** |
| `wheat stem rust` | `wheat__stem_rust` | 148 | 148 | 0 | 0 | **148** |
| `wheat stripe rust` | `wheat__stripe_rust` | 358 | 358 | 0 | 0 | **358** |
| `zucchini bacterial wilt` | `zucchini__bacterial_wilt` | 70 | 70 | 0 | 0 | **70** |
| `zucchini downy mildew` | `zucchini__downy_mildew` | 44 | 44 | 0 | 0 | **44** |
| `zucchini powdery mildew` | `zucchini__powdery_mildew` | 213 | 213 | 0 | 0 | **213** |
| `zucchini yellow mosaic virus` | `zucchini__yellow_mosaic_virus` | 95 | 95 | 0 | 0 | **95** |
| **TOTAL (114 classes)** | **—** | **11,458** | **11,458** | **0** | **0** | **11,458** |

---

## 3. Model 2 Taxonomy Coverage (All 116 Disease Classes)

| Model 2 class | PlantSeg source found? | Images added |
|---|:---:|---:|
| `apple__black_rot` | Yes (`apple black rot`) | 83 |
| `apple__mosaic_virus` | Yes (`apple mosaic virus`) | 89 |
| `apple__rust` | Yes (`apple rust`) | 139 |
| `apple__scab` | Yes (`apple scab`) | 258 |
| `banana__anthracnose` | Yes (`banana anthracnose`) | 71 |
| `banana__black_leaf_streak` | Yes (`banana black leaf streak`) | 167 |
| `banana__bunchy_top` | Yes (`banana bunchy top`) | 157 |
| `banana__cigar_end_rot` | Yes (`banana cigar end rot`) | 60 |
| `banana__cordana_leaf_spot` | Yes (`banana cordana leaf spot`) | 55 |
| `banana__panama_disease` | Yes (`banana panama disease`) | 63 |
| `basil__downy_mildew` | Yes (`basil downy mildew`) | 63 |
| `bean__angular_leaf_spot` | No | 0 |
| `bean__halo_blight` | Yes (`bean halo blight`) | 56 |
| `bean__mosaic_virus` | Yes (`bean mosaic virus`) | 58 |
| `bean__rust` | Yes (`bean rust`) | 233 |
| `bell_pepper__bacterial_spot` | Yes (`bell pepper bacterial spot`) | 76 |
| `bell_pepper__blossom_end_rot` | Yes (`bell pepper blossom end rot`) | 112 |
| `bell_pepper__frogeye_leaf_spot` | Yes (`bell pepper frogeye leaf spot`) | 31 |
| `bell_pepper__powdery_mildew` | Yes (`bell pepper powdery mildew`) | 28 |
| `blueberry__anthracnose` | Yes (`blueberry anthracnose`) | 42 |
| `blueberry__botrytis_blight` | Yes (`blueberry botrytis blight`) | 36 |
| `blueberry__mummy_berry` | Yes (`blueberry mummy berry`) | 47 |
| `blueberry__rust` | Yes (`blueberry rust`) | 43 |
| `blueberry__scorch` | Yes (`blueberry scorch`) | 43 |
| `broccoli__alternaria_leaf_spot` | Yes (`broccoli alternaria leaf spot`) | 65 |
| `broccoli__downy_mildew` | Yes (`broccoli downy mildew`) | 29 |
| `broccoli__ring_spot` | Yes (`broccoli ring spot`) | 16 |
| `cabbage__alternaria_leaf_spot` | Yes (`cabbage alternaria leaf spot`) | 61 |
| `cabbage__black_rot` | Yes (`cabbage black rot`) | 131 |
| `cabbage__downy_mildew` | Yes (`cabbage downy mildew`) | 84 |
| `carrot__alternaria_leaf_blight` | Yes (`carrot alternaria leaf blight`) | 60 |
| `carrot__cavity_spot` | Yes (`carrot cavity spot`) | 72 |
| `carrot__cercospora_leaf_blight` | Yes (`carrot cercospora leaf blight`) | 19 |
| `cauliflower__alternaria_leaf_spot` | Yes (`cauliflower alternaria leaf spot`) | 54 |
| `cauliflower__bacterial_soft_rot` | Yes (`cauliflower bacterial soft rot`) | 36 |
| `celery__anthracnose` | Yes (`celery anthracnose`) | 29 |
| `celery__early_blight` | Yes (`celery early blight`) | 36 |
| `cherry__leaf_spot` | Yes (`cherry leaf spot`) | 106 |
| `cherry__powdery_mildew` | Yes (`cherry powdery mildew`) | 33 |
| `citrus__canker` | Yes (`citrus canker`) | 390 |
| `citrus__greening_disease` | Yes (`citrus greening disease`) | 133 |
| `coffee__berry_blotch` | Yes (`coffee berry blotch`) | 118 |
| `coffee__black_rot` | Yes (`coffee black rot`) | 7 |
| `coffee__brown_eye_spot` | Yes (`coffee brown eye spot`) | 20 |
| `coffee__leaf_rust` | Yes (`coffee leaf rust`) | 159 |
| `corn__gray_leaf_spot` | Yes (`corn gray leaf spot`) | 107 |
| `corn__northern_leaf_blight` | Yes (`corn northern leaf blight`) | 130 |
| `corn__rust` | Yes (`corn rust`) | 177 |
| `corn__smut` | Yes (`corn smut`) | 202 |
| `cucumber__angular_leaf_spot` | Yes (`cucumber angular leaf spot`) | 182 |
| `cucumber__bacterial_wilt` | Yes (`cucumber bacterial wilt`) | 108 |
| `cucumber__powdery_mildew` | Yes (`cucumber powdery mildew`) | 188 |
| `eggplant__cercospora_leaf_spot` | Yes (`eggplant cercospora leaf spot`) | 60 |
| `eggplant__phomopsis_fruit_rot` | Yes (`eggplant phomopsis fruit rot`) | 46 |
| `eggplant__phytophthora_blight` | Yes (`eggplant phytophthora blight`) | 33 |
| `garlic__leaf_blight` | Yes (`garlic leaf blight`) | 92 |
| `garlic__rust` | Yes (`garlic rust`) | 106 |
| `ginger__leaf_spot` | Yes (`ginger leaf spot`) | 25 |
| `ginger__sheath_blight` | Yes (`ginger sheath blight`) | 68 |
| `grape__black_rot` | Yes (`grape black rot`) | 122 |
| `grape__downy_mildew` | Yes (`grape downy mildew`) | 280 |
| `grape__grapevine_leafroll_disease` | Yes (`grapevine leafroll disease`) | 71 |
| `grape__leaf_spot` | Yes (`grape leaf spot`) | 91 |
| `lettuce__downy_mildew` | Yes (`lettuce downy mildew`) | 84 |
| `lettuce__mosaic_virus` | Yes (`lettuce mosaic virus`) | 39 |
| `maple__tar_spot` | Yes (`maple tar spot`) | 114 |
| `peach__anthracnose` | Yes (`peach anthracnose`) | 13 |
| `peach__brown_rot` | Yes (`peach brown rot`) | 173 |
| `peach__leaf_curl` | Yes (`peach leaf curl`) | 182 |
| `peach__rust` | Yes (`peach rust`) | 8 |
| `peach__scab` | Yes (`peach scab`) | 78 |
| `plum__bacterial_spot` | Yes (`plum bacterial spot`) | 16 |
| `plum__brown_rot` | Yes (`plum brown rot`) | 81 |
| `plum__pocket_disease` | Yes (`plum pocket disease`) | 57 |
| `plum__pox_virus` | Yes (`plum pox virus`) | 33 |
| `plum__rust` | Yes (`plum rust`) | 34 |
| `potato__early_blight` | Yes (`potato early blight`) | 126 |
| `potato__late_blight` | Yes (`potato late blight`) | 117 |
| `raspberry__fire_blight` | Yes (`raspberry fire blight`) | 34 |
| `raspberry__gray_mold` | Yes (`raspberry gray mold`) | 40 |
| `raspberry__leaf_spot` | Yes (`raspberry leaf spot`) | 18 |
| `raspberry__yellow_rust` | Yes (`raspberry yellow rust`) | 37 |
| `rice__blast` | Yes (`rice blast`) | 83 |
| `rice__sheath_blight` | Yes (`rice sheath blight`) | 76 |
| `soybean__bacterial_blight` | Yes (`soybean bacterial blight`) | 91 |
| `soybean__brown_spot` | Yes (`soybean brown spot`) | 71 |
| `soybean__downy_mildew` | Yes (`soybean downy mildew`) | 153 |
| `soybean__frog_eye_leaf_spot` | Yes (`soybean frog eye leaf spot`) | 238 |
| `soybean__mosaic` | Yes (`soybean mosaic`) | 117 |
| `soybean__rust` | No | 0 |
| `squash__powdery_mildew` | Yes (`squash powdery mildew`) | 182 |
| `strawberry__anthracnose` | Yes (`strawberry anthracnose`) | 58 |
| `strawberry__leaf_scorch` | Yes (`strawberry leaf scorch`) | 39 |
| `tobacco__blue_mold` | Yes (`tobacco blue mold`) | 60 |
| `tobacco__brown_spot` | Yes (`tobacco brown spot`) | 66 |
| `tobacco__frogeye_leaf_spot` | Yes (`tobacco frogeye leaf spot`) | 28 |
| `tobacco__mosaic_virus` | Yes (`tobacco mosaic virus`) | 41 |
| `tomato__bacterial_leaf_spot` | Yes (`tomato bacterial leaf spot`) | 109 |
| `tomato__early_blight` | Yes (`tomato early blight`) | 187 |
| `tomato__late_blight` | Yes (`tomato late blight`) | 163 |
| `tomato__leaf_mold` | Yes (`tomato leaf mold`) | 156 |
| `tomato__mosaic_virus` | Yes (`tomato mosaic virus`) | 63 |
| `tomato__septoria_leaf_spot` | Yes (`tomato septoria leaf spot`) | 130 |
| `tomato__yellow_leaf_curl_virus` | Yes (`tomato yellow leaf curl virus`) | 93 |
| `wheat__bacterial_leaf_streak_(black_chaff)` | Yes (`wheat bacterial leaf streak (black chaff)`) | 117 |
| `wheat__head_scab` | Yes (`wheat head scab`) | 319 |
| `wheat__leaf_rust` | Yes (`wheat leaf rust`) | 132 |
| `wheat__loose_smut` | Yes (`wheat loose smut`) | 215 |
| `wheat__powdery_mildew` | Yes (`wheat powdery mildew`) | 271 |
| `wheat__septoria_blotch` | Yes (`wheat septoria blotch`) | 232 |
| `wheat__stem_rust` | Yes (`wheat stem rust`) | 148 |
| `wheat__stripe_rust` | Yes (`wheat stripe rust`) | 358 |
| `zucchini__bacterial_wilt` | Yes (`zucchini bacterial wilt`) | 70 |
| `zucchini__downy_mildew` | Yes (`zucchini downy mildew`) | 44 |
| `zucchini__powdery_mildew` | Yes (`zucchini powdery mildew`) | 213 |
| `zucchini__yellow_mosaic_virus` | Yes (`zucchini yellow mosaic virus`) | 95 |
| **TOTAL (116 Disease Classes)** | **114 / 116 Found** | **11,458** |

---

## 4. Split Breakdown per Extracted Class

| Model 2 Class | Output Folder | Training | Validation | Test | Total |
|---|---|---:|---:|---:|---:|
| `apple__black_rot` | `apple_black_rot` | 57 | 9 | 17 | **83** |
| `apple__mosaic_virus` | `apple_mosaic_virus` | 61 | 10 | 18 | **89** |
| `apple__rust` | `apple_rust` | 96 | 15 | 28 | **139** |
| `apple__scab` | `apple_scab` | 179 | 27 | 52 | **258** |
| `banana__anthracnose` | `banana_anthracnose` | 49 | 8 | 14 | **71** |
| `banana__black_leaf_streak` | `banana_black_leaf_streak` | 116 | 18 | 33 | **167** |
| `banana__bunchy_top` | `banana_bunchy_top` | 109 | 17 | 31 | **157** |
| `banana__cigar_end_rot` | `banana_cigar_end_rot` | 41 | 7 | 12 | **60** |
| `banana__cordana_leaf_spot` | `banana_cordana_leaf_spot` | 38 | 6 | 11 | **55** |
| `banana__panama_disease` | `banana_panama_disease` | 43 | 7 | 13 | **63** |
| `basil__downy_mildew` | `basil_downy_mildew` | 43 | 7 | 13 | **63** |
| `bean__halo_blight` | `bean_halo_blight` | 39 | 6 | 11 | **56** |
| `bean__mosaic_virus` | `bean_mosaic_virus` | 40 | 6 | 12 | **58** |
| `bean__rust` | `bean_rust` | 161 | 25 | 47 | **233** |
| `bell_pepper__bacterial_spot` | `bell_pepper_bacterial_spot` | 53 | 8 | 15 | **76** |
| `bell_pepper__blossom_end_rot` | `bell_pepper_blossom_end_rot` | 78 | 12 | 22 | **112** |
| `bell_pepper__frogeye_leaf_spot` | `bell_pepper_frogeye_leaf_spot` | 21 | 4 | 6 | **31** |
| `bell_pepper__powdery_mildew` | `bell_pepper_powdery_mildew` | 19 | 3 | 6 | **28** |
| `blueberry__anthracnose` | `blueberry_anthracnose` | 29 | 5 | 8 | **42** |
| `blueberry__botrytis_blight` | `blueberry_botrytis_blight` | 25 | 4 | 7 | **36** |
| `blueberry__mummy_berry` | `blueberry_mummy_berry` | 33 | 5 | 9 | **47** |
| `blueberry__rust` | `blueberry_rust` | 29 | 5 | 9 | **43** |
| `blueberry__scorch` | `blueberry_scorch` | 29 | 5 | 9 | **43** |
| `broccoli__alternaria_leaf_spot` | `broccoli_alternaria_leaf_spot` | 45 | 7 | 13 | **65** |
| `broccoli__downy_mildew` | `broccoli_downy_mildew` | 20 | 3 | 6 | **29** |
| `broccoli__ring_spot` | `broccoli_ring_spot` | 11 | 2 | 3 | **16** |
| `cabbage__alternaria_leaf_spot` | `cabbage_alternaria_leaf_spot` | 41 | 7 | 13 | **61** |
| `cabbage__black_rot` | `cabbage_black_rot` | 91 | 14 | 26 | **131** |
| `cabbage__downy_mildew` | `cabbage_downy_mildew` | 58 | 9 | 17 | **84** |
| `carrot__alternaria_leaf_blight` | `carrot_alternaria_leaf_blight` | 41 | 7 | 12 | **60** |
| `carrot__cavity_spot` | `carrot_cavity_spot` | 50 | 8 | 14 | **72** |
| `carrot__cercospora_leaf_blight` | `carrot_cercospora_leaf_blight` | 13 | 2 | 4 | **19** |
| `cauliflower__alternaria_leaf_spot` | `cauliflower_alternaria_leaf_spot` | 37 | 6 | 11 | **54** |
| `cauliflower__bacterial_soft_rot` | `cauliflower_bacterial_soft_rot` | 25 | 4 | 7 | **36** |
| `celery__anthracnose` | `celery_anthracnose` | 20 | 3 | 6 | **29** |
| `celery__early_blight` | `celery_early_blight` | 25 | 4 | 7 | **36** |
| `cherry__leaf_spot` | `cherry_leaf_spot` | 73 | 12 | 21 | **106** |
| `cherry__powdery_mildew` | `cherry_powdery_mildew` | 22 | 4 | 7 | **33** |
| `citrus__canker` | `citrus_canker` | 271 | 41 | 78 | **390** |
| `citrus__greening_disease` | `citrus_greening_disease` | 92 | 14 | 27 | **133** |
| `coffee__berry_blotch` | `coffee_berry_blotch` | 81 | 13 | 24 | **118** |
| `coffee__black_rot` | `coffee_black_rot` | 5 | 1 | 1 | **7** |
| `coffee__brown_eye_spot` | `coffee_brown_eye_spot` | 13 | 3 | 4 | **20** |
| `coffee__leaf_rust` | `coffee_leaf_rust` | 110 | 17 | 32 | **159** |
| `corn__gray_leaf_spot` | `corn_gray_leaf_spot` | 74 | 12 | 21 | **107** |
| `corn__northern_leaf_blight` | `corn_northern_leaf_blight` | 90 | 14 | 26 | **130** |
| `corn__rust` | `corn_rust` | 123 | 19 | 35 | **177** |
| `corn__smut` | `corn_smut` | 140 | 22 | 40 | **202** |
| `cucumber__angular_leaf_spot` | `cucumber_angular_leaf_spot` | 128 | 18 | 36 | **182** |
| `cucumber__bacterial_wilt` | `cucumber_bacterial_wilt` | 72 | 14 | 22 | **108** |
| `cucumber__powdery_mildew` | `cucumber_powdery_mildew` | 130 | 20 | 38 | **188** |
| `eggplant__cercospora_leaf_spot` | `eggplant_cercospora_leaf_spot` | 41 | 7 | 12 | **60** |
| `eggplant__phomopsis_fruit_rot` | `eggplant_phomopsis_fruit_rot` | 32 | 5 | 9 | **46** |
| `eggplant__phytophthora_blight` | `eggplant_phytophthora_blight` | 22 | 4 | 7 | **33** |
| `garlic__leaf_blight` | `garlic_leaf_blight` | 64 | 10 | 18 | **92** |
| `garlic__rust` | `garlic_rust` | 73 | 12 | 21 | **106** |
| `ginger__leaf_spot` | `ginger_leaf_spot` | 17 | 3 | 5 | **25** |
| `ginger__sheath_blight` | `ginger_sheath_blight` | 46 | 8 | 14 | **68** |
| `grape__black_rot` | `grape_black_rot` | 85 | 13 | 24 | **122** |
| `grape__downy_mildew` | `grape_downy_mildew` | 194 | 30 | 56 | **280** |
| `grape__leaf_spot` | `grape_leaf_spot` | 63 | 10 | 18 | **91** |
| `grape__grapevine_leafroll_disease` | `grape_grapevine_leafroll_disease` | 49 | 8 | 14 | **71** |
| `lettuce__downy_mildew` | `lettuce_downy_mildew` | 58 | 9 | 17 | **84** |
| `lettuce__mosaic_virus` | `lettuce_mosaic_virus` | 26 | 5 | 8 | **39** |
| `maple__tar_spot` | `maple_tar_spot` | 79 | 12 | 23 | **114** |
| `peach__anthracnose` | `peach_anthracnose` | 8 | 2 | 3 | **13** |
| `peach__brown_rot` | `peach_brown_rot` | 120 | 18 | 35 | **173** |
| `peach__leaf_curl` | `peach_leaf_curl` | 127 | 19 | 36 | **182** |
| `peach__rust` | `peach_rust` | 5 | 1 | 2 | **8** |
| `peach__scab` | `peach_scab` | 53 | 9 | 16 | **78** |
| `plum__bacterial_spot` | `plum_bacterial_spot` | 11 | 2 | 3 | **16** |
| `plum__brown_rot` | `plum_brown_rot` | 56 | 9 | 16 | **81** |
| `plum__pocket_disease` | `plum_pocket_disease` | 40 | 6 | 11 | **57** |
| `plum__pox_virus` | `plum_pox_virus` | 22 | 4 | 7 | **33** |
| `plum__rust` | `plum_rust` | 23 | 4 | 7 | **34** |
| `potato__early_blight` | `potato_early_blight` | 87 | 14 | 25 | **126** |
| `potato__late_blight` | `potato_late_blight` | 81 | 13 | 23 | **117** |
| `raspberry__fire_blight` | `raspberry_fire_blight` | 23 | 4 | 7 | **34** |
| `raspberry__gray_mold` | `raspberry_gray_mold` | 27 | 5 | 8 | **40** |
| `raspberry__leaf_spot` | `raspberry_leaf_spot` | 13 | 2 | 3 | **18** |
| `raspberry__yellow_rust` | `raspberry_yellow_rust` | 26 | 4 | 7 | **37** |
| `rice__blast` | `rice_blast` | 57 | 9 | 17 | **83** |
| `rice__sheath_blight` | `rice_sheath_blight` | 53 | 8 | 15 | **76** |
| `soybean__bacterial_blight` | `soybean_bacterial_blight` | 63 | 10 | 18 | **91** |
| `soybean__brown_spot` | `soybean_brown_spot` | 49 | 8 | 14 | **71** |
| `soybean__downy_mildew` | `soybean_downy_mildew` | 106 | 16 | 31 | **153** |
| `soybean__frog_eye_leaf_spot` | `soybean_frog_eye_leaf_spot` | 165 | 25 | 48 | **238** |
| `soybean__mosaic` | `soybean_mosaic` | 81 | 13 | 23 | **117** |
| `squash__powdery_mildew` | `squash_powdery_mildew` | 127 | 19 | 36 | **182** |
| `strawberry__anthracnose` | `strawberry_anthracnose` | 40 | 6 | 12 | **58** |
| `strawberry__leaf_scorch` | `strawberry_leaf_scorch` | 26 | 5 | 8 | **39** |
| `tobacco__blue_mold` | `tobacco_blue_mold` | 41 | 7 | 12 | **60** |
| `tobacco__brown_spot` | `tobacco_brown_spot` | 46 | 7 | 13 | **66** |
| `tobacco__frogeye_leaf_spot` | `tobacco_frogeye_leaf_spot` | 19 | 3 | 6 | **28** |
| `tobacco__mosaic_virus` | `tobacco_mosaic_virus` | 28 | 5 | 8 | **41** |
| `tomato__bacterial_leaf_spot` | `tomato_bacterial_leaf_spot` | 75 | 12 | 22 | **109** |
| `tomato__early_blight` | `tomato_early_blight` | 130 | 20 | 37 | **187** |
| `tomato__late_blight` | `tomato_late_blight` | 113 | 17 | 33 | **163** |
| `tomato__leaf_mold` | `tomato_leaf_mold` | 108 | 17 | 31 | **156** |
| `tomato__mosaic_virus` | `tomato_mosaic_virus` | 43 | 7 | 13 | **63** |
| `tomato__septoria_leaf_spot` | `tomato_septoria_leaf_spot` | 90 | 14 | 26 | **130** |
| `tomato__yellow_leaf_curl_virus` | `tomato_yellow_leaf_curl_virus` | 64 | 10 | 19 | **93** |
| `wheat__bacterial_leaf_streak_(black_chaff)` | `wheat_bacterial_leaf_streak_(black_chaff)` | 81 | 13 | 23 | **117** |
| `wheat__head_scab` | `wheat_head_scab` | 221 | 34 | 64 | **319** |
| `wheat__leaf_rust` | `wheat_leaf_rust` | 92 | 14 | 26 | **132** |
| `wheat__loose_smut` | `wheat_loose_smut` | 149 | 23 | 43 | **215** |
| `wheat__powdery_mildew` | `wheat_powdery_mildew` | 188 | 29 | 54 | **271** |
| `wheat__septoria_blotch` | `wheat_septoria_blotch` | 161 | 25 | 46 | **232** |
| `wheat__stem_rust` | `wheat_stem_rust` | 102 | 16 | 30 | **148** |
| `wheat__stripe_rust` | `wheat_stripe_rust` | 248 | 38 | 72 | **358** |
| `zucchini__bacterial_wilt` | `zucchini_bacterial_wilt` | 47 | 8 | 15 | **70** |
| `zucchini__downy_mildew` | `zucchini_downy_mildew` | 30 | 5 | 9 | **44** |
| `zucchini__powdery_mildew` | `zucchini_powdery_mildew` | 147 | 23 | 43 | **213** |
| `zucchini__yellow_mosaic_virus` | `zucchini_yellow_mosaic_virus` | 66 | 10 | 19 | **95** |
| **TOTAL** | **[`plantseg_selected/`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external\model2_supplementary\plantseg_selected)** | **7,916** | **1,247** | **2,295** | **11,458** |

---

## 5. Rejected PlantSeg Categories and Rationale

| PlantSeg Disease | Plant | Image Count | Rejection Rationale |
|---|---|---:|---|

---

## 6. SHA-256 Duplicate Auditing

- **Total Class Folders Analyzed:** 114
- **Classes with 100% Unique Images:** 68
- **Classes with Source Duplicate Pairs in PlantSeg:** 46 (268 duplicate groups logged)
- **Action Taken on Duplicates:** Reported in audit logs per project rules; raw binary files preserved without automatic deletion.

### Duplicate Groups Detail:

**Class:** `banana__anthracnose` (2 duplicate groups):
- SHA256 `7d62cf4dc932813a...`: `banana_anthracnose_Bing_0023.jpg, banana_anthracnose_Bing_0075.jpg`
- SHA256 `6024dec6ce5795b1...`: `banana_anthracnose_Bing_0065.jpg, banana_anthracnose_Bing_0300.jpg`

**Class:** `banana__black_leaf_streak` (8 duplicate groups):
- SHA256 `0524ce389fce3d51...`: `banana_black_leaf_streak_banana black sigatoka (101).jpg, banana_black_leaf_streak_banana black sigatoka (51).jpg`
- SHA256 `675256ba1c19fa8e...`: `banana_black_leaf_streak_banana black sigatoka (28).jpg, banana_black_leaf_streak_Bing_0015.jpg`
- SHA256 `81af2d459d31fc83...`: `banana_black_leaf_streak_banana black sigatoka (30).jpg, banana_black_leaf_streak_Bing_0005.jpg`
- SHA256 `9f744664e14d44e8...`: `banana_black_leaf_streak_banana black sigatoka (52).jpg, banana_black_leaf_streak_Bing_0026.jpg`
- SHA256 `6e8310a4ec7d7adf...`: `banana_black_leaf_streak_banana black sigatoka (54).jpg, banana_black_leaf_streak_Bing_0013.jpg`
- SHA256 `ecb15f7fafbed721...`: `banana_black_leaf_streak_banana black sigatoka (7).jpg, banana_black_leaf_streak_Bing_0046.jpg`
- SHA256 `d24499e36f9b4ae2...`: `banana_black_leaf_streak_banana black sigatoka (9).jpg, banana_black_leaf_streak_Bing_0056.jpg`
- SHA256 `b32fbb83449c17e8...`: `banana_black_leaf_streak_Bing_0018.jpg, banana_black_leaf_streak_Bing_0081.jpg`

**Class:** `banana__bunchy_top` (14 duplicate groups):
- SHA256 `961ed7b7eaaa9cb4...`: `banana_bunchy_top_Bing_0006.jpg, banana_bunchy_top_Bing_0298.jpg`
- SHA256 `06607a91d7c81f94...`: `banana_bunchy_top_Bing_0020.jpg, banana_bunchy_top_Bing_0062.jpg, banana_bunchy_top_Bing_0165.jpg`
- SHA256 `bc7243e2f445950b...`: `banana_bunchy_top_Bing_0026.jpg, banana_bunchy_top_Bing_0247.jpg`
- SHA256 `22704d3a14f51578...`: `banana_bunchy_top_Bing_0037.jpg, banana_bunchy_top_Bing_0276.jpg`
- SHA256 `03dd0c5dbbc15124...`: `banana_bunchy_top_Bing_0045.jpg, banana_bunchy_top_Google_0031.jpg`
- SHA256 `e35fbc7e873cf5bb...`: `banana_bunchy_top_Bing_0052.jpg, banana_bunchy_top_Bing_0335.jpg`
- SHA256 `407e39fa70162ffd...`: `banana_bunchy_top_Bing_0083.jpg, banana_bunchy_top_Bing_0334.jpg`
- SHA256 `119a1ae691e9d37a...`: `banana_bunchy_top_Bing_0100.jpg, banana_bunchy_top_Bing_0168.jpg`
- SHA256 `dd946c3d0f3e2e94...`: `banana_bunchy_top_Bing_0122.jpg, banana_bunchy_top_Bing_0245.jpg`
- SHA256 `186495fb393c7c4f...`: `banana_bunchy_top_Bing_0137.jpg, banana_bunchy_top_Bing_0343.jpg`
- SHA256 `f00c4865b7b4d8dd...`: `banana_bunchy_top_Bing_0140.jpg, banana_bunchy_top_Bing_0338.jpg`
- SHA256 `6799cd9660ab9882...`: `banana_bunchy_top_Bing_0141.jpg, banana_bunchy_top_Bing_0347.jpg`
- SHA256 `e1c4e64914371948...`: `banana_bunchy_top_Bing_0152.jpg, banana_bunchy_top_Bing_0189.jpg`
- SHA256 `a94583c63ddd7110...`: `banana_bunchy_top_Bing_0242.jpg, banana_bunchy_top_Bing_0345.jpg`

**Class:** `banana__cigar_end_rot` (3 duplicate groups):
- SHA256 `ebf5e213faaa2529...`: `banana_cigar_end_rot_Bing_0002.jpg, banana_cigar_end_rot_Google_0010.jpg`
- SHA256 `be56e2890ed4a64d...`: `banana_cigar_end_rot_Bing_0004.jpg, banana_cigar_end_rot_Google_0018.jpg`
- SHA256 `5124643baf78a597...`: `banana_cigar_end_rot_Bing_0011.jpg, banana_cigar_end_rot_Google_0035.jpg`

**Class:** `banana__cordana_leaf_spot` (1 duplicate groups):
- SHA256 `17742b314aec28f2...`: `banana_cordana_leaf_spot_Bing_0005.jpg, banana_cordana_leaf_spot_Google_0014.jpg`

**Class:** `bean__rust` (2 duplicate groups):
- SHA256 `a9fc7f6e0824643a...`: `bean_rust_google_0030.jpg, bean_rust_google_0130.jpg`
- SHA256 `bbba9e6f3b76e3c4...`: `soybean_rust_Bing_0098.jpg, soybean_rust_Google_0010.jpg`

**Class:** `bell_pepper__bacterial_spot` (5 duplicate groups):
- SHA256 `5457c3b0666c34bb...`: `bell_pepper_bacterial_spot_Bing_0000.jpg, bell_pepper_bacterial_spot_Google_0000.jpg`
- SHA256 `d83782be7b8f7d01...`: `bell_pepper_bacterial_spot_Bing_0009.jpg, bell_pepper_bacterial_spot_Google_0024.jpg`
- SHA256 `561e96f43289397f...`: `bell_pepper_bacterial_spot_Bing_0013.jpg, bell_pepper_bacterial_spot_Google_0004.jpg`
- SHA256 `6f61d060d71a11bb...`: `bell_pepper_bacterial_spot_Bing_0069.jpg, bell_pepper_bacterial_spot_Google_0160.jpg`
- SHA256 `e40b71a1fb3cc798...`: `bell_pepper_bacterial_spot_Bing_0108.jpg, bell_pepper_bacterial_spot_Google_0008.jpg`

**Class:** `bell_pepper__blossom_end_rot` (3 duplicate groups):
- SHA256 `b96993d3eb430f4c...`: `bell_pepper_blossom_end_rot_Bing_0003.jpg, bell_pepper_blossom_end_rot_Google_0006.jpg`
- SHA256 `a78e7a95f9647ab5...`: `bell_pepper_blossom_end_rot_Bing_0008.jpg, bell_pepper_blossom_end_rot_Google_0038.jpg`
- SHA256 `6530dc6dd127b2e1...`: `bell_pepper_blossom_end_rot_Bing_0143.jpg, bell_pepper_blossom_end_rot_Google_0294.jpg`

**Class:** `bell_pepper__frogeye_leaf_spot` (1 duplicate groups):
- SHA256 `f5d88f2e7ceb8d14...`: `bell_pepper_frogeye_leaf_spot_Bing_0000.jpg, bell_pepper_frogeye_leaf_spot_Google_0000.jpg`

**Class:** `bell_pepper__powdery_mildew` (1 duplicate groups):
- SHA256 `6daa9c21978fa4e2...`: `bell_pepper_powdery_mildew_Bing_0062.jpg, bell_pepper_powdery_mildew_Google_0012.jpg`

**Class:** `blueberry__anthracnose` (2 duplicate groups):
- SHA256 `7bb80f8acb4bd670...`: `blueberry_anthracnose_Bing_0000.jpg, blueberry_anthracnose_Google_0003.jpg`
- SHA256 `3cfe9b0db6b7840b...`: `blueberry_anthracnose_Bing_0055.jpg, blueberry_anthracnose_Google_0011.jpg`

**Class:** `blueberry__mummy_berry` (1 duplicate groups):
- SHA256 `2ba7020988730724...`: `blueberry_mummy_berry_Bing_0001.jpg, blueberry_mummy_berry_Bing_0058.jpg`

**Class:** `blueberry__scorch` (1 duplicate groups):
- SHA256 `0450f9a79064689b...`: `blueberry_scorch_Bing_0011.jpg, blueberry_scorch_Google_0081.jpg`

**Class:** `broccoli__alternaria_leaf_spot` (3 duplicate groups):
- SHA256 `9e76111c1935b6c8...`: `broccoli_alternaria_leaf_spot_Bing_0005.jpg, broccoli_alternaria_leaf_spot_Google_0007.jpg`
- SHA256 `f65c539e6c72585f...`: `broccoli_alternaria_leaf_spot_Bing_0012.jpg, broccoli_alternaria_leaf_spot_Google_0005.jpg`
- SHA256 `9a3243f4fd667100...`: `broccoli_alternaria_leaf_spot_Bing_0021.jpg, broccoli_alternaria_leaf_spot_Google_0278.jpg`

**Class:** `cabbage__black_rot` (8 duplicate groups):
- SHA256 `f0ed2a1742def762...`: `cabbage_black_rot_Bing_0012.jpg, cabbage_black_rot_Google_0049.jpg`
- SHA256 `95089ffa12dba9d6...`: `cabbage_black_rot_Bing_0013.jpg, cabbage_black_rot_Google_0110.jpg`
- SHA256 `5fe0430076ef0207...`: `cabbage_black_rot_Bing_0015.jpg, cabbage_black_rot_Google_0232.jpg`
- SHA256 `2622b21bbbaf19f1...`: `cabbage_black_rot_Bing_0042.jpg, cabbage_black_rot_Google_0341.jpg`
- SHA256 `429d93a47f9f80f0...`: `cabbage_black_rot_Bing_0062.jpg, cabbage_black_rot_Google_0205.jpg`
- SHA256 `378a54972792a471...`: `cabbage_black_rot_Bing_0149.jpg, cabbage_black_rot_Google_0208.jpg`
- SHA256 `9dca1e4a36b8df6f...`: `cabbage_black_rot_Bing_0178.jpg, cabbage_black_rot_Google_0247.jpg`
- SHA256 `1f13d43c8e62b145...`: `cabbage_black_rot_Bing_0211.jpg, cabbage_black_rot_Google_0030.jpg`

**Class:** `cauliflower__alternaria_leaf_spot` (1 duplicate groups):
- SHA256 `63cb52dde7926073...`: `cauliflower_alternaria_leaf_spot_170.jpg, cauliflower_alternaria_leaf_spot_9.jpg`

**Class:** `cauliflower__bacterial_soft_rot` (2 duplicate groups):
- SHA256 `e192634293b1692f...`: `cauliflower_bacterial_soft_rot_Bing_0016.jpg, cauliflower_bacterial_soft_rot_Google_0016.jpg`
- SHA256 `5fdb4d7efe18022e...`: `cauliflower_bacterial_soft_rot_Bing_0082.jpg, cauliflower_bacterial_soft_rot_Google_0013.jpg`

**Class:** `citrus__canker` (2 duplicate groups):
- SHA256 `4d6953efee6a27c9...`: `citrus_canker_276.jpg, citrus_canker_279.jpg`
- SHA256 `7f269a3b6ec36e1e...`: `citrus_canker_306.jpg, citrus_canker_308.jpg`

**Class:** `coffee__berry_blotch` (5 duplicate groups):
- SHA256 `95dbe9adedfd8fbe...`: `coffee_berry_blotch_Bing_0000.jpg, coffee_berry_blotch_Google_0016.jpg`
- SHA256 `4ba1f54533f20ad9...`: `coffee_berry_blotch_Bing_0003.jpg, coffee_berry_blotch_Google_0044.jpg`
- SHA256 `83546f1456df3b55...`: `coffee_berry_blotch_Bing_0036.jpg, coffee_berry_blotch_Google_0010.jpg`
- SHA256 `e6f2799f11ddb148...`: `coffee_berry_blotch_Bing_0049.jpg, coffee_berry_blotch_Google_0021.jpg`
- SHA256 `514567eefd8e7785...`: `coffee_berry_blotch_Bing_0150.jpg, coffee_berry_blotch_Google_0034.jpg`

**Class:** `coffee__brown_eye_spot` (1 duplicate groups):
- SHA256 `56f7ba0b322b1331...`: `coffee_brown_eye_spot_Bing_0006.jpg, coffee_brown_eye_spot_Google_0034.jpg`

**Class:** `grape__downy_mildew` (2 duplicate groups):
- SHA256 `8bebefbf5af250d1...`: `grape_downy_mildew_102.jpg, grape_downy_mildew_216.jpg`
- SHA256 `a1dd65509a5675c5...`: `grape_downy_mildew_122.jpg, grape_downy_mildew_241.jpg`

**Class:** `peach__brown_rot` (3 duplicate groups):
- SHA256 `059966346805f04d...`: `peach_brown_rot_Bing_0029.jpg, peach_brown_rot_Google_0128.jpg`
- SHA256 `02b5841337ecf9d0...`: `peach_brown_rot_Bing_0070.jpg, peach_brown_rot_Google_0110.jpg`
- SHA256 `c7b1843cde13b9fa...`: `peach_brown_rot_Bing_0232.jpg, peach_brown_rot_Google_0392.jpg`

**Class:** `peach__scab` (3 duplicate groups):
- SHA256 `c4f8a8e9ef078afa...`: `peach_scab_Bing_0003.jpg, peach_scab_Google_0004.jpg`
- SHA256 `26784bba99b6207b...`: `peach_scab_Bing_0192.jpg, peach_scab_Google_0239.jpg`
- SHA256 `8b2370038ce7e097...`: `peach_scab_Bing_0223.jpg, peach_scab_Bing_0253.jpg`

**Class:** `plum__brown_rot` (1 duplicate groups):
- SHA256 `30636479d481e9f4...`: `plum_brown_rot_Bing_0016.jpg, plum_brown_rot_Google_0050.jpg`

**Class:** `plum__pox_virus` (1 duplicate groups):
- SHA256 `63cbb1c62373c962...`: `plum_pox_virus_Bing_0074.jpg, plum_pox_virus_Google_0040.jpg`

**Class:** `potato__early_blight` (1 duplicate groups):
- SHA256 `bd539d3ed39a47b0...`: `potato_early_blight_100.jpg, potato_early_blight_31.jpg`

**Class:** `raspberry__fire_blight` (3 duplicate groups):
- SHA256 `5eaac70066bfa944...`: `raspberry_fire_blight_Bing_0001.jpg, raspberry_fire_blight_Google_0003.jpg`
- SHA256 `ee3a8a5d15c311b1...`: `raspberry_fire_blight_Bing_0004.jpg, raspberry_fire_blight_Google_0004.jpg`
- SHA256 `fd9d735508e49a17...`: `raspberry_fire_blight_Bing_0063.jpg, raspberry_fire_blight_Google_0005.jpg`

**Class:** `raspberry__gray_mold` (2 duplicate groups):
- SHA256 `cadd2f2b49ecb94c...`: `raspberry_gray_mold_Bing_0020.jpg, raspberry_gray_mold_Google_0011.jpg`
- SHA256 `19fefc858b666d1c...`: `raspberry_gray_mold_Bing_0040.jpg, raspberry_gray_mold_Google_0000.jpg`

**Class:** `raspberry__yellow_rust` (1 duplicate groups):
- SHA256 `6c9bcf9b0752c4b6...`: `raspberry_yellow_rust_Bing_0010.jpg, raspberry_yellow_rust_Google_0013.jpg`

**Class:** `soybean__bacterial_blight` (1 duplicate groups):
- SHA256 `14592fa8c0f6feab...`: `soybean_bacterial_blight_Bing_0028.jpg, soybean_bacterial_blight_Google_0021.jpg`

**Class:** `soybean__brown_spot` (6 duplicate groups):
- SHA256 `d9f35990f160cd74...`: `soybean_brown_spot_Bing_0025.jpg, soybean_brown_spot_Bing_0042.jpg`
- SHA256 `5da6773c8642665d...`: `soybean_brown_spot_Bing_0046.jpg, soybean_brown_spot_Bing_0070.jpg`
- SHA256 `02eeaf335edff2fb...`: `soybean_brown_spot_Bing_0129.jpg, soybean_brown_spot_Bing_0161.jpg`
- SHA256 `66a5c047206c9005...`: `soybean_brown_spot_Bing_0132.jpg, soybean_brown_spot_Bing_0160.jpg`
- SHA256 `9dd8c7dfe357cda3...`: `soybean_brown_spot_Bing_0229.jpg, soybean_brown_spot_Bing_0255.jpg`
- SHA256 `12430fb30dea8d8d...`: `soybean_brown_spot_Bing_0241.jpg, soybean_brown_spot_Bing_0261.jpg`

**Class:** `soybean__downy_mildew` (10 duplicate groups):
- SHA256 `d3717d1c33a0012d...`: `soybean_downy_mildew_Bing_0017.jpg, soybean_downy_mildew_Google_0015.jpg`
- SHA256 `69855fcf20fcfeb9...`: `soybean_downy_mildew_Bing_0020.jpg, soybean_downy_mildew_Google_0023.jpg`
- SHA256 `6a666b977e776140...`: `soybean_downy_mildew_Bing_0027.jpg, soybean_downy_mildew_Bing_0145.jpg, soybean_downy_mildew_Google_0302.jpg`
- SHA256 `c4f4246c396d4c5b...`: `soybean_downy_mildew_Bing_0031.jpg, soybean_downy_mildew_Google_0102.jpg`
- SHA256 `3184640a0734bd21...`: `soybean_downy_mildew_Bing_0071.jpg, soybean_downy_mildew_Google_0090.jpg, soybean_downy_mildew_Google_0127.jpg`
- SHA256 `448e8d3f2959f476...`: `soybean_downy_mildew_Bing_0076.jpg, soybean_downy_mildew_Google_0061.jpg`
- SHA256 `1f1a1cc83f356333...`: `soybean_downy_mildew_Bing_0101.jpg, soybean_downy_mildew_Google_0046.jpg`
- SHA256 `b6be085db833ecdc...`: `soybean_downy_mildew_Bing_0107.jpg, soybean_downy_mildew_Google_0233.jpg`
- SHA256 `80cc4033f40aef4f...`: `soybean_downy_mildew_Bing_0142.jpg, soybean_downy_mildew_Google_0323.jpg`
- SHA256 `e1abdaad86ca16af...`: `soybean_downy_mildew_Bing_0158.jpg, soybean_downy_mildew_Google_0193.jpg`

**Class:** `soybean__frog_eye_leaf_spot` (19 duplicate groups):
- SHA256 `1a368aa8867b44c8...`: `soybean_frog_eye_leaf_spot_Bing_0004.jpg, soybean_frog_eye_leaf_spot_Bing_0039.jpg`
- SHA256 `3b55f29071d07995...`: `soybean_frog_eye_leaf_spot_Bing_0018.jpg, soybean_frog_eye_leaf_spot_Google_0004.jpg`
- SHA256 `30cee5d01978b961...`: `soybean_frog_eye_leaf_spot_Bing_0046.jpg, soybean_frog_eye_leaf_spot_Google_0018.jpg`
- SHA256 `e20248ea929c030a...`: `soybean_frog_eye_leaf_spot_Bing_0050.jpg, soybean_frog_eye_leaf_spot_Google_0187.jpg`
- SHA256 `feaa60722af8fbee...`: `soybean_frog_eye_leaf_spot_Bing_0055.jpg, soybean_frog_eye_leaf_spot_Google_0026.jpg`
- SHA256 `f1359d978f84617a...`: `soybean_frog_eye_leaf_spot_Bing_0059.jpg, soybean_frog_eye_leaf_spot_Google_0114.jpg`
- SHA256 `b664b77a81dd5b92...`: `soybean_frog_eye_leaf_spot_Bing_0080.jpg, soybean_frog_eye_leaf_spot_Google_0272.jpg`
- SHA256 `15367983859760fb...`: `soybean_frog_eye_leaf_spot_Bing_0089.jpg, soybean_frog_eye_leaf_spot_Google_0218.jpg`
- SHA256 `d3385a4710286050...`: `soybean_frog_eye_leaf_spot_Bing_0091.jpg, soybean_frog_eye_leaf_spot_Google_0149.jpg`
- SHA256 `4c62457c1e78d982...`: `soybean_frog_eye_leaf_spot_Bing_0093.jpg, soybean_frog_eye_leaf_spot_Google_0284.jpg`
- SHA256 `640aa14dca7d1d4c...`: `soybean_frog_eye_leaf_spot_Bing_0104.jpg, soybean_frog_eye_leaf_spot_Google_0074.jpg`
- SHA256 `2de57a7ef295d0ec...`: `soybean_frog_eye_leaf_spot_Bing_0108.jpg, soybean_frog_eye_leaf_spot_Google_0331.jpg`
- SHA256 `71e513268b1c23c9...`: `soybean_frog_eye_leaf_spot_Bing_0172.jpg, soybean_frog_eye_leaf_spot_Google_0327.jpg`
- SHA256 `db13af7205a25d07...`: `soybean_frog_eye_leaf_spot_Bing_0178.jpg, soybean_frog_eye_leaf_spot_Google_0015.jpg`
- SHA256 `b1f37d2bb9f655af...`: `soybean_frog_eye_leaf_spot_Bing_0180.jpg, soybean_frog_eye_leaf_spot_Google_0109.jpg`
- SHA256 `096f122839c1de56...`: `soybean_frog_eye_leaf_spot_Bing_0184.jpg, soybean_frog_eye_leaf_spot_Google_0213.jpg`
- SHA256 `3564a9b9ee56e539...`: `soybean_frog_eye_leaf_spot_Bing_0185.jpg, soybean_frog_eye_leaf_spot_Google_0126.jpg`
- SHA256 `67884736264f9aec...`: `soybean_frog_eye_leaf_spot_Bing_0248.jpg, soybean_frog_eye_leaf_spot_Google_0382.jpg`
- SHA256 `6bb73ec5cb0a57aa...`: `soybean_frog_eye_leaf_spot_Bing_0251.jpg, soybean_frog_eye_leaf_spot_Google_0206.jpg`

**Class:** `soybean__mosaic` (2 duplicate groups):
- SHA256 `d98f601180a5a9f9...`: `soybean_mosaic_Baidu_0093.jpg, soybean_mosaic_Baidu_0094.jpg`
- SHA256 `8d7a9c9937909061...`: `soybean_mosaic_Bing_0070.jpg, soybean_mosaic_Google_0090.jpg`

**Class:** `tobacco__blue_mold` (2 duplicate groups):
- SHA256 `6773b21e86bc8a54...`: `tobacco_blue_mold_Bing_0107.jpg, tobacco_blue_mold_Google_0046.jpg`
- SHA256 `bb5adaf91d2c02a7...`: `tobacco_blue_mold_Bing_0119.jpg, tobacco_blue_mold_Google_0103.jpg`

**Class:** `tobacco__frogeye_leaf_spot` (1 duplicate groups):
- SHA256 `f9acb034964b2114...`: `tobacco_frogeye_leaf_spot_Bing_0034.jpg, tobacco_frogeye_leaf_spot_Bing_0072.jpg`

**Class:** `wheat__bacterial_leaf_streak_(black_chaff)` (1 duplicate groups):
- SHA256 `4f29947d3a6c9bb0...`: `wheat_bacterial_leaf_streak_(black_chaff)_black_chaff (24).jpg, wheat_bacterial_leaf_streak_(black_chaff)_google_black_chaff (1).jpg`

**Class:** `wheat__head_scab` (38 duplicate groups):
- SHA256 `5b2c69e59ebe95d7...`: `wheat_head_scab_Baidu_0065.jpg, wheat_head_scab_Baidu_0291.jpg`
- SHA256 `e442438cf8a34066...`: `wheat_head_scab_Baidu_0085.jpg, wheat_head_scab_Baidu_0298.jpg`
- SHA256 `529075c316c1fdd1...`: `wheat_head_scab_Baidu_0091.jpg, wheat_head_scab_Baidu_0094.jpg`
- SHA256 `9fe3ea8f4588f984...`: `wheat_head_scab_Baidu_0092.jpg, wheat_head_scab_Baidu_0095.jpg`
- SHA256 `571daad7dc5a57e8...`: `wheat_head_scab_Baidu_0131.jpg, wheat_head_scab_Baidu_0364.jpg`
- SHA256 `f5ba222630daf7ac...`: `wheat_head_scab_Baidu_0137.jpg, wheat_head_scab_Baidu_0297.jpg`
- SHA256 `59665ec56a977fd0...`: `wheat_head_scab_Baidu_0192.jpg, wheat_head_scab_Baidu_0289.jpg`
- SHA256 `5bdf10f718b3494e...`: `wheat_head_scab_Baidu_0194.jpg, wheat_head_scab_Baidu_0296.jpg`
- SHA256 `0db2293af54add56...`: `wheat_head_scab_Baidu_0197.jpg, wheat_head_scab_Baidu_0303.jpg`
- SHA256 `d29e0d15b76672bd...`: `wheat_head_scab_Baidu_0202.jpg, wheat_head_scab_Baidu_0310.jpg`
- SHA256 `e1fe7c4345d635f7...`: `wheat_head_scab_Baidu_0215.jpg, wheat_head_scab_Baidu_0322.jpg`
- SHA256 `9ca548b3456c9e2d...`: `wheat_head_scab_Baidu_0231.jpg, wheat_head_scab_Baidu_0344.jpg`
- SHA256 `68680257f91fadd2...`: `wheat_head_scab_Baidu_0247.jpg, wheat_head_scab_Baidu_0368.jpg`
- SHA256 `40efce617ff39f9f...`: `wheat_head_scab_Baidu_0254.jpg, wheat_head_scab_Baidu_0380.jpg`
- SHA256 `64224c61dface794...`: `wheat_head_scab_Baidu_0257.jpg, wheat_head_scab_Baidu_0383.jpg`
- SHA256 `43c6e137f5b57544...`: `wheat_head_scab_Baidu_0271.jpg, wheat_head_scab_Baidu_0394.jpg`
- SHA256 `87ce99897f745067...`: `wheat_head_scab_Baidu_0276.jpg, wheat_head_scab_Baidu_0399.jpg`
- SHA256 `40de3ac854a0c409...`: `wheat_head_scab_Baidu_0281.jpg, wheat_head_scab_Baidu_0403.jpg`
- SHA256 `612944e8ccb16492...`: `wheat_head_scab_Baidu_0282.jpg, wheat_head_scab_Baidu_0404.jpg`
- SHA256 `ac485dccd32277f7...`: `wheat_head_scab_Bing_0008.jpg, wheat_head_scab_Bing_0202.jpg, wheat_head_scab_Google_0259.jpg`
- SHA256 `ff98fe7df3028aec...`: `wheat_head_scab_Bing_0013.jpg, wheat_head_scab_Google_0027.jpg`
- SHA256 `1eedeb978ce4fcba...`: `wheat_head_scab_Bing_0014.jpg, wheat_head_scab_Bing_0206.jpg`
- SHA256 `0eaf358d7bb13708...`: `wheat_head_scab_Bing_0023.jpg, wheat_head_scab_Bing_0156.jpg`
- SHA256 `c8122235e62f6403...`: `wheat_head_scab_Bing_0025.jpg, wheat_head_scab_Bing_0097.jpg, wheat_head_scab_Google_0057.jpg`
- SHA256 `444084a7a78db548...`: `wheat_head_scab_Bing_0036.jpg, wheat_head_scab_Bing_0144.jpg`
- SHA256 `a9a7a1d105a34fe3...`: `wheat_head_scab_Bing_0039.jpg, wheat_head_scab_Bing_0232.jpg`
- SHA256 `f144ffdff2c69049...`: `wheat_head_scab_Bing_0040.jpg, wheat_head_scab_Bing_0229.jpg`
- SHA256 `18e3ea9d29778bf9...`: `wheat_head_scab_Bing_0043.jpg, wheat_head_scab_Bing_0109.jpg`
- SHA256 `5bd879999c67dcac...`: `wheat_head_scab_Bing_0051.jpg, wheat_head_scab_Bing_0102.jpg`
- SHA256 `de7ffb847dbaf396...`: `wheat_head_scab_Bing_0052.jpg, wheat_head_scab_Google_0034.jpg`
- SHA256 `4d32c1aab3c97334...`: `wheat_head_scab_Bing_0056.jpg, wheat_head_scab_Bing_0211.jpg`
- SHA256 `52198bd0224654d1...`: `wheat_head_scab_Bing_0067.jpg, wheat_head_scab_Bing_0132.jpg`
- SHA256 `d465878d5b596677...`: `wheat_head_scab_Bing_0069.jpg, wheat_head_scab_Bing_0118.jpg`
- SHA256 `d0301e8451e790cd...`: `wheat_head_scab_Bing_0100.jpg, wheat_head_scab_Google_0105.jpg`
- SHA256 `2b7369b3cbd11f96...`: `wheat_head_scab_Bing_0129.jpg, wheat_head_scab_Google_0088.jpg`
- SHA256 `a818d58d3fdedd28...`: `wheat_head_scab_Bing_0145.jpg, wheat_head_scab_Google_0083.jpg`
- SHA256 `fc6e1bc31178d302...`: `wheat_head_scab_Bing_0175.jpg, wheat_head_scab_Google_0196.jpg`
- SHA256 `3994aade5aa29709...`: `wheat_head_scab_Bing_0219.jpg, wheat_head_scab_Google_0229.jpg`

**Class:** `wheat__leaf_rust` (3 duplicate groups):
- SHA256 `e4cba7d8076a2c14...`: `wheat_leaf_rust_Baidu_0088.jpg, wheat_leaf_rust_Baidu_0197.jpg`
- SHA256 `5750d27853338e74...`: `wheat_leaf_rust_Bing_0001.jpg, wheat_leaf_rust_Google_0000.jpg`
- SHA256 `ebaf6622e255911d...`: `wheat_leaf_rust_Bing_0037.jpg, wheat_leaf_rust_Google_0079.jpg`

**Class:** `wheat__loose_smut` (23 duplicate groups):
- SHA256 `9489c95737722725...`: `wheat_loose_smut_Bing_0008.jpg, wheat_loose_smut_Bing_0104.jpg, wheat_loose_smut_Bing_0129.jpg`
- SHA256 `c723d67c8ef5c739...`: `wheat_loose_smut_Bing_0014.jpg, wheat_loose_smut_Google_0002.jpg`
- SHA256 `4f7459a727404117...`: `wheat_loose_smut_Bing_0015.jpg, wheat_loose_smut_Google_0041.jpg`
- SHA256 `acd2d940780e6685...`: `wheat_loose_smut_Bing_0023.jpg, wheat_loose_smut_Bing_0192.jpg`
- SHA256 `9102ea9e1245bc5f...`: `wheat_loose_smut_Bing_0032.jpg, wheat_loose_smut_Bing_0128.jpg`
- SHA256 `8f0145f58257979d...`: `wheat_loose_smut_Bing_0043.jpg, wheat_loose_smut_Bing_0169.jpg`
- SHA256 `585e298003bf26c4...`: `wheat_loose_smut_Bing_0048.jpg, wheat_loose_smut_Bing_0076.jpg`
- SHA256 `229ae82e509a0635...`: `wheat_loose_smut_Bing_0062.jpg, wheat_loose_smut_Bing_0239.jpg`
- SHA256 `2e5b022eb55873cb...`: `wheat_loose_smut_Bing_0067.jpg, wheat_loose_smut_Bing_0164.jpg`
- SHA256 `695348e9a18dd5fa...`: `wheat_loose_smut_Bing_0079.jpg, wheat_loose_smut_Bing_0100.jpg`
- SHA256 `6947b74d0ab32b54...`: `wheat_loose_smut_Bing_0091.jpg, wheat_loose_smut_Google_0132.jpg`
- SHA256 `107d58061347076e...`: `wheat_loose_smut_Bing_0103.jpg, wheat_loose_smut_Bing_0133.jpg`
- SHA256 `61fd80fc1bff7d5f...`: `wheat_loose_smut_Bing_0111.jpg, wheat_loose_smut_Bing_0145.jpg`
- SHA256 `8f37b4fad2555ae8...`: `wheat_loose_smut_Bing_0115.jpg, wheat_loose_smut_Bing_0140.jpg`
- SHA256 `0723846c8ed6e0b5...`: `wheat_loose_smut_Bing_0134.jpg, wheat_loose_smut_Bing_0165.jpg`
- SHA256 `22dcd7b9b029f315...`: `wheat_loose_smut_Bing_0176.jpg, wheat_loose_smut_Bing_0203.jpg`
- SHA256 `e4430f7ec0670999...`: `wheat_loose_smut_Bing_0184.jpg, wheat_loose_smut_Bing_0191.jpg`
- SHA256 `6fa16680f31f8301...`: `wheat_loose_smut_Bing_0200.jpg, wheat_loose_smut_Bing_0228.jpg`
- SHA256 `44361d9c7bf579fa...`: `wheat_loose_smut_Bing_0224.jpg, wheat_loose_smut_Google_0065.jpg`
- SHA256 `68e6829824b1d02c...`: `wheat_loose_smut_Bing_0236.jpg, wheat_loose_smut_Bing_0268.jpg`
- SHA256 `e58b79263e3019e4...`: `wheat_loose_smut_Bing_0296.jpg, wheat_loose_smut_Bing_0329.jpg`
- SHA256 `5e6f81e6b830d265...`: `wheat_loose_smut_Bing_0321.jpg, wheat_loose_smut_Bing_0384.jpg`
- SHA256 `c201909bad23e0c2...`: `wheat_loose_smut_Bing_0337.jpg, wheat_loose_smut_Bing_0368.jpg`

**Class:** `wheat__powdery_mildew` (9 duplicate groups):
- SHA256 `1689ed0596d5273f...`: `wheat_powdery_mildew_Bing_0027.jpg, wheat_powdery_mildew_Bing_0107.jpg`
- SHA256 `671d06754ed83d33...`: `wheat_powdery_mildew_Bing_0036.jpg, wheat_powdery_mildew_Bing_0152.jpg`
- SHA256 `120d9a332ad80f94...`: `wheat_powdery_mildew_Bing_0037.jpg, wheat_powdery_mildew_Bing_0206.jpg`
- SHA256 `bd14d598ab5591a7...`: `wheat_powdery_mildew_Bing_0040.jpg, wheat_powdery_mildew_Bing_0110.jpg`
- SHA256 `5feb758043f20928...`: `wheat_powdery_mildew_Bing_0056.jpg, wheat_powdery_mildew_Bing_0187.jpg`
- SHA256 `7f5fe6f70573176f...`: `wheat_powdery_mildew_Bing_0057.jpg, wheat_powdery_mildew_Bing_0224.jpg`
- SHA256 `535a0b1f33a78a63...`: `wheat_powdery_mildew_Bing_0059.jpg, wheat_powdery_mildew_Bing_0163.jpg`
- SHA256 `20c6500f70ca5273...`: `wheat_powdery_mildew_Bing_0066.jpg, wheat_powdery_mildew_Google_0012.jpg`
- SHA256 `e1c6ed0922702f70...`: `wheat_powdery_mildew_Bing_0090.jpg, wheat_powdery_mildew_Google_0163.jpg`

**Class:** `wheat__septoria_blotch` (25 duplicate groups):
- SHA256 `09179d3cbcc07233...`: `wheat_septoria_blotch_Bing_0000.jpg, wheat_septoria_blotch_blotch (1).jpg`
- SHA256 `3cf7537123d55e93...`: `wheat_septoria_blotch_Bing_0014.jpg, wheat_septoria_blotch_blotch (17).jpg, wheat_septoria_blotch_blotch (48).jpg`
- SHA256 `712b557b24f4419f...`: `wheat_septoria_blotch_Bing_0017.jpg, wheat_septoria_blotch_blotch (70).jpg`
- SHA256 `e6c5fd14d2a3fcea...`: `wheat_septoria_blotch_Bing_0045.jpg, wheat_septoria_blotch_blotch (105).jpg`
- SHA256 `46889ac719621de8...`: `wheat_septoria_blotch_blotch (10).jpg, wheat_septoria_blotch_blotch (113).jpg`
- SHA256 `9396b9eb07036ff0...`: `wheat_septoria_blotch_blotch (100).jpg, wheat_septoria_blotch_blotch (22).jpg`
- SHA256 `914cee3ee4132d57...`: `wheat_septoria_blotch_blotch (111).jpg, wheat_septoria_blotch_blotch (16).jpg`
- SHA256 `bac975c570e67610...`: `wheat_septoria_blotch_blotch (12).jpg, wheat_septoria_blotch_blotch (87).jpg`
- SHA256 `64e8ac1ae0cc9ffc...`: `wheat_septoria_blotch_blotch (14).jpg, wheat_septoria_blotch_blotch (69).jpg`
- SHA256 `f412cea3f17575cb...`: `wheat_septoria_blotch_blotch (18).jpg, wheat_septoria_blotch_blotch (41).jpg`
- SHA256 `a9a846bf825ef35a...`: `wheat_septoria_blotch_blotch (27).jpg, wheat_septoria_blotch_blotch (50).jpg`
- SHA256 `19aca78ed1b09094...`: `wheat_septoria_blotch_blotch (30).jpg, wheat_septoria_blotch_blotch (96).jpg`
- SHA256 `8e95fb25e4d8e116...`: `wheat_septoria_blotch_blotch (32).jpg, wheat_septoria_blotch_blotch (68).jpg`
- SHA256 `6f586fc6e2acc736...`: `wheat_septoria_blotch_blotch (33).jpg, wheat_septoria_blotch_blotch (79).jpg`
- SHA256 `ca8774dd80ceb345...`: `wheat_septoria_blotch_blotch (37).jpg, wheat_septoria_blotch_blotch (45).jpg`
- SHA256 `30817c654afb6cbb...`: `wheat_septoria_blotch_blotch (39).jpg, wheat_septoria_blotch_blotch (43).jpg`
- SHA256 `040cce1e1e543a9d...`: `wheat_septoria_blotch_Google_0005.jpg, wheat_septoria_blotch_google_septoria (1).jpg`
- SHA256 `df8242893e26b0a9...`: `wheat_septoria_blotch_Google_0016.jpg, wheat_septoria_blotch_google_septoria (6).jpg`
- SHA256 `591e91f0cee5b04b...`: `wheat_septoria_blotch_Google_0058.jpg, wheat_septoria_blotch_google_septoria (10).jpg`
- SHA256 `7c987590891b4987...`: `wheat_septoria_blotch_Google_0142.jpg, wheat_septoria_blotch_google_septoria (12).jpg`
- SHA256 `bd6f75e4838ad490...`: `wheat_septoria_blotch_Google_0178.jpg, wheat_septoria_blotch_google_septoria (2).jpg`
- SHA256 `9446491e254626cf...`: `wheat_septoria_blotch_Google_0206.jpg, wheat_septoria_blotch_google_septoria (13).jpg`
- SHA256 `a57a72801a650234...`: `wheat_septoria_blotch_Google_0296.jpg, wheat_septoria_blotch_google_septoria (16).jpg`
- SHA256 `95424622ed20158b...`: `wheat_septoria_blotch_Google_0309.jpg, wheat_septoria_blotch_google_septoria (21).jpg`
- SHA256 `da4a6d3b501286fb...`: `wheat_septoria_blotch_Google_0338.jpg, wheat_septoria_blotch_google_septoria (25).jpg`

**Class:** `wheat__stem_rust` (8 duplicate groups):
- SHA256 `77a0f98acff1cacb...`: `wheat_stem_rust_Bing_0001.jpg, wheat_stem_rust_Bing_0111.jpg`
- SHA256 `e65eef68c3ae3692...`: `wheat_stem_rust_Bing_0002.jpg, wheat_stem_rust_Bing_0078.jpg`
- SHA256 `22c1679e03a2b680...`: `wheat_stem_rust_Bing_0013.jpg, wheat_stem_rust_Google_0052.jpg`
- SHA256 `65a9fafecebf0e10...`: `wheat_stem_rust_Bing_0040.jpg, wheat_stem_rust_Google_0035.jpg`
- SHA256 `53d3a9ca3b70fd37...`: `wheat_stem_rust_Bing_0050.jpg, wheat_stem_rust_Bing_0071.jpg`
- SHA256 `632d6f3df3b75b11...`: `wheat_stem_rust_Bing_0070.jpg, wheat_stem_rust_Google_0028.jpg`
- SHA256 `f0ace029364ac274...`: `wheat_stem_rust_Bing_0167.jpg, wheat_stem_rust_Bing_0247.jpg`
- SHA256 `a82ae8f0068cf456...`: `wheat_stem_rust_Bing_0171.jpg, wheat_stem_rust_Bing_0257.jpg`

**Class:** `wheat__stripe_rust` (26 duplicate groups):
- SHA256 `4d687de8b34b84a0...`: `wheat_stripe_rust_Baidu_0106.jpg, wheat_stripe_rust_Baidu_0196.jpg`
- SHA256 `26a3d8decebdd0b4...`: `wheat_stripe_rust_Baidu_0466.jpg, wheat_stripe_rust_Baidu_0484.jpg`
- SHA256 `8694bb4a710be15f...`: `wheat_stripe_rust_Baidu_0468.jpg, wheat_stripe_rust_Baidu_0487.jpg`
- SHA256 `38f8012f5629acf3...`: `wheat_stripe_rust_Bing_0002.jpg, wheat_stripe_rust_Google_0045.jpg`
- SHA256 `8056471d1fe39e6a...`: `wheat_stripe_rust_Bing_0004.jpg, wheat_stripe_rust_Bing_0078.jpg`
- SHA256 `5b0fd5f952056efb...`: `wheat_stripe_rust_Bing_0006.jpg, wheat_stripe_rust_Google_0029.jpg`
- SHA256 `18886b62d751c15e...`: `wheat_stripe_rust_Bing_0014.jpg, wheat_stripe_rust_Bing_0125.jpg`
- SHA256 `9194a3751cf6e214...`: `wheat_stripe_rust_Bing_0021.jpg, wheat_stripe_rust_Bing_0089.jpg`
- SHA256 `96a4645a3f7d8ed9...`: `wheat_stripe_rust_Bing_0023.jpg, wheat_stripe_rust_Bing_0076.jpg`
- SHA256 `7c87c16b5e39f80a...`: `wheat_stripe_rust_Bing_0025.jpg, wheat_stripe_rust_Bing_0194.jpg`
- SHA256 `380727c459af3c38...`: `wheat_stripe_rust_Bing_0027.jpg, wheat_stripe_rust_Bing_0084.jpg`
- SHA256 `3734441d68ad10d0...`: `wheat_stripe_rust_Bing_0029.jpg, wheat_stripe_rust_Bing_0081.jpg`
- SHA256 `aaabd96f7ce38b6c...`: `wheat_stripe_rust_Bing_0031.jpg, wheat_stripe_rust_Bing_0173.jpg`
- SHA256 `14cc7f68415dda32...`: `wheat_stripe_rust_Bing_0033.jpg, wheat_stripe_rust_Bing_0083.jpg`
- SHA256 `d315bc84a837dcbf...`: `wheat_stripe_rust_Bing_0037.jpg, wheat_stripe_rust_Bing_0095.jpg`
- SHA256 `d442611e2cbc48cc...`: `wheat_stripe_rust_Bing_0038.jpg, wheat_stripe_rust_Bing_0272.jpg`
- SHA256 `d81c416816c1f4cc...`: `wheat_stripe_rust_Bing_0039.jpg, wheat_stripe_rust_Bing_0096.jpg`
- SHA256 `2d8a94e8e7844b76...`: `wheat_stripe_rust_Bing_0042.jpg, wheat_stripe_rust_Bing_0153.jpg`
- SHA256 `ad28fc5dd926cffe...`: `wheat_stripe_rust_Bing_0047.jpg, wheat_stripe_rust_Bing_0151.jpg`
- SHA256 `02f5215ee7308a1f...`: `wheat_stripe_rust_Bing_0048.jpg, wheat_stripe_rust_Bing_0122.jpg`
- SHA256 `b45443b61a582d53...`: `wheat_stripe_rust_Bing_0055.jpg, wheat_stripe_rust_Bing_0137.jpg`
- SHA256 `435b525c1c4e2953...`: `wheat_stripe_rust_Bing_0063.jpg, wheat_stripe_rust_Bing_0240.jpg`
- SHA256 `cb38819eb70b7d1a...`: `wheat_stripe_rust_Bing_0126.jpg, wheat_stripe_rust_Google_0149.jpg`
- SHA256 `737ec51eb3e8581c...`: `wheat_stripe_rust_Bing_0145.jpg, wheat_stripe_rust_Google_0009.jpg`
- SHA256 `010088298c2aadc8...`: `wheat_stripe_rust_Bing_0224.jpg, wheat_stripe_rust_Google_0004.jpg`
- SHA256 `0c1ff41ce56e58f2...`: `wheat_stripe_rust_Bing_0225.jpg, wheat_stripe_rust_Google_0143.jpg`

**Class:** `zucchini__bacterial_wilt` (1 duplicate groups):
- SHA256 `757b2b4bd8bb7685...`: `zucchini_bacterial_wilt_Bing_0019.jpg, zucchini_bacterial_wilt_Google_0008.jpg`

**Class:** `zucchini__powdery_mildew` (10 duplicate groups):
- SHA256 `3d58c9220063555f...`: `zucchini_powdery_mildew_Bing_0007.jpg, zucchini_powdery_mildew_Google_0187.jpg`
- SHA256 `3587cff89745dae1...`: `zucchini_powdery_mildew_Bing_0281.jpg, zucchini_powdery_mildew_Bing_0321.jpg`
- SHA256 `7c714bf0f4c9020c...`: `zucchini_powdery_mildew_Bing_0282.jpg, zucchini_powdery_mildew_Bing_0322.jpg`
- SHA256 `34625e95a49f574a...`: `zucchini_powdery_mildew_Bing_0283.jpg, zucchini_powdery_mildew_Bing_0324.jpg`
- SHA256 `43bdc888ef48ce5c...`: `zucchini_powdery_mildew_Bing_0289.jpg, zucchini_powdery_mildew_Bing_0330.jpg`
- SHA256 `05695267cc7f3919...`: `zucchini_powdery_mildew_Bing_0297.jpg, zucchini_powdery_mildew_Bing_0337.jpg`
- SHA256 `bce1a649ba4ed0ce...`: `zucchini_powdery_mildew_Bing_0298.jpg, zucchini_powdery_mildew_Bing_0341.jpg`
- SHA256 `04741b83dfa4a7dd...`: `zucchini_powdery_mildew_Bing_0308.jpg, zucchini_powdery_mildew_Bing_0347.jpg`
- SHA256 `bae9239b62308122...`: `zucchini_powdery_mildew_Bing_0336.jpg, zucchini_powdery_mildew_Bing_0357.jpg`
- SHA256 `c990a0e5135acec1...`: `zucchini_powdery_mildew_Google_0090.jpg, zucchini_powdery_mildew_Google_0114.jpg`


---

## 7. Strict Compliance Audit

- **Zero Dataset Modification:** `data/processed/model2_classifier/` remained 100% untouched.
- **Zero Retraining:** Model 2 weights and evaluation metrics remain baseline.
- **Zero Image Transformations:** All images copied with original resolution, color space, and metadata.
- **Read-Only PlantSeg Safety:** `data/external/model2_supplementary/plantsegv3/plantsegv3` remained untouched.