"""Shared configuration utilities for the RJW-IDD Video AI Enhancer add-in.

Mirrors the 3D add-in loader but targets video quality, latency, and storage
budgets. Uses a lightweight YAML fallback so PyYAML remains optional.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import pathlib
import typing as t

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
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
    in_str = False
    quote: str | None = None
    result: list[str] = []
    for ch in line:
        if ch in {'"', "'"}:
            if quote is None:
                quote = ch
            elif quote == ch:
                quote = None
        if ch == "#" and quote is None:
            break
        result.append(ch)
    return "".join(result)


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
        entries.append((indent, stripped))
    if not entries:
        return {}
    root: t.Any = {}
    stack: list[tuple[int, t.Any]] = [(-1, root)]

    def ensure_container(parent: t.Any, key: str, indent: int, next_entry: tuple[int, str] | None) -> t.Any:
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
            value = content[2:].strip()
            if not value and i + 1 < len(entries) and entries[i + 1][0] > indent:
                item: t.Any = {}
                parent.append(item)
                stack.append((indent, item))
            elif ":" in value:
                key, _, remainder = value.partition(":")
                parent.append({key.strip(): _parse_scalar(remainder.strip())})
            else:
                parent.append(_parse_scalar(value))
        else:
            if ":" not in content:
                raise ConfigError(f"Invalid line in YAML: {content}")
            key, _, remainder = content.partition(":")
            key = key.strip()
            remainder = remainder.strip()
            if not isinstance(parent, dict):
                raise ConfigError("Cannot assign mapping under list context")
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
    if yaml is not None:  # pragma: no branch
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
    return load_yaml(CONFIG_DIR / "video-ai-enhancer.yml")


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
        return "baseline"
    data = load_yaml(features_path)
    try:
        return data["addons"]["video_ai_enhancer"]["profile"]  # type: ignore[index]
    except (KeyError, TypeError):  # pragma: no cover - defensive
        return "baseline"


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
    "PROFILES_DIR",
]
