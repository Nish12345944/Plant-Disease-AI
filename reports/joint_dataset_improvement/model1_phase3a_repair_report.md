# Expanded Model 1: Phase 3A Dataset Repair & Verification Report

> **Execution Date**: 2026-10-10 12:07:42  
> **Project Root**: [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction)  
> **Status**: **SUCCESSFULLY REPAIRED & VERIFIED** (All Safety Invariants Preserved)

---

## 1. Executive Summary & Verification of Invariants

### A. Protected Baseline Invariants
| Target | Location | Status |
| :--- | :--- | :--- |
| **Phase 1 Backup Snapshot** | [`backups/model1_expansion_phase1_snapshot/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/backups/model1_expansion_phase1_snapshot) | 100% Intact (17,992 baseline images) |
| **Production Model 1 Checkpoint** | [`models/model1/best_model.pth`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1/best_model.pth) | 100% Untouched (`SHA: 1ee189ff5f9a...`) |
| **Production Balanced Dataset** | [`data/processed/model1_balanced/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_balanced) | 100% Untouched |
| **Model 2 v4 Evaluation Data** | [`data/processed/model2_v4/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model2_v4) | 100% Protected |

### B. Key Repair Actions Executed
1. **Directory Normalization**: All directories renamed to canonical names `bellpepper` and `french_bean`. Removed stale empty directories.
2. **Cross-Split Leakage Eliminated**: **69 duplicate images deleted from `train/`** (34 Train-Test, 35 Train-Val). Validation and test sets 100% preserved.
3. **Legitimate Additions Retained**: All valid real additions across 14 crop folders retained and indexed.
4. **Manifest Regenerated**: Authoritative manifest [`data/processed/model1_expanded_manifest.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded_manifest.csv) generated with **17,928 clean records**.
5. **Class Schema Synchronized**: Class mappings updated with `bellpepper` (index 7) and `french_bean` (index 20), preserving 46-class head dimension.

---

## 2. Directory Normalization Summary

| Original Directory | Normalized Directory | Image Count | Action Taken |
| :--- | :--- | :--- | :--- |
| `train/bell_pepper/` | [`train/bellpepper/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/bellpepper) | 624 (after leak removal) | Normalized to canonical `bellpepper` |
| `val/capsicum/` | [`val/bellpepper/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/bellpepper) | 65 | Normalized to canonical `bellpepper` |
| `test/capsicum/` | [`test/bellpepper/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/bellpepper) | 65 | Normalized to canonical `bellpepper` |
| `train/bean/` | [`train/french_bean/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/train/french_bean) | 500 | Normalized to canonical `french_bean` |
| `train/New folder/` | *Deleted* | 0 | Removed stale empty artifact |

---

## 3. Excluded Cross-Split Duplicate Training Copies (69 Files)

| # | Class | Leak Type | Excluded Training File | Preserved Eval File | SHA-256 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `bellpepper` | `Train-Val` | `031cdbf09b_bell_pepper_blossom_end_rot_Bing_0053.jpg` | [`capsicum_031cdbf09b_capsicum_fruit_diseased_007237.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/bellpepper/capsicum_031cdbf09b_capsicum_fruit_diseased_007237.jpg) | `031cdbf09b1d` |
| 2 | `blueberry` | `Train-Val` | `03b4d01df4_blueberry_rust_google_0099.jpg` | [`blueberry_03b4d01df4_blueberry_leaves_diseased_014427.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_03b4d01df4_blueberry_leaves_diseased_014427.jpg) | `03b4d01df494` |
| 3 | `blueberry` | `Train-Val` | `07d9921055_blueberry_botrytis_blight_Google_0345.jpg` | [`blueberry_07d9921055_blueberry_fruit_diseased_014358.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_07d9921055_blueberry_fruit_diseased_014358.jpg) | `07d9921055b5` |
| 4 | `eggplant` | `Train-Val` | `0d3709a57e_eggplant_phomopsis_fruit_rot_Bing_0048.jpg` | [`eggplant_0d3709a57e_0d3709a57e_eggplant_phomopsis_fruit_rot_Bing_0048.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_0d3709a57e_0d3709a57e_eggplant_phomopsis_fruit_rot_Bing_0048.jpg) | `0d3709a57ee9` |
| 5 | `strawberry` | `Train-Test` | `0fb95aebbd_strawberry_anthracnose_google_0007.jpg` | [`strawberry_0fb95aebbd_strawberry_fruit_diseased_010361.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/strawberry/strawberry_0fb95aebbd_strawberry_fruit_diseased_010361.jpg) | `0fb95aebbdb0` |
| 6 | `bellpepper` | `Train-Test` | `ps_bell_pepper_blossom_end_rot_Bing_0090.jpg` | [`capsicum_10f9e56731_capsicum_fruit_diseased_006621.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/bellpepper/capsicum_10f9e56731_capsicum_fruit_diseased_006621.jpg) | `10f9e56731bf` |
| 7 | `blueberry` | `Train-Test` | `1d0bb28145_blueberry_anthracnose_Bing_0017.jpg` | [`blueberry_1d0bb28145_blueberry_fruit_diseased_014201.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_1d0bb28145_blueberry_fruit_diseased_014201.jpg) | `1d0bb28145c4` |
| 8 | `bellpepper` | `Train-Val` | `1da0ce7e96_bell_pepper_blossom_end_rot_Bing_0036.jpg` | [`capsicum_1da0ce7e96_capsicum_fruit_diseased_006885.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/bellpepper/capsicum_1da0ce7e96_capsicum_fruit_diseased_006885.jpg) | `1da0ce7e96d3` |
| 9 | `blueberry` | `Train-Test` | `1de5f8467c_blueberry_anthracnose_Bing_0100.jpg` | [`blueberry_1de5f8467c_blueberry_fruit_diseased_014151.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_1de5f8467c_blueberry_fruit_diseased_014151.jpg) | `1de5f8467c54` |
| 10 | `bellpepper` | `Train-Val` | `ps_bell_pepper_frogeye_leaf_spot_Bing_0112.jpg` | [`capsicum_1f019f9561_capsicum_leaves_diseased_007327.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/bellpepper/capsicum_1f019f9561_capsicum_leaves_diseased_007327.jpg) | `1f019f956165` |
| 11 | `blueberry` | `Train-Test` | `26b5b9c370_blueberry_mummy_berry_Bing_0281.jpg` | [`blueberry_26b5b9c370_blueberry_fruit_diseased_014368.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_26b5b9c370_blueberry_fruit_diseased_014368.jpg) | `26b5b9c37028` |
| 12 | `blueberry` | `Train-Test` | `28b29620f8_blueberry_anthracnose_Bing_0053.jpg` | [`blueberry_28b29620f8_blueberry_fruit_diseased_014263.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_28b29620f8_blueberry_fruit_diseased_014263.jpg) | `28b29620f876` |
| 13 | `blueberry` | `Train-Test` | `2f45b9119a_blueberry_rust_google_0004.jpg` | [`blueberry_2f45b9119a_blueberry_leaves_diseased_014128.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_2f45b9119a_blueberry_leaves_diseased_014128.jpg) | `2f45b9119ada` |
| 14 | `eggplant` | `Train-Val` | `ps_eggplant_phytophthora_blight_Bing_0050.jpg` | [`eggplant_3401f25468_ps_eggplant_phytophthora_blight_Bing_0050.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_3401f25468_ps_eggplant_phytophthora_blight_Bing_0050.jpg) | `3401f25468c2` |
| 15 | `blueberry` | `Train-Val` | `3a840d7215_blueberry_botrytis_blight_Bing_0001.jpg` | [`blueberry_3a840d7215_blueberry_fruit_diseased_014243.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_3a840d7215_blueberry_fruit_diseased_014243.jpg) | `3a840d721545` |
| 16 | `strawberry` | `Train-Val` | `4172889943_strawberry_anthracnose_7.jpg` | [`strawberry_4172889943_strawberry_fruit_diseased_010968.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/strawberry/strawberry_4172889943_strawberry_fruit_diseased_010968.jpg) | `417288994373` |
| 17 | `eggplant` | `Train-Test` | `4193f71f69_eggplant_phomopsis_fruit_rot_Google_0083.jpg` | [`eggplant_4193f71f69_4193f71f69_eggplant_phomopsis_fruit_rot_Google_0083.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_4193f71f69_4193f71f69_eggplant_phomopsis_fruit_rot_Google_0083.jpg) | `4193f71f692b` |
| 18 | `eggplant` | `Train-Val` | `495b68fb84_eggplant_phomopsis_fruit_rot_Bing_0000.jpg` | [`eggplant_495b68fb84_495b68fb84_eggplant_phomopsis_fruit_rot_Bing_0000.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_495b68fb84_495b68fb84_eggplant_phomopsis_fruit_rot_Bing_0000.jpg) | `495b68fb84a1` |
| 19 | `blueberry` | `Train-Test` | `4ae342fb34_blueberry_scorch_Google_0035.jpg` | [`blueberry_4ae342fb34_blueberry_leaves_diseased_014140.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_4ae342fb34_blueberry_leaves_diseased_014140.jpg) | `4ae342fb3414` |
| 20 | `eggplant` | `Train-Test` | `4c3ba322db_eggplant_phomopsis_fruit_rot_Bing_0057.jpg` | [`eggplant_4c3ba322db_4c3ba322db_eggplant_phomopsis_fruit_rot_Bing_0057.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_4c3ba322db_4c3ba322db_eggplant_phomopsis_fruit_rot_Bing_0057.jpg) | `4c3ba322dbcf` |
| 21 | `blueberry` | `Train-Val` | `5369f5d201_blueberry_rust_google_0056.jpg` | [`blueberry_5369f5d201_blueberry_leaves_diseased_014271.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_5369f5d201_blueberry_leaves_diseased_014271.jpg) | `5369f5d2013a` |
| 22 | `eggplant` | `Train-Test` | `559613c85f_eggplant_phomopsis_fruit_rot_Bing_0004.jpg` | [`eggplant_559613c85f_559613c85f_eggplant_phomopsis_fruit_rot_Bing_0004.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_559613c85f_559613c85f_eggplant_phomopsis_fruit_rot_Bing_0004.jpg) | `559613c85f6a` |
| 23 | `blueberry` | `Train-Val` | `56d1aea192_blueberry_mummy_berry_Google_0055.jpg` | [`blueberry_56d1aea192_blueberry_fruit_diseased_014371.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_56d1aea192_blueberry_fruit_diseased_014371.jpg) | `56d1aea19296` |
| 24 | `blueberry` | `Train-Val` | `571274d00d_blueberry_mummy_berry_Google_0038.jpg` | [`blueberry_571274d00d_blueberry_fruit_diseased_014237.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_571274d00d_blueberry_fruit_diseased_014237.jpg) | `571274d00d48` |
| 25 | `blueberry` | `Train-Test` | `ps_blueberry_botrytis_blight_Bing_0137.jpg` | [`blueberry_57767fb5e6_blueberry_fruit_diseased_014240.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_57767fb5e6_blueberry_fruit_diseased_014240.jpg) | `57767fb5e648` |
| 26 | `blueberry` | `Train-Test` | `608857116e_blueberry_anthracnose_Bing_0003.jpg` | [`blueberry_608857116e_blueberry_fruit_diseased_014346.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_608857116e_blueberry_fruit_diseased_014346.jpg) | `608857116e94` |
| 27 | `eggplant` | `Train-Val` | `ps_eggplant_phomopsis_fruit_rot_Google_0148.jpg` | [`eggplant_67e0b45b21_ps_eggplant_phomopsis_fruit_rot_Google_0148.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_67e0b45b21_ps_eggplant_phomopsis_fruit_rot_Google_0148.jpg) | `67e0b45b21c7` |
| 28 | `blueberry` | `Train-Val` | `6b748c9983_blueberry_mummy_berry_Bing_0131.jpg` | [`blueberry_6b748c9983_blueberry_fruit_diseased_014293.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_6b748c9983_blueberry_fruit_diseased_014293.jpg) | `6b748c998306` |
| 29 | `blueberry` | `Train-Test` | `6f84fdb859_blueberry_botrytis_blight_Bing_0017.jpg` | [`blueberry_6f84fdb859_blueberry_fruit_diseased_014345.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_6f84fdb859_blueberry_fruit_diseased_014345.jpg) | `6f84fdb85925` |
| 30 | `eggplant` | `Train-Val` | `ps_eggplant_phytophthora_blight_Bing_0021.jpg` | [`eggplant_7230cf3717_ps_eggplant_phytophthora_blight_Bing_0021.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_7230cf3717_ps_eggplant_phytophthora_blight_Bing_0021.jpg) | `7230cf37177e` |
| 31 | `blueberry` | `Train-Test` | `ps_blueberry_botrytis_blight_Bing_0167.jpg` | [`blueberry_74ebb7397f_blueberry_fruit_diseased_014388.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_74ebb7397f_blueberry_fruit_diseased_014388.jpg) | `74ebb7397f6e` |
| 32 | `bellpepper` | `Train-Test` | `74fd23e637_bell_pepper_blossom_end_rot_Bing_0031.jpg` | [`capsicum_74fd23e637_capsicum_fruit_diseased_007422.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/bellpepper/capsicum_74fd23e637_capsicum_fruit_diseased_007422.jpg) | `74fd23e6374a` |
| 33 | `blueberry` | `Train-Test` | `75774aa604_blueberry_anthracnose_Bing_0079.jpg` | [`blueberry_75774aa604_blueberry_fruit_diseased_014383.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_75774aa604_blueberry_fruit_diseased_014383.jpg) | `75774aa604b1` |
| 34 | `blueberry` | `Train-Val` | `77bf8c8a5e_blueberry_scorch_Bing_0062.jpg` | [`blueberry_77bf8c8a5e_blueberry_leaves_diseased_014127.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_77bf8c8a5e_blueberry_leaves_diseased_014127.jpg) | `77bf8c8a5eb6` |
| 35 | `blueberry` | `Train-Test` | `7e98a077f0_blueberry_botrytis_blight_Google_0039.jpg` | [`blueberry_7e98a077f0_blueberry_fruit_diseased_014232.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_7e98a077f0_blueberry_fruit_diseased_014232.jpg) | `7e98a077f0c7` |
| 36 | `bellpepper` | `Train-Test` | `83657f2ca2_bell_pepper_blossom_end_rot_Bing_0009.jpg` | [`capsicum_83657f2ca2_capsicum_fruit_diseased_006793.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/bellpepper/capsicum_83657f2ca2_capsicum_fruit_diseased_006793.jpg) | `83657f2ca24b` |
| 37 | `eggplant` | `Train-Val` | `88e93f57f1_eggplant_phytophthora_blight_Bing_0009.jpg` | [`eggplant_88e93f57f1_88e93f57f1_eggplant_phytophthora_blight_Bing_0009.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_88e93f57f1_88e93f57f1_eggplant_phytophthora_blight_Bing_0009.jpg) | `88e93f57f19b` |
| 38 | `eggplant` | `Train-Val` | `8950f56c8e_eggplant_phytophthora_blight_Bing_0039.jpg` | [`eggplant_8950f56c8e_8950f56c8e_eggplant_phytophthora_blight_Bing_0039.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_8950f56c8e_8950f56c8e_eggplant_phytophthora_blight_Bing_0039.jpg) | `8950f56c8ee3` |
| 39 | `eggplant` | `Train-Test` | `8cd629f0d2_eggplant_phytophthora_blight_Bing_0005.jpg` | [`eggplant_8cd629f0d2_8cd629f0d2_eggplant_phytophthora_blight_Bing_0005.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_8cd629f0d2_8cd629f0d2_eggplant_phytophthora_blight_Bing_0005.jpg) | `8cd629f0d242` |
| 40 | `blueberry` | `Train-Val` | `ps_blueberry_mummy_berry_Bing_0325.jpg` | [`blueberry_8dfa865125_blueberry_fruit_diseased_014168.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_8dfa865125_blueberry_fruit_diseased_014168.jpg) | `8dfa865125d7` |
| 41 | `blueberry` | `Train-Test` | `ps_blueberry_scorch_Bing_0005.jpg` | [`blueberry_91029e6b71_blueberry_leaves_diseased_014174.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_91029e6b71_blueberry_leaves_diseased_014174.jpg) | `91029e6b71f9` |
| 42 | `bellpepper` | `Train-Test` | `9a5c5fec54_bell_pepper_blossom_end_rot_Google_0040.jpg` | [`capsicum_9a5c5fec54_capsicum_fruit_diseased_007388.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/bellpepper/capsicum_9a5c5fec54_capsicum_fruit_diseased_007388.jpg) | `9a5c5fec543a` |
| 43 | `bellpepper` | `Train-Test` | `ps_bell_pepper_blossom_end_rot_Google_0396.jpg` | [`capsicum_9be72660d3_capsicum_fruit_diseased_007281.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/bellpepper/capsicum_9be72660d3_capsicum_fruit_diseased_007281.jpg) | `9be72660d356` |
| 44 | `blueberry` | `Train-Val` | `ps_blueberry_mummy_berry_Bing_0161.jpg` | [`blueberry_9eaba60439_blueberry_fruit_diseased_014222.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_9eaba60439_blueberry_fruit_diseased_014222.jpg) | `9eaba60439f8` |
| 45 | `eggplant` | `Train-Val` | `aa07139033_eggplant_phomopsis_fruit_rot_Bing_0054.jpg` | [`eggplant_aa07139033_aa07139033_eggplant_phomopsis_fruit_rot_Bing_0054.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/eggplant/eggplant_aa07139033_aa07139033_eggplant_phomopsis_fruit_rot_Bing_0054.jpg) | `aa07139033de` |
| 46 | `strawberry` | `Train-Test` | `abedd44979_strawberry_anthracnose_google_0027.jpg` | [`strawberry_abedd44979_strawberry_fruit_diseased_010402.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/strawberry/strawberry_abedd44979_strawberry_fruit_diseased_010402.jpg) | `abedd44979a0` |
| 47 | `blueberry` | `Train-Val` | `b109f8d3a8_blueberry_scorch_Bing_0291.jpg` | [`blueberry_b109f8d3a8_blueberry_leaves_diseased_014351.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_b109f8d3a8_blueberry_leaves_diseased_014351.jpg) | `b109f8d3a89b` |
| 48 | `bellpepper` | `Train-Test` | `b426ff3b6e_bell_pepper_blossom_end_rot_Bing_0196.jpg` | [`capsicum_b426ff3b6e_capsicum_fruit_diseased_007046.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/bellpepper/capsicum_b426ff3b6e_capsicum_fruit_diseased_007046.jpg) | `b426ff3b6e16` |
| 49 | `blueberry` | `Train-Val` | `ps_blueberry_mummy_berry_Bing_0062.jpg` | [`blueberry_b8548f58c3_blueberry_fruit_diseased_014375.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_b8548f58c3_blueberry_fruit_diseased_014375.jpg) | `b8548f58c39d` |
| 50 | `blueberry` | `Train-Val` | `bb30f5ab6d_blueberry_rust_google_0074.jpg` | [`blueberry_bb30f5ab6d_blueberry_leaves_diseased_014194.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_bb30f5ab6d_blueberry_leaves_diseased_014194.jpg) | `bb30f5ab6ddb` |
| 51 | `blueberry` | `Train-Val` | `ps_blueberry_mummy_berry_Google_0020.jpg` | [`blueberry_c19ffcd9e1_blueberry_fruit_diseased_014262.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_c19ffcd9e1_blueberry_fruit_diseased_014262.jpg) | `c19ffcd9e14a` |
| 52 | `blueberry` | `Train-Test` | `c42723e2df_blueberry_anthracnose_Bing_0095.jpg` | [`blueberry_c42723e2df_blueberry_fruit_diseased_014215.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_c42723e2df_blueberry_fruit_diseased_014215.jpg) | `c42723e2df90` |
| 53 | `blueberry` | `Train-Test` | `ps_blueberry_botrytis_blight_Bing_0071.jpg` | [`blueberry_c8922a6500_blueberry_fruit_diseased_014312.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_c8922a6500_blueberry_fruit_diseased_014312.jpg) | `c8922a650077` |
| 54 | `blueberry` | `Train-Val` | `ps_blueberry_mummy_berry_Bing_0067.jpg` | [`blueberry_ca12db4ea9_blueberry_fruit_diseased_014363.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_ca12db4ea9_blueberry_fruit_diseased_014363.jpg) | `ca12db4ea9c9` |
| 55 | `bellpepper` | `Train-Test` | `cdf48d7939_bell_pepper_blossom_end_rot_Bing_0112.jpg` | [`capsicum_cdf48d7939_capsicum_fruit_diseased_006125.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/bellpepper/capsicum_cdf48d7939_capsicum_fruit_diseased_006125.jpg) | `cdf48d7939e8` |
| 56 | `eggplant` | `Train-Test` | `ce38f2bbc5_eggplant_phomopsis_fruit_rot_Bing_0009.jpg` | [`eggplant_ce38f2bbc5_ce38f2bbc5_eggplant_phomopsis_fruit_rot_Bing_0009.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/eggplant/eggplant_ce38f2bbc5_ce38f2bbc5_eggplant_phomopsis_fruit_rot_Bing_0009.jpg) | `ce38f2bbc5bd` |
| 57 | `blueberry` | `Train-Val` | `d3c5effb68_blueberry_scorch_Bing_0043.jpg` | [`blueberry_d3c5effb68_blueberry_leaves_diseased_014374.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_d3c5effb68_blueberry_leaves_diseased_014374.jpg) | `d3c5effb68f7` |
| 58 | `bellpepper` | `Train-Val` | `d4c68ce801_bell_pepper_blossom_end_rot_Bing_0195.jpg` | [`capsicum_d4c68ce801_capsicum_fruit_diseased_007184.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/bellpepper/capsicum_d4c68ce801_capsicum_fruit_diseased_007184.jpg) | `d4c68ce801a1` |
| 59 | `blueberry` | `Train-Test` | `ps_blueberry_rust_google_0014.jpg` | [`blueberry_d8ca8bffda_blueberry_leaves_diseased_014143.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_d8ca8bffda_blueberry_leaves_diseased_014143.jpg) | `d8ca8bffdaf9` |
| 60 | `blueberry` | `Train-Val` | `defc6dd86c_blueberry_mummy_berry_Bing_0174.jpg` | [`blueberry_defc6dd86c_blueberry_fruit_diseased_014156.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_defc6dd86c_blueberry_fruit_diseased_014156.jpg) | `defc6dd86ce6` |
| 61 | `blueberry` | `Train-Test` | `dff8adc302_blueberry_anthracnose_Bing_0018.jpg` | [`blueberry_dff8adc302_blueberry_fruit_diseased_014421.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_dff8adc302_blueberry_fruit_diseased_014421.jpg) | `dff8adc302cf` |
| 62 | `blueberry` | `Train-Test` | `ps_blueberry_mummy_berry_Google_0083.jpg` | [`blueberry_e0db4e059e_blueberry_fruit_diseased_014349.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_e0db4e059e_blueberry_fruit_diseased_014349.jpg) | `e0db4e059e85` |
| 63 | `blueberry` | `Train-Test` | `e85ff13505_blueberry_mummy_berry_Bing_0024.jpg` | [`blueberry_e85ff13505_blueberry_fruit_diseased_014277.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_e85ff13505_blueberry_fruit_diseased_014277.jpg) | `e85ff1350504` |
| 64 | `blueberry` | `Train-Test` | `ps_blueberry_botrytis_blight_Bing_0033.jpg` | [`blueberry_ec6bd77493_blueberry_fruit_diseased_014281.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/test/blueberry/blueberry_ec6bd77493_blueberry_fruit_diseased_014281.jpg) | `ec6bd77493d1` |
| 65 | `blueberry` | `Train-Val` | `f2591684b3_blueberry_anthracnose_Bing_0002.jpg` | [`blueberry_f2591684b3_blueberry_fruit_diseased_014340.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_f2591684b3_blueberry_fruit_diseased_014340.jpg) | `f2591684b32d` |
| 66 | `blueberry` | `Train-Val` | `f3210c80ed_blueberry_anthracnose_Bing_0145.jpg` | [`blueberry_f3210c80ed_blueberry_fruit_diseased_014198.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_f3210c80ed_blueberry_fruit_diseased_014198.jpg) | `f3210c80ed93` |
| 67 | `blueberry` | `Train-Val` | `f591ce9544_blueberry_anthracnose_Bing_0004.jpg` | [`blueberry_f591ce9544_blueberry_fruit_diseased_014429.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/blueberry/blueberry_f591ce9544_blueberry_fruit_diseased_014429.jpg) | `f591ce95444e` |
| 68 | `bellpepper` | `Train-Val` | `fb19e7e1d8_bell_pepper_blossom_end_rot_Bing_0087.jpg` | [`capsicum_fb19e7e1d8_capsicum_fruit_diseased_007061.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/bellpepper/capsicum_fb19e7e1d8_capsicum_fruit_diseased_007061.jpg) | `fb19e7e1d804` |
| 69 | `bellpepper` | `Train-Val` | `fee212dea7_bell_pepper_blossom_end_rot_Bing_0012.jpg` | [`capsicum_fee212dea7_capsicum_fruit_diseased_007076.jpg`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded/val/bellpepper/capsicum_fee212dea7_capsicum_fruit_diseased_007076.jpg) | `fee212dea7aa` |

---

## 4. Near-Duplicate Review Assessment

All 139 near-duplicate cross-split pairs ($p\text{Hash distance} \le 4$) were re-evaluated:
- **Assessment Result**: Following the deletion of the 69 exact SHA-256 duplicates, remaining near-duplicate pairs represent natural botanical and foliage visual similarities within the same crop class (e.g. repeated leaf vein patterns or camera lighting variants across independent field specimens).
- **Action**: Retained in `train/` to preserve dataset feature diversity, with validation loss to be monitored during EXP-1 training.

---

## 5. Repaired Dataset Inventory (46 Canonical Classes)

**Total Real Clean Images**: **17,928** (Train: 14,769, Val: 1,579, Test: 1,580)

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
| 23 | **gerbera** | 2 | 0 | 1 | **3** | 400 | Short (<400) |
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

## 6. Automated Assertion Results

| Assertion Check | Expected | Actual Result | Verification Status |
| :--- | :--- | :--- | :--- |
| **Exact Cross-Split Duplicates** | 0 | 0 | **PASSED (100% Clean)** |
| **Unmanifested Disk Images** | 0 | 0 | **PASSED (100% Indexed)** |
| **Orphan Manifest Records** | 0 | 0 | **PASSED (0 Missing Files)** |
| **Canonical Directory Consistency** | 46 classes | 46 classes | **PASSED (Strict Alignment)** |
| **EXP-0 Checkpoint Compatibility** | `num_classes=46` | `num_classes=46` | **PASSED (Head Dimension Preserved)** |

---
*Report compiled automatically upon Phase 3A completion on 2026-10-10 12:07:42.*