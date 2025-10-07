import json
import pathlib

import pytest

from config_loader import load_merged_config
from latency_guard_video import ConfigError, evaluate


def _write_trace(tmp_path: pathlib.Path, frames):
    payload = {
        "frames": frames,
        "total_frames": len(frames),
    }
    path = tmp_path / "latency.json"
    path.write_text(json.dumps(payload))
    return path


def test_latency_guard_pass(tmp_path: pathlib.Path):
    frames = [
        {"glass_to_glass_ms": 80 + i % 5, "pipeline_ms": 11.5 + (i % 2), "encode_ms": 11.2 + 0.4 * (i % 2), "queue_depth": 3}
        for i in range(120)
    ]
    trace_path = _write_trace(tmp_path, frames)
    config = load_merged_config(profile="live_stream")
    result = evaluate(config, trace_path, variance=0.05, output=None)
    assert result["failures"] == []


def test_latency_guard_failures(tmp_path: pathlib.Path):
    frames = [
        {"glass_to_glass_ms": 150, "pipeline_ms": 30, "encode_ms": 28, "queue_depth": 10}
        for _ in range(10)
    ]
    trace_path = _write_trace(tmp_path, frames)
    config = load_merged_config(profile="baseline")
    with pytest.raises(ConfigError):
        evaluate(config, trace_path, variance=0.0, output=None)
