# 主張層 — v4

candidate-localの合否と、複数architectureへ一般化する主張を分離する。

| 層 | 主張 | 現在状態 |
|---|---|---|
| L0-A | 個別候補がFunctional Coreを満たす | **実行可能 / current** |
| L0-B | 同一・近縁familyで機能責任が再現する | **観測集合で支持** |
| L0-C | 異種architecture family間で機能責任が再現する | **5モデル系統で支持** |
| L0-D | 観測scopeに限定して原理候補となる | `PRINCIPLE_CANDIDATE / REOPEN_REQUIRED` |
| L0-E | 未観測familyへ転移候補となる | OPEN |

## L0-Cの意味

L0-Cは「異種familyで同じ機構名が再現する」という主張ではない。

今回観測されたのはむしろ次である。

```text
異なる機構
  ↓
同じ上位機能責任へ写像可能
```

例:

- standard attention と KDA / Gated MLA
- Dense FFN と MoE
- KV cache と recurrent state
- text-only input と multimodal input

したがって、L0-Cで追跡する対象は**機構の同一性ではなく機能責任の再現性**である。

普遍・最終・唯一最小への自動昇格は禁止する。
