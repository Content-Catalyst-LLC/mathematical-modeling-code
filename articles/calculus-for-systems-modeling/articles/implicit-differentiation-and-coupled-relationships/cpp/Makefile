.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 implicit_sensitivity_audit.cpp -o implicit_sensitivity_audit; mkdir -p ../outputs/tables; ./implicit_sensitivity_audit > ../outputs/tables/cpp_implicit_sensitivity_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f implicit_sensitivity_audit
