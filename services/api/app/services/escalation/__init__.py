"""services/escalation/ — spec-mandated package for the escalation compiler.

Triggers: below-gate / out-of-scope (Phase 2), ``got_worse`` past threshold
(follow-up), no-retrieval on diagnosis (Phase 3).  All three fire
``build_case_summary``.
"""

from app.services.escalation.compiler import build_case_summary  # noqa: F401

__all__ = ["build_case_summary"]
