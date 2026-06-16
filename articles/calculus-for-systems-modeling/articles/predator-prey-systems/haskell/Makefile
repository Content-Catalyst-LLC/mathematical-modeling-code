.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then mkdir -p ../outputs/tables; runhaskell Main.hs > ../outputs/tables/haskell_predator_prey_records.txt; cat ../outputs/tables/haskell_predator_prey_records.txt; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && mkdir -p ../outputs/tables && ./predator-prey-records > ../outputs/tables/haskell_predator_prey_records.txt && cat ../outputs/tables/haskell_predator_prey_records.txt; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o predator-prey-records

clean:
	rm -f predator-prey-records *.hi *.o
