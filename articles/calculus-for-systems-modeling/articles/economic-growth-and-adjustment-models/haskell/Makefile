.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then mkdir -p ../outputs/tables; runhaskell Main.hs > ../outputs/tables/haskell_economic_growth_records.txt; cat ../outputs/tables/haskell_economic_growth_records.txt; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && mkdir -p ../outputs/tables && ./economic-growth-records > ../outputs/tables/haskell_economic_growth_records.txt && cat ../outputs/tables/haskell_economic_growth_records.txt; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o economic-growth-records

clean:
	rm -f economic-growth-records *.hi *.o
