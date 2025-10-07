#!/usr/bin/env python3
"""Set the active profile for the Video AI Enhancer add-in."""
from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "addons" / "video-ai-enhancer" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from config_loader import ConfigError, PROFILES_DIR  # type: ignore  # noqa: E402
from _feature_registry import (  # type: ignore  # noqa: E402
    FeatureRegistryError,
    dump_features,
    ensure_entry,
    load_features as load_feature_registry,
)

FEATURES_PATH = ROOT / "method/config/features.yml"
FEATURE_KEY = "video_ai_enhancer"


def _load_features() -> dict:
    try:
        return load_feature_registry(FEATURES_PATH)
    except FeatureRegistryError as exc:  # pragma: no cover
        raise ConfigError(str(exc)) from exc


def _write_features(data: dict) -> None:
    try:
        dump_features(data, FEATURES_PATH)
    except FeatureRegistryError as exc:  # pragma: no cover
        raise ConfigError(str(exc)) from exc


def set_profile(new_profile: str) -> None:
    profile_path = PROFILES_DIR / f"{new_profile}.yml"
    if not profile_path.exists():
        available = sorted(p.stem for p in PROFILES_DIR.glob("*.yml"))
        raise ConfigError(f"Profile '{new_profile}' not found. Available: {', '.join(available)}")
    data = _load_features()
    entry = ensure_entry(data, FEATURE_KEY)
    entry["profile"] = new_profile
    _write_features(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Set the profile for the Video AI Enhancer add-in")
    parser.add_argument("--profile", required=True, help="Profile name (e.g., live_stream)")
    args = parser.parse_args()
    try:
        set_profile(args.profile)
    except ConfigError as exc:  # pragma: no cover
        parser.error(str(exc))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
