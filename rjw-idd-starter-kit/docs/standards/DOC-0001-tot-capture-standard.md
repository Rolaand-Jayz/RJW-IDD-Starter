# DOC-0001 — RJW-IDD Tree-of-Thought Capture Standard

**Scope:** Defines how RJW-IDD records, stores, validates, and publishes Tree-of-Thought (ToT) decision trails for agents and humans.

## Objectives
- Preserve full decision context, candidate reasoning branches, and final rationale.
- Ensure every decision links to the evidence, specs, tests, integrations, and documents it influences.
- Make ToT content exportable without manual rewriting.

## Storage Rules
1. Each decision lives in `docs/decisions/DEC-####.md` (one file per decision).
2. Files must follow the `DEC-####` identifier used across the traceability model.
3. Sections are mandatory in this order: metadata, problem statement, candidate thoughts (≥3), evaluation, decision, cross-links, follow-up actions.
4. Markdown only—avoid embedded HTML so export tooling remains simple.
5. No TODO placeholders inside committed decisions; if work remains, capture it under “Follow-Up Actions” with owners and due dates.

## Cross-Linking Requirements
- Reference at least one of: evidence IDs (`EVD-####`), specifications (`SPEC-####`), requirements (`REQ-####`), tests (`TEST-####`), docs (`DOC-####`), or integration artefacts.
- When new artefacts will be created, list them under “Follow-Up Actions” and update the decision once delivered.
- Security/privacy decisions should cite multiple independent evidence sources to meet governance scrutiny.

## Validation Hooks
- Use the provided validation script (see `scripts/validate_ids.py`) to check structure, ID formats, and broken links.
- Projects should wire the validator into CI (`make validate-decisions` or equivalent).

## Publication Flow
1. Aggregate `DEC-####` files with the ToT renderer when preparing release notes or PDF bundles.
2. Capture checksums for both the source decisions and rendered outputs in the release manifest used by your project.

## Counterfactual Guardrail
Do not rely on private scratchpads for final reasoning. Decisions become canonical only when captured using this standard, ensuring auditability and compliance with governance criteria.
