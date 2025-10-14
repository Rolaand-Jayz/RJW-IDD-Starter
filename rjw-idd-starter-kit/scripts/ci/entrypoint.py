#!/usr/bin/env python3
"""RJW-IDD CI entrypoint orchestrating quality gates."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _default_log_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "logs" / "ci"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-ref",
        default=os.environ.get("RJW_BASE_REF", "origin/main"),
        help="Git reference used as the baseline for guards (default: origin/main).",
    )
    parser.add_argument(
        "--head-ref",
        default=os.environ.get("RJW_HEAD_REF", "HEAD"),
        help="Git reference representing the candidate changes (default: HEAD).",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=_default_log_dir(),
        help="Directory where CI guard artefacts are written (default: logs/ci).",
    )
    return parser.parse_args()


def run_test_gate(
    *,
    repo_root: Path,
    base_ref: str,
    head_ref: str,
    log_dir: Path,
    timestamp: str,
) -> dict[str, Any]:
    log_dir.mkdir(parents=True, exist_ok=True)
    script_path = repo_root / "scripts" / "ci" / "test_gate.sh"
    env = os.environ.copy()
    env["RJW_BASE_REF"] = base_ref
    env["RJW_HEAD_REF"] = head_ref

    result = subprocess.run(
        ["bash", str(script_path)],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
    )

    log_path = log_dir / f"test_gate_{timestamp}.log"
    with log_path.open("w", encoding="utf-8") as handle:
        handle.write(f"# scripts/ci/test_gate.sh @ {timestamp}\n")
        handle.write(f"# base_ref={base_ref} head_ref={head_ref}\n\n")
        if result.stdout:
            handle.write(result.stdout)
        if result.stderr:
            handle.write("\n# stderr\n")
            handle.write(result.stderr)

    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)

    status = "passed" if result.returncode == 0 else "failed"
    return {
        "step": "test_gate",
        "status": status,
        "returncode": result.returncode,
        "log_path": str(log_path.relative_to(repo_root)),
        "base_ref": base_ref,
        "head_ref": head_ref,
    }


def write_summary(
    *,
    log_dir: Path,
    timestamp: str,
    steps: list[dict[str, Any]],
    repo_root: Path,
) -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "timestamp": timestamp,
        "steps": steps,
    }
    summary_path = log_dir / f"ci_summary_{timestamp}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary_path


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    log_dir = args.log_dir if args.log_dir.is_absolute() else repo_root / args.log_dir
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    steps: list[dict[str, Any]] = []
    steps.append(
        run_test_gate(
            repo_root=repo_root,
            base_ref=args.base_ref,
            head_ref=args.head_ref,
            log_dir=log_dir,
            timestamp=timestamp,
        )
    )

    summary_path = write_summary(log_dir=log_dir, timestamp=timestamp, steps=steps, repo_root=repo_root)

    summary_output = {
        "summary": str(summary_path.relative_to(repo_root)),
        "steps": steps,
    }
    print(json.dumps(summary_output, indent=2))

    if any(step["status"] != "passed" for step in steps):
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
