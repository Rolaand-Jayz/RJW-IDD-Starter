import pathlib
from types import SimpleNamespace

import pytest

from config_loader import load_merged_config
from perf_budget_gate_3d import evaluate_metrics


def test_perf_gate_pass(tmp_path):
    metrics = tmp_path / 'metrics.json'
    metrics.write_text(pathlib.Path('addons/3d-game-core/docs/samples/perf_metrics_generic.json').read_text())
    config = load_merged_config(profile='generic')
    args = SimpleNamespace(metrics=str(metrics), profile='generic', variance=0.0, output=None)
    result = evaluate_metrics(config, args)
    assert result['failures'] == []


def test_perf_gate_fail(tmp_path):
    metrics = tmp_path / 'metrics.json'
    metrics.write_text(pathlib.Path('ci_samples/perf_metrics_violation.json').read_text())
    config = load_merged_config(profile='generic')
    args = SimpleNamespace(metrics=str(metrics), profile='generic', variance=0.0, output=None)
    with pytest.raises(Exception):
        evaluate_metrics(config, args)
