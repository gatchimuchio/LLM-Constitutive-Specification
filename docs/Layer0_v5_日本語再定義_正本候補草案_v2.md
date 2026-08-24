# Layer-0 v5 日本語再定義 — 正本候補草案 v2

## 状態

`DRAFT_V2 / NOT_CANONICAL / REOPENABLE`

- 規定言語: 日本語
- 現行v4正本: 変更しない
- v1草案: 履歴として保持
- 本書: 2026-08-25の追加反例・境界・最小性監査を反映した第二草案

---

# 1. 目的

本仕様は「現代LLMに多い部品」を列挙するものではない。

定義したい対象は、

> **Language Modelとは何か。Largeとは何か。Generativeとは何か。モデル物・実行系・展開systemの境界はどこか。**

である。

その上でLarge Language Modelの成立位置を記述する。

次を定義前提にしない。

- neural network
- Transformer
- Attention
- MoE
- autoregressive
- next-token prediction
- probability distribution
- learned parameter
- parameter count
- tokenizer / decoderという部品名
- chat / API / agent harness

---

# 2. 観測基盤

HDS横断観測対象:

- Llama 3
- K2-V2
- OLMo 3
- Apertus 1.5
- Qwen3.6
- DeepSeek V4
- Kimi K3 v2 full-weight
- GPT-5.6 Sol
- Claude Fable / Mythos
- Gemini 3.x
- Grok 4.6
- MINIDORA

反例・境界対象:

- BERT / encoder-only
- unigram / n-gram
- grammar / parser
- retrieval-only
- retrieval + composition
- diffusion language model
- classifier / ranker
- natural-language calculator

観測深度D4/D3/D2を同一確度として扱わない。

---

# 3. まず四つを分ける

旧Layer-0では次が混線していた。

```text
Language Model identity
Large
Generative capability
Operational system
```

v5では分離する。

## 3.1 Language Model

何であるか。

## 3.2 Large

どれだけ広い状態域・関係域・再利用域を持つか。

## 3.3 Generative

新しい言語系列・構造を形成できるか。

## 3.4 Operational

model artifactをruntime・I/Oへ接続して実行可能か。

---

# 4. Language Model Artifact の最小核

## 4.1 M1 — 言語状態域契約

> モデルが受ける、参照する、または結果として規定する状態のうち、少なくとも一つの主要経路が、言語の単位・順序・構造・関係・意味・候補等へ追跡可能に接続されていること。

重要:

- textである必要はない
- tokenである必要はない
- internal hidden state全てが人間可解釈である必要はない
- **言語接続を要求するのはmodel boundaryの状態契約であり、内部全状態の透明性ではない**

許容例:

- token / token sequence
- masked linguistic state
- contextual representation indexed by linguistic units
- recurrent linguistic state
- graph / symbolic linguistic state
- HDS座標・関係・semantic fact

### 入力側境界

言語が単なる出力装飾であるだけでは足りない。

モデル関係の条件・対象として、言語状態が意味的に作用する経路を要求する。

### 結果側境界

結果は必ずしも文章でなくてよい。

次を許容する。

- 言語状態
- 言語構造
- 言語候補集合
- 言語候補へのscore / relation / ordering
- 言語単位へ対応するcontextual representation

固定task labelや純算術値は、表面が文字列でもそれだけで言語状態とは扱わない。

---

## 4.2 M2 — 再利用可能なモデル関係

> 同一versionとして追跡可能で、複数の言語状態へ再利用される関係仕様が、言語状態・言語候補・言語構造の間にどのような評価・変換・対応が成立するかを規定すること。

model relationの実体は問わない。

- weights
- conditional table
- grammar / rules
- graph
- compiled operator
- program
- hybrid relation set

を許容する。

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

### model identity

model relationは永久不変である必要はない。

少なくとも、

```text
model_id
version
relation_contract
provenance
```

により変化を追跡できることを要求する。

---

# 5. Language Model の最小定義

## 定義候補

> **Language Modelとは、言語状態域契約 M1 と、その状態域上で再利用されるモデル関係 M2 を持つモデル物である。**

より作用として言えば、

> **言語状態・言語候補・言語構造の間の関係を、複数入力へ再利用可能な同一モデルとして規定するもの。**

この段階ではruntime、decoder、API、training methodを含めない。

---

# 6. M1とM2の最小性

## M1を除去

モデル関係が何についてのモデルなのかという言語状態域が消える。

残るのは一般関数・非言語model・opaque relationであり、Language Model identityが成立しない。

## M2を除去

言語状態表現だけが残る。

- text buffer
- passive embedding store
- token sequence storage

等になり、model relationがない。

## M1とM2を一項へ統合できるか

抽象数学上は `言語状態域上のモデル関係` と一語へ畳める。

しかし工学監査では、

- domain / boundaryの誤り
- model relationの誤り

を独立に検査する必要がある。

従ってv5では**一つの不可約関係を構成する二つの論理役割**として保持する。

```text
不可約関係 = 言語状態域契約 × モデル関係
```

`2 roles != 2 physical components`

---

# 7. 実行系をmodel artifactから分離する

Language Model Artifactは、実行されなくてもversioned model objectとして存在し得る。

実際に挙動を発生させるには別途、

```text
現在状態
+
モデル物
+
適用作用/runtime
→
結果状態
```

が必要である。

これを **Layer-0X: Execution Contract** として分ける。

## X1 現在状態

入力・文脈・候補・外部条件等。

## X2 適用作用

model relationを現在状態へ適用するexecutor。

## X3 結果接続

結果をM1で規定した言語状態・言語関係・言語評価へ接続する。

X1-X3はOperational conformanceには必要だが、model artifactのcomponent数へ数えない。

---

# 8. Generativeを別属性にする

## 生成的Language Model

> 現在状態に対して、保存済み完成個体の単純選択だけではない新しい言語系列・言語構造・言語候補状態を形成可能なLanguage Model。

方式は問わない。

- autoregressive
- diffusion
- symbolic generation
- hybrid

等を許容する。

BERT等のrepresentational LMを、外部生成がないという理由だけでLanguage Model外へ追い出さない。

---

# 9. Largeを最小3軸へ圧縮する

LargeはCore作用ではなく程度属性である。

従来の多数のprofile軸は、現時点では次の三軸へかなり圧縮できる。

## L1 — 状態域幅

同一modelが扱える言語状態の広さ。

下位観測例:

- 語彙・表記・言語
- 系列長
- 構造階層
- 入力形態
- 結果状態の開放性

## L2 — 関係域幅

同一model relationが扱える言語関係の多様性・深さ。

下位観測例:

- 局所依存
- 長距離依存
- 構文関係
- 意味関係
- 談話関係
- 関係合成
- 有効計算深度

特定の言語学分類を最終正本に固定しない。重要なのは関係種別・深度の幅である。

## L3 — 再利用域幅

同じmodel relationを、どこまで別状態・未列挙組合せ・領域へ再利用できるか。

下位観測例:

- 未列挙組合せ
- 異なるtopic/domain
- 異なるtask形式
- 文脈差
- 言語差

## Largeの判定

```text
Large = multidimensional profile
```

とする。

普遍的一点thresholdは現時点で規定しない。

用途上二値判定が必要なら、対象scopeごとにreference envelopeを宣言する。

その採用境界を自然法則・普遍定義へ昇格しない。

---

# 10. 旧F1/F2/F3の再配置

旧不可約仕様で存在条件とした、

- F1 内容依存情報検索
- F2 内部知識保持
- F3 十分な直列深度

は有用な観測である。

ただしv5ではCore existence conditionから分離する。

## F1 内容依存情報検索

→ `Capability / Efficiency`

unigram等のLanguage Model一般へは必須でない。

## F2 内部知識保持

→ `Knowledge Placement Profile`

外部R / retrieval / compiled knowledgeを許容するため、parametric内部知識をCore必須にしない。

## F3 十分な直列深度

→ `Capability / Compute Profile`

複雑な推論能力には重要だが、model identityの論理必要条件とは分離する。

旧観測を破棄せず、帰属層を修正する。

---

# 11. Compute Topologyを別層へ置く

HDS横断観測で得た、

- 系列方向
- 深さ方向
- 幅方向
- 未来予測補助

は実装比較に重要である。

しかしLayer-0MのM1/M2へ昇格しない。

```text
Layer-T Compute Topology
  sequence flow
  depth flow
  width flow
  future auxiliary
```

として保持する。

選択・圧縮・MoE・window・recurrent等はここまたはEfficiencyへ置く。

---

# 12. 反例判定

## unigram

M1: 成立
M2: 成立

Language Model。
Large profileは文脈・関係域で小さい。

## n-gram

M1: 成立
M2: 成立

Language Model。
Largeかどうかはprofileで評価。

## BERT / encoder-only

M1: 文脈化言語状態として成立可能
M2: 成立

Language Model candidate。
Generativeは別判定。

## parser / grammar

言語状態→言語構造というrelationを再利用するならLanguage Model candidate。

Large profileの関係域・再利用域で狭さを保持する。

## sentiment classifier

encoder部分がLMである可能性と、classifier applicationを分離する。

固定task labelへの最終写像だけをLanguage Model identityとしない。

## calculator

主要relationが算術状態上にあり、言語はinterfaceへ退く。

Language Model coreではない。

## exact retrieval

M1/M2だけではrelation artifactとして成立し得る。

これを名称禁止で排除しない。

ただしLarge profileでは、

- 関係域の浅さ
- 未列挙組合せへの弱さ
- instance memorization依存

が現れる。

retrieval + compositionは別評価する。

## diffusion LM

M1/M2成立。
autoregressiveを要求しない。

---

# 13. MINIDORAへの再写像（まだ実装変更しない）

新定義候補から見ると、現行MINIDORAは次の再分別が必要である。

## M1候補 — 言語状態域契約

- HDS-IR
- 座標
- 関係
- semantic fact
- candidate / query state

## M2候補 — model relation

- 言語基底
- capability kernelの固定関係
- J / Gateの固定判断関係
- canonical Kのmodel固有部分
- model identityを構成する固定code / rule / compiled relation

## Run Stateへ送る候補

- 入力ごとのHDS-IR
- P / 手順
- 外部R取得Data
- 現在主体状態
- turn-specific候補

特に **Pをmodel identityへ固定せず、run-specific state / executable planとして再監査する**。

## HDS Compiler

HDS Compilerは、外部自然言語からM1の内部状態契約へ接続する**高度なLanguage State Adapter / Compiler**として再監査する。

これをM2のmodel intelligenceと無条件に同一視しない。

この分離は、今回の「Compilerが完全意味IRを増やしすぎ、MINIDORA計算核のnative operandへloweringできていなかった」問題と直接接続する。

---

# 14. 新しい全体層候補

```text
Layer-0M  Language Model Artifact Minimum
          M1 言語状態域契約
          M2 再利用可能なモデル関係

Layer-0X  Execution Contract
          X1 現在状態
          X2 適用作用
          X3 結果接続

Layer-G   Generative Profile

Layer-L   Large Profile
          L1 状態域幅
          L2 関係域幅
          L3 再利用域幅

Layer-C   Capability Profile
          selective access
          knowledge use
          effective compute depth
          reasoning/composition etc.

Layer-T   Compute Topology
          sequence / depth / width / future

Layer-F   Formation / Construction

Layer-O   Operational Wrapper / Serving

Layer-A   Application / Agent System
```

---

# 15. v4からの継承と撤回候補

## 継承

- implementation nameを定義へ固定しない
- constructionとruntimeを分離する
- model/system boundaryを明示する
- negative controlsを持つ
- unknown / SUSPENDを保持する
- exact minimumを再開放可能にする

## 撤回候補

v4の5責任をLanguage Model Artifactのexact minimumとして扱うこと。

特に、

- 言語アドレス化 + 文脈束縛状態
- 変換・合成 + 結果形成
- 結果表面

の分割は、model artifact / runtime / wrapperを跨いでいる。

---

# 16. 現時点の判断

## 強く支持

- Language Model / Large / Generative / Operationalの分離
- model artifact / execution / deploymentの分離
- Language Model Artifact = M1 + M2 の二役割候補
- internal全状態の言語可解釈性を要求しない
- Large = 3軸profile
- decoder/emissionをArtifact Coreから外す
- learned/neural/parameterizedをArtifact Coreから外す
- autoregressiveを普遍条件から外す
- F1/F2/F3をCapability/Profileへ再配置

## OPEN

- M1/M2を完全に一項へ畳むべきか
- exact retrievalをLM Coreの最小例としてどこまで許容するか
- Large reference envelopeの実務閾値
- representational LMを`LLM`という名称へどこまで含めるか
- multimodal modelでLanguage Model subrelationをどの境界で切るか

## 禁止

これらOPENを埋める前にMINIDORA/HDS Compiler実装を新定義へ変更しない。
