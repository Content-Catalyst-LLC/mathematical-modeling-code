.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 total_differential_audit.cpp -o total_differential_audit; mkdir -p ../outputs/tables; ./total_differential_audit > ../outputs/tables/cpp_total_differential_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f total_differential_audit
