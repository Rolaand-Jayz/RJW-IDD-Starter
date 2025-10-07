# Quickstart Guide

Get up and running with RJW-IDD in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- Git
- Terminal access (bash/zsh on Linux/macOS, PowerShell on Windows)

## Installation

### Linux/macOS

```bash
cd /path/to/project
bash rjw-idd-starter-kit/install.sh
source .venv/bin/activate
rjw init
```

### Windows

```powershell
cd C:\path\to\project
.\rjw-idd-starter-kit\install.ps1
.\.venv\Scripts\Activate.ps1
rjw init
```

## Your First Steps

### 1. Initialize Your Project

```bash
rjw init
```

Follow the numbered prompts:
- **[1/7]** Enter your project name
- **[2/7]** Verify Python runtime
- **[3/7]** Create virtual environment
- **[4/7]** Select features (guard, init, prompts-version)
- **[5/7]** Write configuration files
- **[6/7]** Run smoke tests
- **[7/7]** Review next steps

### 2. Validate Agent Outputs

Create a test file `test-output.json`:

```json
{
  "agent_id": "copilot",
  "timestamp": "2025-10-07T10:00:00Z",
  "version": "1.0",
  "actions": [
    {
      "type": "read_file",
      "path": "./README.md"
    }
  ]
}
```

Run validation:

```bash
rjw guard test-output.json
```

Expected output:
```
✔ Validation passed (ruleset=default, errors=0, warnings=0)
```

### 3. Check Prompt Pack Version

```bash
rjw prompts --version
```

Expected output:
```
rjw-prompt-pack 1.0.0 (sha256-placeholder...)
Last updated: 2025-10-07
```

### 4. Start Development

1. **Read the solo workflow guide**: `docs/solo.md`
2. **Review prompts**: `rjw-idd-starter-kit/docs/prompts/`
3. **Bootstrap the environment**: `bash rjw-idd-starter-kit/scripts/setup/bootstrap_project.sh`
4. **Run tests**: `pytest`
5. **Check guards**: `bash rjw-idd-starter-kit/scripts/ci/test_gate.sh`

## Verification

Run these commands to verify your setup:

```bash
# Check CLI is accessible
rjw --help

# Verify features are configured
cat method/config/features.yml

# Run guard on sample data
echo '{"actions": []}' | rjw guard - --format json

# Check Python environment
python --version
pytest --version
```

## Common Issues

### Command not found: rjw

**Solution**: Add bin directory to PATH or use full path:

```bash
export PATH="$PWD/rjw-idd-starter-kit/bin:$PATH"
# OR
./rjw-idd-starter-kit/bin/rjw --help
```

### Permission denied: install.sh

**Solution**: Make script executable:

```bash
chmod +x rjw-idd-starter-kit/install.sh
bash rjw-idd-starter-kit/install.sh
```

### Module not found errors

**Solution**: Activate virtual environment:

```bash
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows
```

## Next Steps

- Read **[Solo Mode Guide](solo.md)** for one-person workflow
- Review **[Troubleshooting Guide](troubleshooting.md)** for common issues
- Explore **[Agent Pledge](#)** for AI safety guidelines
- Check **[Starter Kit Manual](manual/starter-kit-manual.md)** for comprehensive documentation

## Quick Reference

| Command | Purpose |
|---------|---------|
| `rjw guard <file>` | Validate agent output against policy |
| `rjw init` | Initialize new project |
| `rjw prompts --version` | Check prompt pack version |
| `bash scripts/ci/test_gate.sh` | Run all governance guards |
| `pytest` | Run test suite |

## Support

- **Documentation**: `docs/` directory
- **Issues**: Report problems with specific error messages
- **Community**: See `docs/troubleshooting.md` for resources
