.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 flow_to_stock_audit.cpp -o flow_to_stock_audit; mkdir -p ../outputs/tables; ./flow_to_stock_audit > ../outputs/tables/cpp_flow_to_stock_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f flow_to_stock_audit
