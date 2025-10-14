# Deployment Runbook

- **Owner:** Release captain
- **Support:** On-call engineer, product partner
- **Last reviewed:** YYYY-MM-DD

## Purpose
Safely deploy application changes while maintaining rollback options and audit
trails. This runbook follows the starter-kit template in
`templates-and-examples/templates/runbooks/`.

## Preconditions
- Change log entry drafted using `templates-and-examples/templates/change-logs/`
  with planned deployment window.
- Tests and guards pass (`scripts/checks/run_checks.sh`).
- Rollback toggle or procedure documented.
- Logs stage audit template prepared (`templates-and-examples/templates/log-templates/stage-audit-log-template.md`).

## Steps
1. **Announce** — Notify `#deployments` channel with scope, window, and rollback
   plan.
2. **Tag build** — Confirm target commit and tag (`git log -1 --oneline`).
3. **Deploy to staging** — Run deployment script (for example
   `scripts/deploy/apply.sh staging`). Capture guard output in `logs/ci/`.
4. **Smoke test** — Run health checklist from
   `templates-and-examples/templates/tests/test_template.py` derivatives.
5. **Deploy to production** — Execute production deployment once staging passes.
6. **Monitor** — Watch key dashboards for ≥30 minutes; note observations in
   `logs/ci/` and stage-audit log.

## Rollback
1. Trigger feature toggle or redeploy previous tag.
2. Run smoke tests to confirm recovery.
3. Record symptoms, fix, and follow-up actions in the change log and logs.

## Communication
- Update change log with final outcome and guard run references.
- Post summary in team channel, including outstanding actions.
- Schedule follow-up decision if rollback occurred.

## References
- `templates-and-examples/good/runbooks/deployment-bluegreen-runbook.md`
- `templates-and-examples/templates/runbooks/runbook-template.md`
- `templates-and-examples/templates/log-templates/`
