import pathlib

from config_loader import CONFIG_DIR, deep_merge, load_base_config, load_merged_config, load_yaml


def test_load_merged_config_generic():
    cfg = load_merged_config(profile="generic")
    assert cfg.profile == "generic"
    assert cfg.data["performance_budgets"]["frame"]["cpu_ms"] == 16.6
    assert cfg.data["asset_rules"]["meshes"]["max_triangles"] == 120000


def test_deep_merge_simple():
    merged = deep_merge({"a": {"b": 1}, "c": 2}, {"a": {"d": 3}, "c": 4})
    assert merged["a"] == {"b": 1, "d": 3}
    assert merged["c"] == 4


def test_fallback_loader(monkeypatch, tmp_path):
    sample = tmp_path / "sample.yml"
    sample.write_text(
        """root:\n  key: value\n  list:\n    - item\n"""
    )
    monkeypatch.setattr("config_loader.yaml", None)
    data = load_yaml(sample)
    assert data == {"root": {"key": "value", "list": ["item"]}}


def test_profiles_exist():
    profile_dir = CONFIG_DIR.parent / "profiles"
    expected = {"generic", "first_person", "third_person", "topdown", "isometric", "platformer", "driving", "networked"}
    discovered = {p.stem for p in profile_dir.glob("*.yml")}
    assert expected.issubset(discovered)
