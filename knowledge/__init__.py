"""
Agricultural Knowledge & Conversational Reasoning Engine
========================================================
Verified, traceable, LLM-free agricultural reasoning & knowledge retrieval layer.
"""

from knowledge.assistant import AgriculturalAssistant
from knowledge.database import AgriculturalKnowledgeBase, get_knowledge_base
from knowledge.dialogue import ConversationManager
from knowledge.planner import plan_answer
from knowledge.reasoning import reason_agricultural_query
from knowledge.response_builder import build_response
from knowledge.retrieval import retrieve_relevant_knowledge
from knowledge.schema import (
    AnswerPlan,
    CropRecord,
    DialogueState,
    DialogueTurn,
    DiseaseRecord,
    FinalAgentResponse,
    ManagementStrategies,
    SourcedFact,
    SourceRecord,
    SourceTier,
    StructuredReasoningResult,
)
from knowledge.sources import SOURCE_REGISTRY, format_source_citation

__all__ = [
    "AgriculturalAssistant",
    "AgriculturalKnowledgeBase",
    "AnswerPlan",
    "ConversationManager",
    "CropRecord",
    "DialogueState",
    "DialogueTurn",
    "DiseaseRecord",
    "FinalAgentResponse",
    "ManagementStrategies",
    "SOURCE_REGISTRY",
    "SourceRecord",
    "SourceTier",
    "SourcedFact",
    "StructuredReasoningResult",
    "build_response",
    "format_source_citation",
    "get_knowledge_base",
    "plan_answer",
    "reason_agricultural_query",
    "retrieve_relevant_knowledge",
]
