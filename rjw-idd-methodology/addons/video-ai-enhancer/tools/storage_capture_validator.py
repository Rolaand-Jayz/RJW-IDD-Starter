#!/usr/bin/env python3
"""Validate capture/output storage constraints for the Video AI Enhancer add-in."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from config_loader import ConfigError, MergedConfig, load_merged_config

SECONDS_PER_MINUTE = 60
BITS_PER_MEGABIT = 1_000_000
BYTES_PER_MEBIBYTE = 1_048_576


def _load_payload(path: pathlib.Path) -> dict:
    if not path.exists():
        raise ConfigError(f"Storage report not found: {path}")
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ConfigError("Storage payload must be a JSON object")
    return payload


def _validate_segments(segments: list[dict], max_duration: float, max_bitrate: float, variance: float) -> list[str]:
    errors: list[str] = []
    limit_duration = max_duration * (1 + variance)
    limit_bitrate = max_bitrate * (1 + variance)
    for seg in segments:
        if not isinstance(seg, dict):
            errors.append("Segment entry must be an object")
            continue
        name = seg.get("path", "<unnamed>")
        duration = float(seg.get("duration_s", 0))
        bitrate = float(seg.get("average_bitrate_mbps", 0))
        if duration > limit_duration:
            errors.append(f"Segment {name} duration {duration:.2f}s exceeds {limit_duration:.2f}s")
        if bitrate > limit_bitrate:
            errors.append(f"Segment {name} bitrate {bitrate:.2f}Mbps exceeds {limit_bitrate:.2f}Mbps")
    return errors


def evaluate(config: MergedConfig, payload_path: pathlib.Path, variance: float, output: pathlib.Path | None) -> dict:
    payload = _load_payload(payload_path)
    segments = payload.get("segments", [])
    if not isinstance(segments, list) or not segments:
        raise ConfigError("Storage payload must contain a non-empty 'segments' array")

    storage_cfg = config.data.get("storage_pipeline", {})
    max_bitrate = float(storage_cfg.get("max_bitrate_mbps", 0))
    capture_window_min = float(storage_cfg.get("capture_window_minutes", 0))
    retention_hours = float(storage_cfg.get("retention_hours", 0))
    segment_max_seconds = float(storage_cfg.get("segment_max_seconds", 0))
    max_parallel = int(storage_cfg.get("max_parallel_writers", 1))

    errors = _validate_segments(segments, segment_max_seconds, max_bitrate, variance)

    total_duration = float(payload.get("total_duration_s", 0))
    total_storage_mb = float(payload.get("total_storage_mb", 0))
    reported_parallel = int(payload.get("max_parallel_writers", 1))

    capture_window_seconds = capture_window_min * SECONDS_PER_MINUTE
    capture_limit = capture_window_seconds * max_bitrate / 8.0  # Mbps to MB (approx)
    capture_limit *= (1 + variance)

    if total_duration > capture_window_seconds * (1 + variance):
        errors.append(
            f"Total capture duration {total_duration:.2f}s exceeds window {capture_window_seconds:.2f}s"
        )
    if total_storage_mb > capture_limit:
        errors.append(
            f"Total storage footprint {total_storage_mb:.2f}MB exceeds limit {capture_limit:.2f}MB"
        )
    if reported_parallel > max_parallel:
        errors.append(
            f"Parallel writers {reported_parallel} exceeds configured limit {max_parallel}"
        )

    report_lines = [
        f"Video AI Enhancer Storage Validator — profile={config.profile}",
        "Check | Actual | Limit | Status",
        "----- | ------ | ----- | ------",
    ]
    rows = [
        ("Capture duration (s)", total_duration, capture_window_seconds * (1 + variance)),
        ("Total storage (MB)", total_storage_mb, capture_limit),
        ("Parallel writers", reported_parallel, float(max_parallel)),
    ]
    for label, actual, limit in rows:
        ok = actual <= limit
        status = "OK" if ok else "FAIL"
        report_lines.append(f"{label} | {actual:.2f} | {limit:.2f} | {status}")
    report_lines.append(f"Retention expectation (hours): {retention_hours:.1f}")

    report = "\n".join(report_lines) + "\n"
    if output:
        output.write_text(report)
    else:
        print(report)

    if errors:
        raise ConfigError("; ".join(errors))
    return {
        "checked_segments": len(segments),
        "variance": variance,
        "total_duration_s": total_duration,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RJW-IDD Video AI storage validator")
    parser.add_argument("--report", required=True, help="Path to captured storage JSON report")
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
        report_path = pathlib.Path(args.report)
        evaluate(config, report_path, args.variance, output_path)
    except ConfigError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
