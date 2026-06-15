.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 divergence_theorem_audit.cpp -o divergence_theorem_audit; mkdir -p ../outputs/tables; ./divergence_theorem_audit > ../outputs/tables/cpp_divergence_theorem_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f divergence_theorem_audit
