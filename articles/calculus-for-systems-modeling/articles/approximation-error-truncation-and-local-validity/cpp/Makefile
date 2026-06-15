.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 approximation_error_audit.cpp -o approximation_error_audit; mkdir -p ../outputs/tables; ./approximation_error_audit > ../outputs/tables/cpp_approximation_error_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f approximation_error_audit
