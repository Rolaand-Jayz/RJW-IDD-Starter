# PROMPT-CORE — Copy-Paste Library for Level Zero Developers

This file is the safe prompt pack for people who are brand new to software. Every block below is written so you can copy it straight into your AI helper. Use the prompts in order, stay in plain language, and only move forward when the helper confirms the previous stage is complete.

## How to Use This Library
- Keep this file and `project-prompts.md` open while you work.
- Start every new helper session with the Agent Pledge.
- Follow the seven RJW-IDD stages in order: **Start → Explore → Decide → Create → Test → Record → Wrap**.
- When the helper gives you a new reusable prompt, store it in `project-prompts.md` so the next session stays consistent.
- Need an example or definition? Open `EXAMPLE-CONVERSATIONS.md` for transcripts and `GLOSSARY.md` for plain-language terms.

## Always-Use Core Prompts

### 0. Agent Pledge (send once per helper)
```text
You are my coding helper. Please:
- Use friendly, everyday words (about sixth-grade level) for the novice output.
- Follow the RJW-IDD stages: Start → Explore → Decide → Create → Test → Record → Wrap.
- For every stage response, produce TWO clearly-labeled outputs:
  1) Novice Summary — a very short, plain-language summary (2 sentences max) that a non-developer can act on.
  2) Technical Specification — a concise, actionable technical checklist or spec suitable for an advanced developer, including assumptions, required files, commands, and any data formats or IDs.
- If the human cannot or chooses not to provide needed technical details, FILL missing requirements yourself:
  - Generate missing specs, IDs, or config with reasonable defaults and explain each generated item.
  - Mark generated items with a clear tag such as [AUTO-GENERATED] and include a short rationale and confidence level (High/Medium/Low).
  - List any trade-offs, risks, and any areas that should be validated by a domain expert later.
- Always show the next prompt the human should paste to continue, and ask for confirmation before editing files.
- Offer to run safe commands (tests, setup) only after explaining them in both novice and technical terms, and wait for an explicit yes/no.
- Log any new reusable prompts into `project-prompts.md` and remind the user to save them.
If you drift away from this pledge I will resend it.
```

### 1. Start — Kickoff My Project
```text
I am starting a new RJW-IDD cycle. Help me set the mission.
- Summarise what you can see about this repo in very simple words.
- Ask me for the goal, deadline, and any rules I must follow.
- Give me the next prompt to use when you have what you need.
```

### 2. Explore — Help Me Understand
```text
We agreed on the goal. Now guide me through the Explore stage.
- List the key tasks, unknowns, and files we should check.
- Tell me what information I should gather or confirm.
- Suggest the best next prompt once we answer the open questions.
```

### 3. Decide — Lock the Plan
```text
We finished exploring. Create a simple plan.
- Summarise the steps we will take in order.
- Confirm how we know the work is done.
- Ask me to approve or adjust the plan.
- When I approve, give me the Create prompt to paste next.
```

### 4. Create — Build With Me
```text
The plan is approved. Walk me through the Create stage.
- Break the work into the smallest possible steps.
- For every step tell me exactly what to do in my editor.
- Keep checking that I am ready before you move on.
- When all edits are finished, point me to the Test prompt.
```

### 5. Test — Did We Break Anything?
```text
We finished the edits. Lead the Test stage.
- List the checks or commands to run (one at a time, simple words).
- Help me read the results.
- If something fails, guide me back to the Create stage.
- If everything passes, tell me to run the Record prompt.
```

### 6. Record — Update the Paper Trail
```text
Testing is complete. Help me record the work.
- Draft the change-log entry and any notes to add.
- Tell me which documents or specs must be updated.
- Update `docs/status/next-steps.md` with **Do Now**, **Do Next**, and **Backlog**
  items that match our wrap-up.
- Give me clean commit message text if we need it.
- When documentation is ready, send me to the Wrap prompt.
```

### 7. Wrap — Summarise and Next
```text
We are at the end of this RJW-IDD cycle. Wrap it up for me.
- Summarise what we changed in two sentences.
- List any follow-up tasks.
- Remind me where to store any new prompts or notes.
- Confirm the very next action I should take after this chat.
```

## Quick Helper Prompts
Use these anytime the helper needs a nudge.

### Check My Understanding
```text
Pause for a moment. Explain what we are doing in one short paragraph. If I look confused, slow down the steps.
```

### Break This Task Down
```text
This feels big. Please break the current task into smaller steps and wait for me to finish each one before moving on.
```

### Show Me the File Tour
```text
Give me a simple tour of the files we are about to touch. Use one sentence per file and keep the wording friendly.
```

### Reword in Plain Language
```text
Please restate your last answer using very simple words and short sentences. Avoid jargon.
```

### Stuck or Unsure
```text
I am not sure what to do next. List the last confirmed step, the current goal, and the next two tiny actions I should take.
```

### Safety Check Before Changes
```text
Before you edit anything, confirm the plan, list the files you will touch, and ask if I am ready to proceed.
```

## Logging Prompts in `project-prompts.md`
Whenever you receive a helpful prompt that fits your team or project, copy it into `project-prompts.md` using this format:
```
## Short title (use when <moment>)
<exact prompt text>
Notes: <why this helps>
```

Over time this becomes your local playbook. Start every new session by scanning that file so you can copy the right prompt quickly.
