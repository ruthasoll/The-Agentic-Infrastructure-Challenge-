# Command: check-tests

Purpose: Ensure required failing tests are present (TDD) for a spec/feature. This stub documents the expected CI behavior: tests should exist and initially fail until implementation.

Example (manual):

```bash
# Example: check for test files under tests/ or specs/[feature]/tests
if ls "$1"/tests/*.py >/dev/null 2>&1; then
  echo "tests found"
  # Optionally run tests in --failfast mode to verify they fail initially
  # pytest --maxfail=1 --exitfirst "$1/tests"
  exit 0
else
  echo "No tests found under $1/tests" >&2
  exit 2
fi
```

Notes: CI gating should verify that tests exist, and optional pipeline stage can run tests expecting failure prior to implementation (configurable).
