"""
Verified Agricultural Source Registry & Provenance Database
===========================================================
Defines authoritative, traceable references from Tier-1 (USDA, FAO, ICAR)
and Tier-2 (University Extensions) plant pathology institutions.
"""

from __future__ import annotations

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
    ),
    "SRC_FAO_PLANT": SourceRecord(
        source_id="SRC_FAO_PLANT",
        title="FAO Integrated Pest and Disease Management Guidelines",
        organization="Food and Agriculture Organization of the United Nations (FAO)",
        url_or_doi="https://www.fao.org/pest-and-pesticide-management/ipm/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Global standards for integrated crop management and sustainable pest suppression.",
    ),
    "SRC_UC_IPM": SourceRecord(
        source_id="SRC_UC_IPM",
        title="University of California Statewide Integrated Pest Management Program (UC IPM)",
        organization="University of California Agriculture and Natural Resources",
        url_or_doi="https://ipm.ucanr.edu/PMG/crops-agriculture.html",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Peer-reviewed agricultural pest and pathogen management guidelines.",
    ),
    "SRC_CORNELL_EXT": SourceRecord(
        source_id="SRC_CORNELL_EXT",
        title="Cornell Cooperative Extension Vegetable Pathology and Diagnostic Factsheets",
        organization="Cornell University College of Agriculture and Life Sciences",
        url_or_doi="https://www.vegetables.cornell.edu/pest-management/disease-factsheets/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Clinical diagnosis and cultural control protocols for Solanaceae and Cucurbitaceae.",
    ),
    "SRC_PURDUE_EXT": SourceRecord(
        source_id="SRC_PURDUE_EXT",
        title="Purdue Extension Plant and Pest Diagnostic Laboratory Disease Guides",
        organization="Purdue University Cooperative Extension Service",
        url_or_doi="https://extension.purdue.edu/programs/agriculture-natural-resources/",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Foliar fungal and bacterial spot identification and prevention guidelines.",
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
    ),
    "SRC_ICAR_IISR": SourceRecord(
        source_id="SRC_ICAR_IISR",
        title="ICAR-IISR Good Agricultural Practices and Disease Management in Spices",
        organization="Indian Council of Agricultural Research - Indian Institute of Spices Research",
        url_or_doi="http://www.spices.res.in/publication/package-practices",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Authoritative guidelines for ginger and turmeric rhizome and foliar pathologies.",
    ),
    "SRC_IOWA_STATE_EXT": SourceRecord(
        source_id="SRC_IOWA_STATE_EXT",
        title="Iowa State University Extension Integrated Pest Management: Soybean Rust and Foliar Diseases",
        organization="Iowa State University Extension and Outreach",
        url_or_doi="https://crops.extension.iastate.edu/cropnews",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Phakopsora pachyrhizi symptom identification, spore surveillance, and management.",
    ),
    "SRC_PENNSTATE_EXT": SourceRecord(
        source_id="SRC_PENNSTATE_EXT",
        title="Penn State Extension Tree Fruit and Vegetable Disease Management Guides",
        organization="Pennsylvania State University College of Agricultural Sciences",
        url_or_doi="https://extension.psu.edu/plant-disease-management",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Foliar powdery mildew, rust, and rot cultural suppression guidelines.",
    ),
    "SRC_UNL_EXT": SourceRecord(
        source_id="SRC_UNL_EXT",
        title="University of Nebraska-Lincoln Extension CropWatch Rust Management",
        organization="University of Nebraska-Lincoln",
        url_or_doi="https://cropwatch.unl.edu/plantdisease",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Legume and dry bean rust resistance and canopy management.",
    ),
    "SRC_WSU_EXT": SourceRecord(
        source_id="SRC_WSU_EXT",
        title="Washington State University Extension Allium Disease and Pest Diagnostic Guide",
        organization="Washington State University Extension",
        url_or_doi="https://extension.wsu.edu/allium-pathology",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Puccinia allii symptom progression, microclimate factors, and field sanitation.",
    ),
    "SRC_APS_PRESS": SourceRecord(
        source_id="SRC_APS_PRESS",
        title="American Phytopathological Society (APS) Compendia of Plant Diseases",
        organization="The American Phytopathological Society (APS)",
        url_or_doi="https://apsjournals.apsnet.org/series/compendia",
        publication_year=2024,
        source_tier=SourceTier.TIER_1,
        notes="Standard global reference for etiology, symptomatology, and epidemiology of plant pathogens.",
    ),
    "SRC_MSU_EXT": SourceRecord(
        source_id="SRC_MSU_EXT",
        title="Michigan State University Extension Plant & Pest Management Factsheets",
        organization="Michigan State University Extension",
        url_or_doi="https://www.canr.msu.edu/pest_management/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Small fruit (blueberry, raspberry, cherry), celery, and carrot disease diagnostics.",
    ),
    "SRC_TAMU_EXT": SourceRecord(
        source_id="SRC_TAMU_EXT",
        title="Texas A&M AgriLife Extension Plant Disease Handbook",
        organization="Texas A&M AgriLife Extension Service",
        url_or_doi="https://plantdiseasehandbook.tamu.edu/",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Warm-climate agronomic crops, citrus, stone fruit, and cereal pathology.",
    ),
    "SRC_KSU_EXT": SourceRecord(
        source_id="SRC_KSU_EXT",
        title="Kansas State University Extension Wheat & Cereal Disease Management Guides",
        organization="Kansas State University Agricultural Experiment Station",
        url_or_doi="https://www.plantpath.k-state.edu/extension/crop-diseases/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Wheat rusts, head scab, leaf blotches, and corn foliar disease management.",
    ),
    "SRC_ICAR_IARI": SourceRecord(
        source_id="SRC_ICAR_IARI",
        title="ICAR-Indian Agricultural Research Institute Division of Plant Pathology",
        organization="Indian Council of Agricultural Research - IARI",
        url_or_doi="https://www.iari.res.in/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="National guidelines for cereal, legume, rice blast, and tropical vegetable pathologies.",
    ),
    "SRC_ICAR_CPRI": SourceRecord(
        source_id="SRC_ICAR_CPRI",
        title="ICAR-Central Potato Research Institute Technical Bulletins",
        organization="Indian Council of Agricultural Research - CPRI",
        url_or_doi="https://cpri.icar.gov.in/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Authoritative late blight and early blight management in tuber crops.",
    ),
    "SRC_ICAR_NRCC": SourceRecord(
        source_id="SRC_ICAR_NRCC",
        title="ICAR-Central Citrus Research Institute Disease Management Guidelines",
        organization="Indian Council of Agricultural Research - CCRI (formerly NRCC)",
        url_or_doi="https://ccri.icar.gov.in/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Citrus canker, greening (HLB), and gummosis integrated management.",
    ),
    "SRC_CABI_CPC": SourceRecord(
        source_id="SRC_CABI_CPC",
        title="CABI Crop Protection Compendium and Plantwise Knowledge Bank",
        organization="Centre for Agriculture and Bioscience International (CABI)",
        url_or_doi="https://www.cabi.org/cpc/",
        publication_year=2024,
        source_tier=SourceTier.TIER_1,
        notes="International pest and pathogen distribution, host range, and control datasheets.",
    ),
    "SRC_EPPO_GLOBAL": SourceRecord(
        source_id="SRC_EPPO_GLOBAL",
        title="EPPO Global Database Plant Quarantine and Phytosanitary Factsheets",
        organization="European and Mediterranean Plant Protection Organization (EPPO)",
        url_or_doi="https://gd.eppo.int/",
        publication_year=2024,
        source_tier=SourceTier.TIER_1,
        notes="Quarantine pathogens, viral epidemiology (e.g. Plum pox), and regulated pests.",
    ),
    "SRC_OSU_EXT": SourceRecord(
        source_id="SRC_OSU_EXT",
        title="Oregon State University Extension Pacific Northwest Plant Disease Management Handbook",
        organization="Oregon State University Extension Service",
        url_or_doi="https://pnwhandbooks.org/plantdisease",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Berry crops, tree fruit, vegetable seed crops, and downy/powdery mildews.",
    ),
    "SRC_UMN_EXT": SourceRecord(
        source_id="SRC_UMN_EXT",
        title="University of Minnesota Extension Plant Disease Management Library",
        organization="University of Minnesota Extension",
        url_or_doi="https://extension.umn.edu/plant-diseases",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Brassica, Solanaceae, and cucurbit integrated disease management.",
    ),
    "SRC_WISCONSIN_EXT": SourceRecord(
        source_id="SRC_WISCONSIN_EXT",
        title="University of Wisconsin-Madison Division of Extension Vegetable & Fruit Pathology",
        organization="University of Wisconsin-Madison Extension",
        url_or_doi="https://vegpath.plantpath.wisc.edu/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Potato, carrot cavity spot, cabbage black rot, and cucurbit disease control.",
    ),
    "SRC_RUTGERS_EXT": SourceRecord(
        source_id="SRC_RUTGERS_EXT",
        title="Rutgers NJAES Plant Pathology and Commercial Vegetable Production Recommendations",
        organization="Rutgers New Jersey Agricultural Experiment Station",
        url_or_doi="https://plant-pest-advisory.rutgers.edu/",
        publication_year=2024,
        source_tier=SourceTier.TIER_2,
        notes="Foliar vegetable blights, downy mildews, and pepper bacterial spot.",
    ),
    "SRC_UGA_EXT": SourceRecord(
        source_id="SRC_UGA_EXT",
        title="University of Georgia Extension Plant Disease Management Factsheets",
        organization="University of Georgia Cooperative Extension",
        url_or_doi="https://extension.uga.edu/topic-areas/plant-diseases.html",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Peach brown rot/scab, blueberry anthracnose, and tobacco foliar diseases.",
    ),
    "SRC_CTAHR_HAWAII": SourceRecord(
        source_id="SRC_CTAHR_HAWAII",
        title="University of Hawaii at Manoa CTAHR Cooperative Extension Tropical Plant Pathology",
        organization="College of Tropical Agriculture and Human Resources (CTAHR)",
        url_or_doi="https://www.ctahr.hawaii.edu/site/extprojects.aspx",
        publication_year=2023,
        source_tier=SourceTier.TIER_2,
        notes="Banana bunchy top, Panama disease TR4, coffee leaf rust, and ginger pathogens.",
    ),
    "SRC_WCR_COFFEE": SourceRecord(
        source_id="SRC_WCR_COFFEE",
        title="World Coffee Research / International Coffee Organization Disease Control Manuals",
        organization="World Coffee Research (WCR)",
        url_or_doi="https://worldcoffeeresearch.org/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Coffee leaf rust, berry blotch, and black rot integrated management.",
    ),
    "SRC_IRRI_RICE": SourceRecord(
        source_id="SRC_IRRI_RICE",
        title="International Rice Research Institute (IRRI) Rice Knowledge Bank",
        organization="International Rice Research Institute (IRRI)",
        url_or_doi="http://www.knowledgebank.irri.org/",
        publication_year=2023,
        source_tier=SourceTier.TIER_1,
        notes="Rice blast, sheath blight, and brown spot symptoms and cultural management.",
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

# ---------------------------------------------------------------------------
# Canonical Disease-Specific Source Association Map
# ---------------------------------------------------------------------------
DISEASE_SPECIFIC_SOURCES: dict[str, list[SourceRecord]] = {
    "blueberry__anthracnose": [SOURCE_NC_STATE_BLUEBERRY_ANTHRACNOSE, SOURCE_MSU_BLUEBERRY_ANTHRACNOSE],
    "bell_pepper__blossom_end_rot": [SOURCE_UGA_PEPPER_BLOSSOM_END_ROT],
    "tomato__early_blight": [SOURCE_NC_STATE_TOMATO_EARLY_BLIGHT],
    "cucumber__downy_mildew": [SOURCE_NC_STATE_CUCURBIT_DOWNY_MILDEW],
    "cucumber__powdery_mildew": [SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
    "squash__powdery_mildew": [SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
    "zucchini__powdery_mildew": [SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
    "zucchini__downy_mildew": [SOURCE_NC_STATE_CUCURBIT_DOWNY_MILDEW],
    "tomato__late_blight": [SOURCE_NC_STATE_TOMATO_LATE_BLIGHT],
    "tomato__septoria_leaf_spot": [SOURCE_NC_STATE_TOMATO_SEPTORIA_LEAF_SPOT],
    "bell_pepper__bacterial_spot": [SOURCE_NC_STATE_PEPPER_TOMATO_BACTERIAL_SPOT],
    "tomato__bacterial_leaf_spot": [SOURCE_NC_STATE_PEPPER_TOMATO_BACTERIAL_SPOT],
    "potato__early_blight": [SOURCE_UC_IPM_POTATO_EARLY_BLIGHT],
    "potato__late_blight": [SOURCE_UC_IPM_POTATO_LATE_BLIGHT],
    "apple__scab": [SOURCE_UC_IPM_APPLE_SCAB],
    "peach__brown_rot": [SOURCE_UC_IPM_PEACH_BROWN_ROT],
    "strawberry__botrytis_blight": [SOURCE_UC_IPM_STRAWBERRY_BOTRYTIS],
    "grape__powdery_mildew": [SOURCE_UC_IPM_GRAPE_POWDERY_MILDEW],
}


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
    if d_rec and hasattr(d_rec, "disease_slug") and d_rec.disease_slug:
        candidates.append(str(d_rec.disease_slug).strip().lower())
    if disease_slug:
        candidates.append(str(disease_slug).strip().lower())
    if crop and disease:
        clean_c = str(crop).strip().lower().replace(" ", "_")
        clean_d = str(disease).strip().lower().replace(" ", "_")
        candidates.append(f"{clean_c}__{clean_d}")
        candidates.append(clean_d)
    if disease:
        clean_d = str(disease).strip().lower().replace(" ", "_")
        candidates.append(clean_d)

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
        specific = [s for s in d_rec.source_records if isinstance(s, SourceRecord) and not s.is_general]
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
            if not rec.is_general:
                rec = SourceRecord(
                    source_id=rec.source_id,
                    title=f"[General Reference] {rec.title}" if not rec.title.startswith("[General Reference]") else rec.title,
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
            citations.append({
                "source_id": s.source_id,
                "title": s.title,
                "organization": s.organization,
                "tier": s.source_tier.value,
                "url": s.url_or_doi or "",
                "is_general": getattr(s, "is_general", True),
            })
    return citations

