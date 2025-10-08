## Governance runbook — running local checks and remediation

Purpose
-------
This runbook explains how to run local governance checks (tests, lint, dependency audits) and how to respond to common failures. It is intended for learners following the tutorial flow.

Steps
-----
1. Create & activate a venv (explicit learning step):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

2. Install developer dependencies (the agent will show the exact command in chat):

```bash
pip install -r rjw-idd-starter-kit/requirements-dev.txt || pip install -r rjw-idd-starter-kit/requirements.txt
```

3. Run the local checks helper:

```bash
bash scripts/checks/run_checks.sh
```

Remediation guidance
--------------------
- Tests failing: read the failing test output; the agent will propose minimal code edits and suggest re-running specific tests.
- Lint failures: run `flake8` locally and apply formatting or style fixes; the agent can propose automated edits.
- Dependency vulnerabilities: run `pip-audit` (the script runs it) and, if vulnerabilities are found, the agent will suggest pinned/bumped versions or alternative libraries.

Reporting
---------
The runner will produce a short summary log under `tools/governance_logs/` with a timestamp and the basic pass/fail status; this is for tutorial transcripts and auditing.
