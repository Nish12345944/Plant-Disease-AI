# Final Data Acquisition Summary — Model 1 & Model 2

**Generated:** 2026-10-09 from authoritative project manifests. **No datasets downloaded, no models trained, no production/protected data changed.**

## Headline counts

| Metric | Model 1 (Plant ID) | Model 2 (Disease) |
|---|---|---|
| Active classes | **44** with data (+1 empty: gypsophila) | **116 disease** classes + **1 shared healthy** |
| Classes below 400 | 26 | 113 |
| Classes below 500 | 29 | 114 |
| Classes below 100 | 8 (6 real + 1 zero + 1 near-zero gerbera) | 69 |
| Additional REAL images to reach **400** | **6,467** | **33,766** (disease classes only) |
| Additional REAL images to reach **500** | **9,291** | **45,134** (disease classes only) |
| Safely reusable from existing project sources | **298** (gerbera 251, gypsophila 47 — staged, not yet in splits) | **0** identified for disease gaps |
| Must be manually downloaded (after reuse) | **6,169** to 400 / **8,993** to 500 | **33,766** to 400 / **45,134** to 500 |

**Model 1 grand total to download: ≈ 6,169 real images (400-target) or 8,993 (500-target).**
**Model 2 grand total to download: ≈ 33,766 real images (400-target) or 45,134 (500-target).**

## Counting method (no double counting)
- Per-class shortfall = `max(0, target − current_unique_real)`, summed across classes.
- Model 1 reuse (298) is already present on disk in `data/external/model1_expansion/` but NOT yet in the `model1_expanded` train/val/test splits, so it is counted once and subtracted before the external requirement.
- Multi-crop datasets (PlantVillage, New Plant Diseases, PlantDoc) are downloaded once and split by crop/disease folder; each image is counted toward exactly ONE class after hash-based dedupe. No image is counted twice.
- `healthy` (class_id 0, 6,939 images) is a SHARED class and is excluded from the per-disease 400–500 sum. It must instead be balanced PER CROP — check per-crop healthy coverage, do not inflate one crop.

## Model 1 taxonomy & exclusions
- 46 slots; **44 active** (2 empty slots).
- `cherry_tomato` = **alias of `tomato`** → not acquired.
- `french_bean`, `capsicum`, `zucchini` are canonical; aliases bean/bell_pepper/squash fold in.
- **gypsophila**: known data-availability problem, currently 0 images. Partial staged Roboflow set (CC BY 4.0, ~47 usable gypsophila of 143 total across Gypsophila/Hydrangea/Daisy) leaves ~353 still required externally.

## Model 2 disease detail
- 116 disease classes: **69 below 100**, **103 below 250**, **113 below 400**.
- **74 classes have val<10 or test<10** → unreliable evaluation; even after acquisition, reserve ~15% for val/test and consider enlarging the protected test split only via an approved re-split (not by hand here).
- **105 disease classes** have a verified bulk source (PlantVillage / New Plant Diseases / PlantDoc / iNaturalist).
- **11 classes are effectively MANUAL CURATION** (no reliable bulk disease source): coffee (3), raspberry (3), garlic (2), plus ginger__leaf_spot, ginger__sheath_blight, broccoli__ring_spot, celery__anthracnose, plum (several), bell_pepper__powdery_mildew, bell_pepper__frogeye_leaf_spot, carrot__cercospora_leaf_blight. Do NOT relabel similar diseases as these.

## Augmentation priorities (see `final_augmentation_matrix.csv`)
- **Model 1 (46 rows):** 20 classes already ≥400 → moderate augmentation OK; 11 classes 150–399 → augment only after reaching ~200–300 real; **15 classes → HOLD** augmentation until ≥200 real collected (gypsophila, cherry_tomato, gerbera, lilium, carnation, basil, celery, ginger, anthurium, cauliflower, maple, raspberry, eggplant, cherry). Plant-identity-preserving transforms only (flip/rotate/scale/brightness), training images only.
- **Model 2 (117 rows):** **30 disease classes are HIGH/CONSERVATIVE risk** (virus/mosaic, rust pustules, septoria/leaf_spot, powdery_mildew, greening) — very conservative transforms, no blur/erasing/colour-fabrication. 86 moderate. `healthy` = low risk. Validation/test remain unaugmented and deterministic.

## Storage estimate (defensible)
Average curated leaf image ≈ 120–200 KB JPEG. At ~180 KB:
- Model 1 to 400: 6,169 × 180 KB ≈ **1.1 GB**; to 500 ≈ 1.6 GB.
- Model 2 to 400: 33,766 × 180 KB ≈ **6.1 GB**; to 500 ≈ 8.1 GB.
- Combined (500-target): **≈ 9.7 GB** of new source images (before any augmentation variants). If you augment 4× on disk rather than on-the-fly, multiply stored bytes accordingly — prefer on-the-fly augmentation to avoid this.

## Top multi-class datasets to download first
1. **PlantVillage** — https://github.com/spMohanty/PlantVillage-Dataset — fills most Model 2 tomato/potato/apple/grape/corn/bell_pepper/cherry/strawberry/soybean/squash + Model 1 healthy. Highest reliability.
2. **New Plant Diseases Dataset** — https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset — ~38 crop-disease classes (Kaggle account needed).
3. **PlantDoc** — https://github.com/pratikkayal/PlantDoc-Dataset — real-world photos for 13 crops incl. the hard Model 2 crops (broccoli, carrot, celery, bell_pepper, tobacco, strawberry).
4. **Oxford Flowers 102** — https://www.robots.ox.ac.uk/~vgg/data/flowers/102/ — Model 1 flowers (carnation, lilium, chrysanthemum, geranium, marigold, orchid, rose, gerbera).
5. **iNaturalist** — https://www.inaturalist.org — Model 1 all plants + manual curation for Model 2 coffee/raspberry/ginger/garlic/maple.

## Generated report paths
- `reports/joint_dataset_improvement/final_model1_acquisition_matrix.csv`
- `reports/joint_dataset_improvement/final_model2_acquisition_matrix.csv`
- `reports/joint_dataset_improvement/manual_download_checklist.md`
- `reports/joint_dataset_improvement/final_augmentation_matrix.csv`
- `reports/joint_dataset_improvement/final_acquisition_summary.md` (this file)
