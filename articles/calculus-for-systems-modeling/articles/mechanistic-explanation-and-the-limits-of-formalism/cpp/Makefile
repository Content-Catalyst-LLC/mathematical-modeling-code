.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 mechanistic_explanation_limits_formalism.cpp -o mechanistic_explanation_limits_formalism; mkdir -p ../outputs/tables; ./mechanistic_explanation_limits_formalism > ../outputs/tables/cpp_mechanism_records.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f mechanistic_explanation_limits_formalism
