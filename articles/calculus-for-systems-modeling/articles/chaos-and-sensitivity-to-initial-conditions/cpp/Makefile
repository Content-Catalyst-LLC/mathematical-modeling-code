.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 chaos_sensitivity_audit.cpp -o chaos_sensitivity_audit; mkdir -p ../outputs/tables; ./chaos_sensitivity_audit > ../outputs/tables/cpp_chaos_sensitivity_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f chaos_sensitivity_audit
