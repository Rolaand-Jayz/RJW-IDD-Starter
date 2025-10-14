# RJW Starter Kit Helpers

This folder contains the `rjw` command-line helper that wraps the most common
starter-kit workflows so new projects do not need to remember long shell
commands.

- `rjw init` – set up a local Python virtual environment and print activation
  steps.
- `rjw guard` – run the governance checks (`scripts/checks/run_checks.sh`).
- `rjw check-ledgers` – validate requirement and test ledgers when the helper
  script is present in `scripts/`.
- `rjw mcp-scan` – detect available MCP and agent CLIs so the assistant knows
  which tools are installed locally.

Keep this directory limited to deliberately supported helpers. Anything
experimental or project-specific should live under `tools/` so learners do not
accidentally rely on work-in-progress scripts.
