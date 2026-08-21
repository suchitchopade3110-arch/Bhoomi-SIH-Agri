"""The gate's result type — a domain value object, independent of any API schema."""

from dataclasses import dataclass

from app.core.enums import GateOutcome


@dataclass(frozen=True)
class GateDecision:
    """Exactly one outcome: ``compose`` or ``escalate`` — never both, never neither.

    ``reason``/``error_code`` are ``None`` on ``compose`` and always set on
    ``escalate``; ``spoken_summary`` is always set on ``escalate`` (a plain-
    language "not sure — sent to an expert" statement) and ``None`` on
    ``compose``, since the composed advisory generates its own spoken
    summary elsewhere (Phase 3).
    """

    outcome: GateOutcome
    reason: str | None
    error_code: str | None
    spoken_summary: str | None

    @property
    def should_compose(self) -> bool:
        return self.outcome == GateOutcome.COMPOSE

    @property
    def should_escalate(self) -> bool:
        return self.outcome == GateOutcome.ESCALATE
