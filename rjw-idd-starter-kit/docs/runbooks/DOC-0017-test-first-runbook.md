# DOC-0017 — Test-First Guard Playbook

**Linked Requirement:** Populate with your test-first requirement ID.  
**Linked Specification:** Reference the quality gate spec governing test discipline.

## Purpose
Ensure every change introduces or updates automated tests before implementation commits merge, maintaining the RJW-IDD red→green-cycle expectation.

## Workflow
1. Before writing production code, author a failing test that describes the intended behaviour change.
2. Stage files and run `scripts/ci/test_gate.sh`; the guard fails if no test files are present in the diff.
3. Execute the test suite and observe the new test failing (red).
4. Implement the change, rerun tests until they pass (green), then refactor as needed while keeping tests in the diff.
5. Document reproduction steps, guard output, and test results in the Change Log or pull request summary.

## Automation Hooks
- `tools/testing/red_green_guard.py` inspects the diff for test file patterns (configurable via environment variables).
- `scripts/ci/entrypoint.py` integrates the guard into CI and writes logs under `logs/ci/` for audit.
- Configure `RJW_TEST_PATTERNS` if your project uses non-standard test naming conventions.

## Failure Handling
- If the guard blocks the change, pause implementation and extend/add tests before continuing.
- For refactors that legitimately introduce no behavioural change, create characterization tests capturing existing behaviour to satisfy the guard.
- Any temporary bypass requires a `DEC-####` with governance approval and a clear expiry plan.

## Audit Expectations
- Attach guard logs (for example `logs/ci/test_gate_<timestamp>.log`) to the associated Change Log entry.
- Governance Sentinel samples guard logs during audits to confirm the test-first rule remains enforced.
