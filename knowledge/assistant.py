"""
Agricultural Conversational Assistant (No-LLM)
==============================================
Unified orchestrator for conversational agricultural question answering:
  USER QUERY [+ OPTIONAL VISUAL INFERENCE]
      ↓
  QUERY UNDERSTANDING & ENTITY EXTRACTION
      ↓
  DIALOGUE CONTEXT & ANAPHORA RESOLUTION
      ↓
  RULE-BASED STRUCTURED REASONING
      ↓
  TARGETED KNOWLEDGE BASE RETRIEVAL
      ↓
  INTERMEDIATE ANSWER PLANNING
      ↓
  DETERMINISTIC NATURAL LANGUAGE BUILDER
      ↓
  FINAL AGENT RESPONSE WITH PROVENANCE
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from knowledge.database import AgriculturalKnowledgeBase, get_knowledge_base
from knowledge.dialogue import ConversationManager
from knowledge.planner import plan_answer
from knowledge.reasoning import reason_agricultural_query
from knowledge.response_builder import build_response
from knowledge.retrieval import retrieve_relevant_knowledge
from knowledge.schema import FinalAgentResponse
from router.query_router import route_multimodal_query

logger = logging.getLogger(__name__)


class AgriculturalAssistant:
    """
    Conversational Agricultural Assistant.
    Operates strictly deterministically with zero LLM API or generative hallucination risks.
    """

    def __init__(self, kb: Optional[AgriculturalKnowledgeBase] = None):
        self.kb = kb or get_knowledge_base()
        self.conversation = ConversationManager()

    def set_visual_evidence(self, visual_result: dict[str, Any]):
        """
        Binds Model 1 / Model 2 visual inference outputs to the ongoing conversation session.
        """
        self.conversation.update_with_visual_evidence(visual_result)

    def answer_query(
        self,
        query: str,
        visual_result: Optional[dict[str, Any]] = None,
        crop_override: Optional[str] = None,
        disease_override: Optional[str] = None,
    ) -> FinalAgentResponse:
        """
        Processes a user question through the complete 8-step reasoning & retrieval pipeline.
        """
        raw_query = (query or "").strip()

        # Update visual evidence if provided in call
        if visual_result:
            self.conversation.update_with_visual_evidence(visual_result)

        effective_visual = visual_result or self.conversation.state.last_visual_evidence

        # Session context for query understanding
        session_ctx = {}
        if self.conversation.state.current_crop:
            session_ctx["crop"] = self.conversation.state.current_crop
        if self.conversation.state.current_disease:
            session_ctx["disease"] = self.conversation.state.current_disease
        if self.conversation.state.current_status:
            session_ctx["status"] = self.conversation.state.current_status

        # 1. Query Understanding & Intent Routing
        understanding = route_multimodal_query(
            text=raw_query,
            visual_result=effective_visual,
            session_context=session_ctx,
        )

        # 2. Dialogue Context & Anaphora Resolution
        eff_crop, eff_disease, eff_status = self.conversation.resolve_contextual_query(
            query_text=raw_query,
            query_crop=crop_override or understanding.entities.crop,
            query_disease=disease_override or understanding.entities.disease,
        )

        # 3. Structured Rule-Based Agricultural Reasoning
        reasoning = reason_agricultural_query(
            intent=understanding.intent,
            raw_query=raw_query,
            entities=understanding.entities,
            visual_result=effective_visual,
            dialogue_crop=eff_crop,
            dialogue_disease=eff_disease,
            dialogue_status=eff_status,
            kb=self.kb,
        )

        # 4. Targeted Knowledge Base Retrieval
        retrieved_data = {"found": False, "facts": {}, "source_ids": [], "citations": []}
        if reasoning.status not in ("clarification_needed", "uncertain") and not reasoning.is_incompatible_rejected:
            retrieved_data = retrieve_relevant_knowledge(
                intent=understanding.intent,
                crop=reasoning.resolved_crop,
                disease=reasoning.resolved_disease,
                entities=understanding.entities,
                query_text=raw_query,
                kb=self.kb,
            )

        # 5. Intermediate Answer Planning
        plan = plan_answer(
            intent=understanding.intent,
            reasoning=reasoning,
            retrieved_data=retrieved_data,
        )

        # 6. Deterministic Natural-Language Response Builder
        response = build_response(
            plan=plan,
            reasoning=reasoning,
            crop=reasoning.resolved_crop,
            disease=reasoning.resolved_disease,
            status=reasoning.status,
            visual_evidence=effective_visual,
        )

        # 7. Record Turn in Dialogue History
        self.conversation.record_turn(
            user_query=raw_query,
            normalized_query=understanding.normalized_text,
            intent=understanding.intent,
            crop=response.crop,
            disease=response.disease,
            status=response.status,
            system_response=response.text,
        )

        return response

    def reset_session(self):
        """Clears conversational history for a new user session."""
        self.conversation.reset()
