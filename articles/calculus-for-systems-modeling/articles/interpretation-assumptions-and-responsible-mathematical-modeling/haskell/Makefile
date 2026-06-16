.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then mkdir -p ../outputs/tables; runhaskell Main.hs > ../outputs/tables/haskell_responsible_modeling_records.txt; cat ../outputs/tables/haskell_responsible_modeling_records.txt; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && mkdir -p ../outputs/tables && ./responsible-modeling-records > ../outputs/tables/haskell_responsible_modeling_records.txt && cat ../outputs/tables/haskell_responsible_modeling_records.txt; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o responsible-modeling-records

clean:
	rm -f responsible-modeling-records *.hi *.o
