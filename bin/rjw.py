#!/usr/bin/env python3
"""
RJW-IDD CLI - Intelligence Driven Development Command-Line Interface

Agent Pledge (Hardened):
- Fail safe, not silent. If unsure, stop with clear, actionable error and remediation.
- No destructive defaults. Use beginner-friendly, reversible settings with explicit confirmations.
- Deterministic CLI behavior. Same inputs => same outputs; stable exit codes and JSON schemas.
- Respect config sources of truth. Auto-correct drift only when explicitly enabled.
- Transparent changes. Emit decision log for assumptions, defaults, and migrations.
- No hidden network calls during guard or init unless documented and approved by --online flag.
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.rjw_cli import guard, init, prompts


def main():
    parser = argparse.ArgumentParser(
        description="RJW-IDD CLI - Intelligence Driven Development toolkit",
        epilog="Agent Pledge: Fail safe, not silent. Deterministic behavior. Transparent changes."
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Guard command
    guard_parser = subparsers.add_parser('guard', help='Validate agent responses against safety policy')
    guard_parser.add_argument('input', help='Input file path or "-" for stdin')
    guard_parser.add_argument('--format', choices=['json', 'text'], default='text',
                             help='Output format (default: text)')
    guard_parser.add_argument(
        '--ruleset',
        choices=['auto', 'default', 'strict', 'yolo', 'turbo-standard', 'turbo-yolo'],
        default='auto',
        help='Validation ruleset (default: auto)'
    )
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new RJW-IDD project')
    init_parser.add_argument(
        '--preset',
        choices=['default', 'standard', 'lite', 'game', 'yolo', 'turbo-standard', 'turbo-yolo'],
        default='standard',
        help='Project preset (default: standard)'
    )
    init_parser.add_argument('--noninteractive', action='store_true',
                            help='Run without interactive prompts')
    
    # Prompts command
    prompts_parser = subparsers.add_parser('prompts', help='Manage prompt packs')
    prompts_parser.add_argument('--version', action='store_true',
                               help='Show prompt pack version')
    prompts_parser.add_argument('--update', action='store_true',
                               help='Update to latest prompt pack')
    prompts_parser.add_argument('--online', action='store_true',
                               help='Check for updates online')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'guard':
            return guard.run(args)
        elif args.command == 'init':
            return init.run(args)
        elif args.command == 'prompts':
            return prompts.run(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("Remediation: Check logs and ensure all dependencies are installed.", file=sys.stderr)
        return 5  # Internal error


if __name__ == '__main__':
    sys.exit(main())
