# Model 2 Retraining V2 — Final Dataset Build & Validation Report

**Status:** DATASET GENERATION COMPLETE & VALIDATED  
**Dataset Directory:** `data/processed/model2_retraining_v2/`  
**Manifest Path:** `data/processed/model2_retraining_v2_manifest.csv`  
**Class Mapping:** `data/processed/model2_retraining_v2/class_mapping.json` (144 Classes)  
**Crop-Disease Mapping:** `data/processed/model2_retraining_v2/crop_disease_mapping.json`  

---

## 1. Verified Post-Build Split & Class Counts

All counts are verified directly against `data/processed/model2_retraining_v2_manifest.csv` and physical files on disk:

| Split | Historical V1 Count | V2 New Additions | Final V2 Manifest Count | Status |
| :--- | :---: | :---: | :---: | :--- |
| **Train** | 27,982 | +2,106 | **30,088** | Augmented with clean deduplicated images |
| **Validation** | 2,647 | +402 | **3,049** | Augmented (15% deterministic partition) |
| **Test** | **2,304** | **+0** | **2,304** | **100% IMMUTABLE & UNCHANGED** |
| **Total** | **32,933** | **+2,508** | **35,441** | **All 35,441 files resolve on disk** |

---

## 2. Taxonomy & Head Expansion

- **Total Classes:** **144 Classes** (0 = `healthy`, 1..142 = Existing Disease Classes, 143 = `tomato__anthracnose`).
- **New Class:** `tomato__anthracnose` (*Colletotrichum coccodes*) added as Class ID 143.
  - Total Clean Images: **322 images** (274 Train, 48 Validation, 0 Test).
- **Excluded Class:** `tomato fruit fusarium wilt` (231 images) &mdash; **Quarantined and excluded** due to pathological inconsistency and cross-label collisions.

---

## 3. Strict Safety & Integrity Assertions

| Invariant | Result | Evidence |
| :--- | :---: | :--- |
| **Test Set Preservation** | **PASSED** | Exactly 2,304 test images; zero additions, modifications, or reassignments. |
| **Disk File Resolution** | **PASSED** | 35,441 / 35,441 manifest paths exist and resolve to valid decodable image files. |
| **Cross-Split Leakage Check** | **PASSED** | `Train ∩ Test == ∅`, `Val ∩ Test == ∅`, `Train ∩ Val == ∅` (0 duplicate SHA hashes). |
| **Test Set Near-Duplicate Protection** | **PASSED** | 48 images matching protected test set (pHash $\le$ 4) excluded from V2. |
| **Historical V1 Train Duplication** | **PASSED** | 323 duplicate images from `Blueberry Fruit healthy` excluded from V2. |
| **Cross-Folder Label Collisions** | **PASSED** | 213 images shared across conflicting raw folders excluded. |
| **Filename Conflict Quarantine** | **PASSED** | 2 images with conflicting early blight filenames in Anthracnose folder excluded. |
| **Mapping Continuity** | **PASSED** | Class IDs form an unbroken sequence from 0 to 143 matching `class_mapping.json`. |

---

## 4. Per-Class Image Distribution for Augmented & New Classes

| Canonical Class | Class ID | V2 Train | V2 Val | V2 Test | V2 Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `healthy` (Shared) | 0 | 1,566 | 202 | 180 | **1,948** |
| `banana__cigar_end_rot` | 8 | 265 | 45 | 16 | **326** |
| `broccoli__alternaria_leaf_spot` | 28 | 258 | 45 | 16 | **319** |
| `broccoli__downy_mildew` | 29 | 244 | 41 | 16 | **301** |
| `broccoli__ring_spot` | 30 | 227 | 38 | 16 | **281** |
| `celery__anthracnose` | 42 | 183 | 30 | 16 | **229** |
| `eggplant__phomopsis_fruit_rot` | 62 | 173 | 28 | 16 | **217** |
| `eggplant__phytophthora_blight` | 63 | 284 | 48 | 16 | **348** |
| `lettuce__downy_mildew` | 75 | 212 | 35 | 16 | **263** |
| `lettuce__mosaic_virus` | 76 | 197 | 32 | 16 | **245** |
| `tomato__early_blight` | 125 | 625 | 91 | 16 | **732** |
| `tomato__late_blight` | 126 | 619 | 91 | 16 | **726** |
| `tomato__yellow_leaf_curl_virus` | 130 | 561 | 79 | 16 | **656** |
| `tomato__anthracnose` (NEW) | 143 | 274 | 48 | 0 | **322** |
