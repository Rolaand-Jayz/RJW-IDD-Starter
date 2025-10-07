# SPEC-0201 — Quality Gate Template

**Linked Requirements:** Populate per project.  
**Linked Decisions:** Reference the approval decision.  
**Status:** Template

## Purpose
Define the automated and manual gates that must pass before code merges under RJW-IDD. Focus on enforcing test-first behaviour, documentation parity, and validator coverage.

## Scope
- Applies to all repositories and services participating in the initiative.
- Covers pre-commit checks, CI pipelines, and pre-release verification.

## Gate Expectations
1. `scripts/ci/test_gate.sh` (or equivalent) fails if the diff lacks test updates or reserved test IDs.
2. Lint/format checks run in the same pipeline and block merges when violations exist.
3. `scripts/validate_ids.py` runs on changed files to ensure IDs and cross-links remain valid.
4. Living documentation updates are required; pipelines confirm modified artefacts reference the active `change_id`.
5. Change merges require recorded audit reflection (`⟦audit-id:n⟧ <reflect/>`) for the completed stage.

## Release Checklist
- Tests: unit, integration, or contract suites execute and report status to `logs/ci/`.
- Documentation lint passes and relevant docs updated.
- Change Log entry committed with verification artefacts.
- Security checks (dependency scanning, sandbox results) attached if scope touches sensitive areas.

## Implementation Notes
- Projects may extend this spec with language- or framework-specific guards.
- Document additional scripts or tooling in `docs/runbooks/` and link them here.

## Follow-Up Guidance
- Tailor thresholds (coverage %, performance budgets) to project context and capture specifics under “Gate Expectations”.
- Record any temporary gate adjustments in a decision log with expiry dates.
