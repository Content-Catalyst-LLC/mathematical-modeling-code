.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 pivot_structure_audit.cpp -o pivot_structure_audit_cpp && ./pivot_structure_audit_cpp > ../outputs/tables/cpp_pivot_structure_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f pivot_structure_audit_cpp
