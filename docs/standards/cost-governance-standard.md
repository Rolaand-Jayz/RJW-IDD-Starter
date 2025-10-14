# Cost Governance Standard

- **Owner:** Finance steward
- **Applies to:** All production workloads
- **Last reviewed:** YYYY-MM-DD

## Purpose
Ensure product teams monitor and control cloud spend with traceable evidence in
change logs and cost logs.

## Requirements
1. Every change impacting spend includes a change log entry with projected and
   actual cost impacts.
2. Cost dashboards recorded in `logs/cost/` using the starter template.
3. Decisions and specs reference current cost evidence from
   `research/evidence_index.json`.

## Verification
- Guards validate presence of cost log entries for flagged changes.
- Monthly audit samples change log rows vs. billing exports.

## References
- `templates-and-examples/templates/log-templates/cost-log-template.md`
- `templates-and-examples/good/standards/code-review-standard.md`
