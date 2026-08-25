# BHOOMI — Production Data Contract
**Document Version:** 1.2.0  
**Dataset Version:** `v4.1.0-validated`  
**Git Baseline:** `7154607`  
**Author:** Tharun BL (Agricultural Research + Voice Research Lead)  
**Date:** August 2026

---

## 1. System Integration Flow

The BHOOMI Architecture maintains strict layered boundaries:

$$\text{Voice Stream (ASR)} \xrightarrow{\text{Contract 1}} \text{Intent / Entity Parser} \xrightarrow{\text{Contract 2}} \text{RAG Retrieval Layer} \xrightarrow{\text{Contract 3}} \text{Decision Engine} \xrightarrow{\text{Contract 4}} \text{TTS Stream}$$

```
┌─────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐       ┌──────────────────┐
│  Voice Stream   │ ───▶  │ Intent / Entity NLU  │ ───▶  │  RAG Retrieval DB   │ ───▶  │ Decision Engine  │
│ (IndicConformer)│       │ (Slot & Dialect Map) │       │   (BGE-M3 Dense)     │       │ (ETL/Safety Gate)│
└─────────────────┘       └──────────────────────┘       └──────────────────────┘       └──────────────────┘
                                                                                                  │
                                                                                                  ▼
                                                                                        ┌──────────────────┐
                                                                                        │ Indic-TTS Audio  │
                                                                                        │ (16kHz Opus Out) │
                                                                                        └──────────────────┘
```

---

## 2. Interface Contracts

### Contract 1: Voice Input $\rightarrow$ NLU Engine (`VoiceTurnRequest`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "VoiceTurnRequest",
  "type": "object",
  "required": ["session_id", "audio_chunk_base64", "language_code", "is_final"],
  "properties": {
    "session_id": { "type": "string", "format": "uuid" },
    "audio_chunk_base64": { "type": "string" },
    "sample_rate": { "type": "integer", "enum": [8000, 16000, 48000], "default": 16000 },
    "language_code": { "type": "string", "enum": ["ta-IN", "en-IN"], "default": "ta-IN" },
    "is_final": { "type": "boolean" },
    "barge_in_active": { "type": "boolean", "default": false }
  }
}
```

### Contract 2: NLU Engine $\rightarrow$ Retrieval Layer (`RetrievalQuery`)
```json
{
  "title": "RetrievalQuery",
  "type": "object",
  "required": ["query_text", "detected_intent", "entities"],
  "properties": {
    "query_text": { "type": "string" },
    "detected_intent": {
      "type": "string",
      "enum": [
        "IDENTIFY_PEST", "IDENTIFY_DISEASE", "DIAGNOSE_SYMPTOM", "QUERY_ETL",
        "RECOMMEND_CHEMICAL", "QUERY_DOSAGE", "QUERY_CULTURAL_CONTROL",
        "QUERY_REGULATORY_STATUS", "ASK_CLARIFICATION"
      ]
    },
    "entities": {
      "type": "object",
      "properties": {
        "crop": { "type": "string", "default": "Rice" },
        "crop_stage": { "type": "string", "enum": ["nursery", "vegetative", "tillering", "booting", "flowering", "milking", "harvest", null] },
        "pest_name": { "type": "string" },
        "disease_name": { "type": "string" },
        "symptom_tokens": { "type": "array", "items": { "type": "string" } },
        "chemical_mentioned": { "type": "string" }
      }
    },
    "similarity_threshold": { "type": "number", "default": 0.60 }
  }
}
```

### Contract 3: Retrieval Layer $\rightarrow$ Decision Engine (`AdvisoryContext`)
```json
{
  "title": "AdvisoryContext",
  "type": "object",
  "required": ["doc_id", "crop", "canonical_name", "etl_evidence", "severity_tiers", "chemical_prescriptions"],
  "properties": {
    "doc_id": { "type": "string", "pattern": "^DOC-(PEST|DIS)-[0-9]{3}$" },
    "crop": { "type": "string" },
    "canonical_name": { "type": "string" },
    "scientific_name": { "type": "string" },
    "authority_level": { "type": "string", "enum": ["Tier 1 (ICAR / IRRI / TNAU / DPPQS)"] },
    "etl_evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["record_id", "crop_stage", "threshold"],
        "properties": {
          "record_id": { "type": "string", "pattern": "^ETL-[0-9]{3}$" },
          "crop_stage": { "type": "string" },
          "threshold": {
            "type": "object",
            "required": ["base"],
            "properties": {
              "base": { "type": "object", "required": ["value_min", "unit"] },
              "modifier": { "type": ["object", "null"] }
            }
          }
        }
      }
    },
    "chemical_prescriptions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["chemical_id", "active_ingredient", "regulatory_status", "formulation", "dose_per_ha", "phi_days"],
        "properties": {
          "chemical_id": { "type": "string", "pattern": "^CHEM-[0-9]{3}$" },
          "active_ingredient": { "type": "string" },
          "regulatory_status": { "type": "string", "enum": ["VERIFIED_CURRENT", "RESTRICTED", "HISTORICAL_SOURCE_ONLY", "UNVERIFIED"] },
          "formulation": { "type": "string" },
          "dose_per_ha": { "type": "string" },
          "phi_days": { "type": "integer" }
        }
      }
    }
  }
}
```

### Contract 4: Decision Engine $\rightarrow$ Voice Output (`AdvisoryDecisionResponse`)
```json
{
  "title": "AdvisoryDecisionResponse",
  "type": "object",
  "required": ["decision_id", "session_id", "confidence_level", "tamil_response_text", "safety_gate_passed", "evidence_trace"],
  "properties": {
    "decision_id": { "type": "string", "format": "uuid" },
    "session_id": { "type": "string", "format": "uuid" },
    "confidence_level": { "type": "string", "enum": ["HIGH_CONFIDENCE", "MEDIUM_CONFIDENCE", "LOW_CONFIDENCE"] },
    "action_type": { "type": "string", "enum": ["DIRECT_ADVISORY", "ASK_CLARIFYING_QUESTION", "ESCALATE_TO_KVK_OFFICER"] },
    "tamil_response_text": { "type": "string" },
    "audio_stream_url": { "type": "string" },
    "safety_gate_passed": { "type": "boolean" },
    "restricted_chemicals_flagged": { "type": "array", "items": { "type": "string" } },
    "evidence_trace": {
      "type": "object",
      "required": ["dataset_version", "doc_id", "evidence_ids", "source_url"],
      "properties": {
        "dataset_version": { "type": "string", "default": "v4.1.0-validated" },
        "doc_id": { "type": "string" },
        "evidence_ids": { "type": "array", "items": { "type": "string" } },
        "source_url": { "type": "string" }
      }
    }
  }
}
```

---

## 3. Invariants & Prohibited Transformations

1. **Threshold Preservation**: The decision engine MUST NOT calculate average values across `base` and `modifier`.
2. **Chemical Status Immutability**: No client request or LLM prompt may transform `RESTRICTED` into an unrestricted advice string.
3. **Low Confidence Gate**: Any query with confidence $< 0.70$ MUST trigger `ASK_CLARIFYING_QUESTION` or officer escalation; zero hallucinated prescriptions permitted.
