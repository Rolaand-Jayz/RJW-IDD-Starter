import json
import pathlib

import pytest

from config_loader import load_merged_config
from storage_capture_validator import ConfigError, evaluate


def _write_report(tmp_path: pathlib.Path, payload: dict) -> pathlib.Path:
    path = tmp_path / "storage.json"
    path.write_text(json.dumps(payload))
    return path


def test_storage_validator_pass(tmp_path: pathlib.Path):
    payload = {
        "segments": [
            {
                "path": f"segment_{i:04d}.mp4",
                "duration_s": 220,
                "average_bitrate_mbps": 48.0,
            }
            for i in range(6)
        ],
        "total_duration_s": 220 * 6,
        "total_storage_mb": 45 * 60 * 6 / 8,  # approx derived from bitrate
        "max_parallel_writers": 3,
    }
    report_path = _write_report(tmp_path, payload)
    config = load_merged_config(profile="mobile_edge")
    result = evaluate(config, report_path, variance=0.1, output=None)
    assert result["checked_segments"] == 6


def test_storage_validator_failure(tmp_path: pathlib.Path):
    payload = {
        "segments": [
            {
                "path": "oversized_segment.mp4",
                "duration_s": 600,
                "average_bitrate_mbps": 150.0,
            }
        ],
        "total_duration_s": 600,
        "total_storage_mb": 10_000,
        "max_parallel_writers": 8,
    }
    report_path = _write_report(tmp_path, payload)
    config = load_merged_config(profile="baseline")
    with pytest.raises(ConfigError):
        evaluate(config, report_path, variance=0.0, output=None)
