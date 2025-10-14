"""Tests for add-on management scripts."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "addons"))


def test_enable_3d_game_core_creates_entry(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test enabling 3d_game_core addon when entry doesn't exist."""
    pytest.importorskip("yaml")

    from enable_3d_game_core import enable_addon

    # Create method/config directory structure
    method_dir = tmp_path / "method" / "config"
    method_dir.mkdir(parents=True)
    features_file = method_dir / "features.yml"
    features_file.write_text("addons: {}\n")

    enable_addon(tmp_path)

    # Verify the file was updated
    import yaml
    with features_file.open("r") as f:
        config = yaml.safe_load(f)

    assert "addons" in config
    assert "3d_game_core" in config["addons"]
    assert config["addons"]["3d_game_core"]["enabled"] is True
    assert config["addons"]["3d_game_core"]["profile"] == "generic"


def test_enable_3d_game_core_updates_existing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test enabling 3d_game_core addon when entry already exists."""
    pytest.importorskip("yaml")
    import yaml
    from enable_3d_game_core import enable_addon

    # Create method/config directory structure with existing disabled addon
    method_dir = tmp_path / "method" / "config"
    method_dir.mkdir(parents=True)
    features_file = method_dir / "features.yml"

    initial_config = {
        "addons": {
            "3d_game_core": {
                "enabled": False,
                "version": "1.0.0",
                "profile": "first_person",
                "description": "Test",
            }
        }
    }

    with features_file.open("w") as f:
        yaml.safe_dump(initial_config, f)

    enable_addon(tmp_path)

    # Verify the file was updated
    with features_file.open("r") as f:
        config = yaml.safe_load(f)

    assert config["addons"]["3d_game_core"]["enabled"] is True
    assert config["addons"]["3d_game_core"]["profile"] == "first_person"  # Preserved


def test_disable_3d_game_core(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test disabling 3d_game_core addon."""
    pytest.importorskip("yaml")
    import yaml
    from disable_3d_game_core import disable_addon

    # Create method/config directory structure with enabled addon
    method_dir = tmp_path / "method" / "config"
    method_dir.mkdir(parents=True)
    features_file = method_dir / "features.yml"

    initial_config = {
        "addons": {
            "3d_game_core": {
                "enabled": True,
                "version": "1.0.0",
                "profile": "generic",
                "description": "Test",
            }
        }
    }

    with features_file.open("w") as f:
        yaml.safe_dump(initial_config, f)

    disable_addon(tmp_path)

    # Verify the file was updated
    with features_file.open("r") as f:
        config = yaml.safe_load(f)

    assert config["addons"]["3d_game_core"]["enabled"] is False


def test_set_3d_profile(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test setting 3D game profile."""
    pytest.importorskip("yaml")
    import yaml
    from set_3d_profile import set_profile

    # Create method/config directory structure with enabled addon
    method_dir = tmp_path / "method" / "config"
    method_dir.mkdir(parents=True)
    features_file = method_dir / "features.yml"

    initial_config = {
        "addons": {
            "3d_game_core": {
                "enabled": True,
                "version": "1.0.0",
                "profile": "generic",
                "description": "Test",
            }
        }
    }

    with features_file.open("w") as f:
        yaml.safe_dump(initial_config, f)

    set_profile(tmp_path, "third_person")

    # Verify the file was updated
    with features_file.open("r") as f:
        config = yaml.safe_load(f)

    assert config["addons"]["3d_game_core"]["profile"] == "third_person"


def test_enable_video_ai_enhancer_creates_entry(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test enabling video_ai_enhancer addon when entry doesn't exist."""
    pytest.importorskip("yaml")

    from enable_video_ai_enhancer import enable_addon

    # Create method/config directory structure
    method_dir = tmp_path / "method" / "config"
    method_dir.mkdir(parents=True)
    features_file = method_dir / "features.yml"
    features_file.write_text("addons: {}\n")

    enable_addon(tmp_path)

    # Verify the file was updated
    import yaml
    with features_file.open("r") as f:
        config = yaml.safe_load(f)

    assert "addons" in config
    assert "video_ai_enhancer" in config["addons"]
    assert config["addons"]["video_ai_enhancer"]["enabled"] is True
    assert config["addons"]["video_ai_enhancer"]["profile"] == "baseline"


def test_set_video_ai_profile(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test setting video AI enhancer profile."""
    pytest.importorskip("yaml")
    import yaml
    from set_video_ai_profile import set_profile

    # Create method/config directory structure with enabled addon
    method_dir = tmp_path / "method" / "config"
    method_dir.mkdir(parents=True)
    features_file = method_dir / "features.yml"

    initial_config = {
        "addons": {
            "video_ai_enhancer": {
                "enabled": True,
                "version": "1.0.0",
                "profile": "baseline",
                "description": "Test",
            }
        }
    }

    with features_file.open("w") as f:
        yaml.safe_dump(initial_config, f)

    set_profile(tmp_path, "live_stream")

    # Verify the file was updated
    with features_file.open("r") as f:
        config = yaml.safe_load(f)

    assert config["addons"]["video_ai_enhancer"]["profile"] == "live_stream"
