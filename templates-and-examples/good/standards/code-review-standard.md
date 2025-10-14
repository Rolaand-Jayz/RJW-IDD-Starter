# Standard — Code Review Expectations

## Why this matters
Consistent reviews prevent regressions and teach novices how to apply
RJW-IDD artifacts in real pull requests.

## Scope
- Applies to every change merged into `main`.
- Add-ons may extend the checklist but must still meet this baseline.

## Requirements
1. Link at least one current decision and one spec from the starter kit or the
   methodology pack.
2. Capture evidence in the change log using the template from
   `templates-and-examples/templates/change-logs/`.
3. Re-run the guard suite (`scripts/checks/run_checks.sh`) before approval.
4. Update relevant runbooks when operational steps change.

## Enforcement
- The `rjw guard` CLI blocks merges when ledger links are missing.
- CI posts a failure comment referencing this standard when violations occur.

## Review Cadence
- Quarterly review with the governance lead.
- Faster review if two or more incidents cite review gaps in `logs/ci/`.
