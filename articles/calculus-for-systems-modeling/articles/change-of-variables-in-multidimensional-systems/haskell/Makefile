.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then runhaskell Main.hs; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && ./change-of-variables-haskell; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o change-of-variables-haskell

clean:
	rm -f change-of-variables-haskell *.hi *.o
