#!/usr/bin/env python3
"""Set the profile for the video-ai-enhancer add-on."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


VALID_PROFILES = [
    "baseline",
    "live_stream",
    "broadcast_mastering",
    "mobile_edge",
    "remote_collab",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        required=True,
        choices=VALID_PROFILES,
        help="Video AI enhancer profile to activate",
    )
    return parser.parse_args()


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


def set_profile(root: Path, profile: str) -> None:
    """Update the video_ai_enhancer profile in the feature registry."""
    features_path = root / "method" / "config" / "features.yml"
    
    with features_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    
    if "addons" not in config or "video_ai_enhancer" not in config["addons"]:
        print(
            "ERROR: video_ai_enhancer addon not found. Run enable_video_ai_enhancer.py first.",
            file=sys.stderr,
        )
        sys.exit(1)
    
    config["addons"]["video_ai_enhancer"]["profile"] = profile
    
    with features_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Set video_ai_enhancer profile to '{profile}' in {features_path}")
    print("\nNext steps:")
    print("  1. Add a change log entry in docs/change-log.md")
    print("  2. Review profile-specific defaults in rjw-idd-methodology/addons/video-ai-enhancer/profiles/")


def main() -> int:
    try:
        args = parse_args()
        root = find_project_root()
        set_profile(root, args.profile)
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
