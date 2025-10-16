# Migration Guide - Upgrading to This Version

This guide helps you migrate existing RJW-IDD projects to the latest version with CLI tooling, enhanced safety, and improved documentation.

## Version Information

**Current Version**: 0.1.0-alpha
**Previous Version**: 1.3.0
**Release Date**: 2026-02-10

## Breaking Changes

### ⚠️ None

This is a feature-additive release with no breaking changes to existing workflows.

## New Features

1. **CLI Tool** (`bin/rjw`)
   - Guard validation
   - Interactive initialization
   - Prompt pack version management

2. **Safety Hardening**
   - Agent pledge enforcement
   - Deterministic behavior guarantees
   - Config drift detection

3. **Documentation**
   - Quickstart guide
   - Solo mode workflow
   - Troubleshooting reference
   - Migration guide (this document)

4. **Configuration Management**
   - `prompt-pack.json` for versioning
   - Enhanced `features.yml` with profiles
   - CI config enforcement

5. **Accelerated Modes**
   - YOLO auto-approval prompts with explicit guard logging
   - Turbo prompts for reduced gate thresholds (`features.turbo_mode`)
   - Guard auto-ruleset selection via `rjw guard --ruleset auto`

## Migration Steps

### Step 1: Backup Current State

```bash
# Create backup branch
git checkout -b backup-pre-cli-migration
git push origin backup-pre-cli-migration

# Return to main
git checkout main
```

### Step 2: Pull Latest Changes

```bash
# If this is in your repo
git pull origin main

# OR if using subtree/submodule
git subtree pull --prefix=rjw-idd-starter-kit origin main --squash
```

### Step 3: Update Dependencies

```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# OR .\.venv\Scripts\Activate.ps1  # Windows

# Install updated dependencies
pip install -r rjw-idd-starter-kit/requirements-dev.txt
```

### Step 4: Install CLI Tool

```bash
# Make CLI executable
chmod +x rjw-idd-starter-kit/bin/rjw

# Add to PATH (optional)
export PATH="$PWD/rjw-idd-starter-kit/bin:$PATH"
echo 'export PATH="$PWD/rjw-idd-starter-kit/bin:$PATH"' >> ~/.bashrc

# Verify installation
rjw --help
```

### Step 5: Update Configuration Files

Create `prompt-pack.json` in project root:

```bash
cat > prompt-pack.json << 'EOF'
{
  "name": "rjw-prompt-pack",
  "version": "0.1.0-alpha",
  "checksum": "sha256-321fed654cba",
  "last_updated": "2026-02-10",
  "channels": ["core", "modes/yolo", "modes/turbo"],
  "compat": {
    "min_cli": ">=1.0.0"
  }
}
EOF
```

Update `method/config/features.yml` if it exists:

```bash
# Backup existing
cp method/config/features.yml method/config/features.yml.backup

# Update with profiles section
cat >> method/config/features.yml << 'EOF'

mode:
  name: standard
  turbo: false
profiles:
  lite:
    guard: true
    init: true
    prompts_version: true
    yolo_mode: false
    turbo_mode: false
    game_addin: false
  yolo:
    guard: true
    init: true
    prompts_version: true
    yolo_mode: true
    turbo_mode: false
    game_addin: false
  turbo-standard:
    guard: true
    init: true
    prompts_version: true
    yolo_mode: false
    turbo_mode: true
    game_addin: false
  turbo-yolo:
    guard: true
    init: true
    prompts_version: true
    yolo_mode: true
    turbo_mode: true
    game_addin: false
EOF
```

### Step 6: Run Migration Validation

```bash
# Run all tests
pytest

# Run governance guards
bash rjw-idd-starter-kit/scripts/ci/test_gate.sh

# Validate IDs
python rjw-idd-starter-kit/scripts/validate_ids.py

# Test CLI
rjw guard examples/ok.json
rjw prompts --version
```

### Step 7: Update Documentation

Add quickstart link to your project README:

```markdown
## Quickstart

See [docs/quickstart.md](rjw-idd-starter-kit/docs/quickstart.md) for 5-minute setup guide.
```

### Step 8: Update CI/CD (Optional)

If using GitHub Actions, add guard checks:

```yaml
# .github/workflows/rjw-guards.yml
name: RJW Guards

on: [push, pull_request]

jobs:
  guard-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r rjw-idd-starter-kit/requirements-dev.txt
      - name: Run guards
        run: bash rjw-idd-starter-kit/scripts/ci/test_gate.sh
      - name: Validate guard examples
        run: |
          chmod +x rjw-idd-starter-kit/bin/rjw
          rjw guard examples/ok.json
```

### Step 9: Update Change Log

Add migration entry to `templates-and-examples/templates/change-logs/CHANGELOG-template.md`:

```markdown
| change_id | date | description | impacted_ids | operator | verification |
|-----------|------|-------------|--------------|----------|--------------|
| change-20251007-01 | 2025-10-07 | Migrated to CLI v1.1.0 | TOOLS-CLI-GUARD, TOOLS-CLI-INIT, quickstart.md, docs/solo.md | YourName | Migration validation passed |
```

### Step 10: Commit Migration

```bash
# Stage all changes
git add .

# Commit with clear message
git commit -m "chore: Migrate to RJW-IDD v1.1.0 with CLI tooling

- Added bin/rjw CLI tool
- Created prompt-pack.json
- Updated features.yml with profiles
- Added quickstart, solo, and migration docs
- Updated dependencies

Verification: All tests and guards pass"

# Push
git push origin main
```

## Rollback Plan

If you encounter issues:

### Quick Rollback

```bash
# Return to backup branch
git checkout backup-pre-cli-migration

# Reactivate old environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r rjw-idd-starter-kit/requirements-dev.txt
```

### Partial Rollback

Keep new features but disable CLI:

```bash
# Don't add bin/ to PATH
# Continue using scripts directly
python rjw-idd-starter-kit/scripts/validate_ids.py
bash rjw-idd-starter-kit/scripts/ci/test_gate.sh
```

## Feature Adoption Timeline

You can adopt features incrementally:

### Week 1: CLI Basics
- Install CLI tool
- Use `rjw guard` for validation
- Test with existing examples

### Week 2: Integration
- Update CI to use guards
- Create validation examples
- Train team on CLI usage

### Week 3: Workflows
- Adopt quickstart for new contributors
- Use solo mode for individual work
- Reference troubleshooting guide

### Week 4: Optimization
- Add custom guard rules
- Create project-specific profiles
- Document project conventions

## Verification Checklist

After migration, verify:

- [ ] CLI tool is accessible (`rjw --help`)
- [ ] All tests pass (`pytest`)
- [ ] Guards pass (`bash scripts/ci/test_gate.sh`)
- [ ] IDs validate (`python scripts/validate_ids.py`)
- [ ] Evidence validates (`python scripts/validate_evidence.py`)
- [ ] Guard examples work (`rjw guard examples/*.json`)
- [ ] Prompts version shows (`rjw prompts --version`)
- [ ] Documentation accessible (quickstart, solo, troubleshooting)
- [ ] CI still passes (if applicable)
- [ ] Change log updated

## Common Migration Issues

### Issue: Command not found: rjw

**Cause**: CLI not in PATH or not executable

**Fix**:
```bash
chmod +x rjw-idd-starter-kit/bin/rjw
export PATH="$PWD/rjw-idd-starter-kit/bin:$PATH"
```

### Issue: ModuleNotFoundError: tools.rjw_cli

**Cause**: Python path not set correctly

**Fix**:
```bash
export PYTHONPATH="$PWD/rjw-idd-starter-kit:$PYTHONPATH"
# OR use full path
python3 rjw-idd-starter-kit/bin/rjw --help
```

### Issue: Guards fail after migration

**Cause**: New validation rules are stricter

**Fix**:
1. Review guard output: `rjw guard file.json --format json`
2. Fix violations following remediation advice
3. Use `--ruleset default` for lenient mode
4. Document exemptions in DECISION_LOG.md

### Issue: Tests fail after dependency update

**Cause**: Version conflicts or missing dependencies

**Fix**:
```bash
# Clean install
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r rjw-idd-starter-kit/requirements-dev.txt
pytest -v
```

## Support During Migration

- **Documentation**: Check `docs/troubleshooting.md`
- **Examples**: Review `docs/demos/` for sample sessions
- **Issues**: Document problems in project issues with:
  - Error messages
  - Commands run
  - Environment details (`python --version`, OS, shell)

## Post-Migration Best Practices

1. **Update onboarding docs** with new quickstart link
2. **Train team** on CLI usage
3. **Establish cadence** for prompt pack updates
4. **Monitor guards** in CI for early issue detection
5. **Document project-specific conventions** in DECISION_LOG.md

## Next Steps After Migration

1. Read [Solo Mode Guide](solo.md) for workflow optimization
2. Review [Troubleshooting Guide](troubleshooting.md) for common issues
3. Explore guard customization in `tools/rjw_cli/guard.py`
4. Set up automated prompt pack version checks
5. Share feedback on migration experience

## Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| Python | 3.9 | 3.11+ |
| pytest | 8.0 | Latest |
| pyyaml | 6.0 | Latest |
| Git | 2.30 | Latest |

## Questions?

If this migration guide doesn't cover your scenario:

1. Check existing issues in repository
2. Review decision log for similar situations
3. Document your case in `DECISION_LOG.md`
4. Open issue with detailed context
