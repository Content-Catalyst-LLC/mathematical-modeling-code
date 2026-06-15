.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 structural_derivative_audit.cpp -o structural_derivative_audit; mkdir -p ../outputs/tables; ./structural_derivative_audit > ../outputs/tables/cpp_structural_derivative_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f structural_derivative_audit
