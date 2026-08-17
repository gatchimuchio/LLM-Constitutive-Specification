.PHONY: help audit test verify test-all update-golden legacy-v3-audit memory-recomposition-demo

PYTHON ?= python3
PYFLAGS ?= -S
V4_SCRIPT := layer0_functional_conformance_v4.py
STRICT_MANIFEST := REPOSITORY_GIT_BLOB_MANIFEST.txt

help:
	@echo "Targets:"
	@echo "  make audit          - run v4 built-in conformance self-test"
	@echo "  make test           - run v4 unittest suite"
	@echo "  make verify         - verify strict tracked inventory/content manifest"
	@echo "  make test-all       - audit + test + verify; never updates golden state"
	@echo "  make update-golden CONFIRM=1 - explicitly rewrite strict manifest"
	@echo "  make legacy-v3-audit - regenerate v3 artifacts into /tmp only"
	@echo "  make memory-recomposition-demo - run retained recomposition demo"

audit:
	$(PYTHON) $(PYFLAGS) $(V4_SCRIPT) --self-test

test:
	$(PYTHON) -m unittest -v tests/test_layer0_v4.py

verify:
	$(PYTHON) $(PYFLAGS) scripts/strict_manifest.py verify --manifest $(STRICT_MANIFEST)

test-all: audit test verify

update-golden:
	@test "$(CONFIRM)" = "1" || (echo "ERROR: set CONFIRM=1 to rewrite golden manifest" && exit 2)
	$(PYTHON) $(PYFLAGS) scripts/strict_manifest.py generate --manifest $(STRICT_MANIFEST) --confirm

legacy-v3-audit:
	rm -rf /tmp/layer0-v3-artifacts
	$(PYTHON) $(PYFLAGS) llm_minimal_architecture_groups_v3_0.py --outdir /tmp/layer0-v3-artifacts

memory-recomposition-demo:
	$(PYTHON) $(PYFLAGS) layer0_recomposition_memory_demo_bilingual_bundle/demos/layer0_memory_recomposition_demo.py --outdir /tmp/layer0-memory-demo
