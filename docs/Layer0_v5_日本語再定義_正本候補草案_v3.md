# Layer-0 v5 日本語再定義 — 正本候補草案 v3

## 状態

`DRAFT_V3 / NOT_CANONICAL / REOPENABLE`

本書は、2026-08-25の原点再監査、HDS横断観測、反例監査、Large再監査、model/runtime境界監査、random/null反例を統合した第三草案である。

現行v4正本は変更しない。

---

# 1. Layer-0の原点

Layer-0の問いは、特定技術の部品表ではない。

```text
LLMとは何か
Language Modelとは何か
Largeとは何か
何がmodel本体で、何がruntime / wrapper / applicationか
```

を、機能・境界・作用・状態から最小に定義する。

実装名称を定義へ先取りしない。

---

# 2. 最上位分離

v5では最低限、次を別の対象とする。

```text
A. Language Model Artifact Identity
B. Language Modeling Functional Conformance
C. Generative Capability
D. Large Profile
E. Execution / Operational System
F. Compute Topology
G. Formation / Construction
H. Application / Agent System
```

`LLM`一語へこれらを全部押し込まない。

---

# 3. A — Language Model Artifact Identity

## 3.1 M1 言語状態域契約

モデルの入力・条件・結果の主要経路に、言語へ追跡可能に接続された状態域が存在すること。

言語状態は表面文字列に限定しない。

- token / token列
- masked state
- contextual representation
- hidden/recurrent linguistic state
- grammar/syntax state
- semantic relation state
- HDS座標・関係
- linguistic candidate set

等を許容する。

### 境界規則

- internal全状態の可解釈性を要求しない
- model boundaryのstate contractを要求する
- 言語が単なる出力装飾だけの場合は弱い
- 固定task labelや純算術値は、表面が文字列でも自動的に言語状態とはしない

## 3.2 M2 再利用可能なモデル関係

同一versionとして追跡可能で、複数の言語状態へ再利用される関係仕様が存在すること。

この関係は、

- 言語状態同士
- 言語状態と候補
- 言語構造同士
- 言語候補への評価

等を規定する。

実体は問わない。

- weights
- rules
- table
- graph
- compiled operator
- program
- hybrid relation set

形成方法も問わない。

## 3.3 Artifact Identityの最小定義

> **Language Model Artifactとは、言語状態域契約M1と、その状態域上で再利用されるモデル関係M2を持つモデル物である。**

M1とM2は物理component数を意味しない。

```text
不可約関係 = 言語状態域契約 × モデル関係
```

として扱う。

---

# 4. B — Language Modeling Functional Conformance

M1/M2だけではrandom mappingやhash-like relationも形式上通り得る。

従って、Artifact Identityと「実際にlanguage modelとして機能しているか」を分ける。

## C1 言語差依存

宣言scope内の言語差を変えたとき、model relationの結果が無関係な定数のままではない。

## C2 言語規則性

relationが、宣言scopeの言語関係について反復可能な規則性を保持する。

検証形式は固定しない。

- prediction
- reconstruction
- ranking
- relation consistency
- grammar/structure consistency
- semantic transformation consistency

等を許容する。

## C3 relation再利用

一つの完全入力→完全出力pair専用ではなく、複数状態へ同じmodel relationが適用される。

## C4 nullとの差

必要に応じて、

- constant
- random mapping
- global prior
- identity
- exact instance retrieval

等の適切なnull/controlと区別できること。

統計検定を普遍強制しない。対象に応じた実行trace、counterfactual、構造監査でもよい。

## Conformance状態

```text
PASS_LM_FUNCTION
FAIL_LM_FUNCTION
SUSPEND_LM_FUNCTION
```

を持つ。

---

# 5. C — Generative Capability

GenerativeはLanguage Model Identityとは別属性である。

> 現在状態に対し、新しい言語系列・言語構造・言語候補状態を形成できる能力。

方式は問わない。

- autoregressive
- diffusion
- symbolic generation
- hybrid

を許容する。

`text emission`やCLI/APIはOperational側であり、Generative capabilityそのものと分ける。

---

# 6. D — Large Profile

Largeはruntime作用ではなく程度・適用域である。

最小三軸候補:

## L1 状態域幅

同一model artifactが扱える言語状態の広さ。

下位観測:

- 語彙 / 表記 / 言語
- 系列長
- 構造階層
- 入力形態
- 結果状態の開放性

## L2 関係域幅

同一model relationが扱える関係種別・関係深度の広さ。

下位観測:

- 局所 / 長距離依存
- 構造関係
- 意味関係
- 談話関係
- 関係合成
- 有効計算深度

## L3 再利用域幅

同じmodel relationを別状態・未列挙組合せ・異なる領域へ再利用できる範囲。

下位観測:

- 未列挙組合せ
- domain/topic差
- task形式差
- 文脈差
- 言語差

## Large判定

```text
Large = multidimensional profile
```

とする。

普遍的一点thresholdは現時点で規定しない。

用途上二値が必要ならreference envelopeを明示し、その採用境界を普遍原理へ昇格しない。

---

# 7. E — Execution / Operational System

Model Artifactと実行systemを分ける。

## Layer-0X Execution Contract

```text
X1 現在状態
X2 適用作用 / runtime
X3 結果状態接続
```

```text
Run(ModelArtifact, CurrentState) -> ResultState
```

を成立させる。

### Operational Wrapper

- tokenizer/processor implementation
- decoder/surface
- API/CLI
- scheduler
- cache manager
- inference kernel
- speculative serving

等をここへ置く。

ただしstate adapterがM1契約の意味を変更する場合は、effective model identityとの結合を監査する。

---

# 8. F — Compute Topology

HDS横断観測で得た、

- 系列方向
- 深さ方向
- 幅方向
- 未来方向補助

を保持する。

例:

- global / local / window / recurrent / linear / compressed / sparse
- standard residual / AttnRes / mHC
- dense / routed expert / shared expert
- MTP / draft / speculator

これらをArtifact Coreの普遍必須機構へ昇格しない。

---

# 9. G — Formation / Construction

model artifactの形成方法を記録する。

```text
trained
authored
compiled
induced
searched
evolved
retrieved
hybrid
unknown
```

形成方法をArtifact IdentityのPASS条件にしない。

ただしprovenanceは言語適合の根拠として利用できる。

---

# 10. H — Application / Agent System

- RAG
- tools
- search
- persistent memory
- safety classifier
- fallback
- approval
- agent loop
- multi-agent orchestration

等。

model-only claimへ逆帰属しない。

---

# 11. 旧Layer-0の主要項目を再配置する

## v2/v3系6役割

### TOKEN_OR_SYMBOL_SPACE

→ M1 言語状態域契約

### CONTEXT_CONDITIONING_STATE

→ Execution/Capability/Large profile

Language Model一般ではunigram反例があるためArtifact Core必須にはしない。

### LEARNED_PARAMETERIZED_TRANSFORM

→ M2 モデル関係 + Formation

`learned / parameterized`を必須から除去。

### CONDITIONAL_LINGUISTIC_OUTPUT_SURFACE

→ M1結果契約 + Scoring/Generative capability

`next token distribution`へ固定しない。

### SEQUENCE_MODELING_OBJECTIVE / FITTING

→ Formation / Functional Conformance evidence

Artifact Identityから除去。

### DECODING / EMISSION

→ Operational Wrapper

Artifact Identityから除去。

---

# 12. 旧F1/F2/F3を再配置する

## F1 内容依存情報検索

高度能力・効率として重要。

→ Capability / Large L2/L3

## F2 内部知識保持

世界知識配置の一方式。

→ Knowledge Placement / Formation / Capability

外部R型を許容する。

## F3 十分な直列深度

高度推論能力に重要。

→ Capability / Large L2 / Compute Profile

Artifact Identityの論理必須から除去。

---

# 13. 反例適用

## unigram

Artifact Identity: PASS候補
LM Function: PASS候補
Generative/Scoring: Scoring可能
Large: L2/L3狭い

## n-gram

Artifact Identity: PASS候補
LM Function: PASS候補
Large: finite context/orderとしてprofile化

## BERT / encoder-only

Artifact Identity: PASS候補
LM Function: contextual representation / MLM relationで評価
Generative: 別判定

## parser / grammar

Artifact Identity: PASS候補
LM Function: grammar relation再利用ならPASS候補
Large: relation域が狭い可能性

## sentiment classifier

encoderとtask headを分離する。

classifier headの固定label関係だけをLM identityとしない。

## calculator

主要relationがarithmetical state上にある。

Language Model Artifactではない。

## exact retrieval

Artifact structureだけならrelation artifactに見える場合がある。

LM Function C3/C4とLarge L2/L3で縮退を検出する。

storage方式の名称だけで排除しない。

## diffusion LM

Artifact Identity/Functionとも候補。
autoregressive不要。

---

# 14. MINIDORAへの帰還 — 現時点の観測のみ

まだ実装変更しない。

## M1 言語状態域契約候補

- HDS-IR
- HDS座標 / 関係
- semantic fact
- query/candidate state

## M2 model relation候補

- 言語基底
- capability kernelの固定relation
- J/Gateの固定判断relation
- canonical model knowledgeのうちmodel identityへ属する部分
- model versionを構成するcode/rule/compiled relation

## Run Stateへ分離する候補

- 入力ごとのHDS-IR
- P / 手順
- 外部R Data
- 現在主体状態
- turn-specific candidate

## HDS Compilerの暫定位置

外部自然言語をM1のnative state contractへ接続する **Language State Adapter / Compiler** として再監査する。

Compilerの豊富さとModel Relationの能力を同一視しない。

特に、

```text
完全HDS-IR
→ target-native compute state
```

というlowering契約が必要になる可能性が高い。

---

# 15. 現時点の最小図

```text
                 ┌─────────────────────┐
                 │ Language Model      │
                 │ Artifact Identity   │
                 │                     │
External Lang ──>│ M1 State Contract   │
                 │ M2 Model Relation   │
                 └─────────┬───────────┘
                           │
                    Layer-0X Runtime
                           │
                           ▼
                    Result State

別軸:
  LM Functional Conformance
  Generative Capability
  Large Profile L1/L2/L3
  Compute Topology
  Formation
  Operational Wrapper
  Application/Agent
```

---

# 16. 現在判断

## 強く支持

- Artifact Identity / Functional Conformance / Largeの三分離
- Model / Inference / Harnessの境界分離
- M1+M2をArtifact最小核候補とする
- internal全状態の言語可解釈性を要求しない
- Largeを状態域・関係域・再利用域の3軸へ圧縮
- GenerativeをLM identityと分離
- decoder/emissionをOperationalへ送る
- learned/neural/autoregressiveをCore必須から外す
- F1/F2/F3をCapability/Profileへ再配置

## OPEN

- M1+M2を一つのrelation contractとして表記上統合するか
- Large reference envelopeの実務定義
- exact retrievalの最小LM適合境界
- representational LMへ`Large Language Model`名称を適用する実務境界
- multimodal system内のLM artifact boundary
- MINIDORAのM2正本に何を含めるか

## 禁止

OPENを閉じる前に現行v4正本、MINIDORA、HDS Compilerの実装を変更しない。
