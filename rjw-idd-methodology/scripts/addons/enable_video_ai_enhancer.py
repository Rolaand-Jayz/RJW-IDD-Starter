#!/usr/bin/env python3
"""Enable the RJW-IDD Video AI Enhancer add-in."""
from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "addons" / "video-ai-enhancer" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from config_loader import ConfigError, load_yaml  # type: ignore  # noqa: E402
from _feature_registry import (  # type: ignore  # noqa: E402
    FeatureRegistryError,
    dump_features,
    ensure_entry,
    load_features as load_feature_registry,
)

FEATURES_PATH = ROOT / "method/config/features.yml"
CI_INCLUDES_PATH = ROOT / "ci/includes.yml"
README_PATH = ROOT / "README.md"
FEATURE_KEY = "video_ai_enhancer"
ADDIN_LINK = "- [Video AI Enhancer](addons/video-ai-enhancer/README.md) — opt-in real-time video enhancement and capture gates."
GHA_ENTRY = "addons/video-ai-enhancer/ci/snippets/github-actions_video.yml"
GENERIC_ENTRY = "addons/video-ai-enhancer/ci/snippets/generic-ci_video.yml"


def _ensure_parent(path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


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


def _load_ci_includes() -> dict:
    if CI_INCLUDES_PATH.exists():
        return load_yaml(CI_INCLUDES_PATH) or {}
    return {"includes": {}}


def _write_ci_includes(data: dict) -> None:
    _ensure_parent(CI_INCLUDES_PATH)
    includes: dict[str, list[str]] = data.setdefault("includes", {})  # type: ignore[assignment]
    lines = ["includes:"]
    for key in sorted(includes):
        values = includes[key]
        if not isinstance(values, list) or not values:
            continue
        lines.append(f"  {key}:")
        for value in sorted(set(values)):
            lines.append(f"    - {value}")
    if len(lines) == 1:
        lines.append("  {}")
    lines.append("")
    CI_INCLUDES_PATH.write_text("\n".join(lines))


def _ensure_ci_registration() -> None:
    data = _load_ci_includes()
    includes: dict[str, list[str]] = data.setdefault("includes", {})  # type: ignore[assignment]
    includes.setdefault("github_actions", [])
    includes.setdefault("generic", [])
    if GHA_ENTRY not in includes["github_actions"]:
        includes["github_actions"].append(GHA_ENTRY)
    if GENERIC_ENTRY not in includes["generic"]:
        includes["generic"].append(GENERIC_ENTRY)
    _write_ci_includes(data)


def _ensure_readme_link() -> None:
    if not README_PATH.exists():
        return
    lines = README_PATH.read_text().splitlines()
    header = "## Add-ins"
    if header not in lines:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend([header, "", ADDIN_LINK])
    else:
        idx = lines.index(header)
        section_end = idx + 1
        while section_end < len(lines) and not lines[section_end].startswith("## "):
            section_end += 1
        section = lines[idx + 1:section_end]
        if ADDIN_LINK not in section:
            insertion_point = idx + 1
            if insertion_point >= len(lines) or lines[insertion_point].strip():
                lines.insert(insertion_point, "")
                insertion_point += 1
            lines.insert(insertion_point, ADDIN_LINK)
    README_PATH.write_text("\n".join(lines) + "\n")


def enable_addin() -> None:
    data = _load_features()
    entry = ensure_entry(data, FEATURE_KEY)
    entry["enabled"] = True
    _write_features(data)
    _ensure_ci_registration()
    _ensure_readme_link()


def main() -> int:
    parser = argparse.ArgumentParser(description="Enable the Video AI Enhancer add-in")
    parser.parse_args()
    try:
        enable_addin()
    except ConfigError as exc:  # pragma: no cover
        parser.error(str(exc))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
