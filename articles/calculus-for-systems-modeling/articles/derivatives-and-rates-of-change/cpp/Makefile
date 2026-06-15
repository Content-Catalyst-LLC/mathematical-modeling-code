.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 rate_diagnostics.cpp -o rate_diagnostics; mkdir -p ../outputs/tables; ./rate_diagnostics > ../outputs/tables/cpp_rate_diagnostics.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f rate_diagnostics
