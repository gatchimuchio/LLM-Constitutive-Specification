# Audit Procedure

## Current gate

```bash
make test-all
```

This runs:

1. v4 self-test
2. v4 unittest suite
3. strict repository inventory/content verification

`make test-all` MUST NOT regenerate golden state.

Golden state may be rewritten only by explicit operator action:

```bash
make update-golden CONFIRM=1
```

## Status semantics

Candidate conformance uses `PASS / FAIL / SUSPEND / NOT_APPLICABLE`.
Unknown evidence is `SUSPEND`, never implicit PASS.
