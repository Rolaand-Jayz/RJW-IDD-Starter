# Finance Variance Runbook

- **Owner:** Finance steward
- **Support:** Engineering manager, product partner
- **Last reviewed:** YYYY-MM-DD

## Purpose
Investigate cost spikes or budget variance detected by governance dashboards.

## Preconditions
- Alert raised by cost dashboard or change log entry flagged as high risk.
- Latest cost logs available in `logs/cost/` using the starter template.
- Change log entries for recent deployments reviewed.

## Steps
1. **Validate alert** — Confirm the variance is real (not a data delay).
2. **Identify scope** — List affected services, deployments, or toggles.
3. **Collect evidence** — Export billing data, guard outputs, and related
   change log rows.
4. **Decide next action** — Determine if rollback, scaling adjustment, or
   budgeting change is required. Record decision via
   `templates-and-examples/templates/decisions/`.
5. **Implement mitigation** — Coordinate with engineering to apply the fix.
6. **Monitor** — Track costs for 48 hours; add observations to cost logs.

## Recovery / Follow-Up
- If rollback needed, trigger the deployment runbook.
- Update relevant specs or standards to prevent recurrence.
- Capture stage audit entry referencing this investigation.

## Communication
- Share summary with finance and engineering leads.
- Update change log with permanent fix details.

## References
- `templates-and-examples/templates/log-templates/cost-log-template.md`
- `templates-and-examples/good/decisions/decision-use-feature-toggles.md`
