.PHONY: smoke advanced flow-to-stock convergence clean

smoke: flow-to-stock convergence

advanced:
	@for d in articles/*; do \
		if [ -d "$$d/advanced" ]; then \
			echo "Running advanced checks in $$d"; \
			$(MAKE) -C "$$d/advanced" smoke || true; \
		fi; \
	done

flow-to-stock:
	$(MAKE) -C articles/accumulation-exposure-and-flow-to-stock-reasoning smoke

convergence:
	$(MAKE) -C articles/sequences-series-and-the-logic-of-convergence smoke

clean:
	@for d in articles/*; do \
		if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" clean || true; fi; \
		if [ -f "$$d/advanced/Makefile" ]; then $(MAKE) -C "$$d/advanced" clean || true; fi; \
	done
