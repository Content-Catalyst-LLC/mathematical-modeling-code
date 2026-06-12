.PHONY: run build clean
run:
	@if command -v runhaskell >/dev/null 2>&1; then runhaskell Main.hs; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && ./variables-parameters-constraints-haskell; else echo "Haskell toolchain not found; skipping."; fi
build:
	ghc -O2 Main.hs -o variables-parameters-constraints-haskell
clean:
	rm -f variables-parameters-constraints-haskell *.hi *.o
