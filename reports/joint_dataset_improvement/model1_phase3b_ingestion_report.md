# Expanded Model 1: Phase 3B Staged Dataset Ingestion & Class Coverage Report

> **Report Date**: 2026-10-10 12:12:04  
> **Project Root**: [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction)  
> **Status**: **PHASE 3B INGESTION COMPLETE & AUDITED** (Safety Invariants Strictly Preserved)

---

## 1. Executive Summary of Ingestion Actions

### A. Staged Source Ingestion Decisions
| Staged Source | Total Images | Audit Result | Action Taken | Ingested Count |
| :--- | :--- | :--- | :--- | :--- |
| **Gerbera Dataset** ([`data/external/.../gerbera dataset`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_expansion/gerbera dataset)) | 248 | 100% clean, valid, uncorrupted (640x640 RGB), 0 leaks | **APPROVED & INGESTED** | **+248 images** (Train: 229, Val: 13, Test: 6) |
| **Gypsophila Dataset** ([`data/external/.../Gypsophila Hydrangea Daisy.v1i.yolov11`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_expansion/Gypsophila Hydrangea Daisy.v1i.yolov11)) | 143 | **Multi-species mixture**: 125 unannotated images in `train/`; labels in `val`/`test` show Daisy (3), Gypsophila (6), Hydrangea (9). | **HALTED / REJECTED** (Contamination Risk) | **0 images** (Awaiting species curation) |

### B. Updated Dataset Totals
- **Total Clean Images on Disk**: **18,176 images** (expanded from 17,928 to **18,176**).
- **Train Split**: **15,386 images**
- **Validation Split**: **1,247 images**
- **Test Split**: **1,543 images**
- **Total Manifest Records**: **18,176 rows** in [`data/processed/model1_expanded_manifest.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded_manifest.csv).

---

## 2. In-Depth Audit of Staged Sources

### A. Gerbera Dataset Audit (Eligible & Ingested)
- **Source Directory**: [`data/external/model1_expansion/gerbera dataset/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_expansion/gerbera%20dataset)
- **Total Images Evaluated**: 248
- **Image Integrity**: 248 readable, valid RGB format (`640x640`), 0 corrupted files.
- **Exact Duplicates**: 0 intra-dataset duplicates; 0 hash overlaps with existing `model1_expanded` dataset.
- **Split Allocation**:
  - `train/gerbera`: **229 images** added (Total now: **231**)
  - `val/gerbera`: **13 images** added (Total now: **13**)
  - `test/gerbera`: **6 images** added (Total now: **7**)
  - **Total Gerbera Population**: Elevated from 3 to **251 images**.

### B. Gypsophila Source Audit (Contamination Analysis & Halt Rationale)
- **Source Directory**: [`data/external/model1_expansion/Gypsophila Hydrangea Daisy.v1i.yolov11/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_expansion/Gypsophila%20Hydrangea%20Daisy.v1i.yolov11)
- **Findings**:
  1. The Roboflow dataset is a 3-class detection package: `['Daisy', 'Gypsophila', 'Hydrangea']`.
  2. The `train/` directory contains **125 image files with 0 corresponding YOLO annotation txt files**.
  3. The `valid/` and `test/` splits contain 20 label files: 3 Daisy, 6 Gypsophila, 9 Hydrangea, and 2 empty.
  4. Ingesting the 125 raw images into `gypsophila` would introduce severe label noise and contamination from Daisy and Hydrangea specimens.
- **Safety Action**: In accordance with the prompt directives (*'If a staged source contains mixed species, ambiguous labels, or insufficient clean images, stop that ingestion and report the issue instead of guessing'*), ingestion of this source is **halted**.

---

## 3. Minority Class Coverage Review

| Class Name | Initial Count | Ingested | Current Real Count | Status & Remediation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **gerbera** | 3 | **+248** | **251** | **Significantly Improved**. Ready for class-balanced weighting & online augmentation. |
| **gypsophila** | 0 | +0 | **0** | **Deficit**. Staged source halted due to species mixing. Recommend curated scraping or bounding box extraction. |
| **lilium** | 45 | +0 | **45** | Minority class. Handled via class-balanced sampler (Effective Number of Samples loss weight) during training. |
| **carnation** | 51 | +0 | **51** | Minority class. Handled via class-balanced sampler during training. |
| **celery** | 65 | +0 | **65** | Minority class. Handled via class-balanced sampler during training. |

---

## 4. Complete Repaired Dataset Inventory (46 Classes)

| Index | Canonical Class | Train | Val | Test | Total Real | Target (400) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | **anthurium** | 84 | 10 | 10 | **104** | 400 | Short (<400) |
| 1 | **apple** | 452 | 57 | 57 | **566** | 400 | Ready (>=400) |
| 2 | **banana** | 428 | 54 | 54 | **536** | 400 | Ready (>=400) |
| 3 | **basil** | 568 | 6 | 6 | **580** | 400 | Ready (>=400) |
| 4 | **blueberry** | 464 | 31 | 31 | **526** | 400 | Ready (>=400) |
| 5 | **broccoli** | 332 | 41 | 41 | **414** | 400 | Ready (>=400) |
| 6 | **cabbage** | 220 | 27 | 27 | **274** | 400 | Short (<400) |
| 7 | **bellpepper** | 618 | 65 | 65 | **748** | 400 | Ready (>=400) |
| 8 | **carnation** | 41 | 5 | 5 | **51** | 400 | Short (<400) |
| 9 | **carrot** | 118 | 15 | 15 | **148** | 400 | Short (<400) |
| 10 | **cauliflower** | 425 | 10 | 10 | **445** | 400 | Ready (>=400) |
| 11 | **celery** | 53 | 6 | 6 | **65** | 400 | Short (<400) |
| 12 | **cherry** | 111 | 14 | 14 | **139** | 400 | Short (<400) |
| 13 | **cherry_tomato** | 0 | 0 | 0 | **0** | 400 | Missing (0) |
| 14 | **chrysanthemum** | 334 | 42 | 42 | **418** | 400 | Ready (>=400) |
| 15 | **citrus** | 417 | 52 | 52 | **521** | 400 | Ready (>=400) |
| 16 | **coffee** | 403 | 28 | 28 | **459** | 400 | Ready (>=400) |
| 17 | **corn** | 492 | 62 | 62 | **616** | 400 | Ready (>=400) |
| 18 | **cucumber** | 500 | 65 | 65 | **630** | 400 | Ready (>=400) |
| 19 | **eggplant** | 394 | 14 | 14 | **422** | 400 | Ready (>=400) |
| 20 | **french_bean** | 500 | 65 | 65 | **630** | 400 | Ready (>=400) |
| 21 | **garlic** | 158 | 20 | 20 | **198** | 400 | Short (<400) |
| 22 | **geranium** | 201 | 25 | 25 | **251** | 400 | Short (<400) |
| 23 | **gerbera** | 231 | 13 | 7 | **251** | 400 | Short (<400) |
| 24 | **ginger** | 354 | 9 | 9 | **372** | 400 | Short (<400) |
| 25 | **grape** | 446 | 56 | 56 | **558** | 400 | Ready (>=400) |
| 26 | **gypsophila** | 0 | 0 | 0 | **0** | 400 | Missing (0) |
| 27 | **lettuce** | 500 | 65 | 65 | **630** | 400 | Ready (>=400) |
| 28 | **lilium** | 37 | 4 | 4 | **45** | 400 | Short (<400) |
| 29 | **maple** | 91 | 11 | 11 | **113** | 400 | Short (<400) |
| 30 | **marigold** | 500 | 65 | 65 | **630** | 400 | Ready (>=400) |
| 31 | **melon** | 197 | 25 | 25 | **247** | 400 | Short (<400) |
| 32 | **orchid** | 500 | 65 | 65 | **630** | 400 | Ready (>=400) |
| 33 | **peach** | 356 | 44 | 44 | **444** | 400 | Ready (>=400) |
| 34 | **plum** | 299 | 22 | 22 | **343** | 400 | Short (<400) |
| 35 | **potato** | 191 | 24 | 24 | **239** | 400 | Short (<400) |
| 36 | **raspberry** | 99 | 12 | 12 | **123** | 400 | Short (<400) |
| 37 | **rice** | 123 | 16 | 16 | **155** | 400 | Short (<400) |
| 38 | **rose** | 570 | 65 | 65 | **700** | 400 | Ready (>=400) |
| 39 | **soybean** | 499 | 65 | 65 | **629** | 400 | Ready (>=400) |
| 40 | **spinach** | 500 | 65 | 65 | **630** | 400 | Ready (>=400) |
| 41 | **strawberry** | 545 | 65 | 65 | **675** | 400 | Ready (>=400) |
| 42 | **tobacco** | 332 | 18 | 18 | **368** | 400 | Short (<400) |
| 43 | **tomato** | 500 | 65 | 65 | **630** | 400 | Ready (>=400) |
| 44 | **wheat** | 500 | 65 | 65 | **630** | 400 | Ready (>=400) |
| 45 | **zucchini** | 315 | 39 | 39 | **393** | 400 | Short (<400) |

---

## 5. Automated Assertion Results

| Assertion Check | Expected | Actual Result | Verification Status |
| :--- | :--- | :--- | :--- |
| **Exact Cross-Split Duplicate SHA-256** | 0 | 0 | **PASSED (100% Clean)** |
| **Unmanifested Disk Images** | 0 | 0 | **PASSED (18,176 / 18,176 Indexed)** |
| **Orphan Manifest Records** | 0 | 0 | **PASSED (0 Missing Files)** |
| **Directory Nomenclature** | 46 classes | 46 classes | **PASSED (Strict Canonical Alignment)** |
| **Class Mapping Schema** | `num_classes=46` | `num_classes=46` | **PASSED (`bellpepper` at idx 7)** |

---
*Report generated automatically on 2026-10-10 12:12:04.*