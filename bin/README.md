# RJW Bin Utilities

This directory ships command line helpers that novices can run without
remembering long shell commands. The `rjw` Python entrypoint wraps the
most common starter kit actions:

- `rjw init` — create a local virtual environment and print activation steps.
- `rjw guard` — run the governance gate (`scripts/checks/run_checks.sh`).
- `rjw check-ledgers` — validate requirement/test ledgers when the script
  is present.
- `rjw mcp-scan` — probe for available MCP/agent CLIs to let the assistant
  know which tools are installed.

Keep this folder limited to intentionally exposed helpers; anything experimental
or project-specific should live under `tools/` instead so learners are not
overwhelmed.
