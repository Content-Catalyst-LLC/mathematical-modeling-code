.PHONY: run clean
run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 coupled_human_natural_systems.cpp -o coupled_human_natural_systems; mkdir -p ../outputs/tables; ./coupled_human_natural_systems > ../outputs/tables/cpp_coupled_system_scenarios.csv; else echo "c++ compiler not found; skipping."; fi
clean:
	rm -f coupled_human_natural_systems
