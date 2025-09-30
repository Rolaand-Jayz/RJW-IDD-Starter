#!/usr/bin/env python3
"""Pre-merge guard for the Video AI Enhancer add-in."""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "addons" / "video-ai-enhancer" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from config_loader import load_yaml  # type: ignore  # noqa: E402

FEATURES_PATH = ROOT / "method/config/features.yml"


def main() -> int:
    if not FEATURES_PATH.exists():
        return 0
    data = load_yaml(FEATURES_PATH) or {}
    enabled = bool(data.get("addons", {}).get("video_ai_enhancer", {}).get("enabled", False))
    if not enabled:
        return 0
    result = subprocess.run(
        [sys.executable, "scripts/addons/verify_video_ai_enhancer.py", "--mode", "smoke"],
        cwd=ROOT,
        text=True,
    )
    return result.returncode


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
