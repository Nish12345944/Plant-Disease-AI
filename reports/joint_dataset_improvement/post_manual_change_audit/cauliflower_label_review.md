# Cauliflower Dataset Audit & Label Review (Post-Manual Changes)

**Audit Date:** 2026-10-09  
**Audit Scope:** Read-only inspection of cauliflower data across Model 1 and Model 2 processed datasets (`data/processed/model1_expanded` and `data/processed/model2_v4`).  
**Safety Protocol:** Strict read-only audit. No files renamed, moved, deleted, relabeled, or re-split.

---

## 1. Executive Summary: Cauliflower Findings

Manual restructuring has introduced critical structural, taxonomic, and plant-part inconsistencies in `data/processed/model2_v4/train/cauliflower/`:

1. **Destruction of Canonical Directory Hierarchy:**  
   The three canonical Model 2 cauliflower classes (`cauliflower__alternaria_leaf_spot`, `cauliflower__bacterial_soft_rot`, and `cauliflower__healthy` / `healthy`) present in `val/` and `test/` have been completely removed from `train/cauliflower/`. They were replaced by **12 raw source folders** (7 curd/fruit folders and 5 leaf folders).
2. **Displacement of Baseline Training Images:**  
   All 83 original cauliflower training images in the Model 2 v4 manifest (`model2_v4_manifest.csv`) were displaced. 28 were copied into `cauliflower_fruit_Bacterial Soft Rot`, 21 into `cauliflower_leaf_Healthy`, and 34 were removed or unmapped.
3. **Severe Plant-Part Mixing (Curd vs. Foliage):**  
   Model 2 was designed primarily as a foliar crop disease classifier. In the modified training folder, **1,461 curd/head images** (across 7 folders) are mixed alongside **4,581 leaf images** (across 5 folders).
4. **Physiological Condition Labelled as Disease:**  
   `cauliflower_fruit_Purple Tinges` (153 images) represents a physiological anthocyanin accumulation (sun-exposure / temperature reaction or cultivar characteristic), not a pathogen-induced infectious disease.
5. **Redundant & Overlapping Categories:**  
   `cauliflower_fruit_Bacterial Spot` (405 images) and `cauliflower_fruit_Bacterial spot rot` (173 images) share 14 exact duplicate image files (SHA-256 identical) and represent non-standard, competing names for the same curd disease syndrome.
6. **Severe Intra-Class Duplication:**  
   `cauliflower_leaf_Downy Mildew` contains **153 exact duplicate files** (434 unique images across 587 files). `cauliflower_leaf_Healthy` contains 34 duplicate files.
7. **Taxonomy Incompatibility:**  
   Model 2's production class mapping (`models/model2_classifier_v4/class_mapping.json`, 117 classes) has no entries for `cauliflower__black_rot`, `cauliflower__downy_mildew`, `cauliflower__insect_hole`, `cauliflower__black_spot`, `cauliflower__purple_tinges`, or `cauliflower__bacterial_spot`. Standard DataLoader scripts expecting `<crop>__<disease>` matching the mapping will crash or misassign indices.

---

## 2. Folder-by-Folder Technical Inventory

The current `data/processed/model2_v4/train/cauliflower/` directory contains **6,042 total image files** across 12 subdirectories:

| Directory Name | Total Files | Unique SHA-256 | Intra-Folder Duplicates | Primary Plant Part | Common Resolutions | Average File Size | Current Model 2 Mapping Compatibility |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `cauliflower_fruit_Alternaria Brassicae` | 45 | 44 | 1 | Curd / Head | 3060x4080 (100%) | 983.1 KB | ❌ Unmapped class |
| `cauliflower_fruit_Bacterial Soft Rot` | 228 | 227 | 1 | Curd / Head | 3060x4080, 4080x3060 | 848.4 KB | ⚠️ Partial (Name mismatch) |
| `cauliflower_fruit_Bacterial Spot` | 405 | 403 | 2 | Curd / Head | 456x456 (61%), 2712x2712 | 477.5 KB | ❌ Unmapped class |
| `cauliflower_fruit_Bacterial spot rot` | 173 | 168 | 5 | Curd / Head | 4000x3000, 1280x960 | 1,071.8 KB | ❌ Unmapped class |
| `cauliflower_fruit_Black Spot` | 251 | 251 | 0 | Curd / Head | 3060x4080 (71%), 4080x3060 | 1,441.3 KB | ❌ Unmapped class |
| `cauliflower_fruit_healthy` | 206 | 206 | 0 | Curd / Head | 4000x3000 (46%), 3000x4000 | 2,500.7 KB | ⚠️ Maps to unified `healthy` |
| `cauliflower_fruit_Purple Tinges` | 153 | 153 | 0 | Curd / Head | 3123x4160 (79%), 1200x1599 | 834.1 KB | ❌ Unmapped (Physiological) |
| `cauliflower_leaf_Alternaria Leaf Spot` | 308 | 304 | 4 | Leaf / Foliage | 3024x4032, 4032x3024 | 962.8 KB | ⚠️ Partial (Name mismatch) |
| `cauliflower_leaf_Black Rot` | 1,188 | 1,188 | 0 | Leaf / Foliage | 3000x3000 (92%) | 597.2 KB | ❌ Unmapped class |
| `cauliflower_leaf_Downy Mildew` | 587 | 434 | 153 | Leaf / Foliage | 3000x4000, 4000x3000 | 1,852.3 KB | ❌ Unmapped class |
| `cauliflower_leaf_Healthy` | 1,859 | 1,825 | 34 | Leaf / Foliage | 3000x3000 (50%), 456x456 | 510.6 KB | ⚠️ Maps to unified `healthy` |
| `cauliflower_leaf_Insect Hole` | 639 | 639 | 0 | Leaf / Foliage | 3000x3000 (100%) | 380.8 KB | ❌ Unmapped (Pest damage) |
| **Total Train Cauliflower** | **6,042** | **5,842** | **200** | **Mixed (Curd + Leaf)** | - | - | **0 canonical matches** |

---

## 3. Deep-Dive on Specific Problem Categories

### 3.1 `Bacterial Spot` vs. `Bacterial spot rot`
- **Symptom Profile:** Both folders depict dark water-soaked lesions and necrosis across the cauliflower curd (inflorescence).
- **Exact Hash Duplication:** **14 exact duplicate images** exist simultaneously in both `cauliflower_fruit_Bacterial Spot` and `cauliflower_fruit_Bacterial spot rot` (e.g., hashes `4b34e61132...`, `411d9fa26c...`, `1954cf6f02...`).
- **Resolution:** These two folders represent inconsistent naming conventions from different source download batches (*Xanthomonas campestris* pv. *armoraciae* or *Pseudomonas syringae* vs. soft rot complexes). They should **not** exist as two separate classes.

### 3.2 `Purple Tinges`
- **Symptom Profile:** Cauliflower heads displaying reddish-purple pigmentation across outer curds.
- **Pathology Evaluation:** Anthocyanin accumulation occurs when curd heads are exposed to direct sunlight, cold temperatures during head development, or nutrient shifts. It is **not** an infectious pathogenic disease caused by fungi, bacteria, or viruses.
- **Risk:** Training a disease diagnosis model on `Purple Tinges` will teach the model to classify healthy sun-exposed cauliflower as diseased, triggering false positive disease alerts and unnecessary chemical treatments.

### 3.3 `Alternaria Brassicae` vs. `cauliflower_leaf_Alternaria Leaf Spot`
- **Folder Confusion:** `cauliflower_fruit_Alternaria Brassicae` (45 images, curd) and `cauliflower_leaf_Alternaria Leaf Spot` (308 images, leaf) are split across plant parts.
- *Alternaria brassicae* and *Alternaria brassicicola* infect leaves, stems, and seed pods, producing concentric zonate dark leaf spots. Curd infections typically occur as secondary spread from infected leaves.
- **Model 2 Target:** Model 2 v4 defines `cauliflower__alternaria_leaf_spot`. Feeding curd images into an architecture trained on foliar leaf symptoms corrupts feature extraction.

### 3.4 Unmapped Foliar Classes (`Black Rot`, `Downy Mildew`, `Insect Hole`)
- **`Black Rot` (*Xanthomonas campestris* pv. *campestris*):** 1,188 leaf images with characteristic V-shaped chlorotic-to-necrotic marginal lesions. While a valid crucifer disease, `cauliflower__black_rot` is **not present** in the 117-class mapping for Model 2 (only `cabbage__black_rot` is mapped).
- **`Downy Mildew` (*Hyaloperonospora parasitica*):** 587 leaf images showing angular chlorotic patches. Contains 153 redundant duplicates. Not in Model 2 class mapping (only `broccoli__downy_mildew` is mapped).
- **`Insect Hole`:** 639 leaf images displaying mechanical chewing damage from lepidopteran larvae (e.g., diamondback moth). This is physical pest damage, not a phytopathological disease.

---

## 4. Displaced Original Dataset Inventory

In the approved `model2_v4_manifest.csv`, cauliflower had a clean, balanced 3-class baseline:
- `train/cauliflower/alternaria_leaf_spot`: 35 images
- `train/cauliflower/bacterial_soft_rot`: 27 images
- `train/cauliflower/healthy`: 21 images
- Total original train images: **83 images**

**Fate of the Original 83 Images:**
- **28 images** from `bacterial_soft_rot` are currently inside `cauliflower_fruit_Bacterial Soft Rot`.
- **21 images** from `healthy` are currently inside `cauliflower_leaf_Healthy`.
- **34 images** from `alternaria_leaf_spot` were completely displaced / deleted from the training directory.
- `val/cauliflower` (3 classes, 30 images) and `test/cauliflower` (3 classes, 30 images) were **not** modified and remain strictly intact.

---

## 5. Model 1 Cauliflower Audit

In `data/processed/model1_expanded/`:
- `train/cauliflower/`: **425 images** (previously 84 in manifest; **+341 images added**).
- `val/cauliflower/`: **10 images** (unchanged).
- `test/cauliflower/`: **10 images** (unchanged).
- **Plant-Part Composition:** The 341 added images in Model 1 `train/cauliflower/` include a mix of whole plants, leaves, and curd heads. Because Model 1 is a plant species identifier (cauliflower identification), including diverse plant views (leaves + curd) is agronomically helpful, **provided** duplicate leakage into test is prevented (no test leakage detected for cauliflower in Model 1).

---

## 6. Actionable Recommendations for Cauliflower Dataset

1. **Do not retrain Model 2 v4** with the current `train/cauliflower/` folder structure.
2. **Quarantine or Discard Non-Disease Folders:**
   - Remove `cauliflower_fruit_Purple Tinges` (physiological disorder).
   - Remove `cauliflower_leaf_Insect Hole` (pest damage, not disease).
3. **Harmonize Plant Parts:**
   - Standardize Model 2 on **foliar disease symptoms** (leaves) to maintain feature consistency with the rest of the 39 crops.
   - If curd diseases are to be supported, establish explicit curd classes (e.g., `cauliflower_curd__bacterial_soft_rot`) and update the class mapping accordingly.
4. **Deduplicate and Merge Bacterial Folders:**
   - Deduplicate `cauliflower_fruit_Bacterial Spot` and `cauliflower_fruit_Bacterial spot rot` against each other.
   - Deduplicate `cauliflower_leaf_Downy Mildew` (purge 153 identical files).
5. **Restore Valid Directory Names:**
   - Map approved images back to canonical names (`cauliflower/alternaria_leaf_spot`, `cauliflower/bacterial_soft_rot`, `cauliflower/healthy`) matching `models/model2_classifier_v4/class_mapping.json`.
