# Dataset Recovery Audit — Model 1 + Model 2 (AUDIT ONLY)

Date: 2026-10-15. Nothing was modified: no images added/removed/renamed,
no manifests/mappings/checkpoints/prototypes rewritten, no training,
no commits. New files live only in `reports/dataset_recovery_audit/`.

## 1. Active datasets discovered (from training scripts + configs)

- Model 1 crop classification: `data/processed/model1_expanded/`
  (train/val/test image folders), manifest
  `data/processed/model1_expanded_manifest.csv` (18,176 rows + header),
  mapping `models/model1_expanded/class_mapping.json` (46 classes),
  checkpoint `models/model1_expanded/best_model.pth` (46-way head).
  Source: `scripts/train_model1_expanded.py` DATASET_DIR; config expects
  train 12407 / val 1579 / test 1580.
- Model 2 disease classification: `data/processed/model2_retraining_v2/`
  (nested train/val/test/CROP/DISEASE folders), manifest
  `data/processed/model2_retraining_v2_manifest.csv` (35,441 rows:
  train 30088 / val 3049 / test 2304), mapping
  `models/model2_retraining_v2/class_mapping.json` (144 canonical classes,
  ids 0-143 continuous), checkpoint
  `models/model2_retraining_v2/best_model.pth` (num_classes 144,
  embedded class_mapping matches deployed file on sampled keys).

## 2. Model 1 findings

Disk now: train 15,766 / val 1,592 / test 1,586 (manifest expects
train 14,998 / val 1,592 / test 1,586). Deltas are train-only, in exactly
3 classes: cucumber 784 vs 500 (+284), tomato 800 vs 500 (+300),
zucchini 499 vs 315 (+184). Val and test match the manifest file-for-file
(zero per-class mismatch across all 46). Full table:
`model1_class_counts.csv` (46 rows: class, idx, disk vs manifest per split).
- Train class folders: 45 (missing cherry_tomato). Val/test: 46 folders each,
  but gypsophila/ and cherry_tomato/ are EMPTY shells (0 files) in all
  splits; neither has any manifest row (pre-existing zero-shot classes,
  unchanged by the edit).
- Missing from manifest: 1,201 train files (cucumber 284, tomato 300,
  zucchini 184 by delta; unmanifested filenames are disease-tagged web-style,
  e.g. `0279c6622d_cucumber_angular_leaf_spot_151.jpg`). No val/test file
  is missing from the manifest.
- Leakage (SHA256, full): **38 train files duplicate eval images** —
  cucumber 3 (1 test, 2 val), tomato 2 (val), zucchini 33 (19 test, 14 val).
  Same-hash filenames differ (train web-style vs eval canonical renames),
  so the leak came WITH the added images.
- Duplicates: manifest itself has 212 train-only SHA groups (pre-existing
  bellpepper/capsicum alias renames), NOT cross-split, NOT from this edit.
- Decode: all 18,944 M1 files open under PIL verify (0 failures).
- Label integrity: added filenames carry disease tags inside CROP folders —
  fine for Model 1 only if the crop is truly cucumber/tomato/zucchini; crop
  correctness of the 1,201 is UNVERIFIED. No new unmapped class introduced.

## 3. Model 2 findings

Disk now: train 38,001 files + val 3,049 + test 2,304 = 43,354
(manifest: 30,088 + 3,049 + 2,304 = 35,441). Val/test match manifest
exactly. All +8,545 unmanifested files are train-only. Full table:
`model2_class_counts.csv` (152 rows); hash evidence:
`model2_train_hash.json`; all 477 leaked paths:
`model2_leaked_files.csv`.
- Train folders: 38 crops / 168 disease subdirs. 8 subdirs are
  NON-CANONICAL (not in 144-class mapping, invisible to training):
  cucumber/Anthracnose 523, cucumber/Belly Rot 417,
  cucumber/Gummy_stem_blight 514, cucumber/downy_mildew 461,
  cucumber/pythium_fruit_rot 532, tomato/fruit_fusarium 231,
  banana/healthy banana fruit 106,
  banana/healthy banana leaf in plant - Google Search 194.
- Leakage (SHA256 full pass): **477 train files match eval images**, top:
  tomato__anthracnose 47, cucumber__angular_leaf_spot 44,
  tomato__yellow_leaf_curl_virus 44, eggplant__phytophthora_blight 41,
  broccoli__alternaria_leaf_spot 40, healthy 35, cucumber__powdery_mildew 34.
- Duplicates: 3,249 within-train SHA dups (healthy 481,
  tomato__anthracnose 276, tomato__early_blight 248...). Manifest's own
  564 SHA groups are train-only (545) / val-only (19), never cross-split.
- Decode: 0 failures in 38,001 train files.
- Eval coverage (pre-existing): test covers only 116/144 classes; 28 classes
  have zero test images (list in section 6), val covers 144/144.

## 4. Split integrity verdict

- Acceptable: larger train counts per se; web-style filenames; train-only
  alias duplicates (M1 bellpepper); val-only dups (M2).
- NOT acceptable: 38 (M1) + 477 (M2) exact eval-image copies in train =
  cross-split leakage inflating any future scores; 1,201 + 8,545
  unmanifested files with unverified labels; 8 non-canonical M2 folders
  silently ignored by the loader; M1 train missing cherry_tomato folder
  while val/test shells exist.
- Eval sets remain INTACT: val/test byte-identical to manifests for both
  models. Do NOT move test images anywhere.

## 5. Recovery plan (phased, approval-gated; audit touched nothing)

Phase 0 — freeze: no training on current train folders.
Phase 1 — quarantine (copy, never move): copy the 1,201 M1 added files +
  8,545 M2 added files (manifest-missing lists) to quarantine; restore
  train/ to manifest-exact state by DELETING only quarantined copies from
  train (approval required; val/test untouched).
Phase 2 — verify: re-run SHA audit; expect 0 leakage, disk==manifest.
Phase 3 — curate properly: expert-verify quarantined images, dedupe by SHA
  (+pHash review), append survivors to train ONLY with new manifest rows
  under a NEW dataset version (e.g. model1_expanded_v3,
  model2_retraining_v3); never touch val/test.
Phase 4 — new-class evaluation: cherry_tomato/gypsophila (M1) and the 28
  test-blind M2 classes need a SEPARATE verified eval set; keep old
  immutable test sets for history. Regenerate mappings/prototypes ONLY in
  the approved future training run (M1 prototypes already carry NaN
  placeholders for cherry_tomato/gypsophila — must be rebuilt then;
  M2 mapping unchanged at 144 unless new diseases are added).

## 6. Evidence appendix

- M2 28 classes with zero test images (manifest): bell_pepper__leaf_curl,
  blueberry__exobasidium, blueberry__septoria_leaf_spot,
  cauliflower__black_rot, cauliflower__downy_mildew, cauliflower__pest_damage,
  coffee__black_rot, eggplant__mosaic_virus, eggplant__pest_damage,
  eggplant__wilt_disease, ginger__leaf_blight, ginger__pest_damage,
  plum__shot_hole, rose__black_spot, rose__downy_mildew, rose__mosaic_virus,
  rose__pest_damage, rose__powdery_mildew, rose__rust, spinach__anthracnose,
  spinach__bacterial_spot, spinach__downy_mildew, spinach__pest_damage,
  strawberry__angular_leaf_spot, strawberry__gray_mold, strawberry__leaf_spot,
  strawberry__powdery_mildew, tomato__anthracnose.
- M2 477 leaked paths: `model2_leaked_files.csv` (complete). M1 38 leaked
  files: counts by (trainclass, evalsplit, evalclass) —
  (cucumber,test,cucumber) 1, (cucumber,val,cucumber) 2,
  (tomato,val,tomato) 2, (zucchini,test,zucchini) 19,
  (zucchini,val,zucchini) 14; per-file list to be re-emitted in Phase 2 gate.
- pHash near-duplicate scan: NOT run (38k-image O(n^2) unsuitable for audit
  window); SHA-exact results above are complete. Recommend pHash on
  quarantined additions only, during Phase 3.

## 7. GO / NO-GO for training: NO-GO (both models)

Neither model may train on current train folders: eval leakage (38/477),
9,746 unmanifested unverified images, 8 silently-ignored M2 folders.
GO only after Phase 1+2 gate (leak 0, disk==manifest) — then train on the
restored manifest-exact set; train on curated v3 sets only after Phase 3.

