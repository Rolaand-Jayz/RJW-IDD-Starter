# Tools

Helper scripts that sit outside the core workflow scripts. Highlights:
- `rjw_cli/` — starter-kit CLI helpers used by the `rjw` command.
- `integration/`, `sandbox/`, `testing/`, `cost/`, `git/` — specialised
  helpers. Each subfolder should ship its own README explaining usage.
- Stand-alone modules (`health_check.py`, `performance_benchmark.py`, etc.)
  include docstrings describing inputs/outputs.

Keep these scripts documented so novices know when to run them and what logs or
templates they touch.
