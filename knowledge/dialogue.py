"""
Dialogue Context and Conversational State Manager
=================================================
Tracks short-term multi-turn conversational context, resolves anaphoric references
('it', 'this', 'why', 'how to treat it', 'can it spread'), and binds active visual evidence.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from knowledge.schema import DialogueState, DialogueTurn


class ConversationManager:
    """Manages active dialogue session state and reference resolution."""

    def __init__(self):
        self.state = DialogueState()

    def update_with_visual_evidence(self, visual_result: dict[str, Any]):
        """Binds incoming Model 1 / Model 2 visual inference evidence to the dialogue state."""
        if not visual_result:
            return
        self.state.last_visual_evidence = visual_result
        if visual_result.get("crop"):
            self.state.current_crop = visual_result["crop"].lower()
        if visual_result.get("disease"):
            self.state.current_disease = visual_result["disease"].lower()
        if visual_result.get("status"):
            self.state.current_status = visual_result["status"].lower()

    def resolve_contextual_query(
        self,
        query_text: str,
        query_crop: Optional[str] = None,
        query_disease: Optional[str] = None,
    ) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Resolves the effective crop, disease, and status for the current turn.
        Merges query entities with active dialogue state if the query uses relative references.
        """
        crop = query_crop or self.state.current_crop
        disease = query_disease or self.state.current_disease
        status = self.state.current_status

        # If query has explicit crop and disease, update active state
        if query_crop:
            crop = query_crop.lower()
        if query_disease:
            disease = query_disease.lower()

        # Check for pronoun resolution ("it", "this", "that", "why", "spread", "prevent")
        text_lower = query_text.lower()
        has_relative_ref = any(
            re.search(r"\b" + re.escape(w) + r"\b", text_lower)
            for w in ["it", "this", "that", "why", "how", "spread", "cure", "treat", "prevent", "happen", "die"]
        )

        if has_relative_ref and not query_disease and self.state.current_disease:
            disease = self.state.current_disease
        if has_relative_ref and not query_crop and self.state.current_crop:
            crop = self.state.current_crop

        return crop, disease, status

    def record_turn(
        self,
        user_query: str,
        normalized_query: str,
        intent: str,
        crop: Optional[str],
        disease: Optional[str],
        status: Optional[str],
        system_response: str,
    ):
        """Records a completed conversational turn."""
        self.state.add_turn(
            user_query=user_query,
            normalized_query=normalized_query,
            intent=intent,
            crop=crop,
            disease=disease,
            status=status,
            system_response=system_response,
        )

    def reset(self):
        """Resets conversational history and active focus."""
        self.state = DialogueState()
