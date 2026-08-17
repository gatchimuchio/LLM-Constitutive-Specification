# Repository Setup Notes — Current

The repository is already public and connected to archival/release history. This file no longer describes a future repository-creation workflow.

Current development gate:

```bash
make test-all
```

Golden inventory updates are explicit only:

```bash
make update-golden CONFIRM=1
```

Changes to current claims should be made on a branch and reviewed before merge. The v3 tagged release remains immutable legacy material.
