# Scope and Argument — v4

## 定義域

v4は「通常技術用語としてLLMと呼ばれる全システム」を先に固定しない。対象は、明示された`system_boundary`を持つ**candidate system**である。

## 現行命題

候補がv4 Functional Coreへ適合すると主張する場合、その候補について5責任・execution trace・negative controlsを検査できなければならない。

これはcandidate-local conformance命題であり、世界中のLLMに対する普遍定理ではない。

## 反証

必須責任またはnegative controlの失敗は`FAIL`。証拠不足は`SUSPEND`。
