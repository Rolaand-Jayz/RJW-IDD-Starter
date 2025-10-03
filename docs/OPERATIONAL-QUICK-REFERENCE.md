# RJW-IDD Operational Maturity Quick Reference

**Purpose:** Fast navigation guide to operational specs, runbooks, and procedures added in the gap closure work (2025-10-03).

## When You Need To...

### Plan a Deployment

1. **Specs:** `SPEC-0701-deployment-operations.md` (strategies, gates, rollback)
2. **Runbook:** `DOC-0020-deployment-runbook.md` (step-by-step procedures)
3. **Checklist:** Production Readiness Checklist in `SPEC-0701`
4. **Gate:** Phase 4 Gate 1 in `METHOD-0005`

### Respond to an Incident

1. **Runbook:** `DOC-0018-general-incident-runbook.md` (detection → resolution → postmortem)
2. **Severity:** Check SEV classification table (DOC-0018 Section: Incident Severity Classification)
3. **Escalation:** Follow escalation chain (DOC-0018 Section: Escalation Paths)
4. **Postmortem:** Use template in DOC-0018 Section: Phase 5

### Set Up Monitoring & Alerts

1. **Spec:** `SPEC-0801-slo-sli-framework.md` (SLIs, SLOs, alerting tiers)
2. **SLI Selection:** Section: SLI Categories (availability, latency, error rate, etc.)
3. **Alert Design:** Section: Alerting Strategy (Tier 1-4 with routing)
4. **Dashboards:** Section: Dashboard Requirements

### Handle a Rollback

1. **When:** Decision criteria in `DOC-0020` Section: When to Rollback
2. **How:** Execution steps in `DOC-0020` Section: Rollback Execution
3. **Post-Rollback:** Actions in `DOC-0020` Section: Post-Rollback Actions
4. **Postmortem:** Follow `DOC-0018` for incident documentation

### Manage Data & Backups

1. **Spec:** `SPEC-1001-data-governance.md` (retention, backup, migration, quality)
2. **Backup Strategy:** Section: Backup & Restore Procedures
3. **DR Drill:** Disaster Recovery procedures in Section: Restore Procedures
4. **Migration:** Planning and execution in Section: Data Migration
5. **Compliance:** Regulatory requirements in Section: Compliance & Regulatory

### Collect User Feedback

1. **Spec:** `SPEC-0901-user-feedback-loops.md` (research, usability, accessibility)
2. **Channels:** Section: Feedback Collection (in-app, surveys, support, community)
3. **Usability Testing:** Section: Usability Testing (methods, cadence, metrics)
4. **Accessibility:** Section: Accessibility (WCAG standards, checklist)
5. **Satisfaction:** Section: Satisfaction Metrics (NPS, CSAT, CES)

### Conduct Operational Reviews

1. **Framework:** `METHOD-0005-operations-production-support.md`
2. **Daily:** Section: Operational Cadence → Daily
3. **Weekly:** Section: Operational Cadence → Weekly
4. **Monthly:** Section: Operational Cadence → Monthly
5. **Quarterly:** Section: Operational Cadence → Quarterly

### Prepare for Production Launch

1. **Checklist:** Production Readiness Checklist in `SPEC-0701`
2. **Gate:** Gate 1: Production Readiness in `METHOD-0005`
3. **Sign-off:** Governance Sentinel + Service Owner + Security Liaison
4. **Audit:** Log in `logs/LOG-0001-stage-audits.md` with `⟦audit-id:n⟧ <production-ready/>`

### Manage Error Budget

1. **Policy:** Error Budget Policy in `SPEC-0801` Section: SLO Governance
2. **Calculation:** Formula in Section: SLO Definition Process
3. **Exhausted:** Actions in `METHOD-0005` Section: Reliability Sprint
4. **Tracking:** Monthly monitoring in operational metrics

### Set Up On-Call Rotation

1. **Structure:** On-Call Rotation in `SPEC-0801` Section: On-Call Rotation
2. **Responsibilities:** Section: On-Call Responsibilities
3. **Handoff:** Section: On-Call Handoff
4. **Contacts:** Maintain in `docs/status/oncall-status.md`

### Plan a Migration

1. **Spec:** `SPEC-1001` Section: Data Migration
2. **Planning:** Migration plan template in Section: Migration Planning
3. **Execution:** Step-by-step in Section: Migration Execution
4. **Verification:** Checklist in Section: Migration Verification
5. **Decision:** Document in `DEC-DATA-MIGRATION-####`

## Operational Role Quick Reference

### SRE / DevOps Lead

- **Owns:** Deployment, observability, incident response, capacity planning
- **Key Specs:** SPEC-0701, SPEC-0801, SPEC-1001
- **Key Runbooks:** DOC-0020 (deployment), DOC-0018 (incidents)
- **Artifacts:** Deployment logs, SLO reports, DR drill results

### Service Owner

- **Owns:** Business outcomes, user satisfaction, feature prioritization
- **Key Specs:** SPEC-0901 (user feedback), SPEC-0801 (SLOs)
- **Approvals:** Production deployments, hotfixes
- **Artifacts:** User satisfaction reports, roadmap

### On-Call Engineer

- **Owns:** First response, triage, mitigation
- **Key Runbook:** DOC-0018 (incident response)
- **Response Times:** 5 min (SEV-1), 15 min (SEV-2), 1 hour (SEV-3)
- **Artifacts:** Incident timelines, handoff notes

### Governance Sentinel

- **Owns:** Production readiness approval, quarterly audits
- **Key Specs:** METHOD-0005 (operational gates), all new specs
- **Audits:** Production readiness, post-launch stabilization, quarterly excellence
- **Artifacts:** Stage audit logs, gate approvals

## Common Workflows

### Emergency Hotfix Workflow

```
1. Identify critical issue (SEV-1 incident)
2. Create hotfix branch from main
3. Implement minimal fix + targeted tests
4. Get emergency approval (2 Governance Board members)
5. Deploy to staging (15 min soak)
6. Deploy to production (enhanced monitoring)
7. Merge to main within 24 hours
8. Postmortem within 24 hours
```

**References:** DOC-0020 Section: Emergency Hotfix Deployment

### Incident Response Workflow

```
1. Detect (alert or manual report)
2. Triage (assess severity, gather context)
3. Mitigate (rollback, reroute, or manual fix)
4. Resolve (deploy permanent fix)
5. Postmortem (blameless, actionable)
```

**References:** DOC-0018 (full workflow with timelines)

### SLO Violation Workflow

```
1. Alert fires (error budget consumption rate high)
2. On-call investigates and mitigates
3. Create incident record if SEV-2+
4. If error budget exhausted:
   - Declare reliability sprint
   - Freeze feature work
   - Prioritize SLO restoration
5. Postmortem and prevention plan
```

**References:** SPEC-0801 Section: Error Budget Policy, METHOD-0005 Section: Reliability Sprint

### User Feedback Prioritization Workflow

```
1. Collect feedback (multiple channels)
2. Weekly triage (categorize, assign severity)
3. Monthly aggregation (identify themes)
4. Impact vs. Effort mapping:
   - Quick Wins: High impact, low effort → immediate
   - Big Bets: High impact, high effort → next quarter
   - Fill-Ins: Low impact, low effort → backlog
   - Money Pit: Low impact, high effort → reject
5. Create requirements for prioritized items
6. Follow RJW-IDD: RDD → SDD → Implementation
```

**References:** SPEC-0901 Section: Feedback-Driven Development

## Integration with Existing RJW-IDD

### Evidence (RDD)

- User feedback qualifies as evidence (`EVD-UX-####`)
- Incident data informs reliability requirements
- SLO violations trigger focused research

### Specs (SDD)

- New operational specs follow same template structure
- Cross-link to existing functional/quality/security specs
- Requirements generated in ledgers (`REQ-0701+`, etc.)

### Implementation

- Test-first applies to operational tooling
- Living docs include runbooks and operational procedures
- Change Log tracks deployments, incidents, SLO changes

### Governance

- Operational gates extend phase checklist (METHOD-0002)
- New roles extend role handbook (METHOD-0003)
- Decision records capture operational choices

## File Paths Quick Reference

### Specs
```
rjw-idd-starter-kit/specs/
  ├── SPEC-0701-deployment-operations.md
  ├── SPEC-0801-slo-sli-framework.md
  ├── SPEC-0901-user-feedback-loops.md
  └── SPEC-1001-data-governance.md
```

### Runbooks
```
rjw-idd-starter-kit/docs/runbooks/
  ├── DOC-0018-general-incident-runbook.md
  └── DOC-0020-deployment-runbook.md
```

### Method Extensions
```
rjw-idd-methodology/operations/
  ├── METHOD-0004-ai-agent-workflows.md (existing)
  └── METHOD-0005-operations-production-support.md (new)
```

### Logs & Artifacts
```
rjw-idd-starter-kit/logs/
  ├── deployments/       # Deployment logs
  ├── slo/              # SLO compliance reports
  ├── operational-metrics/  # MTTR, MTBF, incident counts
  ├── satisfaction/     # NPS, CSAT, CES data
  ├── accessibility/    # a11y audit results
  └── data-lifecycle/   # Backup, restore, DR drill results
```

## Decision Namespaces

For documenting operational choices:

- **DEC-DEPLOY-####:** Deployment strategy decisions
- **DEC-SLO-####:** SLO targets, error budget policy
- **DEC-UX-####:** UX research, design, prioritization
- **DEC-DATA-####:** Data retention, migration, quality policies
- **DEC-INCIDENT-####:** Incident postmortems
- **DEC-RELIABILITY-####:** Reliability sprint outcomes
- **DEC-OPS-####:** General operational improvements

## Next Steps After Gap Closure

1. **Read:** Full specs for areas relevant to your role
2. **Customize:** Adapt templates for your environment (SLOs, retention policies, etc.)
3. **Assign:** Operational roles (SRE, Service Owner, On-Call)
4. **Implement:** Production readiness checklist items
5. **Audit:** Conduct Gate 1 (Production Readiness) review
6. **Iterate:** Update specs based on operational learnings

---

**For detailed procedures:** Consult the full spec/runbook documents.  
**For questions:** Reference `docs/GAP-CLOSURE-SUMMARY.md` for context on what was added and why.
