<div align="center">
  <img src="./assets/bhoomi-logo.png" alt="Bhoomi" width="240" />

  <h1>Bhoomi</h1>
  <p><strong>Voice-first, multimodal crop advisory that treats every farm as a continuous case file.</strong></p>
  <p>Smart India Hackathon · <code>SIH26131</code> </p>

  <sub>FastAPI · PostgreSQL + PostGIS + pgvector · Flutter · React + Vite</sub>
</div>

---

## 1. What this is

A smallholder farmer with a sick crop has two bad options: ask around the village, or ask a chatbot. The chatbot answers once, forgets the farm, and — the expensive part — produces a fluent, confident answer even when it has no idea. Wrong advice about a leaf blight is not an embarrassing output. It is a lost season.

Bhoomi inverts the default. Instead of *always answer*, the system's default is **answer only when it can show its work, otherwise hand the farmer to a human**.

| Capability | What it does |
|---|---|
| **Multimodal diagnosis** | Photo + voice description + farm context → gated diagnosis (`target_type: disease \| pest`) |
| **Confidence gate** | One decision point that returns advisory *or* escalation, never both |
| **Grounded RAG advisory** | Fixed 5-point structure, every response citing the corpus documents it drew from |
| **Escalation compiler** | Pre-analysed case bundle routed to the next available agronomist |
| **Risk score** | Deterministic weighted rubric, four sub-indices, full breakdown on every snapshot |
| **Problem timeline** | Persistent case file: queries, diagnoses, treatments, follow-ups, score movements |
| **Early-warning alerts** | Weather / seasonal / regional triggers with mandatory inspection tasks |
| **Treatment efficacy** | Outcome tracking wired through diagnose → follow-up → resolve |

---

## 2. The two hard rules

> **1. Never answer below the confidence gate.** If image confidence is under threshold, no advisory is composed at all.
>
> **2. Never fabricate on no-retrieval.** If nothing in the curated corpus clears the relevance threshold, the system says so and offers escalation.

Both are enforced in orchestration code, not in a prompt. A prompt instruction is a request to a model and a model can ignore it; a branch in `domain/gate/decide.py` cannot.

---

## 3. Quick start

### Prerequisites

Docker (or local Postgres 16 with pgvector + PostGIS) · Python 3.11+ · Node 18+ · Flutter stable

### Backend

```bash
# 1. Infrastructure — Postgres 16 + pgvector on :5433, MinIO on :9000 (console :9001)
docker compose -f infra/docker-compose.yml up -d

# 2. API
cd services/api
cp .env.example .env
make install          # creates .venv, installs requirements.txt
make migrate          # Alembic revisions
make ingest-corpus    # embeds CORPUS_DOCS into knowledge_chunks
make seed             # demo fixtures
make run              # uvicorn on :8000
```

| URL | What |
|---|---|
| `http://localhost:8000/docs` | Swagger |
| `http://localhost:8000/redoc` | ReDoc |
| `GET /health` | Liveness |

**One-shot demo reset:** `make demo` chains migrate → ingest-corpus → seed → e2e.

**Seeded logins** (password `bhoomi123`): farmer `+919944400001` · officer `+919944400002` · agronomist `+919944400003`.

> **Demo-day safety net:** the API boots with no Postgres at all. Repositories fall back to in-memory and every port defaults to a stub. You lose persistence and real retrieval, but the app comes up — the difference between a degraded demo and no demo.

### Frontends

```bash
cd apps/kvk_portal      && npm install && npm run dev    # :5174 — agronomist case queue
cd apps/officer_portal  && npm install && npm run dev    # :5173 — land review

cd apps/farmer_app && flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000   # 10.0.2.2 = host, from Android emulator
```

---

## 4. Repository layout

```
Bhoomi-SIH-Agri/
├── apps/
│   ├── farmer_app/            Flutter — Riverpod, go_router, dio
│   ├── kvk_portal/            Agronomist case queue + resolve (React + Vite + Tailwind)
│   └── officer_portal/        Land review (React + Vite + Tailwind + Leaflet)
├── services/
│   ├── api/                   FastAPI backend — the entire intelligence layer
│   │   ├── app/api/v1/        Routers (HTTP in, HTTP out, no logic)
│   │   ├── app/services/      Orchestration: gate/, rag/, escalation/, alerts/, efficacy/
│   │   ├── app/domain/        Pure functions + named constants, zero I/O
│   │   ├── app/repositories/  The only code touching Postgres (+ in-memory twin)
│   │   ├── app/ports/         Typed Protocols for every external dependency
│   │   ├── app/models/        SQLAlchemy models
│   │   ├── corpus/            Human-readable mirror of the corpus (not the ingest source)
│   │   └── tests/             Unit / integration / e2e
│   └── ml/                    Inference microservice — heuristic, see §12
├── data/
│   ├── external/Dataset_v4/            Raw pest dataset snapshot — ground truth, don't edit
│   └── curated/Dataset_v4_validated/   Sourced + manifested pest docs
├── docs/                      PRD, contracts, module specs, decision records, audits
├── rag/                       RAG governance: evaluation, safety, shadow, release
├── infra/                     docker-compose (Postgres + pgvector, MinIO), init-db.sql
├── AGENTS.md                  Standing rules for coding agents in this repo
├── DEMO_REHEARSAL_RUNBOOK.md  The timed demo walk
└── JUDGE_DEFENSE_QA.md        Prepared answers to the predictable questions
```

---

## 5. Architecture

### Dependency flow

`AGENTS.md` fixes a one-way flow, and the code holds to it:

```
api/v1  →  services  →  domain / repositories  →  adapters
```

| Layer | Rule |
|---|---|
| `api/v1/` | Routers only. Parse, authenticate, hand off. Swapping transport shouldn't touch logic. |
| `services/` | Orchestration. Use-cases assembled from pure pieces and ports. |
| `domain/` | Pure functions and named constants. No I/O anywhere. |
| `repositories/` | The only Postgres code, with an in-memory implementation behind the same interface. |
| `ports/` | Typed `Protocol` per external dependency: weather, LLM, embeddings, image diagnosis, ASR/TTS, storage, roster. |
| `adapters/` | Real and stub implementations, selected in `adapters/dependencies.py` from config. |

The payoff is concrete rather than architectural taste: no call site imports a concrete adapter, so flipping `DIAGNOSIS_MODEL=real` in `.env` changes behaviour everywhere with zero code edits, and the whole app runs offline on stubs.

### Request flow — the central interaction

```
Flutter app
  │  POST /assets/presigned-url     → photo uploads straight to MinIO/S3, not through the API
  │  POST /farms/{id}/diagnose      → only the small asset_id travels in JSON
  ▼
api/v1/diagnose.py                   router: parse, authenticate, hand off
  ▼
services/diagnosis_service.py        orchestration
  ├── ImageDiagnosisPort  → label + confidence         (stub or real ML service)
  ├── domain/gate/decide.py → GateDecision             ◄── the decision point
  │
  ├── ESCALATE ──► services/escalation/compiler.py
  │                 case bundle + agronomist routing
  │                 → { above_gate: false, escalation: {...} }
  │
  └── COMPOSE  ──► services/rag/pipeline.py
                    embed query → pgvector search → relevance check →
                    grounded LLM call → parse into 5-point + citations
  ▼
services/health_service.py           recompute score, persist snapshot
  ▼
diagnosis + advisory + citations + risk_delta + spoken_summary
```

Two things worth pointing at. The gate sits *before* composition — there is no path where the LLM writes advice and something downstream decides whether to show it. And escalation produces a complete, useful object; escalating is not an error path, it is the other half of the product.

---

## 6. The confidence gate

`domain/gate/decide.py` is pure — no database, no network, fully unit-testable. Three checks in order, returning on the first failure:

| # | Check | Failure code |
|---|---|---|
| 1 | Label in `SUPPORTED_LABELS[target_type]`? | `OUT_OF_SCOPE_TARGET` |
| 2 | `confidence >= confidence_gate` (0.70) | `BELOW_CONFIDENCE_GATE` |
| 3 | `retrieval_relevance >= relevance_threshold` | `NO_RELEVANT_SOURCE` |

**Bounded scope** (`domain/gate/constants.py`), because a model asked to classify something it was never trained on will still return *something* with a confidence number attached:

- **Disease (8):** bacterial leaf blight, blast, brown spot, sheath blight, early blight, late blight, powdery mildew, leaf curl virus
- **Pest (8):** stem borer, brown planthopper, leaf folder, green leafhopper, gall midge, fall armyworm, aphid, whitefly

Two details that are easy to get wrong and are handled here:

- A **missing** signal is skipped, never treated as a pass. A text-only advisory query has no image confidence, so that check is skipped rather than defaulted to `1.0`.
- `GateDecision` holds exactly one `outcome`, so the invariant is structural — a caller cannot end up holding both an advisory and an escalation.

---

## 7. The health / risk score

The most visible number in the product, so the most tempting thing to fake and the easiest to attack. The defense is a documented weighted rubric in plain Python where every point of movement traces to an input.

Four sub-indices, each 0–100, combined by fixed weights in `domain/health/constants.py` — with an `assert` at import time that they sum to exactly 1.0 (`WEIGHTS_VERSION = "v2-sih26131"`):

| Sub-index | Weight | Measures |
|---|---|---|
| `active_problem_severity` | **0.40** | Open problems weighted by severity — the big mover |
| `environmental_risk` | 0.25 | Weather conditions favourable to outbreak, vs. crop stage |
| `treatment_response` | 0.20 | Follow-up trend: improved / no change / got worse |
| `monitoring_recency` | 0.15 | Whether scans are recent enough to trust the score |

**Severity penalties:** early `30` · moderate `55` · severe `80`.

**Bands:** `unrated` · `0–39 critical` · `40–59 poor` · `60–74 watch` · `75–89 good` · `90–100 excellent`.

`unrated` is not `0`. Day 0 with no inputs returns a null score; a *low* number always means bad health, never missing data.

The deterministic walk — **82 → 73 → 57 → 91** — is a pytest fixture, not a slide. Same inputs, same score, every time, and reproducible live via `POST /farms/{id}/health/recompute`.

---

## 8. Knowledge corpus

Grounded advisory is only as honest as what it retrieves from, so the two stores are kept separate and their maturity is stated plainly.

### Ingested (what exists at runtime)

`app/services/rag/corpus_data.py` → `make ingest-corpus` chunks and embeds the `CORPUS_DOCS` list into `knowledge_chunks`.

- 17 disease/agronomy documents (BLB, blast, brown spot, sheath blight, nitrogen management, seed selection, irrigation, harvest timing)
- 8 pest documents (stem borer, BPH, leaf folder, green leafhopper, gall midge, thrips, earhead bug, whorl maggot)

Every advisory citation resolves against these 25 documents. The `.md` files under `services/api/corpus/` are a human-readable mirror, **not** the ingestion source.

### Staged, chemical content withheld

`data/curated/Dataset_v4_validated/` holds the same 8 pest documents from TNAU / ICAR-IRRI / IRRI / KVK with a source manifest and structured ETL evidence. Their identification, ETL, cultural and biological-control content was ingested. Their `chemical_prescriptions` and regulatory-status sections were deliberately left out — the manifest carries `production_ingested: false` and `chemical_advice_status: UNVERIFIED`.

Shipping unvalidated chemical dosages to farmers is a real-world harm, not a demo detail. The split lets pest diagnosis compose identification and non-chemical guidance honestly while escalating anything needing chemical-specific advice. Read `DATASET_VALIDATION_STATUS.md` before ever ingesting the chemical portion.

---

## 9. Configuration

Defaults in `app/domain/constants.py` and `app/core/config.py`; override in `services/api/.env` (template: `.env.example`).

| Setting | Values | Default | Effect |
|---|---|---|---|
| `PROBLEM_STATEMENT` | `sih26131` \| `sih25076` | `sih26131` | Which routers mount |
| `DIAGNOSIS_MODEL` | `stub` \| `real` | `stub` | `real` calls `ML_SERVICE_URL` |
| `EMBEDDING_PROVIDER` | `stub` \| `bge_m3` | `stub` | Also selects the matching RAG threshold |
| `LLM_PROVIDER` | `stub` \| `groq` | `stub` | `groq` requires a real `LLM_API_KEY` (fails at startup otherwise) |
| `ASR_PROVIDER` / `TTS_PROVIDER` | `stub` \| `bhashini` \| `sarvam` \| `whisper` \| `gtts` | `stub` | Voice adapters |
| `LAND_API_MODE` | `mock` \| `live` | `mock` | Cadastral lookup adapter |
| `CONFIDENCE_GATE` | float | `0.70` | Disease gate |
| `PEST_CONFIDENCE_GATE` | float | `0.70` | Pest gate — same value today, separately tunable |
| `RAG_RELEVANCE_THRESHOLD` | computed | `0.18` stub / `0.60` bge_m3 | Force with `RAG_RELEVANCE_THRESHOLD_OVERRIDE` |

**Why the RAG threshold is computed, not fixed.** Relevance scores from token-hashing stub vectors and from real BGE-m3 dense embeddings sit on completely different scales. One hardcoded number would be either far too strict or effectively disabled depending on the active adapter, so the threshold follows `EMBEDDING_PROVIDER` automatically.

**The problem-statement switch.** Written for SIH25076 (broad farm advisory), realigned toward SIH26131 (crop disease and pest management). Land registry, officer review, scheme discovery and resource planning stay mounted in **both** modes — they are useful trust-building context regardless, and the farmer app's Today's Plan screen depends on `resource_plan` being live. `sih26131` only adds `alerts` and `efficacy` on top of the shared set.

> `docs/specs/api_contract_sih26131_delta.md` §2.1–2.3 is a stale early draft describing the unmounting of `land`/`officer`/`schemes`/`resource_plan`. That plan was superseded; `tests/unit/test_problem_statement_gating.py` is the authoritative contract.

---

## 10. API surface

Base path `/api/v1`. Bearer JWT; the role claim gates portal routes.

| Area | Endpoints |
|---|---|
| **Auth** | `POST /auth/register` · `/auth/login` · `GET /auth/me` · `POST /auth/otp/request` · `/auth/otp/verify` |
| **Media** | `POST /assets/presigned-url` · `GET /assets/{asset_id}` |
| **Voice** | `POST /voice/transcribe` · `/voice/synthesize` · `/voice/query` · `/voice/confirm` |
| **Farms** | `POST /farms` · `GET /farms` · `GET,PUT /farms/{id}` · `GET /farms/{id}/summary` |
| **Risk score** | `GET /farms/{id}/health` · `/health/history` · `POST /health/recompute` |
| **Diagnosis** | `POST /farms/{id}/diagnose` (`target_type: disease \| pest`) |
| **Advisory** | `POST /advisory/query` |
| **Timeline** | `GET /timeline/{farm_id}` · `POST /timeline/events` |
| **Follow-up** | `POST /followup/checkin` |
| **Escalation** | `POST /escalation/create` · `GET /escalation/{id}` |
| **Agronomist** | `GET /agronomist/queue` · `/agronomist/case/{id}` · `POST /agronomist/resolve` |
| **Officer / land** | `GET /officer/queue` · `/officer/review/{parcel_id}` · `POST /officer/action` · `/land/verify` · `/land/cadastral-lookup` |
| **Schemes** | `POST /schemes/match` · `GET /schemes/{id}` |
| **Resource plan** | `POST,GET /resource-plan/{farm_id}` |
| **Weather** | `GET /weather/current` · `/weather/forecast` · `/weather/et0` |
| **SIH26131 only** | `GET /farms/{id}/alerts` · `POST /alerts/{id}/acknowledge` · `GET /treatments/{id}/efficacy` |
| **System** | `GET /system/health` · `GET /health` |

Two conventions recur, both concessions to thin rural bandwidth: large media never passes through the API (presigned upload straight to object storage, then only the `asset_id` travels in JSON), and every consequential response carries a `spoken_summary` the client can read aloud locally.

---

## 11. Testing & CI

```bash
cd services/api
make test        # full suite
make test-e2e    # runbook only — needs a migrated, corpus-ingested Postgres
make smoke       # migrate + ingest + seed, then prove the app talks to Postgres
```

The suite runs offline: the domain layer is pure, so everything except the `tests/e2e` runbook cases passes with no database. Those fail on connection refused until Postgres is up — not on logic.

Frontend:

```bash
cd apps/farmer_app && flutter analyze && flutter test
cd apps/kvk_portal && npm run lint && npm run build
```

GitHub Actions runs two pipelines — `backend-ci.yml` (Alembic migrate + pytest against `pgvector/pgvector:pg16`) and `frontend-ci.yml` (Flutter analyze/test, Vite lint/build).

---

## 12. Known gaps

Written down so nobody rediscovers them at hour 30.

| Gap | Status |
|---|---|
| **`services/ml/` is a heuristic, not a trained model** | Real running FastAPI microservice — `DIAGNOSIS_MODEL=real` genuinely calls it over HTTP (colour-histogram analysis on real bytes, deterministic asset-id hash otherwise). No labelled dataset or trained weights in this repo, so predictions are not diagnostic. `/embed`, `/transcribe`, `/synthesize` exist; only `/diagnose` is wired from `services/api`. |
| **`EMBEDDING_PROVIDER=bge_m3` unverified against real weights** | Wiring is end-to-end real (`RealEmbeddingAdapter` → `services/ml/embed`, lazy-loading `BAAI/bge-m3`). The model-load-and-encode path is not verified — the build environment had no Hugging Face access, so `/embed` reports `"method": "hash"` via graceful fallback. Re-tune `RAG_RELEVANCE_THRESHOLD_PRODUCTION` (0.60) against real retrieval; it is a target figure, not a measured one. |
| **Pest advisory is non-chemical only** | 5 of 8 in-scope pest labels retrieve real identification/ETL/cultural/biological content. `fall_armyworm`, `whitefly`, `aphid` have no corpus backing and correctly escalate on `NO_RELEVANT_SOURCE`. Both paths exercised in `tests/test_pest_diagnosis.py`. |
| **Treatment efficacy is narrowly scoped** | Built and wired through diagnose → follow-up → resolve, but limited to the 3 diseases the corpus documents a first-line treatment for (`domain/efficacy/default_treatments.py`). |
| **OTP store is in-memory** | 5-minute TTL, 60s resend cooldown, 5 verify-attempt cap. Doesn't survive multi-worker deployment. No SMS gateway is configured, so outside `APP_ENV=production` the response returns `debug_otp` directly. |

---

## 13. Team

| Member | Owns |
|---|---|
| **Suchit Chopade** | Health/risk engine, confidence gate, RAG pipeline, escalation compiler, integration |
| **Shreekumar** | Backend: auth, CRUD, uploads, alerts, deployment |
| **Tharun** | Corpus curation, pest research, image model, ASR/TTS research |
| **Shruthi** | Voice endpoints, DB schema and migrations |
| **Santheesh** | `apps/farmer_app` |
| **Thaariha** | `apps/officer_portal`, `apps/kvk_portal` |

---

## 14. Documentation index

| File | Contents |
|---|---|
| `docs/PRD.md` | Product requirements; health-score model in §7 |
| `docs/API_CONTRACT.md` | REST contract, enums mirroring the PRD |
| `docs/TECH_STACK.md` | Stack choices and the alternatives considered |
| `docs/specs/suchit_module_specs_sih26131.md` | Risk engine, gate, RAG, escalation specs |
| `docs/specs/api_contract_sih26131_delta.md` | What the `PROBLEM_STATEMENT` flag changes (see §9 caveat) |
| `docs/specs/early_warning_alert_spec.md` | Alert triggers and mandatory `inspection_tasks[]` |
| `docs/specs/treatment_efficacy_spec.md` | Efficacy metric definition |
| `docs/FRONTEND_API_ALIGNMENT.md` | Contract-vs-client drift audit |
| `docs/contract_freeze_log.md` | Frozen contract deltas |
| `docs/phase5_walkthrough.md` | Live Postgres integration verification log |
| `docs/decisions/` | Decision records (e.g. ASR/TTS provider choice) |
| `DEMO_REHEARSAL_RUNBOOK.md` | The timed demo walk |
| `JUDGE_DEFENSE_QA.md` | Prepared answers to the predictable questions |
| `AGENTS.md` | Standing rules for coding agents on this repo |

---

<div align="center">
  <sub><strong>Bhoomi</strong> — the earth. Every number inspectable; escalate, don't guess.</sub>
</div>
