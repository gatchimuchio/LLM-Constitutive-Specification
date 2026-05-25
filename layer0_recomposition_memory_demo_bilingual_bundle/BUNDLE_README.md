# Layer-0 Recomposition Memory Demo / Layer-0 再合成メモリデモ

This bundle contains both English and Japanese documentation.

## Files

- `docs/layer0_recomposition_memory_demo.md` — English report
- `docs/layer0_recomposition_memory_demo.ja.md` — Japanese report
- `demos/layer0_memory_recomposition_demo.py` — deterministic executable demo
- `README_SNIPPET.md` — English README addition
- `README_SNIPPET.ja.md` — Japanese README addition
- `MAKEFILE_SNIPPET.md` — optional Makefile target
- `SMOKE_OUTPUT.txt` — local smoke-test output

## Run

```bash
python3 -S demos/layer0_memory_recomposition_demo.py --outdir artifacts/layer0_memory_demo
```

Expected:

```text
MEMORY_RECOMPOSITION_DEMO: PASS
active_memory_count: 2
superseded_memory_count: 1
discarded_candidate_count: 1
context_budget_ok: true
```
