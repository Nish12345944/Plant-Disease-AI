"""
Authoritative Plant Pathology Knowledge: Solanaceous Crops (20 diseases)
- Bell Pepper: Bacterial Spot, Blossom End Rot, Frogeye Leaf Spot, Powdery Mildew
- Eggplant: Cercospora Leaf Spot, Phomopsis Fruit Rot, Phytophthora Blight
- Potato: Early Blight, Late Blight
- Tobacco: Blue Mold, Brown Spot, Frogeye Leaf Spot, Mosaic Virus
- Tomato: Bacterial Leaf Spot, Early Blight, Late Blight, Leaf Mold, Mosaic Virus, Septoria Leaf Spot, Yellow Leaf Curl Virus
Sources: Cornell University, UC IPM, Purdue Extension, NC State Extension, UF/IFAS, Penn State, USDA ARS.
"""

from knowledge.schema import (
    DiseaseRecord, PathogenType, PlantPart, TreatmentPlan,
    ChemicalControl, CulturalControl, BiologicalControl, PreventionProtocol
)
from knowledge.sources import (
    SOURCE_CORNELL, SOURCE_UC_IPM, SOURCE_PURDUE, SOURCE_NC_STATE,
    SOURCE_UF_IFAS, SOURCE_PENN_STATE, SOURCE_USDA_ARS, SOURCE_FAO
)

SOLANACEOUS_DISEASES = {
    "bell_pepper__bacterial_spot": DiseaseRecord(
        id="bell_pepper__bacterial_spot",
        canonical_name="Bell Pepper Bacterial Spot",
        crop="bell_pepper",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Xanthomonas euvesicatoria / X. vesicatoria / X. gardneri / X. perforans",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Small, water-soaked, dark green to brown spots on leaves, often surrounded by a narrow yellow halo",
            "Leaf spots turn dark brown to black and necrotic, causing leaves to turn yellow and drop prematurely (severe defoliation)",
            "Stem lesions are elongated, dark brown, and raised or corky",
            "Fruit lesions begin as small blister-like green spots that enlarge, become brown, rough, cracked, and crater-like"
        ],
        symptom_progression="Water-soaked spots -> dark necrotic spots with yellow halos -> severe defoliation exposing fruit -> rough warty fruit lesions.",
        development_conditions="High temperatures (24-30°C), frequent rains, high relative humidity, overhead irrigation, wet foliage.",
        spread_transmission="Wind-driven rain, splashing water, handling wet plants, contaminated seed, and infected transplants.",
        infection_sources="Contaminated seeds, infected volunteer solanaceous weeds, infected crop debris in soil.",
        immediate_actions=[
            "Avoid handling, cultivating, or harvesting plants when foliage is wet",
            "Apply copper bactericide tank-mixed with mancozeb at first sign of disease",
            "Sanitize tools and equipment between rows"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch from overhead sprinkler to drip irrigation, avoid working in wet foliage, and use raised plastic-mulched beds.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide + Mancozeb",
                    application_purpose="Protective contact tank mix bactericide/fungicide spray applied at 7-10 day intervals.",
                    limitations="Mancozeb enhances copper solubility and efficacy against copper-tolerant Xanthomonas strains; observe pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Acibenzolar-S-methyl (Actigard)",
                    application_purpose="Plant defense activator applied preventively to induce systemic acquired resistance (SAR).",
                    limitations="Apply only to healthy, actively growing transplants/plants before high disease pressure develops.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacteriophages (AgriPhage)",
                    application_method="Biological phage spray targeted specifically at Xanthomonas bacterial cells applied at dusk.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified disease-free, hot-water-treated seeds or certified transplants",
                "Select resistant pepper cultivars with multi-race resistance (Races 0-10)",
                "Rotate with non-solanaceous crops for a minimum of 2-3 years"
            ],
            sanitation_measures=[
                "Incorporate or destroy crop residues immediately after harvest to accelerate decomposition",
                "Eradicate solanaceous weeds (e.g., black nightshade) in and around fields"
            ],
            resistant_varieties="Aristotle, Vanguard, Declaration, Outsider, Playmaker (resistant to Xanthomonas races 1-5, 1-10)."
        ),
        similar_diseases=["bell_pepper__frogeye_leaf_spot", "tomato__bacterial_leaf_spot"],
        severity_indicators="Defoliation >30%, widespread blistered/corky fruit lesions, loss of canopy causing severe fruit sunscald.",
        sources=[SOURCE_UF_IFAS, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_CORNELL],
        quality_level="HIGH"
    ),

    "bell_pepper__blossom_end_rot": DiseaseRecord(
        id="bell_pepper__blossom_end_rot",
        canonical_name="Bell Pepper Blossom End Rot",
        crop="bell_pepper",
        pathogen_type=PathogenType.PHYSIOLOGICAL,
        pathogen_name="Calcium deficiency induced by irregular moisture supply / water stress (Physiological Disorder)",
        affected_parts=[PlantPart.FRUIT],
        symptoms=[
            "Water-soaked, soft, sunken lesion at or near the blossom end (or side) of the pepper fruit",
            "Lesion rapidly darkens, turning light tan to dark brown or black, becoming leathery, dry, and flat",
            "Secondary opportunistic saprophytes (e.g., Alternaria, Cladosporium) frequently colonize the dead necrotic patch, producing a black moldy coating",
            "Internal tissue under the lesion is dry, dark, and collapsed; seeds may darken prematurely"
        ],
        symptom_progression="Water-soaked spot on blossom end -> sunken leathery tan-to-black patch -> secondary black mold colonization -> unmarketable cull fruit.",
        development_conditions="Fluctuating soil moisture, drought stress followed by heavy watering, high transpiration rates in hot windy weather, excessive nitrogen (ammonium) fertilization, root damage.",
        spread_transmission="Non-infectious physiological disorder; does NOT spread from plant to plant or through pathogens.",
        infection_sources="Soil moisture fluctuations, poor calcium translocation in xylem under erratic watering or high vegetative vigor.",
        immediate_actions=[
            "Stabilize irrigation schedule to ensure consistent, uniform soil moisture levels",
            "Apply mulch around plant base to buffer soil moisture swings",
            "Remove and discard affected fruits so the plant diverts calcium to developing fruits",
            "Avoid high ammonium-nitrogen fertilizers that compete with calcium uptake"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Strip affected fruits from plants immediately to encourage new healthy fruit development.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            management=[
                CulturalControl(
                    description="Implement steady drip irrigation based on soil tensiometers, use organic/plastic mulch, and maintain soil pH between 6.2 and 6.8.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Calcium Chloride / Calcium Nitrate (Foliar)",
                    application_purpose="Foliar calcium spray applied to young developing fruitlets during periods of rapid growth and heat stress.",
                    limitations="Calcium moves poorly from leaves into fruit; foliar sprays supplement but cannot replace consistent root-zone moisture management.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Ensure consistent, adequate moisture through drip irrigation systems with soil moisture monitoring",
                "Soil test before planting and add agricultural lime or gypsum if calcium is deficient",
                "Avoid excessive nitrogen fertilization, particularly ammonium forms (use nitrate-N)",
                "Avoid deep root cultivation close to plants that damages feeder roots"
            ],
            sanitation_measures=[
                "Cull damaged fruit promptly"
            ],
            resistant_varieties="Cultivars with thicker fruit walls and deeper root systems show reduced susceptibility under stress."
        ),
        similar_diseases=["bell_pepper__sunscald", "bell_pepper__anthracnose"],
        severity_indicators="Sunken black leathery lesions at blossom end on >15% of fruit crop.",
        sources=[SOURCE_UF_IFAS, SOURCE_UC_IPM, SOURCE_PURDUE, SOURCE_CORNELL],
        quality_level="HIGH"
    ),

    "bell_pepper__frogeye_leaf_spot": DiseaseRecord(
        id="bell_pepper__frogeye_leaf_spot",
        canonical_name="Bell Pepper Frogeye Leaf Spot (Cercospora Leaf Spot)",
        crop="bell_pepper",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cercospora capsici",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Small, circular to oblong spots on leaves with light gray to whitish centers and prominent dark brown to reddish borders ('frogeye' look)",
            "Spots are surrounded by a distinct bright chlorotic yellow halo",
            "Spots enlarge up to 1 cm, coalesce, and cause extensive leaf chlorosis and severe defoliation",
            "Stems and fruit pedicels show elongated dark lesions; fruit may suffer sunscald following canopy loss"
        ],
        symptom_progression="Circular gray-centered spots with dark rings -> coalescing lesions -> widespread leaf yellowing and shedding -> severe defoliation.",
        development_conditions="Warm temperatures (24-30°C), high relative humidity (>80%), frequent rains or overhead watering.",
        spread_transmission="Conidia dispersed by wind currents, rain splash, and irrigation water.",
        infection_sources="Infected crop residues, solanaceous weeds, and contaminated seeds.",
        immediate_actions=[
            "Remove and destroy lower, heavily spotted leaves in small plantings",
            "Eliminate overhead irrigation to keep leaf surfaces dry",
            "Apply protective fungicides (e.g., copper, mancozeb, or azoxystrobin) at first symptom onset"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, ensure wide row spacing for canopy aeration, and maintain balanced fertility.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Broad-spectrum contact protectant fungicide applied at 7-14 day intervals.",
                    limitations="Preventive use only; observe pre-harvest intervals and resistance guidelines.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Pyraclostrobin",
                    application_purpose="Systemic strobilurin fungicide for foliar disease suppression.",
                    limitations="Rotate FRAC 11 with other fungicide groups to manage resistance.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free seed and transplants",
                "Rotate out of solanaceous crops for 2 years",
                "Use plastic mulch and drip irrigation to avoid soil splashing"
            ],
            sanitation_measures=[
                "Plow under or destroy crop debris thoroughly after harvest",
                "Eradicate solanaceous weed hosts"
            ],
            resistant_varieties="Cultivars with dense canopies and high general vigor show greater tolerance."
        ),
        similar_diseases=["bell_pepper__bacterial_spot", "tobacco__frogeye_leaf_spot"],
        severity_indicators="Extensive 'frogeye' lesions across canopy, defoliation >25%, sunscald on exposed pepper fruit.",
        sources=[SOURCE_UF_IFAS, SOURCE_NC_STATE, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "bell_pepper__powdery_mildew": DiseaseRecord(
        id="bell_pepper__powdery_mildew",
        canonical_name="Bell Pepper Powdery Mildew",
        crop="bell_pepper",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Leveillula taurica (anamorph Oidiopsis sicula / Oidiopsis taurica)",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Irregular, light green to bright yellow chlorotic patches on the upper leaf surface",
            "Fine, white, powdery fungal growth erupting on the corresponding lower leaf surface (underside)",
            "Leaf margins curl upward, infected leaves turn completely yellow, brown, and drop prematurely",
            "Severe defoliation exposes peppers to sunscald and sharply reduces yield, especially in warm, dry climates"
        ],
        symptom_progression="Upper leaf yellow patches -> white powdery growth on underside -> leaf rolling/curling -> rapid defoliation and fruit sunscald.",
        development_conditions="Warm temperatures (18-30°C), relative humidity fluctuations (high night humidity, dry days), greenhouse or arid field culture.",
        spread_transmission="Windborne conidia traveling through air currents; entry through stomata (endophytic fungus).",
        infection_sources="Infected older crops, greenhouse peppers/tomatoes, solanaceous weeds.",
        immediate_actions=[
            "Inspect underside of lower and middle canopy leaves for fine white powder",
            "Apply sulfur, potassium bicarbonate, or systemic powdery mildew fungicide",
            "Improve greenhouse ventilation and reduce humidity extremes"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Potassium Bicarbonate",
                    application_purpose="Contact curative eradicant to suppress sporulating colonies on leaf undersides.",
                    limitations="Requires high spray volume with targeted lower-canopy coverage.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            management=[
                CulturalControl(
                    description="Maintain greenhouse ventilation, avoid dense crowding, and remove heavily infected defoliating lower leaves.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Sulfur (Micronized / Dust)",
                    application_purpose="Standard preventive protectant fungicide for field and greenhouse peppers.",
                    limitations="Do not apply above 30°C or within 14 days of oil applications.",
                    source_id=SOURCE_UC_IPM.id
                ),
                ChemicalControl(
                    active_ingredient="Myclobutanil / Triflumizole",
                    application_purpose="Systemic DMI fungicide that penetrates leaf tissue to control endophytic mycelium.",
                    limitations="Rotate FRAC 3 with other mode-of-action groups; adhere to harvest intervals.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens",
                    application_method="Foliar bio-fungicide spray applied preventively.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Select powdery mildew-resistant pepper hybrids carrying the L-gene or polygenic resistance",
                "Ensure adequate air movement in greenhouses via horizontal airflow fans",
                "Avoid excessive vegetative fertilizer that creates dense shaded foliage"
            ],
            sanitation_measures=[
                "Thoroughly clean and sanitize greenhouse structures between crop cycles",
                "Remove solanaceous weeds around greenhouses"
            ],
            resistant_varieties="Resistant bell pepper hybrids: Magno, Striker, Bastan, Excursion."
        ),
        similar_diseases=["tomato__leaf_mold", "bell_pepper__bacterial_spot"],
        severity_indicators="Severe foliar curling and defoliation >30%, exposed sunscalded pepper fruit.",
        sources=[SOURCE_UC_IPM, SOURCE_UF_IFAS, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "eggplant__cercospora_leaf_spot": DiseaseRecord(
        id="eggplant__cercospora_leaf_spot",
        canonical_name="Eggplant Cercospora Leaf Spot",
        crop="eggplant",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cercospora melongenae / Cercospora solani-melongenae",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Small, circular to irregular chlorotic spots on leaves that expand to 4-10 mm in diameter",
            "Lesions develop grayish-white to tan centers with dark brown or purplish margins and concentric rings",
            "Underside of spots develops dark velvety spore masses under high humidity",
            "Severely infected leaves turn yellow, wither, and drop prematurely, causing defoliation and fruit sunscald"
        ],
        symptom_progression="Chlorotic spots -> concentric zoned gray/brown lesions -> extensive leaf chlorosis -> defoliation and yield loss.",
        development_conditions="Temperatures 25-32°C, relative humidity >85%, heavy rains, overhead irrigation, dense plantings.",
        spread_transmission="Airborne conidia and rain-splash dispersal.",
        infection_sources="Infected crop residues in soil, volunteer eggplant, solanaceous weeds.",
        immediate_actions=[
            "Prune out severely spotted lower leaves",
            "Switch to drip irrigation to keep canopy dry",
            "Apply protective fungicide (copper or mancozeb) at early disease detection"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Pruning lower leaves, trellising plants, and using drip irrigation to minimize canopy moisture.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb / Chlorothalonil",
                    application_purpose="Broad-spectrum contact protectant fungicide applied every 7-10 days in wet periods.",
                    limitations="Preventive application; observe pre-harvest intervals.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin",
                    application_purpose="Systemic foliar fungicide for Cercospora disease control.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free seed and transplants",
                "Practice a 2-3 year crop rotation away from solanaceous crops",
                "Maintain wide spacing (60-90 cm) between plants"
            ],
            sanitation_measures=[
                "Incorporate or destroy crop residues immediately post-harvest",
                "Sanitize stakes and trellising material"
            ],
            resistant_varieties="Cultivars with upright architecture and high vegetative vigor show improved field tolerance."
        ),
        similar_diseases=["eggplant__phomopsis_fruit_rot", "eggplant__phytophthora_blight"],
        severity_indicators="Defoliation >25%, extensive concentric leaf spots, exposed sun-damaged eggplant fruit.",
        sources=[SOURCE_UF_IFAS, SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_CORNELL],
        quality_level="HIGH"
    ),

    "eggplant__phomopsis_fruit_rot": DiseaseRecord(
        id="eggplant__phomopsis_fruit_rot",
        canonical_name="Eggplant Phomopsis Blight and Fruit Rot",
        crop="eggplant",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Phomopsis vexans (teleomorph Diaporthe vexans)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Seedlings develop dark brown cankers at the soil line causing damping-off and stem girdling",
            "Leaves develop circular to irregular, pale brown to gray necrotic spots with dark margins and abundant tiny black speck-like pycnidia",
            "Stems show elongated, dark, sunken cankers causing branches to wilt and snap",
            "Fruit develops large, sunken, circular, soft, pale brown rotten spots that rapidly engulf the fruit, studded with concentric rings of black pycnidia, ending in mummification"
        ],
        symptom_progression="Seedling cankers -> circular zoned leaf spots with black specks -> stem cankers -> massive soft fruit rot covered with black pycnidia -> fruit mummification.",
        development_conditions="Warm, humid, rainy weather (28-32°C), high humidity (>90%), splashing rain.",
        spread_transmission="Splashing rain, wind-blown rain, contaminated seed, infected tools.",
        infection_sources="Infected seed, crop residues persisting in soil for multiple years, solanaceous weeds.",
        immediate_actions=[
            "Remove and destroy all rotted fruit and cankered branches immediately",
            "Apply protective fungicides (copper, mancozeb, or chlorothalonil) to protect developing fruit",
            "Avoid overhead irrigation and working in wet foliage"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Sanitary removal and deep burial/burning of all blighted fruit and cankered stems.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            management=[
                CulturalControl(
                    description="Use plastic mulch to prevent soil splashing, stake plants to keep fruit off the ground, and use drip irrigation.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Contact protectant fungicide applied from flowering through fruit development.",
                    limitations="Preventive application; reapply following heavy rainfall; observe harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Protectant spray for foliar and fruit rot suppression.",
                    limitations="Preventive only; check for crop safety under high temperatures.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free, hot-water-treated seed",
                "Practice a minimum 3-year crop rotation with non-solanaceous crops",
                "Mulch with black plastic and stake plants to elevate canopy and fruit"
            ],
            sanitation_measures=[
                "Collect and destroy all crop residues and mummified fruits at season end",
                "Sanitize pruning knives and stakes"
            ],
            resistant_varieties="Florida Market, Florida Beauty, and Pant Samrat have shown varying levels of Phomopsis resistance."
        ),
        similar_diseases=["eggplant__phytophthora_blight", "eggplant__cercospora_leaf_spot"],
        severity_indicators="Soft sunken fruit rot with concentric black pycnidia on >15% of fruit, stem cankers causing shoot collapse.",
        sources=[SOURCE_UF_IFAS, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_CORNELL],
        quality_level="HIGH"
    ),

    "eggplant__phytophthora_blight": DiseaseRecord(
        id="eggplant__phytophthora_blight",
        canonical_name="Eggplant Phytophthora Blight and Crown Rot",
        crop="eggplant",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Phytophthora capsici",
        affected_parts=[PlantPart.ROOT, PlantPart.STEM, PlantPart.LEAF, PlantPart.FRUIT, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Sudden, permanent wilting and collapse of plants without initial yellowing",
            "Dark brown to black, water-soaked girdling lesions on the lower stem and crown at the soil line",
            "Leaves develop dark, water-soaked, irregular necrotic lesions that dry and become papery",
            "Fruit develops dark, water-soaked sunken lesions covered with white, powdered-sugar-like yeast-like sporangial growth, rapidly collapsing into a watery rot"
        ],
        symptom_progression="Crown water-soaking -> black girdling canker -> sudden whole-plant wilt -> fruit rotting with white powdered-sugar spore coating.",
        development_conditions="Excessive soil moisture, standing water, waterlogged low spots, warm temperatures (25-30°C), heavy rainfall.",
        spread_transmission="Swimming zoospores in surface water/irrigation run-off, splashing rain, contaminated soil on equipment.",
        infection_sources="Soilborne oospores surviving >5-10 years in soil, infested irrigation ponds, cull piles.",
        immediate_actions=[
            "Improve drainage immediately to eliminate standing water in fields",
            "Rogue out and destroy infected collapsing plants and rotten fruit",
            "Apply targeted oomycete fungicides to healthy surrounding plants"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Plant on high raised beds (20-25 cm), install tile or trench drainage, avoid recycling irrigation run-off water, and rotate crops.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Cyazofamid (Ranman) / Mandipropamid (Revus)",
                    application_purpose="Specialized oomycete fungicides applied as soil drench / directed crown and foliar spray.",
                    limitations="Preventive application; rotate FRAC groups (FRAC 21, 40, 43, 49) to manage resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Oxathiapiprolin + Mefenoxam (Orondis Gold)",
                    application_purpose="Systemic soil application at transplanting for early season crown and root rot suppression.",
                    limitations="Follow strict annual application limits and resistance management protocols.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Trichoderma harzianum",
                    application_method="Soil bio-fungicide amendment at planting to suppress Phytophthora inoculum.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant on dome-shaped raised beds covered with plastic mulch with good subsoil drainage",
                "Avoid planting in low-lying, poorly drained fields with a history of Phytophthora",
                "Practice a 3-4 year rotation with non-host crops (corn, brassicas, small grains)"
            ],
            sanitation_measures=[
                "Wash all tractors, tillage equipment, and boots before moving from infested to clean fields",
                "Never dump diseased fruit or cull piles near production fields"
            ],
            resistant_varieties="Commercial eggplant cultivars have limited Phytophthora resistance; strict water management is critical."
        ),
        similar_diseases=["eggplant__phomopsis_fruit_rot", "eggplant__verticillium_wilt"],
        severity_indicators="Sudden permanent plant wilt, black crown girdling, white powdered-sugar sporangial coating on rotten fruit.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_UF_IFAS, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "potato__early_blight": DiseaseRecord(
        id="potato__early_blight",
        canonical_name="Potato Early Blight",
        crop="potato",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Alternaria solani / Alternaria grandis",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.TUBER],
        symptoms=[
            "Small, dark brown to black spots appearing first on older, lower foliage",
            "Spots enlarge up to 1-2 cm, becoming restricted by large veins and developing distinct concentric rings ('target board' / 'bullseye' pattern)",
            "A narrow chlorotic yellow halo surrounds individual lesions; surrounding leaf tissue turns yellow and senesces",
            "Tuber lesions are dark, sunken, circular to irregular, with raised purplish-brown borders and a dry, corky, dark brown rot beneath the skin"
        ],
        symptom_progression="Target-board spots on lower leaves -> yellowing of leaves -> upward progression through canopy -> premature foliar defoliation -> tuber rot during storage.",
        development_conditions="Alternating wet and dry periods, warm temperatures (24-29°C), heavy dews, plant stress (nitrogen deficiency, nematode damage, heavy tuber bulking).",
        spread_transmission="Windborne conidia, rain splashing, machinery moving through fields.",
        infection_sources="Infected crop debris in soil, infected seed tubers, volunteer potatoes, solanaceous weeds.",
        immediate_actions=[
            "Maintain optimal plant nutrition (especially nitrogen and potassium) to prevent premature vine stress",
            "Avoid overhead irrigation in late afternoon/evening to reduce leaf wetness duration",
            "Initiate protective fungicide program when lower canopy spots appear or when P-Days threshold is reached"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Schedule irrigation for morning hours to allow rapid foliage drying; avoid moisture and nutrient stress during tuber bulking.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Broad-spectrum contact protectant fungicide applied at 7-10 day intervals during canopy closure.",
                    limitations="Preventive only; must be applied before infection penetrates leaf tissue; observe pre-harvest intervals.",
                    source_id=SOURCE_PENN_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Boscalid / Difenoconazole",
                    application_purpose="Translaminar / systemic fungicides for targeted early blight control during high disease pressure.",
                    limitations="Strict resistance management: rotate FRAC groups (FRAC 11, 7, 3) and tank-mix with contact protectants.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Foliar bio-fungicide applied preventively to protect expanding foliage.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified disease-free seed tubers",
                "Practice a minimum 2-3 year crop rotation with non-solanaceous crops (e.g., corn, wheat, legumes)",
                "Ensure balanced soil fertility; avoid nitrogen deficiency during bulking"
            ],
            sanitation_measures=[
                "Deep-till or destroy crop residue after harvest",
                "Allow tubers to fully mature and skin-set before harvesting to prevent bruising and tuber infection"
            ],
            resistant_varieties="Cultivars with medium to late maturity (e.g., Russet Burbank, Superior) show varying levels of tolerance compared to early-maturing cultivars."
        ),
        similar_diseases=["potato__late_blight", "potato__brown_spot_(alternaria_alternata)"],
        severity_indicators="Target-board lesions covering >30% of canopy, premature vine death, dark sunken corky tuber rot.",
        sources=[SOURCE_CORNELL, SOURCE_PENN_STATE, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "potato__late_blight": DiseaseRecord(
        id="potato__late_blight",
        canonical_name="Potato Late Blight",
        crop="potato",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Phytophthora infestans",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.TUBER, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Large, irregular, water-soaked pale to dark green lesions on leaves, rapidly turning dark brown to purplish-black",
            "Lesions expand rapidly with a pale yellowish-green chlorotic border",
            "In humid or wet conditions, a delicate, white, cottony/frosty fungal-like sporulation develops on the underside of leaves at the margin of lesions",
            "Stems develop dark brown to black greasy-looking lesions, becoming brittle and collapsing",
            "Tubers develop irregular, sunken, purplish-brown superficial skin patches with a granular, reddish-brown dry rot extending 5-15 mm into the flesh"
        ],
        symptom_progression="Water-soaked spots -> rapidly expanding black necrotic lesions with white underside mold -> stem collapse -> field-wide foul-smelling canopy destruction -> tuber rot in storage.",
        development_conditions="Cool, wet, foggy, or humid weather (temperatures 10-21°C, relative humidity >90%, continuous leaf wetness for >8-10 hours).",
        spread_transmission="Airborne sporangia carried for miles on wind currents; zoospores washed into soil infecting tubers; contaminated seed tubers.",
        infection_sources="Infected seed tubers, cull piles, volunteer potato plants, overwintered greenhouse tomatoes.",
        immediate_actions=[
            "Inspect field immediately following late blight weather alerts (BlightCast / BlightGuard)",
            "Apply targeted oomycete fungicides with translaminar/systemic activity immediately",
            "Destroy localized infection hotspots by vine burning, desiccation, or herbicide kill to protect the rest of the field",
            "Kill vines completely 2-3 weeks before harvest to prevent tuber infection during digging"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Cymoxanil (Curzate) + Protectant",
                    application_purpose="Kickback curative fungicide with 24-48 hours post-infection activity; must be tank-mixed with a protectant.",
                    limitations="Short residual (3-5 days); apply immediately upon early detection.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Destroy cull piles by freezing, burying (>1 m), or tarping; eliminate volunteer potatoes; monitor late blight forecasting systems.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb / Fluazinam",
                    application_purpose="Standard preventive contact protectant fungicides applied on 5-10 day schedules based on weather risk.",
                    limitations="Must be present on foliage prior to sporangia arrival; wash-off occurs with heavy rains.",
                    source_id=SOURCE_PENN_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Mandipropamid (Revus) / Cyazofamid (Ranman) / Oxathiapiprolin (Orondis)",
                    application_purpose="Translaminar and systemic anti-oomycete fungicides for high disease pressure and active canopy protection.",
                    limitations="Strict resistance management: alternate modes of action and tank-mix with multi-site protectants.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant used in organic production systems.",
                    limitations="Requires frequent reapplication and full canopy coverage; preventive only.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus subtilis / Bacillus amyloliquefaciens",
                    application_method="Foliar bio-fungicide for partial suppression under low-risk conditions.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified late blight-free seed tubers exclusively",
                "Eradicate all potato cull piles and volunteer potatoes before spring emergence",
                "Ensure generous hilling (ridge height) to create a soil barrier preventing sporangia from washing down to tubers",
                "Chemically or mechanically desiccate vines at least 14-21 days before harvest"
            ],
            sanitation_measures=[
                "Never leave unharvested or blighted tubers in the field",
                "Disinfect storage bins and grading equipment with quaternary ammonium or chlorine dioxide"
            ],
            resistant_varieties="Cultivars with late blight resistance genes: Defender, Elba, Jacqueline Lee, Mountain Gem Russet."
        ),
        similar_diseases=["potato__early_blight", "potato__blackleg_(pectobacterium)"],
        severity_indicators="Rapidly expanding black water-soaked lesions with white frosty sporulation on leaf underside, stem girdling, widespread canopy collapse.",
        sources=[SOURCE_CORNELL, SOURCE_PENN_STATE, SOURCE_PURDUE, SOURCE_UC_IPM, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "tobacco__blue_mold": DiseaseRecord(
        id="tobacco__blue_mold",
        canonical_name="Tobacco Blue Mold (Downy Mildew)",
        crop="tobacco",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Peronospora hyoscyami f. sp. tabacina (syn. Peronospora tabacina)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Circular, yellow chlorotic spots on the upper leaf surface",
            "Downy, bluish-gray to purplish velvety fungal-like sporulation on the lower surface of leaf spots in damp morning conditions",
            "Spots rapidly enlarge, become necrotic, turn light brown to bleached, and cause leaves to curl, puckered, and tear",
            "Systemic infection causes stem vascular browning, plant stunting, twisted distorted stalks, and plant death"
        ],
        symptom_progression="Yellow leaf spots -> bluish-gray velvety mold on underside -> rapid foliar browning and tearing -> systemic stem vascular necrosis and lodging.",
        development_conditions="Cool, overcast, wet weather (15-23°C), prolonged leaf wetness, cloudy days with low UV radiation.",
        spread_transmission="Windborne sporangia carried hundreds of miles on weather fronts; splashing rain and transplant trade.",
        infection_sources="Overwintered tobacco in southern areas/greenhouses, wild Nicotiana species, infected greenhouse float beds.",
        immediate_actions=[
            "Ventilate greenhouses and float beds to keep leaf surfaces dry",
            "Apply targeted oomycete fungicides immediately upon blue mold alert",
            "Destroy infected transplant beds to prevent field contamination"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Dimethomorph (Acrobat) + Mancozeb",
                    application_purpose="Translaminar anti-oomycete fungicide with post-infection curative activity applied at early detection.",
                    limitations="Must be tank-mixed with protectant; follow label resistance guidelines.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            management=[
                CulturalControl(
                    description="Greenhouse float-bed moisture control, high ventilation, rapid destruction of abandoned tobacco seedbeds.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb",
                    application_purpose="Protective contact multi-site fungicide for preventive nursery and field sprays.",
                    limitations="Preventive only; observe pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Cyazofamid / Mandipropamid",
                    application_purpose="Specialized oomycete fungicides for foliar blue mold protection.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Acibenzolar-S-methyl (Actigard)",
                    application_purpose="Systemic acquired resistance (SAR) inducer applied to healthy plants before infection.",
                    limitations="Do not apply to stressed plants; follow label timings.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free greenhouse float-bed transplants",
                "Ensure maximum greenhouse airflow and morning sun exposure",
                "Destroy all greenhouse float-bed plants immediately after transplanting is complete"
            ],
            sanitation_measures=[
                "Plow under tobacco stalks and roots immediately after harvest",
                "Eradicate wild tobacco and solanaceous weeds"
            ],
            resistant_varieties="Some cigar and burley cultivars possess partial resistance; chemical and sanitation management remain essential."
        ),
        similar_diseases=["tobacco__brown_spot", "tobacco__frogeye_leaf_spot"],
        severity_indicators="Bluish-gray downy sporulation on leaf underside, rapid foliar bleaching and collapse, systemic stalk necrosis.",
        sources=[SOURCE_NC_STATE, SOURCE_CORNELL, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "tobacco__brown_spot": DiseaseRecord(
        id="tobacco__brown_spot",
        canonical_name="Tobacco Brown Spot",
        crop="tobacco",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Alternaria alternata (tobacco pathotype)",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Small circular brown spots appearing first on lower, maturing, or senescing leaves",
            "Spots enlarge up to 2-3 cm, developing distinct dark brown concentric rings surrounded by a prominent bright yellow halo",
            "Centers of older lesions become thin, dry, papery, and often crack or drop out",
            "Lesions coalesce, causing large dead necrotic patches that destroy cured leaf quality and market value"
        ],
        symptom_progression="Small brown specks on lower leaves -> expanding concentric-ring spots with yellow halos -> leaf tearing and drying -> severe loss of cured leaf grades.",
        development_conditions="Warm, humid, rainy weather (24-30°C), ripening/senescing leaves, dense lush canopies, excessive nitrogen delaying maturity.",
        spread_transmission="Airborne conidia dispersed by wind and splashing rain.",
        infection_sources="Infected crop debris in soil, volunteer tobacco, alternate weed hosts.",
        immediate_actions=[
            "Harvest and cure ripe lower leaves promptly (timely priming)",
            "Avoid over-fertilizing with nitrogen to prevent delayed senescence",
            "Apply protective fungicide if disease develops early in the season"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Timely harvesting (priming) of mature leaves, balanced nitrogen fertilization, and good weed control.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb / Chlorothalonil",
                    application_purpose="Contact protectant fungicide applied when weather favors Alternaria spread.",
                    limitations="Observe pre-harvest intervals and pesticide residue limits on cured leaf.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin",
                    application_purpose="Foliar fungicide for brown spot suppression.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Practice a 2-year crop rotation with non-host crops (e.g., grass sod, corn, small grains)",
                "Apply recommended nitrogen rates based on soil test to avoid delayed leaf ripening",
                "Ensure proper row spacing and prompt topping/suckering"
            ],
            sanitation_measures=[
                "Plow down or destroy tobacco stalks immediately after final priming"
            ],
            resistant_varieties="Cultivars with moderate tolerance: NC 297, Speight 168, K 326 (varies by maturity group)."
        ),
        similar_diseases=["tobacco__frogeye_leaf_spot", "tobacco__blue_mold"],
        severity_indicators="Large zoned brown lesions with wide yellow halos covering >25% of harvestable leaf area.",
        sources=[SOURCE_NC_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "tobacco__frogeye_leaf_spot": DiseaseRecord(
        id="tobacco__frogeye_leaf_spot",
        canonical_name="Tobacco Frogeye Leaf Spot",
        crop="tobacco",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cercospora nicotianae",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Small, circular spots (2-10 mm) with a parchment-white to light gray center and a narrow, dark reddish-brown border ('frogeye')",
            "Spots may show a narrow, faint yellow chlorotic halo",
            "Tiny black specks (spore clusters) appear in the pale center during humid conditions",
            "Green spot symptom: latent infections appear as dark green blemishes on cured tobacco leaves during curing, degrading quality"
        ],
        symptom_progression="Circular white-centered spots -> dark border development -> coalescing spots -> leaf tearing -> 'green spot' blemish during leaf curing.",
        development_conditions="Warm, humid, rainy weather (25-30°C), heavy dews, crowded plant beds, shaded lower leaves.",
        spread_transmission="Airborne conidia and rain splash.",
        infection_sources="Infected crop debris in soil, contaminated seedbeds, weed hosts.",
        immediate_actions=[
            "Harvest and prime ripe lower leaves promptly",
            "Improve field and seedbed ventilation",
            "Apply protective fungicide if disease threatens upper valuable leaves"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Timely priming of lower leaves, good canopy aeration, and balanced fertilization.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb / Copper Hydroxide",
                    application_purpose="Contact protectant fungicide applied at early symptom onset.",
                    limitations="Observe pre-harvest intervals and label guidelines.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin",
                    application_purpose="Systemic strobilurin fungicide for Cercospora spot management.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free seed and sanitize greenhouse plant beds",
                "Practice a 2-year crop rotation with non-solanaceous crops",
                "Avoid excessive plant densities and ensure early weed control"
            ],
            sanitation_measures=[
                "Plow under crop stalks immediately after harvest"
            ],
            resistant_varieties="Cultivars with good field tolerance and upright growth habits reduce lower leaf shading."
        ),
        similar_diseases=["tobacco__brown_spot", "bell_pepper__frogeye_leaf_spot"],
        severity_indicators="Abundant parchment-white frogeye spots across multiple leaf tiers, green spot defects in cured leaves.",
        sources=[SOURCE_NC_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "tobacco__mosaic_virus": DiseaseRecord(
        id="tobacco__mosaic_virus",
        canonical_name="Tobacco Mosaic Virus (TMV)",
        crop="tobacco",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Tobacco mosaic virus (TMV, Tobamovirus)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Light green and dark green mottled mosaic pattern on leaves",
            "Young expanding leaves show blistering, puckering, bubbling, and severe distortion ('shoestringing')",
            "Stunted plant growth and shortened internodes, giving a bushy appearance",
            "Older leaves under hot sunny conditions may develop necrotic patches ('mosaic burn'), reducing leaf yield and quality"
        ],
        symptom_progression="Vein clearing on young leaves -> distinct dark/light green mosaic and blistering -> leaf distortion and stunting -> mosaic burn necrosis.",
        development_conditions="Warm temperatures, manual handling of plants, transplanting, weeding, topping, and suckering operations.",
        spread_transmission="Mechanically transmitted extremely easily through sap on hands, clothing, tools, and direct plant-to-plant contact; NOT insect-vectored; transmitted via tobacco products.",
        infection_sources="Contaminated hands/clothing of workers (especially tobacco users), manufactured tobacco products (cigarettes, chewing tobacco), infected crop residue, perennial solanaceous weeds.",
        immediate_actions=[
            "DO NOT touch healthy plants after touching symptomatic plants",
            "Rogue and bag infected plants carefully without brushing against adjacent healthy foliage",
            "Require all workers to wash hands in 20% non-fat dry milk solution or soapy water before entering fields"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Strict sanitation: workers must wash hands in milk solution (non-fat dry milk 20%) or soap/trisodium phosphate (TSP) before working; no tobacco use by field workers.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Trisodium Phosphate (TSP) / Non-fat Dry Milk Solution",
                    application_purpose="Tool and hand dip disinfectant to denature TMV virions during pruning, topping, and transplanting.",
                    limitations="For sanitation of tools and worker hands; NOT a plant spray.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant TMV-resistant tobacco cultivars carrying the N-gene (hypersensitive resistance)",
                "Prohibit the use of all tobacco products (smoking, chewing) in greenhouses and fields",
                "Dip hands frequently in 20% non-fat dry milk solution during transplanting, topping, and suckering"
            ],
            sanitation_measures=[
                "Disinfect greenhouse trays, benches, and tools with 10% bleach or TSP",
                "Plow under and thoroughly decompose stalks after harvest",
                "Eradicate perennial solanaceous weeds (horsenettle, groundcherry)"
            ],
            resistant_varieties="Many modern flue-cured and burley cultivars possess the N-gene resistance (e.g., NC 297, Speight 168, CC 35, KT 204LC)."
        ),
        similar_diseases=["tomato__mosaic_virus", "cucumber_mosaic_virus"],
        severity_indicators="Severe mosaic mottling, leaf blistering/distortion, mosaic burn necrosis, marked plant stunting.",
        sources=[SOURCE_NC_STATE, SOURCE_USDA_ARS, SOURCE_CORNELL],
        quality_level="HIGH"
    ),

    "tomato__bacterial_leaf_spot": DiseaseRecord(
        id="tomato__bacterial_leaf_spot",
        canonical_name="Tomato Bacterial Leaf Spot",
        crop="tomato",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Xanthomonas perforans / X. euvesicatoria / X. gardneri / X. vesicatoria",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT, PlantPart.FLOWER],
        symptoms=[
            "Small, water-soaked, circular to angular dark brown to black spots on leaves (1-3 mm)",
            "Lesions often have a greasy appearance and may develop a faint yellow halo; centers frequently dry and tear",
            "Severe leaf spotting leads to extensive chlorosis, blighting, and dramatic lower-canopy defoliation",
            "Flower pedicels develop spots causing blossom drop; fruit shows small, raised, black blister-like scabs that enlarge into brown, rough, sunken, cratered lesions"
        ],
        symptom_progression="Water-soaked specks -> angular dark greasy spots -> defoliation exposing fruit to sunscald -> blossom drop and rough cratered fruit scabs.",
        development_conditions="High temperatures (24-30°C), heavy rainfall, high humidity (>85%), wind-blown rain, overhead irrigation, wet foliage work.",
        spread_transmission="Wind-driven rain, splashing water, handling wet plants, contaminated seed, infected transplants.",
        infection_sources="Contaminated seed, infected transplants, volunteer tomato plants, infected solanaceous crop residues.",
        immediate_actions=[
            "Cease all cultivation, pruning, and harvesting while foliage is wet",
            "Apply copper bactericide tank-mixed with mancozeb or bacteriophage spray",
            "Sanitize pruning tools between plants with disinfectant"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Use drip irrigation under plastic mulch, stake and prune plants for airflow, and strictly avoid entering wet fields.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide + Mancozeb",
                    application_purpose="Standard tank mix protectant applied every 5-7 days during warm, rainy weather.",
                    limitations="Mancozeb enhances copper efficacy against copper-tolerant Xanthomonas; observe pre-harvest intervals.",
                    source_id=SOURCE_UF_IFAS.id
                ),
                ChemicalControl(
                    active_ingredient="Acibenzolar-S-methyl (Actigard)",
                    application_purpose="Plant defense activator to induce systemic acquired resistance (SAR).",
                    limitations="Apply only to vigorous, healthy plants before disease becomes widespread.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="AgriPhage (Bacteriophages)",
                    application_method="Targeted biological bacteriophage spray applied in late afternoon to avoid UV degradation.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free, hot-water-treated seed or certified greenhouse transplants",
                "Practice a 2-3 year crop rotation away from solanaceous crops",
                "Mulch with black plastic and stake plants to avoid soil splash"
            ],
            sanitation_measures=[
                "Disinfect greenhouse trays and stakes with 10% bleach or quaternary ammonium",
                "Incorporate crop residues immediately after harvest to speed decomposition"
            ],
            resistant_varieties="Breeding for multi-race resistance is ongoing; commercial varieties with resistance to specific Xanthomonas races exist."
        ),
        similar_diseases=["tomato__septoria_leaf_spot", "tomato__early_blight", "bell_pepper__bacterial_spot"],
        severity_indicators="Severe defoliation >30%, heavy blossom drop, crater-like scabby fruit lesions.",
        sources=[SOURCE_UF_IFAS, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_CORNELL],
        quality_level="HIGH"
    ),

    "tomato__early_blight": DiseaseRecord(
        id="tomato__early_blight",
        canonical_name="Tomato Early Blight",
        crop="tomato",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Alternaria linariae (formerly Alternaria solani)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Small, dark brown to black spots on oldest lower leaves, expanding up to 1-2 cm in diameter",
            "Lesions display distinct concentric rings creating a characteristic 'bullseye' / 'target board' pattern",
            "Tissue around spots turns bright yellow (chlorotic halo); leaves eventually yellow completely, wither, and drop",
            "Stem lesions are dark, sunken, concentric-ringed cankers ('collar rot' on seedlings); fruit develops large, sunken, leathery black spots with concentric rings at the stem end"
        ],
        symptom_progression="Target-board spots on lower leaves -> yellowing and defoliation advancing up plant -> collar rot on stems -> dark sunken leathery fruit rot at calyx end.",
        development_conditions="Warm temperatures (24-29°C), heavy dew, frequent rains, high humidity, plant stress (heavy fruit load, nitrogen deficiency).",
        spread_transmission="Windborne conidia, splashing water, machinery and worker clothing.",
        infection_sources="Infected tomato/potato residues in soil, volunteer solanaceous weeds, infected seed/transplants.",
        immediate_actions=[
            "Prune off heavily spotted lower leaves (bottom 30 cm) to improve airflow and remove inoculum",
            "Mulch soil beneath plants to prevent rain-splash from soil",
            "Apply protective or systemic fungicide upon first appearance of target spots"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Stake and prune indeterminate tomatoes, bottom-prune lower 30 cm of leaves, use drip irrigation, and apply plastic or straw mulch.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Broad-spectrum contact protectant fungicide applied at 7-10 day intervals.",
                    limitations="Preventive application; reapply following heavy rains; observe pre-harvest intervals.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Difenoconazole / Penthiopyrad",
                    application_purpose="Translaminar / systemic fungicides for targeted early blight suppression.",
                    limitations="Strict resistance management: rotate FRAC groups (FRAC 11, 3, 7) with multi-site protectants.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Organic protectant spray providing baseline fungal and bacterial suppression.",
                    limitations="Preventive only; ensure thorough coverage of lower leaf surfaces.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Foliar bio-fungicide applied preventively to protect expanding foliage.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified disease-free seeds and vigorous transplants",
                "Practice a minimum 2-3 year crop rotation away from solanaceous crops",
                "Stake, trellis, and mulch plants to isolate foliage from soil splash"
            ],
            sanitation_measures=[
                "Incorporate or destroy crop debris thoroughly at the end of the season",
                "Disinfect tomato stakes and cages between seasons"
            ],
            resistant_varieties="Cultivars with early blight resistance genes (e.g., Defiant PhR, Mountain Magic, Plum Regal, Iron Lady, Mountain Merit)."
        ),
        similar_diseases=["tomato__septoria_leaf_spot", "tomato__late_blight", "tomato__bacterial_leaf_spot"],
        severity_indicators="Target-board lesions ascending past mid-canopy, defoliation >35%, leathery stem-end fruit rot.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "tomato__late_blight": DiseaseRecord(
        id="tomato__late_blight",
        canonical_name="Tomato Late Blight",
        crop="tomato",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Phytophthora infestans",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Large, irregular, water-soaked pale to dark green lesions on leaves, rapidly turning dark brown to purplish-black",
            "In cool humid conditions, a delicate white frosty/cottony mold appears on the underside of leaf lesions",
            "Stems develop large, dark brown to black greasy-looking lesions, causing branches to become brittle and collapse",
            "Green and ripe fruits develop large, firm, greasy-looking, olive-brown to golden-brown wrinkled lesions with a rough surface, rendering fruit completely unmarketable"
        ],
        symptom_progression="Water-soaked leaf patches -> rapid purplish-black blight with white underside sporulation -> stem girdling -> greasy brown fruit rot -> total field collapse within days.",
        development_conditions="Cool, wet, humid, or foggy weather (temperatures 15-22°C, relative humidity >90%, free leaf moisture for >8 hours).",
        spread_transmission="Airborne sporangia carried for miles by wind currents and storm fronts; infected transplants.",
        infection_sources="Infected tomato transplants, volunteer potatoes/tomatoes, cull piles, overwintering greenhouse crops.",
        immediate_actions=[
            "Inspect plants immediately upon regional late blight forecast alert (USABlight)",
            "Apply targeted oomycete fungicides immediately if late blight is detected locally",
            "Rogue and bag severely infected plants immediately to prevent massive airborne sporangia release",
            "Harvest unblemished mature green fruit before rain events if late blight is present in the field"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Cymoxanil (Curzate) + Mancozeb",
                    application_purpose="Curative kickback anti-oomycete fungicide with 24-48 hours post-infection activity.",
                    limitations="Short residual activity; must be tank-mixed with a multi-site protectant.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Destroy infected cull piles, eliminate volunteer potatoes/tomatoes, track USABlight forecasting, and bag diseased plants during removal.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Standard multi-site preventive protectant applied every 5-7 days during high-risk weather.",
                    limitations="Preventive only; must be applied before spores land on leaves; observe pre-harvest intervals.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Mandipropamid (Revus) / Cyazofamid (Ranman) / Oxathiapiprolin (Orondis)",
                    application_purpose="Specialized systemic/translaminar anti-oomycete fungicides for high disease pressure.",
                    limitations="Strict resistance management: alternate FRAC groups and tank-mix with protectants.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic tomato systems.",
                    limitations="Preventive only; requires regular reapplication and complete canopy coverage.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens",
                    application_method="Foliar bio-fungicide for low-risk preventive management.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant late blight-resistant tomato cultivars carrying Ph-2 and Ph-3 resistance genes",
                "Use certified disease-free transplants; inspect incoming nursery stock carefully",
                "Ensure maximum plant spacing, trellising, and drip irrigation to minimize canopy wetness"
            ],
            sanitation_measures=[
                "Bag and destroy infected plants immediately upon confirmation",
                "Eliminate potato cull piles and volunteer solanaceous plants near fields"
            ],
            resistant_varieties="Highly resistant cultivars: Mountain Magic (Ph-2, Ph-3), Defiant PhR (Ph-2, Ph-3), Iron Lady (Ph-2, Ph-3), Plum Regal, Mountain Merit, Jasper."
        ),
        similar_diseases=["tomato__early_blight", "tomato__bacterial_leaf_spot", "potato__late_blight"],
        severity_indicators="Frosty white mold on lesion undersides, greasy stem lesions, large olive-brown firm fruit rot, rapid canopy collapse.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "tomato__leaf_mold": DiseaseRecord(
        id="tomato__leaf_mold",
        canonical_name="Tomato Leaf Mold",
        crop="tomato",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Passalora fulva (syn. Cladosporium fulvum / Fulvia fulva)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FLOWER, PlantPart.FRUIT],
        symptoms=[
            "Pale green to bright yellowish chlorotic spots with indistinct margins on the upper leaf surface",
            "Dense, velvety, olive-green to grayish-brown fungal sporulation on the corresponding lower leaf surface",
            "Infected leaves curl, wither, turn completely yellow-brown, and drop prematurely (severe defoliation starting from oldest lower leaves)",
            "Blossoms may abort; fruit occasionally develops a smooth, black, leathery stem-end rot"
        ],
        symptom_progression="Upper leaf yellow patches -> dense olive-brown velvety mold on underside -> leaf rolling and yellowing -> extensive lower canopy defoliation.",
        development_conditions="High relative humidity (>85%), moderate temperatures (21-24°C), greenhouse, high tunnel, or protected culture with poor air circulation.",
        spread_transmission="Airborne conidia, rain splash, greenhouse ventilation currents, worker clothing, and contaminated tools.",
        infection_sources="Overwintered conidia and sclerotia in greenhouse structures, crop residues in soil, infected seed.",
        immediate_actions=[
            "Increase greenhouse ventilation and run horizontal airflow fans to lower relative humidity below 85%",
            "Prune out heavily infected lower leaves and discard in closed bags",
            "Apply protective or translaminar fungicides targeting leaf mold"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Potassium Bicarbonate",
                    application_purpose="Contact curative spray to suppress active sporulating colonies on lower leaf surfaces.",
                    limitations="Direct spray contact on leaf undersides is mandatory.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Greenhouse climate control: heat and vent to reduce humidity below 85%, use horizontal airflow fans, prune lower leaves, and space plants generously.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Protective contact spray applied preventively in high tunnels and fields.",
                    limitations="Check greenhouse label registrations; observe pre-harvest intervals.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Cyflufenamid / Difenoconazole / Fluxapyroxad",
                    application_purpose="Systemic fungicides for effective leaf mold control during high humidity periods.",
                    limitations="Rotate FRAC groups to prevent fungal resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Broad-spectrum protectant for organic and conventional systems.",
                    limitations="Preventive application; ensure thorough lower-leaf coverage.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Preventive foliar bio-fungicide spray for greenhouse use.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant leaf mold-resistant greenhouse tomato cultivars carrying Cf resistance genes (Cf-1 through Cf-19)",
                "Maintain relative humidity strictly below 85% in greenhouses and high tunnels",
                "Use drip irrigation under mulch and prune lower canopy leaves for maximum ventilation"
            ],
            sanitation_measures=[
                "Disinfect greenhouse walls, plastic, and framing between crop cycles with quaternary ammonium or hydrogen peroxide",
                "Remove and bag all crop residues at harvest completion"
            ],
            resistant_varieties="Many modern greenhouse cultivars have Cf gene resistance (e.g., Rebelski, Foronti, Geronimo, Torero)."
        ),
        similar_diseases=["tomato__powdery_mildew", "tomato__early_blight"],
        severity_indicators="Olive-brown velvety sporulation covering leaf undersides across >40% of canopy, extensive defoliation.",
        sources=[SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "tomato__mosaic_virus": DiseaseRecord(
        id="tomato__mosaic_virus",
        canonical_name="Tomato Mosaic Virus (ToMV)",
        crop="tomato",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Tomato mosaic virus (ToMV, Tobamovirus)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Light and dark green mottled mosaic pattern on leaves",
            "Leaves become distorted, puckered, blistered, or extremely narrow ('shoestring' or 'fern-leaf' symptom)",
            "Plant stunting, shortened internodes, and poor fruit set",
            "Fruit exhibits internal brown necrosis ('brown wall'), uneven ripening, yellow blotches, and brown necrotic rings"
        ],
        symptom_progression="Vein clearing -> mottled light/dark green mosaic -> leaf puckering and fern-leaf narrowing -> internal brown fruit wall necrosis.",
        development_conditions="Warm temperatures, manual handling of plants during pruning, trellising, sucker removal, and harvesting.",
        spread_transmission="Mechanically transmitted with extreme ease via sap on hands, clothing, pruning shears, stakes, and root-to-root contact; seedborne; transmitted by tobacco products.",
        infection_sources="Contaminated seeds, worker hands/clothing (especially tobacco users), contaminated pruning shears/stakes, infected crop residues in soil.",
        immediate_actions=[
            "Rogue out and destroy infected plants immediately without touching neighboring plants",
            "Wash hands and dip tools in 20% non-fat dry milk solution or 10% trisodium phosphate (TSP)",
            "Prohibit worker tobacco use around greenhouses and fields"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Strict sanitation: workers dip hands and tools in 20% non-fat dry milk solution before and between handling plants; no tobacco use in production areas.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Trisodium Phosphate (TSP) / Non-fat Dry Milk Solution",
                    application_purpose="Decontamination dip for tools, stakes, and worker hands to inactivate viral particles.",
                    limitations="Sanitation agent only; do NOT spray directly as a plant treatment.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant ToMV-resistant tomato varieties carrying the Tm-2 or Tm-2^2 resistance gene",
                "Use certified disease-free, bleach- or heat-treated seed",
                "Dip hands in milk solution every 20-30 minutes during pruning and trellising"
            ],
            sanitation_measures=[
                "Steam or disinfect greenhouse potting media and sanitize seedling trays",
                "Incorporate or remove crop residues immediately post-harvest",
                "Eradicate solanaceous weeds"
            ],
            resistant_varieties="Most modern commercial hybrid tomatoes carry Tm-2^2 resistance (e.g., Mountain Merit, Celebrity, Big Beef, Defiant PhR)."
        ),
        similar_diseases=["tobacco__mosaic_virus", "cucumber_mosaic_virus", "tomato__spotted_wilt_virus"],
        severity_indicators="Severe mosaic distortion, fern-leaf deformation, internal brown fruit wall necrosis, stunted unproductive plants.",
        sources=[SOURCE_CORNELL, SOURCE_UC_IPM, SOURCE_PURDUE, SOURCE_NC_STATE],
        quality_level="HIGH"
    ),

    "tomato__septoria_leaf_spot": DiseaseRecord(
        id="tomato__septoria_leaf_spot",
        canonical_name="Tomato Septoria Leaf Spot",
        crop="tomato",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Septoria lycopersici",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.PETIOLE, PlantPart.CALYX],
        symptoms=[
            "Numerous small, circular spots (2-4 mm) appearing first on older lower leaves near the ground",
            "Lesions have distinctive ash-gray to tan centers surrounded by a narrow, dark brown border and a narrow yellow halo",
            "Tiny, black, pimple-like fruiting bodies (pycnidia) are clearly visible in the pale center of mature spots under magnification",
            "Severely infected leaves turn yellow, wither, dry up, and drop, causing rapid upward defoliation and exposing fruit to severe sunscald"
        ],
        symptom_progression="Numerous tiny circular spots on lower leaves -> black pycnidia specks in gray centers -> yellowing and drying of leaves -> progressive upward defoliation.",
        development_conditions="Moderate to warm temperatures (20-26°C), high humidity, frequent rainfall, overhead irrigation, extended leaf wetness (>8 hours).",
        spread_transmission="Rain splash, wind-blown rain, overhead irrigation, workers handling wet plants.",
        infection_sources="Infected tomato/solanaceous crop debris surviving in soil for 2-3 years, volunteer tomatoes, solanaceous weeds (horsenettle, nightshade).",
        immediate_actions=[
            "Prune off heavily spotted lower leaves (bottom 30 cm) and discard immediately",
            "Avoid overhead watering and working in wet tomato rows",
            "Apply protective contact or systemic fungicide at first sign of lower leaf spotting"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Bottom-pruning (remove leaves below first fruit cluster), staking/caging for canopy aeration, applying plastic or straw mulch, and using drip irrigation.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Broad-spectrum contact protectant fungicide applied at 7-10 day intervals starting at transplant establishment.",
                    limitations="Preventive application; reapply following rain; observe pre-harvest intervals.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Pyraclostrobin / Difenoconazole",
                    application_purpose="Translaminar / systemic fungicides for effective foliar disease suppression.",
                    limitations="Rotate FRAC groups to prevent fungal resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic production systems.",
                    limitations="Preventive use only; requires frequent reapplication during wet weather.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Foliar bio-fungicide applied preventively.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free seeds and transplants",
                "Practice a minimum 2-3 year crop rotation away from solanaceous crops",
                "Apply organic or plastic mulch beneath plants to block soil splash"
            ],
            sanitation_measures=[
                "Incorporate or destroy crop debris thoroughly at the end of the season",
                "Disinfect tomato stakes and cages between seasons",
                "Eradicate solanaceous weeds around field perimeters"
            ],
            resistant_varieties="Cultivars with partial tolerance: Iron Lady, Mountain Magic, Jasper; chemical protection and sanitation remain key."
        ),
        similar_diseases=["tomato__early_blight", "tomato__bacterial_leaf_spot"],
        severity_indicators="High density of gray-centered spots with pycnidia, lower canopy defoliation >40%, severe sunscald on exposed fruit.",
        sources=[SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "tomato__yellow_leaf_curl_virus": DiseaseRecord(
        id="tomato__yellow_leaf_curl_virus",
        canonical_name="Tomato Yellow Leaf Curl Virus (TYLCV)",
        crop="tomato",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Tomato yellow leaf curl virus (TYLCV, Begomovirus)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FLOWER, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Upward curling, cupping, and crinkling of leaf margins (leaves become cup-shaped or spoon-like)",
            "Prominent chlorosis (yellowing) of leaf margins and interveinal areas of young leaves",
            "Leaves become noticeably reduced in size, thick, leathery, and brittle",
            "Severe plant stunting, erect bushy habit, shortened internodes, heavy flower abscission (blossom drop), and drastic reduction or complete loss of fruit yield"
        ],
        symptom_progression="Marginal yellowing on young leaves -> upward cupping and leaf reduction -> bushy stunted plant habit -> blossom drop -> zero marketable fruit production.",
        development_conditions="High populations and feeding activity of sweetpotato whiteflies (Bemisia tabaci, MEAM1/B and MED/Q biotypes) in warm/hot seasons.",
        spread_transmission="Persistently transmitted by the whitefly Bemisia tabaci; NOT transmitted mechanically by sap, seed, or tools.",
        infection_sources="Infected tomato, pepper, bean, or weed hosts (nightshades, mallows), whitefly populations moving from older crops.",
        immediate_actions=[
            "Rogue out and destroy infected symptomatic plants immediately to remove virus reservoirs",
            "Apply systemic insecticides or insecticidal soaps/oils targeted at whitefly adults and nymphs",
            "Install yellow sticky cards to monitor whitefly vector populations"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Immediate roguing of infected plants, deploying reflective silver/metallized mulch, whitefly exclusion netting (50 mesh), and maintaining host-free periods.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Dinotefuran / Imidacloprid / Thiamethoxam",
                    application_purpose="Systemic neonicotinoid soil drench or drip application at transplanting for early-season whitefly suppression.",
                    limitations="Follow strict pollinator protection guidelines and annual application limits.",
                    source_id=SOURCE_UF_IFAS.id
                ),
                ChemicalControl(
                    active_ingredient="Cyantraniliprole / Spiromesifen / Pyriproxyfen",
                    application_purpose="Targeted foliar insecticides for whitefly adult and nymph management.",
                    limitations="Rotate modes of action (IRAC groups 28, 23, 7C, 4A) to manage insecticide resistance.",
                    source_id=SOURCE_UC_IPM.id
                ),
                ChemicalControl(
                    active_ingredient="Insecticidal Soap / Horticultural Oil",
                    application_purpose="Contact sprays to smother whitefly nymphs and reduce adult feeding.",
                    limitations="Requires complete coverage of lower leaf surfaces.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Encarsia formosa / Eretmocerus eremicus",
                    application_method="Parasitic wasps released in greenhouses for biological whitefly control.",
                    source_id=SOURCE_UC_IPM.id
                ),
                BiologicalControl(
                    agent_name="Beauveria bassiana",
                    application_method="Entomopathogenic bio-insecticide spray targeted at whitefly nymphs.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant TYLCV-resistant tomato hybrids carrying Ty-1, Ty-2, or Ty-3 resistance genes",
                "Deploy reflective metallized (silver) mulch at planting to repel incoming whiteflies",
                "Enforce a 2-3 month regional crop-free period (tomato break) to break the whitefly-virus cycle"
            ],
            sanitation_measures=[
                "Destroy spent crop residues immediately by disking or spraying and bagging",
                "Eradicate alternate weed hosts (e.g., Malva, Solanum spp.) around field borders"
            ],
            resistant_varieties="Highly resistant cultivars: Mountain Merit, Invicta, Tycoon, Red Bounty, Grand Marshall, Tribute, Skyway."
        ),
        similar_diseases=["tomato__mosaic_virus", "tomato__yellow_leaf_curl_virus"],
        severity_indicators="Severe upward leaf cupping, margin yellowing, complete stunting, total flower drop with zero fruit set.",
        sources=[SOURCE_UF_IFAS, SOURCE_UC_IPM, SOURCE_PURDUE, SOURCE_NC_STATE],
        quality_level="HIGH"
    ),
}
