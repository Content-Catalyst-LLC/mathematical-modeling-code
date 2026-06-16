.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then mkdir -p ../outputs/tables; runhaskell Main.hs > ../outputs/tables/haskell_condition_scope_records.txt; cat ../outputs/tables/haskell_condition_scope_records.txt; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && mkdir -p ../outputs/tables && ./condition-scope-records > ../outputs/tables/haskell_condition_scope_records.txt && cat ../outputs/tables/haskell_condition_scope_records.txt; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o condition-scope-records

clean:
	rm -f condition-scope-records *.hi *.o
