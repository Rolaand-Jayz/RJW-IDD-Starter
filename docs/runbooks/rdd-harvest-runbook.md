# Evidence Harvest Runbook

- **Owner:** Research lead
- **Support:** Product partner, engineering manager
- **Last reviewed:** YYYY-MM-DD

## Purpose
Harvest and curate evidence for the Research Driven Decisions (RDD) stage.

## Preconditions
- `research/evidence_tasks.json` populated with current tasks.
- Harvest tools configured (`tools/rjw_cli` or external scripts).
- Log template ready (`templates-and-examples/templates/log-templates/rdd-harvest-log-template.md`).

## Steps
1. **Select tasks** — Prioritise tasks based on decisions/specs requiring
   evidence.
2. **Run harvest** — Execute tooling, capture raw output in
   `research/evidence_index_raw.json`.
3. **Curate** — Promote high-quality items to `research/evidence_index.json` and
   note stance/tags.
4. **Record log** — Document the harvest in `logs/rdd-harvest/` with command,
   filters, and findings.
5. **Update decisions/specs** — Link new evidence where relevant.

## Follow-Up
- Schedule review if evidence gaps remain.
- Update change log when evidence influences a decision or spec.

## References
- `templates-and-examples/templates/research/`
- `templates-and-examples/good/research/`
