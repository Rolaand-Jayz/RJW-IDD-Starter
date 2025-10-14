# Change Log — 2025-01-10

- **Summary:** Rolled out multiplayer matchmaking with feature toggles.
- **Related decision:** `templates-and-examples/good/decisions/decision-use-feature-toggles.md`
- **Related spec:** `templates-and-examples/good/specs/spec-ci-guardrails.md`
- **Verification:** `scripts/checks/run_checks.sh` (build #482) — pass
- **Evidence:** `research/evidence_index.json` entry `EVD-1032`

## Details
1. Enabled the toggle for 5% of users after smoke tests passed.
2. Captured the release steps in `logs/ci/2025-01-10-multiplayer.md`.
3. Updated the deployment runbook to document the new smoke checklist.

## Follow-Up
- Schedule a day-3 audit to evaluate matchmaking latency.
- Prepare a runbook addendum once tutorials ship.
