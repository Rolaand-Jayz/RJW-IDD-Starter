# Decision — Adopt Feature Toggles for Risky Launches

- **Date:** 2025-01-15  
- **Participants:** Delivery lead, senior engineer, product partner  
- **Problem:** We must release multiplayer mode without blocking ongoing hotfixes.

## Candidate Options
1. Ship feature branch once QA signs off.
2. Merge behind a feature toggle and ramp exposure gradually.
3. Delay until the next quarterly release train.

## Evaluation
- **Option 1:** Fast path but reverts are painful. No resilience if incidents begin.
- **Option 2 (selected):** Toggle gives us rollout control, keeps trunk green, aligns with `templates-and-examples/templates/runbooks/runbook-template.md` rollback steps.
- **Option 3:** Breaks roadmap commitments; no customer learning until Q3.

## Decision
We will merge behind a toggle, monitor via the deployment runbook, and record exposure decisions in the change log (`templates-and-examples/templates/change-logs/CHANGELOG-template.md`).

## Follow-Up
1. Add toggle registration entry to `artifacts/ledgers/toggles.csv`.
2. Create a regression spec update: `specs/multiplayer-latency.md` derived from the starter kit spec template.
3. Schedule a day-7 audit to confirm toggle removal plan.
