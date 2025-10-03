# DOC-0018 — General Incident Response Runbook

**Applies to:** All production and staging incidents (non-security).  
**Cross-links:** `SPEC-0801`, `SPEC-0701`, `DOC-0016` (security incidents).

## Purpose
Provide standard response procedures for production incidents including outages, performance degradations, data inconsistencies, and service disruptions.

## Scope
- Covers detection, triage, mitigation, resolution, and postmortem.
- Applies to all incidents except security-specific events (use `DOC-0016` for those).
- Integrates with SLO framework (`SPEC-0801`) and deployment operations (`SPEC-0701`).

## Incident Severity Classification

| Severity | Description | Response Time | Examples |
|----------|-------------|---------------|----------|
| **SEV-1** | Complete service outage; critical functionality unavailable; data loss risk | 5 minutes | API down, database unreachable, authentication broken |
| **SEV-2** | Major degradation; significant user impact; workaround available | 15 minutes | High error rates, severe latency, partial feature unavailable |
| **SEV-3** | Minor degradation; limited user impact; non-critical functionality | 1 hour | Slow dashboard, intermittent errors, cosmetic issues |
| **SEV-4** | Minimal impact; internal-only; no user-facing effect | Next business day | Dev environment issue, logging gaps, monitoring alerts |

## Incident Lifecycle

### Phase 1: Detection (0-5 minutes)

#### Automated Detection
- Alert fires from monitoring system (PagerDuty, CloudWatch, Datadog).
- SLO burn rate exceeds critical threshold (defined in `SPEC-0801`).
- Smoke tests fail after deployment.

#### Manual Detection
- Customer support report escalated to engineering.
- Internal user reports via Slack/Teams incident channel.
- Stakeholder observation during business operations.

#### Initial Actions
1. **Acknowledge alert** in on-call system to prevent duplicate pages.
2. **Check dashboards** (`logs/dashboards/` or monitoring URL) for anomaly confirmation.
3. **Declare incident** if impact confirmed:
   - Create incident record: `artifacts/integration/incident-<timestamp>/`
   - Announce in incident response channel: `#incident-response` (Slack/Teams).
   - Assign incident commander (IC): On-call primary or escalated owner.

### Phase 2: Triage (5-15 minutes)

#### Assess Severity
- Determine SEV level using classification table above.
- Confirm user impact scope (all users, specific region, single customer).
- Check for correlated alerts or recent changes.

#### Gather Context
- **Recent deployments:** Review `logs/deployments/` for changes in last 24 hours.
- **Change Log:** Check `docs/change-log.md` for recent updates.
- **Dependencies:** Verify third-party service status pages.
- **Metrics:** Compare current vs. baseline (CPU, memory, request rates, error rates).

#### Assemble Response Team
- **SEV-1:** IC + service owner + DBA (if data-related) + on-call secondary.
- **SEV-2:** IC + service owner + relevant specialist.
- **SEV-3/4:** IC or service owner handles solo; escalate if needed.

#### Document Timeline
Create `artifacts/integration/incident-<timestamp>/timeline.md`:
```markdown
# Incident Timeline: <INCIDENT-ID>

**Severity:** SEV-X  
**Detected:** 2025-10-03 14:23:00 UTC  
**Incident Commander:** ROLE-NAME

## Timeline
- 14:23 - Alert fired: API error rate 15% (threshold 1%)
- 14:25 - IC acknowledged; reviewing dashboards
- 14:27 - Recent deployment identified: v1.2.3 at 14:15
- ...
```

### Phase 3: Mitigation (15-60 minutes)

#### Immediate Actions (SEV-1/2)

**Option A: Rollback Deployment**
1. Execute rollback per `SPEC-0701` rollback procedures.
2. Verify service restoration via smoke tests.
3. Document rollback decision and timestamp in timeline.

**Option B: Traffic Rerouting**
1. Switch traffic to healthy region/cluster (if multi-region).
2. Scale up healthy instances to absorb load.
3. Isolate affected components without full rollback.

**Option C: Feature Flag Disable**
1. Disable recently enabled feature flags via `method/config/features.yml`.
2. Deploy config change via fast-track pipeline.
3. Confirm error rate returns to baseline.

**Option D: Manual Intervention**
1. Restart services, clear caches, or reset connections.
2. Manually correct data inconsistencies (with backup taken first).
3. Apply hotfix patch for critical bug.

#### Communication During Mitigation
- **Internal:** Update incident channel every 15 minutes with status.
- **External (SEV-1/2):** Post status page update within 30 minutes of detection.
- **Stakeholders:** Notify Governance Sentinel and service owner immediately for SEV-1.

### Phase 4: Resolution (30 minutes - hours)

#### Permanent Fix
- Deploy proper fix following standard process (`SPEC-0701`).
- Update tests to prevent regression (`TEST-INCIDENT-####`).
- Update runbooks if new mitigation discovered.

#### Verification
- Monitor SLIs for 1 hour post-resolution (SEV-1/2) or 15 minutes (SEV-3/4).
- Confirm error budget impact and remaining runway.
- Run full smoke test suite.
- Check for secondary effects or cascading issues.

#### Close Incident
- Update timeline with resolution timestamp and verification results.
- Mark incident resolved in tracking system.
- Schedule postmortem meeting (SEV-1/2 within 48 hours; SEV-3 within 1 week).

### Phase 5: Postmortem (24-72 hours post-resolution)

#### Postmortem Template
Create `docs/decisions/DEC-INCIDENT-<timestamp>.md`:

```markdown
# DEC-INCIDENT-20251003-1423 — API Outage Postmortem

**Incident Date:** 2025-10-03  
**Severity:** SEV-1  
**Duration:** 37 minutes  
**Impact:** 15,000 failed requests; 100% of users affected

## Problem Statement
API returned 500 errors due to database connection pool exhaustion after deployment v1.2.3.

## Timeline
- 14:15 - Deployment v1.2.3 completed
- 14:23 - First alert: API error rate 15%
- 14:27 - Rollback initiated
- 14:35 - Rollback completed
- 14:52 - Service fully restored and verified

## Root Cause
New feature introduced N+1 query pattern, exhausting connection pool under production load. 
Load testing in staging used synthetic dataset 10x smaller than production.

## Contributing Factors
- Staging environment not production-equivalent for database size.
- Load test scenarios did not include realistic query patterns.
- Connection pool size not validated against new query volume.

## What Went Well
- Fast detection (8 minutes from deployment to alert).
- Clear rollback procedure executed without issues.
- Communication timely and transparent.

## What Went Poorly
- Load testing missed critical scenario.
- No query performance regression tests.
- Database connection pool monitoring gaps.

## Action Items
1. [REQ-####] Add production-scale dataset to staging (owner: DBA, due: 2025-10-10).
2. [TEST-####] Implement query performance regression suite (owner: IC, due: 2025-10-15).
3. [DOC-####] Update load testing runbook with query pattern checklist (owner: QA, due: 2025-10-08).
4. [SPEC-####] Add connection pool monitoring to SLI framework (owner: SRE, due: 2025-10-12).
5. [CHANGE-####] Log postmortem in Change Log with action item tracking.

## Cross-Links
- `SPEC-0801` (SLO/SLI Framework)
- `SPEC-0701` (Deployment Operations)
- `change-20251003-02` (Change Log entry)

## Status Update — 2025-10-15
All action items completed; staging database scaled; query regression tests deployed.
```

#### Postmortem Principles
- **Blameless:** Focus on systems and processes, not individuals.
- **Actionable:** Every lesson learned must generate a concrete action item.
- **Traceable:** Link action items to requirements, tests, and specs.
- **Transparent:** Share postmortem with all stakeholders.

## Communication Templates

### Internal Status Update (Slack/Teams)
```
🚨 **INCIDENT UPDATE** - <INCIDENT-ID> - SEV-X

**Status:** [INVESTIGATING | MITIGATING | RESOLVED]
**Impact:** [Brief description of user impact]
**Current Actions:** [What's being done right now]
**Next Update:** [Timestamp]
**IC:** @username
```

### External Status Page (SEV-1/2)
```
[INVESTIGATING] API Service Degradation
Posted: 2025-10-03 14:30 UTC

We are investigating elevated error rates on our API service. 
Approximately 100% of requests are affected. 
Our team is actively working to resolve the issue.

Next update: 14:45 UTC
```

## Escalation Paths

### Technical Escalation
1. On-call primary → On-call secondary (if no response in 5 minutes)
2. On-call secondary → Service owner (if expertise needed)
3. Service owner → Engineering manager (if resources needed)
4. Engineering manager → VP Engineering (if executive decision required)

### Business Escalation
- **SEV-1:** Notify customer support, sales leadership, and executive team within 15 minutes.
- **SEV-2:** Notify customer support and product management within 30 minutes.
- **SEV-3/4:** No automatic escalation; handled within engineering.

## Incident Artifacts Checklist

After incident closure, ensure these exist:
- [ ] Timeline document: `artifacts/integration/incident-<timestamp>/timeline.md`
- [ ] Postmortem decision: `docs/decisions/DEC-INCIDENT-<timestamp>.md`
- [ ] Change Log entry: References incident, resolution, and action items
- [ ] Updated runbooks: If new mitigation procedure discovered
- [ ] Regression tests: Prevent same incident from recurring
- [ ] SLO impact: Error budget consumption calculated and logged

## Runbook Maintenance

- Review this runbook quarterly or after every SEV-1 incident.
- Update escalation contacts when on-call rotation changes.
- Add new incident patterns to "Common Scenarios" section (see below).
- Capture runbook changes in Change Log with decision reference.

## Common Scenarios

### Scenario: Database Connection Exhaustion
**Symptoms:** API timeouts, connection pool errors in logs  
**Quick Check:** `SHOW PROCESSLIST;` (MySQL) or `pg_stat_activity` (PostgreSQL)  
**Mitigation:** Restart application servers to reset pools; scale read replicas  
**Runbook:** `docs/runbooks/DOC-0021-database-troubleshooting.md`

### Scenario: Cache Stampede
**Symptoms:** Database load spike, slow response times after cache expiry  
**Quick Check:** Cache hit rate metrics, database query volume  
**Mitigation:** Pre-warm cache, enable cache locking, increase TTL temporarily  
**Runbook:** `docs/runbooks/DOC-0022-cache-management.md`

### Scenario: Third-Party API Failure
**Symptoms:** Specific feature broken, third-party timeout errors  
**Quick Check:** Third-party status page, dependency health dashboard  
**Mitigation:** Enable circuit breaker, activate fallback mode, notify users  
**Runbook:** `docs/runbooks/DOC-0023-dependency-failures.md`

### Scenario: Memory Leak
**Symptoms:** Gradual memory increase, eventual OOM crashes  
**Quick Check:** Memory usage graphs, heap dump analysis  
**Mitigation:** Restart affected services on rotation, deploy fix ASAP  
**Runbook:** `docs/runbooks/DOC-0024-memory-leak-response.md`

## Contacts

Maintain current contact list in `docs/status/oncall-status.md`:
- On-call primary: [Name, Phone, Slack handle]
- On-call secondary: [Name, Phone, Slack handle]
- Service owners: [Service → Owner mapping]
- Escalation chain: [Manager → Director → VP contacts]

## Operational Cadence

- **Daily:** Check incident backlog; assign SEV-3/4 tickets.
- **Weekly:** Review open incidents in standup; update timeline for long-running issues.
- **Monthly:** Analyze incident trends; identify systemic issues; propose DEC-#### improvements.
- **Quarterly:** Conduct incident response drill; update runbook based on learnings.

## Integration with Other Processes

- **Deployment:** Pre-deployment checklist includes rollback plan validation.
- **SLO Management:** Incidents consuming >10% error budget trigger reliability sprint.
- **Change Management:** Post-incident action items tracked in Change Log until closed.
- **Security:** Escalate to `DOC-0016` if security indicators present.

By following this runbook, teams can respond to incidents with consistency, minimize downtime, and continuously improve system reliability through blameless postmortems and actionable lessons learned.
