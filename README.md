# RJW-IDD Starter Kit

> [!TIP]
> **New? Run Turbo.** Tell your assistant “Activate Turbo mode.” They’ll flip on
> the Turbo feature flag with the helper script, enforce the config, and paste
> the Turbo prompt so you start in the accelerated lane.

This kit bootstraps the RJW Intelligence Driven Development workflow in any
repository. It ships templates, examples, prompts, scripts, and documentation so
novice-friendly teams can follow the method without inheriting project history.

## Method Overview
[Read the RJW-IDD methodology](https://github.com/Rolaand-Jayz/RJW-IDD-Methodology)

RJW-IDD is a stage-driven system for pairing humans and AI safely. Every cycle
passes through seven checkpoints (Start → Explore → Decide → Create → Test →
Record → Wrap), collects evidence, and links each decision to the supporting
research and tests. The method emphasises traceability over heroics: prompt
turns and tool invocations are logged, guardrails constrain risky actions, and
living documentation is refreshed in lockstep with code. By default it assumes
beginners are at the keyboard, so instructions, prompts, and logs all use plain
language while still giving experts enough structure to enforce governance.

## About This Starter
[Explore this starter kit](https://github.com/Rolaand-Jayz/RJW-IDD-Starter.git)

The starter is the method enforced. It packages the workflow into a drop-in
baseline with curated prompts, change-log templates, guard scripts, decision and
spec scaffolds, and operating manuals. Standard mode keeps the full guard suite,
YOLO adds auto-approval prompts for fast loops, and Turbo variants lighten gate
requirements while still logging every compromise. Use the starter to spin up a
fresh repo: copy only the templates you need, wire the prompts into your AI
helper, and rely on the built-in scripts to keep evidence, change logs, and
traceability aligned from the first commit.

## Modes & Activation
The starter bundles three prompt packs that you can toggle without leaving chat. Say `Activate <mode name>` and the assistant will run the helper macro to set the feature flags, enforce `scripts/config_enforce.py`, and confirm the active lane before continuing.

- **Standard mode** (default) – maps to the core novice flow prompts and enforces every RJW checkpoint. Activate with `Activate Standard mode`.
- **YOLO mode** – enables auto-approval prompts for rapid loops while still logging every guard. Activate with `Activate YOLO mode` and the assistant will flip the YOLO flag for you.
- **Turbo mode** – relaxes certain gate thresholds for short sprints, but still requires at least one verification step. Activate with `Activate Turbo mode`; the assistant handles the config update.

Need to double-check outside of chat? The same helper lives at `./bin/rjw mode <lane>` (PowerShell: `pwsh ./bin/rjw.ps1 mode <lane>`), and `./bin/rjw plan` (PowerShell: `pwsh ./bin/rjw.ps1 plan`) prints the shared Next-Steps queue. The chat command switches only the active prompt set; governance scripts, CI, and change-log expectations remain in place regardless of the mode you choose.

## Quick Start
1. **Copy the kit** into an empty repository and commit the baseline.
2. **Set up tooling**:
   - Copy the files you actually need from `templates/` (requirements,
     bootstrap scripts) and follow `templates/README.md`.
   - Run `scripts/setup/bootstrap_project.sh` to create a virtual env and smoke
     test the guards (optional but recommended).
3. **Read the manual** in `manual/starter-kit-manual.md` for roles, cadence, and
   FAQs.
4. **Run the Prompt Synthesizer** (`docs/prompts/user/prompt-synthesizer.md`) to
   tailor the assistant instructions, test scaffolds, and log templates to your
   stack.
5. **Plan your first cycle**:
   - Copy templates from `templates-and-examples/templates/` (decisions, specs,
     runbooks, change logs, logs, research JSON, tests, status updates).
   - Compare with the matching examples in `templates-and-examples/good/` and
     anti-patterns in `templates-and-examples/bad/`.
6. **Brief your assistant** with `docs/prompts/user/starter-briefing.md` and
   keep `docs/prompts/agent/guardrails.md` handy.
7. **Track evidence** using the blank files in `research/` and record harvests
   with the log templates.
8. **Document everything**: decisions, specs, runbooks, standards, change log,
   and status entries all link together by file path (no numeric IDs).

## Key Docs
| Doc | Why it matters |
| --- | --- |
[`manual/starter-kit-manual.md`](manual/starter-kit-manual.md) | Full governance, cadence, and glossary reference for every participant. |
[`docs/prompts/user/prompt-synthesizer.md`](docs/prompts/user/prompt-synthesizer.md) | Generates a project-scoped assistant prompt, smoke-test list, and logging links before you start. |
[`docs/prompts/user/batch-cycle.md`](docs/prompts/user/batch-cycle.md) | Step-by-step instructions for research, decision, spec, and approval batching in a single Turbo cycle. |
[`docs/prompts/agent/guardrails.md`](docs/prompts/agent/guardrails.md) | Guard instructions the assistant must follow while working inside your repo. |
[`docs/status/next-steps.md`](docs/status/next-steps.md) | Living queue the agent updates during each stage (Do Now / Do Next / Backlog). |

## Your First Win
Ship a single, novice-friendly improvement before touching feature work. Use
Turbo mode by default so the assistant batches approvals stage-by-stage, then
keep Standard mode on standby for stricter runs.

### Win-1 prompt (Turbo default)
```
You are the RJW-IDD Turbo lane copilot for a novice developer.
Stage-batch the work: collect research, draft the decision, and produce a
single consolidated spec for each stage before coding. Ask for approval once per
stage, never every micro-step.
Minimise surface area, protect history, and call out any extra risks before
moving on.
```

If you need the full guard cadence, switch to the Standard lane prompts in
[`docs/prompts/user/core-novice-flow.md`](docs/prompts/user/core-novice-flow.md)
after the first win.

## Directory Map
- `bin/` – novice-friendly CLI wrappers (`rjw` helper) and README.
- `docs/` – guidance split into decisions, runbooks, standards, prompts
  (`user/` + `agent/`), status notes, demos, and reference guides.
- `manual/` – extended handbook for roles and governance cadence.
- `templates-and-examples/`
  - `templates/` – copy-from blanks for every artifact type (decisions, specs,
    runbooks, standards, change logs, logs, prompts, research JSON, tests,
    status updates).
  - `good/` & `bad/` – completed examples and anti-patterns, including a demo
    project.
- `research/` – empty evidence indexes and allowlist ready for your data plus a
  README explaining how to fill them.
- `logs/` – CI, security, cost, RDD-harvest folders with READMEs; templates now
  live in `templates-and-examples/templates/log-templates/`.
- `scripts/` – bootstrap and guard scripts with a README describing each bucket.
- `tools/` – supporting utilities (integration, sandbox, testing, cost, git) with
  READMEs; keep experiments here rather than exposing them via `bin/`.
- `tests/` – intentionally empty except for a README. Copy templates/examples
  when creating project-specific suites. The legacy kit tests live under
  `artifacts/method-history/tests/` for traceability.
- `tutorials/` – TODO stubs for 15/30/60-minute Slot Car Racing walkthroughs.
- `videos/` – README outlining future video assets and the planned `videos.yml`
  manifest.
- `artifacts/` – archived ledgers, integration transcripts, legacy tutorials,
  tests, and other historical assets.
- `add-ons/advanced/` – Docker and compose files retained for teams that need
  container workflows.

## Key Workflows
- **Decisions**: copy `templates-and-examples/templates/decisions/DEC-template.md`
  and store the filled file under `docs/decisions/`. Link to relevant specs,
  runbooks, change log entries, and logs using file paths.
- **Specs**: reference the authoritative methodology specs in
  `rjw-idd-methodology/specs/`. Create project-specific specs by copying the
  template and storing them alongside your application code.
- **Runbooks & Standards**: updated documents live in `docs/runbooks/` and
  `docs/standards/` with new slug-based filenames. Each file cites the template
  it was derived from.
- **Change Log**: create `change-YYYYMMDD-topic.md` (or a table) by copying the
  template in `templates-and-examples/templates/change-logs/CHANGELOG-template.md`
  and keep it with your project docs.
- **Logs**: for every gate, copy the appropriate log template into `logs/<area>/`
  and update the stage audit using the dedicated template.
- **Status Updates**: copy the status template from
  `templates-and-examples/templates/status/` and store real stage summaries in
  `docs/status/`.

## Prompts & Manual
- `docs/prompts/user/` – novice-facing prompts for each RJW-IDD stage plus
  glossary and example conversations.
- `docs/prompts/agent/` – guardrails and reply template for the assistant.
- `manual/` – comprehensive reference; even experienced contributors should scan
  chapters on roles, cadence, and audits.

## Evidence & Research
- Keep `research/evidence_index.json`, `evidence_index_raw.json`,
  `evidence_tasks.json`, and `evidence_allowlist.txt` under version control.
- Use the research templates and examples to stay consistent.
- Record harvest runs in `logs/rdd-harvest/` and reference them from the change
  log and stage-audit log.

## Traceability Expectations
- Decisions link to specs/runbooks/tests/change-log rows.
- Specs reference decisions and evidence entries.
- Change log rows cite decisions/specs/tests/logs.
- Logs reference change log entries and decisions/specs.
- Stage audit log summarises outstanding risks at each gate.

## Archived Assets
- Legacy tutorials, tests, examples, and Docker tooling are archived under
  `artifacts/method-history/` and `add-ons/advanced/` so the starter kit stays
  lean while preserving provenance.

## Next Steps for Your Project
1. Copy the templates you need and start filling them with project-specific
   content.
2. Run the guard scripts locally (`scripts/checks/run_checks.sh`) as you build
   out your workflow.
3. Replace the TODO tutorials/videos with real content once your team records
   walkthroughs.
4. Update the prompts, runbooks, and standards to reflect your domain and link
   them back to the methodology specs.

Need more structure? Follow the prompts in `docs/prompts/user/core-novice-flow.md`
or the longer manual to walk through a full RJW-IDD cycle.
