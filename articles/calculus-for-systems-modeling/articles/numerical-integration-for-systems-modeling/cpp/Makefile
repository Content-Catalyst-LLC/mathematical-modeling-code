.PHONY: run clean
run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 numerical_integration_audit.cpp -o numerical_integration_audit; mkdir -p ../outputs/tables; ./numerical_integration_audit > ../outputs/tables/cpp_numerical_integration_audit.csv; else echo "c++ compiler not found; skipping."; fi
clean:
	rm -f numerical_integration_audit
