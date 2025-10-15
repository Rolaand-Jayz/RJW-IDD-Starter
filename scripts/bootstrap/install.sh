#!/usr/bin/env bash
# Bootstrap installer that prompts for add-on selection and runs the main bootstrap.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

declare -a CREATED_AGENT_FILES=()

log_created_file() {
  local rel_path="$1"
  CREATED_AGENT_FILES+=("${rel_path}")
}

maybe_create_agents_overview() {
  local overview_file="${ROOT_DIR}/AGENTS.md"
  if [[ -f "${overview_file}" ]]; then
    return
  fi

  cat <<'EOF' > "${overview_file}"
# Repository Agents Overview

These notes are loaded by tools that support `AGENTS.md` (for example, GitHub Copilot, Cursor,
and Roo). They provide shared guardrails so every AI helper starts with the same expectations.

- Run `scripts/setup/bootstrap_project.sh` whenever dependencies or tooling change. The script
  enforces linting, tests, and governance checks described in docs/decisions.
- Prefer incremental pull requests. Reference specs from `specs/` and ADRs from `docs/decisions/`
  in commit messages and review summaries.
- Do not add generated secrets, API tokens, or credentials to the repo. Use `.env` files that stay
  local and document access in `docs/security/`.
- When you create new automation, update the relevant guard descriptions in `docs/`.
- Tests are required for every defect fix and every new feature. Use pytest with coverage and keep
  golden fixtures up to date.
- If a tool proposes changes outside the scope of the current task, pause and capture a follow-up
  ticket instead of committing speculative edits.

Review and extend these bullet points to match your team’s conventions. They are intended as a
lightweight starting point rather than a finished policy.
EOF

  echo "    - Created shared agent overview at AGENTS.md"
  log_created_file "AGENTS.md"
}

create_copilot_scaffolding() {
  echo "  • GitHub Copilot"
  local repo_file="${ROOT_DIR}/.github/copilot-instructions.md"
  local instructions_dir="${ROOT_DIR}/.github/instructions"
  mkdir -p "${instructions_dir}"

  if [[ -f "${repo_file}" ]]; then
    echo "    - Skipping .github/copilot-instructions.md (already exists)"
  else
    maybe_create_agents_overview
    cat <<'EOF' > "${repo_file}"
# GitHub Copilot Repository Instructions

## Workflow
- Always run `scripts/setup/bootstrap_project.sh` after pulling new work. It recreates the virtual
  environment, installs dependencies, and executes pytest plus governance gates.
- Summarise every assistant-generated change in the PR description and reference the related spec,
  ADR, or ticket.
- Keep commits focused. If Copilot suggests follow-up work, capture it in `docs/backlog/` or open
  a tracking issue instead of committing unrelated edits.

## Quality Gates
- Do not merge without green pytest, lint (ruff + mypy), and the governance gate. If any check fails
  the assistant must stop and surface the failure details.
- Prefer refactors that preserve behaviour to be accompanied by targeted characterization tests.

## Security & Secrets
- Never generate or store credentials in the repository. Use `.env` entries kept out of git and
  document access steps in `docs/security/`.
- Flag dependencies that introduce new native code or network services so the security review can
  sign off.

## Communication
- When updating docs, mention the impacted audience and required follow-up actions.
- Emphasise constraints (performance budgets, compatibility requirements, deployment cadence) in
  user-facing summaries.
EOF
    echo "    - Wrote .github/copilot-instructions.md"
    log_created_file ".github/copilot-instructions.md"
  fi

  local path_file="${instructions_dir}/project-baseline.instructions.md"
  if [[ -f "${path_file}" ]]; then
    echo "    - Skipping .github/instructions/project-baseline.instructions.md (already exists)"
  else
    cat <<'EOF' > "${path_file}"
---
description: Baseline workspace guidance
applyTo: "**"
---
# Baseline Guidance

- Keep generated files under `docs/auto/` unless a maintainer directs otherwise.
- When creating Python modules, wire them into the default pytest collection and add fixtures if
  they integrate with services.
- For TypeScript or frontend work, ensure `npm run lint` stays green and update Storybook stories.
- Raise TODOs with an owner and due date when deferring follow-up work.
EOF
    echo "    - Wrote .github/instructions/project-baseline.instructions.md"
    log_created_file ".github/instructions/project-baseline.instructions.md"
  fi
}

create_cursor_rules() {
  echo "  • Cursor"
  local rules_dir="${ROOT_DIR}/.cursor/rules"
  mkdir -p "${rules_dir}"
  local rule_file="${rules_dir}/00-foundations.mdc"
  if [[ -f "${rule_file}" ]]; then
    echo "    - Skipping .cursor/rules/00-foundations.mdc (already exists)"
    return
  fi

  maybe_create_agents_overview
  cat <<'EOF' > "${rule_file}"
---
name: baseline-foundations
description: Repository guardrails for Cursor
alwaysApply: true
globs:
  - "**/*"
---

# Repository Foundations

- Run `scripts/setup/bootstrap_project.sh` before edits. It ensures the virtual environment,
  linters, pytest, and governance gate are all aligned.
- Prefer `Plan` mode before editing multiple files; summarise the proposed plan referencing specs
  in `specs/` and ADRs in `docs/decisions/`.
- Keep secrets out of history. Never read or edit `.env`, `secrets/`, or credentials paths.
- When changing CI or tooling, update the documentation under `docs/` and note follow-up actions.
- After writing code, ask Cursor to generate a brief changelog entry stub in
  `templates-and-examples/templates/change-logs/`.
EOF

  echo "    - Wrote .cursor/rules/00-foundations.mdc"
  log_created_file ".cursor/rules/00-foundations.mdc"
}

create_cline_rules() {
  echo "  • Cline"
  local rules_dir="${ROOT_DIR}/.clinerules"
  mkdir -p "${rules_dir}"
  local rule_file="${rules_dir}/00-baseline.md"
  if [[ -f "${rule_file}" ]]; then
    echo "    - Skipping .clinerules/00-baseline.md (already exists)"
    return
  fi

  maybe_create_agents_overview
  cat <<'EOF' > "${rule_file}"
# RJW-IDD Baseline (Cline)

- Use Plan mode for multi-file edits; confirm the plan includes tests, docs, and governance updates
  before applying diffs.
- Treat `.venv`, `.env*`, and `secrets/` as off-limits. If context is required, describe the need
  and wait for a human to provide sanitized excerpts.
- Every change set must either add or adjust automated tests. Highlight gaps in coverage within the
  plan if a manual follow-up is unavoidable.
- When editing specs, also update the corresponding ADRs or decision logs.
- Summarise migrations or schema changes in `docs/decisions/` and tag owners for coordination.
EOF

  echo "    - Wrote .clinerules/00-baseline.md"
  log_created_file ".clinerules/00-baseline.md"
}

create_roo_rules() {
  echo "  • Roo Code"
  local rules_dir="${ROOT_DIR}/.roo/rules"
  mkdir -p "${rules_dir}"
  local rule_file="${rules_dir}/00-baseline.md"
  if [[ -f "${rule_file}" ]]; then
    echo "    - Skipping .roo/rules/00-baseline.md (already exists)"
    return
  fi

  maybe_create_agents_overview
  cat <<'EOF' > "${rule_file}"
# Roo Code Baseline Rules

- Stay within the current ticket scope; defer unrelated clean-up or feature ideas as TODO items that
  reference an owner.
- Always run pytest (and any guard scripts) after creating diffs. Report failures verbatim.
- Do not read or modify `.env*`, `secrets/`, or credential stores.
- When editing CI or scripts, ensure documentation under `docs/automation/` is updated.
- Prompt for reviewer attention whenever guardrails prevent an automatic action.
EOF

  echo "    - Wrote .roo/rules/00-baseline.md"
  log_created_file ".roo/rules/00-baseline.md"
}

create_continue_rules() {
  echo "  • Continue"
  local rules_dir="${ROOT_DIR}/.continue/rules"
  mkdir -p "${rules_dir}"
  local rule_file="${rules_dir}/00-baseline.md"
  if [[ -f "${rule_file}" ]]; then
    echo "    - Skipping .continue/rules/00-baseline.md (already exists)"
    return
  fi

  maybe_create_agents_overview
  cat <<'EOF' > "${rule_file}"
# Continue Agent Baseline

- Bootstrap the environment via `scripts/setup/bootstrap_project.sh` before making changes.
- Respect the repository layout; new docs live in `docs/`, specs in `specs/`, and ADRs in
  `docs/decisions/`.
- Do not introduce dependencies without updating the corresponding lock files and documenting the
  rationale.
- Mention required follow-up tasks in the chat output so a human can convert them into issues.
- When touching data models, add migration notes and verification steps.
EOF

  echo "    - Wrote .continue/rules/00-baseline.md"
  log_created_file ".continue/rules/00-baseline.md"
}

create_kilocode_rules() {
  echo "  • Kilo Code"
  local rules_dir="${ROOT_DIR}/.kilocode/rules"
  mkdir -p "${rules_dir}"
  local rule_file="${rules_dir}/00-baseline.md"
  if [[ -f "${rule_file}" ]]; then
    echo "    - Skipping .kilocode/rules/00-baseline.md (already exists)"
    return
  fi

  maybe_create_agents_overview
  cat <<'EOF' > "${rule_file}"
# Kilo Code Project Rules

- Treat `scripts/setup/bootstrap_project.sh` as the entry point for environment setup and testing.
- Keep cross-project conventions in sync with docs under `docs/method/`.
- Block on reviewer approval when proposed changes touch security, deployment, or pricing logic.
- Tests are mandatory for every change. If a test cannot be written, explain why and document the
  manual verification steps.
- Note performance budgets (latency, memory, frame time) when working on real-time components.
EOF

  echo "    - Wrote .kilocode/rules/00-baseline.md"
  log_created_file ".kilocode/rules/00-baseline.md"
}

create_zed_rules() {
  echo "  • Zed"
  local rules_file="${ROOT_DIR}/.rules"
  if [[ -f "${rules_file}" ]]; then
    echo "    - Skipping .rules (already exists)"
    return
  fi

  maybe_create_agents_overview
  cat <<'EOF' > "${rules_file}"
# Zed Agent Rules

- Always plan before applying edits; summarise the intent referencing specs or ADRs.
- Run pytest and linting after modifications. If failures occur, halt and report the full output.
- Avoid modifying `.env`, credential stores, or deployment secrets.
- When editing docs, update tables of contents and any cross-links.
- Prompt a reviewer if suggested changes would alter governance or compliance behaviour.
EOF

  echo "    - Wrote .rules"
  log_created_file ".rules"
}

create_gemini_assets() {
  echo "  • Gemini Code Assist"
  local gemini_dir="${ROOT_DIR}/.gemini"
  mkdir -p "${gemini_dir}"

  local config_file="${gemini_dir}/config.yaml"
  if [[ -f "${config_file}" ]]; then
    echo "    - Skipping .gemini/config.yaml (already exists)"
  else
    cat <<'EOF' > "${config_file}"
# Generated by bootstrap. Align with https://developers.google.com/gemini-code-assist/docs/customize-gemini-behavior-github
have_fun: false
code_review:
  disable: false
  comment_severity_threshold: MEDIUM
  max_review_comments: -1
  pull_request_opened:
    help: false
    summary: true
    code_review: true
    include_drafts: true
ignore_patterns: []
EOF
    echo "    - Wrote .gemini/config.yaml"
    log_created_file ".gemini/config.yaml"
  fi

  local styleguide_file="${gemini_dir}/styleguide.md"
  if [[ -f "${styleguide_file}" ]]; then
    echo "    - Skipping .gemini/styleguide.md (already exists)"
  else
    maybe_create_agents_overview
    cat <<'EOF' > "${styleguide_file}"
# Gemini Code Assist Review Styleguide

## Summary
- Reference the related ticket or ADR in every review comment.
- Start summaries with a concise risk assessment (✅ safe, ⚠️ caution, ❌ blocking).

## Coding Standards
- Python: follow black formatting, prefer dataclasses for structured data, place new fixtures under `tests/fixtures`.
- TypeScript: enforce strict null checks, keep exports named, and update Storybook stories.
- Shell: use `set -euo pipefail` and include comments above destructive commands.

## Tests
- Require pytest coverage for new logic. When modifying guards or governance scripts, update the
  simulated workflows under `ci_samples/`.
- Highlight missing tests and suggest the file path where they belong.

## Documentation
- Update the master index in `RJW-IDD-MASTER-INDEX.md` whenever new methodology artifacts are added.
- Ensure changelog stubs are appended under `templates-and-examples/templates/change-logs/`.
EOF
    echo "    - Wrote .gemini/styleguide.md"
    log_created_file ".gemini/styleguide.md"
  fi
}

create_amazonq_rules() {
  echo "  • Amazon Q Developer"
  local q_dir="${ROOT_DIR}/.amazonq/rules"
  mkdir -p "${q_dir}"
  local rule_file="${q_dir}/baseline.md"
  if [[ -f "${rule_file}" ]]; then
    echo "    - Skipping .amazonq/rules/baseline.md (already exists)"
    return
  fi

  maybe_create_agents_overview
  cat <<'EOF' > "${rule_file}"
# Amazon Q Project Rules

- Use `scripts/setup/bootstrap_project.sh` to prepare the environment before asking for changes.
- Keep changes scoped. If a request spans multiple architectural areas, propose a plan and wait for
  confirmation.
- Avoid touching `.env`, `secrets/`, or deployment credentials.
- When updating infrastructure, document the impact under `docs/operations/`.
- Provide test evidence (pytest output, guard logs) with every suggestion.
EOF

  echo "    - Wrote .amazonq/rules/baseline.md"
  log_created_file ".amazonq/rules/baseline.md"
}

create_aider_config() {
  echo "  • Aider"
  local config_file="${ROOT_DIR}/.aider.conf.yml"
  if [[ -f "${config_file}" ]]; then
    echo "    - Skipping .aider.conf.yml (already exists)"
    return
  fi

  cat <<'EOF' > "${config_file}"
## Generated by bootstrap. See https://aider.chat/docs/config/aider_conf.html for details.
model: gpt-4o-mini
weak-model: gpt-4o-mini
map-tokens: 4096
read:
  - README.md
  - CONTRIBUTING.md
  - RJW-IDD-MASTER-INDEX.md
  - docs/decisions
  - specs
watch:
  - docs
  - specs
  - templates-and-examples/templates/change-logs
editor-edit-format: diff
architect: true
auto-accept-architect: false
permissions:
  deny:
    - Read(.env)
    - Read(secrets/**)
    - Bash(rm -rf*)
EOF

  echo "    - Wrote .aider.conf.yml"
  log_created_file ".aider.conf.yml"
}

create_claude_assets() {
  echo "  • Claude Code"
  local claude_dir="${ROOT_DIR}/.claude"
  mkdir -p "${claude_dir}"

  local settings_file="${claude_dir}/settings.json"
  if [[ -f "${settings_file}" ]]; then
    echo "    - Skipping .claude/settings.json (already exists)"
  else
    cat <<'EOF' > "${settings_file}"
{
  "permissions": {
    "allow": [
      "Bash(pnpm run lint)",
      "Bash(pnpm test)",
      "Bash(python -m pytest)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./secrets/**)",
      "Bash(rm -rf*)"
    ]
  },
  "hooks": {
    "PreToolUse": {
      "Bash": "echo '[claude] executing: $CLAUDE_TOOL_COMMAND'"
    }
  }
}
EOF
    echo "    - Wrote .claude/settings.json"
    log_created_file ".claude/settings.json"
  fi

  local memory_file="${ROOT_DIR}/CLAUDE.md"
  if [[ -f "${memory_file}" ]]; then
    echo "    - Skipping CLAUDE.md (already exists)"
  else
    maybe_create_agents_overview
    cat <<'EOF' > "${memory_file}"
# Claude Memory

- Always start by summarising the request and confirming the target directories.
- After edits, run pytest and relevant guard scripts; include the command output in the response.
- Use TODO comments with owner + due date when deferring work.
- Keep credentials, API keys, and secrets out of the repository.
- When updating specs or ADRs, link them in the response so reviewers can verify the alignment.
EOF
    echo "    - Wrote CLAUDE.md"
    log_created_file "CLAUDE.md"
  fi
}

create_cody_config() {
  echo "  • Sourcegraph Cody"
  local vscode_dir="${ROOT_DIR}/.vscode"
  mkdir -p "${vscode_dir}"
  local cody_file="${vscode_dir}/cody.json"
  if [[ -f "${cody_file}" ]]; then
    echo "    - Skipping .vscode/cody.json (already exists)"
    return
  fi

  cat <<'EOF' > "${cody_file}"
{
  "$schema": "https://cody.dev/schemas/v1.0/cody.schema.json",
  "commands": {
    "run-bootstrap": {
      "description": "Run the bootstrap script and summarise the result",
      "prompt": "Execute `scripts/setup/bootstrap_project.sh` and report whether pytest, lint, and the governance gate passed. Highlight any follow-up actions.",
      "context": {
        "selection": false,
        "currentFile": false,
        "codebase": true
      }
    },
    "summarise-adr": {
      "description": "Summarise the most recent ADR for reviewers",
      "prompt": "Locate the newest document in docs/decisions, summarise the problem, decision, and consequences. Include any open questions.",
      "context": {
        "codebase": true
      }
    }
  }
}
EOF

  echo "    - Wrote .vscode/cody.json"
  log_created_file ".vscode/cody.json"
}

ask_and_generate() {
  local label="$1"
  local func_name="$2"
  local default="${3:-N}"
  local prompt_suffix="[y/N]"
  if [[ "${default}" == "Y" || "${default}" == "y" ]]; then
    prompt_suffix="[Y/n]"
  fi

  local reply
  read -r -p "Create scaffolding for ${label}? ${prompt_suffix} " reply
  if [[ -z "${reply}" ]]; then
    reply="${default}"
  fi

  case "${reply}" in
    [yY])
      "${func_name}"
      ;;
    *)
      echo "  • Skipping ${label}"
      ;;
  esac
}

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
  echo "  1. Add a change log entry in templates-and-examples/templates/change-logs/CHANGELOG-template.md"
  echo "  2. Record the add-on decision in docs/decisions/"
fi

echo ""
echo "========================================="
echo "AI agent instruction scaffolding"
echo "========================================="
echo ""
echo "This wizard can scaffold baseline instruction files for the coding agents your team uses."
echo "Each file follows the vendor guidance we collected earlier; review and customise afterwards."
echo ""

read -r -p "Generate agent instruction templates now? [y/N]: " scaffold_choice
if [[ "${scaffold_choice}" =~ ^[yY]$ ]]; then
  echo ""
  ask_and_generate "GitHub Copilot (VS Code / GitHub.com)" create_copilot_scaffolding "Y"
  ask_and_generate "Cursor" create_cursor_rules
  ask_and_generate "Cline" create_cline_rules
  ask_and_generate "Roo Code" create_roo_rules
  ask_and_generate "Continue" create_continue_rules
  ask_and_generate "Kilo Code" create_kilocode_rules
  ask_and_generate "Zed" create_zed_rules
  ask_and_generate "Gemini Code Assist (GitHub integration)" create_gemini_assets
  ask_and_generate "Amazon Q Developer" create_amazonq_rules
  ask_and_generate "Aider" create_aider_config
  ask_and_generate "Claude Code" create_claude_assets
  ask_and_generate "Sourcegraph Cody" create_cody_config
  echo ""
else
  echo "Skipping agent scaffolding."
fi

echo ""
echo "========================================="
echo "Bootstrap complete!"
echo "========================================="

if (( ${#CREATED_AGENT_FILES[@]} > 0 )); then
  echo ""
  echo "The following files were created for your review:"
  for path in "${CREATED_AGENT_FILES[@]}"; do
    echo "  - ${path}"
  done
  echo ""
  echo "Next steps:"
  echo "  • Tailor each file to your team’s conventions."
  echo "  • Commit them alongside any add-on changes."
fi
