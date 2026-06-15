.PHONY: run clean
run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 separable_equation_audit.cpp -o separable_equation_audit; mkdir -p ../outputs/tables; ./separable_equation_audit > ../outputs/tables/cpp_separable_equation_audit.csv; else echo "c++ compiler not found; skipping."; fi
clean:
	rm -f separable_equation_audit
