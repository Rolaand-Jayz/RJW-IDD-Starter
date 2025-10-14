# Starter Kit Scripts

This directory contains the automation that keeps the RJW-IDD starter kit
usable on day one. Organise scripts by the lifecycle they support so novices
know when to run them.

- `bootstrap/` – first-run helpers (create virtualenv, copy templates, smoke
  test guards). Run these right after cloning the kit.
- `setup/` – install/upgrade tooling once the project is underway (for example
  `bootstrap_project.sh`).
- `ci/` – scripts invoked by CI pipelines (entrypoints, sanity checks).
- `cost/` – cost governance helpers (dashboards, usage audits).
- `addons/` – toggles that enable add-on packs (3d-game-core, video-ai
  enhancer). Run them when a team opts in to advanced features.
- `sandbox/` – utilities for resetting the local sandbox or running drills.
- `doc_sync.py`, `promote_evidence.py`, `validate_evidence.py`, `validate_ids.py`
  – Python modules used by the guards and CLI helpers.

When you add a new script, update this README and include a short README inside
the subfolder describing inputs/outputs plus which templates/logs it touches.
Copy `scripts/checks/` from the methodology pack if you need the full guard
suite (`run_checks.sh`) in your project repository.
