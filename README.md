# Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD) Starter Kit

[![Gating CI](https://github.com/Rolaand-Jayz/Rolaand-Jayz-Wayz-IDD/actions/workflows/gating-ci.yml/badge.svg)](https://github.com/Rolaand-Jayz/Rolaand-Jayz-Wayz-IDD/actions/workflows/gating-ci.yml)

> Built so a person with **zero coding background** can partner with an AI helper, stay on the RJW-IDD rails, and ship real work.

---

## Your First 15-Minute Win: 3D Slot Car (Win 1)

Welcome! Your first goal is to succeed at a task that is very difficult for an AI model to complete in a single step: creating a 3D game. This will show you the power of the RJW-IDD method to build complex projects reliably.

We will build the first "win" of a 3D Slot Car game: getting a player-controlled car to drive on a track.

This is a great first win because it's visually impressive and creates a real game mechanic, but it requires several steps that must be done in the correct order. A single "one-shot" prompt would likely fail, but our structured method will succeed.

**Your only task:** Copy the prompt below and paste it to your AI helper. It will guide you through building the core of the game.

```text
You are my AI coding helper. Your goal is to help me create the first "win" for a 3D Slot Car game: a player-controlled car driving on a simple, circular track. We will do this in a single index.html file using Three.js.

This is a difficult benchmark, so we must use the structured RJW-IDD methodology.

To do this, you MUST follow the RJW-IDD methodology. Please perform the following steps:
1.  **Pledge:** First, pledge to follow the project's rules.
2.  **Start:** Announce you are in the "Start" stage. The goal is to create workspace/slot_car_game.html.
3.  **Explore:** Announce the "Explore" stage. Break the project down into these 5 components:
    1.  **Scene Setup:** Basic Three.js scene, camera, renderer, and lighting.
    2.  **The Track:** Define a simple circular 3D curve to act as the track's path, and create a visual model for it.
    3.  **The Car:** Create a simple box to represent the car.
    4.  **"On-Rails" Logic:** The core logic to place the car on the track curve and move it along the path based on a "speed" variable. The car's orientation should match the curve's direction.
    5.  **Player Controls:** Listen for keyboard input (up/down arrows) to increase or decrease the car's speed.
4.  **Decide:** Announce the "Decide" stage. State the final plan is to build the game by implementing each of the 5 components sequentially.
5.  **Create (Iteratively):** Announce the "Create" stage. Now, for each component, one at a time:
    a. Generate ONLY the code for that single component.
    b. Explain what the new code does in simple terms.
    c. Ask for my approval before you write the changes to the file.
    d. After I approve, add the new code to the slot_car_game.html file.
    This iterative process is critical. Do not generate the entire game at once.
6.  **Test (Iteratively):** After each "Create" step, announce the "Test" stage. Give me simple instructions to open the slot_car_game.html file and verify the new functionality (e.g., "Verify you see the track," "Verify the car appears on the track," "Verify the car moves when you press the up arrow").
7.  **Record & Wrap:** Once the car is moving on the track under player control, announce the "Record" and "Wrap" stages. Confirm that "Win 1" is complete and congratulate me on the achievement.
```

---

## Key Documents
| Document | Purpose |
|---|---|
| [**RJW-IDD-MASTER-INDEX.md**](RJW-IDD-MASTER-INDEX.md) | The master list of all documents, specs, and logs. Use this to find anything. |
| [**PROMPT-LIBRARY-QUICK-ACCESS.md**](PROMPT-LIBRARY-QUICK-ACCESS.md) | Your quick-access guide to the most important prompts for you and your AI helper. |
| [**quickstart.md**](quickstart.md) | The fastest path to getting the project running on your local machine. |
| [**rjw-idd-starter-kit/docs/manual/starter-kit-manual.md**](rjw-idd-starter-kit/docs/manual/starter-kit-manual.md) | The detailed field guide for how to use and adapt the starter kit. |

## 👤 Quickstart (For Humans)
1. **Open the Novice Guide:** `rjw-idd-starter-kit/docs/manual/novice-quickstart.md` walks you through the seven RJW-IDD stages.
2. **Load the Core Prompts:** Keep `rjw-idd-starter-kit/docs/prompts/PROMPT-CORE-novice-flow.md` open and copy the prompts in order. Use `project-prompts.md` to store any new prompts the helper gives you.
3. **Share the Guardrails:** Send anything from `rjw-idd-starter-kit/docs/prompts/AGENT-GUARDRAILS.md` to remind your helper to stay in plain language and confirm each step. Point them to the glossary (`rjw-idd-starter-kit/docs/prompts/GLOSSARY.md`) if a new term appears.

## 🤖 Quickstart (For the Helper)
- Start with the **Agent Pledge** from `rjw-idd-starter-kit/docs/prompts/PROMPT-CORE-novice-flow.md`.
- Name the current RJW-IDD stage at the top of every reply.
- Offer the next prompt to paste when you finish a stage.
- Offer to run safe commands (tests, setup, formatting), describe what they do, ask for a yes/no, then summarise the results.
- Before editing files, list the plan and wait for human approval.

<details>
<summary><b>Learn More (Advanced Documentation)</b></summary>

## What's Included
- **Method Pack (`rjw-idd-methodology/`):** Core principles, role handbook, stage checklists, decision template, **and new operations phase (METHOD-0005)**.
- **Docs & Standards (`docs/`):** Change log template, decision templates, living-doc reconciliation log, runbooks, governance standards, **operational quick reference**, and a detailed starter-kit manual (`rjw-idd-starter-kit/docs/manual/starter-kit-manual.md`).
- **Docs/Prompts (`rjw-idd-starter-kit/docs/prompts/`):** Plain-language prompt index (`README.md`), copy-ready novice flow, agent guardrails, glossary, example conversations, and deeper prompts for specs, testing, docs, and audits.
- **Specs (`specs/`):** Template specifications for functional backbone, quality gates, evidence harvest, observability, security, integration, cost governance, **deployment operations (SPEC-0701), SLO framework (SPEC-0801), user feedback (SPEC-0901), and data governance (SPEC-1001)**.
- **Artifacts (`rjw-idd-starter-kit/artifacts/`):** Blank ledgers, integration transcript scaffold, and supporting templates.
- **Research (`rjw-idd-starter-kit/research/`):** Starter evidence task configuration, empty indices, and allowlist instructions ready for harvesting.
- **Scripts & Tools (`scripts/`, `tools/`):** Evidence harvester, ID validators, cost dashboard helper, sandbox utilities, setup bootstrapper, and test-guard helpers.
- **Logs (`rjw-idd-starter-kit/logs/`):** Placeholder directories with README files describing required artefacts for audits **including deployment logs, SLO reports, operational metrics, satisfaction tracking, and DR drill results**.

Use this starter kit as the reusable part of the methodology; layer your product-specific specs, evidence, and code on top.

## Lifecycle Overview
RJW-IDD runs through **four** repeatable phases with continuous governance around them:

1.  **Research-Driven Development (RDD)**
    - Configure evidence tasks (`rjw-idd-starter-kit/research/evidence_tasks.json`).
    - Run the harvester (`rjw-idd-starter-kit/tools/rjw_idd_evidence_harvester.py`) and validation script to populate raw and curated indices.
    - Update ledgers and document decisions (DEC-####) that arise from new evidence.

2.  **Spec-Driven Development (SDD)**
    - Author or update specs using the templates in `specs/`.
    - Reserve requirement and test IDs in `rjw-idd-starter-kit/artifacts/ledgers/`.
    - Log reconciliation items in `rjw-idd-starter-kit/docs/living-docs-reconciliation.md` and resolve them before implementation begins.

3.  **Implementation Engines (TDD / LDDD / IDD)**
    - Enforce test-first rules via `rjw-idd-starter-kit/scripts/ci/test_gate.sh` and `rjw-idd-starter-kit/tools/testing/red_green_guard.py`.
    - Capture integration transcripts in `rjw-idd-starter-kit/artifacts/integration/transcript-archive/`.
    - Update living documentation using the standards in `rjw-idd-starter-kit/docs/standards/` and record verification artefacts in the Change Log.

4.  **Operations & Production Support (NEW)** 🎉
    - Deploy with blue-green/canary strategies and automated rollback (`rjw-idd-starter-kit/specs/SPEC-0701-deployment-operations.md`, `rjw-idd-starter-kit/docs/runbooks/docs/runbooks/deployment-runbook.md`).
    - Monitor SLOs, manage error budgets, respond to incidents (`rjw-idd-starter-kit/specs/SPEC-0801-slo-sli-framework.md`, `rjw-idd-starter-kit/docs/runbooks/docs/runbooks/general-incident-runbook.md`).
    - Collect user feedback, conduct usability testing, ensure accessibility (`rjw-idd-starter-kit/specs/SPEC-0901-user-feedback-loops.md`).
    - Manage data lifecycle, backups, migrations, and compliance (`rjw-idd-starter-kit/specs/SPEC-1001-data-governance.md`).
    - Pass operational maturity gates: Production Readiness → Post-Launch Stabilization → Operational Excellence (`rjw-idd-methodology/operations/METHOD-0005-operations-production-support.md`).

Cross-cutting governance (audits, cost reviews, security drills) runs continuously using the runbooks and scripts provided.

## Getting Started in a New Project
1. **Copy the Starter Kit** into your repository (or add as a subtree) and adjust paths as needed.
2. **Run the Bootstrap Script:** `rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh` ensures dependencies are installed and the guard suite passes locally.
3. **Set Up Ledgers:** Keep `rjw-idd-starter-kit/artifacts/ledgers/requirement-ledger.csv` and `rjw-idd-starter-kit/artifacts/ledgers/test-ledger.csv` under version control. Add entries as requirements/tests are defined.
4. **Establish Roles:** Assign Agent Conductor, Spec Curator, Doc Steward, and Governance Sentinel. Align on expectations in `rjw-idd-starter-kit/docs/manual/starter-kit-manual.md`.
5. **Run Initial Harvest:** Configure `rjw-idd-starter-kit/research/evidence_tasks.json`, execute the harvester, validate output, and log the run in the Change Log.
6. **Author Specs:** Clone the spec templates, fill in project-specific details, and link to evidence/requirements/tests.
7. **Adopt Runbooks:** Tailor documents in `rjw-idd-starter-kit/docs/runbooks/` for your environment (e.g., sandbox reset commands, finance workflows).
8. **Update Naming Conventions:** Follow `rjw-idd-starter-kit/docs/standards/docs/standards/naming-conventions.md` to keep artefacts consistent.

## Key Templates & Scripts
- `rjw-idd-starter-kit/templates-and-examples/templates/change-logs/CHANGELOG-template.md` – table ready for change entries.
- `rjw-idd-starter-kit/docs/living-docs-reconciliation.md` – log for documentation gaps.
- `rjw-idd-starter-kit/docs/runbooks/` – operational playbooks (harvest, test-first, security, finance).
- `rjw-idd-starter-kit/specs/` – editable specifications covering major governance areas.
- `rjw-idd-starter-kit/scripts/validate_ids.py` – validates ledgers, change log, and ID references.
- `rjw-idd-starter-kit/scripts/promote_evidence.py` / `rjw-idd-starter-kit/scripts/validate_evidence.py` – curation helpers.
- `rjw-idd-starter-kit/tools/rjw_idd_evidence_harvester.py` – fetches evidence from public sources.
- `rjw-idd-starter-kit/tools/testing/red_green_guard.py` – ensures tests accompany each change.
- `rjw-idd-starter-kit/tools/testing/change_log_guard.py` – blocks merges that omit a change-log update.
- `rjw-idd-starter-kit/tools/testing/living_docs_guard.py` – fails when living-doc gaps remain open.
- `rjw-idd-starter-kit/tools/testing/governance_alignment_guard.py` – keeps specs, ledgers, and decisions in lockstep.
- `rjw-idd-starter-kit/tools/integration/archive_scaffold.py` – scaffolds integration transcript directories.

## Change Control
- Every meaningful change creates a row in `rjw-idd-starter-kit/templates-and-examples/templates/change-logs/CHANGELOG-template.md` with impacted IDs and verification proof.
- Decisions are recorded using `rjw-idd-methodology/templates/PROJECT-DEC-template.md` and stored in `docs/decisions/`.
- Audit reflections append ⟦audit-id:n⟧ <reflect/> entries to stage summaries (see `rjw-idd-starter-kit/logs/LOG-0001-stage-audits.md`).

## Automated Guardrail
`rjw-idd-starter-kit/scripts/ci/test_gate.sh` runs in CI to enforce the RJW-IDD lifecycle:

- Validates that code diffs include test updates, evidence remains fresh, ledgers match IDs, and the change log records every change.
- Rejects merges while living-document reconciliation entries stay open and requires a documentation/spec update alongside implementation work.
- Verifies that specification or research updates ship with matching ledger adjustments and a new decision record.

Wire this script into your preferred CI system so every pull request satisfies the RDD → SDD → Implementation gates.

## Automated Governance
This repository includes a CI (Continuous Integration) pipeline that automatically enforces the RJW-IDD methodology on every pull request. These automated checks, or "guardrails," ensure that every contribution meets the project's standards for quality, traceability, and documentation.

The primary workflow is defined in [`.github/workflows/gating-ci.yml`](.github/workflows/gating-ci.yml). Key checks include:
- **Test Coverage:** Ensures that new code is accompanied by tests.
- **Linter & Formatter:** Checks for code style and consistency.
- **Security Audit:** Scans for known vulnerabilities in dependencies.
- **Methodology Guards:** Runs scripts to validate that change logs are updated, documentation is current, and all traceability IDs are valid.

These guards prevent common errors and allow the team to focus on the work itself, knowing that the process is being upheld automatically.

## Setup Script Reference
- `rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh` creates a project virtual environment, installs dependencies, runs pytest, and executes the governance test gate.
- Override the detected Python with PYTHON_BIN. If origin/main is not available yet, the script falls back to the repository’s first commit for diffing.
- Use the script after pulling future updates to ensure your environment stays in sync with the kit.

## Adapting the Starter Kit
- Update spec and runbook templates with your domain-specific requirements.
- Add additional tooling or prompts under `scripts/` and `rjw-idd-starter-kit/docs/prompts/` as needed.
- Extend validators to enforce any extra governance rules your organisation requires.

By keeping this starter kit clean and evidence-neutral, you can import it into any project and immediately apply RJW-IDD without carrying over past product baggage. Populate the templates with your research, specs, and tests, then run the methodology end-to-end.

## Feature Toggles
RJW-IDD keeps feature enablement declarative in `method/config/features.yml`. This registry controls both the built-in CLI capabilities and any add-ins you opt into.

| Toggle | Default | Controls | Adjustment |
| --- | --- | --- | --- |
| features.guard | true | CLI guard commands (policy validation) | Set to false only if you are packaging a slim kit and have replacement guard rails. |
| features.init | true | CLI project bootstrapping | Disable if you replace the interactive “rjw init” workflow with your own. |
| features.prompts_version | true | Prompt pack metadata (`rjw-idd-starter-kit/prompt-pack.json`) | Disable for fully offline or prompt-free bundles. |
| features.yolo_mode | false | YOLO auto-approval prompts/templates (`docs/prompts/{user,agent}/core-yolo-flow`) | Enable when you want the helper to auto-approve guarded steps. Keep guard + tests active. |
| features.turbo_mode | false | Turbo prompts/templates (`docs/prompts/{user,agent}/core-turbo-flow`) | Enable for short sprints that allow lighter guardrails; still run at least one verification. |
| addons.3d_game_core.enabled | true | 3D game governance, harnesses, specs | Toggle with the script `rjw-idd-starter-kit/scripts/addons/enable_3d_game_core.py` (or the matching disable script). |
| addons.video_ai_enhancer.enabled | false | Real-time video governance, quality/latency gates | Toggle with the script `rjw-idd-starter-kit/scripts/addons/enable_video_ai_enhancer.py`. |

After editing the registry, run `rjw-idd-starter-kit/scripts/config_enforce.py` (execute with python) to confirm the declared state matches the filesystem (prompt pack, add-in directories, etc.). Scripted helpers under `rjw-idd-starter-kit/scripts/addons/` update the YAML for you and record the right governance entries; manual edits are fine as long as the guard stays green.

## Add-ins

- [3D Game Core](rjw-idd-methodology/addons/3d-game-core/README.md) — opt-in 3D harnesses, specs, and gates (enabled by default; adjust via the feature registry or addon scripts).
- [Video AI Enhancer](rjw-idd-methodology/addons/video-ai-enhancer/README.md) — opt-in real-time video enhancement, latency, and storage governance (disabled by default).

## Capability Matrix

This matrix lists core features and whether they are available (✅), partially available (🟨), or not available (❌).

| Feature | Status | Link |
|---|---:|---|
| Starter kit scripts (bootstrap) | ✅ | `rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh` |
| Governance checks (local) | ✅ | `scripts/checks/run_checks.sh` |
| CI gating workflows | ✅ | `.github/workflows/gating-ci.yml` |
| Release ZIP artifact | ✅ | `.github/workflows/release.yml` |
| 3D add-on harness | 🟨 | `rjw-idd-methodology/addons/3d-game-core/` (opt-in scaffolding) |
| Video AI add-on | 🟨 | `rjw-idd-methodology/addons/video-ai-enhancer/` (opt-in scaffolding) |
| Pre-commit hooks | ✅ | `.pre-commit-config.yaml` |
| Doc-sync checker | ✅ | `scripts/tools/doc_sync_check.py` |

</details>
