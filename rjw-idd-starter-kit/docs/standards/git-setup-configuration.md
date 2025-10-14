# Git Setup & Configuration Standard

- **Owner:** Engineering manager
- **Applies to:** All contributors
- **Last reviewed:** YYYY-MM-DD

## Purpose
Define minimum Git configuration for reproducible, auditable work.

## Requirements
1. Use user.name and user.email matching company directory.
2. Enable commit signing or verified commits.
3. Configure `pull.rebase=false` unless team policy states otherwise.
4. Install pre-commit hooks from `scripts/setup/install_hooks.sh` (if present).

## Verification
- Guards check signed commits on protected branches.
- Quarterly audit verifies config via onboarding checklist.

## References
- `templates-and-examples/templates/runbooks/runbook-template.md`
- `docs/runbooks/git-workflow-runbook.md`
