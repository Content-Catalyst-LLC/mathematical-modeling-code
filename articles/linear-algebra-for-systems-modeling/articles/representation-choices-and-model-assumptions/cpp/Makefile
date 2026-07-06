.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 representation_assumption_audit.cpp -o representation_assumption_audit_cpp && ./representation_assumption_audit_cpp > ../outputs/tables/cpp_representation_assumption_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f representation_assumption_audit_cpp
