# Layer-0 v4 暫定仕様

## 1. 目的

候補システムが、言語要求を文脈依存に処理し、追跡可能な変換または合成を通じて結果を形成できるかを、実装方式から独立して判定する。

Status: `PRINCIPLE_CANDIDATE / REOPEN_REQUIRED`

## 2. Functional Core

- `LINGUISTIC_ADDRESSABILITY`
- `CONTEXT_BOUND_STATE`
- `TRANSFORMATION_OR_COMPOSITION_CORE`
- `CONTEXT_DEPENDENT_RESULT_FORMATION`
- `RESULT_SURFACE`

これらは責任境界であり、物理component数を意味しない。

## 3. Construction / Provenance

`trained / authored / compiled / induced / searched / evolved / retrieved / hybrid / unknown`

Construction profileはFunctional Coreの合否条件と分離する。

## 4. Operational Wrapper

`token_emission / text_api / score_surface / structured_output / interactive_chat / batch_transform / embedded_subsystem / unknown`

## 5. Candidate submission schema

候補は少なくとも次を持つ。

```text
candidate_id
candidate_version
system_boundary
functional_evidence
mechanisms
construction_profile
operational_profile
source_material_digest
execution_trace
negative_controls
unknowns
scope
reopen_conditions
```

## 6. 判定

- `PASS`: 全必須責任 + 全必須negative controlが確認済み
- `FAIL`: 必須責任またはnegative controlが反証済み
- `SUSPEND`: 証拠不足・unknown・boundary不明
- `NOT_APPLICABLE`: scope外

## 7. 必須negative controls

1. context除去/固定
2. transformation bypass/canned response
3. source material破損
4. result surface遮断
5. unknown input fallback
6. contradictory context resolution
7. exact retrieval と composition の区別
8. merged-role implementation の許容確認

## 8. Claim boundary

v4が直接判定するのはcandidate-local conformanceである。architecture family recurrence、cross-family recurrence、scoped principle、transferは別claim layerで扱う。

現時点で次は未確定。

```text
exact minimum                  = OPEN
ordinary-term LLM equivalence = OPEN
universal theorem             = NOT CLAIMED
```
