# Command: check-telemetry

Purpose: Verify that a spec or PR includes telemetry/observability fields required by the constitution (Tenx MCP Sense trace examples, telemetry field list, correlation id usage).

Example (manual):

```bash
# Check for a telemetry snippet file under specs/[feature]/telemetry.md
if [ -f "$1/telemetry.md" ]; then
  echo "telemetry.md present"
  exit 0
else
  echo "Missing telemetry.md in $1" >&2
  exit 2
fi
```

Notes: CI should require telemetry snippets for runtime-affecting changes. The telemetry.md should include example trace ids, correlation-id patterns, and required fields to be emitted at runtime.
