.PHONY: smoke advanced inverse clean

smoke: inverse

advanced:
	@for d in articles/*; do \
		if [ -d "$$d/advanced" ]; then \
			echo "Running advanced checks in $$d"; \
			$(MAKE) -C "$$d/advanced" smoke || true; \
		fi; \
	done

inverse:
	$(MAKE) -C articles/inverse-functions-and-system-interpretation smoke

clean:
	@for d in articles/*; do \
		if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" clean || true; fi; \
		if [ -f "$$d/advanced/Makefile" ]; then $(MAKE) -C "$$d/advanced" clean || true; fi; \
	done
