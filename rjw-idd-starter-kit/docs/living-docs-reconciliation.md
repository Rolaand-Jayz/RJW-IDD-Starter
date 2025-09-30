# Living Documentation Reconciliation Log

Use this log whenever the Doc Steward identifies gaps between living documentation and the current code/spec/test state.

| date (UTC) | agent | doc_id(s) | gap summary | resolution plan | status |
|------------|-------|-----------|-------------|-----------------|--------|
| YYYY-MM-DD | ROLE-NAME | DOC-0000 | Describe the drift or missing coverage. | Outline the steps and link to the owning `change_id`. | open |

> The CI guard (`tools/testing/living_docs_guard.py`) rejects merges while any non-placeholder row remains `open`. Close the gap or remove the row once the change log, docs, and audits confirm resolution. The same guard also requires a documentation/spec update whenever implementation work changes non-doc files.

Update the row to `closed` once the Change Log entry, doc updates, and audits confirm the gap is resolved.
