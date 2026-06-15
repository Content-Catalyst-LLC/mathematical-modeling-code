.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 sequence_series_convergence_audit.cpp -o sequence_series_convergence_audit; mkdir -p ../outputs/tables; ./sequence_series_convergence_audit > ../outputs/tables/cpp_sequence_series_convergence_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f sequence_series_convergence_audit
