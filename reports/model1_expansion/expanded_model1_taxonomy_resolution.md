# EXPANDED MODEL 1 — ZERO-DATA TAXONOMY RESOLUTION (TASK B)

**Phase:** Expanded Model 1 — Evaluation Correction & EXP-1 Preparation  
**Date:** 2026-10-09  
**Scope:** Inspection of `class_mapping.json`, `config.json`, inference code, and all taxonomy/alias consumers; zero-data class resolution rules; Model 2 V4 routing compatibility.  
**Constraint:** The agreed **46-crop taxonomy is NOT changed**, production Model 1 (`models/model1/`) and Model 2 V4 (`models/model2_classifier_v4/`) remain **locked and untouched**. All resolutions below are *directive* (to be enforced at inference/promotion time), not silent edits.

---

## 1. Executive Summary

| Question | Answer |
|:---|:---|
| Can `cherry_tomato` be presented as a learned independent class? | **NO.** 0 train / 0 val / 0 test images. It is a **dead logit** (index 13 in the expanded head, index 5 in production Model 1). It **must resolve to `tomato`** through the existing alias layer before any output or Model 2 routing. |
| How should `gypsophila` be represented with zero training data? | **Reserved unlearned gap class**: keep its taxonomy slot (index 26), loss weight 0.0 (already), never claim learned capability; at inference a `gypsophila` prediction must be flagged **unsupported (no training data)** and must not be presented as a confident crop. |
| Does the 46-crop taxonomy change? | **NO.** Taxonomy, class indices, and all mapping files are byte-unchanged in this phase. |
| Model 2 V4 routing impact? | Documented in §5 — includes one **pre-existing live defect**: the app layer passes a *prettified* label (`"French Bean"`, `"Cherry Tomato"`) into Model 2, whose alias keys are snake_case, so `french_bean`/`cherry_tomato` disease gating silently fails today. Fix is **directive-only** here because production is locked. |

---

## 2. Consumer Inventory (What Was Inspected)

| # | Artifact / Code Path | Role | Alias / Zero-Data Handling Found | Status |
|:--|:---|:---|:---|:---:|
| 1 | `data/processed/model1_expanded_class_mapping.json` | Expanded 46-class taxonomy source of truth | `class_to_idx` (46), `idx_to_class` (46), `target_classes` (46), `aliases`: `bean→french_bean`, `bell_pepper→capsicum`, `squash→zucchini`, **`cherry_tomato→tomato`** | ✅ Alias present |
| 2 | `models/model1_expanded/class_mapping.json` | Copy exported at training time | Byte-equivalent alias block (`cherry_tomato→tomato`) | ✅ Alias present |
| 3 | `data/processed/class_mapping.json` | Source-folder → canonical normalization (dataset build) | `cherry tomato→cherry_tomato`, `gypsophila→gypsophila` | ✅ (build-time only) |
| 4 | `model1_test_app/inference.py` | **Model 1 inference engine** (`load_model`, `predict_image`) | `load_model()` parses `idx_to_class`/`class_to_idx` but **ignores `aliases`**; `format_class_name()` only prettifies (`cherry_tomato → "Cherry Tomato"`). Returns raw `class_name` + prettified `predicted_label`. | ❌ **Alias not consumed** |
| 5 | `model1_test_app/video_inference.py` | Video-path Model 1 inference | Same: `format_class_name()` only; no alias resolution | ❌ **Alias not consumed** |
| 6 | `app/backend/services.py` | Orchestrates Model 1 → Model 2 | `crop_name = m1_result.get("predicted_label")` (line 213) → **prettified string with spaces** is passed as Model 2 `crop_context` | ⚠️ **Label-format defect (§5.3)** |
| 7 | `models/model2_classifier_v4/predict.py` | Disease & healthy routing | `is_compatible()` alias dict: `french_bean↔bean`, `capsicum→bell_pepper`, **`cherry_tomato→tomato`**; plus `crop_disease_map` lookup (39 crop keys) | ✅ Alias present (snake_case keys only) |
| 8 | `data/processed/model2_organized_crop_disease_mapping.json` | Crop → diseases registry | 39 keys; **contains `tomato`, no `cherry_tomato`, no `gypsophila`** | ✅ Correct by design |
| 9 | `models/model1/config.json` (PRODUCTION, LOCKED) | 22-class production config | `num_classes: 22` — indices 5 `cherry_tomato`, 11 `gypsophila` — **both zero-data dead logits in production too** (never predicted on its test set) | 🔒 Untouched, documented |
| 10 | `scripts/plant_part_rules.py`, `scripts/generate_model1_22_crop_coverage_audit.py` | Data prep / coverage audit | `cherry_tomato → tomato` alias applied for disease-coverage inheritance | ✅ |
| 11 | `reports/model1_expansion/expanded_model1_taxonomy.md` | Approved taxonomy architecture | Defines the canonical `CROP_ALIASES` block including `cherry_tomato→tomato` (directive; not yet wired into the app layer) | 📄 Directive exists |
| 12 | `scripts/train_model1_expanded.py` | Training/eval | Gap classes `cherry_tomato`, `gypsophila` assigned loss weight **0.0**; both indexed in the 46-logit head | ✅ Loss-weighted correctly |

**Inspection conclusion:** the *data layer* correctly defines `cherry_tomato` as an alias, but the *inference layer* never applies it, and the *app layer* re-formats labels in a way that defeats Model 2's alias keys.

---

## 3. Zero-Data Class Findings

### 3.1 `cherry_tomato` (expanded index 13; production index 5)
- **Data:** 0 train / 0 val / 0 test images (confirmed by weak-class audit CSV and dataset reports).
- **Network state:** occupies a full output logit in both the expanded 46-head and the locked production 22-head. With zero training examples its weights receive **zero gradient** — it is a dead node (bias drifts only through weight-decay). On the immutable test set it has **support = 0 and was never predicted** (`predicted_as_count = 0`).
- **Taxonomy rule (agreed, unchanged):** `"cherry_tomato": "tomato"` — foliage of *Solanum lycopersicum* var. *cerasiforme* is visually indistinguishable from standard tomato without fruit in frame; all 7 V4 tomato diseases are cataloged strictly as `tomato__*`.

### 3.2 `gypsophila` (expanded index 26; production index 11)
- **Data:** 0 / 0 / 0 — no verified dataset exists locally or in the acquisition backlog (documented since `model1_balanced_report.md`: "EXTERNAL DATA REQUIRED").
- **Taxonomy rule (agreed, unchanged):** floriculture gap class retained in the 46-crop taxonomy; loss weight 0.0 during training (verified in the run-1 training report).
- **Model 2 relevance:** `gypsophila` is absent from the 39-key crop-disease registry (V4 carries **zero** floriculture diseases by design — floriculture crops are healthy-only).

### 3.3 `gerbera` (index 23) — related but different category
- 3 total images (2 train / 0 val / 1 test): **minimal-data**, not zero-data. Taxonomy status is *learned but under-represented*; remedy is data acquisition, not aliasing. Recorded here to avoid conflating it with the two true gap classes.

---

## 4. Resolution Decisions

### 4.1 `cherry_tomato` → `tomato` (MANDATORY at inference)

**Decision:** `cherry_tomato` is a **RESOLVED ALIAS**, never a learned independent class.

Rules (to be enforced at inference and at any future promotion — **not applied in this phase** because the shared inference module serves locked production):

1. **Logit-level:** index 13 is retained in the head (checkpoint shape and 46-taxonomy stay fixed), with loss weight 0.0 — it can never win a meaningful argmax on real data, and must never be *trained into* a class.
2. **Output-level:** after Top-K decoding, any `cherry_tomato` entry is **collapsed to `tomato`** using the mapping's `aliases` block before results are surfaced:
   ```python
   # Directive (model1_test_app/inference.py, future explicit change):
   aliases = mapping_data.get("aliases", {})
   raw_cls = idx_to_class[int(idx)]
   canonical_cls = aliases.get(raw_cls, raw_cls)   # cherry_tomato -> tomato
   ```
3. **Presentation-level:** UI/API output must never display "Cherry Tomato" as a model prediction. If cultivar context is desired, it may appear only as *metadata* ("cherry tomato variant → tomato").
4. **Routing-level:** Model 2 must always receive the **canonical snake_case crop id** (`tomato`), so all 7 `tomato__*` diseases gate correctly.

**Compatibility:** collapsing is monotone and lossless for evaluation (test support = 0) and for production (the logit has never fired).

### 4.2 `gypsophila` → RESERVED UNLEARNED GAP CLASS

**Decision:** `gypsophila` keeps its taxonomy slot but is represented as **reserved, not learned**:

1. **Taxonomy:** remains member #26 of the agreed 46-crop taxonomy (no removal — removal would shrink every head, renumber indices, and violate the "no silent taxonomy change" constraint).
2. **Training:** loss weight 0.0 (already in place); sampler weight 0 samples because no directory exists; it contributes nothing to any gradient.
3. **Inference:** a raw argmax landing on index 26 (possible only through random drift of an untrained bias) must be treated as **unresolvable**:
   - flag: `status: "unsupported_class"`, message: *"gypsophila is a reserved taxonomy class with no training data — prediction not valid"*;
   - **abstain** — do NOT route to Model 2 as a confident crop, and do NOT report "healthy" for it (see §5.2).
4. **Data path:** populate via dedicated floriculture acquisition (≥100 verified images recommended before the class is activated), or explicitly retire the slot in a *future, versioned* taxonomy revision — both out of scope for this phase.
5. **Reporting:** excluded from "active class" metric denominators (already handled by the corrected active-Macro-F1 in Task A) and explicitly listed as zero-support in all reports.

---

## 5. Downstream Model 2 V4 Routing Compatibility

### 5.1 Empirical `is_compatible()` verification (executed against the V4 registry)

| `crop_context` passed | `disease_slug` | Result | Interpretation |
|:---|:---|:---:|:---|
| `cherry_tomato` | `tomato__early_blight` | ✅ True | V4 alias works **only with raw snake_case input** |
| `cherry tomato` (prettified) | `tomato__early_blight` | ❌ **False** | Alias key mismatch — routing broken if prettified label is passed |
| `french bean` (prettified) | `bean__rust` | ❌ **False** | **Pre-existing live defect** (§5.3) |
| `french_bean` | `bean__rust` | ✅ True | Raw id works |
| `tomato` | `tomato__early_blight` | ✅ True | Canonical single-word crops unaffected |
| `gypsophila` | `healthy` | ✅ True | Healthy bypass always passes (by design) |
| `gypsophila` | any `*__*` disease | ❌ False | No gypsophila diseases exist → all disease candidates filtered |

### 5.2 Compatibility implications of the zero-data classes

- **`cherry_tomato`:** once collapsed to `tomato` at Model 1 output (§4.1), routing inherits all 7 `tomato__*` diseases through direct prefix match — **zero coverage loss**. Until the collapse is implemented, a (theoretically) fired index 13 would arrive as `"Cherry Tomato"` and be gated to *healthy/uncertain only* — an incorrect outcome that the §4.1 directive eliminates.
- **`gypsophila`:** absent from the 39-key registry. Because `is_compatible()` returns `True` for `healthy` unconditionally, Model 2 could label a gypsophila prediction **`healthy`** with high confidence. Under §4.2 this must not happen: the abstain flag at the Model 1 layer prevents gypsophila from ever reaching Model 2. **Do not interpret a gypsophila→healthy result as learned validation of the class.**
- **Floriculture set generally** (`anthurium`, `carnation`, `gerbera`, `geranium`, `lilium`, `orchid`, `chrysanthemum`, `marigold`, `rose`): V4 is healthy-only for these — consistent with the approved taxonomy (§4 of `expanded_model1_taxonomy.md`: floriculture = healthy classification).
- **`melon`:** present in the 46-taxonomy but absent from the 39-key registry — V4 contains no melon-prefixed diseases, so melon inherits healthy-only routing. This matches the approved taxonomy table (no `melon__*` entries), **not** a regression introduced by this phase.

### 5.3 Pre-existing label-format defect (documented, NOT fixed here)

`app/backend/services.py` passes Model 1's **prettified** `predicted_label` (`format_class_name()`: underscores → spaces, `.title()`) as Model 2's `crop_context`. Model 2 lowercases it but never converts spaces back to underscores, so its alias dict (`"french_bean"`, `"cherry_tomato"`) and registry keys never match for multi-word crops:

- `french_bean` → `"French Bean"` → `"french bean"` → **all 4 `bean__*` diseases gated OFF** (healthy bypass still applies).
- `cherry_tomato` → `"Cherry Tomato"` → same failure mode.

Single-word crops (tomato, rice, …) — the overwhelming majority — are unaffected, which is why production validation suites pass. **Directive for the promotion phase** (production stays locked today): pass canonical snake_case ids across the Model 1 → Model 2 boundary and collapse aliases on the Model 1 side:

```python
# Directive — app/backend/services.py (future explicit change)
crop_name = m1_result.get("predicted_class")            # snake_case raw id
crop_name = EXPANDED_ALIASES.get(crop_name, crop_name)  # cherry_tomato -> tomato
```

### 5.4 Expanded-model promotion compatibility (forward-looking)

When (and only when) the expanded Model 1 is separately approved for promotion:

1. Model 2 V4 requires **no changes** — its alias dict + registry already accept the 36 canonical expanded crops that carry diseases; the 10 registry-absent crops are healthy-only by approved design.
2. The inference layer must ship the §4.1 alias collapse + §5.3 snake_case contract **atomically** with the new checkpoint.
3. Class indices 0–45 of `model1_expanded_class_mapping.json` remain frozen — downstream consumers (reporting, confusion matrices, manifests) stay stable.

---

## 6. Change Ledger

| Artifact | Action |
|:---|:---|
| 46-crop taxonomy (`class_mapping.json`, `model1_expanded_class_mapping.json`) | **UNCHANGED** — inspection only |
| `models/model1/`, `models/model2_classifier_v4/` | **UNTOUCHED (locked)** |
| `model1_test_app/inference.py`, `app/backend/services.py`, Model 2 `predict.py` | **UNCHANGED in this phase** — defects/required changes documented as directives only |
| Datasets | **UNCHANGED** |
| This report | **CREATED** |

---

## 7. Safety Attestation

- [x] 46-crop taxonomy unchanged; no mapping file edited.
- [x] Production Model 1 and Model 2 V4 remain locked (SHA-256 verified in prior audit, untouched here).
- [x] No datasets downloaded, created, modified, or deleted.
- [x] No model promoted; EXP-1 remains unexecuted.
- [x] Immutable 1,580-image test set and 178-image external benchmark untouched.




