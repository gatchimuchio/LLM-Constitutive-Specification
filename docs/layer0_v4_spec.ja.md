# Layer-0 v4 暫定仕様

## 1. 目的

候補システムが、言語要求を文脈依存に処理し、追跡可能な変換または合成を通じて結果を形成できるかを、実装方式から独立して判定する。

現行仕様版: `v4.0-provisional`

主張状態:

```text
L0-A = executable
L0-B = supported in observed families
L0-C = supported in observed five-model set
L0-D = PRINCIPLE_CANDIDATE / REOPEN_REQUIRED
L0-E = OPEN
```

## 2. Functional Core

機械識別子は既存candidate schemaとの互換性のため維持する。

1. `LINGUISTIC_ADDRESSABILITY` — **言語アドレス化**
2. `CONTEXT_BOUND_STATE` — **文脈束縛状態**
3. `TRANSFORMATION_OR_COMPOSITION_CORE` — **変換・合成中核**
4. `CONTEXT_DEPENDENT_RESULT_FORMATION` — **文脈依存結果形成**
5. `RESULT_SURFACE` — **結果表面**

これらは責任境界であり、物理component数を意味しない。

### 2.1 責任の意味

#### 2.1.1 言語アドレス化

外部の言語記号または言語要求を、候補システム内部で参照・処理可能な状態へ接続できること。

tokenizer、token ID、embedding、記号表、構文木、状態番号、検索キー等は実装例であり、名称自体を必須としない。

#### 2.1.2 文脈束縛状態

現在の処理が、要求に関係する既出状態・系列・履歴・条件へ束縛され、その状態差が後続処理へ作用できること。

KV cache、recurrent state、明示メモリ、スタック、グラフ状態等は実装例である。

#### 2.1.3 変換・合成中核

内部状態に対し、参照・関係形成・状態変換・合成・差分統合のいずれかを通じて、入力の単純な固定反射ではない処理を成立させること。

standard attention、KDA、Dense FFN、MoE、symbolic rule、retrieval + composition等は候補機構であり、特定方式へ固定しない。

#### 2.1.4 文脈依存結果形成

現在の文脈束縛状態と変換・合成結果から、候補結果または次状態を形成できること。

logits、decoding、router後の選択、規則選択、探索、反復生成等は実装例である。生成可能集合と最終選択を同一責任へ潰さず、必要なら内部証拠として分別する。

#### 2.1.5 結果表面

形成された結果を、候補システムのsystem boundary外から観測可能な表面へ接続できること。

text、token、structured output、score、embedded subsystem result等を許容する。

### 2.2 横断観測で得た下位作用との関係

2026-08-21の5モデル突合では、次の局所作用が反復して観測された。

```text
外部記号の住所化
履歴・系列状態の保持
参照関係の形成
状態変換
差分・参照結果の統合帰還
候補の表出
選択・反復
```

現時点では、これらは上記5責任へ情報損失なく写像できるため、7個の独立必須責任へ昇格しない。

```text
責任数 != 機構数
下位作用数 != 必須責任数
```

## 3. Construction / Provenance

`trained / authored / compiled / induced / searched / evolved / retrieved / hybrid / unknown`

Construction profileはFunctional Coreの合否条件と分離する。

学習工程と実行工程は同一視しない。training / post-training / compilation / authoring等は候補を形成する経路であり、形成済み候補のruntime責任とは別に記録する。

## 4. Operational Wrapper

`token_emission / text_api / score_surface / structured_output / interactive_chat / batch_transform / embedded_subsystem / unknown`

model core と deployed system を分離する。

multimodal input、tool protocol、thinking control、安全guard等も、Functional Coreへ直接必要とする根拠がない限りOperational Wrapperまたは上位構成として分離する。

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

## 8. 5モデル横断観測による更新

対象:

- Meta Llama 3 8B / 70B
- LLM360 K2-V2 Base / Instruct
- OLMo 3 7B / 32B Base・Instruct・Think
- Apertus 1.5 8B / 70B
- Kimi K3

観測上、次の実装差が存在した。

- standard Transformer / KDA + Gated MLA
- Dense FFN / MoE
- KV cache / recurrent state / context parallel等の異なる履歴利用方式
- text-only / multimodal input
- 複数のlong-context形成方式
- thinking / effort / tool controlの有無

それでも5責任への写像は維持できた。

このため、現行観測集合については **L0-C「異種architecture family間での機能責任再現」** を支持する。

ただし、次はこの観測からは導かない。

```text
standard attention is universally unnecessary = NOT ESTABLISHED
exact five-responsibility minimum             = OPEN
ordinary-term LLM equivalence                 = OPEN
universal theorem                             = NOT CLAIMED
final minimum                                 = NOT CLAIMED
```

Kimi K3もKDAだけではなくGated MLAを周期的に含むため、「Attention一般が不要」という反例には使わない。今回反証できるのは、少なくとも**標準full-attentionを全層で同じ形に置くことが普遍必須ではない**という範囲までである。

詳細は `docs/5モデル横断機能責任突合_2026-08-21.md` を参照する。

## 9. Claim boundary

v4評価器が直接判定するのはcandidate-local conformanceである。

architecture-family recurrence、cross-family recurrence、scoped principle、transferはcandidate-localのPASSから自動昇格させず、別claim layerで管理する。

現時点:

```text
exact minimum                  = OPEN
ordinary-term LLM equivalence = OPEN
universal theorem             = NOT CLAIMED
```

## 10. 再開放条件

少なくとも次の場合は5責任またはclaim layerを再監査する。

1. 5責任の一つを満たさず同等の言語機能を成立させる反例が出た。
2. 現行5責任の二つ以上を、機能差を失わず恒常的に一責任へ統合できた。
3. 現行5責任に写像できない独立必須責任が観測された。
4. 横断証拠のsource lock、版境界、artifact完全性に破損が見つかった。
5. 未観測architecture familyで現在の責任語彙が破綻した。
