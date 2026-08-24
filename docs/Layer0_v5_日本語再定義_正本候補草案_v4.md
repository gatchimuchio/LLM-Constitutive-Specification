# Layer-0 v5 日本語再定義 — 正本候補草案 v4

## 状態

`DRAFT_V4 / NOT_CANONICAL / REOPENABLE`

本書は、2026-08-25に実施した原点再監査、HDS横断観測、極限反例監査、model/runtime分離、Language/Large/Generative分離、対象/model誤投影監査を統合した第四草案である。

現行v4正本は変更しない。

---

# 1. Layer-0の原点

Layer-0が答える問いは、

```text
LLMとは何か
何をmodelしているのか
model本体はどこか
何が実行時作用か
Largeとは何か
Generativeとは何か
```

である。

実装名称、英語圏の現代用語慣習、既存architecture分類から始めない。

---

# 2. 最上位原則 — 対象とモデルを同一視しない

言語そのもの、または言語に観測される関係と、model artifact内部の関係は同一ではない。

```text
言語対象 T
!=
モデル射影 M
```

modelは対象Tを有限に表現したProjectionであり、損失・偏り・未観測・近似を持ち得る。

従ってLayer-0は、対象/model/観測適合を分ける。

---

# 3. Language Modelの三面契約

## 3.1 T — 言語対象契約

modelが何についてのmodelかを宣言する。

最低限:

```text
language_scope
target_state_domain
target_relations
boundary
exclusions
```

を持つ。

### language_scope

自然言語だけへ固定しない。

- natural language
- code
- artificial/formal language

等を含み得る。

内部token IDやvector自体をlanguageと呼ばず、外部language scopeとのmappingを保持する。

### target_relations

言語対象域で何のrelationをmodelするか。

例:

- sequence relation
- conditional relation
- structural relation
- grammatical relation
- semantic relation
- reconstruction relation
- linguistic candidate relation

固定enumへ閉じない。

`world_knowledge_relation`、`task_label_relation`、`arithmetic_relation`等を言語表面で包んだだけでは、language target relationと自動同一視しない。

---

## 3.2 M — 有限モデル射影

Tをmodel artifactとして表す有限Projection。

実体は問わない。

- neural weights
- conditional table
- rules / grammar
- graph
- compiled operator
- program
- symbolic relation set
- hybrid

形成方法も問わない。

```text
trained
authored
compiled
induced
searched
evolved
retrieved
hybrid
```

を許容する。

Mはversion/provenanceを持ち、対象Tそのものへ昇格しない。

---

## 3.3 C — 言語モデル適合

MがTの宣言relationを、宣言scopeで実際に保持・再現・利用できるかを観測する。

### C1 言語差依存

宣言scope内の意味ある言語状態差へmodel resultが依存する。

### C2 規則性再現

任意random/hash/constantではなく、宣言したtarget relationに対応する反復可能な規則性を示す。

### C3 relation再利用

一つの完成input-output pair専用ではなく、複数状態へ同じmodel relationが適用される。

### C4 null / countermodelとの差

必要に応じて、

- constant
- random mapping
- identity
- global prior
- exact instance retrieval

等の適切なcontrolとの差を確認する。

検証形式を一つに固定しない。

prediction、reconstruction、ranking、structural consistency、grammar consistency、semantic relation consistency、counterfactual等を対象に応じて使う。

---

# 4. Language Modelの定義候補

> **Language Modelとは、言語対象契約Tに対する有限モデル射影Mを持ち、その対応Cが宣言scopeで成立しているmodelである。**

これは三physical componentsを要求するという意味ではない。

T/M/Cは、

```text
対象
モデル
対応観測
```

を混同しないための監査面である。

---

# 5. 実行系を別にする

model artifactとinference/runtimeを同一視しない。

## Layer-0X Execution Contract

最小形:

> **現在状態へモデル射影Mを適用し、Tへ再接続可能な結果状態・関係・評価を形成する遷移。**

説明用表現:

```text
S_t -- Apply(M) --> R_t
```

- `S_t`: 現在入力・文脈・候補等
- `Apply`: runtime/executor
- `R_t`: Tへ接続可能な結果

外部text emissionは必須でない。

---

# 6. Generativeを別属性にする

> **Generative capability = 実行結果Rが新しい言語状態・言語系列・言語構造を形成できる性質。**

方式は問わない。

- autoregressive
- diffusion
- symbolic generation
- hybrid

外部emit/API/UIとは分離する。

BERT等のrepresentational LMを、生成surfaceがないという理由だけでLanguage Model外へ追放しない。

---

# 7. Largeを三軸profileとして扱う

Largeはmodel作用の種類ではなく程度・適用域である。

## L1 状態域幅

同一modelが扱える言語状態の広さ。

## L2 関係域幅

同一model relationが扱える言語関係種別・関係深度の広さ。

## L3 再利用域幅

同じmodel relationを、別状態・未列挙組合せ・異なる領域へ再利用できる範囲。

```text
Large = multidimensional profile
```

とする。

普遍的一点thresholdは現時点で規定しない。

用途上二値判定が必要ならscope-specific reference envelopeを宣言する。

---

# 8. 原理LMと現代LLMを分ける

## 原理Language Model

T/M/Cで監査する。

## Contemporary LLM Reference Envelope 2026

HDSで観測したD3/D4 anchor群では、次が強く再現する。

- 強いcontext dependence
- 広いstate domain
- 多様・深いrelation processing
- 高いeffective compute depth
- 広いrelation reuse
- generative capabilityが運用上中心

これらは2026観測包絡であり、Language Model原理定義へ自動昇格しない。

---

# 9. Compute Topologyを別層に置く

HDS横断観測で得た主要軸:

```text
sequence flow
depth flow
width flow
future/predictive auxiliary
```

例:

- global / local / window / recurrent / linear / compressed / sparse
- standard residual / AttnRes / mHC
- dense / routed expert / shared expert
- MTP / draft / speculator

これらはT/M/Cを実現する方式であり、普遍必須機構名ではない。

---

# 10. Formation / Operational / Applicationを分離する

## Formation

- training
- post-training
- compilation
- authoring
- search
- evolution

## Operational Wrapper

- tokenizer/processor implementation
- inference kernel
- decoder/surface
- scheduler/cache
- API/CLI
- speculative serving

## Application / Agent

- RAG
- tools
- search
- persistent memory
- safety/fallback
- approval
- agent loop

model-only claimへ逆帰属しない。

---

# 11. 旧Layer-0項目の再配置

## 旧6役割

| 旧項目 | v5候補での位置 |
|---|---|
| TOKEN/SYMBOL SPACE | T / state adapter |
| CONTEXT CONDITIONING STATE | Large/Capability/Execution |
| LEARNED PARAMETERIZED TRANSFORM | M + Formation。learned/parameterizedは必須でない |
| CONDITIONAL OUTPUT SURFACE | C / Generative / Scoring |
| SEQUENCE MODELING OBJECTIVE | Formation / C evidence |
| DECODING / EMISSION | Operational Wrapper |

## 旧F1/F2/F3

| 旧項目 | v5候補での位置 |
|---|---|
| F1 内容依存選択的アクセス | Capability / Large L2/L3 / Efficiency |
| F2 内部知識保持 | Knowledge Placement / Formation / Capability |
| F3 有効直列深度 | Capability / Large L2 / Compute Topology |

旧観測を破棄せず、存在条件という帰属を解除する。

---

# 12. 極限反例

## random Transformer

T/Mは持ち得るがCが成立しない。

→ functioning LMとはしない。

## tokenizer

state mappingは持つが、target language relationのmodelではない。

→ adapter。

## unigram / n-gram

T/M/C成立候補。

→ Language Model。

LargeはL1-L3で別評価。

## grammar / parser

grammar modelはT/M/C成立候補。

parser executorはruntimeとして分離。

## sentiment classifier

language encoder部分とtask headを分離。

固定label relationだけをLM target relationとしない。

## calculator

中央target relationがarithmetic。

言語I/OだけではLMにならない。

## exact QA retrieval

question/answerが言語表面でもtarget relationはworld knowledge instance mappingの場合がある。

言語target relationと分ける。

## diffusion LM

T/M/C成立候補。

autoregressive不要。

## multimodal

text outputだけでLMとはしない。

language relation submodelがあるかを分離監査する。

---

# 13. MINIDORAへの現時点の厳格判定

新定義へ合わせてMINIDORAをPASSにしない。

現行実装から確認できるのは、

- `言語基底P` が文字体系・基本文法・基底概念・主要言語関係を保持する
- `HDS英語基底関係射影` が明示言語構文をHDS関係へ補完する
- HDS Compilerが自然言語をrich HDS-IRへ変換する
- K/C/Jが主に意味・知識・候補・関係を計算する

ことである。

従って次を未確定とする。

```text
MINIDORA_LANGUAGE_TARGET_T = OPEN
MINIDORA_MODEL_PROJECTION_M = OPEN
MINIDORA_LM_CONFORMANCE_C = OPEN
```

もし中央model relationが主にworld/task relationで、language relationはCompiler/adapterに局在するなら、現行MINIDORAはLanguage Modelではなくlanguage-mediated semantic reasoning systemである可能性がある。

この可能性を消さない。

---

# 14. HDS Compilerへの帰還

HDS Compilerを名称だけでadapterと固定しない。

次を監査する。

1. language target relation TのどこをCompilerが担うか
2. Compiler自身がmodel projection Mを持つか
3. CompilerとMINIDORA中央核のrelation boundary
4. `完全HDS-IR -> target-native compute state` のlowering契約

今回の性能低下は、rich semantic Projectionとnative compute operandを分離しなかったことの症状である可能性が高い。

---

# 15. 現時点の最小構造

```text
Target side
  T: Language Target Contract
       │
       │ model/projection
       ▼
Model side
  M: Finite Model Projection
       │
       │ observed correspondence
       ▼
  C: Language Modeling Conformance

Execution side
  S_t -- Apply(M) --> R_t

Independent profiles
  Generative
  Large L1/L2/L3
  Capability
  Compute Topology
  Formation
  Operational
  Application/Agent
```

---

# 16. 現在判断

## 強く支持

- T/M/C分離
- model/inference/harness分離
- Executionをstate transition契約として分離
- Language Model / Large / Generative / Operational分離
- Large三軸profile
- contemporary reference envelopeを普遍定義から分離
- implementation/construction名をCore必須から外す
- MINIDORAを反例候補として扱う

## OPEN

- Tの`language relation`境界をどこまで広く取るか
- cross-language modelの分類
- representational LMをLarge Language Model名称へ含める実務境界
- Large reference envelopeの具体実務値
- MINIDORAのT/M/C実体
- CompilerがMの一部かstate adapterか

## 次の再監査

OPENのうち、まず

1. `language relation`境界
2. MINIDORA T/M/C
3. HDS Compiler帰属

を閉じる。

これらが閉じるまで現行v4正本・MINIDORA・Compiler実装を変更しない。
