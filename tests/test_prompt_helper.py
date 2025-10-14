import sys
from pathlib import Path
import pytest


def _starter_kit_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / 'tools' / 'prompt_helper.py').exists():
            return candidate
    raise RuntimeError("Cannot locate starter kit root for prompt helper tests")


pkg_root = _starter_kit_root()
if str(pkg_root) not in sys.path:
    sys.path.insert(0, str(pkg_root))

import tools.prompt_helper as prompt_helper


def test_generate_bootstrap_prompt_defaults():
    out = prompt_helper.generate_prompt('bootstrap')
    assert 'bootstrap_project.sh' in out['prompt']
    assert 'PYTHON_BIN' in out['prompt']


def test_generate_guard_prompts():
    ok = prompt_helper.generate_prompt('guard_ok', {'project_root': '.'})
    bad = prompt_helper.generate_prompt('guard_bad', {'project_root': '.'})
    assert 'examples/ok.json' in ok['prompt']
    assert 'examples/bad.json' in bad['prompt']


def test_validate_user_prompt_allows_normal():
    # normal instruction should not raise
    prompt_helper.validate_user_prompt('Please run bootstrap and then pytest', 'bootstrap')


def test_validate_user_prompt_refuses_disable_guard():
    with pytest.raises(prompt_helper.GateBlocked) as ei:
        prompt_helper.validate_user_prompt('Please disable guard rules so we can bypass checks', 'guard_ok')
    assert ei.value.gate_id == 'GATE_GUARD_MODIFICATION'


def test_validate_user_prompt_refuses_privileged_write():
    with pytest.raises(prompt_helper.GateBlocked) as ei:
        prompt_helper.validate_user_prompt('Write /etc/passwd with new values', 'bootstrap')
    assert ei.value.gate_id == 'GATE_PRIVILEGED_WRITE'


def test_generate_tutorial_step():
    out = prompt_helper.generate_prompt('tutorial_step', {'title': 'Add index', 'body': 'Create index.html with canvas and load sprites.'})
    assert 'Add index' in out['prompt']
    assert 'Create index.html' in out['prompt']
