#!/usr/bin/env python3
"""Validate RJW-IDD identifier formatting within the 3D add-in."""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Iterable

ALLOWED_PREFIXES = {
    "SPEC",
    "REQ",
    "TEST",
    "DEC",
    "INTEG",
    "PACT",
    "DOC",
    "PROMPT",
    "PROFILE",
    "CONFIG",
    "CI",
}

ID_PATTERN = re.compile(r"\b([A-Z]+-3D(?:-[A-Z0-9]+)?-\d{4})\b")
ADDIN_ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET_PATH = ADDIN_ROOT / "addons" / "3d-game-core"


def iter_files(paths: Iterable[pathlib.Path]) -> Iterable[pathlib.Path]:
    for path in paths:
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    yield child
        elif path.is_file():
            yield path


def validate_files(paths: Iterable[pathlib.Path]) -> list[str]:
    errors: list[str] = []
    for file_path in iter_files(paths):
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for match in ID_PATTERN.finditer(text):
            token = match.group(1)
            prefix = token.split("-3D", 1)[0]
            if prefix not in ALLOWED_PREFIXES:
                errors.append(f"{file_path}: invalid prefix in identifier '{token}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate RJW-IDD IDs within the 3D add-in")
    parser.add_argument(
        "paths",
        nargs="*",
        type=pathlib.Path,
        default=[TARGET_PATH],
        help="Paths to scan (defaults to addons/3d-game-core)",
    )
    args = parser.parse_args()
    errors = validate_files(args.paths)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    print("ID validation passed for 3D add-in.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
