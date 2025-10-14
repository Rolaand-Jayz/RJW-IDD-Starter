# RDD Evidence Harvest Log Template

This directory stores logs from evidence harvesting runs per SPEC-0003.

## Log Format

Harvest logs should follow the naming convention:
```
harvest-<date>-<task-id>.log
harvest-summary-<date>.md
```

### Example Filenames
```
harvest-20250103-reddit-governance.log
harvest-20250103-github-security.log
harvest-summary-20250103.md
```

## Harvest Execution Log Template

```
=== RDD Evidence Harvest Log ===
Harvest ID: HRV-2025-001
Date: 2025-01-03T10:00:00Z
Operator: Evidence Lead
Task Configuration: research/evidence_tasks.json

--- Task 1: Reddit Search ---
Source: reddit
Subreddit: r/devops, r/programming
Query: "test-driven development failures"
Time Filter: month
Status: SUCCESS
Results: 15 items collected
Output: research/evidence_index_raw.json (entries 1-15)

--- Task 2: GitHub Issues ---
Source: github
Repository: microsoft/vscode
Query: "automation governance"
Status: SUCCESS
Results: 8 items collected
Output: research/evidence_index_raw.json (entries 16-23)

--- Task 3: Hacker News ---
Source: hn
Query: "security incident postmortem"
Tag: story
Status: SUCCESS
Results: 12 items collected
Output: research/evidence_index_raw.json (entries 24-35)

=== Summary ===
Total Tasks: 3
Successful: 3
Failed: 0
Total Evidence Items: 35
Raw Index Updated: research/evidence_index_raw.json
Curation Required: Yes (35 items awaiting review)

=== Validation ===
✓ Raw index JSON valid
✓ All items have required fields
✓ Timestamps within date range
✓ No duplicate URLs

=== Next Steps ===
1. Review raw evidence (scripts/promote_evidence.py)
2. Curate to evidence_index.json
3. Update requirement ledger with EVD-#### refs
4. Log harvest in Change Log (change-YYYYMMDD-##)

=== Issues/Warnings ===
[WARN] Rate limit approaching for GitHub API (15 requests remaining)
[INFO] 3 items flagged for manual review due to low relevance score
```

## Harvest Summary Template

```markdown
# Evidence Harvest Summary - <Date>

**Harvest ID:** HRV-YYYY-###  
**Date:** YYYY-MM-DD  
**Duration:** X minutes  
**Operator:** Evidence Lead

## Execution Results

| Source | Query | Items | Status |
|--------|-------|-------|--------|
| Reddit | "test failures" | 15 | ✓ Success |
| GitHub | "automation" | 8 | ✓ Success |
| HackerNews | "incidents" | 12 | ✓ Success |

**Total:** 35 items collected

## Coverage Analysis

### By Stance
- Pain Points: 18 items (51%)
- Solutions/Fixes: 12 items (34%)
- Risks/Warnings: 5 items (14%)

### By Topic
- Testing: 12 items
- Governance: 8 items
- Security: 7 items
- Operations: 5 items
- Cost: 3 items

## Quality Metrics

- **Recency:** All items within last 30 days ✓
- **Relevance:** 32/35 high relevance (91%)
- **Diversity:** 3 sources, 8 communities
- **Duplicates:** 2 items (removed)

## Curation Status

### Promoted to Curated Index
- 28 items promoted
- 5 items rejected (low relevance)
- 2 items flagged for follow-up

### Evidence IDs Assigned
- EVD-0201 through EVD-0228 (28 items)

## Insights & Gaps

### Key Findings
1. **Insight:** Practitioners struggle with test maintainability at scale
2. **Pattern:** Security postmortems reveal gaps in automated checks
3. **Trend:** Increasing focus on cost governance in AI projects

### Identified Gaps
- **Gap 1:** Insufficient evidence on deployment rollback strategies
  - **Action:** Schedule micro-harvest on "deployment failures"
  - **Owner:** Evidence Lead
  - **Due:** 2025-01-10

- **Gap 2:** Limited practitioner feedback on observability tools
  - **Action:** Add targeted Reddit search to next harvest
  - **Owner:** Spec Curator
  - **Due:** 2025-01-17

## Validation Results

```
$ python scripts/validate_evidence.py
✓ Raw index: 35 items, all valid
✓ Curated index: 28 items, all valid
✓ Freshness: 100% within 14-day cutoff
✓ Linkage: All curated items link to raw source
✓ No missing fields
```

## Change Log Entry

**Required Entry:**
```
| change-20250103-02 | 2025-01-03 | RDD harvest: 35 items collected, 28 curated; gaps identified in deployment/observability evidence | EVD-0201-0228 | Evidence Lead | harvest-summary-20250103.md |
```

## Follow-up Actions

- [ ] Update requirement ledger with new EVD refs
- [ ] Schedule gap-filling micro-harvest for deployments
- [ ] Review 5 rejected items in weekly meeting
- [ ] Update evidence_tasks.json based on gaps
- [ ] Document insights in DEC-RDD-### decision

## Audit Trail

- Raw log: `logs/rdd-harvest/harvest-20250103-full.log`
- Task config: `research/evidence_tasks.json` (commit a1b2c3d)
- Output indices: `research/evidence_index_raw.json`, `research/evidence_index.json`
- Change log: `templates-and-examples/templates/change-logs/CHANGELOG-template.md` (change-20250103-02)

---

**Status:** Complete ✓  
**Next Harvest:** 2025-01-10 (micro-harvest for deployment gaps)
```

## Retention Policy

- Harvest logs: Keep for 1 year
- Summary reports: Keep indefinitely
- Raw evidence: Archive after promotion but maintain index

## Cross-References

Every harvest should update:
- `research/evidence_index_raw.json` (all collected items)
- `research/evidence_index.json` (curated items only)
- `templates-and-examples/templates/change-logs/CHANGELOG-template.md` (new change row)
- `logs/LOG-0001-stage-audits.md` (audit reflection)

## Troubleshooting

Common issues:
- **Rate Limiting:** Reduce frequency or use API tokens
- **Low Relevance:** Refine query terms in evidence_tasks.json
- **Duplicates:** Harvester checks URLs, but manual review may be needed
- **Parsing Errors:** Update harvester for new source formats

---

**Tool:** `tools/rjw_idd_evidence_harvester.py`  
**Runbook:** `docs/runbooks/docs/runbooks/rdd-harvest-runbook.md`
