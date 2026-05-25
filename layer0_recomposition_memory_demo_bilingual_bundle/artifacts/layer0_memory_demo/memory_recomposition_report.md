# Layer-0 Memory Recomposition Demo Report

Status: `PASS`  
Remote LLM used: `false`  
Is this system an LLM: `false`

## Claim

Layer-0 functional roles can be recomposed into a deterministic non-LLM memory subsystem.

## Operation log

- `create`: `user.preference.language` from `E001`
- `create`: `project.memory_architecture` from `E002`
- `discard`: `general.note.b3ddb947` from `E003`
- `supersede_and_update`: `user.preference.language` from `E004`

## Compiled context

```text
- [project.memory_architecture v1] Project note the memory architecture should separate raw event provenance summary generation retention policy lifecycle state and context compilation
- [user.preference.language v2] Update the previous language preference Japanese remains preferred but technical reports in this repository should be written in English
```

## Invariants

- `all_active_memories_have_provenance_hash`: `true`
- `at_least_one_candidate_discarded`: `true`
- `at_least_one_memory_superseded`: `true`
- `context_budget_ok`: `true`
- `no_discarded_candidate_became_active`: `true`

## Interpretation

This demo does not prove memory quality. It proves that Layer-0-style roles
can be recomposed into a controlled memory lifecycle: candidate generation,
retention decision, supersession, discard, and context emission.
