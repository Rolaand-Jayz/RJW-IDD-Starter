"""Performance budget gate for RJW-IDD 3D add-in."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import typing as t

from config_loader import ConfigError, MergedConfig, load_merged_config


def _get_metrics_value(metrics: dict, path: str) -> float:
    cursor: t.Any = metrics
    for part in path.split('.'):
        if not isinstance(cursor, dict) or part not in cursor:
            raise ConfigError(f"Metric path '{path}' missing in metrics payload")
        cursor = cursor[part]
    try:
        return float(cursor)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"Metric '{path}' must be numeric") from exc


def evaluate_metrics(config: MergedConfig, args: argparse.Namespace) -> dict:
    metrics_path = pathlib.Path(args.metrics)
    if not metrics_path.exists():
        raise ConfigError(f"Metrics file not found: {metrics_path}")
    metrics = json.loads(metrics_path.read_text())

    budgets = config.data.get("performance_budgets", {})
    checks = [
        ("frame.cpu_ms", budgets.get("frame", {}).get("cpu_ms"), "frame.cpu_ms"),
        ("frame.gpu_ms", budgets.get("frame", {}).get("gpu_ms"), "frame.gpu_ms"),
        ("scene.draw_calls", budgets.get("scene", {}).get("draw_calls"), "subsystems.render.draw_calls"),
        ("scene.materials", budgets.get("scene", {}).get("materials"), "subsystems.render.material_switches"),
        ("scene.lights", budgets.get("scene", {}).get("lights"), "subsystems.render.lights"),
        ("memory.system_ram_mb", budgets.get("memory", {}).get("system_ram_mb"), "memory.system_ram_mb"),
        ("memory.vram_mb", budgets.get("memory", {}).get("vram_mb"), "memory.vram_mb"),
        ("memory.texture_pool_mb", budgets.get("memory", {}).get("texture_pool_mb"), "memory.texture_pool_mb"),
    ]

    variance = args.variance
    failures: list[str] = []
    report_lines = ["Metric | Value | Budget | Status", "------ | ----- | ------ | ------"]

    for label, budget_value, metric_path in checks:
        if budget_value is None:
            continue
        actual = _get_metrics_value(metrics, metric_path)
        threshold = float(budget_value) * (1 + variance)
        ok = actual <= threshold
        status = "OK" if ok else "FAIL"
        report_lines.append(f"{label} | {actual:.2f} | {budget_value:.2f} | {status}")
        if not ok:
            failures.append(f"{label} ({actual:.2f} > {budget_value:.2f} * (1 + {variance:.2f}))")

    if args.output:
        pathlib.Path(args.output).write_text("\n".join(report_lines) + "\n")
    else:
        print("\n".join(report_lines))

    if failures:
        raise ConfigError("; ".join(failures))
    return {
        "checked": len(report_lines) - 2,
        "failures": failures,
        "variance": variance,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RJW-IDD performance budget gate")
    parser.add_argument("--metrics", required=True, help="Path to metrics JSON file")
    parser.add_argument("--profile", help="Override profile name")
    parser.add_argument("--variance", type=float, default=0.0, help="Allowed fractional overage (e.g. 0.05 for 5%)")
    parser.add_argument("--output", help="Optional path for textual report")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        config = load_merged_config(profile=args.profile)
        evaluate_metrics(config, args)
    except ConfigError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
