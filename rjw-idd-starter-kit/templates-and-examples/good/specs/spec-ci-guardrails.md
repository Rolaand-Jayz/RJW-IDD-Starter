# SPEC — Continuous Integration Guardrails

## 1. Purpose
Describe the guardrails that keep the CI runway healthy for novice teams using
RJW-IDD.

## 2. Scope
- Applies to every repository built from the starter kit.
- Excludes proprietary add-ons stored under `add-ons/advanced/`.

## 3. Solution Overview
CI runs the `scripts/checks/run_checks.sh` workflow on every push. Guards block
merge when:
- change logs are missing from `templates-and-examples/templates/change-logs/`
  derivatives,
- runbooks are out-of-date with the latest evidence, or
- tests copied from `templates-and-examples/templates/tests/` fail.

## 4. Rationale
- Keeps trunk releasable so beginners can follow the manual without detours.
- Mirrors the reference methodology specs stored in
  `rjw-idd-methodology/specs/`.

## 5. Acceptance Criteria
- ✅ Every CI run reports guard results in `logs/ci/`.
- ✅ The deployment runbook references this spec by filename (no `documentation`).
- ✅ Change log entries link to the merged guard version.

## 6. Open Questions
- Should we add cost dashboards to the guard bundle?
- Do we publish guard metadata in `videos/videos.yml` once tutorials land?
