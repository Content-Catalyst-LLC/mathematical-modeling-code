.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 optimization_matrix_audit.cpp -o optimization_matrix_audit_cpp && ./optimization_matrix_audit_cpp > ../outputs/tables/cpp_optimization_matrix_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f optimization_matrix_audit_cpp
