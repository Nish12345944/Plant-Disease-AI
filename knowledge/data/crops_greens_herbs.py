"""
Authoritative Plant Pathology Knowledge: Greens, Herbs, Alliums & Specialty Trees (6 diseases)
- Basil: Downy Mildew
- Garlic: Leaf Blight (Stemphylium), Rust
- Lettuce: Downy Mildew, Mosaic Virus (LMV)
- Maple: Tar Spot (Rhytisma)
Sources: Cornell University, UC IPM, Purdue Extension, NC State Extension, UF/IFAS, USDA ARS.
"""

from knowledge.schema import (
    DiseaseRecord, PathogenType, PlantPart, TreatmentPlan,
    ChemicalControl, CulturalControl, BiologicalControl, PreventionProtocol
)
from knowledge.sources import (
    SOURCE_CORNELL, SOURCE_UC_IPM, SOURCE_PURDUE, SOURCE_NC_STATE,
    SOURCE_UF_IFAS, SOURCE_USDA_ARS
)

GREENS_HERBS_DISEASES = {
    "basil__downy_mildew": DiseaseRecord(
        id="basil__downy_mildew",
        canonical_name="Basil Downy Mildew",
        crop="basil",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Peronospora belbahrii",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM],
        symptoms=[
            "Diffuse, irregular, yellow chlorotic patches on the upper surface of leaves, initially delimited by main veins (resembles nutritional deficiency)",
            "Diagnostic feature: Dense, velvety, purplish-gray to dark brown fungal-like sporulation on the corresponding lower leaf surface",
            "Infected leaves curl downward, cup under, turn dark brown/black, and wither rapidly",
            "Seedlings and field plants become completely unmarketable; entire beds collapse under humid conditions"
        ],
        symptom_progression="Upper leaf yellow patches -> dense purplish-gray velvety mold on underside -> leaf rolling and browning -> total canopy collapse.",
        development_conditions="Warm, humid weather (temperatures 18-24°C), relative humidity >85%, prolonged leaf wetness (>6-8 hours), poorly ventilated greenhouses.",
        spread_transmission="Windborne sporangia; contaminated seed (seedborne); infected greenhouse transplants; handling wet plants.",
        infection_sources="Contaminated basil seed, infected greenhouse transplants, continuous indoor hydroponic systems.",
        immediate_actions=[
            "Increase greenhouse temperature and use horizontal airflow fans to keep relative humidity strictly below 80-85%",
            "Cease all overhead watering and water strictly at base",
            "Harvest uninfected foliage immediately if downy mildew appears in the greenhouse or field",
            "Apply targeted anti-oomycete fungicides upon first symptom onset"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Greenhouse climate control: night heating and venting to maintain RH <85%, continuous airflow fans, drip/sub-irrigation, and wide plant spacing.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Cyazofamid (Ranman) / Mandipropamid (Revus) / Oxathiapiprolin (Orondis)",
                    application_purpose="Specialized anti-oomycete fungicides applied preventively or at early disease onset in commercial field basil.",
                    limitations="Check greenhouse vs. field label registrations; rotate FRAC groups; observe pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Potassium Phosphite (ProPhyt / Phostrol)",
                    application_purpose="Systemic fungicide for downy mildew suppression and defense stimulation.",
                    limitations="Apply preventively; ensure good coverage of lower leaf surfaces.",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic basil production.",
                    limitations="Preventive only; check for leaf phytotoxicity under slow drying conditions.",
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
                "Plant downy mildew-resistant basil varieties carrying Pb resistance genes (e.g., Prospera, Rutgers Passion, Rutgers Devotion, Amazel)",
                "Use steam-treated or certified disease-free, tested seed lots",
                "Ensure drip or ebb-and-flow sub-irrigation to prevent wetting leaf surfaces"
            ],
            sanitation_measures=[
                "Thoroughly clean and sanitize greenhouse benches and trays between crop cycles",
                "Destroy all infected crop residues immediately in closed bags"
            ],
            resistant_varieties="Resistant cultivars: Prospera series (DMR DMR-F1), Rutgers Obsession DMR, Rutgers Passion DMR, Amazel."
        ),
        similar_diseases=["basil__iron_deficiency", "basil__fusarium_wilt"],
        severity_indicators="Purplish-gray velvety sporulation on leaf undersides, widespread foliar browning and complete crop loss.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM, SOURCE_UF_IFAS],
        quality_level="HIGH"
    ),

    "garlic__leaf_blight": DiseaseRecord(
        id="garlic__leaf_blight",
        canonical_name="Garlic Stemphylium Leaf Blight",
        crop="garlic",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Stemphylium vesicarium (teleomorph Pleospora allii)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM],
        symptoms=[
            "Small, oval to elliptical, water-soaked yellowish-white spots on leaves and scapes",
            "Spots expand into elongated, light brown to tan lesions with darker brown centers and yellow halos",
            "In humid weather, lesions become covered with a dense, black, sooty/velvety layer of fungal conidiophores",
            "Lesions coalesce, causing leaf tips and margins to die back ('leaf dieback'), reducing photosynthetic leaf area and bulb sizing"
        ],
        symptom_progression="Water-soaked oval spots -> expanding tan lesions with black sooty mold -> leaf tip dieback and blighting -> reduced bulb size.",
        development_conditions="Warm, humid, rainy weather (temperatures 20-26°C), prolonged leaf wetness (>12-16 hours of rain, dew, or overhead irrigation).",
        spread_transmission="Windborne and rain-splashed conidia; survives on allium crop residue.",
        infection_sources="Infected garlic/onion crop residue in soil, volunteer alliums, wild allium weeds.",
        immediate_actions=[
            "Avoid overhead irrigation; switch to drip irrigation",
            "Apply protective or systemic fungicides at first detection of leaf spots",
            "Maintain optimal row spacing to facilitate airflow"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Drip irrigation, crop rotation with non-alliums (3 years), wide plant spacing, and balanced fertilization.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Contact protectant fungicide applied at 7-10 day intervals in wet weather.",
                    limitations="Preventive application; observe pre-harvest intervals (Chlorothalonil 7-day PHI on garlic).",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin + Difenoconazole (Quadris Top) / Penthiopyrad (Fontelis)",
                    application_purpose="Systemic fungicides for effective Stemphylium blight control.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact protectant for organic allium production.",
                    limitations="Preventive application only.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified disease-free garlic seed cloves from reputable nurseries",
                "Practice a minimum 3-year crop rotation with non-allium crops",
                "Ensure well-drained raised beds and drip irrigation"
            ],
            sanitation_measures=[
                "Incorporate or destroy all allium residues after harvest",
                "Eradicate wild alliums and volunteer garlic"
            ],
            resistant_varieties="Cultivars show varying tolerance; vigorous hardneck and softneck varieties under good management perform best."
        ),
        similar_diseases=["garlic__rust", "garlic__purple_blotch_(alternaria_porri)"],
        severity_indicators="Black velvety sooty coating on tan lesions, leaf tip dieback >40%, stunted bulbs.",
        sources=[SOURCE_CORNELL, SOURCE_UC_IPM, SOURCE_NC_STATE],
        quality_level="HIGH"
    ),

    "garlic__rust": DiseaseRecord(
        id="garlic__rust",
        canonical_name="Garlic Rust",
        crop="garlic",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Puccinia allii (syn. Puccinia porri)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM],
        symptoms=[
            "Small, circular to elongated, yellowish to whitish chlorotic flecks on leaves and scapes",
            "Flecks erupt into raised, bright orange to reddish-orange powdery pustules (uredinia) on BOTH leaf surfaces",
            "Pustules rupture the epidermis, releasing clouds of powdery orange urediniospores",
            "Leaves turn yellow, wither, and collapse prematurely, severely reducing bulb yield and quality; pustules turn black late in the season (teliospores)"
        ],
        symptom_progression="Yellow leaf flecks -> bright orange powdery pustules erupting on leaves/stems -> foliar necrosis and collapse -> stunted undersized bulbs.",
        development_conditions="Cool to moderate temperatures (10-20°C), high relative humidity (>95%), prolonged leaf wetness (fog, dew, overhead irrigation), excessive nitrogen.",
        spread_transmission="Airborne urediniospores blown across long distances by wind currents; autoecious (completes entire cycle on alliums).",
        infection_sources="Infected volunteer garlic/onions, overwintering allium crops, crop residues.",
        immediate_actions=[
            "Scout leaves weekly in spring for orange powdery pustules",
            "Apply protective or systemic rust fungicides at first sign of pustules",
            "Cease overhead irrigation immediately"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Tebuconazole / Propiconazole",
                    application_purpose="Systemic DMI triazole fungicide providing curative arrest of early rust infections.",
                    limitations="Apply at early disease onset; observe pre-harvest intervals.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, avoid excessive nitrogen fertilization, ensure wide row spacing for airflow, and rotate crops.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Azoxystrobin (Quadris) / Pyraclostrobin (Cabrio)",
                    application_purpose="Systemic strobilurin fungicides for comprehensive rust suppression.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_UC_IPM.id
                ),
                ChemicalControl(
                    active_ingredient="Mancozeb / Chlorothalonil",
                    application_purpose="Contact protectant fungicides applied preventively.",
                    limitations="Observe pre-harvest intervals.",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Sulfur (Wettable / Micronized)",
                    application_purpose="Organic contact protectant.",
                    limitations="Do not apply above 30°C.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified disease-free seed cloves",
                "Practice a minimum 2-3 year crop rotation with non-allium crops",
                "Maintain balanced soil fertility (avoid high nitrogen which promotes dense succulent leaves)"
            ],
            sanitation_measures=[
                "Destroy all volunteer garlic and cull piles",
                "Incorporate crop residues post-harvest"
            ],
            resistant_varieties="Cultivar susceptibility varies; elephant garlic is highly susceptible; hardneck cultivars vary."
        ),
        similar_diseases=["garlic__leaf_blight", "garlic__purple_blotch"],
        severity_indicators="Bright orange powdery pustules covering >30% of leaf area, extensive canopy withering, severely undersized bulbs.",
        sources=[SOURCE_UC_IPM, SOURCE_CORNELL, SOURCE_NC_STATE],
        quality_level="HIGH"
    ),

    "lettuce__downy_mildew": DiseaseRecord(
        id="lettuce__downy_mildew",
        canonical_name="Lettuce Downy Mildew",
        crop="lettuce",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Bremia lactucae",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Light green to bright yellow, angular chlorotic spots on the upper surface of leaves, strictly bounded by leaf veins",
            "Diagnostic feature: Abundant, brilliant white, fluffy/downy fungal-like sporulation on the corresponding lower leaf surface",
            "Lesions expand, coalesce, turn brown, and dry up into papery necrotic patches",
            "Older infected wrapper leaves rot, predisposing head lettuce to secondary bacterial soft rot during transport and storage"
        ],
        symptom_progression="Angular yellow leaf spots bounded by veins -> white downy sporulation on underside -> brown papery necrosis -> secondary soft rot decay.",
        development_conditions="Cool, damp, wet, foggy weather (temperatures 10-18°C), high relative humidity (>90%), prolonged leaf wetness (>4-6 hours of morning dew or rain).",
        spread_transmission="Windborne sporangia discharged in early morning; rain splashing; infected greenhouse transplants; wild prickly lettuce.",
        infection_sources="Infected wild prickly lettuce (Lactuca serriola), continuous lettuce plantings, crop residues.",
        immediate_actions=[
            "Scout lower leaves in early morning for white fluffy down on underside of yellow angular patches",
            "Avoid overhead irrigation; water strictly during midday to allow leaves to dry before night",
            "Apply targeted anti-oomycete fungicides at first detection or when weather risk is high"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Dimethomorph / Cymoxanil",
                    application_purpose="Translaminar anti-oomycete fungicides with post-infection curative activity.",
                    limitations="Must be tank-mixed with protectants; observe harvest intervals.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            management=[
                CulturalControl(
                    description="Switch to drip or furrow irrigation, ensure wide plant spacing for canopy aeration, and destroy wild prickly lettuce near fields.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mandipropamid (Revus) / Cyazofamid (Ranman) / Oxathiapiprolin (Orondis)",
                    application_purpose="Specialized anti-oomycete fungicides applied preventively for high disease pressure.",
                    limitations="Strict resistance management: alternate FRAC groups (FRAC 40, 21, 49) and tank mix with protectants.",
                    source_id=SOURCE_UC_IPM.id
                ),
                ChemicalControl(
                    active_ingredient="Mancozeb / Copper Hydroxide",
                    application_purpose="Contact protectant fungicides applied preventively.",
                    limitations="Observe pre-harvest intervals (Mancozeb 10-day PHI on head lettuce; check leaf lettuce restrictions).",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Potassium Phosphite",
                    application_purpose="Systemic fungicide for downy mildew suppression and defense stimulation.",
                    limitations="Apply preventively; do not tank mix with copper.",
                    source_id=SOURCE_CORNELL.id
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
                "Plant downy mildew-resistant lettuce cultivars carrying updated Dm resistance genes (e.g., Dm1 through Dm38)",
                "Avoid overhead sprinkler irrigation; use sub-surface drip irrigation",
                "Ensure generous plant spacing and open field orientation for morning sunlight"
            ],
            sanitation_measures=[
                "Plow under or destroy crop residues immediately post-harvest",
                "Eradicate wild prickly lettuce (Lactuca serriola) around field borders"
            ],
            resistant_varieties="Select cultivars resistant to the latest Bremia lactucae novel races (e.g., Bl: 16-40EU/US)."
        ),
        similar_diseases=["lettuce__powdery_mildew", "lettuce__bacterial_blight"],
        severity_indicators="Brilliant white downy growth on leaf undersides, angular brown foliar necrosis across >30% of wrapper leaves.",
        sources=[SOURCE_UC_IPM, SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_NC_STATE],
        quality_level="HIGH"
    ),

    "lettuce__mosaic_virus": DiseaseRecord(
        id="lettuce__mosaic_virus",
        canonical_name="Lettuce Mosaic Virus (LMV)",
        crop="lettuce",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Lettuce mosaic virus (LMV, Potyvirus)",
        affected_parts=[PlantPart.LEAF, PlantPart.HEAD, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Light green and dark green mottled mosaic pattern on leaves",
            "Vein clearing, leaf wrinkling, puckering, bubbling, and severe downward rolling/curling of leaf margins",
            "Leaves may develop brown necrotic flecks along veins, causing leaf browning and necrosis",
            "Plant stunting, failure to form a solid marketable head, and loose, unmarketable heads with bitter flavor"
        ],
        symptom_progression="Vein clearing -> mottled green mosaic and leaf puckering -> severe stunting -> failure of head formation -> unmarketable bitter crop.",
        development_conditions="Warm weather supporting green peach aphid (Myzus persicae) and potato aphid migrations.",
        spread_transmission="Non-persistently transmitted within seconds by aphid vectors (Myzus persicae); seedborne (0.1-5% transmission); mechanical sap transmission.",
        infection_sources="Infected lettuce seed (primary source), volunteer lettuce, wild prickly lettuce and other asteraceous weeds.",
        immediate_actions=[
            "Rogue and destroy infected plants in seedbeds and small plantings",
            "Do NOT save seed from symptomatic plants",
            "Strictly plant certified LMV-tested seed with zero tolerance ('0 in 30,000' seed standard)"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Planting certified index-free seed (0 in 30,000 seeds standard), weed sanitation (prickly lettuce eradication), and host-free periods.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Insecticide vector sprays have limited efficacy for non-persistent viruses; primary control relies on seed indexing and resistance.",
                    application_purpose="Aphid control reduces vector pressure but cannot eliminate non-persistent virus transmission.",
                    limitations="Chemical sprays cannot cure viral infections.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant exclusively certified LMV-indexed seed (tested negative in 30,000 seeds)",
                "Select LMV-resistant lettuce cultivars carrying the mo1^1 or mo1^2 recessive resistance alleles",
                "Maintain a lettuce-free host break period between successive crops"
            ],
            sanitation_measures=[
                "Incorporate crop residues immediately after harvest",
                "Eradicate wild prickly lettuce and composite weeds around fields"
            ],
            resistant_varieties="Many modern crisphead, romaine, and leaf lettuce cultivars carry the mo1 resistance gene."
        ),
        similar_diseases=["lettuce__big_vein_virus", "lettuce__dieback_(tombusvirus)"],
        severity_indicators="Severe foliar puckering, stunted open heads, vein necrosis, unmarketable deformed plants.",
        sources=[SOURCE_UC_IPM, SOURCE_CORNELL, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "maple__tar_spot": DiseaseRecord(
        id="maple__tar_spot",
        canonical_name="Maple Tar Spot",
        crop="maple",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Rhytisma acerinum / Rhytisma punctatum",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Late spring: Small, light yellow-green chlorotic spots (1-2 cm) on the upper surface of maple leaves",
            "Mid-summer to autumn: Spots develop thick, raised, shiny, jet-black tar-like stromatic patches ('tar spots') resembling drops of spilled road tar",
            "The black stroma is surrounded by a narrow, bright yellow chlorotic margin",
            "Severe infections cause premature defoliation in late summer, causing aesthetic landscape damage (rarely causes long-term structural harm to established mature trees)"
        ],
        symptom_progression="Yellow leaf spots in spring -> black raised tar-like patches forming in summer -> premature autumn leaf drop -> ascospores overwintering on fallen leaves.",
        development_conditions="Cool, wet, rainy spring weather during leaf expansion (temperatures 15-22°C), high humidity, dense shade.",
        spread_transmission="Windborne ascospores forcibly ejected from overwintered black tar spots on fallen leaves in spring.",
        infection_sources="Overwintered fallen leaves on the ground beneath maple trees (sole primary source of spring inoculum).",
        immediate_actions=[
            "Rake and completely remove or destroy fallen maple leaves in autumn",
            "Foliar fungicides are rarely required on mature trees because tar spot does not kill established trees",
            "Protect young nursery saplings with preventive fungicides during spring bud break if needed"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Rake, bag, burn, or compost all fallen maple leaves in autumn/winter to break the fungal life cycle completely.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide / Mancozeb / Chlorothalonil",
                    application_purpose="Preventive contact fungicide applied to high-value nursery saplings at bud break, half-leaf expansion, and full leaf expansion.",
                    limitations="Preventive application in spring only; spraying large mature landscape trees is unnecessary and economically unjustified.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Thoroughly rake and remove all fallen maple leaves beneath trees in autumn before winter snow",
                "Ensure proper tree spacing and pruning of surrounding canopy to improve airflow and sunlight"
            ],
            sanitation_measures=[
                "Compost, burn, or dispose of fallen leaves off-site to eliminate overwintered apothecia"
            ],
            resistant_varieties="Norway maple (Acer platanoides) and silver maple (Acer saccharinum) are highly susceptible; sugar maple and red maple are also hosts."
        ),
        similar_diseases=["maple__anthracnose", "maple__phyllosticta_leaf_spot"],
        severity_indicators="Raised jet-black tar-like lesions covering >30% of leaf area, premature late summer defoliation.",
        sources=[SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),
}
