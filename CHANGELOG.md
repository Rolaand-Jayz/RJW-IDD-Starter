# Changelog

All notable changes to the RJW-IDD Starter Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-07

### Added

#### CLI Tooling
- **`bin/rjw` CLI tool** - Unified command-line interface for all RJW-IDD operations
- **`rjw guard` command** - Validates agent outputs against safety policy with deterministic behavior
  - Exit codes: 0 (pass), 2 (violation), 3 (schema error), 4 (I/O error), 5 (internal error)
  - JSON and text output formats
  - Default and strict rulesets
  - Validation gates: schema, forbidden capabilities, file operations, network calls, provenance, tool allowlist
- **`rjw init` command** - Interactive project initialization with numbered steps
  - Three presets: default, lite, game
  - Non-interactive mode for automation
  - Safe defaults with explicit confirmations
  - Generates DECISION_LOG.md documenting choices
- **`rjw prompts` command** - Prompt pack version management
  - `--version` flag to check current version
  - `--online` flag for update checks
  - Offline-first behavior

#### Safety & Governance
- **Agent Pledge hardening** - Embedded in CLI help and runtime behavior
  - Fail safe, not silent
  - No destructive defaults
  - Deterministic CLI behavior
  - Config drift detection
  - Transparent changes via decision logs
  - No hidden network calls without `--online` flag
- **Config enforcement script** (`scripts/config_enforce.py`) - Detects drift between `features.yml` and enabled features
- **Doc sync script** (`scripts/doc_sync.py`) - Validates code-doc synchronization using `@doc-sync` tags

#### Documentation
- **`docs/quickstart.md`** - 5-minute setup guide with verification steps
- **`docs/solo.md`** - One-person workflow mapping all roles to timeboxed activities
- **`docs/migrate-to-this-version.md`** - Comprehensive migration guide with rollback plan
- **`docs/troubleshooting.md`** - Copy-paste fixes for common issues (updated)
- **`docs/demos/`** - CLI session transcripts:
  - `guard-pass.md` - Successful validation example
  - `guard-fail.md` - Failed validation with remediation
  - `init-session.md` - Interactive and non-interactive init flows
  - `prompts-version.md` - Version checking workflows

#### Installation & Setup
- **`install.sh`** - Cross-platform installation script for Linux/macOS
- **`install.ps1`** - Windows PowerShell installation script
- **`requirements.txt`** - Core dependencies (pytest, pyyaml)
- **`prompt-pack.json`** - Prompt versioning metadata with channels and compatibility info

#### Examples & Tests
- **`examples/ok.json`** - Valid agent output passing all guards
- **`examples/bad.json`** - Invalid agent output demonstrating violations
- **`tests/test_guard.py`** - Unit tests for guard validation (8 tests)
- **`tests/test_init.py`** - Unit tests for init command (4 tests)
- **`tests/test_prompts.py`** - Unit tests for prompts command (4 tests)

#### Configuration
- **Enhanced `features.yml`** - Added profiles section with lite profile
- **`prompt-pack.json` schema** - Versioning, channels, compatibility tracking

### Changed

#### Documentation Updates
- **README.md** - Added quickstart links, guard examples, solo mode link, CLI installation steps
- **`docs/troubleshooting.md`** - Expanded with CLI-specific troubleshooting, branch/loop prompts for detours
- **Starter kit READMEs** - Updated with CLI references and new workflow guidance

#### Safety Improvements
- Guard validation is now deterministic and reproducible
- All CLI operations have stable exit codes
- Network operations require explicit `--online` flag
- File operations must be signed and sandboxed
- Config drift auto-detected in CI

#### Workflow Enhancements
- Init process uses numbered steps (1/7 through 7/7) for clarity
- All destructive operations require explicit confirmation
- Decision logs automatically created documenting all choices
- Beginner-friendly error messages with remediation steps

### Fixed
- Removed hardcoded `.venv` from repository (now created by install scripts)
- Standardized Python version requirement (3.9+) across all scripts
- Made CLI cross-platform (Linux/macOS/Windows)
- Improved error handling with actionable remediation advice

### Security
- Guard prevents unsigned file writes
- Guard blocks writes outside sandbox directories
- Guard catches forbidden code patterns (eval, exec, os.system)
- Guard validates network operations have explicit permission
- All changes logged in decision log for audit trail

### Developer Experience
- One-command installation: `bash install.sh && rjw init`
- Self-documenting CLI with `--help` on all commands
- Demo transcripts provide copy-paste examples
- Solo mode guide enables single-developer workflow
- Troubleshooting guide has copy-paste fixes

### CI/CD
- Config enforcement check (detects features.yml drift)
- Doc sync check (validates code-doc alignment)
- Guard validation (runs on sample artifacts)
- All checks exit with stable codes for automation

### Breaking Changes
**None** - This is a backward-compatible release. All existing workflows continue to work.

### Migration
See `docs/migrate-to-this-version.md` for detailed upgrade instructions.

### Deprecations
**None** in this release.

### Known Issues
- `rjw prompts --update` is a placeholder (manual update required)
- Doc sync script doesn't validate all code fence languages yet
- Config enforcement only checks core features (addon validation minimal)

### Contributors
This release focuses on novice safety, onboarding, and maintainability per community feedback.

---

## [1.0.0] - 2025-10-03

### Added
- Initial release of RJW-IDD Starter Kit
- Core methodology documents
- Evidence harvester
- Test guards (red-green, change log, living docs, governance alignment)
- Prompt library (8 core prompts)
- Bootstrap scripts
- Ledger management
- Decision templates
- Living documentation system

### Documentation
- Starter kit manual
- API standards
- i18n guide
- IDE setup
- Governance runbooks

---

## Format Notes

### Change Types
- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements

### Versioning
- MAJOR version: Incompatible API changes
- MINOR version: Backward-compatible functionality additions
- PATCH version: Backward-compatible bug fixes

### Links
- [1.1.0]: https://github.com/Rolaand-Jayz/Rolaand-Jayz-Wayz-IDD/releases/tag/v1.1.0
- [1.0.0]: https://github.com/Rolaand-Jayz/Rolaand-Jayz-Wayz-IDD/releases/tag/v1.0.0
