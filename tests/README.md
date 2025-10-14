# Tests

## Test-Driven Development (TDD) Workflow

This project follows a strict TDD approach for all changes. Here's the required workflow:

### 1. Red Phase: Write Failing Test
- Create a test under `tests/` that captures the new behavior or regression fix
- Use descriptive test names: `test_<feature>_<behavior>_<expected_outcome>`
- Run the test to confirm it fails
- Example: `python -m pytest tests/test_new_feature.py::test_specific_behavior -v`

### 2. Green Phase: Minimal Implementation
- Write the minimal code needed to make the test pass
- Don't over-engineer - just make it work
- Run the test again to confirm it passes

### 3. Refactor Phase: Clean Up
- Improve code quality while keeping tests green
- Run full test suite after refactoring
- Run Codacy analysis and fix any issues

### 4. Integration Checks
- Run all tests: `python -m pytest`
- Run Codacy analysis on modified files (required by repo rules)
- Fix any security issues found by trivy scans

## Test Organization

- **Unit tests**: `tests/test_*.py` - Test individual functions/classes
- **Integration tests**: `tests/integration/` - Test component interactions
- **Isolation tests**: `tests/test_isolation_model.py` - Test starter kit isolation

## Running Tests

```bash
# All tests
python -m pytest

# Specific test file
python -m pytest tests/test_example.py -v

# Specific test
python -m pytest tests/test_example.py::test_specific_function -v

# With coverage
python -m pytest --cov=. tests/
```

## Test Requirements

1. **Every behavior change must have a test**
2. **Tests must be written before implementation** (TDD)
3. **Tests must pass Codacy analysis**
4. **Integration tests for cross-component changes**

## Example TDD Cycle

```python
# 1. Write failing test
def test_new_feature_creates_expected_output():
    result = new_feature("input")
    assert result == "expected_output"

# 2. Run test (should fail)
# $ python -m pytest tests/test_new_feature.py::test_new_feature_creates_expected_output -v

# 3. Implement minimal code
def new_feature(input_data):
    return "expected_output"

# 4. Run test (should pass)
# 5. Refactor if needed
# 6. Run full test suite and Codacy checks
```

## Pre-commit Checklist

- [ ] Tests written before code changes
- [ ] All tests pass
- [ ] Codacy analysis clean for modified files
- [ ] No security vulnerabilities introduced
- [ ] Starter kit isolation maintained (if applicable)

## Legacy Note

The starter kit ships **no executable tests**. Instead, copy the templates and
examples from `templates-and-examples/templates/tests/` and
`templates-and-examples/good|bad/tests/` into your project. Document coverage
decisions in change log entries and stage audits.

Recommended workflow:
1. Plan tests with `docs/prompts/user/test-navigator.md`.
2. Copy `test_template.py` into your project repository.
3. Compare your tests with the good/bad examples before committing.
