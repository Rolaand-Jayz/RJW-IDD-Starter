# RJW-IDD Starter Kit

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

This repository packages the RJW-IDD workflow as a developer-friendly starter.
It provides guard scripts, prompt packs, decision/spec scaffolds, logging and
change-log templates, and a lightweight tutorial system that demonstrates how
to use the starter in real development workflows.

Key differences in this branch (v0.1.1-alpha):
- The "bonus" tutorial is now a dynamic, agent-driven experience (see
  `tutorials/bonus-90-minute-win.md`). The tutorial is an execution framing
  and educational guide; the actual work is performed through agent-driven
  interactions and repository artifacts (decisions, specs, logs) rather than
  pre-baked code samples.
- The canonical bootstrap/installer is `scripts/bootstrap/install.sh`. The
  tutorial and onboarding now reference that script instead of any auxiliary
  helper scripts. Run the canonical installer to prepare the environment and
  enable add-ons.
- Modes have been standardized to: `Turbo`, `YOLO`, and `Strict` (strict is the
  deliberate/approval-first workflow). These maps to prompt packs and guard
  behavior rather than hard-coded runtime behavior.
- The CI workflow no longer uses an unpinned third-party Codecov GitHub Action
  by default; the test gate was adjusted to avoid unpinned third-party actions
  and comply with secure defaults.

## Modes & Activation
The starter bundles three prompt packs and operational modes. Modes are
semantics for the agent and prompt packs (they do not bypass governance unless
explicitly configured): `Turbo`, `YOLO`, and `Strict`.

- `Turbo` — high velocity. Agent proposes and implements with fewer interactive
  confirmation points; good for experienced developers who want fast iteration.
- `YOLO` — maximal velocity. Agent runs the research→spec→implement cycle, and
  you review results post-implementation. Suitable for demonstration runs or
  learning by example.
- `Strict` — conservative mode. Agent presents research and options; you must
  explicitly approve each phase transition (Research → Decision → Spec →
  Implement → Verify).

Activation is primarily done via chat or configuration toggles; consult the
manual for how to wire your assistant to the local prompt packs and guards.

## Quick Start
1. **Copy the kit** into an empty repository and commit the baseline.
2. **Set up tooling**:
   - Use the canonical bootstrap/installer to prepare dependencies and select
     optional add-ons:

```bash
chmod +x scripts/bootstrap/install.sh
bash scripts/bootstrap/install.sh
```

   - Optionally run `scripts/setup/bootstrap_project.sh` to create a virtualenv
     and smoke-test guard scripts (recommended for CI parity).
3. **Read the manual** in `manual/starter-kit-manual.md` for roles, cadence, and
   FAQs.
4. **Brief your assistant** with `docs/prompts/user/starter-briefing.md` and
   keep `docs/prompts/agent/guardrails.md` handy.
5. **Plan your first cycle**:
   - Copy templates from `templates-and-examples/templates/` (decisions, specs,
     runbooks, change logs, logs, research JSON, tests, status updates).
   - Compare with the matching examples in `templates-and-examples/good/` and
     anti-patterns in `templates-and-examples/bad/`.
6. **Track evidence** using the blank files in `research/` and record harvests
   with the log templates.
7. **Document everything**: decisions, specs, runbooks, standards, change log,
   and status entries all link together by file path (no numeric IDs).

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
