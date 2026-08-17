#!/usr/bin/env python3
"""Layer-0 Functional Conformance Framework v4.0-provisional.

This module evaluates candidate-local functional conformance. It does not claim
a universal or unique minimum for all systems called LLMs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping

VERSION = "v4.0-provisional"

REQUIRED_RESPONSIBILITIES = (
    "LINGUISTIC_ADDRESSABILITY",
    "CONTEXT_BOUND_STATE",
    "TRANSFORMATION_OR_COMPOSITION_CORE",
    "CONTEXT_DEPENDENT_RESULT_FORMATION",
    "RESULT_SURFACE",
)

REQUIRED_NEGATIVE_CONTROLS = (
    "context_removed_or_fixed",
    "transform_bypassed_to_canned_response",
    "source_material_corrupted",
    "result_surface_blocked",
    "unknown_input_fallback",
    "contradictory_context_resolution",
    "exact_retrieval_vs_composition",
    "merged_role_implementation",
)

ALLOWED_CONSTRUCTION_PROFILES = {
    "trained", "authored", "compiled", "induced", "searched", "evolved",
    "retrieved", "hybrid", "unknown",
}

ALLOWED_OPERATIONAL_PROFILES = {
    "token_emission", "text_api", "score_surface", "structured_output",
    "interactive_chat", "batch_transform", "embedded_subsystem", "unknown",
}

HEX64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class Finding:
    code: str
    status: str
    detail: str


def _nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _status(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    upper = value.upper()
    return upper if upper in {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE"} else None


def _profiles(value: Any, allowed: set[str]) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(x, str) and x in allowed for x in value)


def _mechanism_coverage(candidate: Mapping[str, Any]) -> tuple[set[str], list[str]]:
    covered: set[str] = set()
    errors: list[str] = []
    mechanisms = candidate.get("mechanisms")
    if not isinstance(mechanisms, list) or not mechanisms:
        return covered, ["mechanisms must be a non-empty list"]
    for i, mechanism in enumerate(mechanisms):
        if not isinstance(mechanism, dict):
            errors.append(f"mechanisms[{i}] must be an object")
            continue
        if not _nonempty_str(mechanism.get("mechanism_id")):
            errors.append(f"mechanisms[{i}].mechanism_id is required")
        responsibilities = mechanism.get("responsibilities")
        if not isinstance(responsibilities, list) or not responsibilities:
            errors.append(f"mechanisms[{i}].responsibilities must be a non-empty list")
            continue
        unknown = [x for x in responsibilities if x not in REQUIRED_RESPONSIBILITIES]
        if unknown:
            errors.append(f"mechanisms[{i}] has unknown responsibilities: {unknown}")
        covered.update(x for x in responsibilities if x in REQUIRED_RESPONSIBILITIES)
    return covered, errors


def evaluate_candidate(candidate: Mapping[str, Any]) -> Dict[str, Any]:
    findings: list[Finding] = []

    if not isinstance(candidate, Mapping):
        return {"framework_version": VERSION, "status": "FAIL", "findings": [
            {"code": "CANDIDATE_TYPE", "status": "FAIL", "detail": "candidate must be an object"}
        ]}

    if candidate.get("scope") == "NOT_APPLICABLE":
        return {"framework_version": VERSION, "status": "NOT_APPLICABLE", "findings": [], "claim_scope": "candidate-local"}

    for key in ("candidate_id", "candidate_version", "system_boundary"):
        if not _nonempty_str(candidate.get(key)):
            findings.append(Finding(f"MISSING_{key.upper()}", "SUSPEND", f"{key} is required"))

    digest = candidate.get("source_material_digest")
    if not isinstance(digest, str) or not HEX64.fullmatch(digest):
        findings.append(Finding("SOURCE_DIGEST", "SUSPEND", "source_material_digest must be lowercase SHA-256 hex"))

    if not _profiles(candidate.get("construction_profile"), ALLOWED_CONSTRUCTION_PROFILES):
        findings.append(Finding("CONSTRUCTION_PROFILE", "SUSPEND", "construction_profile is missing or invalid"))
    if not _profiles(candidate.get("operational_profile"), ALLOWED_OPERATIONAL_PROFILES):
        findings.append(Finding("OPERATIONAL_PROFILE", "SUSPEND", "operational_profile is missing or invalid"))

    evidence = candidate.get("functional_evidence")
    if not isinstance(evidence, dict):
        findings.append(Finding("FUNCTIONAL_EVIDENCE", "SUSPEND", "functional_evidence must be an object"))
        evidence = {}

    for responsibility in REQUIRED_RESPONSIBILITIES:
        item = evidence.get(responsibility)
        if not isinstance(item, dict):
            findings.append(Finding(f"RESP_{responsibility}", "SUSPEND", "responsibility evidence is missing"))
            continue
        status = _status(item.get("status"))
        refs = item.get("evidence")
        if status == "FAIL":
            findings.append(Finding(f"RESP_{responsibility}", "FAIL", "candidate failed required responsibility"))
        elif status in {None, "UNKNOWN", "NOT_APPLICABLE"}:
            findings.append(Finding(f"RESP_{responsibility}", "SUSPEND", "required responsibility is not established"))
        elif not isinstance(refs, list) or not refs or not all(_nonempty_str(x) for x in refs):
            findings.append(Finding(f"RESP_{responsibility}_TRACE", "SUSPEND", "PASS requires non-empty evidence references"))

    covered, mechanism_errors = _mechanism_coverage(candidate)
    for err in mechanism_errors:
        findings.append(Finding("MECHANISM_MAP", "SUSPEND", err))
    missing_coverage = set(REQUIRED_RESPONSIBILITIES) - covered
    if missing_coverage:
        findings.append(Finding("MECHANISM_COVERAGE", "SUSPEND", f"responsibilities not mapped to mechanisms: {sorted(missing_coverage)}"))

    trace = candidate.get("execution_trace")
    if not isinstance(trace, list) or not trace or not all(isinstance(x, dict) and _nonempty_str(x.get("event")) for x in trace):
        findings.append(Finding("EXECUTION_TRACE", "SUSPEND", "execution_trace must contain observable events"))

    controls = candidate.get("negative_controls")
    if not isinstance(controls, dict):
        findings.append(Finding("NEGATIVE_CONTROLS", "SUSPEND", "negative_controls must be an object"))
        controls = {}
    for control in REQUIRED_NEGATIVE_CONTROLS:
        status = _status(controls.get(control))
        if status == "FAIL":
            findings.append(Finding(f"NEG_{control}", "FAIL", "required negative control failed"))
        elif status != "PASS":
            findings.append(Finding(f"NEG_{control}", "SUSPEND", "required negative control is unknown or missing"))

    unknowns = candidate.get("unknowns")
    if unknowns is not None and (not isinstance(unknowns, list) or not all(_nonempty_str(x) for x in unknowns)):
        findings.append(Finding("UNKNOWNS_FORMAT", "SUSPEND", "unknowns must be a list of non-empty strings"))
    reopen = candidate.get("reopen_conditions")
    if reopen is not None and (not isinstance(reopen, list) or not all(_nonempty_str(x) for x in reopen)):
        findings.append(Finding("REOPEN_FORMAT", "SUSPEND", "reopen_conditions must be a list of non-empty strings"))

    states = {f.status for f in findings}
    if "FAIL" in states:
        overall = "FAIL"
    elif "SUSPEND" in states:
        overall = "SUSPEND"
    else:
        overall = "PASS"

    return {
        "framework_version": VERSION,
        "claim_scope": "candidate-local functional conformance",
        "status": overall,
        "required_responsibilities": list(REQUIRED_RESPONSIBILITIES),
        "responsibility_count_is_not_mechanism_count": True,
        "construction_profile_is_non_normative_for_functional_pass": True,
        "findings": [f.__dict__ for f in findings],
    }


def reference_candidate() -> Dict[str, Any]:
    source = b"symbolic-reference-program-v1"
    responsibilities = list(REQUIRED_RESPONSIBILITIES)
    return {
        "candidate_id": "symbolic-reference-v1",
        "candidate_version": "1",
        "system_boundary": "request -> symbolic state machine -> structured/text result",
        "scope": "candidate-local",
        "construction_profile": ["authored", "compiled"],
        "operational_profile": ["structured_output", "text_api"],
        "source_material_digest": hashlib.sha256(source).hexdigest(),
        "mechanisms": [
            {"mechanism_id": "symbolic-core", "responsibilities": responsibilities[:4]},
            {"mechanism_id": "result-adapter", "responsibilities": ["RESULT_SURFACE"]},
        ],
        "functional_evidence": {r: {"status": "PASS", "evidence": [f"trace:{r.lower()}"]} for r in responsibilities},
        "execution_trace": [
            {"event": "input_addressed"},
            {"event": "context_bound"},
            {"event": "rules_composed"},
            {"event": "result_formed"},
            {"event": "result_emitted"},
        ],
        "negative_controls": {k: "PASS" for k in REQUIRED_NEGATIVE_CONTROLS},
        "unknowns": [],
        "reopen_conditions": ["new counterexample invalidates one responsibility"],
    }


def self_test() -> Dict[str, Any]:
    base = reference_candidate()
    cases = [("reference_symbolic", "PASS", base)]

    missing_context = json.loads(json.dumps(base))
    missing_context["functional_evidence"]["CONTEXT_BOUND_STATE"]["status"] = "FAIL"
    cases.append(("required_responsibility_fail", "FAIL", missing_context))

    unknown_trace = json.loads(json.dumps(base))
    unknown_trace["execution_trace"] = []
    cases.append(("missing_trace", "SUSPEND", unknown_trace))

    merged = json.loads(json.dumps(base))
    merged["mechanisms"] = [{"mechanism_id": "single-core", "responsibilities": list(REQUIRED_RESPONSIBILITIES)}]
    cases.append(("merged_roles_allowed", "PASS", merged))

    neural = json.loads(json.dumps(base))
    neural["construction_profile"] = ["trained"]
    neural["candidate_id"] = "neural-reference"
    cases.append(("construction_method_neutral", "PASS", neural))

    failed_control = json.loads(json.dumps(base))
    failed_control["negative_controls"]["exact_retrieval_vs_composition"] = "FAIL"
    cases.append(("negative_control_fail", "FAIL", failed_control))

    unknown_control = json.loads(json.dumps(base))
    unknown_control["negative_controls"]["unknown_input_fallback"] = "UNKNOWN"
    cases.append(("negative_control_unknown", "SUSPEND", unknown_control))

    results = []
    ok = True
    for name, expected, candidate in cases:
        actual = evaluate_candidate(candidate)["status"]
        passed = actual == expected
        ok = ok and passed
        results.append({"case": name, "expected": expected, "actual": actual, "pass": passed})
    return {"version": VERSION, "status": "PASS" if ok else "FAIL", "cases": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--candidate", type=Path)
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        result = self_test()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "PASS" else 1

    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    result = evaluate_candidate(candidate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return {"PASS": 0, "FAIL": 1, "SUSPEND": 2, "NOT_APPLICABLE": 3}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
