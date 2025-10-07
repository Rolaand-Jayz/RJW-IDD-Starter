#!/usr/bin/env python3
"""Helper tool to validate and format RJW-IDD commit messages.

This tool helps enforce commit message conventions defined in DOC-0021.

Usage:
    # Validate commit message
    python -m tools.git.commit_msg_helper --validate "feat(api): add endpoint"
    
    # Interactive commit message builder
    python -m tools.git.commit_msg_helper --interactive
    
    # Format change log entry
    python -m tools.git.commit_msg_helper --change-log
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


VALID_TYPES = {
    "feat": "New feature",
    "fix": "Bug fix",
    "docs": "Documentation only",
    "style": "Formatting, no code change",
    "refactor": "Code restructuring",
    "test": "Add/modify tests",
    "chore": "Maintenance",
    "perf": "Performance improvement",
    "ci": "CI/CD changes",
    "build": "Build system changes",
    "revert": "Revert previous commit",
    "hotfix": "Emergency production fix",
}

COMMIT_PATTERN = re.compile(
    r"^(?P<type>\w+)(\((?P<scope>[\w-]+)\))?(?P<breaking>!)?:\s*(?P<subject>.+)$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--validate", help="Validate commit message")
    group.add_argument(
        "--interactive", action="store_true", help="Interactive commit builder"
    )
    group.add_argument(
        "--change-log", action="store_true", help="Generate change log entry"
    )
    return parser.parse_args()


def validate_commit_message(message: str) -> tuple[bool, list[str]]:
    """Validate commit message against RJW-IDD standards.
    
    Returns (is_valid, errors)
    """
    errors = []
    lines = message.strip().split("\n")
    
    if not lines:
        return False, ["Empty commit message"]
    
    # Validate subject line
    subject = lines[0]
    
    # Check format
    match = COMMIT_PATTERN.match(subject)
    if not match:
        errors.append(
            f"Subject line doesn't match format: type(scope): subject\n"
            f"Got: {subject}"
        )
        return False, errors
    
    commit_type = match.group("type")
    scope = match.group("scope")
    breaking = match.group("breaking")
    commit_subject = match.group("subject")
    
    # Validate type
    if commit_type not in VALID_TYPES:
        errors.append(
            f"Invalid type '{commit_type}'. Must be one of: {', '.join(VALID_TYPES.keys())}"
        )
    
    # Check subject length
    if len(subject) > 72:
        errors.append(f"Subject line too long: {len(subject)} chars (max 72)")
    
    # Check subject format
    if commit_subject and commit_subject[0].isupper():
        errors.append("Subject should not start with capital letter")
    
    if commit_subject.endswith("."):
        errors.append("Subject should not end with period")
    
    # Check for body (optional but good practice)
    if len(lines) > 1 and lines[1].strip():
        errors.append("Second line must be blank (separate subject from body)")
    
    # Check for RJW-IDD footer (recommended)
    has_change_id = any("change-" in line for line in lines)
    has_impacted_ids = any("Impacted IDs:" in line for line in lines)
    
    if not has_change_id:
        errors.append("Missing RJW-IDD change ID (change-YYYYMMDD-##)")
    
    if not has_impacted_ids:
        errors.append("Missing 'Impacted IDs:' footer")
    
    return len(errors) == 0, errors


def interactive_builder() -> str:
    """Interactive commit message builder."""
    print("=== RJW-IDD Commit Message Builder ===\n")
    
    # Select type
    print("Commit type:")
    for i, (type_key, desc) in enumerate(VALID_TYPES.items(), 1):
        print(f"  {i:2}. {type_key:10} - {desc}")
    
    type_choice = input("\nEnter number (or type name): ").strip()
    if type_choice.isdigit():
        commit_type = list(VALID_TYPES.keys())[int(type_choice) - 1]
    else:
        commit_type = type_choice
    
    if commit_type not in VALID_TYPES:
        print(f"Invalid type. Using 'feat'")
        commit_type = "feat"
    
    # Scope
    scope = input("Scope (optional, e.g., 'api', 'auth', 'docs'): ").strip()
    
    # Breaking change
    breaking = input("Breaking change? (y/N): ").strip().lower() == "y"
    
    # Subject
    subject = input("Short description (imperative mood, no period): ").strip()
    while not subject or len(subject) > 50:
        if not subject:
            print("Subject is required")
        else:
            print(f"Subject too long ({len(subject)} chars). Keep under 50.")
        subject = input("Short description: ").strip()
    
    # Body (optional)
    print("\nLonger description (optional, press Enter twice when done):")
    body_lines = []
    while True:
        line = input()
        if not line and (not body_lines or not body_lines[-1]):
            break
        body_lines.append(line)
    
    # Remove trailing empty lines
    while body_lines and not body_lines[-1]:
        body_lines.pop()
    
    # RJW-IDD footer
    print("\n=== RJW-IDD Governance ===")
    
    # Change ID
    today = datetime.now().strftime("%Y%m%d")
    change_num = input(f"Change number for today ({today}): ").strip() or "01"
    change_id = f"change-{today}-{change_num.zfill(2)}"
    
    # Impacted IDs
    print("Impacted IDs (comma-separated, e.g., SPEC-0003, TEST-0007):")
    impacted_ids = input().strip()
    
    # Verification
    verification = input("Verification (e.g., 'pytest passes, guards pass'): ").strip()
    
    # Build message
    subject_line = f"{commit_type}"
    if scope:
        subject_line += f"({scope})"
    if breaking:
        subject_line += "!"
    subject_line += f": {subject}"
    
    message_parts = [subject_line]
    
    if body_lines:
        message_parts.append("")  # Blank line
        message_parts.extend(body_lines)
    
    # Add RJW-IDD footer
    message_parts.extend([
        "",
        f"{change_id}: {subject[:40]}",
    ])
    
    if impacted_ids:
        message_parts.append(f"Impacted IDs: {impacted_ids}")
    
    if verification:
        message_parts.append(f"Verification: {verification}")
    
    message = "\n".join(message_parts)
    
    print("\n=== Generated Commit Message ===")
    print(message)
    print("=" * 40)
    
    # Validate
    is_valid, errors = validate_commit_message(message)
    if not is_valid:
        print("\n⚠️  Validation warnings:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✅ Message is valid")
    
    return message


def generate_change_log_entry() -> str:
    """Generate change log entry."""
    print("=== Change Log Entry Generator ===\n")
    
    today = datetime.now().strftime("%Y%m%d")
    change_num = input(f"Change number for {today}: ").strip() or "01"
    change_id = f"change-{today}-{change_num.zfill(2)}"
    
    description = input("Brief description: ").strip()
    impacted_ids = input("Impacted IDs (comma-separated): ").strip()
    operator = input("Operator (role or name): ").strip() or "System"
    verification = input("Verification: ").strip() or "pytest passes, guards pass"
    
    # Generate table row
    entry = (
        f"| {change_id} | {datetime.now().strftime('%Y-%m-%d')} | "
        f"{description} | {impacted_ids} | {operator} | {verification} |"
    )
    
    print("\n=== Add this to docs/change-log.md ===")
    print(entry)
    
    return entry


def main() -> int:
    args = parse_args()
    
    if args.validate:
        is_valid, errors = validate_commit_message(args.validate)
        if is_valid:
            print("✅ Commit message is valid")
            return 0
        else:
            print("❌ Commit message validation failed:")
            for error in errors:
                print(f"  - {error}")
            return 1
    
    elif args.interactive:
        message = interactive_builder()
        
        # Ask if user wants to copy to clipboard
        use_msg = input("\nUse this message? (y/N): ").strip().lower() == "y"
        if use_msg:
            try:
                # Try to copy to clipboard
                import pyperclip
                pyperclip.copy(message)
                print("✅ Copied to clipboard!")
            except ImportError:
                print("\n💡 Install pyperclip to auto-copy: pip install pyperclip")
                print("\nCopy manually:")
                print(message)
        
        return 0
    
    elif args.change_log:
        generate_change_log_entry()
        return 0
    
    else:
        print("Use --validate, --interactive, or --change-log")
        return 1


if __name__ == "__main__":
    sys.exit(main())
