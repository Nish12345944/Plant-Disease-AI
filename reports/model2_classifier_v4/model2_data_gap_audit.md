# MODEL 2 V4 — DISEASE DATA GAP AUDIT (116 Disease Classes + Shared Healthy)

**Task:** Joint Model 1 + Model 2 Dataset Gap Audit — Task 2
**Date:** 2026-10-09
**Production status:** `models/model2_classifier_v4/best_model.pth` remains the untouched production model (read-only inspection only).
**Sources inspected (all read-only):** `models/model2_classifier_v4/class_mapping.json` (117 names→ids), `data/processed/model2_organized_crop_disease_mapping.json` (39 crops → 116 disease slugs), `data/processed/model2_v4/model2_v4_manifest.csv` (recalculated: 19,920 rows), `reports/model2_classifier_v4/model2_v4_dataset_audit.csv` (v3/v4 split ledger), `reports/model2_classifier_v4/classification_report.csv` (test P/R/F1, 2,304 test images), `reports/model2_classifier_v4/test_predictions.csv` (confusion pairs), filesystem recount of `data/processed/model2_v4/`, `reports/model2_classifier_v4/model2_v4_training_report.md`.
**Metric availability:** per-class precision/recall/F1 are from the immutable 2,304-image V4 test set; per-class *validation* metrics were never recorded (only aggregate val Macro F1 71.01% @ epoch 18 and field-val 76.51% on 67 images) and are therefore marked **unavailable** throughout. Aggregate-only val numbers cannot localize weaknesses.
**Status:** AUDIT ONLY. No model, dataset, manifest, or code file was modified.

---

## 0. Integrity Verification (recalculated)

| Check | Result |
|:---|:---|
| Manifest rows | **19,920** (train 15,852 / val 1,764 / test 2,304 — matches training report) |
| Manifest class names ↔ `class_mapping.json` ids | **0 inconsistencies** (all 117 classes, ids match) |
| Filesystem recount vs manifest | **0 mismatches** (per crop/disease dir × split) |
| Cross-split SHA-256 leakage | **0** |
| Cross-class duplicate SHA | **0** (every image has exactly one crop–disease label) |
| `label_verified=True` | **all 19,920 rows** |
| v3_test preserved / benchmark contamination | **unchanged from V3 build audit** (0; re-verified by hash — the protected sets live outside this phase's scope and were not re-enumerated) |

The V4 dataset is internally consistent. Gaps below are data-volume / diversity / domain gaps.

---

## 1. Dataset Composition (measured)

- **Healthy shared class:** 5,308 train / 590 val / 1,041 test (F1 0.994). 10 contributing pools, dominated by `model1_balanced_healthy` (3,181) + external healthy pools (tomato 1,420, bell_pepper 708, spinach 694, …). No acquisition needed; **generic healthy images must never be relabeled as diseased**.
- **Source concentration:** 19,253 of 19,920 rows (96.6%) are `v3_curated_base`; 667 (3.3%) are `authentic_field_photography` covering only 4 tomato classes + cucumber/zucchini powdery mildew (zucchini quota unmet: 0/150). All non-field disease classes come from exactly 2 pools (`plantseg` 7,497 + `plantseg_v3_supplementary` 3,499) — a near-total two-source monoculture for 111 classes.
- **Weak-class overlap with weak crops:** V4's weakest classes cluster in crops that are also weak in Model 1 (cauliflower, raspberry, zucchini, tomato septoria/late-blight), confirming shared botanical difficulty rather than coincidence.

---

## 2. Priority Table — P0 + P1 (dual evidence: low support AND weak pattern)

Full 117-row table with counts, sources, confusions, targets and verification rules: `model2_acquisition_candidates.csv`. Priority totals: **P0: 10 · P1: 27 · P2: 31 · P3: 49**.

| Class | Tr/Va/Te | P / R / F1 (sup) | Why prioritized | Target (+add) |
|:---|---:|---:|:---|---:|
| `coffee__black_rot` | 5/1/0 | 0.00/0.00/0.00 (0) | **P0.** 5 train, **zero test support** — unmeasurable and unlearnable. | 100 (+95) |
| `broccoli__ring_spot` | 8/1/1 | 0.00/0.00/0.00 (1) | **P0.** 8 train; single test image fails (Brassica cross-talk both directions). | 100 (+92) |
| `peach__rust` | 6/1/1 | 1.00/1.00/1.00 (1) | **P0.** F1 1.00 on n=1 proves nothing — 6 train cannot generalize; acquire first. | 100 (+94) |
| `peach__anthracnose` | 11/1/1 | 0.33/1.00/0.50 (1) | **P0.** 11 train; only signal is incoming confusion from `apple__black_rot`×2. | 100 (+89) |
| `coffee__brown_eye_spot` | 12/1/1 | 0.50/1.00/0.67 (1) | **P0.** 12 train, n=1 test. | 100 (+88) |
| `carrot__cercospora_leaf_blight` | 13/1/3 | 0.67/0.67/0.67 (3) | **P0.** 13 train, val=1 (selection noise). | 100 (+87) |
| `plum__bacterial_spot` | 13/2/1 | 0.00/0.00/0.00 (1) | **P0.** F1 0.0; fails into `apple__scab`. | 100 (+87) |
| `raspberry__leaf_spot` | 15/2/1 | 0.00/0.00/0.00 (1) | **P0.** F1 0.0; sole test image → `healthy` (lesion missed entirely). | 100 (+85) |
| `tobacco__frogeye_leaf_spot` | 15/2/3 | 0.33/0.33/0.33 (3) | **P0.** Intra-crop confusion (`blue_mold`, `brown_spot` both directions). | 100 (+85) |
| `ginger__leaf_spot` | 19/2/4 | 1.00/1.00/1.00 (4) | **P0.** Perfect on n=4 with 19 train — same non-evidence as peach__rust. | 100 (+81) |
| `bell_pepper__frogeye_leaf_spot` | 22/2/4 | F1 0.40 (4) | **P1.** Scattershot errors (`bean__rust`, `soybean__frog_eye_leaf_spot`, `potato__early_blight`) — no learned boundary. | 100 (+78) |
| `broccoli__downy_mildew` | 23/2/4 | F1 0.40 (4) | **P1.** Errors into *cabbage* (both diseases) — Brassica confound. | 100 (+77) |
| `celery__anthracnose` | 25/3/1 | F1 0.00 (1) | **P1.** n=1 test; harvests incoming confusion from 3 classes — boundary undefined. | 100 (+75) |
| `eggplant__phytophthora_blight` | 26/3/4 | F1 0.57 (4) | **P1.** Two-way confusion with `tomato__late_blight` (same pathogen genus *Phytophthora*). | 100 (+74) |
| `cherry__powdery_mildew` | 27/3/3 | F1 0.33 (3) | **P1.** Also leaks into `healthy` (lesion missed). | 100 (+73) |
| `celery__early_blight` | 28/3/5 | F1 0.50 (5) | **P1.** Cross-family scatter (`rice__sheath_blight`, `carrot__cercospora`, own anthracnose). | 100 (+72) |
| `plum__rust` | 29/3/2 | F1 0.50 (2) | **P1.** Mutual confusion with `bean__rust` (both directions). | 100 (+71) |
| `lettuce__mosaic_virus` | 31/4/4 | F1 0.57 (4) | **P1.** Leaks into `healthy` + `cabbage__downy_mildew`. | 100 (+69) |
| `blueberry__rust` | 34/4/5 | F1 0.57 (5) | **P1.** Confused with `blueberry__anthracnose`×2 + `apple__rust`. | 100 (+66) |
| `zucchini__downy_mildew` | 34/4/5 | F1 0.00 (5) | **P1.** Worst in-band failure: 0/5, 3→`cucumber__angular_leaf_spot`. | 100 (+66) |
| `cauliflower__alternaria_leaf_spot` | 35/4/4 | F1 0.00 (4) | **P1.** 0/4; mutual cross-talk with `cabbage__alternaria_leaf_spot` (2 in, 1 out) + `tomato__septoria_leaf_spot`. | 100 (+65) |
| `bean__mosaic_virus` | 47/5/5 | F1 0.00 (5) | **P1.** 0/5: 4→`soybean__mosaic`; reverse 3 in. Classic bean/soybean virus boundary failure. | 150 (+103) |
| `cabbage__alternaria_leaf_spot` | 47/5/6 | F1 0.18 (6) | **P1.** Worst measured F1 on n≥5; Alternaria-spot signal shared across Brassicas. | 150 (+103) |
| `broccoli__alternaria_leaf_spot` | 49/5/8 | F1 0.57 (8) | **P1.** Alternaria-spot triangle (cabbage/cauliflower/broccoli) + tomato leakage. | 150 (+101) |
| `soybean__brown_spot` | 49/5/7 | F1 0.59 (7) | **P1.** Brown-spot/rust cluster in soybean. | 150 (+101) |
| `tomato__mosaic_virus` | 50/6/7 | F1 0.25 (7) | **P1.** 3→`tomato__yellow_leaf_curl_virus`; systemic-virus confusion. | 150 (+100) |
| `ginger__sheath_blight` | 52/6/8 | F1 0.31 (8) | **P1.** 3→`rice__sheath_blight` (same *Rhizoctonia* syndrome, different host) + `garlic__leaf_blight`×2. | 150 (+98) |
| `zucchini__bacterial_wilt` | 53/6/9 | F1 0.27 (9) | **P1.** 4→`cucumber__bacterial_wilt`; reciprocal 2 in. Cucurbit bacterial-wilt boundary absent. | 150 (+97) |
| `apple__black_rot` | 66/7/10 | F1 0.53 (10) | **P1.** Apple-internal confusion (`scab`×2 out, `scab` in) + `peach__anthracnose`. | 150 (+84) |
| `grape__leaf_spot` | 70/8/10 | F1 0.50 (10) | **P1.** Recall 0.40; scattered out-errors. | 150 (+80) |
| `soybean__bacterial_blight` | 70/8/9 | F1 0.59 (9) | **P1.** Entangled with `bean__rust`, `soybean__rust`, `soybean__brown_spot`. | 150 (+80) |
| `tomato__bacterial_leaf_spot` | 85/9/13 | F1 0.54 (13) | **P1.** 4↔4 mutual confusion with `tomato__septoria_leaf_spot` despite 150 field septoria images nearby. | 150 (+65) |
| `soybean__mosaic` | 92/10/13 | F1 0.50 (13) | **P1.** Mirror of `bean__mosaic_virus` (4 in, 3 out). | 150 (+58) |
| `squash__powdery_mildew` | 139/15/20 | F1 0.41 (20) | **P1.** 8→`zucchini__powdery_mildew`; strongest confusion pair in the test set. Local pool exhausted (420 dups). | 189 (+50) |
| `zucchini__powdery_mildew` | 164/18/18 | F1 0.47 (18) | **P1.** Cucurbit mildew triangle despite 164 train — volume alone did not fix; needs *disambiguating* pairs. | 214 (+50) |
| `tomato__septoria_leaf_spot` | 233/26/14 | F1 0.41 (14) | **P1.** 150 field images added yet F1 still 0.41 — acquisition must be paired with lesion-level verification, not volume. | 283 (+50) |
| `soybean__rust` | 455/51/9 | F1 0.38 (9) | **P1.** 455 train yet 5/9→`bean__rust` — boundary unresolved by volume; needs rust-lesion contrast sets. | 505 (+50) |

### Cross-cutting patterns (evidence, not assumption)
- **Cucurbit powdery-mildew triangle** (squash/zucchini/cucumber): 6 of the top-20 test confusion pairs involve exactly these three classes in both directions. Same-distribution volume will not help; acquisition must be *contrast-curated* (confirmed pathogen, host-labeled pairs).
- **Bean/soybean mirror classes** (`mosaic`, `rust`): bidirectional confusion proves neither side owns a boundary; both sides of each pair must be acquired together.
- **Alternaria-spot triangle** (cabbage/cauliflower/broccoli): same-lesion-type, same-species-family confound; `cabbage__alternaria_leaf_spot` F1 0.18 is the worst reliable score in V4.
- **Same-pathogen-different-host pairs** (`ginger`/`rice__sheath_blight`, tomato/eggplant *Phytophthora*): the network keys on lesion texture and ignores host — host-context images required.
- **Virus classes** (`tomato__mosaic_virus` 0.25, `soybean__mosaic` 0.50, `lettuce__mosaic_virus` 0.57): systemic symptoms confuse across crops; symptomatic-stage diversity needed.
- **Perfect-on-tiny-n is NOT evidence:** `peach__rust` (1.00/n=1), `ginger__leaf_spot` (1.00/n=4), `bell_pepper__powdery_mildew` (1.00/n=2) are P0/P1 on support grounds — small-test F1 was never treated as proof of health.

### Classes explicitly NOT prioritized
- `healthy` (P3): 5,308 train, F1 0.994 — and healthy images must never be relabeled diseased.
- 25 classes at train ≥100 with F1 ≥0.75 (e.g. `wheat__head_scab` 0.984, `bean__angular_leaf_spot` 0.947, `corn__smut` 0.944): monitor only.

### Label-quality concerns
- **No clerical issues:** 100% `label_verified=True`, zero cross-class SHA collisions, manifest↔mapping↔filesystem consistent.
- Botanical risk concentrates in the confusion triangles above (Alternaria spots, powdery mildews, rusts, bacterial wilts, viruses) — every newly acquired image in these groups needs lesion-level (pathogen-confirmed) verification, not just crop-level.
- `turnip` appears in the compatibility map but has **zero V4 classes** (correct: excluded from training taxonomy).

---

## 3. Acquisition Summary (Model 2)

Full 117-row table: `model2_acquisition_candidates.csv` (train/val/test, test P/R/F1/support, unique images, sources, field-image counts, V3 baselines, additions, targets, priorities, confusion evidence, verification rules). Priority totals: **P0: 10 · P1: 27 (+2,939 combined real images) · P2: 31 · P3: 49**. The four confusion-driven volume classes (`soybean__rust`, `tomato__septoria_leaf_spot`, `zucchini__powdery_mildew`, `squash__powdery_mildew`) are the largest line items because their boundaries need contrast sets, not because their current counts are smallest.

---

## 4. Safety Attestation

- [x] No training started; no downloads; no images generated.
- [x] `models/model2_classifier_v4/` (production) and `data/processed/model2_v4/` unchanged; locked 2,304-image V4 test set and 178-image benchmark untouched.
- [x] Test images never proposed for training reuse; augmentations never counted as originals.

