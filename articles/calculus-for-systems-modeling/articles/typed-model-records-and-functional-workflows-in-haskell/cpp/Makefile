.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 typed_model_records_haskell.cpp -o typed_model_records_haskell; mkdir -p ../outputs/tables; ./typed_model_records_haskell > ../outputs/tables/cpp_typed_model_output.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f typed_model_records_haskell
