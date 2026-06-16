.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 euler_method_audit.cpp -o euler_method_audit; mkdir -p ../outputs/tables; ./euler_method_audit > ../outputs/tables/cpp_euler_method_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f euler_method_audit
