#!/bin/bash

# Bootstrap script for Bonus 90-Minute Win
# This script initiates the real development experience with mode selection

echo "================================"
echo "RJW-IDD Bonus 90-Minute Win"
echo "================================"
echo ""
echo "You've completed the 60-minute tutorial."
echo "Now you'll build advanced features using the real RJW-IDD framework."
echo ""
echo "Select your development mode:"
echo ""
echo "  [1] TURBO - Fast paced. Agent moves forward, you approve at checkpoints."
echo "  [2] YOLO  - Build everything. Agent implements, you review after."
echo "  [3] CLASSIC - Step by step. You decide before each action."
echo ""
read -p "Enter mode (1-3): " mode_choice

case $mode_choice in
  1)
    MODE="turbo"
    echo ""
    echo "✓ Turbo Mode selected"
    echo "  The agent will move quickly through decisions and implementations."
    echo "  You'll approve at key checkpoints."
    ;;
  2)
    MODE="yolo"
    echo ""
    echo "✓ YOLO Mode selected"
    echo "  The agent will implement features and document everything."
    echo "  You'll review the results after."
    ;;
  3)
    MODE="classic"
    echo ""
    echo "✓ Classic Mode selected"
    echo "  The agent will present options. You decide each step."
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
git commit -m "bootstrap: bonus 90-minute win mode=$MODE" || true

echo ""
echo "✓ Bootstrap complete"
echo ""
echo "Next steps:"
echo "  1. Review tutorials/bonus-90-minute-win.md for the educational framework"
echo "  2. Chat with the agent to begin the feature development process"
echo "  3. The agent will research, propose, implement, and document everything"
echo ""
echo "Ready to begin? Talk to the agent about what features you want to build."
