# Crop-Disease Reliability Audit - Plant Disease AI (READ-ONLY, FINALIZED)

**Generated:** 2026-10-13 (original audit) | **Finalized with test evidence:** 2026-10-14 17:55:20  
**Scope:** deployed artifacts only; no retraining, mapping edits, checkpoint or deployment changes. This finalization populated the deployed Model 2 checkpoint's per-class TEST metrics; the original evaluation files were preserved unchanged.

## 1. Artifacts Verified

| Model | Artifact | Status |
|---|---|---|
| Model 1 (crop) | `models/model1_expanded/best_model.pth` + `class_mapping.json` | checkpoint head = 46 vs 46 classes: MATCH |
| Model 1 (crop) | `reports/model1_expansion/expanded_model1_per_class_metrics.csv` | per-crop P/R/F1/support, 1,580-image immutable test set |
| Model 2 (disease) | `models/model2_retraining_v2/best_model.pth` + `class_mapping.json` | checkpoint head = 144 vs 144 classes: MATCH |
| Model 2 (disease) | `reports/model2_retraining_v2/final_test_evaluation/test_classification_report.csv` | **NOW EXISTS** - per-class P/R/F1/support on the 2,304-image protected test set (deployed checkpoint, production preprocessing) |
| Model 2 (disease) | `models/model2_retraining_v2/crop_disease_mapping.json` | 36 crops, 143 crop-disease pairs |
| Inference code | `models/model2_classifier_v4/predict.py` + `app/backend/services.py` | two-stage pipeline, compatibility filter, masking |

## 2. Model 2 vs Crop-Disease Compatibility Cross-Reference

- Disease classes in deployed `class_mapping.json`: **143** (+1 crop-agnostic `healthy`).
- Crop-disease pairs in deployed `crop_disease_mapping.json`: **143** across **36** crops - full 1:1 coverage both directions.
- Model 2 crops unresolved to a Model 1 crop class: **0** (production aliases `bell_pepper->bellpepper`, `bean->french_bean`, `squash->zucchini`).
- Disease classes that cannot be matched to a supported crop: **none**.

## 3. Model 2 Test Evidence (RESOLVED since original audit)

The original audit found **no test evaluation** for the deployed v2 checkpoint. It now exists: `reports/model2_retraining_v2/final_test_evaluation/` evaluated `models/model2_retraining_v2/best_model.pth` (epoch 14) on all 2,304 protected test images with production preprocessing. Headline test metrics: Top-1 **82.99%**, Top-3 **93.58%**, macro F1 **57.45%**, weighted F1 **83.60%**, disease-only macro F1 **50.34%**, healthy P/R/F1 **99.40/96.25/97.80%** (n=1,041). Validation-vs-test comparison lives in that report (validation is optimistic; test split was never seen during training or model selection).

## 4. Quality Criterion (explicit)

| Gate | Threshold | Evidence source |
|---|---|---|
| Crop (Model 1) | F1 >= **0.85** AND test support >= **20** | `expanded_model1_per_class_metrics.csv` |
| Disease (Model 2) | F1 >= **0.8** AND test support >= **10** | `final_test_evaluation/test_classification_report.csv` (**deployed checkpoint test set**) |
| Compatibility | disease registered under its crop; crop resolvable to Model 1 | deployed mapping files |

**RELIABLE** = crop gate PASS + disease gate PASS + compatibility OK (all three evidenced on held-out test sets).  
**UNVERIFIED** = any gate fails or evidence insufficient (zero/low test support) - never assumed accurate.  
Flags: `LOW_CROP_SUPPORT` (crop n<20), `ZERO_CROP_TEST_SUPPORT`, `DISEASE_LOW_SUPPORT` (disease n<10), `ZERO_DISEASE_TEST_SUPPORT`, `DISEASE_BELOW_THRESHOLD` (n>=10 but F1<0.80), `CROP_GATE_TIGHTENED_SUPPORT_LT_20` (crop gate previously passed on F1 alone with n<20; strict criterion now applied), `HEALTHY_METRICS_GLOBAL_NOT_PER_CROP` (healthy class metrics are global, not per-crop).

## 5. Verification of Previously Proposed Classifications

**Tier 1 (19 proposed crop-disease combos):** recomputed from both evidence files - **19 combos across 11 crops** confirmed.  
- Missing vs proposal: none
- Extra vs proposal: none
- DISCREPANCY: the proposal claimed *13 crops*; the evidence supports **11** (banana, bellpepper, citrus, coffee, corn, cucumber, french_bean, peach, soybean, tomato, wheat). The 19-combination count itself is correct.

**Tier 2 (crop ID + healthy status):** crop-gate passers among Model-2 crops = **18**: banana, bellpepper, blueberry, citrus, coffee, corn, cucumber, french_bean, grape, lettuce, peach, rose, soybean, spinach, strawberry, tomato, wheat, zucchini.  
Model-1-only crops passing the crop gate (no Model-2 rows exist for them): chrysanthemum, geranium, marigold, melon, orchid  
- All 12 named Tier-2 crops verified as crop-gate passers: blueberry, chrysanthemum, geranium, grape, lettuce, marigold, melon, orchid, rose, spinach, strawberry, zucchini. Missing: none.
- DISCREPANCY: the proposal heading said *'23 more crops'*. 23 is the count of **all** crops passing the crop gate (Tier-1 + Tier-2 + Model-1-only); Tier-2-only crops beyond Tier 1 number **7** among Model-2 crops (blueberry, grape, lettuce, rose, spinach, strawberry, zucchini) plus the Model-1-only passers above. Also, for those 5 Model-1-only crops (chrysanthemum, geranium, marigold, melon, orchid) Model 2 has **no disease classes at all** - they are outside Model-2's 36-crop taxonomy, so they have no rows in this audit; only crop-ID reliability (Model 1 evidence) applies to them, and their healthy/diseased status is NOT backed by Model-2 test evidence.

**End-to-end limitations (disease stage passes, crop stage fails):** recomputed over all rows - exactly **3**: apple__rust, cabbage__black_rot, potato__late_blight.  
- Missing vs proposal: none; extra vs proposal: none. Proposal confirmed: apple (crop F1 0.7451), cabbage (0.7308), potato (0.8182) all fail the crop gate while `apple__rust` (deployed-checkpoint test F1 0.8571, n=14), `cabbage__black_rot` (deployed-checkpoint test F1 0.8889, n=13), `potato__late_blight` (deployed-checkpoint test F1 0.9565, n=12) pass the disease gate - correct as stated.

## 6. Summary Counts (finalized)

- Total audited rows: **179** (143 disease classes + 36 per-crop healthy rows)
- Final categories: **RELIABLE: 38**, **UNVERIFIED: 141**
- RELIABLE breakdown: **19 crop-disease combinations** + **19 healthy-status rows**
- UNVERIFIED reasons: crop gate: 20, crop gate + disease gate: 51, disease gate: 70

## 7. RELIABLE Crop-Disease Combinations (both gates PASS on held-out test sets)

| Crop (Model 1) | Disease (Model 2) | Crop F1 / n | Disease test F1 / n |
|---|---|---|---|
| banana | banana__black_leaf_streak | 0.9630 / 54 | 0.9143 / 17 |
| bellpepper | bell_pepper__blossom_end_rot | 0.9688 / 65 | 0.8800 / 11 |
| citrus | citrus__canker | 0.9074 / 52 | 0.8667 / 48 |
| citrus | citrus__greening_disease | 0.9074 / 52 | 0.8000 / 14 |
| coffee | coffee__leaf_rust | 0.8929 / 28 | 0.9032 / 16 |
| corn | corn__gray_leaf_spot | 0.9524 / 62 | 0.8000 / 12 |
| corn | corn__northern_leaf_blight | 0.9524 / 62 | 0.8125 / 14 |
| corn | corn__smut | 0.9524 / 62 | 0.9143 / 19 |
| cucumber | cucumber__angular_leaf_spot | 0.9771 / 65 | 0.9302 / 22 |
| french_bean | bean__angular_leaf_spot | 0.9048 / 65 | 0.9403 / 65 |
| french_bean | bean__rust | 0.9048 / 65 | 0.8571 / 77 |
| peach | peach__brown_rot | 0.8632 / 44 | 0.8387 / 14 |
| peach | peach__leaf_curl | 0.8632 / 44 | 0.9143 / 18 |
| soybean | soybean__downy_mildew | 0.8889 / 65 | 0.9167 / 11 |
| tomato | tomato__early_blight | 0.9922 / 65 | 0.8000 / 22 |
| wheat | wheat__head_scab | 0.8571 / 65 | 0.9677 / 30 |
| wheat | wheat__loose_smut | 0.8571 / 65 | 0.9143 / 19 |
| wheat | wheat__powdery_mildew | 0.8571 / 65 | 0.8400 / 27 |
| wheat | wheat__stem_rust | 0.8571 / 65 | 0.9231 / 13 |

**Healthy-status RELIABLE rows (19):** banana, bean, bell_pepper, blueberry, citrus, coffee, corn, cucumber, grape, lettuce, peach, rose, soybean, spinach, squash, strawberry, tomato, wheat, zucchini (19 Model-2 crops; `squash` and `zucchini` both resolve to Model-1 class `zucchini`). Healthy-class metrics are global - F1 0.978, n=1,041 - not per-crop; flagged accordingly.

## 8. Flagged Items

- **Model 1 crops with LOW test support (<20):** basil, carrot, cauliflower, celery, cherry, eggplant, ginger, maple, raspberry, rice, tobacco
- **Crop gates tightened by strict support rule (F1 ok but n<20):** carrot, tobacco (gate now FAIL where the original audit passed on F1 alone)
- **Disease classes with ZERO test support (28):** bell_pepper__leaf_curl, blueberry__exobasidium, blueberry__septoria_leaf_spot, cauliflower__black_rot, cauliflower__downy_mildew, cauliflower__pest_damage, coffee__black_rot, eggplant__mosaic_virus, eggplant__pest_damage, eggplant__wilt_disease, ginger__leaf_blight, ginger__pest_damage, plum__shot_hole, rose__black_spot, rose__downy_mildew, rose__mosaic_virus, rose__pest_damage, rose__powdery_mildew, rose__rust, spinach__anthracnose, spinach__bacterial_spot, spinach__downy_mildew, spinach__pest_damage, strawberry__angular_leaf_spot, strawberry__gray_mold, strawberry__leaf_spot, strawberry__powdery_mildew, tomato__anthracnose - cannot be verified on the deployed checkpoint; UNVERIFIED (incl. `tomato__anthracnose`, the v2-only class)
- **Disease classes with low test support (1-9, 67):** banana__anthracnose, banana__cigar_end_rot, banana__cordana_leaf_spot, banana__panama_disease, basil__downy_mildew, bean__halo_blight, bean__mosaic_virus, bell_pepper__bacterial_spot, bell_pepper__frogeye_leaf_spot, bell_pepper__powdery_mildew, blueberry__anthracnose, blueberry__botrytis_blight, blueberry__mummy_berry, blueberry__rust, blueberry__scorch, broccoli__alternaria_leaf_spot, broccoli__downy_mildew, broccoli__ring_spot, cabbage__alternaria_leaf_spot, cabbage__downy_mildew, carrot__alternaria_leaf_blight, carrot__cavity_spot, carrot__cercospora_leaf_blight, cauliflower__alternaria_leaf_spot, cauliflower__bacterial_soft_rot, celery__anthracnose, celery__early_blight, cherry__powdery_mildew, coffee__berry_blotch, coffee__brown_eye_spot, eggplant__cercospora_leaf_spot, eggplant__phomopsis_fruit_rot, eggplant__phytophthora_blight, ginger__leaf_spot, ginger__sheath_blight, grape__grapevine_leafroll_disease, lettuce__downy_mildew, lettuce__mosaic_virus, maple__tar_spot, peach__anthracnose, peach__rust, peach__scab, plum__bacterial_spot, plum__brown_rot, plum__pocket_disease, plum__pox_virus, plum__rust, raspberry__fire_blight, raspberry__gray_mold, raspberry__leaf_spot, raspberry__yellow_rust, rice__blast, rice__sheath_blight, soybean__bacterial_blight, soybean__brown_spot, soybean__rust, strawberry__anthracnose, strawberry__leaf_scorch, tobacco__blue_mold, tobacco__brown_spot, tobacco__frogeye_leaf_spot, tobacco__mosaic_virus, tomato__mosaic_virus, tomato__yellow_leaf_curl_virus, zucchini__bacterial_wilt, zucchini__downy_mildew, zucchini__yellow_mosaic_virus
- **Disease classes with adequate support but F1 < 0.80 (79):** apple__black_rot, apple__mosaic_virus, apple__scab, banana__anthracnose, banana__bunchy_top, banana__cigar_end_rot, banana__cordana_leaf_spot, banana__panama_disease, basil__downy_mildew, bean__mosaic_virus, bell_pepper__bacterial_spot, bell_pepper__frogeye_leaf_spot, bell_pepper__powdery_mildew, blueberry__anthracnose, blueberry__botrytis_blight, blueberry__rust, blueberry__scorch, broccoli__alternaria_leaf_spot, broccoli__downy_mildew, broccoli__ring_spot, cabbage__alternaria_leaf_spot, cabbage__downy_mildew, carrot__alternaria_leaf_blight, carrot__cercospora_leaf_blight, cauliflower__alternaria_leaf_spot, cauliflower__bacterial_soft_rot, celery__anthracnose, celery__early_blight, cherry__leaf_spot, cherry__powdery_mildew, coffee__brown_eye_spot, corn__rust, cucumber__bacterial_wilt, cucumber__powdery_mildew, eggplant__cercospora_leaf_spot, eggplant__phytophthora_blight, garlic__leaf_blight, garlic__rust, ginger__leaf_spot, ginger__sheath_blight, grape__black_rot, grape__downy_mildew, grape__leaf_spot, lettuce__downy_mildew, lettuce__mosaic_virus, peach__anthracnose, peach__scab, plum__bacterial_spot, plum__pocket_disease, plum__pox_virus, plum__rust, potato__early_blight, raspberry__fire_blight, raspberry__leaf_spot, rice__blast, rice__sheath_blight, soybean__bacterial_blight, soybean__brown_spot, soybean__frog_eye_leaf_spot, soybean__mosaic, soybean__rust, squash__powdery_mildew, strawberry__anthracnose, tobacco__blue_mold, tobacco__brown_spot, tobacco__frogeye_leaf_spot, tomato__bacterial_leaf_spot, tomato__late_blight, tomato__leaf_mold, tomato__mosaic_virus, tomato__septoria_leaf_spot, tomato__yellow_leaf_curl_virus, wheat__bacterial_leaf_streak_(black_chaff), wheat__leaf_rust, wheat__septoria_blotch, wheat__stripe_rust, zucchini__bacterial_wilt, zucchini__downy_mildew, zucchini__powdery_mildew
- **Disease classes not matched to any supported crop:** none - all 143 registered under their crop prefix.

## 9. Full Combination Table

| Crop (M1) | Disease (M2) | M1 P/R/F1/support | Crop gate | M2-v2 test P/R/F1/support | Disease gate | Compat | Flags | Final |
|---|---|---|---|---|---|---|---|---|
| apple | apple__black_rot | 0.8444/0.6667/0.7451/57 | FAIL | 0.6667/0.4000/0.5000/10 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| apple | apple__mosaic_virus | 0.8444/0.6667/0.7451/57 | FAIL | 0.7500/0.8182/0.7826/11 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| apple | apple__rust | 0.8444/0.6667/0.7451/57 | FAIL | 0.8571/0.8571/0.8571/14 | PASS | COMPATIBLE | - | **UNVERIFIED** |
| apple | apple__scab | 0.8444/0.6667/0.7451/57 | FAIL | 0.6957/0.6400/0.6667/25 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| banana | banana__anthracnose | 0.963/0.963/0.963/54 | PASS | 0.7143/0.7143/0.7143/7 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| banana | banana__black_leaf_streak | 0.963/0.963/0.963/54 | PASS | 0.8889/0.9412/0.9143/17 | PASS | COMPATIBLE | - | **RELIABLE** |
| banana | banana__bunchy_top | 0.963/0.963/0.963/54 | PASS | 0.7500/0.8182/0.7826/11 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| banana | banana__cigar_end_rot | 0.963/0.963/0.963/54 | PASS | 0.6000/0.7500/0.6667/4 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| banana | banana__cordana_leaf_spot | 0.963/0.963/0.963/54 | PASS | 0.7500/0.7500/0.7500/4 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| banana | banana__panama_disease | 0.963/0.963/0.963/54 | PASS | 0.7000/0.8750/0.7778/8 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| basil | basil__downy_mildew | 0.5714/0.6667/0.6154/6 | FAIL | 0.6667/0.6667/0.6667/6 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| french_bean | bean__angular_leaf_spot | 0.9344/0.8769/0.9048/65 | PASS | 0.9130/0.9692/0.9403/65 | PASS | COMPATIBLE | - | **RELIABLE** |
| french_bean | bean__halo_blight | 0.9344/0.8769/0.9048/65 | PASS | 1.0000/0.6667/0.8000/6 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| french_bean | bean__mosaic_virus | 0.9344/0.8769/0.9048/65 | PASS | 0.0000/0.0000/0.0000/5 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| french_bean | bean__rust | 0.9344/0.8769/0.9048/65 | PASS | 0.9000/0.8182/0.8571/77 | PASS | COMPATIBLE | - | **RELIABLE** |
| bellpepper | bell_pepper__bacterial_spot | 0.9841/0.9538/0.9688/65 | PASS | 1.0000/0.4286/0.6000/7 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| bellpepper | bell_pepper__blossom_end_rot | 0.9841/0.9538/0.9688/65 | PASS | 0.7857/1.0000/0.8800/11 | PASS | COMPATIBLE | - | **RELIABLE** |
| bellpepper | bell_pepper__frogeye_leaf_spot | 0.9841/0.9538/0.9688/65 | PASS | 0.2500/0.2500/0.2500/4 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| bellpepper | bell_pepper__leaf_curl | 0.9841/0.9538/0.9688/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| bellpepper | bell_pepper__powdery_mildew | 0.9841/0.9538/0.9688/65 | PASS | 0.3333/1.0000/0.5000/2 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| blueberry | blueberry__anthracnose | 0.931/0.871/0.9/31 | PASS | 0.6000/0.7500/0.6667/4 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| blueberry | blueberry__botrytis_blight | 0.931/0.871/0.9/31 | PASS | 0.6667/0.6667/0.6667/3 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| blueberry | blueberry__exobasidium | 0.931/0.871/0.9/31 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| blueberry | blueberry__mummy_berry | 0.931/0.871/0.9/31 | PASS | 1.0000/0.7500/0.8571/4 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| blueberry | blueberry__rust | 0.931/0.871/0.9/31 | PASS | 0.5000/0.4000/0.4444/5 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| blueberry | blueberry__scorch | 0.931/0.871/0.9/31 | PASS | 0.6667/0.8000/0.7273/5 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| blueberry | blueberry__septoria_leaf_spot | 0.931/0.871/0.9/31 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| broccoli | broccoli__alternaria_leaf_spot | 0.814/0.8537/0.8333/41 | FAIL | 0.4444/0.5000/0.4706/8 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| broccoli | broccoli__downy_mildew | 0.814/0.8537/0.8333/41 | FAIL | 0.2000/0.2500/0.2222/4 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| broccoli | broccoli__ring_spot | 0.814/0.8537/0.8333/41 | FAIL | 0.1667/1.0000/0.2857/1 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| cabbage | cabbage__alternaria_leaf_spot | 0.76/0.7037/0.7308/27 | FAIL | 0.5000/0.1667/0.2500/6 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| cabbage | cabbage__black_rot | 0.76/0.7037/0.7308/27 | FAIL | 0.8571/0.9231/0.8889/13 | PASS | COMPATIBLE | - | **UNVERIFIED** |
| cabbage | cabbage__downy_mildew | 0.76/0.7037/0.7308/27 | FAIL | 0.6250/0.6250/0.6250/8 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| carrot | carrot__alternaria_leaf_blight | 0.75/1.0/0.8571/15 | FAIL | 0.5000/0.8571/0.6316/7 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD;CROP_GATE_TIGHTENED_SUPPORT_LT_20 | **UNVERIFIED** |
| carrot | carrot__cavity_spot | 0.75/1.0/0.8571/15 | FAIL | 1.0000/1.0000/1.0000/7 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;CROP_GATE_TIGHTENED_SUPPORT_LT_20 | **UNVERIFIED** |
| carrot | carrot__cercospora_leaf_blight | 0.75/1.0/0.8571/15 | FAIL | 1.0000/0.3333/0.5000/3 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD;CROP_GATE_TIGHTENED_SUPPORT_LT_20 | **UNVERIFIED** |
| cauliflower | cauliflower__alternaria_leaf_spot | 0.5556/0.5/0.5263/10 | FAIL | 0.0000/0.0000/0.0000/4 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| cauliflower | cauliflower__bacterial_soft_rot | 0.5556/0.5/0.5263/10 | FAIL | 1.0000/0.5000/0.6667/2 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| cauliflower | cauliflower__black_rot | 0.5556/0.5/0.5263/10 | FAIL | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | LOW_CROP_SUPPORT;ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| cauliflower | cauliflower__downy_mildew | 0.5556/0.5/0.5263/10 | FAIL | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | LOW_CROP_SUPPORT;ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| cauliflower | cauliflower__pest_damage | 0.5556/0.5/0.5263/10 | FAIL | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | LOW_CROP_SUPPORT;ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| celery | celery__anthracnose | 0.8/0.6667/0.7273/6 | FAIL | 0.0000/0.0000/0.0000/1 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| celery | celery__early_blight | 0.8/0.6667/0.7273/6 | FAIL | 0.3750/0.6000/0.4615/5 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| cherry | cherry__leaf_spot | 0.4545/0.3571/0.4/14 | FAIL | 0.8000/0.4000/0.5333/10 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| cherry | cherry__powdery_mildew | 0.4545/0.3571/0.4/14 | FAIL | 0.5000/0.3333/0.4000/3 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| citrus | citrus__canker | 0.875/0.9423/0.9074/52 | PASS | 0.9286/0.8125/0.8667/48 | PASS | COMPATIBLE | - | **RELIABLE** |
| citrus | citrus__greening_disease | 0.875/0.9423/0.9074/52 | PASS | 0.9091/0.7143/0.8000/14 | PASS | COMPATIBLE | - | **RELIABLE** |
| coffee | coffee__berry_blotch | 0.8929/0.8929/0.8929/28 | PASS | 1.0000/0.8889/0.9412/9 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| coffee | coffee__black_rot | 0.8929/0.8929/0.8929/28 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| coffee | coffee__brown_eye_spot | 0.8929/0.8929/0.8929/28 | PASS | 0.0000/0.0000/0.0000/1 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| coffee | coffee__leaf_rust | 0.8929/0.8929/0.8929/28 | PASS | 0.9333/0.8750/0.9032/16 | PASS | COMPATIBLE | - | **RELIABLE** |
| corn | corn__gray_leaf_spot | 0.9375/0.9677/0.9524/62 | PASS | 1.0000/0.6667/0.8000/12 | PASS | COMPATIBLE | - | **RELIABLE** |
| corn | corn__northern_leaf_blight | 0.9375/0.9677/0.9524/62 | PASS | 0.7222/0.9286/0.8125/14 | PASS | COMPATIBLE | - | **RELIABLE** |
| corn | corn__rust | 0.9375/0.9677/0.9524/62 | PASS | 0.9091/0.5556/0.6897/18 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| corn | corn__smut | 0.9375/0.9677/0.9524/62 | PASS | 1.0000/0.8421/0.9143/19 | PASS | COMPATIBLE | - | **RELIABLE** |
| cucumber | cucumber__angular_leaf_spot | 0.9697/0.9846/0.9771/65 | PASS | 0.9524/0.9091/0.9302/22 | PASS | COMPATIBLE | - | **RELIABLE** |
| cucumber | cucumber__bacterial_wilt | 0.9697/0.9846/0.9771/65 | PASS | 0.7143/0.7692/0.7407/13 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| cucumber | cucumber__powdery_mildew | 0.9697/0.9846/0.9771/65 | PASS | 0.7857/0.5000/0.6111/22 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| eggplant | eggplant__cercospora_leaf_spot | 0.6316/0.8571/0.7273/14 | FAIL | 0.5714/0.6667/0.6154/6 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| eggplant | eggplant__mosaic_virus | 0.6316/0.8571/0.7273/14 | FAIL | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | LOW_CROP_SUPPORT;ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| eggplant | eggplant__pest_damage | 0.6316/0.8571/0.7273/14 | FAIL | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | LOW_CROP_SUPPORT;ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| eggplant | eggplant__phomopsis_fruit_rot | 0.6316/0.8571/0.7273/14 | FAIL | 1.0000/0.8000/0.8889/5 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| eggplant | eggplant__phytophthora_blight | 0.6316/0.8571/0.7273/14 | FAIL | 0.3333/0.2500/0.2857/4 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| eggplant | eggplant__wilt_disease | 0.6316/0.8571/0.7273/14 | FAIL | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | LOW_CROP_SUPPORT;ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| garlic | garlic__leaf_blight | 0.7143/0.75/0.7317/20 | FAIL | 0.5294/0.7500/0.6207/12 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| garlic | garlic__rust | 0.7143/0.75/0.7317/20 | FAIL | 0.7000/0.5833/0.6364/12 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| ginger | ginger__leaf_blight | 0.8333/0.5556/0.6667/9 | FAIL | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | LOW_CROP_SUPPORT;ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| ginger | ginger__leaf_spot | 0.8333/0.5556/0.6667/9 | FAIL | 0.5714/1.0000/0.7273/4 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| ginger | ginger__pest_damage | 0.8333/0.5556/0.6667/9 | FAIL | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | LOW_CROP_SUPPORT;ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| ginger | ginger__sheath_blight | 0.8333/0.5556/0.6667/9 | FAIL | 0.5000/0.1250/0.2000/8 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| grape | grape__black_rot | 0.8909/0.875/0.8829/56 | PASS | 0.6111/0.8462/0.7097/13 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| grape | grape__downy_mildew | 0.8909/0.875/0.8829/56 | PASS | 0.8000/0.7500/0.7742/32 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| grape | grape__grapevine_leafroll_disease | 0.8909/0.875/0.8829/56 | PASS | 0.8000/0.8000/0.8000/5 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| grape | grape__leaf_spot | 0.8909/0.875/0.8829/56 | PASS | 0.6667/0.4000/0.5000/10 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| lettuce | lettuce__downy_mildew | 0.9831/0.8923/0.9355/65 | PASS | 0.6667/0.5000/0.5714/8 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| lettuce | lettuce__mosaic_virus | 0.9831/0.8923/0.9355/65 | PASS | 0.4286/0.7500/0.5455/4 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| maple | maple__tar_spot | 0.7692/0.9091/0.8333/11 | FAIL | 0.8889/1.0000/0.9412/8 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| peach | peach__anthracnose | 0.8039/0.9318/0.8632/44 | PASS | 0.2500/1.0000/0.4000/1 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| peach | peach__brown_rot | 0.8039/0.9318/0.8632/44 | PASS | 0.7647/0.9286/0.8387/14 | PASS | COMPATIBLE | - | **RELIABLE** |
| peach | peach__leaf_curl | 0.8039/0.9318/0.8632/44 | PASS | 0.9412/0.8889/0.9143/18 | PASS | COMPATIBLE | - | **RELIABLE** |
| peach | peach__rust | 0.8039/0.9318/0.8632/44 | PASS | 1.0000/1.0000/1.0000/1 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| peach | peach__scab | 0.8039/0.9318/0.8632/44 | PASS | 0.6364/0.8750/0.7368/8 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| plum | plum__bacterial_spot | 0.7895/0.6818/0.7317/22 | FAIL | 0.0000/0.0000/0.0000/1 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| plum | plum__brown_rot | 0.7895/0.6818/0.7317/22 | FAIL | 0.7143/1.0000/0.8333/5 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| plum | plum__pocket_disease | 0.7895/0.6818/0.7317/22 | FAIL | 1.0000/0.5000/0.6667/4 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| plum | plum__pox_virus | 0.7895/0.6818/0.7317/22 | FAIL | 0.5000/0.5000/0.5000/4 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| plum | plum__rust | 0.7895/0.6818/0.7317/22 | FAIL | 0.2500/0.5000/0.3333/2 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| plum | plum__shot_hole | 0.7895/0.6818/0.7317/22 | FAIL | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| potato | potato__early_blight | 0.9/0.75/0.8182/24 | FAIL | 0.6667/0.4000/0.5000/10 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| potato | potato__late_blight | 0.9/0.75/0.8182/24 | FAIL | 1.0000/0.9167/0.9565/12 | PASS | COMPATIBLE | - | **UNVERIFIED** |
| raspberry | raspberry__fire_blight | 0.5882/0.8333/0.6897/12 | FAIL | 0.0000/0.0000/0.0000/4 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| raspberry | raspberry__gray_mold | 0.5882/0.8333/0.6897/12 | FAIL | 1.0000/1.0000/1.0000/2 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| raspberry | raspberry__leaf_spot | 0.5882/0.8333/0.6897/12 | FAIL | 0.0000/0.0000/0.0000/1 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| raspberry | raspberry__yellow_rust | 0.5882/0.8333/0.6897/12 | FAIL | 1.0000/1.0000/1.0000/4 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| rice | rice__blast | 0.6667/0.75/0.7059/16 | FAIL | 1.0000/0.5714/0.7273/7 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| rice | rice__sheath_blight | 0.6667/0.75/0.7059/16 | FAIL | 0.5333/1.0000/0.6957/8 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| rose | rose__black_spot | 0.9697/0.9846/0.9771/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| rose | rose__downy_mildew | 0.9697/0.9846/0.9771/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| rose | rose__mosaic_virus | 0.9697/0.9846/0.9771/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| rose | rose__pest_damage | 0.9697/0.9846/0.9771/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| rose | rose__powdery_mildew | 0.9697/0.9846/0.9771/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| rose | rose__rust | 0.9697/0.9846/0.9771/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| soybean | soybean__bacterial_blight | 0.8571/0.9231/0.8889/65 | PASS | 0.7143/0.5556/0.6250/9 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| soybean | soybean__brown_spot | 0.8571/0.9231/0.8889/65 | PASS | 0.8000/0.5714/0.6667/7 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| soybean | soybean__downy_mildew | 0.8571/0.9231/0.8889/65 | PASS | 0.8462/1.0000/0.9167/11 | PASS | COMPATIBLE | - | **RELIABLE** |
| soybean | soybean__frog_eye_leaf_spot | 0.8571/0.9231/0.8889/65 | PASS | 0.6667/0.8571/0.7500/21 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| soybean | soybean__mosaic | 0.8571/0.9231/0.8889/65 | PASS | 0.3125/0.3846/0.3448/13 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| soybean | soybean__rust | 0.8571/0.9231/0.8889/65 | PASS | 0.5000/0.4444/0.4706/9 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| spinach | spinach__anthracnose | 0.9848/1.0/0.9924/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| spinach | spinach__bacterial_spot | 0.9848/1.0/0.9924/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| spinach | spinach__downy_mildew | 0.9848/1.0/0.9924/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| spinach | spinach__pest_damage | 0.9848/1.0/0.9924/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| zucchini | squash__powdery_mildew | 0.8372/0.9231/0.878/39 | PASS | 0.3750/0.4500/0.4091/20 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| strawberry | strawberry__angular_leaf_spot | 1.0/0.9538/0.9764/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| strawberry | strawberry__anthracnose | 1.0/0.9538/0.9764/65 | PASS | 1.0000/0.6000/0.7500/5 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| strawberry | strawberry__gray_mold | 1.0/0.9538/0.9764/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| strawberry | strawberry__leaf_scorch | 1.0/0.9538/0.9764/65 | PASS | 1.0000/1.0000/1.0000/3 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| strawberry | strawberry__leaf_spot | 1.0/0.9538/0.9764/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| strawberry | strawberry__powdery_mildew | 1.0/0.9538/0.9764/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| tobacco | tobacco__blue_mold | 0.8095/0.9444/0.8718/18 | FAIL | 0.4444/0.8000/0.5714/5 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD;CROP_GATE_TIGHTENED_SUPPORT_LT_20 | **UNVERIFIED** |
| tobacco | tobacco__brown_spot | 0.8095/0.9444/0.8718/18 | FAIL | 0.6000/0.8571/0.7059/7 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD;CROP_GATE_TIGHTENED_SUPPORT_LT_20 | **UNVERIFIED** |
| tobacco | tobacco__frogeye_leaf_spot | 0.8095/0.9444/0.8718/18 | FAIL | 0.2000/0.3333/0.2500/3 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD;CROP_GATE_TIGHTENED_SUPPORT_LT_20 | **UNVERIFIED** |
| tobacco | tobacco__mosaic_virus | 0.8095/0.9444/0.8718/18 | FAIL | 0.8000/0.8000/0.8000/5 | FAIL | COMPATIBLE | LOW_CROP_SUPPORT;DISEASE_LOW_SUPPORT;CROP_GATE_TIGHTENED_SUPPORT_LT_20 | **UNVERIFIED** |
| tomato | tomato__bacterial_leaf_spot | 1.0/0.9846/0.9922/65 | PASS | 0.5455/0.4615/0.5000/13 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| tomato | tomato__early_blight | 1.0/0.9846/0.9922/65 | PASS | 0.7143/0.9091/0.8000/22 | PASS | COMPATIBLE | - | **RELIABLE** |
| tomato | tomato__late_blight | 1.0/0.9846/0.9922/65 | PASS | 0.8182/0.5294/0.6429/17 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| tomato | tomato__leaf_mold | 1.0/0.9846/0.9922/65 | PASS | 0.6000/0.7500/0.6667/16 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| tomato | tomato__mosaic_virus | 1.0/0.9846/0.9922/65 | PASS | 0.0000/0.0000/0.0000/7 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| tomato | tomato__septoria_leaf_spot | 1.0/0.9846/0.9922/65 | PASS | 0.4167/0.3571/0.3846/14 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| tomato | tomato__yellow_leaf_curl_virus | 1.0/0.9846/0.9922/65 | PASS | 0.5000/0.6667/0.5714/9 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| wheat | wheat__bacterial_leaf_streak_(black_chaff) | 0.8852/0.8308/0.8571/65 | PASS | 0.4444/0.6154/0.5161/13 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| wheat | wheat__head_scab | 0.8852/0.8308/0.8571/65 | PASS | 0.9375/1.0000/0.9677/30 | PASS | COMPATIBLE | - | **RELIABLE** |
| wheat | wheat__leaf_rust | 0.8852/0.8308/0.8571/65 | PASS | 0.5455/0.5455/0.5455/11 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| wheat | wheat__loose_smut | 0.8852/0.8308/0.8571/65 | PASS | 1.0000/0.8421/0.9143/19 | PASS | COMPATIBLE | - | **RELIABLE** |
| wheat | wheat__powdery_mildew | 0.8852/0.8308/0.8571/65 | PASS | 0.9130/0.7778/0.8400/27 | PASS | COMPATIBLE | - | **RELIABLE** |
| wheat | wheat__septoria_blotch | 0.8852/0.8308/0.8571/65 | PASS | 0.8462/0.5789/0.6875/19 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| wheat | wheat__stem_rust | 0.8852/0.8308/0.8571/65 | PASS | 0.9231/0.9231/0.9231/13 | PASS | COMPATIBLE | - | **RELIABLE** |
| wheat | wheat__stripe_rust | 0.8852/0.8308/0.8571/65 | PASS | 0.6279/0.8438/0.7200/32 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| zucchini | zucchini__bacterial_wilt | 0.8372/0.9231/0.878/39 | PASS | 0.3750/0.3333/0.3529/9 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| zucchini | zucchini__downy_mildew | 0.8372/0.9231/0.878/39 | PASS | 0.3333/0.2000/0.2500/5 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT;DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| zucchini | zucchini__powdery_mildew | 0.8372/0.9231/0.878/39 | PASS | 0.4000/0.4444/0.4211/18 | FAIL | COMPATIBLE | DISEASE_BELOW_THRESHOLD | **UNVERIFIED** |
| zucchini | zucchini__yellow_mosaic_virus | 0.8372/0.9231/0.878/39 | PASS | 0.8889/0.8889/0.8889/9 | FAIL | COMPATIBLE | DISEASE_LOW_SUPPORT | **UNVERIFIED** |
| tomato | tomato__anthracnose | 1.0/0.9846/0.9922/65 | PASS | 0.0000/0.0000/0.0000/0 | NO_TEST_SUPPORT | COMPATIBLE | ZERO_DISEASE_TEST_SUPPORT | **UNVERIFIED** |
| apple | healthy | 0.8444/0.6667/0.7451/57 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| banana | healthy | 0.963/0.963/0.963/54 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| basil | healthy | 0.5714/0.6667/0.6154/6 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| french_bean | healthy | 0.9344/0.8769/0.9048/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| bellpepper | healthy | 0.9841/0.9538/0.9688/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| blueberry | healthy | 0.931/0.871/0.9/31 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| broccoli | healthy | 0.814/0.8537/0.8333/41 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| cabbage | healthy | 0.76/0.7037/0.7308/27 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| carrot | healthy | 0.75/1.0/0.8571/15 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP;CROP_GATE_TIGHTENED_SUPPORT_LT_20 | **UNVERIFIED** |
| cauliflower | healthy | 0.5556/0.5/0.5263/10 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| celery | healthy | 0.8/0.6667/0.7273/6 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| cherry | healthy | 0.4545/0.3571/0.4/14 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| citrus | healthy | 0.875/0.9423/0.9074/52 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| coffee | healthy | 0.8929/0.8929/0.8929/28 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| corn | healthy | 0.9375/0.9677/0.9524/62 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| cucumber | healthy | 0.9697/0.9846/0.9771/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| eggplant | healthy | 0.6316/0.8571/0.7273/14 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| garlic | healthy | 0.7143/0.75/0.7317/20 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| ginger | healthy | 0.8333/0.5556/0.6667/9 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| grape | healthy | 0.8909/0.875/0.8829/56 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| lettuce | healthy | 0.9831/0.8923/0.9355/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| maple | healthy | 0.7692/0.9091/0.8333/11 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| peach | healthy | 0.8039/0.9318/0.8632/44 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| plum | healthy | 0.7895/0.6818/0.7317/22 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| potato | healthy | 0.9/0.75/0.8182/24 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| raspberry | healthy | 0.5882/0.8333/0.6897/12 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| rice | healthy | 0.6667/0.75/0.7059/16 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **UNVERIFIED** |
| rose | healthy | 0.9697/0.9846/0.9771/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| soybean | healthy | 0.8571/0.9231/0.8889/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| spinach | healthy | 0.9848/1.0/0.9924/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| zucchini | healthy | 0.8372/0.9231/0.878/39 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| strawberry | healthy | 1.0/0.9538/0.9764/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| tobacco | healthy | 0.8095/0.9444/0.8718/18 | FAIL | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | LOW_CROP_SUPPORT;HEALTHY_METRICS_GLOBAL_NOT_PER_CROP;CROP_GATE_TIGHTENED_SUPPORT_LT_20 | **UNVERIFIED** |
| tomato | healthy | 1.0/0.9846/0.9922/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| wheat | healthy | 0.8852/0.8308/0.8571/65 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |
| zucchini | healthy | 0.8372/0.9231/0.878/39 | PASS | 0.9940/0.9625/0.9780/1041 | PASS | COMPATIBLE (healthy is crop-agnostic) | HEALTHY_METRICS_GLOBAL_NOT_PER_CROP | **RELIABLE** |

---

## Methodology & Limitations

- Read-only audit: evidence files were read without modification; only this CSV and report were updated. The original evaluation files (`expanded_model1_per_class_metrics.csv`, `final_test_evaluation/*`) are preserved unchanged.
- Disease accuracy comes only from the deployed checkpoint's own 2,304-image test evaluation; it is never inferred from crop accuracy, validation aggregates, or training-image counts.
- Superseded v1-reference columns (`model2_v1_reference_*`) are retained for provenance but no longer influence categories; v1-era flags were removed.
- Note: `reports/crop_disease_reliability_audit/generate_audit.py` still regenerates the ORIGINAL (pre-test-evidence) audit; this finalized state was produced by the one-off finalization pass documented in the finalization session. Re-running the original generator would revert these two files.
- Recommendation (not performed here): fold the finalization logic into `generate_audit.py` so the finalized audit is reproducible from one command.