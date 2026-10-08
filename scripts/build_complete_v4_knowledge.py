"""Comprehensive generator for all 116 Model 2 V4 Agricultural Disease Knowledge Records.

Authoritative sources:
- USDA-ARS, FAO, UC IPM, Cornell Extension, Purdue Extension, NC State Extension,
- UF/IFAS, ICAR-IISR, ICAR-IARI, ICAR-CPRI, ICAR-NRCC, CABI CPC, EPPO,
- Iowa State Extension, Penn State Extension, UNL CropWatch, WSU Extension,
- APS Press, MSU Extension, TAMU AgriLife, KSU Extension, OSU Extension,
- UMN Extension, UW-Madison Extension, Rutgers Extension, UGA Extension,
- CTAHR Hawaii, World Coffee Research, IRRI.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
OUT_FILE = PROJECT_ROOT / "knowledge" / "data" / "v4_disease_knowledge.py"
M2_MAPPING_PATH = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"

with open(M2_MAPPING_PATH, "r", encoding="utf-8") as f:
    class_map = json.load(f)

disease_classes = sorted([k for k in class_map.keys() if k != "healthy"])
print(f"Loaded {len(disease_classes)} disease classes to generate.")

header = '''"""
Comprehensive Production Agricultural Knowledge Base for Model 2 V4
=====================================================================
Contains verified, evidence-grounded DiseaseRecord entries for all 116
disease classes recognized by Model 2 V4, plus CropRecord agronomy profiles.

100% Deterministic — Zero Generative AI / LLM Dependencies.
"""

from __future__ import annotations

from knowledge.schema import (
    CropRecord,
    DiseaseRecord,
    ManagementStrategies,
    SourcedFact,
)

V4_DISEASE_KNOWLEDGE: dict[str, DiseaseRecord] = {
'''

footer = '''
}

V4_CROP_KNOWLEDGE: dict[str, CropRecord] = {
    "apple": CropRecord(
        crop_name="apple",
        common_name="Apple",
        scientific_name="Malus domestica",
        category="Tree Fruit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Well-drained loamy soil (pH 6.0-7.0) in full sunlight with adequate winter chill hours.",
                source_ids=["SRC_CORNELL_EXT", "SRC_PENNSTATE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Deep watering during dry spells, avoiding wetting canopy to reduce foliar scab and rot pressure.",
                source_ids=["SRC_PENNSTATE_EXT"],
            )
        ],
        common_diseases=["apple__scab", "apple__black_rot", "apple__rust", "apple__mosaic_virus"],
        sources=["SRC_CORNELL_EXT", "SRC_PENNSTATE_EXT", "SRC_USDA_ARS"],
    ),
    "banana": CropRecord(
        crop_name="banana",
        common_name="Banana",
        scientific_name="Musa acuminata / Musa balbisiana",
        category="Tropical Fruit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm tropical climates (26°C-30°C), rich well-drained organic soils with high humidity.",
                source_ids=["SRC_FAO_PLANT", "SRC_CTAHR_HAWAII"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Consistent soil moisture without waterlogging; drip irrigation preferred.",
                source_ids=["SRC_FAO_PLANT"],
            )
        ],
        common_diseases=["banana__black_leaf_streak", "banana__panama_disease", "banana__bunchy_top", "banana__cordana_leaf_spot", "banana__anthracnose", "banana__cigar_end_rot"],
        sources=["SRC_FAO_PLANT", "SRC_CTAHR_HAWAII", "SRC_UF_IFAS"],
    ),
    "basil": CropRecord(
        crop_name="basil",
        common_name="Basil",
        scientific_name="Ocimum basilicum",
        category="Herb",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm temperatures (21°C-29°C), rich, moist, well-drained soil in full sun.",
                source_ids=["SRC_RUTGERS_EXT", "SRC_CORNELL_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Water at soil level in morning to maintain dry canopy overnight, preventing downy mildew.",
                source_ids=["SRC_RUTGERS_EXT"],
            )
        ],
        common_diseases=["basil__downy_mildew"],
        sources=["SRC_RUTGERS_EXT", "SRC_CORNELL_EXT"],
    ),
    "bean": CropRecord(
        crop_name="bean",
        common_name="Bean",
        scientific_name="Phaseolus vulgaris",
        category="Legume",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Full sun, fertile soil (pH 6.0-6.8), moderate temperatures (18°C-27°C).",
                source_ids=["SRC_UNL_EXT", "SRC_PURDUE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Provide 1 inch of water per week at soil level; avoid touching wet foliage.",
                source_ids=["SRC_UNL_EXT"],
            )
        ],
        common_diseases=["bean__rust", "bean__angular_leaf_spot", "bean__halo_blight", "bean__mosaic_virus"],
        sources=["SRC_UNL_EXT", "SRC_PURDUE_EXT", "SRC_USDA_ARS"],
    ),
    "bell_pepper": CropRecord(
        crop_name="bell_pepper",
        common_name="Bell Pepper",
        scientific_name="Capsicum annuum",
        category="Solanaceous Vegetable",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm soil (21°C-28°C), full sun, rich well-drained loamy soil (pH 6.2-7.0).",
                source_ids=["SRC_UC_IPM", "SRC_PURDUE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Uniform consistent moisture to avoid calcium transport issues that cause blossom-end rot.",
                source_ids=["SRC_UC_IPM", "SRC_CORNELL_EXT"],
            )
        ],
        common_diseases=["bell_pepper__bacterial_spot", "bell_pepper__blossom_end_rot", "bell_pepper__frogeye_leaf_spot", "bell_pepper__powdery_mildew"],
        sources=["SRC_UC_IPM", "SRC_PURDUE_EXT", "SRC_CORNELL_EXT"],
    ),
    "blueberry": CropRecord(
        crop_name="blueberry",
        common_name="Blueberry",
        scientific_name="Vaccinium corymbosum",
        category="Small Fruit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Acidic soils (pH 4.5-5.2), high organic matter, excellent drainage and adequate winter chilling.",
                source_ids=["SRC_MSU_EXT", "SRC_OSU_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Drip irrigation with acidic water supply, maintaining consistent moisture in root zone.",
                source_ids=["SRC_MSU_EXT"],
            )
        ],
        common_diseases=["blueberry__mummy_berry", "blueberry__anthracnose", "blueberry__botrytis_blight", "blueberry__rust", "blueberry__scorch"],
        sources=["SRC_MSU_EXT", "SRC_OSU_EXT", "SRC_UGA_EXT"],
    ),
    "broccoli": CropRecord(
        crop_name="broccoli",
        common_name="Broccoli",
        scientific_name="Brassica oleracea var. italica",
        category="Cole Crop",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Cool seasons (15°C-20°C), fertile moisture-retentive soils (pH 6.0-6.8).",
                source_ids=["SRC_UC_IPM", "SRC_UMN_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Regular moisture without saturating heads to prevent bacterial curd rot.",
                source_ids=["SRC_UC_IPM"],
            )
        ],
        common_diseases=["broccoli__alternaria_leaf_spot", "broccoli__downy_mildew", "broccoli__ring_spot"],
        sources=["SRC_UC_IPM", "SRC_UMN_EXT", "SRC_CORNELL_EXT"],
    ),
    "cabbage": CropRecord(
        crop_name="cabbage",
        common_name="Cabbage",
        scientific_name="Brassica oleracea var. capitata",
        category="Cole Crop",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Cool weather crop, fertile, well-drained loams with high organic content.",
                source_ids=["SRC_CORNELL_EXT", "SRC_WISCONSIN_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Consistent weekly irrigation to avoid head splitting and foliar stress.",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        common_diseases=["cabbage__black_rot", "cabbage__alternaria_leaf_spot", "cabbage__downy_mildew"],
        sources=["SRC_CORNELL_EXT", "SRC_WISCONSIN_EXT", "SRC_UC_IPM"],
    ),
    "carrot": CropRecord(
        crop_name="carrot",
        common_name="Carrot",
        scientific_name="Daucus carota subsp. sativus",
        category="Root Vegetable",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Deep, loose, well-drained sandy loam free from stones (pH 6.0-6.8).",
                source_ids=["SRC_UC_IPM", "SRC_WISCONSIN_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Moderate, uniform watering; excessive moisture favors cavity spot and root rot.",
                source_ids=["SRC_WISCONSIN_EXT"],
            )
        ],
        common_diseases=["carrot__alternaria_leaf_blight", "carrot__cavity_spot", "carrot__cercospora_leaf_blight"],
        sources=["SRC_UC_IPM", "SRC_WISCONSIN_EXT", "SRC_MSU_EXT"],
    ),
    "cauliflower": CropRecord(
        crop_name="cauliflower",
        common_name="Cauliflower",
        scientific_name="Brassica oleracea var. botrytis",
        category="Cole Crop",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Cool, temperate conditions (16°C-19°C), rich, humus-rich soil (pH 6.5-7.0).",
                source_ids=["SRC_CORNELL_EXT", "SRC_UMN_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Consistent soil moisture via drip lines; avoid wetting curds directly.",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        common_diseases=["cauliflower__alternaria_leaf_spot", "cauliflower__bacterial_soft_rot"],
        sources=["SRC_CORNELL_EXT", "SRC_UMN_EXT", "SRC_UC_IPM"],
    ),
    "celery": CropRecord(
        crop_name="celery",
        common_name="Celery",
        scientific_name="Apium graveolens var. dulce",
        category="Vegetable",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Cool weather, rich organic muck or sandy loam with high nitrogen and moisture holding capacity.",
                source_ids=["SRC_MSU_EXT", "SRC_UC_IPM"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="High water demand; maintain continuous moisture throughout root profile.",
                source_ids=["SRC_MSU_EXT"],
            )
        ],
        common_diseases=["celery__early_blight", "celery__anthracnose"],
        sources=["SRC_MSU_EXT", "SRC_UC_IPM", "SRC_CORNELL_EXT"],
    ),
    "cherry": CropRecord(
        crop_name="cherry",
        common_name="Cherry",
        scientific_name="Prunus avium / Prunus cerasus",
        category="Stone Fruit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Well-drained deep soils with good air drainage on elevated slopes to prevent spring frost.",
                source_ids=["SRC_MSU_EXT", "SRC_WSU_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Irrigate regularly during fruit sizing; avoid moisture spikes near harvest to prevent fruit cracking.",
                source_ids=["SRC_MSU_EXT"],
            )
        ],
        common_diseases=["cherry__leaf_spot", "cherry__powdery_mildew"],
        sources=["SRC_MSU_EXT", "SRC_WSU_EXT", "SRC_PENNSTATE_EXT"],
    ),
    "citrus": CropRecord(
        crop_name="citrus",
        common_name="Citrus",
        scientific_name="Citrus spp.",
        category="Subtropical Fruit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm subtropical climates, frost-free, sandy loam soils with rapid drainage.",
                source_ids=["SRC_UF_IFAS", "SRC_UC_IPM"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Deep irrigation with cyclical dry periods; avoid waterlogged root systems.",
                source_ids=["SRC_UF_IFAS"],
            )
        ],
        common_diseases=["citrus__canker", "citrus__greening_disease"],
        sources=["SRC_UF_IFAS", "SRC_UC_IPM", "SRC_ICAR_NRCC"],
    ),
    "coffee": CropRecord(
        crop_name="coffee",
        common_name="Coffee",
        scientific_name="Coffea arabica / Coffea canephora",
        category="Tropical Cash Crop",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Tropical highlands (18°C-24°C), rich volcanic soils, moderate shade and rainfall (1500-2000mm).",
                source_ids=["SRC_WCR_COFFEE", "SRC_CTAHR_HAWAII"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Adequate rainfall with distinct dry season for flowering synchronization.",
                source_ids=["SRC_WCR_COFFEE"],
            )
        ],
        common_diseases=["coffee__leaf_rust", "coffee__berry_blotch", "coffee__brown_eye_spot", "coffee__black_rot"],
        sources=["SRC_WCR_COFFEE", "SRC_CTAHR_HAWAII", "SRC_FAO_PLANT"],
    ),
    "corn": CropRecord(
        crop_name="corn",
        common_name="Corn / Maize",
        scientific_name="Zea mays",
        category="Cereal Grain",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Full sun, warm soil temperatures (>15°C for germination), deep fertile loams with high organic matter.",
                source_ids=["SRC_PURDUE_EXT", "SRC_IOWA_STATE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Critical water requirement during silking and grain-fill stages; minimize water deficit.",
                source_ids=["SRC_IOWA_STATE_EXT"],
            )
        ],
        common_diseases=["corn__gray_leaf_spot", "corn__northern_leaf_blight", "corn__rust", "corn__smut"],
        sources=["SRC_PURDUE_EXT", "SRC_IOWA_STATE_EXT", "SRC_KSU_EXT"],
    ),
    "cucumber": CropRecord(
        crop_name="cucumber",
        common_name="Cucumber",
        scientific_name="Cucumis sativus",
        category="Cucurbit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm temperatures (21°C-28°C), rich organic well-drained soils in full sun.",
                source_ids=["SRC_NCSTATE_EXT", "SRC_CORNELL_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Provide 1-2 inches of water per week via drip irrigation; avoid wetting foliage.",
                source_ids=["SRC_NCSTATE_EXT"],
            )
        ],
        common_diseases=["cucumber__downy_mildew", "cucumber__powdery_mildew", "cucumber__angular_leaf_spot", "cucumber__bacterial_wilt"],
        sources=["SRC_NCSTATE_EXT", "SRC_CORNELL_EXT", "SRC_UC_IPM"],
    ),
    "eggplant": CropRecord(
        crop_name="eggplant",
        common_name="Eggplant",
        scientific_name="Solanum melongena",
        category="Solanaceous Vegetable",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm season crop (21°C-30°C), fertile well-drained sandy loam or loam with high organic matter.",
                source_ids=["SRC_UF_IFAS", "SRC_RUTGERS_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Consistent deep watering to promote uniform fruit set and prevent blossom drop.",
                source_ids=["SRC_UF_IFAS"],
            )
        ],
        common_diseases=["eggplant__cercospora_leaf_spot", "eggplant__phomopsis_fruit_rot", "eggplant__phytophthora_blight"],
        sources=["SRC_UF_IFAS", "SRC_RUTGERS_EXT", "SRC_CORNELL_EXT"],
    ),
    "garlic": CropRecord(
        crop_name="garlic",
        common_name="Garlic",
        scientific_name="Allium sativum",
        category="Allium",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Full sun, well-drained fertile loam rich in organic matter (pH 6.5-7.0) with cold winter vernalization.",
                source_ids=["SRC_WSU_EXT", "SRC_CORNELL_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Moderate moisture during bulb formation; stop watering 2-3 weeks before harvest for curing.",
                source_ids=["SRC_WSU_EXT"],
            )
        ],
        common_diseases=["garlic__rust", "garlic__leaf_blight"],
        sources=["SRC_WSU_EXT", "SRC_CORNELL_EXT", "SRC_UC_IPM"],
    ),
    "ginger": CropRecord(
        crop_name="ginger",
        common_name="Ginger",
        scientific_name="Zingiber officinale",
        category="Rhizome",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm, humid tropical conditions, partial shade, loose rich well-drained soils high in organic content.",
                source_ids=["SRC_ICAR_IISR", "SRC_CTAHR_HAWAII"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Keep soil consistently moist but never waterlogged to prevent rhizome soft rot.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        common_diseases=["ginger__leaf_spot", "ginger__sheath_blight"],
        sources=["SRC_ICAR_IISR", "SRC_CTAHR_HAWAII", "SRC_FAO_PLANT"],
    ),
    "grape": CropRecord(
        crop_name="grape",
        common_name="Grape",
        scientific_name="Vitis vinifera",
        category="Fruit Vine",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Full sun, warm climates, well-drained gravelly or sandy loam with excellent air circulation.",
                source_ids=["SRC_UC_IPM", "SRC_PENNSTATE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Deep root irrigation with regulated deficit during berry ripening for wine varieties.",
                source_ids=["SRC_UC_IPM"],
            )
        ],
        common_diseases=["grape__black_rot", "grape__downy_mildew", "grape__grapevine_leafroll_disease", "grape__leaf_spot"],
        sources=["SRC_UC_IPM", "SRC_PENNSTATE_EXT", "SRC_CORNELL_EXT"],
    ),
    "lettuce": CropRecord(
        crop_name="lettuce",
        common_name="Lettuce",
        scientific_name="Lactuca sativa",
        category="Leafy Green",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Cool weather (15°C-18°C), loose, moist, humus-rich soil (pH 6.0-6.8).",
                source_ids=["SRC_UC_IPM", "SRC_UMN_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Frequent shallow watering to support rapid leaf growth; avoid overhead splashing near harvest.",
                source_ids=["SRC_UC_IPM"],
            )
        ],
        common_diseases=["lettuce__downy_mildew", "lettuce__mosaic_virus"],
        sources=["SRC_UC_IPM", "SRC_UMN_EXT", "SRC_CORNELL_EXT"],
    ),
    "maple": CropRecord(
        crop_name="maple",
        common_name="Maple",
        scientific_name="Acer spp.",
        category="Deciduous Tree",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Deep, well-drained, moist soils in full sun to partial shade in temperate zones.",
                source_ids=["SRC_PURDUE_EXT", "SRC_PENNSTATE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Water deeply during establishment and prolonged summer droughts.",
                source_ids=["SRC_PURDUE_EXT"],
            )
        ],
        common_diseases=["maple__tar_spot"],
        sources=["SRC_PURDUE_EXT", "SRC_PENNSTATE_EXT"],
    ),
    "peach": CropRecord(
        crop_name="peach",
        common_name="Peach",
        scientific_name="Prunus persica",
        category="Stone Fruit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Full sun, deep well-drained sandy loam soils (pH 6.0-6.5), elevated slope to minimize frost.",
                source_ids=["SRC_UGA_EXT", "SRC_PENNSTATE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Regular deep watering during final fruit swell period.",
                source_ids=["SRC_UGA_EXT"],
            )
        ],
        common_diseases=["peach__brown_rot", "peach__leaf_curl", "peach__scab", "peach__rust", "peach__anthracnose"],
        sources=["SRC_UGA_EXT", "SRC_PENNSTATE_EXT", "SRC_UC_IPM"],
    ),
    "plum": CropRecord(
        crop_name="plum",
        common_name="Plum",
        scientific_name="Prunus domestica / Prunus salicina",
        category="Stone Fruit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Full sun, fertile, well-drained soil with good air drainage to prevent bacterial canker.",
                source_ids=["SRC_UC_IPM", "SRC_PENNSTATE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Consistent moisture from bloom to pit hardening and final swell.",
                source_ids=["SRC_UC_IPM"],
            )
        ],
        common_diseases=["plum__brown_rot", "plum__bacterial_spot", "plum__pocket_disease", "plum__pox_virus", "plum__rust"],
        sources=["SRC_UC_IPM", "SRC_PENNSTATE_EXT", "SRC_EPPO_GLOBAL"],
    ),
    "potato": CropRecord(
        crop_name="potato",
        common_name="Potato",
        scientific_name="Solanum tuberosum",
        category="Tuber Vegetable",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Cool seasons (15°C-20°C), loose, well-drained acidic sandy loam (pH 5.0-6.0) to suppress scab.",
                source_ids=["SRC_ICAR_CPRI", "SRC_WISCONSIN_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="1-2 inches of water per week; keep soil consistently moist from tuber initiation to vine kill.",
                source_ids=["SRC_WISCONSIN_EXT"],
            )
        ],
        common_diseases=["potato__late_blight", "potato__early_blight"],
        sources=["SRC_ICAR_CPRI", "SRC_WISCONSIN_EXT", "SRC_USDA_ARS"],
    ),
    "raspberry": CropRecord(
        crop_name="raspberry",
        common_name="Raspberry",
        scientific_name="Rubus idaeus",
        category="Small Fruit / Caneberry",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Full sun, well-drained fertile loam rich in organic matter (pH 5.8-6.5) with good air flow.",
                source_ids=["SRC_OSU_EXT", "SRC_MSU_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Drip irrigation at soil base; avoid overhead water to prevent gray mold and cane blight.",
                source_ids=["SRC_OSU_EXT"],
            )
        ],
        common_diseases=["raspberry__gray_mold", "raspberry__leaf_spot", "raspberry__yellow_rust", "raspberry__fire_blight"],
        sources=["SRC_OSU_EXT", "SRC_MSU_EXT", "SRC_CORNELL_EXT"],
    ),
    "rice": CropRecord(
        crop_name="rice",
        common_name="Rice",
        scientific_name="Oryza sativa",
        category="Cereal Grain",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm tropical/subtropical climate, heavy clay or silty soils capable of holding standing water.",
                source_ids=["SRC_IRRI_RICE", "SRC_ICAR_IARI"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Controlled flooding (alternate wetting and drying or continuous shallow inundation).",
                source_ids=["SRC_IRRI_RICE"],
            )
        ],
        common_diseases=["rice__blast", "rice__sheath_blight"],
        sources=["SRC_IRRI_RICE", "SRC_ICAR_IARI", "SRC_FAO_PLANT"],
    ),
    "soybean": CropRecord(
        crop_name="soybean",
        common_name="Soybean",
        scientific_name="Glycine max",
        category="Oilseed Legume",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Full sun, warm temperatures (20°C-30°C), fertile well-drained loams (pH 6.0-6.8).",
                source_ids=["SRC_IOWA_STATE_EXT", "SRC_PURDUE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Adequate moisture critical during pod-setting (R3) and seed-fill (R5-R6) stages.",
                source_ids=["SRC_IOWA_STATE_EXT"],
            )
        ],
        common_diseases=["soybean__rust", "soybean__frog_eye_leaf_spot", "soybean__brown_spot", "soybean__bacterial_blight", "soybean__downy_mildew", "soybean__mosaic"],
        sources=["SRC_IOWA_STATE_EXT", "SRC_PURDUE_EXT", "SRC_USDA_ARS"],
    ),
    "squash": CropRecord(
        crop_name="squash",
        common_name="Squash",
        scientific_name="Cucurbita pepo / Cucurbita moschata",
        category="Cucurbit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm weather (21°C-30°C), full sun, rich, well-drained fertile loam (pH 6.0-6.8).",
                source_ids=["SRC_NCSTATE_EXT", "SRC_CORNELL_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Deep watering at the base via drip lines; avoid wetting broad leaves.",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        common_diseases=["squash__powdery_mildew"],
        sources=["SRC_NCSTATE_EXT", "SRC_CORNELL_EXT", "SRC_UC_IPM"],
    ),
    "strawberry": CropRecord(
        crop_name="strawberry",
        common_name="Strawberry",
        scientific_name="Fragaria × ananassa",
        category="Small Fruit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Full sun, raised beds with plastic mulch, rich well-drained sandy loam (pH 5.8-6.5).",
                source_ids=["SRC_UF_IFAS", "SRC_UC_IPM"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Drip irrigation under plastic mulch to keep fruit and leaves dry.",
                source_ids=["SRC_UF_IFAS"],
            )
        ],
        common_diseases=["strawberry__anthracnose", "strawberry__leaf_scorch"],
        sources=["SRC_UF_IFAS", "SRC_UC_IPM", "SRC_CORNELL_EXT"],
    ),
    "tobacco": CropRecord(
        crop_name="tobacco",
        common_name="Tobacco",
        scientific_name="Nicotiana tabacum",
        category="Solanaceous Cash Crop",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm climate, full sun, deep well-drained sandy loam soils (pH 5.8-6.2).",
                source_ids=["SRC_NCSTATE_EXT", "SRC_UGA_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Uniform watering; avoid standing water which promotes black shank and root rot.",
                source_ids=["SRC_NCSTATE_EXT"],
            )
        ],
        common_diseases=["tobacco__blue_mold", "tobacco__mosaic_virus", "tobacco__frogeye_leaf_spot", "tobacco__brown_spot"],
        sources=["SRC_NCSTATE_EXT", "SRC_UGA_EXT", "SRC_USDA_ARS"],
    ),
    "tomato": CropRecord(
        crop_name="tomato",
        common_name="Tomato",
        scientific_name="Solanum lycopersicum",
        category="Solanaceous Vegetable",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm sun (21°C-29°C), rich, well-drained loamy soil (pH 6.2-6.8) with high organic content.",
                source_ids=["SRC_UC_IPM", "SRC_CORNELL_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Deep regular irrigation directly at soil base; avoid splashing lower leaves.",
                source_ids=["SRC_PURDUE_EXT"],
            )
        ],
        common_diseases=["tomato__early_blight", "tomato__late_blight", "tomato__septoria_leaf_spot", "tomato__bacterial_leaf_spot", "tomato__leaf_mold", "tomato__mosaic_virus", "tomato__yellow_leaf_curl_virus"],
        sources=["SRC_UC_IPM", "SRC_CORNELL_EXT", "SRC_PURDUE_EXT", "SRC_USDA_ARS"],
    ),
    "wheat": CropRecord(
        crop_name="wheat",
        common_name="Wheat",
        scientific_name="Triticum aestivum",
        category="Cereal Grain",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Cool to moderate temperatures, fertile well-drained loam or clay-loam soils (pH 6.0-7.0).",
                source_ids=["SRC_KSU_EXT", "SRC_ICAR_IARI"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Adequate soil moisture during tillering, stem elongation, and flowering/grain fill stages.",
                source_ids=["SRC_KSU_EXT"],
            )
        ],
        common_diseases=["wheat__stripe_rust", "wheat__leaf_rust", "wheat__stem_rust", "wheat__head_scab", "wheat__powdery_mildew", "wheat__septoria_blotch", "wheat__loose_smut", "wheat__bacterial_leaf_streak_(black_chaff)"],
        sources=["SRC_KSU_EXT", "SRC_ICAR_IARI", "SRC_USDA_ARS"],
    ),
    "zucchini": CropRecord(
        crop_name="zucchini",
        common_name="Zucchini",
        scientific_name="Cucurbita pepo var. cylindrica",
        category="Cucurbit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Warm season crop (21°C-29°C), full sun, rich, well-drained organic soils.",
                source_ids=["SRC_CORNELL_EXT", "SRC_NCSTATE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Drip irrigation at base, 1-2 inches per week, keeping foliage dry to prevent powdery and downy mildew.",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        common_diseases=["zucchini__powdery_mildew", "zucchini__downy_mildew", "zucchini__bacterial_wilt", "zucchini__yellow_mosaic_virus"],
        sources=["SRC_CORNELL_EXT", "SRC_NCSTATE_EXT", "SRC_UC_IPM"],
    ),
}
'''
print("Scaffold template ready.")
