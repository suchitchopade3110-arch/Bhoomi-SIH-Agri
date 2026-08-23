# Phase 5 — Integration Verification (Live Postgres & E2E Proof)

## 1. Executive Summary

Phase 5 integration verification has executed **live against real PostgreSQL with pgvector** (container `bhoomi-postgres` on host port `5433`).

All 8 ICAR Package-of-Practices knowledge documents were embedded and stored in pgvector (`knowledge_chunks` table), all 4 Alembic database migrations applied cleanly, and the complete 8-step runbook along with feature-flag branches were executed twice back-to-back with zero network skips or mocking fallbacks.

---

## 2. Live Test Results & Timings

### A. E2E Test Suite Run 1
```
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\SUCHIT CHOPADE\OneDrive\Desktop\Bhoomi-SIH-Agri\services\api
configfile: pyproject.toml
plugins: anyio-4.12.1, langsmith-0.7.24, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 2 items

tests/e2e/test_runbook.py::test_full_runbook_walks_82_68_86 PASSED       [ 50%]
tests/e2e/test_runbook.py::test_land_api_mode_flag_demos_both_paths PASSED [100%]

============================== slowest durations ==============================
1.77s call     tests/e2e/test_runbook.py::test_full_runbook_walks_82_68_86
0.56s call     tests/e2e/test_runbook.py::test_land_api_mode_flag_demos_both_paths
======================= 2 passed, 231 warnings in 3.40s =======================
```

### B. E2E Test Suite Run 2 (Back-to-Back)
```
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\SUCHIT CHOPADE\OneDrive\Desktop\Bhoomi-SIH-Agri\services\api
configfile: pyproject.toml
plugins: anyio-4.12.1, langsmith-0.7.24, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 2 items

tests/e2e/test_runbook.py::test_full_runbook_walks_82_68_86 PASSED       [ 50%]
tests/e2e/test_runbook.py::test_land_api_mode_flag_demos_both_paths PASSED [100%]

============================== slowest durations ==============================
1.90s call     tests/e2e/test_runbook.py::test_full_runbook_walks_82_68_86
0.80s call     tests/e2e/test_runbook.py::test_land_api_mode_flag_demos_both_paths
======================= 2 passed, 231 warnings in 3.67s =======================
```

### C. Full Repository Suite (Unit, Domain, RAG, E2E)
```
pytest tests/domain tests/rag tests/unit tests/e2e -q
........................................................................ [ 29%]
........................................................................ [ 58%]
........................................................................ [ 87%]
................................                                         [100%]
248 passed, 237 warnings in 4.62s
```

---

## 3. The 8-Step Runbook Verification

The complete lifecycle executed against real Postgres tables:
1. **Onboard**: Farmer registers, adds farm $\rightarrow$ `land_status = unverified`, `score = None (unrated)`
2. **Land Verification**: Unlisted survey number $\rightarrow$ `202 Accepted` (`pending_review`)
3. **Officer Review**: Agronomist/Officer validates record $\rightarrow$ `200 OK` (`verified`)
4. **FAO-56 Resource Plan**: Meteorological data fetched $\rightarrow$ `et0_mm_day`, `kc_factor`, `etc_mm_day`, `effective_rainfall_mm`, `irrigation_need_mm` computed and persisted
5. **Baseline Score**: Calibrated inputs evaluated $\rightarrow$ **`82 / good`**
6. **Day 22 Diagnose (BLB)**: Image diagnosis above confidence gate, retrieves ICAR PoP chunks $\rightarrow$ **`68 / watch`** (`health_delta = {"from": 82, "to": 68}`)
7. **Follow-Up (Got Worse)**: Severity promoted Early $\rightarrow$ Moderate, auto-escalates case $\rightarrow$ **`< 68 / poor`**
8. **Agronomist Resolves**: Dr. Lakshmi prescribes copper oxychloride $\rightarrow$ **`86 / good`**
9. **Scheme Matching**: Verified farm profile with active problem matches TN Crop Protection subsidy scheme.

---

## 4. Feature Flag Duality Verified

- `LAND_API_MODE=mock`: Whitelisted survey number returns `200 OK` with `status="verified"`.
- `LAND_API_MODE=live`: Same survey number routes to human-in-the-loop review, returning `202 Accepted` with `status="pending_review"`.
