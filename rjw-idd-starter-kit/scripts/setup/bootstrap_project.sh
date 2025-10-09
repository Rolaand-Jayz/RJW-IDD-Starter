#!/usr/bin/env bash
# Bootstrap an RJW-IDD project from the starter kit.
# - Creates a project-specific Python virtual environment (./.venv) unless one exists.
# - Installs development dependencies from requirements-dev.txt or pyproject.toml.
# - Runs pytest to confirm guard coverage is green.
# - Executes the governance test gate with a safe fallback base ref when origin/main is unavailable.
# 
# NOTE: This script should be copied to your PROJECT ROOT, not run from the starter kit.
# The starter kit is a template - your project should have its own environment and dependencies.
#
# - To aid local development, you may skip the governance test gate by setting
#   SKIP_RJW_TEST_GATE=1 (or 'true'/'yes') in your environment. This is intended
#   for local iteration only; CI should leave the gate enabled.
# - Use RJW_BASE_REF and RJW_HEAD_REF to override the base/head refs used for the
#   git diff when the default (origin/main) does not apply.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${ROOT_DIR}/.venv"

# Check if we're in the starter kit itself (not recommended)
if [[ "$(basename "${ROOT_DIR}")" == "rjw-idd-starter-kit" ]]; then
  echo "WARNING: You're running this from the starter kit itself." >&2
  echo "The starter kit should be COPIED to your project and customized." >&2
  echo "Each project should have its own environment and dependencies." >&2
  echo "" >&2
  echo "Recommended workflow:" >&2
  echo "1. Copy the starter kit to your new project directory" >&2
  echo "2. Copy templates/setup_project_env.sh to your project root" >&2
  echo "3. Copy and customize dependency files from templates/" >&2
  echo "4. Run ./setup_project_env.sh in your project" >&2
  echo "" >&2
  echo "Continuing anyway for development/testing purposes..." >&2
  sleep 2
fi

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

echo "bootstrap: upgrading pip" >&2
python -m pip install --upgrade pip

# Install dependencies based on what's available
if [[ -f "${ROOT_DIR}/pyproject.toml" ]]; then
  echo "bootstrap: installing project with pyproject.toml" >&2
  pip install -e "${ROOT_DIR}[dev]" 2>/dev/null || pip install -e "${ROOT_DIR}"
elif [[ -f "${ROOT_DIR}/requirements-dev.txt" ]]; then
  echo "bootstrap: installing from requirements-dev.txt" >&2
  pip install -r "${ROOT_DIR}/requirements-dev.txt"
  # Also install main requirements if they exist
  if [[ -f "${ROOT_DIR}/requirements.txt" ]]; then
    echo "bootstrap: installing from requirements.txt" >&2
    pip install -r "${ROOT_DIR}/requirements.txt"
  fi
else
  echo "WARNING: No dependency files found (pyproject.toml or requirements-dev.txt)" >&2
  echo "Consider copying templates from templates/ directory and customizing them" >&2
fi

echo "bootstrap: running pytest"
pytest

if [[ -d "${ROOT_DIR}/.git" ]]; then
  # Allow local developers to opt out of running the heavy governance gate.
  # Accepts: 1, true, yes (case-sensitive on common shells; set exact string)
  if [[ "${SKIP_RJW_TEST_GATE:-}" =~ ^(1|true|yes)$ ]]; then
    echo "bootstrap: SKIP_RJW_TEST_GATE set; skipping scripts/ci/test_gate.sh (local dev)" >&2
  else
    DEFAULT_BASE="origin/main"
    if ! git -C "${ROOT_DIR}" rev-parse --verify "${DEFAULT_BASE}" >/dev/null 2>&1; then
      DEFAULT_BASE="$(git -C "${ROOT_DIR}" rev-list --max-parents=0 HEAD 2>/dev/null || true)"
    fi
    if [[ -n "${DEFAULT_BASE}" ]]; then
      export RJW_BASE_REF="${RJW_BASE_REF:-${DEFAULT_BASE}}"
    fi
    echo "bootstrap: executing scripts/ci/test_gate.sh (RJW_BASE_REF=${RJW_BASE_REF:-unset})"
    bash "${ROOT_DIR}/scripts/ci/test_gate.sh"
  fi
else
  echo "bootstrap: no git repository detected; skipping scripts/ci/test_gate.sh (requires git diff)" >&2
fi

echo "bootstrap: complete"
