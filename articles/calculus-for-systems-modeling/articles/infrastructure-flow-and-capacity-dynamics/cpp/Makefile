.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 infrastructure_flow_capacity.cpp -o infrastructure_flow_capacity; mkdir -p ../outputs/tables; ./infrastructure_flow_capacity > ../outputs/tables/cpp_infrastructure_scenarios.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f infrastructure_flow_capacity
