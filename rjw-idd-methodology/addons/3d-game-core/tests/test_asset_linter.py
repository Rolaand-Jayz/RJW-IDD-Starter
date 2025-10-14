import pathlib
from types import SimpleNamespace


from config_loader import load_merged_config
from asset_linter_3d import lint_assets


def test_asset_linter_pass(tmp_path):
    manifest = tmp_path / 'assets_manifest.json'
    manifest.write_text(pathlib.Path('ci_samples/assets_manifest.json').read_text())
    config = load_merged_config(profile='generic')
    args = SimpleNamespace(manifest=str(manifest), assets=str(tmp_path), profile='generic')
    violations = lint_assets(config, args)
    assert violations == []


def test_asset_linter_failure(tmp_path):
    manifest = tmp_path / 'assets_manifest.json'
    manifest.write_text(pathlib.Path('ci_samples/assets_manifest_violation.json').read_text())
    config = load_merged_config(profile='generic')
    args = SimpleNamespace(manifest=str(manifest), assets=str(tmp_path), profile='generic')
    violations = lint_assets(config, args)
    assert violations  # expect at least one violation
