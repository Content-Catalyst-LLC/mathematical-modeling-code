.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 second_derivative_audit.cpp -o second_derivative_audit; mkdir -p ../outputs/tables; ./second_derivative_audit > ../outputs/tables/cpp_second_derivative_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f second_derivative_audit
