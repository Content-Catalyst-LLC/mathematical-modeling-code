.PHONY: run clean

run:
	@if command -v runghc >/dev/null 2>&1; then runghc Main.hs > ../outputs/tables/haskell_sparse_matrix_efficiency_audit.txt; elif command -v ghc >/dev/null 2>&1; then ghc Main.hs -o sparse_matrix_efficiency_audit_hs >/dev/null && ./sparse_matrix_efficiency_audit_hs > ../outputs/tables/haskell_sparse_matrix_efficiency_audit.txt; else echo "ghc/runghc not found; skipping Haskell."; fi

clean:
	rm -f sparse_matrix_efficiency_audit_hs Main.hi Main.o
