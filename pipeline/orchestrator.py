"""Central orchestrator: image / video / audio / text -> intent -> stages.

Connects existing input + router components into one pipeline WITHOUT
modifying any existing ML code:
  - audio text via audio.test_audio.transcribe_audio (faster-whisper)
  - intent via router.query_router.route_query (imported, never duplicated)

Model 1 / Model 2 / RAG / LLM are clean placeholders for later wiring.
No paid APIs, no cloud services, Python only.

Usage:
    from pipeline.orchestrator import orchestrate
    state = orchestrate(image="leaf.jpg", text_query="What disease is this?")
"""

from __future__ import annotations

from dataclasses import dataclass, field

from router.query_router import route_query


def run_model1_placeholder(image_path=None, video_path=None):
    """Placeholder for Model 1 (crop/plant identification). Not wired yet."""
    return {"stage": "model1", "status": "not_implemented",
            "image": image_path, "video": video_path}


def run_model2_placeholder(image_path=None, video_path=None, plant=None):
    """Placeholder for Model 2 (disease detection). Not wired yet."""
    return {"stage": "model2", "status": "not_implemented",
            "image": image_path, "video": video_path, "plant": plant}


def run_rag_placeholder(query="", context=None):
    """Placeholder for RAG / treatment & plant-info retrieval. Not wired."""
    return {"stage": "rag", "status": "not_implemented",
            "query": query, "context": context}


def run_llm_placeholder(prompt="", context=None):
    """Placeholder for the answer-generation LLM. Not wired yet."""
    return {"stage": "llm", "status": "not_implemented",
            "prompt": prompt, "context": context}


def _clean(value):
    """Trim strings; empty/blank becomes None."""
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def transcribe_audio_input(audio_path):
    """Transcribe audio via the existing faster-whisper module."""
    audio_path = _clean(audio_path)
    if audio_path is None:
        return None
    from audio.test_audio import transcribe_audio

    try:
        result = transcribe_audio(audio_path)
    except (FileNotFoundError, ValueError):
        raise
    except Exception as exc:
        raise RuntimeError(f"Audio transcription failed: {exc}") from exc
    return (result.text or "").strip() or None


def combine_queries(typed_text=None, audio_text=None):
    """Combine typed + transcribed queries without losing either."""
    typed = _clean(typed_text) or ""
    spoken = _clean(audio_text) or ""
    if not typed:
        return spoken
    if not spoken:
        return typed
    if typed.lower() == spoken.lower():
        return typed
    if spoken.lower() in typed.lower():
        return typed
    if typed.lower() in spoken.lower():
        return spoken
    return f"{typed} [Audio says: {spoken}]"


@dataclass
class RequestState:
    """Structured pipeline state returned by orchestrate()."""

    query: str = ""
    intent: str = "unknown"
    needs_model1: bool = False
    needs_model2: bool = False
    needs_rag: bool = False
    inputs: dict = field(default_factory=dict)
    audio_transcription: str = None
    typed_text: str = None
    model1: dict = None
    model2: dict = None
    rag: dict = None

    def to_dict(self):
        """Spec-shaped dict for the main pipeline / API layer."""
        return {
            "query": self.query,
            "intent": self.intent,
            "needs_model1": self.needs_model1,
            "needs_model2": self.needs_model2,
            "needs_rag": self.needs_rag,
            "inputs": self.inputs,
        }


def orchestrate(image=None, video=None, audio=None, text_query=None,
                audio_text=None, run_stages=False):
    """Run the central pipeline and return a RequestState.

    audio_text is an optional pre-transcribed string (used by tests to
    skip heavy STT). run_stages invokes placeholder stage functions.
    """
    image = _clean(image)
    video = _clean(video)
    audio = _clean(audio)
    typed = _clean(text_query)

    spoken = _clean(audio_text)
    if spoken is None and audio is not None:
        spoken = transcribe_audio_input(audio)

    query = combine_queries(typed, spoken)
    routing = route_query(query)

    state = RequestState(
        query=query,
        intent=routing["intent"],
        needs_model1=routing["needs_model1"],
        needs_model2=routing["needs_model2"],
        needs_rag=routing["needs_rag"],
        inputs={"image": image, "video": video, "audio": audio},
        audio_transcription=spoken,
        typed_text=typed,
    )

    if run_stages:
        if state.needs_model1:
            state.model1 = run_model1_placeholder(image, video)
        if state.needs_model2:
            state.model2 = run_model2_placeholder(image, video)
        if state.needs_rag:
            state.rag = run_rag_placeholder(query)

    return state


if __name__ == "__main__":
    import sys

    demo = orchestrate(text_query=" ".join(sys.argv[1:]) or "Hello")
    print(demo.to_dict())
