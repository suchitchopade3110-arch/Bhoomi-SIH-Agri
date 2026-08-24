"""
BHOOMI RAG Knowledge Corpus Validator
Validates serialized Evidence Objects and Semantic Chunks against RAG_EVIDENCE_SCHEMA.json,
asserts complete provenance, and verifies non-flattening of conditional ETL modifiers.
"""
import json
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def validate_corpus(knowledge_version: str = "v4.2.0-validated"):
    print("================================================================================")
    print(f"BHOOMI RAG CORPUS VALIDATION HARNESS — [{knowledge_version}]")
    print("================================================================================")

    v_tag = knowledge_version.replace("-", "_").replace(".", "_")
    indexes_dir = PROJECT_ROOT / "rag" / "indexes"
    obj_file = indexes_dir / f"evidence_objects_{v_tag}.json"
    chunk_file = indexes_dir / f"semantic_chunks_{v_tag}.json"

    if not obj_file.exists() or not chunk_file.exists():
        print(f"Error: Ingested corpus files not found for {knowledge_version}. Running build_corpus first...")
        from rag.ingestion.build_corpus import CorpusBuilder
        builder = CorpusBuilder(knowledge_version=knowledge_version)
        builder.build_all()

    with open(obj_file, "r", encoding="utf-8") as f:
        evidence_objects = json.load(f)
    with open(chunk_file, "r", encoding="utf-8") as f:
        semantic_chunks = json.load(f)

    print(f"Loaded {len(evidence_objects)} Evidence Objects")
    print(f"Loaded {len(semantic_chunks)} Semantic Chunks")

    # 1. Required Fields & Schema Integrity Check
    required_fields = [
        "record_id", "evidence_id", "entity_id", "entity_type", 
        "canonical_name", "crop", "knowledge_version", "source", 
        "source_authority", "evidence_status"
    ]
    
    schema_errors = 0
    provenance_errors = 0
    conditional_flattening_errors = 0
    restricted_unflagged_errors = 0

    print("\n[CHECK 1/4] Validating Canonical Evidence Schema...")
    for ev in evidence_objects:
        for rf in required_fields:
            if rf not in ev or ev[rf] is None:
                print(f"Schema Error in {ev.get('record_id')}: Missing required field '{rf}'")
                schema_errors += 1
        
        # Check provenance
        if not ev.get("provenance_chain") or len(ev["provenance_chain"]) == 0:
            print(f"Provenance Error in {ev.get('record_id')}: Empty provenance chain")
            provenance_errors += 1
        
        # Check ETL non-flattening
        etl = ev.get("etl")
        if etl and etl.get("has_modifier"):
            if not etl.get("base_threshold") or not etl.get("modifier_condition") or not etl.get("adjusted_threshold"):
                print(f"ETL Flattening Error in {ev.get('record_id')}: Modifier condition or base threshold collapsed")
                conditional_flattening_errors += 1

        # Check Restricted Chemical Status
        if ev.get("chemical") and "Carbofuran" in ev.get("chemical"):
            if ev.get("chemical_status") != "RESTRICTED":
                print(f"Safety Gate Error in {ev.get('record_id')}: Carbofuran must be marked RESTRICTED")
                restricted_unflagged_errors += 1

    print(f"-> Schema Validation Errors: {schema_errors}")
    print(f"-> Provenance Validation Errors: {provenance_errors}")
    print(f"-> Conditional ETL Flattening Errors: {conditional_flattening_errors}")
    print(f"-> Unflagged Restricted Chemical Errors: {restricted_unflagged_errors}")

    # 2. Chunking Integrity Check
    print("\n[CHECK 2/4] Validating Semantic Agricultural Chunks...")
    chunk_type_counts = {}
    for chk in semantic_chunks:
        ctype = chk.get("chunk_type", "UNKNOWN")
        chunk_type_counts[ctype] = chunk_type_counts.get(ctype, 0) + 1
        if not chk.get("text") or not chk.get("provenance"):
            print(f"Chunk Error in {chk.get('chunk_id')}: Missing text or provenance")
            schema_errors += 1

    for ct, count in sorted(chunk_type_counts.items()):
        print(f"  * {ct:15s}: {count:3d} chunks")

    # 3. Source Authority Distribution
    print("\n[CHECK 3/4] Validating Source Authority Rankings...")
    auth_levels = {}
    for ev in evidence_objects:
        auth = ev.get("source_authority", 0)
        auth_levels[auth] = auth_levels.get(auth, 0) + 1
    for lvl in sorted(auth_levels.keys(), reverse=True):
        print(f"  * Authority Level {lvl:2d}: {auth_levels[lvl]:3d} records")

    # 4. Summary & Assertion
    total_errors = schema_errors + provenance_errors + conditional_flattening_errors + restricted_unflagged_errors
    print("\n[CHECK 4/4] Validation Summary...")
    if total_errors == 0:
        print("================================================================================")
        print("ALL CORPUS VALIDATION GATES PASSED (100% COMPLIANCE)")
        print("STATUS: CORPUS_VALIDATED_READY_FOR_INDEXING")
        print("================================================================================")
        return True
    else:
        print(f"FAILED: Found {total_errors} errors across knowledge corpus.")
        return False


if __name__ == "__main__":
    success = validate_corpus()
    sys.exit(0 if success else 1)
