.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 high_dimensional_simulation_audit.cpp -o high_dimensional_simulation_audit_cpp && ./high_dimensional_simulation_audit_cpp > ../outputs/tables/cpp_high_dimensional_simulation_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f high_dimensional_simulation_audit_cpp
