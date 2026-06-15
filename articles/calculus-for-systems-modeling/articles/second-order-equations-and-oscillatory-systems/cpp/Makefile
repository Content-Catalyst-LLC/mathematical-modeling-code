.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 second_order_oscillation_audit.cpp -o second_order_oscillation_audit; mkdir -p ../outputs/tables; ./second_order_oscillation_audit > ../outputs/tables/cpp_second_order_oscillation_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f second_order_oscillation_audit
