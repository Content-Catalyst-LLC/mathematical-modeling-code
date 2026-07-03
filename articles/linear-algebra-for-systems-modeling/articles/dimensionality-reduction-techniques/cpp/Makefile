.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 dimensionality_reduction_audit.cpp -o dimensionality_reduction_audit_cpp && ./dimensionality_reduction_audit_cpp > ../outputs/tables/cpp_dimensionality_reduction_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f dimensionality_reduction_audit_cpp
