# Cost Tracking Log Template

This directory stores cost governance reports and variance analyses per SPEC-0602.

## Log Format

Cost reports should follow the naming convention:
```
cost-report-<period>-<date>.md
cost-variance-<incident-id>-<date>.md
```

### Example Filenames
```
cost-report-2025-W01-20250107.md
cost-report-2025-Q1-20250331.md
cost-variance-cv001-20250115.md
```

## Weekly Cost Report Template

```markdown
# Cost Report - Week <W##> <YYYY>

**Period:** YYYY-MM-DD to YYYY-MM-DD  
**Generated:** YYYY-MM-DDThhmmssZ  
**Operator:** Finance Lead / SRE

## Summary

| Metric | Forecast | Actual | Variance | % Change |
|--------|----------|--------|----------|----------|
| Total Spend | $X,XXX | $X,XXX | ±$XXX | ±X% |
| Cloud Infrastructure | $XXX | $XXX | ±$XX | ±X% |
| AI/LLM API Calls | $XXX | $XXX | ±$XX | ±X% |
| Data Storage | $XXX | $XXX | ±$XX | ±X% |
| CI/CD | $XX | $XX | ±$X | ±X% |

## Threshold Status

- 🟢 **Within Budget:** Total spend within 10% of forecast
- 🟡 **Warning:** Category exceeds 15% variance
- 🔴 **Critical:** Total spend exceeds 20% of forecast

**Current Status:** 🟢

## Cost Breakdown by Service

### Cloud Infrastructure
- Compute: $XXX (VM instances, container runtime)
- Networking: $XX (bandwidth, load balancers)
- Storage: $XX (block storage, object storage)

### AI/LLM Services
- GPT-4 API: $XXX (X,XXX tokens)
- Embedding API: $XX (X,XXX requests)
- Fine-tuning: $XX

### Data Services
- Database: $XX (PostgreSQL, Redis)
- Backup/Archive: $X (S3, Glacier)

## Trends & Analysis

- **Week-over-week:** +X% increase due to [reason]
- **Top cost driver:** [Service] contributing X% of total
- **Optimization opportunity:** [Specific action]

## Actions Required

- [ ] Review [specific service] usage with team
- [ ] Investigate spike in [cost category] on [date]
- [ ] Implement cost optimization per DEC-COST-XXX

## Cross-References

- Change Log: change-YYYYMMDD-##
- Decision: DEC-COST-XXX
- Spec: SPEC-0602-cost-governance.md
```

## Cost Variance Report Template

```markdown
# Cost Variance Report - CV###

**Date:** YYYY-MM-DD  
**Severity:** MINOR | MODERATE | SEVERE  
**Category:** [Infrastructure | AI Services | Data | Other]

## Variance Summary

| Item | Expected | Actual | Variance | Root Cause |
|------|----------|--------|----------|------------|
| [Service] | $XXX | $YYY | +$ZZZ (+X%) | [Brief explanation] |

## Impact Assessment

**Financial Impact:** $XXX over budget  
**Project Impact:** [Low | Medium | High]  
**Timeline Impact:** [None | Delays expected]

## Root Cause Analysis

1. **Immediate Trigger:** [What caused the spike]
2. **Contributing Factors:**
   - Factor 1: [Description]
   - Factor 2: [Description]
3. **Detection:** Discovered via [automated alert | manual review]

## Mitigation Actions

### Immediate (24 hours)
- [ ] Action 1: [Specific step]
- [ ] Action 2: [Specific step]

### Short-term (1 week)
- [ ] Action 3: [Implementation plan]
- [ ] Action 4: [Policy update]

### Long-term (1 month)
- [ ] Action 5: [Architectural change]
- [ ] Action 6: [Process improvement]

## Prevention Measures

- Update cost alerts: [New threshold]
- Add monitoring: [Specific metric]
- Document decision: DEC-COST-XXX
- Update forecast: [New baseline]

## Stakeholder Communication

**Notified:** YYYY-MM-DD  
**Recipients:** [Team Lead, Finance, Product Owner]  
**Status:** [Acknowledged | Action pending | Resolved]

## Lessons Learned

1. [Key takeaway]
2. [Process improvement]
3. [Tool/monitoring gap identified]

---

**Status:** OPEN | MONITORING | RESOLVED  
**Resolution Date:** YYYY-MM-DD (if applicable)  
**Final Variance:** $XXX (after mitigation)
```

## Retention Policy

- Weekly reports: Keep for 2 years
- Monthly/Quarterly summaries: Keep indefinitely
- Variance reports: Keep for 3 years (audit compliance)

## Integration

Cost logs should trigger:
- Change Log updates when thresholds exceeded
- Decision records for cost optimization strategies
- Spec updates when policies change (SPEC-0602)

---

**Dashboard:** Run `scripts/cost/run_weekly_dashboard.py` to generate reports  
**Finance Review:** Every Monday per METHOD-0005 operational cadence
