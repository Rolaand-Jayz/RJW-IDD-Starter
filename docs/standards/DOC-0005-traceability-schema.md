# DOC-0005 — RJW-IDD Traceability Schema

**Scope:** Defines identifier formats, cross-link rules, and validation expectations for RJW-IDD artefacts.

## Identifier Formats
| Artifact Type | Prefix | Format | Notes |
|---------------|--------|--------|-------|
| Hypothesis | `HYP-` | `HYP-####` | Four digits, zero-padded. |
| Evidence | `EVD-` | `EVD-####` | Created by the harvester or manual curation. |
| Specification | `SPEC-` | `SPEC-####` | Covers functional, non-functional, budgets, integration, observability, security, etc. |
| Requirement | `REQ-` | `REQ-####` | Captured in the requirement ledger. |
| Test | `TEST-` | `TEST-####` | Acceptance, integration, regression tests. |
| Documentation | `DOC-` | `DOC-####` | Standards, runbooks, guides, living docs. |
| Integration Asset | `INTEG-` | `INTEG-####` | Contracts, pacts, compatibility matrices. |
| Decision | `DEC-` | `DEC-####` | Tree-of-Thought records. |

### Sequencing
- IDs increment monotonically as artefacts are created; avoid reusing numbers.
- Maintain leading zeros for consistent sorting (e.g., `SPEC-0010`).
- Projects may reserve ranges (e.g., 0100–0199 for functional specs) but should document the convention in their charter.

## Cross-Link Rules
1. Every specification references at least one supporting evidence or hypothesis ID.
2. Every requirement links to the specification(s) that satisfy it and the tests that verify it.
3. Standards and runbooks reference the decisions that authorised them and any governing specs.
4. Integration artefacts map to the requirements and tests governing interface behaviour.
5. Test cases reference their source requirements/specs; execution logs embed the ID triple for observability correlation.
6. Decisions enumerate both upstream evidence and downstream artefacts they influence.

## Validation Expectations
- `scripts/validate_ids.py` checks ID formats, enforces cross-link presence, and highlights orphaned artefacts.
- Use backtick-wrapped IDs inside Markdown (`REQ-0104`) so tooling can parse links reliably.
- Release packaging should include a traceability snapshot (graph or CSV) for audit.

## Change Control
- Creating or retiring IDs must be reflected in the relevant ledgers (`artifacts/ledgers/*.csv`) and Change Log entries.
- Renames require a documented decision and explicit mapping from old to new IDs.

## Guardrail
Ad-hoc naming or undocumented artefacts undermine RJW-IDD’s audit trail. Teams must apply IDs at creation time and keep cross-links current to satisfy governance and incident-response needs.
