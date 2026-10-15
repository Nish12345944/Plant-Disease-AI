# Candidate Dataset Ingestion Manifest — `candidate_v1`

**Status:** PROPOSED ONLY — nothing merged into processed datasets.  
**Created:** 2026-10-14 (while Model 1 E2 training is active)  
**Constraints honored:** read-only w.r.t. existing manifests/mappings/datasets/checkpoints; no images opened, hashed, moved, or deleted; no inference; no training; no commit/push/deploy.  
**Validation depth:** metadata-only. File readability, perceptual duplicate hashing, and pixel-level label re-verification were **deferred** (expensive image processing, would compete with E2).

---

## 0. Confirmed V4 canonical class names (from `models/model2_classifier_v4/class_mapping.json`)
`celery__anthracnose`, `broccoli__ring_spot`, `bell_pepper__frogeye_leaf_spot`, `broccoli__alternaria_leaf_spot`, `broccoli__downy_mildew`, `lettuce__mosaic_virus`, `eggplant__phytophthora_blight`, `eggplant__phomopsis_fruit_rot`.
Eggplant taxonomy = `{cercospora_leaf_spot, phomopsis_fruit_rot, phytophthora_blight}` (no `early_blight`).

---

## 1. Model 1 — `data/external/model1_new_data/Tomato detection/`

Leaf, whole-plant, fruit, and stem are **separate organ groups**. For leaf-based crop recognition, **only the leaf subset is a candidate**. Organ is NOT a class; whole-plant/fruit/stem are proposed `holdout` pending an organ-scoped eval (no production organ head exists yet).

| # | Source path (relative) | Canonical crop | Label | Plant organ | Source | Dup status | Label review | Proposed split | Count |
|--:|---|:--|:--|:--|:--|:--|:--|:--|--:|
| 1 | `model1_new_data/Tomato detection/tomato leaf detection` | `tomato` (idx 43) | crop-only (healthy/diseased n/a) | **leaf** | external NewData | clean (no intra-group hash collision reported) | OK (folder = crop label) | **train:70 / val:15 / test:64** | 149 |
| 2 | `.../tomato whole plant detection` | `tomato` | crop-only | whole_plant | external NewData | clean | OK | **holdout (organ-scope review)** | 459 |
| 3 | `.../tomato fruit detection` | `tomato` | crop-only | fruit | external NewData | clean | OK | **holdout (organ-scope review)** | 331 |
| 4 | `.../tomato stem detection` | `tomato` | crop-only | stem | external NewData | clean | OK | **holdout (organ-scope review)** | 196 |

**Rationale for split:** leaf organ only, organic 80/10/10 (no manual dedupe applied). Never mixing an organ group across splits by construction.

**Open:** true leaf vs non-leaf fraction within `tomato leaf detection` unknown until images are opened (deferred). If leaf purity is high → strongest in-hand candidate for the M1 tomato domain-shift regression.


---

## 2. Model 2 — `data/external/model2_new_data/` (priority classes)

All alias-normalization is **candidate-metadata only**; production mapping untouched.

| # | Source folder(s) | Canonical crop | Disease/healthy | Dup status | Label review | Proposed split | In-hand count | Measurable value |
|--:|---|:--|:--|:--|:--|:--|--:|:--|
| 1 | `celery anthracnose/` (top-level) | `celery` | `anthracnose` | clean | OK | train:68 / val:14 / test:16 | 98 | **Highest** (0.00 on support 1) |
| 2 | `broccoli/ring spot/` | `broccoli` | `ring_spot` | clean | OK | train:143 / val:31 / test:31 | 205 | High (P0, 0.00 on support 1) |
| 3 | `bell_pepper/Frogeye_Leaf_Spot/` | `bell_pepper` | `frogeye_leaf_spot` | clean | OK | train:53 / val:11 / test:12 | 76 | High (0.40, no learned boundary) |
| 4 | `broccoli/alternaria leaf spot/` | `broccoli` | `alternaria_leaf_spot` | clean | OK | train:190 / val:41 / test:41 | 272 | High (Brassica Alternaria triangle) |
| 5 | `broccoli/downy mildew/` | `broccoli` | `downy_mildew` | clean | OK | train:162 / val:35 / test:35 | 232 | Medium |
| 6 | `lettuce/mosaic virus/` | `lettuce` | `mosaic_virus` | clean | OK | train:79 / val:17 / test:17 | 113 | Medium (0.57, leaks to healthy) |
| 7 | `eggplant/phytophthora spot/` **+ `eggplant/Google Search/`** | `eggplant` | `phytophthora_blight` | ⚠️ **DUP + CROSS-CROP CONFLICT** | ⚠️ **QUARANTINE → label review** | **QUARANTINED (no split)** | 234 + 234 | Blocked until resolved |
| 8 | `eggplant/phomopsis/` `phomopsis blight/` `eggplant_phomopsis/` | `eggplant` | `phomopsis_fruit_rot` (alias-normalized) | ⚠️ **DUP ACROSS 3 FOLDERS** | ⚠️ **dedupe required** | **QUARANTINED → dedupe first** | 19 + 35 + 88 = 142 | Blocked until deduped |

**Priority ranking basis:** celery__anthracnose and broccoli__ring_spot are both at 0.00 on support 1 → largest measurable lift. bell_pepper__frogeye and broccoli__alternaria are weak with clear incoming support. Downy mildew / lettuce mosaic are solid secondary adds.


---

## 3. Quarantine & out-of-taxonomy flags (do NOT auto-ingest)

### 3a. Quarantine — mislabeled eggplant folder (cross-crop tomato content)
`eggplant/phytophthora spot/` **shares identical SHA256 images with `tomato/Late blight of tomato fruit/` and `tomato/tomato fruit Anthracnose/`** (from the existing `duplicate_audit.csv`). This is a cross-crop label conflict — tomato-fruit content filed under eggplant.
- **Disposition:** QUARANTINE → manual label review. Do not assign to `eggplant__phytophthora_blight` until confirmed.
- **Also:** the two phytophthora folders are **234/234 filename-identical** → intra-class duplicate set; dedupe before any split.

### 3b. Quarantine — eggplant phomopsis triple folder
`eggplant/phomopsis/` + `phomopsis blight/` + `eggplant_phomopsis/` overlap (phomopsis_blight shares images with eggplant_phomopsis per audit).
- **Disposition:** QUARANTINE → dedupe; normalize `phomopsis_blight`→`phomopsis_fruit_rot` in candidate metadata only.

### 3c. Out-of-taxonomy (needs taxonomy decision, NOT candidate_v1)
| Source folder | Count | Issue |
|---|--:|---|
| `tomato/tomato fruit Anthracnose/` | 336 | No `tomato__anthracnose` in V4 117-class taxonomy |
| `tomato/tomato fruit fusarium wilt/` | 231 | No `tomato__fusarium_wilt` in V4 taxonomy |
| `eggplant/early blight of tomato fruit/` | 358 | Mislabeled (tomato-fruit content) **and** out-of-taxonomy |

---

## 4. Split & leakage policy

---

## 5. Candidate counts

| Bucket | Images |
|---|--:|
| **M1 leaf candidate (safe to stage)** | 149 |
| M1 whole-plant (holdout) | 459 |
| M1 fruit (holdout) | 331 |
| M1 stem (holdout) | 196 |
| **M2 clean-priority candidates (5 classes)** | 98 + 205 + 76 + 272 + 232 + 113 = **996** |
| M2 quarantined (eggplant phyto + phomopsis) | 610 |
| M2 out-of-taxonomy (flag only) | 336 + 231 + 358 = 925 |

**Total cleanly candidate-able now:** M1 leaf 149 + M2 clean-priority 996 = **1,145 images** across 6 classes.

---

## 6. Unresolved labels / open items
1. **Eggplant phytophthora** — cross-crop tomato conflict + 234/234 intra-folder dup → quarantine.
2. **Eggplant phomopsis** — 3-folder overlap → dedupe.
3. **`eggplant/early blight of tomato fruit`** — mislabeled + out-of-taxonomy.
4. **tomato fruit Anthracnose / fusarium wilt** — out-of-taxonomy; taxonomy extension decision required.
5. **M1 leaf purity** — actual leaf fraction unverified (deferred image check).
6. **File readability** — not checked (deferred).

---

## 7. Exact next ingestion step (post-E2)
When E2 training completes, run a single lightweight curation pass (no model use):
1. **Dedupe by SHA256** (reuse existing `duplicate_audit.csv` hashes; no re-hash needed) across the M2 `model2_new_data` tree → assign `keep`/`dup`/`cross_crop_conflict` per the audit's disposition column.
2. **Verify readability + leaf fraction** of the 149 M1 leaf images (PIL open, count leaf vs non-leaf).
3. **Stage the 6 clean classes** (M1 tomato-leaf + 5 M2 priority) into a new `candidate_v1/` tree using the organic 70/15/10 splits above; write `candidate_v1/manifest.csv` with the columns in this report.
4. Keep quarantined (610) and out-of-taxonomy (925) groups out of `candidate_v1` pending their resolutions.
5. Only after (1)–(4) sign-off: schedule a Model 1 head fine-tune / Model 2 fine-tune against the frozen held-out sets.

- **Organic split only** (70/15/10 per source group); no manual dedupe applied at this stage.
- **Never mix** the same source or a near-duplicate group across train/val/test — enforced per-group, and by keeping every dup-conflicted / quarantined group **out of all splits** until resolved.
- Candidate data lives under a **separate version (`candidate_v1`)** and is **not merged** into `data/processed/*` yet.
