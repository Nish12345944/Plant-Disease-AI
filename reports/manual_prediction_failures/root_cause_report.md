# Manual Prediction Failure — Root Cause Report (READ-ONLY diagnostic phase)

> **Date (UTC):** 2026-10-13
> **Branch inspected:** `test/stability-release` @ `ecfb460`; deployed code pinned at `origin/main` = `6aacbc8`
> **Guardrails honored:** no retraining, no checkpoint/config overwrites, no pushes, no deploys.
> Immutable Model 2 V2 test set (`data/processed/model2_retraining_v2/test/`, 2,304 images) opened read-only.
> Production Model 2 V4 weights (`models/model2_classifier_v4/best_model.pth`, 117-class, epoch 18) opened read-only.
> **Reuses (not repeats):** `reports/model2_classifier_v4/model2_data_gap_audit.md` (2026-10-09),
> `reports/model1_expansion/joint_model1_data_gap_audit.md` (2026-10-09),
> `reports/end_to_end_external_evaluation/` (178-image external eval),
> `reports/model2_retraining_v2/final_test_evaluation/` (immutable V2 benchmark),
> `reports/model2_retraining_v2/{duplicate_audit.csv,class_balance_report.csv}`.

---

## 0. What the deployed Render app actually runs (verified, not assumed)

| Component | Deployed (`origin/main` = `6aacbc8`) | Evidence |
|---|---|---|
| Model 1 checkpoint | `models/model1/best_model.pth` (22-class legacy, 31,383,885 B, **untracked local dev file**, gitignored) | `6aacbc8:app/backend/config.py` defaults; `services.py` passes `MODEL1_CHECKPOINT` |
| Model 1 mapping | `models/model1/class_mapping.json` (22 crops; **no** apple/grape/tobacco/potato/corn/wheat/soybean/rice/squash/bean) | mapping read directly |
| Model 2 checkpoint | `models/model2_classifier_v4/best_model.pth` (117-class head, epoch 18, **untracked local dev file**, gitignored) | ckpt header: `num_classes=117`, `val_macro_f1=0.7101` |
| Model 2 mapping | `models/model2_classifier_v4/class_mapping.json` (117 classes; strictly V4-only) | mapping read directly |
| Crop–disease map | `models/model2_classifier_v4/crop_disease_mapping.json` (39 crops; `healthy` listed only under tomato, cucumber) | mapping read directly |
| Remote weight sync | `MODEL1/2_WEIGHTS_URL` **not** set in `render.yaml`/`Dockerfile` at `6aacbc8` → `ensure_model_checkpoints()` short-circuits to `existing_valid` for any on-disk file | `weights_manager.py` Case 1/Case 2 |
| Thresholds | M1 top-1 gate 0.25; M2 `uncertainty_threshold=0.40`; `margin_threshold=0.05` accepted but unused | `6aacbc8` sources |

**Decisive consequence:** every failure below was reproduced against the exact deployed code path —
legacy 22-class Model 1 + V4 117-class Model 2 on CPU — using 32 held-out
`model2_retraining_v2/test/` images the deployed weights never saw.
Trace table: `reports/manual_prediction_failures/_deployed_pipeline_trace.csv`
(actual label, M1 top-3 + probs, M2 raw top-5 + probs, crop-aware top-5, final prediction, rejection reason).

**It is NOT Model 2 V2.** The V2 retrained checkpoint (144-class, epoch 14, `val_macro_f1=0.6471`,
top-1 82.99% / macro F1 57.45% on the same 2,304 test images) exists only in the local working tree
(`ecfb460`, unpushed) plus untracked `_fast/_recovery/_resume` variants; it is unreachable from Render.

---

## 1. Failure-by-failure root causes (with traced evidence)

Notation: `M1 ▲` = Model 1 error, `M2 ▲` = Model 2 error, `PIPE ▲` = pipeline/threshold artifact.

### 1.1 Grape leafroll — very low confidence / inconclusive — ROOT CAUSE: `M1 ▲` (primary)
- Trace: `255b4047e3…126.jpg` → M1 `blueberry 0.992` (valid) → V4 raw top-1 is the **correct**
  `grape__grapevine_leafroll_disease 0.859`, but the blueberry gate keeps only blueberry mass (0.006)
  → `uncertain` (reported conf = raw 0.859). Second image → M1 `strawberry 0.617` → same fate (raw 0.886).
- Why: legacy 22-class taxonomy has **no `grape`**; blueberry/strawberry foliage absorbs the mass at >0.6.
### 1.3 Tomato early blight / late blight / Septoria misclassification — ROOT CAUSE: `M2 ▲` + `PIPE ▲`
- Trace (clean lab images, M1 `tomato ~1.0`): EB→EB 0.80–0.91 OK; LB→LB 0.996 OK (one image);
  Septoria→`tomato__bacterial_leaf_spot 0.757` WRONG (raw top-1 wrong, not gating);
  second Septoria→Septoria 0.895 OK — genuinely **inconsistent**, as manually reported.
- V2 benchmark: `tomato__septoria_leaf_spot` F1 0.385 (14 test / 233 train — volume NOT the problem;
  confusions `bacterial_leaf_spot`×4 + `early_blight`×3 both directions). V4 report: Septoria F1 0.414
  with +150 field images (+1.4 pts); `tomato__late_blight` F1 0.643, **−21.4 pts vs V3** after +137 field
  images — added data hurt. A label/boundary problem, not volume.
- Hard evidence: `duplicate_audit.csv` shows web-scraped tomato folders with `CROSS_FOLDER_LABEL_CONFLICT`
  (`early_blight` ≡ `late_blight` ≡ `anthracnose` ≡ `fusarium_wilt` identical files, `EXCLUDE_AMBIGUOUS_LABEL`)
  plus intra-folder exact duplicates — the tomato pool contains cross-labeled EB/LB images.
- Needs: **disease classification — label quality / class-boundary work**, not more of the same images.

### 1.4 Potato early / late blight inconsistent — ROOT CAUSE: `M1 ▲` (primary)
- Trace: 4/4 M1-wrong: `tomato 0.757`, `blueberry 0.949`, `tomato 0.654`, `blueberry 0.566`.
  Legacy taxonomy has **no `potato`**; V4 raw top-1 is correct twice
  (`potato__early_blight 0.493`, `potato__late_blight 0.999`) yet both end `uncertain` via wrong-crop gates.
- V2 benchmark: `potato__early_blight` F1 0.50 (10/103; FN → `tomato__early_blight`, `maple__tar_spot`,
  `plum__rust`); `potato__late_blight` F1 0.957. So LB inconsistency is purely the crop gate;
  EB has an additional weak boundary.
- Needs: **crop classification** (both); **disease classification / data** for `potato__early_blight`.

### 1.5 Grape leaf blight (leaf spot) wrong — ROOT CAUSE: `M1 ▲` (primary) + `M2 ▲` (secondary)
- Trace: image 1 → M1 `zucchini 0.975` → V4 raw top-1 `zucchini__downy_mildew 0.980` exceeds 0.40
  → **`diseased/zucchini__downy_mildew 0.9998` — a confident wrong answer, the worst mode in this set.**
  Image 2 → M1 `french_bean 0.913` → raw `grape__leaf_spot 0.996` discarded → `uncertain`.
- V2 benchmark: `grape__leaf_spot` F1 0.50 (10/70; FN → `grape__downy_mildew`×2, `tomato__early_blight`,
  `zucchini__downy_mildew`) — weak boundary atop the missing crop class.
- Needs: **crop classification first**; then **data/boundary work** for `grape__leaf_spot`.

### 1.6 Corn rust confused with wheat rust — ROOT CAUSE: `M1 ▲` (primary) + `M2 ▲` (secondary)
- Trace: image 1 → M1 `orchid 0.813` → `orchid` not in taxonomy → `uncertain` ("not registered").
  Image 2 → M1 `cucumber 0.496 / french_bean 0.472` → raw top-1 `wheat__leaf_rust 0.809` (wrong crop
  entirely) → `uncertain`. Legacy taxonomy has **no `corn`**, no `wheat`.
- V2 benchmark proves the second half is real with the right gate: `corn__rust` F1 0.690 —
### 1.7 Apple black rot + cherry leaf spot inconsistent — ROOT CAUSE: `M1 ▲` (primary) + `M2 ▲` (secondary)
- Trace: apple #1 → M1 `tomato 0.886` → raw `apple__black_rot 0.950` discarded → `uncertain`;
  apple #2 → M1 `blueberry 0.719` → raw top-1 `soybean__frog_eye_leaf_spot 0.483` (wrong) → `uncertain`.
  cherry #1 → M1 `orchid 0.589` → unregistered → `uncertain`; cherry #2 → M1 `french_bean 0.983` →
  raw `cherry__leaf_spot 0.995` discarded → `uncertain`. Legacy taxonomy has **neither `apple` nor `cherry`**.
- V2 benchmark: `apple__black_rot` F1 0.50 (10/66; FN → `peach__anthracnose`×2, `grape__black_rot`×2,
  `apple__scab`); `cherry__leaf_spot` F1 0.533 (10/86; scattered FN). Both `Weak / Critical (data quality)` —
  volume adequate, boundaries are not.
- Needs: **crop classification first**; then **disease classification / label review** for both classes.

### 1.8 Soybean multi-leaf fail + blueberry prediction — ROOT CAUSE: `M1 ▲` (primary) + `M2 ▲` (secondary)
- Trace: `soybean__rust` #1 → M1 `french_bean 0.974` → bean gate → **`diseased/bean__rust 1.00`
  (confident wrong)**; #2 → M1 `rose 0.524` → `uncertain` (raw `bean__rust 0.917`).
  `soybean__mosaic` #1 → `french_bean 0.985` → **`diseased/bean__mosaic_virus 0.998` (confident wrong)**;
  #2 → `french_bean 0.994` → `uncertain` though raw `soybean__mosaic 0.843`.
  Legacy taxonomy has **no `soybean`**; `french_bean` (legume lookalike) hijacks soybean images —
  same as the external eval (`soybean→french_bean 0.69/0.98`, "Out of Taxonomy").
- "Predicts blueberry": exact instance NOT reproduced here, but the mechanism is confirmed — legacy
  `blueberry` is an over-broad attractor (external eval `wheat→blueberry 0.987`; trace potato→blueberry
  0.95/0.57, grape→blueberry 0.99, apple→blueberry 0.72). Marked **mechanism-confirmed,
  instance-unconfirmed** for soybean→blueberry specifically.
- V2 benchmark: `soybean__mosaic` F1 0.345 (↔ `bean__mosaic_virus` 9 cross-errors both directions);
  `soybean__rust` F1 0.471 despite **455 train** (↔ `bean__rust`×4) — volume cannot fix a bean/soybean boundary.
- Needs: **crop classification first** (french_bean/soybean disambiguation), then **disease classification**
  (mosaic + rust boundaries vs bean).

### 1.9 Cucumber vs zucchini crop-identification confusion — ROOT CAUSE: `M1 ▲` + `M2 ▲` (both, P0)
- Trace: `cucumber__powdery_mildew` #1 → M1 `cucumber 0.973` → `diseased 0.9995` OK;
  #2 → M1 `zucchini 0.985` → raw top-1 `squash__powdery_mildew 0.967` → zucchini gate keeps mass 0.003
  → `uncertain`. Zucchini PM images (M1 `zucchini 0.988/0.994`) → correct only after renormalization
  (raw 0.45/0.92 → compat 0.998/0.9999).
- V2 benchmark — a 3-way powdery-mildew collapse: `squash→zucchini` 9, reverse 8;
  `cucumber→squash` 7; `cucumber↔zucchini bacterial_wilt` 3+3; `zucchini__powdery_mildew` F1 0.421
  (18/164 — volume adequate, boundary collapsed); `squash__powdery_mildew` F1 0.409;
  `cucumber__powdery_mildew` F1 0.611.
- Crop side: legacy M1 HAS both crops, yet expanded-M1 test F1 (cucumber 0.977, zucchini 0.878, zucchini
  precision 0.837 — weakest of the pair) says field cucurbits still bleed.
- `squash` aggravator: V4 crop map HAS `squash` (1 disease) but expanded Model 1 has **zero** squash images
  (manifest 0/0/0; `bean` likewise 0) — squash-like cucurbits are forced into cucumber/zucchini gates while
  V4 predicts `squash__powdery_mildew` raw mass that can never be returned.
- Needs: **crop classification AND disease classification jointly** — the only failure needing both at P0.

### Cross-cutting pipeline defects (all failures, `PIPE ▲`)
1. **Display-label leak (`6aacbc8`):** `crop_name = m1_result.get("predicted_label")` — at `6aacbc8`,
   `predicted_label` is the human display string (`"Bell Pepper"`, title-cased crop), passed as `crop_name`
   into `predict_crop_aware`, whose `6aacbc8` normalization is only `.lower().strip()` (no alias map —
   added in `ecfb460`). Any multi-word crop gate (`"Bell Pepper"`, `"French Bean"`, `"Cherry Tomato"`)
   matches **no** taxonomy key → forced `uncertain`/wrong-crop return. (Fixed in unpushed `ecfb460`.)
2. **Over-confident wrong-crop gate:** legacy M1 emits no `unknown` below 0.25, but field images score
   0.49–0.99 on the *wrong* crop (trace max: 0.995 broccoli on tobacco) — the gate launders misclassification
   into high-confidence wrong-crop conditioning instead of protecting.
3. **`healthy` is taxonomically homeless:** listed under only `tomato` and `cucumber` of 39 V4 crops;
## 2. Classification of each issue (data / inference-logic / crop / disease)

| # | Failure | Crop classif. | Disease classif. | Inference logic | Data |
|---|---|---|---|---|---|
| 1.1 | Grape leafroll inconclusive | **yes (primary)** | no | — | no |
| 1.2 | Tobacco unrecognized | **yes (primary)** | secondary (`frogeye` only) | — | yes (`tobacco__frogeye_leaf_spot`, 15 train) |
| 1.3 | Tomato EB/LB/Septoria | no | **yes (boundary/labels)** | secondary (label-leak fix in `ecfb460` helps ties) | **no new volume** — audit/clean pool |
| 1.4 | Potato EB/LB | **yes (primary)** | secondary (EB only) | — | yes (`potato__early_blight` boundary set) |
| 1.5 | Grape leaf spot wrong | **yes (primary)** | secondary | — | yes (boundary set) |
| 1.6 | Corn↔wheat rust | **yes (primary)** | **yes (rust boundary)** | — | yes (paired rust sets) |
| 1.7 | Apple black rot / cherry spot | **yes (primary)** | secondary (label review) | — | review-first, then targeted |
| 1.8 | Soybean / blueberry | **yes (primary)** | **yes (mosaic+rust vs bean)** | secondary (tie-handling) | yes (paired bean/soybean sets) |
| 1.9 | Cucumber↔zucchini (+squash) | **yes (P0)** | **yes (P0)** | secondary | yes (cucurbit PM matrix) |

---

## 3. Priority-ranked fixes

- **P0-1 — Point Render at the expanded Model 1 (config/inference-logic, no retraining).**
  Every out-of-taxonomy failure (grape, tobacco, potato, corn, apple, cherry, soybean + wheat/rice/bean)
  collapses to a crop-gate error that the 46-class checkpoint (already built; manifest 18,176 rows; test F1
  cucumber 0.977 / tomato 0.992 / corn 0.952 / soybean 0.889 / tobacco 0.872) resolves by construction.
  This is the `ecfb460` config change (unpushed) — deployment-gated, not research-gated.
- **P0-2 — Cucurbit powdery-mildew boundary (disease + crop, needs data).**
  3-way `cucumber↔zucchini↔squash` PM collapse (F1 0.61/0.42/0.41) + zero squash crop images + M1
  zucchini precision 0.837. Largest confident-wrong-answer risk in the set.
- **P0-3 — Tomato Septoria / late-blight label audit (data quality, not volume).**
  Septoria F1 0.385 on 233 train with +150 field images ≈ no gain; LB −21.4 pts after +137 field images;
  duplicate audit proves cross-labeled EB≡LB≡anthracnose≡fusarium web images. Clean before adding.
- **P1-1 — Bean/soybean mosaic + rust paired boundary sets (data + disease).**
  `soybean__mosaic` F1 0.345 (↔bean, 9 cross-errors); `soybean__rust` F1 0.471 on 455 train (↔bean×4).
- **P1-2 — Corn/wheat rust paired sets (data + disease).** Bidirectional (corn→stripe×4, leaf→corn×2).
- **P1-3 — Apple black rot / cherry leaf spot label review (data quality first).**
  F1 0.50/0.53 on adequate volume (66/86 train); scattered cross-family FN suggests mislabels.
- **P1-4 — Tobacco frogeye + potato EB + grape leaf-spot boundary sets (data).**
  Train counts 15/103/70; frogeye F1 0.25 (P0-weak).
## 4. Exact dataset gaps and proposed additions (evidence-backed only)

Conventions: counts are `train/val/test` from `data/processed/model2_retraining_v2_manifest.csv`
(35,441 rows). Test/val are **frozen — additions go to train only** (plus held-out experiment-eval images
that never enter any training pool). "Proposed +" = new **train** images from field capture with provenance;
web-scrape only where the duplicate audit can re-verify (the tomato experience forbids blind scrape).

| Gap | Evidence | Current train | Proposed +train | Acceptance |
|---|---|---|---|---|
| Cucurbit PM matrix (cucumber/zucchini/squash PM, paired by severity/lighting) | V2 F1 0.61/0.42/0.41; 9+8+7 cross-errors; M1 zucchini prec. 0.837 | 283/164/139 | +120 / +150 / +100 | cross-PM errors ≤2 per direction on frozen test |
| Squash **crop** images (Model 1) | manifest squash 0/0/0; `bean` 0/0/0 | 0 | +150 squash field multi-leaf images | M1 squash recall ≥0.80 on held-out 30 |
| Tomato Septoria + LB **label audit** (not volume) | F1 0.385/0.643; +150/+137 field imgs ≈ no gain/negative; `CROSS_FOLDER_LABEL_CONFLICT` EB≡LB web images | 233/497 | **0 new until audit**; quarantine conflicted SHA set (~234 conflict rows) | adjudicated relabel; Septoria↔BLS cross-error ≤2 |
| Bean/soybean mosaic pair | F1 0.345; 9 cross-errors both directions | 92 (+bean counter-class) | +120 soybean mosaic + 60 bean mosaic (same-stage pairs) | mosaic cross-error ≤2 |
| Soybean rust vs bean rust | F1 0.471 on 455 train (volume-proof) | 455 | +100 soybean rust (early-stage, low-severity tail) | rust cross-error ≤2 |
| Corn rust vs wheat rusts | corn F1 0.690 (→stripe×4); leaf F1 0.545 (→corn×2) | 143 / 105+264 | +100 corn rust + 80 wheat leaf rust (same-stage pustule pairs) | rust cross-error ≤2 |
| Apple black rot / cherry leaf spot review | F1 0.50/0.53; scattered cross-family FN | 66 / 86 | **review first**; then ≤+80 each only for adjudicated gaps | FN confined within-crop |
| Tobacco frogeye / potato EB / grape leaf-spot | F1 0.25 / 0.50 / 0.50; train 15/103/70 | 15/103/70 | +100 / +80 / +80 field images | F1 ≥0.65 on frozen test |
| Tobacco/potato/corn/apple/cherry/soybean/grape **crop** images (Model 1) | legacy M1 lacks all 7; expanded M1 already covers (tobacco 368, potato 239, cherry 139 rows) | — | **no new acquisition** — deploy expanded M1 (P0-1) | M1 field spot-check ≥0.85 top-1 on 20 new field photos/crop |

Deliberately **not** proposed: healthy top-ups (7,306 train, F1 0.978 — sufficient);
`tomato__anthracnose` (0 test support — outside the reported failures; needs test-set design, forbidden here);
blind web-scrape volume for any tomato class (pool already label-polluted per duplicate audit).

---

## 5. Recommended experiments and evaluation criteria

- **E0 — Config-flip rehearsal (no training):** deploy expanded-M1 + V4 (== `ecfb460`) to
  `plant-disease-ai-docker-test`; run the 32-image trace + frozen 2,304-image V2 test set through it.
  **Pass:** out-of-taxonomy `uncertain` rate → ~0 on the 7 missing crops; no new confident-wrong answers;
  tomato/cucurbit behavior unchanged or better. **Rollback trigger:** any new confident-wrong on the trace set.
- **E1 — Cucurbit PM boundary probe:** freeze V2 weights; train *only* a 3-class linear probe
  (cucumber/zucchini/squash PM) on existing train images; evaluate on frozen test PM images.
  **Pass:** probe accuracy ≥0.75 → boundary learnable with the P0-2 data plan; **fail** → revisit
  preprocessing/crop-gate before acquiring.
- **E2 — Tomato label quarantine:** remove the `CROSS_FOLDER_LABEL_CONFLICT` tomato SHA set from a scratch
  training copy (never the canonical pool), retrain a probe, evaluate Septoria/LB on frozen test.
  **Pass:** Septoria F1 +0.10 with no LB regression → proceed to adjudicated relabeling.
- **E3 — Bean/soybean + corn/wheat paired acquisition pilots:** acquire 30+30 paired images per pair;
  measure cross-error delta on frozen test with a probe before full acquisition.
- **Global gates (all experiments):** frozen V2 test set untouched (2,304 SHA set);
  val/test images never move to train; macro-F1 and per-class F1 reported with supports;
  any `uncertain`-rate change needs a raw-top1 calibration check (0.40 threshold sensitivity).

---

## Appendix A. Artifacts and provenance (read-only)

- `reports/manual_prediction_failures/_deployed_pipeline_trace.csv` — 32-row deployed-code-equivalent
  trace (2 images × 16 failed classes; legacy M1 22-class + V4 117-class, CPU).
- Reused audits: `reports/model2_classifier_v4/model2_data_gap_audit.md`,
  `reports/model1_expansion/joint_model1_data_gap_audit.md`,
  `reports/end_to_end_external_evaluation/{summary.md,model1_external_errors.csv}`,
  `reports/model2_classifier_v4/model2_v4_training_report.md`,
  `reports/model2_retraining_v2/final_test_evaluation/` (`evaluation_summary.json`,
  `per_class_detailed_evaluation.csv`, `top_misclassifications.csv`, `all_misclassification_pairs.csv`,
  `final_test_evaluation_run.log`),
  `reports/model2_retraining_v2/{duplicate_audit.csv (762 rows),class_balance_report.csv}`,
  `data/processed/model2_retraining_v2_manifest.csv` (35,441 rows),
  `data/processed/model1_expanded_manifest.csv` (18,176 rows).
- Scratch helpers used during diagnosis were deleted (`_diag_*.py`); the trace generator is intentionally
  not retained — rerun from the CSV, not from ad-hoc scripts.
- **Unconfirmed items (explicit):** exact Render in-container file state (inferred from `6aacbc8` + Docker
  layer logic — Dashboard/API check still recommended); the specific soybean→blueberry instance
  (mechanism confirmed via attractor evidence, instance not reproduced); field-image generalization beyond
  the 178-image external eval and the 32-image trace (needs E0 on the test service).

- **P2 — Pipeline hardening (inference logic; mostly already in `ecfb460`, unpushed):**
  display-label leak fix, `compat_mass` floor + zero-support guard (shipped), wire up or remove dead
  `margin_threshold` tie-handling, register `healthy` uniformly across all 39 crops, add squash (and bean)
  crop images or remove `squash__powdery_mildew` from the returnable set.

   other crops rely on the "crop registered" shortcut — workable but inconsistent.
4. **`margin_threshold=0.05` accepted but never used** in either version — near-tie cases
   (e.g. soybean mosaic 0.658 vs bean mosaic 0.323) get no tie-handling; dead parameter.

  4/8 misses → `wheat__stripe_rust`, 2 → `wheat__leaf_rust`; `wheat__leaf_rust` F1 0.545 with
  `corn__rust`×2 incoming. Bidirectional rust confusion.
- Needs: **crop classification first**, then **disease classification** (corn-vs-wheat rust boundary).

- V2 benchmark: leafroll test F1 0.80 (5 test / 59 train / 7 val) — the disease classifier is fine.
- Needs: **crop classification**. No disease-data change required (59 train workable).

### 1.2 Tobacco — crop and disease not recognized — ROOT CAUSE: `M1 ▲` (primary)
- Trace: 4/4 tobacco images → M1 `lettuce 0.90`, `broccoli 0.995`, `zucchini 0.988`, `lettuce 0.62`
  (all "valid"). Legacy taxonomy has **no `tobacco`**; leafy-green neighbors win.
- Downstream: correct raw mass discarded (raw `tobacco__brown_spot 0.947` → `uncertain`;
  raw `tobacco__mosaic_virus 1.000` → `uncertain`).
- V2 benchmark: `tobacco__frogeye_leaf_spot` F1 0.25 (15/2/3) is genuinely weak (P0 in V4 gap audit);
  `blue_mold` 0.57, `brown_spot` 0.71, `mosaic_virus` 0.80 on tiny supports.
- Needs: **crop classification first**, then **data** for `tobacco__frogeye_leaf_spot` (15 train unlearnable).
