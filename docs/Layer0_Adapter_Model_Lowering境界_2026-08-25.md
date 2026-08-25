# Layer-0 Adapter / Model / Lowering 境界 — 2026-08-25

## 状態

`WORKING / NOT_CANONICAL / REOPENABLE`

本書は、外部言語から内部状態へ接続する処理を一律`adapter`または`compiler`と呼ぶことで、representation変換・language modeling・backend loweringを混同する問題を分離する。

---

# 1. 三つの作用を分ける

## A. 表現接続 Adapter

外部状態と内部状態の対応を接続する。

中心目的:

> **同じ対象・relationを別表現へ写し、後段が参照可能にする。**

例:

- encoding/decoding
- token ID mapping
- tensor packing
- schema conversion
- deterministic normalization

純粋Adapterは、対象Tについて新しい解釈relationを主要成果として生成しない。

---

## M. モデル作用 / Semantic Modeling

入力状態から、対象Tについて新しいrelation・structure・evaluationを形成する。

例:

- contextual modeling
- grammar parsing
- semantic relation inference
- masked reconstruction
- candidate scoring
- language relation extraction

この作用は、名称が`parser`や`compiler`であっても、実質がmodelingならM側である。

---

## L. Lowering / Backend Compilation

上位表現で既に確定した意味・作用を、対象計算機が直接演算できるnative state / operandへ変換する。

中心目的:

> **新しい意味を足すことではなく、既存意味を対象計算核の実行契約へ落とすこと。**

例:

- IR -> machine code
- semantic graph -> native relation tuple
- HDS full IR -> MINIDORA compute IR

---

# 2. 三者の失敗を分ける

## Adapter失敗

- state mapping破損
- representation loss
- ID/address不整合

## Model失敗

- 対象relation誤解釈
- semantic relation抽出失敗
- context/structure modeling失敗

## Lowering失敗

- target compute kernelが使わない情報を流す
- target operatorが必要な情報を落とす
- backend native operandへ閉じない
- 上位IR構造をそのまま実行面へ持ち込む

今回のMINIDORA/Compiler問題は主としてLowering失敗の可能性が高いが、Layer-0再監査によりModel境界自体も再評価する。

---

# 3. HDS Compilerの現行混線

現行HDS Compiler契約は、入力から少なくとも、

- 対象・主題
- 関係・作用・方向
- 状態・属性
- 条件・文脈
- 目的・検索焦点
- 否定
- 数量・単位
- 残差
- 意味Projection履歴

等を形成する。

これは単なる表現adapterではない。

**Language/Semantic Modeling作用を明確に持つ。**

一方、MINIDORAへ実行可能な局所閉包を渡す役割まで同じ`Compiler`概念へ抱えている。

従って現在は、

```text
Natural Language
 -> Semantic Modeling
 -> Full HDS Projection
 -> Runtime Projection / Lowering
 -> MINIDORA
```

を一つのCompiler系列として扱っている。

---

# 4. 今回の性能低下との関係

Semantic Modeling側では、

- scope
- modal
- provenance
- residual
- context
- condition

等を豊富に保持することは正しい場合がある。

しかしLowering側でtarget kernelが読まない情報までcompute operandへ混ぜると、

- 比較分母増大
- signature汚染
- irrelevant relation混入
- Kのscore空間膨張

等が起こり得る。

従って、

```text
意味豊富化
=
実行IR豊富化
```

としてはならない。

---

# 5. 新しい責任分離候補

## Language/Semantic Frontend

```text
External Language
 -> Full Semantic/HDS Projection
```

責任:

- target relation interpretation
- ambiguity/residual preservation
- scope/condition/negation等の保持
- provenance

## Compute Lowering Backend

```text
Full Semantic/HDS Projection
 -> Target-Native Compute State
```

責任:

- target kernel operator契約を読む
- 必要十分operandへ縮約
- unsupported semanticsをcompute pathから退避
- fallback pathを明示
- provenance/audit sidecarを分離

---

# 6. Loweringの基本規則候補

1. **Consumer-driven**
   - target operatorが読む情報だけをcompute operandへ入れる。

2. **Strongest-structure-first**
   - directed atomic relationが閉じるなら、同一情報のbag-of-words表現を重複得点させない。

3. **Unsupported semantics stay outside compute path**
   - scope/modal等を演算できないなら、Full IR/Auditへ保持し、compute operandへ半端に混ぜない。

4. **Fallback explicit**
   - relation構造化不能時だけweak representationへ降格する。

5. **Provenance sidecar**
   - source/confidence/audit情報を意味score operandと混ぜない。

---

# 7. Layer-0との接続

新Layer-0 T/M/Cから見ると、

- Semantic FrontendがT/M/Cのどこまでを担うか
- Core Model Artifactが何を保持するか
- LoweringがExecution Contractへどう接続するか

を独立監査する。

`Compiler`という名称だけで境界を決めない。

---

# 8. MINIDORAに対する暫定仮説

現行MINIDORAでは、

- `言語基底P`
- HDS Compiler frontend
- HDS language relation projection

がLanguage/Semantic Modeling側へ寄っている。

K3相当能力核/K/Jはsemantic/world/task relation計算へ寄っている。

`hds_runtime_projection.py`等がLoweringを担っているが、今回の観測ではtarget-native計算契約まで十分細く閉じていない可能性がある。

この仮説を、Layer-0 v5確定後のMINIDORA再監査で検証する。

---

# 9. 現時点の判定

- Adapter / Model / Lowering分離: **必須**
- HDS Compiler全体をpure adapter扱い: **誤り**
- HDS Compiler全体をmodel identity扱い: **未確定**
- Full HDS-IRとCompute IRを同じrichnessで扱う: **誤り方向**
- Semantic FrontendとCompute Backendの分離: **強く支持**
- Consumer-driven lowering: **強く支持**

この境界をLayer-0 v5と後続MINIDORA/HDS Compiler再設計へ帰還させる。
