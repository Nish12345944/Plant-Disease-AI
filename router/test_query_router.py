"""Tests for the Query Understanding / Intent Router.

Run:
    python router/test_query_router.py
    python -m router.test_query_router   (from project root)
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from router.query_router import route_query, route_multimodal_query
from router.taxonomy import Intent

# (query, expected_legacy_intent, expected_official_intent)
TEST_CASES = [
    ("What plant is this?", "plant_identification", "IDENTIFY_CROP"),
    ("What plant is this and what disease does it have?", "disease_detection", "IDENTIFY_DISEASE"),
    ("How do I treat this disease?", "treatment_information", "TREATMENT"),
    ("Tell me about tomato plants.", "general_plant_information", "GENERAL_PLANT_INFO"),
    ("Hello", "unknown", "AMBIGUOUS"),
    ("Identify this flower for me", "plant_identification", "IDENTIFY_CROP"),
    ("Which crop is shown in this image?", "plant_identification", "IDENTIFY_CROP"),
    ("What disease does my cucumber have?", "disease_detection", "IDENTIFY_DISEASE"),
    ("Is this leaf healthy or diseased?", "disease_detection", "CHECK_HEALTH"),
    ("My tomato leaves have spots, what infection is this?", "disease_detection", "IDENTIFY_DISEASE"),
    ("What pesticide should I spray for powdery mildew?", "treatment_information", "TREATMENT"),
    ("How to cure bacterial wilt in tomato?", "treatment_information", "TREATMENT"),
    ("Give me a remedy for leaf rust", "treatment_information", "TREATMENT"),
    ("How to grow roses at home?", "general_plant_information", "GENERAL_PLANT_INFO"),
    ("What fertilizer is best for wheat?", "general_plant_information", "GENERAL_PLANT_INFO"),
    ("Tell me about the uses of aloe vera", "general_plant_information", "GENERAL_PLANT_INFO"),
    ("Hi there, good morning", "unknown", "AMBIGUOUS"),
    ("", "unknown", "INSUFFICIENT_INFO"),
]


def run_tests() -> int:
    passed = 0
    for i, (query, exp_legacy, exp_official) in enumerate(TEST_CASES, 1):
        got = route_query(query)
        legacy_ok = got["intent"] == exp_legacy
        official_ok = got["official_intent"] == exp_official
        ok = legacy_ok and official_ok
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] Test {i:02d}: {query!r} -> Legacy: {got['intent']} (exp {exp_legacy}), Official: {got['official_intent']} (exp {exp_official})")
    
    total = len(TEST_CASES)
    print(f"\n{passed}/{total} tests passed.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(run_tests())
