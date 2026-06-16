.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 numerical_differentiation_audit.cpp -o numerical_differentiation_audit; mkdir -p ../outputs/tables; ./numerical_differentiation_audit > ../outputs/tables/cpp_numerical_differentiation_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f numerical_differentiation_audit
