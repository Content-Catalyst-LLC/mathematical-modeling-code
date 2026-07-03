.PHONY: run clean

run:
	@if command -v runghc >/dev/null 2>&1; then runghc Main.hs > ../outputs/tables/haskell_graph_theory_foundations_audit.txt; elif command -v ghc >/dev/null 2>&1; then ghc Main.hs -o graph_theory_foundations_audit_hs >/dev/null && ./graph_theory_foundations_audit_hs > ../outputs/tables/haskell_graph_theory_foundations_audit.txt; else echo "ghc/runghc not found; skipping Haskell."; fi

clean:
	rm -f graph_theory_foundations_audit_hs Main.hi Main.o
