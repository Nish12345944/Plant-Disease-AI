"""
Verified Agricultural Source Registry & Provenance Database
===========================================================
Defines authoritative, traceable references from Tier-1 (USDA, FAO, ICAR)
and Tier-2 (University Extensions) plant pathology institutions.
"""

from __future__ import annotations

from typing import Any, Optional

from knowledge.schema import SourceRecord, SourceTier

SOURCE_REGISTRY: dict[str, SourceRecord] = {
    "SRC_USDA_ARS": SourceRecord(
        source_id="SRC_USDA_ARS",
        title="USDA Agricultural Research Service Plant Disease Management Compendium",
        organization="United States Department of Agriculture (USDA-ARS)",
        url_or_doi="https://www.ars.usda.gov/research/plant-diseases/",
        publication_year=2024,
        source_tier=SourceTier.TIER_1,
        notes="National research standards for fungal, viral, and bacterial agronomic pathology.",
        is_general=True,
    ),
    "SRC_FAO_PLANT": SourceRecord(
        source_id="SRC_FAO_PLANT",
        title="FAO Integrated Pest and Disease Management Guidelines",
        organization="Food and Agriculture Organization of the United Nations (FAO)",
        url_or_doi="https://www.fao.org/pest-and-pesticide-management/ipm/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Global standards for integrated crop management and sustainable pest suppression.",
        is_general=True,
    ),
    "SRC_UC_IPM": SourceRecord(
        source_id="SRC_UC_IPM",
        title="University of California Statewide Integrated Pest Management Program (UC IPM)",
        organization="University of California Agriculture and Natural Resources",
        url_or_doi="https://ipm.ucanr.edu/PMG/crops-agriculture.html",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Peer-reviewed agricultural pest and pathogen management guidelines.",
        is_general=True,
    ),
    "SRC_CORNELL_EXT": SourceRecord(
        source_id="SRC_CORNELL_EXT",
        title="Cornell Cooperative Extension Vegetable Pathology and Diagnostic Factsheets",
        organization="Cornell University College of Agriculture and Life Sciences",
        url_or_doi="https://www.vegetables.cornell.edu/pest-management/disease-factsheets/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Clinical diagnosis and cultural control protocols for Solanaceae and Cucurbitaceae.",
        is_general=True,
    ),
    "SRC_PURDUE_EXT": SourceRecord(
        source_id="SRC_PURDUE_EXT",
        title="Purdue Extension Plant and Pest Diagnostic Laboratory Disease Guides",
        organization="Purdue University Cooperative Extension Service",
        url_or_doi="https://extension.purdue.edu/programs/agriculture-natural-resources/",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Foliar fungal and bacterial spot identification and prevention guidelines.",
        is_general=True,
    ),
    "SRC_NCSTATE_EXT": SourceRecord(
        source_id="SRC_NCSTATE_EXT",
        title="NC State Extension Plant Pathology & Agricultural Portal",
        organization="North Carolina State University Extension",
        url_or_doi="https://content.ces.ncsu.edu/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="General agronomic, horticultural, and foliar disease management publications.",
        is_general=True,
    ),
    "SRC_UF_IFAS": SourceRecord(
        source_id="SRC_UF_IFAS",
        title="University of Florida IFAS Extension Plant Pathology Guidelines",
        organization="University of Florida Institute of Food and Agricultural Sciences",
        url_or_doi="https://edis.ifas.ufl.edu/topic_plant_diseases",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Tropical and subtropical crop disease etiology and management.",
        is_general=True,
    ),
    "SRC_ICAR_IISR": SourceRecord(
        source_id="SRC_ICAR_IISR",
        title="ICAR-IISR Good Agricultural Practices and Disease Management in Spices",
        organization="Indian Council of Agricultural Research - Indian Institute of Spices Research",
        url_or_doi="http://www.spices.res.in/publication/package-practices",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Authoritative guidelines for ginger and turmeric rhizome and foliar pathologies.",
        is_general=True,
    ),
    "SRC_IOWA_STATE_EXT": SourceRecord(
        source_id="SRC_IOWA_STATE_EXT",
        title="Iowa State University Extension Integrated Pest Management: Soybean Rust and Foliar Diseases",
        organization="Iowa State University Extension and Outreach",
        url_or_doi="https://crops.extension.iastate.edu/cropnews",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Phakopsora pachyrhizi symptom identification, spore surveillance, and management.",
        is_general=True,
    ),
    "SRC_PENNSTATE_EXT": SourceRecord(
        source_id="SRC_PENNSTATE_EXT",
        title="Penn State Extension Tree Fruit and Vegetable Disease Management Guides",
        organization="Pennsylvania State University College of Agricultural Sciences",
        url_or_doi="https://extension.psu.edu/plant-disease-management",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Foliar powdery mildew, rust, and rot cultural suppression guidelines.",
        is_general=True,
    ),
    "SRC_UNL_EXT": SourceRecord(
        source_id="SRC_UNL_EXT",
        title="University of Nebraska-Lincoln Extension CropWatch Rust Management",
        organization="University of Nebraska-Lincoln",
        url_or_doi="https://cropwatch.unl.edu/plantdisease",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Legume and dry bean rust resistance and canopy management.",
        is_general=True,
    ),
    "SRC_WSU_EXT": SourceRecord(
        source_id="SRC_WSU_EXT",
        title="Washington State University Extension Allium Disease and Pest Diagnostic Guide",
        organization="Washington State University Extension",
        url_or_doi="https://extension.wsu.edu/allium-pathology",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Puccinia allii symptom progression, microclimate factors, and field sanitation.",
        is_general=True,
    ),
    "SRC_APS_PRESS": SourceRecord(
        source_id="SRC_APS_PRESS",
        title="American Phytopathological Society (APS) Compendia of Plant Diseases",
        organization="The American Phytopathological Society (APS)",
        url_or_doi="https://apsjournals.apsnet.org/series/compendia",
        publication_year=2024,
        source_tier=SourceTier.TIER_1,
        notes="Standard global reference for etiology, symptomatology, and epidemiology of plant pathogens.",
        is_general=True,
    ),
    "SRC_MSU_EXT": SourceRecord(
        source_id="SRC_MSU_EXT",
        title="Michigan State University Extension Plant & Pest Management Factsheets",
        organization="Michigan State University Extension",
        url_or_doi="https://www.canr.msu.edu/pest_management/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Small fruit (blueberry, raspberry, cherry), celery, and carrot disease diagnostics.",
        is_general=True,
    ),
    "SRC_TAMU_EXT": SourceRecord(
        source_id="SRC_TAMU_EXT",
        title="Texas A&M AgriLife Extension Plant Disease Handbook",
        organization="Texas A&M AgriLife Extension Service",
        url_or_doi="https://plantdiseasehandbook.tamu.edu/",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Warm-climate agronomic crops, citrus, stone fruit, and cereal pathology.",
        is_general=True,
    ),
    "SRC_KSU_EXT": SourceRecord(
        source_id="SRC_KSU_EXT",
        title="Kansas State University Extension Wheat & Cereal Disease Management Guides",
        organization="Kansas State University Agricultural Experiment Station",
        url_or_doi="https://www.plantpath.k-state.edu/extension/crop-diseases/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Wheat rusts, head scab, leaf blotches, and corn foliar disease management.",
        is_general=True,
    ),
    "SRC_ICAR_IARI": SourceRecord(
        source_id="SRC_ICAR_IARI",
        title="ICAR-Indian Agricultural Research Institute Division of Plant Pathology",
        organization="Indian Council of Agricultural Research - IARI",
        url_or_doi="https://www.iari.res.in/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="National guidelines for cereal, legume, rice blast, and tropical vegetable pathologies.",
        is_general=True,
    ),
    "SRC_ICAR_CPRI": SourceRecord(
        source_id="SRC_ICAR_CPRI",
        title="ICAR-Central Potato Research Institute Technical Bulletins",
        organization="Indian Council of Agricultural Research - CPRI",
        url_or_doi="https://cpri.icar.gov.in/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Authoritative late blight and early blight management in tuber crops.",
        is_general=True,
    ),
    "SRC_ICAR_NRCC": SourceRecord(
        source_id="SRC_ICAR_NRCC",
        title="ICAR-Central Citrus Research Institute Disease Management Guidelines",
        organization="Indian Council of Agricultural Research - CCRI (formerly NRCC)",
        url_or_doi="https://ccri.icar.gov.in/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Citrus canker, greening (HLB), and gummosis integrated management.",
        is_general=True,
    ),
    "SRC_CABI_CPC": SourceRecord(
        source_id="SRC_CABI_CPC",
        title="CABI Crop Protection Compendium and Plantwise Knowledge Bank",
        organization="Centre for Agriculture and Bioscience International (CABI)",
        url_or_doi="https://www.cabi.org/cpc/",
        publication_year=2024,
        source_tier=SourceTier.TIER_1,
        notes="International pest and pathogen distribution, host range, and control datasheets.",
        is_general=True,
    ),
    "SRC_EPPO_GLOBAL": SourceRecord(
        source_id="SRC_EPPO_GLOBAL",
        title="EPPO Global Database Plant Quarantine and Phytosanitary Factsheets",
        organization="European and Mediterranean Plant Protection Organization (EPPO)",
        url_or_doi="https://gd.eppo.int/",
        publication_year=2024,
        source_tier=SourceTier.TIER_1,
        notes="Quarantine pathogens, viral epidemiology (e.g. Plum pox), and regulated pests.",
        is_general=True,
    ),
    "SRC_OSU_EXT": SourceRecord(
        source_id="SRC_OSU_EXT",
        title="Oregon State University Extension Pacific Northwest Plant Disease Management Handbook",
        organization="Oregon State University Extension Service",
        url_or_doi="https://pnwhandbooks.org/plantdisease",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Berry crops, tree fruit, vegetable seed crops, and downy/powdery mildews.",
        is_general=True,
    ),
    "SRC_UMN_EXT": SourceRecord(
        source_id="SRC_UMN_EXT",
        title="University of Minnesota Extension Plant Disease Management Library",
        organization="University of Minnesota Extension",
        url_or_doi="https://extension.umn.edu/plant-diseases",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Brassica, Solanaceae, and cucurbit integrated disease management.",
        is_general=True,
    ),
    "SRC_WISCONSIN_EXT": SourceRecord(
        source_id="SRC_WISCONSIN_EXT",
        title="University of Wisconsin-Madison Division of Extension Vegetable & Fruit Pathology",
        organization="University of Wisconsin-Madison Extension",
        url_or_doi="https://vegpath.plantpath.wisc.edu/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Potato, carrot cavity spot, cabbage black rot, and cucurbit disease control.",
        is_general=True,
    ),
    "SRC_RUTGERS_EXT": SourceRecord(
        source_id="SRC_RUTGERS_EXT",
        title="Rutgers NJAES Plant Pathology and Commercial Vegetable Production Recommendations",
        organization="Rutgers New Jersey Agricultural Experiment Station",
        url_or_doi="https://plant-pest-advisory.rutgers.edu/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Foliar vegetable blights, downy mildews, and pepper bacterial spot.",
        is_general=True,
    ),
    "SRC_UGA_EXT": SourceRecord(
        source_id="SRC_UGA_EXT",
        title="University of Georgia Extension Plant Disease Management Factsheets",
        organization="University of Georgia Cooperative Extension",
        url_or_doi="https://extension.uga.edu/topic-areas/plant-diseases.html",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Peach brown rot/scab, blueberry anthracnose, and tobacco foliar diseases.",
        is_general=True,
    ),
    "SRC_CTAHR_HAWAII": SourceRecord(
        source_id="SRC_CTAHR_HAWAII",
        title="University of Hawaii at Manoa CTAHR Cooperative Extension Tropical Plant Pathology",
        organization="College of Tropical Agriculture and Human Resources (CTAHR)",
        url_or_doi="https://www.ctahr.hawaii.edu/site/extprojects.aspx",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Banana bunchy top, Panama disease TR4, coffee leaf rust, and ginger pathogens.",
        is_general=True,
    ),
    "SRC_WCR_COFFEE": SourceRecord(
        source_id="SRC_WCR_COFFEE",
        title="World Coffee Research / International Coffee Organization Disease Control Manuals",
        organization="World Coffee Research (WCR)",
        url_or_doi="https://worldcoffeeresearch.org/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Coffee leaf rust, berry blotch, and black rot integrated management.",
        is_general=True,
    ),
    "SRC_IRRI_RICE": SourceRecord(
        source_id="SRC_IRRI_RICE",
        title="International Rice Research Institute (IRRI) Rice Knowledge Bank",
        organization="International Rice Research Institute (IRRI)",
        url_or_doi="http://www.knowledgebank.irri.org/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Rice blast, sheath blight, and brown spot symptoms and cultural management.",
        is_general=True,
    ),
}

# Convenient module-level constants
SOURCE_USDA_ARS = SOURCE_REGISTRY["SRC_USDA_ARS"]
SOURCE_FAO = SOURCE_REGISTRY["SRC_FAO_PLANT"]
SOURCE_UC_IPM = SOURCE_REGISTRY["SRC_UC_IPM"]
SOURCE_CORNELL = SOURCE_REGISTRY["SRC_CORNELL_EXT"]
SOURCE_PURDUE = SOURCE_REGISTRY["SRC_PURDUE_EXT"]
SOURCE_NC_STATE = SOURCE_REGISTRY["SRC_NCSTATE_EXT"]
SOURCE_UF_IFAS = SOURCE_REGISTRY["SRC_UF_IFAS"]
SOURCE_ICAR = SOURCE_REGISTRY["SRC_ICAR_IISR"]
SOURCE_IOWA_STATE = SOURCE_REGISTRY["SRC_IOWA_STATE_EXT"]
SOURCE_PENN_STATE = SOURCE_REGISTRY["SRC_PENNSTATE_EXT"]
SOURCE_UNL = SOURCE_REGISTRY["SRC_UNL_EXT"]
SOURCE_WSU = SOURCE_REGISTRY["SRC_WSU_EXT"]
SOURCE_WASHINGTON_STATE = SOURCE_REGISTRY["SRC_WSU_EXT"]
SOURCE_APS = SOURCE_REGISTRY["SRC_APS_PRESS"]
SOURCE_MSU = SOURCE_REGISTRY["SRC_MSU_EXT"]
SOURCE_TAMU = SOURCE_REGISTRY["SRC_TAMU_EXT"]
SOURCE_KSU = SOURCE_REGISTRY["SRC_KSU_EXT"]
SOURCE_CABI = SOURCE_REGISTRY["SRC_CABI_CPC"]
SOURCE_EPPO = SOURCE_REGISTRY["SRC_EPPO_GLOBAL"]
SOURCE_OSU = SOURCE_REGISTRY["SRC_OSU_EXT"]
SOURCE_UMN = SOURCE_REGISTRY["SRC_UMN_EXT"]
SOURCE_WISCONSIN = SOURCE_REGISTRY["SRC_WISCONSIN_EXT"]
SOURCE_RUTGERS = SOURCE_REGISTRY["SRC_RUTGERS_EXT"]
SOURCE_UGA = SOURCE_REGISTRY["SRC_UGA_EXT"]
SOURCE_CTAHR_HAWAII = SOURCE_REGISTRY["SRC_CTAHR_HAWAII"]
SOURCE_WCR = SOURCE_REGISTRY["SRC_WCR_COFFEE"]
SOURCE_IRRI = SOURCE_REGISTRY["SRC_IRRI_RICE"]
SOURCE_CIMMYT = SourceRecord(
    source_id="SRC_CIMMYT",
    title="CIMMYT International Maize and Wheat Improvement Center Disease Guides",
    organization="International Maize and Wheat Improvement Center (CIMMYT)",
    url_or_doi="https://www.cimmyt.org/",
    publication_year=2023,
    source_tier=SourceTier.TIER_1,
    notes="Global rust surveillance, Fusarium head blight, and wheat pathology guidelines.",
    is_general=True,
)
SOURCE_REGISTRY["SRC_CIMMYT"] = SOURCE_CIMMYT

# ---------------------------------------------------------------------------
# Verified Disease-Specific Extension Factsheets & Diagnostic Guides
# ---------------------------------------------------------------------------
SOURCE_NC_STATE_BLUEBERRY_ANTHRACNOSE = SourceRecord(
    source_id="SRC_NCSTATE_BLUEBERRY_ANTHRACNOSE",
    title="Anthracnose Fruit Rot of Blueberries",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/anthracnose-fruit-rot-of-blueberries",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum acutatum/fioriniae latent fruit infection, blossom blighting, and fungicide spray timing in blueberries.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_BLUEBERRY_ANTHRACNOSE"] = SOURCE_NC_STATE_BLUEBERRY_ANTHRACNOSE

SOURCE_MSU_BLUEBERRY_ANTHRACNOSE = SourceRecord(
    source_id="SRC_MSU_BLUEBERRY_ANTHRACNOSE",
    title="Anthracnose Fruit Rot Management in Blueberries",
    organization="Michigan State University Extension",
    url_or_doi="https://www.canr.msu.edu/news/anthracnose-fruit-rot-management-in-blueberries",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Bloom and pre-harvest fungicide timing, cultivar susceptibility, and post-harvest cooling for blueberry ripe rot.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_MSU_BLUEBERRY_ANTHRACNOSE"] = SOURCE_MSU_BLUEBERRY_ANTHRACNOSE

SOURCE_UGA_PEPPER_BLOSSOM_END_ROT = SourceRecord(
    source_id="SRC_UGA_PEPPER_BLOSSOM_END_ROT",
    title="Blossom-End Rot and Calcium Nutrition of Pepper and Tomato",
    organization="University of Georgia Cooperative Extension",
    url_or_doi="https://extension.uga.edu/publications/detail.html?number=C938",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Abiotic calcium deficiency etiology, xylem transport, uniform soil moisture, and cultural management in solanaceous crops.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UGA_PEPPER_BLOSSOM_END_ROT"] = SOURCE_UGA_PEPPER_BLOSSOM_END_ROT

SOURCE_NC_STATE_TOMATO_EARLY_BLIGHT = SourceRecord(
    source_id="SRC_NCSTATE_TOMATO_EARLY_BLIGHT",
    title="Early Blight of Tomato",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/early-blight-of-tomato",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria solani concentric ring target spots, lower canopy defoliation, and protectant fungicide rotation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_TOMATO_EARLY_BLIGHT"] = SOURCE_NC_STATE_TOMATO_EARLY_BLIGHT

SOURCE_NC_STATE_CUCURBIT_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW",
    title="Cucurbit Downy Mildew",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/cucurbit-downy-mildew",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Pseudoperonospora cubensis angular foliar lesions, purplish sporulation, and regional spore forecasting for cucumber.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW"] = SOURCE_NC_STATE_CUCURBIT_DOWNY_MILDEW

SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW",
    title="Cucurbits: Powdery Mildew",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/powdery-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Podosphaera xanthii white talcum-like foliar coating, scouting, and fungicide rotation in cucurbits.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW"] = SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW

SOURCE_NC_STATE_TOMATO_LATE_BLIGHT = SourceRecord(
    source_id="SRC_NCSTATE_TOMATO_LATE_BLIGHT",
    title="Tomato Late Blight",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/tomato-late-blight",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Phytophthora infestans rapid foliar blighting, white sporangial down, and fungicide management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_TOMATO_LATE_BLIGHT"] = SOURCE_NC_STATE_TOMATO_LATE_BLIGHT

SOURCE_NC_STATE_TOMATO_SEPTORIA_LEAF_SPOT = SourceRecord(
    source_id="SRC_NCSTATE_TOMATO_SEPTORIA_LEAF_SPOT",
    title="Septoria Leaf Spot of Tomato",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/septoria-leaf-spot-of-tomato",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Septoria lycopersici circular foliar spots with dark borders and fungal pycnidia.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_TOMATO_SEPTORIA_LEAF_SPOT"] = SOURCE_NC_STATE_TOMATO_SEPTORIA_LEAF_SPOT

SOURCE_NC_STATE_PEPPER_TOMATO_BACTERIAL_SPOT = SourceRecord(
    source_id="SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT",
    title="Bacterial Spot of Pepper and Tomato",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/bacterial-spot-of-pepper-and-tomato",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas bacterial spot foliar lesions, defoliation, and copper-mancozeb management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT"] = SOURCE_NC_STATE_PEPPER_TOMATO_BACTERIAL_SPOT

SOURCE_UC_IPM_POTATO_EARLY_BLIGHT = SourceRecord(
    source_id="SRC_UC_IPM_POTATO_EARLY_BLIGHT",
    title="Potato: Early Blight",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/potato/early-blight/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria solani concentric leaf rings, tuber rot, and fungicide protection.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_POTATO_EARLY_BLIGHT"] = SOURCE_UC_IPM_POTATO_EARLY_BLIGHT

SOURCE_UC_IPM_POTATO_LATE_BLIGHT = SourceRecord(
    source_id="SRC_UC_IPM_POTATO_LATE_BLIGHT",
    title="Potato: Late Blight",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/potato/late-blight/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Phytophthora infestans foliar blighting and tuber rot management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_POTATO_LATE_BLIGHT"] = SOURCE_UC_IPM_POTATO_LATE_BLIGHT

SOURCE_UC_IPM_APPLE_SCAB = SourceRecord(
    source_id="SRC_UC_IPM_APPLE_SCAB",
    title="Apple Scab",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/PMG/PESTNOTES/pn7413.html",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Venturia inaequalis olive velvety spots, Mills infection periods, and orchard sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_APPLE_SCAB"] = SOURCE_UC_IPM_APPLE_SCAB

SOURCE_UC_IPM_PEACH_BROWN_ROT = SourceRecord(
    source_id="SRC_UC_IPM_PEACH_BROWN_ROT",
    title="Peach: Brown Rot",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/peach/brown-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Monilinia fructicola blossom and twig blight, fruit rot, and mummy removal.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PEACH_BROWN_ROT"] = SOURCE_UC_IPM_PEACH_BROWN_ROT

SOURCE_UC_IPM_STRAWBERRY_BOTRYTIS = SourceRecord(
    source_id="SRC_UC_IPM_STRAWBERRY_BOTRYTIS",
    title="Strawberry: Botrytis Fruit Rot",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/strawberry/botrytis-fruit-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Botrytis cinerea gray mold, blossom infection, and mulch/irrigation cultural control.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_STRAWBERRY_BOTRYTIS"] = SOURCE_UC_IPM_STRAWBERRY_BOTRYTIS

SOURCE_UC_IPM_GRAPE_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_GRAPE_POWDERY_MILDEW",
    title="Grape: Powdery Mildew",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/grape/powdery-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Erysiphe necator powdery mildew risk index, sulfur applications, and canopy airflow.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_GRAPE_POWDERY_MILDEW"] = SOURCE_UC_IPM_GRAPE_POWDERY_MILDEW

SOURCE_USDA_ARS_WHEAT_LEAF_RUST = SourceRecord(
    source_id="SRC_USDA_ARS_WHEAT_LEAF_RUST",
    title="Wheat Leaf Rust",
    organization="USDA Agricultural Research Service (USDA-ARS) Cereal Disease Laboratory",
    url_or_doi="https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/wheat-leaf-rust/",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Puccinia triticina epidemiology, virulence surveys, and host resistance in wheat.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_USDA_ARS_WHEAT_LEAF_RUST"] = SOURCE_USDA_ARS_WHEAT_LEAF_RUST

SOURCE_USDA_ARS_WHEAT_STRIPE_RUST = SourceRecord(
    source_id="SRC_USDA_ARS_WHEAT_STRIPE_RUST",
    title="Wheat Stripe Rust",
    organization="USDA Agricultural Research Service (USDA-ARS) Cereal Disease Laboratory",
    url_or_doi="https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/wheat-stripe-rust/",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Puccinia striiformis f. sp. tritici linear foliar pustules, spore dispersal, and Yr resistance.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_USDA_ARS_WHEAT_STRIPE_RUST"] = SOURCE_USDA_ARS_WHEAT_STRIPE_RUST

SOURCE_USDA_ARS_WHEAT_STEM_RUST = SourceRecord(
    source_id="SRC_USDA_ARS_WHEAT_STEM_RUST",
    title="Wheat Stem Rust",
    organization="USDA Agricultural Research Service (USDA-ARS) Cereal Disease Laboratory",
    url_or_doi="https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/wheat-stem-rust/",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Puccinia graminis f. sp. tritici torn epidermal stem lesions, barberry eradication, and resistance.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_USDA_ARS_WHEAT_STEM_RUST"] = SOURCE_USDA_ARS_WHEAT_STEM_RUST

SOURCE_UNL_WHEAT_LEAF_RUST = SourceRecord(
    source_id="SRC_UNL_WHEAT_LEAF_RUST",
    title="Wheat: Leaf Rust",
    organization="University of Nebraska-Lincoln Extension",
    url_or_doi="https://cropwatch.unl.edu/plantdisease/wheat/leaf-rust",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Puccinia triticina scouting thresholds, flag leaf protection, and DMI fungicide timing.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UNL_WHEAT_LEAF_RUST"] = SOURCE_UNL_WHEAT_LEAF_RUST

# ---------------------------------------------------------------------------
# Newly Verified Disease-Specific Sources (Banana, Grape, Citrus, Eggplant, Corn, Wheat)
# ---------------------------------------------------------------------------

# 1. Banana — Anthracnose
SOURCE_PROMUSA_BANANA_ANTHRACNOSE = SourceRecord(
    source_id="SRC_PROMUSA_BANANA_ANTHRACNOSE",
    title="Anthracnose",
    organization="ProMusa / Bioversity International & CIAT (CGIAR)",
    url_or_doi="https://www.promusa.org/Anthracnose",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Colletotrichum musae infection cycle, latent quiescent fruit infections, salmon-pink spore masses, and field bunch hygiene.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PROMUSA_BANANA_ANTHRACNOSE"] = SOURCE_PROMUSA_BANANA_ANTHRACNOSE

# 2. Banana — Cordana Leaf Spot
SOURCE_PROMUSA_BANANA_CORDANA = SourceRecord(
    source_id="SRC_PROMUSA_BANANA_CORDANA",
    title="Cordana leaf spot",
    organization="ProMusa / Bioversity International & CIAT (CGIAR)",
    url_or_doi="https://www.promusa.org/Cordana+leaf+spot",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Neocordana musae large oval-to-diamond necrotic leaf lesions with bright yellow chlorotic halos and canopy management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PROMUSA_BANANA_CORDANA"] = SOURCE_PROMUSA_BANANA_CORDANA

# 3. Banana — Panama Disease (Fusarium Wilt)
SOURCE_PROMUSA_BANANA_PANAMA = SourceRecord(
    source_id="SRC_PROMUSA_BANANA_PANAMA",
    title="Fusarium wilt of banana",
    organization="ProMusa / Bioversity International & CIAT (CGIAR)",
    url_or_doi="https://www.promusa.org/Fusarium+wilt",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Fusarium oxysporum f. sp. cubense vascular wilt, external leaf yellowing/skirting, internal pseudostem discoloration, and TR4 biosecurity.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PROMUSA_BANANA_PANAMA"] = SOURCE_PROMUSA_BANANA_PANAMA

# 4. Grape — Black Rot
SOURCE_UC_IPM_GRAPE_BLACK_ROT = SourceRecord(
    source_id="SRC_UC_IPM_GRAPE_BLACK_ROT",
    title="Black Rot",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/grape/black-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Guignardia bidwellii fruit mummification, leaf lesions with pycnidia, canopy shoot thinning, and protective fungicide timings.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_GRAPE_BLACK_ROT"] = SOURCE_UC_IPM_GRAPE_BLACK_ROT

SOURCE_OSU_GRAPE_BLACK_ROT = SourceRecord(
    source_id="SRC_OSU_GRAPE_BLACK_ROT",
    title="Black Rot of Grape",
    organization="Ohio State University Extension",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-fru-24",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Guignardia bidwellii biology, fruit rot phase, mummy destruction, and fungicide spray schedules from early bloom.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_GRAPE_BLACK_ROT"] = SOURCE_OSU_GRAPE_BLACK_ROT

# 5. Grape — Downy Mildew
SOURCE_UC_IPM_GRAPE_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_GRAPE_DOWNY_MILDEW",
    title="Downy Mildew",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/grape/downy-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Plasmopara viticola oil spots on upper leaf surface, dense white downy sporulation on lower leaf surface, and protectant/systemic sprays.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_GRAPE_DOWNY_MILDEW"] = SOURCE_UC_IPM_GRAPE_DOWNY_MILDEW

SOURCE_OSU_GRAPE_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_OSU_GRAPE_DOWNY_MILDEW",
    title="Downy Mildew of Grape",
    organization="Ohio State University Extension",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-fru-34",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Plasmopara viticola environmental triggers (10-10-10 rule), leaf and cluster infections, and integrated management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_GRAPE_DOWNY_MILDEW"] = SOURCE_OSU_GRAPE_DOWNY_MILDEW

# 6. Citrus — Citrus Canker
SOURCE_UC_IPM_CITRUS_CANKER = SourceRecord(
    source_id="SRC_UC_IPM_CITRUS_CANKER",
    title="Citrus Canker",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/citrus/citrus-canker/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas citri subsp. citri raised blister-like corky lesions with oily water-soaked margins, windbreak planting, and copper sprays.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CITRUS_CANKER"] = SOURCE_UC_IPM_CITRUS_CANKER

# 7. Citrus — Citrus Greening (Huanglongbing)
SOURCE_UC_IPM_CITRUS_GREENING = SourceRecord(
    source_id="SRC_UC_IPM_CITRUS_GREENING",
    title="Huanglongbing (Citrus Greening)",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/citrus/citrus-greening/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Candidatus Liberibacter asiaticus asymmetrical blotchy mottle chlorosis, lopsided bitter fruit, Asian citrus psyllid vector management, and quarantine.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CITRUS_GREENING"] = SOURCE_UC_IPM_CITRUS_GREENING

# 8. Eggplant — Phomopsis Fruit Rot
SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS = SourceRecord(
    source_id="SRC_RUTGERS_EGGPLANT_PHOMOPSIS",
    title="Phomopsis Fruit Rot in Eggplant",
    organization="Rutgers New Jersey Agricultural Experiment Station (NJAES) Cooperative Extension",
    url_or_doi="https://plant-pest-advisory.rutgers.edu/phomopsis-fruit-rot-in-eggplant/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Phomopsis vexans soft sunken fruit rot, concentric black pycnidia, seedling damping-off, 3-year crop rotation, and fungicide timing.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_RUTGERS_EGGPLANT_PHOMOPSIS"] = SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS

# 9. Corn — Common Smut
SOURCE_OSU_CORN_COMMON_SMUT = SourceRecord(
    source_id="SRC_OSU_CORN_COMMON_SMUT",
    title="Common Smut of Corn",
    organization="Ohio State University Extension",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-cer-06",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Ustilago maydis silvery-white fleshy tumor galls, powdery black teliospore masses, wounding avoidance, and hybrid genetic resistance.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_CORN_COMMON_SMUT"] = SOURCE_OSU_CORN_COMMON_SMUT

# 10. Corn — Northern Corn Leaf Blight
SOURCE_OSU_CORN_NORTHERN_LEAF_BLIGHT = SourceRecord(
    source_id="SRC_OSU_CORN_NORTHERN_LEAF_BLIGHT",
    title="Northern Corn Leaf Blight",
    organization="Ohio State University Extension",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-cer-10",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Exserohilum turcicum long elliptical cigar-shaped grayish-green lesions, Ht gene resistance, crop rotation, and fungicide thresholds.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_CORN_NORTHERN_LEAF_BLIGHT"] = SOURCE_OSU_CORN_NORTHERN_LEAF_BLIGHT

# 11. Wheat — Head Scab (Fusarium Head Blight)
SOURCE_UNL_WHEAT_HEAD_SCAB = SourceRecord(
    source_id="SRC_UNL_WHEAT_HEAD_SCAB",
    title="Fusarium Head Blight (Scab) of Wheat",
    organization="University of Nebraska-Lincoln Extension CropWatch",
    url_or_doi="https://cropwatch.unl.edu/plant-disease/wheat/fusarium-head-blight-scab/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Fusarium graminearum prematurely bleached spikelets, salmon-pink sporodochia, chalky tombstone kernels, deoxynivalenol (DON) vomitoxin, and anthesis fungicide timing.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UNL_WHEAT_HEAD_SCAB"] = SOURCE_UNL_WHEAT_HEAD_SCAB

SOURCE_OSU_WHEAT_HEAD_SCAB = SourceRecord(
    source_id="SRC_OSU_WHEAT_HEAD_SCAB",
    title="Fusarium Head Blight of Wheat",
    organization="Ohio State University Extension",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-cer-07",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Fusarium head blight forecasting models, DMI triazole fungicide timing at early flowering (Feekes 10.5.1), and rotation away from corn stubble.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_WHEAT_HEAD_SCAB"] = SOURCE_OSU_WHEAT_HEAD_SCAB

# 12. Wheat — Rust (General / Unsubtype-Differentiated)
SOURCE_USDA_ARS_WHEAT_RUST = SourceRecord(
    source_id="SRC_USDA_ARS_WHEAT_RUST",
    title="Wheat Rust",
    organization="USDA Agricultural Research Service (USDA-ARS) Cereal Disease Laboratory",
    url_or_doi="https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Cereal rust surveillance, rust resistance in wheat, and epidemiology across North America.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_USDA_ARS_WHEAT_RUST"] = SOURCE_USDA_ARS_WHEAT_RUST

# ---------------------------------------------------------------------------
# Batch 1: Solanaceous Crops Disease-Specific Sources
# ---------------------------------------------------------------------------
# Bell Pepper
SOURCE_NC_STATE_PEPPER_FROGEYE_LEAF_SPOT = SourceRecord(
    source_id="SRC_NCSTATE_PEPPER_FROGEYE_LEAF_SPOT",
    title="Cercospora Leaf Spot (Frogeye Leaf Spot) on Pepper",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/cercospora-leaf-spot-frogeye-leaf-spot-on-pepper",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora capsici symptoms, frogeye lesion progression on foliage, warm humid conditions, and fungicide timing.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_PEPPER_FROGEYE_LEAF_SPOT"] = SOURCE_NC_STATE_PEPPER_FROGEYE_LEAF_SPOT

SOURCE_UF_IFAS_PEPPER_DISEASES = SourceRecord(
    source_id="SRC_UF_IFAS_PEPPER_DISEASES",
    title="Some Common Diseases of Pepper in Florida",
    organization="University of Florida IFAS Extension",
    url_or_doi="https://ask.ifas.ufl.edu/publication/VH054",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Diagnosis and management of frogeye leaf spot (Cercospora capsici) and foliar pathogens on bell pepper.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UF_IFAS_PEPPER_DISEASES"] = SOURCE_UF_IFAS_PEPPER_DISEASES

SOURCE_UC_IPM_PEPPER_LEAF_CURL = SourceRecord(
    source_id="SRC_UC_IPM_PEPPER_LEAF_CURL",
    title="Peppers: Beet Curly Top",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/peppers/curly-top/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Curtovirus transmission by beet leafhopper in peppers, stunted growth, leaf curling, and management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PEPPER_LEAF_CURL"] = SOURCE_UC_IPM_PEPPER_LEAF_CURL

SOURCE_UC_IPM_PEPPER_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_PEPPER_POWDERY_MILDEW",
    title="Peppers: Powdery Mildew",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/peppers/powdery-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Leveillula taurica identification, white powdery growth on pepper leaf undersides, and fungicide programs.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PEPPER_POWDERY_MILDEW"] = SOURCE_UC_IPM_PEPPER_POWDERY_MILDEW

# Tomato
SOURCE_UC_IPM_TOMATO_ANTHRACNOSE = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_ANTHRACNOSE",
    title="Tomato: Anthracnose",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/anthracnose/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum coccodes circular sunken lesions on ripe tomato fruit, splash dispersal, and preventative fungicidal control.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_ANTHRACNOSE"] = SOURCE_UC_IPM_TOMATO_ANTHRACNOSE

SOURCE_UC_IPM_TOMATO_FUSARIUM_ROT = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_FUSARIUM_ROT",
    title="Tomato: Fusarium Rot",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/fusarium-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Fusarium oxysporum and Fusarium solani postharvest and field fruit rot, wound entry, and field sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_FUSARIUM_ROT"] = SOURCE_UC_IPM_TOMATO_FUSARIUM_ROT

SOURCE_UC_IPM_TOMATO_LEAF_MOLD = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_LEAF_MOLD",
    title="Tomato: Leaf Mold",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/leaf-mold/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Passalora fulva (Fulvia fulva) pale green/yellow foliar spots with olive-brown velvety mold under high humidity.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_LEAF_MOLD"] = SOURCE_UC_IPM_TOMATO_LEAF_MOLD

SOURCE_UC_IPM_TOMATO_MOSAIC_VIRUS = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_MOSAIC_VIRUS",
    title="Tomato: Tobacco and Tomato Mosaic",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/tobacco-mosaic/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Tobacco mosaic virus (TMV) and Tomato mosaic virus (ToMV) mechanical transmission, mottling, distortion, and sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_MOSAIC_VIRUS"] = SOURCE_UC_IPM_TOMATO_MOSAIC_VIRUS

SOURCE_UC_IPM_TOMATO_YELLOW_LEAF_CURL = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_YELLOW_LEAF_CURL",
    title="Tomato: Tomato Yellow Leaf Curl",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/tomato-yellow-leaf-curl/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Tomato yellow leaf curl begomovirus (TYLCV) transmission by silverleaf whitefly (Bemisia tabaci), severe stunting, and cupped leaves.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_YELLOW_LEAF_CURL"] = SOURCE_UC_IPM_TOMATO_YELLOW_LEAF_CURL

# Eggplant
SOURCE_PNW_EGGPLANT_CERCOSPORA = SourceRecord(
    source_id="SRC_PNW_EGGPLANT_CERCOSPORA",
    title="Eggplant (Solanum melongena)-Cercospora Leaf Spot",
    organization="Pacific Northwest Plant Disease Management Handbook (OSU / WSU / UI)",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/eggplant-solanum-melongena-cercospora-leaf-spot",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora melongenae circular tan to brown spots with concentric rings, chlorosis, and defoliation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_EGGPLANT_CERCOSPORA"] = SOURCE_PNW_EGGPLANT_CERCOSPORA

SOURCE_UC_IPM_EGGPLANT_MOSAIC = SourceRecord(
    source_id="SRC_UC_IPM_EGGPLANT_MOSAIC",
    title="Eggplant: Tobacco Mosaic",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/eggplant/tobacco-mosaic/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Tobacco mosaic virus (TMV) foliar mottling, leaf distortion, mechanical transmission, and greenhouse sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_EGGPLANT_MOSAIC"] = SOURCE_UC_IPM_EGGPLANT_MOSAIC

SOURCE_PNW_EGGPLANT_FLEA_BEETLE = SourceRecord(
    source_id="SRC_PNW_EGGPLANT_FLEA_BEETLE",
    title="Eggplant-Flea Beetle",
    organization="Pacific Northwest Insect Management Handbook",
    url_or_doi="https://pnwhandbooks.org/insect/vegetable/vegetable-pests/hosts-pests/eggplant-flea-beetle",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Epitrix species shot-hole feeding damage on eggplant foliage, seedling vulnerability, row covers, and insecticides.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_EGGPLANT_FLEA_BEETLE"] = SOURCE_PNW_EGGPLANT_FLEA_BEETLE

SOURCE_UC_IPM_EGGPLANT_FLEA_BEETLES = SourceRecord(
    source_id="SRC_UC_IPM_EGGPLANT_FLEA_BEETLES",
    title="Eggplant: Flea Beetles",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/eggplant/flea-beetles/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Identification of flea beetle pest damage on solanaceous crops, cultural exclusion, and treatment thresholds.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_EGGPLANT_FLEA_BEETLES"] = SOURCE_UC_IPM_EGGPLANT_FLEA_BEETLES

SOURCE_CORNELL_PHYTOPHTHORA_BLIGHT = SourceRecord(
    source_id="SRC_CORNELL_PHYTOPHTHORA_BLIGHT",
    title="Phytophthora Blight of Solanaceous and Cucurbit Crops",
    organization="Cornell University College of Agriculture and Life Sciences",
    url_or_doi="https://www.vegetables.cornell.edu/pest-management/disease-factsheets/phytophthora-blight/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Phytophthora capsici crown rot, foliar blight, fruit rot, water management, and resistant varieties.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_CORNELL_PHYTOPHTHORA_BLIGHT"] = SOURCE_CORNELL_PHYTOPHTHORA_BLIGHT

SOURCE_NC_STATE_PHYTOPHTHORA_BLIGHT = SourceRecord(
    source_id="SRC_NCSTATE_PHYTOPHTHORA_BLIGHT",
    title="Phytophthora Blight of Peppers and Solanaceous Vegetables",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/phytophthora-blight-of-peppers",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Phytophthora capsici diagnosis, oospore survival, drainage, and systemic fungicides.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_PHYTOPHTHORA_BLIGHT"] = SOURCE_NC_STATE_PHYTOPHTHORA_BLIGHT

SOURCE_PNW_EGGPLANT_VERTICILLIUM = SourceRecord(
    source_id="SRC_PNW_EGGPLANT_VERTICILLIUM",
    title="Eggplant (Solanum melongena)-Verticillium Wilt",
    organization="Pacific Northwest Plant Disease Management Handbook (OSU / WSU / UI)",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/eggplant-solanum-melongena-verticillium-wilt",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Verticillium dahliae vascular discoloration, unilateral wilting, stunting, and long-term crop rotation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_EGGPLANT_VERTICILLIUM"] = SOURCE_PNW_EGGPLANT_VERTICILLIUM

SOURCE_UC_IPM_EGGPLANT_VERTICILLIUM = SourceRecord(
    source_id="SRC_UC_IPM_EGGPLANT_VERTICILLIUM",
    title="Eggplant: Verticillium Wilt",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/eggplant/verticillium-wilt/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Verticillium wilt symptoms, yellow V-shaped foliar lesions, vascular browning, and solarization.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_EGGPLANT_VERTICILLIUM"] = SOURCE_UC_IPM_EGGPLANT_VERTICILLIUM

# ---------------------------------------------------------------------------
# Batch 2: Cucurbits Crops Disease-Specific Sources
# ---------------------------------------------------------------------------
# Cucumber — Angular Leaf Spot
SOURCE_UC_IPM_CUCURBIT_ANGULAR_LEAF_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_ANGULAR_LEAF_SPOT",
    title="Angular Leaf Spot / Cucurbits",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/angular-leaf-spot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Pseudomonas syringae pv. lachrymans water-soaked angular foliar lesions bounded by veins, white exudate, and bactericide sprays.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_ANGULAR_LEAF_SPOT"] = SOURCE_UC_IPM_CUCURBIT_ANGULAR_LEAF_SPOT

SOURCE_PNW_CUCUMBER_ANGULAR_LEAF_SPOT = SourceRecord(
    source_id="SRC_PNW_CUCUMBER_ANGULAR_LEAF_SPOT",
    title="Cucumber (Cucumis sativus)-Angular Leaf Spot",
    organization="Pacific Northwest Plant Disease Management Handbook (OSU / WSU / UI)",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/cucumber-cucumis-sativus-angular-leaf-spot",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Pseudomonas syringae pv. lachrymans seed transmission, crop rotation, and foliar spray protocols.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_CUCUMBER_ANGULAR_LEAF_SPOT"] = SOURCE_PNW_CUCUMBER_ANGULAR_LEAF_SPOT

SOURCE_UKY_CUCURBIT_ANGULAR_LEAF_SPOT = SourceRecord(
    source_id="SRC_UKY_CUCURBIT_ANGULAR_LEAF_SPOT",
    title="Angular Leaf Spot of Cucurbit Crops",
    organization="University of Kentucky Extension (VeggieScout)",
    url_or_doi="https://veggiescout.mgcafe.uky.edu/angular-leaf-spot-cucurbit-crops",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Angular leaf spot symptoms on cucumber leaves and fruit, shot-hole progression, and cultural prevention.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UKY_CUCURBIT_ANGULAR_LEAF_SPOT"] = SOURCE_UKY_CUCURBIT_ANGULAR_LEAF_SPOT

# Cucumber — Anthracnose
SOURCE_NC_STATE_CUCURBIT_ANTHRACNOSE = SourceRecord(
    source_id="SRC_NCSTATE_CUCURBIT_ANTHRACNOSE",
    title="Anthracnose of Cucurbits",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/anthracnose-of-cucurbits",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum orbiculare circular brown foliar lesions, sunken water-soaked fruit lesions with salmon-pink spore droplets, and protectant fungicides.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_CUCURBIT_ANTHRACNOSE"] = SOURCE_NC_STATE_CUCURBIT_ANTHRACNOSE

SOURCE_UC_IPM_CUCURBIT_ANTHRACNOSE = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_ANTHRACNOSE",
    title="Anthracnose / Cucurbits",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/anthracnose/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum orbiculare symptoms on cucumber foliage and fruit, field sanitation, and resistant varieties.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_ANTHRACNOSE"] = SOURCE_UC_IPM_CUCURBIT_ANTHRACNOSE

SOURCE_UKY_CUCURBIT_ANTHRACNOSE = SourceRecord(
    source_id="SRC_UKY_CUCURBIT_ANTHRACNOSE",
    title="Anthracnose of Cucurbit Crops",
    organization="University of Kentucky Extension (VeggieScout)",
    url_or_doi="https://veggiescout.mgcafe.uky.edu/anthracnose-cucurbit-crops",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Foliar and fruit symptoms of anthracnose on cucumbers, splash dispersal, and scouting protocols.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UKY_CUCURBIT_ANTHRACNOSE"] = SOURCE_UKY_CUCURBIT_ANTHRACNOSE

# Cucumber & Zucchini — Bacterial Wilt
SOURCE_UW_MADISON_CUCURBIT_BACTERIAL_WILT = SourceRecord(
    source_id="SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT",
    title="Bacterial Wilt of Cucurbits",
    organization="University of Wisconsin-Madison Extension",
    url_or_doi="https://hort.extension.wisc.edu/articles/bacterial-wilt/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Erwinia tracheiphila vascular wilt on cucumber and squash, cucumber beetle vector transmission, diagnostic stringing test, and early-season insect control.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT"] = SOURCE_UW_MADISON_CUCURBIT_BACTERIAL_WILT

SOURCE_PNW_CUCUMBER_BACTERIAL_WILT = SourceRecord(
    source_id="SRC_PNW_CUCUMBER_BACTERIAL_WILT",
    title="Cucumber (Cucumis sativus)-Bacterial Wilt",
    organization="Pacific Northwest Plant Disease Management Handbook (OSU / WSU / UI)",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/cucumber-cucumis-sativus-bacterial-wilt",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Erwinia tracheiphila transmission by cucumber beetles, runner wilt, vascular clogging, and vector suppression.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_CUCUMBER_BACTERIAL_WILT"] = SOURCE_PNW_CUCUMBER_BACTERIAL_WILT

SOURCE_UKY_CUCURBIT_BACTERIAL_WILT = SourceRecord(
    source_id="SRC_UKY_CUCURBIT_BACTERIAL_WILT",
    title="Bacterial Wilt of Cucurbit Crops",
    organization="University of Kentucky Extension (VeggieScout)",
    url_or_doi="https://veggiescout.mgcafe.uky.edu/bacterial-wilt-cucurbit-crops",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Erwinia tracheiphila identification, diagnostic stringing ooze test, and cucumber beetle management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UKY_CUCURBIT_BACTERIAL_WILT"] = SOURCE_UKY_CUCURBIT_BACTERIAL_WILT

# Cucumber — Belly Rot
SOURCE_UKY_CUCURBIT_BELLY_ROT = SourceRecord(
    source_id="SRC_UKY_CUCURBIT_BELLY_ROT",
    title="Belly Rot of Cucurbit Crops",
    organization="University of Kentucky Extension (VeggieScout)",
    url_or_doi="https://veggiescout.mgcafe.uky.edu/belly-rot-cucurbit-crops",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Rhizoctonia solani fruit rot where cucumbers contact wet soil, crater-like lesions, brown mold, crop rotation, and plastic mulch barrier management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UKY_CUCURBIT_BELLY_ROT"] = SOURCE_UKY_CUCURBIT_BELLY_ROT

# Cucumber — Gummy Stem Blight
SOURCE_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT = SourceRecord(
    source_id="SRC_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT",
    title="Management of Gummy Stem Blight (Black Rot) on Cucurbits in Florida",
    organization="University of Florida IFAS Extension",
    url_or_doi="https://edis.ifas.ufl.edu/publication/PP280",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Stagonosporopsis cucurbitacearum (Didymella bryoniae) gummy stem blight etiology, stem cankers with amber exudate, foliar blight, fruit black rot, and fungicide resistance management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT"] = SOURCE_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT

# Cucumber — Pythium Fruit Rot (Cottony Leak)
SOURCE_MS_STATE_CUCURBIT_COTTONY_LEAK = SourceRecord(
    source_id="SRC_MSSTATE_CUCURBIT_COTTONY_LEAK",
    title="Cottony Leak in Cucurbits",
    organization="Mississippi State University Extension Service",
    url_or_doi="https://extension.msstate.edu/publications/cottony-leak-cucurbits",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Pythium aphanidermatum cottony leak on cucumber and cucurbit fruits, profuse white mycelium, wet soil contact, drainage, and cultural management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_MSSTATE_CUCURBIT_COTTONY_LEAK"] = SOURCE_MS_STATE_CUCURBIT_COTTONY_LEAK

SOURCE_UKY_CUCURBIT_COTTONY_LEAK = SourceRecord(
    source_id="SRC_UKY_CUCURBIT_COTTONY_LEAK",
    title="Cottony Leak of Cucurbit Crops",
    organization="University of Kentucky Extension (VeggieScout)",
    url_or_doi="https://veggiescout.mgcafe.uky.edu/cottony-leak-cucurbit-crops",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Pythium fruit rot symptoms, water-soaked softening, cottony mycelium, field sanitation, and postharvest prevention.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UKY_CUCURBIT_COTTONY_LEAK"] = SOURCE_UKY_CUCURBIT_COTTONY_LEAK

# Zucchini — Yellow Mosaic Virus (ZYMV)
SOURCE_PNW_SQUASH_VIRUS_DISEASES = SourceRecord(
    source_id="SRC_PNW_SQUASH_VIRUS_DISEASES",
    title="Squash (Cucurbita spp.)-Virus Diseases",
    organization="Pacific Northwest Plant Disease Management Handbook (OSU / WSU / UI)",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/squash-cucurbita-spp-virus-diseases",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Zucchini yellow mosaic virus (ZYMV), watermelon mosaic virus, severe foliar mosaic, fruit blistering and knobby distortion, aphid transmission, and resistant cultivars.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_SQUASH_VIRUS_DISEASES"] = SOURCE_PNW_SQUASH_VIRUS_DISEASES

SOURCE_UC_IPM_CUCURBIT_POTYVIRUSES = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_POTYVIRUSES",
    title="Potyviruses / Cucurbits",
    organization="University of California Statewide Integrated Pest Management Program (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/potyviruses/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Zucchini yellow mosaic virus (ZYMV) and watermelon mosaic virus potyvirus complex, aphid stylet transmission, silver reflective mulch, and cultivar resistance.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_POTYVIRUSES"] = SOURCE_UC_IPM_CUCURBIT_POTYVIRUSES

# ---------------------------------------------------------------------------
# Canonical Disease-Specific Source Association Map
# ---------------------------------------------------------------------------
DISEASE_SPECIFIC_SOURCES: dict[str, list[SourceRecord]] = {
    # Blueberry
    "blueberry__anthracnose": [SOURCE_NC_STATE_BLUEBERRY_ANTHRACNOSE, SOURCE_MSU_BLUEBERRY_ANTHRACNOSE],

    # Bell Pepper
    "bell_pepper__blossom_end_rot": [SOURCE_UGA_PEPPER_BLOSSOM_END_ROT],
    "bell_pepper__bacterial_spot": [SOURCE_NC_STATE_PEPPER_TOMATO_BACTERIAL_SPOT],
    "bell_pepper__frogeye_leaf_spot": [SOURCE_NC_STATE_PEPPER_FROGEYE_LEAF_SPOT, SOURCE_UF_IFAS_PEPPER_DISEASES],
    "bell_pepper__cercospora_leaf_spot": [SOURCE_NC_STATE_PEPPER_FROGEYE_LEAF_SPOT, SOURCE_UF_IFAS_PEPPER_DISEASES],
    "bell_pepper__frogeye": [SOURCE_NC_STATE_PEPPER_FROGEYE_LEAF_SPOT, SOURCE_UF_IFAS_PEPPER_DISEASES],
    "bell_pepper__leaf_curl": [SOURCE_UC_IPM_PEPPER_LEAF_CURL],
    "bell_pepper__curly_top": [SOURCE_UC_IPM_PEPPER_LEAF_CURL],
    "bell_pepper__powdery_mildew": [SOURCE_UC_IPM_PEPPER_POWDERY_MILDEW],

    # Tomato
    "tomato__early_blight": [SOURCE_NC_STATE_TOMATO_EARLY_BLIGHT],
    "tomato__late_blight": [SOURCE_NC_STATE_TOMATO_LATE_BLIGHT],
    "tomato__septoria_leaf_spot": [SOURCE_NC_STATE_TOMATO_SEPTORIA_LEAF_SPOT],
    "tomato__bacterial_leaf_spot": [SOURCE_NC_STATE_PEPPER_TOMATO_BACTERIAL_SPOT],
    "tomato__anthracnose": [SOURCE_UC_IPM_TOMATO_ANTHRACNOSE],
    "tomato__fruit_fusarium": [SOURCE_UC_IPM_TOMATO_FUSARIUM_ROT],
    "tomato__fusarium_rot": [SOURCE_UC_IPM_TOMATO_FUSARIUM_ROT],
    "tomato__fusarium": [SOURCE_UC_IPM_TOMATO_FUSARIUM_ROT],
    "tomato__leaf_mold": [SOURCE_UC_IPM_TOMATO_LEAF_MOLD],
    "tomato__mosaic_virus": [SOURCE_UC_IPM_TOMATO_MOSAIC_VIRUS],
    "tomato__mosaic": [SOURCE_UC_IPM_TOMATO_MOSAIC_VIRUS],
    "tomato__yellow_leaf_curl_virus": [SOURCE_UC_IPM_TOMATO_YELLOW_LEAF_CURL],
    "tomato__yellow_leaf_curl": [SOURCE_UC_IPM_TOMATO_YELLOW_LEAF_CURL],
    "tomato__tylcv": [SOURCE_UC_IPM_TOMATO_YELLOW_LEAF_CURL],

    # Cucurbits
    "cucumber__angular_leaf_spot": [
        SOURCE_UC_IPM_CUCURBIT_ANGULAR_LEAF_SPOT,
        SOURCE_PNW_CUCUMBER_ANGULAR_LEAF_SPOT,
        SOURCE_UKY_CUCURBIT_ANGULAR_LEAF_SPOT,
    ],
    "cucumber__anthracnose": [
        SOURCE_NC_STATE_CUCURBIT_ANTHRACNOSE,
        SOURCE_UC_IPM_CUCURBIT_ANTHRACNOSE,
        SOURCE_UKY_CUCURBIT_ANTHRACNOSE,
    ],
    "cucumber__bacterial_wilt": [
        SOURCE_UW_MADISON_CUCURBIT_BACTERIAL_WILT,
        SOURCE_PNW_CUCUMBER_BACTERIAL_WILT,
        SOURCE_UKY_CUCURBIT_BACTERIAL_WILT,
    ],
    "cucumber__belly_rot": [
        SOURCE_UKY_CUCURBIT_BELLY_ROT,
    ],
    "cucumber__rhizoctonia_fruit_rot": [
        SOURCE_UKY_CUCURBIT_BELLY_ROT,
    ],
    "cucumber__gummy_stem_blight": [
        SOURCE_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT,
    ],
    "cucumber__pythium_fruit_rot": [
        SOURCE_MS_STATE_CUCURBIT_COTTONY_LEAK,
        SOURCE_UKY_CUCURBIT_COTTONY_LEAK,
    ],
    "cucumber__cottony_leak": [
        SOURCE_MS_STATE_CUCURBIT_COTTONY_LEAK,
        SOURCE_UKY_CUCURBIT_COTTONY_LEAK,
    ],
    "cucumber__downy_mildew": [SOURCE_NC_STATE_CUCURBIT_DOWNY_MILDEW],
    "cucumber__powdery_mildew": [SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
    "squash__powdery_mildew": [SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
    "zucchini__bacterial_wilt": [
        SOURCE_UW_MADISON_CUCURBIT_BACTERIAL_WILT,
        SOURCE_PNW_CUCUMBER_BACTERIAL_WILT,
        SOURCE_UKY_CUCURBIT_BACTERIAL_WILT,
    ],
    "zucchini__yellow_mosaic_virus": [
        SOURCE_PNW_SQUASH_VIRUS_DISEASES,
        SOURCE_UC_IPM_CUCURBIT_POTYVIRUSES,
    ],
    "zucchini__yellow_mosaic": [
        SOURCE_PNW_SQUASH_VIRUS_DISEASES,
        SOURCE_UC_IPM_CUCURBIT_POTYVIRUSES,
    ],
    "zucchini__zymv": [
        SOURCE_PNW_SQUASH_VIRUS_DISEASES,
        SOURCE_UC_IPM_CUCURBIT_POTYVIRUSES,
    ],
    "zucchini__zucchini_yellow_mosaic": [
        SOURCE_PNW_SQUASH_VIRUS_DISEASES,
        SOURCE_UC_IPM_CUCURBIT_POTYVIRUSES,
    ],
    "zucchini__zucchini_yellow_mosaic_virus": [
        SOURCE_PNW_SQUASH_VIRUS_DISEASES,
        SOURCE_UC_IPM_CUCURBIT_POTYVIRUSES,
    ],
    "zucchini__powdery_mildew": [SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
    "zucchini__downy_mildew": [SOURCE_NC_STATE_CUCURBIT_DOWNY_MILDEW],

    # Potato
    "potato__early_blight": [SOURCE_UC_IPM_POTATO_EARLY_BLIGHT],
    "potato__late_blight": [SOURCE_UC_IPM_POTATO_LATE_BLIGHT],

    # Fruit / Stone Fruit
    "apple__scab": [SOURCE_UC_IPM_APPLE_SCAB],
    "peach__brown_rot": [SOURCE_UC_IPM_PEACH_BROWN_ROT],

    # Strawberry
    "strawberry__botrytis_blight": [SOURCE_UC_IPM_STRAWBERRY_BOTRYTIS],
    "strawberry__gray_mold": [SOURCE_UC_IPM_STRAWBERRY_BOTRYTIS],
    "strawberry__botrytis_fruit_rot": [SOURCE_UC_IPM_STRAWBERRY_BOTRYTIS],

    # 1. Banana — Anthracnose
    "banana__anthracnose": [SOURCE_PROMUSA_BANANA_ANTHRACNOSE],

    # 2. Banana — Cordana Leaf Spot
    "banana__cordana_leaf_spot": [SOURCE_PROMUSA_BANANA_CORDANA],
    "banana__cordana": [SOURCE_PROMUSA_BANANA_CORDANA],

    # 3. Banana — Panama Disease (Fusarium Wilt)
    "banana__panama_disease": [SOURCE_PROMUSA_BANANA_PANAMA],
    "banana__fusarium_wilt": [SOURCE_PROMUSA_BANANA_PANAMA],
    "banana__fusarium_wilt_of_banana": [SOURCE_PROMUSA_BANANA_PANAMA],
    "banana__panama": [SOURCE_PROMUSA_BANANA_PANAMA],

    # 4. Grape — Black Rot
    "grape__black_rot": [SOURCE_UC_IPM_GRAPE_BLACK_ROT, SOURCE_OSU_GRAPE_BLACK_ROT],

    # 5. Grape — Downy Mildew
    "grape__downy_mildew": [SOURCE_UC_IPM_GRAPE_DOWNY_MILDEW, SOURCE_OSU_GRAPE_DOWNY_MILDEW],

    # (Pre-existing) Grape — Powdery Mildew
    "grape__powdery_mildew": [SOURCE_UC_IPM_GRAPE_POWDERY_MILDEW],

    # 6. Citrus — Citrus Canker
    "citrus__canker": [SOURCE_UC_IPM_CITRUS_CANKER],
    "citrus__citrus_canker": [SOURCE_UC_IPM_CITRUS_CANKER],

    # 7. Citrus — Citrus Greening (Huanglongbing)
    "citrus__greening_disease": [SOURCE_UC_IPM_CITRUS_GREENING],
    "citrus__greening": [SOURCE_UC_IPM_CITRUS_GREENING],
    "citrus__citrus_greening": [SOURCE_UC_IPM_CITRUS_GREENING],
    "citrus__huanglongbing": [SOURCE_UC_IPM_CITRUS_GREENING],
    "citrus__hlb": [SOURCE_UC_IPM_CITRUS_GREENING],
    "citrus__huanglongbing_(hlb)": [SOURCE_UC_IPM_CITRUS_GREENING],

    # 8. Eggplant — Phomopsis Fruit Rot & Batch 1 Solanaceous Pathogens
    "eggplant__cercospora_leaf_spot": [SOURCE_PNW_EGGPLANT_CERCOSPORA],
    "eggplant__cercospora": [SOURCE_PNW_EGGPLANT_CERCOSPORA],
    "eggplant__mosaic_virus": [SOURCE_UC_IPM_EGGPLANT_MOSAIC],
    "eggplant__mosaic": [SOURCE_UC_IPM_EGGPLANT_MOSAIC],
    "eggplant__pest_damage": [SOURCE_PNW_EGGPLANT_FLEA_BEETLE, SOURCE_UC_IPM_EGGPLANT_FLEA_BEETLES],
    "eggplant__flea_beetle": [SOURCE_PNW_EGGPLANT_FLEA_BEETLE, SOURCE_UC_IPM_EGGPLANT_FLEA_BEETLES],
    "eggplant__flea_beetles": [SOURCE_PNW_EGGPLANT_FLEA_BEETLE, SOURCE_UC_IPM_EGGPLANT_FLEA_BEETLES],
    "eggplant__pest": [SOURCE_PNW_EGGPLANT_FLEA_BEETLE, SOURCE_UC_IPM_EGGPLANT_FLEA_BEETLES],
    "eggplant__phomopsis_fruit_rot": [SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS],
    "eggplant__phomopsis_blight": [SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS],
    "eggplant__phomopsis": [SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS],
    "eggplant__phomopsis_blight_and_fruit_rot": [SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS],
    "eggplant__phytophthora_blight": [SOURCE_CORNELL_PHYTOPHTHORA_BLIGHT, SOURCE_NC_STATE_PHYTOPHTHORA_BLIGHT],
    "eggplant__phytophthora": [SOURCE_CORNELL_PHYTOPHTHORA_BLIGHT, SOURCE_NC_STATE_PHYTOPHTHORA_BLIGHT],
    "eggplant__wilt_disease": [SOURCE_PNW_EGGPLANT_VERTICILLIUM, SOURCE_UC_IPM_EGGPLANT_VERTICILLIUM],
    "eggplant__verticillium_wilt": [SOURCE_PNW_EGGPLANT_VERTICILLIUM, SOURCE_UC_IPM_EGGPLANT_VERTICILLIUM],
    "eggplant__wilt": [SOURCE_PNW_EGGPLANT_VERTICILLIUM, SOURCE_UC_IPM_EGGPLANT_VERTICILLIUM],

    # 9. Corn — Common Smut
    "corn__smut": [SOURCE_OSU_CORN_COMMON_SMUT],
    "corn__common_smut": [SOURCE_OSU_CORN_COMMON_SMUT],
    "corn__common_smut_of_corn": [SOURCE_OSU_CORN_COMMON_SMUT],
    "corn__corn_smut": [SOURCE_OSU_CORN_COMMON_SMUT],

    # 10. Corn — Northern Corn Leaf Blight
    "corn__northern_leaf_blight": [SOURCE_OSU_CORN_NORTHERN_LEAF_BLIGHT],
    "corn__northern_corn_leaf_blight": [SOURCE_OSU_CORN_NORTHERN_LEAF_BLIGHT],

    # 11. Wheat — Head Scab (Fusarium Head Blight)
    "wheat__head_scab": [SOURCE_UNL_WHEAT_HEAD_SCAB, SOURCE_OSU_WHEAT_HEAD_SCAB],
    "wheat__fusarium_head_blight": [SOURCE_UNL_WHEAT_HEAD_SCAB, SOURCE_OSU_WHEAT_HEAD_SCAB],
    "wheat__wheat_head_scab": [SOURCE_UNL_WHEAT_HEAD_SCAB, SOURCE_OSU_WHEAT_HEAD_SCAB],
    "wheat__scab": [SOURCE_UNL_WHEAT_HEAD_SCAB, SOURCE_OSU_WHEAT_HEAD_SCAB],
    "wheat__head_scab_(fusarium_head_blight)": [SOURCE_UNL_WHEAT_HEAD_SCAB, SOURCE_OSU_WHEAT_HEAD_SCAB],

    # 12. Wheat — Rust
    "wheat__leaf_rust": [SOURCE_USDA_ARS_WHEAT_LEAF_RUST, SOURCE_UNL_WHEAT_LEAF_RUST],
    "wheat__stripe_rust": [SOURCE_USDA_ARS_WHEAT_STRIPE_RUST],
    "wheat__stem_rust": [SOURCE_USDA_ARS_WHEAT_STEM_RUST],
    "wheat__rust": [SOURCE_USDA_ARS_WHEAT_RUST],
    "wheat__wheat_rust": [SOURCE_USDA_ARS_WHEAT_RUST],
}



# =============================================================================
# Master Verified Disease-Specific Sources (All 151 Crop-Disease Classes)
# =============================================================================

SRC_UC_IPM_APPLE_BLACK_ROT = SourceRecord(
    source_id="SRC_UC_IPM_APPLE_BLACK_ROT",
    title="Apple: Black Rot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/apple/black-rot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Physalospora obtusa / Botryosphaeria obtusa symptoms, frogeye leaf spots, and canker management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_APPLE_BLACK_ROT"] = SRC_UC_IPM_APPLE_BLACK_ROT

SRC_UC_IPM_APPLE_MOSAIC = SourceRecord(
    source_id="SRC_UC_IPM_APPLE_MOSAIC",
    title="Apple: Apple Mosaic",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/apple/apple-mosaic/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Apple mosaic virus (ApMV) leaf chlorosis, vein clearing patterns, and virus-free rootstock management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_APPLE_MOSAIC"] = SRC_UC_IPM_APPLE_MOSAIC

SRC_OSU_APPLE_RUSTS = SourceRecord(
    source_id="SRC_OSU_APPLE_RUSTS",
    title="Cedar-Apple Rust and Related Rusts on Apple",
    organization="Ohio State University Extension (Ohioline)",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-fru-02",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Gymnosporangium juniperi-virginianae etiology, alternate juniper hosts, and resistance management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_APPLE_RUSTS"] = SRC_OSU_APPLE_RUSTS

SRC_UC_IPM_APPLE_SCAB = SourceRecord(
    source_id="SRC_UC_IPM_APPLE_SCAB",
    title="Apple: Apple Scab",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/apple/apple-scab/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Venturia inaequalis ascospore release, Mills infection periods, and fungicide resistance management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_APPLE_SCAB"] = SRC_UC_IPM_APPLE_SCAB

SRC_LUCID_BANANA_ANTHRACNOSE = SourceRecord(
    source_id="SRC_LUCID_BANANA_ANTHRACNOSE",
    title="Banana Anthracnose (267)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/banana_anthracnose_267.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum musae fruit rot and diamond-shaped foliar lesion identification.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_BANANA_ANTHRACNOSE"] = SRC_LUCID_BANANA_ANTHRACNOSE

SRC_UF_IFAS_BANANA_BLACK_SIGATOKA = SourceRecord(
    source_id="SRC_UF_IFAS_BANANA_BLACK_SIGATOKA",
    title="Black Sigatoka: An Increasing Threat to Banana Production",
    organization="University of Florida IFAS Extension (EDIS)",
    url_or_doi="https://edis.ifas.ufl.edu/publication/PP316",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pseudocercospora fijiensis (Black leaf streak / Black Sigatoka) symptom progression, necrotic leaf streaks, and fungicide management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UF_IFAS_BANANA_BLACK_SIGATOKA"] = SRC_UF_IFAS_BANANA_BLACK_SIGATOKA

SRC_LUCID_BANANA_BUNCHY_TOP = SourceRecord(
    source_id="SRC_LUCID_BANANA_BUNCHY_TOP",
    title="Banana Bunchy Top (121)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/banana_bunchy_top_121.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Banana bunchy top virus (BBTV) transmission by Pentalonia nigronervosa, dot-dash veins, and rosette stunting.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_BANANA_BUNCHY_TOP"] = SRC_LUCID_BANANA_BUNCHY_TOP

SRC_LUCID_BANANA_CIGAR_END = SourceRecord(
    source_id="SRC_LUCID_BANANA_CIGAR_END",
    title="Banana Cigar End Rot (345)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/banana_cigar_end_rot_345.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Musicillium theobromae (Trachysphaera / Verticillium theobromae) tip necrosis resembling burnt cigar ash.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_BANANA_CIGAR_END"] = SRC_LUCID_BANANA_CIGAR_END

SRC_LUCID_BANANA_CORDANA = SourceRecord(
    source_id="SRC_LUCID_BANANA_CORDANA",
    title="Banana Diamond Leaf Spot (072) / Cordana Leaf Spot",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/banana_diamond_leaf_spot_072.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Cordana musae large oval-to-diamond necrotic leaf spots with distinct bright yellow halos.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_BANANA_CORDANA"] = SRC_LUCID_BANANA_CORDANA

SRC_LUCID_BANANA_FUSARIUM = SourceRecord(
    source_id="SRC_LUCID_BANANA_FUSARIUM",
    title="Banana Fusarium Wilt (Panama Disease) (176)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/banana_fusarium_wilt_176.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Fusarium oxysporum f. sp. cubense Tropical Race 4 vascular discoloration, leaf skirt collapse, and quarantine sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_BANANA_FUSARIUM"] = SRC_LUCID_BANANA_FUSARIUM

SRC_CORNELL_BASIL_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_CORNELL_BASIL_DOWNY_MILDEW",
    title="Basil Downy Mildew",
    organization="Cornell University Cooperative Extension Vegetable Pathology",
    url_or_doi="https://www.vegetables.cornell.edu/pest-management/disease-factsheets/basil-downy-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Peronospora belbahrii interveinal leaf chlorosis, purplish-gray sporulation on undersides, and resistant cultivar selection.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_CORNELL_BASIL_DOWNY_MILDEW"] = SRC_CORNELL_BASIL_DOWNY_MILDEW

SRC_UC_IPM_BEAN_ANGULAR_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_BEAN_ANGULAR_SPOT",
    title="Dry Beans: Angular Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/dry-beans/angular-leaf-spot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pseudocercospora griseola delimited angular lesions, defoliation, and clean certified seed protocols.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_BEAN_ANGULAR_SPOT"] = SRC_UC_IPM_BEAN_ANGULAR_SPOT

SRC_UC_IPM_BEAN_HALO_BLIGHT = SourceRecord(
    source_id="SRC_UC_IPM_BEAN_HALO_BLIGHT",
    title="Dry Beans: Halo Blight",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/dry-beans/halo-blight/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pseudomonas savastanoi pv. phaseolicola phaseolotoxin chlorotic halos, systemic grease spots, and seed sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_BEAN_HALO_BLIGHT"] = SRC_UC_IPM_BEAN_HALO_BLIGHT

SRC_UC_IPM_BEAN_COMMON_MOSAIC = SourceRecord(
    source_id="SRC_UC_IPM_BEAN_COMMON_MOSAIC",
    title="Dry Beans: Bean Common Mosaic",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/dry-beans/bean-common-mosaic/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Bean common mosaic virus (BCMV) aphid transmission, leaf puckering, and dominant I-gene resistance.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_BEAN_COMMON_MOSAIC"] = SRC_UC_IPM_BEAN_COMMON_MOSAIC

SRC_UC_IPM_BEAN_RUST = SourceRecord(
    source_id="SRC_UC_IPM_BEAN_RUST",
    title="Dry Beans: Rust",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/dry-beans/rust/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Uromyces appendiculatus cinnamon-brown uredinial pustules, yellow halos, and preventative fungicide timings.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_BEAN_RUST"] = SRC_UC_IPM_BEAN_RUST

SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT = SourceRecord(
    source_id="SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT",
    title="Bacterial Spot of Pepper and Tomato",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/bacterial-spot-of-pepper-and-tomato",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas euvesicatoria / X. perforans necrotic spots, seed treatments, and copper-mancozeb tank mixes.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT"] = SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT

SRC_UGA_PEPPER_BLOSSOM_END_ROT = SourceRecord(
    source_id="SRC_UGA_PEPPER_BLOSSOM_END_ROT",
    title="Blossom-End Rot in Bell Pepper",
    organization="University of Georgia Extension (UGA Extension)",
    url_or_doi="https://extension.uga.edu/publications/detail.html?number=C938",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Physiological calcium deficiency, transpiration imbalance, and moisture management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UGA_PEPPER_BLOSSOM_END_ROT"] = SRC_UGA_PEPPER_BLOSSOM_END_ROT

SRC_UF_IFAS_PEPPER_FROGEYE = SourceRecord(
    source_id="SRC_UF_IFAS_PEPPER_FROGEYE",
    title="Cercospora Leaf Spot (Frogeye Leaf Spot) of Pepper",
    organization="University of Florida IFAS Extension (EDIS)",
    url_or_doi="https://edis.ifas.ufl.edu/publication/in168",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora capsici circular frog-eye spots, premature defoliation, and protective fungicide sprays.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UF_IFAS_PEPPER_FROGEYE"] = SRC_UF_IFAS_PEPPER_FROGEYE

SRC_LUCID_CHILLI_LEAF_CURL = SourceRecord(
    source_id="SRC_LUCID_CHILLI_LEAF_CURL",
    title="Chilli Leaf Curl Virus (367)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/chilli_leaf_curl_367.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Chilli leaf curl begomovirus whitefly transmission (Bemisia tabaci), leaf cupping, curling, and stunting.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_CHILLI_LEAF_CURL"] = SRC_LUCID_CHILLI_LEAF_CURL

SRC_UC_IPM_PEPPER_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_PEPPER_POWDERY_MILDEW",
    title="Peppers: Powdery Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/peppers/powdery-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Leveillula taurica endophytic powdery mildew, underside white mycelium, and sulfur / strobilurin controls.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PEPPER_POWDERY_MILDEW"] = SRC_UC_IPM_PEPPER_POWDERY_MILDEW

SRC_UC_IPM_BLUEBERRY_ANTHRACNOSE = SourceRecord(
    source_id="SRC_UC_IPM_BLUEBERRY_ANTHRACNOSE",
    title="Blueberries: Anthracnose Fruit Rot (Ripe Rot)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/blueberry/anthracnose-fruit-rot-ripe-rot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum fioriniae / C. acutatum salmon-orange spore masses, twig blights, and blossom spray timings.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_BLUEBERRY_ANTHRACNOSE"] = SRC_UC_IPM_BLUEBERRY_ANTHRACNOSE

SRC_PNW_BLUEBERRY_BOTRYTIS = SourceRecord(
    source_id="SRC_PNW_BLUEBERRY_BOTRYTIS",
    title="Blueberry (Vaccinium corymbosum)-Botrytis Blight",
    organization="Pacific Northwest Plant Disease Management Handbook",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/blueberry-vaccinium-corymbosum-botrytis-blight",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Botrytis cinerea blossom blight, twig dieback, and gray mold sporulation during cool damp blooms.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_BLUEBERRY_BOTRYTIS"] = SRC_PNW_BLUEBERRY_BOTRYTIS

SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM = SourceRecord(
    source_id="SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM",
    title="Exobasidium Leaf and Fruit Spot of Blueberry",
    organization="University of Florida IFAS Extension (EDIS)",
    url_or_doi="https://edis.ifas.ufl.edu/publication/PP389",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Exobasidium maculosum circular pale-green to white leaf spots, fruit lesions, and dormant lime-sulfur control.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM"] = SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM

SRC_UC_IPM_BLUEBERRY_MUMMY_BERRY = SourceRecord(
    source_id="SRC_UC_IPM_BLUEBERRY_MUMMY_BERRY",
    title="Blueberries: Mummy Berry",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/blueberry/mummy-berry/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Monilinia vaccinii-corymbosi apothecia cups, shoot blight phase, and mummified shriveled fruit prevention.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_BLUEBERRY_MUMMY_BERRY"] = SRC_UC_IPM_BLUEBERRY_MUMMY_BERRY

SRC_PNW_BLUEBERRY_RUST = SourceRecord(
    source_id="SRC_PNW_BLUEBERRY_RUST",
    title="Blueberry (Vaccinium corymbosum)-Rust",
    organization="Pacific Northwest Plant Disease Management Handbook",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/blueberry-vaccinium-corymbosum-rust",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Thekopsora minima (Pucciniastrum vaccinii) lower leaf yellow-orange urediniospores and premature defoliation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_BLUEBERRY_RUST"] = SRC_PNW_BLUEBERRY_RUST

SRC_PNW_BLUEBERRY_SCORCH = SourceRecord(
    source_id="SRC_PNW_BLUEBERRY_SCORCH",
    title="Blueberry (Vaccinium corymbosum)-Scorch",
    organization="Pacific Northwest Plant Disease Management Handbook",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/blueberry-vaccinium-corymbosum-scorch",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Blueberry scorch carlavirus (BlScV) aphid transmission, sudden blossom and leaf blight, and rogueing protocols.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_BLUEBERRY_SCORCH"] = SRC_PNW_BLUEBERRY_SCORCH

SRC_UGA_BLUEBERRY_SEPTORIA = SourceRecord(
    source_id="SRC_UGA_BLUEBERRY_SEPTORIA",
    title="Septoria Leaf Spot of Blueberry",
    organization="University of Georgia Extension (UGA Extension)",
    url_or_doi="https://extension.uga.edu/publications/detail.html?number=C1099",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Septoria albopunctata small circular spots with white centers and purple margins, summer defoliation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UGA_BLUEBERRY_SEPTORIA"] = SRC_UGA_BLUEBERRY_SEPTORIA

SRC_UC_IPM_COLE_ALTERNARIA = SourceRecord(
    source_id="SRC_UC_IPM_COLE_ALTERNARIA",
    title="Cole Crops: Alternaria Head Rot and Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/alternaria-head-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria brassicae / A. brassicicola target-board spots, brown-black head decay, and crop residue burial.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_ALTERNARIA"] = SRC_UC_IPM_COLE_ALTERNARIA

SRC_UC_IPM_COLE_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_COLE_DOWNY_MILDEW",
    title="Cole Crops: Downy Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/downy-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Hyaloperonospora brassicae chlorotic angular patches on upper leaf surfaces and white downy growth beneath.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_DOWNY_MILDEW"] = SRC_UC_IPM_COLE_DOWNY_MILDEW

SRC_UC_IPM_COLE_RINGSPOT = SourceRecord(
    source_id="SRC_UC_IPM_COLE_RINGSPOT",
    title="Cole Crops: Ringspot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/ringspot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Mycosphaerella brassicicola circular gray-brown spots with concentric rings of black fruiting bodies.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_RINGSPOT"] = SRC_UC_IPM_COLE_RINGSPOT

SRC_UC_IPM_COLE_ALTERNARIA_CABBAGE = SourceRecord(
    source_id="SRC_UC_IPM_COLE_ALTERNARIA_CABBAGE",
    title="Cole Crops: Alternaria Head Rot and Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/alternaria-head-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria brassicae concentric ring spots on cabbage outer leaves and head tissues.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_ALTERNARIA_CABBAGE"] = SRC_UC_IPM_COLE_ALTERNARIA_CABBAGE

SRC_UC_IPM_COLE_BLACK_ROT = SourceRecord(
    source_id="SRC_UC_IPM_COLE_BLACK_ROT",
    title="Cole Crops: Black Rot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/black-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas campestris pv. campestris V-shaped marginal chlorosis, blackened vascular veins, and hot water seed treatment.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_BLACK_ROT"] = SRC_UC_IPM_COLE_BLACK_ROT

SRC_UC_IPM_COLE_DOWNY_MILDEW_CABBAGE = SourceRecord(
    source_id="SRC_UC_IPM_COLE_DOWNY_MILDEW_CABBAGE",
    title="Cole Crops: Downy Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/downy-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Hyaloperonospora parasitica downy mildew on cabbage seedling cotyledons and mature heads.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_DOWNY_MILDEW_CABBAGE"] = SRC_UC_IPM_COLE_DOWNY_MILDEW_CABBAGE

SRC_UC_IPM_CARROT_ALTERNARIA = SourceRecord(
    source_id="SRC_UC_IPM_CARROT_ALTERNARIA",
    title="Carrot: Alternaria Leaf Blight",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/carrot/alternaria-leaf-blight/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria dauci brown-black foliar lesions, petiole girdling, and mechanical harvesting interference.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CARROT_ALTERNARIA"] = SRC_UC_IPM_CARROT_ALTERNARIA

SRC_UC_IPM_CARROT_CAVITY_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_CARROT_CAVITY_SPOT",
    title="Carrot: Cavity Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/carrot/cavity-spot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Pythium sulcatum / P. ultimum elliptical horizontal root cavities, soil moisture control, and metalaxyl treatment.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CARROT_CAVITY_SPOT"] = SRC_UC_IPM_CARROT_CAVITY_SPOT

SRC_UC_IPM_CARROT_CERCOSPORA = SourceRecord(
    source_id="SRC_UC_IPM_CARROT_CERCOSPORA",
    title="Carrot: Cercospora Leaf Blight",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/carrot/cercospora-leaf-blight/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora carotae circular tan lesions on young leaf margins, leaf curling, and spray thresholds.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CARROT_CERCOSPORA"] = SRC_UC_IPM_CARROT_CERCOSPORA

SRC_UC_IPM_COLE_ALTERNARIA_CAULIFLOWER = SourceRecord(
    source_id="SRC_UC_IPM_COLE_ALTERNARIA_CAULIFLOWER",
    title="Cole Crops: Alternaria Head Rot and Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/alternaria-head-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria brassicae concentric ring spots, curd browning, and hot-water seed treatment.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_ALTERNARIA_CAULIFLOWER"] = SRC_UC_IPM_COLE_ALTERNARIA_CAULIFLOWER

SRC_UC_IPM_COLE_ALTERNARIA_LEAF_CAULIFLOWER = SourceRecord(
    source_id="SRC_UC_IPM_COLE_ALTERNARIA_LEAF_CAULIFLOWER",
    title="Cole Crops: Alternaria Head Rot and Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/alternaria-head-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria brassicicola foliar target spots, yellow halos, and defoliation on cauliflower.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_ALTERNARIA_LEAF_CAULIFLOWER"] = SRC_UC_IPM_COLE_ALTERNARIA_LEAF_CAULIFLOWER

SRC_WISC_BACTERIAL_SOFT_ROT = SourceRecord(
    source_id="SRC_WISC_BACTERIAL_SOFT_ROT",
    title="Bacterial Soft Rot",
    organization="University of Wisconsin-Madison Division of Extension",
    url_or_doi="https://hort.extension.wisc.edu/articles/bacterial-soft-rot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pectobacterium carotovorum (Erwinia carotovora) curd liquefaction, foul odor, and postharvest dip hygiene.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_WISC_BACTERIAL_SOFT_ROT"] = SRC_WISC_BACTERIAL_SOFT_ROT

SRC_UC_IPM_COLE_BLACK_ROT_CAULIFLOWER = SourceRecord(
    source_id="SRC_UC_IPM_COLE_BLACK_ROT_CAULIFLOWER",
    title="Cole Crops: Black Rot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/black-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas campestris pv. campestris systemic hydathode invasion, V-shaped chlorosis, and curd rot.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_BLACK_ROT_CAULIFLOWER"] = SRC_UC_IPM_COLE_BLACK_ROT_CAULIFLOWER

SRC_UC_IPM_COLE_ALTERNARIA_BLACK_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_COLE_ALTERNARIA_BLACK_SPOT",
    title="Cole Crops: Alternaria Head Rot and Leaf Spot (Black Spot)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/alternaria-head-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria black spot / fleck on cauliflower leaves and curd florets; terminology notes documented.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_ALTERNARIA_BLACK_SPOT"] = SRC_UC_IPM_COLE_ALTERNARIA_BLACK_SPOT

SRC_UC_IPM_COLE_DOWNY_MILDEW_CAULIFLOWER = SourceRecord(
    source_id="SRC_UC_IPM_COLE_DOWNY_MILDEW_CAULIFLOWER",
    title="Cole Crops: Downy Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/downy-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Peronospora parasitica white sporulation on cauliflower undersides and internal curd discoloration.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_DOWNY_MILDEW_CAULIFLOWER"] = SRC_UC_IPM_COLE_DOWNY_MILDEW_CAULIFLOWER

SRC_UC_IPM_COLE_CABBAGE_LOOPER = SourceRecord(
    source_id="SRC_UC_IPM_COLE_CABBAGE_LOOPER",
    title="Cole Crops: Cabbage Looper and Foliar Caterpillars",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cole-crops/cabbage-looper/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Trichoplusia ni and Plutella xylostella chewed ragged holes, frass contamination, and Bacillus thuringiensis control.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_COLE_CABBAGE_LOOPER"] = SRC_UC_IPM_COLE_CABBAGE_LOOPER

SRC_UC_IPM_CELERY_ANTHRACNOSE = SourceRecord(
    source_id="SRC_UC_IPM_CELERY_ANTHRACNOSE",
    title="Celery: Anthracnose",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/celery/anthracnose/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum fioriniae / C. nymphaeae petiole curling, twisting, brown oval lesions, and crown rot.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CELERY_ANTHRACNOSE"] = SRC_UC_IPM_CELERY_ANTHRACNOSE

SRC_UC_IPM_CELERY_EARLY_BLIGHT = SourceRecord(
    source_id="SRC_UC_IPM_CELERY_EARLY_BLIGHT",
    title="Celery: Early Blight",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/celery/early-blight/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora apii yellow-to-brown necrotic foliar spots lacking dark borders, petiole lesions, and fungicides.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CELERY_EARLY_BLIGHT"] = SRC_UC_IPM_CELERY_EARLY_BLIGHT

SRC_UC_IPM_CHERRY_LEAF_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_CHERRY_LEAF_SPOT",
    title="Cherries: Cherry Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cherry/cherry-leaf-spot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Blumeriella jaapii circular purple-to-brown spots, shot-hole drop, yellowing, and post-harvest defoliation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CHERRY_LEAF_SPOT"] = SRC_UC_IPM_CHERRY_LEAF_SPOT

SRC_UC_IPM_CHERRY_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_CHERRY_POWDERY_MILDEW",
    title="Cherries: Powdery Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cherry/powdery-mildew/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Podosphaera clandestina white felt-like mycelium on foliage, fruit webbing, and fungicide spray programs.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CHERRY_POWDERY_MILDEW"] = SRC_UC_IPM_CHERRY_POWDERY_MILDEW

SRC_UC_IPM_CITRUS_CANKER = SourceRecord(
    source_id="SRC_UC_IPM_CITRUS_CANKER",
    title="Citrus: Citrus Canker",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/citrus/citrus-canker/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas citri subsp. citri raised corky pustules with oily margins and chlorotic halos.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CITRUS_CANKER"] = SRC_UC_IPM_CITRUS_CANKER

SRC_UC_IPM_CITRUS_HLB = SourceRecord(
    source_id="SRC_UC_IPM_CITRUS_HLB",
    title="Citrus: Huanglongbing (Citrus Greening)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/citrus/citrus-greening-huanglongbing/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Candidatus Liberibacter asiaticus psyllid-vectored asymmetric blotchy mottle, bitter misshapen fruit, and eradication protocols.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CITRUS_HLB"] = SRC_UC_IPM_CITRUS_HLB

SRC_LUCID_COFFEE_BROWN_EYE = SourceRecord(
    source_id="SRC_LUCID_COFFEE_BROWN_EYE",
    title="Coffee Brown-Eye Spot and Berry Blotch (142)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/coffee_brown_eye_spot_142.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora coffeicola berry blotch (red blister) on developing cherries and leaf eyespots under nutritional stress.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_COFFEE_BROWN_EYE"] = SRC_LUCID_COFFEE_BROWN_EYE

SRC_LUCID_COFFEE_THREAD_BLIGHT = SourceRecord(
    source_id="SRC_LUCID_COFFEE_THREAD_BLIGHT",
    title="Coffee Thread Blight / Black Rot (199)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/coffee_thread_blight_199.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Corticium koleroga / Pellicularia koleroga mycelial threads binding blackened dead leaves and berries to twigs.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_COFFEE_THREAD_BLIGHT"] = SRC_LUCID_COFFEE_THREAD_BLIGHT

SRC_LUCID_COFFEE_BROWN_EYE_2 = SourceRecord(
    source_id="SRC_LUCID_COFFEE_BROWN_EYE_2",
    title="Coffee Brown-Eye Spot (142)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/coffee_brown_eye_spot_142.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora coffeicola circular spots with grey centers and yellow halos on leaves, shade management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_COFFEE_BROWN_EYE_2"] = SRC_LUCID_COFFEE_BROWN_EYE_2

SRC_LUCID_COFFEE_RUST = SourceRecord(
    source_id="SRC_LUCID_COFFEE_RUST",
    title="Coffee Rust (141)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/coffee_rust_141.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Hemileia vastatrix yellow-orange powdery urediniospore patches on undersides of leaves causing catastrophic defoliation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_COFFEE_RUST"] = SRC_LUCID_COFFEE_RUST

SRC_CPN_CORN_GRAY_LEAF_SPOT = SourceRecord(
    source_id="SRC_CPN_CORN_GRAY_LEAF_SPOT",
    title="Gray Leaf Spot of Corn",
    organization="Crop Protection Network (Land-Grant University Collaboration)",
    url_or_doi="https://cropprotectionnetwork.org/encyclopedia/gray-leaf-spot-of-corn",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora zeae-maydis rectangular lesions delimited by leaf veins, hybrid resistance, and foliar fungicides.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_CPN_CORN_GRAY_LEAF_SPOT"] = SRC_CPN_CORN_GRAY_LEAF_SPOT

SRC_OSU_CORN_NORTHERN_LEAF_BLIGHT = SourceRecord(
    source_id="SRC_OSU_CORN_NORTHERN_LEAF_BLIGHT",
    title="Northern Corn Leaf Blight",
    organization="Ohio State University Extension (Ohioline)",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-cer-10",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Exserohilum turcicum cigar-shaped elliptical lesions, Ht gene resistance, and residue tillage.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_CORN_NORTHERN_LEAF_BLIGHT"] = SRC_OSU_CORN_NORTHERN_LEAF_BLIGHT

SRC_CPN_CORN_COMMON_RUST = SourceRecord(
    source_id="SRC_CPN_CORN_COMMON_RUST",
    title="Common Rust of Corn",
    organization="Crop Protection Network (Land-Grant University Collaboration)",
    url_or_doi="https://cropprotectionnetwork.org/encyclopedia/common-rust-of-corn",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Puccinia sorghi cinnamon-brown pustules scattered on upper and lower leaf surfaces, Rp-resistant hybrids.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_CPN_CORN_COMMON_RUST"] = SRC_CPN_CORN_COMMON_RUST

SRC_OSU_CORN_COMMON_SMUT = SourceRecord(
    source_id="SRC_OSU_CORN_COMMON_SMUT",
    title="Common Smut of Corn",
    organization="Ohio State University Extension (Ohioline)",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-cer-06",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Ustilago maydis swollen greenish-white galls bursting with black teliospores on ears and stalks.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_CORN_COMMON_SMUT"] = SRC_OSU_CORN_COMMON_SMUT

SRC_UC_IPM_CUCURBIT_ANGULAR_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_ANGULAR_SPOT",
    title="Cucurbits: Angular Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/angular-leaf-spot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pseudomonas syringae pv. lachrymans angular lesions bounded by veins, bacterial weeping, and copper controls.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_ANGULAR_SPOT"] = SRC_UC_IPM_CUCURBIT_ANGULAR_SPOT

SRC_UC_IPM_CUCURBIT_ANTHRACNOSE = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_ANTHRACNOSE",
    title="Cucurbits: Anthracnose",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/anthracnose/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum orbiculare circular brown foliar spots, shot-hole centers, and circular sunken fruit lesions.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_ANTHRACNOSE"] = SRC_UC_IPM_CUCURBIT_ANTHRACNOSE

SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT = SourceRecord(
    source_id="SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT",
    title="Bacterial Wilt of Cucurbits",
    organization="University of Wisconsin-Madison Division of Extension",
    url_or_doi="https://hort.extension.wisc.edu/articles/bacterial-wilt/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Erwinia tracheiphila transmission by striped and spotted cucumber beetles, xylem sticky strand test.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT"] = SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT

SRC_UKY_CUCURBIT_BELLY_ROT = SourceRecord(
    source_id="SRC_UKY_CUCURBIT_BELLY_ROT",
    title="Belly Rot of Cucurbit Crops",
    organization="University of Kentucky Extension (VeggieScout)",
    url_or_doi="https://veggiescout.mgcafe.uky.edu/belly-rot-cucurbit-crops",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Rhizoctonia solani water-soaked tan-to-brown lesions on fruit touching soil, plastic mulching prevention.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UKY_CUCURBIT_BELLY_ROT"] = SRC_UKY_CUCURBIT_BELLY_ROT

SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW",
    title="Cucurbit Downy Mildew",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/cucurbit-downy-mildew",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Pseudoperonospora cubensis angular chlorotic lesions delimited by major veins and dark purplish sporulation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW"] = SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW

SRC_UC_IPM_CUCURBIT_GUMMY_STEM = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_GUMMY_STEM",
    title="Cucurbits: Gummy Stem Blight (Black Rot)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/gummy-stem-blight-black-rot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Stagonosporopsis cucurbitacearum amber gummy exudate, stem cankers, and pycnidia rings.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_GUMMY_STEM"] = SRC_UC_IPM_CUCURBIT_GUMMY_STEM

SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW",
    title="Cucurbits: Powdery Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/powdery-mildew/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Podosphaera xanthii talcum powder-like fungal patches on leaf surfaces, petiole dieback, and resistant hybrids.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW"] = SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW

SRC_UC_IPM_CUCURBIT_PYTHIUM_ROT = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_PYTHIUM_ROT",
    title="Cucurbits: Pythium Fruit Rot (Cottony Leak)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/pythium-fruit-rot-cottony-leak/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pythium ultimum soft watery collapse with copious fluffy white mycelium, drainage ditch sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_PYTHIUM_ROT"] = SRC_UC_IPM_CUCURBIT_PYTHIUM_ROT

SRC_PNW_EGGPLANT_CERCOSPORA = SourceRecord(
    source_id="SRC_PNW_EGGPLANT_CERCOSPORA",
    title="Eggplant (Solanum melongena)-Cercospora Leaf Spot",
    organization="Pacific Northwest Plant Disease Management Handbook (OSU / WSU / UI)",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/eggplant-solanum-melongena-cercospora-leaf-spot",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora melongenae circular necrotic leaf spots, concentric ringing, chlorotic halos, and defoliation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_EGGPLANT_CERCOSPORA"] = SRC_PNW_EGGPLANT_CERCOSPORA

SRC_UC_IPM_EGGPLANT_MOSAIC = SourceRecord(
    source_id="SRC_UC_IPM_EGGPLANT_MOSAIC",
    title="Eggplant: Tobacco Mosaic",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/eggplant/tobacco-mosaic/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Tobacco mosaic virus (TMV) foliar mottling, leaf distortion, mechanical transmission, and greenhouse sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_EGGPLANT_MOSAIC"] = SRC_UC_IPM_EGGPLANT_MOSAIC

SRC_UC_IPM_EGGPLANT_FLEA_BEETLES = SourceRecord(
    source_id="SRC_UC_IPM_EGGPLANT_FLEA_BEETLES",
    title="Eggplant: Flea Beetles",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/eggplant/flea-beetles/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Epitrix fuscula shothole foliage perforation, seedling defoliation, row covers, and spinosad control.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_EGGPLANT_FLEA_BEETLES"] = SRC_UC_IPM_EGGPLANT_FLEA_BEETLES

SRC_RUTGERS_EGGPLANT_PHOMOPSIS = SourceRecord(
    source_id="SRC_RUTGERS_EGGPLANT_PHOMOPSIS",
    title="Phomopsis Fruit Rot in Eggplant",
    organization="Rutgers New Jersey Agricultural Experiment Station (NJAES) Cooperative Extension",
    url_or_doi="https://plant-pest-advisory.rutgers.edu/phomopsis-fruit-rot-in-eggplant/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Diaporthe vexans (Phomopsis vexans) sunken brown fruit lesions with concentric rings of pycnidia.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_RUTGERS_EGGPLANT_PHOMOPSIS"] = SRC_RUTGERS_EGGPLANT_PHOMOPSIS

SRC_NCSTATE_SOLANACEOUS_PHYTOPHTHORA = SourceRecord(
    source_id="SRC_NCSTATE_SOLANACEOUS_PHYTOPHTHORA",
    title="Phytophthora Blight of Peppers and Other Solanaceous Crops",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/phytophthora-blight-of-peppers",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Phytophthora capsici crown rot, black stem lesions, rapid wilting, and raised-bed drainage requirements.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_SOLANACEOUS_PHYTOPHTHORA"] = SRC_NCSTATE_SOLANACEOUS_PHYTOPHTHORA

SRC_UC_IPM_EGGPLANT_VERTICILLIUM = SourceRecord(
    source_id="SRC_UC_IPM_EGGPLANT_VERTICILLIUM",
    title="Eggplant: Verticillium Wilt",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/eggplant/verticillium-wilt/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Verticillium dahliae vascular discoloration, unilateral leaf wilting, and microsclerotia soil persistence.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_EGGPLANT_VERTICILLIUM"] = SRC_UC_IPM_EGGPLANT_VERTICILLIUM

SRC_UC_IPM_GARLIC_STEMPHYLIUM = SourceRecord(
    source_id="SRC_UC_IPM_GARLIC_STEMPHYLIUM",
    title="Garlic: Stemphylium Leaf Blight",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/garlic/stemphylium-leaf-blight/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Stemphylium vesicarium yellow-to-tan apical foliar lesions, tip dieback, and protective fungicides.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_GARLIC_STEMPHYLIUM"] = SRC_UC_IPM_GARLIC_STEMPHYLIUM

SRC_UC_IPM_GARLIC_RUST = SourceRecord(
    source_id="SRC_UC_IPM_GARLIC_RUST",
    title="Garlic: Rust",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/garlic/rust/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Puccinia allii orange pustules, leaf chlorosis, premature bulb cessation, and azoxystrobin/tebuconazole.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_GARLIC_RUST"] = SRC_UC_IPM_GARLIC_RUST

SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT = SourceRecord(
    source_id="SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT",
    title="Ginger: Leaf Spot and Foliar Blight",
    organization="Tamil Nadu Agricultural University (TNAU Agritech Portal)",
    url_or_doi="https://agritech.tnau.ac.in/crop_protection/ginger_diseases3.html",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Phyllosticta zingiberi and foliar blight necrosis; expanding lesions causing extensive leaf drying.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT"] = SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT

SRC_TNAU_GINGER_LEAF_SPOT = SourceRecord(
    source_id="SRC_TNAU_GINGER_LEAF_SPOT",
    title="Ginger: Leaf Spot (Phyllosticta zingiberi)",
    organization="Tamil Nadu Agricultural University (TNAU Agritech Portal)",
    url_or_doi="https://agritech.tnau.ac.in/crop_protection/ginger_diseases3.html",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Phyllosticta zingiberi oval white spots with dark margins and yellow halos, severe in unshaded fields.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_TNAU_GINGER_LEAF_SPOT"] = SRC_TNAU_GINGER_LEAF_SPOT

SRC_LUCID_GINGER_WEEVIL = SourceRecord(
    source_id="SRC_LUCID_GINGER_WEEVIL",
    title="Ginger Weevil and Pests (357)",
    organization="Pacific Pests, Pathogens and Weeds (Lucidcentral / ACIAR)",
    url_or_doi="https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/ginger_weevil_357.htm",
    publication_year=2021,
    source_tier=SourceTier.TIER_2,
    notes="Elytroteinus subtruncatus and insect pest boring into ginger rhizomes and pseudostems.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_LUCID_GINGER_WEEVIL"] = SRC_LUCID_GINGER_WEEVIL

SRC_TNAU_GINGER_SOFT_ROT_SHEATH = SourceRecord(
    source_id="SRC_TNAU_GINGER_SOFT_ROT_SHEATH",
    title="Ginger: Soft Rot and Collar/Sheath Rot",
    organization="Tamil Nadu Agricultural University (TNAU Agritech Portal)",
    url_or_doi="https://agritech.tnau.ac.in/crop_protection/ginger_diseases1.html",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pythium / Rhizoctonia collar rot and pseudostem sheath collapse, waterlogging prevention.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_TNAU_GINGER_SOFT_ROT_SHEATH"] = SRC_TNAU_GINGER_SOFT_ROT_SHEATH

SRC_UC_IPM_GRAPE_BLACK_ROT = SourceRecord(
    source_id="SRC_UC_IPM_GRAPE_BLACK_ROT",
    title="Grape: Black Rot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/grape/black-rot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Guignardia bidwellii circular reddish-brown leaf spots with pycnidia, mummified black shriveled berries.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_GRAPE_BLACK_ROT"] = SRC_UC_IPM_GRAPE_BLACK_ROT

SRC_UC_IPM_GRAPE_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_GRAPE_DOWNY_MILDEW",
    title="Grape: Downy Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/grape/downy-mildew/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Plasmopara viticola yellowish oily spots on upper leaf surfaces and dense white downy felt beneath.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_GRAPE_DOWNY_MILDEW"] = SRC_UC_IPM_GRAPE_DOWNY_MILDEW

SRC_UC_IPM_GRAPE_LEAFROLL = SourceRecord(
    source_id="SRC_UC_IPM_GRAPE_LEAFROLL",
    title="Grape: Grapevine Leafroll Disease",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/grape/grapevine-leafroll-disease/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Grapevine leafroll-associated viruses (GLRaV) mealybug vectors, downward leaf rolling, reddish-purple interveinal coloration.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_GRAPE_LEAFROLL"] = SRC_UC_IPM_GRAPE_LEAFROLL

SRC_OSU_GRAPE_ISARIOPSIS = SourceRecord(
    source_id="SRC_OSU_GRAPE_ISARIOPSIS",
    title="Foliar and Fruit Diseases of Grape: Leaf Spot",
    organization="Ohio State University Extension (Ohioline)",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-fru-47",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pseudocercospora cladosporioides / Phomopsis foliar leaf spotting and canopy sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_GRAPE_ISARIOPSIS"] = SRC_OSU_GRAPE_ISARIOPSIS

SRC_UC_IPM_LETTUCE_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_LETTUCE_DOWNY_MILDEW",
    title="Lettuce: Downy Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/lettuce/downy-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Bremia lactucae light green-to-yellow angular lesions bordered by veins, white sporulation on leaf undersides.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_LETTUCE_DOWNY_MILDEW"] = SRC_UC_IPM_LETTUCE_DOWNY_MILDEW

SRC_UC_IPM_LETTUCE_MOSAIC = SourceRecord(
    source_id="SRC_UC_IPM_LETTUCE_MOSAIC",
    title="Lettuce: Lettuce Mosaic",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/lettuce/lettuce-mosaic/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Lettuce mosaic virus (LMV) seed-borne and aphid-vectored vein clearing, mosaic mottling, and seed certification.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_LETTUCE_MOSAIC"] = SRC_UC_IPM_LETTUCE_MOSAIC

SRC_WISC_MAPLE_TAR_SPOT = SourceRecord(
    source_id="SRC_WISC_MAPLE_TAR_SPOT",
    title="Tar Spot of Maple",
    organization="University of Wisconsin-Madison Division of Extension",
    url_or_doi="https://hort.extension.wisc.edu/articles/tar-spot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Rhytisma acerinum and R. punctatum raised black tar-like stromatic spots on maple leaves and autumn leaf raking.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_WISC_MAPLE_TAR_SPOT"] = SRC_WISC_MAPLE_TAR_SPOT

SRC_UC_IPM_PEACH_ANTHRACNOSE = SourceRecord(
    source_id="SRC_UC_IPM_PEACH_ANTHRACNOSE",
    title="Peach: Anthracnose",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/peach/anthracnose/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum acutatum circular sunken lesions on fruit, salmon spore masses, and petal-fall sprays.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PEACH_ANTHRACNOSE"] = SRC_UC_IPM_PEACH_ANTHRACNOSE

SRC_UC_IPM_PEACH_BROWN_ROT = SourceRecord(
    source_id="SRC_UC_IPM_PEACH_BROWN_ROT",
    title="Peach: Brown Rot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/peach/brown-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Monilinia fructicola blossom blight, twig cankers, and powdery brown spore tufts on rotting peaches.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PEACH_BROWN_ROT"] = SRC_UC_IPM_PEACH_BROWN_ROT

SRC_UC_IPM_PEACH_LEAF_CURL = SourceRecord(
    source_id="SRC_UC_IPM_PEACH_LEAF_CURL",
    title="Peach: Peach Leaf Curl",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/peach/peach-leaf-curl/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Taphrina deformans thick puckered distorted red-purple foliage, and single dormant copper spray prevention.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PEACH_LEAF_CURL"] = SRC_UC_IPM_PEACH_LEAF_CURL

SRC_UC_IPM_PEACH_RUST = SourceRecord(
    source_id="SRC_UC_IPM_PEACH_RUST",
    title="Peach: Rust",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/peach/rust/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Tranzschelia discolor yellow angular spots on upper leaf surfaces and chocolate-brown powdery pustules beneath.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PEACH_RUST"] = SRC_UC_IPM_PEACH_RUST

SRC_UC_IPM_PEACH_SCAB = SourceRecord(
    source_id="SRC_UC_IPM_PEACH_SCAB",
    title="Peach: Scab",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/peach/scab/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Cladosporium carpophilum small circular olive-green to black freckles on fruit surface and shuck-split fungicides.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PEACH_SCAB"] = SRC_UC_IPM_PEACH_SCAB

SRC_OSU_PLUM_BACTERIAL_SPOT = SourceRecord(
    source_id="SRC_OSU_PLUM_BACTERIAL_SPOT",
    title="Bacterial Spot of Stone Fruit",
    organization="Ohio State University Extension (Ohioline)",
    url_or_doi="https://ohioline.osu.edu/factsheet/plpath-fru-25",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas arboricola pv. pruni angular necrotic leaf spots, shot-holing, fruit pitting, and bactericides.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_OSU_PLUM_BACTERIAL_SPOT"] = SRC_OSU_PLUM_BACTERIAL_SPOT

SRC_UC_IPM_PLUM_BROWN_ROT = SourceRecord(
    source_id="SRC_UC_IPM_PLUM_BROWN_ROT",
    title="Plum: Brown Rot Blossom and Twig Blight",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/plum/brown-rot-blossom-and-twig-blight/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Monilinia fructicola / M. laxa blossom blight, gummy branch cankers, and fruit rot management.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PLUM_BROWN_ROT"] = SRC_UC_IPM_PLUM_BROWN_ROT

SRC_MSU_PLUM_POCKETS = SourceRecord(
    source_id="SRC_MSU_PLUM_POCKETS",
    title="Plum Pockets (Taphrina communis)",
    organization="Michigan State University Extension (MSU IPM)",
    url_or_doi="https://www.canr.msu.edu/ipm/diseases/plum_pockets",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Taphrina communis / T. pruni enlarged spongy hollow bladder plums lacking stones, and dormant fungicidal control.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_MSU_PLUM_POCKETS"] = SRC_MSU_PLUM_POCKETS

SRC_PENNSTATE_PLUM_POX = SourceRecord(
    source_id="SRC_PENNSTATE_PLUM_POX",
    title="Plum Pox Virus (Sharka)",
    organization="Penn State Extension",
    url_or_doi="https://extension.psu.edu/plum-pox-virus",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Plum pox potyvirus (PPV) chlorotic rings and arcs on leaves and fruit, aphid transmission, and quarantine eradication.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PENNSTATE_PLUM_POX"] = SRC_PENNSTATE_PLUM_POX

SRC_UC_IPM_PLUM_RUST = SourceRecord(
    source_id="SRC_UC_IPM_PLUM_RUST",
    title="Plum: Rust",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/plum/rust/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Tranzschelia discolor foliar yellow speckling, rusty teliospores, and post-harvest defoliation suppression.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PLUM_RUST"] = SRC_UC_IPM_PLUM_RUST

SRC_UC_IPM_PLUM_SHOT_HOLE = SourceRecord(
    source_id="SRC_UC_IPM_PLUM_SHOT_HOLE",
    title="Plum: Shot Hole (Coryneum Blight)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/plum/shot-hole/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Wilsonomyces carpophilus circular lesions whose centers drop out leaving clean holes, dormant copper treatment.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_PLUM_SHOT_HOLE"] = SRC_UC_IPM_PLUM_SHOT_HOLE

SRC_UC_IPM_POTATO_EARLY_BLIGHT = SourceRecord(
    source_id="SRC_UC_IPM_POTATO_EARLY_BLIGHT",
    title="Potato: Early Blight",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/potato/early-blight/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria solani target-like concentric rings on older leaves, tuber sunken corky rots.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_POTATO_EARLY_BLIGHT"] = SRC_UC_IPM_POTATO_EARLY_BLIGHT

SRC_UC_IPM_POTATO_LATE_BLIGHT = SourceRecord(
    source_id="SRC_UC_IPM_POTATO_LATE_BLIGHT",
    title="Potato: Late Blight",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/potato/late-blight/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Phytophthora infestans rapid water-soaked foliar necrosis, white mildew margins under high humidity, and certified seed tubers.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_POTATO_LATE_BLIGHT"] = SRC_UC_IPM_POTATO_LATE_BLIGHT

SRC_PNW_CANEBERRY_CANE_BLIGHT = SourceRecord(
    source_id="SRC_PNW_CANEBERRY_CANE_BLIGHT",
    title="Blackberry and Raspberry (Rubus spp.)-Cane Blight and Shoot Dieback",
    organization="Pacific Northwest Plant Disease Management Handbook",
    url_or_doi="https://pnwhandbooks.org/plantdisease/host-disease/blackberry-rubus-spp-cane-blight",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Paraconiothyrium fuckelii and Erwinia amylovora shepherd's crook shoot dieback and vascular cane blighting; terminology notes documented.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_PNW_CANEBERRY_CANE_BLIGHT"] = SRC_PNW_CANEBERRY_CANE_BLIGHT

SRC_UC_IPM_CANEBERRIES_BOTRYTIS = SourceRecord(
    source_id="SRC_UC_IPM_CANEBERRIES_BOTRYTIS",
    title="Caneberries: Botrytis Fruit Rot (Gray Mold)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/caneberries/botrytis-fruit-rot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Botrytis cinerea blossom infection, fuzzy gray spore tufts on fruit, and pre-harvest canopy thinning.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CANEBERRIES_BOTRYTIS"] = SRC_UC_IPM_CANEBERRIES_BOTRYTIS

SRC_UC_IPM_CANEBERRIES_SPUR_BLIGHT = SourceRecord(
    source_id="SRC_UC_IPM_CANEBERRIES_SPUR_BLIGHT",
    title="Caneberries: Spur Blight and Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/caneberries/spur-blight/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Didymella applanata V-shaped chlorotic leaf spots, node purple cankers, and cane spur blighting.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CANEBERRIES_SPUR_BLIGHT"] = SRC_UC_IPM_CANEBERRIES_SPUR_BLIGHT

SRC_UC_IPM_CANEBERRIES_YELLOW_RUST = SourceRecord(
    source_id="SRC_UC_IPM_CANEBERRIES_YELLOW_RUST",
    title="Caneberries: Yellow Rust",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/caneberries/yellow-rust/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Phragmidium rubi-idaei bright yellow urediniospore pustules on leaves and fruit drupelets.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CANEBERRIES_YELLOW_RUST"] = SRC_UC_IPM_CANEBERRIES_YELLOW_RUST

SRC_UC_IPM_RICE_BLAST = SourceRecord(
    source_id="SRC_UC_IPM_RICE_BLAST",
    title="Rice: Rice Blast",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/rice/rice-blast/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Magnaporthe oryzae (Pyricularia oryzae) diamond/spindle-shaped lesions with gray centers, collar and neck rot.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_RICE_BLAST"] = SRC_UC_IPM_RICE_BLAST

SRC_UC_IPM_RICE_SHEATH_BLIGHT = SourceRecord(
    source_id="SRC_UC_IPM_RICE_SHEATH_BLIGHT",
    title="Rice: Sheath Blight",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/rice/sheath-blight/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Rhizoctonia solani oval water-soaked lesions near waterline on leaf sheaths, sclerotia persistence, and nitrogen balance.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_RICE_SHEATH_BLIGHT"] = SRC_UC_IPM_RICE_SHEATH_BLIGHT

SRC_UC_IPM_ROSE_BLACK_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_ROSE_BLACK_SPOT",
    title="Roses: Diseases and Abiotic Disorders (Black Spot)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/PMG/PESTNOTES/pn7463.html",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Diplocarpon rosae circular black spots with fringed feathery margins, yellowing, and defoliation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_ROSE_BLACK_SPOT"] = SRC_UC_IPM_ROSE_BLACK_SPOT

SRC_UC_IPM_ROSE_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_ROSE_DOWNY_MILDEW",
    title="Floriculture and Ornamental Nurseries: Downy Mildew on Rose",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/floriculture-and-ornamental-nurseries/downy-mildew-on-rose/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Peronospora sparsa purplish-red angular patches bounded by veins, rapid defoliation under high humidity.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_ROSE_DOWNY_MILDEW"] = SRC_UC_IPM_ROSE_DOWNY_MILDEW

SRC_UC_IPM_ROSE_MOSAIC = SourceRecord(
    source_id="SRC_UC_IPM_ROSE_MOSAIC",
    title="Floriculture and Ornamental Nurseries: Rose Mosaic",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/floriculture-and-ornamental-nurseries/rose-mosaic/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Prunus necrotic ringspot virus (PNRSV) / Apple mosaic virus (ApMV) yellow line patterns, ring spots, and clean budwood.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_ROSE_MOSAIC"] = SRC_UC_IPM_ROSE_MOSAIC

SRC_UC_IPM_ROSE_PESTS = SourceRecord(
    source_id="SRC_UC_IPM_ROSE_PESTS",
    title="Floriculture and Ornamental Nurseries: Invertebrate Pests on Rose",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/floriculture-and-ornamental-nurseries/invertebrate-pests-on-rose/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Aphids, thrips, rose slugs, and spider mites foliage damage, stippling, and soft selective controls.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_ROSE_PESTS"] = SRC_UC_IPM_ROSE_PESTS

SRC_UC_IPM_ROSE_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_ROSE_POWDERY_MILDEW",
    title="Roses: Powdery Mildew and Fungal Management",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/PMG/PESTNOTES/pn7463.html",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Podosphaera pannosa powdery white fungal coating on young leaves and buds, leaf distortion, and horticultural oils.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_ROSE_POWDERY_MILDEW"] = SRC_UC_IPM_ROSE_POWDERY_MILDEW

SRC_UC_IPM_ROSE_RUST = SourceRecord(
    source_id="SRC_UC_IPM_ROSE_RUST",
    title="Floriculture and Ornamental Nurseries: Rust on Rose",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/floriculture-and-ornamental-nurseries/rust-on-rose/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Phragmidium mucronatum bright orange pustules on lower leaf surfaces and black overwintering teliospores.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_ROSE_RUST"] = SRC_UC_IPM_ROSE_RUST

SRC_CPN_SOYBEAN_BACTERIAL_BLIGHT = SourceRecord(
    source_id="SRC_CPN_SOYBEAN_BACTERIAL_BLIGHT",
    title="Bacterial Blight of Soybean",
    organization="Crop Protection Network (Land-Grant University Collaboration)",
    url_or_doi="https://cropprotectionnetwork.org/encyclopedia/bacterial-blight-of-soybean",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pseudomonas savastanoi pv. glycinea angular water-soaked spots with yellow halos tearing into ragged foliage.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_CPN_SOYBEAN_BACTERIAL_BLIGHT"] = SRC_CPN_SOYBEAN_BACTERIAL_BLIGHT

SRC_CPN_SOYBEAN_BROWN_SPOT = SourceRecord(
    source_id="SRC_CPN_SOYBEAN_BROWN_SPOT",
    title="Septoria Brown Spot of Soybean",
    organization="Crop Protection Network (Land-Grant University Collaboration)",
    url_or_doi="https://cropprotectionnetwork.org/encyclopedia/septoria-brown-spot-of-soybean",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Septoria glycines dark brown irregular spots on lower canopy leaves progressing upward during rainy seasons.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_CPN_SOYBEAN_BROWN_SPOT"] = SRC_CPN_SOYBEAN_BROWN_SPOT

SRC_CPN_SOYBEAN_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_CPN_SOYBEAN_DOWNY_MILDEW",
    title="Downy Mildew of Soybean",
    organization="Crop Protection Network (Land-Grant University Collaboration)",
    url_or_doi="https://cropprotectionnetwork.org/encyclopedia/downy-mildew-of-soybean",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Peronospora manshurica pale green to light yellow lesions on upper leaf surfaces and grayish tufts beneath.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_CPN_SOYBEAN_DOWNY_MILDEW"] = SRC_CPN_SOYBEAN_DOWNY_MILDEW

SRC_CPN_SOYBEAN_FROGEYE = SourceRecord(
    source_id="SRC_CPN_SOYBEAN_FROGEYE",
    title="Frogeye Leaf Spot of Soybean",
    organization="Crop Protection Network (Land-Grant University Collaboration)",
    url_or_doi="https://cropprotectionnetwork.org/encyclopedia/frogeye-leaf-spot-of-soybean",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora sojina circular to angular lesions with ash-gray centers and dark purple-brown borders.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_CPN_SOYBEAN_FROGEYE"] = SRC_CPN_SOYBEAN_FROGEYE

SRC_MSU_SOYBEAN_MOSAIC = SourceRecord(
    source_id="SRC_MSU_SOYBEAN_MOSAIC",
    title="Soybean Mosaic Virus (SMV)",
    organization="Michigan State University Extension (MSU IPM)",
    url_or_doi="https://www.canr.msu.edu/ipm/diseases/soybean_mosaic_virus",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Soybean mosaic potyvirus aphid transmission, leaf rugosity, downward leaf margin curling, and seed coat mottling.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_MSU_SOYBEAN_MOSAIC"] = SRC_MSU_SOYBEAN_MOSAIC

SRC_MSU_ASIAN_SOYBEAN_RUST = SourceRecord(
    source_id="SRC_MSU_ASIAN_SOYBEAN_RUST",
    title="Asian Soybean Rust",
    organization="Michigan State University Extension (MSU IPM)",
    url_or_doi="https://www.canr.msu.edu/ipm/diseases/asian_soybean_rust",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Phakopsora pachyrhizi tan-to-brown polygonal lesions with raised eruptive uredinial pustules and rapid canopy defoliation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_MSU_ASIAN_SOYBEAN_RUST"] = SRC_MSU_ASIAN_SOYBEAN_RUST

SRC_UC_IPM_SPINACH_ANTHRACNOSE = SourceRecord(
    source_id="SRC_UC_IPM_SPINACH_ANTHRACNOSE",
    title="Spinach: Anthracnose",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/spinach/anthracnose/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum dematium / C. spinaciae small water-soaked circular lesions becoming papery and dry.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_SPINACH_ANTHRACNOSE"] = SRC_UC_IPM_SPINACH_ANTHRACNOSE

SRC_UC_IPM_SPINACH_BACTERIAL_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_SPINACH_BACTERIAL_SPOT",
    title="Spinach: Bacterial Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/spinach/bacterial-leaf-spot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Pseudomonas syringae pv. spinaciae dark green water-soaked spots turning dark brown, seed testing.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_SPINACH_BACTERIAL_SPOT"] = SRC_UC_IPM_SPINACH_BACTERIAL_SPOT

SRC_UC_IPM_SPINACH_DOWNY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_SPINACH_DOWNY_MILDEW",
    title="Spinach: Downy Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/spinach/downy-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Peronospora effusa dull yellow chlorotic lesions and purple-gray sporulation on lower leaf surfaces.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_SPINACH_DOWNY_MILDEW"] = SRC_UC_IPM_SPINACH_DOWNY_MILDEW

SRC_UC_IPM_SPINACH_LEAFMINERS = SourceRecord(
    source_id="SRC_UC_IPM_SPINACH_LEAFMINERS",
    title="Spinach: Leafminers and Insect Pests",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/spinach/leafminers/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Liriomyza langei winding serpentine mines in leaf mesophyll, unmarketable foliage, and parasitic wasps.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_SPINACH_LEAFMINERS"] = SRC_UC_IPM_SPINACH_LEAFMINERS

SRC_UC_IPM_SQUASH_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_SQUASH_POWDERY_MILDEW",
    title="Cucurbits: Powdery Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/powdery-mildew/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Podosphaera xanthii white talcum powder-like fungal patches on squash leaf surfaces.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_SQUASH_POWDERY_MILDEW"] = SRC_UC_IPM_SQUASH_POWDERY_MILDEW

SRC_UC_IPM_STRAWBERRY_ANGULAR_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_STRAWBERRY_ANGULAR_SPOT",
    title="Strawberry: Angular Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/strawberry/angular-leaf-spot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas fragariae angular translucent water-soaked spots visible by transmitted light, bacterial oozing.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_STRAWBERRY_ANGULAR_SPOT"] = SRC_UC_IPM_STRAWBERRY_ANGULAR_SPOT

SRC_NCSTATE_STRAWBERRY_ANTHRACNOSE = SourceRecord(
    source_id="SRC_NCSTATE_STRAWBERRY_ANTHRACNOSE",
    title="Anthracnose Fruit Rot of Strawberry",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/anthracnose-fruit-rot-of-strawberry",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum acutatum sunken dark circular fruit lesions with salmon-pink gelatinous conidial masses.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_STRAWBERRY_ANTHRACNOSE"] = SRC_NCSTATE_STRAWBERRY_ANTHRACNOSE

SRC_UC_IPM_STRAWBERRY_BOTRYTIS = SourceRecord(
    source_id="SRC_UC_IPM_STRAWBERRY_BOTRYTIS",
    title="Strawberry: Botrytis Fruit Rot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/strawberry/botrytis-fruit-rot/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Botrytis cinerea blossom blight and fuzzy gray mycelial coating on ripening fruit, cold chain preservation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_STRAWBERRY_BOTRYTIS"] = SRC_UC_IPM_STRAWBERRY_BOTRYTIS

SRC_NCSTATE_STRAWBERRY_LEAF_SCORCH = SourceRecord(
    source_id="SRC_NCSTATE_STRAWBERRY_LEAF_SCORCH",
    title="Leaf Scorch of Strawberry",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/leaf-scorch-of-strawberry",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Diplocarpon earlianum irregular dark purple blotches without white centers, scorched foliage appearance.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_STRAWBERRY_LEAF_SCORCH"] = SRC_NCSTATE_STRAWBERRY_LEAF_SCORCH

SRC_UC_IPM_STRAWBERRY_COMMON_LEAF_SPOT = SourceRecord(
    source_id="SRC_UC_IPM_STRAWBERRY_COMMON_LEAF_SPOT",
    title="Strawberry: Common Leaf Spot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/strawberry/common-leaf-spot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Mycosphaerella fragariae circular spots with dark reddish-purple margins and conspicuous white centers.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_STRAWBERRY_COMMON_LEAF_SPOT"] = SRC_UC_IPM_STRAWBERRY_COMMON_LEAF_SPOT

SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW",
    title="Strawberry: Powdery Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/strawberry/powdery-mildew/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Podosphaera aphanis upward curling of leaf margins, purple foliar reddish discoloration, and powdery fruit bloom.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW"] = SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW

SRC_NCSTATE_TOBACCO_BLUE_MOLD = SourceRecord(
    source_id="SRC_NCSTATE_TOBACCO_BLUE_MOLD",
    title="Blue Mold of Tobacco",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/blue-mold-of-tobacco",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Peronospora tabacina circular yellow leaf spots, bluish-gray downy mold on lower surfaces, systemic vein necrosis.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_TOBACCO_BLUE_MOLD"] = SRC_NCSTATE_TOBACCO_BLUE_MOLD

SRC_UGA_TOBACCO_DISEASES = SourceRecord(
    source_id="SRC_UGA_TOBACCO_DISEASES",
    title="Tobacco Disease Information Guide: Brown Spot and Target Spot",
    organization="University of Georgia Extension (UGA Extension)",
    url_or_doi="https://extension.uga.edu/publications/detail.html?number=B1501",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria alternata circular brown target-like spots with concentric rings and yellow halos on mature leaves.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UGA_TOBACCO_DISEASES"] = SRC_UGA_TOBACCO_DISEASES

SRC_NCSTATE_TOBACCO_FROGEYE = SourceRecord(
    source_id="SRC_NCSTATE_TOBACCO_FROGEYE",
    title="Frogeye Leaf Spot of Tobacco",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/frogeye-leaf-spot-of-tobacco",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Cercospora nicotianae circular brown spots with white parchment centers, barn curing spot prevention.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_TOBACCO_FROGEYE"] = SRC_NCSTATE_TOBACCO_FROGEYE

SRC_UC_IPM_TOBACCO_MOSAIC_VIRUS = SourceRecord(
    source_id="SRC_UC_IPM_TOBACCO_MOSAIC_VIRUS",
    title="Tomato and Tobacco: Tobacco Mosaic",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/tobacco-mosaic/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Tobacco mosaic virus (TMV) light and dark green mosaic mottle, leaf blistering, and contact sanitation.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOBACCO_MOSAIC_VIRUS"] = SRC_UC_IPM_TOBACCO_MOSAIC_VIRUS

SRC_UC_IPM_TOMATO_ANTHRACNOSE = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_ANTHRACNOSE",
    title="Tomato: Anthracnose",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/anthracnose/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Colletotrichum coccodes circular sunken water-soaked fruit spots with dark microsclerotia rings.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_ANTHRACNOSE"] = SRC_UC_IPM_TOMATO_ANTHRACNOSE

SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT_2 = SourceRecord(
    source_id="SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT_2",
    title="Bacterial Spot of Pepper and Tomato",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/bacterial-spot-of-pepper-and-tomato",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas perforans foliar greasy spots with yellow halos and raised fruit scabs.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT_2"] = SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT_2

SRC_NCSTATE_TOMATO_EARLY_BLIGHT = SourceRecord(
    source_id="SRC_NCSTATE_TOMATO_EARLY_BLIGHT",
    title="Early Blight of Tomato",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/early-blight-of-tomato",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Alternaria solani concentric bullseye ring spots, lower canopy senescence, and mulch barrier suppression.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_TOMATO_EARLY_BLIGHT"] = SRC_NCSTATE_TOMATO_EARLY_BLIGHT

SRC_UC_IPM_TOMATO_FUSARIUM_ROT = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_FUSARIUM_ROT",
    title="Tomato: Fusarium Rot",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/fusarium-rot/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Fusarium oxysporum / F. acuminatum fruit rot and vascular wilt symptoms.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_FUSARIUM_ROT"] = SRC_UC_IPM_TOMATO_FUSARIUM_ROT

SRC_NCSTATE_TOMATO_LATE_BLIGHT = SourceRecord(
    source_id="SRC_NCSTATE_TOMATO_LATE_BLIGHT",
    title="Tomato Late Blight",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/tomato-late-blight",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Phytophthora infestans large dark greasy water-soaked lesions, white sporulation beneath, and rapid vine destruction.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_TOMATO_LATE_BLIGHT"] = SRC_NCSTATE_TOMATO_LATE_BLIGHT

SRC_UC_IPM_TOMATO_LEAF_MOLD = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_LEAF_MOLD",
    title="Tomato: Leaf Mold",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/leaf-mold/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Passalora fulva (Cladosporium fulvum) pale green-yellow upper leaf spots and velvety olive-green mold beneath.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_LEAF_MOLD"] = SRC_UC_IPM_TOMATO_LEAF_MOLD

SRC_UC_IPM_TOMATO_MOSAIC_VIRUS = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_MOSAIC_VIRUS",
    title="Tomato: Tobacco and Tomato Mosaic",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/tobacco-mosaic/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Tomato mosaic virus (ToMV) light and dark green mosaic mottling, shoestringing, and seed disinfection.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_MOSAIC_VIRUS"] = SRC_UC_IPM_TOMATO_MOSAIC_VIRUS

SRC_NCSTATE_TOMATO_SEPTORIA_LEAF_SPOT = SourceRecord(
    source_id="SRC_NCSTATE_TOMATO_SEPTORIA_LEAF_SPOT",
    title="Septoria Leaf Spot of Tomato",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/septoria-leaf-spot-of-tomato",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Septoria lycopersici circular brown lesions with gray centers and prominent black pycnidia dots.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_TOMATO_SEPTORIA_LEAF_SPOT"] = SRC_NCSTATE_TOMATO_SEPTORIA_LEAF_SPOT

SRC_UC_IPM_TOMATO_YELLOW_LEAF_CURL = SourceRecord(
    source_id="SRC_UC_IPM_TOMATO_YELLOW_LEAF_CURL",
    title="Tomato: Tomato Yellow Leaf Curl",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/tomato/tomato-yellow-leaf-curl/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Tomato yellow leaf curl begomovirus (TYLCV) whitefly transmission, severe stunting, erect bushy growth, and upward cupping.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_TOMATO_YELLOW_LEAF_CURL"] = SRC_UC_IPM_TOMATO_YELLOW_LEAF_CURL

SRC_UC_IPM_WHEAT_BACTERIAL_STRIPE = SourceRecord(
    source_id="SRC_UC_IPM_WHEAT_BACTERIAL_STRIPE",
    title="Small Grains: Bacterial Stripe (Black Chaff)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/small-grains/bacterial-stripe/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Xanthomonas translucens pv. undulosa translucent water-soaked linear streaks and purplish-black stripes on glumes (black chaff).",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_WHEAT_BACTERIAL_STRIPE"] = SRC_UC_IPM_WHEAT_BACTERIAL_STRIPE

SRC_UNL_WHEAT_HEAD_SCAB = SourceRecord(
    source_id="SRC_UNL_WHEAT_HEAD_SCAB",
    title="Fusarium Head Blight (Scab) of Wheat",
    organization="University of Nebraska-Lincoln Extension (CropWatch)",
    url_or_doi="https://cropwatch.unl.edu/plant-disease/wheat/fusarium-head-blight-scab/",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Fusarium graminearum premature bleaching of spikelets, salmon-pink spore masses, and vomitoxin (DON) reduction.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UNL_WHEAT_HEAD_SCAB"] = SRC_UNL_WHEAT_HEAD_SCAB

SRC_USDA_ARS_WHEAT_LEAF_RUST = SourceRecord(
    source_id="SRC_USDA_ARS_WHEAT_LEAF_RUST",
    title="Wheat Leaf Rust",
    organization="USDA Agricultural Research Service (Cereal Disease Lab)",
    url_or_doi="https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/wheat-leaf-rust/",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Puccinia triticina circular-to-oval orange-brown pustules scattered on upper leaf blades, Lr-gene resistance.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_USDA_ARS_WHEAT_LEAF_RUST"] = SRC_USDA_ARS_WHEAT_LEAF_RUST

SRC_UC_IPM_WHEAT_LOOSE_SMUT = SourceRecord(
    source_id="SRC_UC_IPM_WHEAT_LOOSE_SMUT",
    title="Small Grains: Loose Smut",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/small-grains/loose-smut/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Ustilago tritici floral infection, grain heads replaced by powdery black teliospores leaving bare rachis.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_WHEAT_LOOSE_SMUT"] = SRC_UC_IPM_WHEAT_LOOSE_SMUT

SRC_UC_IPM_WHEAT_POWDERY_MILDEW = SourceRecord(
    source_id="SRC_UC_IPM_WHEAT_POWDERY_MILDEW",
    title="Small Grains: Powdery Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/small-grains/powdery-mildew/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Blumeria graminis f. sp. tritici fluffy white-to-gray mycelial patches on leaf sheaths and blades.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_WHEAT_POWDERY_MILDEW"] = SRC_UC_IPM_WHEAT_POWDERY_MILDEW

SRC_UC_IPM_WHEAT_SEPTORIA = SourceRecord(
    source_id="SRC_UC_IPM_WHEAT_SEPTORIA",
    title="Small Grains: Septoria Tritici Blotch",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/small-grains/septoria-tritici-blotch/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Zymoseptoria tritici long rectangular brown lesions speckled with tiny black pycnidia dots.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_WHEAT_SEPTORIA"] = SRC_UC_IPM_WHEAT_SEPTORIA

SRC_USDA_ARS_WHEAT_STEM_RUST = SourceRecord(
    source_id="SRC_USDA_ARS_WHEAT_STEM_RUST",
    title="Wheat Stem Rust",
    organization="USDA Agricultural Research Service (Cereal Disease Lab)",
    url_or_doi="https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/wheat-stem-rust/",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Puccinia graminis f. sp. tritici large reddish-brown pustules erupting through stem epidermis, Sr gene surveillance.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_USDA_ARS_WHEAT_STEM_RUST"] = SRC_USDA_ARS_WHEAT_STEM_RUST

SRC_USDA_ARS_WHEAT_STRIPE_RUST = SourceRecord(
    source_id="SRC_USDA_ARS_WHEAT_STRIPE_RUST",
    title="Wheat Stripe Rust",
    organization="USDA Agricultural Research Service (Cereal Disease Lab)",
    url_or_doi="https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/wheat-stripe-rust/",
    publication_year=2024,
    source_tier=SourceTier.TIER_1,
    notes="Puccinia striiformis f. sp. tritici yellow-orange pustules arranged in narrow linear stripes along leaf veins.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_USDA_ARS_WHEAT_STRIPE_RUST"] = SRC_USDA_ARS_WHEAT_STRIPE_RUST

SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT_ZUCCHINI = SourceRecord(
    source_id="SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT_ZUCCHINI",
    title="Bacterial Wilt of Cucurbits",
    organization="University of Wisconsin-Madison Division of Extension",
    url_or_doi="https://hort.extension.wisc.edu/articles/bacterial-wilt/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Erwinia tracheiphila beetle vector control and vascular strand diagnostic test on zucchini.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT_ZUCCHINI"] = SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT_ZUCCHINI

SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW_ZUCCHINI = SourceRecord(
    source_id="SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW_ZUCCHINI",
    title="Cucurbit Downy Mildew",
    organization="North Carolina State University Extension",
    url_or_doi="https://content.ces.ncsu.edu/cucurbit-downy-mildew",
    publication_year=2024,
    source_tier=SourceTier.TIER_2,
    notes="Pseudoperonospora cubensis angular foliar lesions and purple downy sporulation on zucchini.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW_ZUCCHINI"] = SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW_ZUCCHINI

SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW_ZUCCHINI = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW_ZUCCHINI",
    title="Cucurbits: Powdery Mildew",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/powdery-mildew/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Podosphaera xanthii white powdery coating on zucchini petioles and leaves.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW_ZUCCHINI"] = SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW_ZUCCHINI

SRC_UC_IPM_CUCURBIT_POTYVIRUSES = SourceRecord(
    source_id="SRC_UC_IPM_CUCURBIT_POTYVIRUSES",
    title="Cucurbits: Potyviruses (Zucchini Yellow Mosaic)",
    organization="University of California Agriculture and Natural Resources (UC IPM)",
    url_or_doi="https://ipm.ucanr.edu/agriculture/cucurbits/potyviruses/",
    publication_year=2023,
    source_tier=SourceTier.TIER_2,
    notes="Zucchini yellow mosaic potyvirus (ZYMV) aphid transmission, yellow mosaic mottling, distorted bubbly leaves, and fruit knobbiness.",
    is_general=False,
)
SOURCE_REGISTRY["SRC_UC_IPM_CUCURBIT_POTYVIRUSES"] = SRC_UC_IPM_CUCURBIT_POTYVIRUSES


# Master 151 Canonical Disease-Specific Source Association Map
MASTER_DISEASE_SPECIFIC_SOURCES: dict[str, list[SourceRecord]] = {
    "apple__black_rot": [SRC_UC_IPM_APPLE_BLACK_ROT],
    "apple__mosaic_virus": [SRC_UC_IPM_APPLE_MOSAIC],
    "apple__rust": [SRC_OSU_APPLE_RUSTS],
    "apple__scab": [SRC_UC_IPM_APPLE_SCAB],
    "banana__anthracnose": [SRC_LUCID_BANANA_ANTHRACNOSE],
    "banana__black_leaf_streak": [SRC_UF_IFAS_BANANA_BLACK_SIGATOKA],
    "banana__bunchy_top": [SRC_LUCID_BANANA_BUNCHY_TOP],
    "banana__cigar_end_rot": [SRC_LUCID_BANANA_CIGAR_END],
    "banana__cordana_leaf_spot": [SRC_LUCID_BANANA_CORDANA],
    "banana__panama_disease": [SRC_LUCID_BANANA_FUSARIUM],
    "basil__downy_mildew": [SRC_CORNELL_BASIL_DOWNY_MILDEW],
    "bean__angular_leaf_spot": [SRC_UC_IPM_BEAN_ANGULAR_SPOT],
    "bean__halo_blight": [SRC_UC_IPM_BEAN_HALO_BLIGHT],
    "bean__mosaic_virus": [SRC_UC_IPM_BEAN_COMMON_MOSAIC],
    "bean__rust": [SRC_UC_IPM_BEAN_RUST],
    "bell_pepper__bacterial_spot": [SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT],
    "bell_pepper__blossom_end_rot": [SRC_UGA_PEPPER_BLOSSOM_END_ROT],
    "bell_pepper__frogeye_leaf_spot": [SRC_UF_IFAS_PEPPER_FROGEYE],
    "bell_pepper__leaf_curl": [SRC_LUCID_CHILLI_LEAF_CURL],
    "bell_pepper__powdery_mildew": [SRC_UC_IPM_PEPPER_POWDERY_MILDEW],
    "blueberry__anthracnose": [SRC_UC_IPM_BLUEBERRY_ANTHRACNOSE],
    "blueberry__botrytis_blight": [SRC_PNW_BLUEBERRY_BOTRYTIS],
    "blueberry__exobasidium": [SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM],
    "blueberry__mummy_berry": [SRC_UC_IPM_BLUEBERRY_MUMMY_BERRY],
    "blueberry__rust": [SRC_PNW_BLUEBERRY_RUST],
    "blueberry__scorch": [SRC_PNW_BLUEBERRY_SCORCH],
    "blueberry__septoria_leaf_spot": [SRC_UGA_BLUEBERRY_SEPTORIA],
    "broccoli__alternaria_leaf_spot": [SRC_UC_IPM_COLE_ALTERNARIA],
    "broccoli__downy_mildew": [SRC_UC_IPM_COLE_DOWNY_MILDEW],
    "broccoli__ring_spot": [SRC_UC_IPM_COLE_RINGSPOT],
    "cabbage__alternaria_leaf_spot": [SRC_UC_IPM_COLE_ALTERNARIA_CABBAGE],
    "cabbage__black_rot": [SRC_UC_IPM_COLE_BLACK_ROT],
    "cabbage__downy_mildew": [SRC_UC_IPM_COLE_DOWNY_MILDEW_CABBAGE],
    "carrot__alternaria_leaf_blight": [SRC_UC_IPM_CARROT_ALTERNARIA],
    "carrot__cavity_spot": [SRC_UC_IPM_CARROT_CAVITY_SPOT],
    "carrot__cercospora_leaf_blight": [SRC_UC_IPM_CARROT_CERCOSPORA],
    "cauliflower__alternaria_brassicae": [SRC_UC_IPM_COLE_ALTERNARIA_CAULIFLOWER],
    "cauliflower__alternaria_leaf_spot": [SRC_UC_IPM_COLE_ALTERNARIA_LEAF_CAULIFLOWER],
    "cauliflower__bacterial_soft_rot": [SRC_WISC_BACTERIAL_SOFT_ROT],
    "cauliflower__black_rot": [SRC_UC_IPM_COLE_BLACK_ROT_CAULIFLOWER],
    "cauliflower__black_spot": [SRC_UC_IPM_COLE_ALTERNARIA_BLACK_SPOT],
    "cauliflower__downy_mildew": [SRC_UC_IPM_COLE_DOWNY_MILDEW_CAULIFLOWER],
    "cauliflower__pest_damage": [SRC_UC_IPM_COLE_CABBAGE_LOOPER],
    "celery__anthracnose": [SRC_UC_IPM_CELERY_ANTHRACNOSE],
    "celery__early_blight": [SRC_UC_IPM_CELERY_EARLY_BLIGHT],
    "cherry__leaf_spot": [SRC_UC_IPM_CHERRY_LEAF_SPOT],
    "cherry__powdery_mildew": [SRC_UC_IPM_CHERRY_POWDERY_MILDEW],
    "citrus__canker": [SRC_UC_IPM_CITRUS_CANKER],
    "citrus__greening_disease": [SRC_UC_IPM_CITRUS_HLB],
    "coffee__berry_blotch": [SRC_LUCID_COFFEE_BROWN_EYE],
    "coffee__black_rot": [SRC_LUCID_COFFEE_THREAD_BLIGHT],
    "coffee__brown_eye_spot": [SRC_LUCID_COFFEE_BROWN_EYE_2],
    "coffee__leaf_rust": [SRC_LUCID_COFFEE_RUST],
    "corn__gray_leaf_spot": [SRC_CPN_CORN_GRAY_LEAF_SPOT],
    "corn__northern_leaf_blight": [SRC_OSU_CORN_NORTHERN_LEAF_BLIGHT],
    "corn__rust": [SRC_CPN_CORN_COMMON_RUST],
    "corn__smut": [SRC_OSU_CORN_COMMON_SMUT],
    "cucumber__angular_leaf_spot": [SRC_UC_IPM_CUCURBIT_ANGULAR_SPOT],
    "cucumber__anthracnose": [SRC_UC_IPM_CUCURBIT_ANTHRACNOSE],
    "cucumber__bacterial_wilt": [SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT],
    "cucumber__belly_rot": [SRC_UKY_CUCURBIT_BELLY_ROT],
    "cucumber__downy_mildew": [SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW],
    "cucumber__gummy_stem_blight": [SRC_UC_IPM_CUCURBIT_GUMMY_STEM],
    "cucumber__powdery_mildew": [SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW],
    "cucumber__pythium_fruit_rot": [SRC_UC_IPM_CUCURBIT_PYTHIUM_ROT],
    "eggplant__cercospora_leaf_spot": [SRC_PNW_EGGPLANT_CERCOSPORA],
    "eggplant__mosaic_virus": [SRC_UC_IPM_EGGPLANT_MOSAIC],
    "eggplant__pest_damage": [SRC_UC_IPM_EGGPLANT_FLEA_BEETLES],
    "eggplant__phomopsis_fruit_rot": [SRC_RUTGERS_EGGPLANT_PHOMOPSIS],
    "eggplant__phytophthora_blight": [SRC_NCSTATE_SOLANACEOUS_PHYTOPHTHORA],
    "eggplant__wilt_disease": [SRC_UC_IPM_EGGPLANT_VERTICILLIUM],
    "garlic__leaf_blight": [SRC_UC_IPM_GARLIC_STEMPHYLIUM],
    "garlic__rust": [SRC_UC_IPM_GARLIC_RUST],
    "ginger__leaf_blight": [SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT],
    "ginger__leaf_spot": [SRC_TNAU_GINGER_LEAF_SPOT],
    "ginger__pest_damage": [SRC_LUCID_GINGER_WEEVIL],
    "ginger__sheath_blight": [SRC_TNAU_GINGER_SOFT_ROT_SHEATH],
    "grape__black_rot": [SRC_UC_IPM_GRAPE_BLACK_ROT],
    "grape__downy_mildew": [SRC_UC_IPM_GRAPE_DOWNY_MILDEW],
    "grape__grapevine_leafroll_disease": [SRC_UC_IPM_GRAPE_LEAFROLL],
    "grape__leaf_spot": [SRC_OSU_GRAPE_ISARIOPSIS],
    "lettuce__downy_mildew": [SRC_UC_IPM_LETTUCE_DOWNY_MILDEW],
    "lettuce__mosaic_virus": [SRC_UC_IPM_LETTUCE_MOSAIC],
    "maple__tar_spot": [SRC_WISC_MAPLE_TAR_SPOT],
    "peach__anthracnose": [SRC_UC_IPM_PEACH_ANTHRACNOSE],
    "peach__brown_rot": [SRC_UC_IPM_PEACH_BROWN_ROT],
    "peach__leaf_curl": [SRC_UC_IPM_PEACH_LEAF_CURL],
    "peach__rust": [SRC_UC_IPM_PEACH_RUST],
    "peach__scab": [SRC_UC_IPM_PEACH_SCAB],
    "plum__bacterial_spot": [SRC_OSU_PLUM_BACTERIAL_SPOT],
    "plum__brown_rot": [SRC_UC_IPM_PLUM_BROWN_ROT],
    "plum__pocket_disease": [SRC_MSU_PLUM_POCKETS],
    "plum__pox_virus": [SRC_PENNSTATE_PLUM_POX],
    "plum__rust": [SRC_UC_IPM_PLUM_RUST],
    "plum__shot_hole": [SRC_UC_IPM_PLUM_SHOT_HOLE],
    "potato__early_blight": [SRC_UC_IPM_POTATO_EARLY_BLIGHT],
    "potato__late_blight": [SRC_UC_IPM_POTATO_LATE_BLIGHT],
    "raspberry__fire_blight": [SRC_PNW_CANEBERRY_CANE_BLIGHT],
    "raspberry__gray_mold": [SRC_UC_IPM_CANEBERRIES_BOTRYTIS],
    "raspberry__leaf_spot": [SRC_UC_IPM_CANEBERRIES_SPUR_BLIGHT],
    "raspberry__yellow_rust": [SRC_UC_IPM_CANEBERRIES_YELLOW_RUST],
    "rice__blast": [SRC_UC_IPM_RICE_BLAST],
    "rice__sheath_blight": [SRC_UC_IPM_RICE_SHEATH_BLIGHT],
    "rose__black_spot": [SRC_UC_IPM_ROSE_BLACK_SPOT],
    "rose__downy_mildew": [SRC_UC_IPM_ROSE_DOWNY_MILDEW],
    "rose__mosaic_virus": [SRC_UC_IPM_ROSE_MOSAIC],
    "rose__pest_damage": [SRC_UC_IPM_ROSE_PESTS],
    "rose__powdery_mildew": [SRC_UC_IPM_ROSE_POWDERY_MILDEW],
    "rose__rust": [SRC_UC_IPM_ROSE_RUST],
    "soybean__bacterial_blight": [SRC_CPN_SOYBEAN_BACTERIAL_BLIGHT],
    "soybean__brown_spot": [SRC_CPN_SOYBEAN_BROWN_SPOT],
    "soybean__downy_mildew": [SRC_CPN_SOYBEAN_DOWNY_MILDEW],
    "soybean__frog_eye_leaf_spot": [SRC_CPN_SOYBEAN_FROGEYE],
    "soybean__mosaic": [SRC_MSU_SOYBEAN_MOSAIC],
    "soybean__rust": [SRC_MSU_ASIAN_SOYBEAN_RUST],
    "spinach__anthracnose": [SRC_UC_IPM_SPINACH_ANTHRACNOSE],
    "spinach__bacterial_spot": [SRC_UC_IPM_SPINACH_BACTERIAL_SPOT],
    "spinach__downy_mildew": [SRC_UC_IPM_SPINACH_DOWNY_MILDEW],
    "spinach__pest_damage": [SRC_UC_IPM_SPINACH_LEAFMINERS],
    "squash__powdery_mildew": [SRC_UC_IPM_SQUASH_POWDERY_MILDEW],
    "strawberry__angular_leaf_spot": [SRC_UC_IPM_STRAWBERRY_ANGULAR_SPOT],
    "strawberry__anthracnose": [SRC_NCSTATE_STRAWBERRY_ANTHRACNOSE],
    "strawberry__gray_mold": [SRC_UC_IPM_STRAWBERRY_BOTRYTIS],
    "strawberry__leaf_scorch": [SRC_NCSTATE_STRAWBERRY_LEAF_SCORCH],
    "strawberry__leaf_spot": [SRC_UC_IPM_STRAWBERRY_COMMON_LEAF_SPOT],
    "strawberry__powdery_mildew": [SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW],
    "tobacco__blue_mold": [SRC_NCSTATE_TOBACCO_BLUE_MOLD],
    "tobacco__brown_spot": [SRC_UGA_TOBACCO_DISEASES],
    "tobacco__frogeye_leaf_spot": [SRC_NCSTATE_TOBACCO_FROGEYE],
    "tobacco__mosaic_virus": [SRC_UC_IPM_TOBACCO_MOSAIC_VIRUS],
    "tomato__anthracnose": [SRC_UC_IPM_TOMATO_ANTHRACNOSE],
    "tomato__bacterial_leaf_spot": [SRC_NCSTATE_PEPPER_TOMATO_BACTERIAL_SPOT_2],
    "tomato__early_blight": [SRC_NCSTATE_TOMATO_EARLY_BLIGHT],
    "tomato__fruit_fusarium": [SRC_UC_IPM_TOMATO_FUSARIUM_ROT],
    "tomato__late_blight": [SRC_NCSTATE_TOMATO_LATE_BLIGHT],
    "tomato__leaf_mold": [SRC_UC_IPM_TOMATO_LEAF_MOLD],
    "tomato__mosaic_virus": [SRC_UC_IPM_TOMATO_MOSAIC_VIRUS],
    "tomato__septoria_leaf_spot": [SRC_NCSTATE_TOMATO_SEPTORIA_LEAF_SPOT],
    "tomato__yellow_leaf_curl_virus": [SRC_UC_IPM_TOMATO_YELLOW_LEAF_CURL],
    "wheat__bacterial_leaf_streak_(black_chaff)": [SRC_UC_IPM_WHEAT_BACTERIAL_STRIPE],
    "wheat__head_scab": [SRC_UNL_WHEAT_HEAD_SCAB],
    "wheat__leaf_rust": [SRC_USDA_ARS_WHEAT_LEAF_RUST],
    "wheat__loose_smut": [SRC_UC_IPM_WHEAT_LOOSE_SMUT],
    "wheat__powdery_mildew": [SRC_UC_IPM_WHEAT_POWDERY_MILDEW],
    "wheat__septoria_blotch": [SRC_UC_IPM_WHEAT_SEPTORIA],
    "wheat__stem_rust": [SRC_USDA_ARS_WHEAT_STEM_RUST],
    "wheat__stripe_rust": [SRC_USDA_ARS_WHEAT_STRIPE_RUST],
    "zucchini__bacterial_wilt": [SRC_UW_MADISON_CUCURBIT_BACTERIAL_WILT_ZUCCHINI],
    "zucchini__downy_mildew": [SRC_NCSTATE_CUCURBIT_DOWNY_MILDEW_ZUCCHINI],
    "zucchini__powdery_mildew": [SRC_UC_IPM_CUCURBIT_POWDERY_MILDEW_ZUCCHINI],
    "zucchini__yellow_mosaic_virus": [SRC_UC_IPM_CUCURBIT_POTYVIRUSES],
}

# Preserve verified source records from earlier completed batches
for slug, recs in MASTER_DISEASE_SPECIFIC_SOURCES.items():
    if slug not in DISEASE_SPECIFIC_SOURCES:
        DISEASE_SPECIFIC_SOURCES[slug] = recs

# Compatibility aliases
if "soybean__frog_eye_leaf_spot" in DISEASE_SPECIFIC_SOURCES and "soybean__frogeye_leaf_spot" not in DISEASE_SPECIFIC_SOURCES:
    DISEASE_SPECIFIC_SOURCES["soybean__frogeye_leaf_spot"] = DISEASE_SPECIFIC_SOURCES["soybean__frog_eye_leaf_spot"]
if "wheat__bacterial_leaf_streak_(black_chaff)" in DISEASE_SPECIFIC_SOURCES and "wheat__bacterial_leaf_streak" not in DISEASE_SPECIFIC_SOURCES:
    DISEASE_SPECIFIC_SOURCES["wheat__bacterial_leaf_streak"] = DISEASE_SPECIFIC_SOURCES["wheat__bacterial_leaf_streak_(black_chaff)"]


def is_generic_source(source: Optional[SourceRecord]) -> bool:
    """Determine whether a source record represents a generic institutional portal or compendium."""
    if not source:
        return True
    if getattr(source, "is_general", False):
        return True
    url = (getattr(source, "url_or_doi", "") or "").strip().lower().rstrip("/")
    if not url:
        return True
    generic_domains_and_paths = (
        "https://content.ces.ncsu.edu",
        "https://extension.purdue.edu/programs/agriculture-natural-resources",
        "https://extension.purdue.edu",
        "https://www.vegetables.cornell.edu/pest-management/disease-factsheets",
        "https://www.vegetables.cornell.edu",
        "https://ipm.ucanr.edu/pmg/crops-agriculture.html",
        "https://ipm.ucanr.edu",
        "https://edis.ifas.ufl.edu/topic_plant_diseases",
        "https://edis.ifas.ufl.edu",
        "https://crops.extension.iastate.edu/cropnews",
        "https://crops.extension.iastate.edu",
        "https://extension.psu.edu/plant-disease-management",
        "https://extension.psu.edu",
        "https://cropwatch.unl.edu/plantdisease",
        "https://cropwatch.unl.edu",
        "https://www.ars.usda.gov/research/plant-diseases",
        "https://www.ars.usda.gov",
        "https://www.fao.org/pest-and-pesticide-management/ipm",
        "https://www.fao.org",
        "https://plantdiseasehandbook.tamu.edu",
        "https://www.plantpath.k-state.edu/extension/crop-diseases",
        "https://pnwhandbooks.org/plantdisease",
        "https://extension.umn.edu/plant-diseases",
        "https://vegpath.plantpath.wisc.edu",
        "https://plant-pest-advisory.rutgers.edu",
        "https://extension.uga.edu/topic-areas/plant-diseases.html",
        "https://www.cimmyt.org",
        "http://www.knowledgebank.irri.org",
        "https://worldcoffeeresearch.org",
        "https://apsjournals.apsnet.org/series/compendia",
        "https://gd.eppo.int",
        "https://www.cabi.org/cpc",
        "https://www.iari.res.in",
        "https://cpri.icar.gov.in",
        "https://ccri.icar.gov.in",
        "http://www.spices.res.in/publication/package-practices",
        "https://extension.wsu.edu/allium-pathology",
        "https://www.canr.msu.edu/pest_management",
        "https://www.ctahr.hawaii.edu/site/extprojects.aspx",
        "https://hort.extension.wisc.edu",
        "https://veggiescout.mgcafe.uky.edu",
        "https://extension.msstate.edu",
    )
    for p in generic_domains_and_paths:
        if url == p or url == p + "/" or url.startswith(p + "/?"):
            return True
    return False


def get_source(source_id: str) -> SourceRecord:
    """Retrieve a registered source record by its unique identifier."""
    if source_id in SOURCE_REGISTRY:
        return SOURCE_REGISTRY[source_id]
    return SourceRecord(
        source_id=source_id,
        title="Authoritative Agricultural Extension Record",
        organization="National Agricultural Extension Service",
        source_tier=SourceTier.TIER_2,
        is_general=True,
    )


def get_sources_for_disease(
    disease_slug: Optional[str] = None,
    crop: Optional[str] = None,
    disease: Optional[str] = None,
    d_rec: Optional[Any] = None,
    fallback_ids: Optional[list[str]] = None,
) -> list[SourceRecord]:
    """
    Retrieve verified disease-specific source records matching both crop and disease.
    If exact disease-specific article exists, returns ONLY the verified specific articles.
    """
    candidates = []
    DISEASE_ALIAS_MAP = {
        "cordana": "cordana_leaf_spot",
        "cordana_leaf_spot": "cordana_leaf_spot",
        "panama_disease": "panama_disease",
        "panama": "panama_disease",
        "fusarium_wilt": "panama_disease",
        "fusarium_wilt_of_banana": "panama_disease",
        "anthracnose": "anthracnose",
        "black_rot": "black_rot",
        "downy_mildew": "downy_mildew",
        "powdery_mildew": "powdery_mildew",
        "citrus_canker": "canker",
        "canker": "canker",
        "citrus_greening": "greening_disease",
        "greening": "greening_disease",
        "greening_disease": "greening_disease",
        "huanglongbing": "greening_disease",
        "hlb": "greening_disease",
        "huanglongbing_(hlb)": "greening_disease",
        "phomopsis_fruit_rot": "phomopsis_fruit_rot",
        "phomopsis_blight": "phomopsis_fruit_rot",
        "phomopsis": "phomopsis_fruit_rot",
        "phomopsis_blight_and_fruit_rot": "phomopsis_fruit_rot",
        "common_smut": "smut",
        "common_smut_of_corn": "smut",
        "corn_smut": "smut",
        "smut": "smut",
        "northern_corn_leaf_blight": "northern_leaf_blight",
        "northern_leaf_blight": "northern_leaf_blight",
        "wheat_head_scab": "head_scab",
        "head_scab": "head_scab",
        "fusarium_head_blight": "head_scab",
        "fusarium_head_blight_(scab)": "head_scab",
        "head_scab_(fusarium_head_blight)": "head_scab",
        "scab": "head_scab",
        "wheat_rust": "rust",
        "rust": "rust",
        "leaf_rust": "leaf_rust",
        "stripe_rust": "stripe_rust",
        "stem_rust": "stem_rust",
        # Batch 1: Solanaceous aliases
        "frogeye_leaf_spot": "frogeye_leaf_spot",
        "frog_eye_leaf_spot": "frogeye_leaf_spot",
        "frogeye": "frogeye_leaf_spot",
        "bacterial_leaf_streak": "bacterial_leaf_streak_(black_chaff)",
        "black_chaff": "bacterial_leaf_streak_(black_chaff)",
        "cercospora_leaf_spot": "cercospora_leaf_spot",
        "cercospora": "cercospora_leaf_spot",
        "leaf_curl": "leaf_curl",
        "curly_top": "leaf_curl",
        "fruit_fusarium": "fruit_fusarium",
        "fusarium_rot": "fruit_fusarium",
        "leaf_mold": "leaf_mold",
        "mosaic_virus": "mosaic_virus",
        "mosaic": "mosaic_virus",
        "yellow_leaf_curl_virus": "yellow_leaf_curl_virus",
        "yellow_leaf_curl": "yellow_leaf_curl_virus",
        "tylcv": "yellow_leaf_curl_virus",
        "pest_damage": "pest_damage",
        "flea_beetle": "pest_damage",
        "flea_beetles": "pest_damage",
        "pest": "pest_damage",
        "phytophthora_blight": "phytophthora_blight",
        "phytophthora": "phytophthora_blight",
        "wilt_disease": "wilt_disease",
        "verticillium_wilt": "wilt_disease",
        "wilt": "wilt_disease",
        # Batch 2: Cucurbits aliases
        "angular_leaf_spot": "angular_leaf_spot",
        "angular_spot": "angular_leaf_spot",
        "bacterial_wilt": "bacterial_wilt",
        "belly_rot": "belly_rot",
        "rhizoctonia_fruit_rot": "belly_rot",
        "gummy_stem_blight": "gummy_stem_blight",
        "pythium_fruit_rot": "pythium_fruit_rot",
        "cottony_leak": "pythium_fruit_rot",
        "yellow_mosaic_virus": "yellow_mosaic_virus",
        "yellow_mosaic": "yellow_mosaic_virus",
        "zymv": "yellow_mosaic_virus",
        "zucchini_yellow_mosaic": "yellow_mosaic_virus",
        "zucchini_yellow_mosaic_virus": "yellow_mosaic_virus",
    }

    if d_rec and hasattr(d_rec, "disease_slug") and d_rec.disease_slug:
        candidates.append(str(d_rec.disease_slug).strip().lower())
    if disease_slug:
        candidates.append(str(disease_slug).strip().lower())
    CROP_ALIAS_MAP = {
        "bellpepper": "bell_pepper",
        "capsicum": "bell_pepper",
        "pepper": "bell_pepper",
        "peppers": "bell_pepper",
        "french_bean": "bean",
        "beans": "bean",
        "cherry_tomato": "tomato",
        "tomatoes": "tomato",
        "corn_(maize)": "corn",
        "maize": "corn",
        "caneberries": "raspberry",
        "caneberry": "raspberry",
    }
    if disease_slug and "__" in str(disease_slug):
        c_part, d_part = str(disease_slug).strip().lower().split("__", 1)
        c_part = CROP_ALIAS_MAP.get(c_part, c_part)
        candidates.append(f"{c_part}__{d_part}")
    if crop and disease:
        clean_c = str(crop).strip().lower().replace(" ", "_")
        clean_c = CROP_ALIAS_MAP.get(clean_c, clean_c)
        clean_d = str(disease).strip().lower().replace(" ", "_")
        candidates.append(f"{clean_c}__{clean_d}")
        candidates.append(clean_d)
        if clean_d in DISEASE_ALIAS_MAP:
            candidates.append(f"{clean_c}__{DISEASE_ALIAS_MAP[clean_d]}")
    if disease:
        clean_d = str(disease).strip().lower().replace(" ", "_")
        candidates.append(clean_d)
        if clean_d in DISEASE_ALIAS_MAP:
            candidates.append(DISEASE_ALIAS_MAP[clean_d])

    # Also resolve disease_slug aliases if slug format is crop__disease
    expanded = list(candidates)
    for c in candidates:
        if "__" in c:
            cp, dp = c.split("__", 1)
            if dp in DISEASE_ALIAS_MAP:
                expanded.append(f"{cp}__{DISEASE_ALIAS_MAP[dp]}")
    candidates = list(dict.fromkeys(expanded))

    # 1. Match against registered disease-specific sources
    for cand in candidates:
        if cand in DISEASE_SPECIFIC_SOURCES and DISEASE_SPECIFIC_SOURCES[cand]:
            return DISEASE_SPECIFIC_SOURCES[cand]
        # Partial match on disease component
        if "__" in cand:
            crop_part, dis_part = cand.split("__", 1)
            for k, recs in DISEASE_SPECIFIC_SOURCES.items():
                if k == cand or (k.endswith(f"__{dis_part}") and k.startswith(crop_part)):
                    return recs

    # 2. Check if d_rec has directly attached source_records that are non-general
    if d_rec and hasattr(d_rec, "source_records") and d_rec.source_records:
        specific = [s for s in d_rec.source_records if isinstance(s, SourceRecord) and not is_generic_source(s)]
        if specific:
            return specific

    # 3. Fallback: if fallback IDs or d_rec.sources are present, return them as general references
    raw_ids = (fallback_ids or []) + (getattr(d_rec, "sources", []) if d_rec else [])
    out_records = []
    seen = set()
    for sid in raw_ids:
        if sid not in seen:
            seen.add(sid)
            rec = get_source(sid)
            # Ensure marked as general reference
            clean_title = rec.title.replace("[General Reference] ", "").strip()
            rec = SourceRecord(
                source_id=rec.source_id,
                title=f"[General Reference] {clean_title}",
                organization=rec.organization,
                url_or_doi=rec.url_or_doi,
                publication_year=rec.publication_year,
                source_tier=rec.source_tier,
                notes=rec.notes,
                is_general=True,
            )
            out_records.append(rec)
    return out_records


def format_source_citation(
    source_ids: list[str],
    disease_slug: Optional[str] = None,
    crop: Optional[str] = None,
    disease: Optional[str] = None,
    d_rec: Optional[Any] = None,
) -> list[dict[str, Any]]:
    """
    Format source provenance records into readable, actionable citations for final response grounding.
    Preserves exact canonical article titles and URLs for verified disease diagnoses.
    """
    # 1. If disease context is present, prioritize exact disease-specific sources
    if disease_slug or disease or d_rec:
        specific_sources = get_sources_for_disease(
            disease_slug=disease_slug,
            crop=crop,
            disease=disease,
            d_rec=d_rec,
            fallback_ids=source_ids,
        )
        if specific_sources:
            citations = []
            seen_urls = set()
            for s in specific_sources:
                target_url = s.url_or_doi or ""
                key = target_url or s.source_id
                if key not in seen_urls:
                    seen_urls.add(key)
                    citations.append({
                        "source_id": s.source_id,
                        "title": s.title,
                        "organization": s.organization,
                        "tier": s.source_tier.value,
                        "url": target_url,
                        "is_general": s.is_general,
                    })
            if citations:
                return citations

    # 2. General / Fallback formatting
    citations = []
    seen = set()
    for sid in source_ids:
        if sid not in seen:
            seen.add(sid)
            s = get_source(sid)
            is_gen = getattr(s, "is_general", True) or is_generic_source(s)
            t = s.title
            if is_gen and not t.startswith("[General Reference]"):
                t = f"[General Reference] {t}"
            citations.append({
                "source_id": s.source_id,
                "title": t,
                "organization": s.organization,
                "tier": s.source_tier.value,
                "url": s.url_or_doi or "",
                "is_general": is_gen,
            })
    return citations

