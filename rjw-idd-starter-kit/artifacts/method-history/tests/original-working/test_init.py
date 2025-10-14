"""
Unit tests for RJW Init command
"""

import sys
import tempfile
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.rjw_cli import init


def test_detect_runtime():
    """Test runtime detection"""
    runtime = init.detect_runtime()

    assert runtime['type'] == 'python'
    assert runtime['ok'] is True
    assert 'version' in runtime
    assert 'Python' in runtime['version']


def test_select_features_default():
    """Test feature selection with default preset"""
    features, mode, turbo = init.select_features('default', interactive=False)

    assert 'guard' in features
    assert 'init' in features
    assert 'prompts_version' in features
    assert 'yolo_mode' not in features
    assert mode == 'standard'
    assert turbo is False


def test_select_features_lite():
    """Test feature selection with lite preset"""
    features, mode, turbo = init.select_features('lite', interactive=False)

    assert 'guard' in features
    assert 'init' in features
    assert 'prompts_version' in features
    assert 'game_addin' not in features
    assert 'yolo_mode' not in features
    assert mode == 'standard'
    assert turbo is False


def test_select_features_game():
    """Test feature selection with game preset"""
    features, mode, turbo = init.select_features('game', interactive=False)

    assert 'guard' in features
    assert 'init' in features
    assert 'prompts_version' in features
    assert 'game_addin' in features
    assert 'yolo_mode' not in features
    assert mode == 'standard'
    assert turbo is False


def test_select_features_yolo():
    """Test feature selection with yolo preset"""
    features, mode, turbo = init.select_features('yolo', interactive=False)

    assert 'guard' in features
    assert 'init' in features
    assert 'prompts_version' in features
    assert 'yolo_mode' in features
    assert 'game_addin' not in features
    assert mode == 'yolo'
    assert turbo is False


def test_select_features_turbo_standard():
    """Test feature selection with turbo-standard preset"""
    features, mode, turbo = init.select_features('turbo-standard', interactive=False)

    assert 'guard' in features
    assert 'init' in features
    assert 'prompts_version' in features
    assert 'turbo_mode' in features
    assert 'yolo_mode' not in features
    assert mode == 'standard'
    assert turbo is True


def test_select_features_turbo_yolo():
    """Test feature selection with turbo-yolo preset"""
    features, mode, turbo = init.select_features('turbo-yolo', interactive=False)

    assert 'guard' in features
    assert 'init' in features
    assert 'prompts_version' in features
    assert 'yolo_mode' in features
    assert 'turbo_mode' in features
    assert 'game_addin' not in features
    assert mode == 'yolo'
    assert turbo is True


def test_write_decision_log():
    """Test decision log writing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        decisions = ["Decision 1", "Decision 2"]

        init.write_decision_log(project_dir, decisions)

        log_path = project_dir / 'DECISION_LOG.md'
        assert log_path.exists()

        content = log_path.read_text()
        assert "Decision 1" in content
        assert "Decision 2" in content
        assert "Rationale" in content
