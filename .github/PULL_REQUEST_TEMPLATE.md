## Summary

Describe the change and why it is needed.

## Checklist
- [ ] Tests added/updated
- [ ] Docs updated (CHANGELOG, README, or relevant docs)
- [ ] Issues referenced

## Release notes

Add a short summary for the CHANGELOG entry.
## Description
<!-- Brief summary of what this PR accomplishes -->

## Type of Change
<!-- Check all that apply -->
- [ ] Feature (new functionality)
- [ ] Bug fix (fixes an issue)
- [ ] Documentation (docs only)
- [ ] Refactoring (code restructuring, no behavior change)
- [ ] Performance improvement
- [ ] Test addition/modification
- [ ] Chore (maintenance, dependencies, etc.)
- [ ] Hotfix (emergency production fix)
- [ ] Breaking change (requires version bump)

## RJW-IDD Governance Checklist
<!-- All items must be checked before merge -->
- [ ] **Tests added/updated** — Red-green cycle followed per METHOD-0004
- [ ] **Documentation updated** — Living docs synchronized per DOC-0006
- [ ] **Change log entry added** — Entry in `docs/change-log.md` with format `change-YYYYMMDD-##`
- [ ] **Governance guards pass locally** — `bash scripts/ci/test_gate.sh` succeeds
- [ ] **Linked IDs updated** — Requirement/test ledgers reflect changes
- [ ] **Evidence current** — If research artifacts changed, evidence is <14 days old
- [ ] **Decision documented** — If material decision made, DEC-#### created
- [ ] **Integration artifacts** — If cross-system work, transcript archived

## Impacted Artifacts
<!-- List RJW-IDD artifacts changed or created -->

**Specifications:**
- SPEC-####: Description
- SPEC-####: Description

**Tests:**
- TEST-####: Description
- TEST-####: Description

**Documentation:**
- DOC-####: Description
- DOC-####: Description

**Requirements:**
- REQ-####: Description

**Decisions:**
- DEC-####: Description

**Evidence:**
- EVD-####: Description

## Implementation Details
<!-- Technical explanation of changes -->

### Files Changed
<!-- Brief description of major file changes -->

### Approach
<!-- Explain the solution approach taken -->

### Alternatives Considered
<!-- Other approaches evaluated and why they were rejected -->

## Verification

### Automated Testing
<!-- Paste test results -->
```
pytest output:
[paste results]

Guard validation:
bash scripts/ci/test_gate.sh
[paste results]
```

### Manual Testing
<!-- Describe manual testing performed -->
- [ ] Step 1: Description
- [ ] Step 2: Description
- [ ] Step 3: Description

**Test Environment:**
- OS: 
- Python Version: 
- Key Dependencies: 

### Performance Impact
<!-- If applicable, describe performance changes -->
- Baseline: 
- After change: 
- Impact: 

## Breaking Changes
<!-- If any breaking changes, describe migration path -->
- [ ] No breaking changes

**If breaking changes:**
- What breaks: 
- Migration steps: 
- Documentation: 

## Security Considerations
<!-- Any security implications -->
- [ ] No security impact
- [ ] Security review completed
- [ ] Credentials/secrets properly handled
- [ ] Input validation added
- [ ] Authorization checks added

## Add-on Specific
<!-- If using add-ons, complete relevant section -->

### 3D Game Core
- [ ] Profile updated: [generic/first_person/third_person/etc.]
- [ ] Determinism harness run: PASSED/FAILED
- [ ] Performance budget check: PASSED/FAILED
- [ ] Asset linting: PASSED/FAILED

### Video AI Enhancer
- [ ] Profile updated: [baseline/live_stream/broadcast/etc.]
- [ ] Latency guard: PASSED/FAILED
- [ ] Quality gate: PASSED/FAILED
- [ ] Storage validation: PASSED/FAILED

## Change Log Entry
<!-- Copy exact entry added to docs/change-log.md -->
```
change-YYYYMMDD-##: Brief description
Impacted IDs: SPEC-####, REQ-####, TEST-####, DOC-####
Verification: pytest passes, guards pass, [additional verification]
```

## Deployment Notes
<!-- Any special deployment considerations -->
- [ ] No special deployment needed
- [ ] Database migrations required
- [ ] Configuration changes required
- [ ] Dependencies added/updated
- [ ] Environment variables changed
- [ ] Cache invalidation needed
- [ ] Rollback plan documented

## Screenshots/Evidence
<!-- If UI changes or visual evidence helpful -->


## Related Issues/PRs
<!-- Link related work -->
Fixes #
Closes #
Related to #
Depends on #
Blocks #

## Reviewer Notes
<!-- Anything specific reviewers should focus on -->


## Post-Merge Actions
<!-- Tasks to complete after merge -->
- [ ] Update production documentation
- [ ] Notify stakeholders
- [ ] Schedule follow-up work
- [ ] Update related repositories
- [ ] Backport to release branches

---

## For Reviewers

### Review Checklist
- [ ] Code follows project conventions
- [ ] Tests are adequate and pass
- [ ] Documentation is clear and complete
- [ ] No debugging code or console.logs
- [ ] No TODOs or FIXMEs without tickets
- [ ] Error handling is appropriate
- [ ] Security best practices followed
- [ ] Performance considerations addressed
- [ ] Change log entry is accurate

### RJW-IDD Governance Review
- [ ] All guards pass in CI
- [ ] Change log format correct
- [ ] IDs properly formatted and linked
- [ ] Evidence freshness acceptable
- [ ] Living docs synchronized
- [ ] Decision records complete

### Questions for Author
<!-- Reviewers: Add questions here -->


---

**Merge Strategy Recommendation:**
- [ ] Squash and merge (default for feature branches)
- [ ] Merge commit (preserve detailed history)
- [ ] Rebase and merge (maintain linear history)

<!-- 
Template Version: 1.0
Last Updated: 2025-10-07
Related: DOC-0021, DOC-0022
-->
