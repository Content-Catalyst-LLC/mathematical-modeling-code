.PHONY: run clean

run:
	@if command -v ghc >/dev/null 2>&1; then ghc -O2 Main.hs -o linear_algebra_audit_haskell >/dev/null && ./linear_algebra_audit_haskell > ../outputs/tables/haskell_linear_algebra_audit.txt; else echo "ghc not found; skipping Haskell."; fi

clean:
	rm -f Main.hi Main.o linear_algebra_audit_haskell
