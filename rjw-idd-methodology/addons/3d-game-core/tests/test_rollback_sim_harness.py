import pathlib
from types import SimpleNamespace

import pytest

from config_loader import load_merged_config
from rollback_sim_harness import evaluate_tape


def test_rollback_harness_pass(tmp_path):
    src = pathlib.Path('ci_samples/rollback_tape.json')
    tape_path = tmp_path / 'rollback.json'
    tape_path.write_text(src.read_text())
    config = load_merged_config(profile='generic')
    args = SimpleNamespace(tape=str(tape_path), profile='generic', output=None)
    result = evaluate_tape(config, args)
    assert result['max_depth'] <= config.data['rollback']['rollback_depth_threshold']


def test_rollback_harness_fail(tmp_path):
    src = pathlib.Path('ci_samples/rollback_tape_violation.json')
    tape_path = tmp_path / 'rollback_bad.json'
    tape_path.write_text(src.read_text())
    config = load_merged_config(profile='generic')
    args = SimpleNamespace(tape=str(tape_path), profile='generic', output=None)
    with pytest.raises(Exception):
        evaluate_tape(config, args)
