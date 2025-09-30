# DOC-0004 — RDD Evidence Harvest Runbook

**Applies to:** Research-Driven Development operators. Cross-links `DEC-0002`, `DEC-0003`, `SPEC-0003`, `DOC-0001`.

## Preconditions
- Confirm access to required sources (Reddit, GitHub, Hacker News, Stack Overflow).
- Verify system clock is synced to UTC.
- Ensure Python 3.11+ available and `tools/rjw_idd_evidence_harvester.py` executable.
- Review `research/evidence_tasks.json`, refreshing queries or tags that are older than two weeks.

## Procedure
1. **Snapshot Tasks**
   - Optionally archive the current task set (`cp research/evidence_tasks.json research/archive/evidence_tasks_$(date -u +%Y%m%dT%H%M%SZ).json`).
   - Note the archive path in the stage audit entry.
2. **Smoke Run**
   - `python3 tools/rjw_idd_evidence_harvester.py --config research/evidence_tasks.json --output /tmp/rjw-idd-harvest-smoke.json --max-records 10`
   - Spot-check quotes and metadata for obvious regressions.
3. **Full Harvest**
   - `python3 tools/rjw_idd_evidence_harvester.py --config research/evidence_tasks.json --output research/evidence_index_raw.json --recency-days ${RJW_IDD_RECENCY:-28}`
   - Capture stdout/stderr to `logs/rdd-harvest/harvest_$(date -u +%Y%m%dT%H%M%SZ).log`.
4. **Validate**
   - `python3 scripts/validate_evidence.py --input research/evidence_index_raw.json --fail-on-warning`
   - Fix formatting or tagging issues before proceeding.
5. **Curate**
   - Review the raw file, promote accepted entries into `research/evidence_index.json` (one object per `EVD-####`).
   - Flag unresolved or low-signal items in `quality_flags` and record follow-ups in `docs/living-docs-reconciliation.md` if additional research is needed.
6. **Traceability Update**
   - Update ledgers (`artifacts/ledgers/requirement-ledger.csv`) so new evidence IDs map to the relevant requirements/specs.
   - Add a Change Log row referencing the harvest command, timestamp, record counts, and validation status.

## Exit Criteria
- `research/evidence_index.json` contains only curated, human-reviewed entries and passes validator checks.
- Raw log captured under `logs/rdd-harvest/` with operator initials.
- Change Log entry documents the harvest and any outstanding follow-up work.

## Troubleshooting
- **HTTP 429 / rate limits:** pause, rerun with `--max-records` lowered, or rotate credentials.
- **Invalid JSON:** inspect offending block noted by the validator; sanitize via `research/evidence_tasks.json` adjustments.
- **Recency mismatches:** confirm UTC clock and adjust `--recency-days` within governance-approved bounds if a single source warrants a shorter window.

## Post-Run Checklist
- Remove temporary files from `/tmp`.
- Notify the Spec Curator that the curated index is ready for SDD.
- Update `research/evidence_allowlist.txt` if any evidence needs to persist beyond the recency window.
