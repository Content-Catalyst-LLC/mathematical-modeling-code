.PHONY: run clean
run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 urban_dynamics_congestion.cpp -o urban_dynamics_congestion; mkdir -p ../outputs/tables; ./urban_dynamics_congestion > ../outputs/tables/cpp_urban_congestion_scenarios.csv; else echo "c++ compiler not found; skipping."; fi
clean:
	rm -f urban_dynamics_congestion
