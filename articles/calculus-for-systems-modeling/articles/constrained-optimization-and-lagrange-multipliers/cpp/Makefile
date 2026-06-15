.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 constrained_optimization_audit.cpp -o constrained_optimization_audit; mkdir -p ../outputs/tables; ./constrained_optimization_audit > ../outputs/tables/cpp_constrained_optimization_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f constrained_optimization_audit
