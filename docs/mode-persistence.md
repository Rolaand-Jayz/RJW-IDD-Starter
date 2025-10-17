# Mode Persistence

This document explains how the RJW-IDD starter persists operational mode across sessions and how the agent and local workflows should read and update the setting.

## Purpose

The repository can operate in multiple agent/prompt modes (Turbo, YOLO, Strict). Mode selection controls how the agent presents research, asks for approvals, and whether it implements features automatically. The mode is an operational preference and should be persisted for clarity and auditing.

## File: `.rjw-idd-mode`

- Location: repository root
- Contents: a single ASCII string with one of: `turbo`, `yolo`, `strict`
- Example:
  ```text
  turbo
  ```

## How to set mode manually

From the terminal:

```bash
# set turbo
echo "turbo" > .rjw-idd-mode
# set strict
echo "strict" > .rjw-idd-mode
```

If you want the change tracked in git:

```bash
git add .rjw-idd-mode
git commit -m "chore: set rjw-idd mode to turbo"
```

## How agents should read mode

Agents and automation should read the file at repo root. Behavior should be conservative if file missing or invalid. Example pseudo-code:

```python
try:
    mode = Path('.rjw-idd-mode').read_text().strip()
except FileNotFoundError:
    mode = 'strict'
if mode not in ('turbo','yolo','strict'):
    mode = 'strict'
```

Agents should always ask for user confirmation before performing destructive actions regardless of mode.

## Operational notes

- Mode is advisory and controls agent prompting and workflow cadence only.
- Security and CI guardrails are not bypassed automatically by mode. Explicit configuration toggles are required (e.g., `method/config/features.yml`).
- Mode changes should be committed when they represent a team-wide decision or when run as part of reproducible scripts.
