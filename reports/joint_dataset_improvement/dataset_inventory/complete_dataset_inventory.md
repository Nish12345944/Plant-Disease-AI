# Complete Dataset Inventory — Model 1 & Model 2 (Real Images Only)

**Filesystem audit only. No datasets downloaded, no models trained, no production files changed.**

**Counting method:** SHA-256 content hashing for external folders; processed split counts read from `data/processed/`. Augmented/generated images NOT counted. Aliases resolved to canonical classes.


## Taxonomy sizes

- **Model 1 production:** 22 classes (`models/model1/class_mapping.json`)
- **Model 1 expanded:** 46 class slots - includes aliases `cherry_tomato`(=tomato), `capsicum`(=bell_pepper), `french_bean`(=bean), `zucchini`(=squash)
- **Model 2 production (v4):** 117 = 116 crop diseases + 1 shared `healthy`. Shared healthy total = **6,939**.

- **Crops audited:** 49. **Model 2 disease classes:** 116.


---
## Crop: Anthurium

### Model 1 — Crop identification

- Canonical model class: `anthurium`
- Status: production+expanded
- Splits: train 84, val 10, test 10
- Processed total: 104
- Additional staged external real images: 0
- **Total unique usable real images: 104**
- Target 400-500: shortage to 400 = 296 ; to 500 = 396
- Notes: Flower-only source; limited backgrounds/angles.

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Blueberry

### Model 1 — Crop identification

- Canonical model class: `blueberry`
- Status: production+expanded
- Splits: train 252, val 31, test 31
- Processed total: 314
- Additional staged external real images: 0
- **Total unique usable real images: 314**
- Target 400-500: shortage to 400 = 86 ; to 500 = 186

### Model 2 — Disease classification

- Number of disease classes: 5

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `blueberry__anthracnose` | 32 | 4 | 4 | 40 | 0 | 40 | 210 | 360 | 460 |
| `blueberry__botrytis_blight` | 29 | 3 | 3 | 35 | 0 | 35 | 215 | 365 | 465 |
| `blueberry__mummy_berry` | 38 | 4 | 4 | 46 | 0 | 46 | 204 | 354 | 454 |
| `blueberry__rust` | 34 | 4 | 5 | 43 | 0 | 43 | 207 | 357 | 457 |
| `blueberry__scorch` | 33 | 4 | 5 | 42 | 0 | 42 | 208 | 358 | 458 |


---
## Crop: Broccoli

### Model 1 — Crop identification

- Canonical model class: `broccoli`
- Status: production+expanded
- Splits: train 332, val 41, test 41
- Processed total: 414
- Additional staged external real images: 0
- **Total unique usable real images: 414**
- Target 400-500: shortage to 400 = 0 ; to 500 = 86

### Model 2 — Disease classification

- Number of disease classes: 3

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `broccoli__alternaria_leaf_spot` | 49 | 5 | 8 | 62 | 0 | 62 | 188 | 338 | 438 |
| `broccoli__downy_mildew` | 23 | 2 | 4 | 29 | 0 | 29 | 221 | 371 | 471 |
| `broccoli__ring_spot` | 8 | 1 | 1 | 10 | 0 | 10 | 240 | 390 | 490 |


---
## Crop: Capsicum

### Model 1 — Crop identification

- Canonical model class: `capsicum`
- Status: production+expanded
- Splits: train 631, val 65, test 65
- Processed total: 761
- Additional staged external real images: 0
- **Total unique usable real images: 761**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0
- Health split: 1,607 healthy / 1,183 diseased
- Notes: =bell_pepper. Disease leaf images ~96.5% healthy -> limited diversity; diversify sources before adding count.

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Carnation

### Model 1 — Crop identification

- Canonical model class: `carnation`
- Status: production+expanded
- Splits: train 41, val 5, test 5
- Processed total: 51
- Additional staged external real images: 0
- **Total unique usable real images: 51**
- Target 400-500: shortage to 400 = 349 ; to 500 = 449
- Notes: 51 flower images; single source.

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Cherry_Tomato

### Model 1 — Crop identification

- Canonical model class: `cherry_tomato` (alias of `tomato`)
- Status: production+expanded
- Splits: train 0, val 0, test 0
- Processed total: 0
- Additional staged external real images: 0
- **Total unique usable real images: 0**
- Target 400-500: shortage to 400 = 400 ; to 500 = 500
- Notes: Alias of tomato; 0 standalone by design. Do not collect separately.

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Chrysanthemum

### Model 1 — Crop identification

- Canonical model class: `chrysanthemum`
- Status: production+expanded
- Splits: train 334, val 42, test 42
- Processed total: 418
- Additional staged external real images: 0
- **Total unique usable real images: 418**
- Target 400-500: shortage to 400 = 0 ; to 500 = 82

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Cucumber

### Model 1 — Crop identification

- Canonical model class: `cucumber`
- Status: production+expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- Number of disease classes: 3

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `cucumber__angular_leaf_spot` | 144 | 16 | 22 | 182 | 0 | 182 | 68 | 218 | 318 |
| `cucumber__bacterial_wilt` | 85 | 10 | 13 | 108 | 0 | 108 | 142 | 292 | 392 |
| `cucumber__powdery_mildew` | 283 | 31 | 22 | 336 | 0 | 336 | 0 | 64 | 164 |


---
## Crop: French_Bean

### Model 1 — Crop identification

- Canonical model class: `french_bean`
- Status: production+expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Geranium

### Model 1 — Crop identification

- Canonical model class: `geranium`
- Status: production+expanded
- Splits: train 201, val 25, test 25
- Processed total: 251
- Additional staged external real images: 0
- **Total unique usable real images: 251**
- Target 400-500: shortage to 400 = 149 ; to 500 = 249

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Gerbera

### Model 1 — Crop identification

- Canonical model class: `gerbera`
- Status: production+expanded
- Splits: train 2, val 0, test 1
- Processed total: 3
- Additional staged external real images: 248
- **Total unique usable real images: 251**
- Target 400-500: shortage to 400 = 149 ; to 500 = 249
- Notes: Only 3 in splits; 248 staged images (flower) not incorporated.

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Gypsophila

### Model 1 — Crop identification

- Canonical model class: `gypsophila`
- Status: production+expanded
- Splits: train 0, val 0, test 0
- Processed total: 0
- Additional staged external real images: 47
- **Total unique usable real images: 47**
- Target 400-500: shortage to 400 = 353 ; to 500 = 453
- Notes: 0 in splits; staged Roboflow folder mixes Gypsophila/Hydrangea/Daisy - only ~47 usable gypsophila.

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Lettuce

### Model 1 — Crop identification

- Canonical model class: `lettuce`
- Status: production+expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `lettuce__downy_mildew` | 67 | 7 | 8 | 82 | 0 | 82 | 168 | 318 | 418 |
| `lettuce__mosaic_virus` | 31 | 4 | 4 | 39 | 0 | 39 | 211 | 361 | 461 |


---
## Crop: Lilium

### Model 1 — Crop identification

- Canonical model class: `lilium`
- Status: production+expanded
- Splits: train 37, val 4, test 4
- Processed total: 45
- Additional staged external real images: 0
- **Total unique usable real images: 45**
- Target 400-500: shortage to 400 = 355 ; to 500 = 455
- Notes: 45 tiger-lily flower images; flower-only, single source.

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Marigold

### Model 1 — Crop identification

- Canonical model class: `marigold`
- Status: production+expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Melon

### Model 1 — Crop identification

- Canonical model class: `melon`
- Status: production+expanded
- Splits: train 197, val 25, test 25
- Processed total: 247
- Additional staged external real images: 0
- **Total unique usable real images: 247**
- Target 400-500: shortage to 400 = 153 ; to 500 = 253
- Notes: 247 fruit images; fruit-only.

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Orchid

### Model 1 — Crop identification

- Canonical model class: `orchid`
- Status: production+expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Rose

### Model 1 — Crop identification

- Canonical model class: `rose`
- Status: production+expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Spinach

### Model 1 — Crop identification

- Canonical model class: `spinach`
- Status: production+expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- No crop-specific Model 2 disease class in current taxonomy.


---
## Crop: Strawberry

### Model 1 — Crop identification

- Canonical model class: `strawberry`
- Status: production+expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0
- Health split: 1,649 healthy / 97 diseased
- Notes: 1,373 fruit / 127 leaves -> fruit-heavy.

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `strawberry__anthracnose` | 48 | 5 | 5 | 58 | 0 | 58 | 192 | 342 | 442 |
| `strawberry__leaf_scorch` | 32 | 4 | 3 | 39 | 0 | 39 | 211 | 361 | 461 |


---
## Crop: Tomato

### Model 1 — Crop identification

- Canonical model class: `tomato`
- Status: production+expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0
- Health split: 1,585 healthy / 13,527 diseased

### Model 2 — Disease classification

- Number of disease classes: 7

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tomato__bacterial_leaf_spot` | 85 | 9 | 13 | 107 | 0 | 107 | 143 | 293 | 393 |
| `tomato__early_blight` | 275 | 31 | 22 | 328 | 0 | 328 | 0 | 72 | 172 |
| `tomato__late_blight` | 254 | 29 | 17 | 300 | 0 | 300 | 0 | 100 | 200 |
| `tomato__leaf_mold` | 198 | 22 | 16 | 236 | 0 | 236 | 14 | 164 | 264 |
| `tomato__mosaic_virus` | 50 | 6 | 7 | 63 | 0 | 63 | 187 | 337 | 437 |
| `tomato__septoria_leaf_spot` | 233 | 26 | 14 | 273 | 0 | 273 | 0 | 127 | 227 |
| `tomato__yellow_leaf_curl_virus` | 72 | 8 | 9 | 89 | 0 | 89 | 161 | 311 | 411 |


---
## Crop: Zucchini

### Model 1 — Crop identification

- Canonical model class: `zucchini`
- Status: production+expanded
- Splits: train 315, val 39, test 39
- Processed total: 393
- Additional staged external real images: 0
- **Total unique usable real images: 393**
- Target 400-500: shortage to 400 = 7 ; to 500 = 107

### Model 2 — Disease classification

- Number of disease classes: 4

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `zucchini__bacterial_wilt` | 53 | 6 | 9 | 68 | 0 | 68 | 182 | 332 | 432 |
| `zucchini__downy_mildew` | 34 | 4 | 5 | 43 | 0 | 43 | 207 | 357 | 457 |
| `zucchini__powdery_mildew` | 164 | 18 | 18 | 200 | 0 | 200 | 50 | 200 | 300 |
| `zucchini__yellow_mosaic_virus` | 77 | 9 | 9 | 95 | 0 | 95 | 155 | 305 | 405 |


---
## Crop: Apple

### Model 1 — Crop identification

- Canonical model class: `apple`
- Status: expanded
- Splits: train 452, val 57, test 57
- Processed total: 566
- Additional staged external real images: 0
- **Total unique usable real images: 566**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- Number of disease classes: 4

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `apple__black_rot` | 66 | 7 | 10 | 83 | 0 | 83 | 167 | 317 | 417 |
| `apple__mosaic_virus` | 70 | 8 | 11 | 89 | 0 | 89 | 161 | 311 | 411 |
| `apple__rust` | 112 | 12 | 14 | 138 | 0 | 138 | 112 | 262 | 362 |
| `apple__scab` | 208 | 23 | 25 | 256 | 0 | 256 | 0 | 144 | 244 |


---
## Crop: Banana

### Model 1 — Crop identification

- Canonical model class: `banana`
- Status: expanded
- Splits: train 428, val 54, test 54
- Processed total: 536
- Additional staged external real images: 0
- **Total unique usable real images: 536**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0
- Health split: 0 healthy / 74 diseased (leaves)

### Model 2 — Disease classification

- Number of disease classes: 6

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `banana__anthracnose` | 56 | 6 | 7 | 69 | 0 | 69 | 181 | 331 | 431 |
| `banana__black_leaf_streak` | 127 | 14 | 17 | 158 | 0 | 158 | 92 | 242 | 342 |
| `banana__bunchy_top` | 115 | 13 | 11 | 139 | 0 | 139 | 111 | 261 | 361 |
| `banana__cigar_end_rot` | 47 | 5 | 4 | 56 | 0 | 56 | 194 | 344 | 444 |
| `banana__cordana_leaf_spot` | 42 | 5 | 4 | 51 | 0 | 51 | 199 | 349 | 449 |
| `banana__panama_disease` | 49 | 6 | 8 | 63 | 0 | 63 | 187 | 337 | 437 |


---
## Crop: Basil

### Model 1 — Crop identification

- Canonical model class: `basil`
- Status: expanded
- Splits: train 51, val 6, test 6
- Processed total: 63
- Additional staged external real images: 0
- **Total unique usable real images: 63**
- Target 400-500: shortage to 400 = 337 ; to 500 = 437

### Model 2 — Disease classification

- Number of disease classes: 1

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `basil__downy_mildew` | 51 | 6 | 6 | 63 | 0 | 63 | 187 | 337 | 437 |


---
## Crop: Cabbage

### Model 1 — Crop identification

- Canonical model class: `cabbage`
- Status: expanded
- Splits: train 220, val 27, test 27
- Processed total: 274
- Additional staged external real images: 0
- **Total unique usable real images: 274**
- Target 400-500: shortage to 400 = 126 ; to 500 = 226
- Health split: 11 healthy / 308 diseased

### Model 2 — Disease classification

- Number of disease classes: 3

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `cabbage__alternaria_leaf_spot` | 47 | 5 | 6 | 58 | 0 | 58 | 192 | 342 | 442 |
| `cabbage__black_rot` | 96 | 11 | 13 | 120 | 0 | 120 | 130 | 280 | 380 |
| `cabbage__downy_mildew` | 68 | 8 | 8 | 84 | 0 | 84 | 166 | 316 | 416 |


---
## Crop: Carrot

### Model 1 — Crop identification

- Canonical model class: `carrot`
- Status: expanded
- Splits: train 118, val 15, test 15
- Processed total: 148
- Additional staged external real images: 0
- **Total unique usable real images: 148**
- Target 400-500: shortage to 400 = 252 ; to 500 = 352

### Model 2 — Disease classification

- Number of disease classes: 3

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `carrot__alternaria_leaf_blight` | 47 | 5 | 7 | 59 | 0 | 59 | 191 | 341 | 441 |
| `carrot__cavity_spot` | 59 | 6 | 7 | 72 | 0 | 72 | 178 | 328 | 428 |
| `carrot__cercospora_leaf_blight` | 13 | 1 | 3 | 17 | 0 | 17 | 233 | 383 | 483 |


---
## Crop: Cauliflower

### Model 1 — Crop identification

- Canonical model class: `cauliflower`
- Status: expanded
- Splits: train 84, val 10, test 10
- Processed total: 104
- Additional staged external real images: 0
- **Total unique usable real images: 104**
- Target 400-500: shortage to 400 = 296 ; to 500 = 396
- Health split: 29 healthy / 81 diseased

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `cauliflower__alternaria_leaf_spot` | 35 | 4 | 4 | 43 | 348 | 391 | 0 | 9 | 109 |
| `cauliflower__bacterial_soft_rot` | 27 | 3 | 2 | 32 | 200 | 232 | 18 | 168 | 268 |


---
## Crop: Celery

### Model 1 — Crop identification

- Canonical model class: `celery`
- Status: expanded
- Splits: train 53, val 6, test 6
- Processed total: 65
- Additional staged external real images: 0
- **Total unique usable real images: 65**
- Target 400-500: shortage to 400 = 335 ; to 500 = 435

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `celery__anthracnose` | 25 | 3 | 1 | 29 | 0 | 29 | 221 | 371 | 471 |
| `celery__early_blight` | 28 | 3 | 5 | 36 | 0 | 36 | 214 | 364 | 464 |


---
## Crop: Cherry

### Model 1 — Crop identification

- Canonical model class: `cherry`
- Status: expanded
- Splits: train 111, val 14, test 14
- Processed total: 139
- Additional staged external real images: 0
- **Total unique usable real images: 139**
- Target 400-500: shortage to 400 = 261 ; to 500 = 361
- Health split: 0 healthy / 90 diseased

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `cherry__leaf_spot` | 86 | 10 | 10 | 106 | 0 | 106 | 144 | 294 | 394 |
| `cherry__powdery_mildew` | 27 | 3 | 3 | 33 | 0 | 33 | 217 | 367 | 467 |


---
## Crop: Citrus

### Model 1 — Crop identification

- Canonical model class: `citrus`
- Status: expanded
- Splits: train 417, val 52, test 52
- Processed total: 521
- Additional staged external real images: 0
- **Total unique usable real images: 521**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0
- Health split: 0 healthy / 306 diseased

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `citrus__canker` | 306 | 34 | 48 | 388 | 0 | 388 | 0 | 12 | 112 |
| `citrus__greening_disease` | 107 | 12 | 14 | 133 | 0 | 133 | 117 | 267 | 367 |


---
## Crop: Coffee

### Model 1 — Crop identification

- Canonical model class: `coffee`
- Status: expanded
- Splits: train 228, val 28, test 28
- Processed total: 284
- Additional staged external real images: 0
- **Total unique usable real images: 284**
- Target 400-500: shortage to 400 = 116 ; to 500 = 216

### Model 2 — Disease classification

- Number of disease classes: 4

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `coffee__berry_blotch` | 86 | 10 | 9 | 105 | 0 | 105 | 145 | 295 | 395 |
| `coffee__black_rot` | 5 | 1 | 0 | 6 | 0 | 6 | 244 | 394 | 494 |
| `coffee__brown_eye_spot` | 12 | 1 | 1 | 14 | 0 | 14 | 236 | 386 | 486 |
| `coffee__leaf_rust` | 129 | 14 | 16 | 159 | 0 | 159 | 91 | 241 | 341 |


---
## Crop: Corn

### Model 1 — Crop identification

- Canonical model class: `corn`
- Status: expanded
- Splits: train 492, val 62, test 62
- Processed total: 616
- Additional staged external real images: 0
- **Total unique usable real images: 616**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- Number of disease classes: 4

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `corn__gray_leaf_spot` | 85 | 10 | 12 | 107 | 0 | 107 | 143 | 293 | 393 |
| `corn__northern_leaf_blight` | 104 | 12 | 14 | 130 | 0 | 130 | 120 | 270 | 370 |
| `corn__rust` | 143 | 16 | 18 | 177 | 0 | 177 | 73 | 223 | 323 |
| `corn__smut` | 165 | 18 | 19 | 202 | 0 | 202 | 48 | 198 | 298 |


---
## Crop: Eggplant

### Model 1 — Crop identification

- Canonical model class: `eggplant`
- Status: expanded
- Splits: train 108, val 14, test 14
- Processed total: 136
- Additional staged external real images: 0
- **Total unique usable real images: 136**
- Target 400-500: shortage to 400 = 264 ; to 500 = 364

### Model 2 — Disease classification

- Number of disease classes: 3

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `eggplant__cercospora_leaf_spot` | 47 | 5 | 6 | 58 | 0 | 58 | 192 | 342 | 442 |
| `eggplant__phomopsis_fruit_rot` | 36 | 4 | 5 | 45 | 0 | 45 | 205 | 355 | 455 |
| `eggplant__phytophthora_blight` | 26 | 3 | 4 | 33 | 0 | 33 | 217 | 367 | 467 |


---
## Crop: Garlic

### Model 1 — Crop identification

- Canonical model class: `garlic`
- Status: expanded
- Splits: train 158, val 20, test 20
- Processed total: 198
- Additional staged external real images: 0
- **Total unique usable real images: 198**
- Target 400-500: shortage to 400 = 202 ; to 500 = 302

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `garlic__leaf_blight` | 72 | 8 | 12 | 92 | 0 | 92 | 158 | 308 | 408 |
| `garlic__rust` | 85 | 9 | 12 | 106 | 0 | 106 | 144 | 294 | 394 |


---
## Crop: Ginger

### Model 1 — Crop identification

- Canonical model class: `ginger`
- Status: expanded
- Splits: train 73, val 9, test 9
- Processed total: 91
- Additional staged external real images: 0
- **Total unique usable real images: 91**
- Target 400-500: shortage to 400 = 309 ; to 500 = 409

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `ginger__leaf_spot` | 19 | 2 | 4 | 25 | 0 | 25 | 225 | 375 | 475 |
| `ginger__sheath_blight` | 52 | 6 | 8 | 66 | 0 | 66 | 184 | 334 | 434 |


---
## Crop: Grape

### Model 1 — Crop identification

- Canonical model class: `grape`
- Status: expanded
- Splits: train 446, val 56, test 56
- Processed total: 558
- Additional staged external real images: 0
- **Total unique usable real images: 558**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- Number of disease classes: 4

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `grape__black_rot` | 97 | 11 | 13 | 121 | 0 | 121 | 129 | 279 | 379 |
| `grape__downy_mildew` | 221 | 25 | 32 | 278 | 0 | 278 | 0 | 122 | 222 |
| `grape__grapevine_leafroll_disease` | 59 | 7 | 5 | 71 | 0 | 71 | 179 | 329 | 429 |
| `grape__leaf_spot` | 70 | 8 | 10 | 88 | 0 | 88 | 162 | 312 | 412 |


---
## Crop: Maple

### Model 1 — Crop identification

- Canonical model class: `maple`
- Status: expanded
- Splits: train 91, val 11, test 11
- Processed total: 113
- Additional staged external real images: 0
- **Total unique usable real images: 113**
- Target 400-500: shortage to 400 = 287 ; to 500 = 387

### Model 2 — Disease classification

- Number of disease classes: 1

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `maple__tar_spot` | 95 | 10 | 8 | 113 | 0 | 113 | 137 | 287 | 387 |


---
## Crop: Peach

### Model 1 — Crop identification

- Canonical model class: `peach`
- Status: expanded
- Splits: train 356, val 44, test 44
- Processed total: 444
- Additional staged external real images: 0
- **Total unique usable real images: 444**
- Target 400-500: shortage to 400 = 0 ; to 500 = 56
- Health split: 0 healthy / 219 diseased

### Model 2 — Disease classification

- Number of disease classes: 5

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `peach__anthracnose` | 11 | 1 | 1 | 13 | 0 | 13 | 237 | 387 | 487 |
| `peach__brown_rot` | 137 | 15 | 14 | 166 | 0 | 166 | 84 | 234 | 334 |
| `peach__leaf_curl` | 148 | 16 | 18 | 182 | 0 | 182 | 68 | 218 | 318 |
| `peach__rust` | 6 | 1 | 1 | 8 | 0 | 8 | 242 | 392 | 492 |
| `peach__scab` | 60 | 7 | 8 | 75 | 0 | 75 | 175 | 325 | 425 |


---
## Crop: Plum

### Model 1 — Crop identification

- Canonical model class: `plum`
- Status: expanded
- Splits: train 171, val 22, test 22
- Processed total: 215
- Additional staged external real images: 0
- **Total unique usable real images: 215**
- Target 400-500: shortage to 400 = 185 ; to 500 = 285
- Health split: 0 healthy / 80 diseased

### Model 2 — Disease classification

- Number of disease classes: 5

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `plum__bacterial_spot` | 13 | 2 | 1 | 16 | 0 | 16 | 234 | 384 | 484 |
| `plum__brown_rot` | 64 | 7 | 5 | 76 | 0 | 76 | 174 | 324 | 424 |
| `plum__pocket_disease` | 48 | 5 | 4 | 57 | 0 | 57 | 193 | 343 | 443 |
| `plum__pox_virus` | 25 | 3 | 4 | 32 | 0 | 32 | 218 | 368 | 468 |
| `plum__rust` | 29 | 3 | 2 | 34 | 0 | 34 | 216 | 366 | 466 |


---
## Crop: Potato

### Model 1 — Crop identification

- Canonical model class: `potato`
- Status: expanded
- Splits: train 191, val 24, test 24
- Processed total: 239
- Additional staged external real images: 0
- **Total unique usable real images: 239**
- Target 400-500: shortage to 400 = 161 ; to 500 = 261

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `potato__early_blight` | 103 | 11 | 10 | 124 | 0 | 124 | 126 | 276 | 376 |
| `potato__late_blight` | 93 | 10 | 12 | 115 | 0 | 115 | 135 | 285 | 385 |


---
## Crop: Raspberry

### Model 1 — Crop identification

- Canonical model class: `raspberry`
- Status: expanded
- Splits: train 99, val 12, test 12
- Processed total: 123
- Additional staged external real images: 0
- **Total unique usable real images: 123**
- Target 400-500: shortage to 400 = 277 ; to 500 = 377
- Health split: 0 healthy / 69 diseased

### Model 2 — Disease classification

- Number of disease classes: 4

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `raspberry__fire_blight` | 24 | 3 | 4 | 31 | 0 | 31 | 219 | 369 | 469 |
| `raspberry__gray_mold` | 32 | 4 | 2 | 38 | 0 | 38 | 212 | 362 | 462 |
| `raspberry__leaf_spot` | 15 | 2 | 1 | 18 | 0 | 18 | 232 | 382 | 482 |
| `raspberry__yellow_rust` | 29 | 3 | 4 | 36 | 0 | 36 | 214 | 364 | 464 |


---
## Crop: Rice

### Model 1 — Crop identification

- Canonical model class: `rice`
- Status: expanded
- Splits: train 123, val 16, test 16
- Processed total: 155
- Additional staged external real images: 0
- **Total unique usable real images: 155**
- Target 400-500: shortage to 400 = 245 ; to 500 = 345

### Model 2 — Disease classification

- Number of disease classes: 2

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `rice__blast` | 68 | 8 | 7 | 83 | 0 | 83 | 167 | 317 | 417 |
| `rice__sheath_blight` | 58 | 6 | 8 | 72 | 0 | 72 | 178 | 328 | 428 |


---
## Crop: Soybean

### Model 1 — Crop identification

- Canonical model class: `soybean`
- Status: expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- Number of disease classes: 6

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `soybean__bacterial_blight` | 70 | 8 | 9 | 87 | 0 | 87 | 163 | 313 | 413 |
| `soybean__brown_spot` | 49 | 5 | 7 | 61 | 0 | 61 | 189 | 339 | 439 |
| `soybean__downy_mildew` | 111 | 12 | 11 | 134 | 0 | 134 | 116 | 266 | 366 |
| `soybean__frog_eye_leaf_spot` | 170 | 19 | 21 | 210 | 0 | 210 | 40 | 190 | 290 |
| `soybean__mosaic` | 92 | 10 | 13 | 115 | 0 | 115 | 135 | 285 | 385 |
| `soybean__rust` | 455 | 51 | 9 | 515 | 0 | 515 | 0 | 0 | 0 |


---
## Crop: Tobacco

### Model 1 — Crop identification

- Canonical model class: `tobacco`
- Status: expanded
- Splits: train 142, val 18, test 18
- Processed total: 178
- Additional staged external real images: 0
- **Total unique usable real images: 178**
- Target 400-500: shortage to 400 = 222 ; to 500 = 322

### Model 2 — Disease classification

- Number of disease classes: 4

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tobacco__blue_mold` | 45 | 5 | 5 | 55 | 0 | 55 | 195 | 345 | 445 |
| `tobacco__brown_spot` | 49 | 6 | 7 | 62 | 0 | 62 | 188 | 338 | 438 |
| `tobacco__frogeye_leaf_spot` | 15 | 2 | 3 | 20 | 0 | 20 | 230 | 380 | 480 |
| `tobacco__mosaic_virus` | 32 | 4 | 5 | 41 | 0 | 41 | 209 | 359 | 459 |


---
## Crop: Wheat

### Model 1 — Crop identification

- Canonical model class: `wheat`
- Status: expanded
- Splits: train 500, val 65, test 65
- Processed total: 630
- Additional staged external real images: 0
- **Total unique usable real images: 630**
- Target 400-500: shortage to 400 = 0 ; to 500 = 0

### Model 2 — Disease classification

- Number of disease classes: 8

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `wheat__bacterial_leaf_streak_(black_chaff)` | 92 | 10 | 13 | 115 | 0 | 115 | 135 | 285 | 385 |
| `wheat__head_scab` | 221 | 24 | 30 | 275 | 0 | 275 | 0 | 125 | 225 |
| `wheat__leaf_rust` | 105 | 12 | 11 | 128 | 0 | 128 | 122 | 272 | 372 |
| `wheat__loose_smut` | 154 | 17 | 19 | 190 | 0 | 190 | 60 | 210 | 310 |
| `wheat__powdery_mildew` | 211 | 24 | 27 | 262 | 0 | 262 | 0 | 138 | 238 |
| `wheat__septoria_blotch` | 164 | 18 | 19 | 201 | 0 | 201 | 49 | 199 | 299 |
| `wheat__stem_rust` | 111 | 12 | 13 | 136 | 0 | 136 | 114 | 264 | 364 |
| `wheat__stripe_rust` | 264 | 29 | 32 | 325 | 0 | 325 | 0 | 75 | 175 |


---
## Crop: Bean

### Model 1 — Crop identification

- No Model 1 dataset available (not in either taxonomy).

### Model 2 — Disease classification

- Number of disease classes: 4

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bean__angular_leaf_spot` | 330 | 37 | 65 | 432 | 0 | 432 | 0 | 0 | 68 |
| `bean__halo_blight` | 45 | 5 | 6 | 56 | 0 | 56 | 194 | 344 | 444 |
| `bean__mosaic_virus` | 47 | 5 | 5 | 57 | 0 | 57 | 193 | 343 | 443 |
| `bean__rust` | 471 | 52 | 77 | 600 | 0 | 600 | 0 | 0 | 0 |


---
## Crop: Bell_Pepper

### Model 1 — Crop identification

- No Model 1 dataset available (not in either taxonomy).

### Model 2 — Disease classification

- Number of disease classes: 4

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bell_pepper__bacterial_spot` | 55 | 6 | 7 | 68 | 4,080 | 4,148 | 0 | 0 | 0 |
| `bell_pepper__blossom_end_rot` | 87 | 10 | 11 | 108 | 0 | 108 | 142 | 292 | 392 |
| `bell_pepper__frogeye_leaf_spot` | 22 | 2 | 4 | 28 | 0 | 28 | 222 | 372 | 472 |
| `bell_pepper__powdery_mildew` | 22 | 2 | 2 | 26 | 195 | 221 | 29 | 179 | 279 |


---
## Crop: Squash

### Model 1 — Crop identification

- No Model 1 dataset available (not in either taxonomy).

### Model 2 — Disease classification

- Number of disease classes: 1

| Disease class | Train | Val | Test | Processed | External/staged | Unique real | Short 250 | Short 400 | Short 500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `squash__powdery_mildew` | 139 | 15 | 20 | 174 | 0 | 174 | 76 | 226 | 326 |


---
## Additional external disease categories NOT yet in Model 2 taxonomy

These are reported separately and were NOT added to any taxonomy. Verify labels before approval.

### Cauliflower Dataset (downloaded)

Fruit folders:
- Alternaria Brassicae: 44 images [maps to alternaria_leaf_spot - FRUIT part]
- Bacterial Soft Rot: 200 images [maps to bacterial_soft_rot - FRUIT part]
- Bacterial Spot: 403 images [not in taxonomy]
- Bacterial spot rot: 168 images [AMBIGUOUS vs 'Bacterial Spot']
- Black Spot: 251 images [not in taxonomy]
- Purple Tinges: 153 images [not in taxonomy]
- healthy: 206 images [crop-specific healthy]
Leaf folders:
- Alternaria Leaf Spot: 304 images [maps to alternaria_leaf_spot - LEAF part]
- Black Rot: 1,188 images [not in taxonomy]
- Downy Mildew: 434 images [not in taxonomy]
- Healthy: 1,804 images [crop-specific healthy]
- Insect Hole: 639 images [not in taxonomy]

### Pepper Bell Leaf Disease (downloaded)

- Bacterial Spot: 4,080 images [maps to bacterial_spot]
- Cercospora Leaf Spot: 1,572 images [not in taxonomy]
- Healthy: 1,524 images [crop-specific healthy]
- Leaf Curl: 423 images [not in taxonomy]
- Nutrition Deficiency: 444 images [not in taxonomy]
- Powdery Mildew: 195 images [maps to powdery_mildew]


---
## Summary & priorities

### Top 15 most urgent classes (from acquisition_priority.csv)

| # | Priority | Model | Class | Current unique | Shortage to 400 | Reason |
|---:|---|---|---|---:|---:|---|
| 1 | P1 | Model2 | `coffee__black_rot` | 6 | 394 | Model2 disease <100 (critical) |
| 2 | P1 | Model2 | `peach__rust` | 8 | 392 | Model2 disease <100 (critical) |
| 3 | P1 | Model2 | `broccoli__ring_spot` | 10 | 390 | Model2 disease <100 (critical) |
| 4 | P1 | Model2 | `peach__anthracnose` | 13 | 387 | Model2 disease <100 (critical) |
| 5 | P1 | Model2 | `coffee__brown_eye_spot` | 14 | 386 | Model2 disease <100 (critical) |
| 6 | P1 | Model2 | `plum__bacterial_spot` | 16 | 384 | Model2 disease <100 (critical) |
| 7 | P1 | Model2 | `carrot__cercospora_leaf_blight` | 17 | 383 | Model2 disease <100 (critical) |
| 8 | P1 | Model2 | `raspberry__leaf_spot` | 18 | 382 | Model2 disease <100 (critical) |
| 9 | P1 | Model2 | `tobacco__frogeye_leaf_spot` | 20 | 380 | Model2 disease <100 (critical) |
| 10 | P1 | Model2 | `ginger__leaf_spot` | 25 | 375 | Model2 disease <100 (critical) |
| 11 | P1 | Model2 | `bell_pepper__frogeye_leaf_spot` | 28 | 372 | Model2 disease <100 (critical) |
| 12 | P1 | Model2 | `broccoli__downy_mildew` | 29 | 371 | Model2 disease <100 (critical) |
| 13 | P1 | Model2 | `celery__anthracnose` | 29 | 371 | Model2 disease <100 (critical) |
| 14 | P1 | Model2 | `raspberry__fire_blight` | 31 | 369 | Model2 disease <100 (critical) |
| 15 | P1 | Model2 | `plum__pox_virus` | 32 | 368 | Model2 disease <100 (critical) |

### Zero / near-zero disease classes
- Zero unique images: none
- Zero-image Model 1 crops: cherry_tomato
- Chilli: no dataset currently available (0 Model1, no Model2 class).
- Mango: excluded by project scope (do not collect).