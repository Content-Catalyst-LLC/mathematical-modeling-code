.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 svd_diagnostic_audit.cpp -o svd_diagnostic_audit_cpp && ./svd_diagnostic_audit_cpp > ../outputs/tables/cpp_svd_diagnostic_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f svd_diagnostic_audit_cpp
