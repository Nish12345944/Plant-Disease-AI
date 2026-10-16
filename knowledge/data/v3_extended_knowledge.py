"""
Authoritative Plant Pathology Knowledge Extension for Model 2 V3
Covers the 24 newly added classes and missing crop profiles to complete 100% coverage
across all 151 disease classes and 36 crops.

Authoritative Sources:
- University of California Statewide Integrated Pest Management Program (UC IPM)
- University of Florida IFAS Extension (UF/IFAS)
- University of Georgia Extension (UGA)
- Clemson University Cooperative Extension
- North Carolina State University Extension (NC State)
- Tamil Nadu Agricultural University (TNAU) / ICAR
"""

from knowledge.schema import (
    DiseaseRecord,
    CropRecord,
    PathogenType,
    PlantPart,
    TreatmentPlan,
    ChemicalControl,
    CulturalControl,
    BiologicalControl,
    PreventionProtocol,
    SourcedFact,
)
from knowledge.sources import SOURCE_REGISTRY

V3_EXTENDED_DISEASES: dict[str, DiseaseRecord] = {
    "blueberry__exobasidium": DiseaseRecord(
        id="blueberry__exobasidium",
        canonical_name="Blueberry Exobasidium Fruit and Leaf Spot",
        crop="blueberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Exobasidium maculosum",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.SHOOT],
        symptoms=[
            "Distinct pale green, yellow, or white circular spots on the upper leaf surface",
            "Dense, white, velvety layer of fungal basidiospores on the corresponding lower leaf surface",
            "Circular white-to-greenish-white spots on immature green berries that remain green and firm when surrounding fruit ripens",
            "Defoliation and unmarketable spotted fruit at harvest",
        ],
        symptom_progression="Basidiospore infection occurs at bud break -> latent incubation until leaf/fruit expansion -> dense white spore mat develops on undersides and berries.",
        development_conditions="Prolonged leaf wetness, high relative humidity (>85%), and mild temperatures (15-22°C) during early bud expansion.",
        spread_transmission="Wind-driven basidiospores and rain splash from overwintered fungal colonies on bud scales.",
        infection_sources="Overwintering mycelium on bud scales, twigs, and dormant bark.",
        immediate_actions=[
            "Prune out shoots showing white velvety lower-leaf lesions during early spring scouting",
            "Adjust irrigation timing to ensure bushes dry completely before nightfall",
            "Mark affected blocks for targeted dormant lime sulfur or copper application before the next growing season",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Canopy pruning for air penetration",
                    purpose="Open bush canopy to increase sunlight penetration and accelerate foliage drying.",
                    source_id="SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM",
                ),
                CulturalControl(
                    practice="Drip irrigation conversion",
                    purpose="Eliminate overhead canopy wetting to prevent basidiospore release and germination.",
                    source_id="SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM",
                ),
            ],
            biological=[
                BiologicalControl(
                    agent="Bacillus amyloliquefaciens",
                    application_method="Preventative foliar spray applied at early bud break.",
                    source_id="SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Lime Sulfur or Calcium Polysulfide",
                    application_method="Single delayed-dormant application just before bud swell.",
                    restrictions="Dormant application only; do not apply once green tissue emerges to avoid severe leaf burn. Product must be registered in user region.",
                    source_id="SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM",
                ),
                ChemicalControl(
                    active_ingredient="Captan / Fenbuconazole (FRAC 3)",
                    application_method="Foliar protectant spray applied at late bud break and early bloom.",
                    restrictions="Follow label rates and strict pre-harvest intervals (PHI). Must be approved for blueberry in the grower's area.",
                    source_id="SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM",
                ),
            ],
            immediate_actions=[
                "Prune out shoots showing white velvety lower-leaf lesions during early spring scouting",
                "Cease overhead irrigation to eliminate spore splash",
            ],
        ),
        treatment_limitations=[
            "Fungicides cannot reverse existing circular spots on ripening fruit; timing at late-dormant and bud-break is essential for control.",
            "All chemical applications must strictly follow product label instructions, worker protection standards (PPE), and regional registration.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Prune out dead wood and twig cankers during winter dormancy",
                "Sanitize pruning equipment with 70% isopropyl alcohol between rows",
            ],
            cultural_preventions=[
                "Plant high-bush varieties with open, upright canopy architectures",
                "Maintain weed-free strips beneath bush canopies to optimize airflow",
            ],
            monitoring_schedule="Scout bushes weekly from bud break through green fruit development",
        ),
        sources=[SOURCE_REGISTRY["SRC_UF_IFAS_BLUEBERRY_EXOBASIDIUM"]],
    ),

    "blueberry__septoria_leaf_spot": DiseaseRecord(
        id="blueberry__septoria_leaf_spot",
        canonical_name="Blueberry Septoria Leaf Spot",
        crop="blueberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Septoria albopunctata",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM],
        symptoms=[
            "Small circular to angular leaf spots (1-3 mm) with white or tan centers and sharp dark purple or red margins",
            "Tiny black speck-like pycnidia fruiting bodies embedded inside the white centers of mature lesions",
            "Premature post-harvest defoliation, especially in the lower and interior canopy",
            "Reduced fruit bud formation and weakened cane vigor for the subsequent season",
        ],
        symptom_progression="Ascospores initiate lower leaf lesions in late spring -> secondary conidia splash throughout canopy in summer -> heavy premature defoliation in late summer.",
        development_conditions="Warm temperatures (22-28°C) accompanied by frequent rains or prolonged sprinkler irrigation.",
        spread_transmission="Water-splashed conidia from pycnidia and wind-disseminated ascospores from overwintered leaf litter.",
        infection_sources="Fallen leaves and infected dormant twigs.",
        immediate_actions=[
            "Rake or flail-mow fallen diseased leaves beneath bushes to accelerate litter decomposition",
            "Transition from overhead irrigation to drip or micro-sprinkler systems",
            "Apply post-harvest protectant spray if severe defoliation threatens flower bud initiation",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Canopy thinning and ground aeration",
                    purpose="Facilitate air circulation to dry foliage rapidly following rainfall.",
                    source_id="SRC_UGA_BLUEBERRY_SEPTORIA",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Captan / Boscalid + Pyraclostrobin (FRAC 7 + 11)",
                    application_method="Foliar protectant spray applied post-harvest or at first symptom onset.",
                    restrictions="Rotate FRAC classes to mitigate resistance. Adhere to REI and local agricultural pesticide regulations.",
                    source_id="SRC_UGA_BLUEBERRY_SEPTORIA",
                )
            ],
            immediate_actions=[
                "Rake or mow fallen leaf litter beneath plants",
                "Avoid overhead irrigation during summer months",
            ],
        ),
        treatment_limitations=[
            "Chemical treatments cannot restore necrotic white-centered leaf spots; focus is on preventing secondary spread and preserving photosynthetic leaf area.",
            "Always follow label PPE and state/regional chemical registrations.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Shred or incorporate fallen leaves in late autumn with a flail mower to destroy overwintering pycnidia",
                "Apply organic pine bark mulch to create a barrier over soilborne fungal inocula",
            ],
            cultural_preventions=[
                "Maintain wide row spacing (minimum 10-12 feet between rows)",
                "Avoid planting in low-lying frost pockets with sluggish air drainage",
            ],
            monitoring_schedule="Scout foliage bi-weekly starting mid-summer through post-harvest",
        ),
        sources=[SOURCE_REGISTRY["SRC_UGA_BLUEBERRY_SEPTORIA"]],
    ),

    "cauliflower__alternaria_brassicae": DiseaseRecord(
        id="cauliflower__alternaria_brassicae",
        canonical_name="Cauliflower Alternaria Leaf Spot",
        crop="cauliflower",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Alternaria brassicae",
        affected_parts=[PlantPart.LEAF, PlantPart.HEAD, PlantPart.STEM],
        symptoms=[
            "Yellow to brown circular lesions with distinct dark concentric target-like rings",
            "Black velvety spore growth appearing inside mature lesions under humid conditions",
            "Brown to black sunken necrotic speckling and rotting of the white edible curd",
            "Lower leaf chlorosis followed by premature leaf drop",
        ],
        symptom_progression="Seedborne or airborne conidia infect seedling foliage -> concentric spots expand on wrapper leaves -> spore rain infects maturing curd.",
        development_conditions="Warm, humid weather (18-24°C) with continuous free moisture on leaves for 8-10 hours.",
        spread_transmission="Wind-blown conidia and rain-splash from infected crucifer crop residues.",
        infection_sources="Infected cruciferous seeds, brassica weeds, and overwintering crop debris.",
        immediate_actions=[
            "Rogue out severely diseased outer leaves showing black target lesions",
            "Shift irrigation schedule to early morning so foliage dries rapidly in morning sunlight",
            "Harvest marketable heads promptly before curd surface browning occurs",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Crop rotation out of brassicas",
                    purpose="Rotate with non-cruciferous crops for at least 3 years to starve soilborne spore reserves.",
                    source_id="SRC_UC_IPM_COLE_ALTERNARIA_CAULIFLOWER",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Bacillus amyloliquefaciens (Strain D747)",
                    application_method="Preventative foliar spray applied prior to canopy closure.",
                    source_id="SRC_UC_IPM_COLE_ALTERNARIA_CAULIFLOWER",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide or Azoxystrobin (FRAC 11)",
                    application_method="Foliar protectant spray at first detection of leaf spots.",
                    restrictions="Follow strict pre-harvest interval (PHI) to prevent curd chemical residues. Observe local pesticide laws.",
                    source_id="SRC_UC_IPM_COLE_ALTERNARIA_CAULIFLOWER",
                )
            ],
            immediate_actions=[
                "Remove and bury infected lower wrapper leaves",
                "Ensure morning-only irrigation",
            ],
        ),
        treatment_limitations=[
            "Curd browning lesions cannot be reversed; protectant sprays must be applied before curd exposure.",
            "Verify product registration for brassica vegetable crops in user's state/country.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Deep-plow or shred crop residues immediately following curd harvest",
                "Eradicate cruciferous weed hosts (wild mustard, shepherd's purse) along field boundaries",
            ],
            cultural_preventions=[
                "Use hot-water treated seed (50°C for 25 minutes) or certified disease-free seed",
                "Employ drip irrigation beneath plastic or organic mulch",
            ],
            monitoring_schedule="Inspect seedlings in seedbeds and field crops weekly",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_COLE_ALTERNARIA_CAULIFLOWER"]],
    ),

    "cauliflower__black_spot": DiseaseRecord(
        id="cauliflower__black_spot",
        canonical_name="Cauliflower Black Spot (Alternaria Curd Spot)",
        crop="cauliflower",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Alternaria brassicicola / Alternaria brassicae",
        affected_parts=[PlantPart.HEAD, PlantPart.LEAF],
        symptoms=[
            "Minute dark brown to jet-black necrotic spots on the white florets of the cauliflower curd",
            "Rapid coalescing of spots into larger sunken black rot patches on the curd surface",
            "Associated circular target-spot lesions on outer wrapper leaves",
            "Secondary bacterial soft rot invasion turning curd into foul-smelling mush",
        ],
        symptom_progression="Airborne conidia wash into curd branches -> micro-lesions form on floret tips -> extensive black rotting under wet conditions.",
        development_conditions="High relative humidity (>90%), persistent dew or rain, and temperatures of 16-24°C during curd maturation.",
        spread_transmission="Rain splash, overhead irrigation, and harvesting equipment.",
        infection_sources="Infested seeds, diseased wrapper leaves, and brassica residue.",
        immediate_actions=[
            "Harvest mature heads immediately during dry weather to prevent floret decay",
            "Tie outer leaves over developing curds (blanching) to shield from rain and direct spore deposition",
            "Cease overhead irrigation immediately upon curd initiation",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Curd protection and blanching",
                    purpose="Fold inner leaves over the head to block rain splash and fungal conidia contact.",
                    source_id="SRC_UC_IPM_COLE_ALTERNARIA_BLACK_SPOT",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil or Copper Octanoate",
                    application_method="Foliar protectant spray applied to wrapper leaves before curds develop.",
                    restrictions="Do not apply chlorothalonil directly to exposed edible curds close to harvest. Comply with labeled PHI.",
                    source_id="SRC_UC_IPM_COLE_ALTERNARIA_BLACK_SPOT",
                )
            ],
            immediate_actions=[
                "Harvest unaffected mature heads promptly",
                "Shield exposed curds from moisture",
            ],
        ),
        treatment_limitations=[
            "Black spot blemishes on edible white curds cannot be chemically cured; unmarketable curds must be culled.",
            "Strictly observe harvest withholding intervals.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Sanitize harvest knives and storage bins with food-grade sanitizers",
                "Remove and compost or bury all culled curds away from production fields",
            ],
            cultural_preventions=[
                "Select cauliflower cultivars with strong self-wrapping leaf habits",
                "Maintain 3-year crop rotation out of crucifers",
            ],
            monitoring_schedule="Inspect curds every 3 days once head diameter exceeds 5 cm",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_COLE_ALTERNARIA_BLACK_SPOT"]],
    ),

    "cauliflower__black_rot": DiseaseRecord(
        id="cauliflower__black_rot",
        canonical_name="Cauliflower Black Rot",
        crop="cauliflower",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Xanthomonas campestris pv. campestris",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.HEAD],
        symptoms=[
            "Distinct V-shaped yellow (chlorotic) lesions pointing inward from leaf margins with the wide base at the leaf edge",
            "Veins within the chlorotic and necrotic V-shaped zone turn dark brown or black",
            "Cross-sections of stems and leaf petioles reveal a distinctive black ring of vascular bundles",
            "Severe systemic wilting, stunting, curd malformation, and premature leaf drop",
        ],
        symptom_progression="Bacteria enter leaf hydathodes at margins -> multiply in xylem vessels -> blacken vascular bundles -> cause systemic chlorosis and wilt.",
        development_conditions="Warm, wet weather (24-30°C) with persistent fog, dew, rain, or sprinkler irrigation.",
        spread_transmission="Water splash, machinery, workers walking through wet foliage, and contaminated seed.",
        infection_sources="Contaminated seed, infected transplants, and cruciferous weed hosts.",
        immediate_actions=[
            "Rogue out and destroy infected seedlings and plants showing marginal V-shaped chlorosis",
            "Strictly avoid working in or walking through cauliflower fields when foliage is wet",
            "Sanitize all tools, spray booms, and boots with disinfectant before moving to clean fields",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Strict field hygiene and dry handling",
                    purpose="Prevent mechanical transfer of bacterial ooze through hydathodes and wounds.",
                    source_id="SRC_UC_IPM_COLE_BLACK_ROT_CAULIFLOWER",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide + Mancozeb tank mix",
                    application_method="Preventative foliar spray applied early in disease cycle.",
                    restrictions="Bactericides provide only suppression and will not cure systemic vascular infections. Check local approval.",
                    source_id="SRC_UC_IPM_COLE_BLACK_ROT_CAULIFLOWER",
                )
            ],
            immediate_actions=[
                "Rogue out and destroy symptomatic plants immediately",
                "Disinfect transplant trays and pruning knives",
            ],
        ),
        treatment_limitations=[
            "Once black rot enters the vascular xylem system of cauliflower, no curative chemical spray can cure the plant.",
            "Antibiotic treatments are prohibited in agricultural vegetable production in most jurisdictions.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Hot-water seed treatment at 50°C for 25 minutes to eliminate internal bacterial load",
                "3-year minimum rotation away from all brassica species (broccoli, cabbage, kale, mustard)",
            ],
            cultural_preventions=[
                "Purchase certified black-rot-free seed and inspected transplant plugs",
                "Ensure drip irrigation to prevent water droplet splashing across plants",
            ],
            monitoring_schedule="Inspect seedbeds daily and field plantings twice weekly",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_COLE_BLACK_ROT_CAULIFLOWER"]],
    ),

    "cauliflower__downy_mildew": DiseaseRecord(
        id="cauliflower__downy_mildew",
        canonical_name="Cauliflower Downy Mildew",
        crop="cauliflower",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Hyaloperonospora parasitica (syn. Peronospora parasitica)",
        affected_parts=[PlantPart.LEAF, PlantPart.HEAD, PlantPart.STEM],
        symptoms=[
            "Pale green to yellow angular chlorotic patches on the upper surface of leaves, bordered by veins",
            "Fluffy white to grayish-purple mildew growth on corresponding lower leaf surfaces during cool humid mornings",
            "Internal gray-to-black streak discoloration in the curd and curd branches",
            "Severe seedling damping-off and stunting in nursery beds",
        ],
        symptom_progression="Airborne sporangia infect leaves under cool moist conditions -> fluffy mildew erupts on underside -> systemic invasion discolors curd stalk.",
        development_conditions="Cool temperatures (10-16°C) accompanied by heavy dews, fog, drizzle, and high relative humidity (>90%).",
        spread_transmission="Wind-blown sporangia and rain splash over long distances.",
        infection_sources="Overwintering oospores in soil and crop debris, cruciferous weeds, and infected seedbed transplants.",
        immediate_actions=[
            "Increase ventilation and airflow in seedbeds and tunnels to lower relative humidity",
            "Remove and discard severely infected seedlings showing white mildew on leaf undersides",
            "Water plants early in the day so leaf surfaces dry rapidly in the morning sun",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Moisture reduction and spacing",
                    purpose="Reduce relative humidity below 85% to halt sporangial germination and sporulation.",
                    source_id="SRC_UC_IPM_COLE_DOWNY_MILDEW_CAULIFLOWER",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Bacillus subtilis",
                    application_method="Foliar biofungicide applied prior to onset of cool, wet weather.",
                    source_id="SRC_UC_IPM_COLE_DOWNY_MILDEW_CAULIFLOWER",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mandipropamid (FRAC 40) or Dimethomorph",
                    application_method="Targeted oomycete foliar spray at first appearance of lower leaf mildew.",
                    restrictions="Strictly rotate FRAC modes of action to manage fungicide resistance. Adhere to labeled PHI and REI.",
                    source_id="SRC_UC_IPM_COLE_DOWNY_MILDEW_CAULIFLOWER",
                )
            ],
            immediate_actions=[
                "Ventilate greenhouses to reduce humidity",
                "Apply morning-only drip irrigation",
            ],
        ),
        treatment_limitations=[
            "Systemic curd vascular discoloration cannot be reversed by chemical sprays.",
            "Pesticide products must be labeled for cauliflower and oomycete control in the target region.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Plow down or destroy brassica crop residues immediately after final harvest",
                "Keep field borders clear of wild crucifer weed reservoirs",
            ],
            cultural_preventions=[
                "Select downy-mildew-tolerant cauliflower cultivars",
                "Ensure generous plant spacing (45-60 cm) to allow vigorous cross-canopy ventilation",
            ],
            monitoring_schedule="Scout leaf undersides twice weekly during cool, foggy periods",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_COLE_DOWNY_MILDEW_CAULIFLOWER"]],
    ),

    "cauliflower__pest_damage": DiseaseRecord(
        id="cauliflower__pest_damage",
        canonical_name="Cauliflower Pest Damage (Caterpillars & Flea Beetles)",
        crop="cauliflower",
        pathogen_type=PathogenType.PEST,
        pathogen_name="Trichoplusia ni (Cabbage Looper) / Plutella xylostella / Phyllotreta spp.",
        affected_parts=[PlantPart.LEAF, PlantPart.HEAD],
        symptoms=[
            "Irregular ragged holes chewed in leaves by green caterpillar larvae",
            "Shot-hole damage on young cotyledons and leaves caused by tiny jumping flea beetles",
            "Dark green to black fecal pellets (frass) accumulating on wrapper leaves and contaminating curds",
            "Skeletonized foliage and bore-holes entering mature cauliflower curds",
        ],
        symptom_progression="Moths/beetles lay eggs on leaf undersides -> larvae hatch and feed voraciously -> extensive defoliation and curd contamination.",
        development_conditions="Warm, dry summer temperatures that accelerate insect reproduction and lifecycle completion.",
        spread_transmission="Adult insect flight, migration from wild mustard weeds and adjacent brassica fields.",
        infection_sources="Surrounding cruciferous weeds and field residue harboring pupae.",
        immediate_actions=[
            "Handpick visible green loopers and worms on small plots or home gardens",
            "Apply floating row covers or fine insect netting over young beds to exclude egg-laying adult moths",
            "Wash frass contamination from curds immediately after harvest with potable water",
        ],
        treatment_category="curable",
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    practice="Physical exclusion and netting",
                    purpose="Install 0.8 mm insect mesh to completely block moth oviposition.",
                    source_id="SRC_UC_IPM_COLE_CABBAGE_LOOPER",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Bacillus thuringiensis kurstaki (Bt)",
                    application_method="Foliar biological spray applied late in the afternoon against young caterpillar instars.",
                    source_id="SRC_UC_IPM_COLE_CABBAGE_LOOPER",
                ),
                BiologicalControl(
                    agent="Spinosad",
                    application_method="Bio-insecticide spray applied when caterpillar feeding thresholds are breached.",
                    source_id="SRC_UC_IPM_COLE_CABBAGE_LOOPER",
                ),
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorantraniliprole (FRAC/IRAC 28) or Methoxyfenozide",
                    application_method="Targeted selective insecticide spray applied according to economic thresholds.",
                    restrictions="Preserve beneficial predator populations; do not apply during active pollinator flights. Adhere to PHI.",
                    source_id="SRC_UC_IPM_COLE_CABBAGE_LOOPER",
                )
            ],
            immediate_actions=[
                "Handpick caterpillars or apply Bt kurstaki in evening hours",
                "Deploy floating row covers to exclude moths",
            ],
        ),
        treatment_limitations=[
            "Bt degrades rapidly under intense solar UV radiation; reapply after heavy rain or within 5-7 days.",
            "Insecticide products must be officially registered for edible brassica vegetables.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Disincorporate crop residues immediately after harvest to destroy pupating cocoons in soil",
                "Eliminate wild mustard and radish weed hosts surrounding fields",
            ],
            cultural_preventions=[
                "Intercrop with aromatic companions or use brassica trap crops (e.g. collards)",
                "Conserve beneficial predators (parasitoid wasps, ground beetles, spiders)",
            ],
            monitoring_schedule="Scout 20 plants across field weekly for egg clusters and young larvae",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_COLE_CABBAGE_LOOPER"]],
    ),

    "ginger__leaf_blight": DiseaseRecord(
        id="ginger__leaf_blight",
        canonical_name="Ginger Leaf Blight",
        crop="ginger",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Phyllosticta zingiberi / Colletotrichum zingiberis",
        affected_parts=[PlantPart.LEAF, PlantPart.SHEATH],
        symptoms=[
            "Small oval to elongated yellowish spots appearing on young leaves",
            "Spots enlarge and develop white or papery grayish centers surrounded by dark brown margins and chlorotic halos",
            "Extensive blight patches causing complete drying and shredding of ginger foliage",
            "Severely reduced photosynthetic capability resulting in stunted, small rhizomes",
        ],
        symptom_progression="Conidia germinate on wet leaf blades -> necrotic spots spread along leaf axis -> entire leaf dries and shreds during monsoon rains.",
        development_conditions="High temperatures (25-32°C), heavy rainfall, high humidity (>85%), and excessive shade.",
        spread_transmission="Rain splash, overhead runoff water, and farm implements.",
        infection_sources="Infected seed rhizomes, volunteer ginger plants, and persistent crop residue in soil.",
        immediate_actions=[
            "Prune and burn severely blighted leaves showing papery circular lesions to reduce field spore load",
            "Thin overstory shade trees to provide 30-40% optimal filtered sunlight and improve air drainage",
            "Ensure field drainage channels are clear to prevent waterlogging around raised beds",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Raised-bed cultivation and drainage",
                    purpose="Plant on 30 cm raised beds to prevent stagnant waterlogging around ginger rhizomes.",
                    source_id="SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT",
                ),
                CulturalControl(
                    practice="Shade management",
                    purpose="Maintain 30-40% partial shade to optimize ginger photosynthesis while allowing rapid leaf drying.",
                    source_id="SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT",
                ),
            ],
            biological=[
                BiologicalControl(
                    agent="Trichoderma viride / Pseudomonas fluorescens",
                    application_method="Rhizome treatment and soil application with organic compost at planting.",
                    source_id="SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Bordeaux Mixture (1%) or Copper Oxychloride (0.2%) or Mancozeb",
                    application_method="Foliar protectant spray applied at onset of monsoon rains; repeat at 2-3 week intervals.",
                    restrictions="Ensure thorough coverage of lower leaf surfaces. Follow regional spice board recommendations and safety intervals.",
                    source_id="SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT",
                )
            ],
            immediate_actions=[
                "Remove and burn blighted leaf tips",
                "Ensure drainage channels are open and free-flowing",
            ],
        ),
        treatment_limitations=[
            "Blighted necrotic leaf tissue cannot be regenerated; preventative spray coverage is crucial during peak monsoon showers.",
            "Use only agrochemicals registered for commercial spice production in your jurisdiction.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Select healthy, plump, certified disease-free seed rhizomes for planting",
                "Dip seed rhizomes in bioagent slurry (Trichoderma viride) for 30 minutes prior to storage and planting",
            ],
            cultural_preventions=[
                "Practice 3-year crop rotation with non-host crops like maize, legumes, or tapioca",
                "Apply thick green leaf mulch (e.g. Pongamia or neem leaves) to suppress splash dispersal",
            ],
            monitoring_schedule="Scout ginger plots weekly from shoot emergence through monsoon season",
        ),
        sources=[SOURCE_REGISTRY["SRC_TNAU_GINGER_LEAF_SPOT_BLIGHT"]],
    ),

    "ginger__pest_damage": DiseaseRecord(
        id="ginger__pest_damage",
        canonical_name="Ginger Pest Damage (Shoot Borer & Rhizome Scale)",
        crop="ginger",
        pathogen_type=PathogenType.PEST,
        pathogen_name="Conogethes punctiferalis (Shoot Borer) / Aspidiella hartii (Rhizome Scale)",
        affected_parts=[PlantPart.STEM, PlantPart.SHOOT, PlantPart.ROOT],
        symptoms=[
            "Central pseudostem shoot yellows and dries up, producing a classic 'dead heart' symptom",
            "Bore holes visible on ginger pseudostems with frass (excreta) extruding from the entry points",
            "Rhizomes in storage or soil encrusted with white scale insects, resulting in shriveling and bud death",
            "Stunted pseudostems with poor tiller emergence and rhizome yield reduction",
        ],
        symptom_progression="Larva bores into central pseudostem -> feeds on inner vascular core -> central shoot wilts into 'dead heart' -> larva pupates inside stalk.",
        development_conditions="Warm, humid tropical conditions (26-34°C); peak shoot borer activity occurs July to October.",
        spread_transmission="Adult moth flight between ginger fields and infested seed rhizome movement.",
        infection_sources="Wild host plants (turmeric, castor) and infested stored rhizomes.",
        immediate_actions=[
            "Cut and burn pseudostems showing 'dead hearts' and bore holes to eliminate larvae inside",
            "Inspect stored seed rhizomes and discard scale-infested shriveled seed pieces",
            "Deploy light traps or pheromone monitoring traps around ginger plots",
        ],
        treatment_category="curable",
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    practice="Physical dead-heart roguing",
                    purpose="Cut infested pseudostems below borer entry hole and destroy larvae.",
                    source_id="SRC_LUCID_GINGER_WEEVIL",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Bacillus thuringiensis (Bt) or Neem Seed Kernel Extract (NSKE 5%)",
                    application_method="Foliar spray targeted at pseudostems every 15-20 days from July to October.",
                    source_id="SRC_LUCID_GINGER_WEEVIL",
                ),
                BiologicalControl(
                    agent="Beauveria bassiana",
                    application_method="Rhizome treatment and soil application to manage scale insects.",
                    source_id="SRC_LUCID_GINGER_WEEVIL",
                ),
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorantraniliprole or Flubendiamide",
                    application_method="Targeted pseudostem spray when shoot borer damage exceeds 5% of stalks.",
                    restrictions="Spray directly onto pseudostems. Adhere strictly to spice export pre-harvest intervals.",
                    source_id="SRC_LUCID_GINGER_WEEVIL",
                )
            ],
            immediate_actions=[
                "Cut and destroy stems showing dead hearts",
                "Spray NSKE (5%) or approved bio-insecticide on pseudostems",
            ],
        ),
        treatment_limitations=[
            "Once shoot borer larvae are deeply entrenched within pseudostems, contact chemical sprays have low efficacy.",
            "Observe regional spice board regulations regarding allowable pesticide residue thresholds.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Treat seed rhizomes before storage by dipping in 0.1% bio-insecticide or neem oil",
                "Store seed rhizomes in cool, well-ventilated, shaded pits lined with sand",
            ],
            cultural_preventions=[
                "Avoid planting ginger adjacent to castor bean plots (a primary alternate host for Conogethes)",
                "Intercrop with non-host companion plants to disrupt pest search behavior",
            ],
            monitoring_schedule="Inspect pseudostems weekly from 60 days after planting until harvest",
        ),
        sources=[SOURCE_REGISTRY["SRC_LUCID_GINGER_WEEVIL"]],
    ),

    "plum__shot_hole": DiseaseRecord(
        id="plum__shot_hole",
        canonical_name="Plum Shot Hole (Coryneum Blight)",
        crop="plum",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Wilsonomyces carpophilus",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.TWIG, PlantPart.FLOWER],
        symptoms=[
            "Small round reddish-brown spots (1-3 mm) on young leaves with purple margins",
            "Necrotic tissue dries, shrinks, and falls completely out of the leaf, leaving clean round 'shot holes'",
            "Small purplish spots on fruit that develop rough, corky, raised scabs and fruit gumming",
            "Cankers on twigs that produce gummy exudate and kill surrounding buds",
        ],
        symptom_progression="Spores infect leaves in spring -> host forms abscission layer around spot -> center drops out -> twig cankers overwinter.",
        development_conditions="Prolonged wet weather (14-24 hours of moisture) and mild temperatures (15-22°C) during bud break and leaf emergence.",
        spread_transmission="Water-splashed conidia from infected twig cankers and blighted dormant buds.",
        infection_sources="Overwintering mycelium and spores in twig cankers and bud scales.",
        immediate_actions=[
            "Prune out dead, cankered twigs during dry winter or summer weather",
            "Avoid overhead irrigation that wets tree canopies",
            "Mark orchard blocks for vital dormant copper application in autumn at 50% leaf fall",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Canopy pruning for air penetration",
                    purpose="Open tree center to accelerate leaf drying and remove overwintering twig cankers.",
                    source_id="SRC_UC_IPM_PLUM_SHOT_HOLE",
                ),
                CulturalControl(
                    practice="Irrigation water management",
                    purpose="Use low-angle under-canopy sprinklers or drip to keep leaves completely dry.",
                    source_id="SRC_UC_IPM_PLUM_SHOT_HOLE",
                ),
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Fixed Copper or Bordeaux Mixture (10-10-100)",
                    application_method="Dormant spray applied at 50% autumn leaf fall and again before bud swell in spring.",
                    restrictions="Do NOT apply copper sprays after bud break as severe foliar phytotoxicity and defoliation will occur.",
                    source_id="SRC_UC_IPM_PLUM_SHOT_HOLE",
                ),
                ChemicalControl(
                    active_ingredient="Chlorothalonil or Captan",
                    application_method="Foliar protectant spray applied at petal fall and shuck-split if wet weather persists.",
                    restrictions="Follow strict pre-harvest intervals (PHI). Rotate chemical classes. Comply with local pesticide regulations.",
                    source_id="SRC_UC_IPM_PLUM_SHOT_HOLE",
                ),
            ],
            immediate_actions=[
                "Prune out gummy twig cankers during dry weather",
                "Ensure under-canopy irrigation only",
            ],
        ),
        treatment_limitations=[
            "Shot-hole perforations on leaves cannot heal; dormant sprays are the single most effective control.",
            "Never spray copper onto plum foliage during the growing season.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Collect and burn or bury all pruned cankered twigs and mummified fruit",
                "Disinfect pruning loppers with 10% bleach between trees",
            ],
            cultural_preventions=[
                "Plant plum cultivars with lower susceptibility to Coryneum blight",
                "Maintain balanced tree nutrition; avoid excessive nitrogen that promotes late lush growth",
            ],
            monitoring_schedule="Scout twigs in late winter and inspect new foliage weekly from bloom through shuck split",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_PLUM_SHOT_HOLE"]],
    ),

    "rose__black_spot": DiseaseRecord(
        id="rose__black_spot",
        canonical_name="Rose Black Spot",
        crop="rose",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Diplocarpon rosae",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FLOWER],
        symptoms=[
            "Circular black spots with characteristic feathery or fringed margins on the upper leaf surface",
            "Yellowing (chlorosis) developing around the black spots, spreading across the entire leaf blade",
            "Premature defoliation starting from the lower canopy and moving upward, leaving bare canes",
            "Raised dark purple or black blister-like cankers on young green canes",
        ],
        symptom_progression="Conidia germinate on wet leaves in 7 hours -> fringed black spots develop in 3-10 days -> ethylene causes yellowing and leaf abscission.",
        development_conditions="Warm temperatures (20-27°C) accompanied by continuous leaf wetness for at least 7 hours and high relative humidity.",
        spread_transmission="Water-splashed conidia from rain or overhead sprinkler irrigation.",
        infection_sources="Fallen diseased leaves and infected cane lesions over winter.",
        immediate_actions=[
            "Pick off and discard all infected leaves displaying black spots immediately",
            "Switch to ground-level watering with soaker hoses or drip lines; keep foliage completely dry",
            "Prune back green canes showing purple or black spot cankers to clean healthy wood",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Ground-level irrigation",
                    purpose="Water rose roots directly; eliminate splashing on leaves to halt spore germination.",
                    source_id="SRC_UC_IPM_ROSE_BLACK_SPOT",
                ),
                CulturalControl(
                    practice="Pruning for air circulation",
                    purpose="Prune bushes to an open vase habit so leaves dry in morning breezes.",
                    source_id="SRC_UC_IPM_ROSE_BLACK_SPOT",
                ),
            ],
            biological=[
                BiologicalControl(
                    agent="Neem Oil (1%) or Potassium Bicarbonate",
                    application_method="Foliar spray applied preventatively every 7-10 days during humid periods.",
                    source_id="SRC_UC_IPM_ROSE_BLACK_SPOT",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Myclobutanil (FRAC 3) or Tebuconazole or Chlorothalonil",
                    application_method="Foliar protectant and curative spray applied at 10-14 day intervals.",
                    restrictions="Rotate FRAC groups to prevent resistance. Do not apply oils when temperatures exceed 30°C. Comply with regional laws.",
                    source_id="SRC_UC_IPM_ROSE_BLACK_SPOT",
                )
            ],
            immediate_actions=[
                "Pick off and destroy infected leaves",
                "Ensure foliage stays dry during watering",
            ],
        ),
        treatment_limitations=[
            "Fungicides cannot erase existing black spots from foliage; yellowed leaves will inevitably drop.",
            "Adhere to personal protective equipment (PPE) guidelines on product labels.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Thoroughly rake and discard fallen rose leaves in autumn; never compost infected rose foliage",
                "Prune canes hard in late winter to remove all overwintered cane cankers",
            ],
            cultural_preventions=[
                "Plant black-spot-resistant rose cultivars (e.g. Knock Out, Oso Easy series)",
                "Position rose beds in full sun (6+ hours daily) with generous plant spacing",
            ],
            monitoring_schedule="Inspect lower leaves weekly starting with spring bud break",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_ROSE_BLACK_SPOT"]],
    ),

    "rose__downy_mildew": DiseaseRecord(
        id="rose__downy_mildew",
        canonical_name="Rose Downy Mildew",
        crop="rose",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Peronospora sparsa",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FLOWER],
        symptoms=[
            "Purplish-red to dark brown angular necrotic spots bounded strictly by leaf veins",
            "Sparse, delicate, pale grayish-white downy sporulation on the lower leaf surface under high humidity",
            "Rapid, catastrophic defoliation within days of symptom onset",
            "Purple-to-black longitudinal cankers on young canes and flower calyxes",
        ],
        symptom_progression="Sporangia infect leaves at cool temperatures -> purplish angular blocks develop -> rapid severe leaf drop in 48-72 hours.",
        development_conditions="Cool temperatures (15-20°C) with high relative humidity (>85%) and stagnant air; common in greenhouses and shaded gardens.",
        spread_transmission="Airborne sporangia and water splash.",
        infection_sources="Systemically infected dormant canes, infected nursery stock, and fallen leaves.",
        immediate_actions=[
            "Immediately isolate or rogue out severely defoliating rose bushes to protect surrounding stock",
            "Ventilate and heat greenhouses before sunset to reduce relative humidity below 85%",
            "Prune out symptomatic canes showing purple-red angular markings",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Humidity and temperature management",
                    purpose="Maintain greenhouse or tunnel relative humidity below 85% to block sporulation.",
                    source_id="SRC_UC_IPM_ROSE_DOWNY_MILDEW",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb or Fosetyl-Al or Mandipropamid (FRAC 40)",
                    application_method="Targeted preventative oomycete spray applied before cool, humid weather fronts.",
                    restrictions="Curative control is virtually impossible once systemic defoliation begins. Comply with regional chemical rules.",
                    source_id="SRC_UC_IPM_ROSE_DOWNY_MILDEW",
                )
            ],
            immediate_actions=[
                "Ventilate growing structures to reduce humidity",
                "Remove and bag fallen leaves immediately",
            ],
        ),
        treatment_limitations=[
            "Downy mildew progresses extremely rapidly; once defoliation begins, sprays only protect uninfected canes.",
            "Observe label PPE requirements and local agricultural extension guidelines.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Remove and incinerate all fallen rose leaves and blighted cane clippings",
                "Quarantine and inspect all incoming vegetative rose cuttings for 3 weeks",
            ],
            cultural_preventions=[
                "Provide wide bush spacing (minimum 1 meter) for rapid cross-ventilation",
                "Avoid overhead irrigation entirely",
            ],
            monitoring_schedule="Scout upper and lower leaves twice weekly during cool spring and autumn weather",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_ROSE_DOWNY_MILDEW"]],
    ),

    "rose__mosaic_virus": DiseaseRecord(
        id="rose__mosaic_virus",
        canonical_name="Rose Mosaic Virus Complex",
        crop="rose",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Prunus necrotic ringspot virus (PNRSV) / Apple mosaic virus (ApMV)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FLOWER],
        symptoms=[
            "Distinct bright yellow zig-zag, wavy lines, oak-leaf patterns, or watermarks on green leaves",
            "Yellow mosaic mottling and vein clearing without distorted or curled leaf margins",
            "Mild to severe stunting of bushes and reduced flower production",
            "Increased sensitivity of affected rose plants to winter freeze damage",
        ],
        symptom_progression="Systemic virus infection transmitted during vegetative propagation -> symptoms appear in spring on select canes -> persist indefinitely.",
        development_conditions="Symptoms are most vivid during cool spring weather and may fade or become masked during hot summer temperatures.",
        spread_transmission="Vegetative budding, grafting, and rootstock propagation. NOT transmitted by insects, pruning shears, or pollen.",
        infection_sources="Infected rootstocks (e.g. Dr. Huey, Manetti) and infected scion budwood.",
        immediate_actions=[
            "Mark and isolate symptomatic plants showing yellow wavy line patterns; do NOT take cuttings or budwood",
            "Provide optimal water, mulch, and balanced fertilizer to maintain plant vigor",
            "If severe stunting impairs garden aesthetics, rogue out the bush and replace with certified virus-indexed stock",
        ],
        treatment_category="no established cure",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Vigor maintenance and care",
                    purpose="Provide optimal soil fertility, mulching, and irrigation to help plants tolerate the virus.",
                    source_id="SRC_UC_IPM_ROSE_MOSAIC",
                ),
                CulturalControl(
                    practice="Propagation exclusion",
                    purpose="Never propagate, take cuttings, or bud from plants displaying mosaic patterns.",
                    source_id="SRC_UC_IPM_ROSE_MOSAIC",
                ),
            ],
            chemical=[],
            immediate_actions=[
                "Tag symptomatic plants; do not take vegetative cuttings",
                "Maintain optimal plant nutrition and mulching",
            ],
        ),
        treatment_limitations=[
            "No chemical spray, fungicide, or pesticide can cure plant viruses once established in vascular tissues.",
            "Do NOT apply chemical pesticides hoping to eliminate rose mosaic virus.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Rogue out and destroy severely stunted rose plants",
                "Purchase only certified virus-indexed (heat-treated) rose cultivars and rootstocks",
            ],
            cultural_preventions=[
                "Source rootstocks and budwood exclusively from certified clean plant programs",
            ],
            monitoring_schedule="Inspect spring vegetative flushes for yellow wavy line or watermark patterns",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_ROSE_MOSAIC"]],
    ),

    "rose__pest_damage": DiseaseRecord(
        id="rose__pest_damage",
        canonical_name="Rose Pest Damage (Aphids, Thrips, & Spider Mites)",
        crop="rose",
        pathogen_type=PathogenType.PEST,
        pathogen_name="Macrosiphum rosae (Rose Aphid) / Frankliniella occidentalis / Tetranychidae",
        affected_parts=[PlantPart.FLOWER, PlantPart.LEAF, PlantPart.SHOOT],
        symptoms=[
            "Dense clusters of soft-bodied green or pink aphids coating succulent new shoots and flower buds",
            "Distorted, stunted, curled leaves covered in sticky clear honeydew and black sooty mold",
            "Flower petals with brown, browning edges, deformed opening, and silver streaking (thrips feeding)",
            "Fine stippling and yellow speckling on upper leaf surfaces with delicate webbing on undersides (spider mites)",
        ],
        symptom_progression="Pest populations explode on tender spring flushes -> sap-feeding drains plant carbohydrates -> sooty mold and petal necrosis develop.",
        development_conditions="Warm, dry conditions favor spider mites and thrips; moderate spring weather favors rapid aphid colonization.",
        spread_transmission="Wind drift, adult flight, and active crawling from adjacent landscape vegetation.",
        infection_sources="Weeds, surrounding garden shrubs, and overwintering eggs on rose stems.",
        immediate_actions=[
            "Dislodge aphid colonies from tender shoot tips with a strong blast of water from a garden hose",
            "Prune off heavily distorted flower buds harboring thrips colonies and dispose of in trash",
            "Apply insecticidal soap or horticultural oil to coat leaf undersides thoroughly",
        ],
        treatment_category="curable",
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    practice="Water blast knockdown",
                    purpose="Knock aphids and mites off foliage with high-pressure water spray without chemicals.",
                    source_id="SRC_UC_IPM_ROSE_PESTS",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Insecticidal Soap or Neem Oil (1%)",
                    application_method="Foliar contact spray applied directly onto soft-bodied pests on leaf undersides.",
                    source_id="SRC_UC_IPM_ROSE_PESTS",
                ),
                BiologicalControl(
                    agent="Spinosad",
                    application_method="Targeted bio-insecticide spray applied to flower buds for thrips control.",
                    source_id="SRC_UC_IPM_ROSE_PESTS",
                ),
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Horticultural Mineral Oil or Acetamiprid",
                    application_method="Selective foliar spray when biological thresholds are exceeded.",
                    restrictions="Do not apply oils when temperatures exceed 30°C or within 30 days of sulfur sprays. Avoid spraying open blossoms during pollinator activity.",
                    source_id="SRC_UC_IPM_ROSE_PESTS",
                )
            ],
            immediate_actions=[
                "Dislodge aphids with a sharp water jet",
                "Apply insecticidal soap to leaf undersides",
            ],
        ),
        treatment_limitations=[
            "Insecticidal soaps and horticultural oils require direct contact with the target insect to be effective.",
            "Do not spray broad-spectrum pyrethroids on flowering roses to prevent bee and pollinator poisoning.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Prune dead shoots and weed hosts surrounding rose beds in early spring",
                "Wash dust off foliage periodically to discourage spider mite outbreaks",
            ],
            cultural_preventions=[
                "Avoid excessive high-nitrogen fertilizer which stimulates succulent aphid-attracting flushes",
                "Encourage beneficial predators (lady beetles, green lacewings, predatory mites, syrphid flies)",
            ],
            monitoring_schedule="Inspect tender shoot tips and flower buds twice weekly in spring and summer",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_ROSE_PESTS"]],
    ),

    "rose__powdery_mildew": DiseaseRecord(
        id="rose__powdery_mildew",
        canonical_name="Rose Powdery Mildew",
        crop="rose",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Podosphaera pannosa (syn. Sphaerotheca pannosa)",
        affected_parts=[PlantPart.LEAF, PlantPart.SHOOT, PlantPart.FLOWER],
        symptoms=[
            "White to grayish powdery fungal patches on young leaves, shoot tips, and flower pedicels",
            "Young infected leaves curl upward, distort, pucker, and may turn purplish-red beneath the white mildew",
            "Flower buds fail to open properly or produce distorted, stunted blooms",
            "Thick felt-like white mycelial pads forming on canes late in the growing season",
        ],
        symptom_progression="Airborne conidia germinate without free water -> superficial white powdery mycelium spreads -> shoot tips deform.",
        development_conditions="Warm, dry days (21-27°C) with cool, humid nights (90-99% RH); does NOT require free standing water on leaves to germinate.",
        spread_transmission="Wind-blown conidia carried over large distances.",
        infection_sources="Overwintering mycelium inside dormant buds and cleistothecia on infected canes.",
        immediate_actions=[
            "Prune off heavily coated, distorted shoot tips during routine garden deadheading",
            "Move containerized roses into full sunlight and areas with unobstructed air movement",
            "Apply potassium bicarbonate or horticultural oil at the very first sign of white powdery spots",
        ],
        treatment_category="curable",
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    practice="Sunlight and ventilation improvement",
                    purpose="Ensure 6+ hours of direct sunlight; powdery mildew conidia are killed by solar UV.",
                    source_id="SRC_UC_IPM_ROSE_POWDERY_MILDEW",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Potassium Bicarbonate (e.g. MilStop) or Horticultural Oil (1-2%)",
                    application_method="Foliar contact spray applied thoroughly over leaves and stems at first symptom detection.",
                    source_id="SRC_UC_IPM_ROSE_POWDERY_MILDEW",
                ),
                BiologicalControl(
                    agent="Bacillus amyloliquefaciens",
                    application_method="Preventative biofungicide spray applied every 7-10 days.",
                    source_id="SRC_UC_IPM_ROSE_POWDERY_MILDEW",
                ),
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Myclobutanil (FRAC 3) or Trifloxystrobin (FRAC 11) or Sulfur",
                    application_method="Systemic or protectant foliar spray applied at 10-14 day intervals.",
                    restrictions="NEVER apply sulfur within 30 days of any horticultural oil application to prevent severe leaf scorch. Adhere to label guidelines.",
                    source_id="SRC_UC_IPM_ROSE_POWDERY_MILDEW",
                )
            ],
            immediate_actions=[
                "Prune curled, powdery shoot tips",
                "Apply potassium bicarbonate or 1% horticultural oil",
            ],
        ),
        treatment_limitations=[
            "Curative systemic fungicides can arrest mycelium, but severely deformed leaves cannot uncurl.",
            "Do not spray oils or sulfur in hot weather (>32°C).",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Prune out infected cane tips during winter dormancy",
                "Rake and dispose of fallen rose debris",
            ],
            cultural_preventions=[
                "Select powdery-mildew-resistant rose varieties",
                "Avoid overhead shade and crowded plantings",
            ],
            monitoring_schedule="Inspect young shoot tips weekly during warm, dry spring and autumn days",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_ROSE_POWDERY_MILDEW"]],
    ),

    "rose__rust": DiseaseRecord(
        id="rose__rust",
        canonical_name="Rose Rust",
        crop="rose",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Phragmidium mucronatum",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM],
        symptoms=[
            "Bright orange, powdery pustules (uredinia) on the lower surface of leaves",
            "Small yellow-to-orange speckling on the corresponding upper leaf surface",
            "Severe premature defoliation leaving only young leaves at the shoot tips",
            "In autumn, orange pustules turn dark brown or black as overwintering teliospores develop",
        ],
        symptom_progression="Spring aeciospores infect leaves -> summer urediniospores multiply rapidly -> severe defoliation -> black teliospores overwinter.",
        development_conditions="Cool to mild temperatures (18-21°C) with continuous moisture (fog, dew, rain) for 2-4 hours.",
        spread_transmission="Wind-blown urediniospores and water splash.",
        infection_sources="Overwintering teliospores on fallen leaves and stem cankers.",
        immediate_actions=[
            "Handpick and destroy leaves displaying bright orange pustules on the underside",
            "Water roses at ground level early in the morning; keep foliage dry",
            "Collect and dispose of all fallen leaves beneath the rose bushes",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Foliage moisture elimination",
                    purpose="Ensure leaves remain dry through drip irrigation and wide bush spacing.",
                    source_id="SRC_UC_IPM_ROSE_RUST",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Bacillus subtilis",
                    application_method="Foliar biofungicide applied preventatively ahead of foggy or humid periods.",
                    source_id="SRC_UC_IPM_ROSE_RUST",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Myclobutanil (FRAC 3) or Mancozeb or Copper Hydroxide",
                    application_method="Foliar protectant and curative spray applied at 10-14 day intervals.",
                    restrictions="Rotate FRAC groups to prevent resistance. Adhere to PPE guidelines on pesticide labels.",
                    source_id="SRC_UC_IPM_ROSE_RUST",
                )
            ],
            immediate_actions=[
                "Handpick and discard leaves with orange pustules",
                "Avoid wetting foliage during irrigation",
            ],
        ),
        treatment_limitations=[
            "Rust pustules will not disappear from infected leaves; sprays protect new foliage from infection.",
            "Observe regional pesticide restrictions and PPE standards.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Perform hard dormant pruning in late winter to remove all overwintered stem lesions",
                "Thoroughly clean all fallen leaves before spring bud burst",
            ],
            cultural_preventions=[
                "Choose rust-tolerant rose cultivars",
                "Provide good airflow and open spacing around each bush",
            ],
            monitoring_schedule="Inspect lower leaf undersides weekly during cool, moist spring weather",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_ROSE_RUST"]],
    ),

    "spinach__anthracnose": DiseaseRecord(
        id="spinach__anthracnose",
        canonical_name="Spinach Anthracnose",
        crop="spinach",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Colletotrichum dematium / Colletotrichum spinaciae",
        affected_parts=[PlantPart.LEAF, PlantPart.PETIOLE],
        symptoms=[
            "Small, circular, water-soaked spots on leaves that rapidly turn tan, papery, or bleached white",
            "Tiny black spiny fungal fruiting structures (acervuli with setae) visible in the center of mature spots",
            "Lesions coalesce, causing large blighted holes, leaf tearing, and crown rot",
            "Unmarketable leafy greens with rapid postharvest decay and breakdown",
        ],
        symptom_progression="Conidia splash onto leaves -> necrotic papery spots expand -> acervuli form black central rings -> entire leaf collapses.",
        development_conditions="Warm, rainy, humid conditions (20-27°C) accompanied by overhead irrigation or frequent rainfall.",
        spread_transmission="Water-splashed conidia, farm equipment, workers walking through wet fields, and infected seed.",
        infection_sources="Infested seed, cruciferous/chenopodiaceous crop residues, and volunteer spinach plants.",
        immediate_actions=[
            "Do NOT harvest or walk through fields while spinach foliage is wet",
            "Rogue out and discard plants showing circular bleached leaf spots",
            "Switch to drip or furrow irrigation to eliminate overhead water splash",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Water splash elimination and drip irrigation",
                    purpose="Halt spore dissemination by eliminating overhead sprinkler droplets.",
                    source_id="SRC_UC_IPM_SPINACH_ANTHRACNOSE",
                ),
                CulturalControl(
                    practice="Crop rotation",
                    purpose="Rotate with non-host crops (corn, brassicas, beans) for at least 2-3 years.",
                    source_id="SRC_UC_IPM_SPINACH_ANTHRACNOSE",
                ),
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Azoxystrobin (FRAC 11) or Pyraclostrobin or Copper Hydroxide",
                    application_method="Foliar protectant spray applied at first sign of disease.",
                    restrictions="Strictly comply with pre-harvest intervals (PHI) on leafy greens to prevent chemical residues. Rotate FRAC groups.",
                    source_id="SRC_UC_IPM_SPINACH_ANTHRACNOSE",
                )
            ],
            immediate_actions=[
                "Cease overhead watering immediately",
                "Rogue out infected leaf patches during dry weather",
            ],
        ),
        treatment_limitations=[
            "Bleached circular spots on tender spinach leaves cannot be cured; affected leaves cannot be marketed.",
            "All chemical sprays must be legally registered for leafy greens in the grower's area.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Deep-plow or incorporate crop debris immediately following harvest",
                "Sanitize harvest bins, containers, and packing lines daily",
            ],
            cultural_preventions=[
                "Plant certified pathogen-free, hot-water-treated seed",
                "Ensure generous plant spacing and raised beds for soil drainage",
            ],
            monitoring_schedule="Scout spinach beds twice weekly from seedling stage through harvest",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_SPINACH_ANTHRACNOSE"]],
    ),

    "spinach__bacterial_spot": DiseaseRecord(
        id="spinach__bacterial_spot",
        canonical_name="Spinach Bacterial Leaf Spot",
        crop="spinach",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Pseudomonas syringae pv. spinaciae",
        affected_parts=[PlantPart.LEAF, PlantPart.PETIOLE],
        symptoms=[
            "Small water-soaked, angular spots on both upper and lower leaf surfaces",
            "Spots turn dark brown to black, often surrounded by a chlorotic yellow halo",
            "Lesions coalesce, producing large necrotic blighted areas and leaf distortion",
            "Severe loss of quality, unmarketable leafy greens, and rapid slime decay in bagged salad storage",
        ],
        symptom_progression="Bacteria enter leaf stomata or wounds -> angular water-soaked spots form -> spots turn dark brown and coalesce under wet conditions.",
        development_conditions="Cool, wet weather (12-20°C) with frequent rain, heavy dew, or overhead sprinkler irrigation.",
        spread_transmission="Water splash, wind-driven rain, handling wet foliage, and contaminated seed.",
        infection_sources="Contaminated seed, infected volunteers, and crop debris in soil.",
        immediate_actions=[
            "Cease all overhead sprinkler irrigation immediately",
            "Do NOT enter, cultivate, or harvest spinach when the canopy is wet",
            "Rogue out and bag diseased plants in early localized hot-spots",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Canopy moisture management",
                    purpose="Irrigate only via furrow or drip so leaves stay completely dry.",
                    source_id="SRC_UC_IPM_SPINACH_BACTERIAL_SPOT",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide or Copper Sulfate Pentahydrate",
                    application_method="Foliar protectant bactericide spray applied before predicted rain events.",
                    restrictions="Copper can cause phytotoxic speckling on tender spinach leaves in cool drying conditions. Observe pre-harvest intervals.",
                    source_id="SRC_UC_IPM_SPINACH_BACTERIAL_SPOT",
                )
            ],
            immediate_actions=[
                "Stop overhead sprinkling",
                "Avoid touching or harvesting wet plants",
            ],
        ),
        treatment_limitations=[
            "Bactericides have no curative activity once bacteria enter leaf tissue; preventative suppression only.",
            "Antibiotics are prohibited in vegetable production in most jurisdictions.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Thoroughly clean and sanitize harvest equipment and packing belts",
                "Plow under spinach crop residues promptly after final harvest",
            ],
            cultural_preventions=[
                "Plant only certified, lab-tested, pathogen-free seed",
                "Practice a 2-3 year rotation away from spinach, Swiss chard, and beets",
            ],
            monitoring_schedule="Scout fields twice weekly during cool, wet spring and autumn weather",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_SPINACH_BACTERIAL_SPOT"]],
    ),

    "spinach__downy_mildew": DiseaseRecord(
        id="spinach__downy_mildew",
        canonical_name="Spinach Downy Mildew",
        crop="spinach",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Peronospora effusa (syn. Peronospora farinosa f. sp. spinaciae)",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Pale yellow, irregular to angular chlorotic patches on the upper surface of leaves",
            "Dense, purplish-gray, felt-like sporulation coating the corresponding lower leaf surface",
            "Infected leaves curl, blister, pucker, and turn necrotic",
            "Total crop failure in commercial fields as even minor sporulation causes batch rejection",
        ],
        symptom_progression="Airborne sporangia infect leaves under cool moist conditions -> purple downy felt appears on undersides -> leaf blights completely.",
        development_conditions="Cool temperatures (8-18°C) accompanied by high relative humidity (>85%) and leaf wetness for 4-8 hours.",
        spread_transmission="Wind-blown sporangia carried for miles, and contaminated seed.",
        infection_sources="Overwintering oospores in soil, seedborne inoculum, volunteer spinach, and wild beet weeds.",
        immediate_actions=[
            "Disk or plow down severely infected spinach blocks immediately to prevent spore clouds blowing onto neighboring fields",
            "Avoid overhead irrigation; schedule all watering for early morning",
            "Apply targeted oomycete protectant fungicide if neighboring fields show initial mildew",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Moisture reduction and bed aeration",
                    purpose="Ensure wide row spacing to accelerate dew evaporation and lower canopy humidity.",
                    source_id="SRC_UC_IPM_SPINACH_DOWNY_MILDEW",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bio-protectants",
                    application_method="Foliar biofungicide applied prior to cool, humid periods.",
                    source_id="SRC_UC_IPM_SPINACH_DOWNY_MILDEW",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mandipropamid (FRAC 40) or Oxathiapiprolin (FRAC 49) or Fluopicolide",
                    application_method="Targeted oomycete protectant spray applied at first disease risk alert.",
                    restrictions="Strictly rotate FRAC modes of action to manage evolving physiological pathogen races. Follow label PHI.",
                    source_id="SRC_UC_IPM_SPINACH_DOWNY_MILDEW",
                )
            ],
            immediate_actions=[
                "Destroy heavily sporulating crop blocks immediately",
                "Ensure foliage dries before afternoon",
            ],
        ),
        treatment_limitations=[
            "Chemical sprays cannot cure leaves that already exhibit yellow patches and purple sporulation.",
            "Verify current race resistance ratings and local legal registrations.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Plow under residues deeply immediately following harvest",
                "Eradicate volunteer spinach plants along field edges",
            ],
            cultural_preventions=[
                "Plant spinach cultivars with multi-race genetic resistance (races 1-19)",
                "Use certified disease-free, tested seed lots",
            ],
            monitoring_schedule="Scout leaf undersides twice weekly during cool spring and autumn seasons",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_SPINACH_DOWNY_MILDEW"]],
    ),

    "spinach__pest_damage": DiseaseRecord(
        id="spinach__pest_damage",
        canonical_name="Spinach Pest Damage (Leafminers & Crown Mites)",
        crop="spinach",
        pathogen_type=PathogenType.PEST,
        pathogen_name="Liriomyza spp. (Leafminers) / Rhizoglyphus spp. / Myzus persicae (Aphids)",
        affected_parts=[PlantPart.LEAF, PlantPart.CROWN],
        symptoms=[
            "White to translucent winding serpentine mines carved inside leaf tissue by feeding maggots",
            "Stunted, deformed, crinkled young heart leaves caused by crown mite feeding in the central bud",
            "Yellowing, stippling, and sticky honeydew from green peach aphid colonies on leaf undersides",
            "Loss of cosmetic leafy green quality resulting in harvest rejection",
        ],
        symptom_progression="Adult flies/mites lay eggs in leaf tissue -> larvae feed internally creating winding tunnels -> pupate in soil.",
        development_conditions="Warm, dry temperatures favor rapid lifecycle turnover (14-21 days per generation).",
        spread_transmission="Adult fly flight, wind drift, and crawling from wild weed hosts.",
        infection_sources="Weeds bordering fields (chenopodium, nightshades) and soil with undecayed organic matter.",
        immediate_actions=[
            "Handpick and destroy mined leaves in small plantings to kill larvae inside mines",
            "Deploy yellow sticky cards around beds to trap and monitor adult fly flights",
            "Wash and spin harvested leaves to remove aphids and frass",
        ],
        treatment_category="curable",
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    practice="Physical removal of mined leaves",
                    purpose="Remove and dispose of mined leaves to kill larvae before they exit to pupate.",
                    source_id="SRC_UC_IPM_SPINACH_LEAFMINERS",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Spinosad (Entrust)",
                    application_method="Targeted translaminar bio-insecticide spray applied when mines first appear.",
                    source_id="SRC_UC_IPM_SPINACH_LEAFMINERS",
                ),
                BiologicalControl(
                    agent="Insecticidal Soap or Horticultural Oil (1%)",
                    application_method="Foliar contact spray applied to suppress aphid and mite populations.",
                    source_id="SRC_UC_IPM_SPINACH_LEAFMINERS",
                ),
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Cyromazine or Abamectin",
                    application_method="Translaminar insecticide spray applied according to economic thresholds.",
                    restrictions="Follow strict pre-harvest intervals on leafy greens. Protect natural parasitic wasp populations. Comply with local laws.",
                    source_id="SRC_UC_IPM_SPINACH_LEAFMINERS",
                )
            ],
            immediate_actions=[
                "Remove leaves with active winding mines",
                "Deploy yellow sticky cards for fly monitoring",
            ],
        ),
        treatment_limitations=[
            "Contact insecticides cannot reach leafminer larvae protected inside leaf tissue; only translaminar or biological products are effective.",
            "Strictly observe pre-harvest intervals (PHI) on baby greens.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Disk and incorporate crop residues immediately after harvest to disrupt pupation",
                "Keep field borders clean of broadleaf weed hosts",
            ],
            cultural_preventions=[
                "Conserve native parasitic wasps (Diglyphus isaea) which provide up to 90% natural biological control",
                "Use floating row covers to exclude adult flies from spring plantings",
            ],
            monitoring_schedule="Inspect 20 leaves per bed weekly for early winding mines and stippling",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_SPINACH_LEAFMINERS"]],
    ),

    "strawberry__angular_leaf_spot": DiseaseRecord(
        id="strawberry__angular_leaf_spot",
        canonical_name="Strawberry Angular Leaf Spot",
        crop="strawberry",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Xanthomonas fragariae",
        affected_parts=[PlantPart.LEAF, PlantPart.CALYX],
        symptoms=[
            "Small angular, water-soaked spots on the lower leaf surface, delineated strictly by minor veins",
            "When held up to light, spots appear translucent; under reflected light, they appear dark green",
            "Viscous bacterial exudate (ooze) drying into a whitish, scaly film on the lower leaf surface",
            "In severe infections, spots coalesce causing leaf blight and blackened, dry calyxes ('black cap') on fruit",
        ],
        symptom_progression="Bacteria enter leaf stomata under wet conditions -> angular water-soaked spots develop -> bacterial ooze dries into film -> calyxes blacken.",
        development_conditions="Moderate day temperatures (18-20°C) with cold nights (near freezing) and persistent rain or overhead sprinkler irrigation for frost protection.",
        spread_transmission="Water splash from overhead irrigation, rain, and infected nursery runners.",
        infection_sources="Infected nursery runner plants and overwintered strawberry crown tissue.",
        immediate_actions=[
            "Cease all non-essential overhead irrigation; use drip irrigation beneath plastic mulch",
            "Avoid harvesting, weeding, or moving through fields while plants are wet",
            "Rogue out and destroy infected transplants exhibiting blackened calyxes or water-soaked lesions",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Drip irrigation beneath plastic mulch",
                    purpose="Eliminate splashing water droplets that spread bacterial ooze from plant to plant.",
                    source_id="SRC_UC_IPM_STRAWBERRY_ANGULAR_SPOT",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide or Copper Sulfate Pentahydrate",
                    application_method="Foliar protectant bactericide spray applied before disease-favorable weather.",
                    restrictions="Caution: Repeated copper applications can cause phytotoxicity, stunting, and berry bronzing. Comply with local regulations.",
                    source_id="SRC_UC_IPM_STRAWBERRY_ANGULAR_SPOT",
                )
            ],
            immediate_actions=[
                "Stop overhead sprinkling",
                "Do not handle wet foliage",
            ],
        ),
        treatment_limitations=[
            "Bactericides cannot cure bacteria inside leaf tissue; excessive copper sprays cause severe foliar phytotoxicity.",
            "Antibiotics are not permitted for strawberry field disease control in most jurisdictions.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Inspect incoming runner plant shipments and reject lots with angular water-soaked leaf spots",
                "Sanitize harvest carts, trays, and field equipment regularly",
            ],
            cultural_preventions=[
                "Plant on raised, plastic-mulched beds with optimal soil drainage",
                "Select less susceptible strawberry cultivars where available",
            ],
            monitoring_schedule="Scout foliage and calyxes weekly, especially following frost protection sprinkling",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_STRAWBERRY_ANGULAR_SPOT"]],
    ),

    "strawberry__gray_mold": DiseaseRecord(
        id="strawberry__gray_mold",
        canonical_name="Strawberry Gray Mold (Botrytis Fruit Rot)",
        crop="strawberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Botrytis cinerea",
        affected_parts=[PlantPart.FRUIT, PlantPart.FLOWER, PlantPart.LEAF],
        symptoms=[
            "Soft, light brown, water-soaked rot starting under the calyx or on ripening strawberry fruit",
            "Berries become covered in a dense, velvety, grayish-tan coating of powdery fungal spores",
            "Infected flowers turn brown, die prematurely, and pass latent infection into young green receptacles",
            "Postharvest fruit turns into a soft, leaking, moldy mass within 48 hours at room temperature",
        ],
        symptom_progression="Spores infect flower petals during bloom -> remain latent in developing green fruit -> rot rapidly explodes as berry sugars rise at ripening.",
        development_conditions="Cool to mild temperatures (15-22°C) with continuous wetness (rain, dew, sprinkler) for 8+ hours during bloom.",
        spread_transmission="Wind-blown conidia, water splash, and direct contact with infected rotting berries.",
        infection_sources="Dead strawberry leaf residues, senescing petals, and mummified berries from previous seasons.",
        immediate_actions=[
            "Harvest ripe berries frequently (every 2-3 days) and handle fruit gently to prevent bruising",
            "Cull all moldy, rotting berries from the field; do NOT drop them into the row middles",
            "Cool harvested fruit to 0-2°C within 1-2 hours of picking to arrest Botrytis development",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Frequent harvest and field sanitation",
                    purpose="Remove decaying fruit and senescent leaves to eliminate spore inoculum sources.",
                    source_id="SRC_UC_IPM_STRAWBERRY_BOTRYTIS",
                ),
                CulturalControl(
                    practice="Plastic mulch and canopy aeration",
                    purpose="Keep fruit off bare wet soil and open canopy to promote rapid drying.",
                    source_id="SRC_UC_IPM_STRAWBERRY_BOTRYTIS",
                ),
            ],
            biological=[
                BiologicalControl(
                    agent="Bacillus amyloliquefaciens or Streptomyces lydicus",
                    application_method="Foliar biofungicide applied during 10% to 50% bloom stage.",
                    source_id="SRC_UC_IPM_STRAWBERRY_BOTRYTIS",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Captan / Cyprodinil + Fludioxonil (FRAC 9 + 12) / Fenhexamid (FRAC 17)",
                    application_method="Foliar protectant spray applied primarily during peak bloom (10-20% and 50-70% bloom).",
                    restrictions="Strictly rotate FRAC groups to prevent rapid Botrytis resistance. Comply with labeled pre-harvest intervals.",
                    source_id="SRC_UC_IPM_STRAWBERRY_BOTRYTIS",
                )
            ],
            immediate_actions=[
                "Cull and remove all gray moldy fruit from the field",
                "Chill harvested fruit immediately below 2°C",
            ],
        ),
        treatment_limitations=[
            "Fungicide sprays applied to ripe rotting fruit have zero curative effect; bloom protection is the single most critical intervention.",
            "Rotate chemical classes every application to preserve efficacy.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Remove dead senescing leaves from strawberry plants during spring cleanup",
                "Dispose of all culled fruit away from production fields",
            ],
            cultural_preventions=[
                "Plant on raised beds with black or white plastic mulch to keep fruit dry",
                "Avoid excessive nitrogen fertilization which produces dense, moisture-trapping foliage",
            ],
            monitoring_schedule="Scout blooms and developing fruit twice weekly during flowering and harvest",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_STRAWBERRY_BOTRYTIS"]],
    ),

    "strawberry__leaf_spot": DiseaseRecord(
        id="strawberry__leaf_spot",
        canonical_name="Strawberry Common Leaf Spot",
        crop="strawberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Mycosphaerella fragariae",
        affected_parts=[PlantPart.LEAF, PlantPart.CALYX, PlantPart.PETIOLE, PlantPart.RUNNER],
        symptoms=[
            "Small, deep purple to reddish-brown circular spots (3-6 mm) on the upper leaf surface",
            "Centers of the spots turn light tan to pure white, creating a characteristic 'bird's eye' appearance",
            "Spots on fruit (known as 'black seed') cause superficial dark sunken spots around individual achenes",
            "Severe infections cause leaves to yellow, wither, and drop prematurely, reducing plant vigor",
        ],
        symptom_progression="Spores germinate in wet film -> purple spots expand -> center blanches white with purple halo -> conidia splash to daughter plants.",
        development_conditions="Moderate temperatures (18-24°C) with persistent leaf wetness for 12+ hours and high relative humidity.",
        spread_transmission="Water-splashed conidia and wind-disseminated ascospores from overwintering perithecia.",
        infection_sources="Overwintered diseased strawberry leaves and infected runner transplant stock.",
        immediate_actions=[
            "Mow and remove older infected leaves during post-harvest field renovation",
            "Switch to drip irrigation to prevent water droplets splashing spores across rows",
            "Apply protectant fungicide if wet spring weather threatens new emerging foliage",
        ],
        treatment_category="manageable",
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    practice="Post-harvest renovation mowing",
                    purpose="Mow older diseased foliage just above crown level and remove debris to reduce inoculum.",
                    source_id="SRC_UC_IPM_STRAWBERRY_COMMON_LEAF_SPOT",
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Captan / Pyraclostrobin (FRAC 11) / Azoxystrobin",
                    application_method="Foliar protectant spray applied as new growth emerges in spring.",
                    restrictions="Rotate FRAC classes to mitigate resistance. Adhere to labeled pre-harvest intervals and PPE rules.",
                    source_id="SRC_UC_IPM_STRAWBERRY_COMMON_LEAF_SPOT",
                )
            ],
            immediate_actions=[
                "Remove and destroy spotted leaves during renovation",
                "Ensure foliage remains dry during watering",
            ],
        ),
        treatment_limitations=[
            "White bird's-eye leaf spots cannot be reversed; fungicide sprays protect newly emerging leaves and runners.",
            "Adhere to local agricultural pesticide regulations.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Rake, chop, or incorporate old foliage following harvest renovation",
                "Inspect planting stock and reject runner bundles displaying purple spots",
            ],
            cultural_preventions=[
                "Plant resistant strawberry cultivars (e.g. Chandler, Sweet Charlie, Allstar)",
                "Use raised beds with drip irrigation under plastic mulch",
            ],
            monitoring_schedule="Scout foliage bi-weekly starting with spring crown green-up",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_STRAWBERRY_COMMON_LEAF_SPOT"]],
    ),

    "strawberry__powdery_mildew": DiseaseRecord(
        id="strawberry__powdery_mildew",
        canonical_name="Strawberry Powdery Mildew",
        crop="strawberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Podosphaera aphanis (syn. Sphaerotheca macularis)",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.FLOWER],
        symptoms=[
            "Upward curling of leaf margins, exposing the purplish or reddish lower leaf surface",
            "Delicate white powdery mycelial patches coating the undersides of leaves",
            "Infected flowers turn brown, abort, or produce hard, deformed, unripened fruit",
            "Ripening fruit develops a powdery dull appearance with poor sugar development and off-flavors",
        ],
        symptom_progression="Airborne conidia germinate in humid air -> leaf margins cup upward -> white powdery fungal mats expand across leaves and fruit.",
        development_conditions="Dry days (18-27°C) with humid nights (75-98% RH); rampant in greenhouse and high-tunnel strawberry culture.",
        spread_transmission="Wind-blown conidia carried across fields and tunnels.",
        infection_sources="Overwintering mycelium in dormant strawberry crowns and infected runner plants.",
        immediate_actions=[
            "Increase high-tunnel and greenhouse side-wall ventilation to reduce stagnant relative humidity",
            "Inspect underside of upward-cupped leaves for white powdery mycelium",
            "Apply potassium bicarbonate or 1% horticultural oil at the earliest sign of upward leaf cupping",
        ],
        treatment_category="curable",
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    practice="Tunnel ventilation and humidity reduction",
                    purpose="Open tunnel end-walls and sides to lower nighttime relative humidity below 80%.",
                    source_id="SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW",
                )
            ],
            biological=[
                BiologicalControl(
                    agent="Potassium Bicarbonate or Horticultural Oil (1%)",
                    application_method="Foliar contact spray applied thoroughly to coat lower leaf surfaces.",
                    source_id="SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW",
                ),
                BiologicalControl(
                    agent="Bacillus amyloliquefaciens",
                    application_method="Preventative biofungicide applied at 7-10 day intervals.",
                    source_id="SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW",
                ),
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Myclobutanil (FRAC 3) or Quinoxyfen (FRAC 13) or Triflumizole",
                    application_method="Systemic foliar spray applied at first sign of leaf curling.",
                    restrictions="Strictly observe rotation of FRAC groups. NEVER apply horticultural oils within 14 days of sulfur. Comply with labeled PHI.",
                    source_id="SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW",
                )
            ],
            immediate_actions=[
                "Ventilate tunnels to reduce humidity",
                "Apply potassium bicarbonate or horticultural oil to leaf undersides",
            ],
        ),
        treatment_limitations=[
            "Severely deformed fruit cannot be cured and must be culled.",
            "Never apply oils when temperatures exceed 30°C to avoid leaf burn.",
        ],
        prevention=PreventionProtocol(
            sanitation_measures=[
                "Remove and destroy old infected leaves during post-harvest renovation",
                "Eradicate wild strawberry plants bordering commercial fields",
            ],
            cultural_preventions=[
                "Plant powdery-mildew-tolerant strawberry cultivars",
                "Maintain open plant spacing on raised beds to promote rapid airflow",
            ],
            monitoring_schedule="Scout leaf undersides weekly, especially in protected tunnel structures",
        ),
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_STRAWBERRY_POWDERY_MILDEW"]],
    ),
}

# Add missing crop records: Rose and Spinach
V3_EXTENDED_CROPS: dict[str, CropRecord] = {
    "rose": CropRecord(
        crop_id="rose",
        canonical_name="Rose",
        botanical_name="Rosa spp.",
        family="Rosaceae",
        optimal_ph="6.0 - 6.5",
        optimal_temp="18 - 25°C",
        watering_guidelines=[
            SourcedFact(
                statement="25-35 mm per week applied directly at soil base; avoid overhead foliage wetting.",
                source_ids=["SRC_UC_IPM_ROSE_BLACK_SPOT"],
            )
        ],
        common_diseases=[
            "rose__black_spot",
            "rose__powdery_mildew",
            "rose__downy_mildew",
            "rose__rust",
            "rose__mosaic_virus",
            "rose__pest_damage",
        ],
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_ROSE_BLACK_SPOT"]],
    ),
    "spinach": CropRecord(
        crop_id="spinach",
        canonical_name="Spinach",
        botanical_name="Spinacia oleracea",
        family="Amaranthaceae",
        optimal_ph="6.5 - 7.0",
        optimal_temp="15 - 20°C",
        watering_guidelines=[
            SourcedFact(
                statement="25-30 mm per week via drip or furrow irrigation; maintain uniform soil moisture.",
                source_ids=["SRC_UC_IPM_SPINACH_DOWNY_MILDEW"],
            )
        ],
        common_diseases=[
            "spinach__downy_mildew",
            "spinach__anthracnose",
            "spinach__bacterial_spot",
            "spinach__pest_damage",
        ],
        sources=[SOURCE_REGISTRY["SRC_UC_IPM_SPINACH_DOWNY_MILDEW"]],
    ),
}
