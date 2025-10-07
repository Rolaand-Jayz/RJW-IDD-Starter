#!/usr/bin/env python3
"""Verification harness for the RJW-IDD Video AI Enhancer add-in."""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
from typing import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "addons" / "video-ai-enhancer" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from config_loader import ConfigError  # type: ignore  # noqa: E402
FEATURES_PATH = ROOT / "method/config/features.yml"
CI_INCLUDES_PATH = ROOT / "ci/includes.yml"
README_PATH = ROOT / "README.md"
QUALITY_SAMPLE = ROOT / "addons/video-ai-enhancer/docs/samples/quality_metrics_baseline.json"
LATENCY_SAMPLE = ROOT / "addons/video-ai-enhancer/docs/samples/latency_trace_sample.json"
STORAGE_SAMPLE = ROOT / "addons/video-ai-enhancer/docs/samples/storage_report_sample.json"
ADDIN_LINK = "- [Video AI Enhancer](addons/video-ai-enhancer/README.md) — opt-in real-time video enhancement and capture gates."
GHA_ENTRY = "addons/video-ai-enhancer/ci/snippets/github-actions_video.yml"
GENERIC_ENTRY = "addons/video-ai-enhancer/ci/snippets/generic-ci_video.yml"
FEATURE_KEY = "video_ai_enhancer"


class VerificationError(RuntimeError):
    pass


def _run(cmd: Sequence[str], expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if expect_success and result.returncode != 0:
        raise VerificationError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    if not expect_success and result.returncode == 0:
        raise VerificationError(f"Command expected to fail but passed: {' '.join(cmd)}")
    return result


def _load_features() -> tuple[bool, str]:
    import yaml  # type: ignore

    if not FEATURES_PATH.exists():
        return False, "baseline"
    data = yaml.safe_load(FEATURES_PATH.read_text()) or {}
    try:
        entry = data["addons"][FEATURE_KEY]
    except (KeyError, TypeError):
        raise VerificationError("features.yml missing video_ai_enhancer entry")
    enabled = bool(entry.get("enabled", False))
    profile = str(entry.get("profile", "baseline"))
    return enabled, profile


def _ensure_ci_alignment(enabled: bool) -> None:
    if not CI_INCLUDES_PATH.exists():
        if enabled:
            raise VerificationError("ci/includes.yml missing while add-in enabled")
        return
    import yaml  # type: ignore

    data = yaml.safe_load(CI_INCLUDES_PATH.read_text()) or {}
    includes = data.get("includes", {})
    gha = includes.get("github_actions", []) if isinstance(includes, dict) else []
    generic = includes.get("generic", []) if isinstance(includes, dict) else []
    if enabled:
        if GHA_ENTRY not in gha:
            raise VerificationError("GitHub Actions snippet not registered in ci/includes.yml")
        if GENERIC_ENTRY not in generic:
            raise VerificationError("Generic CI snippet not registered in ci/includes.yml")
    else:
        if GHA_ENTRY in gha or GENERIC_ENTRY in generic:
            raise VerificationError("CI snippets present while add-in disabled")


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
        raise VerificationError("README missing Video AI Enhancer link while enabled")
    if not enabled and present:
        raise VerificationError("README still references Video AI Enhancer while disabled")


def _check_idempotency(profile: str) -> None:
    before = FEATURES_PATH.read_text() if FEATURES_PATH.exists() else ""
    _run([sys.executable, "scripts/addons/set_video_ai_profile.py", "--profile", profile])
    after = FEATURES_PATH.read_text() if FEATURES_PATH.exists() else ""
    if before and before != after:
        raise VerificationError("Profile setter produced changes when reapplying the same profile")


def _run_full_suite(profile: str) -> None:
    _run([
        sys.executable,
        "addons/video-ai-enhancer/tools/quality_gate_video.py",
        "--metrics",
        str(QUALITY_SAMPLE),
        "--profile",
        profile,
    ])
    _run([
        sys.executable,
        "addons/video-ai-enhancer/tools/latency_guard_video.py",
        "--trace",
        str(LATENCY_SAMPLE),
        "--profile",
        profile,
    ])
    _run([
        sys.executable,
        "addons/video-ai-enhancer/tools/storage_capture_validator.py",
        "--report",
        str(STORAGE_SAMPLE),
        "--profile",
        profile,
    ])
    _run([
        sys.executable,
        "addons/video-ai-enhancer/tools/validate_ids_video_addin.py",
        str(ROOT / "addons" / "video-ai-enhancer"),
    ])
    _run([
        sys.executable,
        "-m",
        "compileall",
        "addons/video-ai-enhancer/tools",
    ])


def run_verification(mode: str) -> None:
    enabled, profile = _load_features()
    _ensure_ci_alignment(enabled)
    _ensure_readme_alignment(enabled)
    _check_idempotency(profile)

    if mode == "full" and enabled:
        _run_full_suite(profile)
    elif mode == "full" and not enabled:
        print("Add-in disabled; skipping guard execution.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the Video AI Enhancer add-in")
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
