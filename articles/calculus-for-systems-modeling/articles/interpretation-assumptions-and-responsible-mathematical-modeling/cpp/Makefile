.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 interpretation_assumptions_responsible_modeling.cpp -o interpretation_assumptions_responsible_modeling; mkdir -p ../outputs/tables; ./interpretation_assumptions_responsible_modeling > ../outputs/tables/cpp_responsible_modeling_records.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f interpretation_assumptions_responsible_modeling
