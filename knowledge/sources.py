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
# Canonical Disease-Specific Source Association Map
# ---------------------------------------------------------------------------
DISEASE_SPECIFIC_SOURCES: dict[str, list[SourceRecord]] = {
    # Blueberry
    "blueberry__anthracnose": [SOURCE_NC_STATE_BLUEBERRY_ANTHRACNOSE, SOURCE_MSU_BLUEBERRY_ANTHRACNOSE],

    # Bell Pepper
    "bell_pepper__blossom_end_rot": [SOURCE_UGA_PEPPER_BLOSSOM_END_ROT],
    "bell_pepper__bacterial_spot": [SOURCE_NC_STATE_PEPPER_TOMATO_BACTERIAL_SPOT],

    # Tomato
    "tomato__early_blight": [SOURCE_NC_STATE_TOMATO_EARLY_BLIGHT],
    "tomato__late_blight": [SOURCE_NC_STATE_TOMATO_LATE_BLIGHT],
    "tomato__septoria_leaf_spot": [SOURCE_NC_STATE_TOMATO_SEPTORIA_LEAF_SPOT],
    "tomato__bacterial_leaf_spot": [SOURCE_NC_STATE_PEPPER_TOMATO_BACTERIAL_SPOT],

    # Cucurbits
    "cucumber__downy_mildew": [SOURCE_NC_STATE_CUCURBIT_DOWNY_MILDEW],
    "cucumber__powdery_mildew": [SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
    "squash__powdery_mildew": [SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
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

    # 8. Eggplant — Phomopsis Fruit Rot
    "eggplant__phomopsis_fruit_rot": [SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS],
    "eggplant__phomopsis_blight": [SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS],
    "eggplant__phomopsis": [SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS],
    "eggplant__phomopsis_blight_and_fruit_rot": [SOURCE_RUTGERS_EGGPLANT_PHOMOPSIS],

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
    }

    if d_rec and hasattr(d_rec, "disease_slug") and d_rec.disease_slug:
        candidates.append(str(d_rec.disease_slug).strip().lower())
    if disease_slug:
        candidates.append(str(disease_slug).strip().lower())
    if crop and disease:
        clean_c = str(crop).strip().lower().replace(" ", "_")
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

