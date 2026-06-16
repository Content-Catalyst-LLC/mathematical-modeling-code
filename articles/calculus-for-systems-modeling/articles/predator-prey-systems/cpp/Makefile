.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 predator_prey_systems.cpp -o predator_prey_systems; mkdir -p ../outputs/tables; ./predator_prey_systems > ../outputs/tables/cpp_predator_prey_scenarios.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f predator_prey_systems
