.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 coupled_system_audit.cpp -o coupled_system_audit; mkdir -p ../outputs/tables; ./coupled_system_audit > ../outputs/tables/cpp_coupled_system_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f coupled_system_audit
