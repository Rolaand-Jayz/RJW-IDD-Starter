# DOC-0006 — Living Documentation Guidance

**Scope:** Defines how RJW-IDD teams create, evolve, and audit living documentation so humans and agents share an up-to-date understanding of the system.

## Document Classes
| Class | Location | Purpose | Required Metadata |
|-------|----------|---------|--------------------|
| Implementation Notes | `implementation/` | Explain code-level decisions, API shapes, edge cases. | `DOC-####`, linked `SPEC-####` / `REQ-####` / `TEST-####`, latest `change_id`. |
| API & Integration Guides | `docs/api/`, `docs/integration/` | Describe public interfaces, contracts, compatibility matrices. | `DOC-####`, `INTEG-####`, version, contact. |
| Runbooks & Playbooks | `docs/runbooks/` | Operational and incident workflows. | `DOC-####`, governing spec IDs, validation references. |
| Change Notes | `docs/changelog/` | Summaries of material changes per iteration. | `DOC-####`, `change_id`, impacted artefacts. |

## Authoring Rules
1. Update or create the relevant living doc within the same change that alters behaviour.
2. Maintain ID discipline (`DOC-####`) and cross-link to evidence, specs, requirements, tests, integrations, and decisions.
3. Use the structure: Context → Decision → Implementation → Validation → Follow-up.
4. Include “Operator Steps” and “Agent Checklist” when automation or handoffs are involved.
5. Avoid TODO placeholders; capture incomplete work in `docs/living-docs-reconciliation.md` with owners and due dates.

## Maintenance Workflow
1. **Before Work:** Read applicable docs and log gaps in `docs/living-docs-reconciliation.md`. Reconcile or formally defer via `DEC-####` before implementation starts.
2. **During Work:** Keep docs synchronized with code/spec/test updates. Reference new IDs and the active Change Log entry.
3. **After Work:** Run documentation linting/ID validation (`python scripts/validate_ids.py --paths <changed-docs>`). Attach results to the Change Log verification column.
4. **Periodic Audit:** At least monthly, Governance Sentinel and Doc Steward sample docs for parity and record findings under the next audit tag (`⟦audit-id:n⟧`).

## Tooling Support
- `scripts/validate_ids.py` ensures ID references exist and conform to `DOC-0005`.
- Projects may add doc linters or generators (`make lint-docs`, `make regen-api-docs`) and should document them here.

## Guidance for Agents
1. Start each task by summarizing the relevant living doc and logging any uncertainties.
2. Update docs immediately after code/spec/test modifications; do not defer.
3. Explicitly cross-link IDs in the doc narrative (for example, “Implements `REQ-0104`”).
4. For multi-agent work, add a handoff section outlining remaining actions and context.

## Guardrail
Skipping living documentation erodes traceability and breaks governance reviews. RJW-IDD enforces “no doc update, no merge”; violations must be escalated to the Governance Sentinel.

## References
- `DOC-0005` Traceability Schema
- `DEC-0003` Evidence Curation Approach
- `DEC-0004` Macro Structure
