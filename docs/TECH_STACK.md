# Tech Stack
## AI-Based Farmer Query Support & Advisory System

**Project code:** SIH25076
**Companion to:** `PRD.md` (enums, entities, and the health-score model here mirror PRD §7 and §9), `API_CONTRACT.md` (Part 2 of the original combined doc)
**Status:** Draft v1.0 · for team review
**Assumed baseline:** Python/FastAPI backend, Flutter farmer app, React portals. The JS-first swap is noted inline (§1.6) if your team is TypeScript-first.

---

## 1.1 Guiding constraints

Every stack choice below traces back to a constraint the PRD already committed to:

- **Low-end Android + patchy rural bandwidth** → the farmer client must be light, and the API must tolerate slow/dropped connections and degrade rather than fail.
- **Voice-first in a regional language** → ASR/TTS must handle Tamil credibly, and the Indian-government angle (Bhashini/AI4Bharat) is both a technical fit and a pitch asset.
- **Grounded, cited advisory with a no-retrieval fallback** → we need a real vector store, a relevance threshold, and citation plumbing, not a raw LLM call.
- **Boundary geometry for land records** → geospatial types belong in the database, not bolted on.
- **Explainable health score with an audit trail** → the scoring engine is deterministic backend code, not a model endpoint.
- **Hackathon timeline** → prefer managed/free services and one database that does three jobs over five moving parts.

## 1.2 The stack at a glance

| Layer | Choice | Why this | Hackathon alternative |
|---|---|---|---|
| Farmer app | **Flutter** (Android) | One codebase, strong performance on low-end devices, good native audio/camera access, offline-capable widgets for degraded mode | **PWA (React + Vite)** if you need the fastest possible demo and web is acceptable |
| Officer & KVK portals | **React + Vite + Tailwind + shadcn/ui** | Desktop/laptop users; fast to build; map + queue UIs are trivial in React | Same |
| Map / boundary sketch | **Leaflet + OpenStreetMap** | Free, no key, good enough for boundary drawing and display | MapLibre |
| Backend API | **Python + FastAPI** | Async, first-class Pydantic schemas (typed request/response ≈ this contract for free), best ecosystem for RAG/ML glue | Node + NestJS if JS-first |
| Data + geo + vectors | **PostgreSQL + PostGIS + pgvector** | One database covers relational data, land-boundary geometry, and RAG embeddings — three needs, one service to run | Add Qdrant/Chroma only if pgvector recall is insufficient |
| Object storage (photos/audio) | **S3-compatible (MinIO local / Cloudflare R2)** | Cheap, presigned uploads keep large blobs off the API | Cloudinary (adds free image transforms) |
| ASR / TTS (Tamil) | **Bhashini / AI4Bharat (IndicASR, IndicTTS)** primary; **Whisper** fallback | Indian-language accuracy + a strong SIH narrative; Whisper covers gaps | Google/Azure Speech if you have credits |
| Image disease model | **PyTorch model (ViT/CNN) fine-tuned on PlantVillage + crop-specific data**, served in-process | Bounded crop set; confidence score is native to the model → drives the §5.6 gate | Hosted inference (Hugging Face) if you don't want the weights in the API |
| RAG generation | **LLM API** (Claude / GPT) with strict grounding prompt + citations | Fastest path to reliable, cited output; no model hosting | Local Llama-3-8B-Instruct if offline/cost demands it |
| Embeddings | **BGE-m3** (multilingual) via pgvector | Handles Tamil + English corpus; strong retrieval quality | e5-multilingual |
| Weather | **Open-Meteo** (ET₀, rainfall, forecast; no API key) | Free, reliable for demo, returns reference ET₀ directly | IMD feed for the production story |
| Scheduling (follow-ups) | **APScheduler** (demo) → **Celery + Redis** (pilot) | APScheduler is one dependency for the demo; swap up later | Celery from day one if you prefer |
| Auth | **JWT**; farmer via **phone OTP**, officers via email/password | Matches the literacy-free farmer flow; role claims gate portals | — |
| Hosting | **Single VM (Fly.io / Railway / Render)** + managed Postgres | One box demos the whole loop; scale later | Docker Compose on any VM |

## 1.3 Three decisions worth defending out loud

**One database, three jobs.** Postgres with PostGIS and pgvector handles relational records, land-boundary geometry, and RAG embeddings in a single service. Fewer moving parts to break mid-demo, and boundary queries (does this point fall in a verified polygon?) become plain SQL. If a judge asks about your data layer, this is a crisp, mature answer.

**The scoring engine is code, not a model.** The health score (PRD §7) is deterministic Python: sub-indices in, weighted sum out, every component persisted on the snapshot. This is what makes the audit trail real and the "82 → 68 → 86" walkthrough reproducible on demand. Never let this become an opaque model call — the whole point is explainability.

**The confidence gate lives at the boundary, not inside the LLM.** The image model returns a probability; the RAG retriever returns a relevance score. The orchestration layer checks both against thresholds *before* composing an answer. If either fails, it emits an escalation object instead of advice. This keeps the "never fabricate" guarantee (PRD §5.6, §5.7) enforceable in code you can point at, rather than a hope pinned on prompt wording.

## 1.4 Bandwidth-degraded behaviour (cross-cutting)

The API is designed so the client can survive a bad connection:
- Large blobs (audio, photos) upload directly to object storage via **presigned URLs** — the API only exchanges small JSON.
- Endpoints that trigger heavy work (diagnosis, RAG) accept an already-uploaded `asset_id` rather than the raw bytes, so a dropped upload never blocks the request.
- Every consequential response carries a short `spoken_summary` string the client can TTS locally, so the farmer gets an audible confirmation even on a thin pipe.

## 1.5 Environments & config

- Secrets (LLM keys, DB URL, storage creds) via environment variables; never in the client.
- `X-API-Version` pinned in the path (`/api/v1`).
- Feature flags for the mocked paths (PRD §4): `LAND_API_MODE = mock | live`, `DIAGNOSIS_MODEL = real | stub`. This lets you demo the "auto-lookup succeeds" and "auto-lookup fails → HITL" cases from the same build by flipping a flag.

## 1.6 The JS-first swap

If the team is TypeScript-first and Python isn't a strength, this maps cleanly: **NestJS** (backend, keeps decorator-based DTOs ≈ this contract), **Prisma + PostGIS + pgvector** (data), and the ML pieces (image model, embeddings) run as a small separate Python inference service the Node API calls. Everything in `API_CONTRACT.md` stays identical — the contract is language-agnostic.

---

*End of Tech Stack v1.0. See `API_CONTRACT.md` for Part 2 — the API contract itself.*
