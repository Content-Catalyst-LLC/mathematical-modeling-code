.PHONY: smoke calculators advanced clean list

list:
	@echo "Nested planned article folders:"
	@find articles -mindepth 1 -maxdepth 1 -type d | sort

smoke:
	@for d in articles/*; do if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" smoke || true; fi; done

calculators:
	@for d in articles/*; do if [ -f "$$d/calculators/run_calculator_smoke_tests.sh" ]; then (cd "$$d/calculators" && bash run_calculator_smoke_tests.sh) || true; fi; done

advanced:
	@for d in articles/*; do if [ -f "$$d/advanced/Makefile" ]; then $(MAKE) -C "$$d/advanced" smoke || true; fi; done

clean:
	@for d in articles/*; do if [ -f "$$d/Makefile" ]; then $(MAKE) -C "$$d" clean || true; fi; done
