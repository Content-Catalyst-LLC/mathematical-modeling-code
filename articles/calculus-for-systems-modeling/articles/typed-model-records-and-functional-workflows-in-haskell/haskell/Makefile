.PHONY: run build clean

run:
	@if command -v runhaskell >/dev/null 2>&1; then mkdir -p ../outputs/tables; runhaskell Main.hs > ../outputs/tables/haskell_typed_model_output.txt; cat ../outputs/tables/haskell_typed_model_output.txt; elif command -v ghc >/dev/null 2>&1; then $(MAKE) build && mkdir -p ../outputs/tables && ./typed-model-records > ../outputs/tables/haskell_typed_model_output.txt && cat ../outputs/tables/haskell_typed_model_output.txt; else echo "Haskell toolchain not found; skipping."; fi

build:
	ghc -O2 Main.hs -o typed-model-records

clean:
	rm -f typed-model-records *.hi *.o
