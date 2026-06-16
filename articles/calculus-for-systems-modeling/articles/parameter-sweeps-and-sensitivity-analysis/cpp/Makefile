.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 parameter_sweeps_sensitivity.cpp -o parameter_sweeps_sensitivity; mkdir -p ../outputs/tables; ./parameter_sweeps_sensitivity > ../outputs/tables/cpp_parameter_sweep_grid.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f parameter_sweeps_sensitivity
