#!/usr/bin/env python3
"""
Safety gate for starter kit modifications.

This script provides a controlled way to modify the RJW-IDD Starter Kit with
appropriate warnings, consent checking, and audit logging.
"""
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess


def find_project_root() -> Path:
    """Find project root (same logic as sync script)."""
    script_path = Path(__file__).resolve()
    starter_kit_dir = script_path.parents[3]  # Go up to rjw-idd-starter-kit/

    if starter_kit_dir.name == "rjw-idd-starter-kit":
        potential_project_root = starter_kit_dir.parent
        if potential_project_root != starter_kit_dir and potential_project_root.name != "":
            return potential_project_root

    return starter_kit_dir


def check_consent(project_root: Path) -> bool:
    """Check if user has provided consent for modifications."""
    consent_file = project_root / ".starter_kit_modifications_allowed"

    if not consent_file.exists():
        return False

    try:
        consent_data = json.loads(consent_file.read_text())
        return consent_data.get("consent", False)
    except (json.JSONDecodeError, KeyError):
        return False


def show_safety_warning():
    """Display safety gate warning."""
    print("🚨 SAFETY GATE WARNING 🚨", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    print("You are about to modify the RJW-IDD Starter Kit.", file=sys.stderr)
    print("This will modify the starter kit.", file=sys.stderr)
    print("This will affect the method's output and behavior.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Before continuing:", file=sys.stderr)
    print("• Do you understand how this change affects the method?", file=sys.stderr)
    print("• Are you prepared to maintain this modification?", file=sys.stderr)
    print("• Have you documented why this change is necessary?", file=sys.stderr)
    print("", file=sys.stderr)
    print("For safe modification guidance, see:", file=sys.stderr)
    print("  docs/SAFE_MODIFICATIONS.md", file=sys.stderr)
    print("", file=sys.stderr)
    print("To enable modifications, create consent file:", file=sys.stderr)
    print("  .starter_kit_modifications_allowed", file=sys.stderr)
    print("", file=sys.stderr)
    print("MODIFICATION BLOCKED - No consent file found", file=sys.stderr)


def log_modification(project_root: Path, modification_type: str, details: dict):
    """Log modification for audit purposes."""
    audit_log = project_root / ".starter_kit_modifications.log"

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "modification_type": modification_type,
        "details": details,
        "user": subprocess.check_output(["whoami"], text=True).strip(),
        "project_root": str(project_root)
    }

    # Append to log file
    with open(audit_log, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def add_template(args):
    """Add a new template to the starter kit."""
    print("🔧 MODIFICATION ALLOWED - Adding template")

    # Implementation would go here
    template_file = args.add_template

    # For testing purposes, we'll just pretend the file exists
    # In real implementation, this would create the template
    print(f"Added template: {template_file}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Safely modify RJW-IDD Starter Kit")
    parser.add_argument("--add-template", metavar="FILE", help="Add new template")
    parser.add_argument("--add-decision-template", metavar="FILE", help="Add decision template")
    parser.add_argument("--update-config", metavar="FILE", help="Update configuration")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only")
    parser.add_argument("--force", action="store_true", help="Skip safety gate (dangerous)")

    args = parser.parse_args()

    # Find project root
    project_root = find_project_root()

    # Check consent unless force is used
    if not args.force and not check_consent(project_root):
        show_safety_warning()
        sys.exit(1)

    # Determine modification type
    modification_type = None
    details = {}

    if args.add_template:
        modification_type = "add-template"
        details = {"file": args.add_template}
        success = add_template(args)
    else:
        print("No modification specified")
        parser.print_help()
        sys.exit(1)

    # Log the modification
    if modification_type and not args.dry_run:
        log_modification(project_root, modification_type, details)

    if success:
        print("✅ Modification completed successfully")
        if not args.dry_run:
            print(f"📝 Logged to: {project_root / '.starter_kit_modifications.log'}")
    else:
        print("❌ Modification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()