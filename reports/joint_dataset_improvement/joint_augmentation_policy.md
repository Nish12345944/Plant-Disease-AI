# JOINT AUGMENTATION POLICY (Model 1 + Model 2) — PROPOSAL, NOT APPLIED

**Task:** Joint Gap Audit — Task 4
**Date:** 2026-10-09
**Status:** PROPOSAL ONLY. No augmentation has been applied; no derivative images generated or saved. These policies take effect only inside an approved future training run, as **online (in-memory) transforms during training** — never as persisted derivative files (which would corrupt unique-image counts, SHA dedupe, and leakage controls).

---

## 0. Governing Constraints (both models)

1. **Online only.** Prefer `torchvision.transforms` (or equivalent) applied per-epoch in the DataLoader. Saving augmented copies to disk is prohibited: it inflates "unique image" counts, breaks SHA-256 dedupe, and risks split leakage.
2. **Never augment the test or validation pipelines.** Val/test transforms remain deterministic Resize → ToTensor → Normalize. Validation Macro F1 must stay comparable across runs.
3. **Augmentations never count as originals.** Acquisition targets in the candidate CSVs refer to *verified real* images only.
4. **Identity preservation.** Any transform with evidence of destroying the diagnostic signal for a class is removed for that class (class-conditional policies below).
5. **Reproducibility.** All stochastic transforms seeded (seed 42); parameters versioned in the training config.

---

## 1. Model 1 — Crop Identification (EfficientNet-B2, 46 classes)

**What the network must learn:** crop-identifying morphology — leaf shape/margin, venation, growth habit, flower/fruit structure, canopy context. Augmentations must vary *presentation* without changing *botanical identity*.

| Transform | Parameters | Rationale / Guardrail |
|:---|:---|:---|
| Horizontal flip | p=0.5 | Label-preserving for all 46 crops (leaves are bilaterally variable). |
| Rotation | ±15° (uniform) | Matches run-1 setting; preserves leaf geometry and serration. |
| Affine translate/scale | translate ≤0.08, scale 0.92–1.08 | Conservative; keeps whole-leaf structure in frame. **Excluded for `gerbera`/`lilium`/`carnation`** (flower-head geometry is the signal; scale shifts alter petal-count perception). |
| Brightness / contrast / saturation | ±0.10 each | Mild lighting variation; well below the threshold that alters chlorosis/anthocyanin reading. |
| Hue | ±0.02 | Tight bound: protects nitrogen-deficiency yellowing vs healthy green distinctions. |
| RandomErasing | p=0.15, scale 0.02–0.12, value=random | Forces use of global shape/venation rather than single spot patches. **Excluded for small-leaf herbs (`basil`, `celery`)** where a 12% erase can delete the entire blade. |

**Explicitly prohibited for Model 1:** vertical flip (alters gravitropic habit cues for upright crops: corn, wheat, rice); shear >5° (distorts leaf-margin angles used in Rosaceae/Brassica separation); MixUp/CutMix (synthesizes botanically impossible hybrids); Gaussian blur (destroys serration/venation detail); grayscale (removes chlorophyll signatures); aggressive crop <0.85 (decapitates flower heads and leaf tips).

**Minority-class note:** for classes with <100 train (`gerbera`, `lilium`, `basil`, `celery`, `ginger`, `cauliflower`, `anthurium`, `maple`, `raspberry`, `carnation`), the *sampler* (not augmentation) carries the rebalancing load. Augmentation on <50-image classes must stay at the mild end (flip + rotation + photometric only) — with so few originals, aggressive transforms manufacture background-specific artifacts the model then memorizes.

---

## 2. Model 2 — Disease Classification (EfficientNet-B2, 117 classes)

**What the network must learn:** lesion morphology, symptom color, lesion distribution, leaf texture — the diagnostic evidence itself. Every transform is judged against one question: *would a phytopathologist still confirm the label after this transform?*

| Transform | Parameters | Rationale / Guardrail |
|:---|:---|:---|
| Horizontal flip | p=0.5 | Preserves lesion shape/color/distribution for all 117 classes. |
| Rotation | ±15° (uniform) | Safe for foliar lesions; keeps lesion-to-leaf spatial relations. |
| Affine translate | ≤0.05 | Smaller than Model 1: keeps lesions from being translated out of frame. **No scale <1.0** (downscaling shrinks the very spots being classified). |
| Brightness / contrast | ±0.08 | Tighter than Model 1: protects chlorosis/necrosis intensity reading. |
| Saturation | ±0.08 | Protects rust/pustule color signatures. |
| Hue | **±0.01** | Half the Model 1 bound: yellowing vs mosaic-mottling vs rust-orange distinctions live in hue. |
| RandomErasing | p=0.10, scale 0.02–0.08 | Weaker than Model 1. **Excluded for virus/mosaic classes** (`tomato__mosaic_virus`, `soybean__mosaic`, `bean__mosaic_virus`, `lettuce__mosaic_virus`, `apple__mosaic_virus`) and **low-lesion-count classes** — erasing the only visible symptom converts a diseased image into a `healthy` impostor. |

**Explicitly prohibited for Model 2:** vertical flip on wilt/canker classes where lesion position relative to stem/vein matters; Gaussian/motion blur (destroys sporulation texture, mildew granularity, bacterial-ooze cues); Cutout/CutMix/MixUp (creates/removes lesions, fabricates multi-disease images); grayscale (color IS the diagnosis for rusts, mosaics, chlorosis); strong color jitter (±0.15+, the run-1 Model 1 setting — too aggressive for disease evidence); random crop that can exclude the lesion (lesion-location-aware cropping would be required first — not available, so no cropping beyond the safe affine translate).

---

## 3. Class-Conditional Exceptions (both models)

| Class / Group | Exception | Reason |
|:---|:---|:---|
| Model 1 flower-head classes (`gerbera`, `lilium`, `carnation`, `chrysanthemum`) | No scale/translate beyond 0.05; no erasing | Petal arrangement/count is the signal |
| Model 1 small-leaf herbs (`basil`, `celery`) | No RandomErasing; rotation ±10° | Blade is small relative to frame |
| Model 2 virus/mosaic classes (5 classes) | No RandomErasing; hue ±0.005 | Systemic mottling is diffuse — erasing mimics healthy |
| Model 2 rust classes (`soybean__rust`, `bean__rust`, `wheat__*rust`, `apple__rust`, `plum__rust`, `blueberry__rust`) | Saturation floor: never desaturate (only ±up or neutral) | Pustule orange-brown is the primary cue |
| Model 2 powdery-mildew triangle (squash/zucchini/cucumber) | No blur of any kind; no contrast reduction | White mycelial granularity is low-contrast already |
| Model 2 `healthy` | Same policy as disease (shared loader) but erasing permitted to 0.12 | No lesion to destroy; harder negatives help |

---

## 4. What Changes vs Current Training

- **Model 1 (EXP-1 and later):** keep run-1 base (flip/rotate-15/photometric-0.15/0.03-hue) and *tighten*, not widen: hue 0.03→0.02, add translate/scale + mild RandomErasing with the class exceptions above. Single-variable discipline: augmentation changes must not be bundled with the EXP-1 schedule change.
- **Model 2 (next V-run):** adopt the disease-specific policy above, which is *strictly milder* than Model 1's photometric range. The V4 run's augmentation is not versioned in its config; the next run must log the exact policy block in `config.json`.
- **Validation of the policy itself:** before any production run, a 2-epoch augmentation-sanity probe (train-loss decreases, train/val gap does not explode, weakest-class recall does not collapse) gates policy acceptance.

---

## 5. Safety Attestation

- [x] Proposal only — no transform applied, no image generated, no file written outside this report.
- [x] Online-only rule protects SHA dedupe, split integrity, and unique-image accounting.
- [x] Val/test pipelines explicitly frozen as deterministic.

