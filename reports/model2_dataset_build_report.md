# Model 2 Dataset Build Report (PlantSeg → YOLOX)

**Date:** 2026-10-05 · **Source:** `data/external/plantseg/` (READ-ONLY, unmodified) · **Output:** `data/processed/model2_dataset/`

## 1. Headline numbers

| Metric | Value |
|---|---|
| Source images | 7774 |
| Source annotations | 77394 |
| **Usable images** | **7631** |
| **Usable annotations (boxes)** | **54562** |
| Crops | 34 |
| Diseases (classes) | 115 |
| train images / boxes | 5353 / 38074 |
| val images / boxes | 809 / 6106 |
| test images / boxes | 1469 / 10382 |

## 2. Excluded / invalid (never silently discarded)

- Orphan annotations (image_id not in same split file): **21580** → `excluded_annotations.json`
- Invalid annotation/box rows: **248**
- Images removed for cross-split hash leakage: **127** (policy keep train > val > test) → `hash_leakage.json`
- Cross-split leakage after fix: **0**; same-split duplicate groups retained: 149

### Invalid annotation reasons

| Reason | Count |
|---|---|
| box_out_of_bounds | 233 |
| image_no_valid_boxes | 15 |

## 3. Images per crop (top 20)

| Crop | Images |
|---|---|
| Wheat | 1120 |
| Tomato | 657 |
| Soybean | 490 |
| Corn | 418 |
| Citrus | 414 |
| Apple | 399 |
| Grape | 396 |
| Cucumber | 378 |
| Banana | 350 |
| Peach | 285 |
| Zucchini | 274 |
| Coffee | 191 |
| Cabbage | 176 |
| Bell pepper | 172 |
| Garlic | 158 |
| Potato | 145 |
| Bean | 141 |
| Blueberry | 141 |
| Squash | 141 |
| Tobacco | 125 |

(all 34 crops in summary JSON)

## 4. Annotations per disease — smallest 15 / largest 15

| Disease | Annotations | Images |
|---|---|---|
| peach rust | 21 | 5 |
| coffee black rot | 31 | 3 |
| tobacco mosaic virus | 32 | 28 |
| plum rust | 34 | 17 |
| peach anthracnose | 35 | 10 |
| cauliflower bacterial soft rot | 42 | 19 |
| raspberry gray mold | 42 | 18 |
| eggplant phytophthora blight | 44 | 22 |
| blueberry anthracnose | 53 | 28 |
| plum bacterial spot | 53 | 10 |
| plum brown rot | 59 | 41 |
| blueberry botrytis blight | 60 | 19 |
| grapevine leafroll disease | 65 | 32 |
| blueberry mummy berry | 68 | 29 |
| bean mosaic virus | 70 | 33 |
| ... | ... | ... |
| grape black rot | 914 | 88 |
| bell pepper bacterial spot | 915 | 51 |
| broccoli alternaria leaf spot | 1052 | 52 |
| coffee leaf rust | 1059 | 107 |
| zucchini powdery mildew | 1111 | 129 |
| zucchini downy mildew | 1128 | 33 |
| tomato septoria leaf spot | 1305 | 98 |
| tomato bacterial leaf spot | 1311 | 86 |
| wheat stripe rust | 1415 | 220 |
| cucumber angular leaf spot | 1474 | 147 |
| soybean frog eye leaf spot | 1519 | 149 |
| cherry leaf spot | 1637 | 66 |
| apple scab | 1678 | 168 |
| tomato early blight | 1712 | 151 |
| citrus canker | 3780 | 321 |

## 5. Class mapping

`class_mapping.json`: 115 contiguous IDs 0..114 (sorted, seed 42).

## 6. Dataset structure

```
model2_dataset/
├── images/{train,val,test}/  (<split>_<orig>.jpg)
├── labels/{train,val,test}/  (YOLO: cls xc yc w h normalized)
├── class_mapping.json
├── manifest.csv  (provenance: source_uid, annotation_id, bbox)
├── excluded_annotations.json
└── hash_leakage.json
```

## 7. Limitations

- Boxes derived from disease-region polygons (mask ratios 4e-5..1).
- 21,580 source anns are orphans (IDs restart per split file) — flagged, never merged across splits.
- Source splits reused as final splits (deterministic, seed 42).
- Same-split byte-duplicate groups retained (flagged, no leakage).

## 8. Verdict

PlantSeg **supports** the YOLOX disease-localization dataset: 7631 images / 54562 boxes / 115 classes built and validated.
