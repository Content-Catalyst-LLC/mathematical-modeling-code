.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then mkdir -p ../outputs/tables; runhaskell Main.hs > ../outputs/tables/haskell_carbon_pathway_records.txt; cat ../outputs/tables/haskell_carbon_pathway_records.txt; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && mkdir -p ../outputs/tables && ./carbon-pathway-records > ../outputs/tables/haskell_carbon_pathway_records.txt && cat ../outputs/tables/haskell_carbon_pathway_records.txt; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o carbon-pathway-records

clean:
	rm -f carbon-pathway-records *.hi *.o
