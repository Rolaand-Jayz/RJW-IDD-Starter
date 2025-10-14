# Naming Conventions Standard

- **Owner:** Engineering manager
- **Applies to:** Code, documents, logs
- **Last reviewed:** YYYY-MM-DD

## Purpose
Keep names consistent so novices can find the right files quickly.

## Requirements
1. Use kebab-case for Markdown documents (e.g., `deployment-runbook.md`).
2. Use snake_case for Python modules and tests.
3. Slugs instead of numeric IDs (e.g., `decision-use-feature-toggles.md`).
4. Change log identifiers follow `change-YYYYMMDD-topic` pattern.

## Verification
- Code review checklist includes naming compliance.
- Guards flag unexpected naming patterns when possible.

## References
- `templates-and-examples/templates/`
- `docs/runbooks/git-workflow-runbook.md`
