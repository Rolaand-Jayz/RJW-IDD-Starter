## Governance checks and automated quality gates

Purpose
-------
This document describes the explicit, methodology-aligned governance checks that run on code changes. The goal is to provide transparent, reproducible quality and security validation that is created and managed through the RJW‑IDD process (DEC → Evidence → Spec → Implementation → Tests → Runbooks → Ops).

Principles
----------
- Automation must be explicit and visible to learners (CI workflows and local scripts).
- Security scans and dependency checks should be reproducible locally and in CI.
- All governance automation is produced through a DEC and linked specs so the rationale is traceable.

What runs automatically
-----------------------
- Unit tests (pytest)
- Linting (flake8)
- Dependency vulnerability scan (pip-audit)
- Optional container/image scanning (Trivy) when building images

How this ties to the method
---------------------------
1. DEC: a governance decision (see `docs/decisions/DEC-GOV-0001.md`) records the requirement for automated checks.
2. Evidence & Spec: small evidence tasks and a `SPEC-GOV-functional.md` style entry (kept local to the decision) define acceptance criteria (which tests must pass, which scanners to run).
3. Implementation: the `scripts/checks/run_checks.sh` helper and the GitHub Actions workflow implement the automation.
4. Runbooks: `docs/runbooks/DOC-governance-runbook.md` documents how to run checks locally and remediate common failures.

How learners use it (chat-driven)
--------------------------------
- The agent will present the DEC and proposed spec in the IDE chat. Once accepted, the agent will create the workflow and the local check scripts.
- The user will run `scripts/checks/run_checks.sh` locally (after creating a venv as part of the tutorial flow). The agent will interpret failures and propose fixes in chat.

Codacy MCP & local MCP discovery
--------------------------------
- If you (or an automated agent) rely on the Codacy MCP checks, install the Codacy CLI locally so the agent can run the same analysis the MCP server would. Visit https://docs.codacy.com/ and follow the install steps for your OS. After installing, run `codacy_cli_analyze --help` to confirm it is available.
- This repository includes a conservative helper `scripts/tools/mcp_detector.py` and a wrapper command `./bin/rjw mcp-scan` which checks your PATH for known MCP/agent CLIs and attempts a harmless `--version` to test operability. The agent may ask you to run this scan; if operable MCP CLIs are detected, the agent will intelligently consider using them to improve research/code generation where appropriate.

Quick local commands (example)
```bash
# from repository root
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r rjw-idd-starter-kit/requirements-dev.txt || pip install -r rjw-idd-starter-kit/requirements.txt
bash scripts/checks/run_checks.sh
```

If you'd like different or additional scanners (safety, bandit, trivy), tell me and I will add them to the spec and CI.
