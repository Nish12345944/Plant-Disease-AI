# EXPANDED MODEL 1 — EXP-1 PREFLIGHT REPORT (TASK C)

**Phase:** Expanded Model 1 — Evaluation Correction & EXP-1 Preparation  
**Date:** 2026-10-09  
**Experiment:** EXP-1 — Two-Stage Transfer Learning (EfficientNet-B2, 46 classes)  
**Prepared Script:** `scripts/train_model1_expanded_exp1.py`  
**Execution Status:** **PREPARED — NOT EXECUTED** (no training, no download, no data change)  
**Readiness Verdict:** ✅ **READY TO RUN** — all preflight checks pass; awaiting the explicit `--run` command from the operator.

---

## 1. Experiment Design

| | Stage 1 — Head Warmup | Stage 2 — Full Fine-Tune |
|:---|:---|:---|
| **Trainable parameters** | Classifier head only (`classifier.*`, 2 tensors, ~42.4 K params) | All parameters (~9.2 M) |
| **Backbone** | FROZEN (incl. `conv_head`; BN held in eval — ImageNet stats preserved) | Unfrozen, BN in train mode |
| **Epochs** | 4 (fixed, no early stop) | Up to 10 (early-stop patience 4) |
| **Optimizer** | AdamW(head params, lr=**1e-3**, wd=1e-4) | AdamW(all params, lr=**7e-5**, wd=1e-4) |
| **Scheduler** | Constant LR | CosineAnnealingLR(T_max=10, eta_min=**1e-6**) |
| **Objective** | Adapt the random 46-class head without noisy gradients into pretrained convolutions | Restore/extend feature utility with minimal forgetting |
| **Global epoch index** | 1–4 | 5–14 |
| **Checkpoint selection** | Best-by validation across **both** stages (primary: val Macro F1 active; secondary: val accuracy) | same |

### Held-constant controls (single-variable isolation vs Run 1 / EXP-0)
Seed **42** · batch **16** (4 GB RTX 3050 safe) · AMP FP16 (`autocast` + `GradScaler`, identical API) · ImageNet normalization `[0.485,0.456,0.406]/[0.229,0.224,0.225]` · Run-1 augmentations (HFlip 0.5, Rotate 15, ColorJitter 0.15/0.15/0.15/0.03) · `WeightedRandomSampler` (exp 0.20, clamped) + class-weighted `CrossEntropyLoss` (exp 0.35, clamped, **0.0 for gap classes**) · `num_workers=2`, `pin_memory`, `persistent_workers` · cudnn deterministic · checkpoint metadata schema.

**The single changed factor is the optimization schedule** (freeze policy + staged LRs + cosine decay), exactly as specified in the tuning experiment plan §3.1.

### Corrective refinements over the plan's pseudocode
1. **Freeze scope:** the plan's `for param in model.features.parameters()` leaves `model.conv_head` (part of the pretrained feature extractor) trainable. The prepared script freezes *everything except `classifier.*`* — the correct form of "train only `model.classifier`".
2. **BatchNorm policy:** during Stage 1 the backbone BN layers are forced to eval mode after `model.train()`, so ImageNet running statistics/affine weights cannot drift from head-only updates (otherwise the "frozen" backbone is not actually frozen).
3. **Validation metric:** selection uses **label-constrained** Macro F1 over the **44 active classes** (`labels=[...]`, `zero_division=0`), per the plan's "label-constrained scikit-learn" requirement; gap classes cannot dilute the selection signal.
4. **Test gating:** the 1,580-image test set is **not touched** unless `--evaluate-test` is passed *after* the candidate checkpoint is chosen; when evaluated, it uses the corrected Task A label-bound subset metrics (active + full-taxonomy Macro F1, zero-support documented).

---

## 2. Checkpoint Reuse Review — Can `models/model1_expanded/best_model.pth` Be Resumed?

**Verdict: NO — EXP-1 must NOT resume it.** Detailed analysis:

| Aspect | Finding | Consequence |
|:---|:---|:---|
| **Architecture compatibility** | ✅ Identical: `efficientnet_b2` + `Linear(in_features, 46)`; `class_to_idx`/`sorted_classes` (0–45) identical to `model1_expanded_class_mapping.json`; ImageNet normalization metadata identical. Verified during Task A — the full `state_dict` loads with zero missing/unexpected keys. | The *checkpoint format* is compatible with the prepared script. |
| **Optimizer state** | ❌ Absent. The run-1 checkpoint stores only `{epoch, model_state_dict, val metrics, class_to_idx, sorted_classes, architecture, image_size, mean, std}` — **no `optimizer_state_dict`**. | AdamW first/second moments cannot be restored; a "resume" would silently start a fresh optimizer at a *new* LR — not a resume. |
| **Scheduler / scaler / RNG state** | ❌ Absent (no `scheduler_state_dict`, no `scaler_state_dict`, no CUDA/CPU RNG, no sampler epoch state). | Cosine phase, AMP scaler history and RNG stream are unrecoverable → results could not be honestly labeled "continued run 1". |
| **Backbone weights** | ⚠️ Already co-adapted by 10 single-stage epochs at lr 3e-4 (head noise propagated into convolutions — the very defect EXP-1 tests). | Loading it would make Stage 1 a no-op warm-start on an already-distorted backbone and **confound the hypothesis under test**. |
| **Classifier head** | ⚠️ Already trained (converged on the distorted backbone). Stage 1's purpose is to train a head on a *frozen, pristine* backbone. | Reusing the head injects trained-head bias and defeats the stage-1 rationale. |
| **BatchNorm running stats** | ⚠️ Run-1 stats were updated throughout single-stage training. | Another reason to initialize from cached `EfficientNet_B2_Weights.DEFAULT` (verified present locally — **no download required**). |

**Decisions encoded in the prepared script:**
- `build_model()` → **always** `EfficientNet_B2_Weights.DEFAULT` + fresh random 46-class head; `"resume_from_run1_checkpoint": False` is written into `config_exp1.json`.
- Run-1 `best_model.pth` is **never read** by EXP-1 (comparison-only baseline for EXP-0 vs EXP-1 deltas).
- Run-1 artifacts (`models/model1_expanded/best_model.pth`, `training_summary.json`, run-1 reports) are **never overwritten** — EXP-1 writes exclusively to `models/model1_expanded/exp1/` and `reports/model1_expansion/exp1/`.
- `last_model_exp1.pth` **does** persist optimizer/scheduler/scaler states so a genuine resume of EXP-1 itself remains possible (a gap in run 1 that is closed here).
- A warm-start ablation from run-1 weights (EXP-1b) was considered and **rejected for this run** to preserve single-variable purity; it can be proposed later as a separate experiment.

---

## 3. Safety Gates & Verified Preflight

### 3.1 Built-in gates
| Gate | Mechanism | Verified |
|:---|:---|:---:|
| No accidental training | Bare invocation prints the plan and exits; training requires explicit `--run` | ✅ executed `python scripts/train_model1_expanded_exp1.py` → plan printed, **exit 0, zero files written** |
| No accidental test evaluation | Test pass requires `--run --evaluate-test` (default off; checkpoint must be selected first) | ✅ code-path inspection |
| Production isolation | Script contains **no code path** touching `models/model1/` or `models/model2_classifier_v4/` (read-only existence assertion only) | ✅ code review |
| Run-1 artifact isolation | All EXP-1 outputs under `exp1/` subdirectories; no shared output paths with run 1 | ✅ code review |
| Immutable test set | Dataset constructed read-only; `assert len(test_dataset) == 1580`; no writes to `data/` | ✅ code review |
| No dataset download/creation | Uses existing `data/processed/model1_expanded/` only; ImageNet B2 weights already cached | ✅ preflight check |

### 3.2 Preflight check results (executed this phase)
```
[PASS] dataset root exists
[PASS] train split exists
[PASS] val split exists
[PASS] immutable test split exists
[PASS] class mapping exists
[PASS] run-1 baseline checkpoint present (comparison only, NOT resumed)
[PASS] production Model 1 present (locked, must not be written)
[PASS] production Model 2 V4 present (locked, must not be written)
[PASS] ImageNet-B2 weights cached locally (no download needed)
[PASS] torch importable
```
**10 / 10 PASS.** Script compiles cleanly (`python -m py_compile` → exit 0).

---

## 4. Execution Plan (When Authorized)

```bash
# 1. Execute the two-stage experiment (GPU expected; CPU works but is slow)
python scripts/train_model1_expanded_exp1.py --run

# 2. AFTER validating val metrics and selecting the candidate checkpoint:
python scripts/train_model1_expanded_exp1.py --run --evaluate-test   # or a dedicated eval pass
```
- **Estimated epochs:** 14 total (4 frozen + up to 10 fine-tune). Stage 1 epochs are cheaper (backbone forward-only, no backbone grads); expect total wall time ≈ 1.2–1.5× a run-1 epoch-cost × 14 on the RTX 3050.
- **Artifacts produced:** `models/model1_expanded/exp1/{best_model_exp1.pth, last_model_exp1.pth, config_exp1.json, training_summary_exp1.json}` and `reports/model1_expansion/exp1/{exp1_training.log, exp1_training_metrics.csv, exp1_test_metrics.csv}`.
- **Post-run gate:** compare against EXP-0 (Run 1) using the corrected metrics from `expanded_model1_metric_fix.json`.

---

## 5. Acceptance & Gating Criteria (from the approved experiment plan)

**EXP-1-specific acceptance:** Validation Macro F1 (active classes) **≥ 88.00%** (vs EXP-0 baseline 86.63%, +1.4 pp).

**Promotion-candidate gates (any experiment, evaluated only on corrected metrics):**
1. Overall Top-1 ≥ 92.0% (baseline 90.38%)
2. Overall Top-3 ≥ 98.0% (baseline 97.34%)
3. Overall Macro F1 ≥ 87.0% (baseline 83.81%)
4. Original-22 Top-1 ≥ 95.0% (baseline 95.53%)
5. New-24 Top-1 ≥ 88.0% (baseline 84.02%)
6. Zero regressions on core food crops (`tomato`, `potato`, `wheat`, `rice`, `corn`, `soybean`)
7. 100% SHA-256 integrity & leakage audit pass

**Known risks deliberately held constant (addressed by *other* experiments, not EXP-1):**
- Dual weighting (sampler + weighted loss) remains → EXP-2 territory.
- Under-convergence (val loss still declining at epoch 10) → EXP-3 territory; EXP-1's 14 epochs partially mitigate.
- `gerbera` (3 images) cannot be fixed by any schedule → data acquisition.
- `cherry_tomato` / `gypsophila` dead logits → handled per the taxonomy resolution report (loss weight 0.0 + inference-layer alias/abstain rules); **not** silently removed from the taxonomy.

---

## 6. Readiness Verdict & Safety Attestation

**✅ EXP-1 IS READY TO RUN.** The two-stage script is complete, compiles, passes 10/10 preflight checks, implements the specified Stage-1 (frozen backbone, 4 epochs, lr 1e-3) and Stage-2 (full fine-tune, ≤10 epochs, lr 7e-5 cosine → 1e-6), preserves AMP/reproducibility/GPU-safe batch size, applies the corrected label-constrained metrics, and cannot execute training without an explicit `--run` flag. The old checkpoint's reuse was formally reviewed and **rejected** (no optimizer/scheduler/RNG state; co-adapted backbone would confound the hypothesis) — EXP-1 initializes from cached ImageNet weights with a fresh 46-class head.

**Execution in this phase: NONE.** Specifically:
- [x] Training NOT started (`--run` never passed; preflight mode verified side-effect-free).
- [x] No dataset downloaded or altered; immutable 1,580-image test set and 178-image benchmark untouched.
- [x] Production Model 1 and Model 2 V4 untouched (locked).
- [x] No model promoted; run-1 experimental checkpoint unchanged.
- [x] 46-crop taxonomy unchanged.


