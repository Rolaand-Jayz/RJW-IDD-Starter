#!/usr/bin/env python3
"""Enable the RJW-IDD 3D Game Core add-in."""
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


def _ensure_parent(path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _load_features() -> dict:
    try:
        return load_feature_registry(FEATURES_PATH)
    except FeatureRegistryError as exc:  # pragma: no cover - map to ConfigError for CLI parity
        raise ConfigError(str(exc)) from exc


def _write_features(data: dict) -> None:
    try:
        dump_features(data, FEATURES_PATH)
    except FeatureRegistryError as exc:  # pragma: no cover - map to ConfigError for CLI parity
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
        if not values:
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
    gha_entry = "addons/3d-game-core/ci/snippets/github-actions_3d.yml"
    generic_entry = "addons/3d-game-core/ci/snippets/generic-ci_3d.yml"
    if gha_entry not in includes["github_actions"]:
        includes["github_actions"].append(gha_entry)
    if generic_entry not in includes["generic"]:
        includes["generic"].append(generic_entry)
    _write_ci_includes(data)


def _ensure_readme_link() -> None:
    if not README_PATH.exists():
        return
    lines = README_PATH.read_text().splitlines()
    header = "## Add-ins"
    bullet = ADDIN_LINK
    if header not in lines:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend([header, "", bullet])
    else:
        idx = lines.index(header)
        section_end = idx + 1
        while section_end < len(lines) and not lines[section_end].startswith("## "):
            section_end += 1
        section = lines[idx + 1:section_end]
        if bullet not in section:
            insertion_point = idx + 1
            if insertion_point >= len(lines) or lines[insertion_point].strip():
                lines.insert(insertion_point, "")
                insertion_point += 1
            lines.insert(insertion_point, bullet)
    README_PATH.write_text("\n".join(lines) + "\n")


def enable_addin() -> None:
    data = _load_features()
    entry = ensure_entry(data, "3d_game_core")
    entry["enabled"] = True
    _write_features(data)
    _ensure_ci_registration()
    _ensure_readme_link()


def main() -> int:
    parser = argparse.ArgumentParser(description="Enable the 3D Game Core add-in")
    parser.parse_args()
    try:
        enable_addin()
    except ConfigError as exc:  # pragma: no cover - defensive; raises SystemExit via argparse
        parser.error(str(exc))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
