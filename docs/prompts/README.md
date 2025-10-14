# Prompt Library Overview (Level Zero Friendly)

Welcome! This folder now has two clear homes:

- `user/` — prompts a human copies into the helper (core flow, stage helpers,
  glossary, example conversations, etc.).
- `agent/` — guardrails and response templates that the assistant must follow.

Start in `user/`, then browse `agent/` when you need to tighten the helper’s
behaviour.

## Always Start Here (user/)
- `core-novice-flow.md` — full-cycle script (evidence → decision → spec → build/test → change log).
- `glossary.md` — plain-language definitions you can paste when a new term appears.
- `example-conversations.md` — transcripts showing how to run guards, capture evidence, and prep merges.

## Stage-by-Stage Support (user/)
Use these when you need focused coaching for a specific step.

- `starter-briefing.md` — gentle repo tour before the real work.
- `implementation-coach.md` — step-by-step guidance for writing code.
- `spec-translator.md` — helps convert decisions into spec updates.
- `test-navigator.md` — builds the test plan and run commands.
- `doc-sync.md` — keeps documentation, logs, and change log tidy after edits.
- `governance-audit.md` — compliance sweep before sign-off.
- `change-log-author.md` — drafts the change-log row for you.
- `merge-ready-checklist.md` — confirms everything is ready before a pull request.

## Agent Guardrails (agent/)
- `guardrails.md` — reminders that keep the helper safe, novice friendly, and in workflow order.
- `reply-template.md` — short response framing for tools and humans.

## How to Grow the Library
1. Follow the core flow prompts for every RJW-IDD cycle.
2. Ask the helper for extra prompts when you face a new pattern (bug fix, refactor, documentation-only change, etc.).
3. Paste the best ones into `project-prompts.md` so the whole team can reuse them.

## Tips for Level Zero Developers
- Keep requests short and polite. The helper will slow down if you ask it to.
- If you meet a new word, ask, "Explain that in plain language." Make it a habit.
- When the helper finishes a stage, it should tell you which prompt to paste next. If it forgets, remind it with a Quick Helper prompt from the core file.

Use this library as your menu. Over time you will know exactly which prompt to grab without reading every file.
