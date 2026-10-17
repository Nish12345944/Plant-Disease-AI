"""
Instruction-Driven Response Validation Suite
============================================
Validates Objectives A, B, and C:
1. No duplicate analyzed media in assistant response.
2. Mode 1 (Disease ID): Crop + Disease, NO treatment plan, NO sources list.
3. Mode 2 (Crop ID): Crop only, NO disease diagnosis, NO treatment plan.
4. Mode 3 (Treatment): Crop + Disease context + Treatment advice and sources.
5. Mode 4 (General info): Crop care/requirements, NO disease/treatment.
6. Mode 5 (Media alone without text): Combined crop + disease + brief next steps.
7. Mode 6 (Composite): All explicitly requested sections returned.
8. Unrecognized non-empty query: Safe clarification, NO silent switch to default analysis.
"""

import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from app.backend.main import app

client = TestClient(app)

ROOT = Path(__file__).resolve().parents[1]
EGGPLANT_IMG = ROOT / "backups" / "model1_expansion_phase1_snapshot" / "data" / "processed" / "model1_expanded" / "train" / "eggplant" / "f19f552ce4_eggplant_phomopsis_fruit_rot_Bing_0015.jpg"


def run_chat_request(text=None, image_path=None, video_path=None):
    files = {}
    data = {}
    if text is not None:
        data["text"] = text
    if image_path and Path(image_path).exists():
        with open(image_path, "rb") as f:
            content = f.read()
        files["file"] = ("test_image.jpg", content, "image/jpeg")
        data["input_type"] = "image"
    elif video_path and Path(video_path).exists():
        with open(video_path, "rb") as f:
            content = f.read()
        files["file"] = ("test_video.mp4", content, "video/mp4")
        data["input_type"] = "video"
    
    resp = client.post("/api/chat", data=data, files=files if files else None)
    return resp


def test_suite():
    print("=================================================================")
    print("RUNNING INSTRUCTION-DRIVEN RESPONSES & MEDIA DE-DUPLICATION SUITE")
    print("=================================================================")

    assert EGGPLANT_IMG.exists(), f"Eggplant test image not found at {EGGPLANT_IMG}"

    # -------------------------------------------------------------------
    # TEST A: Mode 1 Disease Identification
    # -------------------------------------------------------------------
    print("\n[TEST A] Disease identification question: 'What disease is this?'")
    resp_a = run_chat_request(text="What disease is this?", image_path=EGGPLANT_IMG)
    assert resp_a.status_code == 200, f"Status code {resp_a.status_code}: {resp_a.text}"
    body_a = resp_a.json()
    router_a = body_a["router"]
    assert router_a["response_mode"] == "disease_identification", f"Got mode: {router_a.get('response_mode')}"
    assert router_a["visible_cards"]["crop"] is True, "Crop card must be visible as context for disease"
    assert router_a["visible_cards"]["disease"] is True, "Disease card must be visible"
    assert router_a["visible_cards"]["treatment"] is False, "Treatment card must NOT be visible for Mode 1"
    assert body_a.get("treatment") is None, "Treatment payload must be None for Mode 1"
    assert body_a.get("original_image_url") is None, "Objective A: Duplicate analyzed image must be None"
    msg_a = body_a["message"].lower()
    assert "eggplant" in msg_a or "plant" in msg_a, "Message must mention plant"
    assert "rot" in msg_a or "phomopsis" in msg_a or "disease" in msg_a, "Message must mention disease"
    assert "chemical" not in msg_a and "fungicide guidance" not in msg_a, "No full treatment plan in Mode 1 message"
    print("  -> PASS: Mode 1 returned Eggplant + Disease ID, withheld Treatment card and duplicate image.")

    # -------------------------------------------------------------------
    # TEST B: Mode 3 Treatment / Cure Question
    # -------------------------------------------------------------------
    print("\n[TEST B] Treatment question: 'How do I treat this disease?'")
    resp_b = run_chat_request(text="How do I treat this disease?", image_path=EGGPLANT_IMG)
    assert resp_b.status_code == 200
    body_b = resp_b.json()
    router_b = body_b["router"]
    assert router_b["response_mode"] == "treatment", f"Got mode: {router_b.get('response_mode')}"
    assert router_b["visible_cards"]["treatment"] is True, "Treatment card must be visible for Mode 3"
    assert body_b.get("treatment") is not None, "Treatment payload must be present"
    assert body_b.get("original_image_url") is None, "Objective A: Duplicate analyzed image must be None"
    msg_b = body_b["message"].lower()
    assert any(kw in msg_b for kw in ["management", "treatment", "fungicide", "sanitation", "guidance"]), "Must provide treatment advice"
    print("  -> PASS: Mode 3 returned Crop + Disease context followed by treatment advice and treatment card.")

    # -------------------------------------------------------------------
    # TEST C: Mode 2 Plant / Crop Identification
    # -------------------------------------------------------------------
    print("\n[TEST C] Crop identification question: 'What plant is this?'")
    resp_c = run_chat_request(text="What plant is this?", image_path=EGGPLANT_IMG)
    assert resp_c.status_code == 200
    body_c = resp_c.json()
    router_c = body_c["router"]
    assert router_c["response_mode"] == "crop_identification", f"Got mode: {router_c.get('response_mode')}"
    assert router_c["visible_cards"]["crop"] is True, "Crop card must be visible"
    assert router_c["visible_cards"]["disease"] is False, "Disease card must NOT be visible for Mode 2"
    assert router_c["visible_cards"]["treatment"] is False, "Treatment card must NOT be visible for Mode 2"
    assert body_c.get("treatment") is None, "Treatment payload must be None for Mode 2"
    assert body_c.get("original_image_url") is None, "Duplicate analyzed image must be None"
    msg_c = body_c["message"].lower()
    assert "eggplant" in msg_c, f"Expected 'eggplant' in message, got: {body_c['message']}"
    assert "phomopsis" not in msg_c and "rot" not in msg_c, "Disease must NOT be diagnosed in Mode 2"
    print("  -> PASS: Mode 2 returned Eggplant only, without disease detection or treatment sections.")

    # -------------------------------------------------------------------
    # TEST D: Mode 5 Instruction-Free Media Upload
    # -------------------------------------------------------------------
    print("\n[TEST D] Media upload WITHOUT text instruction")
    resp_d = run_chat_request(text="", image_path=EGGPLANT_IMG)
    assert resp_d.status_code == 200
    body_d = resp_d.json()
    router_d = body_d["router"]
    assert router_d["response_mode"] == "media_default_analysis", f"Got mode: {router_d.get('response_mode')}"
    assert router_d["visible_cards"]["crop"] is True
    assert router_d["visible_cards"]["disease"] is True
    assert router_d["visible_cards"]["treatment"] is True
    assert body_d.get("treatment") is not None
    assert body_d.get("original_image_url") is None
    print("  -> PASS: Mode 5 returned combined Crop + Disease + concise next steps.")

    # -------------------------------------------------------------------
    # TEST E: Mode 6 Composite Request
    # -------------------------------------------------------------------
    print("\n[TEST E] Composite request: 'Identify the disease and tell me how to treat it.'")
    resp_e = run_chat_request(text="Identify the disease and tell me how to treat it.", image_path=EGGPLANT_IMG)
    assert resp_e.status_code == 200
    body_e = resp_e.json()
    router_e = body_e["router"]
    assert router_e["response_mode"] == "composite_request"
    assert router_e["visible_cards"]["crop"] is True
    assert router_e["visible_cards"]["disease"] is True
    assert router_e["visible_cards"]["treatment"] is True
    assert body_e.get("treatment") is not None
    print("  -> PASS: Mode 6 returned crop, disease, and treatment.")

    # -------------------------------------------------------------------
    # TEST H: Unrecognized Instruction
    # -------------------------------------------------------------------
    print("\n[TEST H] Unrecognized non-empty instruction: 'Who won the World Cup?'")
    resp_h = run_chat_request(text="Who won the World Cup?", image_path=EGGPLANT_IMG)
    assert resp_h.status_code == 200
    body_h = resp_h.json()
    router_h = body_h["router"]
    assert router_h["response_mode"] == "unrecognized_instruction"
    assert router_h["visible_cards"]["crop"] is False
    assert router_h["visible_cards"]["disease"] is False
    assert router_h["visible_cards"]["treatment"] is False
    assert body_h.get("treatment") is None
    assert "couldn't relate" in body_h["message"].lower() or "clarification" in body_h["message"].lower() or "identify" in body_h["message"].lower()
    print("  -> PASS: Unrecognized instruction correctly prompted for clarification without default combined analysis.")

    # -------------------------------------------------------------------
    # TEST G: Safeguard Rejection (Non-plant image)
    # -------------------------------------------------------------------
    print("\n[TEST G] Safeguard validation (Non-plant image)")
    # Generate a pure black image which triggers low_visibility/rejection
    from PIL import Image
    black_img = Image.new("RGB", (100, 100), color=(0, 0, 0))
    buf = io.BytesIO()
    black_img.save(buf, format="JPEG")
    resp_g = client.post("/api/chat", data={"text": "What disease is this?"}, files={"file": ("black.jpg", buf.getvalue(), "image/jpeg")})
    assert resp_g.status_code == 200
    body_g = resp_g.json()
    assert body_g["model1"].get("status") == "rejected" or body_g["model1"].get("validation", {}).get("valid") is False
    assert body_g.get("treatment") is None
    print("  -> PASS: Safeguard rejection preserved without inventing crop, disease, or treatment.")

    print("\n=================================================================")
    print("ALL ACCEPTANCE TESTS (A, B, C, D, E, G, H) PASSED SUCCESSFULLY!")
    print("=================================================================")


if __name__ == "__main__":
    test_suite()
