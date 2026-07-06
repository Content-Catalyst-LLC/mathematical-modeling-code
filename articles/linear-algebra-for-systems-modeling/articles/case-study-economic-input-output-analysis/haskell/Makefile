.PHONY: run clean

run:
	@if command -v runghc >/dev/null 2>&1; then runghc Main.hs > ../outputs/tables/haskell_economic_input_output_audit.txt; elif command -v ghc >/dev/null 2>&1; then ghc Main.hs -o economic_input_output_audit_hs >/dev/null && ./economic_input_output_audit_hs > ../outputs/tables/haskell_economic_input_output_audit.txt; else echo "ghc/runghc not found; skipping Haskell."; fi

clean:
	rm -f economic_input_output_audit_hs Main.hi Main.o
