# Model 2 Dataset Audit — Disease Detection + Localization

**Date:** 2026-10-05 · **Scope:** `data/external/` (35 folders) · **READ-ONLY**
(no dataset modified, renamed, moved, or preprocessed; no downloads; no training)

## Executive summary

- **Localization-ready (boxes/masks, YOLOX-convertible): 4 datasets.**
  `plantseg` (COCO masks, 7,774 images — BEST),
  `Herbal_Dataset.v11i.yolov11` (YOLO plant boxes, 20,938 — NOT disease boxes),
  `herbs.v4i.yolov11` (YOLO herb boxes, 937),
  `Fruits Model.v1i.yolov11` (YOLO fruit boxes, 772 files, 92% empty labels).
- **Classification-only (disease labels, NO boxes): 22 datasets.**
- **Unusable / empty: 9 folders** — `cherry_tomato`, `dutch_rose`, `gypsophila`,
  `lilium`, `Original Image` (0 images); `anthurium` (105 loose files, no labels);
  `gerbera_commons` (3 files); `strawberry_clean` (1,565 loose files, no labels);
  `geranium` (223 files in bare train/test/val splits, no class folders).
- **Bottom line:** NO dataset pairs disease identity WITH boxes except `plantseg`
  (masks + Metadata.csv plant→disease table, 34 plants / 104 diseases). Herb/fruit
  YOLO sets localize the WRONG object (whole plant/fruit, not lesions).

## 1. Crop → disease → image-count table (exact recursive counts)

### Classification-only disease datasets (22)

| Crop | Disease / condition folders | Images |
|---|---|---|
| Tomato (`tomato/`) | Bacterial_spot 2127, Spider mites 1676, Target Spot 1404, YellowLeaf Curl 3208, healthy 1591, bacterial leaf spot 86, early blight 1187, late blight 337, leaf mold 1108, mosaic virus 436, septoria 1901, yellow curl 93; fruit 22 loose | 15,176 |
| Cucumber (`cucumber/`) | angular spot 182, bacterial wilt 108, powdery mildew 189; CDRD/train 6×160=960; CDRD/test flat 1,365; cucumber_disease 11,119 (Downy Mildew 2311, Fresh Leaf 2410, …) | 13,923 |
| Rose (`rose_new/`) | leaves: Black spot 1720, Downy mildew 390, Dry Leaf 324, Healthy 1899, Healthy Leaf 818, Insects 431, Leaf Holes 683, Pest Damage 790, Pure 231, Mosaic Virus 245, botrytis 558; flower 171 loose | 8,260 |
| Spinach (`spinach_disease/`) | Anthracnose 102, Bacterial-Spot 752, Downy-Mildew 240, **Healthy-Leaf 1399**, Pest-Damage 513 | 3,006 |
| Capsicum (`pepper_bell/`) | blossom end rot 112; leaf: spot 74, Bacterial_spot 997, healthy 1478, bacterial spot 76, frogeye 31, mildew 28, healthy 34 | 2,830 |
| Lettuce (`lettuce-disease.v6i.folder`) | downy mildew 84, mosaic virus 39; train D 693/H 636; test D 18/H 22; valid D 20/H 20 | 2,274 |
| Strawberry (`strawberry/`) | leaf scorch 39, healthy 88; fruit anthracnose 58 | 185 |
| Blueberry (`blueberry/`) | fruit anthracnose 42, botrytis 36, mummy berry 47; leaf 204 | 329 |
| Zucchini (`zuchhini/`) | bacterial wilt 81, downy mildew 45, powdery mildew 223, yellow mosaic 95 | 444 |
| Broccoli (`broccoli_new/`) | black_rot 256, alternaria 65, downy mildew 29, ring spot 16, **healthy 110** | 476 |
| Cabbage (`cabbage/`) | Alternaria 63, black rot 131, downy mildew 84, Grey mould 83, **Healthy 132**, Tip burn 90 | 583 |
| Cauliflower (`cauliflower/`) | alternaria 54, soft rot 36, **Healthy 87**, Yellow virus 60 | 237 |
| Celery (`celery/`) | anthracnose 29, early blight 36 (NO healthy) | 65 |
| Basil (`basil/`) | downy mildew 63 (NO healthy) | 63 |
| Turnip (`turnip/`) | Alternaria 116, Black rot 183, **Healthy 181** | 480 |
| Marigold (`Marigold_new/`) | flower 67 loose; leaves: Alternaria 338, Healthy 273, Pest 78 | 756 |
| Raspberry / Carnation / Coriander / Herbal-pool / Medicinal / Orchid | single-folder or species/location-only, no disease split (119 / 52 / 838 / 4,667 / 5,613 / 31,429) | — |

### Box/mask datasets (4)

| Dataset | Object boxed | Images | Labels |

## 2. Annotation availability table

| Dataset | Ann? | Type | Format | Boxes/img | Paired | Empty | Corrupt (60-file sample) |
|---|---|---|---|---|---|---|---|
| `plantseg` | YES | segmentation masks (disease regions) | COCO polygons + PNG masks | ~10/img | 7,774/7,774 | 0 | 0 |
| `Herbal_Dataset.v11i.yolov11` | YES | boxes (PLANT, not lesion) | YOLO | 4.59 | 20,938/20,938 | 0 | 0 |
| `herbs.v4i.yolov11` | YES | boxes (HERB, not lesion) | YOLO | 1.13 | 937/937 | 2 | 0 |
| `Fruits Model.v1i.yolov11` | PARTIAL | boxes (FRUIT) | YOLO | 0.20 | 772/772 files | **712 (92%)** | 0 |
| 22 classification sets | NO | classification-only | none | — | — | — | 0 (Marigold: 60 PNGs misnamed .jpg — readable) |
| `geranium`/`anthurium`/`gerbera_commons`/`strawberry_clean`/5 empties | NO | none | none | — | — | — | — |

## 3. Localization-ready datasets

1. **`plantseg` — READY (masks).** 7,774 images, 77,394 disease-region annotations,
   PNG masks verified, Metadata.csv gives (Plant, Disease) per file — the ONLY
   dataset where disease regions are localized. COCO-seg → YOLOX convertible.
2. **`Herbal_Dataset.v11i.yolov11` — READY (plant boxes).** 100% paired, 0 bad
   lines, YOLO-normalized. Detection-backbone pretraining only — NOT disease boxes.
3. **`herbs.v4i.yolov11` — READY (herb boxes).** 937/937 paired, 12 classes, clean.
4. **`Fruits Model.v1i.yolov11` — MARGINAL.** Drop 712 empty-label images first.

## 4. Classification-only datasets (need NEW boxes for YOLOX)

Tomato (15,176), cucumber (13,923), rose (8,260), spinach (3,006), capsicum
(2,830), lettuce (2,274), zucchini (444), turnip (480), cabbage (583), broccoli
(476), cauliflower (237), strawberry (185), blueberry (329), marigold (756),
celery (65), basil (63), raspberry (119), carnation (healthy-only 52). All are
single-leaf/plant portraits (whole-image label = one disease); single object/image.

## 5. Unusable datasets

| Folder | Images | Reason |
|---|---|---|
| `cherry_tomato`, `dutch_rose`, `gypsophila`, `lilium`, `Original Image` | 0 | empty |
| `anthurium` | 105 | loose files, no labels |
| `gerbera_commons` | 3 | effectively empty |
| `strawberry_clean` | 1,565 | loose files, no labels |
| `geranium` | 223 | bare train/test/val splits, no class folders |
| `coriander_leaf` (838), `herbal_classification_pool` (4,667), `medicinal_plants` (5,613), `Orchid_source` (31,429) | — | species/location only, no disease signal |

## 6. Missing disease/crop data (vs 22 Model-1 targets)

- **Zero images:** cherry_tomato, lilium, gypsophila, dutch_rose.
- **<150 images:** basil (63, no healthy), celery (65, no healthy), raspberry (119,
  single folder), carnation (52 healthy-only), strawberry (185), blueberry (329).
- **No healthy controls:** celery, basil, zucchini, blueberry-fruit, raspberry.
- Healthy available: tomato (1,591+), spinach (1,399), rose (2,717), capsicum
  (1,512), lettuce (676), cabbage (132), broccoli (110), cauliflower (87),
  turnip (181), strawberry-leaf (88), marigold (273).

## 7. Single vs multi-object · pairing · corruption

- Classification sets: single leaf/plant per image (whole-image label valid).
- YOLO sets: multi-object common (Herbal 70% files >1 box, Fruits 57%, max 78).
- Pairing: Herbal/herbs 100%; Fruits 100% files but 92% empty; plantseg COCO
  counts match mask folders (7,774 masks).
- Corruption: 0 bad headers everywhere except Marigold (`.jpg` files are PNG
  bytes — readable, rename at build time). No zero-byte files.

## 8. YOLOX-convertibility verdict

| Source | → YOLOX? | Work needed |
|---|---|---|
| `plantseg` | YES | COCO-seg → YOLOX (bbox from polygons + Metadata class join) — direct |
| `Herbal_Dataset` / `herbs` | YES (plant-level) | YOLO → YOLOX trivial; pretraining only |
| `Fruits Model` | YES after filter | drop 712 empty-label images |
| 22 classification sets | NO (as-is) | NEW lesion-box annotation campaign required |

## 9. Recommended datasets for Model 2

1. `plantseg` — sole localized-disease source (train YOLOX here first).
2. Tomato / cucumber / rose / spinach / capsicum — classifier head + box pool.
3. `Herbal_Dataset.v11i.yolov11` — detection pretraining only.
4. Broccoli / cabbage / cauliflower / turnip / lettuce / marigold — secondary
   classifier coverage (each has healthy + ≥2 diseases).

## 10. Additional data that MUST be collected

1. Lesion bounding boxes for all classification-only crops (priority: tomato,
   cucumber, rose, capsicum, spinach, lettuce, strawberry, blueberry, zucchini,
   broccoli, cabbage, turnip).
2. Healthy controls for celery, basil, zucchini, raspberry, blueberry-fruit.
3. Any data for cherry_tomato, lilium, gypsophila, dutch_rose (0 images).
4. Carnation/gerbera/anthurium disease images (healthy-only or ~100 images).
5. Rename Marigold `.jpg`→`.png` at build time (content is PNG).

---
*Machine-readable companion: `reports/model2_dataset_audit.json` (35 datasets,
120,348 images). Audit script: `scripts/audit_model2_readonly.py` (+
`scripts/fix_audit_totals.py`). Datasets untouched — only `reports/` written.*

|---|---|---|---|
| `plantseg` | **DISEASE-region masks** (COCO polygons + PNG masks + Metadata.csv: 34 plants, 104 diseases) | 7,774 | 77,394 anns (train 52,898 / test 15,569 / val 8,927) |
| `Herbal_Dataset.v11i.yolov11` | whole-PLANT boxes, 59 species, avg 4.6 boxes/img, 70% multi-object | 20,938 | 20,938 paired, 0 empty |
| `herbs.v4i.yolov11` | whole-HERB boxes, 12 species, avg 1.13 boxes/img | 937 | 937 paired, 2 empty |
| `Fruits Model.v1i.yolov11` | whole-FRUIT boxes (Apple/Mango/Muskmelon), 57% multi-object | 772 | **712 EMPTY (92%)** — only 156 boxes |
