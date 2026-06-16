.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then mkdir -p ../outputs/tables; runhaskell Main.hs > ../outputs/tables/haskell_continuous_model_risk_records.txt; cat ../outputs/tables/haskell_continuous_model_risk_records.txt; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && mkdir -p ../outputs/tables && ./continuous-risk-records > ../outputs/tables/haskell_continuous_model_risk_records.txt && cat ../outputs/tables/haskell_continuous_model_risk_records.txt; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o continuous-risk-records

clean:
	rm -f continuous-risk-records *.hi *.o
