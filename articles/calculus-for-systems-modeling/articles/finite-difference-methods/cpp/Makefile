.PHONY: run clean
run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 finite_difference_audit.cpp -o finite_difference_audit; mkdir -p ../outputs/tables; ./finite_difference_audit > ../outputs/tables/cpp_finite_difference_audit.csv; else echo "c++ compiler not found; skipping."; fi
clean:
	rm -f finite_difference_audit
