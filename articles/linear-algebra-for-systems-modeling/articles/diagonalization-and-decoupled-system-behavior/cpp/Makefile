.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 diagonalization_audit.cpp -o diagonalization_audit_cpp && ./diagonalization_audit_cpp > ../outputs/tables/cpp_diagonalization_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f diagonalization_audit_cpp
