# METHOD-0003 — RJW-IDD Role Handbook

Assign each role to a named person before starting. These responsibilities enforce the same loop used to establish RJW-IDD.

## Evidence Lead
- Owns Phase 1.
- Maintains `research/evidence_tasks.json` and schedules harvests/micro-harvests.
- Ensures curated evidence meets recency thresholds; rejects phase advancement if gaps persist.
- Files the first draft of `DEC-####` when new research questions emerge.
- Signs RDD stage audit entries in `logs/LOG-0001-stage-audits.md`.

## Spec Architect
- Leads Phase 2.
- Updates requirement ledger, spec stack, and living-doc reconciliation log.
- Coordinates assumption tracking (e.g., provisional observability guidance) and requests additional RDD cycles where needed.
- Verifies ID validators run cleanly before handing off to Implementation.
- Co-signs SDD stage audit entries in `logs/LOG-0001-stage-audits.md`.

## Security & Privacy Liaison
- Checks that consent-first telemetry, security runbooks, and sandbox drills remain intact.
- During Implementation, reviews consent artefacts and integration transcripts for compliance.
- Blocks releases if audit trail is missing or if consent logs fall out of sync.
- Co-signs SDD and Implementation audit entries recorded in `logs/LOG-0001-stage-audits.md`.

## Implementation Wrangler
- Drives Phase 3.
- Enforces test-first discipline: rejects merges without failing tests and guard logs.
- Ensures documentation changes ship alongside code.
- Archives integration transcripts and attaches artefacts (tests, receipts) to the relevant rows in `docs/change-log.md`.
- Signs Implementation stage audits.

## Governance Board (All Roles)
- Collectively author and approve decisions stored in `docs/decisions/`.
- Review `docs/change-log.md` and `logs/LOG-0001-stage-audits.md` at each gate.
- Trigger additional RDD/SDD loops whenever assumptions or gaps surface.

## Operating Rhythm
- Daily stand-up: Evidence Lead reports on harvest plans; Implementation Wrangler reports guard/test status.
- Weekly review: Board inspects Change Log, stage audits, and outstanding `DEC-####` actions.
- Post-incident/hotfix: Security Liaison leads a retrospective and ensures new decisions capture lessons.
- Quarterly: Board verifies cumulative evidence/decision coverage and decides whether to update the method itself.

Use this handbook to keep ownership explicit. If the same person fills multiple roles, they must still record actions against each hat to preserve accountability.
