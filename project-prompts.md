# Project Prompt Library

This file is your personal prompt notebook. Keep it open while you work. When the helper gives you a reusable prompt, drop it here so the next session stays easy.

---

## 📚 FULL PROMPT LIBRARY LOCATION

**All RJW-IDD prompts are located in:**
```
rjw-idd-starter-kit/docs/prompts/
```

### Available Prompt Files:
1. **PROMPT-CORE-novice-flow.md** ⭐ START HERE
   - Agent Pledge (always use first)
   - 7-stage workflow: Start → Explore → Decide → Create → Test → Record → Wrap
   - Quick helper prompts for common needs

2. **AGENT-GUARDRAILS.md**
   - Plain language request
   - Method pledge
   - Command confirmation rules
   - Drift recovery

3. **GLOSSARY.md**
   - Plain-language definitions for RJW-IDD terms
   - Copy-paste explanations

4. **EXAMPLE-CONVERSATIONS.md**
   - Sample interactions showing how to use prompts
   - Examples for running commands, reviewing diffs

5. **PROMPT-0001-starter-briefing.md**
   - Initial repository tour and planning

6. **PROMPT-0002-implementation-coach.md**
   - Step-by-step file editing guidance

7. **PROMPT-0003-spec-translator.md**
   - Convert plain requirements to specs

8. **PROMPT-0004-test-navigator.md**
   - Test planning and design

9. **PROMPT-0005-doc-sync.md**
   - Documentation update guidance

10. **PROMPT-0006-governance-audit.md**
    - Pre-PR compliance check

11. **PROMPT-0007-change-log-author.md**
    - Change log entry creation

12. **PROMPT-0008-merge-ready-checklist.md**
    - Final merge readiness verification

13. **README.md**
    - Overview and navigation guide

---

## 🚀 QUICK START

### For Complete Beginners:
1. Open `rjw-idd-starter-kit/docs/prompts/PROMPT-CORE-novice-flow.md`
2. Copy the **Agent Pledge** (Section 0)
3. Paste it to your AI helper to start every session
4. Follow the 7 stages in order: Start → Explore → Decide → Create → Test → Record → Wrap

### For Experienced Users:
Use the numbered PROMPT-#### files for specific tasks as needed during your workflow.

---

## Core Prompts (always handy)
These live in `rjw-idd-starter-kit/docs/prompts/PROMPT-CORE-novice-flow.md`. Copy them as needed:
- `Agent Pledge` — sets the tone for plain language and RJW-IDD stages.
- `Start → Wrap` prompts — one prompt per stage so you can run a full cycle without guessing.
- `Quick Helpers` — use them to slow the helper down, ask for a file tour, or restate things in simple words.

## Guardrail Prompts
See `rjw-idd-starter-kit/docs/prompts/AGENT-GUARDRAILS.md` for ready-to-send reminders that keep the helper on the rails (plain language, confirmation before edits, end-of-session wrap up).

---

## Add Your Own Prompts Here
When you capture a new prompt, follow this format so teammates can scan and reuse it:
```
## Short title (use when <moment>)
<exact prompt text>
Notes: <what this prompt delivers or why it matters>
```

### Daily Restart (use when reopening the project)
```
We are picking up the same RJW-IDD cycle from yesterday. Remind me where we stopped, list the open tasks, and tell me the first prompt I should run today.
```
Notes: Keeps the project aligned when there is a break.

### Fix a Failing Test (use when a single test breaks)
```
One test failed. Help me:
1. Restate the failure in simple words.
2. Point me to the file and line I should inspect first.
3. Suggest the smallest fix to try.
4. Tell me which test to run again.
```
Notes: Keeps the fix focused and prevents big rewrites.

### Undo a Change (use when I made a mistake)
```
I changed the wrong thing. Show me the diff, tell me what will happen if we undo it, then roll back the edit safely.
```
Notes: Uses simple language before running any reset commands.

### Sync My Branch (use when git is behind)
```
Help me pull the latest changes. Explain what will happen, resolve any conflicts step by step, and tell me when it is safe to continue.
```
Notes: Keeps git updates calm and narrated.

### Draft a Commit Message (use when ready to commit)
```
We are ready to commit. Draft a commit message in plain words and list the files we are committing. Wait for me to confirm it before running git commands.
```
Notes: Ensures the commit summary makes sense to humans.

### Run the Bootstrap Script (use after cloning)
```
Please run `bash scripts/setup/bootstrap_project.sh` for me. Explain what you are doing, wait for my yes/no before starting, and translate the results into simple words.
```
Notes: Lets the helper drive setup while I stay informed.

---
Add more prompts below this line as the project grows.
