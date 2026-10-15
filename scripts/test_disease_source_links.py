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
    dup_citations = format_source_citation(
        ["SRC_NCSTATE_BLUEBERRY_ANTHRACNOSE", "SRC_NCSTATE_BLUEBERRY_ANTHRACNOSE"],
        disease_slug="blueberry__anthracnose",
        crop="blueberry",
        disease="anthracnose",
    )
    assert_check("6.1 Deduplication prevents duplicate URLs in citations", len(dup_citations) == 2)

    fallback_citations = format_source_citation(
        ["SRC_USDA_ARS", "SRC_FAO_PLANT"],
        disease_slug="fictional_crop__fictional_disease",
        crop="fictional_crop",
        disease="fictional_disease",
    )
    assert_check("6.2 Unverified disease fallback marks sources as general", all(c.get("is_general") is True for c in fallback_citations))
    assert_check("6.3 Fallback sources clearly labeled in title or general flag", all("[General Reference]" in c.get("title", "") or c.get("is_general") for c in fallback_citations))

    # =========================================================================
    # TEST 7: Potato — Early Blight & Late Blight
    # =========================================================================
    print("\n--- Case 7: Potato — Early Blight & Late Blight ---")
    sources_pot_eb = get_sources_for_disease("potato__early_blight", crop="potato", disease="early_blight")
    assert_check("7.1 Potato Early Blight specific sources registered", len(sources_pot_eb) >= 1)
    uc_pot_eb = next((s for s in sources_pot_eb if "early-blight" in (s.url_or_doi or "")), None)
    assert_check("7.2 UC IPM Potato Early Blight source present", uc_pot_eb is not None)
    if uc_pot_eb:
        expected_eb_url = "https://ipm.ucanr.edu/agriculture/potato/early-blight/"
        assert_check("7.3 Potato Early Blight URL matches exactly", uc_pot_eb.url_or_doi == expected_eb_url, f"Got: {uc_pot_eb.url_or_doi}")
        assert_check("7.4 Potato Early Blight title matches destination article", "early blight" in uc_pot_eb.title.lower() and "potato" in uc_pot_eb.title.lower(), f"Got: {uc_pot_eb.title}")
        assert_check("7.5 Potato Early Blight marked specific (not general)", not uc_pot_eb.is_general)

    sources_pot_lb = get_sources_for_disease("potato__late_blight", crop="potato", disease="late_blight")
    assert_check("7.6 Potato Late Blight specific sources registered", len(sources_pot_lb) >= 1)
    uc_pot_lb = next((s for s in sources_pot_lb if "late-blight" in (s.url_or_doi or "")), None)
    assert_check("7.7 UC IPM Potato Late Blight source present", uc_pot_lb is not None)
    if uc_pot_lb:
        expected_lb_url = "https://ipm.ucanr.edu/agriculture/potato/late-blight/"
        assert_check("7.8 Potato Late Blight URL matches exactly", uc_pot_lb.url_or_doi == expected_lb_url, f"Got: {uc_pot_lb.url_or_doi}")
        assert_check("7.9 Potato Late Blight title matches destination article", "late blight" in uc_pot_lb.title.lower() and "potato" in uc_pot_lb.title.lower(), f"Got: {uc_pot_lb.title}")
        assert_check("7.10 Potato Late Blight marked specific", not uc_pot_lb.is_general)

    # Test via Assistant Query
    assistant.reset_session()
    resp_pot = assistant.answer_query("how do I identify and manage late blight on potato crops?")
    has_pot_lb = any(s.get("url") == "https://ipm.ucanr.edu/agriculture/potato/late-blight/" for s in resp_pot.sources)
    assert_check("7.11 Assistant citations contain verified UC IPM Potato Late Blight guide", has_pot_lb)

    # =========================================================================
    # TEST 8: Grape — Powdery Mildew
    # =========================================================================
    print("\n--- Case 8: Grape — Powdery Mildew ---")
    sources_grape_pm = get_sources_for_disease("grape__powdery_mildew", crop="grape", disease="powdery_mildew")
    assert_check("8.1 Grape Powdery Mildew specific sources registered", len(sources_grape_pm) >= 1)
    uc_grape = next((s for s in sources_grape_pm if "ipm.ucanr.edu" in (s.url_or_doi or "")), None)
    assert_check("8.2 UC IPM Grape Powdery Mildew source present", uc_grape is not None)
    if uc_grape:
        expected_grape_url = "https://ipm.ucanr.edu/agriculture/grape/powdery-mildew/"
        assert_check("8.3 Grape Powdery Mildew canonical URL matches", uc_grape.url_or_doi == expected_grape_url, f"Got: {uc_grape.url_or_doi}")
        assert_check("8.4 Grape Powdery Mildew title matches article", "powdery mildew" in uc_grape.title.lower() and "grape" in uc_grape.title.lower(), f"Got: {uc_grape.title}")
        assert_check("8.5 Grape Powdery Mildew marked specific", not uc_grape.is_general)

    ret_grape = retrieve_relevant_knowledge("treatment_information", crop="grape", disease="grape__powdery_mildew", kb=kb)
    has_grape_pm = any(s.get("url") == "https://ipm.ucanr.edu/agriculture/grape/powdery-mildew/" for s in ret_grape.get("citations", []))
    assert_check("8.6 Knowledge retrieval returns verified UC IPM Grape Powdery Mildew citation", has_grape_pm)

    # =========================================================================
    # TEST 9: Strawberry — Gray Mold (Botrytis Fruit Rot)
    # =========================================================================
    print("\n--- Case 9: Strawberry — Gray Mold ---")
    sources_straw = get_sources_for_disease("strawberry__gray_mold", crop="strawberry", disease="gray_mold")
    assert_check("9.1 Strawberry Gray Mold specific sources registered", len(sources_straw) >= 1)
    uc_straw = next((s for s in sources_straw if "strawberry/botrytis-fruit-rot" in (s.url_or_doi or "")), None)
    assert_check("9.2 UC IPM Strawberry Botrytis source present", uc_straw is not None)
    if uc_straw:
        expected_straw_url = "https://ipm.ucanr.edu/agriculture/strawberry/botrytis-fruit-rot/"
        assert_check("9.3 Strawberry Botrytis URL matches canonical article", uc_straw.url_or_doi == expected_straw_url, f"Got: {uc_straw.url_or_doi}")
        assert_check("9.4 Strawberry Gray Mold title matches article", "botrytis" in uc_straw.title.lower() or "gray mold" in uc_straw.title.lower(), f"Got: {uc_straw.title}")
        assert_check("9.5 Strawberry Gray Mold marked specific", not uc_straw.is_general)

    ret_straw = retrieve_relevant_knowledge("treatment_information", crop="strawberry", disease="strawberry__gray_mold", kb=kb)
    has_straw_gm = any(s.get("url") == "https://ipm.ucanr.edu/agriculture/strawberry/botrytis-fruit-rot/" for s in ret_straw.get("citations", []))
    assert_check("9.6 Knowledge retrieval returns verified UC IPM Strawberry Botrytis citation", has_straw_gm)

    # =========================================================================
    # TEST 10: Wheat — Rusts (Leaf, Stripe, Stem)
    # =========================================================================
    print("\n--- Case 10: Wheat — Rusts ---")
    sources_wheat_leaf = get_sources_for_disease("wheat__leaf_rust", crop="wheat", disease="leaf_rust")
    assert_check("10.1 Wheat Leaf Rust sources registered", len(sources_wheat_leaf) >= 1)
    usda_wheat_leaf = next((s for s in sources_wheat_leaf if "ars.usda.gov" in (s.url_or_doi or "") and "wheat-leaf-rust" in (s.url_or_doi or "")), None)
    assert_check("10.2 USDA ARS Wheat Leaf Rust source present", usda_wheat_leaf is not None)
    if usda_wheat_leaf:
        expected_usda_leaf = "https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/wheat-leaf-rust/"
        assert_check("10.3 USDA ARS Wheat Leaf Rust URL matches exactly", usda_wheat_leaf.url_or_doi == expected_usda_leaf, f"Got: {usda_wheat_leaf.url_or_doi}")
        assert_check("10.4 USDA ARS Wheat Leaf Rust title is specific", "wheat leaf rust" in usda_wheat_leaf.title.lower(), f"Got: {usda_wheat_leaf.title}")
        assert_check("10.5 Marked specific (not generic portal)", not usda_wheat_leaf.is_general)

    sources_wheat_stripe = get_sources_for_disease("wheat__stripe_rust", crop="wheat", disease="stripe_rust")
    assert_check("10.6 Wheat Stripe Rust sources registered", len(sources_wheat_stripe) >= 1)
    usda_wheat_stripe = next((s for s in sources_wheat_stripe if "wheat-stripe-rust" in (s.url_or_doi or "")), None)
    assert_check("10.7 USDA ARS Wheat Stripe Rust source present", usda_wheat_stripe is not None)
    if usda_wheat_stripe:
        expected_usda_stripe = "https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/wheat-stripe-rust/"
        assert_check("10.8 USDA ARS Wheat Stripe Rust URL matches", usda_wheat_stripe.url_or_doi == expected_usda_stripe, f"Got: {usda_wheat_stripe.url_or_doi}")

    sources_wheat_stem = get_sources_for_disease("wheat__stem_rust", crop="wheat", disease="stem_rust")
    assert_check("10.9 Wheat Stem Rust sources registered", len(sources_wheat_stem) >= 1)
    usda_wheat_stem = next((s for s in sources_wheat_stem if "wheat-stem-rust" in (s.url_or_doi or "")), None)
    assert_check("10.10 USDA ARS Wheat Stem Rust source present", usda_wheat_stem is not None)

    assistant.reset_session()
    resp_wheat = assistant.answer_query("how to identify and treat leaf rust in wheat?")
    has_wheat_rust = any("wheat-leaf-rust" in s.get("url", "") for s in resp_wheat.sources)
    assert_check("10.11 Assistant citations contain verified USDA ARS Wheat Leaf Rust guide", has_wheat_rust)

    # =========================================================================
    # TEST 11: Institutional Homepage Isolation & Generic Rejection
    # =========================================================================
    print("\n--- Case 11: Institutional Homepage Isolation & Generic Rejection ---")
    # Even if d_rec has generic institutional sources, they MUST NOT be presented as specific articles
    generic_test_citations = format_source_citation(
        ["SRC_USDA_ARS", "SRC_UC_IPM", "SRC_PURDUE_EXT", "SRC_CORNELL_EXT", "SRC_CIMMYT"],
        disease_slug="potato__early_blight",
        crop="potato",
        disease="early_blight",
    )
    # Since potato early blight has a verified specific source (UC IPM early blight),
    # the generic institutional sources must NOT displace it, and any generic source returned
    # must have is_general=True
    assert_check("11.1 Verified specific source takes priority", any("potato/early-blight" in c.get("url", "") for c in generic_test_citations))
    for c in generic_test_citations:
        if "potato/early-blight" not in c.get("url", ""):
            assert_check(f"11.2 Generic source '{c.get('source_id')}' labeled is_general=True", c.get("is_general") is True)
            assert_check(f"11.3 Generic source '{c.get('source_id')}' title has [General Reference]", "[General Reference]" in c.get("title", ""))

    # Pure fallback on unknown disease: all generic homepages must be marked general
    unknown_citations = format_source_citation(
        ["SRC_USDA_ARS", "SRC_UC_IPM", "SRC_PURDUE_EXT"],
        disease_slug="unknown_crop__unknown_disease",
        crop="unknown_crop",
        disease="unknown_disease",
    )
    assert_check("11.4 Unknown disease citations all flagged as is_general=True", all(c.get("is_general") is True for c in unknown_citations))
    assert_check("11.5 Unknown disease citations all titled [General Reference]", all("[General Reference]" in c.get("title", "") for c in unknown_citations))

    # =========================================================================
    # TEST 12: Banana — Anthracnose, Cordana Leaf Spot & Panama Disease
    # =========================================================================
    print("\n--- Case 12: Banana — 3 Combinations (Anthracnose, Cordana, Panama Disease) ---")
    # 12A. Banana Anthracnose
    sources_ban_anth = get_sources_for_disease("banana__anthracnose", crop="banana", disease="anthracnose")
    assert_check("12.1 Banana Anthracnose specific source registered", len(sources_ban_anth) >= 1)
    ban_anth = next((s for s in sources_ban_anth if "promusa.org" in (s.url_or_doi or "") and "Anthracnose" in (s.url_or_doi or "")), None)
    assert_check("12.2 ProMusa Banana Anthracnose source present", ban_anth is not None)
    if ban_anth:
        expected_url = "https://www.promusa.org/Anthracnose"
        assert_check("12.3 Exact canonical ProMusa Anthracnose URL preserved", ban_anth.url_or_doi == expected_url, f"Got: {ban_anth.url_or_doi}")
        assert_check("12.4 Banana Anthracnose article title preserved", ban_anth.title == "Anthracnose", f"Got: {ban_anth.title}")
        assert_check("12.5 Banana Anthracnose marked specific (not general)", not ban_anth.is_general)

    # 12A-2. Regression test: generic FAO, UF/IFAS, CABI fallbacks DO NOT displace ProMusa
    cit_anth_fallback = format_source_citation(
        ["SRC_FAO_PLANT", "SRC_UF_IFAS", "SRC_CABI_CPC"],
        disease_slug="banana__anthracnose",
        crop="banana",
        disease="Anthracnose",
    )
    assert_check("12.5a ProMusa Anthracnose supersedes generic FAO/UF/CABI fallbacks", any(c.get("url") == "https://www.promusa.org/Anthracnose" for c in cit_anth_fallback))
    assert_check("12.5b Exact title 'Anthracnose' returned for ProMusa", any(c.get("title") == "Anthracnose" for c in cit_anth_fallback))
    assert_check("12.5c ProMusa specific source takes precedence as primary citation", cit_anth_fallback[0].get("source_id") == "SRC_PROMUSA_BANANA_ANTHRACNOSE")

    # 12B. Banana Cordana Leaf Spot & alias "Cordana"
    sources_ban_cord = get_sources_for_disease("banana__cordana_leaf_spot", crop="banana", disease="cordana_leaf_spot")
    assert_check("12.6 Banana Cordana specific source registered", len(sources_ban_cord) >= 1)
    ban_cord = next((s for s in sources_ban_cord if "promusa.org" in (s.url_or_doi or "") and "Cordana" in (s.url_or_doi or "")), None)
    assert_check("12.7 ProMusa Banana Cordana source present", ban_cord is not None)
    if ban_cord:
        expected_url = "https://www.promusa.org/Cordana+leaf+spot"
        assert_check("12.8 Exact canonical ProMusa Cordana URL preserved", ban_cord.url_or_doi == expected_url, f"Got: {ban_cord.url_or_doi}")
        assert_check("12.9 Banana Cordana article title preserved", "cordana" in ban_cord.title.lower(), f"Got: {ban_cord.title}")
    # Alias test: "Cordana" -> Cordana leaf spot
    alias_cord = get_sources_for_disease(crop="banana", disease="Cordana")
    assert_check("12.10 Alias 'Cordana' resolves to Cordana leaf spot source", any("Cordana+leaf+spot" in (s.url_or_doi or "") for s in alias_cord))

    # 12C. Banana Panama Disease & alias "Fusarium wilt of banana"
    sources_ban_pan = get_sources_for_disease("banana__panama_disease", crop="banana", disease="panama_disease")
    assert_check("12.11 Banana Panama Disease specific source registered", len(sources_ban_pan) >= 1)
    ban_pan = next((s for s in sources_ban_pan if "promusa.org" in (s.url_or_doi or "") and "Fusarium" in (s.url_or_doi or "")), None)
    assert_check("12.12 ProMusa Banana Panama Disease source present", ban_pan is not None)
    if ban_pan:
        expected_url = "https://www.promusa.org/Fusarium+wilt"
        assert_check("12.13 Exact canonical ProMusa Fusarium wilt URL preserved", ban_pan.url_or_doi == expected_url, f"Got: {ban_pan.url_or_doi}")
        assert_check("12.14 Banana Panama Disease article title preserved", "fusarium wilt" in ban_pan.title.lower(), f"Got: {ban_pan.title}")
    # Alias test: "Fusarium wilt of banana" -> Panama disease
    alias_pan = get_sources_for_disease(crop="banana", disease="Fusarium wilt of banana")
    assert_check("12.15 Alias 'Fusarium wilt of banana' resolves to Panama disease source", any("Fusarium+wilt" in (s.url_or_doi or "") for s in alias_pan))

    # =========================================================================
    # TEST 13: Grape — Black Rot & Downy Mildew
    # =========================================================================
    print("\n--- Case 13: Grape — 2 Combinations (Black Rot, Downy Mildew) ---")
    # 13A. Grape Black Rot
    sources_grape_br = get_sources_for_disease("grape__black_rot", crop="grape", disease="black_rot")
    assert_check("13.1 Grape Black Rot specific source registered", len(sources_grape_br) >= 1)
    has_uc_br = any("ipm.ucanr.edu/agriculture/grape/black-rot/" in (s.url_or_doi or "") for s in sources_grape_br)
    assert_check("13.2 UC IPM Grape Black Rot guide present with exact canonical URL", has_uc_br)
    br_source = next((s for s in sources_grape_br if "black-rot" in (s.url_or_doi or "")), None)
    if br_source:
        assert_check("13.3 Grape Black Rot title preserved", "black rot" in br_source.title.lower(), f"Got: {br_source.title}")
        assert_check("13.4 Grape Black Rot marked specific (not general)", not br_source.is_general)

    # 13B. Grape Downy Mildew
    sources_grape_dm = get_sources_for_disease("grape__downy_mildew", crop="grape", disease="downy_mildew")
    assert_check("13.5 Grape Downy Mildew specific source registered", len(sources_grape_dm) >= 1)
    has_uc_dm = any("ipm.ucanr.edu/agriculture/grape/downy-mildew/" in (s.url_or_doi or "") for s in sources_grape_dm)
    assert_check("13.6 UC IPM Grape Downy Mildew guide present with exact canonical URL", has_uc_dm)
    dm_source = next((s for s in sources_grape_dm if "downy-mildew" in (s.url_or_doi or "")), None)
    if dm_source:
        assert_check("13.7 Grape Downy Mildew title preserved", "downy mildew" in dm_source.title.lower(), f"Got: {dm_source.title}")

    # =========================================================================
    # TEST 14: Citrus — Citrus Canker & Citrus Greening (Huanglongbing)
    # =========================================================================
    print("\n--- Case 14: Citrus — 2 Combinations (Citrus Canker, Citrus Greening) ---")
    # 14A. Citrus Canker & alias
    sources_cit_canker = get_sources_for_disease("citrus__canker", crop="citrus", disease="canker")
    assert_check("14.1 Citrus Canker specific source registered", len(sources_cit_canker) >= 1)
    canker_src = next((s for s in sources_cit_canker if "citrus-canker" in (s.url_or_doi or "")), None)
    assert_check("14.2 UC IPM Citrus Canker guide present", canker_src is not None)
    if canker_src:
        expected_url = "https://ipm.ucanr.edu/agriculture/citrus/citrus-canker/"
        assert_check("14.3 Exact canonical UC IPM Citrus Canker URL preserved", canker_src.url_or_doi == expected_url, f"Got: {canker_src.url_or_doi}")
        assert_check("14.4 Citrus Canker title preserved", "citrus canker" in canker_src.title.lower(), f"Got: {canker_src.title}")
    # Alias test: "Citrus canker"
    alias_canker = get_sources_for_disease(crop="citrus", disease="Citrus canker")
    assert_check("14.5 Alias 'Citrus canker' resolves to Citrus canker source", any("citrus-canker" in (s.url_or_doi or "") for s in alias_canker))

    # 14B. Citrus Greening & aliases "Huanglongbing", "HLB"
    sources_cit_green = get_sources_for_disease("citrus__greening_disease", crop="citrus", disease="greening_disease")
    assert_check("14.6 Citrus Greening specific source registered", len(sources_cit_green) >= 1)
    green_src = next((s for s in sources_cit_green if "citrus-greening" in (s.url_or_doi or "")), None)
    assert_check("14.7 UC IPM Citrus Greening guide present", green_src is not None)
    if green_src:
        expected_url = "https://ipm.ucanr.edu/agriculture/citrus/citrus-greening/"
        assert_check("14.8 Exact canonical UC IPM Citrus Greening URL preserved", green_src.url_or_doi == expected_url, f"Got: {green_src.url_or_doi}")
        assert_check("14.9 Citrus Greening title mentions Huanglongbing", "greening" in green_src.title.lower() or "huanglongbing" in green_src.title.lower(), f"Got: {green_src.title}")
    # Alias tests
    alias_hlb = get_sources_for_disease(crop="citrus", disease="Huanglongbing (HLB)")
    assert_check("14.10 Alias 'Huanglongbing (HLB)' resolves to Citrus Greening source", any("citrus-greening" in (s.url_or_doi or "") for s in alias_hlb))
    alias_green = get_sources_for_disease(crop="citrus", disease="citrus greening")
    assert_check("14.11 Alias 'citrus greening' resolves to Citrus Greening source", any("citrus-greening" in (s.url_or_doi or "") for s in alias_green))

    # =========================================================================
    # TEST 15: Eggplant — Phomopsis Fruit Rot
    # =========================================================================
    print("\n--- Case 15: Eggplant — Phomopsis Fruit Rot ---")
    sources_egg_phom = get_sources_for_disease("eggplant__phomopsis_fruit_rot", crop="eggplant", disease="phomopsis_fruit_rot")
    assert_check("15.1 Eggplant Phomopsis specific source registered", len(sources_egg_phom) >= 1)
    egg_phom = next((s for s in sources_egg_phom if "plant-pest-advisory.rutgers.edu" in (s.url_or_doi or "") and "phomopsis-fruit-rot" in (s.url_or_doi or "")), None)
    assert_check("15.2 Rutgers NJAES Phomopsis source present", egg_phom is not None)
    if egg_phom:
        expected_url = "https://plant-pest-advisory.rutgers.edu/phomopsis-fruit-rot-in-eggplant/"
        assert_check("15.3 Exact canonical Rutgers Phomopsis URL preserved", egg_phom.url_or_doi == expected_url, f"Got: {egg_phom.url_or_doi}")
        assert_check("15.4 Eggplant Phomopsis title preserved", "phomopsis" in egg_phom.title.lower() and "eggplant" in egg_phom.title.lower(), f"Got: {egg_phom.title}")
        assert_check("15.5 Eggplant Phomopsis marked specific (not general)", not egg_phom.is_general)
    # Alias tests: "Phomopsis", "Phomopsis blight"
    alias_phom1 = get_sources_for_disease(crop="eggplant", disease="Phomopsis")
    assert_check("15.6 Alias 'Phomopsis' resolves to Phomopsis source", any("phomopsis-fruit-rot-in-eggplant" in (s.url_or_doi or "") for s in alias_phom1))
    alias_phom2 = get_sources_for_disease(crop="eggplant", disease="Phomopsis blight")
    assert_check("15.7 Alias 'Phomopsis blight' resolves to Phomopsis source", any("phomopsis-fruit-rot-in-eggplant" in (s.url_or_doi or "") for s in alias_phom2))

    # =========================================================================
    # TEST 16: Corn — Common Smut & Northern Corn Leaf Blight
    # =========================================================================
    print("\n--- Case 16: Corn — 2 Combinations (Common Smut, Northern Corn Leaf Blight) ---")
    # 16A. Corn Common Smut & aliases "Corn smut", "Common smut of corn"
    sources_corn_smut = get_sources_for_disease("corn__smut", crop="corn", disease="smut")
    assert_check("16.1 Corn Common Smut specific source registered", len(sources_corn_smut) >= 1)
    smut_src = next((s for s in sources_corn_smut if "ohioline.osu.edu" in (s.url_or_doi or "") and "plpath-cer-06" in (s.url_or_doi or "")), None)
    assert_check("16.2 Ohio State Extension Common Smut source present", smut_src is not None)
    if smut_src:
        expected_url = "https://ohioline.osu.edu/factsheet/plpath-cer-06"
        assert_check("16.3 Exact canonical Ohio State Common Smut URL preserved", smut_src.url_or_doi == expected_url, f"Got: {smut_src.url_or_doi}")
        assert_check("16.4 Common Smut title preserved", "common smut of corn" in smut_src.title.lower(), f"Got: {smut_src.title}")
        assert_check("16.5 Common Smut marked specific (not general)", not smut_src.is_general)
    # Alias tests
    alias_smut1 = get_sources_for_disease(crop="corn", disease="Corn smut")
    assert_check("16.6 Alias 'Corn smut' resolves to Common Smut source", any("plpath-cer-06" in (s.url_or_doi or "") for s in alias_smut1))
    alias_smut2 = get_sources_for_disease(crop="corn", disease="Common smut of corn")
    assert_check("16.7 Alias 'Common smut of corn' resolves to Common Smut source", any("plpath-cer-06" in (s.url_or_doi or "") for s in alias_smut2))

    # 16B. Corn Northern Corn Leaf Blight & alias
    sources_corn_nclb = get_sources_for_disease("corn__northern_leaf_blight", crop="corn", disease="northern_leaf_blight")
    assert_check("16.8 Corn Northern Leaf Blight specific source registered", len(sources_corn_nclb) >= 1)
    nclb_src = next((s for s in sources_corn_nclb if "ohioline.osu.edu" in (s.url_or_doi or "") and "plpath-cer-10" in (s.url_or_doi or "")), None)
    assert_check("16.9 Ohio State Extension NCLB source present", nclb_src is not None)
    if nclb_src:
        expected_url = "https://ohioline.osu.edu/factsheet/plpath-cer-10"
        assert_check("16.10 Exact canonical Ohio State NCLB URL preserved", nclb_src.url_or_doi == expected_url, f"Got: {nclb_src.url_or_doi}")
        assert_check("16.11 Northern Corn Leaf Blight title preserved", "northern corn leaf blight" in nclb_src.title.lower(), f"Got: {nclb_src.title}")
    # Alias test
    alias_nclb = get_sources_for_disease(crop="corn", disease="Northern corn leaf blight")
    assert_check("16.12 Alias 'Northern corn leaf blight' resolves to NCLB source", any("plpath-cer-10" in (s.url_or_doi or "") for s in alias_nclb))

    # =========================================================================
    # TEST 17: Wheat — Head Scab (Fusarium Head Blight) & Wheat Rust
    # =========================================================================
    print("\n--- Case 17: Wheat — 2 Combinations (Head Scab, Rust) ---")
    # 17A. Wheat Head Scab & aliases "Fusarium head blight", "Wheat head scab"
    sources_wheat_scab = get_sources_for_disease("wheat__head_scab", crop="wheat", disease="head_scab")
    assert_check("17.1 Wheat Head Scab specific sources registered", len(sources_wheat_scab) >= 1)
    unl_scab = next((s for s in sources_wheat_scab if "cropwatch.unl.edu" in (s.url_or_doi or "") and "fusarium-head-blight" in (s.url_or_doi or "")), None)
    assert_check("17.2 UNL CropWatch Head Scab guide present", unl_scab is not None)
    if unl_scab:
        expected_url = "https://cropwatch.unl.edu/plant-disease/wheat/fusarium-head-blight-scab/"
        assert_check("17.3 Exact canonical UNL Head Scab URL preserved", unl_scab.url_or_doi == expected_url, f"Got: {unl_scab.url_or_doi}")
        assert_check("17.4 Head Scab title preserved", "fusarium head blight" in unl_scab.title.lower() or "scab" in unl_scab.title.lower(), f"Got: {unl_scab.title}")
        assert_check("17.5 Head Scab marked specific (not general)", not unl_scab.is_general)
    # Alias tests
    alias_scab1 = get_sources_for_disease(crop="wheat", disease="Wheat head scab")
    assert_check("17.6 Alias 'Wheat head scab' resolves to Head Scab sources", any("fusarium-head-blight" in (s.url_or_doi or "") for s in alias_scab1))
    alias_scab2 = get_sources_for_disease(crop="wheat", disease="Fusarium head blight")
    assert_check("17.7 Alias 'Fusarium head blight' resolves to Head Scab sources", any("fusarium-head-blight" in (s.url_or_doi or "") for s in alias_scab2))

    # 17B. Wheat Rust & alias "Wheat rust"
    sources_wheat_rust = get_sources_for_disease("wheat__rust", crop="wheat", disease="rust")
    assert_check("17.8 Wheat Rust specific sources registered", len(sources_wheat_rust) >= 1)
    has_ars_rust = any("cereal-rusts" in (s.url_or_doi or "") for s in sources_wheat_rust)
    assert_check("17.9 USDA ARS Cereal Rusts guide present", has_ars_rust)
    alias_rust = get_sources_for_disease(crop="wheat", disease="Wheat rust")
    assert_check("17.10 Alias 'Wheat rust' resolves to Wheat Rust sources", any("cereal-rusts" in (s.url_or_doi or "") for s in alias_rust))

    # =========================================================================
    # TEST 18: Frontend Citations Independent URL Preservation
    # =========================================================================
    print("\n--- Case 18: Frontend Citations Independent URL Preservation ---")
    # Verify that multi-source results preserve each unique URL and own title
    grape_citations = format_source_citation(
        [],
        disease_slug="grape__black_rot",
        crop="grape",
        disease="black_rot",
    )
    assert_check("18.1 Multiple sources returned for Grape Black Rot", len(grape_citations) >= 2)
    urls = [c.get("url") for c in grape_citations]
    titles = [c.get("title") for c in grape_citations]
    assert_check("18.2 Each citation displays its own distinct title", len(set(titles)) == len(titles))
    assert_check("18.3 Each citation opens its own distinct URL", len(set(urls)) == len(urls))
    assert_check("18.4 No generic homepages used as replacement", not any(is_generic_portal_url(u) for u in urls))

    # =========================================================================
    # TEST 19: Full Runtime End-to-End Verification for All 12 Combinations
    # =========================================================================
    print("\n--- Case 19: Runtime End-to-End Verification for All 12 Combinations ---")
    assistant = AgriculturalAssistant()

    combos_12 = [
        ("banana", "banana__anthracnose", "Anthracnose", "https://www.promusa.org/Anthracnose"),
        ("banana", "banana__cordana_leaf_spot", "Cordana leaf spot", "https://www.promusa.org/Cordana+leaf+spot"),
        ("banana", "banana__panama_disease", "Panama disease", "https://www.promusa.org/Fusarium+wilt"),
        ("grape", "grape__black_rot", "Black rot", "https://ipm.ucanr.edu/agriculture/grape/black-rot/"),
        ("grape", "grape__downy_mildew", "Downy mildew", "https://ipm.ucanr.edu/agriculture/grape/downy-mildew/"),
        ("citrus", "citrus__canker", "Citrus canker", "https://ipm.ucanr.edu/agriculture/citrus/citrus-canker/"),
        ("citrus", "citrus__greening_disease", "Citrus greening", "https://ipm.ucanr.edu/agriculture/citrus/citrus-greening/"),
        ("eggplant", "eggplant__phomopsis_fruit_rot", "Phomopsis fruit rot", "https://plant-pest-advisory.rutgers.edu/phomopsis-fruit-rot-in-eggplant/"),
        ("corn", "corn__smut", "Common smut", "https://ohioline.osu.edu/factsheet/plpath-cer-06"),
        ("corn", "corn__northern_leaf_blight", "Northern corn leaf blight", "https://ohioline.osu.edu/factsheet/plpath-cer-10"),
        ("wheat", "wheat__head_scab", "Head scab", "https://cropwatch.unl.edu/plant-disease/wheat/fusarium-head-blight-scab/"),
        ("wheat", "wheat__rust", "Wheat rust", "https://www.ars.usda.gov/midwest-area/stpaul/cereal-disease-lab/docs/cereal-rusts/"),
    ]

    for idx, (c_name, d_slug, d_display, expected_url) in enumerate(combos_12, 1):
        vis = {
            "crop": c_name,
            "crop_confidence": 0.99,
            "disease": d_slug,
            "disease_name": d_display,
            "disease_confidence": 0.99,
            "status": "diseased",
        }
        res = assistant.answer_query(query=f"How do I manage {d_display} in my {c_name}?", visual_result=vis)
        assert_check(
            f"19.{idx} Runtime resolves {c_name} - {d_display} to {expected_url}",
            any(s.get("url") == expected_url for s in res.sources),
            f"Got sources: {[s.get('url') for s in res.sources]}"
        )
        assert_check(
            f"19.{idx}b Runtime marks source as specific (not general)",
            any((s.get("url") == expected_url and not s.get("is_general")) for s in res.sources)
        )

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
