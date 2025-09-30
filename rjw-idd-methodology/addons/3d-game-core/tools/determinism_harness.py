"""Determinism harness for RJW-IDD 3D projects.

The harness advances a fixed timestep simulation using a pluggable state
provider. By default it executes a lightweight reference provider that models a
simple particle system; projects can supply their own implementation via the
``--provider`` argument (``module:ClassName``).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import pathlib
import random
import sys
import typing as t

from config_loader import ConfigError, MergedConfig, load_merged_config

State = t.Dict[str, t.Any]


@t.runtime_checkable
class StateProviderProtocol(t.Protocol):
    def reset(self, seed: int) -> None:  # pragma: no cover - protocol definition
        ...

    def step(self, tick: int, dt: float, rng: random.Random) -> State:  # pragma: no cover
        ...


class DefaultStateProvider:
    """Reference implementation used for self-tests and dry runs.

    The provider simulates a small collection of particles under gravity and
    drag. It is intentionally deterministic when seeded with the same RNG and
    timestep.
    """

    def __init__(self) -> None:
        self._particles: list[dict[str, float]] = []

    def reset(self, seed: int) -> None:
        rng = random.Random(seed)
        self._particles = []
        for _ in range(5):
            self._particles.append(
                {
                    "x": rng.uniform(-1.0, 1.0),
                    "y": rng.uniform(2.0, 5.0),
                    "z": rng.uniform(-1.0, 1.0),
                    "vx": rng.uniform(-0.5, 0.5),
                    "vy": rng.uniform(0.5, 1.5),
                    "vz": rng.uniform(-0.5, 0.5),
                }
            )

    def step(self, tick: int, dt: float, rng: random.Random) -> State:
        g = -9.81
        drag = 0.98
        for particle in self._particles:
            particle["vx"] += rng.uniform(-0.01, 0.01)
            particle["vz"] += rng.uniform(-0.01, 0.01)
            particle["vy"] += g * dt
            particle["x"] += particle["vx"] * dt
            particle["y"] = max(0.0, particle["y"] + particle["vy"] * dt)
            particle["z"] += particle["vz"] * dt
            particle["vx"] *= drag
            particle["vy"] *= drag if particle["y"] > 0 else 0.0
            particle["vz"] *= drag
        return {
            "tick": tick,
            "particles": [{k: round(v, 6) for k, v in p.items()} for p in self._particles],
        }


def load_provider(import_path: str | None) -> StateProviderProtocol:
    if not import_path:
        return DefaultStateProvider()
    if ":" not in import_path:
        raise ConfigError("Provider must be specified as 'module:ClassName'")
    module_name, class_name = import_path.split(":", 1)
    module = importlib.import_module(module_name)
    provider_cls = getattr(module, class_name)
    provider = provider_cls()
    if not isinstance(provider, StateProviderProtocol):  # type: ignore[arg-type]
        raise ConfigError(f"Provider {import_path} does not implement the expected protocol")
    return provider  # type: ignore[return-value]


def canonical_hash(state: State) -> str:
    canonical = json.dumps(state, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def run_harness(config: MergedConfig, args: argparse.Namespace) -> dict:
    provider = load_provider(args.provider)
    rng = random.Random(args.seed or config.data.get("randomisation", {}).get("default_seed", 42))
    timestep_hz = config.data.get("randomisation", {}).get("fixed_timestep_hz", 60)
    dt = 1.0 / float(timestep_hz)

    provider.reset(rng.randint(0, 2**31 - 1))
    frames: list[dict[str, t.Any]] = []
    state_dump: list[State] = []

    for tick in range(args.ticks):
        state = provider.step(tick, dt, rng)
        frame_hash = canonical_hash(state)
        frames.append({"tick": tick, "hash": frame_hash})
        if args.state_dump:
            state_dump.append(state)

    tape = {
        "metadata": {
            "profile": config.profile,
            "ticks": args.ticks,
            "seed": args.seed,
            "provider": args.provider or "default",
        },
        "frames": frames,
    }

    if args.tape:
        tape_path = pathlib.Path(args.tape)
        if tape_path.exists():
            existing = json.loads(tape_path.read_text())
            mismatches = []
            for expected, actual in zip(existing.get("frames", []), frames):
                if expected.get("hash") != actual.get("hash"):
                    mismatches.append((actual["tick"], expected.get("hash"), actual.get("hash")))
            if mismatches:
                lines = ["Determinism mismatch detected:"]
                for tick, expected_hash, actual_hash in mismatches[:20]:
                    lines.append(f"  tick {tick}: expected {expected_hash}, got {actual_hash}")
                raise ConfigError("\n".join(lines))
        tape_path.write_text(json.dumps(tape, indent=2))
    if args.state_dump:
        dump_path = pathlib.Path(args.state_dump)
        dump_path.write_text(json.dumps(state_dump, indent=2))
    if args.hash_out:
        aggregate = hashlib.sha256("".join(frame["hash"] for frame in frames).encode("utf-8")).hexdigest()
        pathlib.Path(args.hash_out).write_text(json.dumps({"aggregate_hash": aggregate}, indent=2))
    return tape


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RJW-IDD determinism harness")
    parser.add_argument("--ticks", type=int, default=600, help="Number of ticks to simulate (default: 600)")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed override")
    parser.add_argument("--tape", type=str, help="Path to determinism tape JSON (read+write)")
    parser.add_argument("--state-dump", dest="state_dump", type=str, help="Optional path to dump raw states")
    parser.add_argument("--hash-out", dest="hash_out", type=str, help="Path to write aggregate hash JSON")
    parser.add_argument("--profile", type=str, help="Override profile name from features registry")
    parser.add_argument("--provider", type=str, help="Custom provider specified as module:ClassName")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        config = load_merged_config(profile=args.profile)
        run_harness(config, args)
    except ConfigError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover - argparse.error raises SystemExit
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
