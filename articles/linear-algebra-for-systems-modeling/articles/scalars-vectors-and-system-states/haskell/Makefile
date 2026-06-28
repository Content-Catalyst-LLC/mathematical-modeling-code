.PHONY: run clean

run:
	@if command -v ghc >/dev/null 2>&1; then ghc -O2 Main.hs -o state_vector_audit_haskell >/dev/null && ./state_vector_audit_haskell > ../outputs/tables/haskell_state_vector_audit.txt; else echo "ghc not found; skipping Haskell."; fi

clean:
	rm -f Main.hi Main.o state_vector_audit_haskell
