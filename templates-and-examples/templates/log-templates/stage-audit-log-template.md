# Stage Audit Log Template

Start a new log entry at each RJW-IDD gate. Keep entries concise and link back to
supporting artifacts (evidence, decisions, specs, runbooks, change logs).

```
⟦audit-id:<number>⟧ <reflect/> <stage name>
- Evidence harvested: <count> entries promoted to `research/evidence_index.json`
- Outstanding risks: <short summary with links>
- Follow-up: <owner> / <due date>
```

Example:

```
⟦audit-id:12⟧ <reflect/> Build readiness
- Evidence harvested: 6 curated items; gaps in cost coverage.
- Outstanding risks: Need deployment rehearsal (see runbooks/deployment-bluegreen-runbook.md).
- Follow-up: Casey — schedule rehearsal before 2025-01-12.
```
