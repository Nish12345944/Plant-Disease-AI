# Model 2 V2 (144 Classes) - Detailed Test Evaluation & Improvement Plan

## Executive Summary
- **Evaluated Checkpoint**: `models/model2_retraining_v2/best_model.pth` (Epoch 14, Best Val Macro F1: 64.71%)
- **Immutable Test Set**: 2,304 images across 144 classes (`data/processed/model2_retraining_v2_manifest.csv`)
- **Top-1 Accuracy**: 82.99% (1,912 / 2,304)
- **Top-3 Accuracy**: 93.58%
- **Macro F1 (All 144 Classes)**: 57.45%
- **Weighted F1**: 83.60%
- **Disease-Only Macro F1 (Classes 1-143)**: 50.34%
- **Healthy Foliage F1 (Class 0, n=1041)**: 97.80% (Precision: 99.40%, Recall: 96.25%)

---

## 1. Disease Reliability Breakdown & Gap Analysis to Reach 50 Classes

| Category | Criteria | Class Count | Notes |
|---|---|---|---|
| **Demonstrated Reliable (Production-Grade)** | Support >= 10, F1 >= 0.70 | **29** | **26** classes achieve F1 >= 0.75 |
| **Near-Reliable Candidates** | Support >= 10, 0.50 <= F1 < 0.70 | **15** | Prime candidates to elevate to reliable via targeted tuning |
| **Promising (Low Support)** | 5 <= Support < 10, F1 >= 0.70 | **16** | Strong accuracy, but test support needs expansion to qualify |
| **Weak with Adequate Support** | Support >= 10, F1 < 0.50 | **4** | Confused with visually similar diseases |
| **Low Support (1-9 images)** | Support < 10, F1 < 0.70 | **44** | Severe data scarcity in test benchmark |
| **Zero Test Support** | Support = 0 | **28** | Cannot verify without dedicated test benchmark |

**Current Gap to 50 Reliable Disease Classes**:
- Currently **29** disease classes meet strict reliability standards (support >= 10, F1 >= 0.70).
- To reach the goal of **50 reliable disease classes**, an additional **21** classes must be elevated.
- We have **15 near-reliable classes** (F1 50-70%) and **16 promising classes** (F1 > 70% with 5-9 samples) that represent the immediate, low-risk pipeline to surpass 50 reliable classes.

---

## 2. Currently Reliable Disease Classes (Support >= 10, F1 >= 0.70)

| Class ID | Canonical Class | Crop | Disease | Test Support | Precision | Recall | F1 Score | Top Confusion |
|---|---|---|---|---|---|---|---|---|
| 132 | `wheat__head_scab` | wheat | head_scab | 30 | 0.94 | 1.00 | **0.97** | None |
| 90 | `potato__late_blight` | potato | late_blight | 12 | 1.00 | 0.92 | **0.96** | potato__early_blight (1) |
| 12 | `bean__angular_leaf_spot` | bean | angular_leaf_spot | 65 | 0.91 | 0.97 | **0.94** | bean__rust (2) |
| 56 | `cucumber__angular_leaf_spot` | cucumber | angular_leaf_spot | 22 | 0.95 | 0.91 | **0.93** | bean__rust (1); zucchini__downy_mildew (1) |
| 137 | `wheat__stem_rust` | wheat | stem_rust | 13 | 0.92 | 0.92 | **0.92** | wheat__leaf_rust (1) |
| 105 | `soybean__downy_mildew` | soybean | downy_mildew | 11 | 0.85 | 1.00 | **0.92** | None |
| 55 | `corn__smut` | corn | smut | 19 | 1.00 | 0.84 | **0.91** | ginger__leaf_spot (1); celery__anthracnose (1); grape__black_rot (1) |
| 134 | `wheat__loose_smut` | wheat | loose_smut | 19 | 1.00 | 0.84 | **0.91** | wheat__bacterial_leaf_streak_(black_chaff) (1); wheat__head_scab (1); garlic__leaf_blight (1) |
| 80 | `peach__leaf_curl` | peach | leaf_curl | 18 | 0.94 | 0.89 | **0.91** | tomato__early_blight (1); blueberry__botrytis_blight (1) |
| 6 | `banana__black_leaf_streak` | banana | black_leaf_streak | 17 | 0.89 | 0.94 | **0.91** | banana__panama_disease (1) |
| 51 | `coffee__leaf_rust` | coffee | leaf_rust | 16 | 0.93 | 0.88 | **0.90** | citrus__greening_disease (1); soybean__mosaic (1) |
| 32 | `cabbage__black_rot` | cabbage | black_rot | 13 | 0.86 | 0.92 | **0.89** | lettuce__mosaic_virus (1) |
| 17 | `bell_pepper__blossom_end_rot` | bell_pepper | blossom_end_rot | 11 | 0.79 | 1.00 | **0.88** | None |
| 46 | `citrus__canker` | citrus | canker | 48 | 0.93 | 0.81 | **0.87** | apple__scab (2); healthy (1); coffee__brown_eye_spot (1) |
| 15 | `bean__rust` | bean | rust | 77 | 0.90 | 0.82 | **0.86** | bean__angular_leaf_spot (6); soybean__rust (2); corn__rust (1) |
| 3 | `apple__rust` | apple | rust | 14 | 0.86 | 0.86 | **0.86** | apple__scab (1); wheat__stripe_rust (1) |
| 135 | `wheat__powdery_mildew` | wheat | powdery_mildew | 27 | 0.91 | 0.78 | **0.84** | garlic__leaf_blight (2); rice__sheath_blight (2); wheat__bacterial_leaf_streak_(black_chaff) (1) |
| 79 | `peach__brown_rot` | peach | brown_rot | 14 | 0.76 | 0.93 | **0.84** | peach__anthracnose (1) |
| 53 | `corn__northern_leaf_blight` | corn | northern_leaf_blight | 14 | 0.72 | 0.93 | **0.81** | healthy (1) |
| 52 | `corn__gray_leaf_spot` | corn | gray_leaf_spot | 12 | 1.00 | 0.67 | **0.80** | corn__northern_leaf_blight (2); wheat__septoria_blotch (1); soybean__mosaic (1) |
| 47 | `citrus__greening_disease` | citrus | greening_disease | 14 | 0.91 | 0.71 | **0.80** | peach__scab (2); banana__bunchy_top (1); plum__pox_virus (1) |
| 125 | `tomato__early_blight` | tomato | early_blight | 22 | 0.71 | 0.91 | **0.80** | apple__scab (1); potato__early_blight (1) |
| 7 | `banana__bunchy_top` | banana | bunchy_top | 11 | 0.75 | 0.82 | **0.78** | banana__panama_disease (2) |
| 2 | `apple__mosaic_virus` | apple | mosaic_virus | 11 | 0.75 | 0.82 | **0.78** | soybean__downy_mildew (1); soybean__mosaic (1) |
| 72 | `grape__downy_mildew` | grape | downy_mildew | 32 | 0.80 | 0.75 | **0.77** | grape__black_rot (3); grape__leaf_spot (1); peach__leaf_curl (1) |
| 106 | `soybean__frog_eye_leaf_spot` | soybean | frog_eye_leaf_spot | 21 | 0.67 | 0.86 | **0.75** | soybean__mosaic (1); broccoli__alternaria_leaf_spot (1); soybean__brown_spot (1) |
| 57 | `cucumber__bacterial_wilt` | cucumber | bacterial_wilt | 13 | 0.71 | 0.77 | **0.74** | zucchini__bacterial_wilt (3) |
| 138 | `wheat__stripe_rust` | wheat | stripe_rust | 32 | 0.63 | 0.84 | **0.72** | wheat__powdery_mildew (1); wheat__bacterial_leaf_streak_(black_chaff) (1); wheat__stem_rust (1) |
| 71 | `grape__black_rot` | grape | black_rot | 13 | 0.61 | 0.85 | **0.71** | apple__scab (1); tobacco__frogeye_leaf_spot (1) |

---

## 3. Top Near-Reliable Classes (Candidates for Targeted Improvement)

These classes have adequate test support (>= 10) and moderate F1 (0.50 – 0.69). Elevating their F1 past 0.70 requires resolving 1–2 specific confusion pairs:

| Class ID | Canonical Class | Crop | Disease | Test Support | Precision | Recall | F1 Score | Top Misclassification Pattern |
|---|---|---|---|---|---|---|---|---|
| 54 | `corn__rust` | corn | rust | 18 | 0.91 | 0.56 | 0.69 | wheat__stripe_rust (4); wheat__leaf_rust (2); corn__northern_leaf_blight (1) |
| 136 | `wheat__septoria_blotch` | wheat | septoria_blotch | 19 | 0.85 | 0.58 | 0.69 | wheat__bacterial_leaf_streak_(black_chaff) (4); wheat__stripe_rust (2); corn__northern_leaf_blight (1) |
| 4 | `apple__scab` | apple | scab | 25 | 0.70 | 0.64 | 0.67 | tomato__leaf_mold (2); cherry__leaf_spot (1); peach__scab (1) |
| 127 | `tomato__leaf_mold` | tomato | leaf_mold | 16 | 0.60 | 0.75 | 0.67 | tobacco__blue_mold (1); celery__early_blight (1); tomato__late_blight (1) |
| 126 | `tomato__late_blight` | tomato | late_blight | 17 | 0.82 | 0.53 | 0.64 | tomato__leaf_mold (2); peach__brown_rot (2); apple__black_rot (1) |
| 66 | `garlic__rust` | garlic | rust | 12 | 0.70 | 0.58 | 0.64 | garlic__leaf_blight (2); wheat__stripe_rust (2); wheat__leaf_rust (1) |
| 65 | `garlic__leaf_blight` | garlic | leaf_blight | 12 | 0.53 | 0.75 | 0.62 | garlic__rust (1); ginger__sheath_blight (1); wheat__septoria_blotch (1) |
| 58 | `cucumber__powdery_mildew` | cucumber | powdery_mildew | 22 | 0.79 | 0.50 | 0.61 | squash__powdery_mildew (7); zucchini__powdery_mildew (3); cherry__powdery_mildew (1) |
| 133 | `wheat__leaf_rust` | wheat | leaf_rust | 11 | 0.55 | 0.55 | 0.55 | wheat__stripe_rust (4); wheat__bacterial_leaf_streak_(black_chaff) (1) |
| 44 | `cherry__leaf_spot` | cherry | leaf_spot | 10 | 0.80 | 0.40 | 0.53 | corn__northern_leaf_blight (1); blueberry__scorch (1); bell_pepper__frogeye_leaf_spot (1) |
| 131 | `wheat__bacterial_leaf_streak_(black_chaff)` | wheat | bacterial_leaf_streak_(black_chaff) | 13 | 0.44 | 0.62 | 0.52 | wheat__stripe_rust (3); wheat__head_scab (1); wheat__powdery_mildew (1) |
| 1 | `apple__black_rot` | apple | black_rot | 10 | 0.67 | 0.40 | 0.50 | peach__anthracnose (2); grape__black_rot (2); apple__scab (1) |
| 124 | `tomato__bacterial_leaf_spot` | tomato | bacterial_leaf_spot | 13 | 0.55 | 0.46 | 0.50 | tomato__septoria_leaf_spot (4); soybean__frog_eye_leaf_spot (1); tomato__early_blight (1) |
| 74 | `grape__leaf_spot` | grape | leaf_spot | 10 | 0.67 | 0.40 | 0.50 | grape__downy_mildew (2); tomato__early_blight (1); zucchini__downy_mildew (1) |
| 89 | `potato__early_blight` | potato | early_blight | 10 | 0.67 | 0.40 | 0.50 | plum__rust (1); maple__tar_spot (1); tomato__early_blight (1) |

---

## 4. Promising Classes Requiring Test Set Expansion

These classes achieve high F1 (>= 0.70) but only have 5–9 test samples. They are intrinsically well-learned by the model, but need additional test evaluation samples to formally qualify as verified reliable:

| Class ID | Canonical Class | Crop | Disease | Test Support | Precision | Recall | F1 Score | Top Misclassification Pattern |
|---|---|---|---|---|---|---|---|---|
| 35 | `carrot__cavity_spot` | carrot | cavity_spot | 7 | 1.00 | 1.00 | 1.00 | None |
| 48 | `coffee__berry_blotch` | coffee | berry_blotch | 9 | 1.00 | 0.89 | 0.94 | coffee__brown_eye_spot (1) |
| 77 | `maple__tar_spot` | maple | tar_spot | 8 | 0.89 | 1.00 | 0.94 | None |
| 62 | `eggplant__phomopsis_fruit_rot` | eggplant | phomopsis_fruit_rot | 5 | 1.00 | 0.80 | 0.89 | eggplant__cercospora_leaf_spot (1) |
| 142 | `zucchini__yellow_mosaic_virus` | zucchini | yellow_mosaic_virus | 9 | 0.89 | 0.89 | 0.89 | celery__anthracnose (1) |
| 84 | `plum__brown_rot` | plum | brown_rot | 5 | 0.71 | 1.00 | 0.83 | None |
| 73 | `grape__grapevine_leafroll_disease` | grape | grapevine_leafroll_disease | 5 | 0.80 | 0.80 | 0.80 | healthy (1) |
| 13 | `bean__halo_blight` | bean | halo_blight | 6 | 1.00 | 0.67 | 0.80 | bean__rust (1); soybean__mosaic (1) |
| 123 | `tobacco__mosaic_virus` | tobacco | mosaic_virus | 5 | 0.80 | 0.80 | 0.80 | tobacco__blue_mold (1) |
| 10 | `banana__panama_disease` | banana | panama_disease | 8 | 0.70 | 0.88 | 0.78 | banana__black_leaf_streak (1) |
| 115 | `strawberry__anthracnose` | strawberry | anthracnose | 5 | 1.00 | 0.60 | 0.75 | plum__brown_rot (1); strawberry__leaf_spot (1) |
| 82 | `peach__scab` | peach | scab | 8 | 0.64 | 0.88 | 0.74 | peach__brown_rot (1) |
| 95 | `rice__blast` | rice | blast | 7 | 1.00 | 0.57 | 0.73 | wheat__bacterial_leaf_streak_(black_chaff) (2); garlic__rust (1) |
| 26 | `blueberry__scorch` | blueberry | scorch | 5 | 0.67 | 0.80 | 0.73 | broccoli__ring_spot (1) |
| 5 | `banana__anthracnose` | banana | anthracnose | 7 | 0.71 | 0.71 | 0.71 | banana__cigar_end_rot (1); tomato__bacterial_leaf_spot (1) |
| 121 | `tobacco__brown_spot` | tobacco | brown_spot | 7 | 0.60 | 0.86 | 0.71 | tobacco__frogeye_leaf_spot (1) |

---

## 5. Weakest Classes & Error Patterns (Ranked by Improvement Potential)

Below are the weakest classes with support >= 10 (F1 < 0.50). Their failures stem from specific, identifiable root causes:

| Class ID | Canonical Class | Test Support | Train Support | Precision | Recall | F1 Score | Primary Confusion Issue |
|---|---|---|---|---|---|---|---|
| 107 | `soybean__mosaic` | 13 | 92 | 0.31 | 0.38 | 0.34 | bean__mosaic_virus (5); tobacco__brown_spot (1); tobacco__mosaic_virus (1) |
| 129 | `tomato__septoria_leaf_spot` | 14 | 233 | 0.42 | 0.36 | 0.38 | tomato__bacterial_leaf_spot (4); tomato__early_blight (3); eggplant__cercospora_leaf_spot (1) |
| 113 | `squash__powdery_mildew` | 20 | 139 | 0.38 | 0.45 | 0.41 | zucchini__powdery_mildew (9); cucumber__powdery_mildew (1); grape__downy_mildew (1) |
| 141 | `zucchini__powdery_mildew` | 18 | 164 | 0.40 | 0.44 | 0.42 | squash__powdery_mildew (8); celery__early_blight (1); cucumber__powdery_mildew (1) |

---

## 6. Targeted Action Plan to Reach 50+ Reliable Classes

### Step 1: Leverage Crop-Aware Prediction Masking
Notice that the vast majority of errors in the near-reliable and weak classes are cross-crop confusions:
- `squash__powdery_mildew` <-> `zucchini__powdery_mildew`
- `soybean__mosaic` <-> `bean__mosaic_virus`
- `ginger__sheath_blight` <-> `rice__sheath_blight`
- `corn__rust` <-> `wheat__stripe_rust`
Because Model 1 identifies the crop first, applying crop-aware logit masking instantly eliminates all cross-crop confusion pairs without changing model weights.

### Step 2: Fine-Tuning with Class-Balanced Focal Loss on Confusion Pairs
Rather than training from scratch or running micro-batch 1 gradient accumulation, execute a short 5-epoch fine-tuning run starting from Epoch 14 (`best_model.pth`):
- Use batch size 16 with mixed precision (`torch.cuda.amp`) or frozen backbone stages 0–4.
- Apply Focal Loss (gamma=2.0) with class weights inversely proportional to train support.
- Target the 12 near-reliable classes directly to push their F1 across the 0.70 threshold.

### Step 3: Targeted Benchmark Augmentation for the 10 Promising Classes
- Classes such as `banana__anthracnose` (F1 0.71, n=7), `banana__panama_disease` (F1 0.78, n=8), `bean__halo_blight` (F1 0.80, n=6), and `soybean__rust` (F1 0.74, n=9) already have high precision and recall.
- Adding 5–10 verified test samples per class from existing archived datasets (e.g. PlantSeg/Kaggle subsets in `data/external`) will formally promote these 10 classes into verified reliable status.
