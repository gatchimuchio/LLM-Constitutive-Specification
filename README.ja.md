# Layer-0 Functional Conformance Framework

> **Current:** `v4.0-provisional`  
> **Legacy:** v3.0 six-role theorem package is retained for archival reproducibility only.  
> **Claim status:** `PRINCIPLE_CANDIDATE / REOPEN_REQUIRED`

このリポジトリは、LLM候補を特定の実装方式へ固定せず、**言語要求を文脈依存に処理し、追跡可能な変換・合成を通じて結果を形成できるか**を監査するための Layer-0 上位契約を提供する。

v4では、v3の「6コンポーネントが現代LLMの普遍的一意最小構成である」という公開主張を現行仕様から撤回した。v3成果物は削除せず legacy として保存する。v4は普遍定理・最終最小構成を主張しない。

## v4 Functional Core

現在の暫定責任語彙は5つ。

1. `LINGUISTIC_ADDRESSABILITY`
2. `CONTEXT_BOUND_STATE`
3. `TRANSFORMATION_OR_COMPOSITION_CORE`
4. `CONTEXT_DEPENDENT_RESULT_FORMATION`
5. `RESULT_SURFACE`

重要な規則：

```text
responsibility count != mechanism count
```

一つの機構が複数責任を担ってよく、複数機構が一つの責任を担ってよい。

## 三層分離

### A. Functional Core
実行時に観測する責任。合否対象。

### B. Construction / Provenance Profile
`trained / authored / compiled / induced / searched / evolved / retrieved / hybrid / unknown`

作られ方は記録するが、Functional Core のPASS条件そのものにはしない。

### C. Operational Wrapper
`token_emission / text_api / score_surface / structured_output / interactive_chat / batch_transform / embedded_subsystem / unknown`

model core と deployed system を分離する。

## 非ニューラル方式

v4は neural network、decision tree / forest、probabilistic program、symbolic rules、finite-state / pushdown / graph machine、table-driven transducer、retrieval + composition、search / planning、program synthesis、hybrid を定義だけで排除しない。

採否は素材ではなく、機能責任・system boundary・execution trace・negative controls で決める。

## Conformance status

- `PASS` — 全必須責任が実行証拠で確認された
- `FAIL` — 必須責任またはnegative controlが反証された
- `SUSPEND` — boundary / source / trace / evidence が不足
- `NOT_APPLICABLE` — scope外

## Quick start

```bash
make audit
make test
make verify
make test-all
```

`make test-all` は正本manifestを書き換えない。

正本更新は明示操作のみ：

```bash
make update-golden CONFIRM=1
```

## Primary files

- `layer0_functional_conformance_v4.py` — v4 candidate-local conformance evaluator
- `docs/layer0_v4_spec.ja.md` — v4正本仕様（日本語）
- `docs/layer0_v4_spec.md` — v4 specification (English)
- `scripts/strict_manifest.py` — strict inventory/content verifier
- `tests/test_layer0_v4.py` — positive/negative conformance tests
- `docs/v3_legacy_status.ja.md` — v3の現行位置づけ

## v3について

v3の6役割、64部分集合列挙、生成artifact、DOI-backed releaseは履歴として保持する。ただし、現在のmainはそれらを**現代LLM全体への普遍的一意最小性の証明**として扱わない。

詳細：`docs/v3_legacy_status.ja.md`

## Claim ladder

```text
L0-A  candidate-local conformance
L0-B  architecture-family recurrence
L0-C  cross-family mechanism candidate
L0-D  scoped provisional principle
L0-E  transfer candidate
```

`UNIVERSAL_PRINCIPLE` と `FINAL_MINIMUM` は現行statusとして設けない。
