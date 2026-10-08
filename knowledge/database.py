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
from knowledge.data.v4_disease_knowledge import V4_CROP_KNOWLEDGE, V4_DISEASE_KNOWLEDGE
from knowledge.schema import CropRecord, DiseaseRecord
from knowledge.sources import SOURCE_REGISTRY, SourceRecord

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
KNOWLEDGE_STORE_DIR = PROJECT_ROOT / "knowledge" / "store"


class AgriculturalKnowledgeBase:
    """In-memory and file-backed verified agricultural knowledge repository."""

    def __init__(self, load_pilot: bool = True, load_v4: bool = True):
        self.diseases: dict[str, DiseaseRecord] = {}
        self.crops: dict[str, CropRecord] = {}
        self.sources: dict[str, SourceRecord] = SOURCE_REGISTRY

        if load_pilot:
            self.load_pilot_data()
        if load_v4:
            self.load_v4_data()

    def load_pilot_data(self):
        """Populate initial verified knowledge base from pilot dataset."""
        for slug, d_rec in PILOT_DISEASES.items():
            self.diseases[slug.lower()] = d_rec
        for crop_name, c_rec in PILOT_CROPS.items():
            self.crops[crop_name.lower()] = c_rec

    def load_v4_data(self):
        """Populate full Model 2 V4 knowledge base covering all 116 disease classes."""
        for slug, d_rec in V4_DISEASE_KNOWLEDGE.items():
            self.diseases[slug.lower()] = d_rec
        for crop_name, c_rec in V4_CROP_KNOWLEDGE.items():
            self.crops[crop_name.lower()] = c_rec

    def get_disease(self, disease_slug: Optional[str]) -> Optional[DiseaseRecord]:
        """Look up a disease record by slug or common name (case-insensitive)."""
        if not disease_slug:
            return None
        slug_clean = disease_slug.strip().lower()
        if slug_clean in self.diseases:
            return self.diseases[slug_clean]

        # Fallback: match by common name or partial disease slug
        slug_norm = slug_clean.replace(" ", "_")
        for slug, rec in self.diseases.items():
            if slug_norm == slug:
                return rec
            if "__" in slug:
                _, d_part = slug.split("__", 1)
                if slug_norm == d_part or slug_clean == d_part.replace("_", " "):
                    return rec
            if slug_clean == rec.common_name.lower():
                return rec

        return None

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
        return self.get_disease(disease_slug) is not None

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
