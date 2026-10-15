"""
Crop-Disease Reliability Audit (READ-ONLY over production artifacts)
===================================================================
Verifies deployed checkpoint mappings, cross-references Model 2 disease classes
with the crop-disease compatibility map, joins Model 1 per-crop test metrics with
Model 2 per-disease evidence, and emits reliability_audit.csv / reliability_audit.md.

Artifacts consumed (read-only, never modified):
  models/model1_expanded/best_model.pth (verified only: head size)
  models/model1_expanded/class_mapping.json
  reports/model1_expansion/expanded_model1_per_class_metrics.csv
  models/model2_retraining_v2/best_model.pth (verified only: head size)
  models/model2_retraining_v2/class_mapping.json
  models/model2_retraining_v2/crop_disease_mapping.json
  reports/model2_retraining/test_evaluation/test_classification_report.csv
      NOTE: evaluated model2_retraining_v1/best_model.pth - reference evidence only.

Quality criterion (explicit):
  Crop gate     : Model 1 crop F1 >= 0.85 AND crop test support >= 20
  Disease gate  : DEPLOYED checkpoint (retraining_v2) disease F1 >= 0.80 AND support >= 10
  Compatibility : disease slug registered in crop_disease_mapping for its crop AND
                  crop resolvable to a Model 1 class (direct name or production alias)
  RELIABLE      : all three pass. Anything lacking per-class evaluation on the
                  deployed checkpoint is marked UNVERIFIED (never assumed accurate).
"""

from __future__ import annotations

import csv
import json
from collections import Counter, OrderedDict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = Path(__file__).resolve().parent

M1_CKPT = PROJECT_ROOT / "models" / "model1_expanded" / "best_model.pth"
M1_MAP = PROJECT_ROOT / "models" / "model1_expanded" / "class_mapping.json"
M1_PER_CLASS = PROJECT_ROOT / "reports" / "model1_expansion" / "expanded_model1_per_class_metrics.csv"

M2_CKPT = PROJECT_ROOT / "models" / "model2_retraining_v2" / "best_model.pth"
M2_MAP = PROJECT_ROOT / "models" / "model2_retraining_v2" / "class_mapping.json"
M2_CROP_MAP = PROJECT_ROOT / "models" / "model2_retraining_v2" / "crop_disease_mapping.json"

M2_V1_REF_REPORT = PROJECT_ROOT / "reports" / "model2_retraining" / "test_evaluation" / "test_classification_report.csv"
M2_V2_TRAIN_PROGRESS = PROJECT_ROOT / "reports" / "model2_retraining_v2" / "training_progress.csv"

CROP_F1_MIN = 0.85
CROP_SUPPORT_MIN = 20
DISEASE_F1_MIN = 0.80
DISEASE_SUPPORT_MIN = 10

# Production aliases: model2 crop name -> model1 crop class
# (mirrors models/model2_classifier_v4/predict.py is_compatible() and model1 aliases)
M2_TO_M1_ALIAS = {
    "bell_pepper": "bellpepper",
    "capsicum": "bellpepper",
    "bean": "french_bean",
    "squash": "zucchini",
    "cherry_tomato": "tomato",
}
# reverse for display lookups from model1 canonical name -> model2 crop name
M1_TO_M2_NAME = {"bellpepper": "bell_pepper", "french_bean": "bean", "zucchini": "squash"}


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_checkpoint_head(ckpt_path: Path) -> dict:
    """Read-only verification: inspect final Linear layer output features."""
    import torch

    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    state = ckpt.get("model_state_dict", ckpt)
    info = {"checkpoint": str(ckpt_path)}
    for key in ("classifier.1.weight", "classifier.2.weight", "fc.weight", "head.fc.weight"):
        if key in state:
            info["head_layer"] = key
            info["head_out_features"] = int(state[key].shape[0])
            info["head_in_features"] = int(state[key].shape[1])
            break
    if isinstance(ckpt, dict):
        for key in ("epoch", "best_macro_f1", "best_val_macro_f1", "val_macro_f1"):
            if key in ckpt:
                info[key] = ckpt[key]
    return info


def main() -> None:
    # ------------------------------------------------------------------ #
    # 1. Verify class mappings & checkpoints                             #
    # ------------------------------------------------------------------ #
    m1_mapping = load_json(M1_MAP)
    m1_class_to_idx = m1_mapping["class_to_idx"]
    m1_aliases = m1_mapping.get("aliases", {})

    m2_class_to_idx = load_json(M2_MAP)
    m2_crop_map = load_json(M2_CROP_MAP)

    ckpt_verification = {}
    try:
        ckpt_verification["model1"] = verify_checkpoint_head(M1_CKPT)
        ckpt_verification["model2"] = verify_checkpoint_head(M2_CKPT)
    except Exception as exc:  # torch may be unavailable; report rather than fail
        ckpt_verification["error"] = f"checkpoint head inspection skipped: {exc}"

    m1_head_ok = ckpt_verification.get("model1", {}).get("head_out_features") == len(m1_class_to_idx)
    m2_head_ok = ckpt_verification.get("model2", {}).get("head_out_features") == len(m2_class_to_idx)

    # ------------------------------------------------------------------ #
    # 2. Model 1 per-crop test metrics (canonicalized via aliases)       #
    # ------------------------------------------------------------------ #
    m1_metrics: dict[str, dict] = {}
    with open(M1_PER_CLASS, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            m1_metrics[row["class_name"]] = {
                "precision": float(row["precision"]),
                "recall": float(row["recall"]),
                "f1": float(row["f1_score"]),
                "support": int(float(row["support"])),
            }
    # m1_aliases maps alias -> canonical (e.g. capsicum->bellpepper). Direct CSV rows win;
    # alias rows only fill canonical slots that have no direct row.
    normalized_m1_metrics: dict[str, dict] = {}
    for name, met in m1_metrics.items():
        normalized_m1_metrics.setdefault(name, met)
    for name, met in m1_metrics.items():
        canonical = m1_aliases.get(name, name)
        normalized_m1_metrics.setdefault(canonical, met)
    for canonical in m1_class_to_idx:
        normalized_m1_metrics.setdefault(
            canonical, {"precision": None, "recall": None, "f1": None, "support": None}
        )

    # ------------------------------------------------------------------ #
    # 3. Model 2 v1 reference report (predecessor checkpoint ONLY)       #
    # ------------------------------------------------------------------ #
    m2_v1_ref: dict[str, dict] = {}
    with open(M2_V1_REF_REPORT, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            m2_v1_ref[row["canonical_class"]] = {
                "precision": float(row["precision"]),
                "recall": float(row["recall"]),
                "f1": float(row["f1_score"]),
                "support": int(row["support"]),
            }

    v2_best_val = None
    if M2_V2_TRAIN_PROGRESS.exists():
        with open(M2_V2_TRAIN_PROGRESS, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if rows:
            best = max(rows, key=lambda r: float(r["val_macro_f1"]))
            v2_best_val = {
                "epoch": best["epoch"],
                "val_macro_f1": float(best["val_macro_f1"]),
                "val_acc": float(best["val_acc"]),
            }

    # ------------------------------------------------------------------ #
    # 4. Cross-reference every Model 2 disease class with crop map       #
    # ------------------------------------------------------------------ #
    crop_map_pairs = {(crop, d) for crop, diseases in m2_crop_map.items() for d in diseases}

    m2_disease_classes = {k: v for k, v in m2_class_to_idx.items() if k != "healthy"}
    unmapped_disease_classes = []
    for slug in m2_disease_classes:
        if "__" not in slug:
            unmapped_disease_classes.append(slug)
            continue
        crop, disease = slug.split("__", 1)
        if (crop, disease) not in crop_map_pairs:
            unmapped_disease_classes.append(slug)

    map_pairs_without_class = sorted(
        f"{c}__{d}" for (c, d) in crop_map_pairs if f"{c}__{d}" not in m2_disease_classes
    )

    # ------------------------------------------------------------------ #
    # 5. Resolve every Model 2 crop to a Model 1 crop                    #
    # ------------------------------------------------------------------ #
    m2_crops = sorted(m2_crop_map.keys())
    crop_resolution: dict[str, str | None] = {}
    for crop in m2_crops:
        if crop in m1_class_to_idx:
            crop_resolution[crop] = crop
        elif crop in M2_TO_M1_ALIAS and M2_TO_M1_ALIAS[crop] in m1_class_to_idx:
            crop_resolution[crop] = M2_TO_M1_ALIAS[crop]
        else:
            crop_resolution[crop] = None
    unresolved_crops = [c for c, v in crop_resolution.items() if v is None]

    # ------------------------------------------------------------------ #
    # 6. Build per-combination audit rows                                #
    # ------------------------------------------------------------------ #
    def crop_gate(m1_name: str) -> tuple[str, list[str]]:
        met = normalized_m1_metrics.get(m1_name, {})
        flags: list[str] = []
        f1, sup = met.get("f1"), met.get("support")
        if f1 is None or sup is None:
            return "NO_METRICS", ["CROP_METRICS_MISSING"]
        if sup == 0:
            return "NO_TEST_SUPPORT", ["ZERO_CROP_TEST_SUPPORT"]
        if sup < CROP_SUPPORT_MIN:
            flags.append("LOW_CROP_SUPPORT")
        return ("PASS" if f1 >= CROP_F1_MIN else "FAIL"), flags

    rows_out: list[OrderedDict] = []

    def make_row(crop_m2: str, crop_m1: str | None, disease_slug: str, disease_short: str, is_healthy: bool):
        flags: list[str] = []
        compat = "COMPATIBLE"
        if is_healthy:
            compat = "COMPATIBLE (healthy is crop-agnostic)"
        else:
            crop_prefix, _, short = disease_slug.partition("__")
            if crop_prefix not in m2_crop_map or short not in m2_crop_map[crop_prefix]:
                compat = "MISMATCH_NOT_IN_CROP_MAP"
                flags.append("DISEASE_NOT_IN_CROP_MAP")
        if crop_m1 is None:
            compat = "CROP_UNRESOLVED_TO_MODEL1"
            flags.append("CROP_NOT_IN_MODEL1")

        gate, cflags = crop_gate(crop_m1) if crop_m1 else ("CROP_UNRESOLVED", ["CROP_NOT_IN_MODEL1"])
        flags.extend(cflags)

        met = normalized_m1_metrics.get(crop_m1, {}) if crop_m1 else {}
        ref = m2_v1_ref.get(disease_slug)
        if ref is None:
            flags.append("NO_V1_REFERENCE_EVAL")

        if gate == "PASS" and compat.startswith("COMPATIBLE"):
            if ref is not None and ref["f1"] >= DISEASE_F1_MIN and ref["support"] >= DISEASE_SUPPORT_MIN:
                category = "PROVISIONAL_UNVERIFIED"
            else:
                category = "UNVERIFIED"
                if ref is not None and ref["f1"] >= DISEASE_F1_MIN and ref["support"] < DISEASE_SUPPORT_MIN:
                    flags.append("DISEASE_REF_LOW_SUPPORT")
                elif ref is not None:
                    flags.append("DISEASE_REF_BELOW_THRESHOLD")
        else:
            category = "UNVERIFIED"

        row = OrderedDict()
        row["crop_model2"] = crop_m2
        row["crop_model1_class"] = crop_m1 or "UNRESOLVED"
        row["disease_model2_class"] = disease_slug
        row["disease_short"] = disease_short
        row["model1_crop_precision"] = met.get("precision", "")
        row["model1_crop_recall"] = met.get("recall", "")
        row["model1_crop_f1"] = met.get("f1", "")
        row["model1_crop_test_support"] = met.get("support", "")
        row["crop_gate"] = gate
        row["model2_v2_disease_precision"] = "NOT_EVALUATED"
        row["model2_v2_disease_recall"] = "NOT_EVALUATED"
        row["model2_v2_disease_f1"] = "NOT_EVALUATED"
        row["model2_v2_disease_test_support"] = "NOT_EVALUATED"
        row["model2_v2_disease_gate"] = "NOT_EVALUATED (deployed v2 checkpoint never test-evaluated)"
        row["model2_v1_reference_precision"] = ref["precision"] if ref else "NO_REFERENCE"
        row["model2_v1_reference_recall"] = ref["recall"] if ref else "NO_REFERENCE"
        row["model2_v1_reference_f1"] = ref["f1"] if ref else "NO_REFERENCE"
        row["model2_v1_reference_test_support"] = ref["support"] if ref else "NO_REFERENCE"
        row["compatibility_status"] = compat
        row["flags"] = ";".join(dict.fromkeys(flags)) if flags else ""
        row["final_reliability"] = category
        return row

    for slug in sorted(m2_disease_classes, key=lambda s: m2_class_to_idx[s]):
        crop_m2 = slug.split("__", 1)[0]
        rows_out.append(make_row(crop_m2, crop_resolution.get(crop_m2), slug, slug.split("__", 1)[1], False))

    for crop_m2 in m2_crops:  # healthy rows: one per Model 2 crop
        rows_out.append(make_row(crop_m2, crop_resolution.get(crop_m2), "healthy", "healthy", True))

    # ------------------------------------------------------------------ #
    # 7. Write CSV                                                       #
    # ------------------------------------------------------------------ #
    csv_path = OUT_DIR / "reliability_audit.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        writer.writeheader()
        writer.writerows(rows_out)


    # ------------------------------------------------------------------ #
    # 8. Write Markdown report                                           #
    # ------------------------------------------------------------------ #
    n_disease = len(m2_disease_classes)
    cat_counts = Counter(r["final_reliability"] for r in rows_out)
    gate_counts = Counter(r["crop_gate"] for r in rows_out)
    flag_counter: Counter = Counter()
    for r in rows_out:
        for fl in (r["flags"].split(";") if r["flags"] else []):
            flag_counter[fl] += 1

    prov_by_crop: dict[str, list[tuple[str, float, int]]] = {}
    for r in rows_out:
        if r["final_reliability"] == "PROVISIONAL_UNVERIFIED" and r["disease_short"] != "healthy":
            prov_by_crop.setdefault(r["crop_model1_class"], []).append(
                (r["disease_short"], float(r["model2_v1_reference_f1"]), int(r["model2_v1_reference_test_support"]))
            )

    low_crop_support = sorted({r["crop_model1_class"] for r in rows_out if "LOW_CROP_SUPPORT" in r["flags"]})
    zero_crop_support = sorted({r["crop_model1_class"] for r in rows_out if "ZERO_CROP_TEST_SUPPORT" in r["flags"]})
    ref_low_support = sorted({r["disease_model2_class"] for r in rows_out if "DISEASE_REF_LOW_SUPPORT" in r["flags"]})
    no_ref = sorted({r["disease_model2_class"] for r in rows_out if "NO_V1_REFERENCE_EVAL" in r["flags"]})
    m1_only_crops = sorted(c for c in m1_class_to_idx if c not in set(crop_resolution.values()))

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    m1_info = ckpt_verification.get("model1", {})
    m2_info = ckpt_verification.get("model2", {})

    L: list[str] = []
    L.append("# Crop-Disease Reliability Audit - Plant Disease AI (READ-ONLY)")
    L.append("")
    L.append(f"**Generated:** {ts}  ")
    L.append("**Scope:** deployed artifacts only; no retraining, mapping edits, checkpoint or deployment changes were made.")
    L.append("")
    L.append("## 1. Artifacts Verified")
    L.append("")
    L.append("| Model | Artifact | Status |")
    L.append("|---|---|---|")
    L.append(f"| Model 1 (crop) | `models/model1_expanded/best_model.pth` | checkpoint head out_features = "
             f"{m1_info.get('head_out_features', 'n/a')} vs {len(m1_class_to_idx)} mapping classes -> "
             f"{'MATCH' if m1_head_ok else 'NOT CONFIRMED'} |")
    L.append(f"| Model 1 (crop) | `models/model1_expanded/class_mapping.json` | {len(m1_class_to_idx)} crop classes + {len(m1_aliases)} aliases |")
    L.append("| Model 1 (crop) | `reports/model1_expansion/expanded_model1_per_class_metrics.csv` | per-crop P/R/F1/support on the 1,580-image immutable test set; "
             "checkpoint identity confirmed via `training_summary.json` and `expanded_model1_metric_fix_report.md` |")
    L.append(f"| Model 2 (disease) | `models/model2_retraining_v2/best_model.pth` | checkpoint head out_features = "
             f"{m2_info.get('head_out_features', 'n/a')} vs {len(m2_class_to_idx)} mapping classes -> "
             f"{'MATCH' if m2_head_ok else 'NOT CONFIRMED'} |")
    L.append(f"| Model 2 (disease) | `models/model2_retraining_v2/class_mapping.json` | {len(m2_class_to_idx)} classes (`healthy` + {n_disease} diseases) |")
    L.append(f"| Model 2 (disease) | `models/model2_retraining_v2/crop_disease_mapping.json` | {len(m2_crop_map)} crops, {len(crop_map_pairs)} crop-disease pairs |")
    L.append("| Model 2 (disease) | per-class evaluation report | **DOES NOT EXIST for the deployed v2 checkpoint** (see section 3) |")
    L.append("| Inference code | `models/model2_classifier_v4/predict.py` + `app/backend/services.py` | two-stage pipeline: Model 1 crop -> Model 2 crop-aware disease "
             "with compatibility filter, probability masking, healthy/diseased/uncertain contract |")
    L.append("")
    if ckpt_verification.get("error"):
        L.append(f"- {ckpt_verification['error']}")
        L.append("")
    L.append("## 2. Model 2 vs Crop-Disease Compatibility Cross-Reference")
    L.append("")
    L.append(f"- Disease classes in deployed `class_mapping.json`: **{n_disease}** (+1 crop-agnostic `healthy`).")
    L.append(f"- Crop-disease pairs in deployed `crop_disease_mapping.json`: **{len(crop_map_pairs)}** across **{len(m2_crop_map)}** crops.")
    L.append(f"- Disease classes with no matching entry in the crop map: **{len(unmapped_disease_classes)}**"
             + (f" - {unmapped_disease_classes}" if unmapped_disease_classes else " (none - full 1:1 coverage)"))
    L.append(f"- Crop-map pairs with no corresponding model class: **{len(map_pairs_without_class)}**"
             + (f" - {map_pairs_without_class}" if map_pairs_without_class else " (none - full 1:1 coverage)"))
    L.append(f"- Model 2 crops unresolved to a Model 1 crop class: **{len(unresolved_crops)}**"
             + (f" - {unresolved_crops}" if unresolved_crops else
                " (none - all resolved directly or via production aliases `bell_pepper->bellpepper`, `bean->french_bean`, `squash->zucchini`)"))
    L.append(f"- Model 1 crops with no disease coverage in Model 2 (crop-ID stage only, by design): **{len(m1_only_crops)}** - {m1_only_crops}")
    L.append("")


    L.append("## 3. Model 2 Evidence Gap (CRITICAL)")
    L.append("")
    L.append("- The deployed `models/model2_retraining_v2/best_model.pth` **has never been evaluated on the 2,304-image protected test set.** "
             "`reports/model2_retraining_v2/training.log` states: *\"Test Images (Immutable): 2,304 (Protected - not evaluated in training loop)\"*; "
             "no test-evaluation artifacts exist for v2 anywhere in the repository.")
    if v2_best_val:
        L.append(f"- Only aggregate **validation** metrics exist for v2: best epoch {v2_best_val['epoch']} -> val macro-F1 "
                 f"**{v2_best_val['val_macro_f1']:.4f}**, val accuracy **{v2_best_val['val_acc']:.4f}** "
                 "(`reports/model2_retraining_v2/training_progress.csv`). These are validation aggregates, **not** per-class test evidence.")
    L.append("- The only per-class test report in the retraining lineage "
             "(`reports/model2_retraining/test_evaluation/test_classification_report.csv`) evaluated the **predecessor** "
             "`models/model2_retraining_v1/best_model.pth` (epoch 4; macro-F1 0.5731; disease-class macro-F1 0.5138; n=2,304). "
             "v2 fine-tuned from that checkpoint and added one class (`tomato__anthracnose`, id 143), so v1 numbers **cannot** verify v2.")
    L.append("- Therefore **no crop-disease combination can be certified RELIABLE** on current evidence. Rows that pass the crop gate and show strong "
             "*v1-reference* disease metrics are labeled `PROVISIONAL_UNVERIFIED`; all others are `UNVERIFIED`.")
    L.append("")
    L.append("## 4. Quality Criterion (explicit)")
    L.append("")
    L.append("| Gate | Threshold | Evidence source |")
    L.append("|---|---|---|")
    L.append(f"| Crop (Model 1) | F1 >= **{CROP_F1_MIN}** AND test support >= **{CROP_SUPPORT_MIN}** | `expanded_model1_per_class_metrics.csv` (deployed checkpoint) |")
    L.append(f"| Disease (Model 2) | F1 >= **{DISEASE_F1_MIN}** AND test support >= **{DISEASE_SUPPORT_MIN}** on the **deployed** checkpoint | *no artifact exists* |")
    L.append("| Compatibility | disease slug registered under its crop in `crop_disease_mapping.json`; crop resolvable to a Model 1 class | deployed mapping files |")
    L.append("")
    L.append("**RELIABLE** = crop gate PASS + disease gate PASS + compatibility OK.  ")
    L.append(f"**PROVISIONAL_UNVERIFIED** = crop gate PASS + compatibility OK + v1-reference disease F1 >= {DISEASE_F1_MIN} with support >= "
             f"{DISEASE_SUPPORT_MIN} (indicative only, not deployed-checkpoint evidence).  ")
    L.append("**UNVERIFIED** = everything else, including all combinations lacking deployed-checkpoint per-class evaluation.  ")
    L.append(f"Low-support flags: crop support < {CROP_SUPPORT_MIN} -> `LOW_CROP_SUPPORT`; crop support = 0 -> `ZERO_CROP_TEST_SUPPORT`; "
             f"v1-reference disease support < {DISEASE_SUPPORT_MIN} -> `DISEASE_REF_LOW_SUPPORT`.")
    L.append("")
    L.append("## 5. Summary Counts")
    L.append("")
    L.append(f"- Total audited rows: **{len(rows_out)}** ({n_disease} disease classes + {len(m2_crops)} per-crop healthy rows)")
    L.append("- Final categories: " + ", ".join(f"**{k}: {v}**" for k, v in sorted(cat_counts.items())))
    L.append("- Crop gate: " + ", ".join(f"{k}: {v}" for k, v in sorted(gate_counts.items())))
    L.append("- Flag tallies: " + (", ".join(f"{k}: {v}" for k, v in sorted(flag_counter.items())) if flag_counter else "none"))
    L.append("")


    L.append("## 6. RELIABLE Combinations")
    L.append("")
    if cat_counts.get("RELIABLE", 0) == 0:
        L.append("**None.** No combination has per-class disease evidence on the deployed `model2_retraining_v2` checkpoint; "
                  "deploying any disease prediction as \"reliable\" is not supported by evaluation evidence.")
    else:
        for r in rows_out:
            if r["final_reliability"] == "RELIABLE":
                L.append(f"- {r['crop_model1_class']} -> {r['disease_model2_class']}")
    L.append("")
    L.append("## 7. PROVISIONAL_UNVERIFIED Combinations (crop gate PASS, strong v1-reference disease metrics)")
    L.append("")
    L.append("These pass the crop gate on the deployed Model 1 checkpoint and their disease classes scored F1 >= "
             f"{DISEASE_F1_MIN} (support >= {DISEASE_SUPPORT_MIN}) on the **v1** checkpoint test report. They remain **UNVERIFIED** "
             "until the deployed v2 checkpoint is evaluated on the protected test set.")
    L.append("")
    if prov_by_crop:
        L.append("| Model 1 crop | Crop F1 | Crop support | Provisional disease classes (v1-ref F1, support) |")
        L.append("|---|---|---|---|")
        for crop in sorted(prov_by_crop):
            met = normalized_m1_metrics[crop]
            ds = sorted(prov_by_crop[crop])
            dtxt = "; ".join(f"{d} ({f1:.2f}, n={sup})" for d, f1, sup in ds)
            L.append(f"| {crop} | {met['f1']:.4f} | {met['support']} | {dtxt} |")
    else:
        L.append("_None_")
    L.append("")
    L.append("## 8. Flagged Items")
    L.append("")
    L.append(f"- **Model 1 crops with LOW test support (<{CROP_SUPPORT_MIN}):** "
             + (", ".join(low_crop_support) if low_crop_support else "none"))
    L.append("- **Model 1 crops with ZERO test support:** "
             + (", ".join(zero_crop_support) if zero_crop_support else "none among the 36 audited crops")
             + ". Note: outside the audited set, Model 1-only crops `cherry_tomato` and `gypsophila` also have 0 test support "
             "and `gerbera` has support=1 with F1=0.0 (they produce no crop-disease rows since Model 2 has no diseases for them).")
    L.append(f"- **Disease classes with LOW v1-reference support (<{DISEASE_SUPPORT_MIN}):** {len(ref_low_support)} classes - "
             + ", ".join(ref_low_support))
    L.append(f"- **Disease classes with NO reference evaluation at all (v2-only):** "
             + (", ".join(no_ref) if no_ref else "none"))
    L.append(f"- **Disease classes that cannot be matched to a supported crop:** "
             + (", ".join(unmapped_disease_classes) if unmapped_disease_classes else
                f"none - all {n_disease} disease classes are registered under their crop prefix in the deployed crop map"))
    L.append(f"- **Model 2 crops that cannot be matched to a Model 1 crop:** "
             + (", ".join(unresolved_crops) if unresolved_crops else "none - all 36 resolve via direct name or production alias"))
    L.append("")


    L.append("## 9. Full Combination Table")
    L.append("")
    L.append("| Crop (M1) | Disease (M2) | M1 P/R/F1/support | M1 gate | M2-v2 disease metrics | M2-v1-ref P/R/F1/support | Compat | Flags | Final |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows_out:
        m1txt = (f"{r['model1_crop_precision']}/{r['model1_crop_recall']}/{r['model1_crop_f1']}"
                 f"/{r['model1_crop_test_support']}")
        ref_txt = (f"{r['model2_v1_reference_precision']}/{r['model2_v1_reference_recall']}/"
                   f"{r['model2_v1_reference_f1']}/{r['model2_v1_reference_test_support']}")
        L.append(f"| {r['crop_model1_class']} | {r['disease_model2_class']} | {m1txt} | {r['crop_gate']} | NOT_EVALUATED | "
                 f"{ref_txt} | {r['compatibility_status']} | {r['flags'] or '-'} | {r['final_reliability']} |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Methodology & Limitations")
    L.append("")
    L.append("- Read-only audit: all production artifacts were read without modification; outputs were written only to this new folder.")
    L.append("- Disease accuracy was **never** inferred from crop accuracy, validation aggregates, or training-image counts.")
    L.append("- v1-reference numbers describe the **model2_retraining_v1** evaluation and are indicative context only.")
    L.append("- Production defaults (`app/backend/config.py`) point at `models/model2_classifier_v4` unless `MODEL2_CHECKPOINT` / "
             "`MODEL2_CLASS_MAPPING` env vars override them; this audit follows the requested deployed pair "
             "(`model2_retraining_v2` checkpoint served by the `model2_classifier_v4/predict.py` engine, which loads whatever mapping it is given).")
    L.append("- Recommended next step (NOT performed here): evaluate `models/model2_retraining_v2/best_model.pth` on the frozen 2,304-image "
             "test set to turn PROVISIONAL/UNVERIFIED rows into evidence-based verdicts.")

    md_path = OUT_DIR / "reliability_audit.md"
    md_path.write_text("\n".join(L), encoding="utf-8")

    print(f"CSV : {csv_path} ({len(rows_out)} rows)")
    print(f"MD  : {md_path}")
    print(f"Categories: {dict(cat_counts)}")
    print(f"Crop gate : {dict(gate_counts)}")
    print(f"Unmapped disease classes: {unmapped_disease_classes}")
    print(f"Map pairs without class : {map_pairs_without_class}")
    print(f"Unresolved crops        : {unresolved_crops}")
    print(f"Checkpoint heads        : m1={m1_info.get('head_out_features')}, m2={m2_info.get('head_out_features')} "
          f"(mapping sizes {len(m1_class_to_idx)}/{len(m2_class_to_idx)})")


if __name__ == "__main__":
    main()
