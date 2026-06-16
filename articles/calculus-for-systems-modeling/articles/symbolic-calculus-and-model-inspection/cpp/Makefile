.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 symbolic_model_inspection.cpp -o symbolic_model_inspection; mkdir -p ../outputs/tables; ./symbolic_model_inspection > ../outputs/tables/cpp_symbolic_model_inspection.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f symbolic_model_inspection
