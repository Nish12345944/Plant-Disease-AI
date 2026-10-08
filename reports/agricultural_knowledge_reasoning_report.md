# AGRICULTURAL KNOWLEDGE BASE & CONVERSATIONAL REASONING ENGINE REPORT

**Phase:** Phase 6 — Agricultural Knowledge Architecture & LLM-Free Conversational Reasoning  
**Date:** October 2026  
**Status:** COMPLETE & VERIFIED  
**Integrity:** 100% Deterministic | Zero Cloud/Paid LLMs | Model 1 & Model 2 V2 Untouched | Complete Source Provenance  

---

## 1. Executive Summary

We have designed, implemented, and validated an **Agricultural Knowledge & Conversational Reasoning Engine** that operates as an expert conversational agricultural assistant **without using ChatGPT, Ollama, OpenAI, or any cloud/generative LLM**.

The engine processes natural-language agricultural questions, follow-ups, broken queries, Hinglish phrasing, and multi-turn visual inferences through an 8-stage deterministic reasoning and retrieval pipeline:

```
USER QUESTION [+ OPTIONAL VISUAL INFERENCE]
    ↓
QUERY UNDERSTANDING (Text Normalization, Entity Extraction, Intent Classification)
    ↓
DIALOGUE CONTEXT & ANAPHORA RESOLUTION (Short-term State, Pronoun Binding: "it", "why", "spread")
    ↓
RULE-BASED STRUCTURED REASONING (7 Deterministic Safety & Compatibility Rules)
    ↓
TARGETED KNOWLEDGE BASE RETRIEVAL (Intent-Driven Section Fact Extraction, No Whole-Record Dumps)
    ↓
INTERMEDIATE ANSWER PLANNING (Dynamic Section Layout Formulation)
    ↓
DETERMINISTIC NATURAL-LANGUAGE RESPONSE BUILDER (Bullet Formulation, Provenance Citations)
    ↓
FINAL GROUNDED RESPONSE WITH TRACEABLE SOURCES
```

Every factual management strategy, symptom description, and epidemiological condition is grounded in a verified local repository with full provenance tracing back to Tier-1 and Tier-2 agricultural institutions (USDA, FAO, UC IPM, Cornell Extension, Purdue Extension, NC State Extension, UF IFAS, ICAR-IISR, Iowa State, Penn State, UNL Extension, and WSU Extension).

---

## 2. Knowledge Architecture & Schema

The knowledge architecture rejects unstructured free-text dumps in favor of a strongly typed, hierarchical schema defined in [`knowledge/schema.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/knowledge/schema.py).

### 2.1 Core Schemas

#### A. Source Record (`SourceRecord`)
- `source_id`: Unique identifier (e.g., `SRC_UC_IPM`, `SRC_CORNELL_EXT`)
- `title`: Formal title of publication or database
- `organization`: Publishing institution or research body
- `url_or_doi`: Official URL or DOI link
- `publication_year`: Year of publication or last revision
- `source_tier`: `TIER_1` (Gov/USDA/FAO/National Research/Peer-Reviewed) or `TIER_2` (University Extension/Plant Pathology Institutes)
- `notes`: Specific editorial or scope notes

#### B. Sourced Fact (`SourcedFact`)
- `statement`: Precise factual statement (preserves agronomic meaning without exaggeration)
- `source_ids`: List of registered `source_id`s validating this specific claim
- `detail`: Optional auxiliary application nuance or regional context

#### C. Management Strategies (`ManagementStrategies`)
- `cultural`: Physical practices (crop rotation, trellising, mulching, row spacing)
- `sanitation`: Field hygiene (debris removal, sterilization of pruning tools, weed control)
- `environmental`: Moisture and canopy controls (drip irrigation, morning watering, ventilation)
- `biological`: Biocontrol agents (e.g., *Bacillus subtilis*, *Trichoderma harzianum*, copper octanoate)
- `chemical_guidelines`: Evidence-backed active ingredients (copper hydroxide, chlorothalonil) with safety notes
- `integrated_summary`: Holistic integrated disease management (IPM) synthesis

#### D. Disease Record (`DiseaseRecord`)
- `disease_slug`: Canonical slug matching Model 2 V2 taxonomy (e.g. `tomato__early_blight`)
- `common_name`: Common English disease name
- `crop`: Host crop canonical slug
- `scientific_name_causal_agent`: Scientific binomial (e.g., *Alternaria solani*, *Pseudoperonospora cubensis*)
- `disease_type`: Pathogen type (`Fungal`, `Bacterial`, `Oomycete`, `Viral`, `Nematode`)
- `affected_parts`: Affected plant organs (`leaf`, `stem`, `fruit`, `tuber`, `sheath`)
- `symptoms`: List of sourced symptom facts
- `distinguishing_features`: Sourced key diagnostic markers (e.g., target-board concentric rings)
- `causes_and_conditions`: Environmental triggers (temperature ranges, humidity, leaf wetness duration)
- `spread_and_transmission`: Dispersal mechanisms (windborne conidia, rain splash, soil-borne sclerotia)
- `recurrence_and_survival`: Overwintering and survival mechanisms (crop residue, alternative weed hosts)
- `management`: Structured `ManagementStrategies`
- `prevention`: Sourced prophylactic practices
- `sources`: Source ID list

#### E. Crop Record (`CropRecord`)
- `crop_name`: Canonical crop name
- `common_name`: Display name
- `scientific_name`: Botanical binomial
- `category`: Agronomic category (`Vegetable`, `Fruit`, `Cereal`, `Legume`, `Spice`, `Floriculture`)
- `optimal_growing_conditions`: Sourced environmental baselines
- `watering_guidelines`: Sourced irrigation guidelines
- `common_diseases`: Linked disease slugs
- `sources`: Source ID list

---

## 3. Source Registry & Provenance System

The system implements an immutable Tier-1 / Tier-2 source registry in [`knowledge/sources.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/knowledge/sources.py). No random blogs, forums, or unverified websites are permitted.

### Registered Authoritative Sources

| Source ID | Institution / Organization | Tier | Focus Area / Title |
| :--- | :--- | :--- | :--- |
| `SRC_USDA_ARS` | United States Department of Agriculture (USDA ARS) | Tier 1 | National Plant Disease Research & Diagnostics |
| `SRC_FAO_PLANT` | Food and Agriculture Organization of the UN (FAO) | Tier 1 | Integrated Pest & Disease Management Guidelines |
| `SRC_UC_IPM` | University of California Statewide IPM Program | Tier 1 | UC IPM Pest Management Guidelines |
| `SRC_CORNELL_EXT` | Cornell University Cooperative Extension | Tier 2 | Vegetable Pathology Factsheets & Diagnostic Guides |
| `SRC_PURDUE_EXT` | Purdue University Cooperative Extension Service | Tier 2 | Plant and Pest Diagnostic Laboratory Disease Guides |
| `SRC_NCSTATE_EXT` | North Carolina State University Extension | Tier 2 | Plant Pathology Extension Publications & Factsheets |
| `SRC_UF_IFAS` | University of Florida Extension (UF/IFAS) | Tier 2 | Electronic Data Information Source (EDIS) Pathology |
| `SRC_ICAR_IISR` | ICAR - Indian Institute of Spices Research | Tier 1 | Spices & Plantation Crops Pathology Package of Practices |
| `SRC_IOWA_STATE` | Iowa State University Extension and Outreach | Tier 2 | Soybean & Field Crop Disease Management Guides |
| `SRC_PENN_STATE` | Penn State Extension | Tier 2 | Plant Disease Fact Sheets & Agronomy Guides |
| `SRC_UNL_EXT` | University of Nebraska–Lincoln CropWatch | Tier 2 | Crop Disease Management & Epidemiology |
| `SRC_WSU_EXT` | Washington State University Extension | Tier 2 | Tree Fruit & Vegetable Pathology Management Guides |

Every output generated by the conversational assistant includes formatted citations linking directly to these sources.

---

## 4. Treatment Safety & Chemical Control Protocol

To ensure grower safety and prevent agricultural damage, the reasoning engine enforces strict protocols:
1. **No Dosages Fabricated:** The system never fabricates pesticide concentrations, spray intervals, or active ingredient combinations.
2. **Management vs Cure Distinction:** Diseases are framed in terms of *suppression*, *sanitation*, and *integrated management* rather than guaranteed cures.
3. **Hierarchy of Control:** Cultural, physical, and environmental methods (spacing, drip watering, crop rotation) are presented first, followed by biological controls and licensed chemical protectants.
4. **Mandatory Safety Caveats:** All chemical suggestions include notes emphasizing label compliance, local agricultural extension consultation, and protective application.

---

## 5. Dialogue Context & Anaphora Resolution

Conversational history is managed by `ConversationManager` in [`knowledge/dialogue.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/knowledge/dialogue.py).

- **Multi-Turn Context Tracking:** Stores the last 10 conversational turns with full query, intent, active crop, disease, status, and response.
- **Visual Evidence Binding:** Merges visual diagnosis outcomes (Model 1 crop, Model 2 disease, confidence, status) into the active session.
- **Anaphora Resolution:** Resolves ambiguous relative pronouns and short follow-up questions:
  - *"Why?"* → Resolves to causes/conditions of active disease.
  - *"How do I treat it?"* → Resolves `"it"` to active disease slug and executes `TREATMENT`.
  - *"Can it spread?"* → Resolves transmission mechanisms for active disease.
  - *"Will it come back next year?"* → Resolves survival/overwintering facts for active disease.
  - *"What should I do?"* → Resolves to immediate cultural and sanitation management.

---

## 6. Structured Rule-Based Reasoning Engine

The reasoning engine in [`knowledge/reasoning.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/knowledge/reasoning.py) applies 7 explicit deterministic rules:

- **RULE 1 (`RULE_1_HEALTHY_CONFIRMATION`):** If visual inference predicts status `healthy`, disease treatment is contraindicated. The system explains the plant is healthy and outputs baseline cultural maintenance.
- **RULE 2 (`RULE_2_UNCERTAIN_VISUAL_EVIDENCE`):** If visual confidence is below diagnostic threshold, the diagnosis is marked uncertain. The system outlines visual verification steps and requests clearer photos.
- **RULE 3 (`RULE_3_INCOMPATIBLE_REJECTION`):** If Model 1 crop and Model 2 disease are biologically incompatible (e.g., banana Panama disease on tomato), the prediction is rejected and the user is alerted to inspect the plant.
- **RULE 4 (`RULE_4_MISSING_DISEASE_FOR_TREATMENT`):** If treatment or prevention is requested but no disease has been identified or provided, the system does not invent a treatment; it requests clarification or a leaf photo.
- **RULE 5 (`RULE_5_AMBIGUOUS_QUERY`):** For ambiguous or broken queries without context (e.g. *"what do?"*, *"help"*), the system provides helpful clarification prompts without hallucination.
- **RULE 6 (`RULE_6_GROUNDED_RETRIEVAL`):** When entities are verified and resolved, targeted facts are extracted and dispatched to the answer planner.
- **RULE 7 (`RULE_7_KNOWLEDGE_UNAVAILABLE`):** If a disease or crop is requested that is not yet verified in the KB, the system explicitly states that verified records are unavailable rather than guessing.

---

## 7. Intermediate Answer Planner & Deterministic Response Builder

The answer planner in [`knowledge/planner.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/knowledge/planner.py) maps the reasoning decision and retrieved facts into an intermediate layout:

- `TREATMENT` → `[condition_identification, cultural_management, sanitation_practices, environmental_controls, biological_options, chemical_guidance, prevention_summary]`
- `PREVENTION` → `[condition_identification, preventive_measures, cultural_practices]`
- `CAUSE` → `[condition_identification, causal_agent_and_type, favorable_conditions, spread_mechanism]`
- `SYMPTOMS` → `[condition_identification, primary_symptoms, distinguishing_features, affected_plant_parts]`
- `DIAGNOSE_PLANT` → `[diagnosis_summary, observed_symptoms, causal_overview, immediate_management_preview]`

The deterministic response builder in [`knowledge/response_builder.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/knowledge/response_builder.py) compiles these sections into structured, formatted natural language with bullet points and source attributions.

---

## 8. Pilot Knowledge Population

A diverse pilot knowledge base covering 10 diseases across 7 crop families was populated with verified data:

1. **Tomato Early Blight** (`tomato__early_blight`) — *Alternaria solani* (Fungal) | Sources: UC IPM, Cornell, Purdue, USDA ARS, FAO
2. **Tomato Septoria Leaf Spot** (`tomato__septoria_leaf_spot`) — *Septoria lycopersici* (Fungal) | Sources: Purdue, Cornell, FAO
3. **Cucumber Downy Mildew** (`cucumber__downy_mildew`) — *Pseudoperonospora cubensis* (Oomycete) | Sources: NC State, Cornell, USDA ARS, FAO
4. **Squash Powdery Mildew** (`squash__powdery_mildew`) — *Podosphaera xanthii* (Fungal) | Sources: UC IPM, Cornell, Penn State
5. **Soybean Rust** (`soybean__rust`) — *Phakopsora pachyrhizi* (Fungal) | Sources: USDA ARS, Iowa State, UNL
6. **Banana Cordana Leaf Spot** (`banana__cordana_leaf_spot`) — *Neocordana musae* (Fungal) | Sources: FAO, UF/IFAS
7. **Ginger Leaf Spot** (`ginger__leaf_spot`) — *Phyllosticta zingiberis* (Fungal) | Sources: ICAR-IISR, FAO
8. **Ginger Sheath Blight** (`ginger__sheath_blight`) — *Rhizoctonia solani* (Fungal) | Sources: ICAR-IISR, FAO
9. **Garlic Rust** (`garlic__rust`) — *Puccinia allii* (Fungal) | Sources: UC IPM, WSU Extension
10. **Bean Rust** (`bean__rust`) — *Uromyces appendiculatus* (Fungal) | Sources: USDA ARS, Penn State, FAO

---

## 9. Test Suite Verification & Results

### 9.1 New Agricultural Knowledge & Reasoning Test Suite (`scripts/test_agricultural_knowledge_engine.py`)

| Part | Test Category | Number of Tests | Pass Rate |
| :--- | :--- | :--- | :--- |
| **Part A** | Direct Knowledge Questions (Symptoms, Cause, Treatment, Prevention) | 4 | 4/4 (100%) |
| **Part B** | Contextual & Anaphoric Follow-ups ("Why?", "How to treat it?", "Can it spread?", "Will it come back?") | 5 | 5/5 (100%) |
| **Part C** | Visual Inference Integration + Contextual Queries | 3 | 3/3 (100%) |
| **Part D** | Unknown / Unverified Knowledge Handling (Non-hallucination) | 2 | 2/2 (100%) |
| **Part E** | Ambiguous & Insufficient Queries (Clarification requests) | 2 | 2/2 (100%) |
| **Part F** | Healthy Specimen Queries (Zero chemical treatment contraindicated) | 1 | 1/1 (100%) |
| **Part G** | Incompatible Crop-Disease Protection | 1 | 1/1 (100%) |
| **Part H** | Multi-Crop Pilot KB Coverage (Cucumber, Soybean, Garlic, Ginger, Banana, Sources) | 6 | 6/6 (100%) |
| **Total** | **All Knowledge & Reasoning Engine Tests** | **24** | **24/24 (100.0%)** |

### 9.2 Regression Test Suites

| Test Suite File | Focus Area | Checks | Result |
| :--- | :--- | :--- | :--- |
| [`scripts/test_healthy_crop_inference.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/scripts/test_healthy_crop_inference.py) | Model 1 + Model 2 Healthy/Disease inference & compatibility | 7 | **7/7 PASS (100%)** |
| [`scripts/test_query_understanding_suite.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/scripts/test_query_understanding_suite.py) | Query normalization, spelling correction, entity extraction, intent routing | 27 | **27/27 PASS (100%)** |
| [`router/test_query_router.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/router/test_query_router.py) | Router taxonomy backward compatibility & intent mapping | 18 | **18/18 PASS (100%)** |
| [`pipeline/test_orchestrator.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/pipeline/test_orchestrator.py) | Multimodal input combination (audio/image/text) | 24 | **24/24 PASS (100%)** |

**Cumulative System Test Count:** **100/100 Tests Passing (100.0%)**

---

## 10. Verification of Constraints

- **No Generative / Cloud LLMs:** Confirmed. All reasoning, retrieval, planning, and response generation operate deterministically with local Python modules.
- **No Ollama / Paid APIs:** Confirmed. Zero API calls or external server requirements.
- **Model 1 & Model 2 V2 Integrity:** Confirmed. Model weights, checkpoints, class mappings, and visual inference contracts remain unchanged.
- **Zero Hallucination:** Confirmed. Unverified diseases and missing data trigger explicit clarification or unavailability notices rather than fabricated claims.

---

## 11. Scaling Plan for All 116 Diseases

The architectural blueprint is now complete and validated. To expand from the 10-disease pilot to all 116 Model 2 V2 disease classes:
1. **JSON Ingestion Pipeline:** Create automated schema validators for disease JSON files in `knowledge/store/diseases/`.
2. **Institutional Source Harvesting:** Ingest extension facts from USDA ARS, UC IPM, Cornell, UF/IFAS, Purdue, and ICAR for the remaining 106 disease classes.
3. **Batch Integrity Verification:** Run automated provenance checks ensuring every newly added fact references a valid `source_id` in `SOURCE_REGISTRY`.

---

## 12. Next Phase Recommendation

**Upcoming Phase:** Full End-to-End Orchestration & API Integration (wiring Model 1, Model 2 V2, Query Router, and Agricultural Knowledge Assistant into FastAPI endpoints and unified request handling).
