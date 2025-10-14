# Example Conversations

Use these transcripts to understand how a novice can work with the assistant.

## 1. Running the Guard Suite

**User:** "I just finished updating the spec. What next?"

**Assistant:** "Run `scripts/checks/run_checks.sh`. Paste the results here so we can record them in `logs/ci/`."

**User:** "The script passed, build #482."

**Assistant:** "Great! Add a row to the change log using the starter template and link this guard run."

## 2. Capturing Evidence

**User:** "We need proof that toggles work."

**Assistant:** "Add a task to `research/evidence_tasks.json` (copy the template). Once we harvest, promote the useful items into `research/evidence_index.json` and cite them in the decision."

## 3. Preparing Merge Readiness

**User:** "Is the branch ready to merge?"

**Assistant:** "Let’s run the merge-ready checklist prompt. Confirm decisions/specs/runbooks/standards are updated, tests passed, logs captured, and the change log entry is ready."
