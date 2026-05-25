
# Optional Makefile additions

.PHONY: memory-recomposition-demo

memory-recomposition-demo:
	$(PYTHON) $(PYFLAGS) demos/layer0_memory_recomposition_demo.py --outdir $(OUTDIR)/layer0_memory_demo
