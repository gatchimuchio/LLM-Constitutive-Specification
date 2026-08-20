# 適用範囲と論証境界 — v4

## 定義域

v4は「通常技術用語としてLLMと呼ばれる全システム」を先に固定しない。対象は、明示された`system_boundary`を持つ**candidate system**である。

## 現行命題

候補がv4 Functional Coreへ適合すると主張する場合、その候補について5責任・execution trace・negative controlsを検査できなければならない。

これはL0-Aのcandidate-local conformance命題である。

## 横断命題

2026-08-21時点では、次の5モデル系統の公開観測を別途突合した。

- Llama 3
- LLM360 K2-V2
- OLMo 3
- Apertus 1.5
- Kimi K3

異なるarchitecture / state handling / FFN / modality構成を跨いでも現行5責任へ写像できたため、観測集合についてL0-Cを支持する。

ただしこの帰納的横断証拠は、世界中のLLMに対する普遍定理ではない。

## 独立性の留保

4つの日本語構文化資料は、K3で用いた「教師固定→HDS意味分別→残差保持」という同系統の分析手順を共有する。

したがって、**記述形式が似たこと自体**を独立証拠として数えない。

証拠価値を置くのは、実物側に存在する異なる機構・形成経路・媒体境界を同じ基準で観測しても、上位責任への写像が維持された点である。

## 反証

- candidate-localでは、必須責任またはnegative controlの失敗を`FAIL`とする。
- 証拠不足は`SUSPEND`とする。
- cross-family claimでは、責任語彙へ写像不能な反例、または責任欠落でも同等機能が成立する反例が出た場合にL0-C / L0-Dを再開放する。
