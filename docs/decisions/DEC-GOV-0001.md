---
title: Replace MCP-driven Codacy enforcement with methodology-implemented governance automation
date: 2025-10-08
id: DEC-GOV-0001
status: Accepted
---

Context
-------
An earlier instruction file required agents to call an external Codacy MCP server for automated analysis after edits. That approach is opaque to learners and enforces an external MCP dependency.

Decision
--------
We will replace the Codacy MCP enforcement with explicit, reproducible governance automation created and managed via the RJW‑IDD methodology. The automation includes local helper scripts and CI workflows; the rationale and spec are recorded in this DEC.

Consequences
------------
- Positive: Transparent, reproducible checks; better learning experience for novices; no hidden MCP dependencies.
- Negative: Losing an external managed analysis service; responsibility for maintaining local/CI checks moves to repository maintainers.

Acceptance criteria
-------------------
- A documented `docs/governance.md` exists and links to this DEC.
- A `scripts/checks/run_checks.sh` helper exists; GitHub Actions workflow `/.github/workflows/gating-ci.yml` exists and validates on PRs.
- A smoke matrix workflow (`.github/workflows/smoke-matrix.yml`) runs on push/dispatch and uploads artifacts.
- A release workflow (`.github/workflows/release.yml`) creates a starter-kit zip and sha256 on tags.
- A functional spec `specs/SPEC-GOV-functional.md` exists and is referenced by this DEC.

