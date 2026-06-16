.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 climate_feedback_models.cpp -o climate_feedback_models; mkdir -p ../outputs/tables; ./climate_feedback_models > ../outputs/tables/cpp_climate_feedback_scenarios.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f climate_feedback_models
