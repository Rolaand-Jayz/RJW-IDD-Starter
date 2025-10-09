# Project Environment Templates

This directory contains template files for setting up Python environments in projects created from the RJW-IDD starter kit.

## How to Use

When creating a new project:

1. **Copy the templates you need to your project root:**
   ```bash
   # Copy the environment setup script
   cp templates/setup_project_env.sh ./
   
   # Choose ONE of these dependency management approaches:
   
   # Option A: Simple requirements.txt approach
   cp templates/requirements.txt.template requirements.txt
   cp templates/requirements-dev.txt.template requirements-dev.txt
   
   # Option B: Modern pyproject.toml approach (recommended)
   cp templates/pyproject.toml.template pyproject.toml
   ```

2. **Customize the files for your project:**
   - Edit the copied files to include YOUR project's specific dependencies
   - Update project name, description, author info in pyproject.toml
   - Uncomment and add dependencies you actually need

3. **Set up your environment:**
   ```bash
   # Run the setup script
   ./setup_project_env.sh
   
   # Or manually:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"  # if using pyproject.toml
   # OR
   pip install -r requirements-dev.txt  # if using requirements files
   ```

## Philosophy

**The starter kit should NOT impose specific dependencies on your project.**

These templates help you quickly set up a project-specific environment based on:
- What your project actually does (web, ML, games, etc.)
- Which RJW-IDD add-ons you're using (3d-game-core, video-ai-enhancer)
- Your team's preferences and standards

Each project gets its own `.venv` directory with its own dependencies.

## Add-on Specific Dependencies

- **3d-game-core:** Game development libraries (pygame, panda3d, etc.)
- **video-ai-enhancer:** Video processing libraries (opencv, pillow, etc.)

See the template files for examples and uncomment what you need.