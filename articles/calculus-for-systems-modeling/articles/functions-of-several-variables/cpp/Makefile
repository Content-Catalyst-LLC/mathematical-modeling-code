.PHONY: run clean
run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 multivariable_function_audit.cpp -o multivariable_function_audit; mkdir -p ../outputs/tables; ./multivariable_function_audit > ../outputs/tables/cpp_multivariable_function_grid.csv; else echo "c++ compiler not found; skipping."; fi
clean:
	rm -f multivariable_function_audit
