#!/usr/bin/env python3
"""Ensure RJW-IDD changes include a well-formed change log entry."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

IGNORED_PREFIXES = (
    "workspace/",
    "sandbox/",
    "tmp/",
)
REQUIRED_FILE = "docs/change-log.md"
CHANGE_ID_RE = re.compile(r"^change-\d{8}-\d{2}$")
ID_TOKEN_RE = re.compile(r"^[A-Z]{2,}-\d{4}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--files",
        nargs="+",
        help="Changed file paths relative to repository root (as reported by git diff).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root for existence checks.",
    )
    return parser.parse_args()


def normalise(paths: Iterable[str]) -> list[str]:
    normalised: list[str] = []
    for raw in paths:
        if raw is None:
            continue
        path = raw.strip()
        if not path:
            continue
        normalised.append(path.replace("\\", "/"))
    return normalised


def should_ignore(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in IGNORED_PREFIXES)


def extract_change_rows(text: List[str]) -> List[Tuple[int, List[str]]]:
    rows: List[Tuple[int, List[str]]] = []
    for index, line in enumerate(text, start=1):
        if not line.startswith("| change-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append((index, cells))
    return rows


def validate_latest_row(rows: List[Tuple[int, List[str]]]) -> List[str]:
    if not rows:
        return [
            "change-log guard: no rows starting with '| change-' found; add a change entry before merging."
        ]

    line_no, cells = rows[-1]
    errors: List[str] = []

    if len(cells) < 5:
        errors.append(
            f"change-log guard: line {line_no} must contain at least five columns (change id, date, summary, impacted ids, verification)."
        )
        return errors

    change_id, date_str, summary, impacted, verification = cells[:5]

    if not CHANGE_ID_RE.match(change_id):
        errors.append(
            f"change-log guard: line {line_no} has invalid change id '{change_id}'. Expected format 'change-YYYYMMDD-##'."
        )

    if not date_str:
        errors.append(f"change-log guard: line {line_no} missing change date.")

    if not summary or summary.lower() in {"tbd", "todo"}:
        errors.append(f"change-log guard: line {line_no} requires a meaningful summary.")

    impacted_tokens = [token.strip() for token in impacted.split(";") if token.strip()]
    if not impacted_tokens:
        errors.append(f"change-log guard: line {line_no} must list impacted ids.")
    else:
        for token in impacted_tokens:
            if token.upper() == "N/A":
                continue
            if not ID_TOKEN_RE.match(token):
                errors.append(
                    f"change-log guard: line {line_no} contains invalid impacted id '{token}'."
                )

    if not verification or verification.lower() in {"tbd", "todo"}:
        errors.append(f"change-log guard: line {line_no} must record verification evidence.")

    return errors


def main() -> int:
    args = parse_args()
    changed = normalise(args.files or [])
    if not changed:
        return 0

    relevant = [path for path in changed if not should_ignore(path)]
    if not relevant:
        return 0

    change_log_path = args.root / REQUIRED_FILE
    if REQUIRED_FILE not in changed:
        print(
            "change-log guard: detected updates without a matching docs/change-log.md entry",
            file=sys.stderr,
        )
        print(
            "Include an updated row in docs/change-log.md referencing impacted IDs.",
            file=sys.stderr,
        )
        for path in relevant:
            print(f"  - {path}", file=sys.stderr)
        return 1

    if not change_log_path.exists():
        print(
            f"change-log guard: required file {REQUIRED_FILE} not found under {args.root}",
            file=sys.stderr,
        )
        return 1

    rows = extract_change_rows(change_log_path.read_text(encoding="utf-8").splitlines())
    errors = validate_latest_row(rows)
    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
