#!/usr/bin/env python3
"""Verify the living documentation reconciliation log is free of open items."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, List

TARGET_FILE = Path("docs/living-docs-reconciliation.md")
PLACEHOLDER_TOKEN = "YYYY-MM-DD"
STATUS_TOKEN = "| open |"
DOC_PATH_PREFIXES = ("docs/", "specs/")
DOC_EXEMPTIONS = {"templates-and-examples/templates/change-logs/CHANGELOG-template.md"}
IGNORED_PREFIXES = ("workspace/", "sandbox/", "tmp/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root containing docs/living-docs-reconciliation.md.",
    )
    parser.add_argument(
        "--fail-on-placeholder",
        action="store_true",
        help="Also fail if the template placeholder row is still present.",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="Changed file paths relative to repository root (as reported by git diff).",
    )
    return parser.parse_args()


def normalise(paths: Iterable[str]) -> List[str]:
    normalised: List[str] = []
    for raw in paths:
        if raw is None:
            continue
        path = raw.strip()
        if not path:
            continue
        normalised.append(path.replace("\\", "/"))
    return normalised


def classify_changes(paths: Iterable[str]) -> tuple[list[str], list[str]]:
    doc_updates: list[str] = []
    relevant: list[str] = []
    for path in paths:
        if any(path.startswith(prefix) for prefix in IGNORED_PREFIXES):
            continue
        relevant.append(path)
        if any(path.startswith(prefix) for prefix in DOC_PATH_PREFIXES) and path not in DOC_EXEMPTIONS:
            doc_updates.append(path)
    non_doc = [path for path in relevant if path not in doc_updates and path not in DOC_EXEMPTIONS]
    return doc_updates, non_doc


def main() -> int:
    args = parse_args()
    target = args.root / TARGET_FILE
    if not target.exists():
        print(
            f"living-doc guard: expected {TARGET_FILE} under {args.root}, but it was not found",
            file=sys.stderr,
        )
        return 1

    changed = normalise(args.files or [])
    doc_updates, non_doc_changes = classify_changes(changed)

    open_rows: list[str] = []
    placeholder_present = False

    with target.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or not stripped.startswith("|"):
                continue
            if PLACEHOLDER_TOKEN in stripped:
                placeholder_present = True
                if args.fail_on_placeholder and STATUS_TOKEN in stripped:
                    open_rows.append(stripped)
                continue
            if STATUS_TOKEN in stripped:
                open_rows.append(stripped)

    if open_rows:
        print(
            "living-doc guard: outstanding documentation gaps detected. Close or remove them before merging.",
            file=sys.stderr,
        )
        for row in open_rows:
            print(f"  - {row}", file=sys.stderr)
        return 1

    if args.fail_on_placeholder and placeholder_present:
        print(
            "living-doc guard: remove the placeholder row from docs/living-docs-reconciliation.md",
            file=sys.stderr,
        )
        return 1

    if non_doc_changes and not doc_updates:
        print(
            "living-doc guard: detected implementation/spec/research updates without accompanying documentation changes.",
            file=sys.stderr,
        )
        for path in non_doc_changes:
            print(f"  - {path}", file=sys.stderr)
        print(
            "Update a doc/spec/runbook (or log the gap in the reconciliation table) as part of this change.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
