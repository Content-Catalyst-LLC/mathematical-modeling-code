.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 line_integral_audit.cpp -o line_integral_audit; mkdir -p ../outputs/tables; ./line_integral_audit > ../outputs/tables/cpp_line_integral_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f line_integral_audit
