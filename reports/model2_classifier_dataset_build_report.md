# Model 2 Disease Classifier: Dataset Construction & Validation Report

**Date:** 2026-10-07  
**Module:** Model 2 Disease Classifier (EfficientNet-B2 Classification Dataset)  
**Target Directory:** [`data/processed/model2_classifier/`](file:///data/processed/model2_classifier/)  

---

## 1. Executive Summary & Core Dataset Metrics

```
TOTAL IMAGES PROCESSED             : 15,304 images
TOTAL CLASSIFICATION CLASSES       : 117 classes (1 shared 'healthy' + 115 'crop__disease')
TOTAL CROPS REPRESENTED            : 39 crops
TOTAL HEALTHY IMAGES               : 6,939 images (45.3%)
TOTAL DISEASED IMAGES              : 8,365 images (54.7%)
TRAIN SPLIT (70%)                  : 10,705 images
VAL SPLIT (15%)                    : 2,295 images
TEST SPLIT (15%)                   : 2,304 images
CLASSES < 20 IMAGES                : 16 classes
CLASSES < 50 IMAGES                : 55 classes
CLASSES < 100 IMAGES               : 93 classes
```

---

## 2. Source Dataset Contributions

| Source Dataset | Image Count | Contribution (%) | Description |
| :--- | :--- | :--- | :--- |
| `external_healthy_bell_pepper` | 708 | 4.6% | Audited external verified healthy leaf folder |
| `makerere_beans` | 1,295 | 8.5% | Makerere Bean leaf disease & healthy dataset |
| `model1_balanced_healthy` | 3,181 | 20.8% | Verified Model 1 balanced healthy foliage pool |
| `external_healthy_turnip` | 181 | 1.2% | Audited external verified healthy leaf folder |
| `external_healthy_spinach` | 694 | 4.5% | Audited external verified healthy leaf folder |
| `external_healthy_strawberry` | 279 | 1.8% | Audited external verified healthy leaf folder |
| `external_healthy_tomato` | 1,420 | 9.3% | Audited external verified healthy leaf folder |
| `external_healthy_cabbage` | 12 | 0.1% | Audited external verified healthy leaf folder |
| `external_healthy_broccoli` | 8 | 0.1% | Audited external verified healthy leaf folder |
| `external_healthy_cauliflower` | 29 | 0.2% | Audited external verified healthy leaf folder |
| `plantseg` | 7,497 | 49.0% | Audited PlantSeg multi-crop disease collection |

---

## 3. Crop-Disease Compatibility Matrix (Machine-Readable Routing)

| Crop | Compatible Classes Count | Compatible Model 2 Classes |
| :--- | :--- | :--- |
| **Apple** | 5 | `apple__black_rot`, `apple__mosaic_virus`, `apple__rust`, `apple__scab`, `healthy` |
| **Banana** | 7 | `banana__anthracnose`, `banana__black_leaf_streak`, `banana__bunchy_top`, `banana__cigar_end_rot`, `banana__cordana_leaf_spot` *(+2 more)* |
| **Basil** | 2 | `basil__downy_mildew`, `healthy` |
| **Bean** | 5 | `bean__angular_leaf_spot`, `bean__halo_blight`, `bean__mosaic_virus`, `bean__rust`, `healthy` |
| **Bell Pepper** | 5 | `bell_pepper__bacterial_spot`, `bell_pepper__blossom_end_rot`, `bell_pepper__frogeye_leaf_spot`, `bell_pepper__powdery_mildew`, `healthy` |
| **Blueberry** | 6 | `blueberry__anthracnose`, `blueberry__botrytis_blight`, `blueberry__mummy_berry`, `blueberry__rust`, `blueberry__scorch` *(+1 more)* |
| **Broccoli** | 4 | `broccoli__alternaria_leaf_spot`, `broccoli__downy_mildew`, `broccoli__ring_spot`, `healthy` |
| **Cabbage** | 4 | `cabbage__alternaria_leaf_spot`, `cabbage__black_rot`, `cabbage__downy_mildew`, `healthy` |
| **Capsicum** | 1 | `healthy` |
| **Carrot** | 4 | `carrot__alternaria_leaf_blight`, `carrot__cavity_spot`, `carrot__cercospora_leaf_blight`, `healthy` |
| **Cauliflower** | 3 | `cauliflower__alternaria_leaf_spot`, `cauliflower__bacterial_soft_rot`, `healthy` |
| **Celery** | 3 | `celery__anthracnose`, `celery__early_blight`, `healthy` |
| **Cherry** | 3 | `cherry__leaf_spot`, `cherry__powdery_mildew`, `healthy` |
| **Citrus** | 3 | `citrus__canker`, `citrus__greening_disease`, `healthy` |
| **Coffee** | 5 | `coffee__berry_blotch`, `coffee__black_rot`, `coffee__brown_eye_spot`, `coffee__leaf_rust`, `healthy` |
| **Corn** | 5 | `corn__gray_leaf_spot`, `corn__northern_leaf_blight`, `corn__rust`, `corn__smut`, `healthy` |
| **Cucumber** | 4 | `cucumber__angular_leaf_spot`, `cucumber__bacterial_wilt`, `cucumber__powdery_mildew`, `healthy` |
| **Eggplant** | 4 | `eggplant__cercospora_leaf_spot`, `eggplant__phomopsis_fruit_rot`, `eggplant__phytophthora_blight`, `healthy` |
| **Garlic** | 3 | `garlic__leaf_blight`, `garlic__rust`, `healthy` |
| **Ginger** | 3 | `ginger__leaf_spot`, `ginger__sheath_blight`, `healthy` |
| **Grape** | 5 | `grape__black_rot`, `grape__downy_mildew`, `grape__grapevine_leafroll_disease`, `grape__leaf_spot`, `healthy` |
| **Lettuce** | 3 | `healthy`, `lettuce__downy_mildew`, `lettuce__mosaic_virus` |
| **Maple** | 2 | `healthy`, `maple__tar_spot` |
| **Marigold** | 1 | `healthy` |
| **Peach** | 6 | `healthy`, `peach__anthracnose`, `peach__brown_rot`, `peach__leaf_curl`, `peach__rust` *(+1 more)* |
| **Plum** | 6 | `healthy`, `plum__bacterial_spot`, `plum__brown_rot`, `plum__pocket_disease`, `plum__pox_virus` *(+1 more)* |
| **Potato** | 3 | `healthy`, `potato__early_blight`, `potato__late_blight` |
| **Raspberry** | 5 | `healthy`, `raspberry__fire_blight`, `raspberry__gray_mold`, `raspberry__leaf_spot`, `raspberry__yellow_rust` |
| **Rice** | 3 | `healthy`, `rice__blast`, `rice__sheath_blight` |
| **Rose** | 1 | `healthy` |
| **Soybean** | 7 | `healthy`, `soybean__bacterial_blight`, `soybean__brown_spot`, `soybean__downy_mildew`, `soybean__frog_eye_leaf_spot` *(+2 more)* |
| **Spinach** | 1 | `healthy` |
| **Squash** | 2 | `healthy`, `squash__powdery_mildew` |
| **Strawberry** | 3 | `healthy`, `strawberry__anthracnose`, `strawberry__leaf_scorch` |
| **Tobacco** | 5 | `healthy`, `tobacco__blue_mold`, `tobacco__brown_spot`, `tobacco__frogeye_leaf_spot`, `tobacco__mosaic_virus` |
| **Tomato** | 8 | `healthy`, `tomato__bacterial_leaf_spot`, `tomato__early_blight`, `tomato__late_blight`, `tomato__leaf_mold` *(+3 more)* |
| **Turnip** | 1 | `healthy` |
| **Wheat** | 9 | `healthy`, `wheat__bacterial_leaf_streak_(black_chaff)`, `wheat__head_scab`, `wheat__leaf_rust`, `wheat__loose_smut` *(+4 more)* |
| **Zucchini** | 5 | `healthy`, `zucchini__bacterial_wilt`, `zucchini__downy_mildew`, `zucchini__powdery_mildew`, `zucchini__yellow_mosaic_virus` |

---

## 4. Lowest-Count Classes & Tail Distribution Flagging

| Class Name | Total Images | Train | Val | Test | Balance Tier |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `coffee__black_rot` | 3 | 2 | 1 | 0 | Critical (<20) |
| `peach__rust` | 5 | 3 | 1 | 1 | Critical (<20) |
| `broccoli__ring_spot` | 7 | 5 | 1 | 1 | Critical (<20) |
| `peach__anthracnose` | 10 | 7 | 2 | 1 | Critical (<20) |
| `plum__bacterial_spot` | 10 | 7 | 2 | 1 | Critical (<20) |
| `celery__anthracnose` | 11 | 8 | 2 | 1 | Critical (<20) |
| `coffee__brown_eye_spot` | 11 | 8 | 2 | 1 | Critical (<20) |
| `raspberry__leaf_spot` | 11 | 8 | 2 | 1 | Critical (<20) |
| `tobacco__frogeye_leaf_spot` | 15 | 10 | 2 | 3 | Critical (<20) |
| `carrot__cercospora_leaf_blight` | 16 | 11 | 2 | 3 | Critical (<20) |
| `plum__rust` | 17 | 12 | 3 | 2 | Critical (<20) |
| `raspberry__gray_mold` | 17 | 12 | 3 | 2 | Critical (<20) |
| `bell_pepper__powdery_mildew` | 18 | 13 | 3 | 2 | Critical (<20) |
| `cauliflower__bacterial_soft_rot` | 18 | 13 | 3 | 2 | Critical (<20) |
| `blueberry__botrytis_blight` | 19 | 13 | 3 | 3 | Critical (<20) |
| `strawberry__leaf_scorch` | 19 | 13 | 3 | 3 | Critical (<20) |
| `eggplant__phytophthora_blight` | 22 | 15 | 3 | 4 | Low (20-49) |
| `ginger__leaf_spot` | 22 | 15 | 3 | 4 | Low (20-49) |
| `lettuce__mosaic_virus` | 22 | 15 | 3 | 4 | Low (20-49) |
| `plum__pox_virus` | 22 | 15 | 3 | 4 | Low (20-49) |
| `raspberry__yellow_rust` | 22 | 15 | 3 | 4 | Low (20-49) |
| `bell_pepper__frogeye_leaf_spot` | 23 | 16 | 3 | 4 | Low (20-49) |
| `broccoli__downy_mildew` | 23 | 16 | 3 | 4 | Low (20-49) |
| `raspberry__fire_blight` | 23 | 16 | 3 | 4 | Low (20-49) |
| `cherry__powdery_mildew` | 25 | 18 | 4 | 3 | Low (20-49) |

---

## 5. Automated Verification Checklist

- [x] **Zero Corrupt Images**: 100% of generated images verified via PIL open/verify.
- [x] **Zero Cross-Split Leakage**: SHA-256 hash sets across train, val, and test are completely disjoint.
- [x] **Deterministic Class IDs**: Class IDs are 0-indexed and contiguous (0 to 115).
- [x] **Canonical Healthy Class**: Index 0 assigned to unified `healthy` foliage class.
- [x] **Manifest Integrity**: 100% of rows in manifest map to verified files on disk.
- [x] **Crop Compatibility Matrix**: Machine-readable mapping generated for two-stage inference masking.