# RJW-IDD Novice Quickstart

This guide is written for people who have never built software before. Follow each step in order. Use plain language. Whenever you see a prompt block, copy it into your AI helper and wait for the reply before you move on.

## 1. Get Ready
- Pick one project goal you want to reach (for example, "show a welcome message" or "collect email addresses").
- Make sure you can open this repository in your IDE or file browser.
- Keep four files handy while you work:
  - `rjw-idd-starter-kit/docs/prompts/PROMPT-CORE-novice-flow.md` — the copy-ready prompts you will paste.
  - `rjw-idd-starter-kit/docs/prompts/AGENT-GUARDRAILS.md` — quick reminders that keep the helper friendly and on track.
  - `rjw-idd-starter-kit/docs/prompts/GLOSSARY.md` — quick definitions for any new terms.
  - `project-prompts.md` — your growing list of custom prompts made during the project.

## 2. Follow the Seven Stops
Use the stages below as a map. Do not skip forward. Each stage tells you which prompt to send and what to expect in return. Need a pause? Pick a "Quick Helper" prompt from the same core file. See `docs/prompts/EXAMPLE-CONVERSATIONS.md` for full transcripts.

1. **Start** – Set the mission. Copy the "Kickoff: Start My Project" prompt. You will get a short plan and next questions.
2. **Explore** – Understand the work. Use "Explore: Help Me Understand" to list tasks and unknowns.
3. **Decide** – Confirm the plan. Use "Decide: Lock The Plan" to agree on the next steps.
4. **Create** – Build the change. Use "Create: Build With Me". The agent will guide the edits.
5. **Test** – Make sure it works. Use "Test: Did We Break Anything?" and follow the checks.
6. **Record** – Update notes and logs. Use "Record: Update The Paper Trail" to get the change-log text and documentation reminders.
7. **Wrap** – Close the loop. Use "Wrap: Summarise And Next" to confirm what happened and list open follow-ups.

## 3. Keep The Agent On Track
Before you start, share the "Agent Pledge" prompt with every coding helper. Add any guardrails from `AGENT-GUARDRAILS.md` that fit your style (including the rule where the helper runs safe commands for you). These reminders tell the helper to:
- Speak in friendly, everyday words.
- Stick to the RJW-IDD stages above.
- Confirm plans before changing files.
- Tell you what to paste next.

If the helper forgets, resend the pledge.

## 4. Grow Your Project Prompts
Whenever the agent gives you a fresh prompt that you want to reuse:
1. Open `project-prompts.md`.
2. Add a new heading with a short name (for example, "Fix a broken test").
3. Paste the exact prompt text underneath.
4. Note when to use it ("Run this after a failed test", etc.).

This file becomes your personal library. Use it at the start of every session so you do not have to remember what worked.

## 5. Where To Learn More
- Need more detail? Read `rjw-idd-starter-kit/docs/manual/starter-kit-manual.md` but only after the core flow feels comfortable.
- Want to understand why each stage exists? Check `rjw-idd-starter-kit/docs/OPERATIONAL-QUICK-REFERENCE.md`.
- Need to translate a new word? Open `rjw-idd-starter-kit/docs/prompts/GLOSSARY.md`.

## 6. Ready-Made Prompts for Common Tasks
Copy any of these into your helper when you need them:

- **Run setup:** “Please run the bootstrap script for me. Explain what you are doing and share the results in simple words.”
- **Check a diff:** “Show me what changed in plain language before we commit.”
- **Restart the day:** “Remind me where we stopped, list the open tasks, and tell me the first prompt I should run.”
- **Record notes:** “Help me write the change-log entry and tell me which documents must be updated.”

Add more to `project-prompts.md` as you discover new patterns.

## 7. Quick Troubleshooting
- **Agent skipped a stage** – Politely ask them to return to the last finished stage and confirm the checklist.
- **Agent used confusing words** – Reply with, "Please restate that in simple words".
- **Too many tasks at once** – Ask the agent to break the plan into smaller steps and finish them one at a time.
- **Not sure what to do next** – Send the "Wrap" prompt. The agent will summarise progress and tell you the very next action.

Stay patient and move stage by stage. Once you complete the seven stops for one goal, start again for the next goal. Over time your `project-prompts.md` file will fill with shortcuts that fit how you like to work.
