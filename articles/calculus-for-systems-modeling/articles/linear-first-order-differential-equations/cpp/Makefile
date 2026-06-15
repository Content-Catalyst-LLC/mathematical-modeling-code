.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 linear_first_order_audit.cpp -o linear_first_order_audit; mkdir -p ../outputs/tables; ./linear_first_order_audit > ../outputs/tables/cpp_linear_first_order_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f linear_first_order_audit
