# Layer-0 原理LMと現代LLM参照包絡 — 2026-08-25

## 状態

`WORKING / NOT_CANONICAL / REOPENABLE`

目的は、Language Modelの原理的最小関係と、2026年時点で実際にLarge Language Modelとして観測される系統の特徴を分離することである。

---

# 1. 二つの問いは違う

## 原理質問

```text
何が成立すればLanguage Modelなのか
```

## 現代分類質問

```text
2026年にLLMとして実在・運用される主要系統は、どのようなprofile領域に集まっているか
```

後者を前者の定義にしてはならない。

---

# 2. 原理Language Model

現時点の最小候補:

> **言語状態域に存在する言語上の規則的関係を、複数状態へ再利用可能なモデル関係として保持するもの。**

監査面:

1. language scope / state domain
2. reusable model relation
3. linguistic regularity conformance

実装・形成・生成方式は別。

---

# 3. Large Profile

原理LMに対する程度属性を三軸で保持する。

## L1 状態域幅

扱える言語状態の広さ。

## L2 関係域幅

扱える言語関係種別・深度の広さ。

## L3 再利用域幅

同じmodel relationを別状態・未列挙組合せ・異領域へ使える範囲。

普遍的一点thresholdを置かない。

---

# 4. 2026年HDS観測集合

主な高観測深度anchor:

- Llama 3 — D3 dense/global
- K2-V2 — D3 dense/global
- OLMo 3 — D3 sliding/full hybrid
- Apertus 1.5 — D3 multimodal extension
- Qwen3.6 — D3 linear/full + MoE
- DeepSeek V4 — D3 hybrid/compressed + mHC/MoE
- Kimi K3 v2 — D4 KDA/MLA + AttnRes + LatentMoE

補助D2:

- GPT-5.6 Sol
- Claude Fable/Mythos
- Gemini 3.x
- Grok 4.6

D2はcore internalsを推定しない。

---

# 5. 観測集合で強く再現する特徴

以下は「普遍定義」ではなく、現代LLM参照包絡の特徴候補である。

## E1. 強い文脈依存

D3/D4 anchorでは、方式は異なるが複数状態間の関係を現在計算へ利用する。

- global causal attention
- sliding + full
- linear/recurrent + full
- compressed/sparse long-range
- KDA/MLA recurrent/attention hybrid

従って、現代LLM参照包絡はLarge L2/L3の文脈関係幅が大きい。

ただしLanguage Model一般の必須条件にはしない。unigram反例がある。

## E2. 多段の関係変換

D3/D4 anchorは深いstack、recurrent/hybrid更新、depth transport等を持つ。

現代LLM参照包絡では有効計算深度が大きい。

ただし原理LM identityの必須条件ではなくCapability/Large L2へ置く。

## E3. 広い言語状態域

大規模vocab、長系列、複数形式、モデルによってはmultimodal前段を持つ。

Large L1の主要観測になる。

## E4. relationの再利用域が広い

base/instruct/think等のvariant差、長context拡張、multimodal前段追加でも中央coreを再利用する例がある。

これは同一relationの再利用範囲を観測する材料になる。

ただし個々の未知domainへの汎化を、model cardだけから無制限に断定しない。

## E5. Generative capability

今回のD3/D4 contemporary anchorは、language generationを主要運用面として持つ。

従って「2026 contemporary LLM reference envelope」ではGenerativeを強い特徴として保持できる。

ただしLanguage Model原理核へは戻さない。

---

# 6. 現代LLM参照包絡の暫定形

数値thresholdではなく、profile envelopeとして次を記録する。

```text
Contemporary-LLM-Envelope-2026

LM Core Conformance       = PASS
Generative                = strong / operationally central
Large.L1 State Breadth    = high
Large.L2 Relation Breadth = high
Large.L3 Reuse Breadth    = high
Context Dependence        = strong
Effective Compute Depth   = high
Operational Surface       = language generation/scoring
```

これは自然法則ではない。

新familyが現れれば更新する観測包絡である。

---

# 7. 境界事例の位置づけ

## unigram / n-gram

LM Core = PASS候補
Contemporary-LLM-Envelope = 通常かなり外側

## parser / grammar

LM Core = PASS候補
Large profile / Generative / relation breadthを別評価

## BERT / encoder-only

LM Core = PASS候補
Generative = 非必須/弱い場合あり
Contemporary generative LLM envelopeとは別位置

## giant phrase table

LM Core conformanceをrelation scopeで監査
Large L1が大きくてもL2/L3が狭い場合がある

## MINIDORA

新定義へ合わせてPASSにしない。

Layer-0 v5確定後に、LM Core / Functional Conformance / Large / Generative / Operationalを独立再監査する。

---

# 8. 旧「contemporary technical usage」方式との違い

旧v2/v3系では、provider用語の収束を先に使い、

- learned
- parametric
- contextual
- generative
- emission

等をLLM境界へ入れた。

v5候補では逆に、

1. 原理LMを構造から定義
2. Largeを独立profile化
3. Generativeを別属性化
4. contemporary usageをReference Envelopeとして記録

する。

これにより、用語慣習は観測資料として利用するが、原理核のauthorityにはしない。

---

# 9. 現時点の判定

- 原理LMと現代LLM参照包絡の分離: **強く支持**
- contemporary provider usageを原理定義にする: **不採用**
- Generativeを2026参照包絡の強特徴とする: **支持**
- GenerativeをLM原理必須にする: **否定**
- context/depth/breadthをLarge/Capabilityへ置く: **支持**
- 参照包絡を固定普遍threshold化する: **禁止**

この分離をv5最終候補へ統合する。
