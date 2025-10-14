from __future__ import annotations

import types
from pathlib import Path

import pytest

import tools.health_check as health_check_module  # type: ignore[import-not-found]


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    return tmp_path


def test_health_checker_handles_optional_dependencies(monkeypatch: pytest.MonkeyPatch, project_root: Path) -> None:
    expected_modules = {"pytest"}

    def fake_find_spec(name: str) -> object | None:
        if name in expected_modules:
            return object()
        return None

    dummy_pytest = types.SimpleNamespace(__version__="8.0.0")

    def fake_import_module(name: str):
        if name == "pytest":
            return dummy_pytest
        raise ImportError(name)

    class DummyCompletedProcess:
        def __init__(self, returncode: int = 0, stdout: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = ""

    def fake_run(cmd: list[str], **_: object) -> DummyCompletedProcess:
        if cmd[0] == "git":
            return DummyCompletedProcess(0, "git version 2.0\n")
        raise FileNotFoundError

    monkeypatch.setattr(health_check_module.importlib.util, "find_spec", fake_find_spec)
    monkeypatch.setattr(health_check_module.importlib, "import_module", fake_import_module)
    monkeypatch.setattr(health_check_module.subprocess, "run", fake_run)

    checker = health_check_module.HealthChecker(str(project_root))
    results = checker.run_all_checks()

    assert results["overall_status"] != "error"
    assert results["dependencies"]["pytest"]["status"] == "ok"
    assert results["dependencies"]["black"]["status"] == "warning"
    assert results["services"]["git"]["status"] == "ok"
    assert results["services"]["docker"]["status"] == "warning"
