"""
Local Knowledge Base Repository & Indexer
=========================================
Stores and indexes verified DiseaseRecord and CropRecord objects.
Provides fast in-memory indexing with JSON serialization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from knowledge.data.pilot_knowledge import PILOT_CROPS, PILOT_DISEASES
from knowledge.schema import CropRecord, DiseaseRecord
from knowledge.sources import SOURCE_REGISTRY, SourceRecord

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
KNOWLEDGE_STORE_DIR = PROJECT_ROOT / "knowledge" / "store"


class AgriculturalKnowledgeBase:
    """In-memory and file-backed verified agricultural knowledge repository."""

    def __init__(self, load_pilot: bool = True):
        self.diseases: dict[str, DiseaseRecord] = {}
        self.crops: dict[str, CropRecord] = {}
        self.sources: dict[str, SourceRecord] = SOURCE_REGISTRY

        if load_pilot:
            self.load_pilot_data()

    def load_pilot_data(self):
        """Populate initial verified knowledge base from pilot dataset."""
        for slug, d_rec in PILOT_DISEASES.items():
            self.diseases[slug.lower()] = d_rec
        for crop_name, c_rec in PILOT_CROPS.items():
            self.crops[crop_name.lower()] = c_rec

    def get_disease(self, disease_slug: Optional[str]) -> Optional[DiseaseRecord]:
        """Look up a disease record by slug (case-insensitive)."""
        if not disease_slug:
            return None
        slug_clean = disease_slug.strip().lower()
        return self.diseases.get(slug_clean)

    def get_crop(self, crop_name: Optional[str]) -> Optional[CropRecord]:
        """Look up a crop record by name (case-insensitive)."""
        if not crop_name:
            return None
        crop_clean = crop_name.strip().lower()
        return self.crops.get(crop_clean)

    def find_diseases_for_crop(self, crop_name: str) -> list[DiseaseRecord]:
        """Retrieve all registered disease profiles associated with a crop."""
        crop_clean = crop_name.strip().lower()
        return [d for d in self.diseases.values() if d.crop.lower() == crop_clean]

    def has_disease_knowledge(self, disease_slug: Optional[str]) -> bool:
        """Check if verified knowledge exists for a specific disease."""
        if not disease_slug:
            return False
        return disease_slug.strip().lower() in self.diseases

    def export_summary(self) -> dict:
        return {
            "total_diseases": len(self.diseases),
            "total_crops": len(self.crops),
            "total_sources": len(self.sources),
            "disease_slugs": list(self.diseases.keys()),
            "crop_names": list(self.crops.keys()),
        }


# Global Singleton Instance
_KB_INSTANCE: Optional[AgriculturalKnowledgeBase] = None


def get_knowledge_base() -> AgriculturalKnowledgeBase:
    global _KB_INSTANCE
    if _KB_INSTANCE is None:
        _KB_INSTANCE = AgriculturalKnowledgeBase(load_pilot=True)
    return _KB_INSTANCE
