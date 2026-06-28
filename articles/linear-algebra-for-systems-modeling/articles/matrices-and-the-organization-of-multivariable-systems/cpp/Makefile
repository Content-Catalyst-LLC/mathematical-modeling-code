.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 matrix_structure_audit.cpp -o matrix_structure_audit_cpp && ./matrix_structure_audit_cpp > ../outputs/tables/cpp_matrix_structure_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f matrix_structure_audit_cpp
