# Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD) Starter Kit

This starter kit packages the assets you need to run RJW-IDD in any codebase. It ships a reusable directory layout, method documents, scripts, and templates so new projects can copy the process without inheriting project-specific history.

## Quickstart
1. **Clone/Copy:** Place the contents of this kit in an empty repository and run `git init` if you are starting fresh.
2. **Set Up Project Environment:** 
   - Copy `templates/setup_project_env.sh` to your project root
   - Copy and customize dependency templates from `templates/` (see `templates/README.md`)
   - Run `./setup_project_env.sh` to create your project-specific environment
3. **Alternative Bootstrap:** Execute `scripts/setup/bootstrap_project.sh` for a basic setup (creates `.venv`, installs any existing dependencies, runs tests)
4. **Review Manual:** Read `docs/manual/starter-kit-manual.md` for role definitions, cadence guidance, and guard explanations.
5. **Enlist the Prompts:** Choose the right helper from `docs/prompts/` (start with `PROMPT-0001-starter-briefing.md`) so the AI agent can coach you through the workflow even without development experience.
6. **Commit Baseline:** Capture the imported kit as your first change (`docs/change-log.md`) and push to your remote so the GitHub Actions workflow can run.
7. **Customize:** Duplicate the SPEC templates you need, seed the ledgers with your first REQ-#### and TEST-#### entries, and update `research/evidence_tasks.json`.

> Need the bigger picture? The manual provides a full bring-up checklist and FAQ, while the sections below outline every asset shipped in the kit.

## Add-on Support
RJW-IDD supports optional add-ons that extend the methodology for specific domains:
- **3d-game-core** - 3D game development with determinism, replay, asset/perf gates
- **video-ai-enhancer** - Real-time video enhancement with quality, latency, storage gates

The bootstrap installer (`scripts/bootstrap/install.sh`) prompts for add-on selection. See `scripts/addons/README.md` and `docs/manual/starter-kit-manual.md` §9 for details.

## Feature Registry
Feature toggles live in `method/config/features.yml` (shared across the starter kit and the methodology pack).

| Toggle | Default | Purpose |
| --- | --- | --- |
| features.guard | true | Enables the rjw guard CLI entry point. |
| features.init | true | Enables the rjw init bootstrap workflow. |
| features.prompts_version | true | Publishes `rjw-idd-starter-kit/prompt-pack.json` metadata. |
| addons.3d_game_core.enabled | true | Declares the 3D game add-in active. |
| addons.video_ai_enhancer.enabled | false | Declares the video AI add-in active. |

Edit the YAML directly or use the helper scripts under `scripts/addons/`. After any change run the script `rjw-idd-starter-kit/scripts/config_enforce.py` (with Python) to confirm the declaration matches the filesystem (prompt pack, add-in directories, etc.), and capture the governance trail (change log, decision log, audits).

## Environment Philosophy
**The starter kit is a TEMPLATE, not a runnable project with fixed dependencies.**

Each project created from this kit should:
- Define its own dependencies based on what it actually does
- Create its own `.venv` with project-specific packages
- Use the templates in `templates/` as starting points

The starter kit provides:
- Template dependency files for different project types
- Setup scripts that adapt to your project's needs
- Add-on specific dependency suggestions
- Best practices for Python environment management

See `templates/README.md` for detailed guidance on setting up project environments.

## Prompt Workflow (No-Code Friendly)
- `PROMPT-0001-starter-briefing.md` — collect the goal, surface relevant specs, highlight open questions.
- `PROMPT-0002-implementation-coach.md` — plan the file-by-file, test-first implementation path.
- `PROMPT-0003-spec-translator.md` — turn plain-language requirements into SPEC updates and ledger links.
- `PROMPT-0004-test-navigator.md` — design the tests and explain what each should prove.
- `PROMPT-0005-doc-sync.md` — guide change-log, documentation, and decision updates.
- `PROMPT-0006-governance-audit.md` — walk through guardrails and PR preparation.
- `PROMPT-0007-change-log-author.md` — craft the change log row and stakeholder summary.
- `PROMPT-0008-merge-ready-checklist.md` — final safety check before request-for-review or merge.

Each prompt explains what context to gather and which artefacts to update so teammates without engineering experience can still drive the process.

## What’s Included
- **Method Pack (`../rjw-idd-methodology/`):** Core principles, role handbook, stage checklists, and decision template.
- **Docs & Standards (`docs/`):** Change log template, living-doc reconciliation log, runbooks, governance standards, and the new starter-kit manual (`docs/manual/starter-kit-manual.md`).
- **Prompt Suite (`docs/prompts/`):** Eight ready-to-run prompts that guide planning, spec updates, implementation, testing, documentation, governance checks, change logging, and merge readiness for non-developers.
- **Specs (`specs/`):** Template specifications for functional backbone, quality gates, evidence harvest, observability, security, integration, and cost governance.
- **Artifacts (`artifacts/`):** Blank requirement/test ledgers, integration transcript scaffold, and supporting templates.
- **Research (`research/`):** Starter evidence task configuration, empty indices, and allowlist instructions ready for harvesting.
- **Scripts & Tools (`scripts/`, `tools/`):** Evidence harvester, ID validators, cost dashboard helper, sandbox utilities, setup bootstrapper, and test-guard suite.
- **Logs (`logs/`):** Placeholder directories with README files describing required artefacts for audits.

Use this starter kit as the reusable part of the methodology; layer your product-specific specs, evidence, and code on top.

## Lifecycle Overview
RJW-IDD runs through three repeatable phases with continuous governance around them:

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

Cross-cutting governance (audits, cost reviews, security drills) runs continuously using the runbooks and scripts provided.

## Getting Started in a New Project
1. **Copy the Starter Kit** into your repository (or add as a subtree) and adjust paths as needed.
2. **Run the Bootstrap Script:** `scripts/setup/bootstrap_project.sh` ensures dependencies are installed and the guard suite passes locally.
3. **Set Up Ledgers:** Keep `artifacts/ledgers/requirement-ledger.csv` and `test-ledger.csv` under version control. Add entries as requirements/tests are defined.
4. **Establish Roles:** Assign Agent Conductor, Spec Curator, Doc Steward, and Governance Sentinel. Record expectations per `docs/manual/starter-kit-manual.md`.
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

## Setup Script Reference
- `scripts/setup/bootstrap_project.sh` creates `.venv`, installs `requirements-dev.txt`, runs `pytest`, and executes the governance test gate.
- Override the detected Python with `PYTHON_BIN`. If `origin/main` is not available yet, the script falls back to the repository’s first commit for diffing.
- Use the script after pulling future updates to ensure your environment stays in sync with the kit.

## Automated Guardrail
`scripts/ci/test_gate.sh` runs in CI to enforce the RJW-IDD lifecycle:

- Validates that code diffs include test updates, evidence remains fresh, ledgers match IDs, and the change log records every change.
- Rejects merges while living-document reconciliation entries stay open and requires a documentation/spec update alongside implementation work.
- Verifies that specification or research updates ship with matching ledger adjustments and a new decision record.

Wire this script into your preferred CI system so every pull request satisfies the RDD → SDD → Implementation gates.

## CI Integration
- GitHub Actions workflow `.github/workflows/test-gate.yml` ("RJW IDD Test Gate") runs on every pull request event using Python 3.11.
- The job installs developer dependencies via `pip install -r requirements-dev.txt`, executes the guard unit tests under `tests/guards/`, and then calls `scripts/ci/test_gate.sh` to exercise the full governance gate.
- Any failing guard or test breaks the pipeline, mirroring the local command sequence `pytest && bash scripts/ci/test_gate.sh`.
- Fetch depth is set to `0` so the gate compares the pull request against `origin/main`, matching the expectations baked into the guard scripts.

## Adapting the Starter Kit
- Update spec and runbook templates with your domain-specific requirements.
- Add additional tooling or prompts under `scripts/` and `docs/prompts/` as needed.
- Extend validators to enforce any extra governance rules your organisation requires.

By keeping this starter kit clean and evidence-neutral, you can import it into any project and immediately apply RJW-IDD without carrying over past product baggage. Populate the templates with your research, specs, and tests, then run the methodology end-to-end.
