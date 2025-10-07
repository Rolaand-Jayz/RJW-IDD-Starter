#!/usr/bin/env python3
"""Quality and artifact budget gate for the Video AI Enhancer add-in."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Literal

from config_loader import ConfigError, MergedConfig, load_merged_config

Comparator = Literal["min", "max"]


def _get_metric(metrics: dict, path: str) -> float:
    cursor: object = metrics
    for part in path.split('.'):
        if not isinstance(cursor, dict) or part not in cursor:
            raise ConfigError(f"Metric path '{path}' missing in input payload")
        cursor = cursor[part]
    try:
        return float(cursor)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        raise ConfigError(f"Metric '{path}' must be numeric") from exc


def _threshold(baseline: float, variance: float, comparator: Comparator) -> float:
    if comparator == "min":
        return baseline * (1 - variance)
    return baseline * (1 + variance)


def evaluate(config: MergedConfig, metrics_path: pathlib.Path, variance: float, output: pathlib.Path | None) -> dict:
    if not metrics_path.exists():
        raise ConfigError(f"Metrics file not found: {metrics_path}")
    metrics = json.loads(metrics_path.read_text())

    targets = config.data.get("quality_targets", {})
    metrics_cfg = targets.get("metrics", {})
    frame_cfg = targets.get("frame_consistency", {})
    artifact_cfg = targets.get("artifact_budget", {})

    checks = [
        ("VMAF", _get_metric(metrics, "metrics.vmaf"), float(metrics_cfg.get("vmaf", 0)), "min", "metrics.vmaf"),
        ("PSNR", _get_metric(metrics, "metrics.psnr"), float(metrics_cfg.get("psnr", 0)), "min", "metrics.psnr"),
        ("SSIM", _get_metric(metrics, "metrics.ssim"), float(metrics_cfg.get("ssim", 0)), "min", "metrics.ssim"),
        ("LPIPS", _get_metric(metrics, "metrics.lpips"), float(metrics_cfg.get("lpips", 1)), "max", "metrics.lpips"),
        ("Frame Jitter", _get_metric(metrics, "frame_consistency.jitter_ratio"), float(frame_cfg.get("jitter_ratio", 1)), "max", "frame_consistency.jitter_ratio"),
        ("Frame Drops", _get_metric(metrics, "frame_consistency.frame_drop_pct"), float(frame_cfg.get("frame_drop_pct", 100)), "max", "frame_consistency.frame_drop_pct"),
        ("Cadence FPS", _get_metric(metrics, "frame_consistency.actual_fps"), float(frame_cfg.get("cadence_min_fps", 0)), "min", "frame_consistency.actual_fps"),
        ("Hallucination %", _get_metric(metrics, "artifact_budget.hallucination_pct"), float(artifact_cfg.get("hallucination_pct", 100)), "max", "artifact_budget.hallucination_pct"),
        ("Colour Shift", _get_metric(metrics, "artifact_budget.color_shift_delta_e"), float(artifact_cfg.get("color_shift_delta_e", 100)), "max", "artifact_budget.color_shift_delta_e"),
    ]

    report_lines = [
        f"Video AI Enhancer Quality Gate — profile={config.profile}",
        "Metric | Actual | Target | Comparator | Status",
        "------ | ------ | ------ | ---------- | ------",
    ]
    failures: list[str] = []

    for label, actual, target, comparator, path in checks:
        if comparator == "min":
            threshold = _threshold(target, variance, comparator)
            ok = actual >= threshold
            detail = f">= {threshold:.2f}"
        else:
            threshold = _threshold(target, variance, comparator)
            ok = actual <= threshold
            detail = f"<= {threshold:.2f}"
        status = "OK" if ok else "FAIL"
        report_lines.append(f"{label} | {actual:.2f} | {target:.2f} | {detail} | {status}")
        if not ok:
            failures.append(f"{label} metric ({path}) out of bounds: {actual:.2f} vs {detail}")

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
    parser = argparse.ArgumentParser(description="RJW-IDD Video AI quality gate")
    parser.add_argument("--metrics", required=True, help="Path to metrics JSON file")
    parser.add_argument("--profile", help="Override profile name")
    parser.add_argument("--variance", type=float, default=0.0, help="Allowed fractional deviation (e.g. 0.05 for 5%)")
    parser.add_argument("--output", help="Optional report output path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        config = load_merged_config(profile=args.profile)
        output_path = pathlib.Path(args.output) if args.output else None
        metrics_path = pathlib.Path(args.metrics)
        evaluate(config, metrics_path, args.variance, output_path)
    except ConfigError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
