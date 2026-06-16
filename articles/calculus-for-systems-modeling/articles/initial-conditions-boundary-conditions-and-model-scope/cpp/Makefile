.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 initial_conditions_boundary_scope.cpp -o initial_conditions_boundary_scope; mkdir -p ../outputs/tables; ./initial_conditions_boundary_scope > ../outputs/tables/cpp_condition_scope_records.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f initial_conditions_boundary_scope
