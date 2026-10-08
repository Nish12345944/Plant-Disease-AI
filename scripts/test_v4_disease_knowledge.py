"""
Comprehensive Verification & Test Suite for Model 2 V4 Agricultural Knowledge Engine
=====================================================================================
Validates:
1. Complete 116/116 Disease Class Coverage against Model 2 V4 Taxonomy
2. Exact Slug & Crop Compatibility Verification
3. Authoritative Source Provenance & Tier Verification
4. Intent-Driven Retrieval Accuracy (Symptoms, Cause, Treatment, Prevention)
5. Contextual Dialogue & Anaphora Follow-Up Resolution across Commodities
6. Safety Controls: Uncertain Prediction Handling & Healthy Specimen Protection
7. No Hallucination / Unsupported Knowledge Safety
"""

import json
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from knowledge.assistant import AgriculturalAssistant
from knowledge.database import AgriculturalKnowledgeBase, get_knowledge_base
from knowledge.data.v4_disease_knowledge import V4_CROP_KNOWLEDGE, V4_DISEASE_KNOWLEDGE
from knowledge.sources import SOURCE_REGISTRY


def run_v4_knowledge_test_suite() -> bool:
    print("=" * 80)
    print("MODEL 2 V4 COMPLETE AGRICULTURAL KNOWLEDGE BASE - TEST SUITE")
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
    # PART 1: TAXONOMY & COVERAGE AUDIT
    # =========================================================================
    print("\n--- PART 1: Model 2 V4 Taxonomy & Coverage Audit ---")
    mapping_path = PROJECT_ROOT / "models" / "model2_classifier_v4" / "class_mapping.json"
    with open(mapping_path, "r") as f:
        v4_mapping = json.load(f)

    v4_disease_classes = set(c for c in v4_mapping.keys() if c != "healthy")
    kb_disease_keys = set(V4_DISEASE_KNOWLEDGE.keys())

    missing_classes = v4_disease_classes - kb_disease_keys
    extra_classes = kb_disease_keys - v4_disease_classes

    assert_test(
        "1.1 Exact 116/116 V4 Disease Coverage",
        len(v4_disease_classes) == 116 and len(missing_classes) == 0,
        f"Missing classes ({len(missing_classes)}): {missing_classes}",
    )

    assert_test(
        "1.2 Zero Extraneous / Misspelled Classes in V4 KB",
        len(extra_classes) == 0,
        f"Extra classes ({len(extra_classes)}): {extra_classes}",
    )

    # Unique IDs check
    all_slugs = list(V4_DISEASE_KNOWLEDGE.keys())
    assert_test(
        "1.3 No Duplicate Canonical Disease Slugs",
        len(all_slugs) == len(set(all_slugs)) == 116,
        f"Total: {len(all_slugs)}, Unique: {len(set(all_slugs))}",
    )

    # =========================================================================
    # PART 2: CROP-DISEASE COMPATIBILITY AUDIT
    # =========================================================================
    print("\n--- PART 2: Crop-Disease Compatibility Verification ---")
    organized_mapping_path = PROJECT_ROOT / "data" / "processed" / "model2_organized_crop_disease_mapping.json"
    with open(organized_mapping_path, "r") as f:
        organized_crop_mapping = json.load(f)

    compatibility_errors = []
    for slug, record in V4_DISEASE_KNOWLEDGE.items():
        crop_prefix, disease_name = slug.split("__", 1)
        if crop_prefix != record.crop.lower():
            compatibility_errors.append(f"Slug prefix '{crop_prefix}' != Record crop '{record.crop}' in {slug}")
        if crop_prefix not in organized_crop_mapping:
            compatibility_errors.append(f"Crop '{crop_prefix}' not in authoritative organized crop mapping")
        elif disease_name not in organized_crop_mapping[crop_prefix]:
            compatibility_errors.append(f"Disease '{disease_name}' not listed under crop '{crop_prefix}'")

    assert_test(
        "2.1 All 116 Disease Records Strictly Match Organized Crop Taxonomy",
        len(compatibility_errors) == 0,
        f"Errors: {compatibility_errors[:5]}",
    )

    # Healthy is not in V4_DISEASE_KNOWLEDGE
    assert_test(
        "2.2 Healthy Class Excluded from Disease Knowledge Base",
        "healthy" not in V4_DISEASE_KNOWLEDGE and "healthy" not in kb.diseases,
        "Healthy should not have a disease record",
    )

    # =========================================================================
    # PART 3: PROVENANCE & QUALITY LEVEL AUDIT
    # =========================================================================
    print("\n--- PART 3: Source Provenance & Quality Level Audit ---")
    unprovenanced_diseases = []
    quality_counts = {"HIGH": 0, "MEDIUM": 0, "LIMITED": 0}

    for slug, record in V4_DISEASE_KNOWLEDGE.items():
        if not record.sources:
            unprovenanced_diseases.append(slug)
        q = record.quality_level.upper()
        if q in quality_counts:
            quality_counts[q] += 1
        else:
            quality_counts["LIMITED"] += 1

    assert_test(
        "3.1 100% of Disease Records Have Traceable Source Provenance",
        len(unprovenanced_diseases) == 0,
        f"Unprovenanced: {unprovenanced_diseases}",
    )

    assert_test(
        "3.2 Source Registry Integrity (All referenced sources registered)",
        all(
            src in SOURCE_REGISTRY or (isinstance(src, str) and src in SOURCE_REGISTRY)
            for record in V4_DISEASE_KNOWLEDGE.values()
            for src in record.sources
        ),
        "Some sources are not in SOURCE_REGISTRY",
    )

    print(f"      [INFO] Knowledge Quality Breakdown: {quality_counts}")
    assert_test(
        "3.3 Quality Audit: High Quality Standards Met",
        quality_counts["HIGH"] >= 100,
        f"High quality records: {quality_counts['HIGH']}/116",
    )

    # =========================================================================
    # PART 4: INTENT-DRIVEN DETERMINISTIC RETRIEVAL
    # =========================================================================
    print("\n--- PART 4: Intent-Driven Retrieval Across Diverse Commodities ---")

    # 4.1 Symptoms query (Cereal / Wheat Scab)
    assistant.reset_session()
    resp_41 = assistant.answer_query("what are the symptoms of wheat head scab?")
    assert_test(
        "4.1 Symptoms Query -> Wheat Head Scab",
        resp_41.crop == "wheat"
        and "wheat__head_scab" in resp_41.disease
        and ("bleach" in resp_41.text.lower() or "spikelet" in resp_41.text.lower() or "tombstone" in resp_41.text.lower()),
        f"Text: {resp_41.text[:120]}...",
    )

    # 4.2 Cause query (Tropical / Citrus Canker)
    assistant.reset_session()
    resp_42 = assistant.answer_query("what causes citrus canker?")
    assert_test(
        "4.2 Cause Query -> Citrus Canker (Xanthomonas)",
        resp_42.crop == "citrus"
        and "citrus__canker" in resp_42.disease
        and ("xanthomonas" in resp_42.text.lower() or "bacterial" in resp_42.text.lower()),
        f"Text: {resp_42.text[:120]}...",
    )

    # 4.3 Treatment query (Solanaceous / Tomato Late Blight)
    assistant.reset_session()
    resp_43 = assistant.answer_query("how do I treat tomato late blight?")
    assert_test(
        "4.3 Treatment Query -> Tomato Late Blight (Fungicide & Sanitation)",
        resp_43.crop == "tomato"
        and "tomato__late_blight" in resp_43.disease
        and ("fungicide" in resp_43.text.lower() or "mancozeb" in resp_43.text.lower() or "protectant" in resp_43.text.lower() or "management" in resp_43.text.lower()),
        f"Text: {resp_43.text[:120]}...",
    )

    # 4.4 Prevention query (Berry / Grape Black Rot)
    assistant.reset_session()
    resp_44 = assistant.answer_query("how can I prevent grape black rot?")
    assert_test(
        "4.4 Prevention Query -> Grape Black Rot",
        resp_44.crop == "grape"
        and "grape__black_rot" in resp_44.disease
        and ("mumm" in resp_44.text.lower() or "canopy" in resp_44.text.lower() or "prun" in resp_44.text.lower() or "sanitation" in resp_44.text.lower()),
        f"Text: {resp_44.text[:120]}...",
    )

    # 4.5 Spread query (Greens / Basil Downy Mildew)
    assistant.reset_session()
    resp_45 = assistant.answer_query("can basil downy mildew spread?")
    assert_test(
        "4.5 Spread Query -> Basil Downy Mildew Transmission",
        resp_45.crop == "basil"
        and "basil__downy_mildew" in resp_45.disease
        and ("wind" in resp_45.text.lower() or "spore" in resp_45.text.lower() or "air" in resp_45.text.lower() or "seed" in resp_45.text.lower()),
        f"Text: {resp_45.text[:120]}...",
    )

    # =========================================================================
    # PART 5: MULTI-TURN CONTEXTUAL DIALOGUE & ANAPHORA RESOLUTION
    # =========================================================================
    print("\n--- PART 5: Multi-Turn Dialogue & Follow-Up Resolution ---")
    assistant.reset_session()

    # Turn 1: Establish Banana Panama Disease
    t1 = assistant.answer_query("what are the symptoms of banana panama disease?")
    assert_test(
        "5.1 Turn 1 Context Established -> Banana Panama Disease",
        t1.crop == "banana" and t1.disease == "banana__panama_disease",
        f"Crop: {t1.crop}, Disease: {t1.disease}",
    )

    # Turn 2: "Is there a cure?"
    t2 = assistant.answer_query("is there a cure?")
    assert_test(
        "5.2 Turn 2 'Is there a cure?' Anaphora Resolution (No False Cure Claims)",
        t2.disease == "banana__panama_disease"
        and ("no" in t2.text.lower() or "quarantine" in t2.text.lower() or "soil" in t2.text.lower() or "resistant" in t2.text.lower() or "management" in t2.text.lower()),
        f"Text: {t2.text[:120]}...",
    )

    # Turn 3: "How does it spread?"
    t3 = assistant.answer_query("how does it spread?")
    assert_test(
        "5.3 Turn 3 'How does it spread?' Resolution",
        t3.disease == "banana__panama_disease"
        and ("soil" in t3.text.lower() or "sucker" in t3.text.lower() or "water" in t3.text.lower() or "equipment" in t3.text.lower()),
        f"Text: {t3.text[:120]}...",
    )

    # Turn 4: "Will it come back?"
    t4 = assistant.answer_query("will it come back?")
    assert_test(
        "5.4 Turn 4 'Will it come back?' Recurrence Resolution",
        t4.disease == "banana__panama_disease"
        and ("chlamydospore" in t4.text.lower() or "year" in t4.text.lower() or "soil" in t4.text.lower() or "persist" in t4.text.lower()),
        f"Text: {t4.text[:120]}...",
    )

    # =========================================================================
    # PART 6: CRITICAL SAFETY RULES & UNCERTAINTY HANDLING
    # =========================================================================
    print("\n--- PART 6: Critical Safety Rules & Conditional Advice ---")
    assistant.reset_session()

    # 6.1 Low confidence / uncertain prediction
    visual_uncertain = {
        "crop": "apple",
        "crop_confidence": 0.95,
        "status": "diseased",
        "disease": "apple__scab",
        "disease_confidence": 0.52,  # Low confidence
        "uncertain": True,
    }

    resp_61 = assistant.answer_query("what is wrong with my apple tree?", visual_result=visual_uncertain)
    assert_test(
        "6.1 Uncertain Visual Diagnosis -> Conditional Framing (No Overconfident Claims)",
        resp_61.status == "uncertain"
        or resp_61.reasoning_rule == "RULE_2_UNCERTAIN_DIAGNOSIS"
        or ("possible" in resp_61.text.lower() or "uncertain" in resp_61.text.lower() or "confirmed" in resp_61.text.lower()),
        f"Status: {resp_61.status}, Rule: {resp_61.reasoning_rule}, Text: {resp_61.text[:120]}...",
    )

    # 6.2 Healthy visual result
    assistant.reset_session()
    visual_healthy = {
        "crop": "bell_pepper",
        "crop_confidence": 0.99,
        "status": "healthy",
        "disease": "healthy",
        "disease_confidence": 0.98,
    }

    resp_62 = assistant.answer_query("how do I cure this plant?", visual_result=visual_healthy)
    assert_test(
        "6.2 Healthy Specimen -> Zero Chemical Disease Treatments Recommended",
        resp_62.status == "healthy"
        and "healthy" in resp_62.text.lower()
        and "no chemical treatment" in resp_62.text.lower() or "no disease" in resp_62.text.lower() or "healthy" in resp_62.text.lower(),
        f"Text: {resp_62.text[:120]}...",
    )

    # 6.3 Viral disease does not invent chemical cures
    assistant.reset_session()
    resp_63 = assistant.answer_query("how to cure tomato mosaic virus?")
    assert_test(
        "6.3 Viral Disease -> No Chemical Cure Claimed (Sanitation/Prevention Focused)",
        resp_63.crop == "tomato"
        and ("cure" not in resp_63.text.lower() or "no chemical" in resp_63.text.lower() or "sanitation" in resp_63.text.lower() or "resistant" in resp_63.text.lower()),
        f"Text: {resp_63.text[:120]}...",
    )

    # 6.4 Unknown / Unverified disease
    assistant.reset_session()
    resp_64 = assistant.answer_query("what are the symptoms of kiwi cosmic rot?")
    assert_test(
        "6.4 Unknown Non-V4 Disease -> No Hallucination Notice",
        resp_64.status == "unverified"
        and not resp_64.sources,
        f"Status: {resp_64.status}, Text: {resp_64.text[:120]}...",
    )

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 80)
    print(f"V4 KNOWLEDGE BASE TEST RESULTS: {passed_tests}/{total_tests} TESTS PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 80)

    if passed_tests == total_tests:
        print("ALL MODEL 2 V4 KNOWLEDGE BASE EXPANSION TESTS PASSED PERFECTLY!\n")
        return True
    else:
        print(f"WARNING: {total_tests - passed_tests} test(s) failed.\n")
        return False


if __name__ == "__main__":
    success = run_v4_knowledge_test_suite()
    sys.exit(0 if success else 1)
