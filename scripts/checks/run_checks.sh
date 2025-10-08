#!/usr/bin/env bash
set -euo pipefail

# Minimal local governance checks helper
# Usage: bash scripts/checks/run_checks.sh

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
echo "Running local governance checks from ${ROOT_DIR}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found; please install Python 3.8+ and try again." >&2
  exit 2
fi

if [ -z "${VIRTUAL_ENV:-}" ]; then
  echo "Warning: no virtualenv detected. It's recommended you create and activate one." >&2
fi

echo "Installing test deps (best-effort)"
pip install --upgrade pip || true
pip install pytest flake8 pip-audit || true

echo "Running unit tests (pytest)"
pytest -q || { echo "Tests failed"; exit 1; }

echo "Running linter (flake8)"
flake8 || { echo "Lint issues found"; exit 2; }

echo "Running dependency audit (pip-audit)"
if command -v pip-audit >/dev/null 2>&1; then
  pip-audit --progress none || { echo "Dependency issues found"; exit 3; }
else
  echo "pip-audit not available; skipping dependency audit (install pip-audit to enable)" >&2
fi

echo "All checks passed"
