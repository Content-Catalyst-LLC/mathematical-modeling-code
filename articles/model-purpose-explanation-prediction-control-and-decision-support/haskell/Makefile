.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then \
		runhaskell Main.hs; \
	elif command -v ghc >/dev/null 2>&1; then \
		$(MAKE) build && ./model-purpose-haskell; \
	else \
		echo "Haskell toolchain not found; skipping."; \
	fi

build:
	ghc -O2 Main.hs -o model-purpose-haskell

clean:
	rm -f model-purpose-haskell *.hi *.o
