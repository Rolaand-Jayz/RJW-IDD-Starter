# Solo Developer Guide

This page maps the roles in RJW-IDD to a single person and gives a simple daily workflow.

Roles you will play
- Evidence Lead: gather and curate sample inputs
- Spec Architect: write minimal specs to guide tests
- Execution Wrangler: implement features and tests
- Doc Steward: update living docs and runbooks

Daily mini-routine
1. Run `bash scripts/checks/run_checks.sh`
2. Run one discovery task (add one evidence example)
3. Update spec for the small feature you plan to implement
4. Write a failing test and then implement code to pass it
5. Update docs and commit with a change-log row

Tips for solo devs
- Keep changes small and frequent
- Treat DEC files as lightweight contracts (1–2 paragraphs)
- Use `tutorials/` for experiments, keep core CI independent
