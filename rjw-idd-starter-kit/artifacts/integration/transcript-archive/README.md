# Integration Transcript Archive Template

Use this structure to capture every AI-assisted integration session. The archive allows auditors and future operators to replay prompts, manual interventions, and verification evidence.

## Roles
- **Agent Conductor** – Runs the agent session, records prompts/responses, captures diffs.
- **Spec Curator** – Confirms the task aligns with current specs/decisions and prepares context notes.
- **Doc Steward** – Updates living documentation and Change Log references once the run completes.
- **Governance Sentinel** – Checks artefact completeness and retention.

## Directory Layout
```
artifacts/integration/transcript-archive/
  YYYY-MM-DD-task-slug/
    context.md
    prompts.log
    diffs/
    verification.md
```

### `context.md`
Include objective, related IDs (`DEC-####`, `REQ-####`, `SPEC-####`, `TEST-####`), assigned roles, environments touched, and planned documentation updates.

### `prompts.log`
Chronological list of agent prompts, responses, and manual overrides. Annotate deviations with `NOTE:` so follow-up decisions can reference them.

### `diffs/`
Patch files (`<repo>-<path>.patch`) capturing applied changes. Add additional assets (screenshots, data files) if helpful, but keep them under version control when feasible.

### `verification.md`
Document validation steps (tests, manual checks, sandbox drills), approvals, Change Log references, and links to living documentation updates. Record outstanding follow-ups with owners and due dates.

## Workflow
1. Scaffold the directory (`python tools/integration/archive_scaffold.py <task-slug>`) or recreate the structure manually.
2. Complete `context.md` before running the agent. List all docs that must be updated after the session.
3. During the session, append every interaction to `prompts.log` and export diffs into `diffs/` immediately.
4. After implementation, run verification steps and update `verification.md` with results and doc update links.
5. Reference the archive directory in the Change Log entry and living documentation.

## Retention & Governance
- Retain transcript folders for at least the governance-defined window (90 days recommended).
- Redact secrets or personal data before committing artefacts.
- Governance Sentinel samples archives during audits; missing artefacts block release until resolved.

## Automation Tips
- Extend the scaffold script to pre-fill metadata (owners, decision IDs) or to generate report summaries.
- Consider CI checks that ensure referenced transcript directories exist when Change Log entries mention them.
