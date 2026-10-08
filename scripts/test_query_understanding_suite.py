"""
Comprehensive Test Suite: Query Understanding & Intent Router Layer
===================================================================
Tests all categories specified in the phase requirements:
  A. Normal English queries across 12-intent taxonomy
  B. Spelling mistakes and phonetic corrections
  C. Broken / informal and Hinglish agricultural phrasing
  D. Ambiguity detection and non-hallucinatory clarification
  E. Structured entity extraction (crop, disease, symptoms, plant part, action)
  F. Visual context integration & preservation
"""

import sys
import os
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from router.taxonomy import Intent
from router.query_router import route_multimodal_query, route_query


def run_all_tests():
    print("=" * 80)
    print("RUNNING COMPREHENSIVE QUERY UNDERSTANDING & INTENT ROUTER TEST SUITE")
    print("=" * 80)

    total_tests = 0
    passed_tests = 0

    def check(test_name: str, condition: bool, details: str = ""):
        nonlocal total_tests, passed_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f"  [PASS] {test_name}")
        else:
            print(f"  [FAIL] {test_name} - {details}")

    # -------------------------------------------------------------------------
    # SECTION A: Normal English Queries
    # -------------------------------------------------------------------------
    print("\n--- SECTION A: Normal English Intent Classification ---")
    
    sec_a_cases = [
        ("What plant is this?", Intent.IDENTIFY_CROP),
        ("Is my plant healthy?", Intent.CHECK_HEALTH),
        ("What disease does this plant have?", Intent.IDENTIFY_DISEASE),
        ("What happened to my plant?", Intent.DIAGNOSE_PLANT),
        ("Why did this disease happen?", Intent.CAUSE),
        ("What are the symptoms?", Intent.SYMPTOMS),
        ("How do I treat this?", Intent.TREATMENT),
        ("How do I prevent this?", Intent.PREVENTION),
        ("Tell me about tomato plants", Intent.GENERAL_PLANT_INFO),
    ]

    for q, exp_intent in sec_a_cases:
        res = route_multimodal_query(text=q)
        check(
            f"Query: '{q}' -> {exp_intent.value}",
            res.intent == exp_intent.value,
            f"Got intent: {res.intent} (conf: {res.intent_confidence:.2f})"
        )

    # -------------------------------------------------------------------------
    # SECTION B: Spelling Mistakes & Phonetic Normalization
    # -------------------------------------------------------------------------
    print("\n--- SECTION B: Spelling Mistakes & Phonetic Correction ---")
    
    # 1. "what happend to my tomoto"
    res_b1 = route_multimodal_query(text="what happend to my tomoto")
    check(
        "Spelling: 'what happend to my tomoto' -> crop='tomato', intent=DIAGNOSE_PLANT",
        res_b1.entities.crop == "tomato" and res_b1.intent == Intent.DIAGNOSE_PLANT.value,
        f"Crop: {res_b1.entities.crop}, Intent: {res_b1.intent}"
    )

    # 2. "my tomato leafs are yelow"
    res_b2 = route_multimodal_query(text="my tomato leafs are yelow")
    check(
        "Spelling: 'my tomato leafs are yelow' -> crop='tomato', part='leaf', symptoms=['yellowing']",
        res_b2.entities.crop == "tomato" and res_b2.entities.plant_part == "leaf" and "yellowing" in res_b2.entities.symptoms,
        f"Crop: {res_b2.entities.crop}, Part: {res_b2.entities.plant_part}, Symptoms: {res_b2.entities.symptoms}"
    )

    # 3. "how to treet tomato"
    res_b3 = route_multimodal_query(text="how to treet tomato")
    check(
        "Spelling: 'how to treet tomato' -> intent=TREATMENT, crop='tomato'",
        res_b3.intent == Intent.TREATMENT.value and res_b3.entities.crop == "tomato",
        f"Intent: {res_b3.intent}, Crop: {res_b3.entities.crop}"
    )

    # 4. "tomato me ilaj kya h"
    res_b4 = route_multimodal_query(text="tomato me ilaj kya h")
    check(
        "Hinglish: 'tomato me ilaj kya h' -> intent=TREATMENT, crop='tomato'",
        res_b4.intent == Intent.TREATMENT.value and res_b4.entities.crop == "tomato",
        f"Intent: {res_b4.intent}, Crop: {res_b4.entities.crop}"
    )

    # -------------------------------------------------------------------------
    # SECTION C: Broken / Informal & Hinglish Agricultural Language
    # -------------------------------------------------------------------------
    print("\n--- SECTION C: Broken / Informal & Hinglish Agricultural Phrasing ---")

    # 1. "plant not good what do"
    res_c1 = route_multimodal_query(text="plant not good what do")
    check(
        "Informal: 'plant not good what do' -> intent=TREATMENT",
        res_c1.intent == Intent.TREATMENT.value,
        f"Intent: {res_c1.intent}"
    )

    # 2. "leaves bad what happened"
    res_c2 = route_multimodal_query(text="leaves bad what happened")
    check(
        "Informal: 'leaves bad what happened' -> intent=DIAGNOSE_PLANT, part='leaf'",
        res_c2.intent == Intent.DIAGNOSE_PLANT.value and res_c2.entities.plant_part == "leaf",
        f"Intent: {res_c2.intent}, Part: {res_c2.entities.plant_part}"
    )

    # 3. "tomato patte sukh rhe"
    res_c3 = route_multimodal_query(text="tomato patte sukh rhe")
    check(
        "Hinglish: 'tomato patte sukh rhe' -> crop='tomato', part='leaf', symptoms=['drying']",
        res_c3.entities.crop == "tomato" and res_c3.entities.plant_part == "leaf" and "drying" in res_c3.entities.symptoms,
        f"Crop: {res_c3.entities.crop}, Part: {res_c3.entities.plant_part}, Symptoms: {res_c3.entities.symptoms}"
    )

    # 4. "kya karu plant kharab"
    res_c4 = route_multimodal_query(text="kya karu plant kharab")
    check(
        "Hinglish: 'kya karu plant kharab' -> intent=TREATMENT",
        res_c4.intent == Intent.TREATMENT.value,
        f"Intent: {res_c4.intent}"
    )

    # -------------------------------------------------------------------------
    # SECTION D: Ambiguity Detection & Clarification Handling
    # -------------------------------------------------------------------------
    print("\n--- SECTION D: Ambiguity & Insufficient Information Handling ---")

    # 1. "what do" without image -> AMBIGUOUS with needs_clarification=True
    res_d1 = route_multimodal_query(text="what do")
    check(
        "Ambiguity: 'what do' (no image) -> AMBIGUOUS & needs_clarification=True",
        res_d1.intent == Intent.AMBIGUOUS.value and res_d1.needs_clarification is True,
        f"Intent: {res_d1.intent}, Needs Clarification: {res_d1.needs_clarification}"
    )

    # 2. "plant problem" without image -> AMBIGUOUS with needs_clarification=True
    res_d2 = route_multimodal_query(text="plant problem")
    check(
        "Ambiguity: 'plant problem' (no image) -> AMBIGUOUS & needs_clarification=True",
        res_d2.intent == Intent.AMBIGUOUS.value and res_d2.needs_clarification is True,
        f"Intent: {res_d2.intent}, Needs Clarification: {res_d2.needs_clarification}"
    )

    # 3. "what happened" with visual context -> DIAGNOSE_PLANT
    mock_vis = {"crop": "tomato", "disease": "tomato__early_blight", "status": "diseased"}
    res_d3 = route_multimodal_query(text="what happened", visual_result=mock_vis)
    check(
        "Contextual: 'what happened' (with visual result) -> DIAGNOSE_PLANT",
        res_d3.intent == Intent.DIAGNOSE_PLANT.value and res_d3.needs_clarification is False,
        f"Intent: {res_d3.intent}, Needs Clarification: {res_d3.needs_clarification}"
    )

    # 4. "what happened" without image/context -> INSUFFICIENT_INFO / AMBIGUOUS with clarification
    res_d4 = route_multimodal_query(text="")
    check(
        "Empty/Missing Query (no image) -> INSUFFICIENT_INFO & needs_clarification=True",
        res_d4.intent == Intent.INSUFFICIENT_INFORMATION.value and res_d4.needs_clarification is True,
        f"Intent: {res_d4.intent}, Needs Clarification: {res_d4.needs_clarification}"
    )

    # -------------------------------------------------------------------------
    # SECTION E: Structured Entity Extraction
    # -------------------------------------------------------------------------
    print("\n--- SECTION E: Structured Entity Extraction ---")

    # 1. "tomato leaves are yellow"
    res_e1 = route_multimodal_query(text="tomato leaves are yellow")
    check(
        "Entity Extraction: 'tomato leaves are yellow' -> crop='tomato', part='leaf', symptoms=['yellowing']",
        res_e1.entities.crop == "tomato" and res_e1.entities.plant_part == "leaf" and "yellowing" in res_e1.entities.symptoms,
        f"Entities: {res_e1.entities.to_dict()}"
    )

    # 2. "tomato early blight"
    res_e2 = route_multimodal_query(text="what is tomato early blight")
    check(
        "Entity Extraction: 'what is tomato early blight' -> crop='tomato', disease='tomato__early_blight'",
        res_e2.entities.crop == "tomato" and res_e2.entities.disease == "tomato__early_blight",
        f"Entities: {res_e2.entities.to_dict()}"
    )

    # 3. "how to treat this"
    res_e3 = route_multimodal_query(text="how to treat this")
    check(
        "Entity Extraction: 'how to treat this' -> action='treatment', intent=TREATMENT",
        res_e3.entities.action == "treatment" and res_e3.intent == Intent.TREATMENT.value,
        f"Action: {res_e3.entities.action}, Intent: {res_e3.intent}"
    )

    # -------------------------------------------------------------------------
    # SECTION F: Context-Aware Visual Routing
    # -------------------------------------------------------------------------
    print("\n--- SECTION F: Context-Aware Visual Routing ---")

    # Given visual_result: tomato + early_blight
    sample_visual = {
        "crop": "tomato",
        "crop_confidence": 0.98,
        "status": "diseased",
        "disease": "tomato__early_blight",
        "disease_confidence": 0.91,
    }

    # Query 1: "what happened to my plant?" + visual
    res_f1 = route_multimodal_query(text="what happened to my plant?", visual_result=sample_visual)
    check(
        "Visual Context: 'what happened to my plant?' + (Tomato Early Blight) -> DIAGNOSE_PLANT & context preserved",
        res_f1.intent == Intent.DIAGNOSE_PLANT.value and res_f1.context.get("disease") == "tomato__early_blight",
        f"Intent: {res_f1.intent}, Context: {res_f1.context}"
    )

    # Query 2: "how do I treat this?" + visual
    res_f2 = route_multimodal_query(text="how do I treat this?", visual_result=sample_visual)
    check(
        "Visual Context: 'how do I treat this?' + (Tomato Early Blight) -> TREATMENT & context preserved",
        res_f2.intent == Intent.TREATMENT.value and res_f2.context.get("disease") == "tomato__early_blight" and res_f2.needs_rag is True,
        f"Intent: {res_f2.intent}, Context: {res_f2.context}"
    )

    # Query 3: "what plant is this?" + visual
    res_f3 = route_multimodal_query(text="what plant is this?", visual_result=sample_visual)
    check(
        "Visual Context: 'what plant is this?' -> IDENTIFY_CROP & target domain='plant_identification'",
        res_f3.intent == Intent.IDENTIFY_CROP.value and res_f3.target_knowledge_domain == "plant_identification",
        f"Intent: {res_f3.intent}, Domain: {res_f3.target_knowledge_domain}"
    )

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f"QUERY UNDERSTANDING TEST SUITE COMPLETE: {passed_tests}/{total_tests} TESTS PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 80)
    return 0 if passed_tests == total_tests else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
