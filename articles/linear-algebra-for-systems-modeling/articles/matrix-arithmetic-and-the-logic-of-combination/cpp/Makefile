.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 matrix_arithmetic_audit.cpp -o matrix_arithmetic_audit_cpp && ./matrix_arithmetic_audit_cpp > ../outputs/tables/cpp_matrix_arithmetic_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f matrix_arithmetic_audit_cpp
