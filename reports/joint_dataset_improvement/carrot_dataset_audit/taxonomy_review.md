# Carrot Dataset — Taxonomy Review


## Model 2 carrot taxonomy (current)

- `carrot__alternaria_leaf_blight`
- `carrot__cavity_spot`
- `carrot__cercospora_leaf_blight`

## Match status of the 26 source classes

| Source class | Matches carrot taxonomy? | Requires manual review | Should NOT map to carrot | Notes |
|---|:--:|:--:|:--:|---|
| `anthracnose` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `anthracnose_fruit_rot` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `bacterial_spot` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `black_rot` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `bruise` | no | no | YES | physical/quality defect, not a disease - exclude |
| `color` | no | no | YES | physical/quality defect, not a disease - exclude |
| `combined` | no | no | YES | physical/quality defect, not a disease - exclude |
| `contamination` | no | no | YES | physical/quality defect, not a disease - exclude |
| `crack` | no | no | YES | physical/quality defect, not a disease - exclude |
| `cut` | no | no | YES | physical/quality defect, not a disease - exclude |
| `defect` | no | no | YES | physical/quality defect, not a disease - exclude |
| `early_blight` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `esca` | no | no | YES | grapevine disease (wrong crop) - exclude |
| `faulty_imprint` | no | no | YES | physical/quality defect, not a disease - exclude |
| `gray_mold` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `hole` | no | no | YES | physical/quality defect, not a disease - exclude |
| `late_blight` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `leaf scorch` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `mold` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `mold-bread` | no | no | YES | bread mold (wrong product) - exclude |
| `poke` | no | no | YES | physical/quality defect, not a disease - exclude |
| `print` | no | no | YES | physical/quality defect, not a disease - exclude |
| `rust` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `scab` | no | YES | no | disease-named but crop unconfirmed & not in carrot taxonomy - review/re-label |
| `scratch` | no | no | YES | physical/quality defect, not a disease - exclude |
| `squeeze` | no | no | YES | physical/quality defect, not a disease - exclude |

## New disease classes requiring approval

These source classes are disease-like but NOT in the carrot Model 2 taxonomy; they would require your explicit approval AND crop re-verification as carrot before use: `anthracnose`, `anthracnose_fruit_rot`, `bacterial_spot`, `black_rot`, `early_blight`, `gray_mold`, `late_blight`, `leaf scorch`, `mold`, `rust`, `scab`.


## Recommendation

**Do NOT use this dataset as carrot disease data.** It is a generic produce-defect set with unverified crop identity. Options: (1) discard for carrot; (2) request crop/label clarification from the source; (3) use only after manual visual re-verification of crop and re-annotation into approved carrot classes.