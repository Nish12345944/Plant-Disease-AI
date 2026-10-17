"""
Verification Suite: Complete Removal of Disease Insights Component
===================================================================
Tests Disease Identification, Treatment Requests, and Media-Only Uploads
across 3 crop/disease combinations:
1. Eggplant
2. Bell Pepper
3. Tomato

Verifies:
- Disease Insights is completely absent from API payload & visible_cards.
- No symptoms/causes headers or dumps in response text.
- Plant Identification card and Disease Detection card are preserved.
- Treatment & Cure card is preserved when requested/appropriate.
- Inference metadata and debug state are preserved.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from app.backend.main import app

client = TestClient(app)

CROPS_TO_TEST = [
    {
        "name": "Eggplant",
        "path": ROOT / "backups" / "model1_expansion_phase1_snapshot" / "data" / "processed" / "model1_expanded" / "train" / "eggplant" / "f19f552ce4_eggplant_phomopsis_fruit_rot_Bing_0015.jpg",
    },
    {
        "name": "Bell Pepper",
        "path": ROOT / "backups" / "model1_expansion_phase1_snapshot" / "data" / "processed" / "model1_expanded" / "train" / "bell_pepper" / "0075046e8b_bell_pepper_blossom_end_rot_Bing_0260.jpg",
    },
    {
        "name": "Tomato",
        "path": ROOT / "data" / "external" / "end_to_end_test" / "tomato" / "tomato_tomato_early_blight_0001.jpg",
    },
]


def send_chat(image_path: Path, text: str = None):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    data = {"input_type": "image"}
    if text is not None:
        data["text"] = text
    files = {"file": ("sample.jpg", img_bytes, "image/jpeg")}
    return client.post("/api/chat", data=data, files=files)


def extract_response_text(payload: dict) -> str:
    msg = payload.get("message")
    if isinstance(msg, dict):
        return msg.get("text", "") or msg.get("message", "")
    return str(msg or "")


def verify_no_disease_insights(payload: dict):
    # 1. No disease_insights key anywhere in payload, knowledge, or structured_data
    assert "disease_insights" not in payload, "disease_insights found in response payload root!"
    assert "insights_expanded" not in payload, "insights_expanded found in response payload root!"

    knowledge = payload.get("knowledge") or {}
    if isinstance(knowledge, dict):
        assert "disease_insights" not in knowledge, "disease_insights found in knowledge!"
        struct = knowledge.get("structured_data") or {}
        assert "disease_insights" not in struct, "disease_insights found in knowledge.structured_data!"

    # 2. visible_cards does not contain disease_insights or insights
    router = payload.get("router", {})
    vc = router.get("visible_cards", {})
    assert "disease_insights" not in vc, "disease_insights found in visible_cards!"
    assert "insights" not in vc, "insights found in visible_cards!"

    # 3. Text must not reintroduce symptoms or favorable conditions as long paragraph dumps
    text = extract_response_text(payload)
    forbidden_headers = [
        "**Key Diagnostic Symptoms:**",
        "**Causes & Favorable Environmental Conditions:**",
        "**Spread & Transmission:**",
        "**Overwintering & Recurrence:**",
    ]
    for h in forbidden_headers:
        assert h not in text, f"Forbidden header '{h}' was reintroduced in response text!"


def run_tests():
    print("=" * 70)
    print("TESTING COMPLETE REMOVAL OF DISEASE INSIGHTS SECTION")
    print("=" * 70)

    for crop_info in CROPS_TO_TEST:
        crop_name = crop_info["name"]
        img_path = crop_info["path"]
        assert img_path.exists(), f"Image path missing: {img_path}"
        print(f"\n--- Testing Crop: {crop_name} ---")

        # -------------------------------------------------------------
        # Scenario 1: Disease Identification ("What disease is this?")
        # -------------------------------------------------------------
        print(f"  [1] Disease Identification Request for {crop_name}...")
        resp1 = send_chat(img_path, text="What disease is this?")
        assert resp1.status_code == 200, f"Status code {resp1.status_code}: {resp1.text}"
        payload1 = resp1.json()

        verify_no_disease_insights(payload1)
        vc1 = payload1.get("router", {}).get("visible_cards", {})
        assert vc1.get("crop") is True, f"Crop card should be visible in mode 1, got {vc1}"
        assert vc1.get("disease") is True, f"Disease card should be visible in mode 1, got {vc1}"
        assert vc1.get("treatment") is False, f"Treatment card should be hidden in mode 1, got {vc1}"
        # Model predictions preserved
        assert payload1.get("model1") is not None, "model1 prediction missing!"
        assert payload1.get("model2") is not None, "model2 prediction missing!"
        assert payload1.get("model1", {}).get("confidence", 0) > 0, "model1 confidence missing!"
        print(f"      -> PASS: Mode 1 verified (Plant & Disease preserved, Disease Insights absent).")

        # -------------------------------------------------------------
        # Scenario 2: Treatment Request ("How do I treat this disease?")
        # -------------------------------------------------------------
        print(f"  [2] Treatment Guidance Request for {crop_name}...")
        resp2 = send_chat(img_path, text="How do I treat this disease?")
        assert resp2.status_code == 200, f"Status code {resp2.status_code}: {resp2.text}"
        payload2 = resp2.json()

        verify_no_disease_insights(payload2)
        vc2 = payload2.get("router", {}).get("visible_cards", {})
        assert vc2.get("crop") is True, f"Crop card should be visible in mode 3, got {vc2}"
        assert vc2.get("disease") is True, f"Disease card should be visible in mode 3, got {vc2}"
        assert vc2.get("treatment") is True, f"Treatment card should be visible in mode 3, got {vc2}"
        # Treatment details present
        assert payload2.get("treatment") is not None, "Treatment payload missing!"
        sources = payload2.get("knowledge_sources") or payload2.get("knowledge", {}).get("sources", [])
        assert len(sources) > 0, f"Sources missing from treatment response: {payload2.get('knowledge_sources')}"
        print(f"      -> PASS: Mode 3 verified (Treatment & Sources preserved, Disease Insights absent).")

        # -------------------------------------------------------------
        # Scenario 3: Media-Only Upload (Empty instruction)
        # -------------------------------------------------------------
        print(f"  [3] Media-Only Upload (No text) for {crop_name}...")
        resp3 = send_chat(img_path, text="")
        assert resp3.status_code == 200, f"Status code {resp3.status_code}: {resp3.text}"
        payload3 = resp3.json()

        verify_no_disease_insights(payload3)
        vc3 = payload3.get("router", {}).get("visible_cards", {})
        assert vc3.get("crop") is True, f"Crop card should be visible in mode 5, got {vc3}"
        assert vc3.get("disease") is True, f"Disease card should be visible in mode 5, got {vc3}"
        assert vc3.get("treatment") is True, f"Treatment card should be visible in mode 5, got {vc3}"
        # Model predictions preserved
        assert payload3.get("model1") is not None, "model1 prediction missing!"
        assert payload3.get("model2") is not None, "model2 prediction missing!"
        assert payload3.get("treatment") is not None, "treatment payload missing in media-only mode!"
        print(f"      -> PASS: Mode 5 verified (Combined cards preserved, Disease Insights absent).")

    print("\n" + "=" * 70)
    print("ALL 9 CROP/DISEASE COMBINATION CHECKS PASSED PERFECTLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
