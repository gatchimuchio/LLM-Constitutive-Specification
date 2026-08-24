# Layer-0 v5 日本語再定義 — 正本候補草案

## 状態

`DRAFT / NOT_CANONICAL / REOPENABLE`

- 規定言語: 日本語
- 現行v4正本: 変更しない
- 本書の目的: 「LLMとは何か」を、既存名称・Transformer・学習方式・英語圏の慣習定義から先取りせず、HDS横断観測から機能・境界・作用・規模を再構築する。

---

# 1. 出発点

Layer-0が定義する対象は、特定の実装方式ではない。

定義したいものは、

> 大規模言語モデルとして成立するために、どのような状態と作用が最低限必要であり、どこからどこまでをモデル本体として扱うべきか。

である。

次を定義前提にしない。

- neural network
- Transformer
- Attention
- MoE
- autoregressive
- next-token prediction
- probability distribution
- trained parameter
- parameter count
- tokenizerという部品名
- decoderという部品名
- API / chat UI
- agent harness

---

# 2. 観測根拠

主なHDS再観測対象:

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

補助反例:

- BERT / encoder-only model
- n-gram / unigram
- 記号文法
- retrieval-only
- retrieval + composition
- diffusion language model
- classifier / ranker
- natural-language calculator

観測深度D4/D3/D2を同一確度として扱わない。

---

# 3. 第一原則 — 状態と作用を分ける

横断観測を最小まで圧縮すると、計算核には二つの非対称なものが残る。

1. 入力・文脈ごとに変化する状態
2. 複数状態へ再利用され、model identityを保持する作用

この二つを同一視しない。

```text
状態 = 今ここで何が保持・区別されているか
作用 = その状態へ何をするmodelなのか
```

---

# 4. Layer-0 Core — 2責任候補

## A. 言語文脈状態

### 定義

> 言語に接続された単位・差異・関係・順序・条件・履歴等を、現在処理の結果へ作用可能な内部状態として区別できること。

### 必須意味

- 現在の入力差が内部状態差になる。
- 文脈差が結果差へ到達できる。
- 言語との対応が計算途中で完全に失われない。
- 状態は直接tokenである必要はない。

### 許容される実装例

- token / token ID
- embedding
- hidden state
- KV state
- recurrent state
- graph state
- HDS座標
- HDS関係
- semantic fact
- symbolic stack
- structured memory

### 否定条件

- 入力言語差を内部で区別できない。
- 文脈を変えても内部状態または後続結果が変わらない。
- 言語は単なる無関係な外装で、model coreへ言語差が到達しない。

---

## B. モデル作用

### 定義

> 版として同定可能で再利用可能な作用が、現在の言語文脈状態へ適用され、参照・評価・関係形成・変換・合成・統合・更新等を通じて、新しい言語接続状態・関係・評価を形成できること。

### 必須意味

- 一入力専用の固定応答ではない。
- 複数の言語文脈状態へ同じmodel identityを再利用できる。
- 状態を受けるだけでなく、状態差に応じた結果差を形成する。
- 結果は外部文字列でなくてもよい。
- 新状態、関係、score、候補評価、内部表現等でもよい。

### 許容される実装例

- attention + FFN
- recurrent update
- diffusion denoising
- KDA / MLA
- mHC / AttnRes
- MoE / Dense
- symbolic rule
- graph operation
- compiled operator
- table-based conditional model
- retrieval + composition

### exact retrievalとの境界

保存済みの完成個体をkeyで返すだけの系は、model actionの中心例としない。

一方、table lookup自体を禁止しない。

n-gramの条件表のように、保存形式がtableであっても現在文脈から言語状態の評価を形成するなら、実装名だけで排除しない。

---

# 5. Coreの最小性

## Aを除去

モデル作用が作用すべき現在の言語・文脈状態が消える。

残るのは、

- 定数生成
- 非言語関数
- 固定反応

等であり、LLM coreとして成立しない。

## Bを除去

言語文脈状態は存在するが、その状態へmodel identityを持つ作用がない。

残るのは、

- passive storage
- representationだけの保持
- opaque memory

等であり、LLM coreとして成立しない。

## AとBを統合できるか

状態は入力・時点で変わる。

モデル作用は同一version内で複数状態へ再利用される。

この非対称性を失わず一責任へ統合する根拠は、現時点ではない。

従って2責任を暫定最小候補とする。

---

# 6. 「結果形成」を独立責任にしない

モデル作用Bは、状態を入力として新状態・関係・評価を形成する。

従って「結果形成」はBの出力側に内包できる。

外部の、

- text emission
- token emission
- API
- JSON
- score endpoint
- chat UI

等はmodel coreと分離する。

BERT系のように、外部自由生成を持たず文脈化状態を形成するmodelを、結果表面の有無だけでcore外へ追い出さない。

---

# 7. 「Large」はCore作用ではない

Largeは状態作用の種類ではなく程度・規模を表す。

従ってLayer-0 Coreの責任数へ含めない。

## Large profile候補

### L1. 言語状態域幅

同一coreが扱える語彙・構造・意味関係・表現形式の広さ。

### L2. 組合せ開放性

全input-output対を事前列挙せず、未列挙組合せへ同じmodel作用を適用できる範囲。

### L3. 領域横断性

特定task専用programへ差し替えず、複数の話題・知識領域へ同じcoreを適用できる範囲。

### L4. 文脈関係幅

同時に利用できる状態数・距離・階層・関係種別の広さ。

### L5. 結果状態域幅

固定label・有限templateへ閉じず、多様な言語接続状態・関係・評価を形成できる範囲。

### L6. 外部知識依存分離

世界知識の保存量と、言語状態を処理するmodel coreの能力を分離して記述する。

## Largeの判定

Largeに普遍的な一点thresholdがあるという証拠は現時点でない。

したがって、

```text
Large = profile
```

として保持し、parameter数だけで二値化しない。

---

# 8. LLMの暫定再定義

## 機能核

> 言語文脈状態を保持し、その状態へ再利用可能なモデル作用を適用して、新しい言語接続状態・関係・評価を形成する計算系。

## Largeを含む全体

> 上記機能核を持ち、広い言語状態域・文脈関係・組合せ・領域・結果状態へ同じmodel coreを再利用できる規模を持つ言語モデル。

ただしLargeの普遍的数値閾値は規定しない。

---

# 9. 境界層

## 9.1 Core

- 言語文脈状態
- モデル作用

## 9.2 Formation / Construction

- trained
- authored
- compiled
- induced
- searched
- evolved
- hybrid

形成方法をCore identityへ混ぜない。

## 9.3 Compute Topology

- 系列方向の情報流
- 深さ方向の情報流
- 幅方向の情報流
- recurrent / window / global
- compression
- routing
- delta update

これらはCore責任の実現方式であり、普遍必須の機構名ではない。

## 9.4 Efficiency Profile

- top-k
- sparse routing
- cache
- compression
- recurrentization
- local window
- expert routing
- speculative / draft

効率化方式をLLM identityへ昇格しない。

## 9.5 Operational Wrapper

- tokenizer/decoderの物理配置
- API
- text/score surface
- scheduler
- cache manager
- serving runtime

責任Aを満たすためのadapterがcore boundaryの内外どちらに実装されるかは候補systemごとに明示する。

## 9.6 Application / Agent System

- RAG service
- tools
- search service
- safety classifier
- approval
- persistent memory service
- agent loop
- multi-agent orchestration

model能力へ逆帰属しない。

---

# 10. 横断HDSへの適合

| 対象 | A 言語文脈状態 | B モデル作用 | 固有実装差 |
|---|---|---|---|
| Llama 3 | 成立 | 成立 | global GQA / dense / standard residual |
| K2-V2 | 成立 | 成立 | global GQA / dense / long-context形成差 |
| OLMo 3 | 成立 | 成立 | sliding×3 + full×1 |
| Qwen3.6 | 成立 | 成立 | linear×3 + full×1 / MoE / MTP |
| DeepSeek V4 | 成立 | 成立 | sliding/CSA/HCA / mHC / MoE |
| K3 v2 | 成立 | 成立 | KDA/MLA / AttnRes / LatentMoE |
| diffusion LM | 成立 | 成立 | masked/noised state + iterative denoising |
| MINIDORA | 成立 | 成立 | HDS state / K relation / graph / J / deterministic operators |

closed-weight D2対象はcore内部を推測せず、サービス挙動だけからA/B内部実装を確定しない。

---

# 11. 旧Layer-0への判定

## v3以前

`learned parameterized transform`、`sequence fitting`、`emission interface`等をLLM identityへ置いた方法は、新定義では採用しない。

理由:

- formationとruntimeの混同
- coreとwrapperの混同
- 非ニューラル候補の先験排除

## v4

v4の5責任はcandidate conformance語彙として有効な観測を含む。

しかし、

- 言語アドレス化
- 文脈束縛状態

はAへ統合可能であり、

- 変換・合成中核
- 文脈依存結果形成

はBへ統合可能であり、

- 結果表面

はwrapperへ分離可能である。

従って、LLM最小計算構成としては5責任より2責任の方が小さく、現行横断証拠を失わない可能性が高い。

---

# 12. MINIDORAへの示唆

本書確定前にMINIDORAを変更しない。

ただし再監査時は、

- HDS Compiler / language adapterがA「言語文脈状態」をどこまで形成するか
- K/C/J/Layer0等がB「モデル作用」をどう分担するか
- full HDS-IRとCompute IRをどこで分離するか

を新しい責任境界で見直す。

---

# 13. 未確定事項

1. Large profileに最低限必要な軸はどれか。
2. Largeの二値thresholdをあえて設けるべきか。
3. unigramを「Language Model一般」には含めつつLLM Coreから除外する境界の名称。
4. exact retrievalとmodel actionの区別を、behaviorだけでどこまで確定できるか。
5. encoder-only representation modelをLLMの通常語義へ含めるかは、構造分類と別に扱うべきか。
6. MINIDORAにおけるHDS Compilerのcore boundary位置。

---

# 14. 再開放条件

次のいずれかが見つかった場合、2責任候補を再開放する。

1. Aなしで広域LLM機能を成立させる反例。
2. Bなしで広域LLM機能を成立させる反例。
3. A/Bを一責任へ統合しても状態とmodel identityの差を失わない構成。
4. A/Bへ写像できない独立必須作用。
5. D3/D4新architecture familyでA/Bが破綻。
6. MINIDORAの実装再監査でA/Bでは説明できない必須作用が見つかる。

---

# 15. 現在判定

```text
旧v3定義                         = RETIRED FOR NEW ROOT DEFINITION
v4候補適合語彙                   = STILL USEFUL
v4を最小Compute Architectureと扱う = REJECTED
2責任Core                       = STRONG CANDIDATE
Large profile分離               = STRONGLY SUPPORTED
日本語正本化                     = NOT YET
MINIDORA修正                    = NOT STARTED
HDS Compiler修正                = NOT STARTED
```
