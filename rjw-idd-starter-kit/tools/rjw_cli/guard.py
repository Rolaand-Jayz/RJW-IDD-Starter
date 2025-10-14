"""
RJW Guard - Validate agent responses against safety policy

Exit codes:
  0 = pass
  2 = policy violation
  3 = schema error
  4 = I/O error
  5 = internal error
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Optional

import yaml

# Validation rules
FORBIDDEN_CAPABILITIES = [
    'subprocess.Popen',
    'os.system',
    'eval(',
    'exec(',
    '__import__',
]

ALLOWED_TOOLS = [
    'read_file',
    'write_file',
    'run_command',
    'search',
    'grep',
]

def _find_features_file() -> Optional[Path]:
    """Locate method/config/features.yml relative to current working dir."""
    cwd = Path.cwd()
    candidates = [
        cwd / 'method' / 'config' / 'features.yml',
        cwd / 'rjw-idd-starter-kit' / 'method' / 'config' / 'features.yml'
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _detect_ruleset(requested: Optional[str]) -> str:
    """Resolve effective guard ruleset based on features.yml when requested is auto/None."""
    if requested and requested != 'auto':
        return requested

    features_file = _find_features_file()
    if not features_file:
        return 'default'

    try:
        config = yaml.safe_load(features_file.read_text()) or {}
    except Exception:
        return 'default'

    features = config.get('features', {})
    mode = (config.get('mode') or {}).get('name') or ('yolo' if features.get('yolo_mode') else 'standard')
    turbo = bool((config.get('mode') or {}).get('turbo')) or bool(features.get('turbo_mode'))

    if turbo and mode == 'yolo':
        return 'turbo-yolo'
    if turbo:
        return 'turbo-standard'
    if mode == 'yolo':
        return 'yolo'
    return 'default'


def _turbo_ruleset(ruleset: str) -> bool:
    return ruleset in {'turbo-standard', 'turbo-yolo'}

REQUIRED_PROVENANCE_FIELDS = [
    'agent_id',
    'timestamp',
    'version',
]


def validate_schema(data: dict[str, Any]) -> tuple[bool, list[dict]]:
    """Validate basic JSON schema"""
    violations = []

    # Check for required top-level fields
    if not isinstance(data, dict):
        violations.append({
            'code': 'SCHEMA_INVALID_ROOT',
            'severity': 'error',
            'message': 'Root element must be an object',
            'path': '$',
            'remediation': 'Ensure the JSON output is a valid object with required fields'
        })
        return False, violations

    # Check for actions array if present
    if 'actions' in data and not isinstance(data['actions'], list):
        violations.append({
            'code': 'SCHEMA_INVALID_ACTIONS',
            'severity': 'error',
            'message': 'Actions field must be an array',
            'path': '$.actions',
            'remediation': 'Convert actions to an array of action objects'
        })

    return len(violations) == 0, violations


def check_forbidden_capabilities(data: dict[str, Any], ruleset: str) -> list[dict]:
    """Check for forbidden code patterns"""
    violations = []

    def scan_value(value: Any, path: str):
        if isinstance(value, str):
            for forbidden in FORBIDDEN_CAPABILITIES:
                if forbidden in value:
                    violations.append({
                        'code': 'CAPABILITY_FORBIDDEN',
                        'severity': 'error',
                        'message': f'Forbidden capability detected: {forbidden}',
                        'path': path,
                        'remediation': f'Remove {forbidden} or use safe alternatives'
                    })
        elif isinstance(value, dict):
            for k, v in value.items():
                scan_value(v, f"{path}.{k}")
        elif isinstance(value, list):
            for i, item in enumerate(value):
                scan_value(item, f"{path}[{i}]")

    scan_value(data, '$')
    return violations


def _is_absolute_path(path: str) -> bool:
    """Detect absolute paths across POSIX, Windows drive letters, and UNC shares."""
    if os.path.isabs(path):
        return True
    if path.startswith("\\\\") or path.startswith("//"):
        return True
    return bool(re.match(r"^[a-zA-Z]:[\\/]", path))


def _is_within_sandbox(path: str) -> bool:
    """True if path resides under the sandbox directory irrespective of platform separators."""
    normalized = path.replace("\\", "/").lower()
    if normalized.startswith("/sandbox/") or normalized.startswith("sandbox/"):
        return True
    return bool(re.match(r"^[a-z]:/sandbox/", normalized))


def check_file_operations(data: dict[str, Any], ruleset: str) -> list[dict]:
    """Check for unsafe file operations"""
    violations = []

    if 'actions' in data:
        for i, action in enumerate(data['actions']):
            if not isinstance(action, dict):
                continue

            # Check for unsigned file writes
            if action.get('type') == 'file_write':
                if not action.get('signed', False):
                    severity = 'warn' if _turbo_ruleset(ruleset) else 'error'
                    violations.append({
                        'code': 'DRIFT_UNSAFE_WRITE',
                        'severity': severity,
                        'message': 'Unsigned file write detected',
                        'path': f'$.actions[{i}]',
                        'remediation': 'Use sandboxed path or add signature verification'
                    })

                # Check for writes outside sandbox
                file_path = action.get('path', '')
                if _is_absolute_path(file_path) and not _is_within_sandbox(file_path):
                    violations.append({
                        'code': 'DRIFT_UNSAFE_PATH',
                        'severity': 'error',
                        'message': f'File write outside sandbox: {file_path}',
                        'path': f'$.actions[{i}]',
                        'remediation': 'Use paths within project sandbox directory'
                    })

    return violations


def check_network_operations(data: dict[str, Any], ruleset: str) -> list[dict]:
    """Check for unauthorized network calls"""
    violations = []

    if 'steps' in data or 'actions' in data:
        items = data.get('steps', []) + data.get('actions', [])
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                continue

            # Check for network calls
            if item.get('type') in ['http_request', 'api_call', 'fetch']:
                if not item.get('network_allowed', False):
                    severity = 'warn' if _turbo_ruleset(ruleset) else 'error'
                    violations.append({
                        'code': 'NET_CALL_FORBIDDEN',
                        'severity': severity,
                        'message': 'Network call without permission',
                        'path': f'$.steps[{i}]' if 'steps' in data else f'$.actions[{i}]',
                        'remediation': 'Rerun with --online or disable network access'
                    })

    return violations


def check_provenance(data: dict[str, Any], ruleset: str) -> list[dict]:
    """Check for required provenance fields"""
    violations = []

    if ruleset == 'strict':
        for field in REQUIRED_PROVENANCE_FIELDS:
            if field not in data:
                violations.append({
                    'code': 'PROVENANCE_MISSING',
                    'severity': 'warn',
                    'message': f'Missing provenance field: {field}',
                    'path': '$',
                    'remediation': f'Add {field} field to output'
                })

    return violations


def check_tool_allowlist(data: dict[str, Any], ruleset: str) -> list[dict]:
    """Check tool usage against allowlist"""
    violations = []

    if 'tools_used' in data:
        for tool in data['tools_used']:
            if tool not in ALLOWED_TOOLS:
                violations.append({
                    'code': 'TOOL_NOT_ALLOWED',
                    'severity': 'warn',
                    'message': f'Tool not in allowlist: {tool}',
                    'path': '$.tools_used',
                    'remediation': f'Use approved tools: {", ".join(ALLOWED_TOOLS)}'
                })

    return violations


def validate(data: dict[str, Any], ruleset: str = 'default') -> dict[str, Any]:
    """Run all validation checks"""
    start_time = time.time()
    violations = []

    # Schema validation
    schema_valid, schema_violations = validate_schema(data)
    violations.extend(schema_violations)

    if not schema_valid:
        # Don't continue if schema is invalid
        duration_ms = int((time.time() - start_time) * 1000)
        return {
            'passed': False,
            'violations': violations,
            'summary': {
                'errors': len([v for v in violations if v['severity'] == 'error']),
                'warnings': len([v for v in violations if v['severity'] == 'warn']),
                'ruleset': ruleset,
                'duration_ms': duration_ms
            }
        }

    # Run all checks
    violations.extend(check_forbidden_capabilities(data, ruleset))
    violations.extend(check_file_operations(data, ruleset))
    violations.extend(check_network_operations(data, ruleset))
    violations.extend(check_provenance(data, ruleset))
    violations.extend(check_tool_allowlist(data, ruleset))

    duration_ms = int((time.time() - start_time) * 1000)
    error_count = len([v for v in violations if v['severity'] == 'error'])
    warn_count = len([v for v in violations if v['severity'] == 'warn'])

    return {
        'passed': error_count == 0,
        'violations': violations,
        'summary': {
            'errors': error_count,
            'warnings': warn_count,
            'ruleset': ruleset,
            'duration_ms': duration_ms
        }
    }


def format_text_output(result: dict[str, Any], input_source: str) -> str:
    """Format validation result as human-readable text"""
    lines = []

    if result['passed']:
        lines.append(f"✔ Validation passed (ruleset={result['summary']['ruleset']}, "
                    f"errors={result['summary']['errors']}, warnings={result['summary']['warnings']})")
    else:
        lines.append(f"✖ Policy violations: {result['summary']['errors']} "
                    f"(ruleset={result['summary']['ruleset']})")

        for v in result['violations']:
            if v['severity'] == 'error':
                lines.append(f" • {v['code']} @ {v['path']} → {v['remediation']}")

    if result['summary']['warnings'] > 0 and not result['passed']:
        lines.append(f"\nWarnings: {result['summary']['warnings']}")
        for v in result['violations']:
            if v['severity'] == 'warn':
                lines.append(f" • {v['code']} @ {v['path']} → {v['remediation']}")

    return '\n'.join(lines)


def run(args) -> int:
    """Execute guard validation"""
    try:
        ruleset = _detect_ruleset(getattr(args, 'ruleset', None))

        # Read input
        if args.input == '-':
            input_source = 'stdin'
            try:
                data = json.load(sys.stdin)
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid JSON from stdin: {e}", file=sys.stderr)
                return 3  # Schema error
        else:
            input_source = args.input
            input_path = Path(args.input)

            if not input_path.exists():
                print(f"ERROR: File not found: {args.input}", file=sys.stderr)
                return 4  # I/O error

            try:
                with open(input_path) as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid JSON in {args.input}: {e}", file=sys.stderr)
                return 3  # Schema error
            except Exception as e:
                print(f"ERROR: Cannot read {args.input}: {e}", file=sys.stderr)
                return 4  # I/O error

        # Validate
        result = validate(data, ruleset)
        result['input_source'] = input_source

        # Output
        if args.format == 'json':
            print(json.dumps(result, indent=2))
        else:
            print(format_text_output(result, input_source))

        # Return appropriate exit code
        if result['passed']:
            return 0
        else:
            return 2  # Policy violation

    except Exception as e:
        print(f"ERROR: Internal error: {e}", file=sys.stderr)
        return 5  # Internal error
