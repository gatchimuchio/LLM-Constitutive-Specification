# Layer-0 機能適合フレームワーク

> **現行仕様:** `v4.0-provisional`  
> **日本語正本:** `docs/layer0_v4_spec.ja.md`  
> **横断証拠状態:** `L0-C / OBSERVED_SET_SUPPORTED`  
> **原理状態:** `PRINCIPLE_CANDIDATE / REOPEN_REQUIRED`

このリポジトリは、LLM候補を特定の実装方式へ固定せず、**言語要求を文脈依存に処理し、追跡可能な変換または合成を通じて結果を形成できるか**を監査するための Layer-0 上位契約を提供する。

v4では、v3の「6コンポーネントが現代LLMの普遍的一意最小構成である」という公開主張を現行仕様から撤回した。v3成果物は削除せず履歴として保存する。v4は普遍定理・最終最小構成を主張しない。

2026-08-21の横断突合では、Llama 3、LLM360 K2-V2、OLMo 3、Apertus 1.5、Kimi K3 の公開観測をHDS日本語構文で再監査した。標準Attention、KDA、Dense FFN、MoE、text-only、multimodal、複数の長文脈方式という実装差を跨いでも、現行5責任への写像が崩れなかった。この結果により、**観測した5系統に限定して L0-C「異種architecture family間の機能責任再現」を支持**する。

これは「Attentionが不要」「5責任が普遍的一意最小」「全LLMに証明済み」という意味ではない。

## v4 Functional Core

機械識別子は互換性のため英語を維持するが、正本上の意味は次の日本語で固定する。

1. `LINGUISTIC_ADDRESSABILITY` — **言語アドレス化**
2. `CONTEXT_BOUND_STATE` — **文脈束縛状態**
3. `TRANSFORMATION_OR_COMPOSITION_CORE` — **変換・合成中核**
4. `CONTEXT_DEPENDENT_RESULT_FORMATION` — **文脈依存結果形成**
5. `RESULT_SURFACE` — **結果表面**

重要な規則：

```text
責任数 != 機構数
```

一つの機構が複数責任を担ってよく、複数機構が一つの責任を共同で担ってよい。

今回の横断観測で見えた「履歴保持・参照関係形成・状態変換・統合帰還・候補表出・選択・反復」は、現時点では5責任の下位作用として吸収できる。したがって、それらを機械的に独立責任へ増やさない。

## 三層分離

### A. Functional Core
実行時に観測する責任。合否対象。

### B. Construction / Provenance Profile
`trained / authored / compiled / induced / searched / evolved / retrieved / hybrid / unknown`

作られ方は記録するが、Functional Core のPASS条件そのものにはしない。

### C. Operational Wrapper
`token_emission / text_api / score_surface / structured_output / interactive_chat / batch_transform / embedded_subsystem / unknown`

model core と deployed system を分離する。

## 実装方式を定義で固定しない

v4は neural network、decision tree / forest、probabilistic program、symbolic rules、finite-state / pushdown / graph machine、table-driven transducer、retrieval + composition、search / planning、program synthesis、hybrid を定義だけで排除しない。

同様に、Transformer、標準full-attention、Dense FFN、MoE、KDA、GQA、KV cache、RoPE、YaRN、multimodal、tool use、thinking controlのいずれかを、名称だけでLayer-0の必須構成へ昇格しない。

採否は素材名ではなく、機能責任・system boundary・execution trace・negative controls で決める。

## 適合状態

- `PASS` — 全必須責任が実行証拠で確認された
- `FAIL` — 必須責任またはnegative controlが反証された
- `SUSPEND` — boundary / source / trace / evidence が不足
- `NOT_APPLICABLE` — scope外

## 横断主張の現在地

| 層 | 内容 | 現在状態 |
|---|---|---|
| L0-A | 個別候補の機能適合 | 実行可能 |
| L0-B | 同一・近縁family内での責任再現 | 観測集合で支持 |
| L0-C | 異種architecture family間での責任再現 | **観測5系統で支持** |
| L0-D | 限定scopeでの原理候補 | `PRINCIPLE_CANDIDATE / REOPEN_REQUIRED` |
| L0-E | 未観測familyへの転移 | OPEN |

詳細：`docs/5モデル横断機能責任突合_2026-08-21.md`

## 実行

```bash
make audit
make test
make verify
make test-all
```

`make test-all` は正本manifestを書き換えない。

正本manifest更新は明示操作のみ：

```bash
make update-golden CONFIRM=1
```

## 主要ファイル

- `docs/layer0_v4_spec.ja.md` — v4正本仕様（日本語）
- `docs/5モデル横断機能責任突合_2026-08-21.md` — 今回の横断証拠と主張境界
- `layer0_functional_conformance_v4.py` — candidate-local v4適合評価器
- `tests/test_layer0_v4.py` — positive / negative conformance tests
- `scripts/strict_manifest.py` — tracked inventory / content の厳格検証
- `docs/v3_legacy_status.ja.md` — v3の現行位置づけ

## v3について

v3の6役割、64部分集合列挙、生成artifact、DOI-backed releaseは履歴として保持する。ただし、現在のmainはそれらを**現代LLM全体への普遍的一意最小性の証明**として扱わない。
