# Expanded Model 1: Revised Phase 2 Reconciliation & Migration Plan

> **Report Date**: 2026-10-10 11:54:57  
> **Project Root**: [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction)  
> **Mode**: Read-Only Audit & Reconciled Action Plan (Safety Invariants Fully Preserved)

---

## 1. Confirmed Dataset Changes & Snapshot Integrity

### A. Snapshot & Production Integrity Verification
| Safety Check / Target | Value | Status |
| :--- | :--- | :--- |
| **Phase 1 Backup Directory** | [`backups/model1_expansion_phase1_snapshot/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/backups/model1_expansion_phase1_snapshot) | 100% Intact (17,992 images) |
| **Production Model 1 Checkpoint** | [`models/model1/best_model.pth`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/best_model.pth) | Untouched (SHA: `1ee189ff5f9a...`) |
| **Production Balanced Dataset** | [`data/processed/model1_balanced/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_balanced) | 100% Intact & Untouched |
| **Model 2 v4 Evaluation Data** | [`data/processed/model2_v4/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model2_v4) | Protected & Untouched |

### B. Real Post-Manifest Changes Discovered on Disk
The active `data/processed/model1_expanded/` dataset contains **17,992 real images on disk**, whereas the older manifest recorded **15,566 rows**.
An in-depth analysis of file timestamps, paths, and content reveals two distinct groups of discrepancies:

1. **Folder Nomenclature Desynchronization (1,131 files)**:
   - `train/bell_pepper` contains 631 images whose manifest rows expected `train/capsicum/...`.
   - `train/bean` contains 500 images whose manifest rows expected `train/french_bean/...`.
   - `train/New folder` is an empty directory artifact with 0 files.

2. **Legitimate Post-Manifest User Additions (2,297 images across 14 crops)**:
   These are valid, newly added real images placed directly into crop folders after the previous manifest was generated. They are **not corrupt or invalid**; they simply require manifest re-indexing:

| Crop / Class Folder | Split | Additional Images | Ingestion Source / Type |
| :--- | :--- | :--- | :--- |
| `basil` | `train` | **+517 images** | Direct disk ingestion (Valid real images) |
| `bell_pepper` | `train` | **+131 images** | Direct disk ingestion (Valid real images) |
| `blueberry` | `train` | **+252 images** | Direct disk ingestion (Valid real images) |
| `cauliflower` | `train` | **+341 images** | Direct disk ingestion (Valid real images) |
| `coffee` | `train` | **+176 images** | Direct disk ingestion (Valid real images) |
| `eggplant` | `train` | **+299 images** | Direct disk ingestion (Valid real images) |
| `ginger` | `train` | **+281 images** | Direct disk ingestion (Valid real images) |
| `plum` | `train` | **+128 images** | Direct disk ingestion (Valid real images) |
| `rose` | `train` | **+70 images** | Direct disk ingestion (Valid real images) |
| `strawberry` | `train` | **+48 images** | Direct disk ingestion (Valid real images) |
| `tobacco` | `train` | **+190 images** | Direct disk ingestion (Valid real images) |
| **Total Real Additions** | | **+2433 images** | Retained & Indexed for Training |

---

## 2. Canonical Naming & Cross-System Mapping Architecture

### A. Adoption of `bellpepper` as Canonical Name
Per the project requirements, **`bellpepper`** is designated as the authoritative public and canonical crop name (without spaces, without underscores, replacing `capsicum` and `bell_pepper`).

### B. Codebase Occurrence Audit for Naming Terms
| Term | File Occurrences | Key Locations Identified | Action Required |
| :--- | :--- | :--- | :--- |
| `capsicum` | **35 files** (102 occurrences) | `01_audit_all_sources.py`, `02_build_model1_39.py`, `build_and_evaluate_external_pipeline.py`, `build_complete_v4_knowledge.py` | Update to canonical / alias mapping |
| `bell_pepper` | **18 files** (38 occurrences) | `01_audit_all_sources.py`, `02_build_model1_39.py`, `build_and_evaluate_external_pipeline.py`, `build_complete_v4_knowledge.py` | Update to canonical / alias mapping |
| `bellpepper` | **1 files** (1 occurrences) | `02_build_model1_39.py` | Update to canonical / alias mapping |
| `french_bean` | **26 files** (69 occurrences) | `build_and_evaluate_external_pipeline.py`, `build_final_model1.py`, `build_model1_balanced.py`, `build_model1_expanded_dataset.py` | Update to canonical / alias mapping |
| `cherry_tomato` | **26 files** (69 occurrences) | `build_and_evaluate_external_pipeline.py`, `build_final_model1.py`, `build_model1_balanced.py`, `build_model1_expanded_dataset.py` | Update to canonical / alias mapping |

### C. Semantic Distinctions & Taxonomy Clarifications
1. **`bellpepper` vs `capsicum` vs `bell_pepper`**:
   - **Target Canonical**: `bellpepper`
   - **Disk Folders**: Normalize all `train/bell_pepper`, `val/capsicum`, and `test/capsicum` to `bellpepper`.
   - **Compatibility Layer**: Add aliases `{'capsicum': 'bellpepper', 'bell_pepper': 'bellpepper'}` to ensure legacy inference calls succeed seamlessly.
2. **`french_bean` vs `bean`**:
   - **Target Canonical**: `french_bean`
   - **Disk Folders**: Normalize `train/bean`, `val/french_bean`, and `test/french_bean` to `french_bean`.
   - **Alias**: `{'bean': 'french_bean'}`.
3. **`tomato` vs `cherry_tomato`**:
   - In Model 1 (Crop Classification), both standard tomato and cherry tomato foliage share botanical and visual traits. In the 46-class expanded taxonomy, `cherry_tomato` is mapped as an alias to `tomato`.

### D. Checkpoint Compatibility Analysis
- **Production Model 1 (`models/model1/best_model.pth`)**: 39-class model trained on `model1_balanced`. Unaffected; preserved as baseline production model.
- **EXP-0 Checkpoint (`models/model1_expanded/best_model.pth`)**: 46-class prototype checkpoint. Index 7 was mapped to `capsicum`. When training the next expanded iteration (**EXP-1**), updating the class mapping from `capsicum` to `bellpepper` at index 7 maintains identical head dimensionality (`num_classes=46`) while updating string keys in [`model1_expanded_class_mapping.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded_class_mapping.json).
- **Model 2 Routing**: Model 2 classifier v4 uses `bell_pepper` as crop key. The intent router and inference adapter map input string `bellpepper` -> `bell_pepper` for Model 2 sub-classifier routing.

---

## 3. Reassessed Class-by-Class Inventory (46 Classes)

| # | Canonical Class | Train | Val | Test | Total Real | Target (400) | Leakage Detected | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | **anthurium** | 84 | 10 | 10 | **104** | 400 | None (Clean) | Short (<400) |
| 1 | **apple** | 452 | 57 | 57 | **566** | 400 | None (Clean) | Ready (>=400) |
| 2 | **banana** | 428 | 54 | 54 | **536** | 400 | None (Clean) | Ready (>=400) |
| 3 | **basil** | 568 | 6 | 6 | **580** | 400 | None (Clean) | Ready (>=400) |
| 4 | **bellpepper** | 631 | 65 | 65 | **761** | 400 | Train-Test: 7, Train-Val: 6 | Ready (>=400) |
| 5 | **blueberry** | 504 | 31 | 31 | **566** | 400 | Train-Test: 20, Train-Val: 20 | Ready (>=400) |
| 6 | **broccoli** | 332 | 41 | 41 | **414** | 400 | None (Clean) | Ready (>=400) |
| 7 | **cabbage** | 220 | 27 | 27 | **274** | 400 | None (Clean) | Short (<400) |
| 8 | **carnation** | 41 | 5 | 5 | **51** | 400 | None (Clean) | Short (<400) |
| 9 | **carrot** | 118 | 15 | 15 | **148** | 400 | None (Clean) | Short (<400) |
| 10 | **cauliflower** | 425 | 10 | 10 | **445** | 400 | None (Clean) | Ready (>=400) |
| 11 | **celery** | 53 | 6 | 6 | **65** | 400 | None (Clean) | Short (<400) |
| 12 | **cherry** | 111 | 14 | 14 | **139** | 400 | None (Clean) | Short (<400) |
| 13 | **cherry_tomato** | 0 | 0 | 0 | **0** | 400 | None (Clean) | Missing (0) |
| 14 | **chrysanthemum** | 334 | 42 | 42 | **418** | 400 | None (Clean) | Ready (>=400) |
| 15 | **citrus** | 417 | 52 | 52 | **521** | 400 | None (Clean) | Ready (>=400) |
| 16 | **coffee** | 403 | 28 | 28 | **459** | 400 | None (Clean) | Ready (>=400) |
| 17 | **corn** | 492 | 62 | 62 | **616** | 400 | None (Clean) | Ready (>=400) |
| 18 | **cucumber** | 500 | 65 | 65 | **630** | 400 | None (Clean) | Ready (>=400) |
| 19 | **eggplant** | 407 | 14 | 14 | **435** | 400 | Train-Test: 5, Train-Val: 8 | Ready (>=400) |
| 20 | **french_bean** | 500 | 65 | 65 | **630** | 400 | None (Clean) | Ready (>=400) |
| 21 | **garlic** | 158 | 20 | 20 | **198** | 400 | None (Clean) | Short (<400) |
| 22 | **geranium** | 201 | 25 | 25 | **251** | 400 | None (Clean) | Short (<400) |
| 23 | **gerbera** | 2 | 0 | 1 | **3** | 400 | None (Clean) | Short (<400) |
| 24 | **ginger** | 354 | 9 | 9 | **372** | 400 | None (Clean) | Short (<400) |
| 25 | **grape** | 446 | 56 | 56 | **558** | 400 | None (Clean) | Ready (>=400) |
| 26 | **gypsophila** | 0 | 0 | 0 | **0** | 400 | None (Clean) | Missing (0) |
| 27 | **lettuce** | 500 | 65 | 65 | **630** | 400 | None (Clean) | Ready (>=400) |
| 28 | **lilium** | 37 | 4 | 4 | **45** | 400 | None (Clean) | Short (<400) |
| 29 | **maple** | 91 | 11 | 11 | **113** | 400 | None (Clean) | Short (<400) |
| 30 | **marigold** | 500 | 65 | 65 | **630** | 400 | None (Clean) | Ready (>=400) |
| 31 | **melon** | 197 | 25 | 25 | **247** | 400 | None (Clean) | Short (<400) |
| 32 | **orchid** | 500 | 65 | 65 | **630** | 400 | None (Clean) | Ready (>=400) |
| 33 | **peach** | 356 | 44 | 44 | **444** | 400 | None (Clean) | Ready (>=400) |
| 34 | **plum** | 299 | 22 | 22 | **343** | 400 | None (Clean) | Short (<400) |
| 35 | **potato** | 191 | 24 | 24 | **239** | 400 | None (Clean) | Short (<400) |
| 36 | **raspberry** | 99 | 12 | 12 | **123** | 400 | None (Clean) | Short (<400) |
| 37 | **rice** | 123 | 16 | 16 | **155** | 400 | None (Clean) | Short (<400) |
| 38 | **rose** | 570 | 65 | 65 | **700** | 400 | None (Clean) | Ready (>=400) |
| 39 | **soybean** | 499 | 65 | 65 | **629** | 400 | None (Clean) | Ready (>=400) |
| 40 | **spinach** | 500 | 65 | 65 | **630** | 400 | None (Clean) | Ready (>=400) |
| 41 | **strawberry** | 548 | 65 | 65 | **678** | 400 | Train-Test: 2, Train-Val: 1 | Ready (>=400) |
| 42 | **tobacco** | 332 | 18 | 18 | **368** | 400 | None (Clean) | Short (<400) |
| 43 | **tomato** | 500 | 65 | 65 | **630** | 400 | None (Clean) | Ready (>=400) |
| 44 | **wheat** | 500 | 65 | 65 | **630** | 400 | None (Clean) | Ready (>=400) |
| 45 | **zucchini** | 315 | 39 | 39 | **393** | 400 | None (Clean) | Short (<400) |

---

## 4. Reassessed Leakage & Duplicate Findings

### A. Exact Train-Test Leakage Confirmed (34 instances)
> [!CAUTION]
> These 34 images in `train/` share identical SHA-256 hashes with images in the immutable `test/` split. They cause data leakage and must be deleted from `train/` prior to retraining.

| # | Canonical Class | SHA-256 Prefix | Train Path (To Remove) | Test Path (Preserved) |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `strawberry` | `0fb95aebbdb0` | [`0fb95aebbd_strawberry_anthracnose_google_0007.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/strawberry/0fb95aebbd_strawberry_anthracnose_google_0007.jpg) | [`strawberry_0fb95aebbd_strawberry_fruit_diseased_010361.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/strawberry/strawberry_0fb95aebbd_strawberry_fruit_diseased_010361.jpg) |
| 2 | `bellpepper` | `10f9e56731bf` | [`ps_bell_pepper_blossom_end_rot_Bing_0090.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/ps_bell_pepper_blossom_end_rot_Bing_0090.jpg) | [`capsicum_10f9e56731_capsicum_fruit_diseased_006621.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/capsicum/capsicum_10f9e56731_capsicum_fruit_diseased_006621.jpg) |
| 3 | `blueberry` | `1d0bb28145c4` | [`1d0bb28145_blueberry_anthracnose_Bing_0017.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/1d0bb28145_blueberry_anthracnose_Bing_0017.jpg) | [`blueberry_1d0bb28145_blueberry_fruit_diseased_014201.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_1d0bb28145_blueberry_fruit_diseased_014201.jpg) |
| 4 | `blueberry` | `1de5f8467c54` | [`1de5f8467c_blueberry_anthracnose_Bing_0100.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/1de5f8467c_blueberry_anthracnose_Bing_0100.jpg) | [`blueberry_1de5f8467c_blueberry_fruit_diseased_014151.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_1de5f8467c_blueberry_fruit_diseased_014151.jpg) |
| 5 | `blueberry` | `26b5b9c37028` | [`26b5b9c370_blueberry_mummy_berry_Bing_0281.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/26b5b9c370_blueberry_mummy_berry_Bing_0281.jpg) | [`blueberry_26b5b9c370_blueberry_fruit_diseased_014368.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_26b5b9c370_blueberry_fruit_diseased_014368.jpg) |
| 6 | `blueberry` | `28b29620f876` | [`28b29620f8_blueberry_anthracnose_Bing_0053.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/28b29620f8_blueberry_anthracnose_Bing_0053.jpg) | [`blueberry_28b29620f8_blueberry_fruit_diseased_014263.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_28b29620f8_blueberry_fruit_diseased_014263.jpg) |
| 7 | `blueberry` | `2f45b9119ada` | [`2f45b9119a_blueberry_rust_google_0004.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/2f45b9119a_blueberry_rust_google_0004.jpg) | [`blueberry_2f45b9119a_blueberry_leaves_diseased_014128.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_2f45b9119a_blueberry_leaves_diseased_014128.jpg) |
| 8 | `eggplant` | `4193f71f692b` | [`4193f71f69_eggplant_phomopsis_fruit_rot_Google_0083.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/4193f71f69_eggplant_phomopsis_fruit_rot_Google_0083.jpg) | [`eggplant_4193f71f69_4193f71f69_eggplant_phomopsis_fruit_rot_Google_0083.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_4193f71f69_4193f71f69_eggplant_phomopsis_fruit_rot_Google_0083.jpg) |
| 9 | `blueberry` | `4ae342fb3414` | [`4ae342fb34_blueberry_scorch_Google_0035.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/4ae342fb34_blueberry_scorch_Google_0035.jpg) | [`blueberry_4ae342fb34_blueberry_leaves_diseased_014140.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_4ae342fb34_blueberry_leaves_diseased_014140.jpg) |
| 10 | `eggplant` | `4c3ba322dbcf` | [`4c3ba322db_eggplant_phomopsis_fruit_rot_Bing_0057.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/4c3ba322db_eggplant_phomopsis_fruit_rot_Bing_0057.jpg) | [`eggplant_4c3ba322db_4c3ba322db_eggplant_phomopsis_fruit_rot_Bing_0057.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_4c3ba322db_4c3ba322db_eggplant_phomopsis_fruit_rot_Bing_0057.jpg) |
| 11 | `eggplant` | `559613c85f6a` | [`559613c85f_eggplant_phomopsis_fruit_rot_Bing_0004.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/559613c85f_eggplant_phomopsis_fruit_rot_Bing_0004.jpg) | [`eggplant_559613c85f_559613c85f_eggplant_phomopsis_fruit_rot_Bing_0004.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_559613c85f_559613c85f_eggplant_phomopsis_fruit_rot_Bing_0004.jpg) |
| 12 | `blueberry` | `57767fb5e648` | [`ps_blueberry_botrytis_blight_Bing_0137.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_botrytis_blight_Bing_0137.jpg) | [`blueberry_57767fb5e6_blueberry_fruit_diseased_014240.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_57767fb5e6_blueberry_fruit_diseased_014240.jpg) |
| 13 | `blueberry` | `608857116e94` | [`608857116e_blueberry_anthracnose_Bing_0003.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/608857116e_blueberry_anthracnose_Bing_0003.jpg) | [`blueberry_608857116e_blueberry_fruit_diseased_014346.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_608857116e_blueberry_fruit_diseased_014346.jpg) |
| 14 | `blueberry` | `6f84fdb85925` | [`6f84fdb859_blueberry_botrytis_blight_Bing_0017.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/6f84fdb859_blueberry_botrytis_blight_Bing_0017.jpg) | [`blueberry_6f84fdb859_blueberry_fruit_diseased_014345.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_6f84fdb859_blueberry_fruit_diseased_014345.jpg) |
| 15 | `blueberry` | `74ebb7397f6e` | [`ps_blueberry_botrytis_blight_Bing_0167.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_botrytis_blight_Bing_0167.jpg) | [`blueberry_74ebb7397f_blueberry_fruit_diseased_014388.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_74ebb7397f_blueberry_fruit_diseased_014388.jpg) |
| 16 | `bellpepper` | `74fd23e6374a` | [`74fd23e637_bell_pepper_blossom_end_rot_Bing_0031.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/74fd23e637_bell_pepper_blossom_end_rot_Bing_0031.jpg) | [`capsicum_74fd23e637_capsicum_fruit_diseased_007422.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/capsicum/capsicum_74fd23e637_capsicum_fruit_diseased_007422.jpg) |
| 17 | `blueberry` | `75774aa604b1` | [`75774aa604_blueberry_anthracnose_Bing_0079.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/75774aa604_blueberry_anthracnose_Bing_0079.jpg) | [`blueberry_75774aa604_blueberry_fruit_diseased_014383.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_75774aa604_blueberry_fruit_diseased_014383.jpg) |
| 18 | `blueberry` | `7e98a077f0c7` | [`7e98a077f0_blueberry_botrytis_blight_Google_0039.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/7e98a077f0_blueberry_botrytis_blight_Google_0039.jpg) | [`blueberry_7e98a077f0_blueberry_fruit_diseased_014232.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_7e98a077f0_blueberry_fruit_diseased_014232.jpg) |
| 19 | `bellpepper` | `83657f2ca24b` | [`83657f2ca2_bell_pepper_blossom_end_rot_Bing_0009.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/83657f2ca2_bell_pepper_blossom_end_rot_Bing_0009.jpg) | [`capsicum_83657f2ca2_capsicum_fruit_diseased_006793.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/capsicum/capsicum_83657f2ca2_capsicum_fruit_diseased_006793.jpg) |
| 20 | `eggplant` | `8cd629f0d242` | [`8cd629f0d2_eggplant_phytophthora_blight_Bing_0005.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/8cd629f0d2_eggplant_phytophthora_blight_Bing_0005.jpg) | [`eggplant_8cd629f0d2_8cd629f0d2_eggplant_phytophthora_blight_Bing_0005.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_8cd629f0d2_8cd629f0d2_eggplant_phytophthora_blight_Bing_0005.jpg) |
| 21 | `blueberry` | `91029e6b71f9` | [`ps_blueberry_scorch_Bing_0005.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_scorch_Bing_0005.jpg) | [`blueberry_91029e6b71_blueberry_leaves_diseased_014174.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_91029e6b71_blueberry_leaves_diseased_014174.jpg) |
| 22 | `bellpepper` | `9a5c5fec543a` | [`9a5c5fec54_bell_pepper_blossom_end_rot_Google_0040.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/9a5c5fec54_bell_pepper_blossom_end_rot_Google_0040.jpg) | [`capsicum_9a5c5fec54_capsicum_fruit_diseased_007388.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/capsicum/capsicum_9a5c5fec54_capsicum_fruit_diseased_007388.jpg) |
| 23 | `bellpepper` | `9be72660d356` | [`ps_bell_pepper_blossom_end_rot_Google_0396.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/ps_bell_pepper_blossom_end_rot_Google_0396.jpg) | [`capsicum_9be72660d3_capsicum_fruit_diseased_007281.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/capsicum/capsicum_9be72660d3_capsicum_fruit_diseased_007281.jpg) |
| 24 | `strawberry` | `abedd44979a0` | [`abedd44979_strawberry_anthracnose_google_0027.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/strawberry/abedd44979_strawberry_anthracnose_google_0027.jpg) | [`strawberry_abedd44979_strawberry_fruit_diseased_010402.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/strawberry/strawberry_abedd44979_strawberry_fruit_diseased_010402.jpg) |
| 25 | `bellpepper` | `b426ff3b6e16` | [`b426ff3b6e_bell_pepper_blossom_end_rot_Bing_0196.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/b426ff3b6e_bell_pepper_blossom_end_rot_Bing_0196.jpg) | [`capsicum_b426ff3b6e_capsicum_fruit_diseased_007046.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/capsicum/capsicum_b426ff3b6e_capsicum_fruit_diseased_007046.jpg) |
| 26 | `blueberry` | `c42723e2df90` | [`c42723e2df_blueberry_anthracnose_Bing_0095.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/c42723e2df_blueberry_anthracnose_Bing_0095.jpg) | [`blueberry_c42723e2df_blueberry_fruit_diseased_014215.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_c42723e2df_blueberry_fruit_diseased_014215.jpg) |
| 27 | `blueberry` | `c8922a650077` | [`ps_blueberry_botrytis_blight_Bing_0071.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_botrytis_blight_Bing_0071.jpg) | [`blueberry_c8922a6500_blueberry_fruit_diseased_014312.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_c8922a6500_blueberry_fruit_diseased_014312.jpg) |
| 28 | `bellpepper` | `cdf48d7939e8` | [`cdf48d7939_bell_pepper_blossom_end_rot_Bing_0112.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/cdf48d7939_bell_pepper_blossom_end_rot_Bing_0112.jpg) | [`capsicum_cdf48d7939_capsicum_fruit_diseased_006125.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/capsicum/capsicum_cdf48d7939_capsicum_fruit_diseased_006125.jpg) |
| 29 | `eggplant` | `ce38f2bbc5bd` | [`ce38f2bbc5_eggplant_phomopsis_fruit_rot_Bing_0009.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/ce38f2bbc5_eggplant_phomopsis_fruit_rot_Bing_0009.jpg) | [`eggplant_ce38f2bbc5_ce38f2bbc5_eggplant_phomopsis_fruit_rot_Bing_0009.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_ce38f2bbc5_ce38f2bbc5_eggplant_phomopsis_fruit_rot_Bing_0009.jpg) |
| 30 | `blueberry` | `d8ca8bffdaf9` | [`ps_blueberry_rust_google_0014.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_rust_google_0014.jpg) | [`blueberry_d8ca8bffda_blueberry_leaves_diseased_014143.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_d8ca8bffda_blueberry_leaves_diseased_014143.jpg) |
| 31 | `blueberry` | `dff8adc302cf` | [`dff8adc302_blueberry_anthracnose_Bing_0018.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/dff8adc302_blueberry_anthracnose_Bing_0018.jpg) | [`blueberry_dff8adc302_blueberry_fruit_diseased_014421.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_dff8adc302_blueberry_fruit_diseased_014421.jpg) |
| 32 | `blueberry` | `e0db4e059e85` | [`ps_blueberry_mummy_berry_Google_0083.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_mummy_berry_Google_0083.jpg) | [`blueberry_e0db4e059e_blueberry_fruit_diseased_014349.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_e0db4e059e_blueberry_fruit_diseased_014349.jpg) |
| 33 | `blueberry` | `e85ff1350504` | [`e85ff13505_blueberry_mummy_berry_Bing_0024.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/e85ff13505_blueberry_mummy_berry_Bing_0024.jpg) | [`blueberry_e85ff13505_blueberry_fruit_diseased_014277.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_e85ff13505_blueberry_fruit_diseased_014277.jpg) |
| 34 | `blueberry` | `ec6bd77493d1` | [`ps_blueberry_botrytis_blight_Bing_0033.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_botrytis_blight_Bing_0033.jpg) | [`blueberry_ec6bd77493_blueberry_fruit_diseased_014281.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_ec6bd77493_blueberry_fruit_diseased_014281.jpg) |

### B. Exact Train-Validation Leakage Confirmed (35 instances)
> [!WARNING]
> These 35 images in `train/` share identical SHA-256 hashes with images in `val/`. They must be removed from `train/` to prevent validation overfitting.

| # | Canonical Class | SHA-256 Prefix | Train Path (To Remove) | Val Path (Preserved) |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `bellpepper` | `031cdbf09b1d` | [`031cdbf09b_bell_pepper_blossom_end_rot_Bing_0053.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/031cdbf09b_bell_pepper_blossom_end_rot_Bing_0053.jpg) | [`capsicum_031cdbf09b_capsicum_fruit_diseased_007237.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/capsicum/capsicum_031cdbf09b_capsicum_fruit_diseased_007237.jpg) |
| 2 | `blueberry` | `03b4d01df494` | [`03b4d01df4_blueberry_rust_google_0099.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/03b4d01df4_blueberry_rust_google_0099.jpg) | [`blueberry_03b4d01df4_blueberry_leaves_diseased_014427.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_03b4d01df4_blueberry_leaves_diseased_014427.jpg) |
| 3 | `blueberry` | `07d9921055b5` | [`07d9921055_blueberry_botrytis_blight_Google_0345.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/07d9921055_blueberry_botrytis_blight_Google_0345.jpg) | [`blueberry_07d9921055_blueberry_fruit_diseased_014358.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_07d9921055_blueberry_fruit_diseased_014358.jpg) |
| 4 | `eggplant` | `0d3709a57ee9` | [`0d3709a57e_eggplant_phomopsis_fruit_rot_Bing_0048.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/0d3709a57e_eggplant_phomopsis_fruit_rot_Bing_0048.jpg) | [`eggplant_0d3709a57e_0d3709a57e_eggplant_phomopsis_fruit_rot_Bing_0048.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_0d3709a57e_0d3709a57e_eggplant_phomopsis_fruit_rot_Bing_0048.jpg) |
| 5 | `bellpepper` | `1da0ce7e96d3` | [`1da0ce7e96_bell_pepper_blossom_end_rot_Bing_0036.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/1da0ce7e96_bell_pepper_blossom_end_rot_Bing_0036.jpg) | [`capsicum_1da0ce7e96_capsicum_fruit_diseased_006885.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/capsicum/capsicum_1da0ce7e96_capsicum_fruit_diseased_006885.jpg) |
| 6 | `bellpepper` | `1f019f956165` | [`ps_bell_pepper_frogeye_leaf_spot_Bing_0112.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/ps_bell_pepper_frogeye_leaf_spot_Bing_0112.jpg) | [`capsicum_1f019f9561_capsicum_leaves_diseased_007327.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/capsicum/capsicum_1f019f9561_capsicum_leaves_diseased_007327.jpg) |
| 7 | `eggplant` | `3401f25468c2` | [`ps_eggplant_phytophthora_blight_Bing_0050.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/ps_eggplant_phytophthora_blight_Bing_0050.jpg) | [`eggplant_3401f25468_ps_eggplant_phytophthora_blight_Bing_0050.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_3401f25468_ps_eggplant_phytophthora_blight_Bing_0050.jpg) |
| 8 | `blueberry` | `3a840d721545` | [`3a840d7215_blueberry_botrytis_blight_Bing_0001.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/3a840d7215_blueberry_botrytis_blight_Bing_0001.jpg) | [`blueberry_3a840d7215_blueberry_fruit_diseased_014243.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_3a840d7215_blueberry_fruit_diseased_014243.jpg) |
| 9 | `strawberry` | `417288994373` | [`4172889943_strawberry_anthracnose_7.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/strawberry/4172889943_strawberry_anthracnose_7.jpg) | [`strawberry_4172889943_strawberry_fruit_diseased_010968.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/strawberry/strawberry_4172889943_strawberry_fruit_diseased_010968.jpg) |
| 10 | `eggplant` | `495b68fb84a1` | [`495b68fb84_eggplant_phomopsis_fruit_rot_Bing_0000.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/495b68fb84_eggplant_phomopsis_fruit_rot_Bing_0000.jpg) | [`eggplant_495b68fb84_495b68fb84_eggplant_phomopsis_fruit_rot_Bing_0000.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_495b68fb84_495b68fb84_eggplant_phomopsis_fruit_rot_Bing_0000.jpg) |
| 11 | `blueberry` | `5369f5d2013a` | [`5369f5d201_blueberry_rust_google_0056.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/5369f5d201_blueberry_rust_google_0056.jpg) | [`blueberry_5369f5d201_blueberry_leaves_diseased_014271.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_5369f5d201_blueberry_leaves_diseased_014271.jpg) |
| 12 | `blueberry` | `56d1aea19296` | [`56d1aea192_blueberry_mummy_berry_Google_0055.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/56d1aea192_blueberry_mummy_berry_Google_0055.jpg) | [`blueberry_56d1aea192_blueberry_fruit_diseased_014371.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_56d1aea192_blueberry_fruit_diseased_014371.jpg) |
| 13 | `blueberry` | `571274d00d48` | [`571274d00d_blueberry_mummy_berry_Google_0038.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/571274d00d_blueberry_mummy_berry_Google_0038.jpg) | [`blueberry_571274d00d_blueberry_fruit_diseased_014237.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_571274d00d_blueberry_fruit_diseased_014237.jpg) |
| 14 | `eggplant` | `67e0b45b21c7` | [`ps_eggplant_phomopsis_fruit_rot_Google_0148.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/ps_eggplant_phomopsis_fruit_rot_Google_0148.jpg) | [`eggplant_67e0b45b21_ps_eggplant_phomopsis_fruit_rot_Google_0148.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_67e0b45b21_ps_eggplant_phomopsis_fruit_rot_Google_0148.jpg) |
| 15 | `blueberry` | `6b748c998306` | [`6b748c9983_blueberry_mummy_berry_Bing_0131.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/6b748c9983_blueberry_mummy_berry_Bing_0131.jpg) | [`blueberry_6b748c9983_blueberry_fruit_diseased_014293.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_6b748c9983_blueberry_fruit_diseased_014293.jpg) |
| 16 | `eggplant` | `7230cf37177e` | [`ps_eggplant_phytophthora_blight_Bing_0021.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/ps_eggplant_phytophthora_blight_Bing_0021.jpg) | [`eggplant_7230cf3717_ps_eggplant_phytophthora_blight_Bing_0021.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_7230cf3717_ps_eggplant_phytophthora_blight_Bing_0021.jpg) |
| 17 | `blueberry` | `77bf8c8a5eb6` | [`77bf8c8a5e_blueberry_scorch_Bing_0062.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/77bf8c8a5e_blueberry_scorch_Bing_0062.jpg) | [`blueberry_77bf8c8a5e_blueberry_leaves_diseased_014127.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_77bf8c8a5e_blueberry_leaves_diseased_014127.jpg) |
| 18 | `eggplant` | `88e93f57f19b` | [`88e93f57f1_eggplant_phytophthora_blight_Bing_0009.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/88e93f57f1_eggplant_phytophthora_blight_Bing_0009.jpg) | [`eggplant_88e93f57f1_88e93f57f1_eggplant_phytophthora_blight_Bing_0009.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_88e93f57f1_88e93f57f1_eggplant_phytophthora_blight_Bing_0009.jpg) |
| 19 | `eggplant` | `8950f56c8ee3` | [`8950f56c8e_eggplant_phytophthora_blight_Bing_0039.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/8950f56c8e_eggplant_phytophthora_blight_Bing_0039.jpg) | [`eggplant_8950f56c8e_8950f56c8e_eggplant_phytophthora_blight_Bing_0039.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_8950f56c8e_8950f56c8e_eggplant_phytophthora_blight_Bing_0039.jpg) |
| 20 | `blueberry` | `8dfa865125d7` | [`ps_blueberry_mummy_berry_Bing_0325.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_mummy_berry_Bing_0325.jpg) | [`blueberry_8dfa865125_blueberry_fruit_diseased_014168.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_8dfa865125_blueberry_fruit_diseased_014168.jpg) |
| 21 | `blueberry` | `9eaba60439f8` | [`ps_blueberry_mummy_berry_Bing_0161.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_mummy_berry_Bing_0161.jpg) | [`blueberry_9eaba60439_blueberry_fruit_diseased_014222.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_9eaba60439_blueberry_fruit_diseased_014222.jpg) |
| 22 | `eggplant` | `aa07139033de` | [`aa07139033_eggplant_phomopsis_fruit_rot_Bing_0054.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/eggplant/aa07139033_eggplant_phomopsis_fruit_rot_Bing_0054.jpg) | [`eggplant_aa07139033_aa07139033_eggplant_phomopsis_fruit_rot_Bing_0054.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_aa07139033_aa07139033_eggplant_phomopsis_fruit_rot_Bing_0054.jpg) |
| 23 | `blueberry` | `b109f8d3a89b` | [`b109f8d3a8_blueberry_scorch_Bing_0291.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/b109f8d3a8_blueberry_scorch_Bing_0291.jpg) | [`blueberry_b109f8d3a8_blueberry_leaves_diseased_014351.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_b109f8d3a8_blueberry_leaves_diseased_014351.jpg) |
| 24 | `blueberry` | `b8548f58c39d` | [`ps_blueberry_mummy_berry_Bing_0062.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_mummy_berry_Bing_0062.jpg) | [`blueberry_b8548f58c3_blueberry_fruit_diseased_014375.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_b8548f58c3_blueberry_fruit_diseased_014375.jpg) |
| 25 | `blueberry` | `bb30f5ab6ddb` | [`bb30f5ab6d_blueberry_rust_google_0074.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/bb30f5ab6d_blueberry_rust_google_0074.jpg) | [`blueberry_bb30f5ab6d_blueberry_leaves_diseased_014194.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_bb30f5ab6d_blueberry_leaves_diseased_014194.jpg) |
| 26 | `blueberry` | `c19ffcd9e14a` | [`ps_blueberry_mummy_berry_Google_0020.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_mummy_berry_Google_0020.jpg) | [`blueberry_c19ffcd9e1_blueberry_fruit_diseased_014262.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_c19ffcd9e1_blueberry_fruit_diseased_014262.jpg) |
| 27 | `blueberry` | `ca12db4ea9c9` | [`ps_blueberry_mummy_berry_Bing_0067.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/ps_blueberry_mummy_berry_Bing_0067.jpg) | [`blueberry_ca12db4ea9_blueberry_fruit_diseased_014363.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_ca12db4ea9_blueberry_fruit_diseased_014363.jpg) |
| 28 | `blueberry` | `d3c5effb68f7` | [`d3c5effb68_blueberry_scorch_Bing_0043.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/d3c5effb68_blueberry_scorch_Bing_0043.jpg) | [`blueberry_d3c5effb68_blueberry_leaves_diseased_014374.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_d3c5effb68_blueberry_leaves_diseased_014374.jpg) |
| 29 | `bellpepper` | `d4c68ce801a1` | [`d4c68ce801_bell_pepper_blossom_end_rot_Bing_0195.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/d4c68ce801_bell_pepper_blossom_end_rot_Bing_0195.jpg) | [`capsicum_d4c68ce801_capsicum_fruit_diseased_007184.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/capsicum/capsicum_d4c68ce801_capsicum_fruit_diseased_007184.jpg) |
| 30 | `blueberry` | `defc6dd86ce6` | [`defc6dd86c_blueberry_mummy_berry_Bing_0174.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/defc6dd86c_blueberry_mummy_berry_Bing_0174.jpg) | [`blueberry_defc6dd86c_blueberry_fruit_diseased_014156.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_defc6dd86c_blueberry_fruit_diseased_014156.jpg) |
| 31 | `blueberry` | `f2591684b32d` | [`f2591684b3_blueberry_anthracnose_Bing_0002.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/f2591684b3_blueberry_anthracnose_Bing_0002.jpg) | [`blueberry_f2591684b3_blueberry_fruit_diseased_014340.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_f2591684b3_blueberry_fruit_diseased_014340.jpg) |
| 32 | `blueberry` | `f3210c80ed93` | [`f3210c80ed_blueberry_anthracnose_Bing_0145.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/f3210c80ed_blueberry_anthracnose_Bing_0145.jpg) | [`blueberry_f3210c80ed_blueberry_fruit_diseased_014198.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_f3210c80ed_blueberry_fruit_diseased_014198.jpg) |
| 33 | `blueberry` | `f591ce95444e` | [`f591ce9544_blueberry_anthracnose_Bing_0004.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/blueberry/f591ce9544_blueberry_anthracnose_Bing_0004.jpg) | [`blueberry_f591ce9544_blueberry_fruit_diseased_014429.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_f591ce9544_blueberry_fruit_diseased_014429.jpg) |
| 34 | `bellpepper` | `fb19e7e1d804` | [`fb19e7e1d8_bell_pepper_blossom_end_rot_Bing_0087.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/fb19e7e1d8_bell_pepper_blossom_end_rot_Bing_0087.jpg) | [`capsicum_fb19e7e1d8_capsicum_fruit_diseased_007061.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/capsicum/capsicum_fb19e7e1d8_capsicum_fruit_diseased_007061.jpg) |
| 35 | `bellpepper` | `fee212dea7aa` | [`fee212dea7_bell_pepper_blossom_end_rot_Bing_0012.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bell_pepper/fee212dea7_bell_pepper_blossom_end_rot_Bing_0012.jpg) | [`capsicum_fee212dea7_capsicum_fruit_diseased_007076.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/capsicum/capsicum_fee212dea7_capsicum_fruit_diseased_007076.jpg) |

### C. Near-Duplicate Cross-Split Pairs (139 pairs)
The 139 pairs with perceptual hash distance $\le 4$ across train and validation/test splits represent high-overlap photo sequences. These will be monitored during validation loss tracking.

---

## 5. Complete Proposed Migration & Action Plan

### A. Directory Normalization Actions (Phase 3)
1. **Rename Bell Pepper Folders to `bellpepper`**:
   - `data/processed/model1_expanded/train/bell_pepper` $\rightarrow$ `data/processed/model1_expanded/train/bellpepper`
   - `data/processed/model1_expanded/val/capsicum` $\rightarrow$ `data/processed/model1_expanded/val/bellpepper`
   - `data/processed/model1_expanded/test/capsicum` $\rightarrow$ `data/processed/model1_expanded/test/bellpepper`
2. **Rename Bean Folders to `french_bean`**:
   - `data/processed/model1_expanded/train/bean` $\rightarrow$ `data/processed/model1_expanded/train/french_bean`
3. **Remove Stale Artifact Folder**:
   - Delete `data/processed/model1_expanded/train/New folder`

### B. Leakage Elimination Actions (Phase 3)
- Delete the **34 train-test duplicate images** from `data/processed/model1_expanded/train/`.
- Delete the **35 train-val duplicate images** from `data/processed/model1_expanded/train/`.
- Retain all `val/` and `test/` images 100% untouched to preserve evaluation validity.

### C. External Staged Data Ingestion Actions (Phase 3)
1. **Gerbera (248 images)** from [`data/external/model1_expansion/gerbera dataset/`](file:///{(PROJECT_ROOT / 'data/external/model1_expansion/gerbera dataset').as_posix()}):
   - Distribute 198 to `train/gerbera`, 25 to `val/gerbera`, 25 to `test/gerbera`.
2. **Gypsophila (143 images)** from [`data/external/model1_expansion/Gypsophila Hydrangea Daisy.v1i.yolov11/`](file:///{(PROJECT_ROOT / 'data/external/model1_expansion/Gypsophila Hydrangea Daisy.v1i.yolov11').as_posix()}):
   - Distribute 115 to `train/gypsophila`, 14 to `val/gypsophila`, 14 to `test/gypsophila`.
3. **Extracted Eggplant (3,407 images)** in [`data/processed/eggplant/`](file:///{(PROJECT_ROOT / 'data/processed/eggplant').as_posix()}):
   - Ingest high-quality foliage images into `train/eggplant` to expand variety.

### D. Manifest & Code Updates (Phase 4)
1. **Rebuild Manifest**: Re-index the entire normalized `model1_expanded` dataset into `data/processed/model1_expanded_manifest.csv` with updated SHA-256 hashes, splits, and canonical `bellpepper` labels.
2. **Update Class Mapping Schema**: Update `data/processed/model1_expanded_class_mapping.json`:
   - `class_to_idx`: `'bellpepper': 7`
   - `aliases`: `{'capsicum': 'bellpepper', 'bell_pepper': 'bellpepper', 'bean': 'french_bean', 'cherry_tomato': 'tomato'}`
3. **Update Training Script**: Update `scripts/train_model1_expanded_exp1.py` with the updated class mapping and class-balanced sampler for minority crops.

---

## 6. Pre-Retraining Verification Checklist

- [ ] 0 cross-split exact duplicate hashes between train and val/test.
- [ ] All folder names in `train/`, `val/`, `test/` match the 46 canonical class names exactly (`bellpepper`, `french_bean`, etc.).
- [ ] All active images are indexed in `model1_expanded_manifest.csv` with zero orphan records.
- [ ] Baseline production Model 1 checkpoint (`models/model1/best_model.pth`) and dataset (`data/processed/model1_balanced/`) verified unchanged.

---
*Revised report compiled on 2026-10-10 11:54:57.*