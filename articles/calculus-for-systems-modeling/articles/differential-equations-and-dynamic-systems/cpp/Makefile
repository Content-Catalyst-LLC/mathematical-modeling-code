.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 dynamic_system_audit.cpp -o dynamic_system_audit; mkdir -p ../outputs/tables; ./dynamic_system_audit > ../outputs/tables/cpp_dynamic_system_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f dynamic_system_audit
