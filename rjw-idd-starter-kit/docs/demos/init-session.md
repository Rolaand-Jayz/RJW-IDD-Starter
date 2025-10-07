# Demo: RJW Init

## Scenario
Setting up a new RJW-IDD project from scratch.

## Prerequisites
- Python 3.9+ installed
- Terminal access
- Empty or new project directory

## Interactive Session

```bash
$ rjw init
RJW-IDD Project Initialization
==================================================

[1/7] Project name
Enter project name [my-rjw-project]: awesome-app
✔ Project: awesome-app

[2/7] Runtime detection
✔ Runtime detected: Python 3.11.5

[3/7] Environment setup
Create venv and install deps? [Y/n]: Y
Creating virtual environment at .venv...
✔ Virtual environment created
Installing dependencies from requirements.txt...
✔ Dependencies installed successfully

[4/7] Feature selection
Preset: default - Standard RJW-IDD project with core features

Available features:
  [1] guard - Validate agent responses
  [2] init - Project initialization
  [3] prompts-version - Prompt pack versioning
  [4] game-addin - 3D game development tools

Select features (comma-separated numbers) [1,2,3]: 1,2,3
✔ Selected features: guard, init, prompts_version

[5/7] Configuration
Write configuration files (features.yml, prompt-pack.json)? [Y/n]: Y
✔ Created method/config/features.yml
✔ Created prompt-pack.json

[6/7] Smoke tests
Run smoke tests now? [Y/n]: Y
Running smoke tests...
✔ pytest available: pytest 8.0.0

[7/7] Initialization complete
✔ Created DECISION_LOG.md

==================================================
✔ Setup complete!

Next steps:
  1. Review DECISION_LOG.md for choices made
  2. Run: rjw guard examples/ok.json
  3. Read docs/quickstart.md for workflow guidance
  4. Start with: bash scripts/setup/bootstrap_project.sh
```

## Non-Interactive Mode

```bash
$ rjw init --preset lite --noninteractive
RJW-IDD Project Initialization
==================================================

[1/7] Project name
✔ Project: my-rjw-project

[2/7] Runtime detection
✔ Runtime detected: Python 3.11.5

[3/7] Environment setup
Creating virtual environment at .venv...
✔ Virtual environment created
Installing dependencies from requirements.txt...
✔ Dependencies installed successfully

[4/7] Feature selection
Preset: lite - Lightweight project for small codebases
✔ Selected features: guard, init, prompts_version

[5/7] Configuration
✔ Created method/config/features.yml
✔ Created prompt-pack.json

[6/7] Smoke tests
Running smoke tests...
✔ pytest available: pytest 8.0.0

[7/7] Initialization complete
✔ Created DECISION_LOG.md

==================================================
✔ Setup complete!

Next steps:
  1. Review DECISION_LOG.md for choices made
  2. Run: rjw guard examples/ok.json
  3. Read docs/quickstart.md for workflow guidance
  4. Start with: bash scripts/setup/bootstrap_project.sh
```

## Created Files

After running `rjw init`, you'll have:

```
.venv/                      # Virtual environment
method/
  config/
    features.yml            # Feature configuration
prompt-pack.json            # Prompt versioning metadata
DECISION_LOG.md             # Initialization decisions
requirements.txt            # Python dependencies (if created)
```

## DECISION_LOG.md Example

```markdown
# RJW-IDD Initialization Decision Log

Date: 2025-10-07 10:30:00

## Decisions Made During Initialization

1. Project name: awesome-app
2. Runtime: Python 3.11.5
3. Created virtual environment and installed dependencies
4. Features: guard, init, prompts_version
5. Wrote features.yml and prompt-pack.json

## Rationale

All defaults chosen prioritize:
- Beginner-friendly configuration
- Reversible choices
- Safe, non-destructive operations
- Explicit confirmations for risky actions
```

## Verification

```bash
# Check CLI works
$ rjw --help

# Verify features configuration
$ cat method/config/features.yml
features:
  guard: true
  init: true
  prompts_version: true
  game_addin: false
profiles:
  lite:
    guard: true
    init: true
    prompts_version: true
    game_addin: false

# Check prompt pack
$ rjw prompts --version
rjw-prompt-pack 1.0.0 (sha256-abc123de...)
Last updated: 2025-10-07

# Run a guard test
$ rjw guard examples/ok.json
✔ Validation passed (ruleset=default, errors=0, warnings=0)
```

## Troubleshooting

### Issue: "Command not found: rjw"

**Solution**: Use full path or add to PATH
```bash
export PATH="$PWD/rjw-idd-starter-kit/bin:$PATH"
```

### Issue: "No module named 'tools.rjw_cli'"

**Solution**: Run from project root or set PYTHONPATH
```bash
cd /path/to/project
python rjw-idd-starter-kit/bin/rjw init
```

## Next Steps

1. Read quickstart: `docs/quickstart.md`
2. Review solo workflow: `docs/solo.md`
3. Run bootstrap script: `bash scripts/setup/bootstrap_project.sh`
4. Start development with prompts: `docs/prompts/`
