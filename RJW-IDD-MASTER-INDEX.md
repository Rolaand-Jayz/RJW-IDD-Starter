
# RJW-IDD Master Index & Quick Reference
**Version:** 1.0.0  
**Last Updated:** 2025-10-05  
**Purpose:** Comprehensive index for fast lookup and retrieval of all RJW-IDD methodology components

---

## 🆕 Zero-Knowledge Quickstart (for absolute beginners)
If you're new to this repository or the RJW-IDD methodology and want a fast, non-technical path to get useful results, follow these small steps. No prior knowledge required.

1. Read this file end-to-end once to get the big picture (5–10 minutes).
2. Open `rjw-idd-starter-kit/README.md` next — it contains runnable examples and a minimal setup.
3. Create a working Python virtual environment and install the project's dependencies:

```bash
# from the repository root
python3 -m venv .venv
source .venv/bin/activate
pip install -r rjw-idd-starter-kit/requirements.txt || pip install -r rjw-idd-starter-kit/requirements-dev.txt
```

| Toggle | Notes |
| --- | --- |
| `features.guard` | Controls the CLI guard/validator entry points (`rjw guard …`). |
| `features.init` | Enables the interactive `rjw init` workflow. |
| `features.prompts_version` | Publishes `prompt-pack.json` metadata for prompt libraries. |
| `addons.*.enabled` | Declares add-on artefacts active; keep in sync with the addon directories and helper scripts. |

Run `rjw-idd-starter-kit/scripts/config_enforce.py` (with Python) after editing the registry to confirm the declaration matches the filesystem (prompt pack, add-in directories, etc.).

### 3D Game Core Add-on
4. Run the project's basic health check and tests (fast smoke):

```bash
cd rjw-idd-starter-kit
pytest -q  # runs the test suite; expect a small set of quick checks
```

5. Try an example prompt flow (no deep knowledge needed): open `rjw-idd-starter-kit/docs/prompts/` and start with `PROMPT-0001-starter-briefing.md` — it walks you through creating a short plan and next steps.

6. When you want help, use `project-prompts.md` or open `PROMPT-LIBRARY-QUICK-ACCESS.md` — both are curated for newcomers.

Notes for complete beginners:
- You don't need to understand all files to start. Focus on `rjw-idd-starter-kit/docs/`, `docs/runbooks/`, and `docs/prompts/` first.
- If anything fails during setup, copy the terminal output and open `docs/troubleshooting.md`.


## 📋 TABLE OF CONTENTS

1. [Core Methodology Documents](#core-methodology-documents)
2. [Governance & Roles](#governance--roles)
3. [Lifecycle Phases](#lifecycle-phases)
4. [Add-on Systems](#add-on-systems)
5. [Specifications (SPECs)](#specifications-specs)
6. [Documentation Standards (DOCs)](#documentation-standards-docs)
7. [Prompts & Workflows](#prompts--workflows)
8. [Scripts & Tools](#scripts--tools)
9. [Guards & Validators](#guards--validators)
10. [Artifacts & Ledgers](#artifacts--ledgers)
11. [Decision Records (DECs)](#decision-records-decs)
12. [Evidence System](#evidence-system)
13. [CI/CD Integration](#cicd-integration)
14. [Logs & Audits](#logs--audits)
15. [Quick Lookup Tables](#quick-lookup-tables)

---

## 🧭 Simplified Navigation (start here)
If you're just exploring, these are the smallest set of places to click/read to start getting value quickly.

- Starter & runnable examples: `rjw-idd-starter-kit/README.md` — quick setup and example runs.
- Beginner prompts: `rjw-idd-starter-kit/docs/prompts/PROMPT-0001-starter-briefing.md` — guided plan creation.
- Quick prompts library: `PROMPT-LIBRARY-QUICK-ACCESS.md` — one-page access to common prompts.
- Runbooks (how-to): `docs/runbooks/` — step-by-step operational procedures.
- Core doctrine overview: `rjw-idd-methodology/README.md` — high-level explanations of concepts.
- Troubleshooting: `rjw-idd-starter-kit/docs/troubleshooting.md` and `docs/troubleshooting.md` — common fixes.
- Tests & health checks: `rjw-idd-starter-kit` then run `pytest` to validate your environment.

Tip: copy-paste the path into your editor/file-open dialog to jump straight to a file.

## 📘 Beginner Glossary (plain language)
A short list of terms you'll see frequently, explained simply.

- Method / RJW-IDD: The documented process and conventions in this repo — how we plan, specify, build, and operate software.
- Discovery: The research and evidence-gathering phase where you collect facts and user needs.
- Specification (Spec): A formal, traceable description of what the system should do.
- Execution: The building, testing, and delivery phase (where code and tests are written).
- TDD (Test-Driven Development): Write failing tests first, then code to make them pass.
- LDDD (Living Documentation Driven Development): Keep docs and code changes together so docs never go stale.
- Guard: Automated checks (scripts/tests) that block unsafe or incomplete changes before merge/deploy.
- Add-on: Optional feature packs (for example, 3D Game Core) you can enable or disable.
- Runbook: A step-by-step playbook for operational tasks (deploys, incident handling).
- Change Log / DEC-####: Records of decisions and changes; DEC-#### are decision documents you can read for rationale.
- Evidence: Harvested practitioner knowledge or signals used to inform specs and decisions.

If you want more glossary entries, I can expand this into a full `docs/glossary.md` and link it from here.

## 🛠️ Starter Tutorial Projects (pick one to scaffold)
Below are five complete, fun tutorial project options designed for a solo, no-experience developer. Each one is explicitly crafted to exercise the full RJW‑IDD workflow (Discovery → Specification → Execution → Operations) and includes variability axes so every user's result will be different.

1. MoodMix — mood-driven playlist & visualizer
  - Pitch: Type a mood or paste a short journal line; the app returns a playlist, a dynamic visualizer, and a shareable mood card (PNG).
  - Why it teaches the method: evidence-led UX choices, spec for media imports, tests for mapping and rendering, runbook for deployment and file handling.
  - Variability: visual styles, mood→genre mapping, music sources, share templates.
  - Est. effort: 3–5 days
  - Scaffold path: `tutorials/moodmix/`

2. Recipe Remix — creative recipe generator and printable cards
  - Pitch: Give ingredients and constraints; get a novel recipe, shopping list, and printable recipe card (PDF).
  - Why it teaches the method: discovery of edge cases, spec for ingredient formats, TDD for normalization and PDF generation, runbook for persistence & privacy.
  - Variability: cuisine, dietary rules, difficulty, template styles.
  - Est. effort: 3–6 days
  - Scaffold path: `tutorials/recipe-remix/`

3. PixelPet Studio — create and care for a tiny pixel pet
  - Pitch: Feed, play, and customize a pixel pet that evolves; includes deterministic 48-hour replay of player actions.
  - Why it teaches the method: state-machine specs, deterministic replay tests, integration transcripts, runbook for migration/backups.
  - Variability: art packs, growth rules, mini-games, social sharing options.
  - Est. effort: 4–7 days
  - Scaffold path: `tutorials/pixelpet-studio/`

4. Arcade Map Maker — collaborative map editor with versioned snapshots
  - Pitch: Tile-based editor with layers, exportable JSON maps, PNG snapshots, and branching/rollback of map versions.
  - Why it teaches the method: schema specs, snapshot/versioning tests, UI integration tests, runbook for data export/import.
  - Variability: palettes, map size, tile behaviors, collaboration model (fork vs lock).
  - Est. effort: 4–8 days
  - Scaffold path: `tutorials/arcade-map-maker/`

5. StoryForge — collaborative short-story remixing and zine export
  - Pitch: Authors submit fragments; the app suggests merges, checks continuity, and generates a printable zine with author credits.
  - Why it teaches the method: evidence-driven merge rules, spec for attribution, integration tests for merges→export, runbook for zine generation.
  - Variability: genres, merge aggressiveness, layout templates, contributor roles.
  - Est. effort: 4–7 days
  - Scaffold path: `tutorials/storyforge/`

How to proceed

- The tutorial roots have been created as empty starting points (no files were added inside them):
  - `tutorials/moodmix/`
  - `tutorials/recipe-remix/`
  - `tutorials/pixelpet-studio/`
  - `tutorials/arcade-map-maker/`
  - `tutorials/storyforge/`

Scaffold-by-methodology (what will happen next)

All tutorial artifacts (DEC, evidence, specs, scaffolding, tests, runbooks, and ops docs) will be produced by following the RJW‑IDD methodology end-to-end. No pre-built venvs or pre-created source files are included — environment setup is an explicit methodological step to teach developers how to manage their tooling.

Step-by-step flow (interactive, chat-driven in the IDE)

1) Discovery — user in the chat
  - The agent asks a short set of discovery questions and requests 5 example inputs the user wants the tutorial to handle.
  - The user replies in the IDE chat. The agent creates `tutorials/<slug>/DEC-0001.md` capturing scope, success criteria, and constraints and shows a file preview in chat.
  - The agent (optionally) synthesizes or gathers small sample evidence files and places them under `tutorials/<slug>/evidence/` so the spec loop can proceed.

2) Specification — iterative in chat
  - The agent drafts `tutorials/<slug>/specs/SPEC-<slug>-functional.md` from the DEC and evidence and posts it in chat for user review.
  - The user edits or accepts the spec in chat; the agent commits the approved spec and links it from the DEC.

3) Environment (explicit teaching step)
  - The agent teaches venv creation in the chat and explains the reasons and alternatives (poetry, pipx, system interpreter). The learner runs the commands locally.
  - Example commands are provided in chat and saved to `tutorials/<slug>/setup/ENVIRONMENT.md` by the agent (this file documents the expected outcomes and quick troubleshooting tips):

```bash
# from the tutorial root
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

4) Implementation scaffolding (after spec approval)
  - The agent creates minimal, commented starter files under `tutorials/<slug>/src/`, `tutorials/<slug>/tests/`, and `tutorials/<slug>/docs/` guided by the spec.
  - For each file creation the agent provides an educational note in chat explaining what the file does, why it's needed, and what to expect when running it.

5) Tests & guards (TDD workflow)
  - The agent generates unit tests and a small integration test that encode the spec's acceptance criteria and guides the user through running them.
  - The agent interprets test failures in chat and suggests targeted edits until tests pass.

6) Living docs, runbooks & artifacts
  - The agent ensures docs are updated alongside code (`tutorials/<slug>/docs/README.md`, `tutorials/<slug>/docs/runbook.md`).
  - Integration transcripts and example outputs are stored under `tutorials/<slug>/artifacts/integration/` for replay and audit.

7) Operations & SLOs
  - The agent drafts `tutorials/<slug>/docs/ops.md` with simple SLOs, backup policies, and monitoring checklist items.

Chat-driven confirmations

- Every step is confirmed in the IDE chat. The agent always includes:
  - A short educational blurb (what, why, how).
  - Exact copyable commands for the user to run locally.
  - A preview of the files to be created (or the diff) before applying changes.

If you'd like, I can start the Discovery step for a chosen tutorial now. Which tutorial should I begin with?


## 🎯 CORE METHODOLOGY DOCUMENTS

### Primary Method Files
| Document ID | Location | Purpose | Key Concepts |
|-------------|----------|---------|--------------|
| **METHOD-0001** | `rjw-idd-methodology/core/METHOD-0001-core-method.md` | Core methodology distilled from Tree-of-Thought decisions | Mission, Lifecycle Spine, Discovery/Execution Layers, Stage Gates |
| **METHOD-0002** | `rjw-idd-methodology/governance/METHOD-0002-phase-driver-checklists.md` | Phase-by-phase checklists for gate enforcement | Discovery Loop, Specification Loop, Execution Loop, Exit Gates |
| **METHOD-0003** | `rjw-idd-methodology/governance/METHOD-0003-role-handbook.md` | Role definitions and responsibilities | Evidence Lead, Spec Architect, Security Liaison, Execution Wrangler |
| **METHOD-0004** | `rjw-idd-methodology/operations/METHOD-0004-ai-agent-workflows.md` | AI agent-specific workflow guidance | Agent Conductor, Spec Curator, Doc Steward, Governance Sentinel |
| **METHOD-0005** | `rjw-idd-methodology/operations/METHOD-0005-operations-production-support.md` | Production operations and support phase | SLOs, Incident Response, DR, Operational Excellence |

### Methodology README
- **Location:** `rjw-idd-methodology/README.md`
- **Purpose:** Directory layout and usage guidance for the method pack
- **Key Points:**
  - Core doctrine lives in `rjw-idd-methodology/`
  - Templates use `METHOD-####` namespace
  - Add-ons extend under `addons/`
  - Only modify after capturing new `DEC-####`

---

## 👥 GOVERNANCE & ROLES

### Role Matrix (from METHOD-0003)

| Role | Primary Responsibilities | Key Artifacts | Signs Off On |
|------|-------------------------|---------------|--------------|
| **Evidence Lead** | Owns Discovery research loop | `research/evidence_tasks.json`, evidence indices | Discovery research audits |
| **Spec Architect** | Leads Discovery specification loop | Requirement ledger, spec stack, living-doc reconciliation | Discovery audits |
| **Security & Privacy Liaison** | Consent-first telemetry, security runbooks | Consent artifacts, security logs, sandbox drills | Discovery & Execution audits |
| **Execution Wrangler** | Drives Execution layer, enforces test-first | Tests, documentation, integration transcripts | Execution stage audits |
| **Agent Conductor** | Runs prompts, captures transcripts, executes guards | `docs/prompts/`, `artifacts/integration/`, `logs/ci/` | CI gate compliance |
| **Spec Curator** | Maintains ledgers, specs, reconciliation log | `specs/`, `artifacts/ledgers/` | Spec alignment |
| **Doc Steward** | Updates living documentation, verifies Change Log | `docs/standards/DOC-0006`, `docs/change-log.md` | Documentation completeness |
| **Governance Sentinel** | Runs validators, records audits, blocks releases | `logs/LOG-0001-stage-audits.md` | All stage gates |

### Operating Rhythm
- **Daily:** Stand-up reporting on harvest plans and guard/test status
- **Weekly:** Review Change Log, stage audits, outstanding DEC-#### actions
- **Post-incident/hotfix:** Security Liaison leads retrospective
- **Quarterly:** Verify cumulative evidence/decision coverage, method updates

---

## 🔄 LIFECYCLE PHASES

### Phase 0: Governance Setup
**Checklist Items:**
- [ ] `docs/decisions/` directory with sequential `DEC-####.md` records
- [ ] `docs/change-log.md` initialized
- [ ] Roles confirmed and assigned
- [ ] Stage audit log initialized (`logs/LOG-0001-stage-audits.md`)

### Layer 1: Discovery

#### Research Loop (RDD)
**Purpose:** Automated harvest of practitioner insight  
**Key Activities:**
1. Draft `DEC-####` describing harvest goal
2. Update `research/evidence_tasks.json`
3. Run harvester (`tools/rjw_idd_evidence_harvester.py`)
4. Promote curated entries to `research/evidence_index.json`
5. Execute validators
6. Append Change Log row

**Exit Criteria:**
- Curated evidence meets recency requirement (default: 14 days)
- Gaps tracked to owners with due dates
- Validators pass

#### Specification Loop (SDD)
**Purpose:** Translate evidence into formal specifications  
**Key Activities:**
1. Draft/update `DEC-####` capturing spec scope
2. Create/update specs across all dimensions
3. Refresh requirement ledger
4. Update living documentation reconciliation log
5. Run ID validator

**Exit Criteria:**
- Requirement ledger aligned with evidence/specs
- Living-doc reconciliation cleared or deferred with plan
- Scope freeze captured in latest `DEC-####`
- Discovery exit signed by Evidence Lead and Spec Architect

### Layer 2: Execution

#### Parallel Engines
1. **Test-Driven Development (TDD)**
   - Write failing tests first
   - Guards reject changes without tests
   - Red → Green → Refactor cycle

2. **Living Documentation Driven Development (LDDD)**
   - Docs/runbooks evolve in same change-set as code
   - Eliminates stale knowledge
   - Enforced by living_docs_guard.py

3. **Integration-First Delivery (IDD)**
   - Cross-system work archived with transcripts
   - Diffs stored for audit replay
   - Context preservation for future work

**Exit Criteria:**
- Tests, docs, and transcripts present
- Telemetry consent artifacts up to date
- Stage audit signed by Implementation Wrangler and Security Liaison

### Phase 4: Operations & Production Support

#### Gate 1: Production Readiness (Pre-Launch)
**Requirements:**
- Deployment automation with rollback (`SPEC-0701`)
- SLO/SLI framework defined (`SPEC-0801`)
- Incident response and on-call rotation (`DOC-0018`)
- Backup/restore DR tested (`SPEC-1001`)
- Security posture verified (`SPEC-0501`)
- Observability operational (`SPEC-0401`)
- User feedback mechanisms active (`SPEC-0901`)
- Cost governance configured (`SPEC-0602`)
- Documentation current (`DOC-0006`)
- Accessibility compliance (`SPEC-0901`)

**Sign-off:** Governance Sentinel + Service Owner + Security Liaison

#### Gate 2: Post-Launch Stabilization (30 Days)
**Metrics:**
- SLO compliance maintained
- ≤ 1 SEV-1 incident per month
- All SEV-1/2 postmortems completed
- User satisfaction within acceptable range
- Performance stable within SLOs
- Cost within 10% of forecast

#### Gate 3: Operational Excellence (Quarterly)
**Activities:**
- SLO review and adjustment
- Runbook currency verification
- DR drill execution
- Security review/audit
- Cost optimization analysis
- User feedback analysis
- Observability gap identification
- Dependency health audit

---

## 🔌 ADD-ON SYSTEMS

### Feature Registry
**Location:** `method/config/features.yml`  
**Controls:** Core CLI capabilities and add-on state

```yaml
features:
  guard: true
  init: true
  prompts_version: true
addons:
  3d_game_core:
    enabled: true
    version: 1.0.0
    profile: generic
  video_ai_enhancer:
    enabled: false
    version: 1.0.0
    profile: baseline
```

| Toggle | Purpose |
| --- | --- |
| `features.guard` | Enables CLI guard/validator entry points. |
| `features.init` | Enables the interactive `rjw init` bootstrap flow. |
| `features.prompts_version` | Publishes `prompt-pack.json` metadata for prompt packs. |
| `addons.*.enabled` | Declares add-on artefacts active and should match the directories present. |

After editing the registry (or running an add-on helper script) execute `rjw-idd-starter-kit/scripts/config_enforce.py` (with Python) to ensure declarations and filesystem agree, and capture the change in the change log, decision log, and audit log.

### 3D Game Core Add-on
**ID:** `METHOD-ADDIN-3D-CORE`  
**Location:** `rjw-idd-methodology/addons/3d-game-core/`  
**Status:** Included — enabled by default (`profile: generic`)

```bash
# Enable / disable / change profile
python rjw-idd-starter-kit/scripts/addons/enable_3d_game_core.py
python rjw-idd-starter-kit/scripts/addons/set_3d_profile.py --profile third_person
python rjw-idd-starter-kit/scripts/addons/disable_3d_game_core.py
```

### Video AI Enhancer Add-on
**ID:** `METHOD-ADDIN-VIDEO-AI`  
**Location:** `rjw-idd-methodology/addons/video-ai-enhancer/`  
**Status:** Included — disabled by default (`profile: baseline`)

```bash
# Enable / disable / change profile
python rjw-idd-starter-kit/scripts/addons/enable_video_ai_enhancer.py
python rjw-idd-starter-kit/scripts/addons/set_video_ai_profile.py --profile live_stream
python rjw-idd-starter-kit/scripts/addons/disable_video_ai_enhancer.py
```

### Add-on Governance
**Required when enabling/disabling:**
1. Add entry to `docs/change-log.md`
2. Document decision in `docs/decisions/`
3. Update `logs/LOG-0001-stage-audits.md`

---

## 📄 SPECIFICATIONS (SPECs)

### Core Specifications
| SPEC ID | Location | Purpose | Links To |
|---------|----------|---------|----------|
| **SPEC-0003** | `specs/SPEC-0003-rdd-evidence-harvest.md` | Evidence harvest requirements | EVD-####, research/ |
| **SPEC-0101** | `specs/SPEC-0101-functional-backbone.md` | Functional delivery structure | REQ-####, TEST-#### |
| **SPEC-0201** | `specs/SPEC-0201-quality-gates.md` | Quality gate requirements | TEST-####, CI guards |
| **SPEC-0301** | `specs/SPEC-0301-performance-metrics.md` | Performance measurement | Metrics, benchmarks |
| **SPEC-0401** | `specs/SPEC-0401-observability-telemetry.md` | Observability and telemetry | Consent, metrics |
| **SPEC-0501** | `specs/SPEC-0501-security-privacy-controls.md` | Security and privacy | DOC-0016, sandbox |
| **SPEC-0601** | `specs/SPEC-0601-integration-context.md` | Integration requirements | INTEG-####, transcripts |
| **SPEC-0602** | `specs/SPEC-0602-cost-governance.md` | Cost governance | Cost logs, dashboards |
| **SPEC-0701** | `specs/SPEC-0701-deployment-operations.md` | Deployment automation | DOC-0020, rollback |
| **SPEC-0801** | `specs/SPEC-0801-slo-sli-framework.md` | SLO/SLI definitions | Operational metrics |
| **SPEC-0901** | `specs/SPEC-0901-user-feedback-loops.md` | User feedback collection | Satisfaction metrics |
| **SPEC-1001** | `specs/SPEC-1001-data-governance.md` | Data governance and DR | DOC-0026, backups |

### Specification Template Structure
**Common Sections:**
1. **Linked Requirements:** REQ-#### references
2. **Linked Decisions:** DEC-#### references
3. **Status:** Template/Draft/Active/Deprecated
4. **Purpose:** What the spec governs
5. **Scope:** What's included/excluded
6. **Functional Expectations:** Concrete requirements
7. **Process Flow:** Step-by-step procedures
8. **Traceability Controls:** Validation mechanisms
9. **Follow-Up Guidance:** Customization notes

---

## 📚 DOCUMENTATION STANDARDS (DOCs)

### Standards Documents
| DOC ID | Location | Purpose | Key Concepts |
|--------|----------|---------|--------------|
| **DOC-0001** | `docs/standards/DOC-0001-tot-capture-standard.md` | Tree-of-Thought capture standard | Decision recording |
| **DOC-0005** | `docs/standards/DOC-0005-traceability-schema.md` | Traceability ID schema | ID formats, linking |
| **DOC-0006** | `docs/standards/DOC-0006-living-docs-guideline.md` | Living documentation guideline | Doc classes, maintenance |
| **DOC-0011** | `docs/standards/DOC-0011-intelligence-driven-methodology.md` | RJW-IDD overview | Roles, lifecycle, tooling |
| **DOC-0012** | `docs/standards/DOC-0012-cost-governance-standard.md` | Cost governance standard | Budgets, tracking, alerts |
| **DOC-0013** | `docs/standards/DOC-0013-naming-conventions.md` | Naming conventions | Files, IDs, artifacts |
| **DOC-0021** | `docs/standards/DOC-0021-git-setup-configuration.md` | Git configuration and workflows | Version control, commits |

### Runbooks
| DOC ID | Location | Purpose | Used By |
|--------|----------|---------|---------|
| **DOC-0004** | `docs/runbooks/DOC-0004-rdd-harvest-runbook.md` | Evidence harvest procedures | Evidence Lead |
| **DOC-0015** | `docs/runbooks/DOC-0015-finance-variance-runbook.md` | Finance variance handling | Governance Sentinel |
| **DOC-0016** | `docs/runbooks/DOC-0016-security-incident-runbook.md` | Security incident response | Security Liaison |
| **DOC-0017** | `docs/runbooks/DOC-0017-test-first-runbook.md` | Test-first enforcement | Execution Wrangler |
| **DOC-0018** | `docs/runbooks/DOC-0018-general-incident-runbook.md` | General incident response | On-call, SRE |
| **DOC-0020** | `docs/runbooks/DOC-0020-deployment-runbook.md` | Deployment procedures | SRE, DevOps Lead |
| **DOC-0022** | `docs/runbooks/DOC-0022-git-workflow-runbook.md` | Step-by-step git procedures | All developers |

### Document Classes (from DOC-0006)
| Class | Location | Purpose | Required Metadata |
|-------|----------|---------|-------------------|
| **Implementation Notes** | `implementation/` | Code-level decisions, API shapes | DOC-####, SPEC-####, REQ-####, TEST-####, change_id |
| **API & Integration Guides** | `docs/api/`, `docs/integration/` | Public interfaces, contracts | DOC-####, INTEG-####, version, contact |
| **Runbooks & Playbooks** | `docs/runbooks/` | Operational workflows | DOC-####, spec IDs, validation refs |
| **Change Notes** | `docs/changelog/` | Iteration summaries | DOC-####, change_id, impacted artifacts |

---

## 🤖 PROMPTS & WORKFLOWS

### 📍 PROMPT LIBRARY LOCATION
**Full Prompt Library:** `rjw-idd-starter-kit/docs/prompts/`  
**Quick Access Guide:** `/home/rolaand-jayz/Desktop/method/PROMPT-LIBRARY-QUICK-ACCESS.md`  
**Custom Prompts:** `/home/rolaand-jayz/Desktop/method/project-prompts.md`

### Core Prompt Suite (Novice-Friendly)
| Prompt ID | Location | Purpose | Next Step |
|-----------|----------|---------|-----------|
| **PROMPT-CORE** | `docs/prompts/PROMPT-CORE-novice-flow.md` | Seven-stage workflow for beginners | Stage-specific prompts |
| **PROMPT-0001** | `docs/prompts/PROMPT-0001-starter-briefing.md` | Initial briefing and plan | PROMPT-0002 or PROMPT-0003 |
| **PROMPT-0002** | `docs/prompts/PROMPT-0002-implementation-coach.md` | File-by-file implementation guidance | PROMPT-0004 |
| **PROMPT-0003** | `docs/prompts/PROMPT-0003-spec-translator.md` | Plain requirements to formal specs | PROMPT-0002 |
| **PROMPT-0004** | `docs/prompts/PROMPT-0004-test-navigator.md` | Test planning and design | PROMPT-0002 |
| **PROMPT-0005** | `docs/prompts/PROMPT-0005-doc-sync.md` | Documentation updates | PROMPT-0006 |
| **PROMPT-0006** | `docs/prompts/PROMPT-0006-governance-audit.md` | Pre-PR governance check | PROMPT-0007 |
| **PROMPT-0007** | `docs/prompts/PROMPT-0007-change-log-author.md` | Change log entry creation | PROMPT-0008 |
| **PROMPT-0008** | `docs/prompts/PROMPT-0008-merge-ready-checklist.md` | Final merge readiness check | Merge or iterate |

### Supporting Prompt Resources
| Resource | Location | Purpose |
|----------|----------|---------|
| **Agent Guardrails** | `docs/prompts/AGENT-GUARDRAILS.md` | Rules for AI agent behavior |
| **Agent Reply Template** | `docs/prompts/AGENT-REPLY-TEMPLATE.md` | Structured response format |
| **Example Conversations** | `docs/prompts/EXAMPLE-CONVERSATIONS.md` | Sample interactions |
| **Glossary** | `docs/prompts/GLOSSARY.md` | RJW-IDD terminology |
| **Prompt README** | `docs/prompts/README.md` | Prompt suite overview |

### Add-on Prompts: 3D Game Core
| Prompt | Location | Purpose |
|--------|----------|---------|
| **01** | `addons/3d-game-core/prompts/01_research_pack_3d.md` | Research signal gathering |
| **02** | `addons/3d-game-core/prompts/02_gdd_from_evidence_3d.md` | GDD generation |
| **03** | `addons/3d-game-core/prompts/03_test_navigator_3d.md` | Test planning |
| **04** | `addons/3d-game-core/prompts/04_idd_pacts_generator_3d.md` | Pact generation |
| **05** | `addons/3d-game-core/prompts/05_doc_reconciler_3d.md` | Doc reconciliation |

### Add-on Prompts: Video AI Enhancer
| Prompt | Location | Purpose |
|--------|----------|---------|
| **01** | `addons/video-ai-enhancer/prompts/01_research_signal_video.md` | Signal research |
| **02** | `addons/video-ai-enhancer/prompts/02_pipeline_design_video.md` | Pipeline design |
| **03** | `addons/video-ai-enhancer/prompts/03_quality_playbook_video.md` | Quality assurance |
| **04** | `addons/video-ai-enhancer/prompts/04_operational_response_video.md` | Operations |
| **05** | `addons/video-ai-enhancer/prompts/05_doc_reconciler_video.md` | Doc sync |

---

## 🛠️ SCRIPTS & TOOLS

### Setup & Bootstrap
| Script | Location | Purpose | Usage |
|--------|----------|---------|-------|
| **bootstrap_project.sh** | `scripts/setup/bootstrap_project.sh` | Full environment setup | `bash scripts/setup/bootstrap_project.sh` |
| **install.sh** | `scripts/bootstrap/install.sh` | Interactive installer with add-on selection | `bash scripts/bootstrap/install.sh` |

**Bootstrap Script Behavior:**
1. Creates `.venv/` if missing
2. Installs dependencies from `requirements-dev.txt`
3. Installs editable project if `pyproject.toml` exists
4. Runs `pytest`
5. Executes governance gate
6. Uses `origin/main` or first commit as base reference

**Environment Variables:**
- `PYTHON_BIN` - Override Python interpreter (e.g., `python3.11`)
- `RJW_BASE_REF` - Override base branch for diffing
- `RJW_HEAD_REF` - Override head reference for diffing

### Evidence & Research
| Script | Location | Purpose | Inputs |
|--------|----------|---------|--------|
| **rjw_idd_evidence_harvester.py** | `tools/rjw_idd_evidence_harvester.py` | Automated evidence collection | `research/evidence_tasks.json` |
| **promote_evidence.py** | `scripts/promote_evidence.py` | Curate evidence from raw to index | Raw index, allowlist |
| **validate_evidence.py** | `scripts/validate_evidence.py` | Validate evidence freshness | Index files, cutoff days |

**Evidence Harvester:**
- Fetches from configured sources (Reddit, GitHub, forums)
- Maintains metadata (date, platform, source)
- Creates immutable raw index
- Respects recency filters (default: 14 days)

### Validation & ID Management
| Script | Location | Purpose | Validates |
|--------|----------|---------|-----------|
| **validate_ids.py** | `scripts/validate_ids.py` | ID format and cross-link validation | REQ-####, SPEC-####, TEST-####, EVD-####, DOC-####, DEC-####, INTEG-#### |

**ID Format Rules:**
- `EVD-####` - Evidence records
- `REQ-####` - Requirements
- `SPEC-####` - Specifications
- `TEST-####` - Test cases
- `DOC-####` - Documentation
- `DEC-####` - Decisions
- `INTEG-####` - Integration records
- Add-on prefixes: `REQ-VIDEO-####`, `SPEC-3D-####`, etc.

### Cost & Finance
| Script | Location | Purpose | Outputs |
|--------|----------|---------|---------|
| **run_weekly_dashboard.py** | `scripts/cost/run_weekly_dashboard.py` | Generate cost dashboards | `logs/cost/` |

### Security & Sandbox
| Script | Location | Purpose | Usage |
|--------|----------|---------|-------|
| **drill.py** | `scripts/sandbox/drill.py` | Security sandbox drills | `python scripts/sandbox/drill.py` |
| **reset.sh** | `scripts/sandbox/reset.sh` | Reset sandbox environment | `bash scripts/sandbox/reset.sh` |

### Add-on Management
| Script | Location | Purpose | Usage |
|--------|----------|---------|-------|
| **enable_3d_game_core.py** | `scripts/addons/enable_3d_game_core.py` | Enable 3D game add-on | `python scripts/addons/enable_3d_game_core.py` |
| **disable_3d_game_core.py** | `scripts/addons/disable_3d_game_core.py` | Disable 3D game add-on | `python scripts/addons/disable_3d_game_core.py` |
| **set_3d_profile.py** | `scripts/addons/set_3d_profile.py` | Set 3D game profile | `--profile <name>` |
| **enable_video_ai_enhancer.py** | `scripts/addons/enable_video_ai_enhancer.py` | Enable video AI add-on | `python scripts/addons/enable_video_ai_enhancer.py` |
| **disable_video_ai_enhancer.py** | `scripts/addons/disable_video_ai_enhancer.py` | Disable video AI add-on | `python scripts/addons/disable_video_ai_enhancer.py` |
| **set_video_ai_profile.py** | `scripts/addons/set_video_ai_profile.py` | Set video AI profile | `--profile <name>` |

### Integration Tools
| Script | Location | Purpose | Outputs |
|--------|----------|---------|---------|
| **archive_scaffold.py** | `tools/integration/archive_scaffold.py` | Create integration transcript scaffold | `artifacts/integration/transcript-archive/<task-slug>/` |

**Transcript Structure:**
- `context.md` - Scope, linked IDs, roles, planned doc updates
- `prompts.log` - Prompt/response log
- `diffs/` - Code diffs
- `verification.md` - Verification steps and outcomes

### Utility Tools
| Tool | Location | Purpose |
|------|----------|---------|
| **logging_config.py** | `tools/logging_config.py` | Centralized logging configuration |
| **performance_monitor.py** | `tools/performance_monitor.py` | Performance monitoring utilities |
| **backup_manager.py** | `tools/backup_manager.py` | Backup management |
| **health_check.py** | `tools/health_check.py` | System health checks |
| **performance_benchmark.py** | `tools/performance_benchmark.py` | Performance benchmarking |
| **commit_msg_helper.py** | `tools/git/commit_msg_helper.py` | Commit message validation and builder |

---

## 🛡️ GUARDS & VALIDATORS

### Guard Suite Overview
**Location:** `tools/testing/`  
**Orchestration:** `scripts/ci/test_gate.sh`

### Individual Guards
| Guard | Script | Purpose | Trigger | Resolution |
|-------|--------|---------|---------|------------|
| **Red/Green** | `red_green_guard.py` | Enforce test-first discipline | Code changes without test updates | Add/update tests |
| **ID Validator** | `validate_ids.py` (via scripts/) | Validate ID formats and cross-links | Any file with IDs | Fix broken references |
| **Evidence Freshness** | `validate_evidence.py` (via scripts/) | Ensure evidence is recent | Research artifact changes | Refresh evidence via harvester |
| **Change Log** | `change_log_guard.py` | Require change log entries | Any material change | Add row to `docs/change-log.md` |
| **Living Docs** | `living_docs_guard.py` | Enforce doc updates with code | Non-doc file changes | Update docs or log gap |
| **Governance Alignment** | `governance_alignment_guard.py` | Sync specs/ledgers/decisions | Spec or ledger changes | Update aligned artifacts |
| **Agent Response** | `agent_response_guard.py` | Validate agent output structure | Agent-generated files | Fix output format |

### Test Gate Execution Flow
```bash
scripts/ci/test_gate.sh
├── 1. red_green_guard.py (test coverage)
├── 2. validate_ids.py (ID validation)
├── 3. validate_evidence.py (if research/ changed)
├── 4. change_log_guard.py (change log entry)
├── 5. living_docs_guard.py (documentation)
├── 6. agent_response_guard.py (agent output)
└── 7. governance_alignment_guard.py (alignment)
```

### Guard Configuration
**Environment Variables:**
- `RJW_BASE_REF` - Base branch for diff (default: `origin/main`)
- `RJW_HEAD_REF` - Head reference for diff (default: `HEAD`)
- `PYTHON_BIN` - Python interpreter (default: `python3`)
- `RJW_TEST_PATTERNS` - Custom test file patterns

### Test Indicators (Red/Green Guard)
**Patterns detected as test files:**
- `tests/` directory
- `test_` prefix
- `_test.py` suffix
- `Test.` class pattern

---

## 📦 ARTIFACTS & LEDGERS

### Ledger Files
| Ledger | Location | Purpose | Columns |
|--------|----------|---------|---------|
| **Requirement Ledger** | `artifacts/ledgers/requirement-ledger.csv` | Track all requirements | req_id, status, title, evidence_refs, spec_refs, tests_refs, owner, next_review, notes |
| **Test Ledger** | `artifacts/ledgers/test-ledger.csv` | Track all tests | test_id, status, title, req_refs, spec_refs, test_type, automation_status, owner, notes |

**Ledger Format:**
```csv
req_id,status,title,evidence_refs,spec_refs,tests_refs,owner,next_review,notes
REQ-0001,active,User authentication,EVD-0023;EVD-0045,SPEC-0101,TEST-0001;TEST-0002,Security Team,2025-11-01,Initial requirement
```

### Integration Artifacts
**Location:** `artifacts/integration/`

**Transcript Archive Structure:**
```
artifacts/integration/transcript-archive/<task-slug>/
├── context.md          # Scope, IDs, roles, plans
├── prompts.log         # Prompt/response history
├── diffs/              # Code diffs
│   ├── file1.diff
│   └── file2.diff
└── verification.md     # Verification steps
```

**Scaffold Creation:**
```bash
python tools/integration/archive_scaffold.py <task-slug>
```

### Evidence Artifacts
**Location:** `research/`

| File | Purpose | Structure |
|------|---------|-----------|
| **evidence_tasks.json** | Configure harvest tasks | JSON task definitions |
| **evidence_index_raw.json** | Immutable raw harvest | Full metadata, all records |
| **evidence_index.json** | Curated evidence | Promoted, validated records |
| **evidence_allowlist.txt** | Manual promotion list | EVD-#### per line |
| **EVIDENCE-EXAMPLES.md** | Example evidence records | Documentation |

**Evidence Record Schema:**
```json
{
  "evid_id": "EVD-0001",
  "date": "2025-10-05",
  "platform": "Reddit",
  "source_url": "https://...",
  "minimal_quote": "excerpt...",
  "tags": ["engine", "networking"],
  "quality_flags": ["first-hand", "verified"]
}
```

---

## 📝 DECISION RECORDS (DECs)

### Decision Template
**Location:** `rjw-idd-methodology/templates/PROJECT-DEC-template.md`

**Structure:**
```markdown
# DEC-XXXX — Decision Title
**Decision Date:** YYYY-MM-DD
**Participants:** Roles/Names

## Problem Statement
## Candidate Thoughts
## Evaluation
## Outcome
## Cross-Links
## Follow-Up Actions
## Status Update (optional)
```

### Decision Workflow
1. Copy template to `docs/decisions/`
2. Rename to next sequential `DEC-####`
3. Fill in all sections
4. Cross-link to REQ-####, SPEC-####, DOC-####
5. Reference in `docs/change-log.md`
6. Update `logs/LOG-0001-stage-audits.md` if material

### Foundation Decisions
| Decision | Location | Purpose |
|----------|----------|---------|
| **DEC-0001** | `rjw-idd-methodology/docs/decisions/DEC-0001.md` | Governance artifacts anchor |

### Decision Namespaces
- `METHOD-DEC-####` - Methodology-level decisions
- `PROJECT-DEC-####` - Project-specific decisions (template)
- `DEC-####` - Local project decisions (actual use)
- `DEC-RELIABILITY-####` - Reliability sprint decisions
- `DEC-OPS-####` - Operational improvement decisions
- `DEC-INCIDENT-####` - Incident postmortem decisions

---

## 🔍 EVIDENCE SYSTEM

### Evidence Configuration
**Location:** `research/evidence_tasks.json`

**Task Structure:**
```json
{
  "tasks": [
    {
      "task_id": "task-001",
      "focus_areas": ["engine", "networking"],
      "sources": ["reddit", "github"],
      "date_range": "last_30_days",
      "keywords": ["Unity", "multiplayer"]
    }
  ]
}
```

### Evidence Lifecycle
1. **Configure:** Define tasks in `evidence_tasks.json`
2. **Harvest:** Run `tools/rjw_idd_evidence_harvester.py`
3. **Store Raw:** Results in `evidence_index_raw.json`
4. **Curate:** Promote via `scripts/promote_evidence.py`
5. **Validate:** Check with `scripts/validate_evidence.py`
6. **Link:** Reference in requirement ledger as `evidence_refs`
7. **Audit:** Verify freshness (default: 14 days)

### Evidence Quality Flags
- `first-hand` - Direct practitioner experience
- `verified` - Cross-validated information
- `provisional` - Needs additional validation
- `deprecated` - Superseded by newer evidence

### Evidence Freshness Policy
**Default:** 14 days  
**Configurable:** `--cutoff-days` parameter  
**Enforcement:** `validate_evidence.py` with `--fail-on-warning`

**Triggered When:**
- Research artifacts change
- `research/*` files modified
- Evidence validation scripts change

---

## ⚙️ CI/CD INTEGRATION

### GitHub Actions Workflows
**Location:** `.github/workflows/`

#### Test Gate Workflow
**File:** `test-gate.yml`  
**Trigger:** Pull request events  
**Jobs:**
1. Install dependencies (`requirements-dev.txt`)
2. Run pytest on guards (`tests/guards/`)
3. Execute full test gate (`scripts/ci/test_gate.sh`)

**Configuration:**
- Python version: 3.11
- Fetch depth: 0 (full history)
- Base ref: `origin/main`

#### Video AI Enhancer Workflow
**File:** `video-ai-enhancer.yml` (if addon enabled)  
**Trigger:** Manual or feature flag  
**Purpose:** Run video AI quality gates

**Inputs:**
- `force` - Force execution regardless of feature flag
- `ENABLE_RJW_VIDEO` - Environment variable control

### CI Snippets
**Location:** `rjw-idd-methodology/ci/includes.yml`

**Purpose:** Reusable CI configuration snippets for add-ons

### Local CI Simulation
```bash
# Full gate
bash scripts/ci/test_gate.sh

# With custom refs
RJW_BASE_REF=main RJW_HEAD_REF=feature-branch bash scripts/ci/test_gate.sh

# Individual guards
python tools/testing/red_green_guard.py --root . --files <changed-files>
python scripts/validate_ids.py
python scripts/validate_evidence.py --input research/evidence_index.json --cutoff-days 14
```

---

## 📊 LOGS & AUDITS

### Stage Audit Log
**Location:** `logs/LOG-0001-stage-audits.md`

**Format:**
```markdown
| audit_tag | date (UTC) | stage | summary | owners | follow_up |
|-----------|------------|-------|---------|--------|-----------|
| ⟦audit-id:1⟧ <reflect/> | 2024-03-27 | Discovery→Execution | ... | Lead | Action |
```

**Audit Tags:**
- `⟦audit-id:n⟧ <reflect/>` - Standard reflection
- `⟦audit-id:n⟧ <production-ready/>` - Production readiness gate
- Increment `n` for each new audit

### Change Log
**Location:** `docs/change-log.md`

**Format:**
```markdown
| change_id | date (UTC) | description | impacted_ids | operator | verification |
|-----------|------------|-------------|--------------|----------|--------------|
| change-YYYYMMDD-## | 2025-10-05 | ... | SPEC-####;REQ-#### | Role | validator:pass |
```

**Change ID Format:** `change-YYYYMMDD-##`  
**Sequential:** Increment `##` for same-day changes

### Living Documentation Reconciliation
**Location:** `docs/living-docs-reconciliation.md`

**Format:**
```markdown
| date (UTC) | agent | doc_id(s) | gap summary | resolution plan | status |
|------------|-------|-----------|-------------|-----------------|--------|
| 2025-10-05 | Doc Steward | DOC-0006 | ... | Plan | open/closed |
```

**Status Values:** `open`, `closed`  
**Guard:** Rejects merges with `open` status

### Log Directories

#### CI Logs
**Location:** `logs/ci/`  
**Contains:** Test gate executions, guard outputs  
**Template:** `LOG-TEMPLATE.md`

#### Cost Logs
**Location:** `logs/cost/`  
**Contains:** Weekly dashboards, finance sign-offs  
**Script:** `scripts/cost/run_weekly_dashboard.py`

#### Security Logs
**Location:** `logs/security/`  
**Contains:** Sandbox drill results, incident responses  
**Scripts:** `scripts/sandbox/drill.py`, `DOC-0016`

#### RDD Harvest Logs
**Location:** `logs/rdd-harvest/`  
**Contains:** Evidence harvest execution logs  
**Tool:** `tools/rjw_idd_evidence_harvester.py`

#### Data Lifecycle Logs
**Location:** `logs/data-lifecycle/`  
**Contains:** DR drill results, backup verifications  
**Spec:** `SPEC-1001`

#### Operational Metrics
**Location:** `logs/operational-metrics/`  
**Contains:** SLO reports, deployment logs, satisfaction tracking  
**Specs:** `SPEC-0801`, `SPEC-0701`, `SPEC-0901`

---

## 🚀 QUICK LOOKUP TABLES

### Phase Exit Criteria Quick Reference

| Phase | Must Have | Signed By |
|-------|-----------|-----------|
| **Discovery → Execution** | Curated evidence, requirement ledger, scope freeze | Evidence Lead + Spec Architect |
| **Execution → Release** | Tests, docs, transcripts, consent artifacts | Implementation Wrangler + Security Liaison |
| **Pre-Production** | All Gate 1 items (see METHOD-0005) | Governance Sentinel + Service Owner + Security Liaison |
| **30-Day Stabilization** | SLO compliance, postmortems, metrics | Service Owner + Governance Sentinel |

### Common Command Quick Reference

| Task | Command |
|------|---------|
| **Bootstrap environment** | `bash scripts/setup/bootstrap_project.sh` |
| **Run full test gate** | `bash scripts/ci/test_gate.sh` |
| **Harvest evidence** | `python tools/rjw_idd_evidence_harvester.py` |
| **Validate IDs** | `python scripts/validate_ids.py` |
| **Validate evidence** | `python scripts/validate_evidence.py --input research/evidence_index.json` |
| **Promote evidence** | `python scripts/promote_evidence.py` |
| **Create transcript scaffold** | `python tools/integration/archive_scaffold.py <slug>` |
| **Enable 3D addon** | `python scripts/addons/enable_3d_game_core.py` |
| **Enable video addon** | `python scripts/addons/enable_video_ai_enhancer.py` |
| **Run security drill** | `python scripts/sandbox/drill.py` |
| **Generate cost dashboard** | `python scripts/cost/run_weekly_dashboard.py` |

### ID Format Quick Reference

| Prefix | Format | Example | Purpose |
|--------|--------|---------|---------|
| Evidence | `EVD-####` | EVD-0001 | Evidence records |
| Requirement | `REQ-####` | REQ-0001 | Requirements |
| Specification | `SPEC-####` | SPEC-0101 | Specifications |
| Test | `TEST-####` | TEST-0001 | Test cases |
| Documentation | `DOC-####` | DOC-0001 | Documents |
| Decision | `DEC-####` | DEC-0001 | Decisions |
| Integration | `INTEG-####` | INTEG-0001 | Integration records |
| Change | `change-YYYYMMDD-##` | change-20251005-01 | Change log entries |
| Audit | `⟦audit-id:n⟧` | ⟦audit-id:1⟧ | Audit tags |

### File Location Quick Reference

| Looking For | Location |
|-------------|----------|
| **Core method docs** | `rjw-idd-methodology/core/`, `governance/`, `operations/` |
| **Specs** | `rjw-idd-starter-kit/specs/` |
| **Prompts** | `rjw-idd-starter-kit/docs/prompts/` |
| **Standards** | `rjw-idd-starter-kit/docs/standards/` |
| **Runbooks** | `rjw-idd-starter-kit/docs/runbooks/` |
| **Decisions** | `rjw-idd-starter-kit/docs/decisions/` |
| **Change log** | `rjw-idd-starter-kit/docs/change-log.md` |
| **Ledgers** | `rjw-idd-starter-kit/artifacts/ledgers/` |
| **Evidence** | `rjw-idd-starter-kit/research/` |
| **Guards** | `rjw-idd-starter-kit/tools/testing/` |
| **Scripts** | `rjw-idd-starter-kit/scripts/` |
| **Logs** | `rjw-idd-starter-kit/logs/` |
| **3D addon** | `rjw-idd-methodology/addons/3d-game-core/` |
| **Video addon** | `rjw-idd-methodology/addons/video-ai-enhancer/` |
| **Feature config** | `method/config/features.yml` |
| **Demo Project** | `examples/demo_project/` |
| **Workspace** | `workspace/` |

### Operational Metrics Quick Reference

| Metric | Target | Source |
|--------|--------|--------|
| **Uptime %** | ≥99.9% | SPEC-0801 |
| **Error Budget** | <80% consumed/month | SPEC-0801 |
| **MTBF** | >30 days | METHOD-0005 |
| **MTTR (SEV-1)** | <1 hour | METHOD-0005 |
| **Postmortem Completion** | 100% for SEV-1/2 | METHOD-0005 |
| **Deployment Success** | >95% | METHOD-0005 |
| **NPS (internal)** | >30 | SPEC-0901 |
| **NPS (customer)** | >50 | SPEC-0901 |
| **CSAT** | >4.0/5.0 | SPEC-0901 |
| **Cost Variance** | ±10% | SPEC-0602 |

### Severity Levels Quick Reference

| Level | Description | Response Time | Escalation |
|-------|-------------|---------------|------------|
| **SEV-1** | Complete outage, data loss, security breach | 5 minutes | Immediate, notify exec team in 15 min |
| **SEV-2** | Major degradation, customer impact | 15 minutes | Notify PM and customer success in 30 min |
| **SEV-3** | Minor degradation, workaround exists | 1 hour | Standard escalation |
| **SEV-4** | Cosmetic issue, no customer impact | 4 hours | No escalation |

### Cadence Quick Reference

| Activity | Frequency | Owner | Output |
|----------|-----------|-------|--------|
| **Evidence harvest** | Per research need | Evidence Lead | Raw index, curated index |
| **Test gate** | Every commit | CI/CD | Pass/fail status |
| **Stand-up** | Daily | All roles | Status, blockers |
| **SLO review** | Weekly | SRE, Service Owner | Compliance report |
| **Incident review** | Weekly | Engineering Manager | Triage decisions |
| **Cost review** | Monthly | Governance Sentinel | Dashboard, variances |
| **Living docs audit** | Monthly | Doc Steward | Gap list |
| **DR drill** | Quarterly | SRE | Drill results |
| **Security audit** | Quarterly | Security Liaison | Audit report |
| **Method review** | Quarterly | Governance Board | Method updates |

---

## 🔗 CROSS-REFERENCE MATRIX

### Method Documents → Implementation

| Method Doc | Implements Via | Validated By | Outputs |
|------------|----------------|--------------|---------|
| **METHOD-0001** | METHOD-0002, METHOD-0004 | All guards | Stage audits |
| **METHOD-0002** | Checklists in manual | validate_ids.py | Change log |
| **METHOD-0003** | Role assignments in project | Stage audits | Audit signatures |
| **METHOD-0004** | Prompts, guards, scripts | test_gate.sh | Transcripts |
| **METHOD-0005** | SPEC-0701/0801/0901/1001 | Operational metrics | SLO reports |

### Specs → Guards → Artifacts

| Spec | Enforced By | Produces | Logged In |
|------|-------------|----------|-----------|
| **SPEC-0003** | validate_evidence.py | Evidence indices | logs/rdd-harvest/ |
| **SPEC-0101** | governance_alignment_guard.py | Requirement ledger | docs/change-log.md |
| **SPEC-0201** | red_green_guard.py | Test results | logs/ci/ |
| **SPEC-0401** | (manual) | Metrics, consent | logs/operational-metrics/ |
| **SPEC-0501** | sandbox/drill.py | Security logs | logs/security/ |
| **SPEC-0602** | cost/run_weekly_dashboard.py | Cost dashboard | logs/cost/ |
| **SPEC-0701** | (manual) | Deployment logs | logs/operational-metrics/ |
| **SPEC-0801** | (manual) | SLO reports | logs/operational-metrics/ |
| **SPEC-0901** | (manual) | Satisfaction data | logs/operational-metrics/ |
| **SPEC-1001** | (manual) | DR drill results | logs/data-lifecycle/ |

### Prompts → Roles → Artifacts

| Prompt | Primary User | Creates | References |
|--------|--------------|---------|------------|
| **PROMPT-0001** | Any role | Initial plan | Specs, decisions |
| **PROMPT-0002** | Agent Conductor | Implementation plan | REQ-####, TEST-#### |
| **PROMPT-0003** | Spec Curator | Spec updates | REQ-####, EVD-#### |
| **PROMPT-0004** | Execution Wrangler | Test plans | TEST-####, REQ-#### |
| **PROMPT-0005** | Doc Steward | Doc updates | DOC-####, change_id |
| **PROMPT-0006** | Governance Sentinel | Guard checklist | All IDs |
| **PROMPT-0007** | Doc Steward | Change log entry | change_id, impacted IDs |
| **PROMPT-0008** | Governance Sentinel | Merge decision | All artifacts |

---

## 📖 USAGE PATTERNS

### Starting a New Feature
1. **Research:** Run PROMPT-0001, harvest evidence
2. **Specify:** Run PROMPT-0003, create SPEC-####
3. **Plan:** Run PROMPT-0002, update ledgers
4. **Test:** Run PROMPT-0004, create TEST-####
5. **Implement:** Write code, run guards
6. **Document:** Run PROMPT-0005, update docs
7. **Audit:** Run PROMPT-0006, verify compliance
8. **Log:** Run PROMPT-0007, add change entry
9. **Merge:** Run PROMPT-0008, final check

### Responding to an Incident
1. **Triage:** Follow DOC-0018 (general incident)
2. **Security:** If security-related, follow DOC-0016
3. **Mitigate:** Execute runbook procedures
4. **Document:** Create DEC-INCIDENT-####
5. **Postmortem:** If SEV-1/2, complete within 7 days
6. **Actions:** Track remediation in Change Log
7. **Audit:** Update stage audit log with lessons

### Adding an Add-on
1. **Decide:** Create DEC-#### for add-on selection
2. **Enable:** Run enable script (e.g., `enable_3d_game_core.py`)
3. **Configure:** Run profile setter (e.g., `set_3d_profile.py`)
4. **Document:** Add Change Log entry
5. **Audit:** Update stage audit log
6. **Verify:** Run test gate to confirm integration

### Quarterly Review Process
1. **Evidence:** Review freshness, schedule harvests
2. **SLOs:** Adjust targets based on capability
3. **Costs:** Analyze trends, identify optimization
4. **Security:** Complete audit, update runbooks
5. **DR:** Execute drill, document results
6. **Runbooks:** Review and update all operational docs
7. **Method:** Propose method updates via DEC-####
8. **Audit:** Record findings in stage audit log

---

## 🎓 LEARNING PATHS

### Path 1: Complete Beginner (Non-Technical)
1. Read: `docs/manual/novice-quickstart.md`
2. Use: `docs/prompts/PROMPT-CORE-novice-flow.md`
3. Reference: `docs/prompts/GLOSSARY.md`
4. Follow: `docs/prompts/EXAMPLE-CONVERSATIONS.md`
5. Practice: Run bootstrap with AI helper guidance

### Path 2: Technical Lead
1. Read: `docs/manual/starter-kit-manual.md`
2. Study: `rjw-idd-methodology/core/METHOD-0001-core-method.md`
3. Review: `rjw-idd-methodology/governance/METHOD-0002-phase-driver-checklists.md`
4. Assign: Roles per `METHOD-0003`
5. Implement: Follow `METHOD-0004` workflows
6. Operate: Apply `METHOD-0005` for production

### Path 3: Governance Role
1. Read: All METHOD-#### documents
2. Study: `docs/standards/DOC-0005-traceability-schema.md`
3. Master: `scripts/validate_ids.py` and all guards
4. Practice: Run `scripts/ci/test_gate.sh` locally
5. Audit: Review `logs/LOG-0001-stage-audits.md` patterns

### Path 4: Add-on Developer
1. Study: `rjw-idd-methodology/addons/<addon>/README.md`
2. Review: Add-on specs in `addons/<addon>/specs/`
3. Use: Add-on prompts in `addons/<addon>/prompts/`
4. Configure: Profile settings via set_*_profile.py
5. Integrate: CI snippets from `addons/<addon>/ci/`

---

## 🔍 TROUBLESHOOTING INDEX

### Common Issues & Solutions

| Issue | Location | Solution |
|-------|----------|----------|
| **Guards failing on fresh clone** | `docs/troubleshooting.md` | Run bootstrap script |
| **`origin/main` missing** | `docs/manual/starter-kit-manual.md` §10 | Set `RJW_BASE_REF` to first commit |
| **Evidence validation fails** | `scripts/validate_evidence.py` | Refresh evidence via harvester |
| **ID format errors** | `scripts/validate_ids.py` | Fix format per DOC-0005 |
| **Living docs guard blocks** | `docs/living-docs-reconciliation.md` | Close gaps or update status |
| **Change log guard fails** | `tools/testing/change_log_guard.py` | Add change log entry |
| **Test coverage fails** | `tools/testing/red_green_guard.py` | Add tests for changed code |
| **Add-on conflicts** | `scripts/addons/README.md` | Disable unused add-ons |
| **Decision guard fails** | DEC template | Replace `DEC-XXXX` placeholder |

### Debug Commands

```bash
# Check environment
python --version
which python3

# Verify dependencies
pip list | grep -i pytest

# Test single guard
python tools/testing/red_green_guard.py --root . --files <files>

# Verbose validation
python scripts/validate_ids.py --verbose

# Check git state
git status
git log --oneline -10

# List changed files
git diff --name-only origin/main HEAD

# Verify feature config
cat method/config/features.yml
```

---

## 📚 ADDITIONAL RESOURCES

### Documentation Files
- **Top-level README:** `/home/rolaand-jayz/Desktop/method/README.md`
- **Prompt Library Quick Access:** `/home/rolaand-jayz/Desktop/method/PROMPT-LIBRARY-QUICK-ACCESS.md` ⭐ **NEW**
- **Full Prompt Library:** `rjw-idd-starter-kit/docs/prompts/` ⭐ **START HERE FOR PROMPTS**
- **Custom Project Prompts:** `/home/rolaand-jayz/Desktop/method/project-prompts.md`
- **Master Index (This File):** `/home/rolaand-jayz/Desktop/method/RJW-IDD-MASTER-INDEX.md`
- **Copilot Instructions:** `.github/copilot-instructions.md`
- **Operational Quick Reference:** `docs/OPERATIONAL-QUICK-REFERENCE.md`
- **Contributing Guide:** `CONTRIBUTING.md`
- **IDE Setup:** `docs/ide-setup.md`
- **i18n Guide:** `docs/i18n-guide.md`
- **API Standards:** `docs/api-standards.md`
- **Troubleshooting:** `docs/troubleshooting.md`

### Git Configuration Files
- **Git Setup Standard:** `docs/standards/DOC-0021-git-setup-configuration.md` ⭐ **NEW**
- **Git Workflow Runbook:** `docs/runbooks/DOC-0022-git-workflow-runbook.md` ⭐ **NEW**
- **Sample .gitconfig:** `.github/gitconfig-sample` ⭐ **NEW**
- **Pull Request Template:** `.github/PULL_REQUEST_TEMPLATE.md` ⭐ **NEW**
- **Commit Message Helper:** `tools/git/commit_msg_helper.py` ⭐ **NEW**

### Review Documents
- `docs/reviews/CODEBASE-REVIEW-SUMMARY.md`
- `docs/reviews/CLEANUP-SUMMARY.md`
- `docs/reviews/VERIFICATION-CHECKLIST.md`
- `docs/reviews/REVIEW-COMPLETE.md`

### Status Tracking
- `docs/status/STATUS-template.md`
- `COMMIT-READY.md`
- `FINAL-STATUS.md`



---

## 🔄 VERSION HISTORY

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-10-05 | Initial comprehensive index created | System |

---

## 📞 SUPPORT & CONTACT

For methodology questions:
1. Check this index first
2. Review relevant METHOD-#### document
3. Consult GLOSSARY.md for terminology
4. Review EXAMPLE-CONVERSATIONS.md for patterns

For technical issues:
1. Check troubleshooting.md
2. Run health_check.py
3. Verify bootstrap completion
4. Review logs in logs/ directories

---

**End of RJW-IDD Master Index**

*This index is a living document. Update it when adding new methodology components, specs, or tools. Reference this document in the Change Log when updated.*
new methodology components, specs, or tools. Reference this document in the Change Log when updated.*
