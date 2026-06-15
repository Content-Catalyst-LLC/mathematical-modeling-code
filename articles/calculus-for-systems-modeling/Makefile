.PHONY: smoke advanced sequences convergence-tests clean

smoke: sequences convergence-tests

advanced:
	@for d in articles/*; do \
		if [ -d "$$d/advanced" ]; then \
			echo "Running advanced checks in $$d"; \
			$(MAKE) -C "$$d/advanced" smoke || true; \
		fi; \
	done

sequences:
	$(MAKE) -C articles/sequences-series-and-the-logic-of-convergence smoke

convergence-tests:
	$(MAKE) -C articles/convergence-tests-and-the-discipline-of-infinite-approximation smoke

clean:
	@for d in articles/*; do \
		if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" clean || true; fi; \
		if [ -f "$$d/advanced/Makefile" ]; then $(MAKE) -C "$$d/advanced" clean || true; fi; \
	done
