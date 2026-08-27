<div align="center">
  <img src="./assets/bhoomi-logo.png" alt="Bhoomi" width="240" />

  <h1>Bhoomi</h1>
  <p><strong>Voice-first crop advisory that refuses to guess.</strong></p>
  <p>Smart India Hackathon · <code>SIH26131</code> — early detection and management of crop diseases and pest infestations</p>

  <sub>FastAPI · PostgreSQL + PostGIS + pgvector · Flutter · React + Vite</sub>
</div>

---

## The 60-second version

A farmer photographs a sick leaf and describes the problem out loud in their own language. Bhoomi either returns advice it can cite a source for, or tells the farmer it isn't sure and puts a pre-analysed case in front of a real agronomist. There is no third option where it makes something up.

That constraint is the whole product. Wrong advice about a leaf blight isn't a bad output, it's a lost season — so the system is built so that the confident-sounding wrong answer is unreachable in code.

```
photo + voice ──► image model ──► CONFIDENCE GATE ──┬─ above ─► retrieve from corpus ─► cited 5-point advisory
                                                     │
                                                     └─ below ─► case bundle ─► agronomist queue
```

Everything else in this repo — the risk score, the timeline, follow-ups, alerts — exists to make that one decision better informed and its outcome trackable.

---

## The two rules

> **1. Never answer below the confidence gate.** If image confidence is under threshold, no advisory is composed at all.
>
> **2. Never fabricate on no-retrieval.** If nothing in the curated corpus clears the relevance threshold, the system says so and offers escalation.

Both live in orchestration code, not in a prompt. A prompt instruction is a request to a model, and a model can ignore it. A branch in `domain/gate/decide.py` cannot.

---

## Quick start

**You need:** Docker · Python 3.11+ · Node 18+ · Flutter (only for the farmer app)

### 1. Start the infrastructure

```bash
docker compose -f infra/docker-compose.yml up -d
```

Postgres 16 + pgvector on `:5433`, MinIO on `:9000` (console `:9001`).

### 2. Start the API

```bash
cd services/api
cp .env.example .env
make install          # creates .venv, installs requirements.txt
make demo             # migrate → ingest corpus → seed → run e2e
make run              # uvicorn on :8000
```

`make demo` is the one-shot reset. To run the steps separately: `make migrate`, `make ingest-corpus`, `make seed`.

Then open `http://localhost:8000/docs` for Swagger, `/redoc` for ReDoc, or `GET /health` for liveness.

**Seeded logins** (password `bhoomi123`): farmer `+919944400001` · officer `+919944400002` · agronomist `+919944400003`

> **If Postgres won't come up:** the API still boots. Repositories fall back to in-memory and every external dependency defaults to a stub. You lose persistence and real retrieval, but the app runs — the difference between a degraded demo and no demo.

### 3. Start the frontends

```bash
cd apps/kvk_portal      && npm install && npm run dev    # :5174 — agronomist case queue

cd apps/farmer_app && flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000    # 10.0.2.2 = your host, seen from an Android emulator
```

---

## How a diagnosis actually flows

```
Flutter app
  │  POST /assets/presigned-url     photo uploads straight to MinIO, never through the API
  │  POST /farms/{id}/diagnose      only the small asset_id travels in JSON
  ▼
api/v1/diagnose.py                  router — parse, authenticate, hand off
  ▼
services/diagnosis_service.py       orchestration
  ├── ImageDiagnosisPort  →  label + confidence
  ├── domain/gate/decide.py  →  GateDecision          ◄── the decision point
  │
  ├── ESCALATE ──► services/escalation/compiler.py
  │                 case bundle + agronomist routing
  │                 → { above_gate: false, escalation: {...} }
  │
  └── COMPOSE  ──► services/rag/pipeline.py
                    embed query → pgvector search → relevance check →
                    grounded LLM call → parse into 5-point + citations
  ▼
services/health_service.py          recompute risk score, persist snapshot
  ▼
diagnosis + advisory + citations + risk_delta + spoken_summary
```

Two things worth pointing at. The gate sits **before** composition, so there is no path where the LLM writes advice and something downstream decides whether to show it. And escalation returns a complete, useful object — escalating is the other half of the product, not an error path.

### Layering

`AGENTS.md` fixes a one-way dependency flow and the code holds to it:

```
api/v1  →  services  →  domain / repositories  →  adapters
```

| Layer | Rule |
|---|---|
| `api/v1/` | Routers only. Parse, authenticate, hand off. |
| `services/` | Orchestration. Use-cases assembled from pure pieces and ports. |
| `domain/` | Pure functions and named constants. No I/O anywhere. |
| `repositories/` | The only Postgres code, with an in-memory twin behind the same interface. |
| `ports/` | One typed `Protocol` per external dependency: weather, LLM, embeddings, image diagnosis, ASR/TTS, storage, roster. |
| `adapters/` | Real and stub implementations, selected in `adapters/dependencies.py` from config. |

The payoff is concrete: no call site imports a concrete adapter, so flipping `DIAGNOSIS_MODEL=real` in `.env` changes behaviour everywhere with zero code edits, and the whole app runs offline on stubs.

---

## The confidence gate

`domain/gate/decide.py` is pure — no database, no network, fully unit-testable. Three checks in order, returning on the first failure:

| # | Check | Failure code |
|---|---|---|
| 1 | Label in `SUPPORTED_LABELS[target_type]`? | `OUT_OF_SCOPE_TARGET` |
| 2 | `confidence >= confidence_gate` (0.70) | `BELOW_CONFIDENCE_GATE` |
| 3 | `retrieval_relevance >= relevance_threshold` | `NO_RELEVANT_SOURCE` |

Scope is bounded on purpose (`domain/gate/constants.py`), because a model asked to classify something it was never trained on will still return *something* with a confidence number attached:

- **Disease (8):** bacterial leaf blight · blast · brown spot · sheath blight · early blight · late blight · powdery mildew · leaf curl virus
- **Pest (8):** stem borer · brown planthopper · leaf folder · green leafhopper · gall midge · fall armyworm · aphid · whitefly

Two details that are easy to get wrong and are handled here:

- A **missing** signal is skipped, never treated as a pass. A text-only advisory query has no image confidence, so that check is skipped rather than defaulted to `1.0`.
- `GateDecision` holds exactly one `outcome`, so the invariant is structural. A caller cannot end up holding both an advisory and an escalation.

---

## The risk score

The most visible number in the product, so the most tempting thing to fake and the easiest to attack. The defense is a documented weighted rubric in plain Python where every point of movement traces back to an input.

Four sub-indices, each 0–100, combined by fixed weights in `domain/health/constants.py` — with an `assert` at import time that they sum to exactly 1.0 (`WEIGHTS_VERSION = "v2-sih26131"`):

| Sub-index | Weight | Measures |
|---|---|---|
| `active_problem_severity` | **0.40** | Open problems weighted by severity — the big mover |
| `environmental_risk` | 0.25 | Weather conditions favourable to outbreak, against crop stage |
| `treatment_response` | 0.20 | Follow-up trend: improved / no change / got worse |
| `monitoring_recency` | 0.15 | Whether scans are recent enough to trust the score |

**Severity penalties:** early `30` · moderate `55` · severe `80`

**Bands:** `unrated` · `0–39 critical` · `40–59 poor` · `60–74 watch` · `75–89 good` · `90–100 excellent`

`unrated` is not `0`. Day 0 with no inputs returns a null score. A *low* number always means bad health, never missing data.

The deterministic walk — **82 → 73 → 57 → 91** — is a pytest fixture, not a slide. Same inputs, same score, every time, and reproducible live via `POST /farms/{id}/risk/recompute`.

---

## The knowledge corpus

Grounded advisory is only as honest as what it retrieves from, so the two stores are kept separate and their maturity is stated plainly.

**Ingested — what exists at runtime.** `app/services/rag/corpus_data.py` holds `CORPUS_DOCS`; `make ingest-corpus` chunks and embeds it into `knowledge_chunks`. 25 documents: 17 disease and agronomy (BLB, blast, brown spot, sheath blight, nitrogen management, seed selection, irrigation, harvest timing) and 8 pest (stem borer, BPH, leaf folder, green leafhopper, gall midge, thrips, earhead bug, whorl maggot). Doc IDs are namespaced — `kb_2xx` for disease, `kb_p3xx` for pest — which is how pest retrieval is scoped without a schema migration.

Every advisory citation resolves against these 25 documents. The `.md` files under `services/api/corpus/` are a human-readable mirror, **not** the ingestion source.

**Staged, chemical content withheld.** `data/curated/Dataset_v4_validated/` holds the same 8 pest documents from TNAU / ICAR-IRRI / IRRI / KVK with a source manifest and structured ETL evidence. Identification, ETL, cultural and biological-control content was ingested. The `chemical_prescriptions` and regulatory-status sections were deliberately left out — the manifest carries `production_ingested: false` and `chemical_advice_status: UNVERIFIED`.

Shipping unvalidated chemical dosages to farmers is a real-world harm, not a demo detail. The split lets pest diagnosis compose identification and non-chemical guidance honestly, while anything needing chemical-specific advice finds nothing to ground on and correctly escalates. Read `DATASET_VALIDATION_STATUS.md` before ever ingesting the chemical portion.

---

<details>
<summary><strong>Repository layout</strong></summary>

```
Bhoomi-SIH-Agri/
├── apps/
│   ├── farmer_app/            Flutter — Riverpod, go_router, dio
│   └── kvk_portal/            Agronomist case queue + resolve (React + Vite + Tailwind)
├── services/
│   ├── api/                   FastAPI backend — the entire intelligence layer
│   │   ├── app/api/v1/        Routers (HTTP in, HTTP out, no logic)
│   │   ├── app/services/      Orchestration: gate/, rag/, escalation/, alerts/, efficacy/
│   │   ├── app/domain/        Pure functions + named constants, zero I/O
│   │   ├── app/repositories/  The only code touching Postgres (+ in-memory twin)
│   │   ├── app/ports/         Typed Protocols for every external dependency
│   │   ├── app/adapters/      Real + stub implementations, chosen by config
│   │   ├── app/models/        SQLAlchemy models
│   │   ├── corpus/            Human-readable mirror of the corpus (not the ingest source)
│   │   └── tests/             unit / integration / e2e
│   └── ml/                    Inference microservice — heuristic, see Known gaps
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

</details>

<details>
<summary><strong>API surface</strong> — base path <code>/api/v1</code>, Bearer JWT, role claim gates portal routes</summary>

| Area | Endpoints |
|---|---|
| **Auth** | `POST /auth/register` · `/auth/login` · `GET /auth/me` · `POST /auth/otp/request` · `/auth/otp/verify` |
| **Media** | `POST /assets/presigned-url` · `GET /assets/{asset_id}` · `PUT /assets/local-upload/{kind}/{id}/{file_name}` |
| **Voice** | `POST /voice/transcribe` · `/voice/confirm` · `/voice/synthesize` · `/voice/query` |
| **Risk score** | `GET /farms/{id}/risk` · `/risk/history` · `POST /farms/{id}/risk/recompute` |
| **Farms** | `POST /farms` · `GET /farms` · `GET,PUT /farms/{id}` · `GET /farms/{id}/summary` |
| **Diagnosis** | `POST /farms/{id}/diagnose` (`target_type: disease \| pest`) |
| **Advisory** | `POST /advisory/query` |
| **Guidance** | `GET /guidance` · `GET /guidance/{crop}` — static interim containment cards |
| **Timeline** | `GET /timeline/{farm_id}` · `POST /timeline/events` |
| **Follow-up** | `POST /followup/checkin` |
| **Escalation** | `POST /escalation/create` · `GET /escalation/{id}` |
| **Agronomist** | `GET /agronomist/queue` · `/agronomist/case/{id}` · `/agronomist/case/{id}/pdf-payload` · `POST /agronomist/resolve` |
| **Land** | `POST /farms/{id}/land` · `POST /land/verify` · `GET /land/{farm_id}` |
| **Officer** | `GET /officer/queue` · `/officer/review/{parcel_id}` · `POST /officer/action` |
| **Schemes** | `GET /farms/{id}/schemes` · `POST /schemes/match` · `GET,POST /schemes/{id}` |
| **Resource plan** | `POST,GET /resource-plan/{farm_id}` |
| **Weather** | `GET /weather/current` · `/weather/forecast` · `/weather/et0` |
| **SIH26131 only** | `GET /farms/{id}/alerts` · `POST /alerts/{id}/acknowledge` · `GET /treatments/{id}/efficacy` |
| **System** | `GET /system/health` · `GET /health` |

Two conventions recur, both concessions to thin rural bandwidth. Large media never passes through the API — presigned upload straight to object storage, then only the `asset_id` travels in JSON. And every consequential response carries a `spoken_summary` the client can read aloud locally.

> `live_routes.txt` at the repo root is a stale snapshot: it predates the `/health` → `/risk` rename and the alerts, efficacy and guidance routers. Regenerate it from the running app rather than trusting it.

</details>

<details>
<summary><strong>Configuration</strong> — defaults in <code>app/core/config.py</code>, override in <code>services/api/.env</code></summary>

| Setting | Values | Default | Effect |
|---|---|---|---|
| `PROBLEM_STATEMENT` | `sih26131` \| `sih25076` | `sih26131` | Which routers mount |
| `DIAGNOSIS_MODEL` | `stub` \| `real` | `stub` | `real` calls `ML_SERVICE_URL` |
| `EMBEDDING_PROVIDER` | `stub` \| `bge_m3` | `stub` | Also selects the matching RAG threshold |
| `LLM_PROVIDER` | `stub` \| `groq` | `stub` | `groq` requires a real `LLM_API_KEY` (fails at startup otherwise) |
| `ASR_PROVIDER` / `TTS_PROVIDER` | `stub` \| `bhashini` \| `sarvam` \| `whisper` \| `gtts` | `stub` | Voice adapters |
| `CONFIDENCE_GATE` | float | `0.70` | Disease gate |
| `PEST_CONFIDENCE_GATE` | float | `0.70` | Pest gate — same value today, separately tunable |
| `RAG_RELEVANCE_THRESHOLD` | computed | `0.18` stub / `0.60` bge_m3 | Force with `RAG_RELEVANCE_THRESHOLD_OVERRIDE` |

**Why the RAG threshold is computed rather than fixed.** Relevance scores from token-hashing stub vectors and from real BGE-m3 dense embeddings sit on completely different scales. One hardcoded number would be either far too strict or effectively disabled depending on the active adapter, so the threshold follows `EMBEDDING_PROVIDER` automatically.

**What the problem-statement switch actually does.** The project was written for SIH25076 (broad farm advisory) and realigned toward SIH26131 (crop disease and pest management). Land, officer review, schemes and resource planning stay mounted in **both** modes — they're useful trust-building context either way, and the farmer app's Today's Plan screen depends on `resource_plan` being live. `sih26131` only adds `alerts` and `efficacy` on top of the shared set.

> `docs/specs/api_contract_sih26131_delta.md` §2.1–2.3 is a stale early draft describing the unmounting of `land`/`officer`/`schemes`/`resource_plan`. That plan was superseded. `tests/unit/test_problem_statement_gating.py` is the authoritative contract.

</details>

<details>
<summary><strong>Testing & CI</strong></summary>

```bash
cd services/api
make test        # full suite
make test-e2e    # runbook only — needs a migrated, corpus-ingested Postgres
make smoke       # migrate + ingest + seed, proving the app talks to Postgres
```

The suite runs offline. The domain layer is pure, so everything except the `tests/e2e` runbook cases passes with no database. Those fail on connection refused until Postgres is up — a connectivity failure, not a logic one.

Frontend:

```bash
cd apps/farmer_app && flutter analyze && flutter test
cd apps/kvk_portal && npm run lint && npm run build
```

GitHub Actions runs two pipelines: `backend-ci.yml` (Alembic migrate + pytest against `pgvector/pgvector:pg16`) and `frontend-ci.yml` (Flutter analyze/test, Vite lint/build).

</details>

<details>
<summary><strong>Known gaps</strong> — written down so nobody rediscovers them at hour 30</summary>

| Gap | Status |
|---|---|
| **`services/ml/` is a heuristic, not a trained model** | A real running FastAPI microservice — `DIAGNOSIS_MODEL=real` genuinely calls it over HTTP (colour-histogram analysis on real bytes, deterministic asset-id hash otherwise). No labelled dataset or trained weights in this repo, so predictions are not diagnostic. `/embed`, `/transcribe`, `/synthesize` exist; only `/diagnose` is wired from `services/api`. |
| **`EMBEDDING_PROVIDER=bge_m3` unverified against real weights** | Wiring is end-to-end real (`RealEmbeddingAdapter` → `services/ml/embed`, lazy-loading `BAAI/bge-m3`). The model-load-and-encode path is not verified — the build environment had no Hugging Face access, so `/embed` reports `"method": "hash"` via graceful fallback. `RAG_RELEVANCE_THRESHOLD_PRODUCTION` (0.60) is a target figure, not a measured one; re-tune it against real retrieval. |
| **Pest advisory is non-chemical only** | 5 of 8 in-scope pest labels retrieve real identification/ETL/cultural/biological content. `fall_armyworm`, `whitefly` and `aphid` have no corpus backing and correctly escalate on `NO_RELEVANT_SOURCE`. Both paths exercised in `tests/test_pest_diagnosis.py`. |
| **Treatment efficacy is narrowly scoped** | Built and wired through diagnose → follow-up → resolve, but limited to the 3 diseases the corpus documents a first-line treatment for (`domain/efficacy/default_treatments.py`). |
| **OTP store is in-memory** | 5-minute TTL, 60s resend cooldown, 5 verify-attempt cap. Doesn't survive multi-worker deployment. No SMS gateway is configured, so outside `APP_ENV=production` the response returns `debug_otp` directly. |
| **`WEIGHTS_VERSION` is defined twice** | `domain/health/constants.py` (`v2-sih26131`, the one the scoring engine actually uses) and `core/config.py` (`v1.0.0`, unused). Delete the config copy before something reads it by accident. |

</details>

---

## Team

| Member | Owns |
|---|---|
| **Suchit Chopade** | Risk engine, confidence gate, RAG pipeline, escalation compiler, integration |
| **Shreekumar** | Backend: auth, CRUD, uploads, alerts, deployment |
| **Tharun** | Corpus curation, pest research, image model, ASR/TTS research |
| **Shruthi** | Voice endpoints, DB schema and migrations |
| **Santheesh** | `apps/farmer_app` |
| **Thaariha** | `apps/kvk_portal` |

---

## Where to read next

`DEMO_REHEARSAL_RUNBOOK.md` if you're presenting. `AGENTS.md` if you're writing code here. `docs/specs/suchit_module_specs_sih26131.md` if you're touching the gate, RAG or scoring.

<details>
<summary>Full documentation index</summary>

| File | Contents |
|---|---|
| `docs/PRD.md` | Product requirements; scoring model in §7 |
| `docs/API_CONTRACT.md` | REST contract, enums mirroring the PRD |
| `docs/TECH_STACK.md` | Stack choices and the alternatives considered |
| `docs/specs/suchit_module_specs_sih26131.md` | Risk engine, gate, RAG, escalation specs |
| `docs/specs/api_contract_sih26131_delta.md` | What `PROBLEM_STATEMENT` changes (see the caveat under Configuration) |
| `docs/specs/early_warning_alert_spec.md` | Alert triggers and mandatory `inspection_tasks[]` |
| `docs/specs/treatment_efficacy_spec.md` | Efficacy metric definition |
| `docs/FRONTEND_API_ALIGNMENT.md` | Contract-vs-client drift audit |
| `docs/contract_freeze_log.md` | Frozen contract deltas |
| `docs/phase5_walkthrough.md` | Live Postgres integration verification log |
| `docs/decisions/` | Decision records (e.g. ASR/TTS provider choice) |
| `DEMO_REHEARSAL_RUNBOOK.md` | The timed demo walk |
| `JUDGE_DEFENSE_QA.md` | Prepared answers to the predictable questions |
| `AGENTS.md` | Standing rules for coding agents on this repo |

</details>

---

<div align="center">
  <sub><strong>Bhoomi</strong> — the earth. Every number inspectable; escalate, don't guess.</sub>
</div>
