.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 incidence_structure_audit.cpp -o incidence_structure_audit_cpp && ./incidence_structure_audit_cpp > ../outputs/tables/cpp_incidence_structure_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f incidence_structure_audit_cpp
