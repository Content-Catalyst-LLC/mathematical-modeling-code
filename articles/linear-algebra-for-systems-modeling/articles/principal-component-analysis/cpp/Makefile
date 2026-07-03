.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 pca_diagnostic_audit.cpp -o pca_diagnostic_audit_cpp && ./pca_diagnostic_audit_cpp > ../outputs/tables/cpp_pca_diagnostic_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f pca_diagnostic_audit_cpp
