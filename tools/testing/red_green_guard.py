"""Ensure diffs include test updates alongside code changes."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from pathlib import Path

TEST_INDICATORS = ("tests/", "test_", "_test.py", "Test.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files", nargs="+", help="Changed file paths relative to repository root.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (used for existence checks).",
    )
    return parser.parse_args()


def contains_test_path(paths: Iterable[str]) -> bool:
    for path in paths:
        normalized = path.lower()
        if any(indicator in normalized for indicator in TEST_INDICATORS):
            return True
    return False


def validate_files(root: Path, files: list[str]) -> list[str]:
    errors: list[str] = []
    if not files:
        errors.append("no files provided to red-green guard")
        return errors

    if not contains_test_path(files):
        errors.append("diff lacks test updates; add failing test before implementation")

    for relative in files:
        path = (root / relative).resolve()
        if not path.exists():
            errors.append(f"referenced path does not exist: {relative}")

    return errors


def main() -> int:
    args = parse_args()
    errors = validate_files(args.root.resolve(), args.files)
    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
