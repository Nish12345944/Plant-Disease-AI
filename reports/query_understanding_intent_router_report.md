# Query Understanding & Intent Router Technical Report

**Date:** 2026-10-07  
**Module:** `router` (Query Understanding, Normalization, Entity Extraction, Intent Classification, Context Routing)  
**Status:** **COMPLETE & 100% TESTED**

---

## 1. Executive Summary

This phase implements a deterministic, multi-layered **Query Understanding & Intent Router** capable of parsing natural, messy, informal, spelling-corrupted, and Hinglish farmer inquiries without requiring external paid APIs or large LLMs for routine routing.

The architecture decouples query comprehension (**WHAT the user wants**) from agricultural treatment generation (**WHAT knowledge to retrieve**):

```
USER QUERY / AUDIO TRANSCRIPT
              ↓
    TEXT NORMALIZATION
  (Spelling correction, phonetic normalization, Hinglish mapping)
              ↓
    ENTITY EXTRACTION
  (Crop, Disease Slug, Symptoms, Plant Part, Action, Language)
              ↓
    INTENT CLASSIFICATION
  (12-Intent Taxonomy, Pattern Matching, Calibrated Confidence)
              ↓
    CONTEXT-AWARE ROUTER
  (Visual Context Merging, Multimodal Input Contract, Routing Decision)
              ↓
    STANDARDIZED OUTPUT CONTRACT
```

---

## 2. Centralized 12-Intent Taxonomy

| Intent | Description | Example Query | Target Knowledge Domain |
|---|---|---|---|
| `IDENTIFY_CROP` | User asks what crop/plant is shown or described | *"What plant is this?"* | `plant_identification` |
| `CHECK_HEALTH` | User asks if the plant is healthy/normal | *"Is my plant healthy?"* | `health_assessment` |
| `DIAGNOSE_PLANT` | User asks what happened or describes damage/spots | *"What happened to my plant?"* | `diagnosis` |
| `IDENTIFY_DISEASE` | User requests the specific disease name | *"What disease does this plant have?"* | `disease_identification` |
| `SYMPTOMS` | User asks about symptoms/signs of a disease | *"What are the symptoms of early blight?"* | `symptom_knowledge` |
| `CAUSE` | User asks why the problem happened / etiology | *"Why did this disease happen?"* | `disease_etiology` |
| `TREATMENT` | User asks how to cure/treat or what to spray | *"How do I treat this?"* / *"kya karu"* | `treatment_advisory` |
| `PREVENTION` | User asks how to prevent recurrence or spread | *"How can I prevent this?"* | `prevention_guidelines` |
| `GENERAL_PLANT_INFO`| User asks general care/cultivation/growing info | *"Tell me about tomato plants"* | `general_agronomy` |
| `FOLLOW_UP` | Contextual continuation of prior diagnosis | *"Can it spread to other crops?"* | `contextual_follow_up` |
| `AMBIGUOUS` | Query is too vague or lacks clear actionable intent | *"plant problem"* / *"what do"* | `clarification` |
| `INSUFFICIENT_INFO` | Missing required input (e.g. empty prompt & no image)| *""* (No input provided) | `clarification` |

---

## 3. Text Normalization Strategy

The normalization layer ([`router/normalizer.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/router/normalizer.py)) operates in sub-millisecond time:
1. **Spelling & Phonetic Correction:**
   - `"tamato"`, `"tomoto"`, `"tomatos"`, `"tomaato"` → `"tomato"`
   - `"cucamber"`, `"cucmber"` → `"cucumber"`
   - `"leafs"`, `"leafes"` → `"leaves"`
   - `"yelow"` → `"yellow"`, `"brwon"` → `"brown"`
   - `"treet"` → `"treat"`, `"happend"` → `"happened"`
2. **Hinglish & Hindi Agricultural Phrase Mapping:**
   - `"patte"`, `"patta"`, `"patti"` → `"leaves"` / `"leaf"`
   - `"peela"`, `"peele"` → `"yellow"`
   - `"dhabbe"`, `"daag"` → `"spots"`
   - `"sukh rhe"`, `"sukh raha"` → `"drying"`
   - `"kharab"` → `"damaged"`
   - `"bimari"` → `"disease"`, `"ilaj"` → `"treatment"`
   - `"kya hua"` → `"what happened"`, `"kya karu"` → `"what should i do"`
   - `"dawa"`, `"dawai"` → `"medicine"`
   - `"roktham"`, `"bachav"` → `"prevention"`
3. **Language Detection:** Identifies `en` vs `hi-Latn` (transliterated Hindi/Hinglish).

---

## 4. Entity Extraction Strategy

The entity extractor ([`router/entity_extractor.py`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/router/entity_extractor.py)) maps natural phrases into the official project taxonomies:
- **`crop`:** Matches 39 official crop families (e.g., `"tomato"`, `"cucumber"`, `"wheat"`, `"apple"`).
- **`disease`:** Resolves disease mentions to verified Model 2 slugs (e.g., `"tomato__early_blight"`, `"apple__rust"`).
- **`symptoms`:** Normalized symptom tags (`"yellowing"`, `"brown_spots"`, `"wilting"`, `"drying"`, `"rot"`, `"powdery_coating"`).
- **`plant_part`:** Anatomical targets (`"leaf"`, `"fruit"`, `"stem"`, `"flower"`, `"root"`).
- **`action`:** Operational intent signal (`"treatment"`, `"prevention"`, `"identification"`, `"diagnosis"`, `"cause"`, `"symptoms"`).

---

## 5. Context-Aware Visual Routing

Visual context from Model 1 and Model 2 V2 inference is dynamically unified with text queries:
- **Case 1: Visual Result Present + Vague Question**
  - *Query:* `"what happened to my plant?"`
  - *Visual Inference:* `{crop: "tomato", disease: "tomato__early_blight", status: "diseased"}`
  - *Route:* `DIAGNOSE_PLANT` with full context preserved (`tomato` + `tomato__early_blight`).
- **Case 2: Visual Result Present + Treatment Request**
  - *Query:* `"how do I treat this?"`
  - *Route:* `TREATMENT` targeting `treatment_advisory` domain with `{crop: "tomato", disease: "tomato__early_blight"}`.
- **Case 3: Visual Result Present + Identification Question**
  - *Query:* `"what plant is this?"`
  - *Route:* `IDENTIFY_CROP` targeting `plant_identification` (prevents unnecessary treatment dumps).
- **Case 4: No Visual Result + Vague Question**
  - *Query:* `"what happened"`
  - *Route:* `INSUFFICIENT_INFO` / `AMBIGUOUS` with `needs_clarification: true` (prevents diagnostic hallucination).

---

## 6. Standardized Output Contract

```json
{
  "raw_text": "my tamato patte are yelow what happend",
  "normalized_text": "my tomato leaves are yellow what happened",
  "intent": "DIAGNOSE_PLANT",
  "intent_confidence": 0.92,
  "entities": {
    "crop": "tomato",
    "disease": null,
    "symptoms": ["yellowing"],
    "plant_part": "leaf",
    "action": "diagnosis",
    "language": "hi-Latn"
  },
  "routing_decision": {
    "needs_model1": true,
    "needs_model2": true,
    "needs_rag": true,
    "target_knowledge_domain": "diagnosis"
  },
  "needs_clarification": false,
  "clarification_reason": null,
  "suggested_clarification": null,
  "context": {}
}
```

---

## 7. Test Suite Validation Results

Executed test suites:
1. `scripts/test_query_understanding_suite.py`: **27 / 27 (100%) PASSED**
2. `router/test_query_router.py`: **18 / 18 (100%) PASSED**
3. `pipeline/test_orchestrator.py`: **24 / 24 (100%) PASSED**
4. `scripts/test_healthy_crop_inference.py`: **7 / 7 (100%) PASSED** (Zero Model 1 / Model 2 regressions).

### Test Coverage Breakdown:
- **Section A (Normal English):** 9/9 Passed (Identify Crop, Check Health, Identify Disease, Diagnose Plant, Cause, Symptoms, Treatment, Prevention, General Info).
- **Section B (Spelling & Phonetics):** 4/4 Passed (`"tomoto"`, `"leafs are yelow"`, `"treet tomato"`, `"tomato me ilaj kya h"`).
- **Section C (Broken / Hinglish):** 4/4 Passed (`"plant not good what do"`, `"leaves bad what happened"`, `"tomato patte sukh rhe"`, `"kya karu plant kharab"`).
- **Section D (Ambiguity & Clarification):** 4/4 Passed (`"what do"`, `"plant problem"`, contextual `"what happened"`, empty prompt).
- **Section E (Entity Extraction):** 3/3 Passed (`crop`, `plant_part`, `symptoms`, `disease`, `action`).
- **Section F (Contextual Routing):** 3/3 Passed (Preservation of visual ground truth across different questions).

---

## 8. Exact Next Phase

**Phase Next:** Build the verified **Agricultural Treatment & Plant Knowledge Retrieval (RAG / Knowledge Base)** layer to answer the structured intents produced by this router with scientific, non-hallucinatory agronomy recommendations.
