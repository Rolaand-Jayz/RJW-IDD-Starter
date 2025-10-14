# Spec Translator Prompt

```
You are helping me translate the latest decision into a spec update.

Context:
- Decision: <link/path>
- Existing spec: <path>
- Evidence: <research/evidence_index.json entries>

Steps:
1. List the spec sections that need updates (purpose, scope, acceptance criteria, validation).
2. Suggest concrete wording for each section, referencing evidence.
3. Highlight any gaps in tests, runbooks, or standards triggered by this spec change.
4. Provide a quick diff-style summary so I can copy it into the spec file.

Keep the guidance beginner friendly and stop after each section for confirmation.
```
