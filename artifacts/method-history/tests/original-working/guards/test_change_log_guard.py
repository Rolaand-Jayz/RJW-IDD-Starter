import sys
from pathlib import Path

import pytest

from tools.testing import change_log_guard


def run_guard(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, files: list[str] | None) -> int:
    argv = ["change_log_guard.py", "--root", str(tmp_path)]
    if files is not None:
        argv += ["--files", *files]
    monkeypatch.setattr(sys, "argv", argv)
    return change_log_guard.main()


def write_change_log(path: Path, rows: list[str]) -> None:
    content = [
        "| change id | date | summary | impacted ids | verification |",
        "| --- | --- | --- | --- | --- |",
        *rows,
    ]
    path.write_text("\n".join(content), encoding="utf-8")


def test_guard_allows_valid_latest_row(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    specs_dir = tmp_path / "specs"
    specs_dir.mkdir()
    (specs_dir / "SPEC-0401-observability-telemetry.md").write_text("example", encoding="utf-8")
    change_log_path = docs_dir / "change-log.md"
    write_change_log(
        change_log_path,
        ["| change-20240101-01 | 2024-01-01 | Added telemetry insights | SPEC-0401 | Verified with regression |"]
    )

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        [
            "templates-and-examples/templates/change-logs/CHANGELOG-template.md",
            "specs/SPEC-0401-observability-telemetry.md",
        ],
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.err == ""


def test_guard_requires_change_log_for_relevant_updates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "specs").mkdir()

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        ["specs/SPEC-0401-observability-telemetry.md"],
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "change-log guard: detected updates" in captured.err


def test_guard_rejects_invalid_impacted_ids(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    change_log_path = docs_dir / "change-log.md"
    write_change_log(
        change_log_path,
        ["| change-20240101-01 | 2024-01-01 | Added telemetry insights | | Pending |"]
    )

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        ["templates-and-examples/templates/change-logs/CHANGELOG-template.md"],
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "must list impacted ids" in captured.err
