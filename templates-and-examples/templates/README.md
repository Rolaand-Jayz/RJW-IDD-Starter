# Template Library

Copy files from here when you need to create a brand-new artifact.  Every
template includes inline TODOs and pointers back to the relevant RJW-IDD
guidance so you can fill the document in the correct order.

Templates are grouped by artifact type:

- `change-logs/` — release notes and audit entries.
- `decisions/` — structured decision records (no legacy ID requirements).
- `log-templates/` — CI, security, cost, RDD harvest, and stage-audit formats.
- `prompts/agent/` and `prompts/user/` — guardrails, reply shapes, and user
  briefings.
- `research/` — empty JSON shells for tasks, curated evidence, and raw feeds.
- `runbooks/` — incident/operational playbooks.
- `specs/` — solution blueprints aligned with the methodology pack.
- `standards/` — governance expectations teams must meet.
- `tests/` — pytest starter with traceability hints.

Whenever you add a new template, create matching “good” and “bad” examples so
learners can compare expectations quickly.
