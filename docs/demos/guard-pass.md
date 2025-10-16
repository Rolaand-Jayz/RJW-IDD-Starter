# Demo: RJW Guard (Pass Case)

## Scenario
Validating a safe agent output that follows all policies.

## Input File: `examples/ok.json`
```json
{
  "agent_id": "github-copilot",
  "timestamp": "2025-10-07T10:00:00Z",
  "version": "0.1.0-alpha",
  "actions": [
    {
      "type": "read_file",
      "path": "./README.md",
      "signed": true
    },
    {
      "type": "write_file",
      "path": "./sandbox/output.txt",
      "content": "Hello World",
      "signed": true
    }
  ],
  "tools_used": ["read_file", "write_file"]
}
```

## Command
```bash
$ rjw guard examples/ok.json
```

## Output
```
✔ Validation passed (ruleset=default, errors=0, warnings=0)
```

## Exit Code
```
$ echo $?
0
```

## JSON Output (with --format json)
```bash
$ rjw guard examples/ok.json --format json
```

```json
{
  "input_source": "examples/ok.json",
  "passed": true,
  "violations": [],
  "summary": {
    "errors": 0,
    "warnings": 0,
    "ruleset": "default",
    "duration_ms": 12
  }
}
```

## Analysis
- **All actions are signed**: File operations include `signed: true`
- **Paths are sandboxed**: Write goes to `./sandbox/` directory
- **Tools are allowed**: Only `read_file` and `write_file` used
- **No forbidden capabilities**: No dangerous code patterns detected
- **No network calls**: No unauthorized network operations

## Verdict
✅ Safe to proceed with this agent output.
