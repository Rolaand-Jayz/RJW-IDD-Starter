#!/usr/bin/env bash
# Bootstrap installer that prompts for add-on selection and runs the main bootstrap.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

## Telemetry collection removed
## The project previously prompted for telemetry consent by running
## python -m tools.telemetry.install_prompt. This project no longer
## collects telemetry; skip that step entirely.

echo "Telemetry disabled: skipping consent prompt"
echo ""

# Add-on selection prompt
echo "========================================="
echo "RJW-IDD Add-on Selection"
echo "========================================="
echo ""
echo "RJW-IDD supports optional add-ons that extend the methodology for specific domains."
echo "Available add-ons:"
echo ""
echo "  1. 3d-game-core      - 3D game development: determinism, replay, asset/perf gates"
echo "  2. video-ai-enhancer - Real-time video enhancement: quality, latency, storage gates"
echo "  3. None              - Skip add-on installation (default)"
echo ""

read -p "Select an add-on (1-3) [3]: " addon_choice
addon_choice="${addon_choice:-3}"

case "${addon_choice}" in
  1)
    echo "Selected: 3d-game-core"
    ADDON_TO_ENABLE="3d-game-core"
    ;;
  2)
    echo "Selected: video-ai-enhancer"
    ADDON_TO_ENABLE="video-ai-enhancer"
    ;;
  3)
    echo "No add-on selected (you can enable one later)"
    ADDON_TO_ENABLE=""
    ;;
  *)
    echo "Invalid selection. Proceeding without add-on."
    ADDON_TO_ENABLE=""
    ;;
esac

echo ""
echo "========================================="
echo "Running main bootstrap..."
echo "========================================="
echo ""

# Run the main bootstrap script
bash "${ROOT_DIR}/scripts/setup/bootstrap_project.sh"

# Enable the selected add-on if any
if [[ -n "${ADDON_TO_ENABLE}" ]]; then
  echo ""
  echo "========================================="
  echo "Enabling add-on: ${ADDON_TO_ENABLE}"
  echo "========================================="
  echo ""
  
  # Activate the venv created by bootstrap_project.sh
  if [[ -f "${ROOT_DIR}/.venv/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source "${ROOT_DIR}/.venv/bin/activate"
  fi
  
  case "${ADDON_TO_ENABLE}" in
    "3d-game-core")
      python "${ROOT_DIR}/scripts/addons/enable_3d_game_core.py"
      echo ""
      read -p "Select a 3D profile (generic/first_person/third_person/isometric/platformer/driving/action_rpg/networked) [generic]: " profile_choice
      profile_choice="${profile_choice:-generic}"
      python "${ROOT_DIR}/scripts/addons/set_3d_profile.py" --profile "${profile_choice}"
      ;;
    "video-ai-enhancer")
      python "${ROOT_DIR}/scripts/addons/enable_video_ai_enhancer.py"
      echo ""
      read -p "Select a video profile (baseline/live_stream/broadcast_mastering/mobile_edge/remote_collab) [baseline]: " profile_choice
      profile_choice="${profile_choice:-baseline}"
      python "${ROOT_DIR}/scripts/addons/set_video_ai_profile.py" --profile "${profile_choice}"
      ;;
  esac
  
  echo ""
  echo "✓ Add-on ${ADDON_TO_ENABLE} enabled and configured"
  echo ""
  echo "IMPORTANT: Remember to:"
  echo "  1. Add a change log entry in docs/change-log.md"
  echo "  2. Record the add-on decision in docs/decisions/"
fi

echo ""
echo "========================================="
echo "Bootstrap complete!"
echo "========================================="

