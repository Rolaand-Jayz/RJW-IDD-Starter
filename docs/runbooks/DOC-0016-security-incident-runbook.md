# DOC-0016 — Security Incident Runbook

**Linked Requirement:** Document the applicable security requirement ID.  
**Linked Specification:** Reference the security/telemetry spec (e.g., `SPEC-05xx`).

## Context
RJW-IDD requires sandbox-first execution, explicit telemetry consent, and multi-source validation. This runbook provides the standard response steps when a security signal fires during agent-assisted development.

## Detection
- **Automated alerts:** Observability stack marks `security_signal=true` (sandbox escape, consent violation, suspicious dependency, etc.).
- **Manual reports:** Team members log concerns via the Change Log and escalate to the Governance Sentinel.
- **Evidence capture:** Preserve logs, prompts, transcripts, and diffs under `artifacts/integration/transcript-archive/<incident-id>/` with redactions as required.

## Immediate Actions
1. **Isolate environment:** run `scripts/sandbox/reset.sh` (or equivalent) using the active sandbox identifiers to revoke tokens and tear down namespaces. Record the command and timestamp in the incident transcript.
2. **Freeze deployments:** Implementation Wrangler halts merges touching the affected scope until regression tests pass.
3. **Notify stakeholders:** Security Liaison informs the governance board, recording the notification in the Change Log with links to captured artefacts.

## Investigation
- Correlate observability metrics with agent transcripts to trace the triggering action.
- Validate hypotheses with multiple independent evidence sources before declaring a root cause.
- Draft a `DEC-####` covering options, chosen remediation, and any required follow-up work.

## Remediation
- Apply fixes in sandbox branches; create or update requirements/specs/tests as needed.
- Re-run consent/telemetry checks and sandbox drills using the relevant automation (for example `scripts/sandbox/drill.py`). Store outputs under `logs/security/`.
- Update living documentation to reflect the new safeguards.

## Communication
- Publish an incident summary (context, timeline, evidence, remediation, next review date) within 24 hours.
- Reference the transcript archive directory, Change Log entry, and decision ID.

## Post-Incident Follow-Up
1. Update specs and requirements to encode lessons learned.
2. Coordinate with RDD for fresh evidence if the incident reveals new threat patterns.
3. Schedule refresher training or drills for affected teams.
4. Add an entry to `logs/LOG-0001-stage-audits.md` noting the incident and remediation status.

## Operator Checklist
- [ ] Environment isolation complete
- [ ] Governance notified and Change Log updated
- [ ] Evidence stored with incident ID
- [ ] Decision record created/updated
- [ ] Regression tests and drills re-run
- [ ] Specs/docs refreshed
- [ ] Audit entry prepared

## Review Cadence
Assign an owner (e.g., Security & Privacy Liaison) and set a next review date in the requirement ledger to ensure the runbook stays current.
