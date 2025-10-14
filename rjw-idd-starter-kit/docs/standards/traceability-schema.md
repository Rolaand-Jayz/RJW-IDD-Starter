# Traceability Schema Standard

- **Owner:** Governance lead
- **Applies to:** Entire starter kit
- **Last reviewed:** YYYY-MM-DD

## Purpose
Define how artifacts connect so teams can trace work end to end.

## Requirements
1. Decisions link to specs/runbooks/tests they influence (by file path).
2. Specs reference supporting decisions and evidence IDs.
3. Change log entries include related decisions/specs/tests/logs.
4. Logs reference change log entries and decision/spec updates.

## Verification
- Stage audit logs confirm links exist for each gate.
- Guards parse change log rows to ensure linked paths resolve.

## References
- `templates-and-examples/templates/decisions/`
- `templates-and-examples/templates/specs/`
- `templates-and-examples/templates/change-logs/`
