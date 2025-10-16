# Demo: RJW Prompts Version

## Scenario
Checking the current prompt pack version and checking for updates.

## Basic Version Check

```bash
$ rjw prompts --version
rjw-prompt-pack 1.0.0-alpha (sha256-abc123de...)
Last updated: 2025-10-07
```

## Check for Updates (Online)

```bash
$ rjw prompts --version --online
rjw-prompt-pack 1.0.0-alpha (sha256-abc123de...)
Last updated: 2025-10-07
Update available: 1.1.0-alpha (run: rjw prompts --update)
```

## When Up-to-Date

```bash
$ rjw prompts --version --online
rjw-prompt-pack 0.1.0-alpha (sha256-abc123de...)
Last updated: 2025-10-07
You have the latest version
```

## Update Prompt Pack (Placeholder)

```bash
rjw-prompt-pack 0.1.0-alpha (sha256-abc123de...)
Prompt pack update functionality
Update available: 0.1.0-alpha (run: rjw prompts --update)
Not implemented in this version - manual update required
```

## Offline Mode (Default)

```bash
rjw-prompt-pack 0.1.0-alpha (sha256-def456ab...)
rjw-prompt-pack 1.0.0-alpha (sha256-abc123de...)
Last updated: 2025-10-07

# No online check performed unless --online flag used
```

## Inspect Prompt Pack File

rjw-prompt-pack 0.1.0-alpha (sha256-abc123de...)
$ cat prompt-pack.json
{
  "name": "rjw-prompt-pack",
  "version": "1.0.0-alpha",
  "checksum": "sha256-abc123def456",
  "last_updated": "2025-10-07",
  "channels": ["core", "add-ins/game", "lite"],
  "compat": {
    "min_cli": ">=1.0.0"
  "version": "0.1.0-alpha",
}
```

## Verify Compatibility

```bash
# Check if your CLI version meets minimum requirement
$ rjw --help | grep -i version
# Should show version >= 1.0.0
```

## Integration in Scripts

```bash
#!/bin/bash
# Check prompt version in CI/CD

VERSION=$(rjw prompts --version | head -1 | awk '{print $2}')
echo "Using prompt pack version: $VERSION"

if [ "$VERSION" != "1.0.0" ]; then
  echo "Warning: Unexpected prompt pack version"
  exit 1
fi
```

## Automation Example

```bash
# Daily check for updates
#!/bin/bash
# check-prompts.sh

RESULT=$(rjw prompts --version --online 2>&1)

if echo "$RESULT" | grep -q "Update available"; then
  echo "🔔 New prompt pack available!"
  echo "$RESULT"
  # Send notification, create issue, etc.
else
  echo "✔ Prompt pack is up to date"
fi
```

## Version History Tracking

```bash
# Track prompt versions in change log
$ git log --oneline --grep="prompt-pack"
a1b2c3d Update prompt-pack to 1.0.0
d4e5f6g Initial prompt-pack.json

# See what changed
$ git diff HEAD~1 prompt-pack.json
```

## Troubleshooting

### Issue: "prompt-pack.json not found"

**Solution**: Run `rjw init` to create it
```bash
$ rjw init --noninteractive
# Creates prompt-pack.json with defaults
```

### Issue: Version shows 0.0.0

**Solution**: Project not initialized
```bash
$ rjw prompts --version
rjw-prompt-pack 0.0.0 (unknown)
Last updated: unknown

# Fix: Initialize project
$ rjw init
```

## Best Practices

1. **Check version before major changes**
   ```bash
   rjw prompts --version >> DECISION_LOG.md
   ```

2. **Pin versions in CI**
   ```yaml
   - name: Verify prompt version
     run: |
       VERSION=$(rjw prompts --version | awk '{print $2}')
       test "$VERSION" = "1.0.0"
   ```

3. **Document version changes**
   - Update change log when updating prompt pack
   - Link to specific prompts used in decisions
   - Archive old versions for reproducibility

4. **Use offline mode by default**
   - Avoids unexpected network calls
   - Deterministic behavior in CI
   - Only use `--online` when explicitly checking for updates
