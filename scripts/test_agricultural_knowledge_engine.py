"""
Comprehensive Test Suite for Agricultural Knowledge & Conversational Reasoning Engine
======================================================================================
Tests:
  Part A: Direct Knowledge Questions (Symptoms, Cause, Treatment, Prevention)
  Part B: Contextual & Anaphoric Follow-up Questions ("why?", "how to treat it?", "can it spread?", "will it come back?")
  Part C: Visual Inference + Conversational Question Integration
  Part D: Unknown / Unverified Knowledge Handling (Non-hallucination)
  Part E: Ambiguous & Insufficient Queries (Clarification requests)
  Part F: Healthy Specimen Queries (No disease treatments prescribed)
  Part G: Incompatible Disease Detection Protection
  Part H: Multi-Crop Pilot KB Coverage (Cucumber Downy Mildew, Soybean Rust, Garlic Rust, etc.)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from knowledge.assistant import AgriculturalAssistant
from knowledge.database import get_knowledge_base
from knowledge.schema import SourceTier


def run_knowledge_reasoning_test_suite():
    print("=" * 80)
    print("AGRICULTURAL KNOWLEDGE & CONVERSATIONAL REASONING ENGINE - TEST SUITE")
    print("=" * 80)

    kb = get_knowledge_base()
    assistant = AgriculturalAssistant(kb=kb)

    total_tests = 0
    passed_tests = 0

    def assert_test(name: str, condition: bool, details: str = ""):
        nonlocal total_tests, passed_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f" [PASS] {name}")
        else:
            print(f" [FAIL] {name}")
            if details:
                print(f"        Details: {details}")

    # =========================================================================
    # PART A: DIRECT KNOWLEDGE QUESTIONS
    # =========================================================================
    print("\n--- PART A: Direct Knowledge Questions ---")
    assistant.reset_session()

    # A1. Symptoms
    resp_a1 = assistant.answer_query("what are the symptoms of tomato early blight?")
    assert_test(
        "A1. Direct Symptoms Query",
        resp_a1.intent == "SYMPTOMS"
        and resp_a1.crop == "tomato"
        and resp_a1.disease == "tomato__early_blight"
        and "concentric rings" in resp_a1.text.lower()
        and len(resp_a1.sources) > 0,
        f"Intent: {resp_a1.intent}, Crop: {resp_a1.crop}, Sources: {len(resp_a1.sources)}",
    )

    # A2. Cause
    assistant.reset_session()
    resp_a2 = assistant.answer_query("why does early blight happen in tomato?")
    assert_test(
        "A2. Direct Cause Query",
        resp_a2.intent == "CAUSE"
        and "alternaria solani" in resp_a2.text.lower()
        and ("warm" in resp_a2.text.lower() or "humidity" in resp_a2.text.lower()),
        f"Text excerpt: {resp_a2.text[:120]}...",
    )

    # A3. Treatment / Management
    assistant.reset_session()
    resp_a3 = assistant.answer_query("how do I manage tomato early blight?")
    assert_test(
        "A3. Direct Treatment/Management Query",
        resp_a3.intent == "TREATMENT"
        and "management" in resp_a3.text.lower()
        and "sanitation" in resp_a3.text.lower()
        and len(resp_a3.sources) > 0,
        f"Sources count: {len(resp_a3.sources)}",
    )

    # A4. Prevention
    assistant.reset_session()
    resp_a4 = assistant.answer_query("how can I prevent early blight in tomato?")
    assert_test(
        "A4. Direct Prevention Query",
        resp_a4.intent == "PREVENTION"
        and ("crop rotation" in resp_a4.text.lower() or "resistant" in resp_a4.text.lower() or "drip" in resp_a4.text.lower()),
        f"Text excerpt: {resp_a4.text[:120]}...",
    )

    # =========================================================================
    # PART B: CONTEXTUAL & ANAPHORIC FOLLOW-UP QUESTIONS
    # =========================================================================
    print("\n--- PART B: Contextual & Anaphoric Follow-ups ---")
    assistant.reset_session()

    # Turn 1: Establish Context
    t1 = assistant.answer_query("What is wrong with my tomato? It has early blight symptoms.")
    assert_test("B1. Turn 1 Context Established", t1.disease == "tomato__early_blight")

    # Turn 2: Follow-up "Why?"
    t2 = assistant.answer_query("Why?")
    assert_test(
        "B2. Turn 2 'Why?' Anaphora Resolution",
        t2.disease == "tomato__early_blight"
        and t2.intent in ("CAUSE", "FOLLOW_UP")
        and ("alternaria solani" in t2.text.lower() or "fungal pathogen" in t2.text.lower()),
        f"Intent: {t2.intent}, Disease: {t2.disease}",
    )

    # Turn 3: Follow-up "How do I treat it?"
    t3 = assistant.answer_query("How do I treat it?")
    assert_test(
        "B3. Turn 3 'How do I treat it?' Anaphora Resolution",
        t3.disease == "tomato__early_blight"
        and ("cultural management" in t3.text.lower() or "management" in t3.text.lower()),
        f"Disease: {t3.disease}",
    )

    # Turn 4: Follow-up "Can it spread?"
    t4 = assistant.answer_query("Can it spread?")
    assert_test(
        "B4. Turn 4 'Can it spread?' Context & Transmission Facts",
        t4.disease == "tomato__early_blight"
        and ("wind" in t4.text.lower() or "rain" in t4.text.lower() or "spread" in t4.text.lower() or "splash" in t4.text.lower()),
        f"Text excerpt: {t4.text[:120]}...",
    )

    # Turn 5: Follow-up "Will it come back next year?"
    t5 = assistant.answer_query("Will it come back next year?")
    assert_test(
        "B5. Turn 5 'Will it come back?' Recurrence Facts",
        t5.disease == "tomato__early_blight"
        and ("debris" in t5.text.lower() or "overwinter" in t5.text.lower() or "soil" in t5.text.lower() or "survival" in t5.text.lower()),
        f"Text excerpt: {t5.text[:120]}...",
    )

    # =========================================================================
    # PART C: VISUAL INFERENCE + CONVERSATIONAL QUERY INTEGRATION
    # =========================================================================
    print("\n--- PART C: Visual Inference Integration ---")
    assistant.reset_session()

    visual_eb = {
        "crop": "tomato",
        "crop_confidence": 0.98,
        "status": "diseased",
        "disease": "tomato__early_blight",
        "disease_confidence": 0.93,
    }

    # C1. "what happened to my plant?" + Visual
    resp_c1 = assistant.answer_query("what happened to my plant?", visual_result=visual_eb)
    assert_test(
        "C1. Visual + 'what happened?' Diagnosis Explanation",
        resp_c1.crop == "tomato"
        and resp_c1.disease == "tomato__early_blight"
        and "early blight" in resp_c1.text.lower()
        and "93.0%" in resp_c1.text,
        f"Text: {resp_c1.text[:100]}...",
    )

    # C2. "what should I do?" + Context from previous visual
    resp_c2 = assistant.answer_query("what should I do?")
    assert_test(
        "C2. Contextual 'what should I do?' Management",
        resp_c2.disease == "tomato__early_blight"
        and "management" in resp_c2.text.lower(),
        f"Text: {resp_c2.text[:100]}...",
    )

    # C3. "what plant is this?" + Visual
    resp_c3 = assistant.answer_query("what plant is this?", visual_result=visual_eb)
    assert_test(
        "C3. Visual + 'what plant is this?' Crop ID Focus",
        resp_c3.crop == "tomato"
        and "tomato" in resp_c3.text.lower(),
        f"Text: {resp_c3.text[:100]}...",
    )

    # =========================================================================
    # PART D: UNKNOWN / UNVERIFIED KNOWLEDGE HANDLING (NO HALLUCINATION)
    # =========================================================================
    print("\n--- PART D: Unknown / Unverified Knowledge ---")
    assistant.reset_session()

    # D1. Unverified disease not in KB (e.g. apple black rot)
    resp_d1 = assistant.answer_query("what are the symptoms of apple black rot?")
    assert_test(
        "D1. Unverified Disease -> Explicit Missing Knowledge Notice",
        resp_d1.status == "unverified"
        and ("not yet present" in resp_d1.text.lower() or "verified" in resp_d1.text.lower())
        and not resp_d1.sources,
        f"Status: {resp_d1.status}, Text: {resp_d1.text[:100]}...",
    )

    # D2. Treatment requested without known disease
    assistant.reset_session()
    resp_d2 = assistant.answer_query("how do I treat dragonfruit cosmic blight?")
    assert_test(
        "D2. Unknown Condition for Treatment -> Clarification Request (No Hallucination)",
        resp_d2.needs_clarification
        and not resp_d2.sources,
        f"Status: {resp_d2.status}, Text: {resp_d2.text[:100]}...",
    )

    # =========================================================================
    # PART E: AMBIGUOUS & INSUFFICIENT QUERIES
    # =========================================================================
    print("\n--- PART E: Ambiguous & Insufficient Queries ---")
    assistant.reset_session()

    resp_e1 = assistant.answer_query("what do?")
    assert_test(
        "E1. Broken / Ambiguous Query 'what do?'",
        resp_e1.needs_clarification
        and "tell me what you want to know" in resp_e1.text.lower(),
        f"Text: {resp_e1.text}",
    )

    resp_e2 = assistant.answer_query("help plant problem")
    assert_test(
        "E2. Ambiguous Query 'help plant problem'",
        resp_e2.needs_clarification,
        f"Text: {resp_e2.text}",
    )

    # =========================================================================
    # PART F: HEALTHY SPECIMEN QUERIES (NO DISEASE TREATMENT)
    # =========================================================================
    print("\n--- PART F: Healthy Specimen Behavior ---")
    assistant.reset_session()

    visual_healthy = {
        "crop": "tomato",
        "crop_confidence": 0.99,
        "status": "healthy",
        "disease": None,
        "disease_confidence": 0.97,
    }

    resp_f = assistant.answer_query("what treatment does it need?", visual_result=visual_healthy)
    assert_test(
        "F1. Healthy Visual -> Explicit Healthy Notice & No Chemical Treatment",
        resp_f.status == "healthy"
        and "healthy" in resp_f.text.lower()
        and "treatment or chemical sprays are not needed" in resp_f.text.lower(),
        f"Text: {resp_f.text[:120]}...",
    )

    # =========================================================================
    # PART G: INCOMPATIBLE CROP-DISEASE DETECTION PROTECTION
    # =========================================================================
    print("\n--- PART G: Incompatible Disease Protection ---")
    assistant.reset_session()

    visual_incompatible = {
        "crop": "tomato",
        "crop_confidence": 0.95,
        "status": "diseased",
        "disease": "soybean__rust",
        "disease_confidence": 0.88,
        "incompatibility_flag": True,
    }

    resp_g = assistant.answer_query("how do I treat this?", visual_result=visual_incompatible)
    assert_test(
        "G1. Incompatible Crop-Disease Flagged & Rejected",
        resp_g.reasoning_rule == "RULE_3_INCOMPATIBLE_REJECTION"
        and resp_g.needs_clarification,
        f"Rule: {resp_g.reasoning_rule}",
    )

    # =========================================================================
    # PART H: PILOT KB DIVERSITY (MULTIPLE CROPS & DISEASES)
    # =========================================================================
    print("\n--- PART H: Multi-Crop Pilot KB Coverage ---")
    assistant.reset_session()

    # H1. Cucumber Downy Mildew
    resp_h1 = assistant.answer_query("how to prevent cucumber downy mildew?")
    assert_test(
        "H1. Cucumber Downy Mildew Prevention",
        resp_h1.disease == "cucumber__downy_mildew"
        and ("plant early" in resp_h1.text.lower() or "spore" in resp_h1.text.lower() or "downy mildew" in resp_h1.text.lower()),
        f"Text: {resp_h1.text[:100]}...",
    )

    # H2. Soybean Rust
    assistant.reset_session()
    resp_h2 = assistant.answer_query("what are the symptoms of soybean rust?")
    assert_test(
        "H2. Soybean Rust Symptoms",
        resp_h2.disease == "soybean__rust"
        and ("pustules" in resp_h2.text.lower() or "phakopsora" in resp_h2.text.lower()),
        f"Text: {resp_h2.text[:100]}...",
    )

    # H3. Garlic Rust
    assistant.reset_session()
    resp_h3 = assistant.answer_query("how do I manage garlic rust?")
    assert_test(
        "H3. Garlic Rust Management",
        resp_h3.disease == "garlic__rust"
        and ("puccinia allii" in resp_h3.text.lower() or "nitrogen" in resp_h3.text.lower() or "rotation" in resp_h3.text.lower()),
        f"Text: {resp_h3.text[:100]}...",
    )

    # H4. Ginger Sheath Blight
    assistant.reset_session()
    resp_h4 = assistant.answer_query("why does ginger sheath blight occur?")
    assert_test(
        "H4. Ginger Sheath Blight Cause",
        resp_h4.disease == "ginger__sheath_blight"
        and ("rhizoctonia solani" in resp_h4.text.lower() or "humidity" in resp_h4.text.lower() or "icar" in str(resp_h4.sources).lower()),
        f"Text: {resp_h4.text[:100]}...",
    )

    # H5. Banana Cordana Leaf Spot
    assistant.reset_session()
    resp_h5 = assistant.answer_query("what causes banana cordana leaf spot?")
    assert_test(
        "H5. Banana Cordana Leaf Spot Cause",
        resp_h5.disease == "banana__cordana_leaf_spot"
        and ("cordana" in resp_h5.text.lower() or "neocordana" in resp_h5.text.lower()),
        f"Text: {resp_h5.text[:100]}...",
    )

    # H6. Source Registry Verification
    assert_test(
        "H6. Source Registry Integrity (All pilot sources valid)",
        len(kb.sources) >= 12 and all(s.source_tier in (SourceTier.TIER_1, SourceTier.TIER_2) for s in kb.sources.values()),
        f"Sources registered: {len(kb.sources)}",
    )

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed_tests}/{total_tests} TESTS PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 80)

    if passed_tests == total_tests:
        print("ALL KNOWLEDGE & REASONING ENGINE TESTS PASSED PERFECTLY!")
        return 0
    else:
        print(f"WARNING: {total_tests - passed_tests} test(s) failed.")
        return 1


if __name__ == "__main__":
    code = run_knowledge_reasoning_test_suite()
    sys.exit(code)
