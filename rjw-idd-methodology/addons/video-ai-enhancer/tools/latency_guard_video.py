#!/usr/bin/env python3
"""Latency guard for the Video AI Enhancer add-in."""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import statistics
import sys
from typing import Iterable

from config_loader import ConfigError, MergedConfig, load_merged_config


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * pct
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    d0 = sorted_vals[f] * (c - k)
    d1 = sorted_vals[c] * (k - f)
    return d0 + d1


def _read_frames(payload: dict) -> list[dict]:
    frames = payload.get("frames", [])
    if not isinstance(frames, list) or not frames:
        raise ConfigError("Latency payload must include a non-empty 'frames' array")
    return frames


def evaluate(config: MergedConfig, trace_path: pathlib.Path, variance: float, output: pathlib.Path | None) -> dict:
    if not trace_path.exists():
        raise ConfigError(f"Latency trace file not found: {trace_path}")
    payload = json.loads(trace_path.read_text())
    frames = _read_frames(payload)

    glass_values: list[float] = []
    pipeline_values: list[float] = []
    encode_values: list[float] = []
    queue_depths: list[float] = []
    for frame in frames:
        if not isinstance(frame, dict):
            raise ConfigError("Each frame entry must be an object")
        glass_values.append(float(frame.get("glass_to_glass_ms", 0)))
        pipeline_values.append(float(frame.get("pipeline_ms", 0)))
        encode_values.append(float(frame.get("encode_ms", 0)))
        queue_depths.append(float(frame.get("queue_depth", 0)))

    budgets = config.data.get("latency_budgets", {})
    glass_budget = float(budgets.get("glass_to_glass_ms", 0))
    pipeline_budget = float(budgets.get("pipeline_budget_ms", 0))
    encode_budget = float(budgets.get("encode_buffer_ms", 0))
    queue_budget = float(budgets.get("queue_depth_frames", 0))

    variance_factor = 1 + variance

    checks: list[tuple[str, float, float, str]] = [
        ("Glass-to-glass p95", _percentile(glass_values, 0.95), glass_budget * variance_factor, "<="),
        ("Glass-to-glass max", max(glass_values), glass_budget * variance_factor, "<="),
        ("Pipeline mean", statistics.fmean(pipeline_values), pipeline_budget * variance_factor, "<="),
        ("Pipeline max", max(pipeline_values), pipeline_budget * variance_factor, "<="),
        ("Encode mean", statistics.fmean(encode_values), encode_budget * variance_factor, "<="),
        ("Encode max", max(encode_values), encode_budget * variance_factor, "<="),
        ("Queue depth max", max(queue_depths), queue_budget * variance_factor, "<="),
    ]

    report_lines = [
        f"Video AI Enhancer Latency Guard — profile={config.profile}",
        "Metric | Actual | Threshold | Status",
        "------ | ------ | --------- | ------",
    ]
    failures: list[str] = []

    for label, actual, threshold, comparator in checks:
        ok = actual <= threshold if comparator == "<=" else actual >= threshold
        status = "OK" if ok else "FAIL"
        report_lines.append(f"{label} | {actual:.2f} | {threshold:.2f} | {status}")
        if not ok:
            failures.append(f"{label} out of bounds ({actual:.2f} {comparator} {threshold:.2f})")

    report = "\n".join(report_lines) + "\n"
    if output:
        output.write_text(report)
    else:
        print(report)

    if failures:
        raise ConfigError("; ".join(failures))
    return {
        "checked": len(checks),
        "failures": failures,
        "variance": variance,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RJW-IDD Video AI latency guard")
    parser.add_argument("--trace", required=True, help="Path to latency trace JSON file")
    parser.add_argument("--profile", help="Override profile name")
    parser.add_argument("--variance", type=float, default=0.0, help="Allowed fractional overage")
    parser.add_argument("--output", help="Optional report output path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        config = load_merged_config(profile=args.profile)
        output_path = pathlib.Path(args.output) if args.output else None
        trace_path = pathlib.Path(args.trace)
        evaluate(config, trace_path, args.variance, output_path)
    except ConfigError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
