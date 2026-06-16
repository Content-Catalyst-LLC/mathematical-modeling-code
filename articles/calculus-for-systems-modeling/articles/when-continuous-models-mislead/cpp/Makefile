.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 when_continuous_models_mislead.cpp -o when_continuous_models_mislead; mkdir -p ../outputs/tables; ./when_continuous_models_mislead > ../outputs/tables/cpp_continuous_model_risk_records.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f when_continuous_models_mislead
