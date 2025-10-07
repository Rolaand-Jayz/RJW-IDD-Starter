# DOC-0022 — Git Workflow Runbook

**Applies to:** All team members working with RJW-IDD repositories  
**Cross-links:** `DOC-0021`, `DOC-0006`, `METHOD-0004`

## Purpose

Provide step-by-step git procedures for common RJW-IDD workflow scenarios, ensuring consistent version control practices that support governance and traceability.

---

## 1. First-Time Setup

### Prerequisites
- Git installed (`git --version` shows 2.30+)
- GitHub/GitLab account with SSH key or token configured
- RJW-IDD repository cloned locally

### Procedure

```bash
# Step 1: Configure git identity
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"

# Step 2: Set recommended defaults (from DOC-0021)
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global push.default current
git config --global push.autoSetupRemote true

# Step 3: Install pre-commit hooks
cd /path/to/rjw-idd-repository
pip install pre-commit
pre-commit install

# Step 4: Verify setup
bash scripts/setup/bootstrap_project.sh

# Step 5: Test commit
git checkout -b test-setup
echo "# Test" > TEST.md
git add TEST.md
git commit -m "test: verify git setup"
git checkout main
git branch -d test-setup
```

**Expected Result:** All steps complete without errors, pre-commit hooks run successfully.

**Troubleshooting:**
- If pre-commit fails: `pip install -r requirements-dev.txt`
- If SSH fails: Use HTTPS or configure SSH keys (`ssh-keygen`, `ssh-add`)

---

## 2. Starting New Work

### Scenario: Begin a new feature or fix

```bash
# Step 1: Ensure main is current
git checkout main
git pull origin main

# Step 2: Create feature branch with descriptive name
git checkout -b feature/add-health-endpoint
# Or: fix/broken-login
# Or: docs/update-readme

# Step 3: Verify branch created
git branch --show-current
# Output: feature/add-health-endpoint

# Step 4: (Optional) Set upstream immediately
git push -u origin feature/add-health-endpoint
```

**Branch Naming Rules:**
- `feature/<desc>` — New functionality
- `fix/<desc>` — Bug fixes  
- `docs/<desc>` — Documentation only
- `test/<desc>` — Test additions
- `refactor/<desc>` — Code restructuring
- `chore/<desc>` — Maintenance
- `hotfix/<desc>` — Emergency production fixes

---

## 3. Making Changes (RJW-IDD Cycle)

### Scenario: Implement changes following RJW-IDD stages

```bash
# Step 1: Work in small increments (Start → Explore → Decide)
# Edit files as needed

# Step 2: Stage changes
git add <files>
# Or stage all: git add .

# Step 3: Check what's staged
git status
git diff --staged

# Step 4: Commit with RJW-IDD format
git commit -m "feat(health): add GET /health endpoint

Implements SPEC-0003 health monitoring requirement.
Returns JSON {\"status\": \"ok\"} on HTTP 200.

change-$(date +%Y%m%d)-02: Health check endpoint
Impacted IDs: SPEC-0003, TEST-0007
Verification: pytest passes"

# Step 5: Verify commit
git log -1

# Step 6: Repeat for each logical change
# Multiple small commits > one large commit
```

**Commit Frequency:**
- After each RJW-IDD stage (Create, Test, Record)
- When a logical unit of work completes
- Before switching contexts or taking breaks
- Minimum: Daily, even if work is incomplete (use WIP prefix)

---

## 4. Running Governance Guards Locally

### Scenario: Validate changes before pushing

```bash
# Step 1: Run pytest
pytest
# Or specific tests: pytest tests/guards/

# Step 2: Run full test gate
bash scripts/ci/test_gate.sh

# Step 3: If guards fail, fix issues
# Red-green guard failure:
git add tests/test_new_feature.py
git commit -m "test: add tests for new feature"

# Change log guard failure:
# Edit docs/change-log.md, add row
git add docs/change-log.md
git commit -m "docs: add change log entry for feature"

# ID validation failure:
# Fix ID references in files
git add <files>
git commit -m "fix: correct ID references"

# Step 4: Re-run guards until clean
bash scripts/ci/test_gate.sh
```

**Guard Failure Resolution:**

| Guard | Common Fix |
|-------|-----------|
| `red_green_guard` | Add tests in `tests/` directory |
| `change_log_guard` | Add entry to `docs/change-log.md` |
| `living_docs_guard` | Update docs or log reconciliation |
| `governance_alignment_guard` | Sync specs/ledgers/decisions |
| `agent_response_guard` | Add Novice + Technical sections |
| `validate_ids.py` | Fix ID format or broken references |
| `validate_evidence.py` | Refresh evidence via harvester |

---

## 5. Keeping Branch Updated

### Scenario: Sync branch with main while working

```bash
# Step 1: Save work (commit or stash)
git status
# If uncommitted changes: git stash push -m "WIP"

# Step 2: Fetch latest main
git fetch origin main

# Step 3: Rebase onto main (preferred)
git rebase origin/main

# Alternative: Merge (creates merge commit)
# git merge origin/main

# Step 4: Resolve conflicts if any
# Git will pause on conflicts
git status  # Shows conflicted files

# Edit files, remove conflict markers
# <<<<<<<, =======, >>>>>>>

# Mark resolved
git add <resolved-files>

# Continue rebase
git rebase --continue

# Step 5: If stashed, restore work
git stash pop

# Step 6: Force-push (rebase rewrites history)
git push --force-with-lease origin feature/your-branch
```

**When to Sync:**
- Daily (start of day)
- Before pushing to remote
- Before creating pull request
- After main receives important updates

**Merge vs Rebase:**
- **Rebase** (preferred): Clean linear history, easier to review
- **Merge**: Preserves exact development timeline, safer for shared branches

---

## 6. Pushing to Remote

### Scenario: Share work on remote repository

```bash
# Step 1: Ensure guards pass
bash scripts/ci/test_gate.sh

# Step 2: Push to remote
git push origin feature/your-branch

# First push to new branch:
git push -u origin feature/your-branch
# Or with autoSetupRemote configured: just `git push`

# Step 3: Verify push succeeded
git branch -vv
# Shows tracking relationship

# Step 4: Force-push after rebase (use with caution)
git push --force-with-lease origin feature/your-branch
# Never use --force alone (unsafe)
```

**Force-Push Safety:**
- **Never** force-push to `main` or shared branches
- Use `--force-with-lease` instead of `--force`
- Only force-push after rebase on personal feature branches
- Coordinate with team if branch is shared

---

## 7. Creating Pull Request

### Scenario: Submit work for review

```bash
# Step 1: Ensure branch is current
git fetch origin main
git rebase origin/main
git push --force-with-lease origin feature/your-branch

# Step 2: Run final checks
bash scripts/ci/test_gate.sh
pytest

# Step 3: Create PR via GitHub CLI
gh pr create \
  --title "feat(health): add health check endpoint" \
  --body "$(cat <<EOF
## Description
Adds GET /health endpoint returning JSON status.

## RJW-IDD Checklist
- [x] Tests added/updated (red-green cycle followed)
- [x] Documentation updated (living docs reconciled)
- [x] Change log entry added (change-20251007-02)
- [x] Governance guards pass locally
- [x] Linked IDs updated in ledgers

## Changes
- SPEC-0003: Health check API specification
- TEST-0007: Health check functional test
- DOC-0011: Updated API standards

## Verification
- Pytest: PASSED
- Guards: PASSED (all 7 guards clean)
- Manual testing: Endpoint returns 200 + JSON

## Change Log Entry
change-20251007-02: Health check endpoint
Impacted IDs: SPEC-0003, TEST-0007, DOC-0011
Verification: pytest passes, guards pass
EOF
)" \
  --base main \
  --head feature/add-health-endpoint

# Or via web interface:
# Push branch, then visit GitHub and click "Create Pull Request"

# Step 4: Link to PR in commit if needed
git commit --amend -m "$(git log -1 --pretty=%B)

PR: #123"
git push --force-with-lease
```

**PR Checklist (from `.github/PULL_REQUEST_TEMPLATE.md`):**
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Change log entry added
- [ ] Guards pass locally
- [ ] IDs updated in ledgers
- [ ] No TODOs or debug code
- [ ] Breaking changes documented

---

## 8. Reviewing Pull Request

### Scenario: Review teammate's PR

```bash
# Step 1: Fetch PR branch
gh pr checkout <PR-number>
# Or: git fetch origin && git checkout feature/their-branch

# Step 2: Verify guards pass
bash scripts/ci/test_gate.sh

# Step 3: Run tests
pytest
pytest tests/guards/  # Specifically test guards

# Step 4: Review changes
git log origin/main..HEAD --oneline
git diff origin/main..HEAD

# Step 5: Test functionality manually
# ... perform manual testing ...

# Step 6: Check governance artifacts
# - docs/change-log.md has entry?
# - Linked IDs correct in ledgers?
# - Documentation updated?
# - Decision records created if needed?

# Step 7: Provide feedback
gh pr review <PR-number> --comment -b "Feedback here"
# Or approve: gh pr review <PR-number> --approve
# Or request changes: gh pr review <PR-number> --request-changes

# Step 8: Return to main
git checkout main
```

**Review Focus Areas:**
1. **Governance:** Change log, IDs, traceability
2. **Tests:** Coverage, red-green cycle followed
3. **Documentation:** Living docs updated, no stale content
4. **Code quality:** Follows project conventions
5. **Security:** No credentials, sensitive data exposed

---

## 9. Merging Pull Request

### Scenario: Merge approved PR

```bash
# Step 1: Ensure all checks pass
# - CI workflows green
# - Required approvals received
# - No merge conflicts

# Step 2: Merge via GitHub CLI
gh pr merge <PR-number> --squash --delete-branch

# Or choose merge strategy:
# --squash: Single commit (preferred for features)
# --merge: Preserve all commits
# --rebase: Replay commits on main

# Step 3: Pull merged changes
git checkout main
git pull origin main

# Step 4: Verify merge
git log --oneline -5
# Should show merged work

# Step 5: Clean up local branch
git branch -d feature/merged-branch
git fetch --prune  # Remove stale remote refs
```

**Merge Strategy Selection:**
- **Squash** (default): Clean history, single commit per feature
- **Merge commit**: Preserve branching history, good for releases
- **Rebase**: Linear history, individual commits preserved

---

## 10. Hotfix Workflow

### Scenario: Emergency production fix

```bash
# Step 1: Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix

# Step 2: Make minimal fix
# Edit only necessary files

# Step 3: Add tests
# Even hotfixes need tests!

# Step 4: Commit with SEV-level
git commit -m "hotfix(auth): patch SQL injection vulnerability

SEV-1 security incident. CVE-2025-XXXXX.
Details in DEC-INCIDENT-0042.

Immediate actions:
- Sanitize user input in auth/login.py
- Add parameterized queries
- Backport to all affected versions

change-$(date +%Y%m%d)-99: Critical security hotfix
Impacted IDs: SPEC-0501, TEST-0088, DEC-INCIDENT-0042
Verification: manual security audit, automated tests pass

Fixes #INCIDENT-789"

# Step 5: Push and create urgent PR
git push -u origin hotfix/critical-security-fix
gh pr create --title "hotfix(auth): critical security patch" \
             --label "hotfix,security,urgent" \
             --body "SEV-1 incident response. Requires immediate merge."

# Step 6: After merge, backport to other branches
git checkout main
git pull origin main
git checkout release/v2.0
git cherry-pick <hotfix-commit-hash>
git push origin release/v2.0
```

**Hotfix Characteristics:**
- Branch from `main` (or affected release branch)
- Minimal changes only
- Fast-track review (but still requires approval)
- Immediate deployment after merge
- Must include tests and documentation
- Backport to all affected versions

---

## 11. Undoing Mistakes

### Scenario A: Uncommitted changes (discard)

```bash
# Discard unstaged changes to specific file
git restore <file>
# Or old syntax: git checkout -- <file>

# Discard all unstaged changes
git restore .

# Unstage staged changes
git restore --staged <file>
# Or old syntax: git reset HEAD <file>
```

### Scenario B: Bad commit (not pushed)

```bash
# Undo commit, keep changes
git reset --soft HEAD~1

# Undo commit, discard changes
git reset --hard HEAD~1

# Edit commit message
git commit --amend -m "corrected message"

# Add forgotten file to last commit
git add forgotten-file.txt
git commit --amend --no-edit
```

### Scenario C: Bad commit (already pushed)

```bash
# Option 1: Revert (creates new commit undoing changes)
git revert <commit-hash>
git push origin feature/branch

# Option 2: Force-push (use cautiously)
git reset --hard HEAD~1
git push --force-with-lease origin feature/branch

# NEVER force-push to main or shared branches!
```

### Scenario D: Recover deleted branch

```bash
# Find commit hash in reflog
git reflog
# Look for: "checkout: moving from deleted-branch to main"

# Recreate branch
git checkout -b recovered-branch <commit-hash>

# Or restore from remote
git checkout -b recovered-branch origin/branch-name
```

### Scenario E: Resolve merge conflicts

```bash
# During rebase or merge, conflicts appear
git status  # Lists conflicted files

# Open each conflicted file
# Look for conflict markers:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> branch-name

# Edit to resolve (remove markers, keep desired code)

# Mark as resolved
git add <resolved-file>

# Continue operation
git rebase --continue
# Or: git merge --continue

# If stuck, abort
git rebase --abort
# Or: git merge --abort
```

---

## 12. Advanced Operations

### Interactive Rebase (Clean History)

```bash
# Rebase last 3 commits interactively
git rebase -i HEAD~3

# In editor, choose action for each commit:
# pick = use commit
# reword = use commit, edit message
# edit = use commit, stop for amending
# squash = meld into previous commit
# fixup = like squash, discard message
# drop = remove commit

# Save and close editor
# Follow prompts to complete rebase

# Force-push cleaned history
git push --force-with-lease origin feature/branch
```

### Cherry-Pick Specific Commits

```bash
# Apply single commit to current branch
git cherry-pick <commit-hash>

# Cherry-pick range
git cherry-pick <start-hash>^..<end-hash>

# Cherry-pick with custom message
git cherry-pick -e <commit-hash>
```

### Stash Management

```bash
# Save work without committing
git stash push -m "WIP: feature implementation"

# List stashes
git stash list
# Output:
# stash@{0}: WIP: feature implementation
# stash@{1}: emergency: saved before hotfix

# Apply most recent stash
git stash pop
# Or: git stash apply  (keeps stash)

# Apply specific stash
git stash apply stash@{1}

# Delete stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

---

## 13. Troubleshooting

### Issue: Merge conflict during rebase

**Symptoms:**
```
CONFLICT (content): Merge conflict in file.py
error: could not apply abc1234...
```

**Resolution:**
1. Run `git status` to see conflicted files
2. Open each file, resolve conflicts (remove `<<<<<<<`, `=======`, `>>>>>>>`)
3. `git add <resolved-files>`
4. `git rebase --continue`
5. If too complex: `git rebase --abort` and ask for help

### Issue: Accidentally committed to main

**Symptoms:**
```bash
git branch --show-current
# Output: main  (should be feature branch!)
```

**Resolution:**
```bash
# Move commit to new branch
git branch feature/accidental-commit
git reset --hard HEAD~1

# Verify main is clean
git log --oneline -3

# Continue work on feature branch
git checkout feature/accidental-commit
```

### Issue: Push rejected (behind remote)

**Symptoms:**
```
! [rejected] feature -> feature (non-fast-forward)
```

**Resolution:**
```bash
# Fetch and rebase
git fetch origin
git rebase origin/feature

# Resolve conflicts if any
# Then force-push
git push --force-with-lease origin feature
```

### Issue: Pre-commit hooks failing

**Symptoms:**
```
black....................................................................Failed
ruff.....................................................................Failed
```

**Resolution:**
```bash
# Run formatters manually
black .
ruff check --fix .

# Stage fixes
git add .

# Retry commit
git commit -m "..."

# Or bypass hooks temporarily (NOT RECOMMENDED)
git commit --no-verify -m "..."
```

---

## 14. Quick Reference Commands

### Status & Information
```bash
git status -sb              # Short status
git log --oneline -10       # Recent commits
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git branch -vv              # Branches with tracking
git remote -v               # Remote URLs
```

### Branch Operations
```bash
git branch                  # List branches
git branch -d <branch>      # Delete local branch
git push -d origin <branch> # Delete remote branch
git checkout -b <branch>    # Create and switch
git switch <branch>         # Switch branches (new syntax)
```

### Stashing
```bash
git stash                   # Save work
git stash list              # List stashes
git stash pop               # Apply and remove
git stash clear             # Delete all stashes
```

### Undoing
```bash
git restore <file>          # Discard changes
git restore --staged <file> # Unstage
git reset --soft HEAD~1     # Undo commit, keep changes
git reset --hard HEAD~1     # Undo commit, discard changes
git revert <hash>           # Create commit undoing <hash>
```

### Inspection
```bash
git show <hash>             # Show commit
git blame <file>            # Line-by-line authorship
git log --grep="pattern"    # Search commit messages
git log -S"code"            # Search code changes
```

---

## 15. Integration with RJW-IDD Stages

### Git Operations by Stage

| RJW-IDD Stage | Git Operations |
|---------------|----------------|
| **Start** | Create branch, initial commit |
| **Explore** | Frequent commits as you experiment |
| **Decide** | Squash experiment commits, commit plan |
| **Create** | Commit each logical unit of work |
| **Test** | Commit tests, commit fixes |
| **Record** | Commit documentation, change log |
| **Wrap** | Final commit, create PR |

### Example Full Cycle

```bash
# Start
git checkout -b feature/new-capability
git commit -m "docs: initial planning notes"

# Explore (multiple commits OK)
git commit -m "wip: explore approach A"
git commit -m "wip: explore approach B"

# Decide (squash experiments)
git rebase -i HEAD~3
# Squash into: "feat: implement new capability foundation"

# Create
git commit -m "feat(core): add main functionality"
git commit -m "feat(api): expose new endpoints"

# Test
git commit -m "test: add unit tests for new capability"
git commit -m "fix: handle edge case in validation"

# Record
git commit -m "docs: update API documentation"
git commit -m "docs: add change log entry"

# Wrap
bash scripts/ci/test_gate.sh
git push -u origin feature/new-capability
gh pr create
```

---

## 16. Verification

After completing any git operation:

- [ ] `git status` shows clean working tree
- [ ] `git branch -vv` shows correct tracking
- [ ] `bash scripts/ci/test_gate.sh` passes
- [ ] Change log updated for material changes
- [ ] No sensitive data in commit history
- [ ] Commit messages follow RJW-IDD format

---

## References

- **DOC-0021** — Git Setup & Configuration Standard
- **METHOD-0004** — AI Agent Workflows (git procedures)
- **DOC-0006** — Living Documentation Guidelines
- **.github/PULL_REQUEST_TEMPLATE.md** — PR template

---

**Status:** Active  
**Owner:** Development Team  
**Last Updated:** 2025-10-07
