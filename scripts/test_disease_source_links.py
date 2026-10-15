"""
Automated Test Suite for Disease-Specific Source Links in Plant Disease AI
========================================================================
Validates that:
1. Every source displayed under a disease diagnosis links directly to the
   verified, disease-relevant article/factsheet matching both crop and disease.
2. Canonical article titles and specific URLs are preserved through RAG retrieval,
   response building, and API serialization.
3. No generic university portals (e.g., NC State, Cornell, Purdue homepages)
   are returned when verified specific extension guides are available.
4. Validates required test cases:
   - Blueberry — Anthracnose
   - Bell Pepper — Blossom End Rot
   - Tomato — Early Blight
   - Cucumber — Downy Mildew / Powdery Mildew
"""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from knowledge.assistant import AgriculturalAssistant
from knowledge.database import get_knowledge_base
from knowledge.retrieval import retrieve_relevant_knowledge
from knowledge.sources import (
    DISEASE_SPECIFIC_SOURCES,
    format_source_citation,
    get_sources_for_disease,
)


def is_valid_url(url: str) -> bool:
    """Validate that the string is a well-formed http/https URL."""
    if not url or not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc) and len(parsed.path) > 1
    except Exception:
        return False


def is_generic_portal_url(url: str) -> bool:
    """Check if URL points to a generic university/extension portal or homepage rather than a specific article."""
    generic_patterns = [
        "content.ces.ncsu.edu/$",
        "ces.ncsu.edu/$",
        "extension.purdue.edu/programs/agriculture-natural-resources/$",
        "extension.purdue.edu/$",
        "vegetables.cornell.edu/pest-management/disease-factsheets/$",
        "vegetables.cornell.edu/$",
        "ipm.ucanr.edu/PMG/crops-agriculture.html",
        "ipm.ucanr.edu/$",
        "edis.ifas.ufl.edu/topic_plant_diseases",
        "edis.ifas.ufl.edu/$",
    ]
    norm = url.strip().rstrip("/") + "/"
    for pattern in generic_patterns:
        cleaned_pattern = pattern.replace("$", "")
        if cleaned_pattern in norm and len(norm.split(cleaned_pattern)[-1].strip("/")) == 0:
            return True
    return False


def test_disease_source_pipeline():
    print("=" * 80)
    print("DISEASE-SPECIFIC SOURCE LINKS VERIFICATION SUITE")
    print("=" * 80)

    kb = get_knowledge_base()
    assistant = AgriculturalAssistant(kb=kb)

    total_tests = 0
    passed_tests = 0

    def assert_check(name: str, condition: bool, details: str = ""):
        nonlocal total_tests, passed_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name}")
            if details:
                print(f"         {details}")

    # =========================================================================
    # TEST 1: Blueberry — Anthracnose
    # =========================================================================
    print("\n--- Case 1: Blueberry — Anthracnose ---")
    sources_bb = get_sources_for_disease("blueberry__anthracnose", crop="blueberry", disease="anthracnose")
    assert_check("1.1 Disease-specific sources registered", len(sources_bb) >= 1)
    
    ncsu_bb = next((s for s in sources_bb if "ncsu.edu" in (s.url_or_doi or "")), None)
    assert_check("1.2 NC State Blueberry Anthracnose source present", ncsu_bb is not None)
    if ncsu_bb:
        expected_url = "https://content.ces.ncsu.edu/anthracnose-fruit-rot-of-blueberries"
        assert_check("1.3 Canonical article URL matches exactly", ncsu_bb.url_or_doi == expected_url, f"Got: {ncsu_bb.url_or_doi}")
        assert_check("1.4 Title matches destination article", "anthracnose" in ncsu_bb.title.lower() and "blueberr" in ncsu_bb.title.lower(), f"Got: {ncsu_bb.title}")
        assert_check("1.5 URL is valid and non-generic", is_valid_url(ncsu_bb.url_or_doi) and not is_generic_portal_url(ncsu_bb.url_or_doi))

    # Test via Assistant Query
    assistant.reset_session()
    resp_bb = assistant.answer_query("how do I treat anthracnose on highbush blueberry?")
    assert_check("1.6 Assistant response returns knowledge sources", len(resp_bb.sources) >= 1)
    has_specific_bb = any(s.get("url") == "https://content.ces.ncsu.edu/anthracnose-fruit-rot-of-blueberries" for s in resp_bb.sources)
    assert_check("1.7 Assistant citations contain exact NC State Anthracnose guide", has_specific_bb)
    no_generic_bb = not any(is_generic_portal_url(s.get("url", "")) for s in resp_bb.sources)
    assert_check("1.8 No generic homepages/portals displayed for blueberry anthracnose", no_generic_bb)

    # =========================================================================
    # TEST 2: Bell Pepper — Blossom End Rot
    # =========================================================================
    print("\n--- Case 2: Bell Pepper — Blossom End Rot ---")
    sources_bp = get_sources_for_disease("bell_pepper__blossom_end_rot", crop="bell_pepper", disease="blossom_end_rot")
    assert_check("2.1 Disease-specific sources registered", len(sources_bp) >= 1)
    
    uga_bp = next((s for s in sources_bp if "uga.edu" in (s.url_or_doi or "")), None)
    assert_check("2.2 UGA Extension Blossom End Rot source present", uga_bp is not None)
    if uga_bp:
        expected_url = "https://extension.uga.edu/publications/detail.html?number=C938"
        assert_check("2.3 Canonical UGA article URL matches", uga_bp.url_or_doi == expected_url, f"Got: {uga_bp.url_or_doi}")
        assert_check("2.4 Title mentions blossom-end rot and pepper/tomato", "blossom-end rot" in uga_bp.title.lower(), f"Got: {uga_bp.title}")
        assert_check("2.5 URL is valid and non-generic", is_valid_url(uga_bp.url_or_doi) and not is_generic_portal_url(uga_bp.url_or_doi))

    # Test via Assistant Query
    assistant.reset_session()
    resp_bp = assistant.answer_query("what causes blossom end rot in bell peppers?")
    assert_check("2.6 Assistant response returns knowledge sources", len(resp_bp.sources) >= 1)
    has_specific_bp = any(s.get("url") == "https://extension.uga.edu/publications/detail.html?number=C938" for s in resp_bp.sources)
    assert_check("2.7 Assistant citations contain verified UGA Blossom End Rot guide", has_specific_bp)
    no_generic_bp = not any(is_generic_portal_url(s.get("url", "")) for s in resp_bp.sources)
    assert_check("2.8 No generic homepages displayed for bell pepper blossom end rot", no_generic_bp)

    # =========================================================================
    # TEST 3: Tomato — Early Blight
    # =========================================================================
    print("\n--- Case 3: Tomato — Early Blight ---")
    sources_tom = get_sources_for_disease("tomato__early_blight", crop="tomato", disease="early_blight")
    assert_check("3.1 Disease-specific sources registered", len(sources_tom) >= 1)
    
    ncsu_tom = next((s for s in sources_tom if "early-blight-of-tomato" in (s.url_or_doi or "")), None)
    assert_check("3.2 NC State Early Blight Tomato source present", ncsu_tom is not None)
    if ncsu_tom:
        expected_url = "https://content.ces.ncsu.edu/early-blight-of-tomato"
        assert_check("3.3 Canonical article URL matches", ncsu_tom.url_or_doi == expected_url, f"Got: {ncsu_tom.url_or_doi}")
        assert_check("3.4 Title matches 'Early Blight of Tomato'", "early blight of tomato" in ncsu_tom.title.lower(), f"Got: {ncsu_tom.title}")
        assert_check("3.5 URL is valid and non-generic", is_valid_url(ncsu_tom.url_or_doi) and not is_generic_portal_url(ncsu_tom.url_or_doi))

    # Test via Assistant Query
    assistant.reset_session()
    resp_tom = assistant.answer_query("how can I manage early blight on tomato plants?")
    assert_check("3.6 Assistant response returns knowledge sources", len(resp_tom.sources) >= 1)
    has_specific_tom = any(s.get("url") == "https://content.ces.ncsu.edu/early-blight-of-tomato" for s in resp_tom.sources)
    assert_check("3.7 Assistant citations contain exact Early Blight article", has_specific_tom)
    no_generic_tom = not any(is_generic_portal_url(s.get("url", "")) for s in resp_tom.sources)
    assert_check("3.8 No generic homepages displayed for tomato early blight", no_generic_tom)

    # =========================================================================
    # TEST 4: Cucumber — Supported Disease Diagnosis (Downy Mildew & Powdery Mildew)
    # =========================================================================
    print("\n--- Case 4: Cucumber — Supported Disease Diagnosis ---")
    # 4A. Cucumber Downy Mildew
    sources_cuc_dm = get_sources_for_disease("cucumber__downy_mildew", crop="cucumber", disease="downy_mildew")
    assert_check("4.1 Cucumber Downy Mildew source registered", len(sources_cuc_dm) >= 1)
    ncsu_cuc = next((s for s in sources_cuc_dm if "cucurbit-downy-mildew" in (s.url_or_doi or "")), None)
    assert_check("4.2 NC State Cucurbit Downy Mildew source present", ncsu_cuc is not None)
    if ncsu_cuc:
        expected_url = "https://content.ces.ncsu.edu/cucurbit-downy-mildew"
        assert_check("4.3 Canonical Downy Mildew article URL matches", ncsu_cuc.url_or_doi == expected_url, f"Got: {ncsu_cuc.url_or_doi}")
        assert_check("4.4 Title matches 'Cucurbit Downy Mildew'", "downy mildew" in ncsu_cuc.title.lower(), f"Got: {ncsu_cuc.title}")

    assistant.reset_session()
    resp_cuc_dm = assistant.answer_query("how do I stop downy mildew on my cucumbers?")
    assert_check("4.5 Assistant response returns cucumber downy mildew sources", len(resp_cuc_dm.sources) >= 1)
    has_specific_cuc = any(s.get("url") == "https://content.ces.ncsu.edu/cucurbit-downy-mildew" for s in resp_cuc_dm.sources)
    assert_check("4.6 Assistant citations contain Cucurbit Downy Mildew guide", has_specific_cuc)

    # 4B. Cucumber Powdery Mildew
    sources_cuc_pm = get_sources_for_disease("cucumber__powdery_mildew", crop="cucumber", disease="powdery_mildew")
    assert_check("4.7 Cucumber Powdery Mildew source registered", len(sources_cuc_pm) >= 1)
    uc_pm = next((s for s in sources_cuc_pm if "ipm.ucanr.edu" in (s.url_or_doi or "")), None)
    assert_check("4.8 UC IPM Cucurbit Powdery Mildew guide present", uc_pm is not None)
    if uc_pm:
        expected_url = "https://ipm.ucanr.edu/agriculture/cucurbits/powdery-mildew/"
        assert_check("4.9 Canonical UC IPM Cucurbits Powdery Mildew URL matches", uc_pm.url_or_doi == expected_url, f"Got: {uc_pm.url_or_doi}")

    assistant.reset_session()
    resp_cuc_pm = assistant.answer_query("how to prevent powdery mildew in cucumbers?")
    has_specific_pm = any(s.get("url") == "https://ipm.ucanr.edu/agriculture/cucurbits/powdery-mildew/" for s in resp_cuc_pm.sources)
    assert_check("4.10 Assistant citations contain exact UC IPM Powdery Mildew article", has_specific_pm)

    # =========================================================================
    # TEST 5: Multimodal Visual Evidence Integration
    # =========================================================================
    print("\n--- Case 5: Multimodal Visual Evidence Integration ---")
    assistant.reset_session()
    visual_ev = {
        "crop": "blueberry",
        "disease": "blueberry__anthracnose",
        "status": "diseased",
    }
    resp_vis = assistant.answer_query("what disease does this have and how do I treat it?", visual_result=visual_ev)
    assert_check("5.1 Visual query resolves to blueberry anthracnose", resp_vis.crop == "blueberry" and resp_vis.disease == "blueberry__anthracnose")
    has_vis_url = any(s.get("url") == "https://content.ces.ncsu.edu/anthracnose-fruit-rot-of-blueberries" for s in resp_vis.sources)
    assert_check("5.2 Multimodal diagnosis includes exact Blueberry Anthracnose source URL", has_vis_url)
    assert_check("5.3 Response text grounded in specific source title", "Anthracnose Fruit Rot of Blueberries" in resp_vis.text)

    # =========================================================================
    # TEST 6: Source Deduplication & Fallback General Reference Labeling
    # =========================================================================
    print("\n--- Case 6: Source Deduplication & General Reference Safety ---")
    # Multiple duplicate calls should deduplicate cleanly
    dup_citations = format_source_citation(
        ["SRC_NCSTATE_BLUEBERRY_ANTHRACNOSE", "SRC_NCSTATE_BLUEBERRY_ANTHRACNOSE"],
        disease_slug="blueberry__anthracnose",
        crop="blueberry",
        disease="anthracnose",
    )
    assert_check("6.1 Deduplication prevents duplicate URLs in citations", len(dup_citations) == 2)  # returns the 2 unique registered blueberry sources

    # Unknown / unverified disease fallback clearly marked as general reference
    fallback_citations = format_source_citation(
        ["SRC_USDA_ARS", "SRC_FAO_PLANT"],
        disease_slug="fictional_crop__fictional_disease",
        crop="fictional_crop",
        disease="fictional_disease",
    )
    assert_check("6.2 Unverified disease fallback marks sources as general", all(c.get("is_general") is True for c in fallback_citations))
    assert_check("6.3 Fallback sources clearly labeled in title or general flag", all("[General Reference]" in c.get("title", "") or c.get("is_general") for c in fallback_citations))

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed_tests}/{total_tests} TESTS PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 80)

    if passed_tests == total_tests:
        print("ALL DISEASE-SPECIFIC SOURCE LINK TESTS PASSED PERFECTLY!")
        return 0
    else:
        print(f"FAILED: {total_tests - passed_tests} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(test_disease_source_pipeline())
