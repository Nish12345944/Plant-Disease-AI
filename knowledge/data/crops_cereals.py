"""
Authoritative Plant Pathology Knowledge: Cereal & Grain Crops (14 diseases)
- Corn: Gray Leaf Spot, Northern Leaf Blight, Rust (Common Rust), Smut (Common Smut)
- Rice: Rice Blast, Sheath Blight
- Wheat: Bacterial Leaf Streak (Black Chaff), Head Scab (Fusarium Head Blight), Leaf Rust, Loose Smut, Powdery Mildew, Septoria Blotch, Stem Rust, Stripe Rust (Yellow Rust)
Sources: Purdue Extension, Iowa State Extension, Penn State, UNL, USDA ARS, FAO, IRRI, CIMMYT.
"""

from knowledge.schema import (
    DiseaseRecord, PathogenType, PlantPart, TreatmentPlan,
    ChemicalControl, CulturalControl, BiologicalControl, PreventionProtocol
)
from knowledge.sources import (
    SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_PENN_STATE, SOURCE_UNL,
    SOURCE_USDA_ARS, SOURCE_FAO, SOURCE_IRRI, SOURCE_CIMMYT
)

CEREAL_DISEASES = {
    "corn__gray_leaf_spot": DiseaseRecord(
        id="corn__gray_leaf_spot",
        canonical_name="Corn Gray Leaf Spot",
        crop="corn",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cercospora zeae-maydis",
        affected_parts=[PlantPart.LEAF, PlantPart.SHEATH],
        symptoms=[
            "Small, tan to brown spots with yellow halos that expand into long, narrow, strictly rectangular blocky lesions (1-6 cm length, 2-4 mm width)",
            "Lesions are sharply delimited by parallel leaf veins, giving a distinct rectangular or 'zipper' shape",
            "Under humid conditions, mature lesions turn grayish-brown with fungal conidiophores",
            "Lesions coalesce, causing extensive foliar blighting, stalk cannibalization, premature senescence, and lodging"
        ],
        symptom_progression="Lower canopy rectangular tan specks -> expansion into blocky rectangular lesions bounded by veins -> gray spore bloom -> massive foliar blighting -> stalk lodging.",
        development_conditions="Warm, humid, cloudy weather (temperatures 25-32°C), relative humidity >90%, extended dew periods (>10-12 hours), continuous no-till corn.",
        spread_transmission="Windborne and rain-splashed conidia from infected residue on the soil surface.",
        infection_sources="Corn crop residues on the soil surface (pathogen survives strictly in residue).",
        immediate_actions=[
            "Scout middle canopy and ear leaves at VT/R1 (tasseling to silking)",
            "Apply foliar fungicide at VT/R1 if lesions are present on third leaf below ear leaf or higher on susceptible hybrids",
            "Plan for post-harvest residue management (tillage or rotation)"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Crop rotation with non-host crops (soybean, wheat), tillage to bury residue, and selecting resistant hybrids.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Pyraclostrobin + Fluxapyroxad (Headline AMP) / Azoxystrobin + Propiconazole (Quilt Xcel)",
                    application_purpose="Premix fungicide applied at VT/R1 for broad-spectrum foliar disease control and stalk health.",
                    limitations="Strictly obey pre-harvest intervals and label restrictions; avoid single-mode-of-action reliance.",
                    source_id=SOURCE_IOWA_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Difenoconazole + Azoxystrobin / Prothioconazole + Trifloxystrobin",
                    application_purpose="Systemic foliar spray for gray leaf spot suppression.",
                    limitations="Apply between V12 and R2; observe economic threshold guidelines.",
                    source_id=SOURCE_UNL.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant high-yielding corn hybrids with strong genetic resistance ratings to gray leaf spot",
                "Practice a 1-2 year rotation away from corn (e.g., corn-soybean rotation)",
                "In high-risk no-till fields, use residue-sizing tillage to promote microbial breakdown"
            ],
            sanitation_measures=[
                "Shred or incorporate corn stalks post-harvest"
            ],
            resistant_varieties="Commercial seed companies provide GLS resistance ratings (look for ratings of 7-9 on a 1-9 scale)."
        ),
        similar_diseases=["corn__northern_leaf_blight", "corn__diplodia_leaf_streak"],
        severity_indicators="Rectangular vein-bounded lesions covering >30% of ear leaf and upper canopy, stalk lodging.",
        sources=[SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_UNL, SOURCE_PENN_STATE],
        quality_level="HIGH"
    ),

    "corn__northern_leaf_blight": DiseaseRecord(
        id="corn__northern_leaf_blight",
        canonical_name="Corn Northern Corn Leaf Blight (NCLB)",
        crop="corn",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Exserohilum turcicum (syn. Setosphaeria turcica)",
        affected_parts=[PlantPart.LEAF, PlantPart.SHEATH, PlantPart.HUSK],
        symptoms=[
            "Large, elongated, elliptical, cigar-shaped or spindle-shaped grayish-green to tan lesions (2.5-15 cm length, 1-3 cm width)",
            "Lesions are NOT strictly restricted by leaf veins and have smooth, tapering ends",
            "In damp humid conditions, dark olive-gray to black sooty fungal sporulation appears across lesion centers",
            "Lesions coalesce, blighting entire leaves, causing premature plant death, poor ear fill, and severe stalk lodging"
        ],
        symptom_progression="Long cigar-shaped gray/tan lesions starting on lower leaves -> expanding up canopy -> dark sporulation -> extensive leaf blighting -> reduced grain fill and lodging.",
        development_conditions="Moderate temperatures (18-27°C), prolonged leaf wetness (6-18 hours of dew or rain), heavy morning fog, high residue.",
        spread_transmission="Windborne conidia carried across local and regional distances; rain splashing.",
        infection_sources="Infected corn leaf and stalk residue on the soil surface.",
        immediate_actions=[
            "Scout canopy before tasseling (V10-VT) for cigar-shaped lesions",
            "Apply foliar fungicide at VT/R1 if disease is active on lower leaves of susceptible hybrids",
            "Monitor grain drydown and plan timely harvest to prevent lodging"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Planting resistant hybrids (carrying Ht genes), 1-2 year crop rotation with soybeans, and residue incorporation.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Trifloxystrobin + Prothioconazole (Delaro) / Benzovindiflupyr + Azoxystrobin (Trivapro)",
                    application_purpose="Dual/triple mode-of-action fungicide applied at VT/R1 for maximum residual protection.",
                    limitations="Follow regional fungicide resistance guidelines and harvest restrictions.",
                    source_id=SOURCE_IOWA_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Pyraclostrobin + Fluxapyroxad (Veltyma)",
                    application_purpose="Translaminar and systemic foliar protection against NCLB.",
                    limitations="Apply at economic threshold; rotate FRAC groups.",
                    source_id=SOURCE_UNL.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant hybrids with qualitative Ht-gene resistance (Ht1, Ht2, Ht3, HtN) and quantitative multi-genic resistance",
                "Rotate with non-host crops (soybeans, alfalfa, small grains)",
                "Perform conservation tillage to accelerate residue decomposition in continuous corn"
            ],
            sanitation_measures=[
                "Incorporate heavy corn stubble where erosion risk allows"
            ],
            resistant_varieties="Most major commercial seed brands offer hybrids with high Ht-gene resistance."
        ),
        similar_diseases=["corn__gray_leaf_spot", "corn__southern_corn_leaf_blight", "corn__goss_wilt"],
        severity_indicators="Cigar-shaped lesions covering >40% of ear leaf and upper canopy at dough stage (R4), premature stalk death.",
        sources=[SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_UNL, SOURCE_PENN_STATE],
        quality_level="HIGH"
    ),

    "corn__rust": DiseaseRecord(
        id="corn__rust",
        canonical_name="Corn Common Rust",
        crop="corn",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Puccinia sorghi",
        affected_parts=[PlantPart.LEAF, PlantPart.SHEATH, PlantPart.HUSK],
        symptoms=[
            "Small, oval to elongated, cinnamon-brown to golden-brown powdery pustules (uredinia) scattered across BOTH upper and lower leaf surfaces",
            "Pustules rupture the leaf epidermis, releasing powdery reddish-brown urediniospores when touched",
            "Pustules often appear in bands across the leaf blade where dew was held in the whorl",
            "Late in the season, pustules turn dark brownish-black as overwintering teliospores develop; severe infections cause leaf chlorosis and death"
        ],
        symptom_progression="Golden-brown powdery pustules erupting on both leaf surfaces -> coalescence of pustules -> leaf yellowing and death -> black teliospore formation.",
        development_conditions="Cool to moderate temperatures (16-25°C), high relative humidity (>95%), prolonged leaf wetness (6 hours of dew).",
        spread_transmission="Airborne urediniospores blown northward each spring from southern tropical/subtropical regions.",
        infection_sources="Infected corn crops in southern regions; does not overwinter in freezing northern corn belt soils (requires alternate host Oxalis for sexual cycle).",
        immediate_actions=[
            "Scout whorl and lower leaves for cinnamon-brown pustules on both leaf surfaces",
            "Apply foliar fungicide if pustules cover >5-10% of leaf area prior to silking on susceptible inbreds/hybrids",
            "Differentiate from southern rust (which has smaller orange pustules primarily on upper surface only)"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Planting rust-resistant hybrids (carrying Rp resistance genes) and early planting to escape late spore showers.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Azoxystrobin + Propiconazole / Pyraclostrobin",
                    application_purpose="Foliar fungicide applied when rust pustules reach economic threshold on ear leaves.",
                    limitations="Usually only economically justified on seed corn (inbreds), sweet corn, or highly susceptible field hybrids.",
                    source_id=SOURCE_IOWA_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Select field corn hybrids with Rp-gene resistance (e.g., Rp1-d) or high general horizontal resistance",
                "Plant early in the spring to promote maturity before peak spore arrival from the south"
            ],
            sanitation_measures=[
                "Residue management has little effect because pathogen does not overwinter locally in northern soils"
            ],
            resistant_varieties="Most modern field corn hybrids have strong general field resistance; sweet corn and seed inbreds are more susceptible."
        ),
        similar_diseases=["corn__southern_rust_(puccinia_polysora)", "corn__physoderma_brown_spot"],
        severity_indicators="Abundant cinnamon-brown pustules on both leaf surfaces covering >20% of ear leaf area, premature leaf senescence.",
        sources=[SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_UNL, SOURCE_PENN_STATE],
        quality_level="HIGH"
    ),

    "corn__smut": DiseaseRecord(
        id="corn__smut",
        canonical_name="Corn Common Smut",
        crop="corn",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Ustilago maydis (syn. Ustilago zeae)",
        affected_parts=[PlantPart.EAR, PlantPart.TASSEL, PlantPart.STALK, PlantPart.LEAF],
        symptoms=[
            "Prominent, fleshy, tumor-like galls (swellings) developing on ears, tassels, stalks, or leaves",
            "Galls are initially glistening silvery-white to greenish-white, firm, and covered by a smooth membrane",
            "Internal gall tissue rapidly turns into a soft, powdery, black mass of millions of microscopic teliospores",
            "The silvery outer membrane ruptures, releasing dense clouds of powdery black sooty spores; ear galls replace kernels completely"
        ],
        symptom_progression="Silvery-white fleshy tumor gall -> internal blackening -> gall rupture releasing sooty black teliospores -> completely deformed ear/tassel.",
        development_conditions="Warm, dry weather (temperatures 26-34°C) following rain, plant physical injury (hail, cultivation wounds, detasseling, sandblasting, insect feeding), high nitrogen.",
        spread_transmission="Teliospores and sporidia dispersed by wind and splashing rain; survives in soil for 3-5+ years.",
        infection_sources="Teliospores overwintering in soil and crop residues; infected manure.",
        immediate_actions=[
            "In small/sweet corn plots, cut off and remove silvery galls BEFORE they rupture and release black spores",
            "Avoid mechanical wounding during cultivation and side-dressing",
            "Maintain balanced soil fertility (avoid excessive nitrogen rates)"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Avoid plant mechanical injury, manage corn borers and rootworms, maintain balanced fertility, and select resistant hybrids.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="No chemical fungicide is effective or recommended",
                    application_purpose="Foliar fungicides provide NO effective control against corn smut; management relies on genetics and cultural practices.",
                    limitations="Fungicide sprays are ineffective against gall formation.",
                    source_id=SOURCE_IOWA_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant corn hybrids with high resistance to common smut",
                "Avoid excessive nitrogen fertilization and maintain adequate phosphorus/potassium levels",
                "Minimize mechanical injuries during field cultivation and chemical spraying"
            ],
            sanitation_measures=[
                "In home gardens/sweet corn, hand-remove galls before rupture and destroy them",
                "Rotate with non-host crops to reduce soilborne spore concentrations"
            ],
            resistant_varieties="Most modern field corn hybrids have moderate to high genetic resistance; sweet corn varieties vary."
        ),
        similar_diseases=["corn__head_smut_(sphacelotheca_reiliana)", "corn__crazy_top"],
        severity_indicators="Large ruptured black powdery galls on ears and stalks, complete destruction of ear grain.",
        sources=[SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_UNL, SOURCE_PENN_STATE],
        quality_level="HIGH"
    ),

    "rice__blast": DiseaseRecord(
        id="rice__blast",
        canonical_name="Rice Blast (Leaf, Neck, and Node Blast)",
        crop="rice",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Magnaporthe oryzae (anamorph Pyricularia oryzae)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.PANICLE, PlantPart.NODE, PlantPart.COLLAR],
        symptoms=[
            "Leaf blast: Elliptical to spindle-shaped (diamond-shaped) lesions with gray or whitish centers and dark reddish-brown borders",
            "Lesions taper to sharp points at both ends and are surrounded by a chlorotic yellow halo; spots coalesce, blighting whole leaves",
            "Neck blast: Dark brown to black rotting at the panicle base (neck node), causing the panicle to fall over and lodge ('broken neck')",
            "Panicles become completely bleached, sterile, and produce empty, chalky, lightweight grains ('whitehead')"
        ],
        symptom_progression="Spindle-shaped leaf spots -> coalescing leaf blighting -> neck node black rot -> broken neck panicle collapse -> sterile whiteheads.",
        development_conditions="Temperatures 25-28°C, relative humidity >90%, extended leaf wetness (>10-14 hours of dew or rain), excessive nitrogen fertilization, aerobic/drained soils.",
        spread_transmission="Airborne conidia released primarily at night during high humidity and carried by wind currents; infected seed.",
        infection_sources="Infected crop residues, infected seed, volunteer rice, alternate grassy weed hosts.",
        immediate_actions=[
            "Maintain a continuous flood depth of 5-10 cm (2-4 inches) across paddies (avoid draining)",
            "Cease further nitrogen top-dressing in infected fields",
            "Apply protective/systemic blast fungicides at boot-split (late boot) and 50-70% panicle heading"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Maintain continuous floodwater, avoid excessive nitrogen rates, split nitrogen applications, and destroy crop residues.",
                    source_id=SOURCE_IRRI.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Azoxystrobin (Quadris) / Trifloxystrobin (Gem)",
                    application_purpose="Strobilurin fungicide applied at late boot to 10-50% heading for neck blast prevention.",
                    limitations="Preventive application before panicle emergence; observe pre-harvest intervals.",
                    source_id=SOURCE_IRRI.id
                ),
                ChemicalControl(
                    active_ingredient="Tricyclazole / Isoprothiolane",
                    application_purpose="Specialized systemic blast fungicides with strong preventive and translaminar activity.",
                    limitations="Check national/export market Maximum Residue Limits (MRLs) and regional registrations.",
                    source_id=SOURCE_FAO.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Bacillus subtilis / Pseudomonas fluorescens",
                    application_method="Seed treatment and foliar bio-fungicide spray.",
                    source_id=SOURCE_IRRI.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant blast-resistant rice cultivars carrying Pi resistance genes (e.g., Pi-ta, Pi-b, Pi-z)",
                "Maintain continuous deep floodwater throughout vegetative and reproductive growth",
                "Apply nitrogen fertilizer in split doses based on leaf color chart (LCC) recommendations"
            ],
            sanitation_measures=[
                "Burn or incorporate infected straw and stubble post-harvest",
                "Eradicate wild weed grasses around paddy levees"
            ],
            resistant_varieties="Cultivars with multi-genic blast resistance (e.g., CL153, Presidio, Diamond, IR64-derived lines)."
        ),
        similar_diseases=["rice__brown_spot", "rice__sheath_blight"],
        severity_indicators="Neck rot with collapsed broken panicles, extensive sterile whiteheads across >20% of field.",
        sources=[SOURCE_IRRI, SOURCE_FAO, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "rice__sheath_blight": DiseaseRecord(
        id="rice__sheath_blight",
        canonical_name="Rice Sheath Blight",
        crop="rice",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Rhizoctonia solani (teleomorph Thanatephorus cucumeris, AG-1 IA)",
        affected_parts=[PlantPart.STEM, PlantPart.LEAF, PlantPart.SHEATH],
        symptoms=[
            "Water-soaked, oval to oblong, greenish-gray spots appearing first on leaf sheaths near the water line",
            "Lesions enlarge up to 2-3 cm, developing bleached grayish-white centers with dark reddish-brown borders ('snake-skin' or banded look)",
            "Lesions coalesce and advance rapidly up the sheaths and leaf blades toward the upper canopy and flag leaf",
            "Infected tillers lodge easily, leaf blades turn dry and necrotic, and panicles fail to fill completely"
        ],
        symptom_progression="Waterline sheath spots -> banded snake-skin lesions ascending stem -> canopy blighting -> lodging and blanked grains.",
        development_conditions="High temperatures (28-32°C), high relative humidity (>95%), dense plant canopy, excessive nitrogen fertilizer, semi-dwarf cultivars.",
        spread_transmission="Sclerotia floating on irrigation floodwater coming into contact with rice sheaths; runner hyphae spreading plant-to-plant.",
        infection_sources="Soilborne sclerotia surviving in soil/stubble for years and floating on paddy water.",
        immediate_actions=[
            "Avoid excessive nitrogen top-dressing",
            "Scout lower canopy at panicle differentiation (PD) to boot stage",
            "Apply targeted fungicide if lesions are moving up the lower third of the canopy on susceptible cultivars"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Optimizing plant density, split nitrogen fertilization, draining and skimming floating sclerotia, and crop rotation with non-hosts.",
                    source_id=SOURCE_IRRI.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Azoxystrobin (Quadris) / Trifloxystrobin + Propiconazole (Stratego)",
                    application_purpose="Systemic foliar spray applied at panicle differentiation to late boot stage.",
                    limitations="Preventive/early curative; ensure spray penetrates dense canopy to reach lower sheaths.",
                    source_id=SOURCE_IRRI.id
                ),
                ChemicalControl(
                    active_ingredient="Validamycin / Thifluzamide",
                    application_purpose="Specific Rhizoctonia fungicides for sheath blight suppression.",
                    limitations="Observe local regulatory registrations and harvest intervals.",
                    source_id=SOURCE_FAO.id
                )
            ],
            biological=[
                BiologicalControl(
                    agent_name="Trichoderma harzianum / Pseudomonas fluorescens",
                    application_method="Seedling treatment and soil amendment to parasitize overwintering sclerotia.",
                    source_id=SOURCE_IRRI.id
                )
            ]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Avoid excessive planting density and over-seeding",
                "Apply balanced fertilizer with adequate potassium and avoid excessive nitrogen",
                "Rotate with non-host crops (e.g., pasture grasses, small grains) to reduce soil sclerotial density"
            ],
            sanitation_measures=[
                "Incorporate or burn rice stubble after harvest",
                "Skim off floating debris and sclerotia during field preparation"
            ],
            resistant_varieties="No commercial rice cultivars are completely immune; semi-dwarf cultivars are more prone than tall open-canopy varieties."
        ),
        similar_diseases=["rice__blast", "rice__stem_rot", "rice__sheath_rot"],
        severity_indicators="Banded snake-skin lesions reaching the flag leaf sheath, widespread tiller lodging.",
        sources=[SOURCE_IRRI, SOURCE_FAO, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "wheat__bacterial_leaf_streak_(black_chaff)": DiseaseRecord(
        id="wheat__bacterial_leaf_streak_(black_chaff)",
        canonical_name="Wheat Bacterial Leaf Streak and Black Chaff",
        crop="wheat",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Xanthomonas translucens pv. undulosa",
        affected_parts=[PlantPart.LEAF, PlantPart.GLUME, PlantPart.STEM, PlantPart.HEAD],
        symptoms=[
            "Foliage: Small, water-soaked, narrow, translucent streaks on leaves bounded by parallel veins",
            "Streaks turn yellowish-brown to dark brown and coalesce into long irregular necrotic stripes",
            "Diagnostic feature: In humid mornings, tiny milky-white to amber droplets of bacterial ooze form on streaks, drying into shiny resin-like scales",
            "Heads (Black Chaff): Glumes and lemmas show distinct longitudinal dark brown to purplish-black stripes and dark blotches, causing shriveled kernels"
        ],
        symptom_progression="Water-soaked leaf streaks -> amber ooze droplets drying to shiny scales -> foliar stripe necrosis -> dark black glume stripes (black chaff) -> shriveled grain.",
        development_conditions="Warm, humid, rainy, windy weather (temperatures 20-30°C), sprinkler irrigation, hail or wind-blown sand abrasion.",
        spread_transmission="Wind-driven rain, splashing water, plant-to-plant contact, contaminated seed, mechanical equipment.",
        infection_sources="Contaminated seed (primary transmission pathway), infected wheat/barley stubble in soil, volunteer cereals.",
        immediate_actions=[
            "Avoid overhead sprinkler irrigation",
            "Avoid moving field equipment through wet wheat fields",
            "Do NOT save grain from infected fields for seed planting"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Use certified pathogen-free seed, avoid overhead irrigation, practice 1-2 year crop rotation with non-grasses, and bury stubble.",
                    source_id=SOURCE_UNL.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="No chemical fungicide or bactericide is effective or registered for field rescue",
                    application_purpose="Foliar fungicides provide ZERO efficacy against bacterial leaf streak; copper bactericides cause phytotoxicity and lack economic efficacy.",
                    limitations="Chemical sprays are ineffective against internal bacterial infection.",
                    source_id=SOURCE_PENN_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant exclusively certified disease-free, tested seed lots",
                "Practice crop rotation with broadleaf crops (soybeans, sunflowers, pulses)",
                "Avoid sprinkler irrigation during heading and grain fill"
            ],
            sanitation_measures=[
                "Clean combines and seed cleaning equipment thoroughly between seed lots",
                "Destroy volunteer wheat and grassy weeds"
            ],
            resistant_varieties="Cultivars show significant genetic variation in tolerance; consult university wheat trial ratings."
        ),
        similar_diseases=["wheat__septoria_blotch", "wheat__tan_spot", "wheat__head_scab"],
        severity_indicators="Shiny dried bacterial scales on leaves, dark purple-black glume striping, >30% flag leaf necrosis.",
        sources=[SOURCE_UNL, SOURCE_PENN_STATE, SOURCE_CIMMYT, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "wheat__head_scab": DiseaseRecord(
        id="wheat__head_scab",
        canonical_name="Wheat Fusarium Head Blight (Head Scab)",
        crop="wheat",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Fusarium graminearum (teleomorph Gibberella zeae)",
        affected_parts=[PlantPart.HEAD, PlantPart.GLUME, PlantPart.STEM],
        symptoms=[
            "Premature bleaching of individual spikelets or entire heads while the rest of the head and stem remain green",
            "Bleached spikelets show a distinct salmon-pink or orange sporodochia (spore masses) at the base of the glumes during humid weather",
            "The stem directly beneath the infected head (peduncle) may develop a dark purplish-brown discoloration",
            "Kernels are shriveled, lightweight, chalky-white, pink-tinted, or tombstone-like ('tombstones'), contaminated with vomitoxin (DON mycotoxin)"
        ],
        symptom_progression="Flower infection during anthesis -> bleached spikelets with pink spore masses -> peduncle browning -> chalky shriveled 'tombstone' kernels with mycotoxins.",
        development_conditions="Warm, humid, rainy, or misty weather during flowering / anthesis (Feekes 10.5.1; temperatures 20-30°C, RH >90%).",
        spread_transmission="Airborne and rain-splashed ascospores and macroconidia.",
        infection_sources="Corn stalk residue (primary reservoir), small grain stubble on soil surface.",
        immediate_actions=[
            "Monitor regional FHB risk forecasting models (US Wheat & Barley Scab Initiative) at flag leaf/heading",
            "Apply targeted triazole/SDHI fungicide precisely at early flowering (Feekes 10.5.1 / Zadoks 60-65)",
            "Adjust combine fan speed at harvest to blow lightweight tombstone kernels out the back"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Avoid planting wheat directly into corn residue, use FHB-tolerant varieties, and adjust combine settings at harvest to discard tombstones.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Prothioconazole + Tebuconazole (Prosaro) / Metconazole (Caramba) / Pydiflumetofen + Fludioxonil (Miravis Ace)",
                    application_purpose="Specialized DMI/SDHI fungicides applied strictly at early flowering (anthesis / Feekes 10.5.1) with forward/backward angled nozzles.",
                    limitations="DO NOT apply strobilurin (FRAC 11) fungicides after heading as they increase vomitoxin (DON) levels; adhere to 30-day PHI.",
                    source_id=SOURCE_PENN_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant moderately resistant wheat cultivars with known FHB/DON tolerance",
                "Rotate with broadleaf crops (soybeans, canola) rather than following corn",
                "Stagger planting dates or hybrid maturities to avoid having all wheat flower simultaneously during rain"
            ],
            sanitation_measures=[
                "Incorporate heavy corn stalk residue where soil conservation practices permit",
                "Clean seed thoroughly to remove lightweight scabby kernels"
            ],
            resistant_varieties="Cultivars with Fhb1 gene or native quantitative resistance (e.g., Pioneer 25R74, Branson, SY 547)."
        ),
        similar_diseases=["wheat__bacterial_leaf_streak_(black_chaff)", "wheat__loose_smut", "wheat__take-all"],
        severity_indicators="Bleached spikelets with salmon-pink spore masses, chalky pink tombstone kernels, high DON vomitoxin levels.",
        sources=[SOURCE_PURDUE, SOURCE_PENN_STATE, SOURCE_UNL, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "wheat__leaf_rust": DiseaseRecord(
        id="wheat__leaf_rust",
        canonical_name="Wheat Leaf Rust (Brown Rust)",
        crop="wheat",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Puccinia triticina (syn. Puccinia recondita f. sp. tritici)",
        affected_parts=[PlantPart.LEAF, PlantPart.SHEATH],
        symptoms=[
            "Small, circular to oval, reddish-orange to brown powdery pustules (uredinia) scattered randomly across the UPPER leaf surface",
            "Pustules rupture the upper epidermis cleanly and release powdery rust spores on fingers when rubbed",
            "Leaves turn chlorotic, senesce prematurely, and dry up, reducing photosynthesis during grain filling",
            "Late in the season, pustules turn dark brown to black as overwintering teliospores form under the epidermis"
        ],
        symptom_progression="Random circular orange pustules on upper leaves -> progressive leaf chlorosis -> flag leaf destruction -> black teliospores at maturity.",
        development_conditions="Mild to warm temperatures (15-22°C), high humidity, dew periods >6-8 hours, frequent rain showers.",
        spread_transmission="Windborne urediniospores traveling hundreds of miles northward along the 'Puccinia pathway'.",
        infection_sources="Overwintered volunteer wheat in southern areas, green bridge vegetation, southern commercial fields.",
        immediate_actions=[
            "Scout lower leaves and flag leaf between jointing and heading",
            "Apply foliar fungicide at flag leaf emergence (Feekes 8-9) if rust pustules are active in the lower canopy",
            "Destroy volunteer wheat (green bridge) before autumn planting"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Propiconazole / Tebuconazole",
                    application_purpose="Systemic DMI triazole fungicide providing curative arrest of early rust mycelium.",
                    limitations="Apply at early disease onset; obey 30-35 day pre-harvest intervals.",
                    source_id=SOURCE_UNL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Destroy volunteer wheat to break the green bridge, plant resistant cultivars, and apply foliar fungicides at flag leaf emergence.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Pyraclostrobin + Fluxapyroxad / Azoxystrobin + Propiconazole",
                    application_purpose="Foliar premix fungicide applied at flag leaf emergence (Feekes 8-9) for residual leaf protection.",
                    limitations="Observe pre-harvest intervals and resistance management protocols.",
                    source_id=SOURCE_PENN_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant leaf rust-resistant wheat varieties carrying effective Lr resistance genes",
                "Destroy volunteer wheat at least 2 weeks before planting winter wheat to eliminate the green bridge",
                "Plant within the recommended fly-free/disease-safe date window in autumn"
            ],
            sanitation_measures=[
                "Eliminate volunteer wheat along field borders and roadsides"
            ],
            resistant_varieties="Cultivars with adult-plant resistance (APR) genes (e.g., Lr34, Lr46, Lr67, Lr68)."
        ),
        similar_diseases=["wheat__stripe_rust", "wheat__stem_rust"],
        severity_indicators="Randomly scattered orange pustules covering >25% of flag leaf area before milk stage.",
        sources=[SOURCE_PURDUE, SOURCE_UNL, SOURCE_PENN_STATE, SOURCE_CIMMYT],
        quality_level="HIGH"
    ),

    "wheat__loose_smut": DiseaseRecord(
        id="wheat__loose_smut",
        canonical_name="Wheat Loose Smut",
        crop="wheat",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Ustilago tritici",
        affected_parts=[PlantPart.HEAD, PlantPart.SPIKELET],
        symptoms=[
            "Infected heads emerge slightly earlier than healthy heads, completely transformed into a loose, powdery, olive-black mass of teliospores",
            "All spikelet parts (glumes, lemmas, paleas, kernels) are destroyed and replaced by black spore masses, enclosed only by a delicate membrane that ruptures immediately",
            "Wind and rain rapidly blow the black spores away, leaving behind a bare, naked, erect rachis ('skeleton spike')",
            "Plants appear entirely normal until head emergence; no foliar spots or stem stunting occur prior to heading"
        ],
        symptom_progression="Infection of embryo at flowering -> fungus resides dormant inside seed embryo -> grows systemically inside emerging shoot -> complete head transformation into black spore soot -> naked central rachis.",
        development_conditions="Cool, moist, humid weather during open flowering (Feekes 10.5.1; temperatures 16-22°C) favoring flower infection.",
        spread_transmission="Windborne teliospores landing on open flower stigmas at flowering, germinating and directly infecting developing embryos inside seed.",
        infection_sources="Infected seed containing dormant mycelium within the seed embryo.",
        immediate_actions=[
            "DO NOT save grain from infected fields for seed use",
            "Loose smut cannot be stopped in the field once black heads appear (infection occurred the previous year during bloom)",
            "Ensure all future planting seed is treated with systemic fungicide seed treatments"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Use certified disease-free seed and apply systemic fungicide seed treatments before planting.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Difenoconazole / Sedaxane / Tebuconazole / Triticonazole (Seed Treatment)",
                    application_purpose="Systemic seed treatment applied to planting seed to penetrate embryo and eliminate dormant smut mycelium.",
                    limitations="Must be applied to seed prior to planting; foliar sprays applied to headed wheat are completely useless.",
                    source_id=SOURCE_UNL.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified, disease-free seed from certified seed growers",
                "Always treat farm-saved seed with a registered systemic fungicide seed treatment",
                "Select resistant wheat varieties"
            ],
            sanitation_measures=[
                "Clean seed drills and handling equipment between seed varieties"
            ],
            resistant_varieties="Many modern wheat cultivars have genetic resistance to common Ustilago tritici races."
        ),
        similar_diseases=["wheat__head_scab", "wheat__bunt_(stinking_smut)"],
        severity_indicators="Entire head converted to olive-black powdery soot, bare naked rachis remaining after spore dispersal.",
        sources=[SOURCE_PURDUE, SOURCE_UNL, SOURCE_PENN_STATE, SOURCE_CIMMYT],
        quality_level="HIGH"
    ),

    "wheat__powdery_mildew": DiseaseRecord(
        id="wheat__powdery_mildew",
        canonical_name="Wheat Powdery Mildew",
        crop="wheat",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Blumeria graminis f. sp. tritici",
        affected_parts=[PlantPart.LEAF, PlantPart.SHEATH, PlantPart.HEAD],
        symptoms=[
            "White, fluffy, cottony to powdery fungal patches appearing first on the lower leaves and leaf sheaths",
            "Patches expand and coalesce, turning dull grayish-tan with age",
            "Tiny, black, pinhead-sized fruiting bodies (cleistothecia / chasmothecia) form embedded in the mature gray fungal felt",
            "Severe infection spreads up the plant to the flag leaf and heads, causing lower leaf yellowing, premature senescence, and lodging"
        ],
        symptom_progression="White powdery tufts on lower leaves -> dense gray felt with black cleistothecia -> ascent to flag leaf and head -> foliar chlorosis and lodging.",
        development_conditions="Cool, humid, overcast weather (temperatures 15-22°C), high relative humidity (85-100%), dense thick canopy, high nitrogen fertilization.",
        spread_transmission="Windborne conidia carried across fields; survives summer via cleistothecia on stubble.",
        infection_sources="Overwintered mycelium/cleistothecia on volunteer wheat and crop residue.",
        immediate_actions=[
            "Scout lower canopy at jointing (Feekes 5-6) and flag leaf emergence (Feekes 8-9)",
            "Apply foliar fungicide if mildew is advancing toward the flag leaf in dense stands",
            "Avoid excessive spring nitrogen top-dressing"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Metconazole / Propiconazole",
                    application_purpose="Systemic DMI triazole fungicide with curative activity against active powdery mildew colonies.",
                    limitations="Apply at early disease threshold; observe pre-harvest intervals.",
                    source_id=SOURCE_PENN_STATE.id
                )
            ],
            management=[
                CulturalControl(
                    description="Avoid excessive seeding rates and high nitrogen, select resistant varieties, and destroy volunteer wheat.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Pyraclostrobin + Fluxapyroxad / Azoxystrobin + Propiconazole",
                    application_purpose="Foliar broad-spectrum fungicide applied at flag leaf emergence for canopy protection.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_UNL.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant wheat varieties with genetic resistance (Pm genes)",
                "Avoid overly dense seeding rates and balanced nitrogen fertilization",
                "Destroy volunteer wheat prior to autumn planting"
            ],
            sanitation_measures=[
                "Bury or decompose wheat stubble"
            ],
            resistant_varieties="Cultivars carrying Pm resistance genes (e.g., Pm3, Pm8, Pm21, Pm38)."
        ),
        similar_diseases=["wheat__septoria_blotch", "wheat__leaf_rust"],
        severity_indicators="Dense white powdery felt covering flag leaf and head glumes, premature lower leaf death.",
        sources=[SOURCE_PURDUE, SOURCE_PENN_STATE, SOURCE_UNL, SOURCE_CIMMYT],
        quality_level="HIGH"
    ),

    "wheat__septoria_blotch": DiseaseRecord(
        id="wheat__septoria_blotch",
        canonical_name="Wheat Septoria Tritici Blotch (STB)",
        crop="wheat",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Zymoseptoria tritici (formerly Septoria tritici, teleomorph Mycosphaerella graminicola)",
        affected_parts=[PlantPart.LEAF, PlantPart.SHEATH],
        symptoms=[
            "Small, yellow chlorotic flecks appearing first on lower leaves in contact with the soil",
            "Flecks expand into long, irregular, light brown to tan necrotic blotches delimited by leaf veins",
            "Diagnostic feature: Abundant, tiny, pimple-like black fruiting bodies (pycnidia) clearly visible embedded inside the tan lesions (looks like black pepper sprinkles)",
            "Lesions coalesce, blighting entire leaf blades and ascending up the canopy to the flag leaf"
        ],
        symptom_progression="Yellow flecks on lower leaves -> long tan blotches with black pycnidia -> upward progression through canopy -> flag leaf necrosis and poor grain fill.",
        development_conditions="Cool, wet, rainy weather (temperatures 10-20°C), prolonged leaf wetness (>24-48 hours of rain or heavy dew), splashing rain.",
        spread_transmission="Rain-splashed pycnidiospores ascending the canopy from lower leaves; windborne ascospores.",
        infection_sources="Infected wheat stubble on soil surface, volunteer wheat seedlings.",
        immediate_actions=[
            "Scout lower leaves at jointing through flag leaf emergence (Feekes 6-9)",
            "Apply foliar fungicide at flag leaf emergence (Feekes 8-9) if pycnidia-bearing lesions are ascending the canopy",
            "Maintain balanced fertility"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Prothioconazole / Mefentrifluconazole (Revysol) / Difenoconazole",
                    application_purpose="Systemic DMI triazole fungicides providing kickback curative activity on early latent infections.",
                    limitations="Apply at early disease onset; observe resistance management guidelines.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            management=[
                CulturalControl(
                    description="Crop rotation away from wheat for 1-2 years, residue burial, and selecting resistant cultivars.",
                    source_id=SOURCE_PENN_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Fluxapyroxad + Pyraclostrobin (Nexicor) / Benzovindiflupyr + Azoxystrobin (Trivapro)",
                    application_purpose="Premix SDHI + Strobilurin/DMI fungicides applied at flag leaf emergence.",
                    limitations="Rotate modes of action to manage fungicide resistance; observe pre-harvest intervals.",
                    source_id=SOURCE_UNL.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant wheat varieties with high resistance ratings to Septoria tritici blotch (Stb genes)",
                "Practice a 2-year crop rotation with non-cereal broadleaf crops",
                "Incorporate wheat straw where soil conservation allows"
            ],
            sanitation_measures=[
                "Eradicate volunteer wheat before autumn seeding"
            ],
            resistant_varieties="Cultivars carrying Stb resistance genes (e.g., Stb6, Stb16q, Stb18)."
        ),
        similar_diseases=["wheat__tan_spot", "wheat__stagonospora_nodorum_blotch"],
        severity_indicators="High density of black pycnidia embedded in tan blotches covering >30% of flag leaf area.",
        sources=[SOURCE_PURDUE, SOURCE_PENN_STATE, SOURCE_UNL, SOURCE_CIMMYT],
        quality_level="HIGH"
    ),

    "wheat__stem_rust": DiseaseRecord(
        id="wheat__stem_rust",
        canonical_name="Wheat Stem Rust (Black Rust)",
        crop="wheat",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Puccinia graminis f. sp. tritici",
        affected_parts=[PlantPart.STEM, PlantPart.LEAF, PlantPart.SHEATH, PlantPart.GLUME],
        symptoms=[
            "Large, elongated, oval to spindle-shaped, reddish-brown powdery pustules (uredinia) erupting primarily on STEMS and leaf sheaths",
            "Pustules tear and shred the outer epidermis, leaving ragged, papery epidermic collars around the pustules",
            "Spore dust is dark reddish-brown; pustules turn black late in the season as teliospores form (hence 'black rust')",
            "Severely infected stems become brittle, lodge catastrophically, and plants lodge before harvest, causing 100% crop loss in susceptible fields"
        ],
        symptom_progression="Elongated reddish-brown pustules shredding stem epidermis -> pustule coalescence -> massive stem lodging and brittle breakage -> black teliospore formation.",
        development_conditions="Warm temperatures (20-30°C), high relative humidity, dew periods >6-8 hours, presence of alternate host common barberry (Berberis vulgaris).",
        spread_transmission="Windborne urediniospores carried thousands of miles on weather currents.",
        infection_sources="Overwintered southern wheat crops, volunteer wheat, aeciospores from common barberry bushes.",
        immediate_actions=[
            "Immediately report suspected stem rust (especially virulent races like Ug99) to extension plant pathologists",
            "Apply systemic triazole or SDHI foliar fungicide immediately upon early detection",
            "Eradicate common barberry bushes within 1 km of wheat fields"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Propiconazole / Tebuconazole",
                    application_purpose="Systemic DMI triazole fungicide applied immediately upon early detection on stems.",
                    limitations="Time-sensitive rescue treatment; observe pre-harvest intervals.",
                    source_id=SOURCE_UNL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Planting resistant cultivars with multi-genic resistance (e.g., Sr2 complex), eradicating barberry, and foliar fungicide application.",
                    source_id=SOURCE_USDA_ARS.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Pyraclostrobin + Fluxapyroxad / Azoxystrobin + Propiconazole",
                    application_purpose="Broad-spectrum foliar protection applied at heading.",
                    limitations="Observe pre-harvest intervals and resistance guidelines.",
                    source_id=SOURCE_PENN_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant wheat cultivars with complex Sr-gene resistance (e.g., Sr2, Sr25, Sr33, Sr35, Sr57)",
                "Eradicate common barberry (Berberis vulgaris) to eliminate the sexual cycle and new virulent race creation",
                "Plant early in the spring to escape late-season stem rust spore clouds"
            ],
            sanitation_measures=[
                "Eradicate volunteer wheat and barberry bushes around fields"
            ],
            resistant_varieties="Cultivars bred with Ug99 lineage resistance genes through the Borlaug Global Rust Initiative."
        ),
        similar_diseases=["wheat__leaf_rust", "wheat__stripe_rust"],
        severity_indicators="Ragged torn epidermis surrounding large reddish-brown to black pustules on stems, widespread stem lodging.",
        sources=[SOURCE_USDA_ARS, SOURCE_CIMMYT, SOURCE_FAO, SOURCE_UNL],
        quality_level="HIGH"
    ),

    "wheat__stripe_rust": DiseaseRecord(
        id="wheat__stripe_rust",
        canonical_name="Wheat Stripe Rust (Yellow Rust)",
        crop="wheat",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Puccinia striiformis f. sp. tritici",
        affected_parts=[PlantPart.LEAF, PlantPart.SHEATH, PlantPart.GLUME],
        symptoms=[
            "Bright yellow to orange-yellow powdery pustules (uredinia) arranged in distinct, long, narrow, parallel stripes along the leaf veins",
            "Stripes resemble yellow machine stitching or bead-like linear chains extending the entire length of the leaf blade",
            "Infected leaves turn chlorotic, dry out, and turn brown ('scorched' appearance)",
            "Pustules can also develop inside the glumes and lemmas of the head, causing shriveled kernels and severe test-weight reductions"
        ],
        symptom_progression="Linear yellow bead-like pustules arranged in parallel stripes -> yellowing and necrosis of interveinal tissue -> head glume infection -> shriveled grain.",
        development_conditions="Cool, wet, humid weather (temperatures 10-18°C), prolonged dew periods (>6-8 hours), high moisture.",
        spread_transmission="Windborne urediniospores traveling long distances on jet-stream winds.",
        infection_sources="Overwintering mycelium in autumn-sown winter wheat, volunteer wheat, southern wheat crops.",
        immediate_actions=[
            "Scout lower leaves in early spring (tillering to jointing) for yellow linear stripes",
            "Apply foliar fungicide immediately if stripe rust is detected early on susceptible cultivars",
            "Protect flag leaf during jointing and heading (Feekes 6-10.5)"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Propiconazole / Tebuconazole / Prothioconazole",
                    application_purpose="Systemic DMI triazole fungicide providing rapid curative arrest of active stripe rust mycelium.",
                    limitations="Apply at first detection; observe pre-harvest intervals.",
                    source_id=SOURCE_UNL.id
                )
            ],
            management=[
                CulturalControl(
                    description="Planting stripe rust-resistant cultivars (Yr genes), destroying volunteer wheat, and early spring fungicide intervention.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Pyraclostrobin + Fluxapyroxad / Azoxystrobin + Difenoconazole",
                    application_purpose="Premix fungicide applied at flag leaf emergence for long-lasting residual control.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_PENN_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant wheat cultivars with high resistance ratings (carrying Yr genes like Yr18/Lr34, Yr29, Yr36)",
                "Destroy volunteer wheat in late summer to break the green bridge",
                "Avoid excessive spring nitrogen fertilization"
            ],
            sanitation_measures=[
                "Eliminate volunteer wheat around field borders"
            ],
            resistant_varieties="Cultivars with high-temperature adult-plant (HTAP) resistance and all-stage Yr gene combinations."
        ),
        similar_diseases=["wheat__leaf_rust", "wheat__stem_rust"],
        severity_indicators="Bright yellow parallel linear stripes covering >30% of flag leaf, head glume infection.",
        sources=[SOURCE_PURDUE, SOURCE_UNL, SOURCE_PENN_STATE, SOURCE_CIMMYT],
        quality_level="HIGH"
    ),
}
