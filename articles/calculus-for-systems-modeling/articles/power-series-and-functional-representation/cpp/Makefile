.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 power_series_audit.cpp -o power_series_audit; mkdir -p ../outputs/tables; ./power_series_audit > ../outputs/tables/cpp_power_series_approximation_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f power_series_audit
