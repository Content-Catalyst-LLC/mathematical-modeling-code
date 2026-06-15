.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 related_rates_audit.cpp -o related_rates_audit; mkdir -p ../outputs/tables; ./related_rates_audit > ../outputs/tables/cpp_related_rates_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f related_rates_audit
