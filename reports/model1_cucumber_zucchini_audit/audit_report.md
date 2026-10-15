# Model 1 Cucumber vs Zucchini — Phase 1 Audit (read-only)

Date: 2026-10-15. Active checkpoint: `models/model1_expanded/best_model.pth`
(EfficientNet-B2, 46 classes, checkpoint epoch 10). Dataset:
`data/processed/model1_expanded/` + `data/processed/model1_expanded_manifest.csv`.
Method: manifest/folder/mapping inspection, SHA + pHash duplicate scan,
Laplacian-blur/size quality pass, and GPU inference with the deployed mapping
(Resize 224, ImageNet normalize) over the **immutable val+test sets only**
(208 images). **Nothing in the dataset, checkpoint, mappings, or app code was
modified.** Outputs: `audit_summary.json`, `confusion_matrix.csv`,
`misclassified_examples.csv` (+ `misclassified/` image copies),
`quality_metrics.csv`, `near_duplicate_pairs.csv`, this report.

## 1. Counts (unique images, SHA-verified, all present on disk)

| Split | Cucumber (rows / unique SHA / on disk) | Zucchini (rows / unique SHA / on disk) |
|---|---|---|
| train | 500 / 500 / 500 | 315 / 315 / 315 |
| val | 65 / 65 / 65 | 39 / 39 / 39 |
| test | 65 / 65 / 65 | 39 / 39 / 39 |

Exact SHA duplicates: **0 within every cell, 0 cross-split**. Manifest
`duplicate_status` = `unique` and `quality_status` = `verified_clean` for all
1,023 rows; `source_dataset` = `internal_ingested` everywhere (single-source
pipeline — no multi-source domain split to exploit, and no source diversity).

## 2. Class mapping / splits / training setup

- Deployed `class_mapping.json` vs checkpoint-embedded `class_to_idx`: identical
  indices for the audit pair (**cucumber=18, zucchini=45**); the only key-level
  difference in the 46-class dict is a `bellpepper`/`capsicum` alias, which does
  not touch these classes. Inference used the deployed file, so predictions are
  on production indices.
- Split folders are real directories (`train/`, `val/`, `test/`, 46 class
  subfolders each); manifest paths resolve to disk for 100% of rows.
- Training script (`scripts/train_model1_expanded.py`): ImageFolder-style split
  dirs, EfficientNet-B2 ImageNet-pretrained, Resize 224 + flip/rotation/jitter
  (train) / plain resize (eval), class-weighted CrossEntropy + mild smoothed
  WeightedRandomSampler. Imbalance is already compensated — raw counts
  (500 vs 315, ratio 1.6:1) are **not** the headline problem.

## 3. Organ mix — the biggest structural finding

From `original_filename` organ tags:

- **Cucumber: balanced** — train 165 fruit / 168 leaves / 167 stem; val 21/20/24;
  test 24/14/27.
- **Zucchini: leaves ONLY (100%)** — train 315 leaves, val 39 leaves, test 39
  leaves. Zero fruit/stem/flower/whole-plant examples in any split.

The model has never seen a zucchini fruit, stem, or flower. Any production
photo of a zucchini fruit is out-of-distribution by construction.

## 4. Quality / camera-pipeline domain shift

| Group | Median Laplacian-blur | p10 blur | Median size |
|---|---|---|---|
| cucumber train/val/test | 18.0 / 15.9 / 13.6 | ~6-7 | 2296x1724 all splits |
| zucchini train/val/test | 714 / 775 / 544 | 77-282 | 768x600 (val 683x533) |

(Higher blur-var = sharper.) The classes come through visibly different camera
pipelines: cucumber = large soft field photos; zucchini = smaller sharp photos.
A classifier can latch onto pipeline texture instead of botany.

## 5. Duplicates / visual diversity

- Exact duplicates: none (see section 1).
- Perceptual-hash (pHash distance <= 6/64 bits) near-lookalike pairs across the
  1,023 images: **181** — 85 within-split, **63 cross-label**
  (cucumber vs zucchini lookalikes, including test-to-train pairs), 33
  cross-split same-label. The pHash threshold is crude and cucurbit leaves are
  genuinely similar, so these are lookalike flags for human review, not proven
  duplicates — but 63 cross-label pairs (with test-to-train instances) confirm
  low visual diversity at the boundary and a leakage-shaped risk surface.

## 6. Inference on immutable sets — confusion matrices

Published per-class test metrics (unchanged file
`reports/model1_expansion/expanded_model1_per_class_metrics.csv`):
cucumber P 0.9697 / R 0.9846 / F1 **0.9771** (n=65);
zucchini P 0.8372 / R 0.9231 / F1 **0.8780** (n=39).

Fresh GPU rerun, test-only (104 images):

| actual / predicted | cucumber | zucchini | other |
|---|---|---|---|
| cucumber (65) | 64 | 1 | 0 |
| zucchini (39) | 1 | 36 | 2 (grape x2) |

Test accuracy on the pair: **100/104 = 96.2%**; direct swaps **2/104 (1.9%)**.

Combined val+test rerun (`confusion_matrix.csv`, 208 images):

| actual / predicted | cucumber | zucchini | other |
|---|---|---|---|
| cucumber (130) | 126 | 2 | 2 (cabbage, soybean) |
| zucchini (78) | 1 | 72 | 5 (grape x3, lettuce, soybean) |

## 7. Representative misclassified examples (all 10 in `misclassified_examples.csv`)

Test (presentable):
1. `test/cucumber/cucumber_5eea9e9042_cucumber_leaves_healthy_001631.jpg` →
   **zucchini**, conf 0.733 (p_cuc 0.123, margin 0.590). Healthy leaf, soft
   2296x1724 field photo (blur 10.5) — the classic cross-cucurbit leaf swap.
2. `test/zucchini/zucchini_c4ea457923_zucchini_leaves_diseased_013939.jpg` →
   **cucumber**, conf 0.511 vs zucchini 0.483 (**margin 0.028 — a coin flip**).
3. `test/zucchini/zucchini_a07ec8b25d_zucchini_leaves_diseased_013847.jpg` →
   **grape** 0.455 vs zucchini 0.335 (margin 0.119).
4. `test/zucchini/zucchini_ffd5096454_zucchini_leaves_diseased_013951.jpg` →
   **grape** 0.609 (margin 0.510).

Val (same pattern): cucumber to zucchini at conf **0.999**
(`val/cucumber/cucumber_c8f72a3ff6...`, sharp 450x319 web-type image,
p_cuc 0.0006 — a confident pipeline-style error); zucchini to
grape/lettuce/soybean (5 cases); cucumber to cabbage/soybean (2 cases).
Copies with confidences/paths are in `misclassified/`.

## 8. Root-cause verdict

**Primary: visually ambiguous cucurbit leaves + domain shift, not data volume.**
Train volume (500/315) is adequate and imbalance is already handled in
training. The decisive defects: (a) zucchini is leaves-only while cucumber
spans fruit/leaves/stem; (b) the classes ship through different camera
pipelines (2296x1724 soft vs 768x600 sharp); (c) 63 cross-label near-lookalike
pairs show the leaf boundary itself is thin. Direct cucumber-to-zucchini swaps
are rare on test (1.9%) — the larger leak is zucchini diseased leaves escaping
to grape/lettuce/soybean. Secondary: small zucchini test set (n=39) makes every
error cost about 2.6 pts of recall.

## 9. Phase 2 recommendation (no files changed — awaiting approval)

Targeted, verified, **train-only** additions (about 180-230 images total):

- Zucchini **+120-150**: fruit 40-50, stem 25-30, flower/whole-plant 15-20,
  hard leaf lookalikes-vs-cucumber 30-40 (side-by-side same-day/same-camera
  pairs), varied field backgrounds/angles 10+.
- Cucumber **+60-80**: hard leaf lookalikes-vs-zucchini 30-40, diseased stem
  15-20, varied backgrounds/angles 15-20.

## 10. Safe Phase 2 implementation plan (for approval)

1. Ingest candidates into a **quarantine folder outside** `data/processed/`;
   expert-verify each label; record organ/condition/background/camera per image.
2. Dedupe: exact SHA against all 1,023 existing images **plus** pHash review of
   any pair at distance <= 6 before acceptance.
3. Append accepted images to **train/ only** (new files, never move/edit
   val/test); append manifest rows with `source_dataset` + quality/duplicate
   flags following the existing schema.
4. Rebuild/verify manifest counts; rerun this audit script as a regression gate.
5. Train later as a separate approved step with the same recipe; acceptance:
   zucchini test recall >= 0.95 with no cucumber regression, direct swap rate
   below 1%, no new cross-label pHash <= 6 test-to-train pairs.

