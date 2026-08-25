<div align="center">
  <img src="./assets/bhoomi-logo.png" alt="Bhoomi logo" width="280" />
  <h1>Bhoomi — AI-Powered Farmer Companion</h1>
  <p>Voice-first, multimodal crop advisory that treats every farm as a continuous case file.</p>
  <p><em>Smart India Hackathon · SIH25076 (default) · SIH26131 (feature-flagged)</em></p>
</div>

---

## 1. The problem, and the shape of our answer

A smallholder farmer with a sick crop has two bad options: ask around the village, or ask a chatbot. The chatbot answers one question, forgets the farm the moment the conversation ends, and — this is the part that actually costs money — will produce a fluent, confident answer even when it has no idea. Wrong advice about a leaf blight isn't an embarrassing output. It's a lost season.

So Bhoomi is built around a different default. Instead of "always answer," the system's default is **"answer only when you can show your work, otherwise hand the farmer to a human."**

That single decision drives almost every design choice below. It's why the health score is a hand-written weighted formula instead of a model. It's why there's a `GateDecision` type that can only hold one outcome. It's why retrieval failure is a first-class response shape rather than an error.

### The two hard rules

1. **Never answer below the confidence gate.** If the image model's confidence is under the threshold, no advisory is composed at all.
2. **Never fabricate on no-retrieval.** If nothing in the curated corpus is relevant enough, the system says so and offers escalation.

Both are enforced in orchestration code, not in a prompt. The difference matters: a prompt instruction is a request to a model, and a model can ignore it. A branch in `domain/gate/decide.py` cannot.

---

## 2. How a request actually flows

Take the central interaction — a farmer photographs a diseased leaf and speaks a description. Here's what happens, layer by layer:

```
Flutter app
  │  POST /assets/presigned-url        → uploads photo straight to MinIO/S3, not through the API
  │  POST /farms/{id}/diagnose         → sends only the small asset_id
  ▼
api/v1/diagnose.py                     router: parse, authenticate, hand off. No logic.
  ▼
services/diagnosis_service.py          orchestration
  ├── ImageDiagnosisPort  →  label + confidence          (stub or real ML service)
  ├── domain/gate/decide.py  →  GateDecision             ← the decision point
  │
  ├── if ESCALATE ────────────► services/escalation/compiler.py
  │                              builds a case bundle, routes to an agronomist,
  │                              returns { above_gate: false, escalation: {...} }
  │
  └── if COMPOSE ─────────────► services/rag/pipeline.py
                                 embed query → pgvector similarity search →
                                 relevance check → grounded LLM call →
                                 parse into the 5-point structure + citations
  ▼
services/health_service.py             recompute the score, persist a snapshot
  ▼
response: diagnosis + advisory + citations + health_delta + spoken_summary
```

Two things worth pointing at. First, the gate sits *before* composition, not after — there's no path where the LLM writes advice and something downstream decides whether to show it. Second, the escalation branch produces a complete, useful object; escalating isn't an error path, it's the other half of the product.

### The gate, concretely

`domain/gate/decide.py` is pure — no database, no network, fully unit-testable. It checks three things in order and returns on the first failure:

| Check | Failure code |
|---|---|
| Is the label in `SUPPORTED_LABELS[target_type]`? | `OUT_OF_SCOPE_TARGET` |
| Is `confidence >= confidence_gate` (0.70)? | `BELOW_CONFIDENCE_GATE` |
| Is `retrieval_relevance >= relevance_threshold`? | `NO_RELEVANT_SOURCE` |

The scope list is deliberately bounded, because a model asked to classify something it was never trained on will still return *something* with a confidence number attached. Currently 8 diseases (BLB, blast, brown spot, sheath blight, early/late blight, powdery mildew, leaf curl virus) and 8 pests (stem borer, BPH, leaf folder, green leafhopper, gall midge, fall armyworm, aphid, whitefly).

One detail that's easy to get wrong and was handled correctly here: a *missing* signal is skipped, never treated as a pass. A text-only advisory query has no image confidence, so that check is skipped rather than defaulted to 1.0.

The return type makes the invariant structural — `GateDecision` holds exactly one `outcome`, so a caller cannot end up holding both an advisory and an escalation.

---

## 3. The health score, and why it's plain Python

The score is the most visible number in the product, which makes it the most tempting thing to fake and the easiest thing for a judge to attack. The defense is that it's a documented weighted rubric where every point of movement traces to an input.

Four sub-indices, each 0–100, combined by fixed weights (`domain/health/constants.py`, with an `assert` at import time that they sum to exactly 1.0) — this is the SIH26131 risk model, and it's the only one the engine runs; `PROBLEM_STATEMENT` switches which *routes* are mounted (§5), never which scoring rubric computes the number:

| Sub-index | Weight | What moves it |
|---|---|---|
| `active_problem_severity` | **0.40** | Open problems, penalised by severity |
| `environmental_risk` | 0.25 | Weather deviation from the crop's ideal temp/humidity band at its stage |
| `monitoring_recency` | 0.15 | How stale the last scan is (5 pts/day penalty) |
| `treatment_response` | 0.20 | The latest follow-up: improved / no change / got worse / expert-resolved |

`active_problem_severity` carries the heaviest weight on purpose — an active disease is the single most important fact about a farm, and it should be the thing that visibly moves the number.

Severity penalties subtract from that sub-index: early 30, moderate 55, severe 80. So a newly diagnosed early-stage blight takes the sub-index from 100 to 70, and at weight 0.40 that's a 12-point drop in the total, before the environmental and monitoring effects.

Bands: `unrated` · 0–39 critical · 40–59 poor · 60–74 watch · 75–89 good · 90–100 excellent.

**`unrated` is not zero.** `band_for(None)` returns `UNRATED` and the score field stays null. A farm on day one with no data must never look identical to a farm that's dying — that conflation is the kind of thing that destroys trust in a number permanently.

### The walk is a test, not a slide

`tests/e2e/test_runbook.py` and `scripts/run_demo_e2e.py` drive the whole sequence over real HTTP:

**82 → 68 → 59 → 86**

- **82** baseline: no active problems, ordinary imperfection elsewhere.
- **68** after an early BLB diagnosis: problem load drops, monitoring and environmental nudge down too.
- **59** after a `got_worse` follow-up: severity promotes early → moderate, treatment response collapses, and the drop crosses the auto-escalation threshold.
- **86** after the agronomist resolves it: the problem clears *and* the farm now has a logged scan and a successful treatment, so monitoring and treatment response sit above where they started. Ending above baseline is the correct result — a farm that caught and fixed a problem is better understood than one that never logged anything.

If a judge asks whether the score is decorative, the answer is `make test-e2e`.

---

## 4. Repository layout

```
Bhoomi-SIH-Agri/
├── AGENTS.md                  # standing rules for coding agents working in this repo
├── apps/
│   ├── bhoomi_landing/         # marketing/pitch page (React + Vite) — live against the API when reachable, local demo data otherwise
│   ├── farmer_app/            # Flutter — Riverpod, go_router, dio
│   ├── kvk_portal/            # agronomist case queue + resolve (React + Vite + Tailwind)
│   └── officer_portal/        # land review (React + Vite + Tailwind + Leaflet)
├── services/
│   ├── api/                   # FastAPI backend — the entire intelligence layer
│   └── ml/                    # inference microservice — heuristic (not trained) image/embedding/speech endpoints, see §9
├── data/
│   ├── external/Dataset_v4/   # raw pest dataset snapshot — ground truth, don't edit
│   └── curated/Dataset_v4_validated/
├── docs/                      # PRD, contracts, module specs, decision records
├── infra/                     # docker-compose: Postgres 16 + pgvector, MinIO
└── .github/workflows/         # frontend + mobile CI
```

### Why the backend is layered the way it is

`AGENTS.md` fixes a one-way dependency flow, and the code holds to it:

```
api/v1  →  services  →  domain / repositories  →  adapters
```

- **`api/v1/`** — routers. HTTP in, HTTP out, nothing else. Swapping a transport shouldn't touch logic.
- **`services/`** — orchestration. `health/`, `gate/`, `rag/`, `escalation/`, `alerts/`. This is where use-cases are assembled from pure pieces and ports.
- **`domain/`** — pure functions and named constants. `health/score.py`, `gate/decide.py`, `rag/similarity.py`, `fao56.py`, `queue.py`. No I/O anywhere, which is why most of the 353 tests need no database.
- **`repositories/`** — the only code that touches Postgres, with an in-memory implementation behind the same interface.
- **`ports/`** — typed `Protocol` definitions for every external dependency: weather, LLM, embeddings, image diagnosis, ASR/TTS, storage, roster.
- **`adapters/`** — real and stub implementations, selected in `adapters/dependencies.py` from config.

The payoff is concrete rather than architectural taste: no call site imports a concrete adapter, so flipping `DIAGNOSIS_MODEL=real` in `.env` changes behaviour everywhere with zero code edits, and the whole app runs offline on stubs when the demo network dies.

---

## 5. Configuration and the two problem statements

Defaults live in `app/domain/constants.py` and `app/core/config.py`; override in `services/api/.env`.

| Setting | Values | Default | What it does |
|---|---|---|---|
| `PROBLEM_STATEMENT` | `sih25076` \| `sih26131` | `sih26131` | Switches which routers mount |
| `LAND_API_MODE` | `mock` \| `live` | `mock` | Cadastral lookup adapter |
| `DIAGNOSIS_MODEL` | `stub` \| `real` | `stub` | `real` calls `ML_SERVICE_URL` |
| `EMBEDDING_PROVIDER` | `stub` \| `bge_m3` | `stub` | Also selects the matching RAG threshold |
| `ASR_PROVIDER` / `TTS_PROVIDER` | `stub` \| `bhashini` \| `sarvam` \| `whisper` \| `gtts` | `stub` | Voice adapters |
| `CONFIDENCE_GATE` | float | `0.70` | Disease gate |
| `PEST_CONFIDENCE_GATE` | float | `0.70` | Pest gate — same value today, separately tunable |
| `RAG_RELEVANCE_THRESHOLD` | computed | `0.18` stub / `0.60` bge_m3 | Force with `RAG_RELEVANCE_THRESHOLD_OVERRIDE` |

The RAG threshold is computed rather than fixed for a reason worth understanding: relevance scores from token-hashing stub vectors and from real BGE-m3 dense embeddings live on completely different scales. A single hardcoded number would be either far too strict or effectively disabled depending on which adapter is active, so the threshold follows `EMBEDDING_PROVIDER` automatically.

**The problem-statement switch.** The project was written for SIH25076 (broad farm advisory) and realigned toward SIH26131 (crop disease and pest management). Land registry and revenue-officer review stayed mounted in both modes (they're useful trust-building context regardless of problem statement); only **irrigation resource planning** is truly SIH25076-exclusive — `sih26131` unmounts `resource_plan` (404) and mounts `alerts` instead. Net effect: 45 paths under `sih25076`, 46 under `sih26131` (alerts adds 2, resource_plan removes 2, everything else is shared). `default=sih26131` in `core/config.py` is the live default; the SIH25076 mode exists for the demo-day fallback walkthrough. Note `docs/specs/api_contract_sih26131_delta.md` (§2.1/§2.3) is a stale early draft that describes unmounting `land`/`officer`/`schemes` too — the team superseded that plan (see `tests/unit/test_problem_statement_gating.py`, the authoritative contract test) without updating the doc.

---

## 6. Running it

### Backend

```bash
# 1. Infrastructure — Postgres 16 + pgvector on :5433, MinIO on :9000 (console :9001)
docker compose -f infra/docker-compose.yml up -d

# 2. API
cd services/api
cp .env.example .env
make install          # creates .venv, installs requirements.txt
make migrate          # 5 Alembic revisions
make ingest-corpus    # embeds services/api/corpus/*.md into the knowledge_chunks table
make seed             # demo fixtures
make run              # uvicorn on :8000
```

Swagger at `http://localhost:8000/docs`, ReDoc at `/redoc`, liveness at `GET /health`.

`make demo` chains migrate → ingest-corpus → seed → e2e in one command; that's the demo-box reset. Seeded logins use password `bhoomi123`: farmer `+919944400001`, officer `+919944400002`, agronomist `+919944400003`.

Worth knowing before demo day: **the API boots with no Postgres at all.** Repositories fall back to in-memory and every port defaults to a stub. You lose persistence and real retrieval, but the app comes up — which is the difference between a degraded demo and no demo.

### Frontends

```bash
cd apps/kvk_portal      && npm install && npm run dev    # :5174
cd apps/officer_portal  && npm install && npm run dev    # :5173

cd apps/farmer_app && flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000   # 10.0.2.2 = host, from the Android emulator
flutter analyze && flutter test
```

### Tests

```bash
make test        # 353 tests
make test-e2e    # runbook only — needs a migrated, corpus-ingested Postgres
```

As of now: **351 pass with no database**, because the domain layer is pure. The 2 failures are the `tests/e2e` runbook cases, and they fail on connection refused until Postgres is up — not on logic.

---

## 7. API surface

Base path `/api/v1`. Bearer JWT, with the role claim gating portal routes.

| Area | Endpoints |
|---|---|
| Auth | `POST /auth/register` · `POST /auth/login` · `GET /auth/me` |
| Media | `POST /assets/presigned-url` · `GET /assets/{asset_id}` |
| Voice | `POST /voice/transcribe` · `/voice/synthesize` · `/voice/query` · `/voice/confirm` |
| Farms | `POST /farms` · `GET /farms` (list mine) · `GET,PUT /farms/{id}` · `GET /farms/{id}/summary` |
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
| SIH26131 only | `GET /farms/{id}/alerts` · `POST /alerts/{id}/acknowledge` · `GET /treatments/{id}/efficacy` |

Two conventions that recur: large media never passes through the API (presigned upload straight to object storage, then only the small `asset_id` travels in JSON), and every consequential response carries a `spoken_summary` the client can read aloud locally — both concessions to thin rural bandwidth.

---

## 8. The knowledge corpus

Grounded advisory is only as honest as what it retrieves from, so the two stores are kept separate and their maturity is stated plainly.

**Ingested — `services/api/corpus/`.** Eight markdown documents: rice BLB, blast, brown spot, nitrogen management, seed selection, irrigation at vegetative and reproductive stages, harvest timing. `make ingest-corpus` chunks and embeds these into `knowledge_chunks`, and every advisory citation resolves against them. This is the corpus that actually exists at runtime.

**Staged — `data/curated/Dataset_v4_validated/`.** Eight pest documents (stem borer, BPH, leaf folder, green leafhopper, gall midge, thrips, whorl maggot, earhead bug) from TNAU and ICAR-IRRI, with a manifest, source registry, structured evidence records, a 23-entry Tamil pest lexicon, and reference images.

Read `DATASET_VALIDATION_STATUS.md` before wiring any of it in. The manifest states `production_ingested: false` and `chemical_advice_status: UNVERIFIED` — the pesticide recommendations have not passed regulatory validation, and shipping unvalidated chemical dosages to farmers is a real-world harm, not a demo detail.

---

## 9. Known gaps

Written down so nobody rediscovers them at hour 30.

**`services/ml/` is a heuristic, not a trained model.** It's a real, running FastAPI microservice — `DIAGNOSIS_MODEL=real` genuinely calls it over HTTP end-to-end (color-histogram analysis when given real image bytes, a deterministic asset-id hash otherwise) — but there is no labeled crop-disease dataset or trained weights checked into this repo, so its predictions shouldn't be trusted as diagnostic. It also exposes `/embed`, `/transcribe`, and `/synthesize`; only `/diagnose` is wired from `services/api` today (`adapters/dependencies.py` never routes `EmbeddingPort`/`AsrTtsPort` at `ML_SERVICE_URL`).

~~Treatment-efficacy endpoints don't exist.~~ **Built.** `GET /api/v1/treatments/{treatment_id}/efficacy` (sih26131-only), with the full write-side lifecycle wired into diagnose/followup/agronomist-resolve (`services/efficacy/`). Scoped to the 3 diseases (`bacterial_leaf_blight`, `blast`, `brown_spot`) the ingested corpus documents a first-line treatment for — see `app/domain/efficacy/default_treatments.py`.

**`RAG_RELEVANCE_THRESHOLD=0.18` is calibrated against stub embeddings only.** The `0.60` production figure is a target for a real dense embedding model (e.g. BGE-m3), not a measured value — `EMBEDDING_PROVIDER=bge_m3` is accepted by config but `adapters/dependencies.get_embedding_adapter` always returns the stub regardless; there's no real embedding adapter wired yet. Re-tune when one lands.

**CI has no backend job.** The workflow covers the Flutter app, both portals, and a secret scan. Backend tests run locally via `make test`.

---

## 10. Team

| Member | Owns |
|---|---|
| Suchit Chopade | Health/risk engine, confidence gate, RAG pipeline, escalation compiler, integration |
| Shreekumar | Backend: auth, CRUD, uploads, alerts, deployment |
| Tharun | Corpus curation, pest research, image model, ASR/TTS research |
| Shruthi | Voice endpoints, DB schema and migrations |
| Santheesh | `apps/farmer_app` |
| Thaariha | `apps/officer_portal`, `apps/kvk_portal` |

## 11. Docs

| File | Contents |
|---|---|
| `docs/PRD.md` | Product requirements; health-score model in §7 |
| `docs/API_CONTRACT.md` | REST contract, enums mirroring the PRD |
| `docs/TECH_STACK.md` | Stack choices and the alternatives considered |
| `docs/specs/suchit_module_specs_sih26131.md` | Risk engine, gate, RAG, escalation specs |
| `docs/specs/api_contract_sih26131_delta.md` | Exactly what the `PROBLEM_STATEMENT` flag changes |
| `docs/specs/early_warning_alert_spec.md` | Alert triggers and mandatory `inspection_tasks[]` |
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
