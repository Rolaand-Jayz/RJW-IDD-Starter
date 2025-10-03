# RJW-IDD Troubleshooting Guide

This guide helps diagnose and resolve common issues when working with RJW-IDD projects.

## Quick Diagnosis

Run this command to check your environment:

```bash
python tools/health_check.py
```

## Common Issues and Solutions

### 1. Python Environment Issues

#### Virtual Environment Not Activated

**Symptoms:**

- `ModuleNotFoundError` for installed packages
- Python interpreter shows system path instead of `.venv`

**Solutions:**


```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Verify activation
which python  # Should show .venv/bin/python
python -c "import sys; print(sys.executable)"
```

#### Dependencies Not Installed

**Symptoms:**

- Import errors for `pytest`, `ruff`, `black`, etc.
- Tools not found in PATH

**Solutions:**


```bash
# Install dependencies
pip install -r requirements-dev.txt

# Or reinstall everything
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
```

### 2. Testing Issues

#### Tests Not Running

**Symptoms:**

- `pytest` command not found
- No tests discovered

**Solutions:**


```bash
# Check pytest installation
python -m pytest --version

# Run tests explicitly
python -m pytest tests/ -v

# Check test discovery
python -m pytest --collect-only tests/
```

#### Test Failures

**Symptoms:**

- Tests failing unexpectedly
- Import errors in test files

**Solutions:**


```bash
# Run specific test
python -m pytest tests/guards/test_red_green_guard.py::TestContainsTestPath::test_detects_test_directory -v

# Debug imports
python -c "import tools.testing.red_green_guard; print('Import successful')"

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### 3. Linting and Formatting Issues

#### Ruff/MyPy Errors

**Symptoms:**

- Linting fails with import errors
- Type checking reports missing modules

**Solutions:**


```bash
# Check tool versions
ruff --version
mypy --version
black --version

# Run individual tools
ruff check tools/
mypy tools/
black --check tools/

# Fix formatting
black tools/
ruff check --fix tools/
```

#### Pre-commit Hook Failures

**Symptoms:**

- Git commits blocked by pre-commit hooks
- Hook runs fail with errors

**Solutions:**


```bash
# Run hooks manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

### 4. Git and Version Control Issues

#### Git History Issues

**Symptoms:**

- Guards fail with "no git history"
- Branch comparison errors

**Solutions:**


```bash
# Check git status
git status
git log --oneline -10

# Set comparison branch
export RJW_BASE_REF=origin/main
export RJW_HEAD_REF=HEAD

# Run guard manually
python -m tools.testing.red_green_guard --files $(git diff --name-only HEAD~1)
```

#### Change Log Validation Errors

**Symptoms:**

- Commits rejected for missing change log entries
- Invalid change log format

**Solutions:**


```bash
# Check change log format
head -20 docs/change-log.md

# Add missing entry
# Format: change-YYYYMMDD-## - Description
echo "change-$(date +%Y%m%d)-01 - Fixed issue description" >> docs/change-log.md
```

### 5. Docker and Container Issues

#### Container Build Failures

**Symptoms:**

- Docker build fails
- Missing dependencies in container

**Solutions:**


```bash
# Build with no cache
docker build --no-cache -t rjw-idd .

# Check build logs
docker build -t rjw-idd . 2>&1 | tee build.log

# Run container
docker run -it --rm rjw-idd bash
```

#### Volume Mount Issues

**Symptoms:**

- File changes not reflected in container
- Permission errors

**Solutions:**


```bash
# Check volume mounts
docker run -v $(pwd):/app -it rjw-idd bash

# Fix permissions
sudo chown -R $USER:$USER .
```

### 6. Performance Issues

#### Slow Test Runs

**Symptoms:**

- Tests take too long to execute
- CI/CD pipelines timeout

**Solutions:**


```bash
# Run tests in parallel
python -m pytest tests/ -n auto

# Profile tests
python -m pytest tests/ --durations=10

# Run specific slow tests
python -m pytest tests/ -k "slow" --tb=short
```

#### Memory Issues

**Symptoms:**

- Out of memory errors
- Tests fail with memory exhaustion

**Solutions:**


```bash
# Check memory usage
python -c "import psutil; print(f'Memory: {psutil.virtual_memory()}')"

# Run with less parallelism
python -m pytest tests/ -n 2

# Profile memory usage
python -m memory_profiler tools/rjw_idd_evidence_harvester.py
```

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
