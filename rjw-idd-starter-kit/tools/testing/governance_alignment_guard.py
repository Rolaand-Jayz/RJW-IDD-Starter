#!/usr/bin/env python3
"""Verify governed artefacts move together (specs, ledgers, decisions, evidence)."""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Set

IGNORED_PREFIXES = ("workspace/", "sandbox/", "tmp/")
SPEC_PREFIX = "specs/"
LEDGER_PREFIX = "artifacts/ledgers/"
DECISION_PREFIX = "docs/decisions/DEC-"
EVIDENCE_PREFIX = "research/"
LEDGER_PATH = Path("artifacts/ledgers/requirement-ledger.csv")
DECISIONS_DIR = Path("docs/decisions")
SPEC_ID_RE = re.compile(r"(SPEC-\d{4})", re.IGNORECASE)
DEC_ID_RE = re.compile(r"(DEC-\d{4})", re.IGNORECASE)
DEC_PLACEHOLDER = "DEC-XXXX"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="Changed file paths relative to repository root (as reported by git diff).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (currently unused but kept for symmetry with other guards).",
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


def filter_relevant(paths: Iterable[str]) -> List[str]:
    relevant: List[str] = []
    for path in paths:
        if any(path.startswith(prefix) for prefix in IGNORED_PREFIXES):
            continue
        relevant.append(path)
    return relevant


def touched_spec_ids(paths: Iterable[str]) -> Dict[str, List[str]]:
    mapping: Dict[str, List[str]] = {}
    for path in paths:
        if not path.startswith(SPEC_PREFIX):
            continue
        name = Path(path).name
        match = SPEC_ID_RE.search(name)
        if not match:
            continue
        spec_id = match.group(1).upper()
        mapping.setdefault(spec_id, []).append(path)
    return mapping


def extract_ledger_spec_ids(path: Path) -> tuple[Set[str], List[str]]:
    spec_ids: Set[str] = set()
    placeholders: List[str] = []
    if not path.exists():
        return spec_ids, placeholders

    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row_num, row in enumerate(reader, start=2):
            raw_refs = row.get("spec_refs", "")
            for token in (piece.strip() for piece in raw_refs.split(";") if piece.strip()):
                normalised = token.upper()
                if normalised == "SPEC-XXXX":
                    placeholders.append(f"row {row_num}")
                    continue
                spec_ids.add(normalised)
    return spec_ids, placeholders


def touched_decision_ids(paths: Iterable[str]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for path in paths:
        if not path.startswith(str(DECISIONS_DIR)):
            continue
        stem = Path(path).stem
        match = DEC_ID_RE.search(stem)
        if not match:
            continue
        mapping[path] = match.group(1).upper()
    return mapping


def extract_decision_tokens(path: Path) -> tuple[Set[str], bool]:
    text = path.read_text(encoding="utf-8")
    tokens = {token.upper() for token in DEC_ID_RE.findall(text)}
    has_placeholder = DEC_PLACEHOLDER in text.upper()
    return tokens, has_placeholder


def main() -> int:
    args = parse_args()
    changed = filter_relevant(normalise(args.files or []))
    if not changed:
        return 0

    spec_changed = any(path.startswith(SPEC_PREFIX) for path in changed)
    ledger_changed = any(path.startswith(LEDGER_PREFIX) for path in changed)
    decision_changed = any(path.startswith(DECISION_PREFIX) for path in changed)
    evidence_changed = any(path.startswith(EVIDENCE_PREFIX) for path in changed)

    errors: List[str] = []

    if spec_changed and not ledger_changed:
        errors.append(
            "governance guard: specification updates detected without matching ledger updates in artifacts/ledgers/."
        )

    if (spec_changed or evidence_changed) and not decision_changed:
        errors.append(
            "governance guard: specification/evidence changes require a new docs/decisions/DEC-#### entry capturing the rationale."
        )

    spec_updates = touched_spec_ids(changed)
    if spec_updates:
        ledger_path = args.root / LEDGER_PATH
        ledger_spec_ids, placeholders = extract_ledger_spec_ids(ledger_path)
        if placeholders:
            errors.append(
                "governance guard: replace SPEC-XXXX placeholders in artifacts/ledgers/requirement-ledger.csv ("
                + ", ".join(placeholders)
                + ")."
            )
        missing_specs = [
            spec_id
            for spec_id in sorted(spec_updates.keys())
            if spec_id not in ledger_spec_ids
        ]
        if missing_specs:
            details = ", ".join(
                f"{spec_id} ({', '.join(sorted(spec_updates[spec_id]))})" for spec_id in missing_specs
            )
            errors.append(
                "governance guard: ledger spec_refs missing updated IDs: " + details
            )

    decision_updates = touched_decision_ids(changed)
    for rel_path, dec_id in decision_updates.items():
        file_path = args.root / rel_path
        if not file_path.exists():
            continue
        tokens, has_placeholder = extract_decision_tokens(file_path)
        if has_placeholder:
            errors.append(
                f"governance guard: {rel_path} still contains placeholder DEC-XXXX; update it to {dec_id}."
            )
        if not tokens:
            errors.append(
                f"governance guard: {rel_path} must reference its DEC id ({dec_id}) within the document body."
            )
            continue
        if dec_id not in tokens:
            errors.append(
                f"governance guard: {rel_path} references {', '.join(sorted(tokens))} but not its own id {dec_id}."
            )

    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
