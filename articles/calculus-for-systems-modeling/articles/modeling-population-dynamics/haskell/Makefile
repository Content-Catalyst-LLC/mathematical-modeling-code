.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then mkdir -p ../outputs/tables; runhaskell Main.hs > ../outputs/tables/haskell_population_dynamics_records.txt; cat ../outputs/tables/haskell_population_dynamics_records.txt; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && mkdir -p ../outputs/tables && ./population-dynamics-records > ../outputs/tables/haskell_population_dynamics_records.txt && cat ../outputs/tables/haskell_population_dynamics_records.txt; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o population-dynamics-records

clean:
	rm -f population-dynamics-records *.hi *.o
