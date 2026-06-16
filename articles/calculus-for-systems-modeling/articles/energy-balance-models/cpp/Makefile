.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 energy_balance_models.cpp -o energy_balance_models; mkdir -p ../outputs/tables; ./energy_balance_models > ../outputs/tables/cpp_energy_balance_scenarios.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f energy_balance_models
