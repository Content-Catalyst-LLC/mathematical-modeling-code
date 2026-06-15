.PHONY: run build clean
run:
	@if command -v runhaskell >/dev/null 2>&1; then runhaskell Main.hs; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && ./separable-haskell; else echo "Haskell toolchain not found; skipping."; fi
build:
	ghc -O2 Main.hs -o separable-haskell
clean:
	rm -f separable-haskell *.hi *.o
