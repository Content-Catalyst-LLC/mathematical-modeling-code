.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 scaling_units_nondimensionalization.cpp -o scaling_units_nondimensionalization; mkdir -p ../outputs/tables; ./scaling_units_nondimensionalization > ../outputs/tables/cpp_scaling_unit_records.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f scaling_units_nondimensionalization
