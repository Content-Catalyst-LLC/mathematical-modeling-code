.PHONY: smoke advanced definite-integrals fundamental-theorem clean

smoke: definite-integrals fundamental-theorem

advanced:
	@for d in articles/*; do \
		if [ -d "$$d/advanced" ]; then \
			echo "Running advanced checks in $$d"; \
			$(MAKE) -C "$$d/advanced" smoke || true; \
		fi; \
	done

definite-integrals:
	$(MAKE) -C articles/definite-integrals-and-total-change smoke

fundamental-theorem:
	$(MAKE) -C articles/the-fundamental-theorem-of-calculus smoke

clean:
	@for d in articles/*; do \
		if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" clean || true; fi; \
		if [ -f "$$d/advanced/Makefile" ]; then $(MAKE) -C "$$d/advanced" clean || true; fi; \
	done
