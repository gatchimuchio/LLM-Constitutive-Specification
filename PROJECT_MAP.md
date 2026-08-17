# Project Map

## Current purpose

Implementation-neutral Layer-0 functional conformance framework for candidate systems, plus archived v3 reproducibility material.

## Current v4 core

| Path | Purpose |
|---|---|
| `README.md` / `README.ja.md` | Current public entry points |
| `layer0_functional_conformance_v4.py` | Candidate-local v4 conformance evaluator |
| `docs/layer0_v4_spec.md` / `.ja.md` | Current specification |
| `tests/test_layer0_v4.py` | Positive/negative conformance tests |
| `scripts/strict_manifest.py` | Strict tracked-inventory/content verifier |
| `REPOSITORY_GIT_BLOB_MANIFEST.txt` | Golden inventory excluding itself |
| `.github/workflows/audit.yml` | CI: `make test-all` |
| `docs/v3_legacy_status.md` / `.ja.md` | v3 scope and legacy classification |

## Legacy v3 material

The following remain for reproducibility but are not the current universal claim surface:

- `llm_minimal_architecture_groups_v3_0.py`
- `appendices/layer_a_obligation_graph_enumeration_v0_5/`
- `artifacts/llm_minimal_architecture_groups_v3_0_*`
- v3-oriented reference/witness documents

## Recomposition demo

`layer0_recomposition_memory_demo_bilingual_bundle/` is retained as an architecture-recomposition demonstration. It is not itself evidence of universal Layer-0 minimality.
