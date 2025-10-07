# Solo Mode - One-Person RJW-IDD Workflow

This guide maps all RJW-IDD roles to a practical workflow when you're working alone.

## Role Consolidation

In solo mode, you wear all hats but with timeboxed context switching:

| Official Role | Solo Translation | Time Allocation |
|--------------|------------------|-----------------|
| **Agent Conductor** | You + AI assistant | 40% - Active coding & prompting |
| **Spec Curator** | Planning mode | 20% - Requirements & design |
| **Doc Steward** | Documentation mode | 15% - README, specs, decisions |
| **Governance Sentinel** | QA mode | 25% - Testing, validation, guards |

## Daily Workflow Loop

### Morning: Planning Mode (30-60 min)

**Role: Spec Curator**

1. Review change log and open decisions
2. Define today's requirement (`REQ-####`)
3. Draft/update relevant spec in `specs/`
4. Reserve test IDs in `artifacts/ledgers/test-ledger.csv`
5. List expected outcomes in `docs/living-docs-reconciliation.md`

**Prompt to use**: `docs/prompts/PROMPT-0003-spec-translator.md`

```bash
# Quick checklist
[ ] Today's REQ-#### defined
[ ] Spec updated
[ ] Test IDs reserved
[ ] Success criteria clear
```

### Midday: Active Development (2-3 hours)

**Role: Agent Conductor + AI**

1. Start with failing test (TDD)
2. Use prompts to guide AI implementation
3. Run guards after each change
4. Update tests as you go
5. Keep decision log for non-obvious choices

**Prompts to use**:
- `PROMPT-0001-starter-briefing.md` - Start session
- `PROMPT-0002-implementation-coach.md` - Build features
- `PROMPT-0004-test-navigator.md` - Design tests

```bash
# Development loop
while [ work remaining ]; do
  # 1. Write failing test
  pytest tests/ -k "new_feature" --maxfail=1
  
  # 2. Implement with AI
  # (use implementation-coach prompt)
  
  # 3. Run guards
  bash scripts/ci/test_gate.sh
  
  # 4. Commit when green
  git add . && git commit -m "feat: REQ-0042 - description"
done
```

### Afternoon: Documentation & QA (1-2 hours)

**Role: Doc Steward + Governance Sentinel**

1. Update change log with today's work
2. Sync living documentation
3. Run full test suite
4. Execute governance guards
5. Review decision log

**Prompts to use**:
- `PROMPT-0005-doc-sync.md` - Update docs
- `PROMPT-0006-governance-audit.md` - Check compliance
- `PROMPT-0007-change-log-author.md` - Record changes
- `PROMPT-0008-merge-ready-checklist.md` - Final review

```bash
# QA checklist
[ ] All tests pass
[ ] Guards pass (test_gate.sh)
[ ] Change log updated
[ ] Docs synchronized
[ ] Evidence validated
[ ] Decision log complete
```

## Weekly Cadence

### Monday: Research & Planning

- Run evidence harvester if needed
- Review last week's outcomes
- Plan week's requirements
- Update project roadmap

### Tuesday-Thursday: Build

- Implement features using daily loop
- Keep decision log current
- Maintain test coverage

### Friday: Governance & Documentation

- Full governance audit
- Documentation review
- Evidence validation
- Archive integration transcripts
- Plan next week

## Timeboxed Context Switching

Set explicit timers to avoid role confusion:

```bash
# Example using terminal timer
alias spec-mode='echo "SPEC CURATOR MODE - 45 min" && sleep 2700 && echo "Switch roles!"'
alias dev-mode='echo "DEVELOPMENT MODE - 90 min" && sleep 5400 && echo "Switch roles!"'
alias qa-mode='echo "QA MODE - 60 min" && sleep 3600 && echo "Switch roles!"'

# Use them
$ spec-mode
# ... do planning work ...
$ dev-mode
# ... implement features ...
$ qa-mode
# ... run tests and guards ...
```

## Checklists for Each Role

### Spec Curator Checklist

```markdown
- [ ] Requirement has unique REQ-#### ID
- [ ] Spec file exists in specs/
- [ ] Test IDs reserved in ledger
- [ ] Success criteria documented
- [ ] Dependencies identified
- [ ] Evidence linked (EVD-####)
```

### Agent Conductor Checklist

```markdown
- [ ] Test written first (red)
- [ ] Implementation makes test pass (green)
- [ ] Code reviewed (self or AI)
- [ ] Guards pass locally
- [ ] Commit message follows convention
- [ ] Decision log updated if needed
```

### Doc Steward Checklist

```markdown
- [ ] README reflects current state
- [ ] Change log has entry for today
- [ ] Living docs reconciled
- [ ] Decision recorded if architectural
- [ ] Evidence harvested if needed
- [ ] Specs updated with actuals
```

### Governance Sentinel Checklist

```markdown
- [ ] Test coverage maintained/improved
- [ ] All guards pass (test_gate.sh)
- [ ] No orphaned IDs in ledgers
- [ ] Evidence is < 14 days old
- [ ] Audit trail complete
- [ ] No security issues
```

## Tools for Solo Work

### Essential Commands

```bash
# Start work session
rjw init  # First time only

# Development cycle
pytest -v
bash scripts/ci/test_gate.sh
rjw guard output.json

# Documentation
rjw prompts --version
scripts/validate_ids.py
scripts/validate_evidence.py

# End of session
git status
git log --oneline -5
rjw guard - < agent_output.json
```

### Automation Helpers

Create aliases in `.bashrc` or `.zshrc`:

```bash
# RJW-IDD aliases
alias rjw-test='pytest && bash scripts/ci/test_gate.sh'
alias rjw-status='git status && scripts/validate_ids.py'
alias rjw-sync='git pull && bash scripts/setup/bootstrap_project.sh'
alias rjw-validate='rjw guard examples/*.json && echo "All examples valid"'
```

## Decision-Making Solo

When you're both implementer and reviewer:

1. **Use AI as rubber duck**: Explain your reasoning to the AI
2. **Document assumptions**: Write them down even if "obvious"
3. **Sleep on big choices**: Defer architectural decisions 24 hours
4. **Use decision template**: Even for solo work, follow `PROJECT-DEC-template.md`
5. **Checkpoints**: Commit often so you can roll back

## Handling Detours

### Tests Fail Unexpectedly

1. Stop and document the failure
2. Check `docs/troubleshooting.md`
3. Use `PROMPT-0004-test-navigator.md` to debug
4. Update test if requirements changed
5. Record decision if test was wrong

### Tool Missing

1. Check installation in `.venv`
2. Run `bash scripts/setup/bootstrap_project.sh`
3. Verify `requirements-dev.txt` is complete
4. Document missing tool in decision log
5. Add to bootstrap script if needed

### Partial AI Output

1. Don't proceed with incomplete code
2. Use `rjw guard` to validate output
3. Re-prompt with more specific context
4. Document in `docs/troubleshooting.md` if recurring
5. Consider `--noninteractive` mode for reproducibility

## Staying on Track

### Red Flags (Stop and Reflect)

- ⚠️ Skipping tests "just this once"
- ⚠️ Change log is 2+ days behind
- ⚠️ Guards failing but "will fix later"
- ⚠️ No evidence for >14 days
- ⚠️ Decision log empty for a week

### Green Flags (You're Doing Great)

- ✅ All tests pass before commit
- ✅ Change log updated same day
- ✅ Guards pass consistently
- ✅ Evidence current
- ✅ Can explain any decision

## When to Escape Solo Mode

Consider getting help when:

- Stuck on same problem >2 days
- Security decisions needed
- Architecture choices with broad impact
- Regulatory/compliance questions
- Performance optimization beyond basics

## Resources

- **Prompts**: `rjw-idd-starter-kit/docs/prompts/` - All 8 prompts
- **Manual**: `docs/manual/starter-kit-manual.md` - Deep dive
- **Troubleshooting**: `docs/troubleshooting.md` - Common fixes
- **Demos**: `docs/demos/` - Example sessions

## Sample Solo Day

```
09:00-09:30  Spec mode: Define REQ-0108, update SPEC-0200
09:30-11:30  Dev mode: Implement feature, write tests, pass guards
11:30-12:00  Break
12:00-13:30  Dev mode: Continue implementation, handle edge cases
13:30-14:30  Doc mode: Update change log, sync living docs
14:30-15:30  QA mode: Full test suite, governance guards, review
15:30-16:00  Wrap-up: Commit, push, archive transcripts, plan tomorrow
```

## Remember

Solo doesn't mean cutting corners. RJW-IDD's value is **traceability** and **safety**, which matter even more when you're the only reviewer.

The guards are your teammates. Let them catch mistakes before they compound.
