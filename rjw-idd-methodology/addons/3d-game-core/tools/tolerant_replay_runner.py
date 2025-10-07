"""Tolerant replay runner for RJW-IDD 3D add-in.

Compares predicted simulation snapshots against authoritative data using
profile-defined tolerances. The input file is expected to follow the structure
produced by engine exporters (see ``ci_samples/tolerant_snapshots.json``).
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import typing as t

from config_loader import ConfigError, MergedConfig, load_merged_config

Vector = t.Sequence[float]


def _vector_delta(a: Vector | None, b: Vector | None) -> float:
    if not a or not b:
        return 0.0
    if len(a) != len(b):
        raise ConfigError("Vector lengths differ between authoritative and predicted data")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _scalar_delta(a: float | None, b: float | None) -> float:
    if a is None or b is None:
        return 0.0
    return abs(a - b)


def evaluate_snapshots(config: MergedConfig, args: argparse.Namespace) -> dict:
    tolerances = config.data.get("tolerant_replay", {})
    position_tol = float(tolerances.get("position_m", 0.05)) * args.scale
    orientation_tol = float(tolerances.get("orientation_deg", 2.0)) * args.scale
    velocity_tol = float(tolerances.get("velocity_mps", 0.2)) * args.scale
    angular_velocity_tol = float(tolerances.get("angular_velocity_dps", 5.0)) * args.scale
    animation_tol = float(tolerances.get("animation_normalised_error", 0.1)) * args.scale
    drift_limit = int(tolerances.get("consecutive_drift_limit", 3))

    snapshot_path = pathlib.Path(args.snapshots)
    if not snapshot_path.exists():
        raise ConfigError(f"Snapshot file not found: {snapshot_path}")
    payload = json.loads(snapshot_path.read_text())
    snapshots = payload.get("snapshots", [])

    report_rows: list[str] = []
    header = "tick | dPos | dRot | dVel | dAvel | dAnim | status"
    report_rows.append(header)
    report_rows.append("-" * len(header))

    drift_streak = 0
    highest_streak = 0
    failures: list[int] = []

    for entry in snapshots:
        tick = entry.get("tick")
        auth = entry.get("authoritative", {})
        pred = entry.get("predicted", {})

        d_pos = _vector_delta(auth.get("pos"), pred.get("pos"))
        d_rot = _vector_delta(auth.get("rot"), pred.get("rot"))
        d_vel = _vector_delta(auth.get("vel"), pred.get("vel"))
        d_avel = _vector_delta(auth.get("avel"), pred.get("avel"))
        d_anim = _scalar_delta(auth.get("anim"), pred.get("anim"))

        within = (
            d_pos <= position_tol
            and d_rot <= orientation_tol
            and d_vel <= velocity_tol
            and d_avel <= angular_velocity_tol
            and d_anim <= animation_tol
        )
        if within:
            drift_streak = 0
        else:
            drift_streak += 1
            highest_streak = max(highest_streak, drift_streak)
            failures.append(tick)

        status = "OK" if within else f"DRIFT x{drift_streak}"
        report_rows.append(
            f"{tick!s:>4} | {d_pos:>4.2f} | {d_rot:>4.2f} | {d_vel:>4.2f} | {d_avel:>5.2f} | {d_anim:>5.2f} | {status}"
        )

    if args.output:
        pathlib.Path(args.output).write_text("\n".join(report_rows) + "\n")
    else:
        print("\n".join(report_rows))

    if highest_streak > drift_limit:
        raise ConfigError(
            f"Replay drift exceeded limit ({highest_streak} consecutive ticks > {drift_limit}); ticks {failures[:10]}"
        )
    return {
        "failures": failures,
        "highest_streak": highest_streak,
        "tolerances": {
            "position_m": position_tol,
            "orientation_deg": orientation_tol,
            "velocity_mps": velocity_tol,
            "angular_velocity_dps": angular_velocity_tol,
            "animation_normalised_error": animation_tol,
            "consecutive_drift_limit": drift_limit,
        },
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RJW-IDD tolerant replay runner")
    parser.add_argument("--snapshots", required=True, help="Path to tolerant replay snapshot JSON")
    parser.add_argument("--profile", help="Override profile name")
    parser.add_argument("--scale", type=float, default=1.0, help="Tolerance scale multiplier (default: 1.0)")
    parser.add_argument("--output", help="Optional path to write diff report")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        config = load_merged_config(profile=args.profile)
        evaluate_snapshots(config, args)
    except ConfigError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
