"""V1 API Routers aggregator.

Router mounting is gated by ``settings.PROBLEM_STATEMENT`` per
docs/specs/api_contract_sih26131_delta.md:

- ``sih25076`` (default): cadastral/resource routers (``land``, ``officer``,
  ``resource_plan``, ``schemes``) mount alongside core intelligence.
- ``sih26131``: ``land``/``officer``/``resource_plan``/``schemes`` all stay
  mounted in both modes (see README.md §5 — the original plan to unmount
  ``land``/``officer``/``schemes`` under ``sih26131`` was superseded, and
  ``resource_plan`` follows the same "keep it mounted" precedent since
  ``apps/farmer_app``'s Today's Plan screen depends on it live); ``alerts``
  and ``efficacy`` mount additionally.
- Core intelligence routers (auth, farms, health, diagnose, followup,
  agronomist, voice, assets, timeline, weather, system) mount in both modes.
"""

from fastapi import APIRouter
from app.api.v1.advisory import router as advisory_router
from app.api.v1.agronomist import router as agronomist_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.assets import router as assets_router
from app.api.v1.auth import router as auth_router
from app.api.v1.diagnose import router as diagnose_router
from app.api.v1.efficacy import router as efficacy_router
from app.api.v1.escalation import router as escalation_router
from app.api.v1.farms import router as farms_router
from app.api.v1.followup import router as followup_router
from app.api.v1.guidance import router as guidance_router
from app.api.v1.health import router as health_router
from app.api.v1.land import router as land_router
from app.api.v1.officer import router as officer_router
from app.api.v1.resource_plan import router as resource_plan_router
from app.api.v1.schemes import router as schemes_router
from app.api.v1.timeline import router as timeline_router
from app.api.v1.voice import router as voice_router
from app.api.v1.weather import router as weather_router
from app.api.v1.system import router as system_router
from app.core.config import get_settings

api_v1_router = APIRouter()

# Core intelligence routers — active under every PROBLEM_STATEMENT value.
api_v1_router.include_router(auth_router)
api_v1_router.include_router(assets_router)
api_v1_router.include_router(voice_router)
api_v1_router.include_router(farms_router)
api_v1_router.include_router(health_router)
api_v1_router.include_router(diagnose_router)
api_v1_router.include_router(advisory_router)
api_v1_router.include_router(guidance_router)
api_v1_router.include_router(timeline_router)
api_v1_router.include_router(followup_router)
api_v1_router.include_router(escalation_router)
api_v1_router.include_router(agronomist_router)
api_v1_router.include_router(weather_router)
api_v1_router.include_router(system_router)

api_v1_router.include_router(land_router)
api_v1_router.include_router(officer_router)
api_v1_router.include_router(resource_plan_router)
api_v1_router.include_router(schemes_router)

if get_settings().PROBLEM_STATEMENT != "sih25076":
    # sih26131: alerts, efficacy mount additionally.
    api_v1_router.include_router(alerts_router)
    api_v1_router.include_router(efficacy_router)

__all__ = ["api_v1_router"]
