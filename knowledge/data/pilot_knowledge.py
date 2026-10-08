"""
Pilot Agricultural Knowledge Base
=================================
Verified disease profiles and crop agronomy records with complete provenance.
Covers fungal, bacterial, and oomycete pathologies across multiple crop families.
"""

from __future__ import annotations

from knowledge.schema import (
    CropRecord,
    DiseaseRecord,
    ManagementStrategies,
    SourcedFact,
)

# ---------------------------------------------------------------------------
# 1. Pilot Disease Profiles
# ---------------------------------------------------------------------------

PILOT_DISEASES: dict[str, DiseaseRecord] = {
    "tomato__early_blight": DiseaseRecord(
        disease_slug="tomato__early_blight",
        common_name="Early Blight",
        crop="tomato",
        scientific_name_causal_agent="Alternaria solani",
        disease_type="Fungal",
        affected_parts=["leaf", "stem", "fruit"],
        symptoms=[
            SourcedFact(
                statement="Lower, older leaves develop brown to dark brown circular or angular spots.",
                source_ids=["SRC_UC_IPM", "SRC_CORNELL_EXT"],
                detail="Spots often start at the base of the plant and progress upwards as the foliage matures."
            ),
            SourcedFact(
                statement="Lesions typically expand and form distinctive concentric rings giving a 'target board' or 'bullseye' appearance.",
                source_ids=["SRC_CORNELL_EXT", "SRC_PURDUE_EXT"],
            ),
            SourcedFact(
                statement="Tissue surrounding the target-like spots frequently turns yellow (chlorosis), leading to premature leaf drop and sunscald on exposed fruit.",
                source_ids=["SRC_UC_IPM", "SRC_PURDUE_EXT"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Concentric target-like rings within dark brown spots and initial localization on the oldest bottom leaves.",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="The fungus Alternaria solani survives in infected crop debris, soil, and solanaceous weeds.",
                source_ids=["SRC_USDA_ARS", "SRC_UC_IPM"],
            ),
            SourcedFact(
                statement="Disease development is favored by warm temperatures (24°C to 29°C / 75°F to 85°F) combined with frequent rain, heavy dew, or overhead irrigation.",
                source_ids=["SRC_CORNELL_EXT", "SRC_UC_IPM"],
            ),
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Spores (conidia) are spread by wind, splashing rain, overhead irrigation, tools, and workers moving through wet fields.",
                source_ids=["SRC_PURDUE_EXT"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Overwinters in infested solanaceous crop residues, volunteer tomato plants, and nightshade weeds for at least one year.",
                source_ids=["SRC_USDA_ARS"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Practice a 2- to 3-year crop rotation with non-solanaceous crops (avoid rotating with potato, eggplant, or pepper).",
                    source_ids=["SRC_CORNELL_EXT", "SRC_UC_IPM"],
                ),
                SourcedFact(
                    statement="Apply organic or plastic mulch around the base of plants to create a physical barrier preventing soil-borne spores from splashing onto lower leaves.",
                    source_ids=["SRC_PURDUE_EXT"],
                ),
                SourcedFact(
                    statement="Stake and prune lower foliage to improve airflow and facilitate faster canopy drying.",
                    source_ids=["SRC_UC_IPM"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Remove and destroy heavily infected lower leaves during the growing season, and thoroughly clear or deep-plow crop residues after harvest.",
                    source_ids=["SRC_CORNELL_EXT", "SRC_USDA_ARS"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Use drip irrigation or soaker hoses instead of overhead sprinklers, and irrigate early in the morning so foliage dries quickly.",
                    source_ids=["SRC_PURDUE_EXT", "SRC_UC_IPM"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Biofungicide applications containing Bacillus subtilis or Trichoderma harzianum can help suppress early spore germination when applied preventively.",
                    source_ids=["SRC_FAO_PLANT"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Preventive protectant fungicides (such as copper-based formulations or chlorothalonil) may be applied early before infection becomes widespread, following local extension guidelines and label directions.",
                    source_ids=["SRC_CORNELL_EXT", "SRC_UC_IPM"],
                    detail="Ensure thorough coverage of both upper and lower leaf surfaces."
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Combine resistant tomato cultivars, drip watering, strict 3-year rotation, baseline mulching, and targeted protectant sprays during prolonged wet weather.",
                    source_ids=["SRC_FAO_PLANT", "SRC_CORNELL_EXT"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Plant certified disease-free seed and resistant or tolerant tomato varieties.",
                source_ids=["SRC_CORNELL_EXT"],
            ),
            SourcedFact(
                statement="Maintain wide plant spacing (18–24 inches apart) to maximize sunlight penetration and air circulation.",
                source_ids=["SRC_PURDUE_EXT"],
            ),
        ],
        sources=["SRC_UC_IPM", "SRC_CORNELL_EXT", "SRC_PURDUE_EXT", "SRC_USDA_ARS", "SRC_FAO_PLANT"],
    ),

    "tomato__septoria_leaf_spot": DiseaseRecord(
        disease_slug="tomato__septoria_leaf_spot",
        common_name="Septoria Leaf Spot",
        crop="tomato",
        scientific_name_causal_agent="Septoria lycopersici",
        disease_type="Fungal",
        affected_parts=["leaf", "stem", "calyx"],
        symptoms=[
            SourcedFact(
                statement="Numerous small, circular spots (1.5–3 mm) appear first on the lowest leaves after fruit set.",
                source_ids=["SRC_PURDUE_EXT", "SRC_CORNELL_EXT"],
            ),
            SourcedFact(
                statement="Mature spots develop distinctive dark brown margins with grayish-white or tan centers containing tiny black specks (pycnidia).",
                source_ids=["SRC_PURDUE_EXT"],
            ),
            SourcedFact(
                statement="Severely infected leaves turn yellow, wither, and drop, resulting in extensive progressive defoliation from the base upward.",
                source_ids=["SRC_CORNELL_EXT"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Small circular spots with grayish-white centers and tiny black fruiting bodies (pycnidia), distinct from the large target-like rings of Early Blight.",
                source_ids=["SRC_PURDUE_EXT"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="Septoria lycopersici thrives during prolonged wet, humid weather with temperatures between 20°C and 25°C (68°F to 77°F).",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Spores are extruded in gelatinous tendrils during rainy periods and splashed by raindrops, wind-driven mist, tools, and hands.",
                source_ids=["SRC_PURDUE_EXT"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Survives on infected solanaceous crop residues, horsenettle, and jimsonweed.",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Rotate away from Solanaceous crops for at least 2 to 3 years.",
                    source_ids=["SRC_PURDUE_EXT"],
                ),
                SourcedFact(
                    statement="Mulch plants at transplanting to prevent soil splash and stake plants to maintain vertical airflow.",
                    source_ids=["SRC_CORNELL_EXT"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Pinch off and dispose of lower spotted leaves early in the season; never work in the garden when foliage is wet.",
                    source_ids=["SRC_PURDUE_EXT"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Use drip irrigation and eliminate overhead watering to keep leaf surfaces dry.",
                    source_ids=["SRC_CORNELL_EXT"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Preventive biological soil and foliar treatments containing Bacillus amyloliquefaciens can reduce early disease establishment.",
                    source_ids=["SRC_FAO_PLANT"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Protectant fungicides like copper hydroxide or chlorothalonil should be applied preventively at the first appearance of lower leaf spots.",
                    source_ids=["SRC_CORNELL_EXT", "SRC_PURDUE_EXT"],
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Combine bottom leaf pruning, strict drip watering, straw or plastic mulch, weed elimination, and early copper protectants.",
                    source_ids=["SRC_CORNELL_EXT"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Use clean, certified seeds and inspect transplants for any signs of small foliar spots before field planting.",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        sources=["SRC_PURDUE_EXT", "SRC_CORNELL_EXT", "SRC_FAO_PLANT"],
    ),

    "cucumber__downy_mildew": DiseaseRecord(
        disease_slug="cucumber__downy_mildew",
        common_name="Downy Mildew",
        crop="cucumber",
        scientific_name_causal_agent="Pseudoperonospora cubensis",
        disease_type="Oomycete",
        affected_parts=["leaf"],
        symptoms=[
            SourcedFact(
                statement="Angular, bright yellow to pale green spots appear on the upper surface of leaves, strictly bounded by leaf veins.",
                source_ids=["SRC_NCSTATE_EXT", "SRC_CORNELL_EXT"],
            ),
            SourcedFact(
                statement="A purplish-gray to dark brown velvety down (sporangiophores and sporangia) develops on the corresponding underside of the leaf during high humidity.",
                source_ids=["SRC_NCSTATE_EXT"],
            ),
            SourcedFact(
                statement="Infected leaves rapidly turn brown, curl upward, and scorch as if damaged by frost.",
                source_ids=["SRC_CORNELL_EXT"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Angular yellow patches strictly delimited by leaf veins with purplish-gray down on the leaf underside.",
                source_ids=["SRC_NCSTATE_EXT"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="Pseudoperonospora cubensis is an obligate biotrophic oomycete that requires living host tissue and spreads rapidly under cool to warm humid conditions (15°C–22°C / 60°F–72°F) with 6+ hours of leaf wetness.",
                source_ids=["SRC_NCSTATE_EXT", "SRC_USDA_ARS"],
            )
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Airborne sporangia travel long distances on air currents and wind storms over hundreds of miles.",
                source_ids=["SRC_NCSTATE_EXT"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Does not survive winter freezing outdoors in northern climates; overwinters in southern greenhouses or regions without frost.",
                source_ids=["SRC_NCSTATE_EXT"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Plant downy mildew-resistant or tolerant hybrid cucumber varieties.",
                    source_ids=["SRC_NCSTATE_EXT", "SRC_CORNELL_EXT"],
                ),
                SourcedFact(
                    statement="Trellis vines to elevate foliage above soil level and improve air circulation.",
                    source_ids=["SRC_CORNELL_EXT"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Destroy heavily blighted vines immediately after harvest to stop airborne spore production.",
                    source_ids=["SRC_NCSTATE_EXT"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Ensure wide row spacing and orient rows parallel to prevailing winds to hasten dew evaporation.",
                    source_ids=["SRC_CORNELL_EXT"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Biofungicides like Bacillus subtilis and copper octanoate can provide suppression under mild pressure.",
                    source_ids=["SRC_FAO_PLANT"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Targeted oomycete-specific fungicides (such as cyazofamid, fluopicolide, or propamocarb) tank-mixed with protectants like mancozeb or chlorothalonil should be applied when spore alerts are active.",
                    source_ids=["SRC_NCSTATE_EXT"],
                    detail="Rotate fungicide modes of action (FRAC groups) to prevent resistance."
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Rely on resistant cultivars, trellising, regional spore forecast alerts, and preventive targeted sprays before symptoms expand.",
                    source_ids=["SRC_NCSTATE_EXT", "SRC_CORNELL_EXT"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Plant early in the season to mature the crop before peak regional airborne spore influx.",
                source_ids=["SRC_NCSTATE_EXT"],
            )
        ],
        sources=["SRC_NCSTATE_EXT", "SRC_CORNELL_EXT", "SRC_USDA_ARS", "SRC_FAO_PLANT"],
    ),

    "squash__powdery_mildew": DiseaseRecord(
        disease_slug="squash__powdery_mildew",
        common_name="Powdery Mildew",
        crop="squash",
        scientific_name_causal_agent="Podosphaera xanthii",
        disease_type="Fungal",
        affected_parts=["leaf", "petiole", "stem"],
        symptoms=[
            SourcedFact(
                statement="White, powdery fungal spots and talcum-like patches develop on upper and lower surfaces of leaves and petioles.",
                source_ids=["SRC_UC_IPM", "SRC_PENNSTATE_EXT"],
            ),
            SourcedFact(
                statement="As infection spreads, leaves turn yellow, become dull brown and brittle, and dry out prematurely.",
                source_ids=["SRC_PENNSTATE_EXT"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Superficial white powdery fungal growth that can be wiped off with a finger, unlike downy mildew which forms inside leaf veins.",
                source_ids=["SRC_UC_IPM"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="Podosphaera xanthii thrives in warm, dry weather (20°C–27°C / 68°F–80°F) with high relative humidity and dense, shaded canopies; free water is not required for spore germination.",
                source_ids=["SRC_UC_IPM", "SRC_CORNELL_EXT"],
            )
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Conidiospores are blown readily by wind across fields.",
                source_ids=["SRC_PENNSTATE_EXT"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Overwinters on greenhouse cucurbits, weed hosts, and as chasmothecia in crop residue.",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Select powdery mildew-resistant squash varieties (designated PMR).",
                    source_ids=["SRC_CORNELL_EXT", "SRC_UC_IPM"],
                ),
                SourcedFact(
                    statement="Plant in full sun and space plants adequately to minimize dense shading within the canopy.",
                    source_ids=["SRC_PENNSTATE_EXT"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Remove and dispose of early infected leaves if the problem is localized to a few leaves.",
                    source_ids=["SRC_UC_IPM"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Avoid excessive nitrogen fertilization, which generates dense succulent foliage susceptible to mildew.",
                    source_ids=["SRC_PENNSTATE_EXT"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Potassium bicarbonate, horticultural oils, and neem oil sprays provide effective organic suppression by disrupting fungal cell membranes.",
                    source_ids=["SRC_UC_IPM", "SRC_FAO_PLANT"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Sulfur-based fungicides or systemic fungicides (e.g. FRAC 3, 7, 11) should be applied preventively or at the very first sign of white spots.",
                    source_ids=["SRC_PENNSTATE_EXT", "SRC_UC_IPM"],
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Utilize PMR seed varieties, avoid over-fertilization, maximize sun exposure, and apply horticultural oils or sulfur at first spot appearance.",
                    source_ids=["SRC_UC_IPM", "SRC_CORNELL_EXT"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Choose resistant cultivars and rotate planting blocks annually.",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        sources=["SRC_UC_IPM", "SRC_PENNSTATE_EXT", "SRC_CORNELL_EXT", "SRC_FAO_PLANT"],
    ),

    "soybean__rust": DiseaseRecord(
        disease_slug="soybean__rust",
        common_name="Soybean Rust",
        crop="soybean",
        scientific_name_causal_agent="Phakopsora pachyrhizi",
        disease_type="Fungal",
        affected_parts=["leaf", "petiole", "stem", "pod"],
        symptoms=[
            SourcedFact(
                statement="Small, pinpoint chlorotic or tan-to-reddish-brown spots on the lower leaf surface, especially within the lower-to-middle canopy.",
                source_ids=["SRC_USDA_ARS", "SRC_IOWA_STATE_EXT"],
            ),
            SourcedFact(
                statement="Volcano-like pustules (uredinia) develop on the undersides of leaves, releasing powdery masses of tan-to-golden spores.",
                source_ids=["SRC_IOWA_STATE_EXT"],
            ),
            SourcedFact(
                statement="Rapid canopy yellowing and severe premature defoliation occur under favorable weather, causing severe pod abortion and yield reduction.",
                source_ids=["SRC_USDA_ARS"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Raised, cone-shaped pustules on the lower leaf surface with small central pores releasing tan spores (requires a 10x-20x hand lens).",
                source_ids=["SRC_IOWA_STATE_EXT"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="Phakopsora pachyrhizi requires prolonged leaf wetness (6–12 hours) and moderate temperatures (15°C–28°C / 59°F–82°F) for spore germination.",
                source_ids=["SRC_USDA_ARS", "SRC_IOWA_STATE_EXT"],
            )
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Spores are light and transported hundreds of miles by prevailing wind currents during storm systems.",
                source_ids=["SRC_USDA_ARS"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Overwinters on living legume hosts such as kudzu (*Pueraria montana*) in frost-free regions.",
                source_ids=["SRC_USDA_ARS", "SRC_IOWA_STATE_EXT"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Plant early-maturing soybean cultivars to set and fill pods before peak regional rust spore showers arrive.",
                    source_ids=["SRC_IOWA_STATE_EXT"],
                ),
                SourcedFact(
                    statement="Monitor regional sentinel plots and spore trapping networks (e.g. USDA-IPM PIPE) for early detection alerts.",
                    source_ids=["SRC_USDA_ARS"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Eradicate alternate wild hosts like kudzu around field borders where feasible.",
                    source_ids=["SRC_USDA_ARS"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Avoid dense planting populations that trap high humidity inside the inner crop canopy.",
                    source_ids=["SRC_IOWA_STATE_EXT"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Biological control agents currently offer limited field control under high disease pressure; monitoring is essential.",
                    source_ids=["SRC_FAO_PLANT"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Fungicides containing strobilurins (QoI), triazoles (DMI), or SDHI premixes must be applied preventively or at the R1 to R3 reproductive stage upon confirmation in nearby counties.",
                    source_ids=["SRC_IOWA_STATE_EXT", "SRC_USDA_ARS"],
                    detail="Curative fungicide action is ineffective once defoliation exceeds 10-15%."
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Rely on early planting dates, regional spore alert monitoring, and timely preventive triazole/strobilurin fungicide application at flowering/pod-fill.",
                    source_ids=["SRC_USDA_ARS", "SRC_IOWA_STATE_EXT"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Utilize tolerant soybean varieties with Rpp resistance genes when available and monitor regional sentinel alert maps.",
                source_ids=["SRC_USDA_ARS"],
            )
        ],
        sources=["SRC_USDA_ARS", "SRC_IOWA_STATE_EXT", "SRC_FAO_PLANT"],
    ),

    "banana__cordana_leaf_spot": DiseaseRecord(
        disease_slug="banana__cordana_leaf_spot",
        common_name="Cordana Leaf Spot",
        crop="banana",
        scientific_name_causal_agent="Neocordana musae (syn. Cordana musae)",
        disease_type="Fungal",
        affected_parts=["leaf"],
        symptoms=[
            SourcedFact(
                statement="Large, oval to diamond-shaped lesions (several centimeters long) appear on the leaf lamina, often originating along leaf margins.",
                source_ids=["SRC_FAO_PLANT", "SRC_UF_IFAS"],
            ),
            SourcedFact(
                statement="Lesions have pale brown to grayish necrotic centers surrounded by a bright, distinct yellow halo and concentric growth bands.",
                source_ids=["SRC_UF_IFAS"],
            ),
            SourcedFact(
                statement="Under humid conditions, a grayish-brown powdery fungal sporulation is visible on the underside of spots.",
                source_ids=["SRC_FAO_PLANT"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Broad, oval or diamond-shaped lesions with zigzag concentric zones and bright yellow chlorotic halos, typically along leaf edges.",
                source_ids=["SRC_UF_IFAS"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="Neocordana musae is a weak parasite that invades wounded or stressed leaf tissue under high humidity, rainfall, and warm tropical temperatures.",
                source_ids=["SRC_FAO_PLANT"],
            )
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Conidia are dispersed by wind currents and water splashes during heavy tropical rains.",
                source_ids=["SRC_UF_IFAS"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Survives on old infected banana trash, dried leaves, and pseudostem residues.",
                source_ids=["SRC_FAO_PLANT"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Maintain optimal plantation spacing to enhance sunlight penetration and wind ventilation through the canopy.",
                    source_ids=["SRC_UF_IFAS"],
                ),
                SourcedFact(
                    statement="Improve plantation soil drainage to prevent standing water and root asphyxiation.",
                    source_ids=["SRC_FAO_PLANT"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Regularly de-leaf and prune necrotic or severely spotted leaves, removing or mulching trash below ground.",
                    source_ids=["SRC_FAO_PLANT", "SRC_UF_IFAS"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Manage weed growth and maintain adequate potassium/nitrogen balance to support vigorous leaf cuticles.",
                    source_ids=["SRC_UF_IFAS"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Ensure healthy microbial soil communities with organic composts and beneficial Trichoderma root drenches.",
                    source_ids=["SRC_FAO_PLANT"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Standard protectant sprays utilized for Black Sigatoka control (such as copper oxychloride or dithiocarbamates) generally provide adequate suppression of Cordana spot.",
                    source_ids=["SRC_UF_IFAS"],
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Combine routine plantation de-leafing, adequate plant spacing, potassium fertilization, and standard Sigatoka copper management.",
                    source_ids=["SRC_FAO_PLANT", "SRC_UF_IFAS"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Ensure high soil fertility, proper drainage, and prevent mechanical injury to banana leaves during cultivation.",
                source_ids=["SRC_UF_IFAS"],
            )
        ],
        sources=["SRC_FAO_PLANT", "SRC_UF_IFAS"],
    ),

    "ginger__leaf_spot": DiseaseRecord(
        disease_slug="ginger__leaf_spot",
        common_name="Phyllosticta Leaf Spot",
        crop="ginger",
        scientific_name_causal_agent="Phyllosticta zingiberi",
        disease_type="Fungal",
        affected_parts=["leaf"],
        symptoms=[
            SourcedFact(
                statement="Small, oval to elongated yellow spots develop on young leaves, gradually expanding into white or papery tan centers with dark brown margins.",
                source_ids=["SRC_ICAR_IISR"],
            ),
            SourcedFact(
                statement="Multiple spots coalesce causing large areas of foliar drying, tearing, and premature drying of the shoot.",
                source_ids=["SRC_ICAR_IISR"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Papery white or bleached center with dark reddish-brown borders on ginger leaves.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="Favored by heavy monsoon rains, continuous cloudy weather, and high relative humidity (>85%).",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Splashing rain drops and runoff water spread conidia from leaf to leaf.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Survives in infected ginger crop debris in the soil between planting seasons.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Apply thick organic mulch (green leaves) immediately after planting to conserve soil moisture and prevent rain splash.",
                    source_ids=["SRC_ICAR_IISR"],
                ),
                SourcedFact(
                    statement="Ensure proper raised bed drainage to prevent waterlogging during the monsoon season.",
                    source_ids=["SRC_ICAR_IISR"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Collect and burn heavily infected leaves during the early vegetative stage.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Provide moderate shade using companion trees or intercrops in tropical spice gardens.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Seed rhizome treatment with Trichoderma viride and Pseudomonas fluorescens before planting.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Spray 1% Bordeaux mixture or copper oxychloride (0.2%) at the first appearance of leaf spots and repeat at 15-day intervals during wet spells.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Combine disease-free seed rhizome selection, bio-inoculation, green leaf mulching, raised beds, and timely Bordeaux mixture sprays.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Select seed rhizomes only from healthy, disease-free parent crops and treat with biocontrol agents before sowing.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        sources=["SRC_ICAR_IISR"],
    ),

    "ginger__sheath_blight": DiseaseRecord(
        disease_slug="ginger__sheath_blight",
        common_name="Sheath Blight",
        crop="ginger",
        scientific_name_causal_agent="Rhizoctonia solani",
        disease_type="Fungal",
        affected_parts=["stem", "pseudostem", "leaf_sheath"],
        symptoms=[
            SourcedFact(
                statement="Water-soaked, oval or irregular grayish-green lesions appear on the lower leaf sheath near the soil line.",
                source_ids=["SRC_ICAR_IISR"],
            ),
            SourcedFact(
                statement="Lesions enlarge, turn dark brown with bleached centers, and wrap around the pseudostem, causing yellowing and collapse of the entire shoot.",
                source_ids=["SRC_ICAR_IISR"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Blighted, rotting lower pseudostem sheaths near the soil line with brown sclerotia visible under humid conditions.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="Rhizoctonia solani is soil-borne and proliferates in wet, poorly drained soils with warm temperatures (28°C–32°C).",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Sclerotia and mycelia spread through soil water movement, farm implements, and infected planting material.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Sclerotia survive in the soil and on crop debris for several years.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Plant ginger on raised beds (15–20 cm high) with clear drainage channels between beds.",
                    source_ids=["SRC_ICAR_IISR"],
                ),
                SourcedFact(
                    statement="Rotate with non-host crops such as maize or leguminous cover crops.",
                    source_ids=["SRC_ICAR_IISR"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Uproot and destroy severely affected collapsed clumps along with surrounding soil.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Avoid waterlogging and excessive shade that prolongs soil saturation.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Soil application of Trichoderma harzianum enriched in farmyard manure (FYM) at planting.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Drench the base of plants with validamycin or carbendazim at the onset of sheath symptoms.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Ensure excellent raised bed drainage, FYM-Trichoderma soil incorporation, and immediate drenching of early infected foci.",
                    source_ids=["SRC_ICAR_IISR"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Use healthy certified seed rhizomes and solarize nursery beds before planting.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        sources=["SRC_ICAR_IISR"],
    ),

    "garlic__rust": DiseaseRecord(
        disease_slug="garlic__rust",
        common_name="Garlic Rust",
        crop="garlic",
        scientific_name_causal_agent="Puccinia allii",
        disease_type="Fungal",
        affected_parts=["leaf", "stem"],
        symptoms=[
            SourcedFact(
                statement="Small, white to yellow flecks or spots appear on both surfaces of garlic leaves and stems.",
                source_ids=["SRC_UC_IPM", "SRC_WSU_EXT"],
            ),
            SourcedFact(
                statement="Spots expand into raised, circular to elongate bright orange-to-reddish pustules (uredinia) that erupt through the leaf epidermis.",
                source_ids=["SRC_UC_IPM"],
            ),
            SourcedFact(
                statement="Severe infections cause complete leaf yellowing, extensive necrosis, premature leaf drying, and significantly reduced bulb size.",
                source_ids=["SRC_WSU_EXT"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Elongated, bright orange-red blister-like pustules containing powdery rust spores on allium leaves.",
                source_ids=["SRC_UC_IPM"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="Puccinia allii favors cool to moderate temperatures (12°C–20°C / 55°F–68°F) with high relative humidity (>90%) and 4+ hours of leaf moisture.",
                source_ids=["SRC_UC_IPM", "SRC_WSU_EXT"],
            )
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Urediniospores are carried on the wind over moderate to long distances.",
                source_ids=["SRC_UC_IPM"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Survives on volunteer alliums, leeks, chives, and infected allium crop residues.",
                source_ids=["SRC_WSU_EXT"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Rotate with non-allium crops for at least 3 years.",
                    source_ids=["SRC_UC_IPM"],
                ),
                SourcedFact(
                    statement="Plant garlic at wider in-row spacing to promote rapid foliage drying.",
                    source_ids=["SRC_WSU_EXT"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Destroy all volunteer garlic, wild onions, and unharvested allium cull piles near the field.",
                    source_ids=["SRC_UC_IPM"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Avoid excessive nitrogen fertilization late in the season, which promotes lush susceptible growth.",
                    source_ids=["SRC_WSU_EXT"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Sulfur dusts and potassium silicate applications can provide protective barrier suppression.",
                    source_ids=["SRC_FAO_PLANT"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Fungicides containing azoxystrobin, pyraclostrobin, or tebuconazole should be applied preventively when weather conditions favor rust outbreaks.",
                    source_ids=["SRC_UC_IPM"],
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Combine crop rotation, eradication of volunteer alliums, balanced nitrogen management, and timely strobilurin/triazole protectants.",
                    source_ids=["SRC_UC_IPM", "SRC_WSU_EXT"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Plant clean, disease-free certified garlic cloves and avoid planting adjacent to overwintering leek or onion crops.",
                source_ids=["SRC_WSU_EXT"],
            )
        ],
        sources=["SRC_UC_IPM", "SRC_WSU_EXT", "SRC_FAO_PLANT"],
    ),

    "bean__rust": DiseaseRecord(
        disease_slug="bean__rust",
        common_name="Bean Rust",
        crop="bean",
        scientific_name_causal_agent="Uromyces appendiculatus",
        disease_type="Fungal",
        affected_parts=["leaf", "pod"],
        symptoms=[
            SourcedFact(
                statement="Tiny, pale yellow or white flecks on lower and upper leaf surfaces that enlarge into raised, reddish-brown powdery pustules.",
                source_ids=["SRC_USDA_ARS", "SRC_UNL_EXT"],
            ),
            SourcedFact(
                statement="Pustules are often surrounded by a distinct yellow chlorotic border or halo.",
                source_ids=["SRC_UNL_EXT"],
            ),
            SourcedFact(
                statement="Severe rust causes leaf chlorosis, curling, premature defoliation, and reduced pod filling.",
                source_ids=["SRC_USDA_ARS"],
            ),
        ],
        distinguishing_features=[
            SourcedFact(
                statement="Reddish-brown powdery pustules that rub off on fingers, leaving rust-colored marks.",
                source_ids=["SRC_UNL_EXT"],
            )
        ],
        causes_and_conditions=[
            SourcedFact(
                statement="Uromyces appendiculatus requires moderate temperatures (17°C–24°C / 63°F–75°F) and 8+ hours of high humidity or dew.",
                source_ids=["SRC_UNL_EXT", "SRC_USDA_ARS"],
            )
        ],
        spread_and_transmission=[
            SourcedFact(
                statement="Urediniospores are disseminated by wind currents, field equipment, and workers.",
                source_ids=["SRC_UNL_EXT"],
            )
        ],
        recurrence_and_survival=[
            SourcedFact(
                statement="Teliospores survive on dry bean plant debris over the winter.",
                source_ids=["SRC_USDA_ARS"],
            )
        ],
        management=ManagementStrategies(
            cultural=[
                SourcedFact(
                    statement="Plant rust-resistant dry bean or snap bean cultivars.",
                    source_ids=["SRC_USDA_ARS", "SRC_UNL_EXT"],
                ),
                SourcedFact(
                    statement="Practice a 2-year or 3-year crop rotation with non-legume crops (such as corn or cereals).",
                    source_ids=["SRC_UNL_EXT"],
                ),
            ],
            sanitation=[
                SourcedFact(
                    statement="Incorporate or destroy bean crop residues immediately after harvest to accelerate debris decomposition.",
                    source_ids=["SRC_UNL_EXT"],
                )
            ],
            environmental=[
                SourcedFact(
                    statement="Avoid overhead sprinkler irrigation late in the afternoon that extends nighttime leaf wetness.",
                    source_ids=["SRC_UNL_EXT"],
                )
            ],
            biological=[
                SourcedFact(
                    statement="Bacillus pumilus or sulfur-based protective formulations can reduce initial spore infection in organic operations.",
                    source_ids=["SRC_FAO_PLANT"],
                )
            ],
            chemical_guidelines=[
                SourcedFact(
                    statement="Apply protectant or systemic fungicides (e.g., chlorothalonil, azoxystrobin, or tebuconazole) at first sign of rust flecks prior to pod set.",
                    source_ids=["SRC_UNL_EXT"],
                )
            ],
            integrated_summary=[
                SourcedFact(
                    statement="Deploy resistant varieties, 3-year non-host rotation, post-harvest residue burial, and early targeted fungicide applications.",
                    source_ids=["SRC_USDA_ARS", "SRC_UNL_EXT"],
                )
            ],
        ),
        prevention=[
            SourcedFact(
                statement="Plant certified rust-free seed and select varieties resistant to prevailing regional rust races.",
                source_ids=["SRC_USDA_ARS"],
            )
        ],
        sources=["SRC_USDA_ARS", "SRC_UNL_EXT", "SRC_FAO_PLANT"],
    ),
}

# ---------------------------------------------------------------------------
# 2. Pilot Crop Agronomy Profiles
# ---------------------------------------------------------------------------

PILOT_CROPS: dict[str, CropRecord] = {
    "tomato": CropRecord(
        crop_name="tomato",
        common_name="Tomato",
        scientific_name="Solanum lycopersicum",
        category="Solanaceous Vegetable",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Tomatoes thrive in full sunlight (6-8 hours daily) with well-drained, loam soil rich in organic matter (pH 6.0 to 6.8).",
                source_ids=["SRC_CORNELL_EXT", "SRC_UC_IPM"],
            ),
            SourcedFact(
                statement="Optimal daytime temperatures are 21°C–29°C (70°F–85°F) and nighttime temperatures between 15°C–20°C (60°F–68°F).",
                source_ids=["SRC_UC_IPM"],
            ),
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Provide consistent, deep watering (1–2 inches per week) using drip irrigation at the soil base to avoid wetting foliage and prevent blossom end rot.",
                source_ids=["SRC_PURDUE_EXT", "SRC_CORNELL_EXT"],
            )
        ],
        common_diseases=["tomato__early_blight", "tomato__septoria_leaf_spot", "tomato__late_blight", "tomato__bacterial_leaf_spot"],
        sources=["SRC_CORNELL_EXT", "SRC_UC_IPM", "SRC_PURDUE_EXT"],
    ),

    "cucumber": CropRecord(
        crop_name="cucumber",
        common_name="Cucumber",
        scientific_name="Cucumis sativus",
        category="Cucurbitaceous Vegetable",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Cucumbers require warm soil (>18°C / 65°F), full sun, and fertile, well-drained soil rich in compost (pH 6.0 to 6.8).",
                source_ids=["SRC_CORNELL_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Maintain consistent moisture (approx 1 inch per week) via drip irrigation; uneven watering causes bitterness and fruit malformation.",
                source_ids=["SRC_NCSTATE_EXT"],
            )
        ],
        common_diseases=["cucumber__downy_mildew", "cucumber__angular_leaf_spot", "cucumber__powdery_mildew", "cucumber__bacterial_wilt"],
        sources=["SRC_CORNELL_EXT", "SRC_NCSTATE_EXT"],
    ),

    "soybean": CropRecord(
        crop_name="soybean",
        common_name="Soybean",
        scientific_name="Glycine max",
        category="Legume / Oilseed",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Soybeans grow best in well-drained silt loam to clay loam soils with temperatures between 20°C–30°C (68°F–86°F) and adequate seasonal rainfall.",
                source_ids=["SRC_USDA_ARS", "SRC_IOWA_STATE_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Critical moisture periods are during flowering (R1-R2) and pod development (R3-R5); water stress at these stages reduces yield.",
                source_ids=["SRC_IOWA_STATE_EXT"],
            )
        ],
        common_diseases=["soybean__rust", "soybean__bacterial_blight", "soybean__downy_mildew", "soybean__frog_eye_leaf_spot"],
        sources=["SRC_USDA_ARS", "SRC_IOWA_STATE_EXT"],
    ),

    "banana": CropRecord(
        crop_name="banana",
        common_name="Banana",
        scientific_name="Musa acuminata / Musa balbisiana",
        category="Tropical Fruit",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Bananas require tropical climates with temperatures above 26°C (78°F), high humidity, full sunlight, and deep, well-drained volcanic or alluvial soils (pH 5.5 to 7.0).",
                source_ids=["SRC_FAO_PLANT", "SRC_UF_IFAS"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="High water demand (100–150 mm per month) distributed evenly; avoid waterlogging which triggers root asphyxiation.",
                source_ids=["SRC_FAO_PLANT"],
            )
        ],
        common_diseases=["banana__cordana_leaf_spot", "banana__panama_disease", "banana__black_leaf_streak", "banana__anthracnose"],
        sources=["SRC_FAO_PLANT", "SRC_UF_IFAS"],
    ),

    "ginger": CropRecord(
        crop_name="ginger",
        common_name="Ginger",
        scientific_name="Zingiber officinale",
        category="Spice / Rhizome",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Ginger requires a warm, humid tropical or subtropical climate, partial shade (20–30%), and rich, loose, well-drained sandy loam or clay loam soil rich in organic matter (pH 5.5 to 6.5).",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Requires frequent light watering during rhizome development on raised beds; waterlogging causes rhizome soft rot.",
                source_ids=["SRC_ICAR_IISR"],
            )
        ],
        common_diseases=["ginger__leaf_spot", "ginger__sheath_blight"],
        sources=["SRC_ICAR_IISR"],
    ),

    "garlic": CropRecord(
        crop_name="garlic",
        common_name="Garlic",
        scientific_name="Allium sativum",
        category="Allium Vegetable",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Garlic requires cold winter vernalization (0°C–10°C for 4–8 weeks) followed by warm sunny days for bulb development in well-drained, loose loam soil (pH 6.0 to 7.0).",
                source_ids=["SRC_UC_IPM", "SRC_WSU_EXT"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Provide 1 inch of water weekly during active vegetative growth; cease watering 2–3 weeks before harvest to allow wrappers to dry.",
                source_ids=["SRC_WSU_EXT"],
            )
        ],
        common_diseases=["garlic__rust", "garlic__leaf_blight"],
        sources=["SRC_UC_IPM", "SRC_WSU_EXT"],
    ),

    "bean": CropRecord(
        crop_name="bean",
        common_name="Common Bean",
        scientific_name="Phaseolus vulgaris",
        category="Legume",
        optimal_growing_conditions=[
            SourcedFact(
                statement="Beans grow best in full sun, warm soil (>15°C / 60°F), and well-drained loam soil with moderate fertility (pH 6.0 to 6.8).",
                source_ids=["SRC_UNL_EXT", "SRC_USDA_ARS"],
            )
        ],
        watering_guidelines=[
            SourcedFact(
                statement="Deliver 1 inch of water per week; avoid wetting leaves during flowering and pod development to minimize fungal spore spread.",
                source_ids=["SRC_UNL_EXT"],
            )
        ],
        common_diseases=["bean__rust", "bean__angular_leaf_spot", "bean__halo_blight", "bean__mosaic_virus"],
        sources=["SRC_USDA_ARS", "SRC_UNL_EXT"],
    ),
}
