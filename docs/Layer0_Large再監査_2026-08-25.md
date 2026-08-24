# Layer-0 「Large」再監査 — 2026-08-25

## 状態

`WORKING / NOT_CANONICAL`

本書は Large Language Model の `Large` を、機能・作用・規模・適用域のどこへ置くべきか再監査する。

---

## 1. 出発点

`Large` は、

- 状態を保持する
- 関係を参照する
- 状態を変換する
- 結果を形成する

のようなruntime作用ではない。

したがって、`Large`をLayer-0の独立計算作用として置くことはできない。

---

## 2. 横断HDSからの観測

既存HDS構文化では、同一または近縁architecture familyの中でも規模が異なる個体が同じ上位機能へ写る。

例:

- Llama 3: 8B / 70B
- OLMo 3: 7B / 32B
- Apertus 1.5: 8B / 70B
- Dense / MoEでも総parameter数とactive parameter数が異なる

この差は性能・容量・効率へ作用しても、

```text
言語状態を持つ
文脈を効かせる
model作用で状態を更新・評価する
```

という機能核の種類を変えない。

従ってparameter countをLayer-0の不可約責任へしない。

---

## 3. 「Large」はカテゴリではなく程度語である可能性

`Language Model` は機能カテゴリとして定義可能である。

一方、`Large` は少なくとも次の尺度を含み得る。

- 状態域の広さ
- 文脈幅
- 関係深度
- 適用領域幅
- 未列挙組合せへの再利用範囲
- 形成された知識量
- 内部容量
- 計算資源

これらは連続的であり、「この一点を越えればLarge」という自然な普遍境界が現時点で観測されていない。

したがって、Largeを二値のLayer-0責任へ無理に変換しない。

---

## 4. parameter数を根拠にしない理由

### 4.1 実装依存

同じ機能を、

- dense parameter
- sparse expert
- rule
- graph
- external memory
- compiled relation
- retrieval + composition

で実現した場合、必要parameter数は一致しない。

### 4.2 active capacityとtotal capacityが違う

MoEでは総parameter数と一回の計算で使うparameter数が違う。

### 4.3 MINIDORA反例

MINIDORAは、HDS Compiler、K、R、J等へ機能を分離するため、ニューラルweight総量をLargeの代理変数にすると定義だけで排除される。

これは今回の目的に反する。

---

## 5. 大規模性を何で見るか

数値一つではなく、まず**言語域プロファイル**として保持する。

### L1. 言語状態域幅

同一model coreが、どれだけ広い語彙・構文・意味関係・表現形を扱えるか。

### L2. 組合せ開放性

全input-output組を事前列挙せず、未観測・未列挙の組合せへ同じmodel作用を再利用できるか。

### L3. 領域横断性

特定task専用programへ差し替えず、複数の異なる話題・知識領域へ同じcoreを適用できるか。

### L4. 文脈関係幅

同時に保持・参照・統合できる状態数、距離、階層、関係種別の広さ。

### L5. 結果状態域幅

固定labelや有限templateだけでなく、多様な言語接続状態・構造・評価を形成できるか。

### L6. 外部知識依存分離

世界知識量そのものと、言語状態を処理するmodel coreの能力を分離して評価する。

---

## 6. calculator / classifierとの境界

自然言語calculatorやsentiment classifierは、狭い範囲では言語状態接続・文脈・状態作用を持てる。

しかし通常は、

- 主作用対象が算術や固定labelへ閉じる
- 適用領域がtask固有
- 結果状態域が狭い
- 同じcoreを unrelated domain へ再利用できない

ため、Large側の言語域プロファイルで明確に縮退する。

ここから、narrow task systemを除外する責任をFunctional Coreへ押し込まず、適用域側で扱う。

---

## 7. n-gramとの境界

大規模n-gramは、

- 言語状態
- 有限文脈
- 条件付き評価
- 言語結果状態

を持ち得る。

したがって機能だけを見ればLanguage Modelである。

それが`Large`に相当するかは、parameterization方式ではなく、実際の言語状態域・組合せ開放性・文脈関係幅等で評価する。

この結果、巨大n-gramが十分なLarge profileを満たすなら、構造定義上はLLM候補から先験的に排除しない。

これは現代業界用語の慣習と一致することを目的としない。対象の機能・境界・作用を先に取る。

---

## 8. 新Layer-0の二段構造候補

### Layer-0 Core: 言語モデル核

現在の3責任候補:

1. 言語接続状態域
2. 文脈有効関係
3. 再利用可能な状態作用

### Layer-L: 大規模性／言語域

連続profile:

- L1 言語状態域幅
- L2 組合せ開放性
- L3 領域横断性
- L4 文脈関係幅
- L5 結果状態域幅
- L6 外部知識依存分離

### 現時点の意味

```text
LM identity = categorical core
Large       = scalar/profile qualification
LLM         = LM core + sufficiently broad Large profile
```

ただし `sufficiently broad` の単一普遍thresholdは現時点で定義しない。

---

## 9. 重要な帰結

もしLargeに普遍的な一点閾値が存在しないなら、`LLMか否か`は完全な二値自然種ではない。

その場合、Layer-0が厳密に定義すべきものは、

1. 言語モデルとして成立する最小機能核
2. Largeを評価する独立profile
3. model core / runtime / wrapper / applicationの境界

である。

`Large`を無理に機能責任へ変換しないこと自体が、旧Layer-0からの重要な修正になる。

---

## 10. 現時点の判定

- `Large = runtime function`: **否定**
- `Large = parameter count threshold`: **普遍定義として否定**
- `Large = continuous scale/profile`: **強く支持**
- `Language Model core + Large profile`二段構造: **強く支持**
- 単一普遍threshold: **OPEN / 現時点で根拠なし**

次は3責任候補自体をさらにmergeできるか、MINIDORAとD3/D4モデルへ再写像して最小性を監査する。
