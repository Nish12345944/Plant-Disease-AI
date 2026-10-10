# Manual Download Checklist — Model 1 & Model 2 Data Acquisition

**Target:** 400–500 unique, valid **REAL** images per class (augmented copies do NOT count).
**Generated from authoritative manifests** on 2026-10-09. No datasets were downloaded; this is a download/selection checklist only.

**Protected sets — DO NOT touch:** `data/processed/model2_v4/*/test`, `data/external/end_to_end_test/`, Model 1 `test` folders, EXP-0 checkpoint. Never move a protected test image into train/val.

**Counting method:** Per-class shortfall = max(0, target − current_real_unique). Multi-crop / multi-class datasets (PlantVillage, New Plant Diseases, PlantDoc) are listed ONCE per class they cover; when downloaded once, split by crop/disease folder and dedupe by hash before counting toward any class. Never count one image toward two classes.

---

## MODEL 1 — Crop/Plant Identification (44 active classes with data + 1 empty slot)

Alias rules applied from `model1_expanded_class_mapping.json`:
- `cherry_tomato` → **alias of `tomato`** (NOT acquired separately).
- `french_bean`, `capsicum`, `zucchini` are canonical here (aliases bean/bell_pepper/squash fold into them).

### Priority 0 — ZERO images (critical)
| Class | Current | To 400 | To 500 | Links | Destination | Augment after? |
|---|---|---|---|---|---|---|
| gypsophila | 0 | 400 (353 after reuse) | 500 (453 after reuse) | STAGED partial: `data/external/model1_expansion/Gypsophila Hydrangea Daisy.v1i.yolov11` (Roboflow, **CC BY 4.0**, https://universe.roboflow.com/gypsophila-hydrangea-daisy/gypsophila-hydrangea-daisy-ybmkz/dataset/1); add iNaturalist Gypsophila https://www.inaturalist.org/observations?taxon_name=Gypsophila | `data/external/model1_acquisition/gypsophila/` | Hold until ≥200 |
| cherry_tomato | 0 | — ALIAS of tomato — | — | no separate download | n/a | n/a |

### Priority 1 — Below 100 real images
| Class | Current | To 400 | To 500 | Links | Destination | Augment after? |
|---|---|---|---|---|---|---|
| gerbera | 3 | **146 (after 251 staged reuse)** | 246 | STAGED: `data/external/model1_expansion/gerbera dataset` (251 imgs); Oxford Flowers 102 https://www.robots.ox.ac.uk/~vgg/data/flowers/102/ ; iNaturalist Gerbera | `data/external/model1_acquisition/gerbera/` | Hold until ≥200 |
| lilium | 45 | 355 | 455 | Oxford Flowers 102 ; iNaturalist Lilium | `.../lilium/` | Hold until ≥200 |
| carnation | 51 | 349 | 449 | Oxford Flowers 102 ; iNaturalist Dianthus | `.../carnation/` | Hold until ≥200 |
| basil | 63 | 337 | 437 | iNaturalist Ocimum ; Herbal leaf datasets | `.../basil/` | Hold until ≥200 |
| celery | 65 | 335 | 435 | iNaturalist Apium ; Herbal leaf datasets | `.../celery/` | Hold until ≥200 |
| ginger | 91 | 309 | 409 | iNaturalist Zingiber ; Herbal datasets | `.../ginger/` | Hold until ≥200 |

### Priority 2 — 100–249 real images
| Class | Current | To 400 | To 500 | Links | Destination | Augment after? |
|---|---|---|---|---|---|---|
| anthurium | 104 | 296 | 396 | iNaturalist Anthurium | `.../anthurium/` | Hold until ≥200 |
| cauliflower | 104 | 296 | 396 | iNaturalist Brassica ; PlantNet | `.../cauliflower/` | Hold until ≥200 |
| maple | 113 | 287 | 387 | iNaturalist Acer ; Leafsnap | `.../maple/` | Hold until ≥200 |
| raspberry | 123 | 277 | 377 | PlantVillage healthy raspberry ; iNaturalist Rubus | `.../raspberry/` | Hold until ≥200 |
| eggplant | 136 | 264 | 364 | PlantVillage healthy eggplant ; iNaturalist Solanum melongena | `.../eggplant/` | Hold until ≥200 |
| cherry | 139 | 261 | 361 | PlantVillage healthy cherry ; iNaturalist Prunus avium | `.../cherry/` | Hold until ≥200 |
| carrot | 148 | 252 | 352 | iNaturalist Daucus ; PlantNet | `.../carrot/` | Yes after ~250 |
| rice | 155 | 245 | 345 | iNaturalist Oryza ; RiceDisease dataset | `.../rice/` | Yes after ~250 |
| tobacco | 178 | 222 | 322 | iNaturalist Nicotiana ; PlantNet | `.../tobacco/` | Yes after ~250 |
| garlic | 198 | 202 | 302 | iNaturalist Allium sativum ; PlantNet | `.../garlic/` | Yes after ~250 |
| plum | 215 | 185 | 285 | New Plant Diseases ; iNaturalist Prunus domestica | `.../plum/` | Yes after ~250 |
| potato | 239 | 161 | 261 | PlantVillage healthy potato ; iNaturalist Solanum tuberosum | `.../potato/` | Yes after ~250 |
| melon | 247 | 153 | 253 | PlantVillage healthy ; iNaturalist Cucumis melo | `.../melon/` | Yes after ~250 |

### Priority 3 — 250–399 real images
| Class | Current | To 400 | To 500 | Links | Destination | Augment after? |
|---|---|---|---|---|---|---|
| cabbage | 274 | 126 | 226 | PlantVillage healthy ; iNaturalist Brassica | `.../cabbage/` | Yes |
| geranium | 251 | 149 | 249 | iNaturalist Pelargonium ; Oxford Flowers 102 | `.../geranium/` | Yes |
| coffee | 284 | 116 | 216 | iNaturalist Coffea ; PlantNet | `.../coffee/` | Yes |
| blueberry | 314 | 86 | 186 | PlantVillage healthy blueberry ; iNaturalist Vaccinium | `.../blueberry/` | Yes |
| zucchini | 393 | 7 | 107 | PlantVillage healthy squash ; iNaturalist Cucurbita | `.../zucchini/` | Yes |

### Classes already at/above 400 (no download needed; augment moderately if desired)
apple 566, banana 536, capsicum 630, citrus 521, corn 616, cucumber 630, french_bean 630, grape 558, lettuce 630, marigold 630, orchid 630, rose 630, soybean 630, spinach 630, strawberry 630, tomato 630, wheat 630, peach 444, broccoli 414, chrysanthemum 418.

### Best multi-class downloads for Model 1 (one download, many classes)
1. **Oxford Flowers 102** — https://www.robots.ox.ac.uk/~vgg/data/flowers/102/ → carnation, lilium, chrysanthemum, geranium, marigold, orchid, rose, gerbera.
2. **PlantVillage (healthy folders)** — https://github.com/spMohanty/PlantVillage-Dataset → apple, blueberry, cherry, citrus, corn, cucumber, eggplant, grape, lettuce, melon, peach, potato, raspberry, spinach, strawberry, tomato, zucchini.
3. **iNaturalist** — https://www.inaturalist.org → all plant classes (maple, anthurium, carrot, cauliflower, celery, garlic, ginger, basil, coffee, banana, tobacco, plum, rice, soybean).

---

## MODEL 2 — Crop-Qualified Disease Classifier (116 disease classes + 1 shared healthy)

### Priority 0/1 — Lowest disease classes (urgent; 69 classes are <100)
Ordered by current count. "To 400/500" = additional real images to acquire (no safe reuse identified for these).

| Class | Crop | Current | To 400 | To 500 | Val/Test | Source |
|---|---|---|---|---|---|---|
| coffee__black_rot | coffee | 6 | 394 | 494 | WARN | MANUAL CURATION / coffee disease research |
| peach__rust | peach | 8 | 392 | 492 | WARN | iNaturalist/PlantDoc peach rust |
| broccoli__ring_spot | broccoli | 10 | 390 | 490 | WARN | MANUAL CURATION / PlantDoc |
| peach__anthracnose | peach | 13 | 387 | 487 | WARN | PlantVillage peach ; PlantDoc |
| coffee__brown_eye_spot | coffee | 14 | 386 | 486 | WARN | MANUAL CURATION |
| plum__bacterial_spot | plum | 16 | 384 | 484 | WARN | New Plant Diseases ; iNaturalist |
| carrot__cercospora_leaf_blight | carrot | 17 | 383 | 483 | WARN | PlantDoc ; iNaturalist Daucus |
| raspberry__leaf_spot | raspberry | 18 | 382 | 482 | WARN | MANUAL CURATION |
| tobacco__frogeye_leaf_spot | tobacco | 20 | 380 | 480 | WARN | PlantDoc ; Tobacco research |
| ginger__leaf_spot | ginger | 25 | 375 | 475 | WARN | MANUAL CURATION |
| bell_pepper__powdery_mildew | bell_pepper | 26 | 374 | 474 | WARN | MANUAL CURATION / iNaturalist |
| bell_pepper__frogeye_leaf_spot | bell_pepper | 28 | 372 | 472 | WARN | MANUAL CURATION |
| broccoli__downy_mildew | broccoli | 29 | 371 | 471 | WARN | PlantDoc ; iNaturalist |
| celery__anthracnose | celery | 29 | 371 | 471 | WARN | MANUAL CURATION |
| raspberry__fire_blight | raspberry | 31 | 369 | 469 | WARN | MANUAL CURATION |

Full per-class numbers for all 116 disease classes are in `final_model2_acquisition_matrix.csv`.

### Priority 2 — 100–249 real images
34 classes (e.g. lettuce__mosaic_virus, carrot__alternaria, eggplant__phomopsis, strawberry__leaf_scorch, maple__tar_spot, cauliflower__bacterial_soft_rot, ginger__sheath_blight, banana__cigar_end_rot, banana__black_leaf_streak, tobacco__blue_mold, rice__blast, etc.). See matrix — each needs roughly 150–300 more real images.

### Priority 3 — 250–399 real images
10 classes (e.g. garlic__leaf_blight, corn__rust, cherry__leaf_spot, squash__powdery_mildew, wheat__loose_smut, zucchini__downy_mildew, coffee__leaf_rust, apple__rust, etc.). See matrix.

### Shared `healthy` class (class_id 0)
- Current: **6,939** images (train 5308 / val 590 / test 1041). Large but **shared across all crops**.
- **Implication:** the 400–500 target is per-disease-class; `healthy` should instead be balanced PER CROP. Verify each crop has enough healthy leaves; fill crop-specific healthy gaps from PlantVillage "healthy" / New Plant Diseases healthy folders. Do NOT treat 6,939 as one homogeneous class.

### Best multi-class downloads for Model 2 (one download, many disease classes)
1. **PlantVillage** — https://github.com/spMohanty/PlantVillage-Dataset → tomato (9 diseases), potato (2), apple (4), grape (4), corn (4), bell_pepper, cherry (2), peach, strawberry, blueberry, soybean, squash, orange/citrus. Highest reliability.
2. **New Plant Diseases Dataset** — https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset → apple, blueberry, cherry, corn, grape, orange, peach, bell_pepper, potato, raspberry, soybean, squash, strawberry, tomato (~38 classes).
3. **PlantDoc** — https://github.com/pratikkayal/PlantDoc-Dataset → 13 crops / 17 disease classes incl. bell_pepper, broccoli, carrot, celery, cherry, corn, cucumber, eggplant, potato, rice, strawberry, tobacco (real-world photos).
4. **Anand Soybean Rust (HF)** — https://huggingface.co/datasets → soybean__rust.
5. **iNaturalist** — https://www.inaturalist.org → manual curation for raspberry, coffee, ginger, garlic, maple, celery, broccoli ring spot, tobacco frogeye.

### Classes flagged MANUAL CURATION / NO VERIFIED BULK SOURCE
coffee__black_rot, coffee__brown_eye_spot, coffee__berry_blotch, ginger__leaf_spot, ginger__sheath_blight, garlic__leaf_blight, garlic__rust, maple__tar_spot, raspberry__leaf_spot, raspberry__fire_blight, raspberry__gray_mold, raspberry__yellow_rust, broccoli__ring_spot, celery__anthracnose, celery__early_blight, plum__bacterial_spot, plum__brown_rot, plum__pocket_disease, plum__pox_virus, plum__rust, bell_pepper__powdery_mildew, bell_pepper__frogeye_leaf_spot, carrot__cercospora_leaf_blight. **Do NOT relabel visually similar diseases as these target diseases.**
