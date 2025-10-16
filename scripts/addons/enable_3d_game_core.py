#!/usr/bin/env python3
"""Enable the 3d-game-core add-on for RJW-IDD projects."""
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


def enable_addon(root: Path) -> None:
    """Enable the 3d_game_core addon in the feature registry."""
    features_path = root / "method" / "config" / "features.yml"

    with features_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    if "addons" not in config:
        config["addons"] = {}

    if "3d_game_core" not in config["addons"]:
        config["addons"]["3d_game_core"] = {
            "enabled": True,
            "version": "0.1.0-alpha",
            "profile": "generic",
            "description": "RJW-IDD add-in for all 3D games: profiles, determinism/rollback harnesses, tolerant replays, asset & perf gates, GDD/engine spec templates, IDD pacts.",
        }
        print("✓ Created 3d_game_core addon entry")
    else:
        config["addons"]["3d_game_core"]["enabled"] = True
        print("✓ Enabled 3d_game_core addon (was already defined)")

    with features_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Updated {features_path}")
    print("\nNext steps:")
    print("  1. Set a profile: python scripts/addons/set_3d_profile.py --profile <profile>")
    print("  2. Add a change log entry in templates-and-examples/templates/change-logs/CHANGELOG-template.md")
    print("  3. Record the decision in docs/decisions/")


def main() -> int:
    try:
        root = find_project_root()
        enable_addon(root)
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
