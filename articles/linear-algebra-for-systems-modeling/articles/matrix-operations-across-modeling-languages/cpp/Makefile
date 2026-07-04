.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 cross_language_matrix_audit.cpp -o cross_language_matrix_audit_cpp && ./cross_language_matrix_audit_cpp > ../outputs/tables/cpp_cross_language_matrix_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f cross_language_matrix_audit_cpp
