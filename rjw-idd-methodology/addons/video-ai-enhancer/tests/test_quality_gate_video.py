import json
import pathlib

import pytest

from config_loader import load_merged_config
from quality_gate_video import ConfigError, evaluate


@pytest.fixture
def metrics_payload() -> dict:
    return {
        "metrics": {
            "vmaf": 91.2,
            "psnr": 36.4,
            "ssim": 0.945,
            "lpips": 0.055,
        },
        "frame_consistency": {
            "jitter_ratio": 0.028,
            "frame_drop_pct": 0.4,
            "actual_fps": 62.0,
        },
        "artifact_budget": {
            "hallucination_pct": 0.3,
            "color_shift_delta_e": 1.2,
        },
    }


def _write_metrics(tmp_path: pathlib.Path, payload: dict) -> pathlib.Path:
    path = tmp_path / "metrics.json"
    path.write_text(json.dumps(payload))
    return path


def test_quality_gate_pass(tmp_path: pathlib.Path, metrics_payload: dict) -> None:
    metrics_path = _write_metrics(tmp_path, metrics_payload)
    config = load_merged_config(profile="live_stream")
    result = evaluate(config, metrics_path, variance=0.05, output=None)
    assert result["failures"] == []


def test_quality_gate_failure_detects_drift(tmp_path: pathlib.Path, metrics_payload: dict) -> None:
    metrics_payload["metrics"]["vmaf"] = 70.0
    metrics_payload["metrics"]["lpips"] = 0.2
    metrics_payload["frame_consistency"]["actual_fps"] = 20
    metrics_path = _write_metrics(tmp_path, metrics_payload)
    config = load_merged_config(profile="baseline")
    with pytest.raises(ConfigError):
        evaluate(config, metrics_path, variance=0.02, output=None)
