import pathlib
from types import SimpleNamespace

import pytest

from config_loader import load_merged_config
from tolerant_replay_runner import evaluate_snapshots


def test_tolerant_replay_pass(tmp_path):
    src = pathlib.Path('ci_samples/tolerant_snapshots.json')
    tmp_file = tmp_path / 'snapshots.json'
    tmp_file.write_text(src.read_text())
    config = load_merged_config(profile='generic')
    args = SimpleNamespace(snapshots=str(tmp_file), profile='generic', scale=1.0, output=None)
    result = evaluate_snapshots(config, args)
    assert result['highest_streak'] == 0


def test_tolerant_replay_failure(tmp_path):
    src = pathlib.Path('ci_samples/tolerant_snapshots_drift.json')
    tmp_file = tmp_path / 'snapshots.json'
    tmp_file.write_text(src.read_text())
    config = load_merged_config(profile='generic')
    args = SimpleNamespace(snapshots=str(tmp_file), profile='generic', scale=1.0, output=None)
    with pytest.raises(Exception):
        evaluate_snapshots(config, args)
