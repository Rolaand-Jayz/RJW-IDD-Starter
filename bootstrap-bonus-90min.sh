#!/bin/bash

# Bootstrap script for Bonus 90-Minute Win
# Run this script to set your development mode for the bonus tutorial
# Usage: ./bootstrap-bonus-90min.sh

echo "================================"
echo "RJW-IDD Bonus 90-Minute Win"
echo "================================"
echo ""
echo "Select your development mode:"
echo ""
echo "  [1] TURBO   - Fast. Agent proposes, you approve at checkpoints."
echo "  [2] YOLO    - Full steam. Agent builds, you review after."
echo "  [3] CLASSIC - Deliberate. You decide before each major action."
echo ""
read -p "Enter mode (1-3): " mode_choice

case $mode_choice in
  1)
    MODE="turbo"
    echo ""
    echo "✓ Turbo Mode selected"
    echo "  Agent will move quickly through research, decisions, and implementations."
    echo "  You approve at key checkpoints."
    ;;
  2)
    MODE="yolo"
    echo ""
    echo "✓ YOLO Mode selected"
    echo "  Agent will research, decide, spec, and implement everything."
    echo "  You review the results and git history after."
    ;;
  3)
    MODE="classic"
    echo ""
    echo "✓ Classic Mode selected"
    echo "  Agent presents options. You make decisions before each step."
    echo "  Slower but deeper learning."
    ;;
  *)
    echo "Invalid selection. Defaulting to Turbo Mode."
    MODE="turbo"
    ;;
esac

echo ""
echo "Storing mode: $MODE"
echo "$MODE" > .rjw-idd-mode
git add .rjw-idd-mode
git commit -m "bootstrap: bonus 90-minute win - mode set to $MODE"

echo ""
echo "✓ Bootstrap complete"
echo ""
echo "Next: Chat with the agent to begin building features."
echo ""
