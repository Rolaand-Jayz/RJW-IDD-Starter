import sys
from pathlib import Path

import pytest

from tools.testing import governance_alignment_guard


LEDGER_HEADER = "req_id,status,title,evidence_refs,spec_refs,tests_refs,owner,next_review,notes"


def run_guard(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, files: list[str]) -> int:
    argv = ["governance_alignment_guard.py", "--root", str(tmp_path), "--files", *files]
    monkeypatch.setattr(sys, "argv", argv)
    return governance_alignment_guard.main()


def write_ledger(path: Path, spec_refs: str) -> None:
    content = "\n".join(
        [
            LEDGER_HEADER,
            f"REQ-0001,active,Sample requirement,EVD-0001,{spec_refs},TEST-0001,owner,2024-01-01,notes",
        ]
    )
    path.write_text(content, encoding="utf-8")


@pytest.fixture()
def setup_repo(tmp_path: Path) -> None:
    (tmp_path / "artifacts" / "ledgers").mkdir(parents=True)
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    (tmp_path / "specs").mkdir()


def test_guard_accepts_aligned_spec_and_decision(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], setup_repo: None) -> None:
    ledger_path = tmp_path / "artifacts/ledgers/requirement-ledger.csv"
    write_ledger(ledger_path, "SPEC-0401")
    spec_path = tmp_path / "specs/SPEC-0401-example.md"
    spec_path.write_text("Spec body", encoding="utf-8")
    decision_path = tmp_path / "docs/decisions/DEC-0001.md"
    decision_path.write_text("# DEC-0001 — Decision\nDetails referencing DEC-0001", encoding="utf-8")

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        [
            "specs/SPEC-0401-example.md",
            "artifacts/ledgers/requirement-ledger.csv",
            "docs/decisions/DEC-0001.md",
        ],
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.err == ""


def test_guard_flags_missing_spec_reference(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], setup_repo: None) -> None:
    ledger_path = tmp_path / "artifacts/ledgers/requirement-ledger.csv"
    write_ledger(ledger_path, "SPEC-0501")
    (tmp_path / "specs/SPEC-0401-example.md").write_text("Spec body", encoding="utf-8")
    decision_path = tmp_path / "docs/decisions/DEC-0001.md"
    decision_path.write_text("# DEC-0001 — Decision\nDetails referencing DEC-0001", encoding="utf-8")

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        [
            "specs/SPEC-0401-example.md",
            "artifacts/ledgers/requirement-ledger.csv",
            "docs/decisions/DEC-0001.md",
        ],
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "SPEC-0401" in captured.err


def test_guard_flags_decision_placeholder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], setup_repo: None) -> None:
    ledger_path = tmp_path / "artifacts/ledgers/requirement-ledger.csv"
    write_ledger(ledger_path, "SPEC-0501")
    decision_path = tmp_path / "docs/decisions/DEC-0002.md"
    decision_path.write_text("# DEC-XXXX — Update\nPending final ID", encoding="utf-8")

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        ["docs/decisions/DEC-0002.md"],
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "placeholder DEC-XXXX" in captured.err


def test_guard_flags_missing_decision_id_reference(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], setup_repo: None) -> None:
    ledger_path = tmp_path / "artifacts/ledgers/requirement-ledger.csv"
    write_ledger(ledger_path, "SPEC-0501")
    decision_path = tmp_path / "docs/decisions/DEC-0003.md"
    decision_path.write_text("# Decision without id", encoding="utf-8")

    exit_code = run_guard(
        monkeypatch,
        tmp_path,
        ["docs/decisions/DEC-0003.md"],
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "must reference its DEC id" in captured.err
