"""
Authoritative Commodity Modules Builder for all 116 Model 2 V4 Disease Classes.
Generates knowledge/data/ commodity modules with 100% exact class name coverage.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 1. FRUIT DISEASES (16)
FRUIT_RECORDS = """
FRUIT_DISEASES: dict[str, DiseaseRecord] = {
    "apple__black_rot": DiseaseRecord(
        disease_id="apple__black_rot",
        canonical_name="Apple Black Rot (Frogeye Leaf Spot)",
        crop_name="apple",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Botryosphaeria obtusa",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.TWIG, PlantPart.STEM],
        symptoms=[
            "Small purple spots on upper leaf surfaces that enlarge into circular lesions with light brown/tan centers and dark purple margins (frogeye leaf spot)",
            "Sunken, reddish-brown circular decay on fruit expanding into dark concentric zones with embedded black pycnidia pimples",
            "Firm, leathery rot turning the entire fruit into a shriveled, pitch-black mummified apple that clings to twigs",
            "Sunken, reddish-brown cankers on branches and scaffold limbs with cracked, peeling bark",
        ],
        symptom_progression="Ascospores/conidia infect leaves in spring -> frogeye spots appear within 1-3 weeks -> summer spores infect fruit via wounds/calyx -> black concentric fruit rot develops near harvest -> mummified apples overwinter on tree.",
        favorable_conditions="Warm temperatures (20-27 deg C), high relative humidity, frequent rainfall, mechanical/insect wounding, and dead wood/cankers left in canopy.",
        transmission_mode="Airborne ascospores from overwintered limb cankers; rain-splashed conidia from mummies; pruning shears.",
        primary_sources=["Overwintered mummified apples hanging in the tree canopy", "Dead wood, pruning brush piles, and fire-blight-killed twigs"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Prune out all dead wood, cankered limbs, and fire-blight-killed twigs during dormant winter pruning",
                "Remove and burn or deeply bury all hanging and fallen mummified apples",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Canopy sanitation and dead wood removal",
                    timing="Dormant season (late winter)",
                    purpose="Eliminate the primary overwintering reservoir of Botryosphaeria obtusa spores",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Pruning brush disposal",
                    timing="Immediately following pruning",
                    purpose="Remove or shred prunings to prevent sporulation on dead brush",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens",
                    target_stage="Bloom to petal fall",
                    application_method="Foliar spray applied during early vegetative flush",
                    source=SOURCE_CORNELL.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Captan / Mancozeb (Protectant)",
                    target_pathogen="Botryosphaeria obtusa",
                    application_method="Foliar protective spray applied from tight cluster through cover sprays at 10-14 day intervals",
                    restrictions="Follow label rates and legal pre-harvest intervals (Mancozeb 77-day PHI; Captan 0-day PHI)",
                    source=SOURCE_PENN_STATE.name,
                ),
                ChemicalControl(
                    active_ingredient="Thiophanate-methyl, Pyraclostrobin + Boscalid, or Difenoconazole",
                    target_pathogen="Botryosphaeria obtusa",
                    application_method="Foliar spray applied at petal fall and cover sprays",
                    restrictions="Rotate FRAC groups to prevent fungicide resistance",
                    source=SOURCE_PURDUE.name,
                ),
            ],
            organic_alternatives=[
                "Fixed copper fungicides applied at delayed dormant stage",
                "Sulfur or potassium bicarbonate sprays during early season",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=[
                "Inspect tree canopy during winter and remove 100% of mummified apples",
                "Cut out limb cankers 15-20 cm below the lowest visible bark discoloration",
            ],
            cultural_preventions=[
                "Open tree canopies with corrective pruning to allow rapid air drying after rain",
                "Manage insect pests (curculio, codling moth) to avoid fruit entry wounds",
            ],
            resistant_varieties="Most apple cultivars are susceptible; Honeycrisp and Rome Beauty show high susceptibility; manage via sanitation",
            monitoring_schedule="Scout leaves starting at petal fall for frogeye spots; inspect fruit monthly through harvest",
        ),
        differential_diagnosis=[
            "Cedar Apple Rust (Gymnosporangium juniperi-virginianae) - produces bright orange-yellow spots with spermagonia rather than purple-bordered frogeye spots",
            "Bitter Rot (Colletotrichum spp.) - causes saucer-shaped sunken lesions with gelatinous salmon-pink spore masses in hot weather",
        ],
        severity_indicators="Pitch-black mummified fruit; deep girdling limb cankers; defoliation exceeding 30%.",
        treatment_limitations="Fungicide sprays cannot cure established limb cankers or restore rotten fruit; sanitation is essential.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_CORNELL, SOURCE_PENN_STATE, SOURCE_PURDUE, SOURCE_USDA_ARS],
    ),

    "apple__mosaic_virus": DiseaseRecord(
        disease_id="apple__mosaic_virus",
        canonical_name="Apple Mosaic Virus (ApMV)",
        crop_name="apple",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Apple Mosaic Virus (ApMV) - Ilarvirus",
        affected_parts=[PlantPart.LEAF, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Distinct pale yellow, creamy-white to bright yellow chlorotic spots, blotches, and mosaic banding along leaf veins",
            "Oak-leaf or chevron patterns of yellow banding on mature spring leaves",
            "In hot summer weather, yellowed leaf areas become necrotic, dry out, turn brown, and drop prematurely",
            "Symptom expression is most severe on spring foliage and masked during high summer temperatures",
            "Severe infections reduce tree vigor, yield by 20-40%, and graft union strength.",
        ],
        symptom_progression="Virus introduces systemically through grafting/budding -> spring flush leaves show vivid yellow vein banding -> high summer heat causes chlorotic patches to turn brown and scorched -> infected trees show reduced annual terminal growth.",
        favorable_conditions="Cool to moderate spring temperatures (15-22 deg C) favor symptom expression; warm temperatures (>28 deg C) mask foliar symptoms.",
        transmission_mode="Vegetative propagation (grafting, budding, top-working, infected rootstocks); root grafting between adjacent trees; NOT transmitted by aphids or seed.",
        primary_sources=["Infected budwood or rootstock propagation material", "Natural root grafting in mature high-density orchards"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "DO NOT spray fungicides or bactericides - VIRUSES CANNOT BE CURED WITH CHEMICAL SPRAYS",
                "Mark and map infected trees; do not collect budwood or scions from symptomatic trees",
                "If young high-density blocks show extensive stunting, rogue out infected trees during orchard renovation",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Certified virus-tested nursery stock use",
                    timing="At orchard planting",
                    purpose="Ensure planting material is free of systemic ilarviruses",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Root severance between trees",
                    timing="Orchard maintenance",
                    purpose="Subsoil trenching between rows to sever root grafts connecting infected and healthy trees",
                    effectiveness="Medium",
                ),
            ],
            biological_controls=[],
            chemical_controls=[],
            organic_alternatives=[
                "Use certified virus-free rootstocks (e.g., EMLA or Geneva series produced from heat-treated nuclear stock)",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=[
                "Never propagate from uncertified or symptom-expressing scion mother trees",
                "Sanitize budding knives with 70% alcohol between trees during top-working",
            ],
            cultural_preventions=[
                "Plant exclusively certified virus-tested trees from accredited nurseries",
                "Thermotherapy (heat therapy at 36-38 deg C for 3-4 weeks) of shoot tips in tissue culture propagation",
            ],
            resistant_varieties="Golden Delicious, Jonathan, and Granny Smith express severe symptoms; Red Delicious shows milder expression",
            monitoring_schedule="Scout orchard blocks in late spring (May-June) when yellow mosaic and oak-leaf patterns are most vivid",
        ),
        differential_diagnosis=[
            "Iron / Zinc micronutrient deficiency - causes uniform interveinal chlorosis across young leaves without distinct creamy-white vein banding or oak-leaf patterns",
            "Leafhopper feeding injury - produces stippled white specks on upper leaf surface rather than systemic yellow mosaic banding",
        ],
        severity_indicators="Severe yellow oak-leaf vein banding across >50% of canopy; premature summer defoliation; severe tree stunting.",
        treatment_limitations="NO chemical spray can cure ApMV in an infected tree; management relies on clean planting stock and roguing.",
        quality_level="HIGH",
        treatment_category="no established cure",
        sources=[SOURCE_CORNELL, SOURCE_WSU, SOURCE_USDA_ARS, SOURCE_CABI],
    ),

    "apple__rust": DiseaseRecord(
        disease_id="apple__rust",
        canonical_name="Apple Rust (Cedar Apple Rust / Quince Rust / Hawthorn Rust)",
        crop_name="apple",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Gymnosporangium juniperi-virginianae / Gymnosporangium clavipes",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.TWIG],
        symptoms=[
            "Bright, conspicuous yellow-orange to reddish-orange circular spots on upper leaf surfaces in late spring",
            "Tiny black pimple-like dots (spermagonia) visible inside the center of orange spots",
            "Lower leaf surface directly beneath spots develops raised, tube-like cylindrical projections (aecia) that split open releasing rusty powdery spores",
            "Fruit symptoms: raised, puckered, yellowish-orange lesions near the calyx end of the apple",
            "Severe infection leads to early summer defoliation and reduced fruit size.",
        ],
        symptom_progression="Spring rains trigger gelatinous orange telial horns on cedar galls -> basidiospores blow to apple leaves -> bright orange spots form within 10-14 days -> tubular aecia form on leaf underside in mid-summer -> aeciospores blow back to junipers.",
        favorable_conditions="Warm, rainy spring weather (13-24 deg C) coinciding with apple bud break through petal fall, and presence of Eastern red cedar (Juniperus virginiana) within 1-2 miles.",
        transmission_mode="Wind-borne basidiospores from cedar galls to apple; wind-borne aeciospores from apple to cedar; heteroecious life cycle.",
        primary_sources=["Overwintered cedar galls on Juniperus virginiana and ornamental junipers within 1-2 miles"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Remove Eastern red cedar trees or prune out brown cedar galls within 500-1000 feet of the orchard perimeter",
                "Apply protectant or DMI systemic fungicide starting at pink bud through petal fall and first cover",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Cedar gall removal and alternate host eradication",
                    timing="Late winter / early spring before spring rains",
                    purpose="Cut out galls on surrounding junipers before gelatinous telial horns emerge",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens",
                    target_stage="Pink bud to petal fall",
                    application_method="Foliar spray applied at early bloom",
                    source=SOURCE_CORNELL.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Myclobutanil, Fenbuconazole, or Difenoconazole (DMI / Triazoles)",
                    target_pathogen="Gymnosporangium juniperi-virginianae",
                    application_method="Foliar spray applied at pink bud, bloom, petal fall, and first cover",
                    restrictions="Follow label rates and pre-harvest intervals; triazoles offer strong kick-back activity",
                    source=SOURCE_CORNELL.name,
                ),
                ChemicalControl(
                    active_ingredient="Mancozeb (Protectant)",
                    target_pathogen="Gymnosporangium spp.",
                    application_method="Foliar spray applied from tight cluster to petal fall",
                    restrictions="Adhere to 77-day pre-harvest interval; protect beneficial predatory mites",
                    source=SOURCE_PENN_STATE.name,
                ),
            ],
            organic_alternatives=[
                "Wettable sulfur or liquid lime sulfur applied at pink bud and petal fall",
                "Planting cedar-apple-rust-resistant apple varieties",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=["Eradicate red cedar trees within 500 feet of orchard boundaries"],
            cultural_preventions=[
                "Plant rust-resistant apple cultivars (e.g., Liberty, Enterprise, Freedom, Pristine)",
                "Avoid planting ornamental junipers near commercial or home orchards",
            ],
            resistant_varieties="Liberty, Enterprise, Freedom, Pristine, Redfree (highly resistant; Gala, Golden Delicious, Honeycrisp, Rome are susceptible)",
            monitoring_schedule="Inspect cedar trees for swollen galls in late winter; scout apple leaves weekly from bloom through June",
        ),
        differential_diagnosis=[
            "Apple Black Rot (Botrytis / Botryosphaeria) - produces frogeye spots with purple margins and gray centers without bright orange coloration or tubular aecia",
            "Apple Scab - produces olive-green to black velvety spots without bright orange color or spermagonia",
        ],
        severity_indicators="Bright orange spots with underside tubular aecia covering >25% of canopy; calyx-end fruit distortion.",
        treatment_limitations="Fungicide sprays applied after tubular aecia have formed on apple leaves provide zero curative benefit.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_CORNELL, SOURCE_PENN_STATE, SOURCE_PURDUE, SOURCE_NC_STATE],
    ),

    "apple__scab": DiseaseRecord(
        disease_id="apple__scab",
        canonical_name="Apple Scab",
        crop_name="apple",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Venturia inaequalis",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.TWIG],
        symptoms=[
            "Olive-green to dull brownish-black, velvety spots on upper and lower leaf surfaces with feathery, indistinct margins",
            "Spots become raised, dark olive-brown to corky, causing leaves to pucker, curl, and drop prematurely",
            "Fruit symptoms: distinct circular, olive-green spots that become sunken, brown, corky, and rough (scabby)",
            "Fruit infected early becomes misshapen, cracked, stunted, and severely deformed",
            "Severe early-season defoliation weakens trees and drastically reduces fruit marketability.",
        ],
        symptom_progression="Ascospores discharge from overwintered leaf litter during spring rains -> infect young emerging leaves -> velvety olive-green conidial lesions form in 9-17 days -> secondary summer conidia infect developing fruit -> corky scab lesions and fruit cracking.",
        favorable_conditions="Cool, wet spring weather (temperatures 13-24 deg C), prolonged leaf wetness (6-12+ hours depending on temperature per Mills Scab Table), and heavy rainfall during bud break through petal fall.",
        transmission_mode="Airborne ascospores from overwintered fallen leaves; rain-splashed conidia within the tree canopy.",
        primary_sources=["Overwintered infected fallen apple leaves on the orchard floor"],
        treatment_plan=ImmediateActionPlan := TreatmentPlan(
            immediate_actions=[
                "Apply urea (5% solution) or shred fallen leaves with a flail mower in autumn/early spring to accelerate leaf decomposition",
                "Apply protectant or systemic fungicide at green tip, continuing through primary ascospore discharge period (petal fall)",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Leaf litter shredding and urea application",
                    timing="Post-harvest / late autumn or early spring",
                    purpose="Accelerate microbial breakdown of fallen leaves to eliminate overwintering pseudothecia",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Canopy pruning for air penetration",
                    timing="Dormant season",
                    purpose="Open the tree canopy to facilitate fast leaf drying and improve spray penetration",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens",
                    target_stage="Green tip through petal fall",
                    application_method="Foliar spray applied before predicted rain events",
                    source=SOURCE_CORNELL.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Captan or Mancozeb (Protectant)",
                    target_pathogen="Venturia inaequalis",
                    application_method="Foliar protective spray applied at green tip, tight cluster, pink bud, bloom, and petal fall",
                    restrictions="Follow label rates; maintain continuous protective barrier before rain events; adhere to PHIs",
                    source=SOURCE_CORNELL.name,
                ),
                ChemicalControl(
                    active_ingredient="Difenoconazole, Cyprodinil, or Fluopyram (Systemic / Curative)",
                    target_pathogen="Venturia inaequalis",
                    application_method="Foliar spray applied within 48-72 hours after start of an infection period",
                    restrictions="Strict resistance management: tank-mix with protectant (Captan); rotate FRAC groups (FRAC 3, 9, 7)",
                    source=SOURCE_PENN_STATE.name,
                ),
            ],
            organic_alternatives=[
                "Liquid lime sulfur or wettable sulfur applied preventatively before rain",
                "Autumn leaf shredding and flail mowing to destroy pseudothecia",
                "Planting scab-resistant apple cultivars possessing the Vf gene",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=[
                "Mow and shred fallen apple leaf litter in late autumn to reduce spring ascospore load by 80-90%",
                "Apply 5% agricultural urea to fallen leaves to speed decomposition",
            ],
            cultural_preventions=[
                "Plant scab-resistant apple cultivars carrying the Vf resistance gene (e.g., Liberty, Enterprise, Pristine, GoldRush)",
                "Use the Mills Table / NEWA apple scab forecasting model to time sprays accurately",
            ],
            resistant_varieties="Liberty, Enterprise, Pristine, GoldRush, Freedom, CrimsonCrisp (possessing Vf resistance; McIntosh, Gala, Fuji, Cortland are highly susceptible)",
            monitoring_schedule="Scout green tip through petal fall using NEWA scab infection models; inspect cluster leaves weekly",
        ),
        differential_diagnosis=[
            "Apple Black Rot (Botryosphaeria obtusa) - produces frogeye leaf spots with purple margins rather than olive-green velvety feathery spots",
            "Powdery Mildew - produces white talcum powder coating on shoot tips rather than dark olive-green velvety spots",
        ],
        severity_indicators="Olive-velvety lesions covering >20% of cluster leaves; corky cracked fruit lesions; premature June drop.",
        treatment_limitations="Fungicide sprays cannot repair corky cracked fruit lesions; primary ascospore control in spring is critical.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_CORNELL, SOURCE_PENN_STATE, SOURCE_PURDUE, SOURCE_USDA_ARS],
    ),

    "cherry__leaf_spot": DiseaseRecord(
        disease_id="cherry__leaf_spot",
        canonical_name="Cherry Leaf Spot (Shot-Hole / Yellow Leaf)",
        crop_name="cherry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Blumeriella jaapii (syn. Coccomyces hiemalis)",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.STEM],
        symptoms=[
            "Small, circular, purple to reddish-brown spots (1-3 mm) appearing on upper leaf surfaces in late spring",
            "Centers of spots may dry out and drop out, creating a 'shot-hole' appearance",
            "Under humid conditions, whitish-pink gelatinous masses of conidial spores ooze from the underside of leaf spots",
            "Infected leaves turn bright yellow (chlorosis) except for green halos around spots ('yellow leaf')",
            "Massive premature defoliation by mid-summer, leaving trees bare, reducing cold hardiness, and stunting fruit buds.",
        ],
        symptom_progression="Ascospores discharge from overwintered leaf litter during spring rains -> infect unfolding leaves -> purple spots form -> conidia erupt on underside -> leaves turn bright yellow and drop -> severe mid-summer defoliation.",
        favorable_conditions="Moderate temperatures (16-24 deg C), frequent rainfall, high relative humidity, and prolonged leaf wetness (minimum 5-8 hours).",
        transmission_mode="Wind-dispersed airborne ascospores from overwintered leaves; rain-splashed conidia for secondary spread.",
        primary_sources=["Overwintered infected fallen cherry leaves on the orchard floor"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Shred or disk fallen leaves in autumn or apply urea spray to accelerate microbial leaf breakdown",
                "Apply protectant or systemic fungicide starting at petal fall / shuck split, continuing at 10-14 day intervals through post-harvest",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Leaf litter shredding and urea application",
                    timing="Post-harvest / autumn",
                    purpose="Accelerate decomposition of fallen leaves to eliminate overwintering apothecia",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Canopy pruning and aeration",
                    timing="Late winter / post-harvest",
                    purpose="Improve air circulation and sunlight penetration to shorten leaf wetness periods",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens",
                    target_stage="Petal fall to cover sprays",
                    application_method="Foliar spray applied before predicted rain",
                    source=SOURCE_MSU.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Captan or Chlorothalonil (Protectant)",
                    target_pathogen="Blumeriella jaapii",
                    application_method="Foliar spray applied at petal fall, shuck split, and first to third cover sprays",
                    restrictions="Follow label rates; chlorothalonil must NOT be applied after shuck split on cherries (fruit marking)",
                    source=SOURCE_MSU.name,
                ),
                ChemicalControl(
                    active_ingredient="Fluopyram + Trifloxystrobin or Fenbuconazole (SDHI / DMI)",
                    target_pathogen="Blumeriella jaapii",
                    application_method="Foliar spray applied during cover sprays and post-harvest",
                    restrictions="Strict resistance management: rotate FRAC groups (FRAC 7, 11, 3); adhere to label PHI",
                    source=SOURCE_PENN_STATE.name,
                ),
            ],
            organic_alternatives=[
                "Fixed copper fungicides applied at post-harvest stage",
                "Liquid lime sulfur or wettable sulfur applied during early season",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=[
                "Shred fallen leaves with a flail mower in autumn to eliminate overwintering spore reservoirs",
                "Apply 5% urea spray to orchard floor after leaf fall",
            ],
            cultural_preventions=[
                "Prune trees to open canopy and allow fast drying after morning dew",
                "Avoid overhead irrigation",
            ],
            resistant_varieties="Tart / sour cherry cultivars (Montmorency) are highly susceptible; sweet cherry cultivars vary in susceptibility",
            monitoring_schedule="Scout lower canopy leaves weekly starting at petal fall through harvest and post-harvest",
        ),
        differential_diagnosis=[
            "Bacterial Canker / Shot-Hole (Pseudomonas syringae) - produces angular water-soaked spots with dark margins on leaves and gumming cankers on twigs (Cherry leaf spot produces circular purple spots with yellowing leaves)",
            "Cherry Powdery Mildew - produces white powdery mycelium on leaves and shoot tips without purple spots or bright yellow leaf drop",
        ],
        severity_indicators="Extensive bright yellow leaves dropping in June/July; defoliation >50% before harvest; bare scaffold branches.",
        treatment_limitations="Fungicide cannot re-attach fallen leaves; post-harvest sprays are critical to protect winter hardiness.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_MSU, SOURCE_PENN_STATE, SOURCE_CORNELL, SOURCE_PURDUE],
    ),

    "cherry__powdery_mildew": DiseaseRecord(
        disease_id="cherry__powdery_mildew",
        canonical_name="Cherry Powdery Mildew",
        crop_name="cherry",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Podosphaera clandestina (syn. Podosphaera oxyacanthae)",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.TWIG],
        symptoms=[
            "White, powdery, talcum-powder-like fungal patches appearing first on the underside of young expanding leaves and green shoot tips",
            "Infected leaves cup, curl upward, become distorted, and develop yellow or necrotic patches",
            "Severe shoot infection causes terminal stunting, shortened internodes, and distorted foliage",
            "Fruit symptoms: circular, sunken, white powdery patches on green and ripening cherries, causing fruit blemishes, cracking, and unmarketability",
            "Tiny black chasmothecia pimples embedded within older white powdery mats late in the season.",
        ],
        symptom_progression="Ascospores from overwintered chasmothecia on bark/twigs infect young leaves in spring -> white powdery patches form on leaf undersides -> conidia spread to developing green fruit -> fruit becomes scarred and unmarketable.",
        favorable_conditions="Warm, dry daytime weather (temperatures 18-28 deg C) with high relative humidity at night, dense shaded canopies, and vigorous succulent shoot growth (does NOT require rain).",
        transmission_mode="Airborne ascospores in early spring; wind-dispersed conidia throughout late spring and summer.",
        primary_sources=["Overwintering chasmothecia lodged in tree bark crevices, crotches, and dead leaves in the tree canopy"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Apply protectant or systemic mildewicide starting at shuck fall (when fruit becomes susceptible) through harvest",
                "Ensure spray coverage reaches both leaf undersides and developing green fruit clusters",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Canopy pruning and water sprout removal",
                    timing="Dormant season and summer pruning",
                    purpose="Remove dense, shaded, succulent sucker growth that serves as primary powdery mildew infection courts",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Avoid excessive nitrogen fertilization",
                    timing="Spring / early summer",
                    purpose="Prevent excessive succulent vegetative growth flushes",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus amyloliquefaciens / Bacillus subtilis",
                    target_stage="Shuck fall through cover sprays",
                    application_method="Foliar spray applied at early fruit development",
                    source=SOURCE_WSU.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Sulfur / Wettable sulfur (Protectant)",
                    target_pathogen="Podosphaera clandestina",
                    application_method="Foliar protective spray applied at 10-14 day intervals starting at shuck fall",
                    restrictions="Do not apply sulfur when temperatures exceed 30 deg C (phytotoxicity risk); follow label rates",
                    source=SOURCE_WSU.name,
                ),
                ChemicalControl(
                    active_ingredient="Quintec (Quinoxyfen), Luna Sensation (Fluopyram + Trifloxystrobin), or Difenoconazole",
                    target_pathogen="Podosphaera clandestina",
                    application_method="Foliar spray applied at shuck fall, first cover, and pre-harvest",
                    restrictions="Strict resistance management: rotate FRAC groups (FRAC 13, 7, 11, 3); follow label PHI",
                    source=SOURCE_PENN_STATE.name,
                ),
            ],
            organic_alternatives=[
                "Wettable sulfur or potassium bicarbonate (MilStop) foliar sprays",
                "Horticultural mineral oils applied during early vegetative flush",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=["Prune out heavily infected shoot tips and water sprouts during summer pruning"],
            cultural_preventions=[
                "Prune trees to open canopy and allow maximum sunlight penetration",
                "Manage irrigation to avoid drought stress alternating with lush growth spurts",
            ],
            resistant_varieties="Sweet cherry cultivars (Bing, Rainier, Chelan) are highly susceptible; tart cherries show variable tolerance",
            monitoring_schedule="Inspect lower leaf undersides and water sprouts weekly starting at shuck split; check green fruit clusters",
        ),
        differential_diagnosis=[
            "Cherry Leaf Spot (Blumeriella jaapii) - produces purple spots and bright yellow leaf drop without white powdery coating",
            "Apple Powdery Mildew - attacks apple foliage and shoots (Podosphaera leucotricha)",
        ],
        severity_indicators="White powdery fungal mats covering green fruit; distorted, cupped terminal shoots; scarred unmarketable cherries.",
        treatment_limitations="Fungicides cannot remove scar blemishes from already infected fruit; sprays must protect green fruit from shuck fall until harvest.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_WSU, SOURCE_PENN_STATE, SOURCE_CORNELL, SOURCE_UC_IPM],
    ),

    "peach__anthracnose": DiseaseRecord(
        disease_id="peach__anthracnose",
        canonical_name="Peach Anthracnose",
        crop_name="peach",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Colletotrichum acutatum / Colletotrichum gloeosporioides",
        affected_parts=[PlantPart.FRUIT, PlantPart.LEAF, PlantPart.TWIG],
        symptoms=[
            "Circular, sunken, crater-like necrotic spots on green and ripening peach fruit",
            "Lesions develop a characteristic dark brown to black target-ring appearance with salmon-pink to orange gelatinous spore masses in the center",
            "Infected fruit rots rapidly and turns into a hard, dark mummified peach that clings to the tree",
            "Twig dieback and small dark elliptical cankers on young shoots",
            "Leaves develop small reddish-brown necrotic spots with yellow halos.",
        ],
        symptom_progression="Spores splash from infected twigs/mummies in warm spring rains -> infect developing fruit -> latent infections emerge as fruit ripens -> sunken crater lesions erupt with bright salmon-pink spore masses -> fruit mummifies.",
        favorable_conditions="Warm, humid, rainy weather (temperatures 24-30 deg C), prolonged rain events, heavy dew, and dense unpruned tree canopies in subtropical/warm peach regions.",
        transmission_mode="Rain-splashed conidia; wind-driven rain; contaminated pruning tools; harvesting equipment.",
        primary_sources=["Overwintered mummified peaches in canopy or orchard floor", "Infected twig cankers and dead wood"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Prune out all dead twigs, cankers, and mummified peaches during dormant pruning",
                "Apply protectant or systemic fungicide starting at bloom / shuck split through pre-harvest during warm rainy periods",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Canopy pruning and sanitation",
                    timing="Dormant season",
                    purpose="Remove mummified fruit and dead wood to eliminate Colletotrichum spore sources",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens",
                    target_stage="Bloom to petal fall",
                    application_method="Foliar spray applied during early fruit development",
                    source=SOURCE_UF_IFAS.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Captan (Protectant)",
                    target_pathogen="Colletotrichum spp.",
                    application_method="Foliar protective spray applied at shuck split and cover sprays at 10-14 day intervals",
                    restrictions="Follow label rates and pre-harvest intervals; maintain continuous coverage",
                    source=SOURCE_UF_IFAS.name,
                ),
                ChemicalControl(
                    active_ingredient="Azoxystrobin, Pyraclostrobin + Boscalid, or Difenoconazole",
                    target_pathogen="Colletotrichum acutatum",
                    application_method="Foliar spray applied during pre-harvest cover sprays",
                    restrictions="Strict resistance management: rotate FRAC groups (FRAC 11, 7, 3); follow label PHI",
                    source=SOURCE_UGA.name,
                ),
            ],
            organic_alternatives=[
                "Fixed copper fungicides applied at dormant stage",
                "Sulfur or bio-fungicides applied preventatively before rain events",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=["Remove all mummies and cankered twigs from the orchard and burn or bury them"],
            cultural_preventions=[
                "Prune open-center vase canopies to allow rapid sunlight penetration and air movement",
                "Avoid overhead irrigation",
            ],
            resistant_varieties="Most commercial peach cultivars are susceptible; cultivars with firm flesh show slightly lower rot severity",
            monitoring_schedule="Scout green fruit monthly from shuck split through harvest; check for sunken crater spots and pink spores",
        ),
        differential_diagnosis=[
            "Peach Brown Rot (Monilinia fructicola) - produces soft brown rot covered in tan/gray powdery spore tufts rather than sunken crater spots with bright salmon-pink gelatinous spore masses",
            "Peach Scab (Cladosporium carpophilum) - produces superficial small olive-green/black freckle spots without deep sunken craters or salmon-pink spores",
        ],
        severity_indicators="Sunken crater lesions with salmon-pink spore masses covering ripening fruit; fruit mummification.",
        treatment_limitations="Fungicide cannot rescue already sunken rotting fruit; preventative bloom-to-harvest protection is essential.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_UF_IFAS, SOURCE_UGA, SOURCE_NC_STATE, SOURCE_TAMU],
    ),

    "peach__brown_rot": DiseaseRecord(
        disease_id="peach__brown_rot",
        canonical_name="Peach Brown Rot",
        crop_name="peach",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Monilinia fructicola / Monilinia laxa",
        affected_parts=[PlantPart.FLOWER, PlantPart.FRUIT, PlantPart.TWIG],
        symptoms=[
            "Blossom blight: open flowers turn brown, water-soaked, wilt, and collapse, often remaining glued to the twig by gummy exudate",
            "Twig cankers: small elliptical cankers girdling green twigs beneath blighted blossoms, exuding clear to amber gum",
            "Fruit rot: rapidly expanding, soft, circular, brown water-soaked rot on ripening fruit",
            "Dense, powdery, tan to grayish-brown tufts of fungal spores (monilioid conidia) covering the rotting fruit surface in concentric rings",
            "Infected fruit rots completely within 48-72 hours, shriveling into hard, wrinkled, dark brown/black mummies that cling to branches over winter.",
        ],
        symptom_progression="Airborne ascospores/conidia infect blossoms in spring -> blossom blight and twig cankers develop -> conidia infect ripening fruit through wounds or direct contact -> fruit rots rapidly into gray-brown mold -> mummified peaches overwinter on tree.",
        favorable_conditions="Warm, humid, rainy weather (temperatures 20-27 deg C), frequent rainfall, morning dew, insect feeding wounds (curculio, oriental fruit moth), and touching fruit clusters.",
        transmission_mode="Wind-dispersed airborne conidia; rain splash from mummies and twig cankers; insect vectors (fruit flies, beetles); handling.",
        primary_sources=["Overwintered mummified peaches hanging on trees or on the orchard floor", "Overwintered twig cankers"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Remove and destroy all hanging and fallen mummified peaches during dormant pruning",
                "Prune out all blighted twigs and gumming cankers",
                "Apply protectant or systemic fungicide at pink bud / full bloom for blossom blight, and at 3 weeks, 2 weeks, and 1 day pre-harvest for fruit rot",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Mummy removal and canopy sanitation",
                    timing="Dormant season (winter)",
                    purpose="Eliminate the primary overwintering source of Monilinia fructicola conidia and ascospores",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Fruit thinning",
                    timing="Early summer (pit hardening)",
                    purpose="Thin peaches to 15-20 cm apart to prevent touching fruit clusters that foster rapid rot spread",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens / Aureobasidium pullulans",
                    target_stage="Bloom and pre-harvest window",
                    application_method="Foliar spray applied at 50% bloom and 7 days pre-harvest",
                    source=SOURCE_CORNELL.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Propiconazole, Tebuconazole, or Difenoconazole (DMI / Triazoles)",
                    target_pathogen="Monilinia fructicola",
                    application_method="Foliar spray applied at pink bud, full bloom, and during the 3-week pre-harvest ripening window",
                    restrictions="Follow label rates and legal pre-harvest intervals; rotate with different FRAC groups to prevent resistance",
                    source=SOURCE_PENN_STATE.name,
                ),
                ChemicalControl(
                    active_ingredient="Fluopyram + Trifloxystrobin or Cyprodinil + Fludioxonil",
                    target_pathogen="Monilinia fructicola",
                    application_method="Foliar spray applied during pre-harvest cover sprays",
                    restrictions="Strict resistance management: maximum 2 applications per season; adhere to label PHI",
                    source=SOURCE_UGA.name,
                ),
            ],
            organic_alternatives=[
                "Wettable sulfur or liquid lime sulfur applied at bloom and pre-harvest",
                "Aggressive mummy removal and fruit thinning",
                "Bio-fungicides based on Bacillus species",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=[
                "Remove 100% of mummified fruit from trees and ground during winter pruning",
                "Sanitize harvesting lugs and sorting belts daily during harvest",
            ],
            cultural_preventions=[
                "Thin fruit clusters to eliminate touching fruit surfaces",
                "Manage plum curculio and oriental fruit moth to prevent insect entry wounds",
            ],
            resistant_varieties="All commercial peach cultivars are susceptible; cultivars with firm flesh (e.g., Elberta, Glohaven) show slightly slower rot spread",
            monitoring_schedule="Scout blossoms at 20-80% bloom; inspect ripening fruit weekly starting 4 weeks before harvest",
        ),
        differential_diagnosis=[
            "Peach Anthracnose (Colletotrichum acutatum) - produces sunken crater lesions with bright salmon-pink spore masses (Brown rot produces soft rot with tan/gray powdery spore tufts)",
            "Rhizopus Rot - produces coarse whisker-like black-spotted mold on warm harvested fruit (Brown rot produces uniform tan/gray powdery spore tufts)",
        ],
        severity_indicators="Tan/gray powdery spore tufts covering ripening fruit; blossom blight with gumming cankers; mummified fruit clusters.",
        treatment_limitations="Fungicides cannot cure already rotting fruit; sprays during bloom and the 3-week pre-harvest ripening window are mandatory.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_PENN_STATE, SOURCE_UGA, SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_USDA_ARS],
    ),

    "peach__leaf_curl": DiseaseRecord(
        disease_id="peach__leaf_curl",
        canonical_name="Peach Leaf Curl",
        crop_name="peach",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Taphrina deformans",
        affected_parts=[PlantPart.LEAF, PlantPart.TWIG, PlantPart.FRUIT],
        symptoms=[
            "Newly emerged spring leaves become severely thickened, puckered, twisted, and curled",
            "Distorted leaf areas turn bright reddish-purple, pink, or yellow",
            "As leaves age, distorted areas develop a powdery, grayish-velvety bloom (naked asci releasing ascospores)",
            "Infected leaves turn brown, wither, and drop prematurely in late spring, forcing the tree to expend energy growing a second flush of foliage",
            "Young green shoots become swollen, stunted, and distorted; fruit may develop raised reddish warty bumps.",
        ],
        symptom_progression="Overwintered blastospores on bark/bud scales infect bud scales during bud swell -> leaves emerge thickened and curled red/yellow -> velvety gray spores erupt -> leaves turn brown and drop by June -> tree re-foliates at high energy cost.",
        favorable_conditions="Cool, wet spring weather (temperatures 10-18 deg C) coinciding with bud swell and bud break, and prolonged rainfall or heavy fog (>12-24 hours).",
        transmission_mode="Rain-splashed blastospores from bark crevices and bud scales onto newly expanding bud tissue; NOT airborne over long distances.",
        primary_sources=["Overwintered blastospores surviving in bark crevices and under bud scales on the tree itself"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "CRITICAL TIMING: Apply a single thorough dormant fungicide spray in late autumn after leaf fall (November/December) OR in late winter before bud swell (January/February)",
                "Spraying AFTER buds have swollen or after leaves have emerged curled is 100% INEFFECTIVE",
                "If leaf curl defoliates the tree, apply light nitrogen fertilization and ensure adequate irrigation to support the second leaf flush",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Dormant spray timing",
                    timing="After 90% leaf fall in autumn OR before bud swell in late winter",
                    purpose="Eradicate overwintered Taphrina blastospores on bark before they can penetrate expanding bud scales",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Supplemental watering and nitrogen for defoliated trees",
                    timing="Late spring after leaf drop",
                    purpose="Help defoliated trees recover and produce a healthy second canopy flush without drought stress",
                    effectiveness="Medium",
                ),
            ],
            biological_controls=[],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Copper hydroxide, Copper oxychloride, or Bordeaux mixture (Fixed copper)",
                    target_pathogen="Taphrina deformans",
                    application_method="High-volume dormant wash applied to the entire tree trunk and branches until run-off",
                    restrictions="Apply strictly during dormancy before green tissue emerges to prevent phytotoxicity; follow label rates",
                    source=SOURCE_UC_IPM.name,
                ),
                ChemicalControl(
                    active_ingredient="Chlorothalonil or Liquid lime sulfur",
                    target_pathogen="Taphrina deformans",
                    application_method="Dormant spray applied in late winter before bud swell",
                    restrictions="Follow product label safety directions; do not apply chlorothalonil after bloom",
                    source=SOURCE_PENN_STATE.name,
                ),
            ],
            organic_alternatives=[
                "Dormant application of liquid lime sulfur or fixed copper fungicides",
                "Planting peach leaf curl-resistant cultivars (e.g., Frost, Avalon Pride, Q-1-8)",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=["Ensure thorough dormant spray coverage reaching all bark crevices and bud scales"],
            cultural_preventions=[
                "Plant peach cultivars with documented resistance to peach leaf curl",
                "Schedule dormant spray annually without skipping seasons",
            ],
            resistant_varieties="Frost, Avalon Pride, Mary Jane, Q-1-8, Muir (possessing high resistance; Redhaven, Elberta, Reliance are highly susceptible)",
            monitoring_schedule="Inspect expanding leaf buds at spring green-up for early red thickening and curling",
        ),
        differential_diagnosis=[
            "Green Peach Aphid (Myzus persicae) feeding - causes leaf curling and puckering, but leaves remain normal green and contain active aphid colonies inside curled rolls (Leaf curl causes thick, rubbery, red/yellow tissue without aphids)",
            "Plum Pocket Disease (Taphrina communis) - attacks plum fruit causing enlarged spongy bladder fruit",
        ],
        severity_indicators="Thick rubbery red/purple curled leaves covering >40% of canopy; premature leaf drop in early June.",
        treatment_limitations="Fungicide sprays applied in spring after symptoms are visible on leaves are 100% ineffective; dormant timing is mandatory.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_UC_IPM, SOURCE_PENN_STATE, SOURCE_CORNELL, SOURCE_PURDUE],
    ),

    "peach__rust": DiseaseRecord(
        disease_id="peach__rust",
        canonical_name="Peach Rust (Stone Fruit Rust)",
        crop_name="peach",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Tranzschelia discolor (syn. Tranzschelia pruni-spinosae)",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.TWIG],
        symptoms=[
            "Small, pale yellow, angular chlorotic spots on upper leaf surfaces in mid-to-late summer",
            "Lower leaf surface directly beneath spots develops powdery, dusty, chocolate-brown to cinnamon-brown pustules (uredinia)",
            "Severe infection causes leaves to turn yellow and drop prematurely (autumn defoliation), weakening flower buds for the next season",
            "Fruit symptoms: small, circular, sunken green spots on yellow fruit with reddish-brown halo, developing brown spore pustules",
            "Twig cankers: small blister-like longitudinal splits on young green twigs.",
        ],
        symptom_progression="Airborne urediniospores land on leaves in spring/summer -> yellow spots appear on upper surface -> dusty chocolate-brown pustules erupt on underside in 10-14 days -> defoliation accelerates in late summer -> teliospores overwinter on twigs.",
        favorable_conditions="Warm temperatures (20-28 deg C), high relative humidity, frequent summer rain showers, morning fog, or heavy dew; dense unpruned canopies.",
        transmission_mode="Wind-dispersed airborne urediniospores; rain splash from overwintered twig cankers; alternate hosts (Anemone spp.).",
        primary_sources=["Overwintered twig cankers on peach branches", "Alternate ranunculaceous weed hosts (Anemone spp.)"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Apply protectant or systemic fungicide if rust pustules appear on lower foliage in mid-summer",
                "Ensure spray coverage reaches the lower surface of leaves across the entire canopy",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Canopy pruning and aeration",
                    timing="Dormant season and summer pruning",
                    purpose="Improve air circulation and sunlight penetration to shorten leaf wetness periods",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens",
                    target_stage="Summer foliar spray",
                    application_method="Foliar spray applied at early symptom detection",
                    source=SOURCE_UF_IFAS.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Sulfur / Wettable sulfur (Protectant)",
                    target_pathogen="Tranzschelia discolor",
                    application_method="Foliar spray applied at 10-14 day intervals starting in mid-summer",
                    restrictions="Avoid spraying sulfur when temperatures exceed 30 deg C; follow label rates",
                    source=SOURCE_UC_IPM.name,
                ),
                ChemicalControl(
                    active_ingredient="Myclobutanil, Tebuconazole, or Difenoconazole (DMI / Triazoles)",
                    target_pathogen="Tranzschelia discolor",
                    application_method="Foliar spray applied at first appearance of yellow leaf spotting",
                    restrictions="Rotate FRAC groups to prevent resistance; adhere to legal pre-harvest intervals",
                    source=SOURCE_UF_IFAS.name,
                ),
            ],
            organic_alternatives=[
                "Wettable sulfur or potassium bicarbonate foliar sprays during cool periods",
                "Fixed copper fungicides applied at post-harvest stage",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=["Prune out twig cankers during dormant pruning"],
            cultural_preventions=[
                "Avoid overhead irrigation; use under-tree drip or micro-sprinklers",
                "Maintain open tree canopies to accelerate leaf drying",
            ],
            resistant_varieties="Most commercial peach and nectarine cultivars are susceptible; maintain preventative sprays in humid climates",
            monitoring_schedule="Scout lower leaf undersides bi-weekly from mid-summer (July) through autumn leaf drop",
        ),
        differential_diagnosis=[
            "Peach Bacterial Spot (Xanthomonas arboricola) - produces angular purple/brown spots that drop out creating shot-holes without powdery chocolate-brown spores on the underside",
            "Peach Scab (Cladosporium carpophilum) - produces olive-green/black freckles on fruit and twigs without powdery brown pustules on leaf undersides",
        ],
        severity_indicators="Chocolate-brown powdery pustules covering >30% of leaf undersides; premature autumn defoliation before natural dormancy.",
        treatment_limitations="Fungicides cannot re-green yellowed leaves; post-harvest sprays are critical to prevent early defoliation and flower bud death.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_UC_IPM, SOURCE_UF_IFAS, SOURCE_UGA, SOURCE_TAMU],
    ),

    "peach__scab": DiseaseRecord(
        disease_id="peach__scab",
        canonical_name="Peach Scab (Freckles)",
        crop_name="peach",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Cladosporium carpophilum (syn. Venturia carpophila)",
        affected_parts=[PlantPart.FRUIT, PlantPart.TWIG, PlantPart.LEAF],
        symptoms=[
            "Fruit symptoms: small, circular, olive-green to dark brown or black velvety spots (freckles, 1-3 mm) on the stem end / sun-exposed side of the peach",
            "Lesions multiply and coalesce, forming large, rough, corky, dark crusts that cause the peach skin and flesh to crack open",
            "Cracked fruit is invaded by secondary brown rot (Monilinia fructicola) and flies",
            "Twig symptoms: small, oval, light brown to reddish-brown cankers with raised dark margins on 1-year-old green twigs",
            "Leaf symptoms: small, angular, yellowish-green to brown spots on leaf undersides that may drop out.",
        ],
        symptom_progression="Overwintered twig cankers produce conidia during spring rains -> conidia splash to developing green fruit from petal fall to 6 weeks post-bloom -> latent period of 40-70 days -> olive-green freckle spots appear as fruit nears maturity -> skin cracking.",
        favorable_conditions="Warm, rainy, humid weather (temperatures 20-27 deg C) during the 40-day post-bloom window; dense unpruned canopies with abundant 1-year-old twig cankers.",
        transmission_mode="Rain-splashed conidia from overwintered twig lesions; wind-blown rain.",
        primary_sources=["Overwintered twig cankers on 1-year-old peach shoots"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Prune out dead wood and older unproductive twigs during dormant pruning",
                "Apply protectant or systemic fungicide starting at shuck split and repeating at 10-14 day intervals for 4-6 weeks (critical fruit protection window)",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Canopy pruning and twig renewal",
                    timing="Dormant season",
                    purpose="Remove 1-year-old cankered twigs and open the canopy to sunlight and fast drying",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens",
                    target_stage="Shuck split to cover sprays",
                    application_method="Foliar spray applied at shuck split and cover sprays",
                    source=SOURCE_UGA.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Captan or Sulfur (Protectant)",
                    target_pathogen="Cladosporium carpophilum",
                    application_method="Foliar protective spray applied at shuck split, 1st cover, 2nd cover, and 3rd cover (at 10-14 day intervals)",
                    restrictions="Follow label rates and pre-harvest intervals; maintain continuous coverage during 40 days post-bloom",
                    source=SOURCE_PENN_STATE.name,
                ),
                ChemicalControl(
                    active_ingredient="Difenoconazole, Tebuconazole, or Pyraclostrobin + Boscalid",
                    target_pathogen="Cladosporium carpophilum",
                    application_method="Foliar spray applied at shuck split and cover sprays",
                    restrictions="Strict resistance management: rotate FRAC groups; adhere to label PHI",
                    source=SOURCE_UGA.name,
                ),
            ],
            organic_alternatives=[
                "Wettable sulfur or liquid lime sulfur sprays applied at 10-day intervals from shuck split for 40 days",
                "Bio-fungicides based on Bacillus species",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=["Prune out twig cankers and open up dense tree canopies"],
            cultural_preventions=[
                "Maintain an aggressive protective spray program from petal fall through 40 days post-bloom",
                "Avoid overhead irrigation",
            ],
            resistant_varieties="Most commercial peach and nectarine cultivars are susceptible; maintain preventative sprays",
            monitoring_schedule="Inspect 1-year-old twigs in winter for oval reddish cankers; inspect fruit from pit hardening through harvest",
        ),
        differential_diagnosis=[
            "Peach Bacterial Spot (Xanthomonas arboricola) - causes pitted, angular black spots on fruit and angular shot-holes on leaves (Peach scab causes superficial olive-green velvety freckles without leaf pitting)",
            "Peach Anthracnose - causes large sunken crater lesions with salmon-pink spores",
        ],
        severity_indicators="Abundant olive-green/black freckles coalescing into cracked corky crusts; secondary brown rot invasion.",
        treatment_limitations="Fungicide applications within 3-4 weeks of harvest are ineffective because scab infections occurred 40-70 days earlier during post-bloom.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_PENN_STATE, SOURCE_UGA, SOURCE_CORNELL, SOURCE_PURDUE],
    ),

    "plum__bacterial_spot": DiseaseRecord(
        disease_id="plum__bacterial_spot",
        canonical_name="Plum Bacterial Spot (Bacterial Shot-Hole / Canker)",
        crop_name="plum",
        pathogen_type=PathogenType.BACTERIAL,
        pathogen_name="Xanthomonas arboricola pv. pruni",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.TWIG],
        symptoms=[
            "Small, angular, water-soaked, dark brown to black spots on leaves, often concentrated along the midrib and leaf tips",
            "Lesions become dry, brittle, and drop out, creating a distinct 'shot-hole' perforation with a red/purple halo",
            "Heavily spotted leaves turn yellow and drop prematurely, causing severe summer defoliation",
            "Fruit symptoms: small, sunken, circular to irregular black spots that expand into deep pitted craters and cracks exuding amber gum",
            "Twig cankers: dark, water-soaked, sunken elliptical cankers on 1-to-2-year-old twigs that girdle shoot tips.",
        ],
        symptom_progression="Bacteria overwinter in twig cankers -> splash to unfolding leaves during warm spring rains -> angular shot-holes form in 7-14 days -> bacteria splash to developing fruit causing deep pitted craters and gumming -> severe summer defoliation.",
        favorable_conditions="Warm, humid, rainy, windy weather (temperatures 20-30 deg C), sandy soils, blown sand creating tissue micro-abrasions, and overhead sprinkler irrigation.",
        transmission_mode="Wind-blown rain; splashing water; contaminated pruning shears; movement of infected nursery trees.",
        primary_sources=["Overwintered spring and summer cankers on 1-year-old plum and peach twigs", "Infected budwood"],
        treatment_plan=ImmediateActionPlan := TreatmentPlan(
            immediate_actions=[
                "Prune out all cankered twigs and water sprouts during dormant winter pruning",
                "Apply fixed copper bactericide at late dormant stage and low-rate copper/oxytetracycline sprays from shuck split through cover sprays",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Canopy pruning and twig canker removal",
                    timing="Dormant season (late winter)",
                    purpose="Remove overwintered spring and summer cankers containing bacterial inoculum",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Windbreaks and ground cover",
                    timing="At orchard establishment",
                    purpose="Reduce wind-blown sand abrasions on foliage and fruit in sandy soils",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacteriophages specific to Xanthomonas arboricola / Bacillus amyloliquefaciens",
                    target_stage="Petal fall through cover sprays",
                    application_method="Foliar spray applied in late afternoon before predicted rain",
                    source=SOURCE_UF_IFAS.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Copper hydroxide or Copper oxychloride (Fixed copper)",
                    target_pathogen="Xanthomonas arboricola pv. pruni",
                    application_method="High-volume spray applied at late dormancy; low-rate copper applied from petal fall at 7-10 day intervals",
                    restrictions="CAUTION: Prunus foliage is highly sensitive to copper phytotoxicity; strictly adhere to low-rate label instructions",
                    source=SOURCE_PENN_STATE.name,
                ),
                ChemicalControl(
                    active_ingredient="Oxytetracycline (Mycoshield / FireLine)",
                    target_pathogen="Xanthomonas arboricola pv. pruni",
                    application_method="Foliar spray applied at shuck split and weekly cover sprays during rainy periods",
                    restrictions="Follow label rates and legal pre-harvest intervals (21-day PHI); adhere to antibiotic stewardship",
                    source=SOURCE_NC_STATE.name,
                ),
            ],
            organic_alternatives=[
                "Fixed copper bactericides applied at dormant and post-harvest stages",
                "Bio-bactericides based on Bacillus species applied preventatively",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=[
                "Use certified disease-free, tested nursery trees and rootstocks",
                "Sanitize pruning shears with 70% alcohol or 10% bleach between trees",
            ],
            cultural_preventions=[
                "Plant bacterial spot-resistant plum cultivars",
                "Maintain balanced tree nutrition; avoid excessive nitrogen that produces succulent vulnerable growth",
            ],
            resistant_varieties="Cultivars with documented field resistance to Xanthomonas arboricola (e.g., Stanley, Bluebyrd, Au-Cherry, Au-Rosa)",
            monitoring_schedule="Scout 1-year-old twigs for cankers in winter; inspect lower leaf tips weekly starting at petal fall",
        ),
        differential_diagnosis=[
            "Plum Pocket Disease (Taphrina communis) - produces large, hollow, spongy bladder-like fruit rather than sunken crater pits and shot-hole leaves",
            "Cherry Leaf Spot - produces circular purple spots that yellow without deep pitted fruit craters or amber gumming",
        ],
        severity_indicators="Deep pitted gumming craters on fruit; extensive shot-hole defoliation >40%; girdling spring twig cankers.",
        treatment_limitations="Bactericides cannot cure deep fruit craters or internal vascular twig cankers; preventative sprays and resistant varieties are required.",
        quality_level="HIGH",
        treatment_category="management",
        sources=[SOURCE_PENN_STATE, SOURCE_NC_STATE, SOURCE_UF_IFAS, SOURCE_CORNELL],
    ),

    "plum__brown_rot": DiseaseRecord(
        disease_id="plum__brown_rot",
        canonical_name="Plum Brown Rot",
        crop_name="plum",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Monilinia fructicola / Monilinia laxa",
        affected_parts=[PlantPart.FLOWER, PlantPart.FRUIT, PlantPart.TWIG],
        symptoms=[
            "Blossom blight: open plum blossoms turn brown, wilt, wither, and remain glued to twigs by sticky amber gum",
            "Twig cankers: small elliptical cankers girdling green twigs beneath blighted blossoms, exuding clear to amber gum",
            "Fruit rot: rapidly expanding, soft, circular, brown water-soaked rot on ripening plums",
            "Dense, powdery, tan to grayish-brown spore tufts (monilioid conidia) erupting across the rotting fruit surface",
            "Infected fruit rots completely within 48-72 hours, shriveling into hard, wrinkled, dark brown/black mummies that cling to branches over winter.",
        ],
        symptom_progression="Airborne conidia/ascospores infect blossoms in spring -> blossom blight and twig cankers form -> conidia infect ripening fruit through wounds or direct contact -> fruit rots rapidly into gray-brown mold -> mummified plums overwinter on tree.",
        favorable_conditions="Warm, humid, rainy weather (temperatures 20-27 deg C), frequent rainfall, morning dew, insect feeding wounds (curculio), and touching fruit clusters.",
        transmission_mode="Wind-dispersed airborne conidia; rain splash from mummies and twig cankers; insect vectors (fruit flies, beetles); handling.",
        primary_sources=["Overwintered mummified plums hanging on trees or on the orchard floor", "Overwintered twig cankers"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Remove and destroy all hanging and fallen mummified plums during dormant pruning",
                "Prune out all blighted twigs and gumming cankers",
                "Apply protectant or systemic fungicide at pink bud / full bloom for blossom blight, and at 3 weeks, 2 weeks, and 1 day pre-harvest for fruit rot",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Mummy removal and canopy sanitation",
                    timing="Dormant season (winter)",
                    purpose="Eliminate the primary overwintering source of Monilinia fructicola conidia and ascospores",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Fruit thinning",
                    timing="Early summer",
                    purpose="Thin plums to prevent touching fruit clusters that foster rapid rot spread",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens / Aureobasidium pullulans",
                    target_stage="Bloom and pre-harvest window",
                    application_method="Foliar spray applied at 50% bloom and 7 days pre-harvest",
                    source=SOURCE_CORNELL.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Propiconazole, Tebuconazole, or Difenoconazole (DMI / Triazoles)",
                    target_pathogen="Monilinia fructicola",
                    application_method="Foliar spray applied at popcorn, full bloom, and during the 3-week pre-harvest ripening window",
                    restrictions="Follow label rates and legal pre-harvest intervals; rotate with different FRAC groups to prevent resistance",
                    source=SOURCE_PENN_STATE.name,
                ),
                ChemicalControl(
                    active_ingredient="Fluopyram + Trifloxystrobin or Cyprodinil + Fludioxonil",
                    target_pathogen="Monilinia fructicola",
                    application_method="Foliar spray applied during pre-harvest cover sprays",
                    restrictions="Strict resistance management: maximum 2 applications per season; adhere to label PHI",
                    source=SOURCE_PENN_STATE.name,
                ),
            ],
            organic_alternatives=[
                "Wettable sulfur or liquid lime sulfur applied at bloom and pre-harvest",
                "Aggressive mummy removal and fruit thinning",
                "Bio-fungicides based on Bacillus species",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=[
                "Remove 100% of mummified fruit from trees and ground during winter pruning",
                "Sanitize harvesting lugs and sorting equipment daily during harvest",
            ],
            cultural_preventions=[
                "Thin fruit clusters to eliminate touching fruit surfaces",
                "Manage plum curculio to prevent insect entry wounds",
            ],
            resistant_varieties="Most commercial plum cultivars are susceptible; maintain preventative sprays during bloom and pre-harvest ripening",
            monitoring_schedule="Scout blossoms at 20-80% bloom; inspect ripening fruit weekly starting 3-4 weeks before harvest",
        ),
        differential_diagnosis=[
            "Plum Pocket Disease (Taphrina communis) - causes young green fruit to swell into hollow, spongy, bladder-like pods without powdery tan spore tufts",
            "Plum Bacterial Spot - causes deep sunken pitted craters with amber gumming rather than soft brown rot covered in powdery tan tufts",
        ],
        severity_indicators="Tan/gray powdery spore tufts covering ripening fruit; blossom blight with gumming cankers; mummified fruit clusters.",
        treatment_limitations="Fungicides cannot cure already rotting fruit; sprays during bloom and the 3-week pre-harvest ripening window are mandatory.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_PENN_STATE, SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_USDA_ARS],
    ),

    "plum__pocket_disease": DiseaseRecord(
        disease_id="plum__pocket_disease",
        canonical_name="Plum Pocket Disease (Bladder Plums / False Plums)",
        crop_name="plum",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Taphrina communis (syn. Taphrina pruni)",
        affected_parts=[PlantPart.FRUIT, PlantPart.LEAF, PlantPart.TWIG],
        symptoms=[
            "Young developing green plum fruits enlarge abnormally rapidly, swelling to 10-20 times their normal size within weeks",
            "Infected plums become hollow, spongy, bladder-like, elongated, and distorted pods ('pockets / bladders')",
            "The stone / pit fails to develop inside the hollow spongy fruit",
            "Fruit surface turns pale yellow, then becomes covered in a powdery, grayish-white velvety bloom of fungal asci",
            "Infected fruit eventually turns dark brown, withers, and falls prematurely or remains mummified on branches",
            "Young leaves and shoot tips may become swollen, curled, and distorted.",
        ],
        symptom_progression="Overwintered blastospores on bark/twigs infect flower ovaries during bud break/bloom -> fruit swells into hollow spongy bladders -> powdery gray asci cover fruit surface -> fruit turns brown, withers, and drops.",
        favorable_conditions="Cool, wet, rainy spring weather (temperatures 10-18 deg C) coinciding with bud swell through bloom, and prolonged rain or heavy fog (>12-24 hours).",
        transmission_mode="Rain-splashed blastospores from bark crevices and bud scales onto newly expanding flowers; NOT airborne over long distances.",
        primary_sources=["Overwintered blastospores surviving in bark crevices and under bud scales on the tree itself"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "CRITICAL TIMING: Apply a single thorough dormant fungicide spray in late autumn after leaf fall OR in late winter before bud swell (January/February)",
                "Spraying AFTER buds have opened or after fruit has started swelling into bladders is 100% INEFFECTIVE",
                "Hand-pick and destroy developing hollow bladder plums immediately to reduce ascospore production",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Dormant spray timing",
                    timing="After 90% leaf fall in autumn OR before bud swell in late winter",
                    purpose="Eradicate overwintered Taphrina blastospores on bark before they can penetrate expanding flower buds",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Hand-picking swollen bladder plums",
                    timing="Late spring when pockets are green/yellow",
                    purpose="Remove and bury swollen bladder fruits before gray spore layer matures",
                    effectiveness="Medium",
                ),
            ],
            biological_controls=[],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Copper hydroxide, Copper oxychloride, or Bordeaux mixture (Fixed copper)",
                    target_pathogen="Taphrina communis",
                    application_method="High-volume dormant wash applied to the entire tree trunk and branches until run-off",
                    restrictions="Apply strictly during dormancy before green tissue emerges to prevent phytotoxicity; follow label rates",
                    source=SOURCE_CORNELL.name,
                ),
                ChemicalControl(
                    active_ingredient="Chlorothalonil or Liquid lime sulfur",
                    target_pathogen="Taphrina communis",
                    application_method="Dormant spray applied in late winter before bud swell",
                    restrictions="Follow product label safety directions; do not apply chlorothalonil after bloom",
                    source=SOURCE_PENN_STATE.name,
                ),
            ],
            organic_alternatives=[
                "Dormant application of liquid lime sulfur or fixed copper fungicides",
                "Hand-picking and destruction of immature bladder plums",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=["Ensure thorough dormant spray coverage reaching all bark crevices and bud scales"],
            cultural_preventions=[
                "Schedule dormant spray annually without skipping seasons",
                "Plant plum cultivars with lower susceptibility to Taphrina pocket disease",
            ],
            resistant_varieties="European plum cultivars (Prunus domestica) generally show higher tolerance than American wild plum and Japanese hybrids",
            monitoring_schedule="Inspect expanding flower buds in spring; check young green plums 2-3 weeks post-bloom for abnormal swelling",
        ),
        differential_diagnosis=[
            "Plum Brown Rot (Monilinia fructicola) - produces soft brown rot covered in tan/gray powdery spore tufts on normal-sized fruit containing hard pits (Plum pocket produces giant hollow spongy fruit without pits)",
            "Plum Curculio damage - causes crescent-shaped scars on normal-sized fruit containing insect larvae",
        ],
        severity_indicators="Abnormally enlarged hollow spongy bladder plums; powdery gray-white ascospore layer; fruit lacking internal stones.",
        treatment_limitations="Fungicide sprays applied after fruit has set are 100% ineffective; dormant timing is mandatory.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_CORNELL, SOURCE_PENN_STATE, SOURCE_PURDUE, SOURCE_USDA_ARS],
    ),

    "plum__pox_virus": DiseaseRecord(
        disease_id="plum__pox_virus",
        canonical_name="Plum Pox Virus (Sharka)",
        crop_name="plum",
        pathogen_type=PathogenType.VIRAL,
        pathogen_name="Plum Pox Virus (PPV) - Potyvirus",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.SEED, PlantPart.WHOLE_PLANT],
        symptoms=[
            "Leaf symptoms: chlorotic yellow rings, blotches, bands, and pale green halos scattered across leaves in late spring",
            "Fruit symptoms: distinct chlorotic to necrotic rings, sunken crescent-shaped bands, pits, and grooved deformities on plum fruit skin",
            "Infected fruit flesh beneath rings becomes brown, gummy, and acidic, rendering fruit unmarketable",
            "Seed / stone symptoms: distinct dark brownish-red to pale yellow ring patterns on the surface of the fruit stone / pit",
            "Severe premature fruit drop (up to 80-100% of fruit drops before ripening).",
        ],
        symptom_progression="Aphid vector or infected budwood introduces PPV -> systemic replication -> spring leaves show chlorotic rings -> fruit develops sunken grooved rings and gumming -> severe premature fruit drop -> tree becomes permanently debilitated.",
        favorable_conditions="High aphid vector activity (Brachycaudus helichrysi, Myzus persicae), warm spring weather, unregulated movement of infected Prunus nursery stock or budwood.",
        transmission_mode="Non-persistently transmitted within seconds by numerous aphid species; vegetative propagation (budding, grafting, infected rootstocks); NOT seed-transmitted.",
        primary_sources=["Infected Prunus trees (plum, peach, apricot, cherry) in surrounding orchards or wild prunus thickets", "Infected nursery stock"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "STRICT REGULATORY ACTION: Plum Pox is a regulated quarantine pathogen in many agricultural jurisdictions",
                "DO NOT spray fungicides or bactericides - VIRUSES CANNOT BE CURED WITH CHEMICAL SPRAYS",
                "Confirm diagnosis via official ELISA or RT-PCR testing; upon confirmation, immediately eradicate (uproot and burn) the infected tree",
                "Apply systemic aphicide to surrounding trees to suppress aphid vector dispersal",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Quarantine enforcement and eradication",
                    timing="Immediate upon confirmation",
                    purpose="Rogue and destroy infected trees to prevent aphids from vectoring PPV to healthy orchard blocks",
                    effectiveness="High",
                ),
                CulturalControl(
                    practice="Certified virus-tested nursery stock use",
                    timing="At planting",
                    purpose="Plant exclusively certified virus-free trees tested and certified under official quarantine certification programs",
                    effectiveness="High",
                ),
            ],
            biological_controls=[],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Horticultural mineral oil (1%)",
                    target_pathogen="Aphid stylet PPV transmission",
                    application_method="Foliar spray applied during spring aphid flights to reduce transmission efficiency",
                    restrictions="Follow label rates; apply in early morning or evening to prevent phytotoxicity",
                    source=SOURCE_EPPO.name,
                ),
            ],
            organic_alternatives=[
                "Planting genetically resistant or transgenic PPV-immune cultivars (e.g., HoneySweet plum containing the RNAi-based PPV resistance trait in approved regions)",
                "Immediate eradication and burning of infected trees",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=[
                "Strict adherence to plant quarantine regulations; never import uncertified Prunus budwood or nursery stock",
                "Eradicate wild Prunus thickets (wild plum, chokecherry) around commercial orchard borders",
            ],
            cultural_preventions=[
                "Plant certified virus-tested trees from accredited nurseries",
                "Plant resistant cultivars (e.g., HoneySweet possesses high RNAi-mediated resistance to PPV)",
            ],
            resistant_varieties="HoneySweet (transgenic plum with near-complete PPV resistance), Jojo (hypersensitive resistant European plum)",
            monitoring_schedule="Scout leaves in late spring (May-June) for chlorotic rings; inspect fruit 2-4 weeks before harvest for sunken ring grooves",
        ),
        differential_diagnosis=[
            "Plum Bacterial Spot - causes deep angular pitted craters with amber gumming without distinct concentric chlorotic rings on fruit stones",
            "Apple Mosaic Virus in stone fruit - causes creamy-white vein banding without sunken grooved fruit rings or stone ring patterns",
        ],
        severity_indicators="Distinct chlorotic/necrotic rings on fruit skin and stones; severe premature fruit drop (>50%); confirmed positive ELISA/PCR test.",
        treatment_limitations="NO chemical spray can cure a PPV-infected tree; tree eradication and quarantine are mandatory.",
        quality_level="HIGH",
        treatment_category="removal/destruction",
        sources=[SOURCE_EPPO, SOURCE_USDA_ARS, SOURCE_PENN_STATE, SOURCE_CABI],
    ),

    "plum__rust": DiseaseRecord(
        disease_id="plum__rust",
        canonical_name="Plum Rust (Prunus Rust)",
        crop_name="plum",
        pathogen_type=PathogenType.FUNGAL,
        pathogen_name="Tranzschelia pruni-spinosae / Tranzschelia discolor",
        affected_parts=[PlantPart.LEAF, PlantPart.FRUIT, PlantPart.TWIG],
        symptoms=[
            "Small, pale yellow, angular chlorotic spots on upper leaf surfaces in mid-to-late summer",
            "Lower leaf surface directly beneath spots develops powdery, dusty, chocolate-brown to cinnamon-brown pustules (uredinia)",
            "Severe infection causes leaves to turn yellow and drop prematurely (autumn defoliation), weakening flower buds for the next season",
            "Fruit symptoms: small, circular, sunken green spots on ripening fruit with brown spore pustules",
            "Twig cankers: small blister-like longitudinal splits on young green twigs.",
        ],
        symptom_progression="Airborne urediniospores land on leaves in spring/summer -> yellow spots appear on upper surface -> dusty chocolate-brown pustules erupt on underside in 10-14 days -> defoliation accelerates in late summer -> teliospores overwinter on twigs.",
        favorable_conditions="Warm temperatures (20-28 deg C), high relative humidity, frequent summer rain showers, morning fog, or heavy dew; dense unpruned canopies.",
        transmission_mode="Wind-dispersed airborne urediniospores; rain splash from overwintered twig cankers; alternate hosts (Anemone spp.).",
        primary_sources=["Overwintered twig cankers on plum branches", "Alternate ranunculaceous weed hosts (Anemone spp.)"],
        treatment_plan=TreatmentPlan(
            immediate_actions=[
                "Apply protectant or systemic fungicide if rust pustules appear on lower foliage in mid-summer",
                "Ensure spray coverage reaches the lower surface of leaves across the entire canopy",
            ],
            cultural_controls=[
                CulturalControl(
                    practice="Canopy pruning and aeration",
                    timing="Dormant season and summer pruning",
                    purpose="Improve air circulation and sunlight penetration to shorten leaf wetness periods",
                    effectiveness="High",
                ),
            ],
            biological_controls=[
                BiologicalControl(
                    agent="Bacillus subtilis / Bacillus amyloliquefaciens",
                    target_stage="Summer foliar spray",
                    application_method="Foliar spray applied at early symptom detection",
                    source=SOURCE_CORNELL.name,
                )
            ],
            chemical_controls=[
                ChemicalControl(
                    active_ingredient="Sulfur / Wettable sulfur (Protectant)",
                    target_pathogen="Tranzschelia pruni-spinosae",
                    application_method="Foliar spray applied at 10-14 day intervals starting in mid-summer",
                    restrictions="Avoid spraying sulfur when temperatures exceed 30 deg C; follow label rates",
                    source=SOURCE_PENN_STATE.name,
                ),
                ChemicalControl(
                    active_ingredient="Myclobutanil, Tebuconazole, or Difenoconazole (DMI / Triazoles)",
                    target_pathogen="Tranzschelia pruni-spinosae",
                    application_method="Foliar spray applied at first appearance of yellow leaf spotting",
                    restrictions="Rotate FRAC groups to prevent resistance; adhere to legal pre-harvest intervals",
                    source=SOURCE_CORNELL.name,
                ),
            ],
            organic_alternatives=[
                "Wettable sulfur or potassium bicarbonate foliar sprays during cool periods",
                "Fixed copper fungicides applied at post-harvest stage",
            ],
        ),
        prevention_protocol=PreventionProtocol(
            sanitation_measures=["Prune out twig cankers during dormant pruning"],
            cultural_preventions=[
                "Avoid overhead irrigation; use under-tree drip or micro-sprinklers",
                "Maintain open tree canopies to accelerate leaf drying",
            ],
            resistant_varieties="Most commercial plum cultivars are susceptible; maintain preventative sprays in humid climates",
            monitoring_schedule="Scout lower leaf undersides bi-weekly from mid-summer (July) through autumn leaf drop",
        ),
        differential_diagnosis=[
            "Plum Bacterial Spot (Xanthomonas arboricola) - produces angular purple/brown spots that drop out creating shot-holes without powdery chocolate-brown spores on the underside",
            "Plum Pocket Disease - produces giant hollow spongy fruit bladders without powdery leaf rust pustules",
        ],
        severity_indicators="Chocolate-brown powdery pustules covering >30% of leaf undersides; premature autumn defoliation before natural dormancy.",
        treatment_limitations="Fungicides cannot re-green yellowed leaves; post-harvest sprays are critical to prevent early defoliation and flower bud death.",
        quality_level="HIGH",
        treatment_category="curative treatment",
        sources=[SOURCE_PENN_STATE, SOURCE_CORNELL, SOURCE_PURDUE, SOURCE_USDA_ARS],
    ),
}
"""

print("Fruit records defined successfully.")
