# RJW-IDD Initialization Decision Log

Date: 2025-10-07

## Context

This update (v1.1.0) adds CLI tooling, safety hardening, and comprehensive documentation to the RJW-IDD Starter Kit to make it safer for novices and easier to maintain.

## Decisions Made During Implementation

### 1. CLI Design

**Decision:** Implement `rjw` as a Python CLI with subcommands rather than individual scripts.

**Rationale:**
- Unified interface easier for beginners
- Consistent help system (`rjw --help`, `rjw guard --help`)
- Stable exit codes across all commands
- Easier to extend with new commands

**Alternatives Considered:**
- Individual shell scripts (rejected: harder to maintain)
- Make-based commands (rejected: not cross-platform)
- Node.js CLI (rejected: adds dependency)

### 2. Exit Code Convention

**Decision:** Use deterministic exit codes:
- 0 = success
- 1 = general error
- 2 = policy violation
- 3 = schema error
- 4 = I/O error
- 5 = internal error

**Rationale:**
- CI/CD systems rely on exit codes
- Deterministic behavior required by Agent Pledge
- Matches Unix conventions
- Easy to document and test

### 3. Offline-First for Prompt Versioning

**Decision:** Default to offline mode; require explicit `--online` flag for network checks.

**Rationale:**
- No hidden network calls (Agent Pledge)
- Deterministic behavior in CI
- Faster operation
- Respects bandwidth constraints
- Explicit user intent

**Trade-off:** Users must opt-in to update checks, but this aligns with safety principles.

### 4. Guard Validation Strategy

**Decision:** Implement both "default" and "strict" rulesets.

**Rationale:**
- Default: Beginner-friendly, focuses on critical safety
- Strict: Production-ready, enforces all governance rules
- Allows gradual adoption
- Teams can customize per environment

**Default Ruleset Checks:**
- Schema validity
- Forbidden capabilities (eval, exec, os.system)
- File operation safety (unsigned writes, sandbox violations)
- Network authorization
- Tool allowlist

**Strict Ruleset Adds:**
- Provenance field requirements
- Timestamp validation
- Version compatibility checks

### 5. Init Flow: Numbered Steps

**Decision:** Use numbered steps (1/7 through 7/7) instead of progress bar or unstructured flow.

**Rationale:**
- Clear progress indication
- Each step can be explained before execution
- Easy to resume if interrupted
- Matches novice mental model
- Works in all terminal types

**Steps Chosen:**
1. Project name
2. Runtime check
3. Environment setup
4. Feature selection
5. Config write
6. Smoke tests
7. Next steps summary

### 6. Decision Log Auto-Generation

**Decision:** Automatically create `DECISION_LOG.md` during `rjw init`.

**Rationale:**
- Transparency (Agent Pledge)
- Audit trail from day one
- Documents default choices
- Helps teams review decisions later
- Low friction for users

### 7. Installation Scripts: Bash + PowerShell

**Decision:** Provide both `install.sh` (Unix) and `install.ps1` (Windows) rather than Python-only installer.

**Rationale:**
- Cross-platform from day one
- Bash/PowerShell are platform defaults
- Can check Python before running Python code
- Native error handling per platform
- Familiar to system administrators

**Alternatives Considered:**
- Python-only (rejected: bootstrapping problem)
- Docker-only (rejected: too heavyweight for starter kit)

### 8. Examples: ok.json and bad.json

**Decision:** Include both passing and failing guard examples in repository.

**Rationale:**
- Self-documenting
- Easy to test guard is working
- CI can validate both paths
- Users learn by example
- Demo transcripts reference these files

### 9. Doc Sync Tags

**Decision:** Use `@doc-sync:<tag>` format in code comments.

**Rationale:**
- Simple grep-able pattern
- Unique prefix avoids false positives
- Tags are human-readable
- Can extend with metadata later
- Works in any programming language

**Format:** `@doc-sync:FEATURE-NAME` (e.g., `@doc-sync:guard-validation`)

### 10. Config Enforcement Strategy

**Decision:** Discover actual feature state from file system, not just parse config.

**Rationale:**
- Detects real drift (files present but config says disabled)
- Cannot be fooled by stale config
- Validates entire deployment, not just YAML
- Provides remediation steps

**Discovery Methods:**
- CLI exists → guard/init enabled
- prompt-pack.json exists → prompts_version enabled
- Addon directories exist → game_addin enabled
- Features.yml read for addon settings

### 11. Lite Profile for Small Projects

**Decision:** Provide "lite" profile that skips heavy checks (determinism, asset validation).

**Rationale:**
- Small projects don't need full game engine governance
- Reduces barrier to entry
- Can graduate to full profile later
- Performance gates still checked
- Safety still enforced

**Lite Profile Includes:**
- FPS threshold check
- Memory limit check
- Basic telemetry

**Lite Profile Skips:**
- Determinism replay
- Rollback tape validation
- Asset manifest checking
- Complex performance profiling

### 12. Dummy Telemetry Generator

**Decision:** Provide `dummy_telemetry.py` that generates valid metrics without requiring game engine.

**Rationale:**
- Enables CI testing without engine
- Documents schema by example
- Useful for mocking in tests
- Shows expected format
- Deterministic for test stability

**Trade-off:** Not real metrics, but validates infrastructure.

### 13. Documentation Structure

**Decision:** Create separate guides for different audiences:
- `quickstart.md` → First-time users (5 minutes)
- `solo.md` → Solo developers (workflow)
- `game-setup.md` → Game developers (addon)
- `migrate-to-this-version.md` → Upgraders
- `troubleshooting.md` → Problem solvers

**Rationale:**
- Right depth for each audience
- Can read just what's needed
- Clear entry points
- Reduces cognitive load
- Easy to maintain separately

**Alternative Considered:** Single comprehensive manual (rejected: overwhelming for beginners)

### 14. Demo Transcripts Format

**Decision:** Use markdown files with command-output pairs rather than GIFs or videos.

**Rationale:**
- Copy-paste friendly
- Searchable
- Version controllable
- Accessible to screen readers
- Easy to update
- Works in all viewers

### 15. CI Workflows: Individual Files

**Decision:** Create 4 separate workflow files rather than one monolithic file.

**Rationale:**
- Clear responsibilities
- Can enable/disable independently
- Easier to debug failures
- Parallel execution
- Selective triggering (e.g., nightly for doc-sync)

**Workflows:**
1. `guard.yml` - Every push/PR
2. `config-enforce.yml` - Every push/PR
3. `doc-sync-nightly.yml` - Scheduled
4. `addins.yml` - Conditional on feature enabled

### 16. No Breaking Changes

**Decision:** Make v1.1.0 fully backward compatible with v1.0.0.

**Rationale:**
- Existing projects continue working
- Users adopt new features at their pace
- Reduces migration friction
- Builds trust
- All new functionality is opt-in

### 17. Prompt Pack Versioning

**Decision:** Use semantic versioning for prompt packs with SHA-256 checksum.

**Rationale:**
- Detects tampering
- Reproducible builds
- Clear compatibility rules
- Standard versioning scheme
- Can verify integrity

**Format:** `<name> <version> (sha256-<hex>)`

### 18. Test Strategy

**Decision:** Unit tests + integration tests + demo transcripts.

**Rationale:**
- Unit tests: Fast, cover logic
- Integration tests: End-to-end CLI
- Demo transcripts: Documentation + validation
- All three together provide confidence

**Coverage:**
- Unit: 17 tests
- Integration: 7 CLI commands tested
- Demos: 4 transcripts

### 19. Error Messages Include Remediation

**Decision:** Every error message must include actionable remediation step.

**Rationale:**
- Novice-friendly (don't just say "error")
- Reduces support burden
- Teaches as it fails
- Aligns with "fail safe" principle
- Builds user confidence

**Format:** `ERROR: <what went wrong>. Remediation: <how to fix it>.`

### 20. File Operations Must Be Sandboxed

**Decision:** Guard rejects writes outside `./sandbox/` or `./workspace/` unless explicitly signed.

**Rationale:**
- Prevents accidental system file modification
- Clear boundary for safe operations
- Easy to audit
- Can relax for specific cases
- Aligns with security best practices

## Assumptions Made

1. **Python 3.9+ available** - Documented in requirements
2. **Git installed** - Needed for version control (documented)
3. **Terminal access** - Required for CLI (documented)
4. **Write permissions** - In project directory (validated by install script)
5. **Internet optional** - Works fully offline (documented)

## Defaults Chosen

| Choice | Default | Rationale |
|--------|---------|-----------|
| Preset | default | Balanced features |
| Output format | text | Human-readable |
| Ruleset | default | Beginner-friendly |
| Network | offline | Safe, no surprises |
| Interactive | yes | Novice-friendly |
| Venv | create | Isolated environment |
| Dependencies | install | Complete setup |
| Tests | run | Verify immediately |

## Non-Obvious Implementations

### 1. Config Enforcement Uses File System
Rather than just parsing YAML, we check if files actually exist. This catches more drift scenarios.

### 2. Guard Validation is Recursive
We scan nested objects/arrays for violations, not just top-level fields.

### 3. Decision Log is Markdown
Not JSON or YAML - Markdown is more readable for humans and still processable.

### 4. CLI is Python Script, Not Entry Point
Uses `#!/usr/bin/env python3` shebang for maximum compatibility. Setup.py entry points added later if needed.

### 5. Exit Codes Follow Unix Convention
But extended with specific codes (2=violation, 3=schema, 4=I/O, 5=internal) for automation.

## Migration from This Decision Log

When upgrading from v1.0.0:
1. Review this log for context
2. Run install script to set up new CLI
3. Use `rjw init` to generate configs
4. Reference migration guide for steps
5. Adopt features incrementally

## Rationale Summary

All choices prioritized:
- **Safety first** - No destructive defaults
- **Beginner-friendly** - Clear errors, explicit steps
- **Deterministic** - Same inputs → same outputs
- **Transparent** - Decision logs for all choices
- **Reversible** - Can roll back easily
- **Cross-platform** - Linux, macOS, Windows
- **Offline-capable** - No forced network calls
- **Well-documented** - Guides for every audience

## Review and Update

This decision log should be updated when:
- New CLI commands added
- Exit codes changed
- Guard rules modified
- Presets added/removed
- Installation process changes
- Major assumptions invalidated

**Last Updated:** 2025-10-07  
**Version:** 1.1.0  
**Status:** Final
