"""Shared configuration loading utilities for the RJW-IDD 3D game core add-in.

The helpers avoid a hard dependency on PyYAML by providing a small fallback
parser that understands the subset of YAML used in the repository. If PyYAML is
installed it will be used automatically.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import pathlib
import typing as t

try:  # pragma: no cover - optional import
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - handled by fallback
    yaml = None  # type: ignore

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / "config"
PROFILES_DIR = BASE_DIR / "profiles"
FEATURES_PATH = pathlib.Path("method/config/features.yml")


class ConfigError(RuntimeError):
    """Raised when configuration files are missing or malformed."""


def _strip_inline_comment(line: str) -> str:
    if "#" not in line:
        return line
    quote = None
    result_chars = []
    for ch in line:
        if ch in {'"', "'"}:
            if quote is None:
                quote = ch
            elif quote == ch:
                quote = None
        if ch == "#" and quote is None:
            break
        result_chars.append(ch)
    return "".join(result_chars)


def _parse_scalar(token: str) -> t.Any:
    token = token.strip()
    if not token:
        return None
    lowered = token.lower()
    if lowered in {"null", "~"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if token.startswith("\"") and token.endswith("\""):
        return token[1:-1]
    if token.startswith("'") and token.endswith("'"):
        return token[1:-1]
    try:
        if "." in token:
            return float(token)
        return int(token)
    except ValueError:
        pass
    if token.startswith("[") and token.endswith("]"):
        try:
            return json.loads(token)
        except json.JSONDecodeError:
            return token
    return token


def _fallback_yaml_load(text: str) -> t.Any:
    entries: list[tuple[int, str]] = []
    for raw_line in text.splitlines():
        stripped = _strip_inline_comment(raw_line).rstrip()
        if not stripped:
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        entries.append((indent, stripped.strip()))
    if not entries:
        return {}
    root: t.Any = {}
    stack: list[tuple[int, t.Any]] = [(-1, root)]

    def ensure_container(parent: t.Any, key: str, indent: int, next_entry: t.Optional[tuple[int, str]]) -> t.Any:
        if next_entry and next_entry[0] > indent and next_entry[1].startswith("- "):
            container: t.Any = []
        else:
            container = {}
        parent[key] = container
        stack.append((indent, container))
        return container

    i = 0
    while i < len(entries):
        indent, content = entries[i]
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if content.startswith("- "):
            if not isinstance(parent, list):
                raise ConfigError("Unexpected list item without list context")
            value_part = content[2:].strip()
            if not value_part and i + 1 < len(entries) and entries[i + 1][0] > indent:
                item: t.Any = {}
                parent.append(item)
                stack.append((indent, item))
            elif ":" in value_part:
                key, _, remainder = value_part.partition(":")
                item = {key.strip(): _parse_scalar(remainder.strip())}
                parent.append(item)
            else:
                parent.append(_parse_scalar(value_part))
        else:
            if ":" not in content:
                raise ConfigError(f"Invalid line in YAML: {content}")
            key, _, remainder = content.partition(":")
            key = key.strip()
            remainder = remainder.strip()
            if not isinstance(parent, dict):
                raise ConfigError("Cannot assign key/value under a list item")
            if remainder:
                value = _parse_scalar(remainder)
                parent[key] = value
                if isinstance(value, (dict, list)):
                    stack.append((indent, value))
            else:
                next_entry = entries[i + 1] if i + 1 < len(entries) else None
                ensure_container(parent, key, indent, next_entry)
        i += 1
    return root


def load_yaml(path: pathlib.Path) -> t.Any:
    if not path.exists():
        raise ConfigError(f"Missing configuration file: {path}")
    text = path.read_text()
    if yaml is not None:  # pragma: no branch - depends on environment
        data = yaml.safe_load(text)  # type: ignore[arg-type]
        return data or {}
    return _fallback_yaml_load(text)


def deep_merge(base: t.Mapping[str, t.Any], override: t.Mapping[str, t.Any]) -> dict:
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_base_config() -> dict:
    return load_yaml(CONFIG_DIR / "3d-game-core.yml")


def load_profile(profile: str) -> dict:
    profile_path = PROFILES_DIR / f"{profile}.yml"
    data = load_yaml(profile_path)
    if not isinstance(data, dict):
        raise ConfigError(f"Profile {profile} malformed: expected mapping")
    overrides = data.get("overrides", {})
    if not isinstance(overrides, dict):
        raise ConfigError(f"Profile {profile} overrides must be a mapping")
    return {
        "name": data.get("profile", profile),
        "description": data.get("description", ""),
        "overrides": overrides,
    }


def get_active_profile(features_path: pathlib.Path = FEATURES_PATH) -> str:
    if not features_path.exists():
        return "generic"
    data = load_yaml(features_path)
    try:
        return data["addons"]["3d_game_core"]["profile"]  # type: ignore[index]
    except (KeyError, TypeError):  # pragma: no cover - defensive
        return "generic"


@dataclass(frozen=True)
class MergedConfig:
    profile: str
    description: str
    data: dict


def load_merged_config(profile: str | None = None) -> MergedConfig:
    base = load_base_config()
    effective_profile = profile or get_active_profile()
    profile_data = load_profile(effective_profile)
    merged = deep_merge(base, profile_data.get("overrides", {}))
    merged["profile"] = effective_profile
    return MergedConfig(
        profile=effective_profile,
        description=profile_data.get("description", ""),
        data=merged,
    )


__all__ = [
    "ConfigError",
    "FEATURES_PATH",
    "MergedConfig",
    "deep_merge",
    "load_base_config",
    "load_merged_config",
    "load_profile",
    "load_yaml",
]
