# General Incident Runbook

- **Owner:** Incident commander (on-call)
- **Support:** Feature expert, comms lead
- **Last reviewed:** YYYY-MM-DD

## Purpose
Provide a lightweight response plan for unclassified incidents affecting users
or infrastructure.

## Preconditions
- Incident ticket opened with timestamp and summary.
- Latest deployment/change log reviewed for recent changes.
- Logs and monitoring dashboards accessible.

## Steps
1. **Triage** — Identify blast radius, severity, and stakeholders.
2. **Stabilise** — Apply quick mitigations (feature toggle, rollback, traffic
   shaping) referencing relevant runbooks.
3. **Collect evidence** — Save logs, guard outputs, and user reports.
4. **Communicate** — Update status page / stakeholder channel every 30 minutes.
5. **Decision point** — Choose long-term fix path using decision template.

## Recovery
- Execute permanent fix (patch, configuration change, or rollback) and monitor
  until stable.
- Close the incident with a summary and next steps.

## Post-Incident
- Schedule a decision review and update specs/runbooks/standards as needed.
- Add change log entry referencing the incident resolution.
- Capture lessons learned in `logs/security/` or `logs/ci/` as applicable.

## References
- `templates-and-examples/templates/decisions/DEC-template.md`
- `templates-and-examples/templates/runbooks/runbook-template.md`
