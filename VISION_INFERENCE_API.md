# BHOOMI Vision Inference API Specification

**Model ID:** `bhoomi-mobilenetv3-large-16cls`  
**Endpoint:** `POST /farms/{farm_id}/diagnose`  
**Protocol:** FastAPI async over HTTP/JSON & Multipart Form-Data

---

## 1. Request Schema

```json
{
  "image_asset_url": "https://storage.bhoomi.agri/assets/sample_leaf.jpg",
  "crop_hint": "rice"
}
```

---

## 2. Response Schema (High Confidence >= 0.70)

```json
{
  "status": "success",
  "routing": {
    "decision": "DOWNSTREAM_ADVISORY",
    "gate_reason": null
  },
  "prediction": {
    "canonical_id": "DISEASE_003",
    "canonical_name": "Rice Blast",
    "confidence": 0.9240,
    "model_id": "bhoomi-mobilenetv3-large-16cls",
    "model_version": "1.0.0",
    "top_k_predictions": [
      {"canonical_id": "DISEASE_003", "canonical_name": "Rice Blast", "confidence": 0.9240},
      {"canonical_id": "DISEASE_004", "canonical_name": "Brown Spot", "confidence": 0.0520},
      {"canonical_id": "DISEASE_001", "canonical_name": "Bacterial Leaf Blight", "confidence": 0.0140}
    ]
  },
  "advisory": {
    "disease_severity": "MODERATE",
    "recommended_actions": "Apply Tricyclazole 75% WP @ 120 g/acre during early morning.",
    "citations": [
      {"source_id": "ICAR-POP-RICE-2024", "section": "Blast Management §4.2"}
    ]
  }
}
```

---

## 3. Response Schema (Low Confidence < 0.70)

```json
{
  "status": "escalated",
  "routing": {
    "decision": "ESCALATE_TO_KVK_OFFICER",
    "gate_reason": "confidence 0.58 < gate 0.70"
  },
  "prediction": {
    "canonical_id": "PEST_002",
    "canonical_name": "Brown Planthopper",
    "confidence": 0.5810,
    "model_id": "bhoomi-mobilenetv3-large-16cls"
  },
  "advisory": null,
  "spoken_summary": "I'm not sure — I've sent this to an expert."
}
```
