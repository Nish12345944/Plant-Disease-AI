"""
Authoritative Plant Pathology Knowledge: Legume & Pulse Crops (10 diseases)
- Bean: Angular Leaf Spot, Halo Blight, Mosaic Virus (BCMV), Rust
- Soybean: Bacterial Blight, Brown Spot (Septoria), Downy Mildew, Frogeye Leaf Spot, Mosaic Virus (SMV), Rust (Asian Soybean Rust)
Sources: Purdue Extension, Iowa State Extension, NC State Extension, UF/IFAS, USDA ARS, FAO, CIAT.
"""

from knowledge.schema import (
    DiseaseRecord, PathogenType, PlantPart, TreatmentPlan,
    ChemicalControl, CulturalControl, BiologicalControl, PreventionProtocol
)
from knowledge.sources import (
    SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_NC_STATE, SOURCE_UF_IFAS,
    SOURCE_USDA_ARS, SOURCE_FAO, SOURCE_CORNELL, SOURCE_UC_IPM
)

LEGUME_DISEASES = {
    "bean__angular_leaf_spot": DiseaseRecord(
        id="bean__angular_leaf_spot",
        canonical_name="Bean Angular Leaf Spot",
        crop="bean",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Pseudocercospora griseola (formerly Phaeoisariopsis griseola)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.POD],
        symptoms=[
            "Small, angular, brown to tan spots on leaves strictly delimited by veins",
            "On lower surface of leaf spots, tiny dark grayish synnemata (spore-bearing stalks) are visible under magnification",
            "Severe infection causes extensive chlorosis, premature defoliation, and stem lesions",
            "Pods develop circular to elliptical, sunken, reddish-brown spots with dark borders, damaging seed quality"
        ],
        symptom_progression="Angular vein-bounded spots on lower leaves -> synnemata sporulation on underside -> upward defoliation -> sunken pod spots and seed decay.",
        development_conditions="Moderate to warm temperatures (20-24°C), high relative humidity (>95%), alternating wet and dry periods, rain splash.",
        spread_transmission="Windborne and rain-splashed conidia, contaminated seed, workers moving through wet fields.",
        infection_sources="Infected crop residues, contaminated seed (primary pathway), volunteer bean plants.",
        immediate_actions=[
            "Avoid entering or cultivating fields when foliage is wet",
            "Apply protective fungicides (e.g., copper or azoxystrobin) at first symptom onset",
            "Do NOT save seed from infected fields for future planting"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Switch to drip irrigation, avoid touching wet plants, use 2-year crop rotation with non-legumes, and bury crop residues.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide / Copper Oxychloride",
                    application_purpose="Contact protectant spray applied at flowering and pod set.",
                    limitations="Preventive only; ensure thorough coverage of lower foliage.",
                    source_id=SOURCE_NC_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Pyraclostrobin",
                    application_purpose="Systemic strobilurin fungicide for foliar and pod disease suppression.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Use certified disease-free seed from arid western seed-producing regions",
                "Practice a minimum 2-year crop rotation with non-legumes (corn, cereals, brassicas)",
                "Ensure proper plant spacing for canopy aeration"
            ],
            sanitation_measures=[
                "Incorporate crop residues deeply after harvest to accelerate decomposition"
            ],
            resistant_varieties="Cultivars show gene-for-gene resistance; Mesoamerican and Andean gene pools offer specific Phg resistance genes."
        ),
        similar_diseases=["bean__halo_blight", "bean__bacterial_brown_spot"],
        severity_indicators="Angular vein-delimited spots with gray synnemata, defoliation >30%, sunken reddish-brown pod lesions.",
        sources=[SOURCE_NC_STATE, SOURCE_PURDUE, SOURCE_USDA_ARS, SOURCE_FAO],
        quality_level="HIGH"
    ),

    "bean__halo_blight": DiseaseRecord(
        id="bean__halo_blight",
        canonical_name="Bean Halo Blight",
        crop="bean",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Pseudomonas savastanoi pv. phaseolicola (syn. Pseudomonas syringae pv. phaseolicola)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.POD, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Small, water-soaked, pinpoint angular spots on the underside of leaves",
            "Spots develop a wide, conspicuous, light greenish-yellow to bright chlorotic halo (halo effect caused by phaseolotoxin)",
            "Systemic chlorosis: young emerging leaves turn completely pale yellow/lime-green without distinct spots in cool weather",
            "Pods develop circular, water-soaked, dark green greasy-looking spots with white to cream-colored bacterial ooze"
        ],
        symptom_progression="Water-soaked specks -> wide chlorotic yellow halos -> systemic apical yellowing -> greasy pod spots with white bacterial ooze.",
        development_conditions="Cool, wet, humid weather (temperatures 16-22°C), rainstorms, overhead irrigation, wet foliage operations.",
        spread_transmission="Wind-driven rain, splashing water, machinery moving through wet fields, contaminated seed.",
        infection_sources="Contaminated seed (primary source), infected crop residues, volunteer bean plants.",
        immediate_actions=[
            "Cease all field cultivation, weeding, and spraying while foliage is wet",
            "Apply copper bactericide at first detection to protect healthy surrounding plants",
            "Do NOT save seed from affected fields"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Strict avoidance of working in wet fields, drip irrigation, 2-3 year crop rotation, and planting certified seed.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact bactericide applied preventively to reduce bacterial populations on leaf surfaces.",
                    limitations="Preventive application only; cannot cure internal systemic infection; avoid copper injury in hot weather.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant exclusively certified disease-free, western-grown seed",
                "Practice a 2-3 year crop rotation away from dry and snap beans",
                "Use drip irrigation to prevent bacterial splash dispersal"
            ],
            sanitation_measures=[
                "Incorporate crop residues immediately after harvest",
                "Disinfect harvesting equipment between fields"
            ],
            resistant_varieties="Cultivars carrying resistance genes to specific halo blight races (e.g., Pse-1, Pse-2, Pse-3, Pse-4)."
        ),
        similar_diseases=["bean__common_bacterial_blight", "bean__angular_leaf_spot"],
        severity_indicators="Wide prominent yellow halos around leaf spots, systemic bright yellow top growth, greasy pod lesions with white ooze.",
        sources=[SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_CORNELL, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "bean__mosaic_virus": DiseaseRecord(
        id="bean__mosaic_virus",
        canonical_name="Bean Common Mosaic Virus (BCMV)",
        crop="bean",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Bean common mosaic virus (BCMV, Potyvirus)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.POD, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Prominent light and dark green mottled mosaic pattern on leaves",
            "Downward curling, cupping, puckering, and blistering of leaf blades",
            "Leaves become narrowed, elongated, and distorted; plants become stunted and bushy",
            "Systemic necrosis / black root: in cultivars carrying the dominant I gene without protective genes, high temperatures trigger rapid black vascular wilting and plant death; pods are mottled and distorted"
        ],
        symptom_progression="Vein clearing -> mottled green mosaic and puckering -> leaf curling and stunting -> black root necrosis in hypersensitive cultivars -> deformed pods with infected seed.",
        development_conditions="Warm weather supporting high aphid populations (Acyrthosiphon pisum, Myzus persicae, Aphis fabae).",
        spread_transmission="Non-persistently transmitted within seconds by numerous aphid species; seedborne (up to 30-80% seed transmission); mechanically via sap.",
        infection_sources="Infected bean seed (primary source), volunteer beans, infected wild legume hosts.",
        immediate_actions=[
            "Rogue out and destroy infected symptomatic plants immediately",
            "Do NOT save seed from symptomatic plants",
            "Control aphid vector populations with insecticidal soaps or mineral oils"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Rogue infected plants early, plant certified virus-free seed, and use reflective mulches to deter aphids.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Stylet-Oil / Insecticidal Soap",
                    application_purpose="Foliar sprays to reduce aphid transmission efficiency.",
                    limitations="Must be reapplied frequently with complete coverage.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified virus-tested, disease-free seed",
                "Select BCMV-resistant bean cultivars carrying the dominant I gene combined with recessive bc genes",
                "Plant early before aphid migration flights peak"
            ],
            sanitation_measures=[
                "Eradicate wild legume weeds around field borders"
            ],
            resistant_varieties="Most modern commercial snap and dry bean cultivars carry the dominant I gene or protected I + bc-3 combinations."
        ),
        similar_diseases=["bean__yellow_mosaic_virus", "cucumber_mosaic_virus"],
        severity_indicators="Severe foliar blistering and downward cupping, black root vascular collapse, mottled deformed pods.",
        sources=[SOURCE_PURDUE, SOURCE_UC_IPM, SOURCE_NC_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "bean__rust": DiseaseRecord(
        id="bean__rust",
        canonical_name="Bean Rust",
        crop="bean",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Uromyces appendiculatus (syn. Uromyces phaseoli)",
        affected_parts=[PlantPart.LEAF, PlantPart.POD, PlantPart.STEM],
        symptoms=[
            "Small, circular, yellowish to whitish chlorotic spots on leaves",
            "Spots erupt into raised, reddish-brown powdery pustules (uredinia) on BOTH upper and lower leaf surfaces",
            "Pustules are often surrounded by a distinct chlorotic yellow halo",
            "Severely infected leaves turn yellow, brown, dry out, and drop prematurely (severe defoliation); pods develop pustules that degrade quality"
        ],
        symptom_progression="Yellow flecks -> reddish-brown powdery pustules erupting on leaves and pods -> leaf yellowing and shedding -> black teliospores at maturity.",
        development_conditions="Moderate temperatures (17-27°C), high relative humidity (>95%), prolonged leaf wetness (>8-10 hours of dew or rain).",
        spread_transmission="Airborne urediniospores blown across long distances by wind currents; rain splashing; autoecious (completes entire cycle on bean).",
        infection_sources="Overwintered bean crop residues in soil, volunteer beans, alternate wild Phaseolus species.",
        immediate_actions=[
            "Scout lower canopy leaves weekly for reddish-brown powdery pustules",
            "Apply protective or DMI fungicides upon first appearance of pustules",
            "Avoid overhead irrigation to keep foliage dry"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Propiconazole / Tebuconazole",
                    application_purpose="Systemic DMI triazole fungicide providing curative arrest of early rust mycelium.",
                    limitations="Apply at first symptom detection; observe pre-harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            management=[
                CulturalControl(
                    description="Crop rotation (2 years), deep plowing of crop residues, wide plant spacing for airflow, and drip irrigation.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Contact protectant fungicide applied preventively at early bloom/pod set.",
                    limitations="Preventive application; observe pre-harvest intervals.",
                    source_id=SOURCE_PURDUE.id
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin / Pyraclostrobin",
                    application_purpose="Systemic strobilurin fungicide for comprehensive rust management.",
                    limitations="Rotate FRAC groups to manage resistance.",
                    source_id=SOURCE_UF_IFAS.id
                ),
                ChemicalControl(
                    active_ingredient="Sulfur (Wettable)",
                    application_purpose="Organic contact protectant.",
                    limitations="Do not apply above 30°C or within 14 days of oil sprays.",
                    source_id=SOURCE_UC_IPM.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant rust-resistant bean cultivars carrying Ur resistance genes",
                "Practice a minimum 2-year crop rotation away from beans",
                "Ensure drip irrigation to prevent leaf wetness"
            ],
            sanitation_measures=[
                "Incorporate or destroy crop debris thoroughly after harvest"
            ],
            resistant_varieties="Cultivars carrying specific Ur resistance genes (e.g., Ur-3, Ur-4, Ur-5, Ur-11)."
        ),
        similar_diseases=["bean__angular_leaf_spot", "soybean__rust"],
        severity_indicators="Reddish-brown powdery pustules covering >25% of leaf area, premature defoliation, pustules on pods.",
        sources=[SOURCE_PURDUE, SOURCE_NC_STATE, SOURCE_UF_IFAS, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "soybean__bacterial_blight": DiseaseRecord(
        id="soybean__bacterial_blight",
        canonical_name="Soybean Bacterial Blight",
        crop="soybean",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Pseudomonas savastanoi pv. glycinea (syn. Pseudomonas syringae pv. glycinea)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.POD],
        symptoms=[
            "Small, angular, water-soaked, translucent spots on leaves bounded by veins",
            "Spots turn reddish-brown to black with a prominent yellow chlorotic halo",
            "Lesions coalesce into large dead necrotic patches; dead center tissue tears away, giving leaves a ragged, shredded appearance ('tattered leaves')",
            "Symptoms appear predominantly in the upper canopy following strong rainstorms with high winds"
        ],
        symptom_progression="Angular water-soaked spots -> black spots with yellow halos -> coalescence and tissue tearing -> ragged tattered upper canopy leaves.",
        development_conditions="Cool, wet, rainy, windy weather (temperatures 20-26°C), hail or wind-driven rain causing plant abrasions.",
        spread_transmission="Wind-driven rain, splashing water, machinery moving through wet fields, contaminated seed.",
        infection_sources="Infected soybean residue on the soil surface, contaminated seed.",
        immediate_actions=[
            "Avoid field cultivation or driving equipment through fields while foliage is wet",
            "Disease typically halts naturally when hot, dry summer weather (>30°C) arrives",
            "Do NOT apply fungal fungicides (they have zero efficacy against bacteria)"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Avoid working in wet fields, practice crop rotation with non-hosts (corn, small grains), and use residue management.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Copper Hydroxide",
                    application_purpose="Contact bactericide; rarely economically justified on commercial field soybeans.",
                    limitations="Preventive only; may cause slight phytotoxicity; check economic thresholds.",
                    source_id=SOURCE_IOWA_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified disease-free seed",
                "Practice a 1-2 year rotation away from soybeans",
                "Select resistant/tolerant soybean varieties (Rpg resistance genes)"
            ],
            sanitation_measures=[
                "Incorporate heavy soybean residue where soil erosion permits"
            ],
            resistant_varieties="Cultivars carrying specific Rpg resistance genes (Rpg1, Rpg2, Rpg3, Rpg4)."
        ),
        similar_diseases=["soybean__brown_spot", "soybean__frog_eye_leaf_spot", "soybean__bacterial_pustule"],
        severity_indicators="Extensive leaf tattering and ragged holes in upper canopy, angular black spots with bright yellow halos.",
        sources=[SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "soybean__brown_spot": DiseaseRecord(
        id="soybean__brown_spot",
        canonical_name="Soybean Septoria Brown Spot",
        crop="soybean",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Septoria glycines",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.POD],
        symptoms=[
            "Small, irregular, dark brown to black spots appearing first on lower unifoliate and trifoliate leaves",
            "Spots are surrounded by a diffuse chlorotic yellow halo",
            "Spots enlarge and coalesce into large, dark brown necrotic blotches; infected lower leaves turn yellow and drop prematurely",
            "Disease progresses upward from lower to middle canopy during extended wet, rainy periods"
        ],
        symptom_progression="Lower leaf dark brown spots with yellow halos -> leaf yellowing and shedding -> gradual upward progression -> lower canopy defoliation.",
        development_conditions="Warm, wet, humid weather (temperatures 20-28°C), frequent rains, dense canopy, continuous no-till soybean.",
        spread_transmission="Rain-splashed conidia ascending the canopy from soil residue.",
        infection_sources="Infected soybean residue on the soil surface (primary reservoir).",
        immediate_actions=[
            "Scout lower and middle canopy at R1-R3 (flowering to pod development)",
            "Apply foliar fungicide at R3 if disease is actively advancing into the upper canopy on susceptible varieties",
            "Rotate crops post-harvest"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Crop rotation with corn or small grains, residue incorporation, and selecting tolerant varieties.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Pyraclostrobin + Fluxapyroxad (Priaxor) / Azoxystrobin + Difenoconazole (Quadris Top)",
                    application_purpose="Premix fungicide applied at R3 (early pod set) to prevent upward progression.",
                    limitations="Observe pre-harvest intervals and resistance guidelines.",
                    source_id=SOURCE_IOWA_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Practice a 1-2 year rotation with non-host crops (corn, wheat, sorghum)",
                "Select soybean varieties with good standability and horizontal disease tolerance",
                "Ensure optimal planting populations"
            ],
            sanitation_measures=[
                "Incorporate soybean residue"
            ],
            resistant_varieties="Varieties show varying tolerance; university trial ratings indicate varietal response."
        ),
        similar_diseases=["soybean__bacterial_blight", "soybean__frog_eye_leaf_spot"],
        severity_indicators="Dark brown blotches ascending past mid-canopy, extensive lower canopy defoliation before pod fill.",
        sources=[SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "soybean__downy_mildew": DiseaseRecord(
        id="soybean__downy_mildew",
        canonical_name="Soybean Downy Mildew",
        crop="soybean",
        pathogen_type=PathogenType.OOMYCETE,
        pathogen_name="Peronospora manshurica",
        affected_parts=[PlantPart.LEAF, PlantPart.POD, PlantPart.SEED],
        symptoms=[
            "Pale green to bright yellow, irregular chlorotic spots on the upper leaf surface",
            "Spots turn grayish-brown to dark brown with a distinct yellowish-green border",
            "A delicate, fluffy, grayish-white to pale purplish downy mold develops on the corresponding lower leaf surface under humid conditions",
            "Infected pods may show no external symptoms, but internal seeds are encrusted with a white, crusty, chalky coating of fungal oospores"
        ],
        symptom_progression="Upper leaf yellow spots -> grayish-purple downy mold on underside -> leaf browning -> chalky oospore coating on harvested seeds.",
        development_conditions="Cool, humid, wet weather (temperatures 18-24°C), prolonged high relative humidity, heavy dews.",
        spread_transmission="Windborne sporangia; seedborne oospores encrusting seeds; oospores in crop residue.",
        infection_sources="Infected soybean residue, oospore-encrusted seed.",
        immediate_actions=[
            "Scout upper leaves in cool wet periods for yellow spots with lower-surface downy mold",
            "Foliar fungicide application is rarely necessary or economically justified for downy mildew alone",
            "Do NOT use oospore-encrusted grain for planting seed"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Planting resistant varieties (carrying Rpm genes), seed fungicide treatment, and 1-year crop rotation.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Mefenoxam / Metalaxyl (Seed Treatment)",
                    application_purpose="Systemic seed treatment applied to planting seed to eliminate seedborne oospores.",
                    limitations="Preventive seed treatment only.",
                    source_id=SOURCE_IOWA_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant soybean varieties with genetic resistance (Rpm resistance genes)",
                "Use certified disease-free, professionally treated seed",
                "Practice crop rotation with corn or small grains"
            ],
            sanitation_measures=[
                "Incorporate infected soybean stubble"
            ],
            resistant_varieties="Cultivars carrying specific Rpm resistance genes (e.g., Rpm1)."
        ),
        similar_diseases=["soybean__bacterial_blight", "soybean__brown_spot"],
        severity_indicators="Fluffy grayish-purple downy sporulation on leaf undersides, white crusty oospore crust on seed coats.",
        sources=[SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "soybean__frog_eye_leaf_spot": DiseaseRecord(
        id="soybean__frog_eye_leaf_spot",
        canonical_name="Soybean Frogeye Leaf Spot",
        crop="soybean",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cercospora sojina",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.POD, PlantPart.SEED],
        symptoms=[
            "Small, circular to angular spots (1-5 mm) on upper leaf surfaces",
            "Spots have a light gray to ash-colored or tan center surrounded by a narrow, dark reddish-brown to purple border ('frogeye' appearance)",
            "Underside of mature spots develops dark gray velvety clusters of conidiophores in the center during humid weather",
            "Lesions coalesce, causing leaf blighting, premature defoliation, stem lesions, and circular sunken reddish-brown spots on pods"
        ],
        symptom_progression="Circular gray-centered spots with purple rings on upper canopy -> gray velvety centers on underside -> foliar blighting -> pod lesions and seed staining.",
        development_conditions="Warm, humid, rainy weather (temperatures 25-30°C), relative humidity >90%, extended dew periods, continuous soybean.",
        spread_transmission="Windborne and rain-splashed conidia; contaminated seed.",
        infection_sources="Infected soybean residue on soil surface, contaminated seed.",
        immediate_actions=[
            "Scout middle and upper canopy at R1-R4 (flowering through pod development)",
            "Apply foliar fungicide with MULTIPLE modes of action at R3 (early pod) if spots appear on susceptible varieties",
            "Note: High prevalence of Quinone Outside Inhibitor (QoI / FRAC 11 strobilurin) resistance requires tank-mixing with DMI (FRAC 3) or SDHI (FRAC 7)"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Prothioconazole / Difenoconazole / Tetraconazole",
                    application_purpose="Systemic DMI triazole fungicide with curative activity against strobilurin-resistant strains.",
                    limitations="Apply at R3; observe resistance management guidelines.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            management=[
                CulturalControl(
                    description="Planting Rcs-resistant varieties (Rcs3 gene), multi-mode-of-action fungicides at R3, and 1-2 year crop rotation.",
                    source_id=SOURCE_IOWA_STATE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Fluxapyroxad + Pyraclostrobin + Difenoconazole (Revyloc / Lucento / Miravis Top)",
                    application_purpose="Multi-mode-of-action premix fungicide (FRAC 7 + 11 + 3) applied at R3 for comprehensive protection.",
                    limitations="DO NOT apply solo FRAC 11 strobilurins due to widespread QoI resistance.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant soybean varieties with Rcs3 genetic resistance (provides broad resistance to all known North American races)",
                "Practice a 2-year crop rotation with non-host crops (corn, sorghum, small grains)",
                "Use certified disease-free, fungicide-treated seed"
            ],
            sanitation_measures=[
                "Incorporate soybean residue"
            ],
            resistant_varieties="Cultivars carrying the Rcs3 single dominant resistance gene."
        ),
        similar_diseases=["soybean__bacterial_blight", "soybean__brown_spot", "soybean__target_spot"],
        severity_indicators="Abundant frogeye lesions across upper canopy leaves at R3-R5, premature defoliation, sunken pod lesions.",
        sources=[SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_NC_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "soybean__mosaic": DiseaseRecord(
        id="soybean__mosaic",
        canonical_name="Soybean Mosaic Virus (SMV)",
        crop="soybean",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Soybean mosaic virus (SMV, Potyvirus)",
        affected_parts=[PlantPart.LEAF, PlantPart.STEM, PlantPart.POD, PlantPart.SEED, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Yellow vein clearing on young leaves, advancing into light and dark green mosaic patterns",
            "Leaves become blistered, puckered, wrinkled, and curl downward along leaf margins",
            "Plant stunting, shortened internodes, and reduced pod set; pods are smaller, curved, flattened, and contain fewer seeds",
            "Seed coat mottling: seeds show dark brown or black pigment bleeding outward from the hilum across the seed coat"
        ],
        symptom_progression="Vein clearing -> leaf blistering and downward curling -> plant stunting -> reduced distorted pods -> seed coat discoloration/mottling.",
        development_conditions="Cool temperatures (20-25°C) intensify leaf symptoms; warm weather with active soybean aphid (Aphis glycines) migrations.",
        spread_transmission="Non-persistently vectored by >30 aphid species including the soybean aphid (Aphis glycines); seedborne (up to 5-30%); mechanical sap transmission.",
        infection_sources="Infected soybean seed (primary source), volunteer soybeans, wild legume hosts.",
        immediate_actions=[
            "Do NOT save mottled grain for planting seed",
            "Rogue out early symptomatic plants in seed production plots",
            "Control aphid populations during early vegetative stages"
        ],
        treatment=TreatmentPlan(
            curative=[],
            management=[
                CulturalControl(
                    description="Planting certified virus-free seed, selecting Rsv-resistant varieties, and controlling aphid vectors.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Insecticide vector control has limited efficacy for non-persistently transmitted viruses; management relies on genetics and clean seed.",
                    application_purpose="Aphicides target vector populations but cannot halt non-persistent transmission across fields.",
                    limitations="Chemical sprays cannot cure viral infections.",
                    source_id=SOURCE_IOWA_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant certified, disease-free seed with zero or low seed coat mottling",
                "Plant SMV-resistant soybean varieties carrying Rsv resistance genes (Rsv1, Rsv3, Rsv4)",
                "Plant within the normal planting window to minimize early aphid exposure"
            ],
            sanitation_measures=[
                "Destroy volunteer soybeans and wild legume weeds"
            ],
            resistant_varieties="Cultivars carrying Rsv1, Rsv3, or Rsv4 resistance genes."
        ),
        similar_diseases=["bean__mosaic_virus", "bean__pod_mottle_virus"],
        severity_indicators="Severe leaf puckering and downward rolling, plant stunting, dark brown/black pigment bleeding across seed coats.",
        sources=[SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),

    "soybean__rust": DiseaseRecord(
        id="soybean__rust",
        canonical_name="Soybean Rust (Asian Soybean Rust / ASR)",
        crop="soybean",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Phakopsora pachyrhizi",
        affected_parts=[PlantPart.LEAF, PlantPart.PETIOLE, PlantPart.STEM, PlantPart.POD],
        symptoms=[
            "Small, pinpoint, tan to dark reddish-brown polygonal lesions appearing first on lower canopy leaves",
            "Diagnostic feature: Volcaniform raised rust pustules (uredinia) with a central pore erupting predominantly on the LOWER leaf surface inside lesions (caused by Phakopsora pachyrhizi)",
            "Tan lesions produce abundant powdery tan urediniospores; reddish-brown lesions produce fewer spores",
            "Disease moves rapidly up the canopy, causing massive leaf yellowing, rapid defoliation, premature plant death, and complete yield collapse within 10-14 days"
        ],
        symptom_progression="Pinpoint lower leaf specks -> volcaniform raised uredinia on underside -> rapid upward canopy climb -> total field-wide defoliation and pod abortion.",
        development_conditions="Temperatures 15-28°C, prolonged leaf wetness (6-12 hours of rain or heavy dew), relative humidity >75-80%.",
        spread_transmission="Windborne urediniospores carried hundreds to thousands of miles on hurricane/storm fronts.",
        infection_sources="Overwintered kudzu (Pueraria montana var. lobata) in southern coastal zones, continuous green-bridge legume hosts.",
        immediate_actions=[
            "Track regional soybean rust sentinel plot monitoring (sbr.ipmpipe.org)",
            "Apply foliar fungicide at R1-R3 immediately if rust is detected within 100 miles during favorable weather",
            "Ensure spray penetration into the lower and middle canopy using high pressure and high volume"
        ],
        treatment=TreatmentPlan(
            curative=[
                ChemicalControl(
                    active_ingredient="Prothioconazole / Tebuconazole / Flutriafol",
                    application_purpose="Systemic DMI triazole fungicides with curative activity applied at early detection (pustules present on <5% of lower leaves).",
                    limitations="Apply promptly; curative efficacy drops dramatically once rust advances past lower canopy; obey pre-harvest intervals.",
                    source_id=SOURCE_UF_IFAS.id
                )
            ],
            management=[
                CulturalControl(
                    description="Monitoring IPM pipe sentinel networks, early planting to mature before rust arrival, and targeted multi-mode fungicides at R3.",
                    source_id=SOURCE_PURDUE.id
                )
            ],
            chemical=[
                ChemicalControl(
                    active_ingredient="Pyraclostrobin + Fluxapyroxad + Difenoconazole / Azoxystrobin + Propiconazole",
                    application_purpose="Multi-mode-of-action premix fungicide (FRAC 11 + 7 + 3) applied at R3 for residual canopy protection.",
                    limitations="Rotate FRAC groups to prevent resistance.",
                    source_id=SOURCE_IOWA_STATE.id
                ),
                ChemicalControl(
                    active_ingredient="Chlorothalonil / Mancozeb",
                    application_purpose="Contact multi-site protectant tank-mixed with systemic fungicides to manage resistance.",
                    limitations="Preventive application; observe harvest intervals.",
                    source_id=SOURCE_NC_STATE.id
                )
            ],
            biological=[]
        ),
        prevention=PreventionProtocol(
            cultural_practices=[
                "Plant early in the spring to promote pod filling before airborne rust spore showers arrive from the south",
                "Eradicate kudzu patches near soybean production fields",
                "Use narrow row spacing only if adequate spray penetration into lower canopy can be maintained"
            ],
            sanitation_measures=[
                "Residue management does not control rust because the pathogen does not overwinter in freezing soils"
            ],
            resistant_varieties="Commercial cultivars with Rpp resistance genes (Rpp1 through Rpp6) are being developed; current management relies heavily on fungicides."
        ),
        similar_diseases=["soybean__bacterial_pustule", "soybean__brown_spot", "soybean__frog_eye_leaf_spot"],
        severity_indicators="Volcaniform cone-shaped uredinia on leaf undersides, rapid upward canopy defoliation, premature pod drop.",
        sources=[SOURCE_UF_IFAS, SOURCE_PURDUE, SOURCE_IOWA_STATE, SOURCE_NC_STATE, SOURCE_USDA_ARS],
        quality_level="HIGH"
    ),
}
