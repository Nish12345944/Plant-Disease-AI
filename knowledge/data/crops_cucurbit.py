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
    SOURCE_UF_IFAS, SOURCE_USDA_ARS, SOURCE_FAO
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
        sources=[SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_UC_IPM, SOURCE_PURDUE],
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
                    source_id=SOURCE_PURDUE.id
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
                    source_id=SOURCE_UC_IPM.id
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
        sources=[SOURCE_PURDUE, SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_UC_IPM],
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
        sources=[SOURCE_CORNELL, SOURCE_UC_IPM, SOURCE_PURDUE, SOURCE_NC_STATE],
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
        sources=[SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_UC_IPM, SOURCE_NC_STATE],
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
        sources=[SOURCE_PURDUE, SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_UC_IPM],
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
        sources=[SOURCE_NC_STATE, SOURCE_UF_IFAS, SOURCE_CORNELL, SOURCE_UC_IPM],
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
        sources=[SOURCE_CORNELL, SOURCE_UC_IPM, SOURCE_NC_STATE, SOURCE_PURDUE],
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
        sources=[SOURCE_UC_IPM, SOURCE_CORNELL, SOURCE_NC_STATE, SOURCE_UF_IFAS],
        quality_level="HIGH"
    ),
}
