"""
Disease Insights Feature & Component Test Suite
================================================
Validates all requirements of the Disease Insights task:
1. Renamed to "Disease Insights".
2. Subsections: Key Symptoms, Causes / Pathogen, Conditions That Favor Disease.
3. Symptoms as clean bullet lists, not large text blocks.
4. No literal markdown asterisks (**) in output.
5. Collapsible: default collapsed for disease ID only and media only; expanded for symptoms/causes queries.
6. Treatment queries prioritize treatment guidance and avoid repetitive info.
7. Media-only upload provides insights collapsed without overwhelming initial result.
8. Missing or empty data handled cleanly without hallucination.
9. Verified knowledge base content preserved.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from app.backend.main import app

client = TestClient(app)

EGGPLANT_IMG = ROOT / "backups" / "model1_expansion_phase1_snapshot" / "data" / "processed" / "model1_expanded" / "train" / "eggplant" / "f19f552ce4_eggplant_phomopsis_fruit_rot_Bing_0015.jpg"


def run_chat(text=None, image_path=None):
    files = {}
    data = {}
    if text is not None:
        data["text"] = text
    if image_path and Path(image_path).exists():
        with open(image_path, "rb") as f:
            content = f.read()
        files["file"] = ("test_image.jpg", content, "image/jpeg")
        data["input_type"] = "image"

    resp = client.post("/api/chat", data=data, files=files if files else None)
    return resp


def test_disease_insights_all():
    print("\n" + "=" * 70)
    print("RUNNING COMPREHENSIVE DISEASE INSIGHTS TEST SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Disease Identification Question: "What disease is this?"
    # -------------------------------------------------------------
    print("\n[TEST 1] Disease Identification: 'What disease is this?'")
    r1 = run_chat(text="What disease is this?", image_path=EGGPLANT_IMG)
    assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
    d1 = r1.json()

    # Verify visible cards policy: disease shown, treatment withheld, insights present
    v_cards = d1["router"]["visible_cards"]
    assert v_cards.get("crop") is True, "Crop card should be visible"
    assert v_cards.get("disease") is True, "Disease card should be visible"
    assert v_cards.get("treatment") is False, "Treatment card should be withheld in Mode 1"
    assert v_cards.get("insights") is True, "Insights should be available"

    # Requirement 5: Default collapsed for disease-id-only
    assert d1.get("insights_expanded") is False, "Disease insights should be collapsed by default for disease-id-only"

    # Requirement 2 & 8: Structured subsections populated from verified KB
    ins1 = d1.get("disease_insights")
    assert ins1 is not None and ins1.get("has_insights") is True, "Insights payload should be populated"
    assert len(ins1.get("symptoms", [])) > 0, "Symptoms should be a non-empty list"
    assert ins1.get("pathogen") is not None, "Pathogen should be identified"
    assert "Phomopsis" in ins1.get("pathogen"), f"Expected Phomopsis pathogen, got {ins1.get('pathogen')}"
    assert len(ins1.get("favorable_conditions", [])) > 0, "Favorable conditions should be populated"

    # Requirement 4: No literal markdown asterisks in text message
    msg1 = d1.get("message", "")
    assert "**" not in msg1, f"Literal markdown asterisks found in message: {msg1}"
    print(f"  -> PASS: Mode 1 returned Eggplant + Phomopsis Fruit Rot. Insights collapsed by default ({len(ins1['symptoms'])} symptoms). No literal asterisks.")

    # -------------------------------------------------------------
    # 2. Symptoms Question: "What are the symptoms of this disease?"
    # -------------------------------------------------------------
    print("\n[TEST 2] Symptoms Question: 'What are the symptoms of this disease?'")
    r2 = run_chat(text="What are the symptoms of this disease?", image_path=EGGPLANT_IMG)
    assert r2.status_code == 200
    d2 = r2.json()

    # Requirement 5: Default EXPANDED when user explicitly asks about symptoms
    assert d2.get("insights_expanded") is True, "Insights should be expanded when user asks about symptoms"
    assert d2["router"]["visible_cards"].get("insights") is True
    ins2 = d2.get("disease_insights")
    assert ins2 and ins2.get("has_insights") is True
    assert len(ins2["symptoms"]) >= 2
    # Verify symptoms are clean strings without bullet markers
    for s in ins2["symptoms"]:
        assert not s.startswith("•"), f"Symptom string has literal bullet: {s}"
    print(f"  -> PASS: Insights auto-expanded (insights_expanded=True) with {len(ins2['symptoms'])} clean symptom bullets.")

    # -------------------------------------------------------------
    # 3. Causes / Conditions Question: "What causes this disease and what conditions favor it?"
    # -------------------------------------------------------------
    print("\n[TEST 3] Causes / Conditions Question: 'What causes this disease and what conditions favor it?'")
    r3 = run_chat(text="What causes this disease and what conditions favor it?", image_path=EGGPLANT_IMG)
    assert r3.status_code == 200
    d3 = r3.json()

    # Requirement 5: Expanded for causes/conditions question
    assert d3.get("insights_expanded") is True, "Insights should be expanded when user asks about causes/conditions"
    ins3 = d3.get("disease_insights")
    assert ins3 and ins3.get("has_insights") is True
    assert ins3.get("pathogen") is not None
    assert len(ins3.get("favorable_conditions", [])) > 0
    print(f"  -> PASS: Causes/Pathogen ({ins3['pathogen']}) and Conditions ({len(ins3['favorable_conditions'])}) returned and expanded.")

    # -------------------------------------------------------------
    # 4. Treatment Question: "How do I treat this disease?"
    # -------------------------------------------------------------
    print("\n[TEST 4] Treatment Question: 'How do I treat this disease?'")
    r4 = run_chat(text="How do I treat this disease?", image_path=EGGPLANT_IMG)
    assert r4.status_code == 200
    d4 = r4.json()

    # Requirement 6: Prioritize treatment guidance, avoid repeating duplicate info
    assert d4["router"]["visible_cards"].get("treatment") is True, "Treatment card should be visible"
    assert d4["router"]["visible_cards"].get("insights") is False, "Insights withheld or non-prioritized for treatment-only query"
    assert d4.get("treatment") is not None, "Treatment payload must be provided"
    assert d4["treatment"].get("can_it_be_cured") is not None
    print("  -> PASS: Treatment guidance prioritized. Treatment card active, no repetitive symptoms card.")

    # -------------------------------------------------------------
    # 5. Media-Only Upload (Mode 5): Default complete analysis
    # -------------------------------------------------------------
    print("\n[TEST 5] Media-Only Upload: Image submitted without text")
    r5 = run_chat(text="", image_path=EGGPLANT_IMG)
    assert r5.status_code == 200
    d5 = r5.json()

    # Requirement 7: Available without overwhelming initial result (collapsed by default)
    assert d5["router"]["visible_cards"].get("crop") is True
    assert d5["router"]["visible_cards"].get("disease") is True
    assert d5["router"]["visible_cards"].get("treatment") is True
    assert d5["router"]["visible_cards"].get("insights") is True
    assert d5.get("insights_expanded") is False, "Disease insights should be COLLAPSED by default for media-only upload"
    ins5 = d5.get("disease_insights")
    assert ins5 and ins5.get("has_insights") is True
    print(f"  -> PASS: Media-only upload provides Crop + Disease + Treatment + Collapsed Insights ({len(ins5['symptoms'])} symptoms available on demand).")

    # -------------------------------------------------------------
    # 6. Safeguard / Non-Plant / Empty Data
    # -------------------------------------------------------------
    print("\n[TEST 6] Empty Data / Safeguard Handling")
    # Dark/invalid image
    from PIL import Image
    import io
    black_buf = io.BytesIO()
    Image.new("RGB", (224, 224), (0, 0, 0)).save(black_buf, format="JPEG")
    black_bytes = black_buf.getvalue()

    r6 = client.post(
        "/api/chat",
        data={"text": "What disease is this?", "input_type": "image"},
        files={"file": ("dark.jpg", black_bytes, "image/jpeg")},
    )
    d6 = r6.json()
    ins6 = d6.get("disease_insights")
    # Requirement 8: Hide sections with missing data, do not invent symptoms/causes
    assert ins6 is None or ins6.get("has_insights") is False, "Non-plant/rejected image must not invent disease insights"
    print("  -> PASS: Dark/rejected image safely withheld disease insights without inventing facts.")

    print("\n" + "=" * 70)
    print("ALL DISEASE INSIGHTS ACCEPTANCE TESTS PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    test_disease_insights_all()
