# Git Workflow Runbook

- **Owner:** Engineering manager
- **Support:** Tech lead, release captain
- **Last reviewed:** YYYY-MM-DD

## Purpose
Describe the baseline Git workflow for teams using the RJW-IDD starter kit.

## Branch Strategy
- Default branch: `main`
- Feature branches: `feature/<slug>`
- Hotfix branches: `hotfix/<slug>`
- Keep branches small; align each with a single decision/spec update.

## Workflow
1. **Plan** — Capture decision and spec updates before creating the branch.
2. **Create branch** — `git checkout -b feature/<slug>`.
3. **Implement** — Follow the implementation coach prompt and run guards.
4. **Change log** — Update change log and logs before opening a PR.
5. **Pull request** — Link decisions/specs/runbooks/tests in the PR template.
6. **Merge** — Use fast-forward or squash depending on team policy.

## Rollback / Revert
- Use `git revert` for public history; update change log and logs accordingly.
- Reference the relevant runbook if a deployment rollback is required.

## Governance Hooks
- Guards run on every push (`scripts/checks/run_checks.sh`).
- Change log and evidence entries must be present before merge.
- Stage audit log updated after each release.

## References
- `templates-and-examples/templates/tests/test_template.py`
- `templates-and-examples/templates/change-logs/CHANGELOG-template.md`
- `templates-and-examples/templates/log-templates/`
