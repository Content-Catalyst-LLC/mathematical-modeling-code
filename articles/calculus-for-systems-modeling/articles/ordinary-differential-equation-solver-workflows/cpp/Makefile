.PHONY: run clean

run:
	@if command -v c++ >/dev/null 2>&1; then c++ -O2 -std=c++17 ode_solver_audit.cpp -o ode_solver_audit; mkdir -p ../outputs/tables; ./ode_solver_audit > ../outputs/tables/cpp_ode_solver_audit.csv; else echo "c++ compiler not found; skipping."; fi

clean:
	rm -f ode_solver_audit
