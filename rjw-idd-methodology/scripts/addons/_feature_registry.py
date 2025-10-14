"""Shared helpers for managing the RJW-IDD feature registry."""
from __future__ import annotations

import json
import pathlib
import typing as t

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback parser will be used
    yaml = None  # type: ignore

ROOT = pathlib.Path(__file__).resolve().parents[2]
FEATURES_PATH = ROOT / "method/config/features.yml"

DEFAULT_ENTRIES: dict[str, dict[str, t.Any]] = {
    "3d_game_core": {
        "enabled": False,
        "version": "1.0.0",
        "profile": "generic",
        "description": "RJW-IDD add-in for all 3D games: profiles, determinism/rollback harnesses, tolerant replays, asset & perf gates, GDD/engine spec templates, IDD pacts.",
    },
    "video_ai_enhancer": {
        "enabled": False,
        "version": "1.0.0",
        "profile": "baseline",
        "description": "RJW-IDD add-in for real-time video enhancement/upscaling pipelines with capture, quality, latency, and storage governance.",
    },
}

_FIELD_ORDER = ("enabled", "version", "profile", "description")


class FeatureRegistryError(RuntimeError):
    """Raised when the feature registry cannot be processed."""


def _strip_inline_comment(line: str) -> str:
    if "#" not in line:
        return line
    quote: str | None = None
    out: list[str] = []
    for ch in line:
        if ch in {'"', "'"}:
            if quote is None:
                quote = ch
            elif quote == ch:
                quote = None
        if ch == "#" and quote is None:
            break
        out.append(ch)
    return "".join(out)


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
    for raw in text.splitlines():
        stripped = _strip_inline_comment(raw).rstrip()
        if not stripped:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
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
                raise FeatureRegistryError("Unexpected list item without parent list")
            value_part = content[2:].strip()
            if not value_part and i + 1 < len(entries) and entries[i + 1][0] > indent:
                item: t.Any = {}
                parent.append(item)
                stack.append((indent, item))
            elif ":" in value_part:
                key, _, remainder = value_part.partition(":")
                parent.append({key.strip(): _parse_scalar(remainder.strip())})
            else:
                parent.append(_parse_scalar(value_part))
        else:
            if ":" not in content:
                raise FeatureRegistryError(f"Invalid line in features registry: {content}")
            key, _, remainder = content.partition(":")
            key = key.strip()
            remainder = remainder.strip()
            if not isinstance(parent, dict):
                raise FeatureRegistryError("Cannot assign mapping entry under list context")
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


def load_features(path: pathlib.Path = FEATURES_PATH) -> dict:
    if not path.exists():
        return {"addons": {}}
    text = path.read_text()
    if yaml is not None:  # pragma: no branch - depends on runtime deps
        loaded = yaml.safe_load(text)  # type: ignore[arg-type]
    else:
        loaded = _fallback_yaml_load(text)
    if not isinstance(loaded, dict):
        raise FeatureRegistryError("Feature registry must contain a mapping")
    addons = loaded.setdefault("addons", {})
    if not isinstance(addons, dict):
        raise FeatureRegistryError("'addons' section must be a mapping")
    return loaded


def ensure_entry(data: dict, key: str, defaults: dict[str, t.Any] | None = None) -> dict[str, t.Any]:
    addons = data.setdefault("addons", {})
    if not isinstance(addons, dict):
        raise FeatureRegistryError("'addons' must remain a mapping")
    entry = addons.get(key)
    if entry is None:
        entry = dict(DEFAULT_ENTRIES.get(key, {}))
        if defaults:
            entry.update(defaults)
        addons[key] = entry
    else:
        entry_defaults = DEFAULT_ENTRIES.get(key, {})
        for d_key, d_value in entry_defaults.items():
            entry.setdefault(d_key, d_value)
        if defaults:
            for d_key, d_value in defaults.items():
                entry.setdefault(d_key, d_value)
    return entry


def _format_scalar(value: t.Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    escaped = text.replace('"', '\\"')
    return f'"{escaped}"'


def dump_features(data: dict, path: pathlib.Path = FEATURES_PATH) -> None:
    addons = data.get("addons", {})
    if not isinstance(addons, dict):
        raise FeatureRegistryError("'addons' section must be a mapping")
    lines = ["# FEATURE-REGISTRY-0001 — RJW-IDD Add-ins Registry", "addons:"]
    for key in sorted(addons):
        lines.append(f"  {key}:")
        entry = addons[key]
        if not isinstance(entry, dict):
            raise FeatureRegistryError(f"Add-in '{key}' must map to a dictionary")
        seen: set[str] = set()
        for field in _FIELD_ORDER:
            if field in entry:
                lines.append(f"    {field}: {_format_scalar(entry[field])}")
                seen.add(field)
        for field in sorted(entry):
            if field in seen:
                continue
            lines.append(f"    {field}: {_format_scalar(entry[field])}")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


__all__ = [
    "DEFAULT_ENTRIES",
    "FEATURES_PATH",
    "FeatureRegistryError",
    "dump_features",
    "ensure_entry",
    "load_features",
]
