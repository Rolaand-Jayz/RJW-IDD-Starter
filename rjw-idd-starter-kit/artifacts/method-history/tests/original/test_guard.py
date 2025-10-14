"""
Unit tests for RJW Guard validation
"""

import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.rjw_cli import guard


def test_validate_good_input():
    """Test that valid input passes validation"""
    data = {
        "agent_id": "test",
        "timestamp": "2025-10-07T10:00:00Z",
        "version": "1.0",
        "actions": [
            {
                "type": "read_file",
                "path": "./README.md"
            }
        ]
    }

    result = guard.validate(data, ruleset='default')
    assert result['passed'] is True
    assert result['summary']['errors'] == 0


def test_validate_unsigned_write():
    """Test that unsigned file writes are caught"""
    data = {
        "actions": [
            {
                "type": "file_write",
                "path": "/etc/passwd",
                "signed": False
            }
        ]
    }

    result = guard.validate(data, ruleset='default')
    assert result['passed'] is False
    assert any(v['code'] == 'DRIFT_UNSAFE_WRITE' for v in result['violations'])


def test_validate_unsigned_write_turbo():
    """Unsigned writes in turbo mode should downgrade to warn but be reported"""
    data = {
        "actions": [
            {
                "type": "file_write",
                "path": "./tmp/output.txt",
                "signed": False
            }
        ]
    }

    result = guard.validate(data, ruleset='turbo-standard')
    assert result['passed'] is True
    violation = next(v for v in result['violations'] if v['code'] == 'DRIFT_UNSAFE_WRITE')
    assert violation['severity'] == 'warn'


def test_validate_network_call():
    """Test that unauthorized network calls are caught"""
    data = {
        "steps": [
            {
                "type": "http_request",
                "url": "https://example.com",
                "network_allowed": False
            }
        ]
    }

    result = guard.validate(data, ruleset='default')
    assert result['passed'] is False
    assert any(v['code'] == 'NET_CALL_FORBIDDEN' for v in result['violations'])


def test_validate_network_call_turbo_yolo():
    """Unauthorized network call in turbo yolo should become warning"""
    data = {
        "steps": [
            {
                "type": "http_request",
                "url": "https://example.com",
                "network_allowed": False
            }
        ],
        "actions": [
            {"type": "file_write", "path": "./log.txt", "signed": True}
        ]
    }

    result = guard.validate(data, ruleset='turbo-yolo')
    assert result['passed'] is True
    violation = next(v for v in result['violations'] if v['code'] == 'NET_CALL_FORBIDDEN')
    assert violation['severity'] == 'warn'


def test_validate_forbidden_capabilities():
    """Test that forbidden code patterns are caught"""
    data = {
        "code": "import os; os.system('rm -rf /')"
    }

    result = guard.validate(data, ruleset='default')
    assert result['passed'] is False
    assert any(v['code'] == 'CAPABILITY_FORBIDDEN' for v in result['violations'])


def test_validate_schema_error():
    """Test that invalid schema is caught"""
    data = "not a dict"

    result = guard.validate(data, ruleset='default')
    assert result['passed'] is False
    assert any(v['code'] == 'SCHEMA_INVALID_ROOT' for v in result['violations'])


def test_format_text_output_pass():
    """Test text formatting for passed validation"""
    result = {
        'passed': True,
        'violations': [],
        'summary': {
            'errors': 0,
            'warnings': 0,
            'ruleset': 'default',
            'duration_ms': 10
        }
    }

    output = guard.format_text_output(result, 'test.json')
    assert '✔' in output
    assert 'passed' in output.lower()


def test_format_text_output_fail():
    """Test text formatting for failed validation"""
    result = {
        'passed': False,
        'violations': [
            {
                'code': 'TEST_ERROR',
                'severity': 'error',
                'message': 'Test error',
                'path': '$.test',
                'remediation': 'Fix the test'
            }
        ],
        'summary': {
            'errors': 1,
            'warnings': 0,
            'ruleset': 'default',
            'duration_ms': 10
        }
    }

    output = guard.format_text_output(result, 'test.json')
    assert '✖' in output
    assert 'TEST_ERROR' in output


def test_provenance_strict():
    """Test that strict ruleset enforces provenance"""
    data = {
        "actions": []
    }

    result = guard.validate(data, ruleset='strict')
    # In strict mode, missing provenance should warn
    assert any(v['code'] == 'PROVENANCE_MISSING' for v in result['violations'])
