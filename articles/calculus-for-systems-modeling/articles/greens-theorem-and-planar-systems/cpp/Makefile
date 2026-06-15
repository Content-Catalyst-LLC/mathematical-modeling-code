.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 greens_theorem_audit.cpp -o greens_theorem_audit; mkdir -p ../outputs/tables; ./greens_theorem_audit > ../outputs/tables/cpp_greens_theorem_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f greens_theorem_audit
