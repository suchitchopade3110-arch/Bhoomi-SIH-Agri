# Bhoomi API — Phase 5 dev/demo targets.
#
# Assumes a PostgreSQL + PostGIS + pgvector instance reachable at
# $DATABASE_URL (see .env / .env.example) — `docker compose -f
# ../../infra/docker-compose.yml up -d postgres` locally, or the
# system-installed postgresql-16 + postgresql-16-pgvector + postgresql-16-postgis-3
# packages this environment used during development.

PYTHON := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: venv install migrate downgrade ingest-corpus seed run test test-e2e smoke demo

venv:
	python3 -m venv .venv

install: venv
	$(PIP) install -q -r requirements.txt

migrate:
	$(PYTHON) -m alembic upgrade head

downgrade:
	$(PYTHON) -m alembic downgrade base

ingest-corpus:
	$(PYTHON) -m app.services.rag.ingest

seed:
	$(PYTHON) -m scripts.seed

run:
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# All unit/domain tests (offline, no DB required) + the Phase-5 e2e runbook
# (needs a migrated, corpus-ingested Postgres — see `make demo` below).
test:
	$(PYTHON) -m pytest -q

test-e2e:
	$(PYTHON) -m pytest tests/e2e -q

# The judge's demo-box command: fresh migrations, corpus, seed data, then
# proves the app actually boots and talks to Postgres — all before judging
# starts (Phase 5 DoD item 5).
smoke: migrate ingest-corpus seed
	$(PYTHON) -m scripts.smoke

# One-shot: get a clean environment to the exact state the runbook and demo
# script assume, then run the full e2e proof.
demo: migrate ingest-corpus seed test-e2e
	@echo ""
	@echo "Demo data seeded. Login as farmer +919944400001 / officer +919944400002 / agronomist +919944400003, password: bhoomi123"
	@echo "Run 'make run' to start the API on http://localhost:8000 (docs at /docs)."
