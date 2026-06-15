.PHONY: smoke advanced substitution integration-by-parts clean

smoke: substitution integration-by-parts

advanced:
	@for d in articles/*; do \
		if [ -d "$$d/advanced" ]; then \
			echo "Running advanced checks in $$d"; \
			$(MAKE) -C "$$d/advanced" smoke || true; \
		fi; \
	done

substitution:
	$(MAKE) -C articles/substitution-and-transformations-of-accumulation smoke

integration-by-parts:
	$(MAKE) -C articles/integration-by-parts-and-structured-decomposition smoke

clean:
	@for d in articles/*; do \
		if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" clean || true; fi; \
		if [ -f "$$d/advanced/Makefile" ]; then $(MAKE) -C "$$d/advanced" clean || true; fi; \
	done
