# Starter Kit Modification Reference

Complete guide for modifying the RJW-IDD Starter Kit safely and effectively.

## Table of Contents
- [Overview](#overview)
- [Modification API](#modification-api)
- [File Structure Impact](#file-structure-impact)
- [Advanced Configuration](#advanced-configuration)
- [Breaking Changes](#breaking-changes)
- [Troubleshooting](#troubleshooting)
- [Migration Patterns](#migration-patterns)

## Overview

The RJW-IDD Starter Kit is designed to be extensible while maintaining method integrity. This reference documents all supported modification patterns.

### Modification Categories

| Category | Risk Level | Approval Required | Auto-Rollback |
|----------|------------|-------------------|---------------|
| Template Addition | Low | No | Yes |
| Configuration Update | Medium | Yes | Yes |
| Core Method Change | High | Yes | Manual |
| Governance Modification | Critical | Yes | Manual |

## Modification API

### Command Line Interface

```bash
# Base command
./scripts/safety/modify_starter.py [OPTIONS] [MODIFICATION_TYPE] [ARGS]

# Global options
--consent-file PATH     # Custom consent file location
--audit-log PATH        # Custom audit log location  
--dry-run              # Preview changes without applying
--backup               # Create backup before modification
--force                # Skip safety confirmations (dangerous)
```

### Template Operations

#### Add Agent Template
```bash
./scripts/safety/modify_starter.py --add-template \
  --file my-template.md \
  --id AGENT-CUSTOM-001 \
  --role agent \
  --tags custom,project
```

Template Structure:
```yaml
---
id: AGENT-CUSTOM-001
version: 1
role: agent
visibility: internal
tags: [custom, project]
description: Project-specific agent template
---

Template content here...
```

#### Add Decision Template
```bash
./scripts/safety/modify_starter.py --add-decision-template \
  --file PROJECT-DEC-XXXX.md \
  --category governance \
  --impact medium
```

### Configuration Operations

#### Update Feature Flags
```bash
./scripts/safety/modify_starter.py --update-config \
  --file method/config/features.yml \
  --key custom_addon_enabled \
  --value true
```

#### Add Addon Configuration
```bash
./scripts/safety/modify_starter.py --add-addon \
  --name custom-addon \
  --type experimental \
  --dependencies "numpy>=1.21.0"
```

### Prompt Operations

#### Extend Existing Prompt
```bash
./scripts/safety/modify_starter.py --extend-prompt \
  --id PROMPT-0001 \
  --add-section "## Project Context" \
  --content "Custom project instructions..."
```

#### Add Custom Prompt
```bash
./scripts/safety/modify_starter.py --add-prompt \
  --file PROMPT-PROJ-001.md \
  --role user \
  --category project-specific
```

## File Structure Impact

### Safe Modification Zones

✅ **Always Safe:**
```
rjw-idd-starter-kit/
├── docs/prompts/agent/           # Add custom agent templates
├── method/config/                # Extend configuration
├── scripts/addons/               # Custom addon scripts
└── templates-and-examples/       # Project templates
```

⚠️ **Modification with Care:**
```
rjw-idd-starter-kit/
├── docs/prompts/user/            # Managed by sync script
├── scripts/ci/                   # Test carefully
├── tools/                        # Validate compatibility
└── artifacts/ledgers/            # Backup before changes
```

❌ **Dangerous Zones:**
```
rjw-idd-methodology/
├── core/                         # Method fundamentals
├── governance/                   # Audit requirements
└── operations/                   # Production workflows
```

### Isolation Boundaries

The isolation model protects these areas:

1. **Project Artifacts** → `/IDD-DOCS/`
   - Research, specs, decisions
   - Generated prompts
   - Project-specific documentation

2. **Starter Kit Core** → `rjw-idd-starter-kit/`
   - Templates and methodology
   - Core scripts and tools
   - Governance framework

3. **Method Definition** → `rjw-idd-methodology/`
   - Immutable method definition
   - Role handbooks
   - Audit checklists

## Advanced Configuration

### Custom Addon Development

Create a new addon:

```bash
# 1. Create addon structure
mkdir -p rjw-idd-starter-kit/scripts/addons/my-custom-addon/

# 2. Add addon configuration
./scripts/safety/modify_starter.py --create-addon \
  --name my-custom-addon \
  --description "Custom project addon" \
  --author "$(git config user.name)" \
  --version "1.0.0"

# 3. Implement addon logic
# See templates-and-examples/templates/addons/ for patterns
```

### Template Inheritance

Extend existing templates:

```yaml
# my-extended-template.md
---
id: AGENT-EXTENDED-001
version: 1
role: agent
extends: PROMPT-AGENT-CORE-NOVICE-FLOW
visibility: internal
tags: [extended, project]
description: Extended version of core novice flow
overrides:
  - section: "Rules"
  - section: "Initial step"
---

# Extended content that builds on base template
```

### Configuration Schema Validation

Custom configuration must follow schema:

```json
{
  "$schema": "method/config/schema.json",
  "custom_settings": {
    "addon_name": {
      "enabled": true,
      "config": {
        "setting1": "value1",
        "setting2": 42
      }
    }
  }
}
```

## Breaking Changes

### Major Version Changes

When modifying core components, document breaking changes:

```markdown
## BREAKING CHANGE: v2.0.0

### What Changed
- Modified core agent template format
- Added required `priority` field to all templates

### Migration Required
1. Update all custom templates to include `priority` field
2. Run migration script: `./scripts/migrate/v1_to_v2.py`
3. Test all custom prompts still work

### Rollback Plan
- Backup created automatically in `.modifications/backups/`
- Rollback command: `./scripts/safety/rollback.py --to-version v1.9.0`
```

### Compatibility Matrix

| Starter Kit Version | Method Version | Compatibility |
|-------------------|----------------|---------------|
| 2.0.x | 1.4.x | ✅ Full |
| 2.0.x | 1.3.x | ⚠️ Limited |
| 1.9.x | 1.4.x | ⚠️ Deprecated |
| 1.9.x | 1.3.x | ✅ Full |

## Troubleshooting

### Common Issues

#### Modification Blocked
```
Error: Safety gate blocked modification
Solution: Create consent file or check permissions
```

#### Template Validation Failed
```
Error: Invalid YAML frontmatter in template
Solution: Check required fields (id, version, role, visibility)
```

#### Sync Script Errors
```
Error: Prompt generation failed
Solution: Validate agent templates have correct format
```

#### Addon Conflicts
```
Error: Addon dependency conflict
Solution: Check compatibility matrix, update dependencies
```

### Debug Mode

Enable verbose logging:

```bash
export RJW_DEBUG=1
./scripts/safety/modify_starter.py --debug [COMMAND]
```

### Recovery Procedures

#### Restore from Backup
```bash
./scripts/safety/restore.py --from-backup latest
./scripts/safety/restore.py --from-backup 2025-10-13T16:30:00Z
```

#### Reset to Clean State
```bash
./scripts/safety/reset.py --confirm-data-loss
```

## Migration Patterns

### From Standalone to Project Integration

When moving from standalone starter kit to project integration:

1. **Preserve Customizations:**
   ```bash
   ./scripts/migrate/export_customizations.py > my-customizations.json
   ```

2. **Set Up Project Structure:**
   ```bash
   mkdir -p IDD-DOCS/{prompts,research,specs,decisions}
   ```

3. **Import Customizations:**
   ```bash
   ./scripts/migrate/import_customizations.py my-customizations.json
   ```

### Version Upgrades

Safe upgrade process:

```bash
# 1. Export current state
./scripts/safety/export_state.py > current-state.json

# 2. Backup everything
./scripts/safety/backup.py --full

# 3. Upgrade starter kit
git pull origin main

# 4. Migrate customizations
./scripts/migrate/apply_customizations.py current-state.json

# 5. Validate everything works
./scripts/ci/test_gate.sh
```

## Safety Checklist

Before making any modification:

- [ ] Have I read the safe modifications guide?
- [ ] Do I understand the impact of this change?
- [ ] Have I created a backup?
- [ ] Is there a rollback plan?
- [ ] Will this break the isolation model?
- [ ] Have I tested in a copy first?
- [ ] Is this documented in IDD-DOCS?
- [ ] Should this be contributed back to the method?

## Contributing Modifications Back

If your modification would benefit others:

1. **Generalize the Change:** Remove project-specific details
2. **Add Tests:** Follow TDD workflow
3. **Document Impact:** Update method documentation
4. **Submit PR:** Follow contribution guidelines
5. **Update Migration:** Provide upgrade path

Remember: The starter kit is a shared resource. Modifications that improve the method for everyone should be contributed back to the community.