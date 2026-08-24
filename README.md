<div align="center">
  <img src="./assets/bhoomi-logo.png" alt="Bhoomi logo" width="280" />
  <h1>Bhoomi — AI-Powered Farmer Companion</h1>
  <p>Voice-first, multimodal crop advisory that treats every farm as a continuous case file.</p>
  <p><em>Smart India Hackathon · SIH25076 (default) · SIH26131 (feature-flagged)</em></p>
</div>

---

## What this is

Smallholder farmers get advice from scattered channels and can't reach an extension officer when it matters. A generic agri-chatbot answers one question, forgets the farm, and will confidently invent an answer — which costs a crop.

Bhoomi keeps a persistent record per farm: voice onboarding, a transparent health score, confidence-gated image diagnosis, grounded advisory retrieved from a dated corpus, closed-loop follow-up, and escalation to a KVK agronomist with a pre-compiled case bundle.

### The two hard rules

Both are enforced in orchestration code, not in prompt wording:

1. **Never answer below the confidence gate.** Image confidence under `CONFIDENCE_GATE` → escalate.
2. **Never fabricate on no-retrieval.** No corpus chunk above `RAG_RELEVANCE_THRESHOLD` → say so and offer a human.

---

## Repository layout

```
Bhoomi-SIH-Agri/
├── AGENTS.md                  # pinned context rules for coding agents
├── CLAUDE.md
├── apps/
│   ├── farmer_app/            # Flutter farmer app (Riverpod + go_router + dio)
│   ├── kvk_portal/            # agronomist case queue/resolve (React + Vite + Tailwind)
│   └── officer_portal/        # land review portal (React + Vite + Tailwind + Leaflet)
├── services/
│   ├── api/                   # FastAPI backend — the whole intelligence layer
│   └── ml/                    # inference microservice — scaffold only, files are empty
├── packages/shared/           # legacy Phase-0 enum/constant scaffold (see caveats)
├── data/
│   ├── external/Dataset_v4/   # raw pest dataset snapshot (ground truth, do not edit)
│   └── curated/Dataset_v4_validated/  # staged pest corpus, manifests, Tamil lexicon
├── docs/                      # PRD, contracts, specs, decision records
├── infra/                     # docker-compose: Postgres 16 (pgvector) + MinIO
└── .github/workflows/         # frontend + mobile CI
```

### Backend internals (`services/api/app/`)

Strict one-way layering, per `AGENTS.md`:

```
api/v1  →  services  →  domain / repositories  →  adapters
```

- `api/v1/` — routers only. HTTP in, HTTP out.
- `services/` — orchestration: `health/`, `gate/`, `rag/`, `escalation/`, `alerts/`, plus per-entity services.
- `domain/` — pure logic and constants: `health/score.py`, `gate/decide.py`, `rag/` (chunking, similarity, prompt), `fao56.py`, `queue.py`, `routing.py`. No I/O.
- `repositories/` — SQLAlchemy 2.0 async persistence, with an in-memory fallback implementation.
- `ports/` — typed Protocols: `weather`, `llm`, `embeddings`, `image_diagnosis`, `asr_tts`, `storage`, `roster`.
- `adapters/` — real and stub implementations per port, selected in `adapters/dependencies.py` from config. No call site imports a concrete adapter.

---

## The health score

Deterministic Python, not a model call. Six sub-indices, weights summing to 1.0 (asserted at import time in `domain/health/constants.py`):

| Sub-index | Weight |
|---|---|
| `environmental_suitability` | 0.20 |
| `resource_adequacy` | 0.15 |
| `crop_stage_progression` | 0.15 |
| `active_problem_load` | **0.30** |
| `monitoring_recency` | 0.10 |
| `treatment_response` | 0.10 |

Severity penalties: early 30, moderate 55, severe 80. Bands: `unrated` · 0–39 critical · 40–59 poor · 60–74 watch · 75–89 good · 90–100 excellent. `unrated` is a distinct state — day 0 is null, never 0.

The demo walk is a test, not a slide: `scripts/run_demo_e2e.py` and `tests/e2e/test_runbook.py` drive **82 → 68 → 59 → 86** over HTTP (baseline → BLB diagnosis → `got_worse` follow-up → agronomist resolve).

---

## Thresholds and feature flags

Set in `services/api/.env`; defaults live in `app/domain/constants.py` and `app/core/config.py`.

| Setting | Values | Default | Effect |
|---|---|---|---|
| `PROBLEM_STATEMENT` | `sih25076` \| `sih26131` | `sih25076` | Switches the mounted API surface (see below) |
| `LAND_API_MODE` | `mock` \| `live` | `mock` | Cadastral lookup adapter |
| `DIAGNOSIS_MODEL` | `stub` \| `real` | `stub` | `real` calls `ML_SERVICE_URL`; fails loudly rather than guessing |
| `EMBEDDING_PROVIDER` | `stub` \| `bge_m3` | `stub` | Also selects the matching RAG threshold |
| `ASR_PROVIDER` / `TTS_PROVIDER` | `stub` \| `bhashini` \| `sarvam` \| `whisper` \| `gtts` | `stub` | Voice adapters |
| `CONFIDENCE_GATE` | float | `0.70` | Disease diagnosis gate |
| `PEST_CONFIDENCE_GATE` | float | `0.70` | Pest gate, independently tunable |
| `RAG_RELEVANCE_THRESHOLD` | computed | `0.18` stub / `0.60` bge_m3 | Override with `RAG_RELEVANCE_THRESHOLD_OVERRIDE` |

`PROBLEM_STATEMENT=sih26131` unmounts `land`, `officer`, `resource_plan`, and `schemes` (they 404) and mounts `alerts` instead — 33 paths versus 40. Efficacy endpoints are specced but not yet built.

---

## Quickstart

### Backend

```bash
# 1. Infrastructure — Postgres 16 + pgvector on :5433, MinIO on :9000/:9001
docker compose -f infra/docker-compose.yml up -d

# 2. API
cd services/api
cp .env.example .env
make install          # creates .venv, installs requirements.txt
make migrate          # 5 Alembic revisions
make ingest-corpus    # embeds services/api/corpus/*.md into pgvector
make seed             # demo fixtures
make run              # uvicorn on :8000
```

Docs at `http://localhost:8000/docs`, ReDoc at `/redoc`, liveness at `GET /health`.

`make demo` chains migrate → ingest-corpus → seed → e2e. Seeded logins (password `bhoomi123`): farmer `+919944400001`, officer `+919944400002`, agronomist `+919944400003`.

The app boots without Postgres — repositories fall back to in-memory, and every port defaults to a stub adapter.

### Frontends

```bash
cd apps/kvk_portal      && npm install && npm run dev    # :5174
cd apps/officer_portal  && npm install && npm run dev    # :5173

cd apps/farmer_app && flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000   # Android emulator
flutter analyze && flutter test
```

### Tests

```bash
cd services/api
make test        # 353 tests
make test-e2e    # runbook only — requires a migrated, corpus-ingested Postgres
```

Current state: 351 pass with no database at all; the 2 `tests/e2e` cases fail on connection until Postgres is up.

---

## API surface

Base path `/api/v1`. Bearer JWT; role claim gates portal routes.

| Area | Endpoints |
|---|---|
| Auth | `POST /auth/register` · `POST /auth/login` · `GET /auth/me` |
| Media | `POST /assets/presigned-url` · `GET /assets/{asset_id}` |
| Voice | `POST /voice/transcribe` · `/voice/synthesize` · `/voice/query` · `/voice/confirm` |
| Farms | `POST /farms` · `GET,PUT /farms/{id}` · `GET /farms/{id}/summary` |
| Health score | `GET /farms/{id}/health` · `/health/history` · `POST /health/recompute` |
| Diagnosis | `POST /farms/{id}/diagnose` |
| Advisory (RAG) | `POST /advisory/query` |
| Timeline | `GET /timeline/{farm_id}` · `POST /timeline/events` |
| Follow-up | `POST /followup/checkin` |
| Escalation | `POST /escalation/create` · `GET /escalation/{id}` |
| Agronomist | `GET /agronomist/queue` · `/agronomist/case/{id}` · `POST /agronomist/resolve` |
| Weather | `GET /weather/current` · `/weather/forecast` · `/weather/et0` |
| System | `GET /system/health` |
| SIH25076 only | `/land/*` · `/officer/*` · `/resource-plan/{farm_id}` · `/schemes/*` |
| SIH26131 only | `GET /farms/{id}/alerts` · `POST /alerts/{id}/acknowledge` |

---

## Knowledge corpus

Two separate stores, at different maturity levels.

**Ingested (`services/api/corpus/`)** — 8 markdown documents covering rice BLB, blast, brown spot, nitrogen management, seed selection, irrigation (vegetative and reproductive), and harvest timing. These are what `make ingest-corpus` embeds into `knowledge_chunks`, and what advisory citations resolve against.

**Staged (`data/curated/Dataset_v4_validated/`)** — 8 pest documents (stem borer, BPH, leaf folder, green leafhopper, gall midge, thrips, whorl maggot, earhead bug) sourced from TNAU/ICAR-IRRI, with a manifest, source registry, evidence records, a 23-entry Tamil pest lexicon, and reference images. Status in the manifest is `production_ingested: false`, `chemical_advice_status: UNVERIFIED`. Read `DATASET_VALIDATION_STATUS.md` before wiring any of it into advisory output — the chemical recommendations have not passed regulatory validation.

---

## Team

| Member | Owns |
|---|---|
| Suchit Chopade | Health/risk engine, confidence gate, RAG pipeline, escalation compiler, integration |
| Shreekumar | Backend: auth, CRUD, uploads, alerts, deployment |
| Tharun | Corpus curation, pest research, image model, ASR/TTS research |
| Shruthi | Voice endpoints, DB schema and migrations |
| Santheesh | `apps/farmer_app` |
| Thaariha | `apps/officer_portal`, `apps/kvk_portal` |

---

## Known gaps

Listed so nobody rediscovers them at hour 30.

- `services/ml/` is empty files. `DIAGNOSIS_MODEL=real` points at `ML_SERVICE_URL` and will raise a connection error by design; the working path is the stub adapter.
- `packages/shared/constants.py` carries a different six-sub-index rubric (`soil_water`, `crop_vigor`, …) and different band thresholds than the live engine. It is Phase-0 scaffold. The authoritative source is `services/api/app/domain/health/constants.py`.
- The SIH26131 risk-score rework (four sub-indices: `active_problem_severity` 0.40, `environmental_risk` 0.25, `monitoring_recency` 0.15, `treatment_response` 0.20) exists in `docs/specs/suchit_module_specs_sih26131.md` but is not implemented — the engine still ships the six-sub-index PRD §7 rubric.
- Treatment-efficacy endpoints are specced (`docs/specs/treatment_efficacy_spec.md`) and not mounted.
- `RAG_RELEVANCE_THRESHOLD=0.18` is calibrated against the token-hashing stub embeddings. Re-tune when a real BGE-m3 adapter lands; `0.60` is the placeholder production target, not a measured value.
- CI covers the Flutter app and both portals. There is no backend job — run `make test` locally.

---

## Docs

| File | Contents |
|---|---|
| `docs/PRD.md` | Product requirements; health-score model in §7 |
| `docs/API_CONTRACT.md` | REST contract, enums mirroring the PRD |
| `docs/TECH_STACK.md` | Stack choices and alternatives |
| `docs/specs/suchit_module_specs_sih26131.md` | Risk engine, gate, RAG, escalation specs |
| `docs/specs/api_contract_sih26131_delta.md` | What the `PROBLEM_STATEMENT` flag changes |
| `docs/specs/early_warning_alert_spec.md` | Alert triggers and `inspection_tasks[]` |
| `docs/specs/treatment_efficacy_spec.md` | Efficacy metric definition |
| `docs/phase5_walkthrough.md` | Live Postgres integration verification log |
| `docs/FRONTEND_API_ALIGNMENT.md` | Contract-vs-client drift audit |
| `docs/contract_freeze_log.md` | Frozen contract deltas |
| `docs/decisions/asr-tts-provider-choice.md` | ASR/TTS provider decision record |
| `AGENTS.md` | Standing rules for coding agents on this repo |

---

<div align="center">
  <sub>Bhoomi — the earth. Every number inspectable; escalate, don't guess.</sub>
</div>
