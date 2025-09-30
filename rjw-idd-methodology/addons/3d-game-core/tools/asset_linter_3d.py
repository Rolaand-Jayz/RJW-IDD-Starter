"""Asset linter for RJW-IDD 3D add-in."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import typing as t

from config_loader import ConfigError, MergedConfig, load_merged_config

Asset = t.Dict[str, t.Any]


def load_manifest(path: pathlib.Path) -> list[Asset]:
    if not path.exists():
        raise ConfigError(f"Asset manifest not found: {path}")
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        assets = data.get("assets", [])
    else:
        assets = data
    if not isinstance(assets, list):
        raise ConfigError("Asset manifest must be a list or contain an 'assets' list")
    return assets


def check_mesh(asset: Asset, rules: dict) -> list[str]:
    metrics = asset.get("metrics", {})
    violations = []
    def require(key: str, default: float | int) -> float:
        value = metrics.get(key, default)
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(default)
    tri = require("triangles", 0)
    if tri > rules.get("max_triangles", float("inf")):
        violations.append(f"triangles {tri} > {rules.get('max_triangles')}")
    verts = require("vertices", 0)
    if verts > rules.get("max_vertices", float("inf")):
        violations.append(f"vertices {verts} > {rules.get('max_vertices')}")
    lods = int(metrics.get("lods", 0))
    if lods > rules.get("max_lods", lods):
        violations.append(f"lod count {lods} > {rules.get('max_lods')}")
    scale = metrics.get("scale_unit")
    expected_scale = rules.get("enforce_scale_unit")
    if expected_scale and scale and scale != expected_scale:
        violations.append(f"scale '{scale}' != '{expected_scale}'")
    pivot = metrics.get("pivot")
    expected_pivot = rules.get("pivot_rules")
    if expected_pivot and pivot and pivot != expected_pivot:
        violations.append(f"pivot '{pivot}' != '{expected_pivot}'")
    collision = metrics.get("collision_complexity")
    allowed = rules.get("collision_complexity")
    if allowed and collision and collision not in {allowed, "low"}:
        violations.append(f"collision complexity '{collision}' > {allowed}")
    if rules.get("non_manifold_check") and metrics.get("non_manifold", False):
        violations.append("non-manifold geometry present")
    return violations


def check_material(asset: Asset, rules: dict) -> list[str]:
    metrics = asset.get("metrics", {})
    violations = []
    mats = int(metrics.get("material_count", 0))
    if mats > rules.get("max_per_mesh", mats):
        violations.append(f"material count {mats} > {rules.get('max_per_mesh')}")
    variants = int(metrics.get("shader_variants", 0))
    if variants > rules.get("shader_variant_cap", variants):
        violations.append(f"shader variants {variants} > {rules.get('shader_variant_cap')}")
    return violations


def check_texture(asset: Asset, rules: dict) -> list[str]:
    metrics = asset.get("metrics", {})
    violations = []
    dim = int(metrics.get("max_dimension", metrics.get("width", 0)))
    if dim > rules.get("max_dimension", dim):
        violations.append(f"dimension {dim} > {rules.get('max_dimension')}")
    atlas_dim = int(metrics.get("atlas_dimension", dim))
    if atlas_dim > rules.get("atlas_max_dimension", atlas_dim):
        violations.append(f"atlas dimension {atlas_dim} > {rules.get('atlas_max_dimension')}")
    fmt = metrics.get("format")
    whitelist = rules.get("formats_whitelist")
    if whitelist and fmt and fmt not in whitelist:
        violations.append(f"format '{fmt}' not in whitelist {whitelist}")
    if rules.get("enforce_power_of_two") and metrics.get("power_of_two", True) is False:
        violations.append("texture dimensions must be power of two")
    return violations


def check_skeletal(asset: Asset, rules: dict) -> list[str]:
    metrics = asset.get("metrics", {})
    violations = []
    bones = int(metrics.get("bones", 0))
    if bones > rules.get("max_bones_per_mesh", bones):
        violations.append(f"bones {bones} > {rules.get('max_bones_per_mesh')}")
    duration = float(metrics.get("animation_seconds", 0.0))
    if duration > rules.get("animation_max_seconds", duration):
        violations.append(f"animation seconds {duration} > {rules.get('animation_max_seconds')}")
    fps = float(metrics.get("animation_fps", 0.0))
    if fps > rules.get("animation_max_fps", fps):
        violations.append(f"animation fps {fps} > {rules.get('animation_max_fps')}")
    return violations


def check_audio(asset: Asset, rules: dict) -> list[str]:
    metrics = asset.get("metrics", {})
    violations = []
    lufs = float(metrics.get("lufs", 0.0))
    if lufs > rules.get("target_lufs", lufs):
        violations.append(f"LUFS {lufs} > target {rules.get('target_lufs')}")
    peak = float(metrics.get("peak_db", 0.0))
    if peak > rules.get("peak_ceiling_db", peak):
        violations.append(f"peak {peak}dB > ceiling {rules.get('peak_ceiling_db')}dB")
    return violations


CHECKS = {
    "mesh": check_mesh,
    "material": check_material,
    "texture": check_texture,
    "skeletal": check_skeletal,
    "audio": check_audio,
}

RULE_KEYS = {
    "mesh": "meshes",
    "material": "materials",
    "texture": "textures",
    "skeletal": "skeletal",
    "audio": "audio",
}


def lint_assets(config: MergedConfig, args: argparse.Namespace) -> list[str]:
    manifest_path = pathlib.Path(args.manifest) if args.manifest else pathlib.Path(args.assets) / "assets_manifest.json"
    assets = load_manifest(manifest_path)
    asset_rules = config.data.get("asset_rules", {})

    violations_output: list[str] = []
    for asset in assets:
        asset_type = asset.get("type")
        name = asset.get("name", "<unnamed>")
        checker = CHECKS.get(str(asset_type))
        if not checker:
            continue
        rules = asset_rules.get(RULE_KEYS.get(str(asset_type), ""), {})
        violations = checker(asset, rules)
        if violations:
            violations_output.append(f"{asset_type}:{name} -> {', '.join(violations)}")
    return violations_output


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RJW-IDD 3D asset linter")
    parser.add_argument("--assets", default=".", help="Asset root directory")
    parser.add_argument("--manifest", help="Optional explicit path to manifest JSON")
    parser.add_argument("--profile", help="Override profile name")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        config = load_merged_config(profile=args.profile)
        violations = lint_assets(config, args)
    except ConfigError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover

    if violations:
        print("Asset violations detected:")
        for violation in violations:
            print(f"  - {violation}")
        return 1
    print("No asset violations detected.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
