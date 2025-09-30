#!/usr/bin/env python3
"""Schedule-friendly wrapper for cost dashboard generation."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
COST_DASHBOARD = REPO_ROOT / "tools" / "cost" / "cost_dashboard.py"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--usage-csv", type=Path, required=True, help="Usage CSV passed to cost_dashboard.py")
    parser.add_argument("--invoice-csv", type=Path, required=True, help="Invoice CSV passed to cost_dashboard.py")
    parser.add_argument("--monthly-ceiling", type=float, required=True, help="Monthly cost ceiling in USD")
    parser.add_argument(
        "--alert-threshold",
        type=float,
        default=0.8,
        help="Alert threshold forwarded to cost_dashboard.py (default: 0.8)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "logs" / "cost",
        help="Directory where JSON snapshots will be written (default: logs/cost)",
    )
    return parser.parse_args(argv)


def run_dashboard(args: argparse.Namespace) -> Dict[str, Any]:
    command = [
        sys.executable,
        str(COST_DASHBOARD),
        "--usage-csv",
        str(args.usage_csv),
        "--invoice-csv",
        str(args.invoice_csv),
        "--monthly-ceiling",
        str(args.monthly_ceiling),
        "--alert-threshold",
        str(args.alert_threshold),
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    payload: Dict[str, Any]
    if result.stdout.strip():
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            payload = {"status": "error", "raw_stdout": result.stdout}
    else:
        payload = {"status": "error", "raw_stdout": ""}

    payload["returncode"] = result.returncode
    if result.stderr:
        payload["stderr"] = result.stderr.splitlines()

    return payload


def write_snapshot(
    *,
    output_dir: Path,
    payload: Dict[str, Any],
    args: argparse.Namespace,
    timestamp: str,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "generated_at": timestamp,
        "inputs": {
            "usage_csv": str(args.usage_csv),
            "invoice_csv": str(args.invoice_csv),
            "monthly_ceiling": args.monthly_ceiling,
            "alert_threshold": args.alert_threshold,
        },
        "report": payload,
    }
    path = output_dir / f"cost_dashboard_{timestamp}.json"
    path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return path


def main() -> int:
    args = parse_args()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload = run_dashboard(args)
    snapshot_path = write_snapshot(output_dir=args.output_dir, payload=payload, args=args, timestamp=timestamp)
    summary = {
        "snapshot": str(snapshot_path.relative_to(REPO_ROOT)),
        "status": payload.get("status", "unknown"),
        "returncode": payload.get("returncode", 1),
    }
    print(json.dumps(summary, indent=2))
    return int(payload.get("returncode", 1))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
