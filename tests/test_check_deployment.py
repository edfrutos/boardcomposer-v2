"""Tests for scripts/check_deployment.py (the stale-deploy guardrail)."""

import importlib.util
import sys
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "check_deployment",
    Path(__file__).resolve().parent.parent / "scripts" / "check_deployment.py",
)
check_deployment = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(check_deployment)


@pytest.fixture
def fake_health(monkeypatch):
    """Replace the network call with a canned /health payload."""

    def _install(payload):
        monkeypatch.setattr(
            check_deployment,
            "_fetch_health",
            lambda api_url, auth, timeout: payload,
        )

    return _install


def _run(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["check_deployment.py", *argv])
    check_deployment.main()


def test_in_sync_returns_cleanly(monkeypatch, fake_health, capsys):
    current = check_deployment._project_version()
    fake_health({"status": "ok", "version": current})

    _run(monkeypatch)

    assert "en sync" in capsys.readouterr().out


def test_drift_exits_with_code_1(monkeypatch, fake_health):
    fake_health({"status": "ok", "version": "0.0.1"})

    with pytest.raises(SystemExit) as exc:
        _run(monkeypatch)

    assert exc.value.code == check_deployment.EXIT_DRIFT


def test_missing_version_field_exits_with_code_1(monkeypatch, fake_health):
    fake_health({"status": "ok"})

    with pytest.raises(SystemExit) as exc:
        _run(monkeypatch)

    assert exc.value.code == check_deployment.EXIT_DRIFT


def test_expect_override_is_honoured(monkeypatch, fake_health, capsys):
    fake_health({"status": "ok", "version": "9.9.9"})

    _run(monkeypatch, "--expect", "9.9.9")

    assert "en sync (9.9.9)" in capsys.readouterr().out


def test_studio_reminder_is_always_printed(monkeypatch, fake_health, capsys):
    fake_health({"status": "ok", "version": check_deployment._project_version()})

    _run(monkeypatch)

    assert check_deployment.STUDIO_CONTAINER in capsys.readouterr().out


def test_project_version_regex_fallback_matches_tomllib(monkeypatch):
    """The pre-3.11 path (VPS host has no tomllib) must read the same value."""
    with_tomllib = check_deployment._project_version()

    monkeypatch.setattr(check_deployment, "tomllib", None)
    without_tomllib = check_deployment._project_version()

    assert without_tomllib == with_tomllib
