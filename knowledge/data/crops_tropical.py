"""
Authoritative Plant Pathology Knowledge: Tropical & Subtropical Crops (14 diseases)
- Banana: Anthracnose, Black Leaf Streak (Black Sigatoka), Bunchy Top, Cigar End Rot, Cordana Leaf Spot, Panama Disease (Fusarium Wilt)
- Citrus: Citrus Canker, Citrus Greening (Huanglongbing)
- Coffee: Berry Blotch, Black Rot (Koleroga), Brown Eye Spot, Leaf Rust
- Ginger: Leaf Spot (Phyllosticta), Sheath Blight (Rhizoctonia)
Sources: FAO, USDA ARS, UF/IFAS, UC IPM, ICAR-IISR, CABI, EPPO.
"""

from knowledge.schema import (
    DiseaseRecord, PathogenType, PlantPart, TreatmentPlan,
    ChemicalControl, CulturalControl, BiologicalControl, PreventionProtocol
)
from knowledge.sources import (
    SOURCE_USDA_ARS, SOURCE_FAO, SOURCE_UF_IFAS, SOURCE_UC_IPM,
    SOURCE_ICAR, SOURCE_CABI, SOURCE_EPPO
)

TROPICAL_DISEASES = {
    "banana__anthracnose": DiseaseRecord(
        id="banana__anthracnose",
        canonical_name="Banana Anthracnose",
        crop="banana",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Colletotrichum musae",
        affected_parts=[PlantPart.FRUIT, PlantPart.FLOWER, PlantPart.LEAF],
        symptoms=[
            "Small black or dark brown sunken circular spots on banana peel",
            "Lesions coalesce causing large dark rotten patches on ripening fingers",
            "Salmon-pink or orange gelatinous spore masses (acervuli) emerge under humid conditions",
            "Premature ripening, fruit softening, and severe peel decay post-harvest"
        ],
        symptom_progression="Latent quiescent infection establishes on young green fruit -> remains dormant until ripening -> rapidly erupts into expanding necrotic lesions as sugars rise.",
        development_conditions="Temperatures 25-30°C, relative humidity >90%, wet tropical weather, physical fruit abrasions.",
        spread_transmission="Conidia dispersed by rain splashing, dew run-off, insects, and contaminated harvesting knives or hands.",
        infection_sources="Senescent floral parts, dying banana leaves hanging in the canopy, mummified fruit, and contaminated postharvest wash water.",
        immediate_actions=[
            "Remove and destroy rotten fruit bunches and dying floral bracts",
            "Prune senescent hanging banana leaves from mats to lower inoculum load",
            "Sanitize all bunch-cutting tools with 70% alcohol or 1% quaternary ammonium"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="De-hand and pack fruit under hygienic conditions; wash in clean potable running water and dry thoroughly.",
                    source_id=SOURCE_FAO.id
                )
            ],
            management=[
                CulturalControl(
                    description="Field bunch hygiene: debudding (removal of male flower bell), deflowering, and prompt bunch bagging with perforated polyethylene.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Azoxystrobin",
                    application_purpose="Protective post-shooting bunch spray where approved by local regulations.",
                    limitations="Follow label instructions; rotate FRAC groups (FRAC 11) to manage resistance.",
                    source_id=SOURCE_FAO.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Field protectant spray on developing fruit clusters in wet seasons.",
                    limitations="Strictly obey pre-harvest intervals and local label restrictions.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus subtilis",
                    application_method="Postharvest fruit wash / bio-fungicide dip to suppress spore germination.",
                    source_id=SOURCE_CABI.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Field sanitation: remove dead leaves and senescent floral tissues before bunch emergence",
                "Bag bunches early (at bract fall) using treated or ventilated polythene sleeves",
                "Careful postharvest handling to avoid bruising, wounding, or sun-scald"
            ],
            sanitation_measures=[
                "Regularly sanitize de-handing knives and packing lines",
                "Ensure packing station water is filtered or treated"
            ],
            resistant_varieties="Commercial Cavendish cultivars are susceptible; field sanitation and bunch bagging are key."
        ),
        similar_diseases=["banana__cigar_end_rot", "banana__crown_rot"],
        severity_indicators="More than 25% peel surface covered with salmon-pink sporulating sunken lesions, finger drop.",
        sources=[SOURCE_FAO, SOURCE_UF_IFAS, SOURCE_CABI],
        quality_level="HIGH"
    ),

    "banana__black_leaf_streak": DiseaseRecord(
        id="banana__black_leaf_streak",
        canonical_name="Banana Black Leaf Streak (Black Sigatoka)",
        crop="banana",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Pseudocercospora fijiensis (formerly Mycosphaerella fijiensis)",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Minute reddish-brown to dark rusty specks on underside of leaves (stage 1)",
            "Specks elongate into narrow rusty-brown streaks parallel to leaf veins (stage 2-3)",
            "Streaks broaden into elliptical dark brown to black spots with yellow halos (stage 4-5)",
            "Centers become sunken, bleached gray with black dots, causing extensive leaf death and premature bunch ripening"
        ],
        symptom_progression="Faint streaks -> necrotic black spots -> massive leaf collapse -> reduced photosynthetic leaf area -> stunted bunches and uneven premature ripening.",
        development_conditions="High temperatures (27°C optimum), continuous leaf wetness, relative humidity >95%, dense plantation spacing.",
        spread_transmission="Ascospores carried by wind over long distances; conidia dispersed locally via rain splash.",
        infection_sources="Infected standing foliage, decomposing leaf trash on the plantation floor.",
        immediate_actions=[
            "De-leaf: systematically excise severely infected leaf blades or partial necroses and deposit on ground face down",
            "Improve plantation drainage and reduce weed competition",
            "Maintain minimum of 8-10 healthy functional green leaves at flowering for full bunch filling"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Surgically cut out necrotic leaf tips and diseased sections (sanitary deleafing) weekly.",
                    source_id=SOURCE_FAO.id
                )
            ],
            management=[
                CulturalControl(
                    description="Optimizing plantation density, rapid drainage to lower microclimate humidity, and balanced potassium/nitrogen nutrition.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb",
                    application_purpose="Protective contact multi-site fungicide (FRAC M03) applied in oil-water emulsion.",
                    limitations="Preventive only; must be applied before fungal penetration; observe harvest intervals.",
                    source_id=SOURCE_FAO.id
                ),
                ChemicalControl(
                    active_ingredient="Difenoconazole",
                    application_purpose="Systemic DMI fungicide (FRAC 3) for early-stage streak arrest.",
                    limitations="Strict resistance management: maximum 2-3 applications per year rotated with multi-site contact fungicides.",
                    source_id=SOURCE_CABI.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens",
                    application_method="Foliar bio-fungicide spray to competitively inhibit spore germination on young unfurling leaves.",
                    source_id=SOURCE_CABI.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Maintain wide plant spacing (2.5m x 2.5m) to enhance airflow and sunlight penetration",
                "Ensure rapid drainage ditches to eliminate standing surface water",
                "Balanced fertilization avoiding excessive nitrogen that promotes lush soft tissue"
            ],
            sanitation_measures=[
                "Weekly removal and mulching of necrotic leaves below the canopy",
                "Clean boots and machetes when moving between plantation blocks"
            ],
            resistant_varieties="FHIA hybrids (e.g., FHIA-01, FHIA-17, FHIA-21) exhibit strong field resistance/tolerance."
        ),
        similar_diseases=["banana__cordana_leaf_spot", "banana__yellow_sigatoka"],
        severity_indicators="Less than 5 functional green leaves remaining at shooting/bunch emergence; bunch undersized and ripening prematurely on the plant.",
        sources=[SOURCE_FAO, SOURCE_UF_IFAS, SOURCE_CABI],
        quality_level="HIGH"
    ),

    "banana__bunchy_top": DiseaseRecord(
        id="banana__bunchy_top",
        canonical_name="Banana Bunchy Top Virus (BBTV)",
        crop="banana",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Banana bunchy top virus (BBTV, Babuvirus)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Dark green 'Morse code' dash-and-dot streaks along leaf veins and petioles",
            "Leaves emerge progressively shorter, narrower, upright, stiff, and brittle",
            "Leaves become bunched in a tight rosette crown at the apex of the pseudostem",
            "Leaf margins show chlorosis and upward curling; infected mats become severely stunted and completely unproductive"
        ],
        symptom_progression="Morse code streaks on veins -> stunted narrow leaves -> tight rosette bunching at apex -> failure to produce bunches or producing distorted, unmarketable fruit.",
        development_conditions="Warm humid tropical environments supporting banana aphid vector populations (Pentalonia nigronervosa).",
        spread_transmission="Persistently transmitted by the banana aphid (Pentalonia nigronervosa) and propagated via infected suckers/corms.",
        infection_sources="Infected banana stools, alternative host plants (Heliconia, Zingiberaceae), and aphid colonies.",
        immediate_actions=[
            "DO NOT merely cut the top of the pseudostem as regrowth will harbor the virus",
            "Spray entire mat and surrounding soil with insecticidal soap or registered aphicide to kill aphid vectors before roguing",
            "Inject whole mat with herbicide (e.g., glyphosate) or dig out entire corm/root system and burn/bury on-site"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Total roguing of infected stools (complete destruction of mother plant and all suckers) following aphid control.",
                    source_id=SOURCE_FAO.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Imidacloprid",
                    application_purpose="Systemic insecticide targeted at controlling vector aphid (Pentalonia nigronervosa) populations.",
                    limitations="Strictly follow local pollinator protection regulations and pre-harvest intervals.",
                    source_id=SOURCE_CABI.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Chrysoperla carnea (Green lacewing larvae)",
                    application_method="Biological predator for aphid vector suppression in integrated pest management.",
                    source_id=SOURCE_CABI.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified virus-indexed tissue-cultured banana plantlets exclusively",
                "Quarantine new planting materials and avoid sharing suckers from unverified farm blocks",
                "Regular field scouting for early 'Morse code' petiole streaks"
            ],
            sanitation_measures=[
                "Eradicate virus-infected mats promptly upon visual detection",
                "Disinfect tools and maintain aphid-free nursery conditions"
            ],
            resistant_varieties="No commercial cultivars are fully immune; all Cavendish and plantains require strict aphid and propagation hygiene."
        ),
        similar_diseases=["banana__panama_disease", "banana__burl"],
        severity_indicators="Choked rosette crown, severe stunting, dark green vein dots ('Morse code'), zero marketable fruit yield.",
        sources=[SOURCE_FAO, SOURCE_CABI, SOURCE_EPPO],
        quality_level="HIGH"
    ),

    "banana__cigar_end_rot": DiseaseRecord(
        id="banana__cigar_end_rot",
        canonical_name="Banana Cigar End Rot",
        crop="banana",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Trachysphaera fructigena / Musicillium theobromae",
        affected_parts=[PlantPart.FRUIT, PlantPart.FLOWER],
        symptoms=[
            "Dry, firm, black necrotic rot starting at the perianth (tip) of the young banana finger",
            "Rot slowly progresses 1 to 3 cm up the fruit pulp and peel",
            "Tip develops a powdery gray-white or ash-colored ash-like fungal coating, resembling the burnt ash tip of a lit cigar",
            "Affected fruit peel becomes corrugated, dark, and prematurely dried"
        ],
        symptom_progression="Flower parts fail to abscise and become infected -> fungus penetrates perianth into finger tip -> dry black rot extends -> characteristic powdery cigar ash appearance.",
        development_conditions="Cool, wet, high-altitude banana growing regions or humid monsoon seasons.",
        spread_transmission="Airborne conidia entering through retained flower floral parts and physical perianth wounds.",
        infection_sources="Dead flower floral remnants, senescent bracts, and diseased fruit mummies.",
        immediate_actions=[
            "Manually remove pistils and perianths (deflowering) 8 to 11 days after bunch emergence",
            "Excise and dispose of cigar-tipped fingers",
            "Place bunch bags over developing fingers immediately following deflowering"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Manual flower removal (deflowering) by hand as soon as bracts lift to eliminate infection court.",
                    source_id=SOURCE_FAO.id
                )
            ],
            management=[
                CulturalControl(
                    description="Early bunch bagging with perforated polyethylene bags after floral part removal.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Oxychloride",
                    application_purpose="Foliar/bunch spray applied to young emerging bunches before bagging.",
                    limitations="Apply only if disease pressure is severe and permitted by local product registrations.",
                    source_id=SOURCE_FAO.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Prompt deflowering of fingers 7-14 days after shoot emergence",
                "Bunch trimming and polyethylene bunch sleeving",
                "Adequate plantation spacing to facilitate air circulation"
            ],
            sanitation_measures=[
                "Clear old floral residues and infected bunches from the orchard floor",
                "Sanitize harvest tools regularly"
            ],
            resistant_varieties="Varietal susceptibility varies; standard Cavendish requires active deflowering and bunch bagging."
        ),
        similar_diseases=["banana__anthracnose", "banana__crown_rot"],
        severity_indicators="Black dry necrotic rot extending more than 2 cm up multiple fingers with thick ash-gray spore mantle.",
        sources=[SOURCE_FAO, SOURCE_UF_IFAS, SOURCE_CABI],
        quality_level="HIGH"
    ),

    "banana__cordana_leaf_spot": DiseaseRecord(
        id="banana__cordana_leaf_spot",
        canonical_name="Banana Cordana Leaf Spot",
        crop="banana",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cordana musae (syn. Neocordana musae)",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Large, prominent oval to diamond-shaped necrotic lesions on banana leaves",
            "Lesions feature distinct concentric brown rings with a pale gray center and a bright yellow surrounding halo",
            "Spots frequently expand along leaf margins or coalesce into large irregular marginal blights",
            "Underside of lesions displays a delicate grayish-brown velvety coating of conidiophores"
        ],
        symptom_progression="Small yellow/brown specks -> expanding zoned elliptical spots -> coalescing large marginal leaf necrosis -> premature leaf drying.",
        development_conditions="High humidity, warm temperatures (24-28°C), frequent rain showers, shaded or crowded undercanopies.",
        spread_transmission="Conidia dispersed by wind and splashing raindrops.",
        infection_sources="Old infected banana leaves, fallen trash, and secondary colonization of Sigatoka lesions.",
        immediate_actions=[
            "Prune out heavily spotted or necrotic leaf portions",
            "Clear plantation floor trash to enhance air circulation",
            "Ensure Sigatoka spray program is active (standard Sigatoka fungicides also suppress Cordana)"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Sanitary deleafing to remove necrotic leaf tissue showing concentric rings.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            management=[
                CulturalControl(
                    description="Maintain proper drainage, weed management, and open canopy spacing.",
                    source_id=SOURCE_FAO.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb",
                    application_purpose="Broad-spectrum protectant fungicide applied to foliage during high disease pressure.",
                    limitations="Preventive use only; follow local pesticide laws and harvest interval guidelines.",
                    source_id=SOURCE_CABI.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin",
                    application_purpose="Systemic foliar spray for broad fungal leaf spot control.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_FAO.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Maintain optimal plant spacing to allow rapid leaf drying",
                "Ensure weed control and adequate soil fertility (avoid potassium deficiency)",
                "Avoid sprinkler irrigation wetting the leaf canopy"
            ],
            sanitation_measures=[
                "Routine removal of dry and heavily diseased lower leaves"
            ],
            resistant_varieties="Most dessert bananas are susceptible under wet crowded conditions; robust cultural management provides effective control."
        ),
        similar_diseases=["banana__black_leaf_streak", "banana__yellow_sigatoka"],
        severity_indicators="Coalescence of multiple zoned lesions covering >30% of functional leaf area on upper canopy.",
        sources=[SOURCE_FAO, SOURCE_UF_IFAS, SOURCE_CABI],
        quality_level="HIGH"
    ),

    "banana__panama_disease": DiseaseRecord(
        id="banana__panama_disease",
        canonical_name="Banana Panama Disease (Fusarium Wilt)",
        crop="banana",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Fusarium oxysporum f. sp. cubense (Foc Race 1, Subtropical Race 4, and Tropical Race 4 - TR4)",
        affected_parts=[PlantPart.ROOT, PlantPart.STEM, PlantPart.LEAF, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Progressive yellowing of oldest lower leaves along margins, advancing inward toward midrib",
            "Leaves wilt, buckle at the petiole base, and collapse to form a skirt of dead dry foliage around the pseudostem",
            "Internal vascular discoloration: intense reddish-brown, purple, or black vascular strands inside the pseudostem and corm",
            "Longitudinal splitting of the lower pseudostem base; infected plant eventually wilts completely and dies"
        ],
        symptom_progression="Root infection via soil -> fungal colonization of xylem vessels -> vascular occlusion and toxin production -> leaf yellowing and buckling -> skirt of dead leaves -> total plant death.",
        development_conditions="Warm soil temperatures (25-30°C), acidic sandy or clay soils, poor drainage, root-knot nematode damage.",
        spread_transmission="Soilborne chlamydospores persisting 20-30+ years; spread by contaminated soil, infected suckers/rhizomes, floodwater, farm equipment, and footwear.",
        infection_sources="Infested soil, contaminated irrigation run-off, infected asymptomatic propagation material.",
        immediate_actions=[
            "Strict quarantine: immediately fence off and isolate the affected mat and surrounding 5-meter buffer zone",
            "DO NOT move soil, suckers, or equipment out of the infested zone",
            "Eradicate infected mat by in-situ burning or injection of registered arboricide inside secure containment",
            "Report suspected TR4 incursions immediately to national plant protection authorities"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Strict biosecurity, field zoning, footbaths with 20% quaternary ammonium, and crop rotation with non-host wetland crops.",
                    source_id=SOURCE_FAO.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Didecyl dimethyl ammonium chloride (DDAC)",
                    application_purpose="Disinfectant for farm machinery, tools, and footwear at biosecurity checkpoints (NOT for plant application).",
                    limitations="Use for sanitation only; follow safety protocols for corrosive disinfectants.",
                    source_id=SOURCE_FAO.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Trichoderma harzianum",
                    application_method="Soil amendment in seedling planting holes to competitively suppress Fusarium inoculum.",
                    source_id=SOURCE_CABI.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use exclusively certified pathogen-free tissue-cultured plantlets",
                "Establish strict on-farm biosecurity: vehicle wheel baths, boot washing stations, designated farm footwear",
                "Ensure effective surface water diversion to prevent runoff from neighboring fields"
            ],
            sanitation_measures=[
                "Disinfect all tools, machetes, and boots before entering and leaving field blocks",
                "Never share farm equipment with unverified plantations"
            ],
            resistant_varieties="For Race 1: Cavendish cultivars are resistant. For TR4 (Tropical Race 4): somaclonal variants (e.g., Formosana / GCTCV-218) show intermediate tolerance; breeding programs ongoing."
        ),
        similar_diseases=["banana__bunchy_top", "banana__burl", "banana__moko_disease"],
        severity_indicators="Vascular browning inside corm/pseudostem, skirt of collapsed yellow leaves, complete wilt of the mat.",
        sources=[SOURCE_FAO, SOURCE_EPPO, SOURCE_CABI],
        quality_level="HIGH"
    ),

    "citrus__canker": DiseaseRecord(
        id="citrus__canker",
        canonical_name="Citrus Canker",
        crop="citrus",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Xanthomonas citri subsp. citri",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Raised, blister-like corky lesions on leaves, fruit, and green twigs",
            "Leaf lesions are surrounded by a distinct oily or water-soaked margin and a prominent bright yellow chlorotic halo",
            "Both upper and lower surfaces of leaves exhibit raised crater-like erupted pustules",
            "Fruit lesions are rough, brown, cracked, and sunken in the center, causing severe fruit drop and market rejection"
        ],
        symptom_progression="Tiny water-soaked specks -> raised spongy eruptions -> corky cratered pustules with yellow halos on leaves/fruit -> premature leaf and fruit drop -> twig dieback.",
        development_conditions="High temperatures (20-30°C), heavy rainfall with wind gusts (>8 m/s), high humidity, presence of Asian citrus leafminer wounds.",
        spread_transmission="Wind-driven rain, overhead irrigation, contaminated pruning shears, transport of infected budwood or fruit.",
        infection_sources="Old stem cankers, infected foliage, uncertified nursery budwood.",
        immediate_actions=[
            "Prune out infected twigs during dry weather and destroy clippings",
            "Establish windbreaks around orchards to reduce wind-blown rain spread",
            "Implement copper-based protective spray program during new flush and early fruit development"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Install natural or artificial windbreaks, avoid overhead sprinkler irrigation, and sanitize pruning equipment.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Protective contact bactericide applied to leaf flushes and young developing fruit (2-3 week intervals during wet periods).",
                    limitations="Preventive only; avoid excessive build-up to prevent phytotoxicity and copper soil accumulation.",
                    source_id=SOURCE_UF_IFAS.id
                ),
                ChemicalControl(
                    active_ingredient="Abamectin",
                    application_purpose="Insecticide targeted at Asian citrus leafminer to reduce larval feeding wounds that facilitate bacterial entry.",
                    limitations="Rotate modes of action for insect resistance management; follow local label directions.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus amyloliquefaciens",
                    application_method="Foliar bio-bactericide spray to reduce bacterial colonization on young flushes.",
                    source_id=SOURCE_CABI.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified disease-free nursery stock from quarantined repositories",
                "Construct windbreaks (Casuarina, Eucalyptus, or shade netting) to reduce wind speed below 8 m/s",
                "Schedule pruning strictly during dry weather conditions"
            ],
            sanitation_measures=[
                "Disinfect harvesting shears, ladders, and machinery with 20% quaternary ammonium or 10% household bleach",
                "Enforce orchard entry biosecurity protocols"
            ],
            resistant_varieties="Grapefruit and Mexican lime are highly susceptible; Mandarins (Tangerines) and calamondin show moderate to high tolerance."
        ),
        similar_diseases=["citrus__greening_disease", "citrus__black_spot", "citrus__scab"],
        severity_indicators="Extensive corky eruptions on fruit peel, premature fruit drop >20%, severe defoliation and twig dieback.",
        sources=[SOURCE_UF_IFAS, SOURCE_UC_IPM, SOURCE_USDA_ARS, SOURCE_EPPO],
        quality_level="HIGH"
    ),

    "citrus__greening_disease": DiseaseRecord(
        id="citrus__greening_disease",
        canonical_name="Citrus Greening (Huanglongbing / HLB)",
        crop="citrus",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Candidatus Liberibacter asiaticus (CLas)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT, PlantPart.ROOT, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Asymmetrical blotchy mottle chlorosis on leaves crossing leaf veins (not symmetrical like zinc deficiency)",
            "Leaves become small, upright, thickened, with yellow veins ('corky veins')",
            "Fruit remains small, lopsided, asymmetrical with an inverted color break (remains green at stylar end)",
            "Fruit has bitter, sour taste, aborted dark seeds, and drops prematurely; tree suffers progressive twig dieback and decline"
        ],
        symptom_progression="Blotchy mottle on single branch ('yellow shoot') -> systemic decline across canopy -> root system dieback -> lopsided bitter fruit -> complete orchard collapse within 3-5 years.",
        development_conditions="Warm subtropical/tropical conditions favoring the Asian citrus psyllid (Diaphorina citri) vector.",
        spread_transmission="Vector transmission by Asian citrus psyllid (Diaphorina citri) and grafting with infected budwood.",
        infection_sources="Infected citrus trees, residential citrus hosts, vector psyllid populations, uncertified nurseries.",
        immediate_actions=[
            "Scout for Asian citrus psyllids on young flush and blotchy mottle foliage",
            "Apply vector control (targeted insecticides or horticultural oils) immediately",
            "Remove and destroy confirmed HLB-infected trees to eliminate bacterial reservoir in non-endemic areas",
            "Provide balanced foliar nutrition and root health enhancers to maintain tree vigor"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Area-wide psyllid vector management, rigorous roguing of infected trees in low-incidence zones, and planting in protective screenhouses (CUPS).",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Imidacloprid",
                    application_purpose="Systemic soil drench on young trees for persistent psyllid vector suppression.",
                    limitations="Strict adherence to pollinator protection labels and annual application caps.",
                    source_id=SOURCE_UF_IFAS.id
                ),
                ChemicalControl(
                    active_ingredient="Oxytetracycline",
                    application_purpose="Trunk injection into infected trees where legally approved (e.g. Florida special local need) to suppress bacterial titer.",
                    limitations="Restricted use; strict pre-harvest intervals and special label requirements apply.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Tamarixia radiata",
                    application_method="Ectoparasitoid wasp released for biological control of Asian citrus psyllid nymphs.",
                    source_id=SOURCE_USDA_ARS.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified HLB-free nursery trees propagated in psyllid-proof screenhouses",
                "Grow citrus under protected screen structures (Citrus Under Protective Screen - CUPS)",
                "Conduct regular area-wide psyllid trapping and coordinated scouting"
            ],
            sanitation_measures=[
                "Disinfect budding knives and prohibit unauthorized citrus budwood movement",
                "Remove abandoned or wild host plants (e.g., Murraya paniculata / Orange Jasmine)"
            ],
            resistant_varieties="No fully immune commercial scion cultivars exist; trifoliate orange (Poncirus trifoliata) and certain hybrid rootstocks show enhanced tolerance."
        ),
        similar_diseases=["citrus__canker", "citrus__stubborn_disease", "citrus__mineral_deficiencies"],
        severity_indicators="Widespread asymmetrical blotchy mottle across multiple scaffolds, root loss >50%, lopsided bitter green fruit drop.",
        sources=[SOURCE_UF_IFAS, SOURCE_UC_IPM, SOURCE_USDA_ARS, SOURCE_EPPO],
        quality_level="HIGH"
    ),

    "coffee__berry_blotch": DiseaseRecord(
        id="coffee__berry_blotch",
        canonical_name="Coffee Berry Blotch",
        crop="coffee",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cercospora coffeicola (fruit phase)",
        affected_parts=[PlantPart.FRUIT, PlantPart.LEAF],
        symptoms=[
            "Brown to dark reddish-black sunken lesions on green or semi-ripe coffee berries",
            "Lesions develop a light gray or whitish center and often cover the sun-exposed side of the berry",
            "Pulp adheres tightly to the parchment, making pulping and processing extremely difficult",
            "Premature berry drop, berry mummification, and reduced cup bean quality"
        ],
        symptom_progression="Small dark spots on young green berries -> expanding sunken dark blotches -> skin drying and sticking to parchment -> fruit dropping prematurely.",
        development_conditions="High sunlight exposure (inadequate shade), high temperatures, nutrient deficiency (nitrogen/potassium), and drought stress.",
        spread_transmission="Conidia dispersed by wind, rain splashing, and manual harvesting operations.",
        infection_sources="Infected leaves with brown eye spot, fallen mummified berries, old nursery stock.",
        immediate_actions=[
            "Regulate shade canopy to prevent excessive sun-scorch on developing berries",
            "Apply balanced nitrogen and potassium fertilizers to boost plant resilience",
            "Apply protective copper or triazole fungicide during early fruit setting"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Sanitary removal of mummified and blotched berries during harvest.",
                    source_id=SOURCE_FAO.id
                )
            ],
            management=[
                CulturalControl(
                    description="Maintain 30-40% agroforestry shade cover, correct soil nutrient deficiencies, and apply adequate organic mulch.",
                    source_id=SOURCE_CABI.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Oxychloride",
                    application_purpose="Protective contact fungicide sprayed onto developing berry clusters 6-12 weeks after flowering.",
                    limitations="Observe local registration labels and spray volume guidelines.",
                    source_id=SOURCE_FAO.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin",
                    application_purpose="Systemic strobilurin fungicide for comprehensive berry disease suppression.",
                    limitations="Rotate FRAC groups to prevent resistance development.",
                    source_id=SOURCE_CABI.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Establish appropriate shade tree canopy (e.g., Inga, Grevillea) to buffer solar radiation and temperature extremes",
                "Soil testing and balanced N-P-K fertilization to avoid nutrient stress",
                "Maintain weed-free zones around coffee bush bases"
            ],
            sanitation_measures=[
                "Strip all unharvested and diseased berries at the end of the harvest season",
                "Sanitize pruning shears"
            ],
            resistant_varieties="Varieties with dense vegetative foliage and good vigor show lower disease incidence under moderate shade."
        ),
        similar_diseases=["coffee__brown_eye_spot", "coffee__black_rot", "coffee__anthracnose"],
        severity_indicators="Sunken dark blotches on >20% of green berry clusters causing parchment adhesion and fruit drop.",
        sources=[SOURCE_FAO, SOURCE_CABI, SOURCE_ICAR],
        quality_level="HIGH"
    ),

    "coffee__black_rot": DiseaseRecord(
        id="coffee__black_rot",
        canonical_name="Coffee Black Rot (Koleroga / Pellicularia Disease)",
        crop="coffee",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Ceratobasidium noxium (syn. Pellicularia koleroga / Corticium koleroga)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.FRUIT],
        symptoms=[
            "Blackening and rotting of leaves, green twigs, and developing berry clusters",
            "Infected leaves lose color, turn dark brown/black, and detach from petiole but remain suspended in mid-air by delicate white fungal threads (hyphal cords)",
            "A thin white-to-grayish web of fungal mycelium covers the underside of leaves and stems",
            "Berries turn black, rot, and fall or remain hanging by fungal strands in clusters"
        ],
        symptom_progression="Superficial mycelial threads spread along twigs -> leaves rot and turn black -> leaves drop but hang suspended by mycelial webs -> berry clusters rot and blacken completely.",
        development_conditions="Continuous monsoon rains, high relative humidity (>95%), mist, dense unpruned shade canopy, poor drainage.",
        spread_transmission="Mycelial growth along branches, basidiospores carried by wind and splashing rain, physical contact.",
        infection_sources="Dormant mycelium and sclerotia in twig bark crevices, infected hanging leaves, and alternate forest hosts.",
        immediate_actions=[
            "Prune shade trees immediately to let sunlight and wind ventilate the coffee canopy",
            "Collect and burn all blackened hanging leaves, twigs, and rotting berries",
            "Apply pre-monsoon and mid-monsoon protective copper fungicide sprays"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Immediate excision of infected branches and manual collection of dangling mummified leaves.",
                    source_id=SOURCE_ICAR.id
                )
            ],
            management=[
                CulturalControl(
                    description="Canopy shade thinning before the monsoon, desuckering, and opening drainage channels to lower plantation humidity.",
                    source_id=SOURCE_ICAR.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Bordeaux Mixture (1%)",
                    application_purpose="Traditional multi-site contact fungicide spray applied before and during heavy monsoon periods.",
                    limitations="Prepare fresh; ensure complete coverage of lower leaf surfaces and berry clusters.",
                    source_id=SOURCE_ICAR.id
                ),
                ChemicalControl(
                    active_ingredient="Carbendazim",
                    application_purpose="Systemic fungicide applied at early disease onset where permitted by local regulation.",
                    limitations="Follow regional regulatory restrictions and maximum residue limits.",
                    source_id=SOURCE_CABI.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Thorough pre-monsoon shade lopping and canopy centering (bush pruning)",
                "Ensure spacing allows lateral sunlight penetration",
                "Avoid over-shading in valley bottoms and mist-prone mountain pockets"
            ],
            sanitation_measures=[
                "Burn all excised diseased plant parts outside the plantation blocks",
                "Sanitize pruning saws and shears with disinfectant"
            ],
            resistant_varieties="Robusta coffee is generally more susceptible under heavy monsoon conditions; both Arabica and Robusta require active canopy management."
        ),
        similar_diseases=["coffee__brown_eye_spot", "coffee__leaf_rust"],
        severity_indicators="Leaves blackened and dangling by fungal threads over >25% of canopy, berry cluster rot, extensive branch dieback.",
        sources=[SOURCE_ICAR, SOURCE_FAO, SOURCE_CABI],
        quality_level="HIGH"
    ),

    "coffee__brown_eye_spot": DiseaseRecord(
        id="coffee__brown_eye_spot",
        canonical_name="Coffee Brown Eye Spot (Cercospora Leaf Spot)",
        crop="coffee",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cercospora coffeicola",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT],
        symptoms=[
            "Circular brown spots with a distinct light gray to whitish ash-colored center ('eye') on leaves",
            "Spots are surrounded by a bright, prominent yellow halo",
            "Lesions coalesce under high disease pressure, causing extensive chlorosis and premature defoliation",
            "Nursery seedlings and stressed field bushes show severe leaf drop and stunted growth"
        ],
        symptom_progression="Tiny brown dots on leaf blade -> expanding circular spots with white eyes and yellow halos -> heavy premature leaf drop -> weakened vegetative vigor.",
        development_conditions="High sunlight exposure, nitrogen and potassium deficiencies, water stress, crowded humid nurseries.",
        spread_transmission="Conidia dispersed by wind, rain splashes, and irrigation water.",
        infection_sources="Infected older coffee leaves, nursery residues, and infected wild coffee plants.",
        immediate_actions=[
            "Provide 30-50% shade cover over nursery beds and young field plantings",
            "Apply nitrogen and potassium fertilizer to correct nutritional stress",
            "Apply protective copper or systemic fungicide spray on foliage"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Prune heavily spotted foliage and remove defoliated leaf trash from nursery floors.",
                    source_id=SOURCE_FAO.id
                )
            ],
            management=[
                CulturalControl(
                    description="Provide balanced nutrition, regulate shade, and optimize irrigation frequency to prevent moisture stress.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Oxychloride",
                    application_purpose="Protective contact spray applied to foliage at 3-4 week intervals during wet periods.",
                    limitations="Preventive application; ensure thorough coverage of both leaf sides.",
                    source_id=SOURCE_FAO.id
                ),
                ChemicalControl(
                    active_ingredient="Pyraclostrobin",
                    application_purpose="Systemic strobilurin fungicide for control of foliar Cercospora spots.",
                    limitations="Rotate with contact fungicides to manage resistance.",
                    source_id=SOURCE_CABI.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Maintain adequate shade trees in field plantations (30-40% shade)",
                "Use well-drained, fertile potting medium in nurseries and avoid overwatering",
                "Regular application of organic compost and balanced NPK fertilizer"
            ],
            sanitation_measures=[
                "Clean nursery beds and discard severely stunted diseased seedlings",
                "Disinfect pruning equipment"
            ],
            resistant_varieties="Varieties with high vegetative vigor and adaptability to shade show improved tolerance."
        ),
        similar_diseases=["coffee__leaf_rust", "coffee__berry_blotch"],
        severity_indicators="Over 30% defoliation on nursery seedlings or young bushes; numerous eyespots with bright halos on main leaves.",
        sources=[SOURCE_FAO, SOURCE_UF_IFAS, SOURCE_CABI, SOURCE_ICAR],
        quality_level="HIGH"
    ),

    "coffee__leaf_rust": DiseaseRecord(
        id="coffee__leaf_rust",
        canonical_name="Coffee Leaf Rust (Roya del Café)",
        crop="coffee",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Hemileia vastatrix",
        affected_parts=[PlantPart.LEAF],
        symptoms=[
            "Pale yellow, translucent spots on upper leaf surface",
            "Bright orange to yellow powdery spore masses (urediniospores) erupting on the corresponding lower leaf surface",
            "Spots enlarge, coalesce, and turn dark brown/black and necrotic in the center",
            "Massive defoliation, branch dieback, severe yield reduction, and eventual plant starvation"
        ],
        symptom_progression="Pale yellow spots -> bright powdery orange-yellow pustules on underside -> necrotic brown centers -> widespread premature leaf drop -> branch dieback.",
        development_conditions="Temperatures 21-25°C, high relative humidity, liquid water on leaf surface for >6 hours (rain, dew), unpruned dense canopy.",
        spread_transmission="Urediniospores dispersed primarily by wind, rain splash, insects, and human workers moving through foliage.",
        infection_sources="Living infected coffee leaves harboring active sporulating pustules throughout the year.",
        immediate_actions=[
            "Prune dying branches and open the canopy to increase aeration",
            "Apply protective copper fungicide prior to the onset of the rainy season",
            "Apply systemic triazole fungicide if rust pustules are active on more than 5-10% of leaves"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Pruning out dead branches and lower unproductive foliage to improve air circulation.",
                    source_id=SOURCE_FAO.id
                )
            ],
            management=[
                CulturalControl(
                    description="Balanced nutrition with emphasis on potassium and nitrogen, weed control, and regulated shade management.",
                    source_id=SOURCE_CABI.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Standard preventive multi-site contact fungicide applied before the rainy season.",
                    limitations="Thorough lower-leaf coverage is mandatory; strictly preventive.",
                    source_id=SOURCE_FAO.id
                ),
                ChemicalControl(
                    active_ingredient="Cyproconazole / Epoxiconazole",
                    application_purpose="Systemic DMI triazole fungicide for curative halt of early rust mycelium.",
                    limitations="Maximum 2 applications per season rotated with copper; observe pre-harvest intervals.",
                    source_id=SOURCE_CABI.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Lecanicillium lecanii (syn. Verticillium lecanii)",
                    application_method="Hyperparasitic fungus naturally attacking Hemileia urediniospores under high humidity.",
                    source_id=SOURCE_CABI.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant rust-resistant cultivars (Catimor, Sarchimor, Castillo, Ruiru 11, Batian)",
                "Maintain optimal plant nutrition to keep bushes vigorous and resilient",
                "Prune regularly to ensure good light penetration and airflow through the canopy"
            ],
            sanitation_measures=[
                "Avoid moving through wet rust-infected fields during harvest",
                "Disinfect clothing and tools after working in high-rust blocks"
            ],
            resistant_varieties="Catimor hybrids, Sarchimor, Castillo, Colombia, Ruiru 11, Batian, and IAPAR 59 possess major resistance genes (SH genes)."
        ),
        similar_diseases=["coffee__brown_eye_spot", "coffee__black_rot"],
        severity_indicators="Orange powdery pustules on >20% of leaf area, extensive premature defoliation, and twig dieback.",
        sources=[SOURCE_FAO, SOURCE_USDA_ARS, SOURCE_CABI, SOURCE_ICAR],
        quality_level="HIGH"
    ),

    "ginger__leaf_spot": DiseaseRecord(
        id="ginger__leaf_spot",
        canonical_name="Ginger Leaf Spot (Phyllosticta Leaf Spot)",
        crop="ginger",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Phyllosticta zingiberi",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM],
        symptoms=[
            "Small, oval to elongated yellowish-white spots on ginger leaves",
            "Spots enlarge with papery, thin, translucent centers surrounded by a dark brown margin and yellow halo",
            "Tiny black pycnidia (fruiting bodies) form in the necrotic central area",
            "Lesions coalesce, causing leaf shredding, premature drying, and extensive foliar blighting"
        ],
        symptom_progression="Minute yellow flecks -> expanding oval papery spots -> black pycnidia in center -> tearing and drying of leaf blades -> reduced rhizome sizing.",
        development_conditions="High humidity (>85%), temperatures 25-30°C, cloudy rainy monsoon weather, overhead splashing.",
        spread_transmission="Pycnidiospores spread by splashing raindrops and wind-blown mist.",
        infection_sources="Infected plant debris in soil, infected seed rhizomes, and wild ginger relatives.",
        immediate_actions=[
            "Collect and destroy heavily spotted leaves",
            "Provide organic mulch around plants to minimize rain-splash from soil",
            "Apply protective copper or mancozeb fungicide spray"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Sanitary hand-picking and destruction of initial spotted leaves.",
                    source_id=SOURCE_ICAR.id
                )
            ],
            management=[
                CulturalControl(
                    description="Heavy mulching with green leaves or straw, crop rotation, and maintaining good field drainage.",
                    source_id=SOURCE_ICAR.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mancozeb",
                    application_purpose="Foliar protective contact spray (0.2%) applied at 2-3 week intervals during monsoon.",
                    limitations="Preventive application; ensure coverage on both leaf surfaces.",
                    source_id=SOURCE_ICAR.id
                ),
                ChemicalControl(
                    active_ingredient="Copper Oxychloride",
                    application_purpose="Protective contact bactericide/fungicide spray for broad foliar protection.",
                    limitations="Follow local label directions and harvest intervals.",
                    source_id=SOURCE_FAO.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Trichoderma viride",
                    application_method="Rhizome treatment and soil application with organic manure at planting.",
                    source_id=SOURCE_ICAR.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Select healthy, disease-free seed rhizomes from certified seed production plots",
                "Apply thick green leaf mulch (10-12 tons/ha) at planting and repeated after weeding",
                "Ensure raised beds with 30 cm drainage trenches between beds"
            ],
            sanitation_measures=[
                "Burn crop residues after harvest to destroy overwintering pycnidia",
                "Avoid waterlogging around root zones"
            ],
            resistant_varieties="Varieties like IISR Mahima and IISR Rejatha show moderate field tolerance under proper management."
        ),
        similar_diseases=["ginger__sheath_blight", "ginger__bacterial_wilt"],
        severity_indicators="Papery necrotic lesions covering >40% of leaf area with extensive foliar blighting and premature drying.",
        sources=[SOURCE_ICAR, SOURCE_FAO, SOURCE_CABI],
        quality_level="HIGH"
    ),

    "ginger__sheath_blight": DiseaseRecord(
        id="ginger__sheath_blight",
        canonical_name="Ginger Sheath Blight (Rhizoctonia Blight)",
        crop="ginger",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Rhizoctonia solani",
        affected_parts=[PlantPart.STEM, PlantPart.LEAF, PlantPart.ROOT],
        symptoms=[
            "Water-soaked, greenish-gray oval to irregular lesions on pseudostem sheaths near the soil line",
            "Lesions enlarge rapidly with dark reddish-brown borders and grayish-white centers",
            "Blight ascends up the pseudostem, causing outer leaf sheaths to rot, loosen, and peel away",
            "Stems lodge or break easily at ground level; shoots turn yellow and dry up prematurely"
        ],
        symptom_progression="Water-soaked sheath spot at soil level -> expanding banded necrotic lesions up pseudostem -> sheath rotting and peeling -> shoot yellowing, lodging, and premature death.",
        development_conditions="High soil moisture, waterlogging, high temperatures (28-32°C), dense planting, excessive nitrogen fertilization.",
        spread_transmission="Soilborne sclerotia and mycelial fragments spread by irrigation water, rain splash, and soil movement.",
        infection_sources="Sclerotia surviving in soil for multiple years, infected seed rhizomes, and weed hosts.",
        immediate_actions=[
            "Improve drainage to eliminate water accumulation in beds",
            "Drench affected pseudostem bases and surrounding soil with fungicide",
            "Remove and destroy severely blighted collapsing tillers"
        ],
        treatment=TreatmentPlan(
            curative=[
                CulturalControl(
                    description="Careful removal and burning of blighted shoots and infected pseudostem sheaths.",
                    source_id=SOURCE_ICAR.id
                )
            ],
            management=[
                CulturalControl(
                    description="Deep drainage channels, raised planting beds (25-30 cm high), balanced fertilization, and avoiding waterlogging.",
                    source_id=SOURCE_ICAR.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Validamycin",
                    application_purpose="Antibiotic/fungicide specific for Rhizoctonia sheath blight suppression; drench around plant base.",
                    limitations="Follow regional regulatory registrations and label dosage instructions.",
                    source_id=SOURCE_ICAR.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin",
                    application_purpose="Systemic strobilurin fungicide applied as foliar and collar spray.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_CABI.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Trichoderma harzianum",
                    application_method="Soil application mixed with well-rotted farmyard manure (FYM) at planting and earthing up.",
                    source_id=SOURCE_ICAR.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant ginger on raised beds (1 m width, 30 cm height) with deep drainage furrows",
                "Treat seed rhizomes before planting with biological or chemical protectants",
                "Rotate with non-host crops (maize, pulses) and avoid continuous monoculture in infested plots"
            ],
            sanitation_measures=[
                "Solarize nursery beds and rogue out diseased clumps promptly",
                "Sanitize harvesting and tillage implements"
            ],
            resistant_varieties="Cultivars with upright erect pseudostems and good vigor show reduced lodging and disease severity."
        ),
        similar_diseases=["ginger__leaf_spot", "ginger__soft_rot", "ginger__bacterial_wilt"],
        severity_indicators="Pseudostem rot at soil level, outer sheath peeling, extensive shoot yellowing, and pseudostem collapse.",
        sources=[SOURCE_ICAR, SOURCE_FAO, SOURCE_CABI],
        quality_level="HIGH"
    ),
}
