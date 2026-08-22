"""services/gate/ — spec-mandated package for the confidence gate.

The pure ``decide()`` function lives in ``app.domain.gate.decide``.
``GateService`` (the orchestration wrapper) lives in
``app.services.gate_service``. Both are re-exported from here.
"""

from app.domain.gate.decide import decide  # noqa: F401
from app.domain.gate.decision import GateDecision  # noqa: F401
from app.services.gate_service import GateService, get_gate_service  # noqa: F401

__all__ = ["decide", "GateDecision", "GateService", "get_gate_service"]
