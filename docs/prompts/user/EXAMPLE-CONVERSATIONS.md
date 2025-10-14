# Example Conversations (Copy These)

These transcripts show how a level-zero teammate can talk to the coding helper. Copy the wording that fits your situation.

## 1. Ask the Helper to Run a Command
```
Human: Please run the bootstrap script for me. Tell me what you are doing and share the results in simple words.
Helper: ✅ Stage: Create
Helper: I will run `bash scripts/setup/bootstrap_project.sh`. It prepares the project. Ready to run it? (yes/no)
Human: yes
Helper: (runs the command) The script finished. Tests passed and the governance gate is green. Nothing failed.
```

## 2. Confirm File Changes Before Editing
```
Human: Before you change anything, list the files you plan to touch and why.
Helper: ✅ Stage: Create
Helper: I plan to edit `README.md` to add the new welcome section and `docs/manual/novice-quickstart.md` for the checklist. Ready to proceed? (yes/no)
Human: yes
Helper: Great. I will make the edits now and report back before moving on.
```

## 3. Inspect a Diff in Plain Language
```
Human: Show me what changed in simple words before we commit.
Helper: ✅ Stage: Record
Helper: We added a prompt block to `project-prompts.md` and created a new guide at `docs/prompts/EXAMPLE-CONVERSATIONS.md`. No other files changed.
Human: Thanks. That matches what I expected.
```

## 4. Recover After a Failed Test
```
Human: Tests failed. Restate the error in simple words and tell me what to try.
Helper: ✅ Stage: Test
Helper: Test `tests/app/test_login.py::test_rejects_blank_password` failed because the form now allows empty passwords. I suggest updating `app/login.py` to block blanks, then rerun `pytest tests/app/test_login.py -k blank_password`.
Human: Got it. Walk me through the fix step by step.
```

## 5. Write the Change-Log Entry Together
```
Human: Help me record the change log entry.
Helper: ✅ Stage: Record
Helper: Here is the row for `templates-and-examples/templates/change-logs/CHANGELOG-template.md`:
  - Change ID: change-20251004-01
  - Summary: Add novice-friendly bootstrap prompt and update README welcome copy.
  - Impacted IDs: docs/standards/tot-capture-standard.md, PROMPT-CORE
  - Verification: pytest, governance gate
Please paste this row into the table and let me know when it is saved.
Human: All set.
Helper: Great. Ready for the Wrap prompt?
```

Keep the guardrails in `AGENT-GUARDRAILS.md` active so the helper continues to follow this style.
