"""
Authoritative Plant Pathology Knowledge: Brassica, Root & Cole Crops (13 diseases)
- Broccoli: Alternaria Leaf Spot, Downy Mildew, Ring Spot
- Cabbage: Alternaria Leaf Spot, Black Rot, Downy Mildew
- Carrot: Alternaria Leaf Blight, Cavity Spot, Cercospora Leaf Blight
- Cauliflower: Alternaria Leaf Spot, Bacterial Soft Rot
- Celery: Anthracnose, Early Blight
Sources: Cornell University, UC IPM, Purdue Extension, NC State Extension, UF/IFAS, Penn State, USDA ARS.
"""

from knowledge.schema import (
    DiseaseRecord, PathogenType, PlantPart, TreatmentPlan,
    ChemicalControl, CulturalControl, BiologicalControl, PreventionProtocol
)
from knowledge.sources import (
    SOURCE_CORNELL, SOURCE_UC_IPM, SOURCE_PURDUE, SOURCE_NC_STATE,
    SOURCE_UF_IFAS, SOURCE_PENN_STATE, SOURCE_USDA_ARS
)

BRASSICA_ROOT_DISEASES = {
    "broccoli__alternaria_leaf_spot": DiseaseRecord(
        id="broccoli__alternaria_leaf_spot",
        canonical_name="Broccoli Alternaria Leaf Spot and Head Rot",
        crop="broccoli",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Alternaria brassicicola / Alternaria brassicae",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FLOWER, PlantPart.HEAD],
        symptoms=[
            "Small, dark brown to black circular spots on leaves that expand up to 1-2 cm",
            "Spots develop distinct concentric rings with a target-board appearance and a chlorotic yellow halo",
            "Under humid conditions, lesions become covered with a black, sooty/velvety layer of fungal conidia",
            "Infection on broccoli heads causes dark brown to black water-soaked rotting of florets and bead drop, ruining harvest quality"
        ],
        symptom_progression="Lower leaf circular target spots -> black sooty spore coating -> spread to developing heads -> floret rotting and head unmarketability.",
        development_conditions="Warm, humid, rainy weather (temperatures 20-28°C), prolonged leaf wetness (>8-10 hours), dense plantings.",
        spread_transmission="Airborne and rain-splashed conidia, contaminated seed, infected transplants.",
        infection_sources="Infected cruciferous crop residues in soil, infected seed, wild brassica weeds.",
        immediate_actions=[
            "Avoid overhead irrigation, especially during head development",
            "Apply protective fungicides (e.g., chlorothalonil, copper, or azoxystrobin) at first symptom onset",
            "Harvest broccoli heads promptly when mature during dry weather"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, maintain wide plant spacing for canopy aeration, and rotate crops with non-crucifers.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Broad-spectrum contact protectant fungicide applied every 7-10 days in wet conditions.",
                    limitations="Preventive application; observe pre-harvest intervals (7-day PHI for chlorothalonil on broccoli).",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Boscalid + Pyraclostrobin",
                    application_purpose="Systemic fungicides for head rot and foliar disease suppression.",
                    limitations="Rotate FRAC groups (FRAC 11, 7) to manage resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic brassica production.",
                    limitations="Preventive use only; check for crop safety under slow drying conditions.",
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
                "Use certified disease-free, hot-water-treated seed (50°C for 20-30 min)",
                "Practice a minimum 3-year crop rotation with non-brassica crops",
                "Ensure drip irrigation and well-drained soil"
            ],
            sanitation_measures=[
                "Plow under or destroy crop residues immediately after harvest",
                "Eradicate cruciferous weeds (wild mustard, shepherd's purse)"
            ],
            resistant_varieties="Cultivars with domed heads, tight florets, and good water-shedding architecture show reduced head rot."
        ),
        similar_diseases=["broccoli__ring_spot", "broccoli__downy_mildew", "cabbage__black_rot"],
        severity_indicators="Black velvety target-board spots, water-soaked brown/black rot across >15% of head florets.",
        sources=[SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "broccoli__downy_mildew": DiseaseRecord(
        id="broccoli__downy_mildew",
        canonical_name="Broccoli Downy Mildew",
        crop="broccoli",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Hyaloperonospora brassicae (syn. Peronospora parasitica)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.HEAD],
        symptoms=[
            "Irregular, angular, yellow to pale green chlorotic patches on upper leaf surfaces bounded by main veins",
            "Fluffy, white to grayish-white fungal-like downy sporulation on the corresponding lower leaf surface in humid mornings",
            "Infected leaves turn yellow, brown, and drop prematurely (seedlings can be killed rapidly in nursery beds)",
            "Systemic head infection causes internal gray to black vascular discoloration and dark streaks inside the main stalk and head florets"
        ],
        symptom_progression="Angular yellow leaf spots -> white downy sporulation on underside -> leaf yellowing and necrosis -> dark internal stem/floret discoloration.",
        development_conditions="Cool, wet, foggy, or humid weather (temperatures 10-18°C), prolonged dew or fog, crowded seedling flats.",
        spread_transmission="Windborne and rain-splashed sporangia; overwintering oospores in soil and crop residues.",
        infection_sources="Infected cruciferous crop debris in soil, infected transplants, brassica weeds.",
        immediate_actions=[
            "Ventilate greenhouses and nursery beds to keep foliage dry",
            "Avoid overhead irrigation in late afternoon",
            "Apply targeted anti-oomycete fungicides upon first appearance of lower leaf sporulation"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Dimethomorph / Cymoxanil",
                    application_purpose="Translaminar anti-oomycete fungicides with post-infection activity.",
                    limitations="Must be tank-mixed with protectant fungicides.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            management=[
                CulturalControl(
                    description="Greenhouse ventilation, wide field spacing, drip irrigation, and avoiding continuous brassica rotations.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb / Chlorothalonil / Copper Hydroxide",
                    application_purpose="Preventive contact protectants applied on 7-10 day schedules during cool wet weather.",
                    limitations="Preventive application only; adhere to pre-harvest intervals.",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Cyazofamid (Ranman) / Mandipropamid (Revus) / Oxathiapiprolin (Orondis)",
                    application_purpose="Specialized anti-oomycete fungicides for severe downy mildew pressure.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Potassium Phosphite (Phosphorous Acid)",
                    application_purpose="Systemic fungicide for downy mildew suppression and defense stimulation.",
                    limitations="Apply preventively; do not tank-mix with copper.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens",
                    application_method="Foliar bio-fungicide applied preventively.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free seed and clean greenhouse transplant trays",
                "Ensure generous plant spacing and open field exposure to morning sun",
                "Practice a minimum 2-3 year rotation away from brassicas"
            ],
            sanitation_measures=[
                "Incorporate crop residues immediately post-harvest",
                "Eradicate cruciferous weeds"
            ],
            resistant_varieties="Select resistant broccoli hybrids (e.g., Arcadia, Diplomat, Marathon, Gypsy)."
        ),
        similar_diseases=["broccoli__alternaria_leaf_spot", "broccoli__ring_spot"],
        severity_indicators="White downy growth on leaf undersides, severe seedling blight, black internal vascular streaks in floret stalks.",
        sources=[SOURCE_UC_IPM, SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "broccoli__ring_spot": DiseaseRecord(
        id="broccoli__ring_spot",
        canonical_name="Broccoli Ring Spot (Mycosphaerella Ring Spot)",
        crop="broccoli",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Mycosphaerella brassicicola",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.HEAD],
        symptoms=[
            "Distinct circular, dark brownish-gray to black spots (3-20 mm) on leaves",
            "Spots are characterized by numerous tiny black speck-like fruiting bodies (pseudothecia and spermogonia) arranged in prominent concentric rings",
            "Surrounding leaf tissue turns yellow and senesces prematurely; severely infected leaves drop",
            "Infected heads and floret stalks develop dark speckling and necrotic lesions, degrading marketable quality"
        ],
        symptom_progression="Circular gray spots -> concentric rings of black fruiting specks -> foliar yellowing and premature leaf shedding -> floret speckling.",
        development_conditions="Cool, wet, cloudy, coastal or foggy weather (temperatures 15-20°C), extended leaf wetness (>12 hours).",
        spread_transmission="Airborne ascospores discharged forcibly during wet periods and carried by wind currents.",
        infection_sources="Cruciferous crop residues in soil, volunteer brassicas, wild cruciferous weeds.",
        immediate_actions=[
            "Prune or remove severely spotted lower leaves",
            "Avoid overhead irrigation",
            "Apply protective or systemic fungicides at first appearance of circular ringed spots"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Deep plowing of crop residues, crop rotation, and optimizing row spacing for air movement.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil",
                    application_purpose="Contact protectant fungicide applied preventively during cool wet seasons.",
                    limitations="Preventive application; observe 7-day PHI.",
                    source_id=SOURCE_UC_IPM.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Difenoconazole",
                    application_purpose="Systemic fungicides for ring spot control.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Practice a 3-year crop rotation with non-brassica crops",
                "Plant in fields with good air drainage and avoid low, fog-pocket areas",
                "Ensure drip irrigation"
            ],
            sanitation_measures=[
                "Deep-bury or shred crop debris immediately after harvest",
                "Eradicate wild mustard and radish weeds"
            ],
            resistant_varieties="Cultivars with upright growth habit and open frames show reduced ring spot incidence."
        ),
        similar_diseases=["broccoli__alternaria_leaf_spot", "cabbage__alternaria_leaf_spot"],
        severity_indicators="Abundant concentric rings of black specks, lower canopy defoliation >30%, head floret spotting.",
        sources=[SOURCE_UC_IPM, SOURCE_CORNELL, SOURCE_NC_STATE],
        quality_level="HIGH"
    ),

    "cabbage__alternaria_leaf_spot": DiseaseRecord(
        id="cabbage__alternaria_leaf_spot",
        canonical_name="Cabbage Alternaria Leaf Spot",
        crop="cabbage",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Alternaria brassicicola / Alternaria brassicae",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.HEAD],
        symptoms=[
            "Small, dark brown to black circular spots on wrapper and frame leaves",
            "Spots enlarge up to 2-3 cm, developing distinct concentric rings resembling a target board with a chlorotic yellow halo",
            "Under humid conditions, lesions become covered with a velvety black/brown layer of fungal conidia",
            "Infection penetrates head wrapper leaves, causing unsightly black sunken lesions and decay during cold storage"
        ],
        symptom_progression="Circular target-board spots on outer leaves -> velvety black sporulation -> penetration into cabbage head wrapper leaves -> post-harvest storage decay.",
        development_conditions="Warm, humid, rainy weather (temperatures 20-28°C), prolonged leaf wetness, overhead irrigation.",
        spread_transmission="Airborne and water-splashed conidia, contaminated seeds, infected transplants.",
        infection_sources="Infected cruciferous crop residues, contaminated seed, cruciferous weeds.",
        immediate_actions=[
            "Avoid overhead irrigation and working in wet cabbage fields",
            "Apply protective or systemic fungicides at first detection of leaf spots",
            "Strip infected outer wrapper leaves at harvest before packing into cold storage"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, ensure wide row spacing, and strip damaged wrapper leaves at harvest.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Broad-spectrum contact protectant fungicide applied at 7-10 day intervals.",
                    limitations="Preventive application; observe pre-harvest intervals (7-day PHI for chlorothalonil on cabbage).",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Boscalid + Pyraclostrobin",
                    application_purpose="Systemic fungicides for foliar and head protection.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic cabbage production.",
                    limitations="Preventive only; check for crop safety under slow drying conditions.",
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
                "Use certified disease-free, hot-water-treated seed (50°C for 25 min)",
                "Practice a minimum 3-year crop rotation away from brassicas",
                "Ensure drip irrigation and well-drained soil"
            ],
            sanitation_measures=[
                "Incorporate or destroy crop residues immediately post-harvest",
                "Eradicate cruciferous weeds around fields"
            ],
            resistant_varieties="Cultivars with thick waxy cuticles (e.g., Rivera, Bronco) show greater resistance to spore penetration."
        ),
        similar_diseases=["cabbage__black_rot", "cabbage__downy_mildew"],
        severity_indicators="Velvety black target-board spots, penetration of black necrotic rot into cabbage head leaves.",
        sources=[SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "cabbage__black_rot": DiseaseRecord(
        id="cabbage__black_rot",
        canonical_name="Cabbage Black Rot",
        crop="cabbage",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Xanthomonas campestris pv. campestris",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.HEAD, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Diagnostic V-shaped chlorotic (yellow) to necrotic lesions at leaf margins with the wide base of the 'V' at the leaf edge and the point directed toward the leaf vein",
            "Veins within the yellow V-shaped lesion turn dark brown to black, creating a distinct blackened vein netting",
            "Stem cross-sections show a distinct ring of blackened vascular xylem bundles",
            "Severely infected plants show yellowing, wilting, premature leaf drop, stunted cabbage heads, and secondary soft-rot breakdown"
        ],
        symptom_progression="Marginal hydathode infection -> yellow V-shaped lesions -> blackened vein netting -> vascular invasion -> stem vascular ring blackening -> head rot.",
        development_conditions="Warm, humid, wet weather (temperatures 24-30°C), heavy dews, rainstorms, overhead irrigation, handling wet foliage.",
        spread_transmission="Wind-driven rain, splashing water, handling wet plants, contaminated seed, infected transplants, flea beetles.",
        infection_sources="Contaminated seeds (primary source), infected crop residues in soil (survives 1-2 years), cruciferous weeds.",
        immediate_actions=[
            "Avoid entering, cultivating, or harvesting fields while plants are wet with dew or rain",
            "Rogue out and destroy infected transplants immediately",
            "Apply copper bactericide tank-mixed with mancozeb to slow bacterial spread"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, avoid touching wet plants, use raised beds, and rotate with non-crucifers for 3-4 years.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide + Mancozeb",
                    application_purpose="Protective contact tank mix bactericide/fungicide spray applied every 7 days during warm wet periods.",
                    limitations="Preventive application; cannot cure established vascular infections; observe harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Acibenzolar-S-methyl (Actigard)",
                    application_purpose="Plant defense activator to induce systemic acquired resistance (SAR).",
                    limitations="Apply preventively to healthy, actively growing plants before infection.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens / Bacillus subtilis",
                    application_method="Foliar bio-bactericide spray applied preventively in seedbeds.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free, hot-water-treated seed (50°C for 25 min) or bleach-treated seed",
                "Purchase certified disease-free greenhouse transplants",
                "Practice a strict 3-year crop rotation away from all cruciferous crops",
                "Ensure drip irrigation to prevent water splashing"
            ],
            sanitation_measures=[
                "Plow under or destroy crop residues immediately after harvest to accelerate bacterial die-off",
                "Eradicate cruciferous weeds (wild mustard, wild radish, shepherd's purse)",
                "Disinfect greenhouse transplant flats with 10% bleach or quaternary ammonium"
            ],
            resistant_varieties="Resistant/tolerant cabbage hybrids: Bronco, Atlantis, Defender, Blue Vantage, Bravo, Cecile."
        ),
        similar_diseases=["cabbage__alternaria_leaf_spot", "cauliflower__bacterial_soft_rot"],
        severity_indicators="Prominent V-shaped marginal yellow lesions with blackened veins, blackened xylem ring in cut stem, stunted heads.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM, SOURCE_UF_IFAS],
        quality_level="HIGH"
    ),

    "cabbage__downy_mildew": DiseaseRecord(
        id="cabbage__downy_mildew",
        canonical_name="Cabbage Downy Mildew",
        crop="cabbage",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Hyaloperonospora brassicae (syn. Peronospora parasitica)",
        affected_parts=[PlantPart.LEAF, PlantPart.HEAD],
        symptoms=[
            "Angular, irregular, pale green to bright yellow chlorotic patches on upper leaf surfaces",
            "Fluffy, white to grayish-white downy fungal-like sporulation on the corresponding lower leaf surface in damp morning conditions",
            "Infected spots turn purplish-brown to necrotic and dry up; leaves turn yellow and drop prematurely",
            "Infection on mature cabbage heads causes small black speckles, dark sunken lesions, and internal dark vascular flecks in head leaves"
        ],
        symptom_progression="Angular yellow leaf patches -> white downy sporulation on underside -> foliar necrosis -> black specks on cabbage head leaves.",
        development_conditions="Cool, wet, foggy, or humid weather (temperatures 10-18°C), prolonged leaf wetness (>6-10 hours), crowded plant beds.",
        spread_transmission="Windborne and rain-splashed sporangia; overwintering oospores in soil and crop debris.",
        infection_sources="Infected brassica residues in soil, infected nursery transplants, cruciferous weeds.",
        immediate_actions=[
            "Ventilate greenhouses and seedling beds to reduce humidity",
            "Cease overhead watering in late afternoon",
            "Apply targeted anti-oomycete fungicides upon weather-risk alerts"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Dimethomorph / Cymoxanil",
                    application_purpose="Translaminar anti-oomycete fungicides with post-infection activity.",
                    limitations="Must be tank-mixed with protectant fungicides.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            management=[
                CulturalControl(
                    description="Greenhouse ventilation, wide plant spacing, drip irrigation, and 3-year crop rotation.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb / Chlorothalonil / Copper Hydroxide",
                    application_purpose="Preventive contact protectants applied on 7-10 day schedules during cool wet weather.",
                    limitations="Preventive only; observe pre-harvest intervals.",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Cyazofamid (Ranman) / Mandipropamid (Revus)",
                    application_purpose="Specialized anti-oomycete fungicides for severe downy mildew pressure.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Potassium Phosphite",
                    application_purpose="Systemic fungicide for downy mildew suppression and defense stimulation.",
                    limitations="Apply preventively; do not tank mix with copper.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens",
                    application_method="Foliar bio-fungicide applied preventively.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free, hot-water-treated seed",
                "Ensure wide row spacing and good air circulation",
                "Practice a minimum 2-3 year crop rotation away from brassicas"
            ],
            sanitation_measures=[
                "Incorporate crop residues immediately post-harvest",
                "Eradicate cruciferous weeds"
            ],
            resistant_varieties="Many modern cabbage cultivars have field tolerance (e.g., Riviera, Cheers, Superstar)."
        ),
        similar_diseases=["cabbage__alternaria_leaf_spot", "cabbage__black_rot"],
        severity_indicators="White downy growth on leaf undersides, severe seedling defoliation, black flecking across cabbage head wrapper leaves.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "carrot__alternaria_leaf_blight": DiseaseRecord(
        id="carrot__alternaria_leaf_blight",
        canonical_name="Carrot Alternaria Leaf Blight",
        crop="carrot",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Alternaria dauci",
        affected_parts=[PlantPart.LEAF, PlantPart.PETIOLE, PlantPart.ROOT],
        symptoms=[
            "Small, irregular, dark brown to black spots with yellow chlorotic halos appearing first on oldest outer leaves",
            "Spots enlarge, coalesce, and cause leaf margins to curl, turn brown, and die ('scorched' or 'burned' foliage)",
            "Petioles develop elongated, dark brown, sunken lesions that weaken the top attachment",
            "Severe blight causes top foliage to collapse, preventing mechanical top-lifting harvesting and reducing root sizing"
        ],
        symptom_progression="Small dark spots on outer leaves -> leaf browning and margin curling -> petiole cankers -> canopy death and failure of mechanical harvesting.",
        development_conditions="Warm, humid, rainy weather (temperatures 20-28°C), extended leaf wetness (>8-12 hours), dense foliage canopy.",
        spread_transmission="Windborne and rain-splashed conidia, contaminated seed, machinery moving through wet fields.",
        infection_sources="Infected carrot crop residues in soil (survives 1-2 years), contaminated seed, volunteer carrots, wild carrot (Queen Anne's lace).",
        immediate_actions=[
            "Avoid overhead irrigation in late afternoon; switch to drip irrigation",
            "Apply protective or systemic fungicides when disease forecast threshold (e.g., TOM-CAST / FAST) is reached",
            "Ensure balanced fertilization; avoid excess nitrogen that creates dense lush tops"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, plant on raised beds, optimize row spacing for canopy aeration, and avoid over-fertilizing with nitrogen.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Broad-spectrum contact protectant fungicide applied at 7-10 day intervals starting when canopy is 50% closed.",
                    limitations="Preventive application; observe pre-harvest intervals (Chlorothalonil 0-day PHI; Mancozeb 7-day PHI on carrots).",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Difenoconazole / Boscalid + Pyraclostrobin",
                    application_purpose="Systemic fungicides providing translaminar protection and curative suppression of early lesions.",
                    limitations="Strict resistance management: rotate FRAC groups (FRAC 11, 3, 7) with multi-site protectants.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic carrot production.",
                    limitations="Preventive only; reapply after rain.",
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
                "Use certified disease-free, hot-water-treated seed (50°C for 20 min) or fungicide-treated seed",
                "Practice a minimum 2-3 year crop rotation away from umbelliferous crops (carrots, celery, parsley, parsnips)",
                "Plant on raised beds and maintain optimal plant spacing"
            ],
            sanitation_measures=[
                "Incorporate or deep-plow crop residues immediately after harvest",
                "Eradicate wild carrot (Daucus carota) weeds around field borders"
            ],
            resistant_varieties="Highly resistant cultivars: Bolero, Enterprise, Maverick, Cupar, Bergen, Carson."
        ),
        similar_diseases=["carrot__cercospora_leaf_blight", "carrot__cavity_spot"],
        severity_indicators="Severe foliar browning covering >40% of canopy, petiole girdling, complete canopy collapse preventing mechanical harvest.",
        sources=[SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "carrot__cavity_spot": DiseaseRecord(
        id="carrot__cavity_spot",
        canonical_name="Carrot Cavity Spot",
        crop="carrot",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Pythium sulcatum / Pythium violae",
        affected_parts=[PlantPart.ROOT],
        symptoms=[
            "Small, circular to oval, sunken, water-soaked, dark lesions on the carrot taproot",
            "Lesions expand horizontally (transversely across the root width) to form elliptical, dark brown to black sunken cavities (craters)",
            "The skin over the lesion ruptures, exposing the underlying dark necrotic flesh",
            "Secondary opportunistic bacteria and fungi colonize the cavities, causing deep root rotting and total loss of fresh market value"
        ],
        symptom_progression="Small sunken root spots -> transverse elliptical crater-like cavities -> skin rupture and flesh necrosis -> unmarketable culled roots.",
        development_conditions="Cool, wet soil conditions (temperatures 10-18°C), waterlogged or poorly drained soils, high soil moisture in the upper 15 cm.",
        spread_transmission="Soilborne oospores and mycelium; spread by irrigation water, contaminated tillage implements, and soil movement.",
        infection_sources="Oospores persisting in soil for multiple years, volunteer carrots, alternate weed hosts.",
        immediate_actions=[
            "Improve soil drainage and avoid overwatering during root expansion",
            "Apply targeted anti-oomycete soil treatments (e.g., mefenoxam / metalaxyl) if approved",
            "Harvest roots promptly when mature to prevent cavity enlargement"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Plant on high raised beds (20-25 cm), install tile drainage, monitor soil moisture with tensiometers, and avoid excessive irrigation.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mefenoxam (Ridomil Gold) / Metalaxyl",
                    application_purpose="Systemic soil fungicide applied pre-plant incorporated or at planting / early post-emergence.",
                    limitations="Apply according to label restrictions; observe resistance management guidelines; check regional registrations.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Trichoderma harzianum / Gliocladium virens",
                    application_method="Soil bio-fungicide amendment at planting to suppress Pythium inoculum.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Construct high raised beds with deep subsoil ripping to maximize root-zone drainage",
                "Practice a 3-4 year crop rotation with non-host crops (e.g., corn, small grains, brassicas)",
                "Avoid over-irrigating during the final 4-6 weeks of root sizing"
            ],
            sanitation_measures=[
                "Thoroughly wash tillage equipment before moving between fields",
                "Do not return carrot culls to production fields"
            ],
            resistant_varieties="Cultivars show varying tolerance; Bolero and Romance show moderate tolerance to cavity spot."
        ),
        similar_diseases=["carrot__alternaria_leaf_blight", "carrot__cercospora_leaf_blight", "carrot__rhizoctonia_canker"],
        severity_indicators="Transverse sunken black cavities on >10% of harvested carrot roots, skin rupture, secondary soft rot.",
        sources=[SOURCE_UC_IPM, SOURCE_CORNELL, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "carrot__cercospora_leaf_blight": DiseaseRecord(
        id="carrot__cercospora_leaf_blight",
        canonical_name="Carrot Cercospora Leaf Blight",
        crop="carrot",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cercospora carotae",
        affected_parts=[PlantPart.LEAF, PlantPart.PETIOLE],
        symptoms=[
            "Small, circular, chlorotic spots appearing first on young, rapidly growing leaves near the center of the crown",
            "Spots turn tan to dark brown with a distinct grayish-white center and a prominent yellow chlorotic halo",
            "Lesions on leaf margins cause leaflets to curl, become cupped, wither, and die prematurely",
            "Petioles develop elongated, tan to dark brown lesions with pale centers, causing petioles to break easily and shedding foliage"
        ],
        symptom_progression="Circular gray-centered spots on young inner leaves -> leaf curling and blighting -> petiole lesions -> premature canopy loss and weakened top lifting.",
        development_conditions="Warm, humid, rainy weather (temperatures 22-28°C), prolonged leaf wetness (>8-12 hours), dense lush plant stands.",
        spread_transmission="Windborne and water-splashed conidia, contaminated seed, machinery.",
        infection_sources="Infected carrot debris in soil, contaminated seed, wild carrot weeds.",
        immediate_actions=[
            "Avoid overhead irrigation, especially in late afternoon/evening",
            "Apply protective or systemic fungicides starting early when plants are 10-15 cm tall",
            "Maintain optimal row spacing to enhance airflow"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, ensure wide row spacing for canopy aeration, and practice 2-3 year crop rotation.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Contact protectant fungicide applied every 7-10 days in wet warm conditions.",
                    limitations="Preventive application; observe pre-harvest intervals.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Difenoconazole / Pyraclostrobin",
                    application_purpose="Systemic fungicides for effective Cercospora blight management.",
                    limitations="Rotate FRAC groups (FRAC 11, 3) to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic systems.",
                    limitations="Preventive only; ensure thorough coverage of young crown leaves.",
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
                "Use certified disease-free, hot-water-treated seed (50°C for 20 min)",
                "Practice a minimum 2-3 year crop rotation with non-umbelliferous crops",
                "Ensure raised beds and balanced non-excessive nitrogen fertilization"
            ],
            sanitation_measures=[
                "Plow under or destroy crop debris thoroughly after harvest",
                "Eradicate wild carrot weeds"
            ],
            resistant_varieties="Cultivars with high tolerance/resistance: Bolero, Enterprise, Maverick, Carson."
        ),
        similar_diseases=["carrot__alternaria_leaf_blight", "carrot__cavity_spot"],
        severity_indicators="Abundant gray-centered spots on young leaves, petiole cankers, severe foliar blighting >35%.",
        sources=[SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "cauliflower__alternaria_leaf_spot": DiseaseRecord(
        id="cauliflower__alternaria_leaf_spot",
        canonical_name="Cauliflower Alternaria Leaf Spot and Curd Rot",
        crop="cauliflower",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Alternaria brassicicola / Alternaria brassicae",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.HEAD, PlantPart.FLOWER],
        symptoms=[
            "Small, dark brown to black circular spots on wrapper and frame leaves",
            "Spots enlarge with distinct concentric rings creating a target-board appearance and a yellow halo",
            "Under humid conditions, spots become covered with a velvety black soot-like layer of fungal conidia",
            "Infection on the white cauliflower curd causes brown, water-soaked, sunken blemishes and superficial brown specks that ruin market quality"
        ],
        symptom_progression="Circular target-board leaf spots -> black velvety spore mantle -> curd water-soaking and brown blemish development -> unmarketable curd rot.",
        development_conditions="Warm, humid, wet weather (temperatures 20-28°C), prolonged leaf/curd wetness (>8 hours), overhead irrigation.",
        spread_transmission="Airborne and rain-splashed conidia, contaminated seed, infected transplants.",
        infection_sources="Infected cruciferous crop residues, contaminated seed, wild brassica weeds.",
        immediate_actions=[
            "Tie wrapper leaves over curds (blanching) during dry weather to protect curds",
            "Avoid overhead irrigation during curd development",
            "Apply protective fungicides at first sign of leaf spotting"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, maintain wide plant spacing, tie wrapper leaves properly, and rotate with non-crucifers.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Broad-spectrum contact protectant fungicide applied every 7-10 days in wet conditions.",
                    limitations="Preventive application; observe pre-harvest intervals (Chlorothalonil 7-day PHI on cauliflower).",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Boscalid + Pyraclostrobin",
                    application_purpose="Systemic fungicides for curd rot and foliar disease suppression.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic brassica production.",
                    limitations="Preventive only; check for crop safety under slow drying conditions.",
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
                "Use certified disease-free, hot-water-treated seed (50°C for 20-25 min)",
                "Practice a minimum 3-year crop rotation away from brassicas",
                "Ensure drip irrigation and well-drained soil"
            ],
            sanitation_measures=[
                "Incorporate crop residues immediately post-harvest",
                "Eradicate cruciferous weeds"
            ],
            resistant_varieties="Cultivars with self-wrapping leaves that shield curds from rain splash show lower curd rot incidence."
        ),
        similar_diseases=["cauliflower__bacterial_soft_rot", "cabbage__alternaria_leaf_spot"],
        severity_indicators="Velvety black target spots on leaves, brown sunken water-soaked blemishes across >10% of white curd surface.",
        sources=[SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "cauliflower__bacterial_soft_rot": DiseaseRecord(
        id="cauliflower__bacterial_soft_rot",
        canonical_name="Cauliflower Bacterial Soft Rot",
        crop="cauliflower",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Pectobacterium carotovorum subsp. carotovorum (formerly Erwinia carotovora) / Pseudomonas marginalis",
        affected_parts=[PlantPart.HEAD, PlantPart.STEM, PlantPart.LEAF, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Small, water-soaked, glassy, translucent spots on the curd or stem",
            "Spots rapidly enlarge into a soft, mushy, slimy, watery rot that completely breaks down the curd tissue",
            "A foul, nauseating, sulfurous odor emanates from the rotting plant tissue",
            "Infected curd collapses into a dark, slimy, liquefied mass within 24 to 48 hours in warm, wet conditions"
        ],
        symptom_progression="Water-soaked curd spot -> rapid tissue liquefaction and mushy collapse -> foul odor emission -> total curd disintegration.",
        development_conditions="Warm, wet, humid weather (temperatures 22-30°C), free water on curds, physical wounds (insect feeding, mechanical harvesting, hail, frost damage).",
        spread_transmission="Splashing rain, overhead irrigation water, insects (maggots, flea beetles), contaminated harvest knives and packing bins.",
        infection_sources="Soil, decaying plant residues, infested irrigation water, insect vectors.",
        immediate_actions=[
            "Harvest curds only when completely dry",
            "Sanitize harvesting knives frequently in 70% alcohol or 10% bleach",
            "Discard and bury infected soft-rotted plants immediately (do not pack with healthy heads)",
            "Cool harvested cauliflower rapidly to 0-2°C immediately after cutting"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Strict sanitation: harvest during dry weather, avoid bruising curds, sanitize knives, rapid postharvest cooling (0-2°C), and drip irrigation.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Foliar contact bactericide spray applied preventively before rain events to reduce bacterial populations.",
                    limitations="Preventive only; cannot arrest internal soft rot; avoid excessive copper buildup.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use drip irrigation to keep curds and heads completely dry",
                "Control insect pests (flea beetles, cabbage loopers, maggots) that create bacterial entry wounds",
                "Ensure well-drained raised beds and balanced non-excessive nitrogen fertilization"
            ],
            sanitation_measures=[
                "Disinfect harvesting knives, cutting surfaces, and harvesting lugs regularly with food-grade sanitizer",
                "Deep-bury or remove infected cull piles far away from packing sheds and fields"
            ],
            resistant_varieties="Cultivars with dome-shaped curds that shed water rapidly have lower disease incidence."
        ),
        similar_diseases=["cauliflower__alternaria_leaf_spot", "cabbage__black_rot"],
        severity_indicators="Slimy water-soaked curd collapse, foul sulfurous odor, total liquefaction of curd head.",
        sources=[SOURCE_CORNELL, SOURCE_UF_IFAS, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "celery__anthracnose": DiseaseRecord(
        id="celery__anthracnose",
        canonical_name="Celery Anthracnose (Leaf Curl and Stunt)",
        crop="celery",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Colletotrichum fioriniae / Colletotrichum nymphaeae (Colletotrichum acutatum complex)",
        affected_parts=[PlantPart.LEAF, PlantPart.PETIOLE, PlantPart.STEM, PlantPart.HEART],
        symptoms=[
            "Severe downward curling, cupping, twisting, and distortion of young inner leaves and petioles",
            "Elongated, sunken, reddish-brown to dark brown necrotic lesions on petioles (stalks)",
            "Heart rot: internal necrosis and secondary decay of the central heart of the celery stalk",
            "Salmon-pink or orange gelatinous spore masses (acervuli) appear in lesions during humid periods; severe plant stunting"
        ],
        symptom_progression="Leaflet curling and twisting -> sunken reddish-brown petiole lesions -> salmon-pink spore masses -> heart rot and severe plant stunting.",
        development_conditions="Warm, humid, rainy weather (temperatures 22-30°C), frequent overhead irrigation, splashing water.",
        spread_transmission="Water-splashed conidia, contaminated seed, infected transplants, machinery moving through wet fields.",
        infection_sources="Infected crop debris in soil, infected seed/transplants, alternate weed hosts.",
        immediate_actions=[
            "Switch from overhead sprinkler to drip irrigation",
            "Avoid cultivating or moving through celery fields when foliage is wet",
            "Apply protective or systemic fungicides at first sign of leaf curling"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, plant on raised beds, rogue severely curled transplants, and practice 3-year crop rotation.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil",
                    application_purpose="Broad-spectrum contact protectant fungicide applied at 7-day intervals.",
                    limitations="Preventive application; observe 7-day PHI on celery.",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin (Quadris) / Pyraclostrobin (Cabrio)",
                    application_purpose="Systemic strobilurin fungicides for anthracnose suppression.",
                    limitations="Strict resistance management: rotate FRAC 11 with FRAC 3 (Difenoconazole) and multi-site protectants.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic systems.",
                    limitations="Preventive application only.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free, hot-water-treated seed (50°C for 25 min) or certified transplants",
                "Practice a minimum 3-year crop rotation with non-umbelliferous crops",
                "Ensure drip irrigation to prevent water splashing"
            ],
            sanitation_measures=[
                "Incorporate crop residues immediately after harvest to speed breakdown",
                "Disinfect greenhouse transplant benches and trays"
            ],
            resistant_varieties="Cultivars show varying susceptibility; maintaining strict crop rotation and drip irrigation is essential."
        ),
        similar_diseases=["celery__early_blight", "celery__late_blight_(septoria)"],
        severity_indicators="Severe downward leaf curling, sunken reddish-brown petiole cankers with salmon-pink spores, heart rot.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_UC_IPM, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "celery__early_blight": DiseaseRecord(
        id="celery__early_blight",
        canonical_name="Celery Early Blight (Cercospora Leaf Blight)",
        crop="celery",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cercospora apii",
        affected_parts=[PlantPart.LEAF, PlantPart.PETIOLE],
        symptoms=[
            "Small, circular to irregular, yellowish-brown spots appearing first on both upper and lower leaf surfaces",
            "Spots enlarge up to 1 cm, becoming light brown to grayish-tan with an ash-colored center and a faint yellow halo",
            "Under humid conditions, lesions become covered with a delicate gray, velvety coating of fungal conidiophores",
            "Petioles (stalks) develop elongated, dark brown, sunken lesions that make stalks unmarketable"
        ],
        symptom_progression="Circular yellow/brown spots on leaves -> gray velvety sporulation -> petiole streak cankers -> premature foliage blighting and stalk culling.",
        development_conditions="Warm, humid, rainy weather (temperatures 24-30°C), relative humidity >85%, extended dew periods (>8-10 hours).",
        spread_transmission="Windborne and rain-splashed conidia, infected transplants, machinery.",
        infection_sources="Infected celery crop residues in soil, infected seed, volunteer celery, weed hosts.",
        immediate_actions=[
            "Avoid overhead irrigation; schedule watering for early morning to allow rapid leaf drying",
            "Apply protective or systemic fungicides at first appearance of foliar spotting",
            "Trim out and cull heavily spotted outer petioles at harvest"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Drip irrigation, raised beds, wide plant spacing for airflow, and balanced non-excessive nitrogen fertilization.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil",
                    application_purpose="Standard contact protectant fungicide applied on a 7-day schedule.",
                    limitations="Preventive only; observe 7-day PHI on celery.",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Difenoconazole + Azoxystrobin (Quadris Top) / Penthiopyrad (Fontelis)",
                    application_purpose="Systemic fungicides for effective early blight suppression.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic celery production.",
                    limitations="Preventive application only.",
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
                "Use certified disease-free, hot-water-treated seed (50°C for 25 min) or aged seed (2-3 years old)",
                "Practice a minimum 2-3 year crop rotation away from celery, parsley, and carrots",
                "Ensure raised beds and drip irrigation"
            ],
            sanitation_measures=[
                "Incorporate crop residues deeply immediately after harvest",
                "Eradicate wild umbelliferous weeds"
            ],
            resistant_varieties="Cultivars with partial resistance/tolerance: Tango, Sabroso, Matador."
        ),
        similar_diseases=["celery__anthracnose", "celery__late_blight_(septoria)"],
        severity_indicators="Ash-colored spots with gray velvety mold covering >30% of foliage, sunken petiole lesions.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),
}
