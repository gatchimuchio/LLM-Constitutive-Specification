# 大規模言語模型成立規定

> 状態: 局所安定正本 / 再開放可  
> 版: 2026-08-28-成立規定-7

## v7の中核

v6の `条件付き言語重み関係` をさらに独立監査し、**arbitrary scoreとlanguage modelを分け切れていない**と判定しました。

現行の厳密LM中核は次です。

```text
完全言語状態空間
+ 持続模型状態
→ 一つの整合した言語確率法則
```

local conditional / autoregressive factorization / diffusion / energy等は、このglobal lawを誘導する成立形として扱います。

## v6からの主要修正

- arbitrary score / ordinal weightingを厳密LM中核から外した。
- energy LMはglobal normalization / normalizabilityを要求する。
- arbitrary weighted grammarとprobabilistic grammarを分離した。
- variable-length LMではEOS / termination / length lawを監査する。
- deterministic transducerのdelta distributionは数学的には成立し得るため、「delta禁止」ではなく**分類証拠として不十分**へ修正した。
- 条件付きLM / transducer / MLM / scorer / representation modelを隣接カテゴリとして分離した。
- source code / design文書だけを因果証拠としない。

## 境界

```text
言語模型物 != 言語模型実行系 != 利用系
厳密LM != 局所予測 != scorer != representation != transducer
```

## MINIDORA

GPQAは能力監査です。MINIDORAのLM性は、参照NNの構造コピーではなく、完全言語状態上の整合したLM法則をどの方式で成立させるかを先に監査します。

## 監査

```bash
python scripts/規定監査.py
python -m unittest discover -s tests -p 'test_*.py'
```
