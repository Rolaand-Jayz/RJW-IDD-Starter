# SPEC-0003 — Research-Driven Development (RDD) Harvest Template

**Linked Requirements:** Add evidence governance requirement IDs.  
**Status:** Template

## Purpose
Describe how RJW-IDD teams gather, curate, and validate external evidence to ground specifications and decisions.

## Scope
- Covers harvest cadence, data sources, curation workflow, and validation steps.
- Applies to all projects adopting RJW-IDD, regardless of domain.

## Expectations
1. Maintain `research/evidence_tasks.json` defining sources, queries, stances, and tags.
2. Run the evidence harvester at the agreed cadence (default weekly) and store raw output in `research/evidence_index_raw.json`.
3. Promote curated entries into `research/evidence_index.json`, tagging stance, relevance, and quality flags.
4. Track long-lived evidence in `research/evidence_allowlist.txt` when it must outlive the recency window.
5. Log harvest runs in Change Log entries that include command, record counts, and validation results; archive logs under `logs/rdd-harvest/`.

## Validation
- Use `scripts/validate_evidence.py` to enforce schema rules (quote length, tag presence, recency).
- Update requirement ledger entries with new evidence IDs once curated.
- Any evidence gaps discovered must be recorded in `docs/living-docs-reconciliation.md` or deferred via decision record.

## Follow-Up Guidance
- Tailor source list and stance tags to the project domain; document adjustments in `docs/runbooks/rdd-harvest-runbook.md`.
- Coordinate with SDD to ensure curated evidence is consumed promptly when populating specs and requirements.
