#!/usr/bin/env python3
"""Verification harness for the RJW-IDD 3D Game Core add-in."""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "addons" / "3d-game-core" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from config_loader import ConfigError, load_yaml  # type: ignore  # noqa: E402

FEATURES_PATH = ROOT / "method/config/features.yml"
CI_INCLUDES_PATH = ROOT / "ci/includes.yml"
README_PATH = ROOT / "README.md"
ADDIN_LINK = "- [3D Game Core](addons/3d-game-core/README.md) — opt-in 3D harnesses, specs, and gates."


class VerificationError(RuntimeError):
    pass


def _load_features() -> dict:
    if not FEATURES_PATH.exists():
        raise VerificationError("feature registry missing; run enable script once")
    return load_yaml(FEATURES_PATH) or {}


def _ensure_ci_alignment(enabled: bool) -> None:
    if not CI_INCLUDES_PATH.exists():
        if enabled:
            raise VerificationError("ci/includes.yml missing while add-in enabled")
        return
    data = load_yaml(CI_INCLUDES_PATH) or {}
    includes: dict = data.get("includes", {})
    gha_entry = "addons/3d-game-core/ci/snippets/github-actions_3d.yml"
    generic_entry = "addons/3d-game-core/ci/snippets/generic-ci_3d.yml"
    gha = includes.get("github_actions", []) if isinstance(includes, dict) else []
    gen = includes.get("generic", []) if isinstance(includes, dict) else []
    if enabled:
        if gha_entry not in gha:
            raise VerificationError("GitHub Actions snippet not registered in ci/includes.yml")
        if generic_entry not in gen:
            raise VerificationError("Generic CI snippet not registered in ci/includes.yml")
    else:
        if gha_entry in gha or generic_entry in gen:
            raise VerificationError("CI snippets should not be registered when add-in disabled")


def _ensure_readme_alignment(enabled: bool) -> None:
    if not README_PATH.exists():
        raise VerificationError("repository README missing")
    lines = README_PATH.read_text().splitlines()
    header = "## Add-ins"
    present = False
    if header in lines:
        idx = lines.index(header)
        section_end = idx + 1
        while section_end < len(lines) and not lines[section_end].startswith("## "):
            section_end += 1
        section = lines[idx + 1:section_end]
        present = ADDIN_LINK in section
    if enabled and not present:
        raise VerificationError("README missing 3D Game Core link while enabled")
    if not enabled and present:
        raise VerificationError("README still references 3D Game Core while disabled")


def _copy_sample(name: str, tmp_dir: pathlib.Path) -> pathlib.Path:
    src = ROOT / name
    dst = tmp_dir / pathlib.Path(name).name
    dst.write_text(src.read_text())
    return dst


def _run(cmd: list[str], expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if expect_success and result.returncode != 0:
        raise VerificationError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    if not expect_success and result.returncode == 0:
        raise VerificationError(f"Command unexpectedly succeeded: {' '.join(cmd)}")
    return result


def _check_idempotency(enabled: bool, profile: str) -> None:
    features_before = FEATURES_PATH.read_text() if FEATURES_PATH.exists() else ""
    ci_before = CI_INCLUDES_PATH.read_text() if CI_INCLUDES_PATH.exists() else ""
    readme_before = README_PATH.read_text() if README_PATH.exists() else ""
    script = "scripts/addons/enable_3d_game_core.py" if enabled else "scripts/addons/disable_3d_game_core.py"
    _run([sys.executable, script])
    if FEATURES_PATH.read_text() != features_before:
        raise VerificationError("Running toggle script modified features.yml unexpectedly")
    if (CI_INCLUDES_PATH.read_text() if CI_INCLUDES_PATH.exists() else "") != ci_before:
        raise VerificationError("Running toggle script modified ci/includes.yml unexpectedly")
    if README_PATH.read_text() != readme_before:
        raise VerificationError("Running toggle script modified README unexpectedly")
    # restore profile to ensure explicit profile remains intact
    _run([sys.executable, "scripts/addons/set_3d_profile.py", "--profile", profile])


def _run_full_suite(profile: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = pathlib.Path(tmp)
        tape = _copy_sample("ci_samples/determinism_tape.json", tmp_dir)
        state_dump = tmp_dir / "states.json"
        hash_out = tmp_dir / "hash.json"
        _run(
            [
                sys.executable,
                "addons/3d-game-core/tools/determinism_harness.py",
                "--ticks",
                "120",
                "--seed",
                "42",
                "--tape",
                str(tape),
                "--state-dump",
                str(state_dump),
                "--hash-out",
                str(hash_out),
                "--profile",
                profile,
            ]
        )
        snapshots = _copy_sample("ci_samples/tolerant_snapshots.json", tmp_dir)
        _run(
            [
                sys.executable,
                "addons/3d-game-core/tools/tolerant_replay_runner.py",
                "--snapshots",
                str(snapshots),
                "--profile",
                profile,
            ]
        )
        tape_rb = _copy_sample("ci_samples/rollback_tape.json", tmp_dir)
        _run(
            [
                sys.executable,
                "addons/3d-game-core/tools/rollback_sim_harness.py",
                "--tape",
                str(tape_rb),
                "--profile",
                profile,
            ]
        )
    _run(
        [
            sys.executable,
            "addons/3d-game-core/tools/asset_linter_3d.py",
            "--manifest",
            "ci_samples/assets_manifest.json",
            "--profile",
            profile,
        ]
    )
    _run(
        [
            sys.executable,
            "addons/3d-game-core/tools/asset_linter_3d.py",
            "--manifest",
            "ci_samples/assets_manifest_violation.json",
            "--profile",
            profile,
        ],
        expect_success=False,
    )
    _run(
        [
            sys.executable,
            "addons/3d-game-core/tools/perf_budget_gate_3d.py",
            "--metrics",
            "addons/3d-game-core/docs/samples/perf_metrics_generic.json",
            "--profile",
            profile,
        ]
    )
    _run(
        [
            sys.executable,
            "addons/3d-game-core/tools/perf_budget_gate_3d.py",
            "--metrics",
            "ci_samples/perf_metrics_violation.json",
            "--profile",
            profile,
        ],
        expect_success=False,
    )
    _run([sys.executable, "-m", "compileall", "addons/3d-game-core/tools"], expect_success=True)


def run_verification(mode: str) -> None:
    data = _load_features()
    try:
        entry = data["addons"]["3d_game_core"]  # type: ignore[index]
    except (KeyError, TypeError) as exc:
        raise VerificationError("features.yml missing 3d_game_core entry") from exc
    enabled = bool(entry.get("enabled", False))
    profile = str(entry.get("profile", "generic"))

    _ensure_ci_alignment(enabled)
    _ensure_readme_alignment(enabled)
    _check_idempotency(enabled, profile)

    if mode == "full" and enabled:
        _run_full_suite(profile)
    elif mode == "full" and not enabled:
        print("Add-in disabled; skipping harness execution.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the 3D Game Core add-in")
    parser.add_argument("--mode", choices=["full", "smoke"], default="full", help="Verification depth")
    args = parser.parse_args()
    try:
        run_verification(args.mode)
    except (VerificationError, ConfigError) as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
