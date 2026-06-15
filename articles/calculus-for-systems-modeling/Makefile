.PHONY: smoke advanced improper-integrals flow-to-stock clean

smoke: improper-integrals flow-to-stock

advanced:
	@for d in articles/*; do \
		if [ -d "$$d/advanced" ]; then \
			echo "Running advanced checks in $$d"; \
			$(MAKE) -C "$$d/advanced" smoke || true; \
		fi; \
	done

improper-integrals:
	$(MAKE) -C articles/improper-integrals-and-unbounded-quantities smoke

flow-to-stock:
	$(MAKE) -C articles/accumulation-exposure-and-flow-to-stock-reasoning smoke

clean:
	@for d in articles/*; do \
		if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" clean || true; fi; \
		if [ -f "$$d/advanced/Makefile" ]; then $(MAKE) -C "$$d/advanced" clean || true; fi; \
	done
