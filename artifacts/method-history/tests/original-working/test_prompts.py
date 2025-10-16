"""
Unit tests for RJW Prompts command
"""

import json
import sys
import tempfile
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.rjw_cli import prompts


def test_load_prompt_pack_missing():
    """Test loading prompt pack when file doesn't exist"""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        pack = prompts.load_prompt_pack(project_dir)

        assert pack['name'] == 'rjw-prompt-pack'
        assert pack['version'] == '0.0.0'


def test_load_prompt_pack_valid():
    """Test loading valid prompt pack"""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        pack_path = project_dir / 'prompt-pack.json'

        pack_data = {
            'name': 'test-pack',
            'version': '0.1.0-alpha',
            'checksum': 'sha256-test',
            'last_updated': '2025-10-07',
            'channels': ['core'],
            'compat': {'min_cli': '>=1.0.0'}
        }

        with open(pack_path, 'w') as f:
            json.dump(pack_data, f)

        pack = prompts.load_prompt_pack(project_dir)

        assert pack['name'] == 'test-pack'
        assert pack['version'] == '1.2.3'


def test_check_for_updates_offline():
    """Test update check in offline mode"""
    update_info = prompts.check_for_updates(online=False)

    assert update_info['available'] is False
    assert 'offline' in update_info['message'].lower()


def test_check_for_updates_online():
    """Test update check in online mode"""
    update_info = prompts.check_for_updates(online=True)

    assert 'available' in update_info
    # Note: This is a placeholder implementation
