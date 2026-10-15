# Model 2 Retraining V2 - FINAL TEST EVALUATION (Immutable Protected Benchmark)

**Generated:** 2026-10-13 11:19:13  
**Checkpoint:** `models/model2_retraining_v2/best_model.pth` (saved at epoch 14)  
**Test set:** 2,304 images (`data/processed/model2_retraining_v2_manifest.csv`, split == 'test')  
**Taxonomy:** 144 classes (`healthy` + 143 diseases)  
**Preprocessing:** Resize(260x260) -> ToTensor -> Normalize(ImageNet) - identical to production `predict.py`  
**Device:** cuda | **Duration:** 37.5s

## 1. Prerequisite Verification (all PASSED)

- Checkpoint classifier head = (144, 1408) - matches deployed taxonomy (strict state-dict load)
- Checkpoint `num_classes` field = 144 - matches mapping
- Deployed `models/model2_retraining_v2/class_mapping.json` byte-identical to dataset-dir copy (144 continuous ids, healthy=0)
- Manifest contains exactly 2304 test rows; every image exists on disk; every `class_id` consistent with the mapping
- No dataset substitution, no retraining, no threshold or mapping changes
- Checkpoint-embedded class mapping matches the deployed mapping file: **True**

## 2. Aggregate Test Metrics (n = 2,304, ALL samples included)

| Metric | Value |
|---|---|
| Test loss (CE) | 0.8164 |
| Top-1 accuracy | 82.99% (1912 / 2304) |
| Top-3 accuracy | 93.58% |
| Macro F1 (144 classes) | 57.45% |
| Weighted F1 | 83.60% |
| Disease-only macro F1 (classes 1-143) | 50.34% |
| Healthy precision (class 0, n=1041) | 99.40% |
| Healthy recall (class 0) | 96.25% |
| Healthy F1 (class 0) | 97.80% |

## 3. TEST vs VALIDATION (clearly distinguished)

| Metric | Validation (best epoch, n=3,049) | TEST (this report, n=2,304) | Delta |
|---|---|---|---|
| Top-1 accuracy | 78.68% | 82.99% | +4.31 pts |
| Top-3 accuracy | 91.11% | 93.58% | +2.47 pts |
| Macro F1 | 64.71% | 57.45% | -7.26 pts |
| Weighted F1 | 78.69% | 83.60% | +4.91 pts |
| Healthy F1 | 94.48% | 97.80% | +3.32 pts |
| Disease-only macro F1 | 64.50% | 50.34% | -14.16 pts |

Validation numbers come from `C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\reports\model2_retraining_v2\training_progress.csv` (best epoch 14 by val macro F1). Validation images guided model selection and are therefore optimistic; the test split was never seen during training or checkpoint selection.

## 4. Most Frequent Misclassifications (Top 25)

| Rank | Actual | Predicted | Count |
|---|---|---|---|
| 1 | healthy | spinach__pest_damage | 17 |
| 2 | squash__powdery_mildew | zucchini__powdery_mildew | 9 |
| 3 | zucchini__powdery_mildew | squash__powdery_mildew | 8 |
| 4 | cucumber__powdery_mildew | squash__powdery_mildew | 7 |
| 5 | bean__rust | bean__angular_leaf_spot | 6 |
| 6 | soybean__mosaic | bean__mosaic_virus | 5 |
| 7 | bean__mosaic_virus | soybean__mosaic | 4 |
| 8 | corn__rust | wheat__stripe_rust | 4 |
| 9 | ginger__sheath_blight | rice__sheath_blight | 4 |
| 10 | healthy | rose__pest_damage | 4 |
| 11 | tomato__bacterial_leaf_spot | tomato__septoria_leaf_spot | 4 |
| 12 | tomato__mosaic_virus | tomato__yellow_leaf_curl_virus | 4 |
| 13 | tomato__septoria_leaf_spot | tomato__bacterial_leaf_spot | 4 |
| 14 | wheat__leaf_rust | wheat__stripe_rust | 4 |
| 15 | wheat__septoria_blotch | wheat__bacterial_leaf_streak_(black_chaff) | 4 |
| 16 | cabbage__downy_mildew | broccoli__downy_mildew | 3 |
| 17 | cucumber__bacterial_wilt | zucchini__bacterial_wilt | 3 |
| 18 | cucumber__powdery_mildew | zucchini__powdery_mildew | 3 |
| 19 | grape__downy_mildew | grape__black_rot | 3 |
| 20 | healthy | tomato__leaf_mold | 3 |
| 21 | tomato__septoria_leaf_spot | tomato__early_blight | 3 |
| 22 | wheat__bacterial_leaf_streak_(black_chaff) | wheat__stripe_rust | 3 |
| 23 | zucchini__bacterial_wilt | cucumber__bacterial_wilt | 3 |
| 24 | apple__black_rot | grape__black_rot | 2 |
| 25 | apple__black_rot | peach__anthracnose | 2 |

Full pair list: `all_misclassification_pairs.csv` (270 distinct error pairs).

## 5. Low-Support & Zero-Support Classes (NOT excluded)

- Zero-support classes in the test split: **28** - bell_pepper__leaf_curl, blueberry__exobasidium, blueberry__septoria_leaf_spot, cauliflower__black_rot, cauliflower__downy_mildew, cauliflower__pest_damage, coffee__black_rot, eggplant__mosaic_virus, eggplant__pest_damage, eggplant__wilt_disease, ginger__leaf_blight, ginger__pest_damage, plum__shot_hole, rose__black_spot, rose__downy_mildew, rose__mosaic_virus, rose__pest_damage, rose__powdery_mildew, rose__rust, spinach__anthracnose, spinach__bacterial_spot, spinach__downy_mildew, spinach__pest_damage, strawberry__angular_leaf_spot, strawberry__gray_mold, strawberry__leaf_spot, strawberry__powdery_mildew, tomato__anthracnose
- Low-support classes (1-9 images): **67** - banana__anthracnose (n=7), banana__cigar_end_rot (n=4), banana__cordana_leaf_spot (n=4), banana__panama_disease (n=8), basil__downy_mildew (n=6), bean__halo_blight (n=6), bean__mosaic_virus (n=5), bell_pepper__bacterial_spot (n=7), bell_pepper__frogeye_leaf_spot (n=4), bell_pepper__powdery_mildew (n=2), blueberry__anthracnose (n=4), blueberry__botrytis_blight (n=3), blueberry__mummy_berry (n=4), blueberry__rust (n=5), blueberry__scorch (n=5), broccoli__alternaria_leaf_spot (n=8), broccoli__downy_mildew (n=4), broccoli__ring_spot (n=1), cabbage__alternaria_leaf_spot (n=6), cabbage__downy_mildew (n=8), carrot__alternaria_leaf_blight (n=7), carrot__cavity_spot (n=7), carrot__cercospora_leaf_blight (n=3), cauliflower__alternaria_leaf_spot (n=4), cauliflower__bacterial_soft_rot (n=2), celery__anthracnose (n=1), celery__early_blight (n=5), cherry__powdery_mildew (n=3), coffee__berry_blotch (n=9), coffee__brown_eye_spot (n=1), eggplant__cercospora_leaf_spot (n=6), eggplant__phomopsis_fruit_rot (n=5), eggplant__phytophthora_blight (n=4), ginger__leaf_spot (n=4), ginger__sheath_blight (n=8), grape__grapevine_leafroll_disease (n=5), lettuce__downy_mildew (n=8), lettuce__mosaic_virus (n=4), maple__tar_spot (n=8), peach__anthracnose (n=1), peach__rust (n=1), peach__scab (n=8), plum__bacterial_spot (n=1), plum__brown_rot (n=5), plum__pocket_disease (n=4), plum__pox_virus (n=4), plum__rust (n=2), raspberry__fire_blight (n=4), raspberry__gray_mold (n=2), raspberry__leaf_spot (n=1), raspberry__yellow_rust (n=4), rice__blast (n=7), rice__sheath_blight (n=8), soybean__bacterial_blight (n=9), soybean__brown_spot (n=7), soybean__rust (n=9), strawberry__anthracnose (n=5), strawberry__leaf_scorch (n=3), tobacco__blue_mold (n=5), tobacco__brown_spot (n=7), tobacco__frogeye_leaf_spot (n=3), tobacco__mosaic_virus (n=5), tomato__mosaic_virus (n=7), tomato__yellow_leaf_curl_virus (n=9), zucchini__bacterial_wilt (n=9), zucchini__downy_mildew (n=5), zucchini__yellow_mosaic_virus (n=9)
- All classes remain in macro F1 and in the per-class report; low-support rows are flagged in the `low_support` column of `test_classification_report.csv`.

## 6. Artifacts

- `evaluation_summary.json` - machine-readable summary incl. all per-class metrics
- `test_classification_report.csv` - per-class precision/recall/F1/support for all 144 classes
- `test_predictions.csv` - every one of the 2,304 predictions incl. failures (correct flag + top-3)
- `confusion_matrix.csv` / `confusion_matrix.png` - 144x144 test confusion matrix
- `top_misclassifications.csv` / `all_misclassification_pairs.csv` - error analysis

## 7. Follow-Up for the Reliability Audit

This evaluation supplies the per-class disease evidence recorded as MISSING in `reports/crop_disease_reliability_audit/reliability_audit.md` (all 143 disease rows carried `NOT_EVALUATED` disease metrics). The audit was not modified by this run; re-running its generator would now be able to apply the disease gate on real test metrics.
