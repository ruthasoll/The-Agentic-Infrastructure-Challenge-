# Command: check-spec

Purpose: Validate that a feature/spec directory contains a GitHub Spec Kit `spec.md` and required metadata. This command is intended to be called by CI or by `/speckit` helpers before Phase 0 research.

Example (manual):

```bash
# basic check: verify spec.md exists
if [ -f "$1/spec.md" ]; then
  echo "spec.md found"
  exit 0
else
  echo "MISSING spec.md in $1" >&2
  exit 2
fi
```

Expected outputs: exit 0 if present, exit non-zero otherwise.

Notes: CI should call this command for each `specs/*` folder and fail the build if any spec is missing.
