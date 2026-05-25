
## Optional README addition

### Recomposition demo

Layer-0 is not only a boundary theorem for LLM status. It can also be used as a decomposition basis for adjacent architectures.

This repository includes a deterministic non-LLM demo showing how Layer-0-style reading, summarization, context-conditioning, and emission roles can be recomposed into a memory subsystem:

```bash
python3 -S demos/layer0_memory_recomposition_demo.py --outdir artifacts/layer0_memory_demo
```

The demo emits a JSON certificate and Markdown report. It does not call a remote LLM and does not claim to be an LLM. Its purpose is to demonstrate the architectural recomposition space opened by the Layer-0 functional decomposition.
