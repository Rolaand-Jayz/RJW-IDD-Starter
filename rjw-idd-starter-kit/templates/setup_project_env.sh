#!/usr/bin/env bash
# Project Environment Setup Script
# Copy this script to your project root and customize as needed

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${PROJECT_ROOT}/.venv"

echo "Setting up Python environment for project at: ${PROJECT_ROOT}"

# Check Python is available
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "Error: Python interpreter '${PYTHON_BIN}' not found" >&2
  echo "Set PYTHON_BIN environment variable to specify a different Python" >&2
  exit 1
fi

# Create virtual environment if it doesn't exist
if [[ ! -d "${VENV_DIR}" ]]; then
  echo "Creating virtual environment at ${VENV_DIR}"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
else
  echo "Virtual environment already exists at ${VENV_DIR}"
fi

# Activate the environment
echo "Activating virtual environment"
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

# Upgrade pip
echo "Upgrading pip"
pip install --upgrade pip

# Install requirements if they exist
if [[ -f "${PROJECT_ROOT}/requirements.txt" ]]; then
  echo "Installing requirements from requirements.txt"
  pip install -r "${PROJECT_ROOT}/requirements.txt"
else
  echo "No requirements.txt found - install packages manually or create one from templates/"
fi

# Install development requirements if they exist
if [[ -f "${PROJECT_ROOT}/requirements-dev.txt" ]]; then
  echo "Installing development requirements from requirements-dev.txt"
  pip install -r "${PROJECT_ROOT}/requirements-dev.txt"
fi

echo ""
echo "Environment setup complete!"
echo "To activate in your shell, run:"
echo "  source ${VENV_DIR}/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"