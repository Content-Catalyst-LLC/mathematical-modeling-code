.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 partial_derivative_audit.cpp -o partial_derivative_audit; mkdir -p ../outputs/tables; ./partial_derivative_audit > ../outputs/tables/cpp_partial_derivative_interaction_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f partial_derivative_audit
