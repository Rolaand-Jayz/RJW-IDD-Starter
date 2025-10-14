# Security Incident Runbook

- **Owner:** Security incident commander
- **Support:** Platform engineer, communications lead
- **Last reviewed:** YYYY-MM-DD

## Purpose
Coordinate response to security or privacy incidents.

## Preconditions
- Incident declared and severity assessed.
- Access to monitoring, logs, and audit trails.
- Stage-audit log ready for updates.

## Steps
1. **Contain** — Disable compromised accounts, revoke tokens, or isolate
   services.
2. **Preserve evidence** — Snapshots of logs, alerts, and change log entries.
3. **Investigate** — Determine root cause, affected data, and blast radius.
4. **Eradicate** — Patch, rotate secrets, or roll back changes.
5. **Recover** — Restore normal operations; monitor for recurrence.

## Communication
- Notify stakeholders per response matrix (legal, product, support).
- Provide updates at least every 30 minutes until resolution.

## Post-Incident
- File decision and update specs/standards as needed.
- Record summary in `logs/security/` using the security log template.
- Update change log with remediation actions.

## References
- `templates-and-examples/templates/log-templates/security-log-template.md`
- `templates-and-examples/templates/decisions/DEC-template.md`
