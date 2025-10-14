# Test-First Runbook

- **Owner:** Quality lead
- **Support:** Feature engineer
- **Last reviewed:** YYYY-MM-DD

## Purpose
Ensure teams write or update tests before implementing changes (red → green →
refactor).

## Preconditions
- Decision and spec sections identified.
- Target behaviour agreed upon.
- Test environment available.

## Steps
1. **Plan tests** — Use `docs/prompts/user/test-navigator.md` to list scenarios.
2. **Write failing test** — Add or update tests using
   `templates-and-examples/templates/tests/test_template.py` and run `pytest` to
   confirm failure.
3. **Implement feature** — Follow implementation coach prompt.
4. **Run tests** — Execute pytest/guards until green.
5. **Refactor** — Clean up code/tests while keeping tests green.
6. **Document** — Update change log and related runbooks/standards as needed.

## Rollback
- If tests continue to fail, revert to last green commit and reassess plan.

## References
- `templates-and-examples/good/tests/test_feature_toggle_guard.py`
- `templates-and-examples/templates/tests/test_template.py`
