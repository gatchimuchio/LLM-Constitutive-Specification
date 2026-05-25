#!/usr/bin/env python3
"""
Layer-0 Memory Recomposition Demo

This script demonstrates a non-LLM architecture derived from Layer-0 roles.

It does not call an LLM.
It does not claim to be an LLM.
It uses deterministic stand-ins to show how LLM-style reading, summarization,
context formation, and emission can be recomposed into a memory subsystem.

Run:
    python3 -S demos/layer0_memory_recomposition_demo.py --outdir artifacts/layer0_memory_demo
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple


VERSION = "v0.1"

LAYER0_TO_MEMORY_RECOMPOSITION = [
    {
        "layer0_role": "TOKEN_OR_SYMBOL_SPACE",
        "llm_role": "represents linguistic units",
        "memory_role": "serializable event and memory record space",
    },
    {
        "layer0_role": "CONTEXT_CONDITIONING_STATE",
        "llm_role": "conditions output on prior context",
        "memory_role": "rolling user/project/task context used for memory updates",
    },
    {
        "layer0_role": "LEARNED_PARAMETERIZED_TRANSFORM",
        "llm_role": "maps context to conditional output surface",
        "memory_role": "summarizer/extractor module; deterministic stand-in in this demo",
    },
    {
        "layer0_role": "CONDITIONAL_LINGUISTIC_OUTPUT_SURFACE",
        "llm_role": "candidate linguistic outputs",
        "memory_role": "candidate memory operations: create/update/supersede/discard",
    },
    {
        "layer0_role": "SEQUENCE_MODELING_OBJECTIVE_OR_EQUIVALENT_FITTING_CRITERION",
        "llm_role": "fits the model to language sequences",
        "memory_role": "retention objective: preserve future-relevant state under a context budget",
    },
    {
        "layer0_role": "DECODING_OR_EMISSION_INTERFACE",
        "llm_role": "emits observable tokens/text",
        "memory_role": "emits durable memory writes and compiled context blocks",
    },
]


@dataclass(frozen=True)
class Event:
    event_id: str
    source: str
    text: str


@dataclass
class MemoryCandidate:
    candidate_id: str
    event_id: str
    key: str
    summary: str
    tags: List[str]
    retention: str
    score: int
    raw_event_hash: str
    operation_hint: str


@dataclass
class MemoryRecord:
    memory_id: str
    version: int
    key: str
    summary: str
    tags: List[str]
    status: str
    created_from_event: str
    updated_from_event: str
    raw_event_hashes: List[str]
    supersedes: str | None


def stable_hash(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def tokenize(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9_+-]+|[一-龥ぁ-んァ-ンー]+", text)


def classify_tags(text: str) -> List[str]:
    lower = text.lower()
    tags: List[str] = []

    if any(k in lower for k in ["prefer", "preference", "from now on", "going forward"]):
        tags.append("user_preference")
    if any(k in lower for k in ["project", "repository", "repo", "architecture"]):
        tags.append("project_state")
    if any(k in lower for k in ["must", "never", "always", "required", "boundary"]):
        tags.append("constraint")
    if any(k in lower for k in ["temporary", "transient", "scratch", "do not remember"]):
        tags.append("transient")
    if any(k in lower for k in ["update", "replace", "instead", "supersede"]):
        tags.append("update")

    return tags or ["general"]


def retention_policy(tags: List[str], text: str) -> Tuple[str, int, str]:
    lower = text.lower()

    if "transient" in tags:
        return ("discard", 0, "discard")

    score = 1
    if "user_preference" in tags:
        score += 3
    if "project_state" in tags:
        score += 2
    if "constraint" in tags:
        score += 2
    if "update" in tags:
        score += 1
    if any(k in lower for k in ["from now on", "going forward", "must", "always"]):
        score += 2

    retention = "long_term" if score >= 5 else "session"
    operation = "upsert" if score >= 3 else "create"
    return (retention, score, operation)


def infer_key(tags: List[str], text: str) -> str:
    lower = text.lower()

    if "user_preference" in tags and any(k in lower for k in ["japanese", "日本語"]):
        return "user.preference.language"
    if "project_state" in tags and "memory" in lower:
        return "project.memory_architecture"
    if "project_state" in tags:
        return "project.state"
    if "constraint" in tags:
        return "constraint.general"
    return "general.note." + stable_hash(text, 8)


def summarize(text: str, max_words: int = 22) -> str:
    """
    Deterministic stand-in for an LLM summarizer.

    This intentionally does not claim semantic quality. Its only purpose is to
    make the memory lifecycle reproducible.
    """
    tokens = tokenize(normalize(text))
    summary = " ".join(tokens[:max_words])
    if len(tokens) > max_words:
        summary += " ..."
    return summary


def read_event_into_candidate(event: Event) -> MemoryCandidate:
    text = normalize(event.text)
    tags = classify_tags(text)
    retention, score, operation_hint = retention_policy(tags, text)
    key = infer_key(tags, text)

    return MemoryCandidate(
        candidate_id="cand_" + stable_hash(event.event_id + text, 12),
        event_id=event.event_id,
        key=key,
        summary=summarize(text),
        tags=tags,
        retention=retention,
        score=score,
        raw_event_hash=stable_hash(event.text, 32),
        operation_hint=operation_hint,
    )


def apply_candidate(
    store: Dict[str, MemoryRecord],
    candidate: MemoryCandidate,
    discarded: List[MemoryCandidate],
    operation_log: List[Dict[str, object]],
) -> None:
    if candidate.retention == "discard":
        discarded.append(candidate)
        operation_log.append(
            {
                "operation": "discard",
                "candidate_id": candidate.candidate_id,
                "event_id": candidate.event_id,
                "key": candidate.key,
                "reason": "retention_policy_discard",
            }
        )
        return

    existing = store.get(candidate.key)

    if existing is None:
        memory = MemoryRecord(
            memory_id="mem_" + stable_hash(candidate.key, 12),
            version=1,
            key=candidate.key,
            summary=candidate.summary,
            tags=candidate.tags,
            status="active",
            created_from_event=candidate.event_id,
            updated_from_event=candidate.event_id,
            raw_event_hashes=[candidate.raw_event_hash],
            supersedes=None,
        )
        store[candidate.key] = memory
        operation_log.append(
            {
                "operation": "create",
                "memory_id": memory.memory_id,
                "version": memory.version,
                "event_id": candidate.event_id,
                "key": candidate.key,
            }
        )
        return

    old_id = existing.memory_id + f":v{existing.version}"
    previous_hashes = list(existing.raw_event_hashes)

    existing.version += 1
    existing.summary = candidate.summary
    existing.tags = sorted(set(existing.tags + candidate.tags))
    existing.status = "active"
    existing.updated_from_event = candidate.event_id
    existing.raw_event_hashes = previous_hashes + [candidate.raw_event_hash]
    existing.supersedes = old_id

    operation_log.append(
        {
            "operation": "supersede_and_update",
            "memory_id": existing.memory_id,
            "version": existing.version,
            "event_id": candidate.event_id,
            "key": candidate.key,
            "supersedes": old_id,
        }
    )


def compile_context(store: Dict[str, MemoryRecord], budget_chars: int) -> Dict[str, object]:
    active = [m for m in store.values() if m.status == "active"]
    active.sort(key=lambda m: (m.key, m.version))

    lines: List[str] = []
    used = 0

    for memory in active:
        line = f"- [{memory.key} v{memory.version}] {memory.summary}"
        if used + len(line) + 1 > budget_chars:
            break
        lines.append(line)
        used += len(line) + 1

    return {
        "budget_chars": budget_chars,
        "used_chars": used,
        "context_budget_ok": used <= budget_chars,
        "compiled_context": "\n".join(lines),
        "included_memory_count": len(lines),
    }


def build_demo_events() -> List[Event]:
    return [
        Event(
            event_id="E001",
            source="user",
            text="Going forward, prefer concise Japanese business-style responses for this repository work.",
        ),
        Event(
            event_id="E002",
            source="user",
            text="Project note: the memory architecture should separate raw event provenance, summary generation, retention policy, lifecycle state, and context compilation.",
        ),
        Event(
            event_id="E003",
            source="user",
            text="Temporary scratch note: try a funny name for the demo, but do not remember this.",
        ),
        Event(
            event_id="E004",
            source="user",
            text="Update the previous language preference: Japanese remains preferred, but technical reports in this repository should be written in English.",
        ),
    ]


def run_demo(outdir: Path) -> Dict[str, object]:
    events = build_demo_events()
    candidates = [read_event_into_candidate(event) for event in events]

    store: Dict[str, MemoryRecord] = {}
    discarded: List[MemoryCandidate] = []
    operation_log: List[Dict[str, object]] = []

    for candidate in candidates:
        apply_candidate(store, candidate, discarded, operation_log)

    context = compile_context(store, budget_chars=420)

    active_records = [asdict(m) for m in store.values() if m.status == "active"]
    superseded_count = sum(1 for op in operation_log if op["operation"] == "supersede_and_update")

    invariants = {
        "all_active_memories_have_provenance_hash": all(
            len(m.raw_event_hashes) >= 1 for m in store.values() if m.status == "active"
        ),
        "at_least_one_candidate_discarded": len(discarded) >= 1,
        "at_least_one_memory_superseded": superseded_count >= 1,
        "context_budget_ok": bool(context["context_budget_ok"]),
        "no_discarded_candidate_became_active": all(
            d.key not in store for d in discarded
        ),
    }

    pass_status = all(invariants.values())

    certificate = {
        "demo": "layer0_memory_recomposition_demo",
        "version": VERSION,
        "claim": "Layer-0 functional roles can be recomposed into a deterministic non-LLM memory subsystem.",
        "is_llm": False,
        "uses_remote_llm": False,
        "recomposition_map": LAYER0_TO_MEMORY_RECOMPOSITION,
        "events": [asdict(e) for e in events],
        "candidates": [asdict(c) for c in candidates],
        "active_memory": active_records,
        "discarded_candidates": [asdict(c) for c in discarded],
        "operation_log": operation_log,
        "compiled_context": context,
        "invariants": invariants,
        "status": "PASS" if pass_status else "FAIL",
    }

    outdir.mkdir(parents=True, exist_ok=True)
    cert_path = outdir / "memory_recomposition_certificate.json"
    report_path = outdir / "memory_recomposition_report.md"

    cert_path.write_text(json.dumps(certificate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(render_markdown_report(certificate), encoding="utf-8")

    return certificate


def render_markdown_report(certificate: Dict[str, object]) -> str:
    context = certificate["compiled_context"]
    invariants = certificate["invariants"]

    invariant_lines = "\n".join(
        f"- `{name}`: `{str(value).lower()}`"
        for name, value in invariants.items()
    )

    operations = "\n".join(
        f"- `{op['operation']}`: `{op.get('key', '')}` from `{op.get('event_id', '')}`"
        for op in certificate["operation_log"]
    )

    return f"""# Layer-0 Memory Recomposition Demo Report

Status: `{certificate['status']}`  
Remote LLM used: `{str(certificate['uses_remote_llm']).lower()}`  
Is this system an LLM: `{str(certificate['is_llm']).lower()}`

## Claim

{certificate['claim']}

## Operation log

{operations}

## Compiled context

```text
{context['compiled_context']}
```

## Invariants

{invariant_lines}

## Interpretation

This demo does not prove memory quality. It proves that Layer-0-style roles
can be recomposed into a controlled memory lifecycle: candidate generation,
retention decision, supersession, discard, and context emission.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Layer-0 memory recomposition demo.")
    parser.add_argument("--outdir", default="artifacts/layer0_memory_demo", help="Output directory.")
    args = parser.parse_args()

    certificate = run_demo(Path(args.outdir))

    active_count = len(certificate["active_memory"])
    superseded_count = sum(1 for op in certificate["operation_log"] if op["operation"] == "supersede_and_update")
    discarded_count = len(certificate["discarded_candidates"])
    context_budget_ok = certificate["compiled_context"]["context_budget_ok"]

    print(f"MEMORY_RECOMPOSITION_DEMO: {certificate['status']}")
    print(f"active_memory_count: {active_count}")
    print(f"superseded_memory_count: {superseded_count}")
    print(f"discarded_candidate_count: {discarded_count}")
    print(f"context_budget_ok: {str(context_budget_ok).lower()}")

    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
