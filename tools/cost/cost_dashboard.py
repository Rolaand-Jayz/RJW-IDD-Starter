"""Aggregate AI tooling costs and flag budget anomalies."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--usage-csv", type=Path, required=True, help="CSV of per-feature usage spend.")
    parser.add_argument("--invoice-csv", type=Path, required=True, help="CSV of vendor invoices.")
    parser.add_argument("--monthly-ceiling", type=float, required=True, help="Monthly cost ceiling in USD.")
    parser.add_argument("--alert-threshold", type=float, default=0.8, help="Fraction of ceiling that triggers alerts (default: 0.8).")
    return parser.parse_args()


def load_total(path: Path, value_field: str) -> float:
    total = 0.0
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                total += float(row[value_field])
            except (KeyError, ValueError) as exc:
                raise ValueError(f"{path}: invalid row {row}") from exc
    return total


def main() -> int:
    args = parse_args()

    try:
        usage_total = load_total(args.usage_csv, "cost_usd")
        invoice_total = load_total(args.invoice_csv, "amount_usd")
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    ceiling = args.monthly_ceiling
    alert_boundary = ceiling * args.alert_threshold
    variance = abs(usage_total - invoice_total)
    reconciled = invoice_total if invoice_total else usage_total
    variance_ratio = variance / reconciled if reconciled else 0.0

    status = "ok"
    alerts = []

    if invoice_total >= alert_boundary or usage_total >= alert_boundary:
        status = "alert"
        alerts.append("spend approaching ceiling")

    if variance_ratio > 0.05:
        status = "alert"
        alerts.append("usage/invoice variance exceeds 5%")

    report = {
        "usage_total_usd": round(usage_total, 2),
        "invoice_total_usd": round(invoice_total, 2),
        "ceiling_usd": round(ceiling, 2),
        "variance_ratio": round(variance_ratio, 4),
        "status": status,
        "alerts": alerts,
    }
    print(json.dumps(report, indent=2))

    return 0 if status == "ok" else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
