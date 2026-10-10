# PRIORITIZED ACQUISITION PLAN (Joint Model 1 + Model 2)

**Task:** Joint Gap Audit — Tasks 5+6 (targets + ranking)
**Date:** 2026-10-09
**Inputs:** `model1_acquisition_candidates.csv` (46 rows), `model2_acquisition_candidates.csv` (117 rows), `joint_augmentation_policy.md` (Task 4).
**Units:** all counts are verified REAL images to acquire (augmentations never count). Test/benchmark images are never reused.
**Status:** PLAN ONLY. No downloads, no acquisitions, no modifications until explicitly authorized.

---

## 1. Cross-Model Impact Ranking (highest first, with reasons)

| Rank | Item | Model | Priority | Addition | Why this rank |
|:---:|:---|:---:|:---:|---:|:---|
| 1 | `gerbera` (2 train → 100) | M1 | P0 | +98 | Only original-22 class that is effectively absent (test F1 0.00, val 0). Unblocks the active-macro denominator and the floriculture set. Zero local pool — external sourcing is the critical path. |
| 2 | `gypsophila` founding set (0 → 100) | M1 | P0 | +100 | Reserved taxonomy slot with no data; must exist before the class can ever be activated or evaluated. Long-lead floriculture sourcing — start immediately. |
| 3 | `cabbage__alternaria_leaf_spot` (47 → 150) | M2 | P1 | +103 | Worst reliable F1 in V4 (0.18, n=6). Symptom of the Alternaria-spot triangle; fixing it helps three classes at once. |
| 4 | `bean__mosaic_virus` + `soybean__mosaic` (47/92 → 150) | M2 | P1 | +103/+58 | Bidirectional 0.00/0.50 failure; both sides must be collected as a *paired* contrast set (mirror boundary). |
| 5 | `cherry` (111 → 150) | M1 | P1 | +39 | Worst volume-adjusted performer in M1 (F1 0.40 on 111 train) — background-bias + Rosaceae overlap; needs canopy-context imagery, best return per image in M1. |
| 6 | Cucurbit mildew disambiguation sets (`zucchini__powdery_mildew`, `squash__powdery_mildew` + cucumber counterpart) | M2 | P1 | +50/+50 | Strongest confusion pairs in V4 (8/4 counts); volume already failed (164/139 train); LOCAL POOL EXHAUSTED (420 dups) — external contrast curation only. |
| 7 | `tomato__septoria_leaf_spot` + `tomato__bacterial_leaf_spot` paired set | M2 | P1 | +50/+65 | 4↔4 mutual confusion despite 150 field images; needs lesion-verified pairs, not volume. Core food crop. |
| 8 | `soybean__rust` + `bean__rust` contrast set | M2 | P1 | +50 | 455 train yet 5/9→bean__rust; boundary unresolved by volume. Core food crop. |
| 9 | Brassica joint program: M1 `cauliflower` (+16) + M2 cabbage/cauliflower/broccoli Alternaria trio | M1+M2 | P1 | +16 / +103+65+101 | Same-species-family confound shared by both models; one coordinated Brassica collection serves both. |
| 10 | M1 P1 tail: `basil` (+49), `celery` (+47), `ginger` (+27), `raspberry` (+1), `lilium` (+63) | M1 | P1 | +187 | Small, cheap wins; refill val to ≥10 first (fragile selection metrics). |
| 11 | M2 P0 founding sets (10 classes, +883 total) | M2 | P0 | +883 | Unmeasurable classes (`coffee__black_rot` test support 0; five more at n≤1). Ranked below ranks 3–8 because several affect rare crops, but they gate any claim of 116-class coverage. |
| 12 | M2 P1 volume/weak tail (remaining ~+1,200) | M2 | P1 | ~+1,200 | Per-CSV targets. |
| 13 | P2 programs both models | M1+M2 | P2 | per CSV | `apple`/`cabbage` domain-diversity (M1), wheat/rust and virus classes (M2), 100–199 band top-ups. |
| 14 | P3 monitor | both | P3 | 0 | No acquisition; re-audit after next runs. |

**Why this order:** unblocking zero-coverage classes first (ranks 1–2, 11), then the highest-error-density confusion clusters where evidence shows volume alone fails and *paired contrast* collection is required (ranks 3–9), then cheap small wins (10), then the long tail (12–14).

---

## 2. Proposed Acquisition Order (waves)

- **Wave 0 — sourcing setup (no images yet):** confirm licenses and expert reviewers for floriculture (gerbera, gypsophila), Brassica trials, cucurbit pathology, soybean/bean virus collections, tomato spot collections. Establish the SHA-256 + benchmark + V3-test dedupe gate and the lesion-level QA checklist *before* any file lands.
- **Wave 1 — P0 criticals:** `gerbera` (+98, M1), `gypsophila` founding set (+100, M1), M2 P0 ten-class founding sets (+883). Refill M1 val splits to ≥10 for `basil/carnation/celery/ginger/lilium` from the same intake.
- **Wave 2 — confusion-cluster pairs:** Alternaria-spot trio, bean/soybean mosaic+rust pairs, cucurbit mildew triangle, tomato spot pair. Collect *both sides* of each mirror confusion together; lesion/pathogen confirmation mandatory.
- **Wave 3 — M1 P1 tail + M2 P1 volume:** cherry canopy-context set, cauliflower/ginger/raspberry top-ups, remaining M2 P1 targets.
- **Wave 4 — P2 programs:** M1 `apple`/`cabbage` domain-diversity, M2 wheat/rust and virus classes, 100–199 top-ups.
- **After each wave:** re-run the SHA/leakage audit, rebuild manifests, re-evaluate; stop or reprioritize if a class's error pattern changes (data may reveal a label or augmentation issue instead of a volume issue).

## 3. Per-Wave Verification Gates (mandatory before any image enters train/val)

1. SHA-256 exact-dedupe vs M1 train/val/test, M2 train/val/test, V3 2,304-image test set, and the 178-image benchmark — **zero matches required** (precedent: 1,906 rejections in the V4 field round, including 420 zucchini duplicates).
2. Perceptual near-duplicate screen (pHash) against the same protected sets.
3. Crop label sign-off (M1: expert or 2-reviewer; M2: phytopathologist + lesion-visible QA; confusion-triangle classes need pathogen-level confirmation).
4. License check per source batch.
5. Split assignment recorded in the manifest **before** training; val refills (val<10 classes) allocated first.
6. No healthy→diseased relabeling, ever (M2).

## 4. Totals and Status

- M1 P0+P1: **+440 real images** (P0 +198, P1 +242). M2 P0+P1: **+2,939 real images**.
- Augmentation strategy: online-only policies in `joint_augmentation_policy.md` (Model 1: morphology-preserving; Model 2: lesion-evidence-preserving, strictly milder photometrics + class-conditional exceptions); val/test pipelines frozen.
- **Final status: READY FOR APPROVED DATA ACQUISITION.** All six deliverables exist, counts are measured (not estimated), priorities cite dual evidence, verification gates are defined, and no protected artifact was touched. Nothing will be downloaded, generated, or modified until explicitly authorized. STOP.

