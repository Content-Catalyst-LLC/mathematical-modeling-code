.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 sparse_matrix_efficiency_audit.cpp -o sparse_matrix_efficiency_audit_cpp && ./sparse_matrix_efficiency_audit_cpp > ../outputs/tables/cpp_sparse_matrix_efficiency_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f sparse_matrix_efficiency_audit_cpp
