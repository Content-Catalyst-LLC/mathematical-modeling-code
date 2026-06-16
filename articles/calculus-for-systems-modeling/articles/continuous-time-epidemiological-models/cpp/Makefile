.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 continuous_time_epidemiology.cpp -o continuous_time_epidemiology; mkdir -p ../outputs/tables; ./continuous_time_epidemiology > ../outputs/tables/cpp_epidemiological_scenarios.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f continuous_time_epidemiology
