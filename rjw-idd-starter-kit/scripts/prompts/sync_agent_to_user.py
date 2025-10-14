#!/usr/bin/env python3
"""Sync agent prompt templates to human-friendly user prompt files.

Behavior:
- Read Markdown files under docs/prompts/agent/
- Validate YAML frontmatter contains required keys
- Extract the Prompt block or main content and write to docs/prompts/user/ as a simplified markdown file
- Write mapping to scripts/prompts/mapping.json
- Write a suggested changelog row to scripts/prompts/PENDING_CHANGELOG_ROWS.txt (not auto-applied)

This script intentionally does NOT modify repository CHANGELOGs or ledgers automatically to respect manual review.
"""
import re
import json
from pathlib import Path

def find_project_root() -> Path:
    """Find project root by looking for starter kit within project structure."""
    script_path = Path(__file__).resolve()

    # If we're in rjw-idd-starter-kit/scripts/prompts/sync_agent_to_user.py
    # Check if this is within a larger project (has parent that contains rjw-idd-starter-kit/)
    starter_kit_dir = script_path.parents[2]  # Go up to rjw-idd-starter-kit/

    if starter_kit_dir.name == "rjw-idd-starter-kit":
        # Check if starter kit is within a project (has a parent)
        potential_project_root = starter_kit_dir.parent
        if potential_project_root != starter_kit_dir and potential_project_root.name != "":
            # We're inside a project - use project root
            return potential_project_root

    # Otherwise, we're in standalone starter kit
    return starter_kit_dir


ROOT = find_project_root()
STARTER_KIT_DIR = ROOT / "rjw-idd-starter-kit" if (ROOT / "rjw-idd-starter-kit").exists() else ROOT
AGENT_DIR = STARTER_KIT_DIR / "docs" / "prompts" / "agent"

# Use isolation model: project artifacts go to /IDD-DOCS/, not starter kit
if STARTER_KIT_DIR != ROOT:
    # We're in a project - use /IDD-DOCS/
    USER_DIR = ROOT / "IDD-DOCS" / "prompts"
    SCRIPT_DIR = ROOT / "IDD-DOCS"
else:
    # We're in standalone starter kit - use original paths
    USER_DIR = ROOT / "docs" / "prompts" / "user"
    SCRIPT_DIR = ROOT / "scripts" / "prompts"

REQUIRED_KEYS = {"id", "version", "role", "visibility"}


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    # Very small YAML frontmatter parser for required keys
    m = re.match(r"---\n(.*?)\n---\n(.*)$", content, re.S)
    if not m:
        raise ValueError("Missing YAML frontmatter")
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if not line.strip():
            continue
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        fm[k.strip()] = v.strip()
    return fm, body


def extract_prompt_block(body: str) -> str:
    # Look for a fenced code block labeled Prompt or a block starting with 'Prompt:'
    m = re.search(r"```(?:.|\n)*?\n\s*Prompt:\n(.*?)```", body, re.S)
    if m:
        return m.group(1).strip()
    # fallback: return the whole body
    return body.strip()


def make_user_filename(fm: dict, src_path: Path) -> str:
    short = src_path.stem.lower().replace('prompt-agent-', '').replace('prompt-', '')
    safe_id = fm.get('id', 'UNKNOWN').replace(':', '-')
    return f"{safe_id}-{short}.md"


def main():
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    USER_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    mapping = {}
    pending_rows = []

    for p in sorted(AGENT_DIR.glob('*.md')):
        try:
            content = read_file(p)
            fm, body = parse_frontmatter(content)
            missing = REQUIRED_KEYS - set(fm.keys())
            if missing:
                print(f"Skipping {p.name}: missing keys {missing}")
                continue
            prompt_text = extract_prompt_block(body)
            user_fname = make_user_filename(fm, p)
            user_path = USER_DIR / user_fname
            # Create a minimal user-facing file
            user_content = f"# {fm.get('id')} — {fm.get('description', fm.get('id'))}\n\n" \
                + "Copy this into the assistant when you begin a new cycle.\n\n" \
                + "```\n" + prompt_text + "\n```\n"
            user_path.write_text(user_content, encoding='utf-8')
            mapping[str(p.relative_to(ROOT))] = str(user_path.relative_to(ROOT))
            # Suggest changelog row but do not edit changelog automatically
            pending_rows.append(f"{fm.get('id')}, {fm.get('version')}, added agent template -> {user_path}\n")
            print(f"Exported {p.name} -> {user_path}")
        except Exception as e:
            print(f"Error processing {p.name}: {e}")

    # Write mapping
    mapping_path = SCRIPT_DIR / 'prompt_mapping.json'
    mapping_path.write_text(json.dumps(mapping, indent=2), encoding='utf-8')

    # Write pending changelog suggestions
    pending_path = SCRIPT_DIR / 'PENDING_CHANGELOG_ROWS.txt'
    pending_path.write_text(''.join(pending_rows), encoding='utf-8')

    # Add isolation info
    if STARTER_KIT_DIR != ROOT:
        print(f"Using isolation model: project root = {ROOT}")
        print(f"Starter kit (pristine) = {STARTER_KIT_DIR}")
        print(f"Project artifacts = {SCRIPT_DIR}")

    print(f"Wrote mapping to {mapping_path}")
    print(f"Wrote pending changelog suggestions to {pending_path}")


if __name__ == '__main__':
    main()
