#!/usr/bin/env python3
"""Validate RJW-IDD evidence index files."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

EVID_RE = re.compile(r"^EVD-\d{4}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def count_words(text: str) -> int:
    return len(text.strip().split())


def validate_record(record: dict, *, cutoff_days: int, now: dt.datetime, warnings: list[str]) -> list[str]:
    errors: list[str] = []
    evid_id = record.get("evid_id")
    if not isinstance(evid_id, str) or not EVID_RE.match(evid_id):
        errors.append(f"invalid evid_id: {evid_id!r}")
    uri = record.get("uri")
    if not isinstance(uri, str) or not uri.strip():
        errors.append(f"{evid_id}: missing uri")
    author = record.get("author_or_handle")
    if not isinstance(author, str) or not author.strip():
        warnings.append(f"{evid_id}: missing or blank author handle")
    platform = record.get("platform")
    if platform not in {"hn", "reddit", "github", "so", "official"}:
        errors.append(f"{evid_id}: unsupported platform {platform!r}")
    date_str = record.get("date")
    if not isinstance(date_str, str) or not DATE_RE.match(date_str):
        errors.append(f"{evid_id}: invalid date {date_str!r}")
    else:
        year, month, day = map(int, date_str.split("-"))
        try:
            recorded = dt.datetime(year, month, day)
        except ValueError as exc:  # pragma: no cover
            errors.append(f"{evid_id}: invalid date value {exc}")
        else:
            delta = now.date() - recorded.date()
            if delta.days < 0:
                warnings.append(f"{evid_id}: future date {date_str}")
            if delta.days > cutoff_days:
                errors.append(f"{evid_id}: older than {cutoff_days} days ({delta.days}d)")
    quote = record.get("minimal_quote", "")
    if not isinstance(quote, str) or not quote.strip():
        errors.append(f"{evid_id}: empty minimal_quote")
    if count_words(quote) > 50:
        errors.append(f"{evid_id}: minimal_quote exceeds 50 words")
    tags = record.get("tags")
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        errors.append(f"{evid_id}: tags must be list[str]")
    stance = record.get("stance")
    if stance not in {"pain", "fix", "aha", "win", "risk", "contra"}:
        errors.append(f"{evid_id}: invalid stance {stance!r}")
    quality_flags = record.get("quality_flags", [])
    if not isinstance(quality_flags, list) or not all(isinstance(flag, str) for flag in quality_flags):
        errors.append(f"{evid_id}: quality_flags must be list[str]")
    return errors


def validate_curated(curated: dict, raw: dict, errors: list[str]) -> None:
    raw_ids = {rec["evid_id"] for rec in raw.get("records", [])}
    for rec in curated.get("records", []):
        evid_id = rec.get("evid_id")
        if evid_id not in raw_ids:
            errors.append(f"curated record {evid_id} missing in raw index")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate RJW-IDD evidence indices")
    parser.add_argument("--input", required=True, help="Path to evidence index (raw or curated)")
    parser.add_argument("--raw", help="Optional path to the raw index when validating curated files")
    parser.add_argument("--cutoff-days", type=int, default=28)
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args(argv)

    payload = load(Path(args.input))
    now = dt.datetime.now(dt.timezone.utc)
    errors: list[str] = []
    warnings: list[str] = []

    records = payload.get("records", [])
    if not isinstance(records, list):
        errors.append("root.records must be a list")
    else:
        for record in records:
            if not isinstance(record, dict):
                errors.append(f"non-object record: {record!r}")
                continue
            errors.extend(validate_record(record, cutoff_days=args.cutoff_days, now=now, warnings=warnings))

    if args.raw:
        validate_curated(payload, load(Path(args.raw)), errors)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        return 1
    if args.fail_on_warning and warnings:
        return 2
    print(f"Validated {len(records)} records in {args.input}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
