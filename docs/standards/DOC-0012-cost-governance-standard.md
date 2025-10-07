# DOC-0012 — Cost Governance Standard

**Linked Requirement:** Fill with cost governance requirement IDs.  
**Linked Specification:** Reference `SPEC-0602` (or your customised version).

## Purpose
Monitor AI tooling spend, reconcile it with invoices, and trigger timely mitigations when budgets drift.

## Data Inputs
- Usage data (CSV/JSON) containing dates and spend metrics (e.g., `date, agent_minutes, cost_usd`).
- Finance or vendor invoices exported in CSV/JSON format.

## Procedure
1. Run your dashboard script (e.g., `scripts/cost/run_weekly_dashboard.py --usage-csv <usage.csv> --invoice-csv <invoice.csv> --monthly-ceiling <usd>`).
2. Store the generated report in `logs/cost/` with an ISO-8601 timestamp.
3. If the report status is `alert`, log the details in the Change Log, capture Finance approval (name, timestamp, mitigation plan), and create/update a decision entry if structural changes are needed.
4. Document mitigation steps and schedule a follow-up run to confirm the alert cleared.
5. Use the finance variance runbook (`docs/runbooks/DOC-0015-finance-variance-runbook.md`) for rehearsals and stakeholder coordination.

## Governance Expectations
- Define alert thresholds (default 80% of ceiling, configurable) and include them in living documentation.
- Require Finance Partner acknowledgement for every alert or mitigation rehearsal.
- Record dashboard snapshot paths and sign-off notes in Change Log verification columns.

## Audit Trail
- Retain dashboard outputs, invoice snapshots, and sign-off notes for at least 12 months.
- Governance Sentinel samples artefacts during audits to ensure alerts were acknowledged and resolved within agreed timelines.
- Any changes to dashboards, ceilings, or processes must be documented via decision records and spec updates.
