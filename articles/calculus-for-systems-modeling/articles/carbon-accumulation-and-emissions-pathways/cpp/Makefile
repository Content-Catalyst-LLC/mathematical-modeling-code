.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 carbon_accumulation_pathways.cpp -o carbon_accumulation_pathways; mkdir -p ../outputs/tables; ./carbon_accumulation_pathways > ../outputs/tables/cpp_carbon_pathway_scenarios.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f carbon_accumulation_pathways
