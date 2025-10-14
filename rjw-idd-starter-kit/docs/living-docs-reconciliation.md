# Living Documentation Reconciliation Log

Use this log whenever the Doc Steward identifies gaps between living documentation and the current code/spec/test state.

| date (UTC) | agent | doc_id(s) | gap summary | resolution plan | status |
|------------|-------|-----------|-------------|-----------------|--------|
| 2025-10-12 | Doc Steward | rjw-idd-starter-kit/* | Reorganised starter kit: moved templates/examples into `templates-and-examples/`, archived legacy tutorials/tests, updated manual/quickstart to point to methodology specs. | Verify downstream references in consuming repos, run guard suite once virtualenv available. | open |
| YYYY-MM-DD | ROLE-NAME | docs/path/to/doc.md | Describe the drift or missing coverage. | Outline the steps and link to the owning `change_id`. | open |

> The CI guard (`tools/testing/living_docs_guard.py`) rejects merges while any non-placeholder row remains `open`. Close the gap or remove the row once the change log, docs, and audits confirm resolution. The same guard also requires a documentation/spec update whenever implementation work changes non-doc files.

Update the row to `closed` once the Change Log entry, doc updates, and audits confirm the gap is resolved.
