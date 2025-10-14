# Contributing (Novice-first)

This project welcomes contributions. The process is intentionally simple so a new developer can follow it.

Branch protections (assumed and recommended)
- Protect `main` with: required status checks (lint, tests, security), at least 1 review, and linear history.
- We recommend creating topic branches named `feature/<short-desc>` or `fix/<short-desc>`.

How to contribute
1. Fork the repo, create a branch.
2. Run local checks (see `scripts/checks/run_checks.sh`) and fix issues.
3. Open a PR with description and link to tests run.
4. At least one maintainer review is required; fix requested changes and re-run checks.

Codacy MCP CLI (optional but recommended for automated analysis):

- If you use the Codacy MCP workflows or the repository guidance, install the Codacy CLI to enable local analyses and to satisfy automated agent prompts. Install via your package manager or follow instructions at https://docs.codacy.com/.
- After installing, you can run `codacy_cli_analyze --help` to confirm installation. The agent may prompt to run `codacy_cli_analyze` when performing automated fixes.

Local MCP discovery
- The repository includes `scripts/tools/mcp_detector.py` and an `rjw mcp-scan` helper to discover operable MCP/agent CLIs on your system. Run `./bin/rjw mcp-scan` to check available CLIs and version output.

Coding standards
- Use `black`/`ruff`/`mypy` in CI — the project enforces style and type checks.

Security
- For security issues, follow `SECURITY.md`.
=== Summary ===
Total Tasks: 3
Successful: 3
Failed: 0
Total Evidence Items: 35
Raw Index Updated: research/evidence_index_raw.json
Curation Required: Yes (35 items awaiting review)

=== Validation ===
✓ Raw index JSON valid
✓ All items have required fields
✓ Timestamps within date range
✓ No duplicate URLs

=== Next Steps ===
1. Review raw evidence (scripts/promote_evidence.py)
2. Curate to evidence_index.json
3. Update requirement ledger with EVD-#### refs
4. Log harvest in Change Log (change-YYYYMMDD-##)

=== Issues/Warnings ===
[WARN] Rate limit approaching for GitHub API (15 requests remaining)
[INFO] 3 items flagged for manual review due to low relevance score
```

## Harvest Summary Template

```markdown
# Evidence Harvest Summary - <Date>

**Harvest ID:** HRV-YYYY-###  
**Date:** YYYY-MM-DD  
**Duration:** X minutes  
**Operator:** Evidence Lead

## Execution Results

| Source | Query | Items | Status |
|--------|-------|-------|--------|
| Reddit | "test failures" | 15 | ✓ Success |
| GitHub | "automation" | 8 | ✓ Success |
| HackerNews | "incidents" | 12 | ✓ Success |

**Total:** 35 items collected

## Coverage Analysis

### By Stance
- Pain Points: 18 items (51%)
- Solutions/Fixes: 12 items (34%)
- Risks/Warnings: 5 items (14%)

### By Topic
- Testing: 12 items
- Governance: 8 items
- Security: 7 items
- Operations: 5 items
- Cost: 3 items

## Quality Metrics

- **Recency:** All items within last 30 days ✓
- **Relevance:** 32/35 high relevance (91%)
- **Diversity:** 3 sources, 8 communities
- **Duplicates:** 2 items (removed)

## Curation Status

### Promoted to Curated Index
- 28 items promoted
- 5 items rejected (low relevance)
- 2 items flagged for follow-up

### Evidence IDs Assigned
- EVD-0201 through EVD-0228 (28 items)

## Insights & Gaps

### Key Findings
1. **Insight:** Practitioners struggle with test maintainability at scale
2. **Pattern:** Security postmortems reveal gaps in automated checks
3. **Trend:** Increasing focus on cost governance in AI projects

### Identified Gaps
- **Gap 1:** Insufficient evidence on deployment rollback strategies
  - **Action:** Schedule micro-harvest on "deployment failures"
  - **Owner:** Evidence Lead
  - **Due:** 2025-01-10

- **Gap 2:** Limited practitioner feedback on observability tools
  - **Action:** Add targeted Reddit search to next harvest
  - **Owner:** Spec Curator
  - **Due:** 2025-01-17

## Validation Results
```
$ python scripts/validate_evidence.py
✓ Raw index: 35 items, all valid
✓ Curated index: 28 items, all valid
✓ Freshness: 100% within 14-day cutoff
✓ Linkage: All curated items link to raw source
✓ No missing fields
```
## Change Log Entry

**Required Entry:**
```
| change-20250103-02 | 2025-01-03 | RDD harvest: 35 items collected, 28 curated; gaps identified in deployment/observability evidence | EVD-0201-0228 | Evidence Lead | harvest-summary-20250103.md |
```
## Follow-up Actions

- [ ] Update requirement ledger with new EVD refs
- [ ] Schedule gap-filling micro-harvest for deployments
- [ ] Review 5 rejected items in weekly meeting
- [ ] Update evidence_tasks.json based on gaps
- [ ] Document insights in DEC-RDD-### decision

## Audit Trail

- Raw log: `logs/rdd-harvest/harvest-20250103-full.log`
- Task config: `research/evidence_tasks.json` (commit a1b2c3d)
- Output indices: `research/evidence_index_raw.json`, `research/evidence_index.json`
- Change log: `templates-and-examples/templates/change-logs/CHANGELOG-template.md` (change-20250103-02)

---

**Status:** Complete ✓  
**Next Harvest:** 2025-01-10 (micro-harvest for deployment gaps)
```

## Retention Policy

- Harvest logs: Keep for 1 year
- Summary reports: Keep indefinitely
- Raw evidence: Archive after promotion but maintain index

## Cross-References

Every harvest should update:
- `research/evidence_index_raw.json` (all collected items)
- `research/evidence_index.json` (curated items only)
- `templates-and-examples/templates/change-logs/CHANGELOG-template.md` (new change row)
- `logs/LOG-0001-stage-audits.md` (audit reflection)

## Troubleshooting

Common issues:
- **Rate Limiting:** Reduce frequency or use API tokens
- **Low Relevance:** Refine query terms in evidence_tasks.json
- **Duplicates:** Harvester checks URLs, but manual review may be needed
- **Parsing Errors:** Update harvester for new source formats

---

**Tool:** `tools/rjw_idd_evidence_harvester.py`  
**Runbook:** `docs/runbooks/docs/runbooks/rdd-harvest-runbook.md`
# Contributing to RJW-IDD

Thank you for your interest in contributing to the Rolaand Jayz Wayz - Intelligence Driven Development (RJW-IDD) project! This guide will help you understand our workflow and make effective contributions.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Contribution Workflow](#contribution-workflow)
4. [Code Standards](#code-standards)
5. [Testing Requirements](#testing-requirements)
6. [Documentation Requirements](#documentation-requirements)
7. [Pull Request Process](#pull-request-process)
8. [Decision Records](#decision-records)
9. [Community Guidelines](#community-guidelines)

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of test-driven development
- Familiarity with governance frameworks (helpful but not required)

### Understanding RJW-IDD

Before contributing, please review:
- [README.md](README.md) - Project overview
- [METHOD-0001](rjw-idd-methodology/core/METHOD-0001-core-method.md) - Core methodology
- [Starter Kit Manual](rjw-idd-starter-kit/docs/manual/starter-kit-manual.md) - Detailed guide

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Rolaand-Jayz-Wayz-IDD.git
cd Rolaand-Jayz-Wayz-IDD
```

### 2. Bootstrap Environment

The starter-kit includes a convenience bootstrap script that performs the common setup steps:

```bash
cd rjw-idd-starter-kit
bash scripts/setup/bootstrap_project.sh
```

What the script does:
- Create a local Python virtual environment (`.venv`) if one does not exist
- Install development dependencies from `requirements-dev.txt`
- Run the test suite (`pytest`) to verify the setup
- Execute the governance test gate (CI-style guards) when a Git repository is present

Controlling the base/head refs used by the governance gate
- The test gate uses `origin/main` by default as the base ref. If your repo uses a different mainline branch or you want to test against a specific commit/branch, set the environment variables the bootstrap/CI scripts honor:
  - `RJW_BASE_REF` — base ref used for the diff (default: `origin/main`)
  - `RJW_HEAD_REF` — head ref used for the diff (default: `HEAD`)
- Examples:
  - Use a different base branch:
    ```bash
    export RJW_BASE_REF=origin/develop
    bash scripts/setup/bootstrap_project.sh
    ```
  - Use a specific commit as the base:
    ```bash
    export RJW_BASE_REF="$(git rev-list --max-parents=0 HEAD)"  # first commit as base
    bash scripts/setup/bootstrap_project.sh
    ```
  - Override head ref:
    ```bash
    export RJW_HEAD_REF=my-feature-branch
    bash scripts/setup/bootstrap_project.sh
    ```

Skipping the governance test gate for local iteration
- The bootstrap script will run the governance gate only when it detects a `.git` directory. To iterate quickly on your local machine without invoking the gate, prefer one of these safe options:

  1) Run the individual setup steps manually (recommended for local development):
    ```bash
    # from repo/rjw-idd-starter-kit
    python3 -m venv ./.venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements-dev.txt
    # optional: install editable package for local imports
    pip install -e .
    # run tests locally
    pytest
    ```
    These commands perform the same setup as the bootstrap script up to (but not including) the governance gate.

  2) If you still want to use the bootstrap script but avoid the gate for a one-off local run, run the manual steps above instead of the script. (Do not rename or delete `.git` to bypass the gate — that is destructive and not recommended.)

Why you might skip the gate locally
- The governance gate enforces change-log, ledger, spec, and test alignment. It is intentionally strict to mirror CI. Skipping it is acceptable for quick local iterations but remember to run the full bootstrap (or let CI run the gate) before opening PRs so the repo-level checks pass.

Developer note on CI / reproducibility
- CI systems should not skip the gate. Use the environment variables `RJW_BASE_REF` and `RJW_HEAD_REF` in your CI configuration if your mainline branch is not `origin/main`.
- If your initial repository clone lacks `origin/main`, the bootstrap script falls back to the repository’s first commit for diffing. You can replicate that behavior manually with:
  ```bash
  export RJW_BASE_REF="$(git rev-list --max-parents=0 HEAD)"
  bash scripts/setup/bootstrap_project.sh
  ```

### 3. Activate Environment

```bash
source rjw-idd-starter-kit/.venv/bin/activate
```


### 4. Install Pre-commit Hooks

```bash
cd rjw-idd-starter-kit
pre-commit install
```

## Contribution Workflow

RJW-IDD follows a **test-first, governance-aware** workflow:

### 1. Choose Your Contribution Type

- **Bug Fix:** Start with failing test that reproduces the bug
- **New Feature:** Start with spec update and requirement definition
- **Documentation:** Update docs alongside related code changes
- **Methodology Change:** Start with a decision record (DEC-####)

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Follow Test-First Approach

**For Code Changes:**

```bash
# 1. Write failing test FIRST
vim rjw-idd-starter-kit/tests/test_your_feature.py

# 2. Run test (should fail)
pytest rjw-idd-starter-kit/tests/test_your_feature.py

# 3. Implement minimum code to pass
vim rjw-idd-starter-kit/tools/your_feature.py

# 4. Run test again (should pass)
pytest rjw-idd-starter-kit/tests/test_your_feature.py

# 5. Refactor if needed
```

### 4. Update Documentation

**Required updates:**
- Change log entry in `templates-and-examples/templates/change-logs/CHANGELOG-template.md`
- Relevant specs in `specs/`
- Decision record if methodology changes
- Living documentation (runbooks, standards)

### 5. Run Quality Checks

```bash
# Run all tests
pytest

# Run governance guards
bash rjw-idd-starter-kit/scripts/ci/test_gate.sh

# Check code quality (auto-runs if pre-commit installed)
black rjw-idd-starter-kit/
ruff check rjw-idd-starter-kit/
```

## Code Standards

### Python Style

- **Formatter:** Black (line length: 100)
- **Linter:** Ruff
- **Type Hints:** Encouraged (mypy checks enabled)
- **Docstrings:** Required for public functions

Example:

```python
def validate_evidence(
    evidence_path: Path, 
    cutoff_days: int = 14
) -> List[str]:
    """Validate evidence index freshness.
    
    Args:
        evidence_path: Path to evidence JSON file
        cutoff_days: Maximum age of evidence in days
        
    Returns:
        List of validation errors (empty if valid)
        
    Raises:
        FileNotFoundError: If evidence file doesn't exist
    """
    # Implementation...
```{{{{
        "\"/home/rolaandjayz__/Desktop/Rolaand": true,
        "git add": true,
        "git commit": true,
        "add": true,
        "start": true,
        "green": true,
        "true": true,
        "*": true,
        "ps": true,
        "PYTHONPATH=.": true,
        "(echo": true,
        "/tmp/rve_dev_demo.log": true,
        "sed": true,
        "RVE_TORCH_AVAILABLE=1": true,
        "print(PySide6.__version__)\"": true,
        "env": true,
        "WAYLAND_DISPLAY": true,
        "XDG_SESSION_TYPE'": true,
        "python": true,
        "'PY'": true,
        "printf": true,
        "research/evidence_allowlist.txt": true,
        "printf \"# Promote all first-hand engine/networking records\\n%s\\n\" \"$(python -c \"import json\nwith open('research/evidence_index_raw.json') as f:\n data=json.load(f)\n recs=[r['evid_id'] for r in data['records'] if 'first-hand' in r.get('quality_flags',[]) and any(t in ('engine','networking') for t in r.get('tags',[]))]\n print('\\n'.join(recs))\")\" > research/evidence_allowlist.txt && sed -n '1,120p' research/evidence_allowlist.txt": {
            "approve": true,
            "matchCommandLine": true
        },
        "'id':r['evid_id'],'platform':r['platform'],'date':r['date'],'quote':r['minimal_quote'][:240]})": true,
        "Netcode": true,
        "s['id']}": true,
        "s['platform']}": true,
        "s['date']}):": true,
        "s['quote']}\"": true,
        "pytest": true,
        "bash": true,
        "pip": true,
        "ERROR": true,
        "packages)\"": true,
        "cd /home/rolaandjayz__/Desktop/method/rjw-idd-starter-kit && python -c \"\nimport re\n\n# Read the file\nwith open('docs/troubleshooting.md', 'r') as f:\n    content = f.read()\n\n# Fix all the markdown linting issues\n# Add blank lines around lists\ncontent = re.sub(r'(\\*\\*Symptoms:\\*\\*)\\n(-)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(\\*\\*Solutions:\\*\\*)\\n(```
)', r'\\1\\n\\n\\2', content)\n\n# Add blank lines around headings\ncontent = re.sub(r'(### Environment Check Script)\\n(
```)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Performance Benchmark Script)\\n(```
)', r'\\1\\n\\n\\2', content)\n\n# Write back\nwith open('docs/troubleshooting.md', 'w') as f:\n    f.write(content)\n\nprint('Fixed markdown formatting issues')\n\"": {
            "approve": true,
            "matchCommandLine": true
        },
        "cd /home/rolaandjayz__/Desktop/method/rjw-idd-starter-kit && python -c \"\nimport re\n\n# Read the file\nwith open('docs/troubleshooting.md', 'r') as f:\n    content = f.read()\n\n# Fix all markdown issues systematically\n\n# 1. Add blank lines around all lists (Symptoms and Solutions)\ncontent = re.sub(r'(\\*\\*Symptoms:\\*\\*)\\n(-)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(\\*\\*Solutions:\\*\\*)\\n(
```)', r'\\1\\n\\n\\2', content)\n\n# 2. Add blank lines around headings before code blocks\ncontent = re.sub(r'(### Environment Check Script)\\n(```
)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Performance Benchmark Script)\\n(
```)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Community Resources)\\n(1\\.)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Escalation Path)\\n(1\\.)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Diagnostic Information to Include)\\n(-)', r'\\1\\n\\n\\2', content)\n\n# 3. Add blank lines around fenced code blocks\ncontent = re.sub(r'(```\\n)(### )', r'\\1\\n\\2', content)\n\n# 4. Ensure file ends with single newline\nif not content.endswith('\\n'):\n    content += '\\n'\n\n# Write back\nwith open('docs/troubleshooting.md', 'w') as f:\n    f.write(content)\n\nprint('Fixed all markdown formatting issues')\n\"": {
            "approve": true,
            "matchCommandLine": true
        },
        "tools/health_check.py": true,
        "tools/performance_benchmark.py": true
    }r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Performance Benchmark Script)\\n(
```)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Community Resources)\\n(1\\.)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Escalation Path)\\n(1\\.)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Diagnostic Information to Include)\\n(-)', r'\\1\\n\\n\\2', content)\n\n# 3. Add blank lines around fenced code blocks\ncontent = re.sub(r'(```\\n)(### )', r'\\1\\n\\2', content)\n\n# 4. Ensure file ends with single newline\nif not content.endswith('\\n'):\n    content += '\\n'\n\n# Write back\nwith open('docs/troubleshooting.md', 'w') as f:\n    f.write(content)\n\nprint('Fixed all markdown formatting issues')\n\"": {
            "approve": true,
            "matchCommandLine": true
        },
        "tools/health_check.py": true
    }', r'\\1\\n\\n\\2', content)\n\n# 2. Add blank lines around headings before code blocks\ncontent = re.sub(r'(### Environment Check Script)\\n(```
)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Performance Benchmark Script)\\n(
```)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Community Resources)\\n(1\\.)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Escalation Path)\\n(1\\.)', r'\\1\\n\\n\\2', content)\ncontent = re.sub(r'(### Diagnostic Information to Include)\\n(-)', r'\\1\\n\\n\\2', content)\n\n# 3. Add blank lines around fenced code blocks\ncontent = re.sub(r'(```\\n)(### )', r'\\1\\n\\2', content)\n\n# 4. Ensure file ends with single newline\nif not content.endswith('\\n'):\n    content += '\\n'\n\n# Write back\nwith open('docs/troubleshooting.md', 'w') as f:\n    f.write(content)\n\nprint('Fixed all markdown formatting issues')\n\"": {
            "approve": true,
            "matchCommandLine": true
        }
    }        "matchCommandLine": true
        }
    }    result = process_feature(input_data)
        
        # Assert
        assert result.is_valid()
        assert result.output == expected_output
    
    def test_error_handling(self):
        """Should handle invalid input gracefully."""
        with pytest.raises(ValidationError):
            process_feature(invalid_input)
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/guards/test_change_log_guard.py

# With coverage
pytest --cov=tools --cov=scripts --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

## Documentation Requirements

### Change Log Entry

**Every** meaningful change requires a row in `templates-and-examples/templates/change-logs/CHANGELOG-template.md`:

```markdown
| change-20250103-01 | 2025-01-03 | Add red_green_guard test coverage | TEST-0301;DEC-0012 | Contributor | test_red_green_guard.py:pass |
```

### Spec Updates

If your change affects specifications:

1. Update relevant `specs/SPEC-####.md` file
2. Link to requirements in ledger
3. Cross-reference decision records
4. Update examples if needed

### Decision Records

For methodology changes, create `docs/decisions/DEC-####.md`:

```markdown
# DEC-0042 — Add Coverage Reporting to CI

**Decision Date:** 2025-01-03  
**Participants:** Engineering Team

## Problem Statement
No visibility into test coverage percentage, risking untested code paths.

## Outcome
**Selected:** Add pytest-cov to CI pipeline with HTML reports

**Benefits:** Track coverage trends, identify gaps, enforce minimum thresholds

## Cross-Links
- SPEC-0201-quality-gates.md
- TEST-0201
```

## Pull Request Process

### 1. Pre-submission Checklist

- [ ] Tests written FIRST and passing
- [ ] Code follows style guide (black, ruff pass)
- [ ] Documentation updated
- [ ] Change log entry added
- [ ] All governance guards passing
- [ ] No linting errors
- [ ] Commit messages are clear

### 2. Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create PR on GitHub with:

**Title:** Clear, concise description (e.g., "Add test coverage for red_green_guard")

**Description Template:**

```markdown
## Summary
[Brief description of changes]

## Motivation
[Why this change is needed]

## Changes
- Added test file: `test_red_green_guard.py`
- Updated CI workflow with coverage reporting
- Added pyproject.toml for package configuration

## Testing
- [x] All tests pass locally
- [x] Coverage > 80%
- [x] Governance guards pass

## Documentation
- [x] Change log updated (change-20250103-01)
- [x] Spec updated (if applicable)
- [x] Decision record created (if applicable)

## Cross-References
- Addresses Issue #42
- Related to SPEC-0201
- Implements DEC-0012
```

### 3. Review Process

1. **Automated Checks:** CI must pass (tests, guards, linting)
2. **Peer Review:** At least one approving review required
3. **Governance Review:** Changes to methodology require Governance Board approval
4. **Final Check:** Maintainer verifies alignment with RJW-IDD principles

### 4. Addressing Feedback

```bash
# Make requested changes
git add .
git commit -m "Address review feedback: improve error handling"
git push origin feature/your-feature-name
```

### 5. Merge

Once approved:
- Squash commits if requested
- Ensure CI is green
- Maintainer will merge

## Decision Records

### When to Create a Decision Record

Create a `DEC-####` for:
- Methodology changes
- Architectural decisions
- Tool or framework selections
- Process modifications
- Significant trade-off decisions

### Decision Record Template

Use `rjw-idd-methodology/templates/PROJECT-DEC-template.md` as your starting point.

### Decision Record Process

1. Create `DEC-####.md` in `docs/decisions/`
2. Present to Governance Board (if applicable)
3. Update Change Log with DEC reference
4. Link from affected specs/documents

## Community Guidelines

### Code of Conduct

- **Be Respectful:** Value diverse perspectives and experiences
- **Be Collaborative:** Help others learn and grow
- **Be Professional:** Keep discussions focused and constructive
- **Be Patient:** Remember everyone was new once

### Communication Channels

- **Issues:** Bug reports, feature requests
- **Discussions:** Questions, ideas, general discussion
- **Pull Requests:** Code contributions with context

### Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open an Issue with reproduction steps
- **Security:** Email security@example.com (do not open public issues)

### Beginner-Friendly Issues

Look for issues labeled:
- `good first issue` - Good for new contributors
- `documentation` - Documentation improvements
- `help wanted` - Community input needed

## Recognition

Contributors will be:
- Added to Contributors list in README
- Credited in Change Log entries
- Mentioned in release notes

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Questions?

- Read the [Starter Kit Manual](rjw-idd-starter-kit/docs/manual/starter-kit-manual.md)
- Check [existing issues](https://github.com/Rolaand-Jayz/Rolaand-Jayz-Wayz-IDD/issues)
- Open a [Discussion](https://github.com/Rolaand-Jayz/Rolaand-Jayz-Wayz-IDD/discussions)

---

**Thank you for contributing to RJW-IDD!** Your contributions help improve AI-assisted development governance for everyone.
