# JOINT MODEL 1 — DATA GAP AUDIT (Expanded 46-Class Crop Classifier)

**Task:** Joint Model 1 + Model 2 Dataset Gap Audit — Task 1
**Date:** 2026-10-09
**Sources inspected (all read-only):** `data/processed/model1_expanded_manifest.csv` (recalculated row-by-row), `data/processed/model1_expanded_class_mapping.json`, `data/processed/model1_expanded_summary.json`, `reports/model1_expansion/expanded_model1_per_class_metrics.csv`, `reports/model1_expansion/expanded_model1_weak_class_audit.csv`, `reports/model1_expansion/expanded_model1_metric_fix_report.md`, plus a filesystem recount of `data/processed/model1_expanded/`.
**Method:** every count below was recomputed from manifest rows and cross-checked against the filesystem and the stored summary (all three agree exactly). Test metrics are the corrected post-fix values (orig-22 active Macro F1 92.51%, new-24 Macro F1 79.72%).
**Status:** AUDIT ONLY. No dataset, manifest, model, or code file was modified.

---

## 0. Integrity Verification (recalculated)

| Check | Result |
|:---|:---|
| Manifest rows | **15,566** (train 12,407 / val 1,579 / test 1,580) |
| Filesystem recount vs manifest | **0 mismatches** (46 classes × 3 splits) |
| Stored summary vs manifest | **0 mismatches** |
| Missing / extra files on disk | **0 / 0** |
| Cross-split SHA-256 leakage | **0** (train/val/test fully disjoint) |
| Cross-class duplicate SHA | **0** (no image under two crop labels) |
| Rows with `verified_valid` + `unique` status | **all 15,566** |

The dataset is internally consistent and leak-free. All gaps below are genuine data-volume / diversity / domain gaps, not bookkeeping errors.

---

## 1. Canonical 46-Class Table (recalculated counts + corrected test metrics)

Flags: `ZERO` = 0 train; `CRIT` = <20; `LOW` = 20–40; `SUB100` = 41–99; `SUB200` = 100–199; `WEAK` = test F1 < 0.75 with test support ≥ 6; `1SRC` = single source dataset. `u` = unique SHA-256 (== total everywhere: no intra-class duplicates). `T-sup` = immutable test support. P/R/F1 from the corrected evaluation.

| Class | Train | Val | Test | u | Srcs | T-sup | P | R | F1 | Flags |
|:---|---:|---:|---:|---:|:---|---:|---:|---:|---:|:---|
| anthurium | 84 | 10 | 10 | 104 | anthurium | 10 | 1.00 | 1.00 | 1.00 | SUB100, 1SRC |
| apple | 452 | 57 | 57 | 566 | plantseg, plantseg_suppl | 57 | 0.84 | 0.67 | **0.75** | WEAK |
| banana | 428 | 54 | 54 | 536 | plantseg, plantseg_suppl | 54 | 0.96 | 0.96 | 0.96 | — |
| basil | 51 | 6 | 6 | 63 | plantseg, plantseg_suppl | 6 | 0.57 | 0.67 | **0.62** | SUB100, WEAK |
| blueberry | 252 | 31 | 31 | 314 | blueberry_leaves, blueberry | 31 | 0.93 | 0.87 | 0.90 | — |
| broccoli | 332 | 41 | 41 | 414 | broccoli_new | 41 | 0.81 | 0.85 | 0.83 | 1SRC |
| cabbage | 220 | 27 | 27 | 274 | plantseg, plantseg_suppl, ext_cabbage | 27 | 0.76 | 0.70 | **0.73** | WEAK |
| capsicum | 500 | 65 | 65 | 630 | pepper_bell | 65 | 0.98 | 0.95 | 0.97 | 1SRC |
| carnation | 41 | 5 | 5 | 51 | carnation | 5 | 1.00 | 1.00 | 1.00 | LOW, 1SRC |
| carrot | 118 | 15 | 15 | 148 | plantseg, plantseg_suppl | 15 | 0.75 | 1.00 | 0.86 | SUB200 |
| cauliflower | 84 | 10 | 10 | 104 | plantseg, plantseg_suppl, ext_cauli | 10 | 0.56 | 0.50 | **0.53** | SUB100, WEAK |
| celery | 53 | 6 | 6 | 65 | plantseg, plantseg_suppl | 6 | 0.80 | 0.67 | **0.73** | SUB100, WEAK |
| cherry | 111 | 14 | 14 | 139 | plantseg, plantseg_suppl | 14 | 0.45 | 0.36 | **0.40** | SUB200, WEAK |
| cherry_tomato | 0 | 0 | 0 | 0 | — | 0 | 0.00 | 0.00 | 0.00 | **ZERO — alias→tomato; NO acquisition** |
| chrysanthemum | 334 | 42 | 42 | 418 | Herbal_Dataset | 42 | 1.00 | 0.98 | 0.99 | 1SRC |
| citrus | 417 | 52 | 52 | 521 | plantseg, plantseg_suppl | 52 | 0.88 | 0.94 | 0.91 | — |
| coffee | 228 | 28 | 28 | 284 | plantseg, plantseg_suppl | 28 | 0.89 | 0.89 | 0.89 | — |
| corn | 492 | 62 | 62 | 616 | plantseg, plantseg_suppl | 62 | 0.94 | 0.97 | 0.95 | — |
| cucumber | 500 | 65 | 65 | 630 | cucumber, Herbal×5 | 65 | 0.97 | 0.98 | 0.98 | — |
| eggplant | 108 | 14 | 14 | 136 | plantseg, plantseg_suppl | 14 | 0.63 | 0.86 | **0.73** | SUB200, WEAK |
| french_bean | 500 | 65 | 65 | 630 | hf_makerere_beans, plantseg | 65 | 0.93 | 0.88 | 0.90 | alias-pair (↔bean) |
| garlic | 158 | 20 | 20 | 198 | plantseg, plantseg_suppl | 20 | 0.71 | 0.75 | **0.73** | SUB200, WEAK |
| geranium | 201 | 25 | 25 | 251 | medicinal_plants, geranium | 25 | 0.96 | 1.00 | 0.98 | — |
| gerbera | 2 | 0 | 1 | 3 | gerbera_commons | 1 | 0.00 | 0.00 | **0.00** | **CRIT** |
| ginger | 73 | 9 | 9 | 91 | plantseg, plantseg_suppl | 9 | 0.83 | 0.56 | **0.67** | SUB100, WEAK |
| grape | 446 | 56 | 56 | 558 | plantseg, plantseg_suppl | 56 | 0.89 | 0.88 | 0.88 | — |
| gypsophila | 0 | 0 | 0 | 0 | — | 0 | 0.00 | 0.00 | 0.00 | **ZERO — P0 founding set** |
| lettuce | 500 | 65 | 65 | 630 | lettuce-disease | 65 | 0.98 | 0.89 | 0.94 | 1SRC |
| lilium | 37 | 4 | 4 | 45 | oxford_flowers_102 | 4 | 1.00 | 1.00 | 1.00 | LOW, 1SRC |
| maple | 91 | 11 | 11 | 113 | plantseg, plantseg_suppl | 11 | 0.77 | 0.91 | 0.83 | SUB100 |
| marigold | 500 | 65 | 65 | 630 | Marigold_new, Herbal | 65 | 0.97 | 1.00 | 0.98 | — |
| melon | 197 | 25 | 25 | 247 | Herbal, Fruits_Model | 25 | 1.00 | 1.00 | 1.00 | SUB200 |
| orchid | 500 | 65 | 65 | 630 | Orchid_source | 65 | 1.00 | 1.00 | 1.00 | 1SRC |
| peach | 356 | 44 | 44 | 444 | plantseg, plantseg_suppl | 44 | 0.80 | 0.93 | 0.86 | — |
| plum | 171 | 22 | 22 | 215 | plantseg, plantseg_suppl | 22 | 0.79 | 0.68 | **0.73** | SUB200, WEAK |
| potato | 191 | 24 | 24 | 239 | plantseg, plantseg_suppl | 24 | 0.90 | 0.75 | 0.82 | SUB200 |
| raspberry | 99 | 12 | 12 | 123 | plantseg, plantseg_suppl | 12 | 0.59 | 0.83 | **0.69** | SUB100, WEAK |
| rice | 123 | 16 | 16 | 155 | plantseg, plantseg_suppl | 16 | 0.67 | 0.75 | **0.71** | SUB200, WEAK |
| rose | 500 | 65 | 65 | 630 | rose_new, Herbal×19 | 65 | 0.97 | 0.98 | 0.98 | — |
| soybean | 500 | 65 | 65 | 630 | plantseg, anand_soybean_rust_hf, plantseg_suppl | 65 | 0.86 | 0.92 | 0.89 | — |
| spinach | 500 | 65 | 65 | 630 | spinach_disease | 65 | 0.98 | 1.00 | 0.99 | 1SRC |
| strawberry | 500 | 65 | 65 | 630 | strawberry_clean, strawberry_leaves, strawberry | 65 | 1.00 | 0.95 | 0.98 | — |
| tobacco | 142 | 18 | 18 | 178 | plantseg, plantseg_suppl | 18 | 0.81 | 0.94 | 0.87 | SUB200 |
| tomato | 500 | 65 | 65 | 630 | tomato, plantseg, Herbal×6 | 65 | 1.00 | 0.98 | 0.99 | alias-target |
| wheat | 500 | 65 | 65 | 630 | plantseg, plantseg_suppl | 65 | 0.89 | 0.83 | 0.86 | — |
| zucchini | 315 | 39 | 39 | 393 | plantseg, zuchhini | 39 | 0.84 | 0.92 | 0.88 | — |

*(Source abbreviations: plantseg = `model2_v4_plantseg`, plantseg_suppl = `model2_v4_plantseg_v3_supplementary`, ext_cabbage/cauli = `model2_v4_external_healthy_*`.)*

---

## 2. Gap Bands (planning-band summary)

| Band | Classes |
|:---|:---|
| **Zero train (0)** | `cherry_tomato` (ALIAS → tomato — no acquisition), `gypsophila` (P0 founding set) |
| **Critical <20** | `gerbera` (2; P0) |
| **Severe 20–40** | `lilium` (37; P1 despite F1 1.00 — test support only 4) |
| **41–99 (target ≥100)** | `carnation` 41 (P1), `basil` 51 (P1), `celery` 53 (P1), `ginger` 73 (P1), `anthurium` 84 (P1), `cauliflower` 84 (P1), `maple` 91 (P1), `raspberry` 99 (P1) |
| **100–199 (evaluate + diversify)** | `eggplant` 108 (P2, WEAK), `cherry` 111 (P1, WEAK 0.40), `carrot` 118 (P2), `rice` 123 (P2, WEAK), `tobacco` 142 (P2), `garlic` 158 (P2, WEAK), `plum` 171 (P2, WEAK), `potato` 191 (P2), `melon` 197 (P3, F1 1.00) |
| **Weak despite 200+** | `apple` 452 (P2, F1 0.75/R 0.67 — confusions grape→apple, apple→citrus/peach: source-domain issue, not volume), `cabbage` 220 (P2, F1 0.73/R 0.70 — Brassica cross-talk) |
| **Strong / monitor (P3)** | remaining 500-train and ≥0.85-F1 classes |

### Class imbalance and source-domain bias (observed, not assumed)
- **Volume skew:** 13 classes capped at 500 train vs `gerbera` 2, `lilium` 37 — a 250× spread. The imbalance weights in training (exp 0.35) already compensate numerically, but cannot synthesize unseen poses/backgrounds.
- **Source concentration:** 19 of 31 source pools are the two PlantSeg pools (`model2_v4_plantseg` 4,550 + `plantseg_v3_supplementary` 2,181 ≈ 43% of the dataset). Classes drawn *only* from PlantSeg (apple, cherry, cabbage, ginger, rice,…) share one photographic domain (tight single-leaf close-ups, uniform backgrounds) — the documented background bias behind the `cherry` and `basil` error patterns.
- **Single-source classes (1SRC):** anthurium, broccoli, capsicum, carnation, chrysanthemum, lettuce, lilium, orchid, spinach (plus 2-row cases). These are brittle to domain shift; the acquisition plan prioritizes *new independent sources* over sheer volume for them.
- **Val-split fragility:** 6 classes have val < 10 (basil 6, carnation 5, celery 6, gerbera 0, ginger 9, lilium 4). Selection metrics for these classes are noisy; acquired images should first refill val to ≥10 before inflating train.

### Suspected label-quality issues
- **None systemic:** 100% `verified_valid`; zero cross-class SHA collisions; class directories match manifest classes. Residual risk is *botanical* rather than clerical: `cauliflower`↔`broccoli`↔`cabbage` (same species *Brassica oleracea* — foliage genuinely ambiguous), `cherry` fruit-tree vs stone-fruit neighbors, `french_bean`↔`soybean` (already documented confusions). Mitigation = expert-review the *confusion-pair* images specifically, not the whole class.

### Alias rules respected
`cherry_tomato→tomato` (no acquisition, no separate class), `french_bean↔bean`, `capsicum↔bell_pepper`, `squash→zucchini` — no duplicate canonical classes were created in this audit. Model 1's `french_bean` (500), `capsicum` (500), `zucchini` (315) counts already serve their alias partners.

---

## 3. Acquisition Summary (Model 1)

Full per-class targets in `model1_acquisition_candidates.csv` (46 rows: current counts, test P/R/F1, sources, proposed additions, targets, priorities, verification requirements). Priority totals: **P0: 2 classes (+198 real images) · P1: 7 classes (+242) · P2: 9 classes · P3: 27 monitor · ALIAS: 1**. Highest-impact: `gerbera` P0 (+98), `gypsophila` P0 founding set (+100), `cherry` P1 (+39, F1 0.40 on 111 train — worst volume-adjusted performer), `cauliflower` P1 (+16) and `ginger` P1 (+27) with documented confusion patterns.

---

## 4. Safety Attestation

- [x] No training started; no downloads; no images generated.
- [x] `models/model1/`, `models/model1_expanded/`, `data/processed/model1_expanded/` unchanged; locked 1,580-image test set and 178-image benchmark untouched.
- [x] Test images never proposed for training reuse; augmentations never counted as originals.


