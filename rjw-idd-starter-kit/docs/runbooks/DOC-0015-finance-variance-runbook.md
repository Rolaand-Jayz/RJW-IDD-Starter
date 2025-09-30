# DOC-0015 — Finance Variance Rehearsal Playbook

**Linked Requirement:** Document in requirement ledger when adopting.  
**Linked Specification:** Reference your cost governance spec ID (e.g., `SPEC-06xx`).

## Purpose
Ensure Finance and Engineering rehearse the variance response anytime the weekly cost dashboard flags anomalies so corrective actions are documented and repeatable.

## Trigger
- `scripts/cost/run_weekly_dashboard.py` (or equivalent) exits with `status: "alert"`.
- Scheduled rehearsal (at least once per sprint) even if production data is clean.

## Procedure
1. Capture the dashboard output path reported by the script (for example `logs/cost/cost_dashboard_<timestamp>.json`).
2. For each alert, assign an owner and summarise the suspected driver.
3. Meet with Finance, confirm the variance, and log acknowledgement in a sign-off note under `logs/cost/` (recommended format: Markdown with name, UTC timestamp, and mitigation plan).
4. Create or update a `DEC-####` if mitigation requires budget changes, model swaps, or policy updates. Link to the dashboard snapshot and sign-off note.
5. Update the Change Log verification column for the active change with references to the dashboard snapshot and sign-off artefact.
6. Schedule a follow-up run (within seven days) to confirm the mitigation cleared the alert; append the outcome to the same sign-off note.

## Artefacts
- Dashboard snapshot JSON under `logs/cost/`.
- Finance sign-off note (Markdown or CSV) in `logs/cost/`.
- Change Log row covering the alert, mitigation, and verification.

## Contacts
- Finance Partner (as defined in your charter).
- Implementation Wrangler (ensures mitigations land in code/tests/docs).

## Rehearsal Cadence
Simulate an alert at least once per sprint using synthetic cost data if no real alert has fired. Store the synthetic inputs alongside the rehearsal notes for auditability.
