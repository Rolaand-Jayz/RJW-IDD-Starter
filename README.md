# Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD) Starter Kit

This starter kit packages the assets you need to run RJW-IDD in any codebase. It ships a reusable directory layout, method documents, scripts, and templates so new projects can copy the process without inheriting project-specific history.

## 🎉 New: Operational Maturity Framework (2025-10-03)

RJW-IDD now includes **complete operational guidance** from development through production:

- **SPEC-0701:** Deployment operations (blue-green, canary, rollback procedures)
- **SPEC-0801:** SLO/SLI framework (availability, latency, error budgets, alerting)
- **SPEC-0901:** User experience & feedback loops (usability, accessibility, satisfaction)
- **SPEC-1001:** Data governance (retention, backup/restore, migration, compliance)
- **DOC-0018:** General incident response runbook (SEV classification, postmortems)
- **DOC-0020:** Deployment runbook (step-by-step procedures)
- **METHOD-0005:** Operations & Production Support phase (maturity gates, SRE practices)

**Quick Start:** See `docs/OPERATIONAL-QUICK-REFERENCE.md` for navigation guide.  
**Full Context:** Read `docs/GAP-CLOSURE-SUMMARY.md` for complete gap analysis and remediation.

## Quickstart
1. **Clone/Copy:** Place the contents of this kit in an empty repository and run `git init` if starting fresh.
2. **Bootstrap Tooling:** Execute `scripts/setup/bootstrap_project.sh` (set `PYTHON_BIN` if you need a specific interpreter). The script builds `.venv`, installs `requirements-dev.txt`, runs `pytest`, and executes the governance test gate.
3. **Review Manual:** Read `docs/manual/starter-kit-manual.md` for role definitions, cadence guidance, and troubleshooting.
4. **Commit Baseline:** Record the imported kit in `docs/change-log.md` (`change-YYYYMMDD-01`) and push so the GitHub Actions workflow runs on pull requests.
5. **Customize:** Duplicate SPEC templates, seed the ledgers with initial REQ-####/TEST-#### entries, and update `research/evidence_tasks.json`.

> The manual covers the full bring-up checklist and FAQ. The sections below outline every asset shipped in the kit.

## What's Included
- **Method Pack (`../rjw-idd-methodology/`):** Core principles, role handbook, stage checklists, decision template, **and new operations phase (METHOD-0005)**.
- **Docs & Standards (`docs/`):** Change log template, decision templates, living-doc reconciliation log, runbooks, governance standards, **operational quick reference**, and a detailed starter-kit manual (`docs/manual/starter-kit-manual.md`).
- **Specs (`specs/`):** Template specifications for functional backbone, quality gates, evidence harvest, observability, security, integration, cost governance, **deployment operations (SPEC-0701), SLO framework (SPEC-0801), user feedback (SPEC-0901), and data governance (SPEC-1001)**.
- **Artifacts (`artifacts/`):** Blank ledgers, integration transcript scaffold, and supporting templates.
- **Research (`research/`):** Starter evidence task configuration, empty indices, and allowlist instructions ready for harvesting.
- **Scripts & Tools (`scripts/`, `tools/`):** Evidence harvester, ID validators, cost dashboard helper, sandbox utilities, setup bootstrapper, and test-guard helpers.
- **Logs (`logs/`):** Placeholder directories with README files describing required artefacts for audits **including deployment logs, SLO reports, operational metrics, satisfaction tracking, and DR drill results**.

Use this starter kit as the reusable part of the methodology; layer your product-specific specs, evidence, and code on top.

## Lifecycle Overview
RJW-IDD runs through **four** repeatable phases with continuous governance around them:

1. **Research-Driven Development (RDD)**
   - Configure evidence tasks (`research/evidence_tasks.json`).
   - Run the harvester (`tools/rjw_idd_evidence_harvester.py`) and validation script to populate raw and curated indices.
   - Update ledgers and document decisions (`DEC-####`) that arise from new evidence.

2. **Spec-Driven Development (SDD)**
   - Author or update specs using the templates in `specs/`.
   - Reserve requirement and test IDs in `artifacts/ledgers/*.csv`.
   - Log reconciliation items in `docs/living-docs-reconciliation.md` and resolve them before implementation begins.

3. **Implementation Engines (TDD / LDDD / IDD)**
   - Enforce test-first rules via `scripts/ci/test_gate.sh` and `tools/testing/red_green_guard.py`.
   - Capture integration transcripts in `artifacts/integration/transcript-archive/`.
   - Update living documentation using the standards in `docs/standards/` and record verification artefacts in the Change Log.

4. **Operations & Production Support (NEW)** 🎉
   - Deploy with blue-green/canary strategies and automated rollback (`SPEC-0701`, `DOC-0020`).
   - Monitor SLOs, manage error budgets, respond to incidents (`SPEC-0801`, `DOC-0018`).
   - Collect user feedback, conduct usability testing, ensure accessibility (`SPEC-0901`).
   - Manage data lifecycle, backups, migrations, and compliance (`SPEC-1001`).
   - Pass operational maturity gates: Production Readiness → Post-Launch Stabilization → Operational Excellence (`METHOD-0005`).

Cross-cutting governance (audits, cost reviews, security drills) runs continuously using the runbooks and scripts provided.

## Getting Started in a New Project
1. **Copy the Starter Kit** into your repository (or add as a subtree) and adjust paths as needed.
2. **Run the Bootstrap Script:** `scripts/setup/bootstrap_project.sh` ensures dependencies are installed and the guard suite passes locally.
3. **Set Up Ledgers:** Keep `artifacts/ledgers/requirement-ledger.csv` and `test-ledger.csv` under version control. Add entries as requirements/tests are defined.
4. **Establish Roles:** Assign Agent Conductor, Spec Curator, Doc Steward, and Governance Sentinel. Align on expectations in `docs/manual/starter-kit-manual.md`.
5. **Run Initial Harvest:** Configure `research/evidence_tasks.json`, execute the harvester, validate output, and log the run in the Change Log.
6. **Author Specs:** Clone the spec templates, fill in project-specific details, and link to evidence/requirements/tests.
7. **Adopt Runbooks:** Tailor documents in `docs/runbooks/` for your environment (e.g., sandbox reset commands, finance workflows).
8. **Update Naming Conventions:** Follow `docs/standards/DOC-0013-naming-conventions.md` to keep artefacts consistent.

## Key Templates & Scripts
- `docs/change-log.md` – table ready for change entries.
- `docs/living-docs-reconciliation.md` – log for documentation gaps.
- `docs/runbooks/*.md` – operational playbooks (harvest, test-first, security, finance).
- `specs/*.md` – editable specifications covering major governance areas.
- `scripts/validate_ids.py` – validates ledgers, change log, and ID references.
- `scripts/promote_evidence.py` / `scripts/validate_evidence.py` – curation helpers.
- `tools/rjw_idd_evidence_harvester.py` – fetches evidence from public sources.
- `tools/testing/red_green_guard.py` – ensures tests accompany each change.
- `tools/testing/change_log_guard.py` – blocks merges that omit a change-log update.
- `tools/testing/living_docs_guard.py` – fails when living-doc gaps remain open.
- `tools/testing/governance_alignment_guard.py` – keeps specs, ledgers, and decisions in lockstep.
- `tools/integration/archive_scaffold.py` – scaffolds integration transcript directories.

## Change Control
- Every meaningful change creates a row in `docs/change-log.md` with impacted IDs and verification proof.
- Decisions are recorded using `../rjw-idd-methodology/templates/PROJECT-DEC-template.md` and stored in `docs/decisions/`.
- Audit reflections append `⟦audit-id:n⟧ <reflect/>` entries to stage summaries (see `logs/LOG-0001-stage-audits.md`).

## Automated Guardrail
`scripts/ci/test_gate.sh` runs in CI to enforce the RJW-IDD lifecycle:

- Validates that code diffs include test updates, evidence remains fresh, ledgers match IDs, and the change log records every change.
- Rejects merges while living-document reconciliation entries stay open and requires a documentation/spec update alongside implementation work.
- Verifies that specification or research updates ship with matching ledger adjustments and a new decision record.

Wire this script into your preferred CI system so every pull request satisfies the RDD → SDD → Implementation gates.

## Setup Script Reference
- `scripts/setup/bootstrap_project.sh` creates `.venv`, installs `requirements-dev.txt`, runs `pytest`, and executes the governance test gate.
- Override the detected Python with `PYTHON_BIN`. If `origin/main` is not available yet, the script falls back to the repository’s first commit for diffing.
- Use the script after pulling future updates to ensure your environment stays in sync with the kit.

## Adapting the Starter Kit
- Update spec and runbook templates with your domain-specific requirements.
- Add additional tooling or prompts under `scripts/` and `docs/prompts/` as needed.
- Extend validators to enforce any extra governance rules your organisation requires.

By keeping this starter kit clean and evidence-neutral, you can import it into any project and immediately apply RJW-IDD without carrying over past product baggage. Populate the templates with your research, specs, and tests, then run the methodology end-to-end.

## Add-ins

- [3D Game Core](addons/3d-game-core/README.md) — opt-in 3D harnesses, specs, and gates.
- [Video AI Enhancer](addons/video-ai-enhancer/README.md) — opt-in real-time video enhancement, latency, and storage governance.
