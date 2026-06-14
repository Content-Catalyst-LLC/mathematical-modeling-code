.PHONY: smoke what-is functions-variables domains-ranges infinity-infinitesimals clean

smoke: what-is functions-variables domains-ranges infinity-infinitesimals

what-is:
	@if [ -d articles/what-is-calculus-for-systems-modeling ]; then $(MAKE) -C articles/what-is-calculus-for-systems-modeling smoke; else echo "Skipping missing article folder: what-is-calculus-for-systems-modeling"; fi

functions-variables:
	@if [ -d articles/functions-variables-and-mathematical-representation ]; then $(MAKE) -C articles/functions-variables-and-mathematical-representation smoke; else echo "Skipping missing article folder: functions-variables-and-mathematical-representation"; fi

domains-ranges:
	@if [ -d articles/domains-ranges-and-the-structure-of-functional-models ]; then $(MAKE) -C articles/domains-ranges-and-the-structure-of-functional-models smoke; else echo "Skipping missing article folder: domains-ranges-and-the-structure-of-functional-models"; fi

infinity-infinitesimals:
	$(MAKE) -C articles/infinity-infinitesimals-and-the-historical-problem-of-change smoke

clean:
	@if [ -d articles/what-is-calculus-for-systems-modeling ]; then $(MAKE) -C articles/what-is-calculus-for-systems-modeling clean || true; fi
	@if [ -d articles/functions-variables-and-mathematical-representation ]; then $(MAKE) -C articles/functions-variables-and-mathematical-representation clean || true; fi
	@if [ -d articles/domains-ranges-and-the-structure-of-functional-models ]; then $(MAKE) -C articles/domains-ranges-and-the-structure-of-functional-models clean || true; fi
	$(MAKE) -C articles/infinity-infinitesimals-and-the-historical-problem-of-change clean || true
