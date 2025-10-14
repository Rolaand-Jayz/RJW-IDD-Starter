"""Sandbox breach drill automation.

Writes JSON artefacts under `logs/security/` capturing the simulated drill,
including optional execution of `scripts/sandbox/reset.sh` when `--run-reset`
(or API equivalent) is used.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_LOG_DIR = Path("logs/security")
_DEFAULT_RESET_SCRIPT = _REPO_ROOT / "scripts" / "sandbox" / "reset.sh"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operator", required=True, help="Operator running the drill (recorded for governance).")
    parser.add_argument("--scenario", default="sandbox-breach-drill", help="Scenario identifier for the drill run.")
    parser.add_argument("--log-dir", type=Path, default=_DEFAULT_LOG_DIR, help="Directory for drill artefacts (default: logs/security).")
    parser.add_argument("--notes", help="Additional human notes captured with the drill artefact.")
    parser.add_argument("--run-reset", action="store_true", help="Execute sandbox reset script as part of the drill.")
    parser.add_argument(
        "--reset-script",
        type=Path,
        default=_DEFAULT_RESET_SCRIPT,
        help="Path to the sandbox reset script (default: scripts/sandbox/reset.sh).",
    )
    parser.add_argument("--sandbox-session-id", help="Session id passed to reset script when --run-reset is set.")
    parser.add_argument("--sandbox-token-dir", help="Token directory passed to reset script when --run-reset is set.")
    parser.add_argument("--sandbox-netns-path", help="Network namespace path passed to reset script when --run-reset is set.")
    return parser.parse_args(argv)


def _build_env(args: argparse.Namespace) -> dict[str, str]:
    env = os.environ.copy()
    if args.sandbox_session_id:
        env["RJW_SANDBOX_SESSION_ID"] = args.sandbox_session_id
    if args.sandbox_token_dir:
        env["RJW_SANDBOX_TOKEN_DIR"] = args.sandbox_token_dir
    if args.sandbox_netns_path:
        env["RJW_SANDBOX_NETNS_PATH"] = args.sandbox_netns_path
    return env


def execute(args: argparse.Namespace) -> dict[str, object]:
    repo_root = _REPO_ROOT
    log_dir = args.log_dir if args.log_dir.is_absolute() else repo_root / args.log_dir
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = log_dir / f"sandbox_drill_{timestamp}.json"

    record: dict[str, object] = {
        "timestamp": timestamp,
        "operator": args.operator,
        "scenario": args.scenario,
        "notes": args.notes or "",
        "status": "recorded",
        "reset": {"executed": False},
    }

    if args.run_reset:
        env = _build_env(args)
        result = subprocess.run(
            [str(args.reset_script)],
            cwd=repo_root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        record["reset"] = {
            "executed": True,
            "script": str(args.reset_script),
            "returncode": result.returncode,
            "stdout": result.stdout.splitlines(),
            "stderr": result.stderr.splitlines(),
        }
        record["status"] = "passed" if result.returncode == 0 else "failed"

    log_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    try:
        artefact = log_path.relative_to(repo_root)
    except ValueError:
        artefact = log_path
    record["artefact"] = str(artefact)
    return record


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    summary = execute(args)
    print(json.dumps(summary, indent=2))
    return 0 if summary.get("status") != "failed" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
