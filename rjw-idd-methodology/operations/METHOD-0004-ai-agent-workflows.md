# METHOD-0004 — RJW-IDD Workflow for AI Coding Agents

This playbook turns the RJW-IDD method pack into concrete steps for teams working with AI coding agents. Follow it to reproduce the evidence → spec → implementation loop captured in the scaffold.

## 0. Assign Roles
Record role owners in `rjw-idd-methodology/governance/METHOD-0003-role-handbook.md` and the active row in `docs/change-log.md`.

| Role | Responsibilities | Companion Artefacts |
|------|------------------|---------------------|
| Agent Conductor | Runs prompts, captures transcripts, executes guard scripts. | `docs/prompts/`, `artifacts/integration/transcript-archive/`, `logs/ci/` |
| Spec Curator | Maintains ledgers, specs, reconciliation log, and decision links. | `specs/`, `artifacts/ledgers/`, `docs/living-docs-reconciliation.md` |
| Doc Steward | Updates living documentation and verifies Change Log entries. | `docs/standards/DOC-0006`, `docs/runbooks/` |
| Governance Sentinel | Runs validators, records audits, blocks releases missing artefacts. | `scripts/validate_ids.py`, `logs/LOG-0001-stage-audits.md` |

## 1. Inputs Before Work
1. Copy `rjw-idd-starter-kit/docs/change-log.md` into your repository and open a new `change-YYYYMMDD-##` row.
2. Draft a `DEC-####` stub using `rjw-idd-methodology/templates/PROJECT-DEC-template.md` for the problem you are addressing.
3. Review `docs/living-docs-reconciliation.md`; log and assign any documentation gaps.
4. Schedule audit tags (`⟦audit-id:n⟧ <reflect/>`) and note them in the stage audit log.

## 2. Stage Workflows
### Layer 1 — Discovery
**Research Loop**
- Run `tools/rjw_idd_evidence_harvester.py` with `research/evidence_tasks.json`.
- Store logs under `logs/discovery-harvest/` (or your chosen path) and validate results with `scripts/validate_evidence.py`.
- Promote curated evidence into `research/evidence_index.json` via `scripts/promote_evidence.py`.
- Update requirement ledger entries with new evidence IDs and log the harvest in `docs/change-log.md`.

**Specification Loop**
- Author/update specs using templates in `specs/`, linking to relevant evidence and planned tests.
- Reserve requirement/test IDs in `artifacts/ledgers/*.csv` (or equivalent datasets).
- Resolve items in `docs/living-docs-reconciliation.md` before declaring Discovery complete.
- Capture outcomes in `docs/decisions/` and update `docs/change-log.md` with verification details.

### Layer 2 — Execution (TDD, Living Docs, Delivery)
- Use `docs/prompts/PROMPT-0001-omega-engineering.md` (or a customised prompt) to drive the agent.
- Enforce test-first and governance guards via `scripts/ci/test_gate.sh`, which now executes:
  - `tools/testing/red_green_guard.py` to require failing tests before implementation.
  - `scripts/validate_ids.py` to keep ledgers, specs, and change-log references aligned.
  - `scripts/validate_evidence.py` (triggered when research assets change) to ensure Execution sticks to fresh Discovery insight using a 14-day recency window.
  - `tools/testing/change_log_guard.py` to block merges that skip the change log.
  - `tools/testing/living_docs_guard.py` to reject outstanding living-doc gaps and demand documentation updates alongside implementation.
  - `tools/testing/governance_alignment_guard.py` to keep specification changes, ledgers, and decision logs synchronized.
- Capture full integration transcripts under `artifacts/integration/transcript-archive/`.
- Update living documentation according to `docs/standards/DOC-0006`.
- Append `⟦audit-id:n⟧ <reflect/>` when the layer exits.

## 3. Living Documentation Enforcement
- Before work: log gaps in `docs/living-docs-reconciliation.md`.
- During work: update docs, runbooks, and specs with new IDs and Change Log references.
- After work: validate docs/IDs, link outputs in `docs/change-log.md`, and ensure doc updates ship with code.

## 4. Integration Transcript Checklist
For every AI-assisted integration:
1. Scaffold a directory with `tools/integration/archive_scaffold.py <task-slug>`.
2. Complete `context.md` with scope, linked IDs, roles, and planned doc updates.
3. Log prompts/responses in `prompts.log`, store diffs in `diffs/`, and document verification steps in `verification.md`.
4. Reference the archive path in `docs/change-log.md` and in the living documentation.

## 5. Cost, Security, and Observability Controls
- Run cost dashboards using `scripts/cost/run_weekly_dashboard.py`; store outputs and finance sign-offs under `logs/cost/`.
- Execute sandbox drills with `scripts/sandbox/drill.py` and record artefacts under `logs/security/`.
- Maintain telemetry/observability artefacts per `specs/SPEC-0301` and `specs/SPEC-0401`, ensuring consent receipts and metric snapshots are logged.

## 6. Decision & Audit Hygiene
- Every major choice gets a `DEC-####` entry referencing evidence, specs, and follow-up actions.
- Governance Sentinel keeps `logs/LOG-0001-stage-audits.md` current with stage reflections.
- Quarterly reviews revisit evidence recency, cost thresholds, security posture, and method changes; record outcomes as new decisions or spec updates.

## 7. Companion Assets
- `METHOD-0001` — Core methodology principles.
- `METHOD-0002` — Phase checklists.
- `METHOD-0003` — Role handbook.
- `rjw-idd-methodology/templates/PROJECT-DEC-template.md` — Decision boilerplate.

Run this workflow step-by-step. When artefacts, prompts, or scripts evolve, update the corresponding specs/runbooks so the scaffold remains reusable for the next project.
