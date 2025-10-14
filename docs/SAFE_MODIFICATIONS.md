# Safe Modifications Guide

⚠️ **SAFETY GATE WARNING** ⚠️

You are about to modify the RJW-IDD Starter Kit. This will affect the method's output and behavior.

## Before You Continue

**Ask yourself:**
- Do I understand how this change affects the method?
- Am I prepared to maintain this modification?
- Have I documented why this change is necessary?

## Common Safe Modifications

These modifications are generally safe and well-supported:

### 1. Adding Project-Specific Templates
```bash
# Add a new agent template
./scripts/safety/modify_starter.py --add-template my-template.md

# Add a new decision template
./scripts/safety/modify_starter.py --add-decision-template PROJECT-DEC-XXXX.md
```

### 2. Customizing Configuration
```bash
# Modify feature flags
./scripts/safety/modify_starter.py --update-config method/config/features.yml

# Add project-specific addons
./scripts/safety/modify_starter.py --enable-addon custom-addon
```

### 3. Extending Prompt Library
```bash
# Add project-specific prompts
./scripts/safety/modify_starter.py --add-prompt PROMPT-PROJ-001.md

# Update existing prompt with project context
./scripts/safety/modify_starter.py --extend-prompt PROMPT-0001 --context "project-specific-info"
```

## Things to Watch Out For

❌ **DANGEROUS MODIFICATIONS:**
- Changing core method files in `rjw-idd-methodology/core/`
- Modifying governance checklists without understanding impact
- Removing required validation steps
- Breaking the isolation model

⚠️ **RISKY MODIFICATIONS:**
- Changing ledger templates (affects audit trail)
- Modifying sync scripts without testing
- Altering CI/test infrastructure
- Changing prompt IDs (breaks traceability)

✅ **SAFE MODIFICATIONS:**
- Adding new templates
- Extending configuration options
- Adding project-specific documentation
- Creating custom addons

## Safety Gate Process

1. **Consent Required**: Modifications require explicit consent via `.starter_kit_modifications_allowed` file
2. **Audit Logging**: All modifications are logged in `.starter_kit_modifications.log`
3. **Impact Warning**: Each modification shows expected impact
4. **Rollback Option**: Modifications can be reverted using backup system

## Getting Consent

To enable modifications, create a consent file:

```bash
echo '{
  "consent": true,
  "timestamp": "'$(date -Iseconds)'",
  "user_acknowledgment": "I understand this affects the method output",
  "project": "'$(basename $(pwd))'",
  "modifications_approved": [
    "add-template",
    "update-config",
    "add-prompt"
  ]
}' > .starter_kit_modifications_allowed
```

## Comprehensive Reference

For complete modification documentation, see:
**[STARTER_KIT_MODIFICATION_REFERENCE.md](STARTER_KIT_MODIFICATION_REFERENCE.md)**

This reference contains:
- Complete API for all modification types
- Advanced configuration options
- Troubleshooting guide
- Migration patterns
- Breaking change warnings

## Need Help?

If you're unsure about a modification:
1. Check the comprehensive reference first
2. Test in a isolated copy
3. Document the change in your project's IDD-DOCS
4. Consider if this should be contributed back to the method

Remember: The starter kit is your agent's brain. Modifications change how it thinks and behaves.