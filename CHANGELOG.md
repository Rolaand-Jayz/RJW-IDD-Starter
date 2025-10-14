# Starter Kit Change Log

Project-level change logs belong in your downstream repository. Copy the
template from `templates-and-examples/templates/change-logs/CHANGELOG-template.md`
to get started. This file tracks high-level updates to the starter kit itself.

## [Unreleased]
- Completed starter-kit re-org: templates/examples split, runbooks/standards refactored, prompts reorganised, advanced tooling archived in `add-ons/advanced/`.

## [1.2.0] - 2025-10-12
- Added: Demo fixtures for the RJW guard (`examples/ok.json`, `examples/bad.json`)
- Changed: Starter kit version bumped to 1.2.0 (pyproject and prompt-pack)
- Docs: Added demo pass/fail examples for guard messaging (docs/demos)
- CI: Include examples in packaging via MANIFEST.in and setuptools include-package-data
