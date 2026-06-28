.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 solution_space_audit.cpp -o solution_space_audit_cpp && ./solution_space_audit_cpp > ../outputs/tables/cpp_solution_space_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f solution_space_audit_cpp
