# AGENTS.md — Bhoomi Intelligence Layer (SIH25076)

> Pinned workspace context for Antigravity. Not a task — standing rules.

You are building the backend intelligence layer for **Bhoomi**, a voice-first agricultural advisory platform. You own four modules only: the **health-score engine**, the **confidence gate**, the **RAG pipeline**, and the **escalation compiler**. Everything else (Flutter app, React portals, auth, land registry, scheme discovery) is owned by teammates — do not build it, and do not modify it unless a task explicitly says so.

## Stack (non-negotiable)

- Python 3.11+, FastAPI, Pydantic v2, `pydantic-settings`
- PostgreSQL with PostGIS and pgvector; SQLAlchemy 2.0 async; Alembic for migrations
- pytest for tests
- Package manager: `pyproject.toml` at `services/api/`. Add dependencies there, never with loose `pip install` in code.

## Architecture (non-negotiable)

Strict layered flow, one direction only:

```
api  →  services  →  domain / repositories  →  adapters
```

- **api/** — FastAPI routers. HTTP in, HTTP out. No business logic, no external calls.
- **services/** — orchestration and use-cases. The four modules live here. Services call ports (Protocols) and repositories, never concrete adapters.
- **domain/** — pure types, enums, constants, errors. No I/O, no imports from adapters/repositories.
- **repositories/** — DB persistence via SQLAlchemy async. The only place that touches the database.
- **ports/** — typed `Protocol` interfaces for every external dependency.
- **adapters/** — real and stub implementations of each port. Selection happens in wiring (`app/deps.py`), driven by config.

## Repo structure (monorepo)

```
Bhoomi-SIH-Agri/
├── AGENTS.md                       ← this file (pinned context)
├── services/
│   └── api/                        ← the FastAPI backend (Python)
│       ├── pyproject.toml
│       ├── app/
│       │   ├── main.py             # FastAPI factory + router registration
│       │   ├── config.py           # shim → app.core.config (pydantic-settings)
│       │   ├── deps.py             # shim → app.adapters.dependencies (DI wiring)
│       │   ├── api/v1/             # FastAPI routers
│       │   ├── domain/             # Pure types, enums, constants, errors
│       │   │   ├── enums.py        # All shared enums (spec §2.2)
│       │   │   ├── models.py       # Pydantic v2 domain models
│       │   │   ├── constants.py    # WEIGHTS, SEVERITY_PENALTY, gate thresholds
│       │   │   ├── errors.py       # Stable error codes + domain exceptions
│       │   │   ├── gate/           # Pure gate domain logic (decide.py)
│       │   │   ├── health/         # Pure health score computation (score.py, subindices.py)
│       │   │   ├── rag/            # Pure chunking, similarity, prompt templates
│       │   │   └── escalation/     # Pure escalation summary assembler
│       │   ├── ports/              # Typed Protocol interfaces (one file per port)
│       │   │   ├── weather.py
│       │   │   ├── llm.py
│       │   │   ├── embeddings.py
│       │   │   ├── image_diagnosis.py
│       │   │   ├── asr_tts.py
│       │   │   └── storage.py
│       │   ├── services/           # Orchestration & use-cases
│       │   │   ├── health/         # Health engine (engine.py; re-exports + orchestrates)
│       │   │   ├── health_service.py # Health persistence & context orchestrator
│       │   │   ├── gate/           # Confidence gate (gate.py; re-exports)
│       │   │   ├── gate_service.py # Image + retrieval gating service
│       │   │   ├── rag/            # RAG pipeline (pipeline.py, advisory_service.py)
│       │   │   ├── diagnosis_service.py # Image diagnosis orchestration
│       │   │   ├── escalation/     # Escalation compiler (compiler.py)
│       │   │   └── escalation_service.py # DB-backed case summary & routing
│       │   ├── adapters/           # Concrete + stub port implementations
│       │   └── repositories/       # DB persistence (SQLAlchemy async + pgvector)
│       ├── corpus/                 # Curated advisory docs (8 ICAR PoP markdown docs)
│       ├── db/                     # SQLAlchemy ORM + Alembic migrations
│       └── tests/
│           ├── unit/
│           ├── domain/
│           ├── rag/
│           └── e2e/
└── infra/
    └── docker-compose.yml          # Postgres+PostGIS+pgvector + MinIO
```

## Two hard rules

1. **Never answer below the confidence gate.** If image confidence or retrieval relevance is below its threshold, the system emits an escalation, never advice.
2. **Never fabricate on no-retrieval.** If retrieval returns nothing above `RAG_RELEVANCE_THRESHOLD`, return an honest no-retrieval result and offer escalation. Do not let the LLM compose from its own knowledge.

Both rules live in `services/`, in code a reviewer can point at — not in an LLM system prompt.

## Two failure risks to guard against

1. **A non-deterministic health score.** Same inputs → same output, every time. No randomness, no `datetime.now()` inside the computation (inject timestamps), no floating-point config that drifts.
2. **Bypassing the ports layer.** No service, router, or repository may import a concrete adapter or call an external service directly. Every external dependency goes through a `Protocol` in `ports/`, injected via `deps.py`.

## Config constants

```python
CONFIDENCE_GATE = 0.70  # image-diagnosis confidence floor

# RAG_RELEVANCE_THRESHOLD is NOT a flat value — it's a computed_field on
# Settings (app/core/config.py) that depends on EMBEDDING_PROVIDER:
#   EMBEDDING_PROVIDER=stub (the default)  -> 0.18 (token-hashing vectors)
#   EMBEDDING_PROVIDER=bge_m3              -> 0.60 (real dense embeddings)
# Reading this as a flat 0.60 is wrong for the default config — check
# settings.RAG_RELEVANCE_THRESHOLD (or GET /system/health) for the live
# value, never assume one number.
```

## Domain terminology

`health_band`, `subindex_key`, `HealthSnapshot`, `SubIndex`, `Advisory`, `Citation`, `CaseSummary`, `Decision`, `asset_id`.

Stable error codes: `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `VALIDATION_FAILED`, `LAND_NOT_VERIFIED`, `BELOW_CONFIDENCE_GATE`, `NO_RELEVANT_SOURCE`, `OFFICER_UNAVAILABLE`.

## Working agreement

- Every phase ships with tests. A phase is not done until its own verification block passes.
- Keep changes inside the phase's scope. List any file you touch in your plan before editing it.
- When a dependency is not ready, use the stub adapter and flag it — never block a module you can build in isolation.
- Produce a walkthrough artifact at the end of each phase showing the passing test output.
