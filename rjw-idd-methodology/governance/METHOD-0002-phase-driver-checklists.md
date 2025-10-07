# METHOD-0002 — RJW-IDD Phase Driver Checklists

Use these checklists to force the same lifecycle run that originally created RJW-IDD. Every box must be checked before advancing to the next phase. Record completion in `docs/change-log.md` and append the relevant `DEC-####` entry each time you revisit the method.

## Phase 0 — Governance Setup
- [ ] `docs/decisions/` directory exists with sequential `DEC-####.md` records; new work starts by drafting a decision stub.
- [ ] `docs/change-log.md` initialised and ready to track `change-YYYYMMDD-##` entries.
- [ ] Roles confirmed (Evidence Lead, Spec Architect, Security Liaison, Implementation Wrangler).
- [ ] Stage audit log initialised (`logs/LOG-0001-stage-audits.md`) with audit tag `⟦audit-id:1⟧` reserved.

## Layer 1 — Discovery (Research + Specification)

### Research Loop
1. **Plan**
   - [ ] Draft `DEC-####` describing the harvest goal, sources, and date range.
   - [ ] Update `research/evidence_tasks.json` with focus areas.
2. **Harvest & Curate**
   - [ ] Run the automated harvester (`tools/rjw_idd_evidence_harvester.py`) capturing raw output.
   - [ ] Promote curated entries into `research/evidence_index.json` and log any gaps.
3. **Validate & Log**
   - [ ] Execute validators (`scripts/validate_evidence.py`, `scripts/validate_ids.py --paths research/evidence_index.json`).
   - [ ] Append Change Log row in `docs/change-log.md` detailing harvest, validator status, and outstanding gaps.
   - [ ] Complete `⟦audit-id:n⟧ <reflect/>` entry in stage audit log summarising coverage and open items.

### Specification Loop
1. **Prep**
   - [ ] Draft or update `DEC-####` capturing spec scope and trade-offs (e.g., provisional observability guidance).
   - [ ] Ensure requirement ledger template is ready.
2. **Author & Align**
   - [ ] Create/update specs across functional, quality, observability, security, integration, cost bands.
   - [ ] Refresh the requirement ledger linking each work item ID to evidence, specs, and planned tests.
   - [ ] Update living documentation reconciliation log with any outstanding doc gaps.
3. **Validate & Log**
   - [ ] Run ID validator on updated specs/ledger.
   - [ ] Record change in `docs/change-log.md` with linked `DEC-####` and validation results.
   - [ ] Capture `⟦audit-id:n⟧ <reflect/>` stage summary noting remaining assumptions and scheduled micro-harvests.

### Discovery Exit Gate (must be true)
- [ ] Curated evidence meets recency requirement; gaps tracked to owners and due dates.
- [ ] Requirement ledger, specs, and reconciliation log are aligned and reference the supporting evidence IDs.
- [ ] Scope freeze captured in latest `DEC-####`; Discovery exit signed by Evidence Lead and Spec Architect.

## Layer 2 — Execution
1. **Readiness**
   - [ ] Implementation decision (`DEC-####`) crafted describing scope of the sprint/run.
   - [ ] Tooling (test guard, consent manager, metric emitter) configured locally or ported to the new environment.
2. **Execution Loops**
   - [ ] For each change, write failing tests first; record guard output or log refusal until tests exist.
   - [ ] Update documentation (standards, runbooks, implementation notes) alongside code modifications.
   - [ ] Archive integration transcripts for cross-system changes under `artifacts/integration/...`.
   - [ ] Maintain consent records and metrics receipts when instrumentation is exercised.
3. **Validation & Log**
   - [ ] Run full test suite (`python -m unittest ...` or equivalent) and capture artefacts.
   - [ ] Update `docs/change-log.md` with guard/test results, consent receipt paths, and transcript locations.
   - [ ] Add `⟦audit-id:n⟧ <reflect/>` noting whether observability, security, and cost controls remain intact.
4. **Exit Gate (must be true)**
   - [ ] Tests, docs, and transcripts present for the change set.
   - [ ] Telemetry consent artefacts up to date.
   - [ ] Stage audit signed by Implementation Wrangler and Security Liaison.

## Continuous Governance (applies every cycle)
- [ ] Every new insight spawns a `DEC-####` log before being institutionalised.
- [ ] Stage audits kept current; every follow-up noted in `logs/LOG-0001-stage-audits.md` is tracked to closure.
- [ ] Change Log verification column always references tangible artefacts (validator outputs, logs, receipts).

Use this checklist pack as a gatekeeper. If any box stays unchecked, loop back, capture a new decision, or schedule additional Discovery work before progressing.
