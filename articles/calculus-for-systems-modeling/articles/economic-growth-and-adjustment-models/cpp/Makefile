.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 economic_growth_adjustment.cpp -o economic_growth_adjustment; mkdir -p ../outputs/tables; ./economic_growth_adjustment > ../outputs/tables/cpp_economic_growth_scenarios.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f economic_growth_adjustment
