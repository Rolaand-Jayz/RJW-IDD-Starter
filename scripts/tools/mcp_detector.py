#!/usr/bin/env python3
"""Detect installed MCP/agent CLI tools and report if they appear operable.

This script is conservative: it only runs `--version` or `-v` where available
and does not perform network operations. Exit codes:
 0 - none found
 1 - found at least one operable CLI
 2 - error running checks
"""
import shutil
import subprocess
from pathlib import Path
import sys

KNOWN_CLIS = [
    'codacy_cli_analyze',
    'codacy_cli_install',
    'codacy',
    'apify',
    'apify-cli',
    'mcp-cli',
    'mcp',
    'upstash',
]

def try_version(cmd):
    try:
        completed = subprocess.run([cmd, '--version'], capture_output=True, text=True, check=False, timeout=5)
        if completed.returncode == 0:
            print(f'Found operable CLI: {cmd} --version -> {completed.stdout.strip() or completed.stderr.strip()}')
            return True
        # try -v
        completed = subprocess.run([cmd, '-v'], capture_output=True, text=True, check=False, timeout=5)
        if completed.returncode == 0:
            print(f'Found operable CLI: {cmd} -v -> {completed.stdout.strip() or completed.stderr.strip()}')
            return True
    except Exception:
        return False
    return False

def main():
    found = []
    for cli in KNOWN_CLIS:
        path = shutil.which(cli)
        if path:
            print(f'Executable on PATH: {cli} -> {path}')
            ok = try_version(cli)
            if ok:
                found.append((cli, path))
            else:
                print(f'CLI appears present but version check failed for: {cli}')
    if found:
        print('\nOperable MCP/agent CLIs detected:')
        for cli, path in found:
            print(' -', cli, '->', path)
        # guidance to agent: choose best match
        print('\nAgent guidance: consider using the first operable CLI detected to enhance research/code generation where applicable.')
        sys.exit(1)
    else:
        print('No operable MCP/agent CLIs detected on PATH.')
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('MCP detector error:', e)
        sys.exit(2)
