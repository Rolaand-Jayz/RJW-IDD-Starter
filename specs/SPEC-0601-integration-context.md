# SPEC-0601 — Integration Context Template

**Linked Requirements:** Add integration workflow requirement IDs.  
**Status:** Template

## Purpose
Define how integration work captures context, transcripts, and verification evidence so multi-repo or multi-service changes remain reproducible.

## Scope
- Applies to all integration tasks involving agents or humans under RJW-IDD.
- Covers transcript capture, diff packaging, and verification artefacts.

## Expectations
1. Create an integration transcript directory (`artifacts/integration/transcript-archive/<identifier>/`) for each change that crosses repository or service boundaries.
2. Record context (`context.md`), prompts/responses (`prompts.log`), diffs (`diffs/`), and verification results (`verification.md`).
3. Link transcripts to Change Log entries and living documentation updates.
4. Ensure integration checks/tests run with references to the relevant requirement/spec/test IDs.
5. Retain transcripts for at least the retention window defined by governance (default 90 days) and surface them during audits.

## Implementation Guidance
- Provide templates for transcript contents in `artifacts/integration/transcript-archive/README.md`.
- Automate transcript creation where possible (e.g., CLI wrappers that scaffold directories).
- Include integration handoff notes in living documentation so future operators can replay the change.

## Verification
- Integration tests or manual validation steps recorded in the transcript must pass before merging.
- Governance Sentinel samples transcript archives during audits to confirm completeness and traceability.
