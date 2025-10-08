---
title: Governance automation functional spec
id: SPEC-GOV-FUNC-0001
---

Acceptance criteria
- CI gating workflow runs pytest, flake8, bandit, pip-audit on PRs and fails the PR if any check fails.
- Smoke matrix exists and uploads artifacts.
- Doc-sync nightly job verifies README paths.
- Local helper `scripts/checks/run_checks.sh` executes the same checks locally.
- Release workflow produces zip + sha256 on tags.

Metrics
- CI pass rate on main: 100% for gating checks.
