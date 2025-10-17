# Contributing

This file documents the minimal contribution workflow for the RJW-IDD Starter Kit.

## Branching & PRs

- Base work on `main` with feature branches named `feat/<what>` or `fix/<what>`.
- Open a pull request against `main` with a description of the change and links to any decision/spec artifacts.

## Local checks

- Run basic checks before opening a PR:

```bash
python -m pip install -r requirements-dev.txt
pytest
# optional linters
ruff .
black --check .
mypy .
```

## Tests & CI

- The project uses GitHub Actions for unit tests. Make sure your branch passes the `test-gate` workflow.
- If you modify CI files, avoid unpinned third-party GitHub Actions; prefer pinned commit SHAs or approved vendor actions.

## Versioning & Releases

- Bump `pyproject.toml` for Python package version when releasing. Use PEP 440 compatible versioning (e.g. `0.1.1a0` for alpha).
- Tag releases using annotated git tags, e.g. `git tag -a v0.1.1-alpha -m "v0.1.1-alpha"`.

## Documentation

- Add or update `docs/` files for any feature or behavioral changes.
- Tutorials remain living doc/agent artifacts; prefer agent-driven cycles for tutorial content edits.

## How to run the agent-driven tutorial

1. Run the repository bootstrap: `bash scripts/bootstrap/install.sh`.
2. Start the guided tutorial by following `tutorials/bonus-90-minute-win.md` and interacting with the project agent.

## Contact

Open issues or reach out in the project's issue tracker with questions or to request access to additional privileged tools (if applicable).