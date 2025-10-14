"""Temporary runner to invoke rjw guard.run(args) with simple args.
"""
import sys
from types import SimpleNamespace

# Import the guard module from the starter kit path
import importlib.util
from pathlib import Path

guard_path = Path('rjw-idd-starter-kit/tools/rjw_cli/guard.py')
spec = importlib.util.spec_from_file_location('rjw_guard', guard_path)
if spec is None:
    raise ImportError(f"Could not load spec for module at {guard_path}")
module = importlib.util.module_from_spec(spec)
if spec.loader is None:
    raise ImportError(f"Could not load loader for module at {guard_path}")
spec.loader.exec_module(module)

def run_with_input(input_path, fmt='text', ruleset='default'):
    args = SimpleNamespace(input=input_path, format=fmt, ruleset=ruleset)
    rc = module.run(args)
    print(f"Exited with code: {rc}")
    return rc

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python tools/run_guard_test.py <path-to-json> [format]', file=sys.stderr)
        sys.exit(3)
    input_path = sys.argv[1]
    fmt = sys.argv[2] if len(sys.argv) > 2 else 'text'
    rc = run_with_input(input_path, fmt)
    sys.exit(rc)
