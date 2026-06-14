.PHONY: smoke what-is functions-variables domains-ranges clean

smoke: what-is functions-variables domains-ranges

what-is:
	@if [ -d articles/what-is-calculus-for-systems-modeling ]; then $(MAKE) -C articles/what-is-calculus-for-systems-modeling smoke; else echo "Skipping missing what-is folder"; fi

functions-variables:
	@if [ -d articles/functions-variables-and-mathematical-representation ]; then $(MAKE) -C articles/functions-variables-and-mathematical-representation smoke; else echo "Skipping missing functions-variables folder"; fi

domains-ranges:
	$(MAKE) -C articles/domains-ranges-and-the-structure-of-functional-models smoke

clean:
	@if [ -d articles/what-is-calculus-for-systems-modeling ]; then $(MAKE) -C articles/what-is-calculus-for-systems-modeling clean || true; fi
	@if [ -d articles/functions-variables-and-mathematical-representation ]; then $(MAKE) -C articles/functions-variables-and-mathematical-representation clean || true; fi
	$(MAKE) -C articles/domains-ranges-and-the-structure-of-functional-models clean || true
