# Agent Guardrails

```
You operate inside the RJW-IDD starter kit sandbox.

Do:
- Follow the RJW-IDD order: evidence → decision → spec → build/test → logs/change log.
- Cite file paths relative to repo root.
- Offer novice-friendly instructions and pause for confirmation before edits.
- Record TODOs when sandbox limits block a change.
- Update `docs/status/next-steps.md` every response: keep **Do Now** to 3 or
  fewer items, **Do Next** to 5, and capture the backlog there instead of the
  reply body.
- When someone says “Activate <mode> mode,” run `./bin/rjw mode <mode>`
  (PowerShell: `pwsh ./bin/rjw.ps1 mode <mode>`) to flip the feature flags, let
  `scripts/config_enforce.py` finish, and confirm which lane is now active.

Do not:
- Modify files outside approved directories.
- Invent evidence, decisions, or test results.
- Skip validation steps or the change log update.

Escalate any destructive command, missing validation, or unclear requirement.
Wrap responses with a short recap and suggested next step, then confirm the
queue reflects the same plan.
```
