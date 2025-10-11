#!/usr/bin/env bash

# --- RJW-IDD Reality Checker ---
#
# This script checks the status of the repository to verify which
# core components, optional add-ons, and project artefacts are present.

set -euo pipefail

# Helper function to print status
check_path() {
  local path="$1"
  local description="$2"
  local status="✅ Found"
  local optional_note=""

  if [[ "$path" == *"(optional)" ]]; then
    path="${path// (optional)/}"
    optional_note=" (Optional)"
  fi

  if [ ! -e "$path" ]; then
    status="❌ Missing"
  fi

  printf "% -50s %s %s\n" "$description" "$status" "$optional_note"
}

echo "--- RJW-IDD Repository Status ---"
echo ""

echo "Core Methodology:"
check_path "rjw-idd-methodology" "RJW-IDD Methodology"
check_path "rjw-idd-starter-kit" "RJW-IDD Starter Kit"
echo ""

echo "Project Artefacts:"
check_path "workspace" "Project Workspace"
check_path "workspace/decisions" "Decisions"
check_path "workspace/specs" "Specifications"
echo ""

echo "Optional Add-ons:"
check_path "rjw-idd-methodology/addons/3d-game-core (optional)" "3D Game Core Add-on"
check_path "rjw-idd-methodology/addons/video-ai-enhancer (optional)" "Video AI Enhancer Add-on"
echo ""

echo "Key Scripts & Config:"
check_path ".github/workflows/gating-ci.yml" "CI Workflow"
check_path "rjw-idd-starter-kit/scripts/ci/test_gate.sh" "CI Test Gate Script"
check_path "rjw-idd-starter-kit/pyproject.toml" "Python Project Config"
check_path ".pre-commit-config.yaml" "Pre-commit Hooks"
echo ""
echo "Check complete."
