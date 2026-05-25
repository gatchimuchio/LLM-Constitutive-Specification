# Layer-0 Recomposition Demo: Memory System from LLM Functional Roles

> Status: demonstration artifact  
> Scope: non-LLM derived architecture  
> Purpose: show how Layer-0 functional roles can be recomposed into a deterministic memory subsystem.

---

## 1. Why this demo exists

The Layer-0 theorem defines the minimum functional roles required for a contemporary Large Language Model.  
That result has a second research implication:

> Once the LLM functional core is decomposed into stable roles, those roles can be recomposed into adjacent non-LLM systems.

This demo shows one such recomposition: a memory subsystem.

The target system is **not** an LLM.  
It is a deterministic architecture that reuses the operational pattern of LLM reading, summarization, context formation, and emission to construct:

- memory candidate generation,
- memory update,
- memory supersession,
- memory discard,
- context compilation.

The point is not model performance.  
The point is architectural transfer.

---

## 2. Recomposition map

| Layer-0 role | LLM role | Memory-system recomposition |
| --- | --- | --- |
| `TOKEN_OR_SYMBOL_SPACE` | Represents language units | Defines serializable event and memory records |
| `CONTEXT_CONDITIONING_STATE` | Conditions output on prior context | Maintains rolling task/user/project context |
| `LEARNED_PARAMETERIZED_TRANSFORM` | Learned transform from context to output surface | In deployment: an LLM summarizer/extractor; in this demo: deterministic stand-in |
| `CONDITIONAL_LINGUISTIC_OUTPUT_SURFACE` | Alternative next-token/text outputs | Candidate memory operations: create/update/supersede/discard |
| `SEQUENCE_MODELING_OBJECTIVE_OR_EQUIVALENT_FITTING_CRITERION` | Fits sequences during training | Replaced by a memory-retention objective: preserve future-relevant state under a context budget |
| `DECODING_OR_EMISSION_INTERFACE` | Emits observable text/tokens | Emits durable memory writes and compiled context blocks |

This is a deliberate boundary shift.

The original Layer-0 roles define when a system qualifies as an LLM.  
This recomposition shows what can be built when those roles are treated as reusable architectural primitives rather than as a monolithic model.

---

## 3. What the demo proves

The demo proves only the following limited claim:

> A minimal, deterministic memory subsystem can be constructed by recomposing Layer-0-style reading, summarization, context-conditioning, and emission roles into a non-LLM architecture.

It does **not** prove:

- that the deterministic heuristic is a good summarizer,
- that this is itself an LLM,
- that all agent memory systems must use this design,
- that semantic memory quality can be measured without task-specific evaluation.

The proof target is structural, not semantic.

---

## 4. Demonstrated lifecycle

The executable demo processes a small event stream:

1. An initial durable user preference is observed.
2. A project decision is observed.
3. A transient note is observed and discarded.
4. A later event updates the durable preference.
5. The older memory is marked as superseded.
6. A compiled context is generated from active memories.
7. A JSON certificate records the lifecycle and invariant checks.

Expected lifecycle states:

```text
candidate -> active -> superseded
candidate -> discarded
active -> context block
```

This is the key architectural point:

> memory is not a blob of chat history; it is a controlled state machine over summarized, attributable, versioned records.

---

## 5. Why this matters for agents

Most simple agent memory implementations collapse into one of three weak forms:

1. append-only chat log,
2. vector-search retrieval store,
3. unstructured model-written notes.

Those are useful but incomplete.

A recomposed Layer-0 memory architecture separates:

- raw event provenance,
- summary generation,
- retention policy,
- lifecycle state,
- update/supersession,
- context compilation,
- audit output.

That separation makes memory:

- model-replaceable,
- inspectable,
- revocable,
- context-budget aware,
- safer against stale or transient information,
- usable across long-running sessions.

---

## 6. Determinism policy

The repository's core artifacts are executable and reproducible.  
For that reason, this demo does not call any remote LLM.

The `LEARNED_PARAMETERIZED_TRANSFORM` role is represented by a deterministic stand-in so that the lifecycle can be audited without network access, API keys, nondeterministic sampling, or vendor-specific behavior.

In a deployed system, that deterministic stand-in can be replaced by:

- a frontier LLM,
- a local LLM,
- a small summarization model,
- a hybrid rules + model extractor.

The surrounding memory-control structure remains the same.

---

## 7. Run

```bash
python3 -S demos/layer0_memory_recomposition_demo.py --outdir artifacts/layer0_memory_demo
```

Expected outputs:

```text
artifacts/layer0_memory_demo/memory_recomposition_certificate.json
artifacts/layer0_memory_demo/memory_recomposition_report.md
```

Expected terminal result:

```text
MEMORY_RECOMPOSITION_DEMO: PASS
active_memory_count: 2
superseded_memory_count: 1
discarded_candidate_count: 1
context_budget_ok: true
```

---

## 8. Research implication

The Layer-0 theorem is not only a boundary theorem for LLM status.  
It also opens a recomposition space.

Once a model class is decomposed into functional roles, the roles can be:

- removed,
- replaced,
- externalized,
- constrained,
- made deterministic,
- routed through a policy layer,
- converted into state-machine operations.

This turns Layer-0 from a classification result into a basis for architectural exploration.
