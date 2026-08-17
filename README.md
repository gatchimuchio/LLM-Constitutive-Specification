# Layer-0 Functional Conformance Framework

> **Current:** `v4.0-provisional`  
> **Legacy:** the v3.0 six-role theorem package is retained for archival reproducibility only.  
> **Claim status:** `PRINCIPLE_CANDIDATE / REOPEN_REQUIRED`

This repository provides an implementation-neutral Layer-0 contract for auditing whether a candidate can process linguistic requests under context and form results through traceable transformation or composition.

v4 withdraws the current-repository claim that the v3 six components are a universal and unique minimum for every contemporary LLM. v3 artifacts remain available as legacy material; v4 does not claim a universal theorem or a final minimum.

## v4 Functional Core

The current provisional responsibility vocabulary is:

1. `LINGUISTIC_ADDRESSABILITY`
2. `CONTEXT_BOUND_STATE`
3. `TRANSFORMATION_OR_COMPOSITION_CORE`
4. `CONTEXT_DEPENDENT_RESULT_FORMATION`
5. `RESULT_SURFACE`

Core rule:

```text
responsibility count != mechanism count
```

One mechanism may satisfy multiple responsibilities and multiple mechanisms may jointly satisfy one responsibility.

## Three-layer separation

### A. Functional Core
Runtime-observable responsibilities. This is the conformance target.

### B. Construction / Provenance Profile
`trained / authored / compiled / induced / searched / evolved / retrieved / hybrid / unknown`

Construction method is recorded but is not itself a functional PASS requirement.

### C. Operational Wrapper
`token_emission / text_api / score_surface / structured_output / interactive_chat / batch_transform / embedded_subsystem / unknown`

This separates model-core behavior from deployed-system interfaces.

## Non-neural candidates

v4 does not reject a candidate merely because it is symbolic, programmatic, table-driven, retrieval-plus-composition, search-based, or otherwise non-neural. Acceptance depends on functional evidence, system boundary, execution trace, and negative controls.

## Conformance status

- `PASS` — all required responsibilities are established by execution evidence
- `FAIL` — a required responsibility or negative control is falsified
- `SUSPEND` — boundary/source/trace/evidence is insufficient
- `NOT_APPLICABLE` — outside the declared scope

## Quick start

```bash
make audit
make test
make verify
make test-all
```

`make test-all` never updates the golden manifest.

Explicit golden update only:

```bash
make update-golden CONFIRM=1
```

## Primary files

- `layer0_functional_conformance_v4.py`
- `docs/layer0_v4_spec.md`
- `scripts/strict_manifest.py`
- `tests/test_layer0_v4.py`
- `docs/v3_legacy_status.md`

## Claim ladder

```text
L0-A  candidate-local conformance
L0-B  architecture-family recurrence
L0-C  cross-family mechanism candidate
L0-D  scoped provisional principle
L0-E  transfer candidate
```

`UNIVERSAL_PRINCIPLE` and `FINAL_MINIMUM` are not current status labels.
