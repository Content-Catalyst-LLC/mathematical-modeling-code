.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 elasticity_sensitivity_audit.cpp -o elasticity_sensitivity_audit; mkdir -p ../outputs/tables; ./elasticity_sensitivity_audit > ../outputs/tables/cpp_elasticity_sensitivity_audit.csv; else echo "c++ compiler not found; skipping C++ workflow."; fi

clean:
	rm -f elasticity_sensitivity_audit
