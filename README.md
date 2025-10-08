# Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD) Starter Kit

> Built so a person with **zero coding background** can partner with an AI helper, stay on the RJW-IDD rails, and ship real work.

This starter kit gives you the directory layout, scripts, documents, and—most importantly—the copy-paste prompts that make RJW-IDD approachable for everyone. Bring it into any codebase to get a consistent, traceable workflow.

## Who This Kit Supports
- **Level zero developers** who need plain-language guidance, one prompt at a time.
- **Teams** who want a shared prompt library and predictable governance steps.
- **AI helpers** that must confirm plans, follow RJW-IDD, and leave a clear paper trail.

## Quickstart (Human Friendly)
1. **Open the Novice Guide:** `rjw-idd-starter-kit/docs/manual/novice-quickstart.md` walks you through the seven RJW-IDD stages.
2. **Load the Core Prompts:** Keep `rjw-idd-starter-kit/docs/prompts/PROMPT-CORE-novice-flow.md` open and copy the prompts in order. Use `project-prompts.md` to store any new prompts the helper gives you.
3. **Share the Guardrails:** Send anything from `rjw-idd-starter-kit/docs/prompts/AGENT-GUARDRAILS.md` to remind your helper to stay in plain language and confirm each step. Point them to the glossary (`docs/prompts/GLOSSARY.md`) if a new term appears.
4. **Use the Example Conversations:** `rjw-idd-starter-kit/docs/prompts/EXAMPLE-CONVERSATIONS.md` shows how to ask the helper to run commands like the bootstrap script, review diffs, or write the change log.
5. **Let the Helper Run Setup:** Paste a prompt such as “Please run the bootstrap script for me. Explain what you are doing and share the results.” The helper will execute `scripts/setup/bootstrap_project.sh`, confirm success, and translate the output.
6. **Log the Baseline:** Add a row to `docs/change-log.md` (for example `change-YYYYMMDD-01`) so the history starts clean, then push so the GitHub Actions workflow runs on pull requests.

Need deeper context or role guidance? Read `docs/manual/starter-kit-manual.md` after the novice flow feels comfortable.

## Quickstart (For the Helper)
- Start with the **Agent Pledge** from `PROMPT-CORE-novice-flow.md`.
- Name the current RJW-IDD stage at the top of every reply.
- Offer the next prompt to paste when you finish a stage.
- Offer to run safe commands (tests, setup, formatting), describe what they do, ask for a yes/no, then summarise the results.
- Before editing files, list the plan and wait for human approval.

## What's Included
- **Method Pack (`../rjw-idd-methodology/`):** Core principles, role handbook, stage checklists, decision template, **and new operations phase (METHOD-0005)**.
- **Docs & Standards (`docs/`):** Change log template, decision templates, living-doc reconciliation log, runbooks, governance standards, **operational quick reference**, and a detailed starter-kit manual (`docs/manual/starter-kit-manual.md`).
- **Docs/Prompts (`docs/prompts/`):** Plain-language prompt index (`README.md`), copy-ready novice flow, agent guardrails, glossary, example conversations, and deeper prompts for specs, testing, docs, and audits.
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

## Capability Matrix

This matrix lists core features and whether they are available (✅), partially available (🟨), or not available (❌).

| Feature | Status | Link |
|---|---:|---|
| Starter kit scripts (bootstrap) | ✅ | `rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh` |
| Governance checks (local) | ✅ | `scripts/checks/run_checks.sh` |
| CI gating workflows | ✅ | `.github/workflows/gating-ci.yml` |
| Release ZIP artifact | ✅ | `.github/workflows/release.yml` |
| 3D add-on harness | 🟨 | `addons/3d-game-core/` (opt-in scaffolding) |
| Video AI add-on | 🟨 | `addons/video-ai-enhancer/` (opt-in scaffolding) |
| Pre-commit hooks | ✅ | `.pre-commit-config.yaml` |
| Doc-sync checker | ✅ | `scripts/tools/doc_sync_check.py` |

