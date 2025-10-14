import sys
from pathlib import Path

import pytest

from tools.testing import living_docs_guard


def run_guard(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    files: list[str],
    extra_args: list[str] | None = None,
) -> int:
    argv = ["living_docs_guard.py", "--root", str(tmp_path)]
    if extra_args:
        argv.extend(extra_args)
    argv.extend(["--files", *files])
    monkeypatch.setattr(sys, "argv", argv)
    return living_docs_guard.main()


def write_reconciliation(path: Path, rows: list[str]) -> None:
    content = [
        "| date | artifact | status | notes |",
        "| --- | --- | --- | --- |",
        *rows,
    ]
    path.write_text("\n".join(content), encoding="utf-8")


def test_guard_passes_with_closed_items(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "update.md").write_text("updated doc", encoding="utf-8")
    reconciliation = docs_dir / "living-docs-reconciliation.md"
    write_reconciliation(
        reconciliation,
        ["| 2024-01-01 | Update runbook | closed | completed |"],
    )

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        ["docs/update.md"],
        extra_args=["--fail-on-placeholder"],
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.err == ""


def test_guard_fails_on_open_rows(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "update.md").write_text("baseline", encoding="utf-8")
    reconciliation = docs_dir / "living-docs-reconciliation.md"
    write_reconciliation(
        reconciliation,
        ["| 2024-01-02 | Capture metrics | open | pending evidence |"],
    )

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        ["docs/update.md"],
        extra_args=["--fail-on-placeholder"],
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "outstanding documentation gaps" in captured.err


def test_guard_requires_doc_updates_for_non_doc_changes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    reconciliation = docs_dir / "living-docs-reconciliation.md"
    write_reconciliation(
        reconciliation,
        ["| 2024-01-03 | Baseline docs | closed | synced |"],
    )

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        ["tools/new_script.py"],
        extra_args=["--fail-on-placeholder"],
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "without accompanying documentation changes" in captured.err


def test_guard_fails_when_placeholder_present(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "update.md").write_text("baseline", encoding="utf-8")
    reconciliation = docs_dir / "living-docs-reconciliation.md"
    write_reconciliation(
        reconciliation,
        ["| YYYY-MM-DD | Placeholder | pending | fill me |"],
    )

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        ["docs/update.md"],
        extra_args=["--fail-on-placeholder"],
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "remove the placeholder row" in captured.err
