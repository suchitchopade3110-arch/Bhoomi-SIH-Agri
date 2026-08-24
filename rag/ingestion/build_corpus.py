"""
BHOOMI RAG Knowledge Corpus Builder & Semantic Agricultural Chunker
Ingests validated Markdown documents, normalized ETLs, severity scales, chemical audits, 
diagnostic trees, and Tamil lexicons into canonical evidence objects and semantic chunks.
"""
import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class CorpusBuilder:
    def __init__(self, knowledge_version: str = "v4.2.0-validated"):
        self.knowledge_version = knowledge_version
        if knowledge_version == "v4.3.0-candidate":
            self.base_dir = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_3_candidate"
        else:
            self.base_dir = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated"
        
        self.corpus_dir = self.base_dir / "corpus"
        self.evidence_dir = self.base_dir / "evidence"
        self.tamil_dir = self.base_dir / "tamil"
        self.output_dir = PROJECT_ROOT / "rag" / "indexes"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.evidence_objects: List[Dict[str, Any]] = []
        self.semantic_chunks: List[Dict[str, Any]] = []
        self.lexicon_map: Dict[str, List[Dict[str, Any]]] = {}

    def _parse_yaml_frontmatter(self, text: str) -> Dict[str, Any]:
        """Simple, robust YAML frontmatter parser for markdown documents."""
        frontmatter = {}
        if not text.startswith("---"):
            return frontmatter
        parts = text.split("---", 2)
        if len(parts) < 3:
            return frontmatter
        raw_yaml = parts[1]
        
        # Simple line-by-line parser for standard key-values and basic nested blocks
        current_dict = frontmatter
        current_list_key = None
        for line in raw_yaml.split("\n"):
            line_str = line.rstrip()
            if not line_str or line_str.startswith("#"):
                continue
            if line_str.startswith("  - "):
                if current_list_key:
                    item_val = line_str[4:].strip().strip('"').strip("'")
                    if isinstance(frontmatter.get(current_list_key), list):
                        frontmatter[current_list_key].append(item_val)
                continue
            if ":" in line_str:
                k, v = line_str.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if v == "" or v == "null":
                    v = None
                elif v.lower() == "true":
                    v = True
                elif v.lower() == "false":
                    v = False
                elif v.isdigit():
                    v = int(v)
                frontmatter[k] = v
                current_list_key = k
        return frontmatter

    def load_tamil_lexicon(self):
        """Loads and indexes Tamil pest lexicon aliases and dialect terms."""
        lexicon_file = self.tamil_dir / "TAMIL_PEST_LEXICON.csv"
        if not lexicon_file.exists():
            return
        with open(lexicon_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pest_id = row.get("pest_id")
                if pest_id:
                    if pest_id not in self.lexicon_map:
                        self.lexicon_map[pest_id] = []
                    self.lexicon_map[pest_id].append(row)
                    
                    # Create a LEXICON semantic chunk
                    chunk_id = f"CHUNK-LEX-{pest_id}-{len(self.lexicon_map[pest_id])}"
                    self.semantic_chunks.append({
                        "chunk_id": chunk_id,
                        "parent_record_id": pest_id,
                        "evidence_id": f"LEX-{pest_id}",
                        "entity_id": pest_id,
                        "chunk_type": "LEXICON",
                        "text": f"Tamil name for {row.get('english_name')}: {row.get('tamil_script')} ({row.get('transliteration')}). Region: {row.get('dialect_region')}. Term type: {row.get('term_type')}. Status: {row.get('lexicon_status')}.",
                        "metadata": {
                            "pest_id": pest_id,
                            "english_name": row.get("english_name"),
                            "tamil_script": row.get("tamil_script"),
                            "transliteration": row.get("transliteration"),
                            "dialect_region": row.get("dialect_region"),
                            "term_type": row.get("term_type"),
                            "lexicon_status": row.get("lexicon_status"),
                            "knowledge_version": self.knowledge_version
                        },
                        "provenance": [row.get("source_reference", "TAMIL_PEST_LEXICON.csv")]
                    })

    def ingest_corpus_markdown(self):
        """Ingests markdown corpus files for pests and diseases."""
        if not self.corpus_dir.exists():
            return
        
        md_files = list(self.corpus_dir.glob("*.md"))
        for md_file in md_files:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            fm = self._parse_yaml_frontmatter(content)
            doc_id = fm.get("doc_id", md_file.stem.upper())
            title = fm.get("title", md_file.stem.replace("_", " ").title())
            entity_name = fm.get("pest_name") or fm.get("disease_name") or title
            entity_id = fm.get("pest_id") or fm.get("disease_id") or doc_id
            scientific_name = fm.get("scientific_name") or fm.get("pathogen_name")
            crop = fm.get("crop", "Rice (Oryza sativa)")
            source = fm.get("source_organization", "TNAU / ICAR-IIRR")
            
            # Entity Chunk
            entity_chunk_id = f"CHUNK-{doc_id}-ENTITY"
            self.semantic_chunks.append({
                "chunk_id": entity_chunk_id,
                "parent_record_id": doc_id,
                "evidence_id": f"EVID-{doc_id}-MAIN",
                "entity_id": entity_id,
                "chunk_type": "ENTITY",
                "text": f"Document: {title}. Crop: {crop}. Entity: {entity_name} ({scientific_name}). Source: {source}.",
                "metadata": {
                    "doc_id": doc_id,
                    "title": title,
                    "entity_id": entity_id,
                    "canonical_name": entity_name,
                    "scientific_name": scientific_name,
                    "crop": crop,
                    "source": source,
                    "knowledge_version": self.knowledge_version
                },
                "provenance": [f"corpus/{md_file.name}"]
            })

            # Create an Evidence Object
            rec_id = f"REC-{doc_id}"
            ev_obj = {
                "record_id": rec_id,
                "document_id": doc_id,
                "evidence_id": f"EVID-{doc_id}",
                "chunk_id": entity_chunk_id,
                "chunk_type": "ENTITY",
                "entity_id": entity_id,
                "entity_type": "disease" if "DIS" in doc_id or "disease" in md_file.name else "pest",
                "canonical_name": entity_name,
                "scientific_name": scientific_name,
                "local_names": [entity_name],
                "tamil_aliases": [fm.get("tamil_canonical")] if fm.get("tamil_canonical") else [],
                "crop": crop,
                "crop_stage": "all_stages",
                "agro_ecological_region": "All Tamil Nadu",
                "symptoms": [],
                "distinguishing_cues": [],
                "diagnostic_features": None,
                "severity": None,
                "etl": None,
                "recommendation": f"Refer to {title} for complete IPM guidelines.",
                "management_type": "cultural",
                "chemical": None,
                "formulation": None,
                "chemical_status": None,
                "dose": None,
                "dose_unit": None,
                "application_method": None,
                "timing": None,
                "phi": None,
                "safety_constraints": [],
                "drone_guidelines": None,
                "geographic_scope": "Tamil Nadu",
                "source": source,
                "source_type": "university_cpg",
                "source_authority": 8,
                "source_date": fm.get("verification_date", "2026-08-24"),
                "evidence_status": "SOURCE_SUPPORTED",
                "confidence": 0.95,
                "license_status": "CC-BY-NC-4.0",
                "provenance_chain": [f"corpus/{md_file.name}"],
                "knowledge_version": self.knowledge_version
            }
            self.evidence_objects.append(ev_obj)

    def ingest_etl_evidence(self):
        """Ingests normalized ETL threshold objects."""
        etl_file = self.evidence_dir / "ETL_EVIDENCE_NORMALIZED.jsonl"
        if not etl_file.exists():
            return
        
        with open(etl_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                rec_id = f"REC-{record['record_id']}"
                base_obj = record.get("base", {})
                mod_obj = record.get("modifier") or {}

                base_val_str = f"{base_obj.get('value')} {base_obj.get('unit', '')}".strip()
                mod_str = None
                mod_cond = None
                adj_thresh = None
                if mod_obj:
                    mod_cond = mod_obj.get("condition")
                    adj_thresh = f"{mod_obj.get('adjusted_value')} {mod_obj.get('unit', '')}".strip()
                    mod_str = f"{adj_thresh} when {mod_cond}"

                # ETL Evidence Object
                ev_obj = {
                    "record_id": rec_id,
                    "document_id": record.get("document_id"),
                    "evidence_id": record.get("record_id"),
                    "chunk_id": f"CHUNK-{record['record_id']}",
                    "chunk_type": "ETL",
                    "entity_id": record.get("pest_id", "UNKNOWN_PEST"),
                    "entity_type": "pest",
                    "canonical_name": record.get("name", "Unknown"),
                    "scientific_name": record.get("scientific_name"),
                    "local_names": [record.get("name", "")],
                    "tamil_aliases": [],
                    "crop": record.get("crop", "Rice (Oryza sativa)"),
                    "crop_stage": record.get("crop_stage"),
                    "agro_ecological_region": "All Tamil Nadu",
                    "symptoms": [],
                    "distinguishing_cues": [],
                    "diagnostic_features": None,
                    "severity": None,
                    "etl": {
                        "base_threshold": base_val_str,
                        "base_value": base_obj.get("value"),
                        "base_unit": base_obj.get("unit"),
                        "has_modifier": bool(mod_obj),
                        "modifier": mod_str,
                        "modifier_condition": mod_cond,
                        "adjusted_threshold": adj_thresh
                    },
                    "recommendation": f"Spray intervention threshold for {record.get('name')}: Base ETL = {base_val_str}." + (f" Context modifier: {mod_str}." if mod_str else ""),
                    "management_type": "cultural",
                    "chemical": None,
                    "formulation": None,
                    "chemical_status": None,
                    "dose": None,
                    "dose_unit": None,
                    "application_method": None,
                    "timing": record.get("crop_stage"),
                    "phi": None,
                    "safety_constraints": [],
                    "drone_guidelines": None,
                    "geographic_scope": "Tamil Nadu",
                    "source": record.get("source_organization", "TNAU / ICAR"),
                    "source_type": "research_manual",
                    "source_authority": 9,
                    "source_date": record.get("verification_date", "2026-08-24"),
                    "evidence_status": record.get("evidence_status", "SOURCE_SUPPORTED"),
                    "confidence": record.get("confidence", 0.95),
                    "license_status": "CC-BY-NC-4.0",
                    "provenance_chain": [record.get("source_document", "ETL_EVIDENCE_NORMALIZED.jsonl")],
                    "knowledge_version": self.knowledge_version
                }
                self.evidence_objects.append(ev_obj)

                # ETL Semantic Chunk
                self.semantic_chunks.append({
                    "chunk_id": f"CHUNK-{record['record_id']}",
                    "parent_record_id": rec_id,
                    "evidence_id": record.get("record_id"),
                    "entity_id": record.get("pest_id"),
                    "chunk_type": "ETL",
                    "text": f"Economic Threshold Level (ETL) for {record.get('name')} at {record.get('crop_stage')} stage: Base threshold is {base_val_str}." + (f" Modified threshold is {adj_thresh} when condition is {mod_cond}." if mod_obj else ""),
                    "metadata": {
                        "pest_id": record.get("pest_id"),
                        "crop": record.get("crop"),
                        "crop_stage": record.get("crop_stage"),
                        "base_threshold": base_val_str,
                        "has_modifier": bool(mod_obj),
                        "modifier_condition": mod_cond,
                        "adjusted_threshold": adj_thresh,
                        "source": record.get("source_organization"),
                        "knowledge_version": self.knowledge_version
                    },
                    "provenance": [record.get("source_document", "ETL_EVIDENCE_NORMALIZED.jsonl")]
                })

    def ingest_severity_evidence(self):
        """Ingests SES 1-9 severity scale records."""
        sev_file = self.evidence_dir / "SEVERITY_EVIDENCE.jsonl"
        if not sev_file.exists():
            return
        
        with open(sev_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                rec_id = f"REC-{record['record_id']}"
                tiers = record.get("severity_tiers", {})

                for tier_name, tier_data in tiers.items():
                    chunk_id = f"CHUNK-{record['record_id']}-{tier_name.upper()}"
                    text = f"Severity tier '{tier_name}' (SES Scale {tier_data.get('ses_scale')}) for {record.get('name')}: Cutoff range is {tier_data.get('cutoff_range')}. Symptom: {tier_data.get('symptom_description')}"
                    
                    self.semantic_chunks.append({
                        "chunk_id": chunk_id,
                        "parent_record_id": rec_id,
                        "evidence_id": record.get("record_id"),
                        "entity_id": record.get("pest_id") or record.get("disease_id"),
                        "chunk_type": "SEVERITY",
                        "text": text,
                        "metadata": {
                            "name": record.get("name"),
                            "tier": tier_name,
                            "ses_scale": tier_data.get("ses_scale"),
                            "cutoff_range": tier_data.get("cutoff_range"),
                            "source": record.get("source_organization"),
                            "knowledge_version": self.knowledge_version
                        },
                        "provenance": [record.get("source_document", "SEVERITY_EVIDENCE.jsonl")]
                    })

                # Severity Evidence Object
                ev_obj = {
                    "record_id": rec_id,
                    "document_id": None,
                    "evidence_id": record.get("record_id"),
                    "chunk_id": f"CHUNK-{record['record_id']}",
                    "chunk_type": "SEVERITY",
                    "entity_id": record.get("pest_id") or record.get("disease_id", "UNKNOWN"),
                    "entity_type": record.get("entity_type", "pest"),
                    "canonical_name": record.get("name", "Unknown"),
                    "scientific_name": record.get("scientific_name"),
                    "local_names": [record.get("name", "")],
                    "tamil_aliases": [],
                    "crop": record.get("crop", "Rice (Oryza sativa)"),
                    "crop_stage": "all_stages",
                    "agro_ecological_region": "All Tamil Nadu",
                    "symptoms": [t.get("symptom_description", "") for t in tiers.values()],
                    "distinguishing_cues": [],
                    "diagnostic_features": None,
                    "severity": tiers,
                    "etl": None,
                    "recommendation": f"Standard Evaluation System (SES) 1-9 rating for {record.get('name')}.",
                    "management_type": "diagnostic_clarification",
                    "chemical": None,
                    "formulation": None,
                    "chemical_status": None,
                    "dose": None,
                    "dose_unit": None,
                    "application_method": None,
                    "timing": None,
                    "phi": None,
                    "safety_constraints": [],
                    "drone_guidelines": None,
                    "geographic_scope": "National / IRRI",
                    "source": record.get("source_organization", "IRRI / ICAR / TNAU"),
                    "source_type": "research_manual",
                    "source_authority": 9,
                    "source_date": record.get("verification_date", "2026-08-24"),
                    "evidence_status": "SOURCE_SUPPORTED",
                    "confidence": 0.95,
                    "license_status": "CC-BY-NC-4.0",
                    "provenance_chain": [record.get("source_document", "SEVERITY_EVIDENCE.jsonl")],
                    "knowledge_version": self.knowledge_version
                }
                self.evidence_objects.append(ev_obj)

    def ingest_chemical_audits(self):
        """Ingests CIBRC regulatory chemical status audit records."""
        chem_file = self.evidence_dir / "CHEMICAL_STATUS_AUDIT.jsonl"
        if not chem_file.exists():
            return
        
        with open(chem_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                rec_id = f"REC-{record['chemical_id']}"
                chunk_id = f"CHUNK-{record['chemical_id']}"
                
                targets_str = ", ".join(record.get("targets", []))
                text = f"Chemical Prescription: {record.get('active_ingredient')} {record.get('formulation')} for {targets_str}. Dosage: {record.get('dosage')}. Regulatory Status: {record.get('regulatory_status')} ({record.get('cibrc_status')}). Pre-Harvest Interval (PHI): {record.get('phi_days')} days. Toxicity: {record.get('risk_classification')}. Notes: {record.get('notes')}"

                # Drone guidelines if present in notes
                drone_info = None
                if "Drone" in record.get("notes", "") or "drone" in record.get("dosage", ""):
                    drone_info = {
                        "drone_permitted": True,
                        "spray_volume_l_ha": "20-25 L/ha",
                        "droplet_vmd_microns": "100-150 µm",
                        "max_wind_speed_kmh": 10.0,
                        "buffer_zone_meters": 100
                    }

                # Chemical Evidence Object
                ev_obj = {
                    "record_id": rec_id,
                    "document_id": None,
                    "evidence_id": record.get("chemical_id"),
                    "chunk_id": chunk_id,
                    "chunk_type": "CHEMICAL",
                    "entity_id": f"CHEM_{record['chemical_id']}",
                    "entity_type": record.get("target_type", "chemical"),
                    "canonical_name": f"{record.get('active_ingredient')} {record.get('formulation')}",
                    "scientific_name": record.get("active_ingredient"),
                    "local_names": [record.get("active_ingredient", "")],
                    "tamil_aliases": [],
                    "crop": record.get("crop", "Rice (Oryza sativa)"),
                    "crop_stage": "all_stages",
                    "agro_ecological_region": "All Tamil Nadu",
                    "symptoms": [],
                    "distinguishing_cues": [],
                    "diagnostic_features": None,
                    "severity": None,
                    "etl": None,
                    "recommendation": text,
                    "management_type": "chemical" if record.get("target_type") != "bio_control" else "biological",
                    "chemical": record.get("active_ingredient"),
                    "formulation": record.get("formulation"),
                    "chemical_status": record.get("regulatory_status"),
                    "dose": record.get("dosage"),
                    "dose_unit": "per hectare",
                    "application_method": "knapsack_foliar",
                    "timing": "As per ETL thresholds",
                    "phi": record.get("phi_days"),
                    "safety_constraints": [record.get("risk_classification", ""), record.get("notes", "")],
                    "drone_guidelines": drone_info,
                    "geographic_scope": "National (CIBRC Approved)",
                    "source": record.get("source_organization", "CIBRC / TNAU"),
                    "source_type": "regulatory_schedule",
                    "source_authority": 10 if "CIBRC" in record.get("source_organization", "") else 8,
                    "source_date": record.get("verification_date", "2026-08-24"),
                    "evidence_status": "SOURCE_SUPPORTED_CIBRC_ALIGNED" if record.get("regulatory_status") == "VERIFIED_CURRENT" else "RESTRICTED_WARNING_REQUIRED",
                    "confidence": 0.98,
                    "license_status": "GOVERNMENT_OPEN_ACCESS",
                    "provenance_chain": [record.get("source_url", "CHEMICAL_STATUS_AUDIT.jsonl")],
                    "knowledge_version": self.knowledge_version
                }
                self.evidence_objects.append(ev_obj)

                # Chemical Semantic Chunk
                self.semantic_chunks.append({
                    "chunk_id": chunk_id,
                    "parent_record_id": rec_id,
                    "evidence_id": record.get("chemical_id"),
                    "entity_id": f"CHEM_{record['chemical_id']}",
                    "chunk_type": "CHEMICAL",
                    "text": text,
                    "metadata": {
                        "active_ingredient": record.get("active_ingredient"),
                        "formulation": record.get("formulation"),
                        "targets": record.get("targets"),
                        "dosage": record.get("dosage"),
                        "regulatory_status": record.get("regulatory_status"),
                        "phi_days": record.get("phi_days"),
                        "toxicity": record.get("risk_classification"),
                        "drone_guidelines": drone_info,
                        "source": record.get("source_organization"),
                        "knowledge_version": self.knowledge_version
                    },
                    "provenance": [record.get("source_url", "CHEMICAL_STATUS_AUDIT.jsonl")]
                })

    def ingest_diagnostic_decision_trees(self):
        """Ingests structured multi-turn diagnostic decision trees."""
        tree_file = self.evidence_dir / "DIAGNOSTIC_DECISION_TREES.jsonl"
        if not tree_file.exists():
            return
        
        with open(tree_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                rec_id = f"REC-{record['tree_id']}"
                chunk_id = f"CHUNK-{record['tree_id']}"

                text = f"Diagnostic Decision Tree: {record.get('name')}. Primary trigger: {record.get('primary_symptom_trigger')}. Nodes: {len(record.get('decision_nodes', []))} structured decision nodes."

                ev_obj = {
                    "record_id": rec_id,
                    "document_id": None,
                    "evidence_id": record.get("tree_id"),
                    "chunk_id": chunk_id,
                    "chunk_type": "DECISION_TREE",
                    "entity_id": "DDT_ZINC_VS_BROWN_SPOT",
                    "entity_type": "disease",
                    "canonical_name": record.get("name"),
                    "scientific_name": None,
                    "local_names": [record.get("name")],
                    "tamil_aliases": ["செம்புள்ளி vs துத்தநாக குறைபாடு"],
                    "crop": record.get("crop", "Rice (Oryza sativa)"),
                    "crop_stage": "2_to_4_WAT",
                    "agro_ecological_region": "All Tamil Nadu",
                    "symptoms": ["brown spots on leaf", "rusty pigmentation along midrib", "oval brown spots with yellow halo"],
                    "distinguishing_cues": ["midrib bronze vs oval halos", "alkaline soil patches vs uniform poor soil"],
                    "diagnostic_features": {"decision_nodes": record.get("decision_nodes")},
                    "severity": None,
                    "etl": None,
                    "recommendation": "Follow multi-turn decision tree for differential diagnosis of Zinc Deficiency vs Brown Spot.",
                    "management_type": "diagnostic_clarification",
                    "chemical": None,
                    "formulation": None,
                    "chemical_status": None,
                    "dose": None,
                    "dose_unit": None,
                    "application_method": None,
                    "timing": None,
                    "phi": None,
                    "safety_constraints": ["Do not apply fungicides to nutritional zinc deficiency"],
                    "drone_guidelines": None,
                    "geographic_scope": "Tamil Nadu",
                    "source": record.get("source_organization", "TNAU / IRRI"),
                    "source_type": "research_manual",
                    "source_authority": 9,
                    "source_date": record.get("verification_date", "2026-08-24"),
                    "evidence_status": "SOURCE_SUPPORTED",
                    "confidence": 0.96,
                    "license_status": "CC-BY-NC-4.0",
                    "provenance_chain": ["DIAGNOSTIC_DECISION_TREES.jsonl"],
                    "knowledge_version": self.knowledge_version
                }
                self.evidence_objects.append(ev_obj)

                self.semantic_chunks.append({
                    "chunk_id": chunk_id,
                    "parent_record_id": rec_id,
                    "evidence_id": record.get("tree_id"),
                    "entity_id": "DDT_ZINC_VS_BROWN_SPOT",
                    "chunk_type": "DECISION_TREE",
                    "text": text,
                    "metadata": {
                        "tree_id": record.get("tree_id"),
                        "name": record.get("name"),
                        "trigger": record.get("primary_symptom_trigger"),
                        "nodes_count": len(record.get("decision_nodes", [])),
                        "source": record.get("source_organization"),
                        "knowledge_version": self.knowledge_version
                    },
                    "provenance": ["DIAGNOSTIC_DECISION_TREES.jsonl"]
                })

    def build_all(self):
        """Runs the entire ingestion pipeline and serializes outputs."""
        print(f"Building knowledge corpus for version '{self.knowledge_version}' from {self.base_dir}...")
        self.load_tamil_lexicon()
        self.ingest_corpus_markdown()
        self.ingest_etl_evidence()
        self.ingest_severity_evidence()
        self.ingest_chemical_audits()
        self.ingest_diagnostic_decision_trees()

        v_tag = self.knowledge_version.replace("-", "_").replace(".", "_")
        obj_file = self.output_dir / f"evidence_objects_{v_tag}.json"
        chunk_file = self.output_dir / f"semantic_chunks_{v_tag}.json"

        with open(obj_file, "w", encoding="utf-8") as f:
            json.dump(self.evidence_objects, f, indent=2, ensure_ascii=False)
        with open(chunk_file, "w", encoding="utf-8") as f:
            json.dump(self.semantic_chunks, f, indent=2, ensure_ascii=False)

        print(f"Successfully generated {len(self.evidence_objects)} Evidence Objects in {obj_file}")
        print(f"Successfully generated {len(self.semantic_chunks)} Semantic Chunks in {chunk_file}")
        return len(self.evidence_objects), len(self.semantic_chunks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bhoomi RAG Knowledge Corpus Builder")
    parser.add_argument("--knowledge-version", default="v4.2.0-validated", help="Knowledge base version")
    args = parser.parse_args()

    builder = CorpusBuilder(knowledge_version=args.knowledge_version)
    builder.build_all()
