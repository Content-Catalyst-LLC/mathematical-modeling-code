.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 bifurcation_audit.cpp -o bifurcation_audit; mkdir -p ../outputs/tables; ./bifurcation_audit > ../outputs/tables/cpp_bifurcation_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f bifurcation_audit
