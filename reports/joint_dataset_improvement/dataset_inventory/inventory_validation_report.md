# Inventory Validation Report

**Scope:** Inspection and reporting only. No datasets downloaded, no models trained, no production/class-mapping files changed, no images moved between splits.

## 1. Counting method
- **Processed splits** (`data/processed/model1_balanced`, `model1_expanded`, `model2_v4`): counts were read by walking `train/val/test` subfolders per class. These files are already deduplicated by the existing pipeline (the balanced report states 0 exact/near duplicates removed and 0 cross-split leakage). Processed counts are treated as **unique real images**.
- **External/staged folders** (`data/external/...`): files were enumerated and hashed with **SHA-256**; duplicate counts = files minus unique hashes. Examples: Pepper Bell `PepperBell_Bacterial Spot` 4,901 files -> 4,080 unique; Cercospora 1,796 -> 1,572; all other Pepper Bell folders 100% unique.
- **No augmentation counted.** Only real, unique source images count toward acquisition targets.
- **Aliases resolved** via class mappings: `cherry_tomato`->`tomato`, `capsicum`->`bell_pepper`, `french_bean`->`bean`, `zucchini`->`squash`. `cherry_tomato` is documented as 0 standalone by design.
- **External + processed never blindly summed.** The model2 manifest provenance (`source_dataset` column) was checked: the Pepper Bell and Cauliflower external datasets are **not** present in the processed splits (processed bell_pepper/cauliflower images come from `external_healthy_*`, `plantseg`, `plantseg_v3_supplementary`, `model1_balanced_healthy`). Therefore staged external counts for those two datasets are reported as additive and clearly flagged.

## 2. Resolved / documented ambiguities
- **Cauliflower `Bacterial Spot` vs `Bacterial spot rot`:** two separate folders (403 fruit and 168 fruit images). NOT merged. Neither is in the current cauliflower taxonomy; both are reported as additional categories requiring an owner decision.
- **Cauliflower fruit vs leaf:** the downloaded dataset ships both fruit and leaf subfolders. `Alternaria Brassicae` (fruit, 44) and `Alternaria Leaf Spot` (leaves, 304) were both mapped to `alternaria_leaf_spot`, mixing plant parts - flagged. Fruit classes are flagged as fruit-part; disease classes typically expect leaf images.
- **`Cerespora`** (bell_pepper experimental subfolder, 226 train), **`Leaf_Curl`** (335 train) and **`Pepper__bell___Bacterial_spot_Leaf_Curl_Cercospora`** (301 train) exist in `data/processed/model2_v4/train/bell_pepper/` but are **not** in the v4 class mapping. They are experimental only and were excluded from the 116-class taxonomy totals.
- **Capsicum vs bell_pepper:** Model 1 uses `capsicum`; Model 2 uses `bell_pepper`. Same crop. `capsicum__healthy` (804) and `bell_pepper__healthy` (708) are reported under their respective taxonomies.
- **Shared `healthy` class:** Model 2 has one shared `healthy` class (total 6,939 across all crop/healthy subfolders). It is NOT counted as a per-crop disease class. Crop-specific healthy availability is reported separately per crop.

## 3. Missing / unverified items
- **Model 1 external dedup:** SHA-256 hashing was performed on the Pepper Bell (bell pepper) and Cauliflower external folders and the staged gerbera/gypsophila folders. Older external model1 sources already inside the processed splits were not re-hashed (already deduplicated upstream).
- **Gypsophila:** the staged Roboflow folder is a 3-class mix (Gypsophila/Hydrangea/Daisy); only ~47 images are usable gypsophila. Exact usable count is **unverified** pending per-image review.
- **Chilli:** confirmed no dataset available (0 Model 1, no Model 2 class).
- **Mango:** present in the expanded taxonomy but **excluded by project scope**; not recommended for collection.
- **Health splits** (healthy vs diseased) are taken from `data/processed/health_distribution.csv` where the label was known; unknown-label images are not force-assigned.

## 4. Files generated
- complete_dataset_inventory.md
- model1_inventory.csv
- model2_inventory.csv
- dataset_source_inventory.csv
- acquisition_priority.csv
- inventory_validation_report.md (this file)
