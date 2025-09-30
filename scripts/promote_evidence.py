#!/usr/bin/env python3
"""Create curated RJW-IDD evidence index from a raw harvest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set


def load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_allowlist(path: Path) -> Set[str]:
    entries: Set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            clean = line.strip()
            if not clean or clean.startswith("#"):
                continue
            entries.add(clean.split()[0])
    return entries


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Promote curated evidence records from a raw index")
    parser.add_argument("--raw", required=True, help="Path to evidence_index_raw.json")
    parser.add_argument("--allowlist", required=True, help="Path to allowlist file containing EVD IDs")
    parser.add_argument("--output", required=True, help="Destination curated JSON path")
    args = parser.parse_args(argv)

    raw_path = Path(args.raw)
    allow_path = Path(args.allowlist)
    out_path = Path(args.output)

    payload = load_json(raw_path)
    raw_records = payload.get("records", [])
    if not isinstance(raw_records, list):
        raise SystemExit("Raw evidence file missing 'records' array")

    allow_ids = load_allowlist(allow_path)
    if not allow_ids:
        raise SystemExit("Allowlist is empty; nothing to promote")

    lookup: Dict[str, Dict] = {record.get("evid_id"): record for record in raw_records if isinstance(record, dict)}
    missing = sorted(allow_ids - lookup.keys())
    if missing:
        raise SystemExit(f"Allowlist contains unknown EVD IDs: {', '.join(missing)}")

    curated_records = [lookup[evid_id] for evid_id in sorted(allow_ids)]
    curated_payload = {
        "generated_at": payload.get("generated_at"),
        "recency_cutoff": payload.get("recency_cutoff"),
        "total_records": len(curated_records),
        "records": curated_records,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(curated_payload, handle, indent=2, ensure_ascii=False)

    print(f"Promoted {len(curated_records)} records to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
