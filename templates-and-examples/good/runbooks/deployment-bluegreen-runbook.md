# Deployment Runbook — Blue/Green Swap

- **Owner:** Release captain  
- **Last reviewed:** 2025-01-10  
- **Related assets:** `templates-and-examples/templates/runbooks/runbook-template.md`,
  change log entry `CHANGELOG-2025-01-10.md`, spec `spec-ci-guardrails.md`

## 1. Preconditions
- Health checks from `templates-and-examples/templates/tests/test_template.py`
  pass in staging.
- Current production version is tagged in the change log.
- Rollback toggle listed in `artifacts/ledgers/toggles.csv`.

## 2. Steps
1. Announce release in `logs/ci/ci-log-template.md` derived log.
2. Deploy to the green environment via `scripts/deploy/bluegreen_swap.sh`.
3. Run smoke tests (`scripts/checks/run_checks.sh --smoke`).
4. Flip traffic using the load balancer helper script.
5. Monitor dashboards for 30 minutes; capture notes in `logs/ci/`.

## 3. Rollback
1. Restore traffic to blue immediately.
2. Re-run the smoke test to confirm recovery.
3. Create a decision draft referencing this runbook for follow-up analysis.

## 4. Communication
- Publish summary in the change log with links to evidence and test runs.
- Update the status board if the release remains dark for more than 2 hours.
