# Copilot Instructions

## Repo map
- Root kit lives in `rjw-idd-starter-kit/`; copy or adapt this tree when shipping a new project.
- `rjw-idd-methodology/` is doctrine: edit only when a new decision (`DEC-####`) justifies changing the method. Reference it from deliverables instead of inlining content.
- Add-ons under `rjw-idd-methodology/addons/` extend the method (e.g., `video-ai-enhancer/` quality gates) and ship reusable CI snippets; pull them in deliberately.
- The top-level `method/` directory holds shared feature toggles (`config/features.yml`) for tooling experiments.

## Template boundaries
- Ship the starter kit pristine: leave placeholder tables such as `docs/change-log.md`, `artifacts/ledgers/*.csv`, and `specs/*.md` untouched so downstream projects can fill them after copying.
- Use `rjw-idd-starter-kit/docs/manual/starter-kit-manual.md` for the end-to-end bring-up checklist, guard explanations, and role expectations.
- Sample scaffolds (`workspace/`, `ci_samples/`) illustrate expected artefacts; treat them as documentation rather than editable inputs.

## When you change things
- Every material update gets a new `change-YYYYMMDD-##` row in `rjw-idd-starter-kit/docs/change-log.md`, linked to affected IDs and integration artifacts.
- Specs live in `rjw-idd-starter-kit/specs/`; use the templates and keep IDs aligned with `artifacts/ledgers/requirement-ledger.csv` and `test-ledger.csv`.
- Decisions stay in `rjw-idd-starter-kit/docs/decisions/` using `rjw-idd-methodology/templates/PROJECT-DEC-template.md`; cross-link evidence (`EVD-####`), requirements (`REQ-####`), and tests (`TEST-####`).
- Integration work should create a transcript bundle via `tools/integration/archive_scaffold.py` and log its path in the Change Log.

## Local workflows
- Bootstrap the dev environment from repository root with:
  - `bash rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh` (honors `PYTHON_BIN` if you need a specific interpreter).
- Day-to-day: work inside `rjw-idd-starter-kit/`, activate `.venv`, then run `pytest` followed by `bash scripts/ci/test_gate.sh` to mirror CI.
- Guard scripts assume the Git history includes `origin/main`; set `RJW_BASE_REF`/`RJW_HEAD_REF` when diffing other ranges.

## Governance guards
- `scripts/ci/test_gate.sh` chains the method requirements:
  - `tools/testing/red_green_guard.py` enforces red→green test flow.
  - `scripts/validate_ids.py` ensures ledgers, specs, and Change Log stay consistent.
  - `scripts/validate_evidence.py` (auto-runs when research assets move) rejects evidence older than 14 days.
  - `tools/testing/change_log_guard.py` blocks missing Change Log rows; `living_docs_guard.py` forces documentation updates; `governance_alignment_guard.py` checks decision/spec linkage.
- Keep guard fixtures synchronized with the tests under `rjw-idd-starter-kit/tests/guards/` when behaviour changes.

## Evidence & prompts
- Evidence configuration lives in `research/evidence_tasks.json`; harvest with `tools/rjw_idd_evidence_harvester.py`, curate via `scripts/promote_evidence.py`, and validate freshness through `scripts/validate_evidence.py`.
- Prompt playbooks under `docs/prompts/` drive non-coders: start with `PROMPT-0001-starter-briefing.md`, then `PROMPT-0002-implementation-coach.md` for build tasks.
- `rjw-idd-methodology/operations/METHOD-0004-ai-agent-workflows.md` enumerates role expectations; follow it when coordinating multi-agent work.

## CI hooks
- GitHub Actions workflow `.github/workflows/video-ai-enhancer.yml` can be called directly or reused; it runs add-on quality gates only when `ENABLE_RJW_VIDEO` (or a `force` input) enables them.
- Reusable snippets in `addons/*/ci/` document how to wire additional gates when integrating with downstream repos.
