# RJW-IDD Troubleshooting Guide

This guide helps diagnose and resolve common issues when working with RJW-IDD projects.

## Quick Diagnosis

Copy this prompt into your helper:

```
Please run `python tools/health_check.py` and explain the results in simple words.
```

The helper should run the command, share the output, and translate anything confusing.

## Level-Zero Fix Flow

1. Share the guardrails (`docs/prompts/AGENT-GUARDRAILS.md`) so the helper confirms each action and offers to run commands for you.
2. Pick the issue below that matches what you see and copy the “Ask the helper” prompt.
3. Let the helper run the suggested commands, then follow the next steps it gives you.
4. When you discover a new reusable prompt, add it to `project-prompts.md`.

## Common Issues and Solutions

### 1. Python Environment Issues

#### Virtual Environment Not Activated

**Symptoms:**

- `ModuleNotFoundError` for installed packages
- Python interpreter shows system path instead of `.venv`

**Ask the helper:** “Help me activate the virtual environment and confirm Python is using `.venv`.” The helper will run `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows), followed by `which python` and `python -c "import sys; print(sys.executable)"`, then explain the output.

#### Dependencies Not Installed

**Symptoms:**

- Import errors for `pytest`, `ruff`, `black`, etc.
- Tools not found in PATH

**Ask the helper:** “Please reinstall the project dependencies inside `.venv` and let me know when it is done.” The helper will run the install commands (including rebuilding the virtual environment if needed) and report success or errors.

### 2. Testing Issues

#### Tests Not Running

**Symptoms:**

- `pytest` command not found
- No tests discovered

**Ask the helper:** “Pytest is not finding tests. Run the detection commands and tell me what they mean.” The helper will execute `python -m pytest --version`, `python -m pytest tests/ -v`, and `python -m pytest --collect-only tests/`, explaining any failures.

#### Test Failures

**Symptoms:**

- Tests failing unexpectedly
- Import errors in test files

**Ask the helper:** “A test failed. Rerun the failing test only, restate the error in plain words, and coach me on the smallest fix.” The helper can also check imports and the Python path if modules are missing, then guide you back to the Create stage.

### 3. Linting and Formatting Issues

#### Ruff/MyPy Errors

**Symptoms:**

- Linting fails with import errors
- Type checking reports missing modules

**Ask the helper:** “Linting failed. Run the lint commands, fix what you can automatically, and summarise what is left.” The helper will run the Ruff, MyPy, and Black commands and translate any remaining errors, then point you to the next prompt.

#### Pre-commit Hook Failures

**Symptoms:**

- Git commits blocked by pre-commit hooks
- Hook runs fail with errors

**Ask the helper:** “Pre-commit blocked my commit. Run the hooks, explain any errors, and guide me through the fix.” The helper can update hooks, rerun them, and only skip as a last resort while warning you about the risks.

### 4. Git and Version Control Issues

#### Git History Issues

**Symptoms:**

- Guards fail with "no git history"
- Branch comparison errors

**Ask the helper:** “The guards say git history is missing. Check git status, set the comparison branches if needed, and rerun the guard so I know what changed.” The helper will run the git commands and report what to do next.

#### Change Log Validation Errors

**Symptoms:**

- Commits rejected for missing change log entries
- Invalid change log format

**Ask the helper:** “The guard says the change log is missing. Show me the first few lines, draft the row I need, and wait for me to confirm it’s added.” The helper will display the log, craft the entry, and remind you to run the Record stage prompts.

### 5. Docker and Container Issues

#### Container Build Failures

**Symptoms:**

- Docker build fails
- Missing dependencies in container

**Ask the helper:** “Docker build failed. Re-run the build (with `--no-cache` if needed), capture the logs, and tell me the first error in plain words.” The helper can also start the container for inspection if the build succeeds.

#### Volume Mount Issues

**Symptoms:**

- File changes not reflected in container
- Permission errors

**Ask the helper:** “The container is not seeing my files. Check the volume mount and fix any permission issues, then tell me what changed.” The helper can run the docker commands and report the results.

### 6. Performance Issues

#### Slow Test Runs

**Symptoms:**

- Tests take too long to execute
- CI/CD pipelines timeout

**Ask the helper:** “Tests are slow. Try the speed-up commands for me, explain what they do, and suggest next steps based on the output.” The helper will run the parallel and profiling options, then translate the findings.

#### Memory Issues

**Symptoms:**

- Out of memory errors
- Tests fail with memory exhaustion

**Ask the helper:** “We are running out of memory. Check how much RAM is free, try running fewer parallel tests, and show me where the memory goes.” The helper can execute the monitoring and profiling commands, then describe the findings in everyday language.

### 7. Network and API Issues

#### Evidence Harvester Failures

**Symptoms:**

- Network timeouts
- API rate limiting
- SSL certificate errors

**Solutions:**


```bash
# Check network connectivity
curl -I https://news.ycombinator.com

# Run with debug logging
python tools/rjw_idd_evidence_harvester.py --debug

# Check rate limits
# Wait and retry, or use different API keys
```

#### GitHub API Issues

**Symptoms:**

- Authentication failures
- Rate limit exceeded

**Solutions:**


```bash
# Check GitHub token
echo $GITHUB_TOKEN | head -c 10

# Test API access
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Use different token or wait for rate limit reset
```

### 8. IDE and Editor Issues

#### Extension/Plugin Problems

**Symptoms:**

- Linting not working in editor
- Formatting not applied
- Intellisense broken

**Solutions:**


```bash
# Reload editor window
# VS Code: Ctrl+Shift+P -> "Developer: Reload Window"

# Reinstall extensions
# VS Code: Extensions -> Right-click -> Uninstall -> Install

# Check settings
cat .vscode/settings.json
```

#### Python Interpreter Issues

**Symptoms:**

- Wrong interpreter selected
- Virtual environment not recognized

**Solutions:**


```bash
# Select interpreter in editor
# VS Code: Ctrl+Shift+P -> "Python: Select Interpreter"

# Check interpreter path
python -c "import sys; print(sys.executable)"

# Recreate virtual environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 9. Documentation Issues

#### Living Docs Guard Failures

**Symptoms:**

- Commits rejected for documentation issues
- Reconciliation log errors

**Solutions:**


```bash
# Check reconciliation log
cat docs/living-docs-reconciliation.md

# Update documentation
# Add missing entries to reconciliation log

# Run guard manually
python -m tools.testing.living_docs_guard
```

### 10. Security Issues

#### Dependency Vulnerabilities

**Symptoms:**

- Security scan failures
- Vulnerable package warnings

**Solutions:**


```bash
# Check for vulnerabilities
pip audit

# Update dependencies
pip install --upgrade -r requirements-dev.txt

# Check specific package
pip show <package-name>
```

## Diagnostic Tools

### Environment Check Script

```bash
#!/bin/bash
# RJW-IDD Environment Diagnostic Script

echo "=== RJW-IDD Environment Check ==="
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Directory: $(pwd)"
echo

echo "=== Python Environment ==="
python --version
which python
python -c "import sys; print('Python path:', sys.executable)"
echo

echo "=== Virtual Environment ==="
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual env active: $VIRTUAL_ENV"
else
    echo "No virtual environment active"
fi
echo

echo "=== Key Dependencies ==="
python -c "
try:
    import pytest
    print('pytest: OK')
except ImportError:
    print('pytest: MISSING')

try:
    import ruff
    print('ruff: OK')
except ImportError:
    print('ruff: MISSING')

try:
    import black
    print('black: OK')
except ImportError:
    print('black: MISSING')
"
echo

echo "=== Git Status ==="
git status --porcelain | head -10
echo

echo "=== Recent Commits ==="
git log --oneline -5
echo

echo "=== Test Status ==="
python -m pytest --version >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "pytest: Available"
    python -m pytest --collect-only tests/ 2>/dev/null | grep -c "test session starts" || echo "Test collection failed"
else
    echo "pytest: Not available"
fi
```

### Performance Benchmark Script

```python
#!/usr/bin/env python3
"""Performance benchmark for RJW-IDD tools."""

import time
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run command and measure execution time."""
    print(f"Running: {description}")
    start = time.time()

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        end = time.time()

        if result.returncode == 0:
            print(".2f"        else:
            print(".2f"            print(f"Error: {result.stderr}")
            return None

        return end - start
    except Exception as e:
        end = time.time()
        print(".2f"        return None

def main():
    """Run performance benchmarks."""
    print("=== RJW-IDD Performance Benchmarks ===")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    benchmarks = [
        ("python -m pytest tests/", "Run test suite"),
        ("ruff check tools/ scripts/", "Run Ruff linting"),
        ("black --check tools/ scripts/", "Check Black formatting"),
        ("mypy tools/ scripts/", "Run MyPy type checking"),
        ("python tools/rjw_idd_evidence_harvester.py --help", "Evidence harvester help"),
    ]

    results = {}
    for cmd, desc in benchmarks:
        duration = run_command(cmd, desc)
        if duration is not None:
            results[desc] = duration
        print()

    print("=== Summary ===")
    for desc, duration in results.items():
        print(".2f"
if __name__ == "__main__":
    main()
```

## Getting Help

### Community Resources

1. **Documentation**: Check `docs/` directory first
2. **GitHub Issues**: Search existing issues
3. **Discussions**: Use GitHub Discussions for questions
4. **Change Log**: Review recent changes in `docs/change-log.md`

### Escalation Path

1. Check this troubleshooting guide
2. Search existing issues and documentation
3. Create a new issue with diagnostic information
4. Include output from diagnostic scripts
5. Provide environment details and steps to reproduce

### Diagnostic Information to Include

When reporting issues, always include:

- Operating system and version
- Python version
- Git version and status
- Output of diagnostic script
- Steps to reproduce
- Expected vs actual behavior
- Any error messages or stack traces

This ensures faster resolution and helps improve the methodology for everyone.
