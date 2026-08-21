"""POST /problems/{id}/escalate schemas — mirror contract §2.13 exactly."""

from pydantic import BaseModel

from app.core.enums import CaseStatus


class EscalateResponse(BaseModel):
    """Contract §2.13: ``{ "case_id": "c_5", "assigned_to": "agronomist:kvk_erode", "status": "assigned" }``."""

    case_id: str
    assigned_to: str
    status: CaseStatus
