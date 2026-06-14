.PHONY: smoke first-article functions-variables clean

smoke: first-article functions-variables

first-article:
	$(MAKE) -C articles/what-is-calculus-for-systems-modeling smoke

functions-variables:
	$(MAKE) -C articles/functions-variables-and-mathematical-representation smoke

clean:
	$(MAKE) -C articles/what-is-calculus-for-systems-modeling clean || true
	$(MAKE) -C articles/functions-variables-and-mathematical-representation clean || true
