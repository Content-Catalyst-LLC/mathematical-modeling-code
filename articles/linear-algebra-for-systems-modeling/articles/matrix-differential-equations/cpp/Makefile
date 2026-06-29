.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 matrix_differential_equation_audit.cpp -o matrix_differential_equation_audit_cpp && ./matrix_differential_equation_audit_cpp > ../outputs/tables/cpp_matrix_differential_equation_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f matrix_differential_equation_audit_cpp
