"""
Authoritative Plant Pathology Knowledge: Berry & Small Fruit Crops (15 diseases)
- Blueberry: Anthracnose, Botrytis Blight, Mummy Berry, Rust, Scorch
- Grape: Black Rot, Downy Mildew, Grapevine Leafroll Disease, Leaf Spot (Isariopsis / Pseudocercospora)
- Raspberry: Fire Blight, Gray Mold, Leaf Spot, Yellow Rust
- Strawberry: Anthracnose, Leaf Scorch
Sources: Cornell University, UC IPM, NC State Extension, UF/IFAS, Purdue Extension, USDA ARS, Washington State University.
"""

from knowledge.schema import (
    DiseaseRecord, PathogenType, PlantPart, TreatmentPlan,
    ChemicalControl, CulturalControl, BiologicalControl, PreventionProtocol
)
from knowledge.sources import (
    SOURCE_CORNELL, SOURCE_UC_IPM, SOURCE_NC_STATE, SOURCE_UF_IFAS,
    SOURCE_PURDUE, SOURCE_USDA_ARS, SOURCE_WASHINGTON_STATE
)

BERRY_DISEASES = {
    "blueberry__anthracnose": DiseaseRecord(
        id="blueberry__anthracnose",
        canonical_name="Blueberry Anthracnose (Ripe Rot)",
        crop="blueberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Colletotrichum fioriniae / Colletotrichum acutatum species complex",
        affected_parts=[PlantPart.FRUIT, PlantPart.FLOWER, PlantPart.TWIG, PlantPart.LEAF],
        symptoms=[
            "Ripening or ripe berries soften, shrivel, and puckered around the blossom end",
            "Bright orange to salmon-pink gelatinous spore masses (conidia) erupt across the shriveled fruit surface",
            "Infected blossom clusters turn brown and dry; young twigs develop dark brown cankers",
            "Postharvest rot causes rapid fruit decay, leaking, and severe storage breakdown"
        ],
        symptom_progression="Latent infection during bloom -> fungus remains dormant in green fruit -> explodes into salmon-pink sporulating soft rot as fruit ripens.",
        development_conditions="Warm temperatures (18-28°C), high relative humidity, frequent rain, extended overhead irrigation during bloom and fruit ripening.",
        spread_transmission="Conidia dispersed by rain splash, overhead irrigation, and harvesting machinery/hands.",
        infection_sources="Overwintered twig cankers, infected bud scales, dead flower parts, and mummified berries.",
        immediate_actions=[
            "Prune out dead, diseased, and weak twigs during dormancy to open canopy",
            "Avoid overhead sprinkler irrigation; switch to drip irrigation",
            "Apply protective fungicides from early bloom through harvest",
            "Rapidly cool harvested fruit below 4°C immediately after picking"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Pruning out dead canes, switching to drip irrigation, harvesting at frequent intervals, and rapid post-harvest cooling.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Captan / Ziram",
                    application_purpose="Multi-site protectant fungicide applied from bloom through pre-harvest.",
                    limitations="Preventive only; observe pre-harvest intervals and re-entry guidelines.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Pyraclostrobin / Cyprodinil + Fludioxonil",
                    application_purpose="Translaminar / systemic fungicides applied during bloom and early green fruit stages.",
                    limitations="Rotate FRAC groups (FRAC 11, 9, 12) to manage fungicide resistance.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Foliar bio-fungicide applied during bloom for organic suppression.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Select resistant cultivars with upright, open canopies",
                "Prune annually to maximize sunlight and rapid air drying",
                "Ensure drip irrigation to prevent wetting of blossoms and berries"
            ],
            sanitation_measures=[
                "Prune out and destroy old infected twigs during winter dormancy",
                "Sanitize harvesting lugs and sorting lines"
            ],
            resistant_varieties="Cultivars with lower susceptibility: Elliott, Legacy, Brigitta; highly susceptible: Bluecrop, Jersey."
        ),
        similar_diseases=["blueberry__botrytis_blight", "blueberry__mummy_berry"],
        severity_indicators="Salmon-pink spore masses on softening fruit, blossom blighting, >15% fruit rot at harvest.",
        sources=[SOURCE_NC_STATE, SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "blueberry__botrytis_blight": DiseaseRecord(
        id="blueberry__botrytis_blight",
        canonical_name="Blueberry Botrytis Blight (Gray Mold)",
        crop="blueberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Botrytis cinerea",
        affected_parts=[PlantPart.FLOWER, PlantPart.FRUIT, PlantPart.TWIG, PlantPart.LEAF],
        symptoms=[
            "Blossoms turn brown, water-soaked, and wither rapidly (blossom blight)",
            "Abundant, velvety, brownish-gray powdery mold covers blighted blossoms and ripening fruit",
            "Infection spreads from infected petals into green fruit clusters and young succulent twigs",
            "Leaves show large, brown, water-soaked necrotic blotches; ripe fruit becomes soft, leaks juice, and rots"
        ],
        symptom_progression="Blossom water-soaking -> gray velvety mold coating -> blight travels into twigs and fruit -> soft fruit decay and berry drop.",
        development_conditions="Cool, wet, cloudy, foggy spring weather (temperatures 15-20°C), prolonged blossom wetness (>12 hours), frost-damaged tissue.",
        spread_transmission="Airborne conidia carried by wind currents; splashing rain.",
        infection_sources="Senescing plant debris, dead twigs, decaying weed vegetation, overwintered sclerotia.",
        immediate_actions=[
            "Prune bushes to increase airflow and accelerate blossom drying",
            "Avoid overhead irrigation during flowering",
            "Apply targeted botryticides during bloom periods when wet cool weather is forecast"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Canopy pruning, row weed management, drip irrigation, and timely harvest of ripe fruit.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Cyprodinil + Fludioxonil (Switch) / Fenhexamid (Elevate)",
                    application_purpose="Specialized botryticide fungicides applied at 10% bloom, full bloom, and petal fall.",
                    limitations="Strict resistance management: alternate FRAC groups (FRAC 9+12, 17, 7).",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Captan",
                    application_purpose="Multi-site protectant applied during bloom.",
                    limitations="Preventive application only; adhere to pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens / Streptomyces lydicus",
                    application_method="Foliar bio-fungicide spray applied during bloom.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Prune bushes annually to maintain an open vase shape for optimal wind flow",
                "Protect plants from spring frost injury which creates infection courts",
                "Maintain clean weed-free understory beneath blueberry rows"
            ],
            sanitation_measures=[
                "Remove and destroy blighted twigs and mummified clusters during winter",
                "Sanitize harvest equipment regularly"
            ],
            resistant_varieties="Cultivars with loose flower clusters and rapid petal drop are less prone to blossom blight."
        ),
        similar_diseases=["blueberry__anthracnose", "blueberry__mummy_berry"],
        severity_indicators="Brownish-gray velvety mold on blossoms, blighted flower clusters >20%, twig dieback.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_UC_IPM, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "blueberry__mummy_berry": DiseaseRecord(
        id="blueberry__mummy_berry",
        canonical_name="Blueberry Mummy Berry",
        crop="blueberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Monilinia vaccinii-corymbosi",
        affected_parts=[PlantPart.SHOOT, PlantPart.FLOWER, PlantPart.FRUIT, PlantPart.LEAF],
        symptoms=[
            "Phase 1 (Shoot Blight): Young emerging leaves and flower shoots suddenly wilt, turn brown/black along the midrib, and die ('shepherd's crook')",
            "Blighted shoots develop a sweet-scented tan/gray powdery spore layer that attracts pollinating bees",
            "Phase 2 (Fruit Infection): Infected developing berries look normal initially, but turn salmon-pink, cream, or whitish-tan instead of ripening blue",
            "Infected fruit becomes hard, shriveled, pumpkin-shaped, drops to the ground, and forms a hard, black, pumpkin-ridged overwintering pseudosclerotium ('mummy')"
        ],
        symptom_progression="Apothecia cup emergence in spring -> ascospores infect young shoots -> conidia carried by bees to open flowers -> infected berries turn pink/white, harden, shrivel, and drop as black mummies.",
        development_conditions="Cool, wet spring weather (10-18°C), standing soil moisture around bush crowns, prolonged leaf wetness.",
        spread_transmission="Phase 1: windborne ascospores from ground mummies. Phase 2: conidia carried by pollinating insects (bees) and wind to open flower stigmas.",
        infection_sources="Overwintered pseudosclerotia (mummies) on the soil surface beneath blueberry bushes.",
        immediate_actions=[
            "Rake, disk, or cover the soil beneath bushes with 5 cm (2 inches) of fresh mulch to bury apothecia before bud break",
            "Apply protective fungicides at green tip and continue through bloom",
            "Remove and destroy shoot strikes (blighted shoots) if feasible"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Soil management: shallow disking or raking between rows, covering ground with 5 cm mulch to prevent mushroom cup (apothecia) emergence.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Indar (Fenbuconazole) / Proline (Prothioconazole) / Difenoconazole",
                    application_purpose="Systemic DMI fungicides applied from green tip to bloom for shoot blight and blossom infection protection.",
                    limitations="Observe resistance guidelines; rotate with multi-site protectants (Captan/Ziram); obey label limits.",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Ziram / Captan",
                    application_purpose="Protectant contact fungicide applied at bud break to suppress shoot blight.",
                    limitations="Preventive application only.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens",
                    application_method="Foliar bio-fungicide applied at bloom.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Apply fresh bark/sawdust mulch (5 cm depth) in early spring before bud swell to bury overwintering mummies",
                "Cultivate or disk row middles to disturb and bury apothecial cups",
                "Plant cultivars with high field resistance or staggered bloom periods"
            ],
            sanitation_measures=[
                "Rake and remove fallen mummified berries from beneath plants"
            ],
            resistant_varieties="Cultivars with high resistance: Jersey, Duke, Elliott; susceptible: Rubel, Blueray, Bluecrop."
        ),
        similar_diseases=["blueberry__anthracnose", "blueberry__botrytis_blight"],
        severity_indicators="Shepherd's crook shoot strikes, hard pinkish-white mummified berries dropping before harvest.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "blueberry__rust": DiseaseRecord(
        id="blueberry__rust",
        canonical_name="Blueberry Rust",
        crop="blueberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Thekopsora minima (syn. Pucciniastrum vaccinii)",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT],
        symptoms=[
            "Small, circular, yellowish to reddish-brown chlorotic spots on the upper leaf surface",
            "Bright yellow to orange-red powdery pustules (uredinia) erupting on the corresponding lower leaf surface",
            "Pustules turn dark brown to purplish-black late in the season as telia form",
            "Severe infections cause widespread premature defoliation, reducing floral bud set for the following season and causing berry drop"
        ],
        symptom_progression="Yellow leaf flecks -> bright orange-yellow uredinia on lower surface -> leaf browning -> severe premature defoliation -> reduced flower bud development.",
        development_conditions="Warm temperatures (20-28°C), high humidity, frequent rainfall, presence of hemlock (Tsuga spp.) as alternate host in northern zones; continuous cycling on evergreen Southern highbush in subtropical zones.",
        spread_transmission="Windborne urediniospores, splashing rain, contaminated farm clothing/equipment.",
        infection_sources="Overwintering uredinia on evergreen foliage in southern regions; aeciospores from alternate hemlock hosts in northern regions.",
        immediate_actions=[
            "Apply targeted rust fungicides (DMI triazoles or strobilurins) post-harvest or at first symptom detection",
            "Prune bushes to increase airflow through the canopy",
            "Avoid overhead irrigation in late afternoon"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Canopy pruning for air circulation, drip irrigation, and removing alternate hemlock hosts within 1 km in northern regions.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Difenoconazole + Azoxystrobin (Abound / Quadris Top)",
                    application_purpose="Systemic foliar spray applied post-harvest or when rust pustules first appear on lower leaves.",
                    limitations="Strict resistance management; rotate FRAC 3 and 11; observe label limits.",
                    source_id=SOURCE_UF_IFAS.id
                ),
                ChemicalControl(
                    active_ingredient="Pyraclostrobin (Cabrio) / Fenbuconazole (Indar)",
                    application_purpose="Foliar rust suppression during summer and post-harvest vegetative flushes.",
                    limitations="Observe pre-harvest and post-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Select resistant or tolerant Southern highbush and Northern highbush cultivars",
                "Maintain optimal plant spacing and annual canopy pruning",
                "Ensure drip irrigation to prevent foliar wetting"
            ],
            sanitation_measures=[
                "In evergreen production systems, use post-harvest pruning and sanitation sprays to reduce overwintering spore loads"
            ],
            resistant_varieties="Cultivar susceptibility varies significantly; Southern highbush cultivars require proactive post-harvest rust programs."
        ),
        similar_diseases=["blueberry__scorch", "blueberry__leaf_spot"],
        severity_indicators="Bright orange pustules covering >25% of lower leaf surface, premature defoliation >30% before autumn.",
        sources=[SOURCE_UF_IFAS, SOURCE_NC_STATE, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "blueberry__scorch": DiseaseRecord(
        id="blueberry__scorch",
        canonical_name="Blueberry Scorch Virus (BlScV)",
        crop="blueberry",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Blueberry scorch virus (BlScV, Carlavirus)",
        affected_parts=[PlantPart.FLOWER, PlantPart.LEAF, PlantPart.TWIG, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Sudden, complete blighting and death of blossom clusters and young leaves during bloom ('scorched' look)",
            "Dead brown blossoms and leaves remain tenaciously attached to the twigs throughout the summer",
            "Twigs may develop a slight chlorotic yellowing or red line pattern on leaves in some cultivars",
            "Progressive decline over 2-4 years, extreme yield loss, and overall bush stunting"
        ],
        symptom_progression="Blossom and young shoot blight during bloom -> dead foliage persists on twigs -> systemic spread through crown -> complete crop loss and bush decline.",
        development_conditions="Presence of blueberry aphid vectors (Ericaphis fimbriata) in spring and early summer.",
        spread_transmission="Transmitted non-persistently by blueberry aphids (Ericaphis spp.) and through infected propagation stock.",
        infection_sources="Infected blueberry bushes, wild Vaccinium species, infected nursery cuttings.",
        immediate_actions=[
            "Test symptomatic bushes via ELISA or PCR to confirm BlScV",
            "DO NOT merely prune blighted twigs (the virus is systemic in the root system)",
            "Spray bush with aphicide to kill aphid vectors, then dig out and destroy entire bush including root ball"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Total roguing and destruction of virus-positive bushes following aphicide treatment; intensive aphid vector management.",
                    source_id=SOURCE_WASHINGTON_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Acetamiprid / Spirotetramat",
                    application_purpose="Targeted insecticide applied in spring to control blueberry aphid vectors (Ericaphis fimbriata).",
                    limitations="Strictly protect pollinators; do not apply during active bloom when bees are foraging.",
                    source_id=SOURCE_WASHINGTON_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant exclusively certified virus-tested, disease-free nursery stock",
                "Conduct annual farm-wide visual surveys during bloom and ELISA testing",
                "Establish strict quarantine barriers preventing uncertified plant movement"
            ],
            sanitation_measures=[
                "Eradicate virus-infected bushes immediately upon lab confirmation",
                "Sanitize mechanical harvesting and pruning equipment"
            ],
            resistant_varieties="No cultivars are fully immune; some cultivars (e.g., Jersey, Draper) show severe blighting, while others show latent tolerance but act as virus reservoirs."
        ),
        similar_diseases=["blueberry__shock_virus", "blueberry__botrytis_blight", "blueberry__mummy_berry"],
        severity_indicators="Sudden blossom death during bloom with dead leaves persisting on twigs, positive ELISA test, severe bush decline.",
        sources=[SOURCE_WASHINGTON_STATE, SOURCE_NC_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "grape__black_rot": DiseaseRecord(
        id="grape__black_rot",
        canonical_name="Grape Black Rot",
        crop="grape",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Phyllosticta ampelicida (teleomorph Guignardia bidwellii)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT, PlantPart.SHOOT],
        symptoms=[
            "Small, circular, reddish-brown spots on leaves that enlarge up to 2-10 mm",
            "Spots develop a distinct dark brown border and tiny, pimple-like black pycnidia arranged in a prominent ring near the lesion margin",
            "Shoot and cane lesions are elongated, dark brown to black, sunken cankers",
            "Infected berries develop a small brown spot that rapidly rots the entire berry within 48 hours; berries shrivel into hard, black, wrinkled, mummified raisins covered with black pycnidia"
        ],
        symptom_progression="Circular leaf spots with pycnidia rings -> shoot cankers -> berry rot -> complete mummification into hard wrinkled black berries ('raisins').",
        development_conditions="Warm, wet weather (21-27°C optimum), continuous leaf/fruit wetness (>6-12 hours), dense unpruned canopies.",
        spread_transmission="Ascospores and pycnidiospores dispersed by wind and rain splashing.",
        infection_sources="Overwintered mummified berries hanging on trellises or lying on the ground, cane cankers.",
        immediate_actions=[
            "Remove and destroy all mummified berries from vine trellises and ground",
            "Prune out diseased canes during winter dormancy",
            "Apply protective or DMI triazole fungicides starting at early shoot growth (1-3 inch shoots) through 4 weeks post-bloom"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Myclobutanil (Rally) / Tebuconazole",
                    application_purpose="Systemic DMI fungicide with 48-72 hour post-infection 'reachback' curative activity.",
                    limitations="Apply promptly following an infection period; rotate FRAC 3 to manage resistance.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Thorough canopy management (shoot positioning, leaf pulling around fruit zones), and rigorous removal of overwintered mummies.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb / Captan",
                    application_purpose="Multi-site protectant contact fungicide applied from bud break to bloom.",
                    limitations="Preventive only; observe pre-harvest interval (Mancozeb 66-day PHI on grapes).",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Pyraclostrobin",
                    application_purpose="Strobilurin fungicide providing excellent black rot protection.",
                    limitations="Rotate FRAC 11 with FRAC 3 and multi-site protectants.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Implement open canopy training systems (e.g., VSP, Scott Henry) to maximize sun and air exposure",
                "Perform shoot thinning and selective leaf removal in the fruiting zone immediately post-bloom",
                "Cultivate or disk under vine rows before bud break to bury fallen mummies"
            ],
            sanitation_measures=[
                "Hand-strip all mummified grape clusters from vine trellises during winter pruning and burn/bury them",
                "Prune out infected cane cankers"
            ],
            resistant_varieties="Vitis vinifera cultivars are generally highly susceptible; certain French-American hybrids (e.g., Chancellor, Cayuga White) have moderate tolerance."
        ),
        similar_diseases=["grape__downy_mildew", "grape__anthracnose", "grape__botrytis_bunch_rot"],
        severity_indicators="Black wrinkled mummified berries covered in pycnidia, leaf spots with ringed pycnidia, >20% fruit cluster loss.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "grape__downy_mildew": DiseaseRecord(
        id="grape__downy_mildew",
        canonical_name="Grape Downy Mildew",
        crop="grape",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Plasmopara viticola",
        affected_parts=[PlantPart.LEAF, PlantPart.FLOWER, PlantPart.FRUIT, PlantPart.SHOOT],
        symptoms=[
            "Yellowish, oily, translucent chlorotic spots on the upper leaf surface ('oil spots')",
            "Brilliant white, dense, cottony/downy fungal-like sporulation on the corresponding lower leaf surface in humid conditions",
            "Infected flower clusters and young berries curl, turn brown, wither, and become covered with white downy mold",
            "Older infected berries turn dull grayish-brown, shrivel, harden, and shell off the cluster ('leather rot')"
        ],
        symptom_progression="Upper leaf 'oil spots' -> brilliant white cottony down on underside -> blossom/cluster blighting -> berry shriveling and leather rot -> extensive late-season defoliation.",
        development_conditions="Warm, humid, rainy weather (the '10-10-10' rule: 10 mm rain, temperature >=10°C, shoot growth >=10 cm), high relative humidity (>95% at night).",
        spread_transmission="Windborne and rain-splashed sporangia; overwintering oospores in fallen leaf litter.",
        infection_sources="Decomposing leaf litter in vineyard soil harboring overwintered oospores.",
        immediate_actions=[
            "Pull leaves around fruiting zone to improve air circulation and speed drying",
            "Apply targeted anti-oomycete fungicides immediately upon weather-risk alerts",
            "Avoid overhead vineyard irrigation"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Cymoxanil (Curzate) + Mancozeb / Captan",
                    application_purpose="Curative kickback anti-oomycete fungicide with 24-48 hours post-infection activity.",
                    limitations="Short residual; must be tank-mixed with a multi-site protectant.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Canopy management (leaf pulling, shoot hedging), soil drainage, and vineyard floor cover crop mowing.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb / Captan / Copper Hydroxide",
                    application_purpose="Standard preventive protectant contact fungicides applied on a 7-14 day schedule from 4-inch shoots through veraison.",
                    limitations="Preventive only; observe 66-day PHI for Mancozeb; monitor copper phytotoxicity on sensitive cultivars.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Mandipropamid (Revus) / Cyazofamid (Ranman) / Oxathiapiprolin (Orondis)",
                    application_purpose="Specialized translaminar/systemic oomycete fungicides for intense downy mildew pressure.",
                    limitations="Strict resistance management: alternate FRAC groups (FRAC 40, 21, 49).",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Phosphorous Acid (Potassium Phosphite)",
                    application_purpose="Systemic fungicide with excellent translaminar movement and plant defense stimulation.",
                    limitations="Apply preventively or at early disease onset; do not tank mix with copper.",
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
                "Train vines on upright trellis systems and position shoots vertically (VSP)",
                "Pull leaves in the fruiting zone 2-3 weeks post-bloom to accelerate cluster drying",
                "Ensure vineyard rows align with prevailing wind directions to facilitate canopy ventilation"
            ],
            sanitation_measures=[
                "Disk or chop fallen leaf litter in autumn to accelerate oospore decomposition",
                "Mow cover crops regularly to lower humidity beneath vines"
            ],
            resistant_varieties="Vitis vinifera cultivars are highly susceptible; interspecific hybrids (e.g., Norton, Traminette, Frontenac) have superior field tolerance."
        ),
        similar_diseases=["grape__powdery_mildew", "grape__black_rot"],
        severity_indicators="Brilliant white downy sporulation on leaf underside and berry clusters, severe defoliation before veraison.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_UC_IPM, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "grape__grapevine_leafroll_disease": DiseaseRecord(
        id="grape__grapevine_leafroll_disease",
        canonical_name="Grapevine Leafroll Disease (GLD)",
        crop="grape",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Grapevine leafroll-associated viruses (GLRaV-1, GLRaV-3, GLRaV-4 complex; Closteroviridae)",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Red cultivars: Interveinal leaf areas turn dark red to purple in late summer/autumn, while the primary and secondary veins remain distinctly green",
            "White cultivars: Interveinal leaf areas show mild chlorosis, yellowing, or slight metallic sheen (veins remain green)",
            "Leaf margins roll downward and cup under, becoming thick, leathery, and brittle",
            "Fruit clusters show delayed ripening, uneven color development, reduced soluble solids (Brix), high acidity, and yield reduction up to 20-40%"
        ],
        symptom_progression="Mid-summer downward leaf curling -> intense red/purple interveinal coloration (green veins) in red cultivars -> delayed fruit ripening and reduced sugar accumulation -> progressive vineyard decline.",
        development_conditions="Presence of soft scale insects and mealybugs (Pseudococcus maritimus, Planococcus ficus); vegetative propagation.",
        spread_transmission="Vectored by mealybugs and soft scales; spread long distances through infected dormant cuttings and rootstocks.",
        infection_sources="Infected rootstocks, infected budwood cuttings, mealybug populations in neighboring infected vineyards.",
        immediate_actions=[
            "Test symptomatic vines using ELISA or RT-PCR to confirm specific GLRaV species",
            "Map infected vines and rogue them out if overall vineyard infection rate is low (<25%)",
            "Implement aggressive mealybug/scale insect control programs"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Vineyard mapping, roguing of infected vines (when incidence is <25%), replanting with certified clean stock, and controlling mealybug vectors.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Spirotetramat (Movento) / Dinotefuran",
                    application_purpose="Systemic insecticide applied post-bloom to control vine mealybug and grape mealybug crawlers.",
                    limitations="Follow pollinator protection and resistance management guidelines.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Anagyrus pseudococci / Cryptolaemus montrouzieri",
                    application_method="Parasitoid wasps and mealybug destroyer beetles released for biological vector suppression.",
                    source_id=SOURCE_UC_IPM.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant exclusively certified virus-tested nursery stock (Protocol 2010 / FPS certified)",
                "Deploy pheromone traps to monitor and detect male mealybugs early in the season",
                "Quarantine new planting blocks and avoid taking cuttings from unverified field selections"
            ],
            sanitation_measures=[
                "Disinfect harvesting machines and equipment when moving between vineyard blocks",
                "Remove and burn virus-positive vines including root crowns"
            ],
            resistant_varieties="All Vitis vinifera cultivars are susceptible to GLRaVs; rootstocks can be asymptomatic carriers."
        ),
        similar_diseases=["grape__grapevine_red_blotch_disease", "grape__potassium_deficiency"],
        severity_indicators="Severe downward leaf rolling, dark red interveinal coloration with green veins, Brix reduction >3-4 degrees, uneven cluster ripening.",
        sources=[SOURCE_UC_IPM, SOURCE_CORNELL, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "grape__leaf_spot": DiseaseRecord(
        id="grape__leaf_spot",
        canonical_name="Grape Leaf Spot (Isariopsis / Pseudocercospora Leaf Blight)",
        crop="grape",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Pseudocercospora vitis (syn. Isariopsis clavispora / Phaeoisariopsis vitis)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Large, irregular to angular, dark brown to black necrotic blotches on leaves",
            "Lesions develop a prominent yellowish to reddish-brown border",
            "Underside of spots exhibits a dark olive-brown to black velvety coating of fungal conidiophores",
            "Severe infection late in the season causes extensive leaf browning, curling, premature defoliation, and sunscald of grape clusters"
        ],
        symptom_progression="Small dark leaf spots -> expanding angular dark blotches with olive velvety mold on underside -> premature canopy defoliation -> weakened vines.",
        development_conditions="Warm, humid, rainy weather in mid to late summer (24-30°C), shaded dense canopies, overhead moisture.",
        spread_transmission="Conidia dispersed by wind currents and splashing rain.",
        infection_sources="Overwintered fallen leaves on the vineyard floor and dormant cane residues.",
        immediate_actions=[
            "Prune canopy and pull leaves in fruit zones to increase sunlight and air penetration",
            "Apply protective or systemic foliar fungicides in mid to late summer",
            "Clear fallen leaf debris after harvest"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Canopy shoot thinning, leaf pulling, and good vineyard floor sanitation to reduce humidity and inoculum.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb / Copper Hydroxide",
                    application_purpose="Contact protectant fungicide applied during summer months.",
                    limitations="Observe pre-harvest intervals (Mancozeb 66-day PHI).",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Pyraclostrobin",
                    application_purpose="Systemic strobilurin fungicide for comprehensive foliar disease management.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Maintain open canopy architecture through vertical shoot positioning (VSP)",
                "Avoid overhead irrigation",
                "Ensure balanced soil nutrition"
            ],
            sanitation_measures=[
                "Chop or incorporate fallen leaves after harvest",
                "Prune out dead canes during winter"
            ],
            resistant_varieties="Cultivar susceptibility varies; Muscadine and certain native American grape hybrids show strong field tolerance."
        ),
        similar_diseases=["grape__black_rot", "grape__anthracnose"],
        severity_indicators="Large angular black blotches with olive velvety underside sporulation, defoliation >25% in late summer.",
        sources=[SOURCE_NC_STATE, SOURCE_CORNELL, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "raspberry__fire_blight": DiseaseRecord(
        id="raspberry__fire_blight",
        canonical_name="Raspberry Fire Blight (Cane and Shoot Blight)",
        crop="raspberry",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Erwinia amylovora (Rubus-specific strain)",
        affected_parts=[PlantPart.SHOOT, PlantPart.CANE, PlantPart.FLOWER, PlantPart.FRUIT],
        symptoms=[
            "Shoot tips wilt, turn dark brown to black, and curl over into a characteristic 'shepherd's crook'",
            "Blighted leaves, flowers, and young fruits turn dark brown to black and remain tenaciously attached to the canes",
            "In warm, humid weather, milky to amber-colored droplets of bacterial ooze exude from blighted cane surfaces",
            "Dark, water-soaked, purple-black cankers girdle primocanes and floricanes, causing complete cane collapse and berry drying"
        ],
        symptom_progression="Flower infection -> shepherd's crook tip wilt -> bacterial ooze on canes -> girdling stem cankers -> complete cane dieback and dried black berries.",
        development_conditions="Warm, humid, rainy weather during bloom (temperatures 18-28°C), high humidity (>80%), heavy dew, hail or insect wounding.",
        spread_transmission="Rain splash, wind-blown mist, pollinating insects (bees, flies), and contaminated pruning shears.",
        infection_sources="Overwintering cane cankers and nearby infected rosaceous hosts (apples, pears, wild brambles).",
        immediate_actions=[
            "Prune out infected cane tips immediately, cutting at least 20-30 cm (8-12 inches) below visible blight into healthy wood",
            "Disinfect pruning shears between EVERY cut in 70% alcohol or 10% bleach",
            "Apply protective copper bactericide during dormancy and early bloom"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Surgical pruning of blighted canes 20-30 cm below visible symptoms during dry weather; burn or bag all clippings immediately.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Avoid excessive nitrogen fertilization that produces lush succulent shoot tips; maintain narrow hedgerows for ventilation.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide / Copper Oxychloride",
                    application_purpose="Bactericide protectant applied at delayed dormant and early bloom stages.",
                    limitations="Preventive application; avoid applying during hot sunny weather to prevent foliar phytotoxicity.",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Streptomycin (Agricultural grade)",
                    application_purpose="Antibiotic spray applied during bloom when fire blight forecasting models indicate severe infection risk.",
                    limitations="Strictly restricted; check regional regulations; rotate to prevent bacterial antibiotic resistance.",
                    source_id=SOURCE_WASHINGTON_STATE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus subtilis (strain QST 713) / Bacillus amyloliquefaciens",
                    application_method="Foliar bio-bactericide spray applied during bloom to colonize flowers before bacterial arrival.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Maintain narrow hedgerows (30-45 cm width) to maximize air movement and rapid drying",
                "Apply moderate, balanced nitrogen fertilizer to prevent overly vigorous, susceptible shoot growth",
                "Use drip irrigation to prevent wetting cane foliage and blooms"
            ],
            sanitation_measures=[
                "Cut out and burn all overwintered cankered canes during winter pruning",
                "Disinfect pruning tools constantly with disinfectant"
            ],
            resistant_varieties="Cultivars show varying susceptibility; Boyne, Killarney, and Latham exhibit moderate tolerance; Autumn Bliss is susceptible."
        ),
        similar_diseases=["raspberry__cane_canker", "raspberry__spur_blight"],
        severity_indicators="Shepherd's crook cane curling, bacterial ooze exudate, girdling dark purple cankers, dried blackened berries.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_WASHINGTON_STATE, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "raspberry__gray_mold": DiseaseRecord(
        id="raspberry__gray_mold",
        canonical_name="Raspberry Gray Mold (Botrytis Fruit Rot)",
        crop="raspberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Botrytis cinerea",
        affected_parts=[PlantPart.FLOWER, PlantPart.FRUIT, PlantPart.CANE, PlantPart.LEAF],
        symptoms=[
            "Individual drupelets or entire ripening berries become soft, pale, water-soaked, and watery",
            "A dense, fuzzy, velvety brownish-gray fungal mold rapidly envelops the berry surface",
            "Infected flowers turn brown and die; cane lesions are pale tan to bleached white with tiny black overwintering sclerotia",
            "Postharvest breakdown occurs rapidly, causing harvested berries to collapse into a moldy mass within 24-48 hours"
        ],
        symptom_progression="Blossom infection -> latent colonization -> gray fuzzy mold covering ripe fruit -> cane lesions with black sclerotia -> postharvest fruit melt.",
        development_conditions="Cool to moderate temperatures (15-22°C), high humidity (>85%), prolonged rain during bloom and harvest, dense unpruned canopies.",
        spread_transmission="Airborne conidia carried by wind; rain splashing; physical contact between healthy and diseased berries.",
        infection_sources="Overwintered sclerotia on canes, dead plant debris in the mulch, senescing flower parts.",
        immediate_actions=[
            "Harvest fruit frequently (daily or every 2 days) and handle gently",
            "Cull and discard moldy berries immediately (do not leave in planting)",
            "Cool harvested fruit to 0.5-2°C immediately upon picking",
            "Apply targeted botryticides during bloom periods"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Narrow hedgerow pruning (30-45 cm), aggressive cane thinning (4-6 canes/foot), drip irrigation, clean picking, and immediate cold chain storage.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Cyprodinil + Fludioxonil (Switch) / Fenhexamid (Elevate) / Penthiopyrad (Fontelis)",
                    application_purpose="Specialized botryticide fungicides applied at 5-10% bloom, full bloom, and pre-harvest.",
                    limitations="Strict resistance management: rotate FRAC groups (FRAC 9+12, 17, 7); observe pre-harvest intervals.",
                    source_id=SOURCE_CORNELL.id
                ),
                ChemicalControl(
                    active_ingredient="Captan",
                    application_purpose="Broad-spectrum multi-site protectant contact fungicide.",
                    limitations="Preventive only; observe re-entry and pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens / Aureobasidium pullulans",
                    application_method="Bio-fungicide applied during bloom and pre-harvest for organic fruit rot management.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Maintain narrow hedgerows (maximum 45 cm wide) with good trellis support",
                "Thin canes to allow abundant sunlight and wind penetration throughout the canopy",
                "Use drip irrigation and maintain clean weed-free understories"
            ],
            sanitation_measures=[
                "Prune out spent floricanes immediately after harvest completion and destroy them",
                "Remove all overripe or rotten fruit from the field"
            ],
            resistant_varieties="Cultivars with firm fruit and upright open canopies (e.g., Heritage, Caroline, Nova) suffer less fruit rot."
        ),
        similar_diseases=["raspberry__leaf_spot", "raspberry__anthracnose"],
        severity_indicators="Fuzzy brownish-gray sporulation on fruit, >15% pre-harvest fruit rot, rapid postharvest collapse.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),

    "raspberry__leaf_spot": DiseaseRecord(
        id="raspberry__leaf_spot",
        canonical_name="Raspberry Leaf Spot (Sphaerulina Leaf Spot)",
        crop="raspberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Sphaerulina westendorpii (syn. Septoria rubi / Mycosphaerella rubi)",
        affected_parts=[PlantPart.LEAF, PlantPart.CANE],
        symptoms=[
            "Small, circular to angular spots (1-3 mm) on leaves with light brown to ash-gray centers and a dark purple to reddish border",
            "Tiny black specks (pycnidia) are visible in the pale center of mature spots",
            "Spots coalesce to form large necrotic patches; leaves turn yellow and drop prematurely (severe defoliation starting from lower canes)",
            "Cane lesions are small, dark, circular to elliptical spots with light gray centers"
        ],
        symptom_progression="Small purple-bordered spots on lower leaves -> gray centers with pycnidia -> leaf chlorosis -> progressive upward defoliation -> reduced winter hardiness.",
        development_conditions="Warm, wet, humid weather (20-26°C), frequent rains, overhead irrigation, dense weed-filled rows.",
        spread_transmission="Pycnidiospores and ascospores dispersed by rain splash and wind currents.",
        infection_sources="Infected fallen leaves on the ground, cane lesions, wild Rubus species.",
        immediate_actions=[
            "Prune out old fruiting floricanes immediately after harvest",
            "Thin primocanes to improve airflow through the row",
            "Apply protective fungicides starting before bloom and continuing post-harvest"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Pruning out old floricanes post-harvest, trellising, keeping hedgerows narrow, and destroying fallen leaf litter.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Captan",
                    application_purpose="Broad-spectrum contact protectant fungicide applied from early green leaf emergence through harvest.",
                    limitations="Preventive application only; observe pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Pyraclostrobin (Cabrio) / Azoxystrobin (Abound)",
                    application_purpose="Systemic strobilurin fungicide providing excellent leaf spot and cane disease control.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Dormant and post-harvest sanitation spray.",
                    limitations="Do not apply during active green growth under slow drying conditions to avoid leaf burn.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Maintain narrow hedgerow width and optimal cane density",
                "Ensure drip irrigation to prevent wetting canopy foliage",
                "Eradicate wild blackberries and raspberries near cultivated plantings"
            ],
            sanitation_measures=[
                "Cut floricanes to the ground immediately after harvest and remove from field",
                "Shred or incorporate fallen leaves"
            ],
            resistant_varieties="Cultivars show varying susceptibility; maintaining open canopy architecture is the primary defense."
        ),
        similar_diseases=["raspberry__yellow_rust", "raspberry__anthracnose"],
        severity_indicators="Ash-gray spots with purple borders covering >30% of leaf area, extensive lower cane defoliation.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE],
        quality_level="HIGH"
    ),

    "raspberry__yellow_rust": DiseaseRecord(
        id="raspberry__yellow_rust",
        canonical_name="Raspberry Yellow Rust",
        crop="raspberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Phragmidium rubi-idaei",
        affected_parts=[PlantPart.LEAF, PlantPart.CANE, PlantPart.FRUIT],
        symptoms=[
            "Spring: Small, bright yellow to orange-yellow aecial pustules on the upper surface of emerging primocane leaves",
            "Summer: Masses of powdery golden-yellow to bright orange urediniospores erupting on the lower leaf surface",
            "Severely infected leaves turn yellow, brown, and drop prematurely, causing extensive mid-summer defoliation",
            "Autumn: Pustules turn dark brown to black as teliospores form; infected canes develop dark cankers, and fruit may become seedy and dry"
        ],
        symptom_progression="Upper leaf yellow aecial spots in spring -> bright orange-yellow powdery uredinia on leaf undersides in summer -> defoliation -> black teliospores in autumn.",
        development_conditions="Cool to moderate temperatures (15-21°C), high humidity, frequent rain, dense weed-choked canopies.",
        spread_transmission="Windborne urediniospores and teliospores; autoecious (completes entire life cycle on red raspberry).",
        infection_sources="Overwintered teliospores on old cane stubs, fallen leaves, and dormant cane bark.",
        immediate_actions=[
            "Prune out old fruiting canes down to the crown immediately after harvest",
            "Apply delayed-dormant lime sulfur spray before green tip",
            "Apply protective or DMI fungicides upon first appearance of yellow pustules"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Strict removal of old floricanes right at soil level, thinning primocanes, and improving air circulation.",
                    source_id=SOURCE_WASHINGTON_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Liquid Lime Sulfur",
                    application_purpose="Delayed-dormant eradicant spray applied before green tissue emerges to kill overwintering teliospores.",
                    limitations="Apply strictly during dormancy before bud swell; avoid drift.",
                    source_id=SOURCE_WASHINGTON_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Myclobutanil / Pyraclostrobin",
                    application_purpose="Foliar fungicides applied in spring when aecial pustules first appear on young leaves.",
                    limitations="Rotate FRAC groups (FRAC 3 and 11); observe pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant yellow rust-resistant red raspberry cultivars",
                "Ensure narrow hedgerows and remove non-productive weak canes",
                "Use drip irrigation to keep canopy foliage dry"
            ],
            sanitation_measures=[
                "Cut old floricanes completely flush with the ground (leave no stubs) and destroy them",
                "Clear fallen leaves from row bases"
            ],
            resistant_varieties="Resistant cultivars: Meeker, Willamette, Chilliwack; highly susceptible: Glen Moy, Tulameen, Fairview."
        ),
        similar_diseases=["raspberry__leaf_spot", "raspberry__orange_rust_(gymnoconia)"],
        severity_indicators="Bright orange-yellow powdery spore masses covering leaf undersides, premature defoliation >30%, cane lesions.",
        sources=[SOURCE_WASHINGTON_STATE, SOURCE_CORNELL, SOURCE_NC_STATE],
        quality_level="HIGH"
    ),

    "strawberry__anthracnose": DiseaseRecord(
        id="strawberry__anthracnose",
        canonical_name="Strawberry Anthracnose (Crown Rot and Fruit Rot)",
        crop="strawberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Colletotrichum acutatum / Colletotrichum gloeosporioides / Colletotrichum fragariae",
        affected_parts=[PlantPart.FRUIT, PlantPart.CROWN, PlantPart.PETIOLE, PlantPart.RUNNER],
        symptoms=[
            "Fruit: Circular, sunken, firm, dark brown to black spots on green and ripe berries",
            "Under humid conditions, masses of salmon-pink to orange gelatinous spores erupt in the sunken fruit lesions",
            "Crowns: Plants suddenly wilt and collapse during warm weather; cutting the crown reveals a firm, marbled reddish-brown internal rot",
            "Petioles and runners: Elongated, sunken, dark brown to black girdling lesions ('craters')"
        ],
        symptom_progression="Petiole/runner craters -> salmon-pink sporulating sunken fruit rot -> crown vascular invasion -> sudden permanent plant wilt and death.",
        development_conditions="Warm, humid, rainy weather (temperatures 25-30°C), splashing rain, overhead sprinkler irrigation, plastic mulch.",
        spread_transmission="Water-splashed conidia, farm equipment, workers handling wet plants, infected nursery transplants.",
        infection_sources="Infected nursery runner plants, crop debris in soil, volunteer strawberry plants, wild weed hosts.",
        immediate_actions=[
            "Remove and destroy infected collapsing plants and rotten fruit immediately",
            "Avoid overhead irrigation; switch to drip irrigation under plastic mulch",
            "Apply targeted fungicides (e.g., captan, azoxystrobin, or fludioxonil) immediately upon disease detection"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Use drip irrigation, plant on raised plastic-mulched beds, avoid working in wet foliage, and rogue out wilting plants.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Captan",
                    application_purpose="Standard multi-site contact protectant applied on a 7-10 day schedule during bloom and fruiting.",
                    limitations="Preventive application only; observe pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Cyprodinil + Fludioxonil (Switch) / Azoxystrobin (Abound)",
                    application_purpose="Systemic / translaminar fungicides for crown and fruit rot protection during warm, wet periods.",
                    limitations="Strict resistance management: rotate FRAC groups (FRAC 9+12, 11, 7).",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens (strain D747)",
                    application_method="Foliar bio-fungicide applied preventively to protect blooms and green fruit.",
                    source_id=SOURCE_PURDUE.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified disease-free, pathogen-tested nursery runner plants",
                "Dip bare-root transplants in preventive fungicide or hot-water treatment prior to planting",
                "Grow on raised plastic-mulched beds with straw in furrow middles to suppress rain splash"
            ],
            sanitation_measures=[
                "Rogue out and destroy infected mother plants and runners promptly",
                "Sanitize harvesting trays and equipment"
            ],
            resistant_varieties="Cultivars show varying resistance; Sweet Charlie and Florida Radiance show moderate tolerance; Camarosa and Chandler are susceptible."
        ),
        similar_diseases=["strawberry__botrytis_fruit_rot", "strawberry__phytophthora_crown_rot"],
        severity_indicators="Sunken firm fruit rot with salmon-pink spore masses, marbled reddish-brown crown rot, sudden permanent plant collapse.",
        sources=[SOURCE_UF_IFAS, SOURCE_NC_STATE, SOURCE_UC_IPM, SOURCE_CORNELL],
        quality_level="HIGH"
    ),

    "strawberry__leaf_scorch": DiseaseRecord(
        id="strawberry__leaf_scorch",
        canonical_name="Strawberry Leaf Scorch",
        crop="strawberry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Diplocarpon earlianum (anamorph Marssoniella fragariae)",
        affected_parts=[PlantPart.LEAF, PlantPart.PETIOLE, PlantPart.CALYX, PlantPart.RUNNER],
        symptoms=[
            "Numerous small, irregular, dark purple to purplish-black spots (1-5 mm) scattered across the upper leaf surface",
            "Unlike common leaf spot, scorch spots remain dark purple throughout and DO NOT develop white or gray centers",
            "Spots enlarge, coalesce, and tissue between spots turns dark purplish-brown to bright red, then dries and curls up",
            "Entire leaf blades appear burned or scorched; calyx lobes develop purple spots and dry up, reducing fruit marketability"
        ],
        symptom_progression="Irregular purple flecks -> coalescing purple patches -> leaf tissue browning and crisping ('scorched' canopy) -> calyx blighting ('brown cap').",
        development_conditions="Moderate to warm temperatures (18-25°C), frequent rains, overhead sprinkler irrigation, extended leaf wetness (>8-12 hours).",
        spread_transmission="Conidia and ascospores dispersed by rain splash and overhead irrigation.",
        infection_sources="Overwintered infected green leaves and dead crop debris in the strawberry bed.",
        immediate_actions=[
            "Mow and renovate perennial strawberry beds immediately post-harvest",
            "Eliminate overhead irrigation and use drip watering",
            "Apply protective fungicides in spring and during post-harvest renovation"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Bed renovation immediately after final harvest (mowing foliage, narrowing rows, fertilizing), and switching to drip irrigation.",
                    source_id=SOURCE_CORNELL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Captan / Thiram",
                    application_purpose="Contact protectant fungicide applied from early spring emergence through harvest.",
                    limitations="Preventive application only; observe pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Pyraclostrobin (Cabrio) / Azoxystrobin (Abound)",
                    application_purpose="Systemic strobilurin fungicide for comprehensive foliar disease suppression.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Early spring and post-renovation protectant spray.",
                    limitations="Avoid spraying during high temperatures to prevent leaf injury.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified disease-free transplants",
                "Ensure good row spacing and weed control to promote rapid foliage drying",
                "Renovate perennial matted-row plantings promptly after harvest"
            ],
            sanitation_measures=[
                "Rake and destroy old diseased foliage during post-harvest renovation",
                "Avoid planting in low, poorly drained areas"
            ],
            resistant_varieties="Cultivars with good resistance: Allstar, Honeoye, Jewel, Earliglow; susceptible: Raritan, Winona."
        ),
        similar_diseases=["strawberry__common_leaf_spot", "strawberry__leaf_blight"],
        severity_indicators="Dark purple irregular spots coalescing over >40% of canopy, curled burned scorched leaves, brown dried fruit calyxes.",
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_UC_IPM],
        quality_level="HIGH"
    ),
}
