.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 stokes_theorem_audit.cpp -o stokes_theorem_audit; mkdir -p ../outputs/tables; ./stokes_theorem_audit > ../outputs/tables/cpp_stokes_theorem_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f stokes_theorem_audit
