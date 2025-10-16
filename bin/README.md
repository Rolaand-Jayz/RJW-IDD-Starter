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

### Mode automation

The bash (`bin/rjw`) and PowerShell (`bin/rjw.ps1`) shims back the chat
shortcuts. When someone says “Activate Turbo mode,” the assistant runs the
matching helper so nobody has to edit YAML by hand. The same commands are
available if you ever need to drive locally:

- `./bin/rjw mode turbo` – enable Turbo lane, disable YOLO, and enforce the
  config drift checker.
- `./bin/rjw mode yolo` – enable YOLO lane, disable Turbo, and re-run
  `scripts/config_enforce.py`.
- `./bin/rjw mode standard` – reset both toggles to the guarded Standard flow.
- `./bin/rjw plan` – print `docs/status/next-steps.md` so the team can update
  the shared checklist together.

On Windows, run `pwsh ./bin/rjw.ps1 <command>` for the same behaviour.

Keep this directory limited to deliberately supported helpers. Anything
experimental or project-specific should live under `tools/` so learners do not
accidentally rely on work-in-progress scripts.
