.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 row_reduction_audit.cpp -o row_reduction_audit_cpp && ./row_reduction_audit_cpp > ../outputs/tables/cpp_row_reduction_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f row_reduction_audit_cpp
