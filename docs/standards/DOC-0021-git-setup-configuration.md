# DOC-0021 — Git Setup & Configuration Standard

**Linked Requirement:** Document git workflow requirement IDs when adopting.  
**Linked Specification:** Reference version control spec (e.g., `SPEC-0201`).  
**Status:** Active

## Purpose

Define git configuration, branch strategy, commit conventions, and tooling integration for RJW-IDD projects to ensure consistent, auditable version control practices.

## Scope

- Initial git setup and user configuration
- Repository initialization with RJW-IDD structure
- Branch naming conventions
- Commit message standards
- Pre-commit hooks and automation
- GitHub/GitLab integration patterns

---

## 1. Initial Git Configuration

### User Identity Setup

Every developer must configure their git identity:

```bash
# Set your name and email (used in commit metadata)
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global --list
```

### Recommended Global Settings

Create or update `~/.gitconfig`:

```ini
[user]
    name = Your Full Name
    email = your.email@example.com

[core]
    # Use VS Code as default editor (or vim, nano, etc.)
    editor = code --wait
    # Normalize line endings
    autocrlf = input  # Linux/Mac
    # autocrlf = true  # Windows
    # Exclude file for personal ignores
    excludesfile = ~/.gitignore_global

[init]
    # Use 'main' as default branch name
    defaultBranch = main

[pull]
    # Rebase by default to keep history clean
    rebase = true

[push]
    # Push current branch to same-named remote branch
    default = current
    # Automatically set up remote tracking
    autoSetupRemote = true

[fetch]
    # Remove deleted remote branches
    prune = true

[rebase]
    # Auto-stash before rebase
    autoStash = true

[diff]
    # Better diff algorithm
    algorithm = histogram
    # Show renames and copies
    renames = copies

[merge]
    # Include common ancestor in conflict markers
    conflictStyle = diff3

[alias]
    # Useful shortcuts
    st = status -sb
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    lg = log --graph --oneline --decorate --all
    rjw-status = !git st && echo "\n=== RJW-IDD Status ===" && git diff --name-only origin/main...HEAD
    
[color]
    ui = auto
```

### Project-Specific Configuration

Inside the RJW-IDD repository:

```bash
cd /path/to/rjw-idd-repository

# Set project-specific email if different from global
git config user.email "project-specific@example.com"

# Enable GPG signing (optional but recommended)
git config commit.gpgsign true
git config user.signingkey YOUR_GPG_KEY_ID
```

---

## 2. Repository Initialization

### For New Projects

```bash
# Initialize repository
git init

# Set main as default branch
git branch -M main

# Add RJW-IDD starter kit as remote template
git remote add template https://github.com/your-org/rjw-idd-starter-kit.git
git fetch template
git merge template/main --allow-unrelated-histories

# Or start fresh and copy structure manually
cp -r /path/to/rjw-idd-starter-kit/* .
git add .
git commit -m "feat: Initialize RJW-IDD project structure

- Copy starter kit directory layout
- Initialize governance artifacts
- Set up initial documentation

change-$(date +%Y%m%d)-01: Project initialization
Impacted IDs: DOC-0001, METHOD-0001
Verification: bootstrap_project.sh passes"
```

### For Existing Projects

```bash
# Add RJW-IDD structure to existing repo
cd /path/to/existing-project

# Create RJW-IDD branch
git checkout -b rjw-idd-integration

# Merge or copy RJW-IDD artifacts
# ... add files ...

git add rjw-idd-starter-kit/ docs/ .github/
git commit -m "feat: Integrate RJW-IDD governance framework"
```

---

## 3. Branch Strategy

### Branch Naming Convention

| Pattern | Purpose | Example |
|---------|---------|---------|
| `main` | Production-ready code | `main` |
| `feature/<description>` | New features | `feature/health-check-endpoint` |
| `fix/<description>` | Bug fixes | `fix/login-validation` |
| `docs/<description>` | Documentation only | `docs/update-readme` |
| `refactor/<description>` | Code refactoring | `refactor/extract-auth-service` |
| `test/<description>` | Test additions/fixes | `test/add-integration-tests` |
| `chore/<description>` | Maintenance tasks | `chore/update-dependencies` |
| `hotfix/<description>` | Emergency production fixes | `hotfix/critical-security-patch` |

### Branch Lifecycle

```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/my-new-feature

# Work on feature (multiple commits)
git add <files>
git commit -m "..."

# Keep branch updated with main
git fetch origin
git rebase origin/main

# Push to remote
git push origin feature/my-new-feature

# After PR merge, clean up
git checkout main
git pull origin main
git branch -d feature/my-new-feature
```

### Protected Branches

Configure `main` branch protection in GitHub/GitLab:

- Require pull request reviews (minimum 1 reviewer)
- Require status checks to pass before merging:
  - `test-gate` workflow
  - All guard validations
  - Code coverage thresholds
- Require branches to be up to date before merging
- Restrict who can push to main (disable direct pushes)
- Require signed commits (optional but recommended)

---

## 4. Commit Message Standards

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat(api): add health check endpoint` |
| `fix` | Bug fix | `fix(auth): validate empty passwords` |
| `docs` | Documentation only | `docs(readme): update installation steps` |
| `style` | Formatting, no code change | `style(lint): fix indentation` |
| `refactor` | Code restructuring | `refactor(db): extract query builder` |
| `test` | Add/modify tests | `test(guards): add red-green guard tests` |
| `chore` | Maintenance | `chore(deps): update pytest to 8.0` |
| `perf` | Performance improvement | `perf(query): add database index` |
| `ci` | CI/CD changes | `ci(workflow): add caching step` |
| `build` | Build system changes | `build(docker): update base image` |
| `revert` | Revert previous commit | `revert: feat(api): add health check` |

### Scope (Optional but Recommended)

- Module, component, or subsystem affected
- Examples: `auth`, `api`, `guards`, `docs`, `ci`, `3d-addon`, `video-addon`

### Subject Line Rules

1. Use imperative mood ("add" not "added" or "adds")
2. Don't capitalize first letter
3. No period at the end
4. Maximum 50 characters
5. Be specific and descriptive

### Body (Optional)

- Wrap at 72 characters
- Explain **what** and **why**, not **how**
- Reference related issues/tickets
- Include breaking changes

### Footer

**Required for RJW-IDD:**

```
change-YYYYMMDD-##: Brief description
Impacted IDs: SPEC-####, REQ-####, TEST-####, DOC-####
Verification: pytest passes, guards pass
```

**Optional:**

```
Fixes #123
Closes #456
BREAKING CHANGE: API endpoint renamed from /health to /status
```

### Examples

**Simple feature:**
```
feat(health): add health check endpoint

Add GET /health endpoint returning JSON status.
Implements SPEC-0003 health monitoring requirement.

change-20251007-02: Health check endpoint
Impacted IDs: SPEC-0003, TEST-0007
Verification: pytest passes, test_gate.sh passes
```

**Bug fix with details:**
```
fix(auth): reject blank passwords in login form

The login validator was allowing empty password fields,
creating a security vulnerability. Added validation to
reject requests with blank passwords.

Root cause: Missing null check in auth/validator.py
Impact: SEV-2 security issue (user enumeration possible)

change-20251007-03: Fix blank password validation
Impacted IDs: SPEC-0101, TEST-0012, DEC-0045
Verification: test_login.py passes, security audit clean

Fixes #789
```

**Breaking change:**
```
feat(api)!: rename health endpoint from /health to /status

BREAKING CHANGE: The health check endpoint has moved from
/health to /status to align with company standards.
Update all clients to use the new endpoint.

Migration path documented in docs/api-standards.md

change-20251007-04: Rename health endpoint
Impacted IDs: SPEC-0003, DOC-0011
Verification: integration tests updated and passing
```

---

## 5. Pre-commit Hooks

### Install Pre-commit Framework

```bash
# Install pre-commit (if not in requirements-dev.txt)
pip install pre-commit

# Install hooks from .pre-commit-config.yaml
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### RJW-IDD Hook Configuration

The `.pre-commit-config.yaml` already includes:

- Trailing whitespace removal
- End-of-file fixing
- YAML/JSON validation
- Python formatting (black)
- Python linting (ruff)
- Markdown linting

### Custom RJW-IDD Hooks

Add to `.pre-commit-config.yaml`:

```yaml
# RJW-IDD specific hooks
repos:
  - repo: local
    hooks:
      # Validate commit message format
      - id: commit-msg-validation
        name: Validate RJW-IDD commit message
        entry: python -m tools.git.validate_commit_msg
        language: system
        stages: [commit-msg]
        
      # Ensure change log entry
      - id: change-log-check
        name: Check change log entry exists
        entry: python -m tools.testing.change_log_guard --files
        language: system
        pass_filenames: true
        
      # Red-green guard
      - id: red-green-test-guard
        name: Enforce test-first discipline
        entry: python -m tools.testing.red_green_guard --files
        language: system
        pass_filenames: true
```

### Bypass Hooks (Emergency Only)

```bash
# Skip pre-commit hooks (NOT RECOMMENDED)
git commit --no-verify -m "emergency: critical hotfix"

# Document in commit message why hooks were skipped
```

---

## 6. Git Workflow Integration

### Daily Workflow

```bash
# Morning: Sync with main
git checkout main
git pull origin main

# Start work
git checkout -b feature/my-task

# During work: frequent small commits
git add <files>
git commit -m "feat(scope): descriptive message"

# Before pushing: run guards locally
bash scripts/ci/test_gate.sh

# Push to remote
git push origin feature/my-task

# Evening: keep branch updated
git fetch origin
git rebase origin/main
git push --force-with-lease origin feature/my-task
```

### Pull Request Workflow

1. **Create PR:**
   ```bash
   # Push branch
   git push origin feature/my-task
   
   # Create PR via GitHub CLI or web interface
   gh pr create --title "feat(scope): description" \
                --body "$(cat PR_TEMPLATE.md)"
   ```

2. **PR Template** (`.github/PULL_REQUEST_TEMPLATE.md`):
   ```markdown
   ## Description
   Brief summary of changes
   
   ## RJW-IDD Checklist
   - [ ] Tests added/updated (red-green cycle followed)
   - [ ] Documentation updated (living docs reconciled)
   - [ ] Change log entry added (`change-YYYYMMDD-##`)
   - [ ] Governance guards pass locally
   - [ ] Linked IDs updated in ledgers
   
   ## Changes
   - SPEC-####: Description
   - TEST-####: Description
   - DOC-####: Description
   
   ## Verification
   - Pytest: PASSED
   - Guards: PASSED
   - Manual testing: PASSED
   
   ## Breaking Changes
   None / List any breaking changes
   
   ## Change Log Entry
   ```
   change-YYYYMMDD-##: Brief description
   Impacted IDs: SPEC-####, REQ-####, TEST-####
   Verification: pytest passes, guards pass
   ```
   ```

3. **Review Process:**
   - Reviewer checks governance compliance
   - CI must pass (test-gate.yml)
   - At least 1 approval required
   - Address feedback with new commits
   - Squash or rebase before merge (project preference)

4. **Merge:**
   ```bash
   # Squash merge (preferred for feature branches)
   gh pr merge --squash --delete-branch
   
   # Or merge commit (preserves full history)
   gh pr merge --merge --delete-branch
   
   # Never force-push to main after merge
   ```

### Hotfix Workflow

```bash
# Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue

# Make fix
git add <files>
git commit -m "hotfix(scope): critical fix description

SEV-1 incident response. Issue details in DEC-INCIDENT-####

change-$(date +%Y%m%d)-##: Critical hotfix
Impacted IDs: SPEC-####, TEST-####
Verification: manual verification, rollback tested"

# Push and create PR
git push origin hotfix/critical-issue

# After merge, ensure fix is in all active branches
git checkout main
git pull origin main
git checkout develop
git merge main  # or cherry-pick specific commit
```

---

## 7. Git Ignore Configuration

### Project .gitignore

Already includes:

```gitignore
# Python
__pycache__/
*.py[cod]
.pytest_cache/
.venv/

# IDE
.idea/
.vscode/
.cursor/

# OS
.DS_Store
Thumbs.db

# RJW-IDD specific
logs/ci/*.log
logs/cost/*.json
logs/security/*.json
artifacts/integration/transcript-archive/*/diffs/
research/evidence_index_raw.json.bak
```

### Personal .gitignore_global

Create `~/.gitignore_global`:

```gitignore
# Personal IDE settings
.vscode/settings.json
.cursor/settings.json

# Personal notes
TODO.md
NOTES.md
scratch/

# OS files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Temporary files
*.swp
*.swo
*~
.#*
```

---

## 8. Advanced Git Operations

### Interactive Rebase (Clean History)

```bash
# Squash last 3 commits
git rebase -i HEAD~3

# In editor, change 'pick' to 'squash' or 'fixup'
# Update commit message
```

### Cherry-pick Specific Commits

```bash
# Apply specific commit to current branch
git cherry-pick <commit-hash>

# Cherry-pick with edits
git cherry-pick -e <commit-hash>
```

### Stash Work in Progress

```bash
# Save work without committing
git stash push -m "WIP: description"

# List stashes
git stash list

# Apply stash
git stash pop stash@{0}

# Apply without removing from stash
git stash apply stash@{0}
```

### Bisect for Bug Hunting

```bash
# Start bisect
git bisect start
git bisect bad  # Current commit is bad
git bisect good <known-good-commit>

# Git will checkout commits
# After each test:
git bisect good  # or git bisect bad

# When found, reset
git bisect reset
```

---

## 9. Troubleshooting

### Undo Last Commit (Not Pushed)

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes and commit
git reset --hard HEAD~1
```

### Fix Wrong Commit Message

```bash
# Amend last commit message
git commit --amend -m "corrected message"

# If already pushed (use with caution)
git push --force-with-lease origin feature/branch
```

### Recover Deleted Branch

```bash
# Find commit hash of deleted branch
git reflog

# Recreate branch at that commit
git checkout -b recovered-branch <commit-hash>
```

### Resolve Merge Conflicts

```bash
# During rebase or merge
git status  # Shows conflicted files

# Edit files, resolve conflicts
# Remove conflict markers: <<<<<<<, =======, >>>>>>>

# Mark as resolved
git add <resolved-files>

# Continue rebase
git rebase --continue

# Or abort
git rebase --abort
```

---

## 10. Verification

### Pre-push Checklist

- [ ] All tests pass locally (`pytest`)
- [ ] All guards pass (`bash scripts/ci/test_gate.sh`)
- [ ] Change log entry added
- [ ] Commit message follows convention
- [ ] No merge conflicts with main
- [ ] No debugging code or TODOs left

### Repository Health Check

```bash
# Check for uncommitted changes
git status

# Verify remote tracking
git remote -v

# Check branch relationships
git branch -vv

# Validate repository
git fsck

# Optimize repository
git gc --aggressive
```

---

## 11. References

**Related Documents:**
- `DOC-0022` — Git Workflow Runbook (step-by-step procedures)
- `DOC-0006` — Living Documentation Guidelines
- `DOC-0013` — Naming Conventions
- `METHOD-0004` — AI Agent Workflows (git integration)

**External Resources:**
- [Git Documentation](https://git-scm.com/doc)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pre-commit Framework](https://pre-commit.com/)

**Git Configuration Files:**
- `~/.gitconfig` — User-level settings
- `.git/config` — Repository-level settings
- `.gitignore` — Repository ignore patterns
- `~/.gitignore_global` — Personal ignore patterns
- `.pre-commit-config.yaml` — Hook configuration

---

## Audit Trail

| Date | Change | Author | Change ID |
|------|--------|--------|-----------|
| 2025-10-07 | Initial creation | System | change-20251007-05 |

---

**Status:** Active  
**Next Review:** 2025-11-07 or when git tooling changes
