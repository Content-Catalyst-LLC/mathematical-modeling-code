.PHONY: run clean
run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 modeling_population_dynamics.cpp -o modeling_population_dynamics; mkdir -p ../outputs/tables; ./modeling_population_dynamics > ../outputs/tables/cpp_population_growth_scenarios.csv; else echo "c++ compiler not found; skipping."; fi
clean:
	rm -f modeling_population_dynamics
