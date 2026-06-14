.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then \
		runhaskell Main.hs; \
	elif command -v ghc >/dev/null 2>&1; then \
		$(MAKE) build && ./public-health-model-records-haskell; \
	else \
		echo "Haskell toolchain not found; skipping."; \
	fi

build:
	ghc -O2 Main.hs -o public-health-model-records-haskell

clean:
	rm -f public-health-model-records-haskell *.hi *.o
