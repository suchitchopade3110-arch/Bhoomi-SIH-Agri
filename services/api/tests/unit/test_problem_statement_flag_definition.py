"""The PROBLEM_STATEMENT flag is *defined*, with an explicit default.

Verification gate for the flag itself, separate from what it gates:

- it exists on ``Settings`` (reachable via both the ``app.config`` spec path
  and the ``app.core.config`` implementation path);
- it defaults to ``"sih26131"`` with nothing set in the environment, so no
  read of it is ever undefined;
- an unrecognized value fails loudly at construction instead of silently
  disabling the SIH26131 feature set;
- the shipped ``.env.example`` files pin it explicitly rather than leaning on
  that default.
"""

from pathlib import Path

import pytest
from pydantic import ValidationError

import app.config as spec_config
import app.core.config as impl_config

REPO_ROOT = Path(__file__).resolve().parents[4]
ENV_EXAMPLES = [
    REPO_ROOT / ".env.example",
    REPO_ROOT / "services" / "api" / ".env.example",
]


def test_flag_is_declared_on_settings():
    assert "PROBLEM_STATEMENT" in impl_config.Settings.model_fields


def test_flag_default_is_sih26131():
    assert impl_config.PROBLEM_STATEMENT_DEFAULT == "sih26131"
    assert impl_config.Settings.model_fields["PROBLEM_STATEMENT"].default == "sih26131"


def test_flag_resolves_to_the_default_when_the_environment_is_silent(monkeypatch):
    """The 'undefined read' case: nothing in the environment, no .env override
    — the attribute still resolves, to the documented default."""
    monkeypatch.delenv("PROBLEM_STATEMENT", raising=False)

    settings = impl_config.Settings(_env_file=None)

    assert settings.PROBLEM_STATEMENT == "sih26131"


def test_flag_is_reachable_through_the_spec_config_path():
    assert spec_config.PROBLEM_STATEMENT_DEFAULT == "sih26131"
    assert spec_config.Settings is impl_config.Settings


def test_unrecognized_value_fails_loudly(monkeypatch):
    """A typo must not silently gate the SIH26131 feature set off."""
    monkeypatch.setenv("PROBLEM_STATEMENT", "sih26132")

    with pytest.raises(ValidationError):
        impl_config.Settings(_env_file=None)


@pytest.mark.parametrize("env_example", ENV_EXAMPLES, ids=lambda p: str(p.name) + ":" + p.parent.name)
def test_env_example_pins_the_flag_explicitly(env_example: Path):
    """The demo environment sets the value rather than relying on the default,
    so `cp .env.example .env` produces a deployment whose contract is visible
    in the file."""
    assert env_example.exists(), f"missing {env_example}"

    lines = [
        line.strip()
        for line in env_example.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("PROBLEM_STATEMENT=")
    ]

    assert len(lines) == 1, f"expected exactly one PROBLEM_STATEMENT= line in {env_example}, got {lines}"
    value = lines[0].split("=", 1)[1].split("#", 1)[0].strip()
    assert value == "sih26131"
