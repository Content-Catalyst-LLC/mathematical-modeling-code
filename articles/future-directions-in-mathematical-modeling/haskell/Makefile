.PHONY: run build clean
run:
	@if command -v runhaskell >/dev/null 2>&1; then runhaskell Main.hs; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && ./future-direction-records-haskell; else echo "Haskell toolchain not found; skipping."; fi
build:
	ghc -O2 Main.hs -o future-direction-records-haskell
clean:
	rm -f future-direction-records-haskell *.hi *.o
