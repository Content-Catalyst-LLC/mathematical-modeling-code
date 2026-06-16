.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 resource_depletion_regeneration.cpp -o resource_depletion_regeneration; mkdir -p ../outputs/tables; ./resource_depletion_regeneration > ../outputs/tables/cpp_resource_scenarios.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f resource_depletion_regeneration
