# CI Execution Log Template

This directory stores CI/CD execution logs for audit and troubleshooting purposes.

## Log Format

Each CI run should create a log file with the naming convention:
```
ci-<workflow-name>-<date>-<run-id>.log
```

### Example Filename
```
ci-test-gate-20250103-1234567890.log
ci-lint-20250103-1234567891.log
ci-security-scan-20250103-1234567892.log
```

## Required Log Contents

### 1. Execution Metadata
```
CI Run ID: 1234567890
Workflow: test-gate
Triggered By: pull_request #123
Branch: feature/auth-implementation
Commit: a1b2c3d4e5f6
Started: 2025-01-03T14:30:00Z
Completed: 2025-01-03T14:35:00Z
Status: SUCCESS | FAILURE
```

### 2. Guard Results
```
=== Governance Guard Results ===
✓ red_green_guard: PASS (tests present)
✓ validate_ids: PASS (all IDs valid)
✓ change_log_guard: PASS (change-20250103-01)
✓ living_docs_guard: PASS (no open items)
✓ governance_alignment_guard: PASS (aligned)
```

### 3. Test Results
```
=== Test Execution ===
Collected: 11 tests
Passed: 11
Failed: 0
Skipped: 0
Coverage: 87%
Duration: 2.3s
```

### 4. Artifact Paths
```
=== Generated Artifacts ===
- Coverage Report: ./htmlcov/index.html
- Test Results: ./test-results.xml
- Lint Report: ./lint-results.txt
```

### 5. Error Details (if applicable)
```
=== Errors ===
[ERROR] test_auth.py::test_invalid_token FAILED
AssertionError: Expected None, got {'error': 'invalid'}
  File: tests/test_auth.py:45
  
[ERROR] governance_alignment_guard: Missing DEC-0015 reference
  File: specs/SPEC-0501.md:120
```

## Retention Policy

- Keep all logs for the current release cycle
- Archive logs older than 90 days
- Maintain failure logs for 1 year for audit purposes

## Cross-References

Log entries should reference:
- Change Log ID (`change-YYYYMMDD-##`)
- Pull Request number
- Relevant SPEC/REQ/TEST IDs
- Decision records (DEC-####)

---

**Example Log:** See `ci-test-gate-20250103-example.log` for a complete sample.
