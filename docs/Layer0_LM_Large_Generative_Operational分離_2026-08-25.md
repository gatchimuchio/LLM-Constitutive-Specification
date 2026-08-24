# Layer-0 LM / Large / Generative / Operational 分離 — 2026-08-25

## 状態

`WORKING / NOT_CANONICAL / REOPENABLE`

旧Layer-0が揺れた主要因の一つは、次の異なる性質を `LLM` 一語へ押し込んだことである。

```text
Language Model identity
Large scale / breadth
Generative capability
Operational deployment
```

本書ではこれらを分離する。

---

# 1. Language Model

## 定義候補

> **Language Modelとは、言語へ追跡可能に接続された状態域の上で、複数の状態へ再利用されるモデル関係を持ち、その関係により言語状態・言語関係・言語候補の評価を規定できるモデル物である。**

重要:

- neuralである必要はない
- trainedである必要はない
- autoregressiveである必要はない
- textを外部生成する必要はない
- probability distributionを必須としない
- tokenizerという物理部品を必須としない

この定義は`model artifact`を対象にする。

---

# 2. Generative

GenerativeはLanguage Model identityとは別の能力属性とする。

## 生成的言語モデル

> 現在の言語状態から、保存済み完成個体の単純取得だけではない新しい言語系列・言語構造・言語候補状態を形成できるLanguage Model。

これにより、

- autoregressive LM
- diffusion LM
- grammar generator
- MINIDORAの言語結果形成

等を同一上位属性へ置ける。

一方、BERT encoder-only等はLanguage Model候補であっても、model artifact単体では自由系列生成を必須としない。

---

# 3. Large

Largeは機能種別ではなく**程度・適用域**である。

Large profileは少なくとも次を持つ。

1. 言語状態域幅
2. 言語関係多様性
3. 組合せ開放性
4. 文脈関係幅
5. 領域横断性
6. 結果域開放性
7. 有効計算深度
8. 知識・記憶依存の配置

`parameter count`は実装固有の観測値として記録できるが、Largeの定義そのものにしない。

## Largeの二値化

普遍的一点thresholdは現時点で観測されていない。

従って正本候補では、

```text
LM_CORE = categorical
LARGE   = multidimensional profile
```

を原則とする。

必要な用途では、対象分野ごとにreference envelopeを採用して `Large相当` を判定できるが、そのthresholdを自然法則へ昇格しない。

---

# 4. Operational

Operationalはmodel artifactが実際に実行可能なsystemへ接続されているかという別属性である。

```text
Model Artifact
  + Runtime
  + Current State
  + I/O adapter
  = Operational Model System
```

API、CLI、chat UI、decoder surface等はここへ置く。

`isolated model artifact` と `deployed system` を同一視しない。

---

# 5. 新しい分類面

## 5.1 Representational LM

言語状態から文脈化された言語状態・表現を形成する。

例:

- encoder-only contextual model

## 5.2 Scoring / Conditional LM

現在言語状態に対して、別の言語状態・候補の評価関係を形成する。

例:

- unigram / n-gram
- masked token scoring
- next-token scoring

## 5.3 Generative LM

現在言語状態から新しい言語系列・構造を形成できる。

方式は問わない。

- autoregressive
- diffusion
- symbolic generation
- hybrid

## 5.4 Large LM

上記Language Model coreのうち、Large profileが対象reference envelopeで十分広いもの。

## 5.5 Operational LLM system

Large LM artifactをruntimeへ接続し、外部から観測可能な実行系にしたもの。

---

# 6. 旧Layer-0の混線を説明する

## decoder / emission必須問題

旧仕様はOperational Generative LLMを対象にしたため、decoder/emissionをLayer-0へ入れた。

しかしこれは、

```text
Language Model identity
≠
Operational generative interface
```

を混ぜていた。

## encoder-only排除問題

BERT等を「LLMでない」と定義側から排除すると、Language ModelとGenerative/Operationalの境界が崩れる。

新仕様では、

- LMか
- Generativeか
- Largeか
- Operationalか

を別々に判定する。

## unigram / n-gram問題

LMとしては成立し得る。

Large profileは小さい／限定的になり得る。

従って「古いから非LM」としない。

---

# 7. MINIDORAへの意味

MINIDORAは少なくとも次を別々に監査する。

1. **LM artifact identity**
   - 何をMINIDORAのmodel relation正本とするか
2. **Generative capability**
   - 新しい言語結果状態を形成できるか
3. **Large profile**
   - 状態域・関係域・組合せ域・文脈幅等
4. **Operational system**
   - Runtime / Compiler / R / J / surface等の接続

これにより、

```text
MINIDORAが動く
```

ことと、

```text
MINIDORAのmodel artifactは何か
```

を分離できる。

---

# 8. 現時点の判定

- Language ModelとGenerativeの分離: **強く支持**
- Language ModelとOperationalの分離: **強く支持**
- Largeを独立profile化: **強く支持**
- GenerativeをLM Core必須にする: **否定方向**
- decoder/emissionをLM artifact必須にする: **否定**
- BERT系を名称だけでLM外へ追い出す: **不採用**
- contemporary usageへの一致を最上位基準にする: **不採用**

次はLanguage Model artifactの最小核を、`言語状態域契約 + モデル関係`の二役割で固定できるかを監査する。
