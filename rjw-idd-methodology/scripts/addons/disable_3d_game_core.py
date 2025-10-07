#!/usr/bin/env python3
"""Disable the RJW-IDD 3D Game Core add-in."""
from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "addons" / "3d-game-core" / "tools"
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
ADDIN_LINK = "- [3D Game Core](addons/3d-game-core/README.md) — opt-in 3D harnesses, specs, and gates."


def _load_generic(path: pathlib.Path) -> dict:
    if path.exists():
        return load_yaml(path) or {}
    return {}


def _load_features() -> dict:
    try:
        return load_feature_registry(FEATURES_PATH)
    except FeatureRegistryError as exc:  # pragma: no cover - defensive bridge
        raise ConfigError(str(exc)) from exc


def _write_features(data: dict) -> None:
    try:
        dump_features(data, FEATURES_PATH)
    except FeatureRegistryError as exc:  # pragma: no cover - defensive bridge
        raise ConfigError(str(exc)) from exc


def _write_ci(data: dict) -> None:
    includes = data.get("includes", {})
    clean: dict[str, list[str]] = {}
    if isinstance(includes, dict):
        for key, values in includes.items():
            if isinstance(values, list):
                filtered = [item for item in values if item]
                if filtered:
                    clean[key] = filtered
    lines = ["includes:"]
    if clean:
        for key in sorted(clean):
            lines.append(f"  {key}:")
            for item in sorted(set(clean[key])):
                lines.append(f"    - {item}")
    else:
        lines.append("  {}")
    lines.append("")
    CI_INCLUDES_PATH.parent.mkdir(parents=True, exist_ok=True)
    CI_INCLUDES_PATH.write_text("\n".join(lines))


def _prune_ci_entries() -> None:
    if not CI_INCLUDES_PATH.exists():
        return
    data = _load_generic(CI_INCLUDES_PATH)
    includes: dict = data.get("includes", {})
    target = {
        "addons/3d-game-core/ci/snippets/github-actions_3d.yml",
        "addons/3d-game-core/ci/snippets/generic-ci_3d.yml",
    }
    changed = False
    for key, values in list(includes.items()):
        if not isinstance(values, list):
            continue
        filtered = [item for item in values if item not in target]
        if len(filtered) != len(values):
            includes[key] = filtered
            changed = True
    if changed:
        _write_ci({"includes": includes})


def _remove_readme_link() -> None:
    if not README_PATH.exists():
        return
    lines = README_PATH.read_text().splitlines()
    header = "## Add-ins"
    if header not in lines:
        return
    idx = lines.index(header)
    section_end = idx + 1
    while section_end < len(lines) and not lines[section_end].startswith("## "):
        section_end += 1
    section = lines[idx + 1:section_end]
    if ADDIN_LINK in section:
        section.remove(ADDIN_LINK)
    while section and section[0].strip() == "":
        section.pop(0)
    while section and section[-1].strip() == "":
        section.pop()
    if not section:
        del lines[idx:section_end]
        if idx < len(lines) and lines[idx].strip() == "":
            lines.pop(idx)
    else:
        lines[idx + 1:section_end] = section
    README_PATH.write_text("\n".join(lines) + "\n")


def disable_addin() -> None:
    data = _load_features()
    entry = ensure_entry(data, "3d_game_core")
    entry["enabled"] = False
    _write_features(data)
    _prune_ci_entries()
    _remove_readme_link()


def main() -> int:
    parser = argparse.ArgumentParser(description="Disable the 3D Game Core add-in")
    parser.parse_args()
    try:
        disable_addin()
    except ConfigError as exc:  # pragma: no cover
        parser.error(str(exc))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
