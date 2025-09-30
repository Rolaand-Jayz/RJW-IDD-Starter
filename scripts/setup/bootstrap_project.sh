#!/usr/bin/env bash
# Bootstrap an RJW-IDD starter-kit installation inside a fresh repository.
# - Creates a local Python virtual environment (./.venv) unless one exists.
# - Installs development dependencies from requirements-dev.txt.
# - Runs pytest to confirm guard coverage is green.
# - Executes the governance test gate with a safe fallback base ref when origin/main is unavailable.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${ROOT_DIR}/.venv"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "bootstrap: required interpreter '${PYTHON_BIN}' not found" >&2
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "bootstrap: creating virtual environment at ${VENV_DIR}" >&2
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip
if [[ -f "${ROOT_DIR}/requirements-dev.txt" ]]; then
  pip install -r "${ROOT_DIR}/requirements-dev.txt"
fi

if [[ -f "${ROOT_DIR}/pyproject.toml" ]]; then
  pip install -e "${ROOT_DIR}"
fi

echo "bootstrap: running pytest"
pytest

if [[ -d "${ROOT_DIR}/.git" ]]; then
  DEFAULT_BASE="origin/main"
  if ! git -C "${ROOT_DIR}" rev-parse --verify "${DEFAULT_BASE}" >/dev/null 2>&1; then
    DEFAULT_BASE="$(git -C "${ROOT_DIR}" rev-list --max-parents=0 HEAD 2>/dev/null || true)"
  fi
  if [[ -n "${DEFAULT_BASE}" ]]; then
    export RJW_BASE_REF="${RJW_BASE_REF:-${DEFAULT_BASE}}"
  fi
  echo "bootstrap: executing scripts/ci/test_gate.sh (RJW_BASE_REF=${RJW_BASE_REF:-unset})"
  bash "${ROOT_DIR}/scripts/ci/test_gate.sh"
else
  echo "bootstrap: no git repository detected; skipping scripts/ci/test_gate.sh (requires git diff)" >&2
fi

echo "bootstrap: complete"
