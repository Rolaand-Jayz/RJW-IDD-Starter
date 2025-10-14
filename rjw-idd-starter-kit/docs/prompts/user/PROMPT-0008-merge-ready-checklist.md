 # PROMPT-0008 — Merge-Ready Checklist

You provide the final safety net before merging.

**Confirm and report back on:**
1. Git status: no untracked or uncommitted files except intentional artefacts.
2. Tests and guards: `pytest` and `scripts/ci/test_gate.sh` have run successfully in the current branch.
3. Documentation: change log row present, docs updated, reconciliation log clean.
4. Decisions & ledgers: all new IDs reflected in `artifacts/ledgers/*.csv` and `docs/decisions/`.
5. Communication: PR description ready, reviewers identified, follow-up tasks captured.

End with “You are safe to request review” *or* a list of blockers to resolve first.

If you mention any RJW-IDD term, quickly define it or reference `docs/prompts/GLOSSARY.md` so the teammate stays comfortable.
