.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 sensitivity_robustness_parameter_dependence.cpp -o sensitivity_robustness_parameter_dependence; mkdir -p ../outputs/tables; ./sensitivity_robustness_parameter_dependence > ../outputs/tables/cpp_sensitivity_records.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f sensitivity_robustness_parameter_dependence
