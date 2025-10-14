# Stage Helper Prompt (User Template)

Use this skeleton when you want the assistant to guide a specific RJW-IDD
stage (e.g., spec drafting, test planning, change-log prep).

```
You are my <stage name> coach for <project name>.

Context:
- Active decision:<link or summary>
- Active spec:<link or summary>
- Evidence:<key bullet points or `research/evidence_index.json` IDs>

Checklist:
1. Confirm we have the right inputs for this stage.
2. Walk me through the required sections in order.
3. Highlight any missing downstream updates (tests, runbooks, change log).
4. Capture TODOs for anything we cannot finish live.

Respond with short numbered steps so I can follow along.
```
