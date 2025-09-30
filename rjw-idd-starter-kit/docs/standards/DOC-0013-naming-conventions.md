# DOC-0013 — RJW-IDD Naming Convention Standard

**Scope:** Defines mandatory naming rules for RJW-IDD artefacts, keeping method assets and project assets discoverable by automation and safe to reuse across repositories.

## Core Principles
1. **Method vs Project Separation:** Files inside `rjw-idd-methodology/` retain the `METHOD-####` namespace. Project-level artefacts (decisions, specs, ledgers, prompts, scripts) must never reuse the `METHOD-` prefix; instead follow the project prefixes below.
2. **Prefix + Sequence + Slug:** Managed artefacts use an uppercase prefix, zero-padded numeric sequence, and hyphenated lowercase slug (for example `DOC-0017-test-first-runbook.md`).
3. **Stable Identifiers:** Once issued, an identifier is never reused. Deprecated items retain their files with status called out in front matter or an archival register.
4. **Mirrored Layouts:** Directories mirror governance domains (`docs/`, `specs/`, `artifacts/`, `logs/`, `research/`, `scripts/`, `tools/`). Artefact prefixes align with their directory.
5. **Portable Links:** Use relative links rooted at the methodology or starter-kit folders so the pack can be copied without edits.

## Prefix Registry
| Prefix | Purpose | Location | Example |
|--------|---------|----------|---------|
| `METHOD-` | Method doctrine documents | `rjw-idd-methodology/**` | `rjw-idd-methodology/core/METHOD-0001-core-method.md` |
| `DOC-` | Standards, runbooks, implementation notes, templates | `docs/**` | `docs/runbooks/DOC-0017-test-first-runbook.md` |
| `DEC-` | Decision records | `docs/decisions/` | `docs/decisions/DEC-0004.md` |
| `SPEC-` | Specification stack | `specs/` | `specs/SPEC-0201-quality-gates.md` |
| `REQ-` | Requirement ledger entries | `artifacts/ledgers/requirement-ledger.csv` | `REQ-0001` |
| `TEST-` | Test ledger entries and contracts | `artifacts/ledgers/test-ledger.csv`, project test suites | `TEST-0001` |
| `LOG-` | Formal audit logs | `logs/` | `logs/LOG-0001-stage-audits.md` |
| `PROMPT-` | Prompt library entries | `docs/prompts/` | `docs/prompts/PROMPT-0001-omega-engineering.md` |
| `STATUS-` | Stage status snapshots | `docs/status/` | `docs/status/STATUS-template.md` |
| `INTEG-` | Integration artefacts (optional naming for transcripts) | `artifacts/integration/` | `INTEG-0001-context.md` |
| `EVD-` | Evidence identifiers | `research/evidence_index*.json` | `EVD-0001` |

## Directory Rules
- Files in `docs/` use `DOC-` prefixes unless the subfolder specifies another namespace (decisions, prompts, status).
- Specs follow `SPEC-####-slug.md`; choose slugs that reflect the domain (e.g., `performance-metrics`).
- Scripts and tools keep descriptive snake_case filenames and document the artefact IDs they support in module docstrings or headers. When scripts emit files (reports, logs), those outputs must follow the relevant prefix convention.
- Project workspaces (for example `workspace/`) may host drafts temporarily, but promote artefacts into the governed directories with proper prefixes before committing.

## Cross-Link Requirements
- In Markdown, wrap IDs in backticks (``REQ-0104``) so validators can detect them.
- Change Log rows list impacted IDs separated by semicolons.
- Ledgers store semicolon-delimited ID lists (`SPEC-0101;SPEC-0601`) and must be maintained alongside artefact changes.

## Onboarding Checklist
1. Determine the next sequence number for the prefix you need.
2. Create the file using the prefix + number + slug pattern before adding content.
3. Update referencing artefacts (ledgers, docs, specs) within the same change.
4. Run `scripts/validate_ids.py --paths <modified-files>` to confirm compliance.

## Exceptions & Generated Assets
- Exceptions require a decision entry with remediation plan and expiry date.
- Generated or transient files (for example raw logs) should live outside the methodology/starter-kit folders or in clearly marked directories ignored by validators.

Applying these conventions keeps RJW-IDD artefacts distinct between method and project layers, while remaining discoverable by automation and easy to audit.
