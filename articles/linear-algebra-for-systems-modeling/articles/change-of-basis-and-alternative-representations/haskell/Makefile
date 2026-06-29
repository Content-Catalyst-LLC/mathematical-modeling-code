.PHONY: run clean

run:
	@if command -v runghc >/dev/null 2>&1; then runghc Main.hs > ../outputs/tables/haskell_change_of_basis_audit.txt; elif command -v ghc >/dev/null 2>&1; then ghc Main.hs -o change_of_basis_audit_hs >/dev/null && ./change_of_basis_audit_hs > ../outputs/tables/haskell_change_of_basis_audit.txt; else echo "ghc/runghc not found; skipping Haskell."; fi

clean:
	rm -f change_of_basis_audit_hs Main.hi Main.o
