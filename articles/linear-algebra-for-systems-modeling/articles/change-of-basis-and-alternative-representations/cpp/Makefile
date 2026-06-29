.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 change_of_basis_audit.cpp -o change_of_basis_audit_cpp && ./change_of_basis_audit_cpp > ../outputs/tables/cpp_change_of_basis_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f change_of_basis_audit_cpp
