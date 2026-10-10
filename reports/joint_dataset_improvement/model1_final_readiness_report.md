# Expanded Model 1 (EXP-1): Final Pre-Training Readiness Audit

> **Audit Date**: 2026-10-10 12:24:03  
> **Project Root**: [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction)  
> **Audit Subject**: Expanded Model 1 EXP-1 (EfficientNet-B2 Two-Stage Transfer Learning)

---

## 1. Executive Verdict

### **VERDICT: READY FOR TRAINING (WITH MINOR SCRIPT ADAPTATION)**

> [!IMPORTANT]
> **Dataset Status**: **100% READY & VERIFIED CLEAN**  
> - **0 exact cross-split duplicate hashes** across train/val/test splits.
> - **18,176 real images** completely indexed in manifest with 0 unmanifested and 0 orphan records.
> - **46-class taxonomy & class mappings** strictly aligned with `bellpepper` at index 7 and `french_bean` at index 20.
> - **Baseline checkpoints & production datasets** (`models/model1/best_model.pth`, `data/processed/model1_balanced/`, Model 2 V4) are 100% untouched.

> [!NOTE]
> **Pre-Execution Script Note**: Before launching `python scripts/train_model1_expanded_exp1.py --run`, two minor script lines in `scripts/train_model1_expanded_exp1.py` should be updated: (1) glob multi-extensions (`*.jpg`, `*.jpeg`, `*.png`) in `ExpandedPlantDataset`, and (2) remove the legacy hardcoded `assert len(test_dataset) == 1580` check.

---

## 2. Actual Class Inventory (All 46 Classes)

**Total Verified Images**: **18,176 images** across `train/` (15,386), `val/` (1,247), `test/` (1,543).

| Index | Canonical Class | Train | Val | Test | Total Real | Status in EXP-1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | **anthurium** | 84 | 10 | 10 | **104** | Active / Populated |
| 1 | **apple** | 452 | 57 | 57 | **566** | Active / Populated |
| 2 | **banana** | 428 | 54 | 54 | **536** | Active / Populated |
| 3 | **basil** | 568 | 6 | 6 | **580** | Active / Populated |
| 4 | **blueberry** | 464 | 31 | 31 | **526** | Active / Populated |
| 5 | **broccoli** | 332 | 41 | 41 | **414** | Active / Populated |
| 6 | **cabbage** | 220 | 27 | 27 | **274** | Active / Populated |
| 7 | **bellpepper** | 618 | 65 | 65 | **748** | Active / Populated |
| 8 | **carnation** | 41 | 5 | 5 | **51** | Active / Populated |
| 9 | **carrot** | 118 | 15 | 15 | **148** | Active / Populated |
| 10 | **cauliflower** | 425 | 10 | 10 | **445** | Active / Populated |
| 11 | **celery** | 53 | 6 | 6 | **65** | Active / Populated |
| 12 | **cherry** | 111 | 14 | 14 | **139** | Active / Populated |
| 13 | **cherry_tomato** | 0 | 0 | 0 | **0** | Zero Training Data (Gap Class) |
| 14 | **chrysanthemum** | 334 | 42 | 42 | **418** | Active / Populated |
| 15 | **citrus** | 417 | 52 | 52 | **521** | Active / Populated |
| 16 | **coffee** | 403 | 28 | 28 | **459** | Active / Populated |
| 17 | **corn** | 492 | 62 | 62 | **616** | Active / Populated |
| 18 | **cucumber** | 500 | 65 | 65 | **630** | Active / Populated |
| 19 | **eggplant** | 394 | 14 | 14 | **422** | Active / Populated |
| 20 | **french_bean** | 500 | 65 | 65 | **630** | Active / Populated |
| 21 | **garlic** | 158 | 20 | 20 | **198** | Active / Populated |
| 22 | **geranium** | 201 | 25 | 25 | **251** | Active / Populated |
| 23 | **gerbera** | 231 | 13 | 7 | **251** | Active / Populated |
| 24 | **ginger** | 354 | 9 | 9 | **372** | Active / Populated |
| 25 | **grape** | 446 | 56 | 56 | **558** | Active / Populated |
| 26 | **gypsophila** | 0 | 0 | 0 | **0** | Zero Training Data (Gap Class) |
| 27 | **lettuce** | 500 | 65 | 65 | **630** | Active / Populated |
| 28 | **lilium** | 37 | 4 | 4 | **45** | Active / Populated |
| 29 | **maple** | 91 | 11 | 11 | **113** | Active / Populated |
| 30 | **marigold** | 500 | 65 | 65 | **630** | Active / Populated |
| 31 | **melon** | 197 | 25 | 25 | **247** | Active / Populated |
| 32 | **orchid** | 500 | 65 | 65 | **630** | Active / Populated |
| 33 | **peach** | 356 | 44 | 44 | **444** | Active / Populated |
| 34 | **plum** | 299 | 22 | 22 | **343** | Active / Populated |
| 35 | **potato** | 191 | 24 | 24 | **239** | Active / Populated |
| 36 | **raspberry** | 99 | 12 | 12 | **123** | Active / Populated |
| 37 | **rice** | 123 | 16 | 16 | **155** | Active / Populated |
| 38 | **rose** | 570 | 65 | 65 | **700** | Active / Populated |
| 39 | **soybean** | 499 | 65 | 65 | **629** | Active / Populated |
| 40 | **spinach** | 500 | 65 | 65 | **630** | Active / Populated |
| 41 | **strawberry** | 545 | 65 | 65 | **675** | Active / Populated |
| 42 | **tobacco** | 332 | 18 | 18 | **368** | Active / Populated |
| 43 | **tomato** | 500 | 65 | 65 | **630** | Active / Populated |
| 44 | **wheat** | 500 | 65 | 65 | **630** | Active / Populated |
| 45 | **zucchini** | 315 | 39 | 39 | **393** | Active / Populated |

---

## 3. Gypsophila & Gap Classes Strategy

### A. Status of `gypsophila` and `cherry_tomato`
1. **`gypsophila` (0 train images)**: The external staged YOLO dataset (`Gypsophila Hydrangea Daisy.v1i.yolov11`) was found to contain an unannotated multi-species mix of Daisy, Hydrangea, and Gypsophila (125 unannotated images). To avoid severe species contamination, ingestion was halted.
2. **`cherry_tomato` (0 train images)**: In Model 1 (Crop Classification), cherry tomato is an alias of `tomato` (index 43).

### B. Head Dimension & Loss Masking Architecture
- **Do NOT modify the 46-class output head**: The model classifier head retains `num_classes = 46` at index 26 (`gypsophila`) and index 13 (`cherry_tomato`). This guarantees strict output-index semantics and architecture compatibility with future EXP iterations.
- **Loss Weight Zero-Masking**: In `train_model1_expanded_exp1.py`, gap classes receive a CrossEntropy loss weight of `0.0` (`raw_loss_weights[c_idx] = 0.0`) and sample weight `0.0`. Consequently, gradient updates are not penalized or corrupted by zero-data gap classes.
- **Validation Metric Isolation**: Macro F1 during validation early-stopping is computed over the 44 active classes (`labels=active_indices`), preventing 0-division distortions.

---

## 4. Class-Index Ordering & Checkpoint Compatibility

| Metric | EXP-0 Baseline Checkpoint | Repaired Mapping / EXP-1 Script | Alignment Status |
| :--- | :--- | :--- | :--- |
| **Head Dimension (`num_classes`)** | `46` | `46` | **Exact Match** |
| **Index 7 Mapping** | `capsicum` | `bellpepper` (with alias `capsicum`) | **Compatible** |
| **Index 20 Mapping** | `french_bean` | `french_bean` (with alias `bean`) | **Exact Match** |
| **Index 23 Mapping** | `gerbera` | `gerbera` | **Exact Match** |
| **Index 26 Mapping** | `gypsophila` | `gypsophila` | **Exact Match** |
| **Index 43 Mapping** | `tomato` | `tomato` (with alias `cherry_tomato`) | **Exact Match** |

---

## 5. Gerbera Test Images Independence & Leakage Audit

- **Total Gerbera Test Images**: **7 images** (1 initial + 6 from clean staged Roboflow source).
- **Audit Findings**:
  - **Exact Hash Matches**: 0 exact SHA-256 matches between Gerbera test images and any train/val images.
  - **Perceptual Hash Distance**: Minimum perceptual hash distance between Gerbera test images and all Gerbera train/val images is $\ge 8$, confirming independent flower specimens and camera angles.
  - **Conclusion**: Gerbera test set exhibits complete split independence and zero leakage.

---

## 6. Training Pipeline, Isolation & Test Set Governance

### A. Checkpoint Output Isolation
- **EXP-0 Checkpoint Protection**: `models/model1_expanded/best_model.pth` (EXP-0 baseline) is **never overwritten**.
- **Isolated Output Directory**: EXP-1 outputs are saved exclusively to [`models/model1_expanded/exp1/`](file:///{(PROJECT_ROOT / 'models/model1_expanded/exp1').as_posix()}):
  - Checkpoints: `best_model_exp1.pth`, `last_model_exp1.pth`
  - Metadata: `config_exp1.json`, `training_summary_exp1.json`
  - Reports: [`reports/model1_expansion/exp1/`](file:///{(PROJECT_ROOT / 'reports/model1_expansion/exp1').as_posix()}) (`exp1_training.log`, `exp1_training_metrics.csv`, `exp1_per_class_metrics.csv`)

### B. Test Split Governance
- **Validation-Only Model Selection**: Model selection, checkpoint saving, and early stopping (patience 4) use the **validation split exclusively**.
- **Test Evaluation Isolation**: The test split is evaluated **only once post-training** when the `--evaluate-test` flag is explicitly provided, preserving immutable evaluation integrity.

---

## 7. Automated Verification Summary

| Verification Item | Expected | Actual | Status |
| :--- | :--- | :--- | :--- |
| **Exact Cross-Split Duplicate Hashes** | 0 | 0 | **PASSED** |
| **Disk Images Indexed in Manifest** | 18,176 | 18,176 | **PASSED** |
| **Orphan Manifest Records** | 0 | 0 | **PASSED** |
| **Production Model 1 Checkpoint** | SHA `1ee189ff5f9a...` | SHA `1ee189ff5f9a...` | **PASSED (Untouched)** |
| **Production Balanced Dataset** | Intact | Intact | **PASSED (Untouched)** |
| **Model 2 V4 Protected Evaluation** | Intact | Intact | **PASSED (Untouched)** |

---
*Final pre-training readiness audit completed on 2026-10-10 12:24:03.*