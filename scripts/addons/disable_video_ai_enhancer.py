#!/usr/bin/env python3
"""Disable the video-ai-enhancer add-on for RJW-IDD projects."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def find_project_root() -> Path:
    """Locate the project root by searching for method/config/features.yml."""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        features_file = parent / "method" / "config" / "features.yml"
        if features_file.exists():
            return parent
    raise FileNotFoundError(
        "Cannot locate method/config/features.yml. "
        "Run this script from within the RJW-IDD project structure."
    )


def disable_addon(root: Path) -> None:
    """Disable the video_ai_enhancer addon in the feature registry."""
    features_path = root / "method" / "config" / "features.yml"
    
    with features_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    
    if "addons" not in config or "video_ai_enhancer" not in config["addons"]:
        print("✓ video_ai_enhancer addon was not enabled")
        return
    
    config["addons"]["video_ai_enhancer"]["enabled"] = False
    
    with features_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Disabled video_ai_enhancer addon in {features_path}")
    print("\nNext steps:")
    print("  1. Add a change log entry in docs/change-log.md")
    print("  2. Record the decision in docs/decisions/")


def main() -> int:
    try:
        root = find_project_root()
        disable_addon(root)
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
