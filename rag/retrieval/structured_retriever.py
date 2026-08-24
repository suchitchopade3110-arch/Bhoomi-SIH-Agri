"""
BHOOMI Structured Evidence Retriever
Performs direct, deterministic indexing and query filtering on quantitative fields:
ETL thresholds, conditional modifiers, SES severity tiers, CIBRC chemical regulatory status,
and diagnostic trees. Outranks generic semantic matches for safety and numerical decisions.
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class StructuredRetriever:
    def __init__(self, knowledge_version: str = "v4.2.0-validated"):
        self.knowledge_version = knowledge_version
        self.indexes_dir = PROJECT_ROOT / "rag" / "indexes"
        
        v_tag = knowledge_version.replace("-", "_").replace(".", "_")
        self.obj_file = self.indexes_dir / f"evidence_objects_{v_tag}.json"

        self.evidence_objects: List[Dict[str, Any]] = []
        self.entity_index: Dict[str, List[Dict[str, Any]]] = {}
        self.chemical_index: Dict[str, List[Dict[str, Any]]] = {}
        self.etl_index: Dict[str, List[Dict[str, Any]]] = {}
        self.severity_index: Dict[str, List[Dict[str, Any]]] = {}

        self._load_and_index()

    def _load_and_index(self):
        """Loads canonical evidence objects and indexes them by structured keys."""
        if not self.obj_file.exists():
            from rag.ingestion.build_corpus import CorpusBuilder
            builder = CorpusBuilder(knowledge_version=self.knowledge_version)
            builder.build_all()

        with open(self.obj_file, "r", encoding="utf-8") as f:
            self.evidence_objects = json.load(f)

        for obj in self.evidence_objects:
            # Index by Entity ID
            ent_id = obj.get("entity_id")
            if ent_id:
                if ent_id not in self.entity_index:
                    self.entity_index[ent_id] = []
                self.entity_index[ent_id].append(obj)

            # Index by Canonical Name
            cname = obj.get("canonical_name", "").lower()
            if cname:
                if cname not in self.entity_index:
                    self.entity_index[cname] = []
                self.entity_index[cname].append(obj)

            # Index by Chemical Active Ingredient
            chem = obj.get("chemical")
            if chem:
                chem_lower = chem.lower()
                if chem_lower not in self.chemical_index:
                    self.chemical_index[chem_lower] = []
                self.chemical_index[chem_lower].append(obj)

            # Index ETL records
            if obj.get("etl"):
                if ent_id not in self.etl_index:
                    self.etl_index[ent_id] = []
                self.etl_index[ent_id].append(obj)

            # Index Severity records
            if obj.get("severity"):
                if ent_id not in self.severity_index:
                    self.severity_index[ent_id] = []
                self.severity_index[ent_id].append(obj)

    def retrieve_by_entity(self, entity_identifier: str) -> List[Dict[str, Any]]:
        """Direct lookup for an entity ID or canonical name."""
        key = entity_identifier.lower().strip()
        return self.entity_index.get(key, []) or self.entity_index.get(entity_identifier, [])

    def retrieve_etl(self, entity_id: str, stage: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves exact economic threshold levels (ETLs) with conditional modifiers."""
        candidates = self.etl_index.get(entity_id, [])
        if not stage or stage == "all_stages":
            return candidates
        return [c for c in candidates if c.get("crop_stage") == stage or c.get("crop_stage") == "all_stages"]

    def retrieve_chemical(self, chemical_name: str) -> List[Dict[str, Any]]:
        """Retrieves CIBRC regulatory chemical status, dosage, and PHI."""
        chem_lower = chemical_name.lower().strip()
        for k, v in self.chemical_index.items():
            if chem_lower in k or k in chem_lower:
                return v
        return []

    def retrieve_by_query_context(self, parsed_context: Dict[str, Any], top_k: int = 5) -> List[Dict[str, Any]]:
        """Structured retrieval based on parsed agricultural entities, chemicals, and intents."""
        results = []
        seen_ids = set()

        # 1. Chemical lookup
        chem = parsed_context.get("chemical")
        if chem:
            chem_matches = self.retrieve_chemical(chem)
            for m in chem_matches:
                if m["record_id"] not in seen_ids:
                    results.append({
                        "chunk_id": m.get("chunk_id"),
                        "parent_record_id": m.get("record_id"),
                        "evidence_id": m.get("evidence_id"),
                        "entity_id": m.get("entity_id"),
                        "chunk_type": m.get("chunk_type"),
                        "text": m.get("recommendation"),
                        "metadata": {
                            "canonical_name": m.get("canonical_name"),
                            "chemical": m.get("chemical"),
                            "formulation": m.get("formulation"),
                            "chemical_status": m.get("chemical_status"),
                            "phi": m.get("phi"),
                            "source_authority": m.get("source_authority", 10),
                            "drone_guidelines": m.get("drone_guidelines")
                        },
                        "provenance": m.get("provenance_chain"),
                        "structured_score": 1.0,
                        "knowledge_version": self.knowledge_version
                    })
                    seen_ids.add(m["record_id"])

        # 2. Entity / Alias lookup
        for ent_name in parsed_context.get("expanded_canonical_entities", []):
            ent_matches = self.retrieve_by_entity(ent_name)
            for m in ent_matches:
                if m["record_id"] not in seen_ids:
                    results.append({
                        "chunk_id": m.get("chunk_id"),
                        "parent_record_id": m.get("record_id"),
                        "evidence_id": m.get("evidence_id"),
                        "entity_id": m.get("entity_id"),
                        "chunk_type": m.get("chunk_type"),
                        "text": m.get("recommendation"),
                        "metadata": {
                            "canonical_name": m.get("canonical_name"),
                            "etl": m.get("etl"),
                            "severity": m.get("severity"),
                            "source_authority": m.get("source_authority", 9)
                        },
                        "provenance": m.get("provenance_chain"),
                        "structured_score": 0.95,
                        "knowledge_version": self.knowledge_version
                    })
                    seen_ids.add(m["record_id"])

        return results[:top_k]
