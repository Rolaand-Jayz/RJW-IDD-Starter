"""Rollback simulation harness for RJW-IDD 3D add-in."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from config_loader import ConfigError, MergedConfig, load_merged_config


def evaluate_tape(config: MergedConfig, args: argparse.Namespace) -> dict:
    thresholds = config.data.get("rollback", {})
    max_prediction_ticks = int(thresholds.get("max_prediction_ticks", 8))
    misprediction_threshold = float(thresholds.get("misprediction_rate_threshold", 0.05))
    rollback_depth_threshold = int(thresholds.get("rollback_depth_threshold", 4))

    tape_path = pathlib.Path(args.tape)
    if not tape_path.exists():
        raise ConfigError(f"Rollback tape not found: {tape_path}")
    payload = json.loads(tape_path.read_text())
    frames = payload.get("frames", [])
    if not frames:
        raise ConfigError("Rollback tape is empty")

    mismatches = 0
    max_depth = 0
    exceeding_prediction_window = False

    for frame in frames:
        pred = frame.get("predicted", {})
        auth = frame.get("authoritative", {})
        depth = int(frame.get("rollback_depth", 0))
        max_depth = max(max_depth, depth)
        if depth > max_prediction_ticks:
            exceeding_prediction_window = True
        if pred.get("state_hash") != auth.get("state_hash"):
            mismatches += 1

    misprediction_rate = mismatches / len(frames)
    status_lines = [
        f"Frames analysed: {len(frames)}",
        f"Mispredictions: {mismatches} ({misprediction_rate:.3f})",
        f"Max rollback depth: {max_depth}",
        f"Exceeded prediction window: {'yes' if exceeding_prediction_window else 'no'}",
    ]

    if args.output:
        pathlib.Path(args.output).write_text("\n".join(status_lines) + "\n")
    else:
        print("\n".join(status_lines))

    if misprediction_rate > misprediction_threshold:
        raise ConfigError(
            f"Misprediction rate {misprediction_rate:.3f} exceeds threshold {misprediction_threshold:.3f}"
        )
    if max_depth > rollback_depth_threshold:
        raise ConfigError(
            f"Rollback depth {max_depth} exceeds threshold {rollback_depth_threshold}"
        )
    if exceeding_prediction_window:
        raise ConfigError(
            f"Prediction window exceeded (>{max_prediction_ticks} ticks)"
        )
    return {
        "frames": len(frames),
        "misprediction_rate": misprediction_rate,
        "max_depth": max_depth,
        "thresholds": thresholds,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RJW-IDD rollback simulation harness")
    parser.add_argument("--tape", required=True, help="Path to rollback tape JSON")
    parser.add_argument("--profile", help="Override profile name")
    parser.add_argument("--output", help="Optional path for textual summary")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        config = load_merged_config(profile=args.profile)
        evaluate_tape(config, args)
    except ConfigError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
