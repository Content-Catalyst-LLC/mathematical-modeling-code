.PHONY: smoke advanced second-derivatives elasticity clean

smoke: second-derivatives elasticity

advanced:
	@for d in articles/*; do \
		if [ -d "$$d/advanced" ]; then \
			echo "Running advanced checks in $$d"; \
			$(MAKE) -C "$$d/advanced" smoke || true; \
		fi; \
	done

second-derivatives:
	$(MAKE) -C articles/second-derivatives-curvature-and-acceleration smoke

elasticity:
	$(MAKE) -C articles/elasticity-sensitivity-and-marginal-response smoke

clean:
	@for d in articles/*; do \
		if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" clean || true; fi; \
		if [ -f "$$d/advanced/Makefile" ]; then $(MAKE) -C "$$d/advanced" clean || true; fi; \
	done
