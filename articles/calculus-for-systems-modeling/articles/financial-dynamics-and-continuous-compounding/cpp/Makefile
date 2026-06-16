.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 financial_dynamics_compounding.cpp -o financial_dynamics_compounding; mkdir -p ../outputs/tables; ./financial_dynamics_compounding > ../outputs/tables/cpp_financial_scenarios.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f financial_dynamics_compounding
