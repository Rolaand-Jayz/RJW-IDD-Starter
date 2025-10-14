import subprocess
from pathlib import Path


def _starter_kit_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / 'scripts' / 'prompts' / 'sync_agent_to_user.py').exists():
            return candidate
    raise RuntimeError("Cannot locate starter kit root for sync prompt tests")


ROOT = _starter_kit_root()
SCRIPT = ROOT / 'scripts' / 'prompts' / 'sync_agent_to_user.py'
MAPPING = ROOT / 'scripts' / 'prompts' / 'mapping.json'
PENDING = ROOT / 'scripts' / 'prompts' / 'PENDING_CHANGELOG_ROWS.txt'
USER_DIR = ROOT / 'docs' / 'prompts' / 'user'


def test_sync_creates_user_prompt_and_mapping(tmp_path):
    # Run the script
    subprocess.check_call([str(SCRIPT)])

    assert MAPPING.exists(), 'mapping.json should exist'
    assert PENDING.exists(), 'pending changelog suggestions should exist'
    # There should be at least one file in the user prompts directory
    user_files = list(USER_DIR.glob('*.md'))
    assert len(user_files) > 0, 'expected at least one generated user prompt'
