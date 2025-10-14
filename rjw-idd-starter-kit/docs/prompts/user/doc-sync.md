# Documentation Sync Prompt

```
You are ensuring documentation stays aligned after our changes.

Inputs:
- Code changes: <summary or PR link>
- Affected artifacts: decisions, specs, runbooks, change log, logs

Tasks:
1. Verify the change log entry using the template (path to file).
2. Check whether decisions or specs need edits; list exact sections.
3. Point to runbooks or standards that must be refreshed.
4. Remind me to capture relevant logs (CI, security, cost, stage audit).

Use bullet lists and provide direct file paths for quick copying.
```
