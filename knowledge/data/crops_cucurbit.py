"""
Authoritative Plant Pathology Knowledge: Cucurbit Crops (8 diseases)
- Cucumber: Angular Leaf Spot, Bacterial Wilt, Powdery Mildew
- Squash: Powdery Mildew
- Zucchini: Bacterial Wilt, Downy Mildew, Powdery Mildew, Yellow Mosaic Virus
Sources: Cornell University, UC IPM, Purdue Extension, NC State Extension, UF/IFAS, USDA ARS.
"""

from knowledge.schema import (
    DiseaseRecord, PathogenType, PlantPart, TreatmentPlan,
    ChemicalControl, CulturalControl, BiologicalControl, PreventionProtocol
)
from knowledge.sources import (
    SOURCE_CORNELL, SOURCE_UC_IPM, SOURCE_PURDUE, SOURCE_NC_STATE,
    SOURCE_UF_IFAS, SOURCE_USDA_ARS, SOURCE_FAO,
    SOURCE_NC_STATE_CUCURBIT_DOWNY_MILDEW, SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW,
    SOURCE_UC_IPM_CUCURBIT_ANGULAR_LEAF_SPOT, SOURCE_PNW_CUCUMBER_ANGULAR_LEAF_SPOT,
    SOURCE_UKY_CUCURBIT_ANGULAR_LEAF_SPOT,
    SOURCE_NC_STATE_CUCURBIT_ANTHRACNOSE, SOURCE_UC_IPM_CUCURBIT_ANTHRACNOSE,
    SOURCE_UKY_CUCURBIT_ANTHRACNOSE,
    SOURCE_UW_MADISON_CUCURBIT_BACTERIAL_WILT, SOURCE_PNW_CUCUMBER_BACTERIAL_WILT,
    SOURCE_UKY_CUCURBIT_BACTERIAL_WILT,
    SOURCE_UKY_CUCURBIT_BELLY_ROT,
    SOURCE_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT,
    SOURCE_MS_STATE_CUCURBIT_COTTONY_LEAK, SOURCE_UKY_CUCURBIT_COTTONY_LEAK,
    SOURCE_PNW_SQUASH_VIRUS_DISEASES, SOURCE_UC_IPM_CUCURBIT_POTYVIRUSES,
)

CUCURBIT_DISEASES = {
    "cucumber__angular_leaf_spot": DiseaseRecord(
        id="cucumber__angular_leaf_spot",
        canonical_name="Cucumber Angular Leaf Spot",
        crop="cucumber",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Pseudomonas syringae pv. lachrymans",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Small, water-soaked, angular lesions on leaves strictly bounded by veins",
            "Lesions turn tan to brown and dry out, frequently falling out to produce a 'shot-hole' appearance",
            "Under humid conditions, milky white bacterial exudate droplets ooze from lesions on the lower leaf surface and dry into a white crust",
            "Fruit lesions are small, circular, water-soaked, and crack open, allowing secondary soft-rot decay organisms to enter"
        ],
        symptom_progression="Water-soaked vein-delimited angular spots -> white crusty exudate on underside -> centers drop out leaving ragged holes -> fruit cracking and rot.",
        development_conditions="Temperatures 24-28°C, relative humidity >95%, frequent rain showers, overhead sprinkler irrigation, wet field work.",
        spread_transmission="Splashing rain, overhead irrigation, farm machinery, workers handling wet vines, and infected seed.",
        infection_sources="Contaminated seeds, infected crop residues in soil (survives 1-2 years), and volunteer cucurbits.",
        immediate_actions=[
            "Avoid entering or working in cucumber fields when foliage is wet",
            "Prune or remove severely diseased plants if localized",
            "Apply copper bactericide mixed with mancozeb for disease suppression"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Avoid overhead sprinkler irrigation; switch to drip irrigation to keep leaf surfaces dry.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide + Mancozeb",
                    application_purpose="Tank mix bactericide/fungicide protectant spray to reduce bacterial populations and secondary infection.",
                    limitations="Apply preventively before heavy rain events; monitor for copper phytotoxicity in hot dry weather.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Foliar preventive bio-bactericide spray to reduce leaf surface colonization.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free, hot-water or bleach-treated seed",
                "Practice a minimum 2-year crop rotation with non-cucurbit crops",
                "Ensure drip irrigation and plastic mulch to prevent soil splashing"
            ],
            sanitation_measures=[
                "Plow under or destroy crop residues immediately after harvest",
                "Disinfect harvesting shears and trellising stakes"
            ],
            resistant_varieties="Many modern slicing and pickling cucumber hybrids possess high resistance to angular leaf spot (e.g., Dasher II, Speedway, Raider)."
        ),
        similar_diseases=["cucumber__downy_mildew", "cucumber__anthracnose"],
        severity_indicators="More than 30% leaf area with ragged shot-holes, water-soaked fruit cracking, secondary soft rot.",
        sources=[
            SOURCE_UC_IPM_CUCURBIT_ANGULAR_LEAF_SPOT,
            SOURCE_PNW_CUCUMBER_ANGULAR_LEAF_SPOT,
            SOURCE_UKY_CUCURBIT_ANGULAR_LEAF_SPOT,
            SOURCE_CORNELL,
            SOURCE_NC_STATE,
            SOURCE_PURDUE,
        ],
        quality_level="HIGH"
    ),

    "cucumber__anthracnose": DiseaseRecord(
        id="cucumber__anthracnose",
        canonical_name="Cucumber Anthracnose",
        crop="cucumber",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Colletotrichum orbiculare",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Small, circular, water-soaked foliar spots that enlarge rapidly into circular brown-tan lesions up to 1-2 cm wide",
            "Lesions frequently develop shot-holes as brittle dead centers fall out",
            "Elongated, sunken water-soaked cankers on stems and petioles",
            "Circular, sunken, crater-like lesions on fruit that exude salmon-pink or orange gelatinous spore masses under humid conditions"
        ],
        symptom_progression="Water-soaked leaf flecks -> circular brown lesions with shot-holes -> sunken stem cankers -> sunken circular fruit rot with salmon-colored spore droplets.",
        development_conditions="Warm, humid weather (22-27°C) with frequent rain, morning dew, overhead sprinkler irrigation, and splash dispersal.",
        spread_transmission="Splashing rain, overhead irrigation, farm equipment, workers in wet fields, and infected seed.",
        infection_sources="Infected crop residue (survives 1-2 years in soil), volunteer cucurbits, and contaminated seed.",
        immediate_actions=[
            "Do not cultivate, spray, or harvest in cucumber fields when vines are wet",
            "Apply preventative broad-spectrum protectant fungicides (chlorothalonil or mancozeb)",
            "Cull and destroy visibly infected fruit immediately to prevent field spread"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Never work in wet fields; switch to drip irrigation under plastic mulch to prevent splash dispersal.",
                    source_id=SOURCE_NC_STATE_CUCURBIT_ANTHRACNOSE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil (Bravo) / Mancozeb",
                    application_purpose="Broad-spectrum protectant foliar spray applied prior to infection events.",
                    limitations="Apply preventively before rain; adhere to pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE_CUCURBIT_ANTHRACNOSE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin (Quadris) / Difenoconazole (Inspire Super)",
                    application_purpose="Translaminar and systemic fungicide for foliar and fruit anthracnose control.",
                    limitations="Rotate FRAC mode of action groups (FRAC 11 and FRAC 3) to prevent resistance.",
                    source_id=SOURCE_UC_IPM_CUCURBIT_ANTHRACNOSE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus subtilis / amyloliquefaciens",
                    application_method="Foliar bio-fungicide protectant spray to reduce fungal spore germination.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Practice a minimum 2 to 3-year crop rotation out of all cucurbit crops",
                "Use certified disease-free, fungicide-treated seed",
                "Ensure drip irrigation and trellising to keep foliage and fruit dry"
            ],
            sanitation_measures=[
                "Plow down or destroy infected vines immediately after harvest",
                "Disinfect harvesting crates and knives"
            ],
            resistant_varieties="Many commercial slicing and pickling cucumber hybrids carry genetic resistance to Colletotrichum orbiculare races 1 and 2."
        ),
        similar_diseases=["cucumber__angular_leaf_spot", "cucumber__belly_rot", "cucumber__gummy_stem_blight"],
        severity_indicators="Sunken crater fruit rot with pink gelatinous spore masses, extensive defoliation, stem girdling.",
        sources=[
            SOURCE_NC_STATE_CUCURBIT_ANTHRACNOSE,
            SOURCE_UC_IPM_CUCURBIT_ANTHRACNOSE,
            SOURCE_UKY_CUCURBIT_ANTHRACNOSE,
            SOURCE_NC_STATE,
            SOURCE_UC_IPM,
        ],
        quality_level="HIGH"
    ),

    "cucumber__bacterial_wilt": DiseaseRecord(
        id="cucumber__bacterial_wilt",
        canonical_name="Cucumber Bacterial Wilt",
        crop="cucumber",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Erwinia tracheiphila",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Initial wilting of individual leaves or single runner vines during the heat of the day, recovering slightly at night",
            "Wilting becomes permanent and progresses rapidly along the entire vine",
            "Vines turn dull dark green, shrivel, and die without preliminary yellowing",
            "Diagnostic vascular stringing: cutting a wilted stem and slowly drawing the two cut ends apart reveals fine, sticky, viscous bacterial threads"
        ],
        symptom_progression="Individual leaf wilt -> runner collapse -> systemic vine wilt -> plant death within days of first symptoms.",
        development_conditions="Presence of striped (Acalymma vittatum) or spotted (Diabrotica undecimpunctata) cucumber beetles; beetle feeding wounds.",
        spread_transmission="Vectored exclusively by cucumber beetles carrying bacteria in their digestive tracts and defecating/regurgitating into feeding wounds.",
        infection_sources="Overwintering adult cucumber beetles and infected wild perennial cucurbits.",
        immediate_actions=[
            "Conduct diagnostic sticky thread test to confirm bacterial wilt",
            "Rogue and destroy wilted plants immediately (they cannot be saved and serve as beetle feeding reservoirs)",
            "Apply targeted insecticide to control cucumber beetles immediately"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Immediate roguing of wilted plants and intense beetle vector suppression.",
                    source_id=SOURCE_UW_MADISON_CUCURBIT_BACTERIAL_WILT.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Acetamiprid / Bifenthrin",
                    application_purpose="Insecticide targeted at striped and spotted cucumber beetles from cotyledon stage to 5-leaf stage.",
                    limitations="Apply in late afternoon or evening when honeybees are not actively foraging to protect pollinators.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Kaolin Clay",
                    application_purpose="Particle film barrier applied to foliage to deter beetle feeding and oviposition.",
                    limitations="Must be reapplied after heavy rains to maintain full white protective coat.",
                    source_id=SOURCE_UW_MADISON_CUCURBIT_BACTERIAL_WILT.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Steinernema carpocapsae (Entomopathogenic nematodes)",
                    application_method="Soil drench to target and suppress cucumber beetle larvae in root zones.",
                    source_id=SOURCE_CORNELL.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Deploy floating row covers from seeding until flowering to physically exclude cucumber beetles",
                "Use yellow sticky traps and pheromone lures for early beetle detection",
                "Trap cropping with highly preferred cucurbit cultivars around field borders"
            ],
            sanitation_measures=[
                "Remove and burn wilted vines promptly",
                "Clear wild cucurbit weeds (e.g., wild burcucumber) from field borders"
            ],
            resistant_varieties="Cucumber cultivars show varying susceptibility; County Fair is reported to have tolerance/resistance."
        ),
        similar_diseases=["zucchini__bacterial_wilt", "cucumber__fusarium_wilt"],
        severity_indicators="Diagnostic bacterial strands stretching between cut stem sections, irreversible systemic vine collapse.",
        sources=[
            SOURCE_UW_MADISON_CUCURBIT_BACTERIAL_WILT,
            SOURCE_PNW_CUCUMBER_BACTERIAL_WILT,
            SOURCE_UKY_CUCURBIT_BACTERIAL_WILT,
            SOURCE_PURDUE,
            SOURCE_CORNELL,
            SOURCE_NC_STATE,
        ],
        quality_level="HIGH"
    ),

    "cucumber__belly_rot": DiseaseRecord(
        id="cucumber__belly_rot",
        canonical_name="Cucumber Belly Rot",
        crop="cucumber",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Rhizoctonia solani",
        affected_parts=[PlantPart.FRUIT],
        symptoms=[
            "Water-soaked, yellowish-brown to dark brown discoloration on the underside ('belly') of cucumber fruit touching the ground",
            "Lesions become sunken, dry, irregular, and crater-like or cracked as they expand",
            "Dense brown crusty mold or web-like fungal mycelium developing over the rotted area under humid conditions",
            "Fruit rot remains predominantly on the lower rind surface without immediately turning internal fruit mushy"
        ],
        symptom_progression="Superficial yellowish-brown rind discoloration -> water-soaked sunken crater lesion -> cracked corky surface with brown fungal webbing -> postharvest cull.",
        development_conditions="Warm soil temperatures (25-32°C), high humidity, heavy rainfall, prolonged 24+ hour fruit-to-soil contact.",
        spread_transmission="Direct contact with soilborne fungal sclerotia and hyphae in infested field soil; splash dispersal during heavy rains.",
        infection_sources="Soilborne sclerotia surviving in soil, infested crop residues, and weed hosts.",
        immediate_actions=[
            "Cull affected fruit at harvest to avoid contaminating packing bins and grading lines",
            "Install plastic mulch or trellis vines to keep developing cucumbers off wet bare soil",
            "Avoid overhead irrigation that pools water around fruit-soil contact zones"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Keep developing fruit off bare soil using plastic mulch, straw barriers, or vertical trellising; maintain adequate plant spacing for soil drying.",
                    source_id=SOURCE_UKY_CUCURBIT_BELLY_ROT.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Azoxystrobin (Quadris)",
                    application_purpose="Directed soil/lower canopy protectant spray at vine tip over or early fruiting to suppress Rhizoctonia fruit rot.",
                    limitations="Direct spray beneath foliage to cover soil and fruit; rotate FRAC 11 fungicides.",
                    source_id=SOURCE_UKY_CUCURBIT_BELLY_ROT.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Trichoderma harzianum (strain T-22)",
                    application_method="Soil bio-fungicide inoculation at transplanting to suppress soilborne Rhizoctonia inoculum.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Practice a minimum 3 to 4-year crop rotation with non-host crops (corn, small grains)",
                "Plant cucumbers on raised beds covered with black plastic mulch",
                "Ensure excellent field drainage to prevent standing puddles"
            ],
            sanitation_measures=[
                "Deep-plow crop residues after harvest to bury sclerotia below root zones",
                "Sanitize harvest totes and grading belts"
            ],
            resistant_varieties="Cucumber cultivars with tougher rinds and upright plant architecture show reduced belly rot incidence."
        ),
        similar_diseases=["cucumber__pythium_fruit_rot", "cucumber__anthracnose"],
        severity_indicators="Large sunken corky crater lesions on fruit underside, brown fungal webbing, rejection at processing grading.",
        sources=[
            SOURCE_UKY_CUCURBIT_BELLY_ROT,
            SOURCE_UC_IPM,
            SOURCE_PURDUE,
        ],
        quality_level="HIGH"
    ),

    "cucumber__gummy_stem_blight": DiseaseRecord(
        id="cucumber__gummy_stem_blight",
        canonical_name="Cucumber Gummy Stem Blight",
        crop="cucumber",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Stagonosporopsis cucurbitacearum",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Round to triangular or wedge-shaped tan-to-brown spots beginning at leaf margins and rapidly enlarging",
            "Water-soaked, cracked oval cankers on stems that exude a diagnostic amber or reddish-brown gummy sap",
            "Tiny, black speck-like fruiting bodies (pycnidia/pseudothecia) visible inside older dead stem and leaf lesions",
            "Fruit phase (black rot): circular sunken water-soaked spots with black fruiting bodies and internal dry rot"
        ],
        symptom_progression="Marginal leaf chlorosis/necrosis -> stem lesion with gummy amber exudate -> stem girdling and vine wilt -> black rot on fruit.",
        development_conditions="Warm temperatures (20-28°C), prolonged leaf wetness (>95% RH for 1-2 days), frequent rainfall or overhead irrigation.",
        spread_transmission="Airborne ascospores and water-splashed conidia from crop debris; seedborne transmission.",
        infection_sources="Infected crop residue (survives over 2 years), volunteer cucurbit vines, contaminated seed lots.",
        immediate_actions=[
            "Cease overhead irrigation immediately to reduce canopy wetness duration",
            "Prune or remove severely cankered vines with gummy exudate",
            "Apply systemic and protectant fungicide rotation (e.g., chlorothalonil + difenoconazole/cyprodinil)"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation under plastic mulch, ensure wide plant spacing for canopy aeration, and avoid wounding vines during field work.",
                    source_id=SOURCE_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil (Bravo WeatherStik)",
                    application_purpose="Broad-spectrum protectant base spray applied preventively at 7-day intervals.",
                    limitations="Apply before rain events; do not use with copper when weather is hot and dry.",
                    source_id=SOURCE_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT.id
                ),
                ChemicalControl(
                    active_ingredient="Difenoconazole + Cyprodinil (Inspire Super) / Fluopyram (Luna)",
                    application_purpose="Targeted systemic fungicides for active gummy stem blight suppression.",
                    limitations="Strictly rotate FRAC groups 3, 9, and 7 to prevent fungicide resistance.",
                    source_id=SOURCE_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Foliar bio-fungicide protectant spray to reduce leaf surface colonization.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Practice a strict 2 to 3-year crop rotation out of all cucurbit crops",
                "Use certified disease-free, tested seed lots",
                "Trellis slicing cucumbers to elevate vines above ground level"
            ],
            sanitation_measures=[
                "Destroy or deeply incorporate infected cucurbit debris immediately after final harvest",
                "Disinfect greenhouse transplant flats and propagation benches"
            ],
            resistant_varieties="Commercial cucumber cultivars show variable tolerance; select varieties with documented gummy stem blight tolerance."
        ),
        similar_diseases=["cucumber__anthracnose", "cucumber__angular_leaf_spot", "cucumber__bacterial_wilt"],
        severity_indicators="Amber gummy exudate oozing from cracked stem cankers, black pycnidia visible under hand lens, complete vine collapse.",
        sources=[
            SOURCE_UF_IFAS_CUCURBIT_GUMMY_STEM_BLIGHT,
            SOURCE_UF_IFAS,
            SOURCE_CORNELL,
            SOURCE_NC_STATE,
        ],
        quality_level="HIGH"
    ),

    "cucumber__pythium_fruit_rot": DiseaseRecord(
        id="cucumber__pythium_fruit_rot",
        canonical_name="Cucumber Pythium Fruit Rot (Cottony Leak)",
        crop="cucumber",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Pythium aphanidermatum",
        affected_parts=[PlantPart.FRUIT, PlantPart.STEM],
        symptoms=[
            "Water-soaked, dark green or brown soft rot initiating on the portion of the cucumber contacting wet soil",
            "Rapid softening and liquefaction of internal fruit tissues within 24-48 hours ('leak')",
            "Profuse, thick, brilliant white cottony mycelial growth blanketing the rotted fruit under warm, humid conditions",
            "Rotted fruit collapses completely into a watery mush, exuding liquid"
        ],
        symptom_progression="Water-soaked fruit lesion in contact with wet soil -> soft watery decay -> dense white cottony mycelium blanket -> complete fruit liquefaction.",
        development_conditions="High temperatures (28-35°C), saturated soils, waterlogged fields, poorly drained soils, prolonged fruit wetness.",
        spread_transmission="Motile zoospores swimming through free water in saturated soils; direct contact with mycelium in soil.",
        infection_sources="Oospores and mycelium surviving in soil, infested surface irrigation water, crop debris.",
        immediate_actions=[
            "Remove and destroy all rotting fruit showing cottony growth to prevent packing bin contamination",
            "Improve field drainage and eliminate standing water immediately",
            "Switch off surface or overhead irrigation to allow topsoil to dry"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Plant on raised plastic-mulched beds to elevate fruit above saturated soil; avoid harvest during or immediately after heavy rain.",
                    source_id=SOURCE_MS_STATE_CUCURBIT_COTTONY_LEAK.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mefenoxam (Ridomil Gold) / Metalaxyl",
                    application_purpose="Soil drench or band application targeted at oomycete root and fruit rot prevention.",
                    limitations="Apply at planting or early vine layby; observe rotational restrictions.",
                    source_id=SOURCE_MS_STATE_CUCURBIT_COTTONY_LEAK.id
                ),
                ChemicalControl(
                    active_ingredient="Cyazofamid (Ranman)",
                    application_purpose="Protectant foliar/ground spray directed at fruit and soil interface before heavy rain events.",
                    limitations="Preventive application only; rotate with other oomycete FRAC chemistry.",
                    source_id=SOURCE_UKY_CUCURBIT_COTTONY_LEAK.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Gliocladium virens / Trichoderma virens",
                    application_method="Soil bio-fungicide application to colonize rhizosphere and outcompete Pythium spp.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Install raised beds with black or silver plastic mulch to provide a physical barrier between fruit and soil",
                "Ensure laser-leveled fields or gentle slopes with excellent tile drainage",
                "Practice a 2 to 3-year rotation away from cucurbits and solanaceous crops"
            ],
            sanitation_measures=[
                "Rogue out water-soaked or cottony cucumbers prior to bin loading",
                "Disinfect dump tanks and wash water with chlorine or peroxyacetic acid"
            ],
            resistant_varieties="Select cucumber cultivars with firm rinds and strong field holding capacity."
        ),
        similar_diseases=["cucumber__belly_rot", "cucumber__anthracnose"],
        severity_indicators="Profuse white cottony fungal blanket over entire fruit, rapid liquefaction/leak, water-soaked collapse.",
        sources=[
            SOURCE_MS_STATE_CUCURBIT_COTTONY_LEAK,
            SOURCE_UKY_CUCURBIT_COTTONY_LEAK,
            SOURCE_UC_IPM,
            SOURCE_PURDUE,
        ],
        quality_level="HIGH"
    ),

    "cucumber__powdery_mildew": DiseaseRecord(
        id="cucumber__powdery_mildew",
        canonical_name="Cucumber Powdery Mildew",
        crop="cucumber",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Podosphaera xanthii (syn. Sphaerotheca fuliginea) / Golovinomyces cichoracearum",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.PETIOLE],
        symptoms=[
            "White, talcum powder-like fungal spots on upper and lower leaf surfaces, petioles, and stems",
            "Spots rapidly expand and coalesce into a continuous white powdery fungal mat",
            "Infected leaves turn chlorotic, senesce prematurely, turn brown and crisp ('paper-like')",
            "Premature defoliation leads to fruit sunscald, poor fruit sizing, and shortened harvest duration"
        ],
        symptom_progression="Isolated white powdery spots on lower shaded leaves -> dense fungal mats covering both leaf surfaces -> leaf yellowing and browning -> defoliation and sunscald.",
        development_conditions="Moderate to warm temperatures (20-28°C), high relative humidity (50-90%), dense shaded canopies, dry leaf surfaces (liquid water inhibits germination).",
        spread_transmission="Airborne conidia carried over long distances by wind currents.",
        infection_sources="Greenhouse cucurbits, weed hosts, and southern spore migrations.",
        immediate_actions=[
            "Scout lower, older, and shaded leaves for initial white powdery colonies",
            "Prune dense canopy foliage to enhance light penetration and airflow",
            "Apply protective or eradicant powdery mildew fungicides at first sign of disease"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Potassium Bicarbonate",
                    application_purpose="Contact eradicant fungicide that disrupts fungal cell membranes on contact.",
                    limitations="Provides no residual activity; must directly contact fungal mycelium.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Maintain good plant spacing, trellis vines to improve airflow, and remove old senescent lower leaves.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Sulfur (Micronized / Wettable)",
                    application_purpose="Contact multi-site protectant fungicide applied at early disease onset.",
                    limitations="DO NOT apply when temperatures exceed 30°C (85°F) or within 14 days of an oil spray to prevent severe phytotoxicity.",
                    source_id=SOURCE_UC_IPM.id
                ),
                ChemicalControl(
                    active_ingredient="Cyflufenamid / Fluxapyroxad",
                    application_purpose="Systemic powdery mildew fungicide for high disease pressure.",
                    limitations="Rotate FRAC groups (FRAC U06, 7, 3, 11) to prevent rapid resistance buildup.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Narrow Range Horticultural Oil / Neem Oil",
                    application_purpose="Suffocates and disrupts fungal hyphae and conidia upon direct contact.",
                    limitations="Do not apply during high heat (>32°C) or in combination with sulfur.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Foliar bio-fungicide applied preventively to protect emerging foliage.",
                    source_id=SOURCE_PURDUE.id
                ),
                BiologicalControl(
                    agent_name="Ampelomyces quisqualis",
                    application_method="Hyperparasitic fungus that specifically parasitizes powdery mildew colonies.",
                    source_id=SOURCE_CORNELL.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant powdery mildew resistant cucumber hybrids (PMR varieties)",
                "Trellis vines vertically to maximize air circulation and reduce canopy shading",
                "Maintain balanced fertilization; avoid excess nitrogen which stimulates lush, susceptible tissue"
            ],
            sanitation_measures=[
                "Destroy spent crop residues immediately upon harvest completion",
                "Eliminate volunteer cucurbits and weed hosts around greenhouses and fields"
            ],
            resistant_varieties="Widely available resistant cultivars: Marketmore 76, Diva, Bristol, SV5047CA, General Lee."
        ),
        similar_diseases=["cucumber__downy_mildew", "squash__powdery_mildew"],
        severity_indicators="White powdery coating over >50% of leaf area, extensive leaf necrosis, premature vine death.",
        sources=[SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
        quality_level="HIGH"
    ),

    "squash__powdery_mildew": DiseaseRecord(
        id="squash__powdery_mildew",
        canonical_name="Squash Powdery Mildew",
        crop="squash",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Podosphaera xanthii / Golovinomyces cichoracearum",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.PETIOLE],
        symptoms=[
            "Talc-like white powdery spots appearing primarily on the underside and upper surface of crown and lower leaves",
            "Spots expand rapidly to cover whole leaf blades and petioles in a dense white felt",
            "Infected leaves turn yellow, brown, and become brittle and dry",
            "Premature leaf death exposes developing squash fruit to solar injury (sunscald) and lowers fruit sugar content"
        ],
        symptom_progression="Powdery white spots on lower shaded leaves -> spreading white mycelium over all foliage and stems -> leaf chlorosis, crisping, and death -> sunscalded unmarketable squash.",
        development_conditions="Temperatures 20-27°C, shade, dense plantings, high relative humidity (50-90%), dry leaf foliage.",
        spread_transmission="Windborne conidia carried across wide geographical areas.",
        infection_sources="Greenhouse plants, southern cucurbit production areas, alternate weed hosts.",
        immediate_actions=[
            "Inspect underside of oldest leaves weekly for white powdery specks",
            "Ensure proper vine spacing and weed control",
            "Initiate targeted fungicide spray program at the first sign of mildew colonies"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Potassium Bicarbonate",
                    application_purpose="Contact curative eradicant to knock down existing powdery mildew mycelium.",
                    limitations="Requires complete, high-volume spray coverage of both leaf surfaces.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Maintain wide row spacing to maximize sunlight and airflow; avoid excessive canopy nitrogen.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Sulfur (Micronized)",
                    application_purpose="Economical preventive contact fungicide.",
                    limitations="Do not apply above 30°C or within 2 weeks of oil applications to prevent phytotoxicity.",
                    source_id=SOURCE_UC_IPM.id
                ),
                ChemicalControl(
                    active_ingredient="Quintec (Quinoxyfen) / Vivando (Metrafenone)",
                    application_purpose="Specialty powdery mildew fungicides with vapor action providing superior canopy penetration.",
                    limitations="Strict FRAC rotation (FRAC 13 / FRAC U08); observe pre-harvest intervals.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens",
                    application_method="Foliar bio-fungicide applied preventively to protect newly expanding leaves.",
                    source_id=SOURCE_NC_STATE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant PM-resistant squash hybrids (e.g., Autumn Delight, Dunja, Payroll)",
                "Space squash plants generously (0.9 to 1.2 m apart)",
                "Apply balanced organic or mineral fertilizer; avoid excessive vegetative nitrogen"
            ],
            sanitation_measures=[
                "Mow and disk crop debris immediately post-harvest",
                "Keep field borders clear of wild cucurbits"
            ],
            resistant_varieties="Resistant winter squash (e.g., Metro PMR, Bush Delicata PMR) and summer squash (e.g., Dunja PMR, Green Machine PMR)."
        ),
        similar_diseases=["zucchini__powdery_mildew", "cucumber__powdery_mildew"],
        severity_indicators="Severe powdery covering on crown leaves, extensive leaf collapse, exposed sunscalded fruit.",
        sources=[SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
        quality_level="HIGH"
    ),

    "zucchini__bacterial_wilt": DiseaseRecord(
        id="zucchini__bacterial_wilt",
        canonical_name="Zucchini Bacterial Wilt",
        crop="zucchini",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Erwinia tracheiphila",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Rapid wilting of individual zucchini leaves, progressing down the petiole to the main crown",
            "Wilting occurs rapidly during hot, sunny afternoons, initially recovering at night",
            "Within days, entire plant becomes permanently wilted, collapses, and dies while retaining green coloration",
            "Diagnostic vascular stringing: cutting crown stem and pulling segments apart produces sticky, thread-like bacterial strands"
        ],
        symptom_progression="Leaf wilting -> petiole drooping -> crown collapse -> total plant death with bacterial vascular plugging.",
        development_conditions="Presence and feeding activity of striped or spotted cucumber beetles.",
        spread_transmission="Vectored by cucumber beetles through frass and mouthparts entering feeding wounds.",
        infection_sources="Overwintered adult cucumber beetles and wild cucurbit weeds.",
        immediate_actions=[
            "Perform stem cut stringing test to differentiate from squash vine borer or Fusarium",
            "Rogue out and destroy infected zucchini plants immediately",
            "Apply insecticide or kaolin clay to suppress cucumber beetle feeding"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Immediate roguing of infected plants to remove beetle food reservoirs; intensive vector management.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Bifenthrin / Acetamiprid",
                    application_purpose="Insecticide applied at seedling emergence to 5-leaf stage to suppress beetle feeding.",
                    limitations="Apply at dusk to protect honeybees and native pollinators.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Kaolin Clay",
                    application_purpose="Protective mineral film applied to foliage to deter beetle feeding.",
                    limitations="Reapply after overhead irrigation or rain.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Steinernema feltiae / carpocapsae",
                    application_method="Entomopathogenic nematodes applied to soil to attack cucumber beetle grubs.",
                    source_id=SOURCE_CORNELL.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use physical floating row covers from direct seeding until female flowers appear",
                "Deploy yellow sticky cards around field margins to monitor beetle arrival",
                "Trap cropping around plot edges with preferred squash cultivars (e.g., Blue Hubbard)"
            ],
            sanitation_measures=[
                "Deep-bury or bag wilted plants immediately",
                "Eradicate wild cucurbit weeds around perimeter"
            ],
            resistant_varieties="Most zucchini cultivars are highly susceptible to bacterial wilt; aggressive beetle exclusion is essential."
        ),
        similar_diseases=["cucumber__bacterial_wilt", "squash_vine_borer_damage", "zucchini__fusarium_wilt"],
        severity_indicators="Positive bacterial streaming test from cut crown, irreversible crown collapse and plant death.",
        sources=[
            SOURCE_UW_MADISON_CUCURBIT_BACTERIAL_WILT,
            SOURCE_PNW_CUCUMBER_BACTERIAL_WILT,
            SOURCE_UKY_CUCURBIT_BACTERIAL_WILT,
            SOURCE_PURDUE,
            SOURCE_CORNELL,
            SOURCE_NC_STATE,
        ],
        quality_level="HIGH"
    ),

    "zucchini__downy_mildew": DiseaseRecord(
        id="zucchini__downy_mildew",
        canonical_name="Zucchini Downy Mildew",
        crop="zucchini",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Pseudoperonospora cubensis",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Angular, chlorotic bright yellow spots on upper leaf surface, strictly restricted by plant veins",
            "On corresponding lower leaf surface, a purplish-gray to dark velvety downy sporulation appears in humid conditions",
            "Angular spots rapidly turn brown, necrotic, and brittle ('crispy leaf')",
            "Leaves curl upward and die, producing a scorched canopy appearance and terminating fruit production"
        ],
        symptom_progression="Angular yellow vein-bounded spots -> purple-gray downy mold on underside -> rapid foliar necrosis -> entire canopy collapse.",
        development_conditions="Temperatures 15-22°C, relative humidity >85%, free moisture on leaves (dew, rain, overhead irrigation) for >2 hours.",
        spread_transmission="Airborne sporangia carried long distances by storm fronts and wind currents.",
        infection_sources="Southern cucurbit fields, continuous greenhouse crops, and weed hosts.",
        immediate_actions=[
            "Scout underside of lower leaves for purple-gray velvety mold during humid mornings",
            "Cease overhead irrigation immediately",
            "Apply targeted oomycete-specific fungicides upon regional forecast alerts"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, increase plant spacing for faster leaf drying, and track regional Downy Mildew forecasting (Cucurbit Downy Mildew IPM pipe).",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Cyazofamid (Ranman) / Oxathiapiprolin (Orondis)",
                    application_purpose="Specialized oomycete fungicides for highly effective preventive and translaminar downy mildew control.",
                    limitations="Must be tank-mixed with a protectant (e.g., Mancozeb or Chlorothalonil) and strictly rotated to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Broad-spectrum contact protectant for organic or conventional IPM programs.",
                    limitations="Preventive only; must be reapplied at 7-day intervals during wet weather.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens",
                    application_method="Foliar bio-fungicide spray applied before disease arrival.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant early in the season before airborne downy mildew spore fronts arrive from the south",
                "Ensure generous plant spacing and open field exposure to morning sun",
                "Use drip irrigation under black plastic mulch"
            ],
            sanitation_measures=[
                "Destroy infected crop residues promptly at the end of the season"
            ],
            resistant_varieties="Select newer downy mildew-tolerant zucchini varieties (e.g., Dunja, Paycheck)."
        ),
        similar_diseases=["zucchini__powdery_mildew", "cucumber__downy_mildew", "cucumber__angular_leaf_spot"],
        severity_indicators="Velvety purple-gray sporulation on leaf underside, rapid angular foliar necrosis across >40% of canopy.",
        sources=[SOURCE_NC_STATE_CUCURBIT_DOWNY_MILDEW],
        quality_level="HIGH"
    ),

    "zucchini__powdery_mildew": DiseaseRecord(
        id="zucchini__powdery_mildew",
        canonical_name="Zucchini Powdery Mildew",
        crop="zucchini",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Podosphaera xanthii / Golovinomyces cichoracearum",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.PETIOLE],
        symptoms=[
            "White talcum powder-like fungal patches on both upper and lower leaf surfaces, petioles, and main stems",
            "Patches coalesce into a dense white powdery fungal felt",
            "Underlying leaf tissue turns chlorotic, yellows, and dries into a brittle brown paper texture",
            "Leaves die prematurely, exposing zucchini fruits to severe sunscald and decreasing yield"
        ],
        symptom_progression="White powdery spots on lower leaves -> widespread powdery coating on all leaves/stems -> foliar chlorosis and necrosis -> plant exhaustion and sunscald.",
        development_conditions="Warm temperatures (20-27°C), shade, high humidity (50-90%), dry leaf foliage.",
        spread_transmission="Windborne conidia transported over long distances.",
        infection_sources="Overwintered crops in greenhouses, southern production zones, alternate weed hosts.",
        immediate_actions=[
            "Inspect underside of crown leaves weekly for initial powdery colonies",
            "Apply potassium bicarbonate, horticultural oil, or sulfur at first detection",
            "Improve air penetration through the plant canopy"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Potassium Bicarbonate",
                    application_purpose="Contact curative eradicant that collapses fungal hyphae and spores.",
                    limitations="Must contact the fungus directly; reapply every 7 days as needed.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Space plants properly, remove old dying crown leaves, and maintain balanced non-excessive nitrogen nutrition.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Sulfur (Wettable)",
                    application_purpose="Broad-spectrum preventive contact protectant.",
                    limitations="Do not apply above 30°C or within 14 days of horticultural oils.",
                    source_id=SOURCE_UC_IPM.id
                ),
                ChemicalControl(
                    active_ingredient="Metrafenone (Vivando) / Penthiopyrad (Fontelis)",
                    application_purpose="Systemic fungicides with strong powdery mildew efficacy and translaminar movement.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Foliar bio-fungicide applied preventively to protect emerging foliage.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant powdery mildew-resistant zucchini cultivars (e.g., Dunja PMR, Green Machine, Payroll)",
                "Provide wide spacing (0.9 to 1.2 m) in full sun",
                "Avoid overhead irrigation and excessive nitrogen fertilizers"
            ],
            sanitation_measures=[
                "Destroy spent crop residues promptly at harvest completion"
            ],
            resistant_varieties="Dunja PMR, Green Machine PMR, Spineless Perfection PMR, Payroll PMR."
        ),
        similar_diseases=["zucchini__downy_mildew", "squash__powdery_mildew", "cucumber__powdery_mildew"],
        severity_indicators="Dense white powdery coating over >50% of canopy, extensive foliar crisping and leaf death.",
        sources=[SOURCE_UC_IPM_CUCURBIT_POWDERY_MILDEW],
        quality_level="HIGH"
    ),

    "zucchini__yellow_mosaic_virus": DiseaseRecord(
        id="zucchini__yellow_mosaic_virus",
        canonical_name="Zucchini Yellow Mosaic Virus (ZYMV)",
        crop="zucchini",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Zucchini yellow mosaic virus (ZYMV, Potyvirus)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Severe yellow mosaic, blistering, distortion, and shoestring-like narrowing of leaves",
            "Plants become severely stunted with bushy, rosetted growth and shortened internodes",
            "Fruit exhibits extreme knobby bubbling, prominent green warts, intense yellow-green mottled discoloration, and grotesque physical malformation",
            "Complete unmarketability of fruit and dramatic drop in overall plant yield"
        ],
        symptom_progression="Vein clearing -> brilliant yellow mosaic and leaf bubbling -> shoestring leaf deformation -> knobby, warty, distorted fruit.",
        development_conditions="High populations of aphid vectors (Aphis gossypii, Myzus persicae) in warm weather.",
        spread_transmission="Non-persistently transmitted within seconds by numerous aphid species; mechanically through sap and contaminated tools.",
        infection_sources="Infected wild cucurbit weeds (Cucumis melo var. dudaim, Sicyos angulatus), volunteer cucurbits, adjacent older infected fields.",
        immediate_actions=[
            "Rogue and immediately destroy infected symptomatic plants to limit virus spread",
            "Apply reflective silver plastic mulch to deter incoming winged aphid vectors",
            "Control aphid populations with insecticidal soap or mineral oils"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Immediate roguing of infected plants, reflective mulches, and strict weed sanitation.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Stylet-Oil / Mineral Oil",
                    application_purpose="Foliar oil sprays to interfere with aphid viral transmission by cleaning viral particles from aphid stylets.",
                    limitations="Must be applied frequently (every 3-5 days) with complete canopy coverage.",
                    source_id=SOURCE_UF_IFAS.id
                ),
                ChemicalControl(
                    active_ingredient="Flonicamid / Pymetrozine",
                    application_purpose="Targeted anti-feeding insecticides to halt aphid vector feeding rapidly.",
                    limitations="Follow pollinator protection and resistance management guidelines.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Aphidius colemani (Parasitic wasp)",
                    application_method="Biological aphid vector control in protected culture / greenhouses.",
                    source_id=SOURCE_UC_IPM.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant virus-resistant zucchini varieties with multi-virus resistance (ZYMV, WMV, CMV)",
                "Deploy reflective metallized (silver) mulch at planting to repel winged aphids",
                "Plant early in the season before peak aphid migration flights occur"
            ],
            sanitation_measures=[
                "Eradicate wild cucurbit weeds within a 50-meter perimeter of fields",
                "Sanitize pruning knives and harvesting tools between plants"
            ],
            resistant_varieties="Resistant zucchini cultivars: Judgement III, Tigress, Cashflow, Dividend, Provision (carrying ZYMV resistance genes)."
        ),
        similar_diseases=["watermelon_mosaic_virus", "cucumber_mosaic_virus"],
        severity_indicators="Severe foliar blistering, shoestring leaf distortion, and knobby, warty, deformed unmarketable zucchini fruit.",
        sources=[
            SOURCE_PNW_SQUASH_VIRUS_DISEASES,
            SOURCE_UC_IPM_CUCURBIT_POTYVIRUSES,
            SOURCE_UC_IPM,
            SOURCE_CORNELL,
            SOURCE_NC_STATE,
            SOURCE_UF_IFAS,
        ],
        quality_level="HIGH"
    ),
}
