.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then mkdir -p ../outputs/tables; runhaskell Main.hs > ../outputs/tables/haskell_urban_mobility_records.txt; cat ../outputs/tables/haskell_urban_mobility_records.txt; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && mkdir -p ../outputs/tables && ./urban-mobility-records > ../outputs/tables/haskell_urban_mobility_records.txt && cat ../outputs/tables/haskell_urban_mobility_records.txt; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o urban-mobility-records

clean:
	rm -f urban-mobility-records *.hi *.o
