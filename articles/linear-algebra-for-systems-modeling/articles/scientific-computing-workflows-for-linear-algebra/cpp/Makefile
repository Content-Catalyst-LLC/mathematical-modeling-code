.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 scientific_computing_linear_algebra_audit.cpp -o scientific_computing_linear_algebra_audit_cpp && ./scientific_computing_linear_algebra_audit_cpp > ../outputs/tables/cpp_scientific_computing_linear_algebra_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f scientific_computing_linear_algebra_audit_cpp
