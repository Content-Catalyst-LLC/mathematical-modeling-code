.PHONY: smoke advanced integration-by-parts improper-integrals clean

smoke: integration-by-parts improper-integrals

advanced:
	@for d in articles/*; do \
		if [ -d "$$d/advanced" ]; then \
			echo "Running advanced checks in $$d"; \
			$(MAKE) -C "$$d/advanced" smoke || true; \
		fi; \
	done

integration-by-parts:
	$(MAKE) -C articles/integration-by-parts-and-structured-decomposition smoke

improper-integrals:
	$(MAKE) -C articles/improper-integrals-and-unbounded-quantities smoke

clean:
	@for d in articles/*; do \
		if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" clean || true; fi; \
		if [ -f "$$d/advanced/Makefile" ]; then $(MAKE) -C "$$d/advanced" clean || true; fi; \
	done
