<div align="center">
  <img src="./assets/bhoomi-logo.png" alt="Bhoomi logo" width="280" />
  <h1>Bhoomi</h1>
  <p><strong>AI-Powered Farmer Companion</strong></p>
  <p>A voice-first, multimodal advisory that treats every farm as a continuous case — not a one-off chatbot.</p>
  <p><em>SIH25076 · Agriculture, Food Security & Rural Development</em></p>
</div>

---

## What Bhoomi is

Smallholder farmers get advice from scattered, low-trust channels and can't reach extension officers when it matters. Existing agri-chatbots answer one question and forget everything — no farm history, no land context, and a real risk of confidently wrong answers that cost a crop.

Bhoomi runs each farm as a living case file. A farmer onboards by speaking in their own language; every interaction updates a persistent record, feeds a transparent health score, and — when the AI is out of its depth — routes to a human expert with a pre-packaged summary instead of guessing.

The principle behind every feature: **every number is inspectable, and the system escalates to a human instead of fabricating an answer** — because in agriculture, a confidently wrong answer means real crop loss.

## The lifecycle

```
Voice onboarding → HITL land verification → FAO-56 resource plan → transparent health score → confidence-gated diagnosis → grounded 5-point advisory → closed-loop follow-up → expert escalation → scheme matching
```

## Core features

- **Voice-first regional interaction** — full spoken input/output; consequential numbers are read back before they're saved.
- **HITL land verification** — automated cadastral lookup is treated as an accelerator that often fails; a local officer confirms the boundary as the primary path.
- **FAO-56 resource planner** — daily irrigation (liters/day) and seed mass from $\text{ET}_0 \times K_c$ minus effective rainfall, with every input returned so "why this many liters?" has an answer.
- **Transparent health score** — a weighted six-sub-index rubric (not a black box); every point movement links to the input that caused it.
- **Confidence-gated diagnosis** — the image model answers only above a confidence threshold; below it, it escalates instead of risking a wrong call.
- **Grounded 5-point advisory (RAG)** — retrieves only from a curated, dated, cited corpus; on no relevant source it says so and escalates rather than fabricating.
- **Case timeline + closed-loop follow-up** — Improved / No Change / Got Worse check-ins that move the score and can auto-escalate.
- **Expert escalation** — auto-compiled Farm Case Summary routed to the nearest KVK agronomist.
- **Scheme discovery** — matches verified land + crop + category to active subsidies, each flagged with a `last_verified` date.

## The two hard rules

These are enforced in the orchestration layer, not left to prompt wording:

1. **Never answer below the confidence gate.** Low image confidence or low retrieval relevance → escalate, don't guess.
2. **Never fabricate on no-retrieval.** If the corpus has nothing relevant, the system states the limit and offers a human — it does not invent advice.

## Tech stack

| Layer | Choice |
| --- | --- |
| **Farmer app** | Flutter (Android) |
| **Officer & agronomist portals** | React + Vite + Tailwind + shadcn/ui + Leaflet |
| **Backend API** | Python + FastAPI (Pydantic) |
| **Data + geo + vectors** | PostgreSQL + PostGIS + pgvector |
| **Object storage** | S3-compatible (MinIO / R2), presigned uploads |
| **ASR / TTS (Tamil)** | Bhashini / AI4Bharat primary · Whisper fallback |
| **Image disease model** | PyTorch (ViT/CNN), bounded crop set, native confidence |
| **RAG** | LLM API + BGE-m3 embeddings via pgvector, cited output |
| **Weather** | Open-Meteo ($\text{ET}_0$, rainfall) |

Full rationale and alternatives: [docs/TECH_STACK.md](docs/TECH_STACK.md).

## Repository structure

```
bhoomi/
├── docs/                 # PRD, API contract, tech stack
├── apps/
│   ├── farmer-flutter/   # farmer app (voice-first, Android)
│   ├── officer-portal/   # HITL land verification (React + Leaflet)
│   └── agronomist-portal/# KVK case queue + resolve (React)
├── services/
│   ├── api/              # FastAPI backend + intelligence layer
│   │   └── app/
│   │       ├── routers/  # endpoints (mirrors the API contract)
│   │       ├── schemas/  # Pydantic request/response models
│   │       ├── db/       # models + migrations (PostGIS + pgvector)
│   │       └── domain/   # health score, confidence gate, RAG, escalation
│   └── ml/               # voice (ASR/TTS) + image model service
├── packages/
│   └── shared/           # enums + constants (single source of truth)
└── infra/                # docker-compose (postgres+postgis+pgvector, minio)
```

## Team & ownership

| Member | Owns |
| --- | --- |
| **Suchit Sachin Chopade** — *intelligence & integration* | `services/api/app/domain/` — health score, confidence gate, RAG pipeline, escalation; end-to-end integration |
| **Shreekumar** — *backend* | `services/api/` — FastAPI app, auth, CRUD, presigned uploads, deployment |
| **Tharun** — *voice + research* | `services/ml/` ASR/TTS (Bhashini/Whisper); RAG corpus curation + FAO-56/Kc data |
| **Shruthi** — *voice + database* | Voice endpoints; `services/api/app/db/` schema, PostGIS + pgvector, migrations |
| **Santheesh** — *frontend* | `apps/farmer-flutter/` — onboarding, summary, diagnose, timeline, follow-up |
| **Thaariha** — *frontend* | `apps/officer-portal/` + `apps/agronomist-portal/` |

## Getting started

*Phase 0 Skeleton — stubs, in-memory repository fallbacks, and OpenAPI schemas are wired.*

### Running the Backend API (Phase 0)

```bash
# 1. (Optional) Infrastructure - Postgres 16 (PostGIS + pgvector) & MinIO
cd infra
docker compose up -d
cd ..

# 2. Start Backend API
cd services/api
pip install -r requirements.txt
cp .env.example .env    # loads default stubs, feature flags, and thresholds

# Run the API with uvicorn (boots with in-memory repos if Postgres is offline)
uvicorn app.main:app --reload --port 8000
```

- **Interactive Swagger / OpenAPI docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc API Explorer**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health check probe**: `GET http://localhost:8000/health`

### Running Backend Tests

```bash
cd services/api
pytest -v
```

Feature flags (in `.env`) control adapter modes:
- `LAND_API_MODE = mock | live`
- `DIAGNOSIS_MODEL = real | stub`
- `CONFIDENCE_GATE = 0.70`
- `RAG_RELEVANCE_THRESHOLD = 0.35`


## Documentation

- [docs/PRD.md](docs/PRD.md) — product requirements, including the full health-score model (§7).
- [docs/API_CONTRACT.md](docs/API_CONTRACT.md) — REST contract; enums and entities mirror the PRD.
- [docs/TECH_STACK.md](docs/TECH_STACK.md) — stack choices, rationale, and alternatives.

---

<div align="center">
  <sub>Bhoomi — the earth. Every number inspectable; escalate, don't guess.</sub>
</div>
