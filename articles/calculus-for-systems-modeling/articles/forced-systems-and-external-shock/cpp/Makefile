.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 forced_system_shock_audit.cpp -o forced_system_shock_audit; mkdir -p ../outputs/tables; ./forced_system_shock_audit > ../outputs/tables/cpp_forced_system_shock_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f forced_system_shock_audit
