# DOC-0011 — Rolaand Jayz Wayz: Intelligence Driven Development Overview

**Purpose:** Describe how to operationalise RJW-IDD using the reusable assets in this scaffold. This document is intentionally product-neutral so teams can adapt it to any codebase.

## Why RJW-IDD
- Evidence-first planning avoids vibe-driven coding and keeps specs grounded in practitioner signals.
- Traceability IDs (`EVD-####`, `REQ-####`, `SPEC-####`, `TEST-####`, `DOC-####`) create a verifiable audit trail across code, docs, and metrics.
- Test-first, living documentation, and integration transcripts ensure human and agent contributors stay aligned.
- Consent-aware telemetry and cost governance build stakeholder trust from the start.

## Roles
| Role | Responsibilities | Key Artefacts |
|------|------------------|---------------|
| Agent Conductor | Runs agent sessions, captures transcripts, executes guard scripts. | `artifacts/integration/transcript-archive/`, `logs/ci/` |
| Spec Curator | Maintains requirement/spec ledgers, ensures evidence coverage. | `specs/`, `artifacts/ledgers/` |
| Doc Steward | Keeps living documentation current and reconciles gaps. | `docs/standards/DOC-0006`, `docs/living-docs-reconciliation.md` |
| Governance Sentinel | Enforces gates, audits artefacts, records stage reflections. | `docs/change-log.md`, `logs/LOG-0001-stage-audits.md` |

## Lifecycle Summary
1. **Research-Driven Development (RDD)**
   - Configure evidence tasks, run the harvester, validate outputs, and promote curated evidence.
   - Log harvest runs in the Change Log and update requirement ledgers with new evidence IDs.
   - Store collection logs under `logs/rdd-harvest/`.

2. **Spec-Driven Development (SDD)**
   - Author specs using templates in `specs/`, linking to evidence and planned tests.
   - Reserve requirement/test IDs in the ledgers; capture decisions with `DEC-####` using the template.
   - Reconcile documentation gaps before closing the phase.

3. **Implementation Engines**
   - Enforce test-first using `scripts/ci/test_gate.sh` and `tools/testing/red_green_guard.py`.
   - Capture integration transcripts and verification artefacts for every cross-system change.
   - Update living documentation in the same change; attach guard/test/telemetry outputs to the Change Log.

4. **Continuous Governance**
   - Run security drills (`scripts/sandbox/drill.py`), consent checks, and cost dashboards (`scripts/cost/run_weekly_dashboard.py`) on defined cadences.
   - Append `⟦audit-id:n⟧ <reflect/>` entries to `logs/LOG-0001-stage-audits.md` after each gate.
   - Refresh evidence tasks and specs whenever audits surface new requirements.

## Tooling Checklist
- `tools/rjw_idd_evidence_harvester.py` — gather evidence.  
- `scripts/validate_evidence.py`, `scripts/promote_evidence.py` — curate and validate evidence.  
- `scripts/validate_ids.py` — enforce ID formats and cross-links.  
- `tools/testing/red_green_guard.py` — verify test coverage in diffs.  
- `tools/integration/archive_scaffold.py` — scaffold transcript folders.  
- `scripts/cost/run_weekly_dashboard.py` — produce spend dashboards and alerts.  
- `scripts/sandbox/reset.sh` / `scripts/sandbox/drill.py` — support sandbox hygiene.

## Documentation & Naming
- Follow `docs/standards/DOC-0013-naming-conventions.md` for files and IDs.
- All documentation updates must cross-link IDs and the active `change_id`.
- Use `docs/runbooks/` as living playbooks; customize them for your environment.

## Change Control & Audits
- Every material change logs a row in `docs/change-log.md` with verification artefacts.
- Decisions live in `docs/decisions/` using the DEC template.
- Governance Sentinel samples artefacts (ledgers, transcripts, cost logs) during audits and blocks release on missing items.

## Adapting to Your Project
1. Copy the scaffold and adjust directory paths as needed.
2. Populate evidence tasks, run initial harvest, and record decisions establishing scope.
3. Tailor spec and runbook templates with domain-specific requirements, metrics, and playbooks.
4. Integrate the provided scripts with your CI/CD pipeline; extend validators as required.
5. Train contributors on role expectations and review cadence using `../../rjw-idd-methodology/` documents.

Follow this guide to keep the methodology consistent while allowing teams to layer their own domain context, tooling, and governance policies on top.
