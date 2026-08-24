"""
BHOOMI Structured Evidence Retriever
Performs direct, deterministic indexing and query filtering on quantitative fields:
ETL thresholds, conditional modifiers, SES severity tiers, CIBRC chemical regulatory status,
traditional agro-inputs, and diagnostic trees. Outranks generic semantic matches for numerical & safety decisions.
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
        self.traditional_index: Dict[str, List[Dict[str, Any]]] = {}

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
            ent_id = obj.get("entity_id")
            if ent_id:
                if ent_id not in self.entity_index:
                    self.entity_index[ent_id] = []
                self.entity_index[ent_id].append(obj)

            cname = (obj.get("canonical_name") or "").lower()
            if cname:
                if cname not in self.entity_index:
                    self.entity_index[cname] = []
                self.entity_index[cname].append(obj)

            for t_alias in obj.get("tamil_aliases", []):
                t_key = t_alias.lower().strip()
                if t_key:
                    if t_key not in self.entity_index:
                        self.entity_index[t_key] = []
                    self.entity_index[t_key].append(obj)

            chem = obj.get("chemical")
            if chem:
                chem_lower = chem.lower()
                for key in [chem_lower, cname, obj.get("evidence_id", "").lower()]:
                    if key:
                        if key not in self.chemical_index:
                            self.chemical_index[key] = []
                        self.chemical_index[key].append(obj)

                # Index Tamil aliases for chemicals
                for t_alias in obj.get("tamil_aliases", []):
                    t_k = t_alias.lower().strip()
                    if t_k:
                        if t_k not in self.chemical_index:
                            self.chemical_index[t_k] = []
                        self.chemical_index[t_k].append(obj)

            # Index ETL records
            if obj.get("etl") or obj.get("chunk_type") == "ETL":
                if ent_id:
                    if ent_id not in self.etl_index:
                        self.etl_index[ent_id] = []
                    self.etl_index[ent_id].append(obj)
                ev_id = obj.get("evidence_id")
                if ev_id:
                    if ev_id not in self.etl_index:
                        self.etl_index[ev_id] = []
                    self.etl_index[ev_id].append(obj)

            # Index Severity records
            if obj.get("severity") or obj.get("chunk_type") == "SEVERITY":
                if ent_id:
                    if ent_id not in self.severity_index:
                        self.severity_index[ent_id] = []
                    self.severity_index[ent_id].append(obj)

            # Index Traditional Inputs
            if obj.get("chunk_type") == "TRADITIONAL_INPUT":
                for name_token in [cname, obj.get("evidence_id", "").lower()]:
                    if name_token not in self.traditional_index:
                        self.traditional_index[name_token] = []
                    self.traditional_index[name_token].append(obj)

        # Seed Tamil chemical synonyms in chemical index
        chem_synonyms = {
            "சுடோமோனாஸ்": "CHEM-015",
            "சூடோமோனாஸ்": "CHEM-015",
            "pseudomonas": "CHEM-015",
            "குளோரான்ட்ரனிலிப்ரோல்": "CHEM-001",
            "coragen": "CHEM-001",
            "கோரஜென்": "CHEM-001",
            "பப்ரோபெசின்": "CHEM-002",
            "தயாமீதாக்சம்": "CHEM-004",
            "டிரைசைக்ளசோல்": "CHEM-008",
            "ஹெக்சாகோனசோல்": "CHEM-009",
            "வாலிடமைசின்": "CHEM-010",
            "மேன்கோசெப்": "CHEM-011",
            "அசாக்சிஸ்ட்ரோபின்": "CHEM-012",
            "புரோபிகோனசோல்": "CHEM-013",
            "காப்பர் ஹைட்ராக்சைடு": "CHEM-007"
        }
        for syn, cid in chem_synonyms.items():
            matching_objs = [o for o in self.evidence_objects if o.get("evidence_id") == cid]
            if matching_objs:
                self.chemical_index[syn.lower()] = matching_objs

    def retrieve_by_entity(self, entity_identifier: str) -> List[Dict[str, Any]]:
        """Direct lookup for an entity ID or canonical name."""
        key = entity_identifier.lower().strip()
        return self.entity_index.get(key, []) or self.entity_index.get(entity_identifier, [])

    def retrieve_etl(self, entity_id: str, stage: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves exact ETL threshold rules, filtering by growth stage if specified."""
        records = self.etl_index.get(entity_id, [])
        if not records:
            records = self.etl_index.get(entity_id.replace("_", "-"), [])
        if not stage:
            return records
        
        filtered = []
        for r in records:
            r_stage = r.get("crop_stage")
            if not r_stage or r_stage == "all_stages" or r_stage == stage:
                filtered.append(r)
        return filtered if filtered else records

    def retrieve_severity(self, entity_id: str) -> List[Dict[str, Any]]:
        """Retrieves standard SES severity scale definitions for the entity."""
        records = self.severity_index.get(entity_id, [])
        if not records:
            records = self.severity_index.get(entity_id.replace("_", "-"), [])
        return records

    def retrieve_chemical(self, chemical_name: str) -> List[Dict[str, Any]]:
        """Retrieves CIBRC regulatory and dosage specifications for a chemical."""
        chem_lower = chemical_name.lower().strip()
        if chem_lower in self.chemical_index:
            return self.chemical_index[chem_lower]
        for k, v in self.chemical_index.items():
            if chem_lower in k or k in chem_lower:
                return v
        return []

    def retrieve_by_query_context(self, parsed_context: Dict[str, Any], top_k: int = 10) -> List[Dict[str, Any]]:
        """Performs structured lookup combining intent, chemical, ETL, and traditional inputs."""
        results: List[Dict[str, Any]] = []
        seen_ids = set()

        # 1. Traditional Agro-Inputs (மயில் துத்தம், அண்ணாமலை கலவை)
        orig_q = parsed_context.get("original_query", "")
        if "மயில் துத்தம்" in orig_q or "copper sulphate" in orig_q.lower():
            for obj in self.evidence_objects:
                if obj.get("evidence_id") == "AGRO_INPUT_COPPER_SULPHATE":
                    if obj["record_id"] not in seen_ids:
                        results.append({
                            "chunk_id": obj.get("chunk_id"),
                            "parent_record_id": obj.get("record_id"),
                            "evidence_id": obj.get("evidence_id"),
                            "entity_id": obj.get("entity_id"),
                            "chunk_type": obj.get("chunk_type"),
                            "text": obj.get("recommendation"),
                            "metadata": {
                                "canonical_name": obj.get("canonical_name"),
                                "source_authority": obj.get("source_authority", 8)
                            },
                            "provenance": obj.get("provenance_chain", ["TNAU Traditional Guide"]),
                            "structured_score": 1.0,
                            "knowledge_version": self.knowledge_version
                        })
                        seen_ids.add(obj["record_id"])

        if "அண்ணாமலை கலவை" in orig_q or "annamalai" in orig_q.lower():
            for obj in self.evidence_objects:
                if obj.get("evidence_id") == "AGRO_NUTRITION_IRON_CHLOROSIS":
                    if obj["record_id"] not in seen_ids:
                        results.append({
                            "chunk_id": obj.get("chunk_id"),
                            "parent_record_id": obj.get("record_id"),
                            "evidence_id": obj.get("evidence_id"),
                            "entity_id": obj.get("entity_id"),
                            "chunk_type": obj.get("chunk_type"),
                            "text": obj.get("recommendation"),
                            "metadata": {
                                "canonical_name": obj.get("canonical_name"),
                                "source_authority": obj.get("source_authority", 8)
                            },
                            "provenance": obj.get("provenance_chain", ["TNAU / Annamalai Guide"]),
                            "structured_score": 1.0,
                            "knowledge_version": self.knowledge_version
                        })
                        seen_ids.add(obj["record_id"])

        # 2. Chemical lookup
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

        # 3. ETL lookup for ETL intents
        req_action = parsed_context.get("requested_action")
        ent_ids = parsed_context.get("expanded_entity_ids", [])
        if req_action == "QUERY_ETL":
            for eid in ent_ids:
                etl_matches = self.retrieve_etl(eid, stage=parsed_context.get("crop_stage"))
                for m in etl_matches:
                    if m["record_id"] not in seen_ids:
                        results.append({
                            "chunk_id": m.get("chunk_id"),
                            "parent_record_id": m.get("record_id"),
                            "evidence_id": m.get("evidence_id"),
                            "entity_id": m.get("entity_id"),
                            "chunk_type": "ETL",
                            "text": f"ETL Rule for {m.get('canonical_name')}: {m.get('etl', {}).get('description', '')}",
                            "metadata": {
                                "canonical_name": m.get("canonical_name"),
                                "etl": m.get("etl"),
                                "source_authority": m.get("source_authority", 9)
                            },
                            "provenance": m.get("provenance_chain", ["ICAR-IIRR ETL Guidelines"]),
                            "structured_score": 1.0,
                            "knowledge_version": self.knowledge_version
                        })
                        seen_ids.add(m["record_id"])

        # 4. Entity-level direct match
        for eid in ent_ids:
            ent_matches = self.retrieve_by_entity(eid)
            for m in ent_matches:
                if m["record_id"] not in seen_ids:
                    results.append({
                        "chunk_id": m.get("chunk_id"),
                        "parent_record_id": m.get("record_id"),
                        "evidence_id": m.get("evidence_id"),
                        "entity_id": m.get("entity_id"),
                        "chunk_type": m.get("chunk_type"),
                        "text": m.get("recommendation") or m.get("description", ""),
                        "metadata": {
                            "canonical_name": m.get("canonical_name"),
                            "source_authority": m.get("source_authority", 8)
                        },
                        "provenance": m.get("provenance_chain", ["TNAU / ICAR Protection Guide"]),
                        "structured_score": 0.95,
                        "knowledge_version": self.knowledge_version
                    })
                    seen_ids.add(m["record_id"])

        return results[:top_k]
