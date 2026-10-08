# Model 1 Expansion External Dataset Staging Area

> **MANDATORY AUDIT NOTICE:**  
> **No dataset acquisition has been performed during the taxonomy-audit phase.**

This directory is reserved for future dataset acquisition and staging for the expanded 46-class Model 1 crop classifier, in accordance with the specifications established in:
- `reports/model1_expansion/model1_model2_crop_gap_audit.md`
- `reports/model1_expansion/expanded_model1_taxonomy.md`
- `reports/model1_expansion/model1_expansion_dataset_requirements.md`

### Directory Protocol:
1. Do not download or copy raw images into this folder until the dataset acquisition phase is explicitly authorized.
2. Existing project images in `data/processed/model2_v4/` should be audited and reused as the primary data source (Tier 1 & Tier 2) before initiating external downloads.
3. All future datasets staged here must undergo SHA-256 deduplication and label verification prior to incorporation into training manifests.
