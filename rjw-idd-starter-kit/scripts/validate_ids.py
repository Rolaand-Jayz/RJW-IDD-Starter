#!/usr/bin/env python3
"""Validate RJW-IDD traceability ledgers and evidence references."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, List


EVD_RE = re.compile(r"EVD-\d{4}")
REQ_RE = re.compile(r"REQ-\d{4}")
SPEC_RE = re.compile(r"SPEC-\d{4}")
TEST_RE = re.compile(r"TEST-\d{4}")
DOC_RE = re.compile(r"DOC-\d{4}")
ID_TOKEN_RE = re.compile(r"(?:REQ|SPEC|TEST|DOC|DEC|EVD|INTEG)-\d{4}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root to validate (default: project root)",
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        default=[],
        help="Relative file paths that must include evidence references when referencing specs/requirements.",
    )
    return parser.parse_args()


def validate_requirement_ledger(path: Path, errors: List[str]) -> None:
    if not path.exists():
        errors.append(f"missing requirement ledger: {path}")
        return

    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row_num, row in enumerate(reader, start=2):
            req_id = row.get("req_id", "").strip()
            if not REQ_RE.fullmatch(req_id):
                errors.append(f"{path}: row {row_num} invalid req_id '{req_id}'")

            evidence = [token.strip() for token in row.get("evidence_refs", "").split(";") if token.strip()]
            if not evidence:
                errors.append(f"{path}: {req_id} missing evidence_refs")
            for token in evidence:
                if not EVD_RE.fullmatch(token):
                    errors.append(f"{path}: {req_id} invalid evidence token '{token}'")

            specs = [token.strip() for token in row.get("spec_refs", "").split(";") if token.strip()]
            if not specs:
                errors.append(f"{path}: {req_id} missing spec_refs")
            for token in specs:
                if not SPEC_RE.fullmatch(token):
                    errors.append(f"{path}: {req_id} invalid spec token '{token}'")

            tests = [token.strip() for token in row.get("tests_refs", "").split(";") if token.strip()]
            if not tests:
                errors.append(f"{path}: {req_id} missing tests_refs")
            for token in tests:
                if not TEST_RE.fullmatch(token):
                    errors.append(f"{path}: {req_id} invalid test token '{token}'")

            next_review = row.get("next_review", "").strip()
            if not next_review:
                errors.append(f"{path}: {req_id} missing next_review date")
            else:
                try:
                    datetime.strptime(next_review, "%Y-%m-%d")
                except ValueError:
                    errors.append(f"{path}: {req_id} invalid next_review '{next_review}'")


def validate_test_ledger(path: Path, errors: List[str]) -> None:
    if not path.exists():
        errors.append(f"missing test ledger: {path}")
        return

    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row_num, row in enumerate(reader, start=2):
            test_id = row.get("test_id", "").strip()
            if not TEST_RE.fullmatch(test_id):
                errors.append(f"{path}: row {row_num} invalid test_id '{test_id}'")

            related_req = [token.strip() for token in row.get("related_req", "").split(";") if token.strip()]
            if not related_req:
                errors.append(f"{path}: {test_id} missing related_req")
            for token in related_req:
                if not REQ_RE.fullmatch(token):
                    errors.append(f"{path}: {test_id} invalid related_req token '{token}'")

            related_spec = [token.strip() for token in row.get("related_spec", "").split(";") if token.strip()]
            for token in related_spec:
                if not SPEC_RE.fullmatch(token):
                    errors.append(f"{path}: {test_id} invalid related_spec token '{token}'")

            criteria = row.get("criteria", "").strip()
            if not criteria:
                errors.append(f"{path}: {test_id} missing criteria description")


def validate_change_log(path: Path, errors: List[str]) -> None:
    if not path.exists():
        errors.append(f"missing change log: {path}")
        return

    with path.open(encoding="utf-8") as handle:
        for line_num, line in enumerate(handle, start=1):
            if not line.startswith("| change-"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) < 4:
                errors.append(f"{path}: line {line_num} malformed change row")
                continue
            change_id = cells[0]
            impacted = cells[3]
            if not change_id or not change_id.startswith("change-"):
                errors.append(f"{path}: line {line_num} invalid change_id '{change_id}'")
            impacted_tokens = [token.strip() for token in impacted.split(";") if token.strip()]
            if not impacted_tokens:
                errors.append(f"{path}: {change_id} missing impacted_ids")


def validate_paths(root: Path, paths: Iterable[str], errors: List[str]) -> None:
    for raw_path in paths:
        path = (root / raw_path).resolve()
        if not path.exists():
            errors.append(f"specified path not found: {raw_path}")
            continue
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        references_present = any(pattern.search(text) for pattern in (REQ_RE, SPEC_RE, DOC_RE))
        if references_present and not EVD_RE.search(text):
            errors.append(f"{raw_path}: references requirements/specs without citing evidence")


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors: List[str] = []

    validate_requirement_ledger(root / "artifacts" / "ledgers" / "requirement-ledger.csv", errors)
    validate_test_ledger(root / "artifacts" / "ledgers" / "test-ledger.csv", errors)
    validate_change_log(root / "docs" / "change-log.md", errors)
    validate_paths(root, args.paths, errors)

    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
