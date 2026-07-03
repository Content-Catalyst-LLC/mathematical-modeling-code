.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 ml_linear_algebra_audit.cpp -o ml_linear_algebra_audit_cpp && ./ml_linear_algebra_audit_cpp > ../outputs/tables/cpp_ml_linear_algebra_audit.csv; else echo "c++ not found; skipping C++."; fi

clean:
	rm -f ml_linear_algebra_audit_cpp
