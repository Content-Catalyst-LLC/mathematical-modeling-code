.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 model_calibration_calculus.cpp -o model_calibration_calculus; mkdir -p ../outputs/tables; ./model_calibration_calculus > ../outputs/tables/cpp_calibration_candidates.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f model_calibration_calculus
