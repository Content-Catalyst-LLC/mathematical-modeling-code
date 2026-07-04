.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 large_scale_matrix_computation_audit.cpp -o large_scale_matrix_computation_audit_cpp && ./large_scale_matrix_computation_audit_cpp > ../outputs/tables/cpp_large_scale_matrix_computation_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f large_scale_matrix_computation_audit_cpp
