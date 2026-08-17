# Functional Responsibility Granularity — v4

v4の5項目は**暫定責任語彙**であり、5つの物理componentが必要だという主張ではない。

```text
responsibility count != mechanism count
```

- 一機構が複数責任を満たしてよい。
- 複数機構が一責任を共同で満たしてよい。
- merge/splitは機能同値性と観測証拠で評価する。
- exact minimumはOPEN。

v3の「責任境界が別ならcomponentも別でなければならない」という扱いは現行仕様では採用しない。
