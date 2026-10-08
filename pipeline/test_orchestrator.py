"""Tests for the central orchestrator.

Run:
    python pipeline/test_orchestrator.py

Audio STT is stubbed via the audio_text parameter (no model download).
A missing-audio error path is also covered.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.orchestrator import (
    combine_queries,
    orchestrate,
    run_model1_placeholder,
    run_model2_placeholder,
    run_rag_placeholder,
)

PASS = "PASS"
FAIL = "FAIL"
results = []


def check(name, got, expected):
    ok = got == expected
    results.append(ok)
    print(f"[{PASS if ok else FAIL}] {name}")
    if not ok:
        print(f"       expected: {expected}")
        print(f"       got     : {got}")


def test_image_typed_plant():
    s = orchestrate(image="leaf.jpg", text_query="What plant is this?")
    d = s.to_dict()
    check("1a intent", d["intent"], "plant_identification")
    check("1b flags", (d["needs_model1"], d["needs_model2"], d["needs_rag"]),
          (True, False, False))
    check("1c inputs", d["inputs"],
          {"image": "leaf.jpg", "video": None, "audio": None})
    check("1d query kept", d["query"], "What plant is this?")


def test_image_disease():
    s = orchestrate(image="leaf.jpg",
                    text_query="What disease does this plant have?")
    d = s.to_dict()
    check("2a intent", d["intent"], "disease_detection")
    check("2b flags", (d["needs_model1"], d["needs_model2"], d["needs_rag"]),
          (True, True, False))


def test_image_treatment():
    s = orchestrate(image="leaf.jpg",
                    text_query="How do I treat this disease?")
    d = s.to_dict()
    check("3a intent", d["intent"], "treatment_information")
    check("3b flags", (d["needs_model1"], d["needs_model2"], d["needs_rag"]),
          (True, True, True))
    s2 = orchestrate(image="leaf.jpg",
                     text_query="How do I treat this disease?",
                     run_stages=True)
    check("3c m1 placeholder", s2.model1["status"], "not_implemented")
    check("3d m2 placeholder", s2.model2["status"], "not_implemented")
    check("3e rag placeholder", s2.rag["status"], "not_implemented")


def test_audio_question():
    s = orchestrate(image="leaf.jpg", audio="voice.mp3",
                    audio_text="What plant is this?")
    d = s.to_dict()
    check("4a query from audio", d["query"], "What plant is this?")
    check("4b intent", d["intent"], "plant_identification")
    check("4c audio kept", d["inputs"]["audio"], "voice.mp3")
    check("4d transcription stored", s.audio_transcription,
          "What plant is this?")


def test_typed_plus_audio():
    s = orchestrate(text_query="It has yellow spots",
                    audio_text="What disease is this?")
    d = s.to_dict()
    check("5a both kept", d["query"],
          "It has yellow spots [Audio says: What disease is this?]")
    check("5b intent", d["intent"], "disease_detection")
    check("5c combine identical",
          combine_queries("Hello", "hello"), "Hello")


def test_unknown():
    s = orchestrate(text_query="Hello")
    d = s.to_dict()
    check("6a intent", d["intent"], "unknown")
    check("6b nothing runs",
          (d["needs_model1"], d["needs_model2"], d["needs_rag"]),
          (False, False, False))
    s2 = orchestrate(text_query="Hello", run_stages=True)
    check("6c no m1 call", s2.model1, None)
    check("6d no m2 call", s2.model2, None)
    check("6e no rag call", s2.rag, None)


def test_missing_audio_errors_cleanly():
    try:
        orchestrate(audio="no_such_file.mp3")
        check("7a missing audio raises", "no-error", "FileNotFoundError")
    except FileNotFoundError as exc:
        check("7a missing audio raises", "FileNotFoundError",
              "FileNotFoundError")
        print(f"       message: {exc}")


def main():
    test_image_typed_plant()
    test_image_disease()
    test_image_treatment()
    test_audio_question()
    test_typed_plus_audio()
    test_unknown()
    test_missing_audio_errors_cleanly()
    n = sum(results)
    print(f"\n{n}/{len(results)} checks passed.")
    return 0 if n == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
