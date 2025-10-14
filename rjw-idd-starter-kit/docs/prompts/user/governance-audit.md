# Governance Audit Prompt

```
You are performing a governance audit before we call the work complete.

Context:
- Decision updated: <path>
- Spec updated: <path>
- Change log entry: <path>
- Logs captured: <list>

Audit steps:
1. Confirm every change has supporting evidence and that evidence lives in research/.
2. Check decisions/specs/runbooks/standards for broken links or missing updates.
3. Ensure tests were run and recorded (cite command and outcome).
4. Summarise open risks or TODOs and who owns them.

Respond with a pass/fail table and highlight anything blocking sign-off.
```
