## README追記案（日本語）

### 再合成デモ

Layer-0は、LLM該当性を判定するための境界定理であるだけではない。  
隣接する非LLMアーキテクチャを設計するための分解基盤としても利用できる。

本リポジトリには、Layer-0的な読込・要約・文脈条件づけ・出力の役割を再合成し、メモリサブシステムを構成する決定論的な非LLMデモを含めることができる。

```bash
python3 -S demos/layer0_memory_recomposition_demo.py --outdir artifacts/layer0_memory_demo
```

このデモはJSON証明書とMarkdownレポートを出力する。  
リモートLLMは呼び出さず、このシステム自体がLLMであるとも主張しない。  
目的は、Layer-0機能分解によって開かれるアーキテクチャ再合成空間を示すことである。
