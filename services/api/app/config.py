"""app/config.py — spec-mandated shim to app.core.config.

The implementation lives in ``app.core.config`` (pydantic-settings, reads
``.env``). This shim exists so the spec-path ``from app.config import ...``
works alongside the existing ``from app.core.config import ...`` path.

Feature flag ``PROBLEM_STATEMENT`` is declared on ``Settings`` in
``app.core.config`` with an explicit default of ``"sih26131"``, re-exported
here as ``PROBLEM_STATEMENT_DEFAULT`` so ``from app.config import
PROBLEM_STATEMENT_DEFAULT`` resolves. It is a field with a default, not an
optional lookup: every read (``settings.PROBLEM_STATEMENT``) is defined even
when the environment and ``.env`` say nothing about it, and an unrecognized
value fails validation at import time instead of silently gating features
off. See docs/specs/problem_statement_flag_off_contract.md for what the
SIH26131-only endpoints return when the flag is not ``"sih26131"``.
"""

from app.core.config import (  # noqa: F401
    PROBLEM_STATEMENT_DEFAULT,
    PROBLEM_STATEMENT_VALUES,
    ProblemStatement,
    Settings,
    get_settings,
    settings,
)

__all__ = [
    "PROBLEM_STATEMENT_DEFAULT",
    "PROBLEM_STATEMENT_VALUES",
    "ProblemStatement",
    "Settings",
    "get_settings",
    "settings",
]
