import pathlib

import pytest

import config_loader
from config_loader import ConfigError, load_base_config, load_merged_config, load_profile


def test_load_base_config_contains_metadata():
    data = load_base_config()
    metadata = data["metadata"]
    assert metadata["default_profile"] == "baseline"
    assert metadata["version"] == "1.0.0"


def test_load_profile_overrides_live_stream():
    profile = load_profile("live_stream")
    assert profile["name"] == "live_stream"
    overrides = profile["overrides"]
    assert overrides["quality_targets"]["metrics"]["vmaf"] == 90
    assert overrides["latency_budgets"]["glass_to_glass_ms"] == 90


def test_load_merged_config_specific_profile():
    merged = load_merged_config(profile="broadcast_mastering")
    assert merged.profile == "broadcast_mastering"
    assert merged.data["quality_targets"]["metrics"]["vmaf"] == 94
    # Ensure base values still present when not overridden
    assert merged.data["storage_pipeline"]["max_parallel_writers"] == 4


def test_get_active_profile_reads_features(tmp_path: pathlib.Path):
    features = tmp_path / "features.yml"
    features.write_text(
        """# FEATURE-REGISTRY-0001 — RJW-IDD Add-ins Registry
addons:
  video_ai_enhancer:
    enabled: true
    version: 1.0.0
    profile: live_stream
    description: "test"
"""
    )
    assert config_loader.get_active_profile(features) == "live_stream"


def test_get_active_profile_defaults_when_missing(tmp_path: pathlib.Path):
    missing = tmp_path / "missing.yml"
    assert config_loader.get_active_profile(missing) == "baseline"


def test_load_profile_missing_raises():
    with pytest.raises(ConfigError):
        load_profile("does-not-exist")
