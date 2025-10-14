 # Merge-Ready Checklist Prompt

```
You are confirming the branch is ready to merge.

Inputs:
- Decision/spec references: <list>
- Change log entry path: <path>
- Tests run: <commands>
- Outstanding TODOs: <list or none>

Checklist:
1. Verify all planned artifacts were updated (decisions, specs, runbooks, standards, logs).
2. Confirm tests/guards were executed and passed.
3. Ensure change log and evidence indexes are updated.
4. List any follow-up tasks or approvals still required.

Respond with a Markdown checklist showing pass/fail for each item plus next steps if anything is missing.
```
