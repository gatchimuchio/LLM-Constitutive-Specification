# 機能責任の粒度 — v4

v4の5項目は**暫定責任語彙**であり、5つの物理componentが必要だという主張ではない。

```text
責任数 != 機構数
```

- 一機構が複数責任を満たしてよい。
- 複数機構が一責任を共同で満たしてよい。
- merge / splitは機能差と観測証拠で評価する。
- exact minimumはOPEN。

## 2026-08-21 横断突合による粒度監査

Llama 3、K2-V2、OLMo 3、Apertus 1.5、Kimi K3を突合すると、局所作用として少なくとも次が反復して見える。

1. 外部記号の住所化
2. 履歴・系列状態の保持
3. 参照関係の形成
4. 状態変換
5. 差分・参照結果の統合帰還
6. 候補の表出
7. 選択・反復

しかし、現時点ではこれらを7個の独立必須責任へ分割する根拠は不足する。

| 局所作用 | 現行責任への写像 |
|---|---|
| 外部記号の住所化 | `LINGUISTIC_ADDRESSABILITY` |
| 履歴・系列状態の保持 | `CONTEXT_BOUND_STATE` |
| 参照関係の形成 | `TRANSFORMATION_OR_COMPOSITION_CORE` |
| 状態変換 | `TRANSFORMATION_OR_COMPOSITION_CORE` |
| 統合帰還 | `TRANSFORMATION_OR_COMPOSITION_CORE` / `CONTEXT_DEPENDENT_RESULT_FORMATION` |
| 候補の表出 | `CONTEXT_DEPENDENT_RESULT_FORMATION` |
| 選択・反復 | `CONTEXT_DEPENDENT_RESULT_FORMATION` / `RESULT_SURFACE` |

したがって今回の証拠は、責任数を増やすより、**5責任が異種機構を吸収できる抽象粒度にある**ことを支持する。

同時に、5が最終最小であることは確定しない。将来、責任間の恒常的な統合または新しい独立責任が観測された場合は再開放する。

v3の「責任境界が別ならcomponentも別でなければならない」という扱いは現行仕様では採用しない。
