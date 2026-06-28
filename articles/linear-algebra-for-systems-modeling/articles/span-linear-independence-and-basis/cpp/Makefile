.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 span_basis_audit.cpp -o span_basis_audit_cpp && ./span_basis_audit_cpp > ../outputs/tables/cpp_span_basis_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f span_basis_audit_cpp
